#!/usr/bin/env python3
"""Recompute topic representations for an already-compared BO call with the
current (cleaned) custom stoplist.

Why: Phase 2 compare-fit runs did not save BERTopic artifacts, and the
safetensors format would not carry per-document assignments anyway. Clustering
is embedding-driven (UMAP + HDBSCAN never see the stoplist), so refitting with
the same ``umap_random_state`` used for the original export reproduces the
same topic structure while the c-TF-IDF / KeyBERT / MMR / POS keyword layer is
rebuilt against the cleaned stoplist.

Outputs go to ``final_compare/call_N/<out-subdir>/`` (default
``repr_stoplist_v2``) next to the original export, which is left untouched:
topic_info.csv, top_words.csv, representative_docs.csv, posthoc artifacts and
metrics.json (with the original metrics inlined for delta reporting).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from gensim.corpora import Dictionary

from src.common.config import load_config, resolve_path
from src.stage03_train.corpus_store import (
    CorpusDocStore,
    corpus_metadata_path,
    corpus_offsets_path,
)
from src.stage03_train.tune import _build_paths, _prepare_bertopic_fit_data
from src.stage05_final_fit.compare_fit import (
    LOGGER,
    _compute_fit_metrics,
    _fit_bertopic,
    _jsonable,
    _read_calculate_probabilities,
    _read_trial_hyperparameters,
    _write_posthoc_for_dir,
    _write_topic_tables,
    setup_compare_logging,
    stage_timer,
)
from src.legacy.stage03_modeling.bertopic_octis_model import (
    BERTopicOctisModelWithEmbeddings,
    load_embedding_model,
)
from src.legacy.stage03_modeling.memory_utils import cleanup_gpu_memory

MIN_WORDS_FIT = 4  # must match compare_fit's short-doc filter


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=Path, required=True)
    parser.add_argument("--bo-call", type=int, required=True)
    parser.add_argument("--run-id", type=str, required=True)
    parser.add_argument("--paths-config", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--umap-seed",
        type=int,
        required=True,
        help="umap_random_state of the original median-seed export (see stability.json).",
    )
    parser.add_argument("--fit-max-docs", type=int, default=500_000)
    parser.add_argument("--sample-seed", type=int, default=42, help="Fit-sample seed (compare-fit default).")
    parser.add_argument("--out-subdir", type=str, default="repr_stoplist_v2")
    return parser.parse_args()


def _stoplist_fingerprint() -> dict[str, object]:
    paths_cfg = load_config(Path("configs/paths.yaml"))
    raw = paths_cfg.get("inputs", {}).get("custom_stoplist")
    if not raw:
        return {"path": None}
    p = resolve_path(Path(raw))
    data = p.read_bytes()
    return {
        "path": str(p),
        "n_lines": sum(1 for line in data.splitlines() if line.strip()),
        "sha256": hashlib.sha256(data).hexdigest()[:16],
    }


def main() -> None:
    args = _parse_args()
    trials_csv = resolve_path(args.trials)
    paths_cfg = load_config(args.paths_config)
    train_cfg = load_config(args.config)
    paths = _build_paths(paths_cfg, args.run_id)

    logs_dir = resolve_path(Path(paths_cfg.get("outputs", {}).get("logs", "logs")))
    setup_compare_logging(logs_dir / f"stage05_repr_{args.run_id}.log")

    call_dir = paths.experiments_dir / "final_compare" / f"call_{args.bo_call}"
    if not (call_dir / "metrics.json").exists():
        raise FileNotFoundError(f"Original compare-fit export not found: {call_dir}/metrics.json")
    out_dir = call_dir / args.out_subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    original_metrics = json.loads((call_dir / "metrics.json").read_text(encoding="utf-8"))
    stoplist_info = _stoplist_fingerprint()
    LOGGER.info(
        "Repr recompute: run=%s call=%d umap_seed=%d stoplist=%s (%s lines)",
        args.run_id,
        args.bo_call,
        args.umap_seed,
        stoplist_info.get("path"),
        stoplist_info.get("n_lines"),
    )

    inputs_cfg = paths_cfg.get("inputs", {})
    corpus_dir_override = inputs_cfg.get("octis_corpus_dir")
    corpus_root = (
        resolve_path(Path(corpus_dir_override)) if corpus_dir_override else paths.octis_dir
    )
    doc_store = CorpusDocStore(corpus_root / "corpus.tsv", corpus_offsets_path(corpus_root))
    n_docs_total = len(doc_store)
    n_train_docs = n_docs_total
    meta_path = corpus_metadata_path(corpus_root)
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        n_train_docs = int(meta.get("last-training-doc", n_docs_total))

    flat_hp, reported = _read_trial_hyperparameters(trials_csv, args.bo_call)
    embedding_model_name = reported.get("embedding_model")
    overrides = (train_cfg.get("embeddings_cache", {}) or {}).get("overrides", {}) or {}
    cache_file = resolve_path(Path(overrides[embedding_model_name]))
    embeddings_mmap = np.load(cache_file, mmap_mode="r")
    LOGGER.info("Embeddings cache (mmap): %s", cache_file)

    fit_indices_cfg = inputs_cfg.get("fit_indices_file")
    fit_indices_path = resolve_path(Path(fit_indices_cfg)) if fit_indices_cfg else None
    eval_indices_cfg = inputs_cfg.get("eval_indices_file")
    eval_indices_path = resolve_path(Path(eval_indices_cfg)) if eval_indices_cfg else None

    with stage_timer("load fit sample (docs + embeddings)"):
        fit_docs, fit_embeddings, _ = _prepare_bertopic_fit_data(
            doc_store,
            embeddings_mmap,
            fit_max_docs=args.fit_max_docs,
            seed=args.sample_seed,
            logger=LOGGER,
            n_train=n_train_docs,
            fit_indices_path=fit_indices_path,
        )
    keep_mask = np.array([len(d.split()) >= MIN_WORDS_FIT for d in fit_docs])
    fit_docs = [d for d, keep in zip(fit_docs, keep_mask) if keep]
    fit_embeddings = fit_embeddings[keep_mask]
    LOGGER.info("Fit docs after short-doc filter: %d", len(fit_docs))

    fit_dictionary = Dictionary(d.split() for d in fit_docs)

    with stage_timer("load stratified eval tokens"):
        eval_idx = np.asarray(np.load(eval_indices_path), dtype=np.int64)
        in_val = eval_idx[(eval_idx >= n_train_docs) & (eval_idx < n_docs_total)]
        eval_docs = doc_store.fetch_documents(np.unique(in_val))
        tokens_eval = [d.split() for d in eval_docs if d]
        eval_dictionary = Dictionary(tokens_eval)
    LOGGER.info("Coherence eval tokens: %d docs", len(tokens_eval))

    embedding_model = load_embedding_model(embedding_model_name)
    wrapper = BERTopicOctisModelWithEmbeddings(
        embedding_model=embedding_model,
        embedding_model_name=embedding_model_name,
        embeddings=fit_embeddings,
        dataset_as_list_of_strings=fit_docs,
        dataset_as_list_of_lists=None,
        verbose=False,
        calculate_probabilities=_read_calculate_probabilities(train_cfg),
        topic_filter_dictionary=fit_dictionary,
    )

    start = time.perf_counter()
    with stage_timer(f"call_{args.bo_call} BERTopic refit (cleaned stoplist)"):
        topic_model = _fit_bertopic(
            wrapper,
            flat_hp,
            fit_docs,
            fit_embeddings,
            umap_random_state=args.umap_seed,
        )

    with stage_timer(f"call_{args.bo_call} metrics + topic tables"):
        fit_metrics = _compute_fit_metrics(
            topic_model, fit_dictionary, tokens_eval, eval_dictionary
        )
        _write_topic_tables(topic_model, out_dir)
        _write_posthoc_for_dir(out_dir)

    metrics = {
        "run_id": args.run_id,
        "bo_call": args.bo_call,
        "embedding_model": embedding_model_name,
        **{k: v for k, v in fit_metrics.items()},
        "umap_random_state": args.umap_seed,
        "stoplist": stoplist_info,
        "elapsed_s": round(time.perf_counter() - start, 1),
        "recomputed_at": datetime.now(timezone.utc).isoformat(),
        "original": {
            "n_topics": original_metrics.get("n_topics"),
            "coherence_c_v": original_metrics.get("coherence_c_v"),
            "topic_diversity": original_metrics.get("topic_diversity"),
            "outlier_rate": original_metrics.get("outlier_rate"),
        },
        "hyperparameters": _jsonable(flat_hp),
    }
    with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(_jsonable(metrics), f, indent=2)
    LOGGER.info(
        "Recompute done: n_topics=%d (orig %s) coherence=%.4f (orig %.4f) -> %s",
        int(fit_metrics["n_topics"]),
        original_metrics.get("n_topics"),
        fit_metrics["coherence_c_v"],
        float(original_metrics.get("coherence_c_v") or 0.0),
        out_dir,
    )

    del topic_model
    cleanup_gpu_memory(verbose=False)


if __name__ == "__main__":
    main()
