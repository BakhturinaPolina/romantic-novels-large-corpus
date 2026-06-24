#!/usr/bin/env python3
"""Pilot: BERTopic on 5-sentence windows from the stratified 500k fit sample.

Compares window-level clustering vs the sentence-level baseline (same hyperparameters,
same stratified indices, one embedding model).

Outputs timing breakdown + metrics under results/experiments/<out_name>/.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch

from src.legacy.stage03_modeling.bertopic_octis_model import (
    BERTopicWithSafeVectorizer,
    SafeClassTfidfTransformer,
    create_representation_models,
    load_custom_stopwords_from_config,
    load_embedding_model,
)
from src.stage03_train.corpus_store import CorpusDocStore, corpus_offsets_path
from src.stage03_train.tune import _safe_outlier_rate_from_topics
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP
from bertopic.vectorizers import ClassTfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

# v3_minilm12v2_first call_3 (sentence baseline: 45 topics, ~72.6% outliers in logs)
DEFAULT_FLAT_HP: dict[str, Any] = {
    "bertopic__min_topic_size": 450,
    "bertopic__top_n_words": 37,
    "hdbscan__min_cluster_size": 731,
    "hdbscan__min_samples": 27,
    "umap__min_dist": 0.050865749113900974,
    "umap__n_components": 6,
    "umap__n_neighbors": 14,
    "vectorizer__min_df": 0.006033790375808364,
}

LOGGER = logging.getLogger("window_pilot")


def _fetch_text_and_work_id(doc_store: CorpusDocStore, index: int) -> tuple[str, str]:
    offsets = doc_store._offsets
    start = int(offsets[index])
    end = int(offsets[index + 1])
    with open(doc_store.corpus_path, "rb") as f:
        f.seek(start)
        raw = f.read(end - start).decode("utf-8")
    parts = raw.split("\t")
    text = parts[0]
    work_id = parts[-1].strip() if len(parts) >= 3 else "unknown"
    return text, work_id


def build_windows_from_fit_indices(
    doc_store: CorpusDocStore,
    fit_indices: np.ndarray,
    *,
    window_size: int = 5,
    max_windows: int | None = None,
) -> tuple[list[str], list[list[int]], dict[str, Any]]:
    """Group stratified sentence indices into within-book non-overlapping windows."""
    t0 = time.perf_counter()
    by_work: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for idx in fit_indices:
        text, work_id = _fetch_text_and_work_id(doc_store, int(idx))
        if text.strip():
            by_work[work_id].append((int(idx), text))

    window_docs: list[str] = []
    window_sentence_indices: list[list[int]] = []
    books_used = 0
    dropped_tail_sentences = 0

    for work_id in sorted(by_work.keys()):
        items = sorted(by_work[work_id], key=lambda x: x[0])
        n_full = (len(items) // window_size) * window_size
        dropped_tail_sentences += len(items) - n_full
        if n_full == 0:
            continue
        books_used += 1
        for start in range(0, n_full, window_size):
            chunk = items[start : start + window_size]
            window_docs.append(" ".join(text for _, text in chunk))
            window_sentence_indices.append([idx for idx, _ in chunk])
            if max_windows is not None and len(window_docs) >= max_windows:
                break
        if max_windows is not None and len(window_docs) >= max_windows:
            break

    stats = {
        "n_fit_sentences": int(len(fit_indices)),
        "n_books_with_windows": int(books_used),
        "n_windows": int(len(window_docs)),
        "window_size": int(window_size),
        "dropped_tail_sentences": int(dropped_tail_sentences),
        "avg_sentences_per_window": float(window_size),
        "build_seconds": round(time.perf_counter() - t0, 2),
    }
    return window_docs, window_sentence_indices, stats


def encode_windows(
    docs: list[str],
    model_name: str,
    *,
    batch_size: int = 256,
    device: str = "auto",
) -> tuple[np.ndarray, float]:
    t0 = time.perf_counter()
    resolved = "cuda" if device == "auto" and torch.cuda.is_available() else device
    model = load_embedding_model(model_name, device=resolved)
    embeddings = model.encode(
        docs,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=False,
    )
    elapsed = time.perf_counter() - t0
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return np.asarray(embeddings, dtype=np.float32), elapsed


def _nested_hp(flat: dict[str, Any]) -> dict[str, Any]:
    """Expand flat section__param dict into nested BERTopic config."""
    defaults: dict[str, Any] = {
        "umap": {
            "n_neighbors": 11,
            "n_components": 5,
            "min_dist": 0.05,
            "metric": "cosine",
            "random_state": 42,
        },
        "hdbscan": {
            "min_cluster_size": 150,
            "metric": "euclidean",
            "cluster_selection_method": "eom",
            "prediction_data": True,
            "gen_min_span_tree": True,
            "min_samples": 20,
        },
        "vectorizer": {
            "stop_words": "english",
            "min_df": 0.005,
            "ngram_range": (1, 1),
        },
        "tfdf_vectorizer": {"reduce_frequent_words": True, "bm25_weighting": True},
        "bertopic": {
            "language": "english",
            "top_n_words": 30,
            "n_gram_range": (1, 1),
            "min_topic_size": 127,
            "nr_topics": None,
            "low_memory": False,
            "calculate_probabilities": False,
            "verbose": True,
        },
    }
    for key, value in flat.items():
        if "__" not in key:
            continue
        section, param = key.split("__", 1)
        if section in defaults and param in defaults[section]:
            defaults[section][param] = value
    return defaults


def fit_bertopic_on_windows(
    docs: list[str],
    embeddings: np.ndarray,
    flat_hp: dict[str, Any],
    embedding_model_name: str,
    *,
    use_representation: bool = True,
) -> tuple[Any, dict[str, Any]]:
    t0 = time.perf_counter()
    hp = _nested_hp(flat_hp)
    if "bertopic__verbose" in flat_hp:
        hp["bertopic"]["verbose"] = bool(flat_hp["bertopic__verbose"])

    umap_model = UMAP(**hp["umap"])
    hdbscan_model = HDBSCAN(**hp["hdbscan"])

    vectorizer_params = dict(hp["vectorizer"])
    custom_stopwords = load_custom_stopwords_from_config(verbose=False)
    merged = sorted(set(ENGLISH_STOP_WORDS).union(custom_stopwords))
    vectorizer_params["stop_words"] = merged
    orig_min_df = vectorizer_params.get("min_df", 1)
    if isinstance(orig_min_df, float) and orig_min_df < 1.0:
        vectorizer_params["min_df"] = 5
    if "token_pattern" not in vectorizer_params:
        vectorizer_params["token_pattern"] = r"(?u)\b[a-zA-Z]{2,}\b"

    topic_model = BERTopicWithSafeVectorizer(
        embedding_model=embedding_model_name,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=CountVectorizer(**vectorizer_params),
        ctfidf_model=SafeClassTfidfTransformer(**hp["tfdf_vectorizer"]),
        representation_model=create_representation_models() if use_representation else None,
        **hp["bertopic"],
    )

    topics = topic_model.fit_transform(docs, embeddings=embeddings)
    topic_arr = np.asarray(topics[0] if isinstance(topics, tuple) else topics)
    outlier_rate = _safe_outlier_rate_from_topics(topic_arr)
    n_topics = len(set(topic_arr.tolist())) - (1 if -1 in topic_arr.tolist() else 0)

    info = topic_model.get_topic_info()
    top5 = info[info["Topic"] != -1].nlargest(5, "Count")
    top5_rows = []
    for _, row in top5.iterrows():
        tid = int(row["Topic"])
        pairs = topic_model.get_topic(tid)
        words = [w for w, _ in (pairs or [])[:8] if w]
        top5_rows.append(
            {"topic": tid, "count": int(row["Count"]), "words": words}
        )

    elapsed = time.perf_counter() - t0
    metrics = {
        "n_docs": len(docs),
        "n_topics": int(n_topics),
        "outlier_rate": float(outlier_rate),
        "outlier_pct": round(100.0 * outlier_rate, 2),
        "fit_seconds": round(elapsed, 2),
        "top5_topics": top5_rows,
    }
    return topic_model, metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fit-indices",
        default="data/stage03_samples_v3/fit_indices_seed42.npy",
        type=Path,
    )
    parser.add_argument(
        "--octis-dir",
        default="data/interim/octis/v3_english_only",
        type=Path,
    )
    parser.add_argument(
        "--out-dir",
        default="results/experiments/window_pilot_minilm12_seed42",
        type=Path,
    )
    parser.add_argument("--window-size", default=5, type=int)
    parser.add_argument("--max-windows", default=None, type=int)
    parser.add_argument(
        "--embedding-model",
        default="sentence-transformers/all-MiniLM-L12-v2",
    )
    parser.add_argument("--batch-size", default=256, type=int)
    parser.add_argument("--skip-fit", action="store_true")
    parser.add_argument("--skip-build", action="store_true", help="Reuse cached windows npz.")
    parser.add_argument("--skip-encode", action="store_true", help="Reuse window_embeddings.npy.")
    parser.add_argument(
        "--hyperparams-json",
        default=None,
        type=Path,
        help="Optional JSON file with flat section__param hyperparameters.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    fit_indices = np.load(args.fit_indices)
    octis_dir = args.octis_dir
    doc_store = CorpusDocStore(
        octis_dir / "corpus.tsv",
        corpus_offsets_path(octis_dir),
    )

    flat_hp = dict(DEFAULT_FLAT_HP)
    if args.hyperparams_json and args.hyperparams_json.exists():
        flat_hp.update(json.loads(args.hyperparams_json.read_text(encoding="utf-8")))

    cache_npz = out_dir / f"windows_w{args.window_size}.npz"
    embed_path = out_dir / "window_embeddings.npy"

    if args.skip_build and cache_npz.exists():
        cached = np.load(cache_npz, allow_pickle=True)
        window_docs = cached["docs"].tolist()
        window_idx = cached["sentence_indices"].tolist()
        build_stats = {
            "n_fit_sentences": int(len(fit_indices)),
            "n_windows": int(len(window_docs)),
            "window_size": int(args.window_size),
            "build_seconds": 0.0,
            "reused_cache": str(cache_npz),
        }
        LOGGER.info("Reusing cached windows: %s (%d docs)", cache_npz, len(window_docs))
    else:
        LOGGER.info(
            "Building %d-sentence windows from %d stratified indices...",
            args.window_size,
            len(fit_indices),
        )
        window_docs, window_idx, build_stats = build_windows_from_fit_indices(
            doc_store,
            fit_indices,
            window_size=args.window_size,
            max_windows=args.max_windows,
        )
        LOGGER.info("Built %d windows in %.1fs", build_stats["n_windows"], build_stats["build_seconds"])
        np.savez_compressed(
            cache_npz,
            docs=np.array(window_docs, dtype=object),
            sentence_indices=np.array(window_idx, dtype=object),
        )

    if args.skip_encode and embed_path.exists():
        embeddings = np.load(embed_path, mmap_mode="r")
        encode_seconds = 0.0
        build_stats["encode_seconds"] = 0.0
        build_stats["encode_reused"] = str(embed_path)
        LOGGER.info("Reusing cached embeddings: %s", embed_path)
    else:
        LOGGER.info("Encoding %d windows with %s...", len(window_docs), args.embedding_model)
        embeddings, encode_seconds = encode_windows(
            window_docs,
            args.embedding_model,
            batch_size=args.batch_size,
        )
        np.save(embed_path, embeddings)
        build_stats["encode_seconds"] = round(encode_seconds, 2)
        build_stats["encode_docs_per_sec"] = round(len(window_docs) / max(encode_seconds, 1e-6), 2)

    report: dict[str, Any] = {
        "pilot": "five_sentence_windows",
        "embedding_model": args.embedding_model,
        "flat_hyperparameters": flat_hp,
        "window_stats": build_stats,
        "sentence_baseline_reference": {
            "source": "v3_minilm12v2_first call_3 (sentence-level)",
            "n_topics": 45,
            "outlier_pct_log": 72.56,
            "coherence_c_v": 0.6467,
            "note": "Same hyperparameters; sentence fit used 432,145 docs after short-sentence filter",
        },
    }

    if not args.skip_fit:
        LOGGER.info("Fitting BERTopic on window documents...")
        _, fit_metrics = fit_bertopic_on_windows(
            window_docs,
            embeddings,
            flat_hp,
            args.embedding_model,
        )
        report["window_fit"] = fit_metrics
        total = build_stats["build_seconds"] + encode_seconds + fit_metrics["fit_seconds"]
        report["timing_summary"] = {
            "build_windows_min": round(build_stats["build_seconds"] / 60, 2),
            "encode_min": round(encode_seconds / 60, 2),
            "bertopic_fit_min": round(fit_metrics["fit_seconds"] / 60, 2),
            "total_pilot_min": round(total / 60, 2),
        }

    manifest_path = out_dir / "pilot_report.json"
    manifest_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Wrote %s", manifest_path)
    if "timing_summary" in report:
        LOGGER.info("Total pilot time: %.1f min", report["timing_summary"]["total_pilot_min"])


if __name__ == "__main__":
    main()
