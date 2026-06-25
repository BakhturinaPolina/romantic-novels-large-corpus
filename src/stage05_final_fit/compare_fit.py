"""Stage 05 compare-fit: refit top-N Stage03 BO trials for manual topic inspection.

Why this exists (and why the legacy Stage05 path is not used here):
- The v2 selection's ``train_csv`` is the full 82M-sentence corpus. cuML UMAP/HDBSCAN
  need the embedding matrix resident on the GPU; 82M x 384 x 4B ~= 126 GB cannot fit
  in 8 GB VRAM (nor host RAM). The legacy ``load_and_validate_csv`` also reads the
  whole CSV into RAM, keeps only 4-column rows with a ``Sentence`` column, and
  re-encodes from scratch -- incompatible with the 5-column / lowercase ``sentence``
  v2 CSV.
- Every BO trial was scored on the 500k stratified fit sample using the cached
  full-corpus embeddings memmap. To compare the top-N candidates apples-to-apples we
  refit each on the same sample with the same cached embeddings and GPU cuML path,
  reusing the Stage03 building blocks.

This module fits each requested BO call on the shared 500k sample and writes topic
tables + metrics per config. Optional ``save_model`` writes a BERTopic artifact for
Stage05b holdout scoring. Runs are incremental and resumable.
"""

from __future__ import annotations

import csv
import json
import logging
import shutil
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from gensim.corpora import Dictionary
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer

from bertopic import BERTopic  # noqa: F401 — re-exported type for annotations
from bertopic.vectorizers import ClassTfidfTransformer

from src.common.config import load_config, resolve_path
from src.common.topic_posthoc.rules import write_posthoc_artifacts
from src.stage03_train.corpus_store import (
    CorpusDocStore,
    corpus_metadata_path,
    corpus_offsets_path,
)
from src.stage03_train.topic_stability import (
    refit_collapse_flag,
    stability_pass,
    topic_run_stats,
)
from src.stage03_train.tune import (
    _build_paths,
    _coherence_cv,
    _diversity_adaptive,
    _prepare_bertopic_fit_data,
    _safe_outlier_rate_from_topics,
)
from src.legacy.stage03_modeling.bertopic_octis_model import (
    BERTopicOctisModelWithEmbeddings,
    BERTopicWithSafeVectorizer,
    SafeClassTfidfTransformer,
    create_representation_models,
    load_custom_stopwords_from_config,
    load_embedding_model,
)

# cuML UMAP/HDBSCAN (GPU). Imported via the model module which requires RAPIDS; we
# import directly too so the fit here mirrors the Stage03 base train_model path.
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP

LOGGER = logging.getLogger("stage05_compare_fit")

# Hyperparameter columns in trials_partial.csv use the flat ``section__param`` form
# consumed by ``set_hyperparameters``. Cast to native Python types for cuML.
_INT_PARAMS = {
    "umap__n_neighbors",
    "umap__n_components",
    "hdbscan__min_cluster_size",
    "hdbscan__min_samples",
    "bertopic__top_n_words",
    "bertopic__min_topic_size",
}
_FLOAT_PARAMS = {"umap__min_dist"}


def _coerce_vectorizer_min_df(value: Any) -> int | float:
    """v4 BO uses integer absolute min_df; legacy trials use float proportions."""
    v = float(value)
    if v >= 1.0 and v == int(v):
        return int(v)
    return v


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def setup_compare_logging(log_file: Path, *, console: bool = True) -> logging.Logger:
    """Configure timestamped logging to ``log_file`` and optionally stderr.

    When launching via ``nohup ... >> logfile``, pass ``console=False`` to avoid
    duplicate lines (FileHandler + redirected stdout writing the same file).
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = LOGGER
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    if console:
        stream = logging.StreamHandler()
        stream.setFormatter(fmt)
        logger.addHandler(stream)
    logger.propagate = False
    return logger


@contextmanager
def stage_timer(name: str):
    """Log start/elapsed for a named stage."""
    LOGGER.info("> %s | start", name)
    start = time.perf_counter()
    try:
        yield
    finally:
        LOGGER.info("< %s | done in %.1fs", name, time.perf_counter() - start)


def _read_trial_hyperparameters(
    trials_csv: Path, bo_call: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (flat hyperparameters, reported trial metrics) for a given bo_call."""
    df = pd.read_csv(trials_csv)
    if "bo_call" not in df.columns:
        raise KeyError(f"'bo_call' column missing in {trials_csv}")
    match = df[df["bo_call"] == bo_call]
    if match.empty:
        raise ValueError(f"bo_call={bo_call} not found in {trials_csv}")
    row = match.iloc[0]

    flat_hp: dict[str, Any] = {}
    for col in df.columns:
        if "__" not in col:
            continue
        value = row[col]
        if pd.isna(value):
            continue
        if col == "vectorizer__min_df":
            flat_hp[col] = _coerce_vectorizer_min_df(value)
        elif col in _INT_PARAMS:
            flat_hp[col] = int(value)
        elif col in _FLOAT_PARAMS:
            flat_hp[col] = float(value)
        else:
            flat_hp[col] = value

    reported = {
        "embedding_model": row.get("embedding_model"),
        "coherence_c_v": float(row["coherence_c_v"]) if not pd.isna(row.get("coherence_c_v")) else None,
        "topic_diversity": float(row["topic_diversity"]) if not pd.isna(row.get("topic_diversity")) else None,
        "n_topics": float(row["n_topics"]) if not pd.isna(row.get("n_topics")) else None,
    }
    return flat_hp, reported


def _fit_bertopic(
    wrapper: BERTopicOctisModelWithEmbeddings,
    flat_hp: dict[str, Any],
    fit_docs: list[str],
    fit_embeddings: np.ndarray,
    *,
    umap_random_state: int | None = None,
) -> BERTopic:
    """Fit a BERTopic model mirroring the Stage03 base ``train_model`` path.

    Reuses the wrapper's ``set_hyperparameters`` to expand the flat trial params into
    the nested config, then rebuilds the cuML UMAP/HDBSCAN + vectorizer + ctfidf +
    representation models exactly like the base wrapper, and returns the fitted
    BERTopic instance (so topic tables / representative docs are available).
    """
    hp_input = dict(flat_hp)
    if umap_random_state is not None:
        hp_input["umap__random_state"] = int(umap_random_state)
        LOGGER.info(
            "[COMPARE-FIT] umap_random_state=%d docs=%d",
            umap_random_state,
            len(fit_docs),
        )
    wrapper.set_hyperparameters(hp_input)
    hp = wrapper.hyperparameters
    LOGGER.info("Resolved hyperparameters: %s", json.dumps(_jsonable(hp), default=str))

    umap_model = UMAP(**hp["umap"])
    hdbscan_model = HDBSCAN(**hp["hdbscan"])

    vectorizer_params = dict(hp["vectorizer"])
    custom_stopwords = load_custom_stopwords_from_config(verbose=False)
    base_stop = vectorizer_params.get("stop_words", "english")
    if isinstance(base_stop, (list, set, tuple)):
        merged = sorted(set(base_stop).union(custom_stopwords))
    else:
        merged = sorted(set(ENGLISH_STOP_WORDS).union(custom_stopwords))
    vectorizer_params["stop_words"] = merged

    # Fix for garbage tokens: enforce alphabetic tokens of 2+ characters only.
    # This matches legacy retrain_models.py behavior and filters numbers, single chars,
    # and special patterns like "â€™" that slip through without proper mojibake cleanup.
    if "token_pattern" not in vectorizer_params:
        vectorizer_params["token_pattern"] = r"(?u)\b[a-zA-Z]{2,}\b"
        LOGGER.info("Set token_pattern to enforce 2+ char alphabetic tokens only")

    LOGGER.info("CountVectorizer stopwords: %d total, min_df=%s", len(merged), vectorizer_params["min_df"])
    vectorizer_model = CountVectorizer(**vectorizer_params)

    tfdf_model = SafeClassTfidfTransformer(**hp["tfdf_vectorizer"])
    representation_model = create_representation_models()

    topic_model = BERTopicWithSafeVectorizer(
        embedding_model=wrapper.embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        ctfidf_model=tfdf_model,
        representation_model=representation_model,
        **hp["bertopic"],
    )
    embeddings_numpy = np.asarray(fit_embeddings, dtype=np.float32)
    LOGGER.info(
        "Fitting BERTopic on %d docs (embeddings %s)...",
        len(fit_docs),
        embeddings_numpy.shape,
    )
    topic_model.fit_transform(fit_docs, embeddings=embeddings_numpy)

    # Early diagnostic: print topic counts and check for empty representations
    info = topic_model.get_topic_info()
    n_topics_real = len([t for t in info["Topic"] if int(t) != -1])
    outlier_count = int(info[info["Topic"] == -1]["Count"].sum()) if -1 in info["Topic"].values else 0
    LOGGER.info(
        "Post-fit snapshot: %d topics (excl. outliers), outlier docs=%d (%.2f%%)",
        n_topics_real,
        outlier_count,
        100.0 * outlier_count / len(fit_docs),
    )
    # Check for empty-representation topics (a red flag)
    empty_repr_topics = []
    for tid in info["Topic"].tolist():
        if int(tid) == -1:
            continue
        pairs = topic_model.get_topic(int(tid))
        if not pairs or all(w == "" for (w, _) in pairs[:10]):
            empty_repr_topics.append(int(tid))
    if empty_repr_topics:
        LOGGER.warning(
            "DIAGNOSTIC: %d/%d topics have empty representations: %s",
            len(empty_repr_topics),
            n_topics_real,
            empty_repr_topics[:10],
        )
    # Print top-5 topics by count with their top words
    top5 = info[info["Topic"] != -1].nlargest(5, "Count")
    for _, row in top5.iterrows():
        tid = int(row["Topic"])
        pairs = topic_model.get_topic(tid)
        words = [w for (w, _) in pairs[:8] if w] if pairs else []
        LOGGER.info(
            "  Topic %d (%d docs): %s",
            tid,
            int(row["Count"]),
            ", ".join(words) if words else "(empty)",
        )

    return topic_model


def _count_topics(topic_model: BERTopic) -> int:
    info = topic_model.get_topic_info()
    return len([t for t in info["Topic"] if int(t) != -1])


def _compute_fit_metrics(
    topic_model: BERTopic,
    fit_dictionary: Dictionary,
    tokens_eval: list[list[str]],
    eval_dictionary: Dictionary,
) -> dict[str, float]:
    topics_words = _topics_words_for_coherence(topic_model, fit_dictionary)
    doc_topics = topic_model.topics_
    return {
        "n_topics": float(len(topics_words)),
        "coherence_c_v": float(_coherence_cv(topics_words, tokens_eval, eval_dictionary)),
        "topic_diversity": float(_diversity_adaptive(topics_words)),
        "outlier_rate": float(_safe_outlier_rate_from_topics(np.asarray(doc_topics))),
    }


def _run_stability_check(
    wrapper: BERTopicOctisModelWithEmbeddings,
    flat_hp: dict[str, Any],
    fit_docs: list[str],
    fit_embeddings: np.ndarray,
    *,
    bo_call: int,
    reported_n_topics: float | None,
    n_runs: int,
    seed: int,
    max_std: float,
    collapse_ratio: float,
) -> tuple[dict[str, Any], BERTopic | None]:
    """Refit ``n_runs`` times with varying UMAP seeds; return stability report."""
    run_results: list[dict[str, Any]] = []
    topic_counts: list[float] = []
    fitted_models: list[BERTopic] = []
    for run_i in range(n_runs):
        umap_seed = seed + run_i
        LOGGER.info(
            "[COMPARE-FIT][STABILITY] call_%d run %d/%d umap_random_state=%d",
            bo_call,
            run_i + 1,
            n_runs,
            umap_seed,
        )
        topic_model = _fit_bertopic(
            wrapper,
            flat_hp,
            fit_docs,
            fit_embeddings,
            umap_random_state=umap_seed,
        )
        n_topics = _count_topics(topic_model)
        topic_counts.append(float(n_topics))
        fitted_models.append(topic_model)
        run_results.append({"run": run_i, "umap_random_state": umap_seed, "n_topics": n_topics})
        LOGGER.info(
            "[COMPARE-FIT][STABILITY] call_%d run %d/%d n_topics=%d",
            bo_call,
            run_i + 1,
            n_runs,
            n_topics,
        )

    stats = topic_run_stats(topic_counts)
    passed = stability_pass(topic_counts, max_std=max_std, collapse_ratio=collapse_ratio)
    refit_collapse = refit_collapse_flag(
        stats["median"],
        reported_n_topics or float("nan"),
        collapse_ratio=collapse_ratio,
    )
    report = {
        "bo_call": bo_call,
        "n_runs": n_runs,
        "seed": seed,
        "runs": run_results,
        "stats": stats,
        "stability_pass": passed and not refit_collapse,
        "topic_stability_pass": passed,
        "refit_collapse": refit_collapse,
        "reported_n_topics": reported_n_topics,
        "max_std": max_std,
        "collapse_ratio": collapse_ratio,
    }
    LOGGER.info(
        "[COMPARE-FIT][STABILITY] call_%d summary counts=%s std=%.2f pass=%s refit_collapse=%s",
        bo_call,
        topic_counts,
        stats["std"],
        report["stability_pass"],
        refit_collapse,
    )
    best_model: BERTopic | None = None
    if fitted_models and topic_counts:
        median_n = float(np.median(topic_counts))
        best_idx = int(np.argmin([abs(c - median_n) for c in topic_counts]))
        best_model = fitted_models[best_idx]
    return report, best_model


def _apply_reduce_outliers(
    topic_model: BERTopic,
    fit_docs: list[str],
    *,
    threshold: float = 0.05,
) -> BERTopic:
    """Reassign outlier (-1) docs and refresh topic assignments."""
    topics = np.asarray(topic_model.topics_)
    before_rate = _safe_outlier_rate_from_topics(topics)
    LOGGER.info(
        "[COMPARE-FIT] reduce_outliers start: outlier_rate=%.4f threshold=%.3f",
        before_rate,
        threshold,
    )
    new_topics = topic_model.reduce_outliers(
        fit_docs,
        topics,
        strategy="embeddings",
        threshold=threshold,
    )
    topic_model.update_topics(fit_docs, topics=new_topics)
    after_rate = _safe_outlier_rate_from_topics(np.asarray(topic_model.topics_))
    LOGGER.info(
        "[COMPARE-FIT] reduce_outliers done: outlier_rate %.4f -> %.4f",
        before_rate,
        after_rate,
    )
    return topic_model


def _topics_words_for_coherence(
    topic_model: BERTopic, fit_dictionary: Dictionary
) -> list[list[str]]:
    """Vocabulary-filtered topic words, mirroring the base wrapper output."""
    info = topic_model.get_topic_info()
    topic_ids = [int(t) for t in info["Topic"].tolist() if int(t) != -1]
    topics: list[list[str]] = []
    for tid in topic_ids:
        pairs = topic_model.get_topic(tid)
        if not pairs:
            continue
        words = [w for (w, _score) in pairs]
        words = [w for w in words if w in fit_dictionary.token2id]
        words = [w for w in words if w.lower() not in ("mr", "ms")]
        if words:
            topics.append(words)
    return topics


def compare_model_dir(out_dir: Path) -> Path:
    """Directory where compare-fit stores the BERTopic native artifact."""
    return out_dir / "model_compare"


def _model_is_saved(out_dir: Path) -> bool:
    model_dir = compare_model_dir(out_dir)
    return model_dir.is_dir() and any(model_dir.iterdir())


def _save_compare_model(
    topic_model: BERTopic,
    out_dir: Path,
    embedding_model_name: str,
) -> Path:
    """Persist BERTopic in native format for Stage05b holdout scoring."""
    model_dir = compare_model_dir(out_dir)
    if model_dir.exists():
        shutil.rmtree(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    embedding_model_path = embedding_model_name
    if not embedding_model_path.startswith("sentence-transformers/"):
        embedding_model_path = f"sentence-transformers/{embedding_model_name}"
    topic_model.save(
        str(model_dir),
        serialization="safetensors",
        save_embedding_model=embedding_model_path,
        save_ctfidf=True,
    )
    LOGGER.info("Saved compare-fit model: %s", model_dir)
    return model_dir


def _write_topic_tables(
    topic_model: BERTopic,
    out_dir: Path,
    *,
    n_repr_docs: int = 3,
) -> None:
    """Write topic_info.csv, top_words.csv, representative_docs.csv for inspection."""
    info = topic_model.get_topic_info()
    info.to_csv(out_dir / "topic_info.csv", index=False)

    with open(out_dir / "top_words.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["topic", "rank", "word", "ctfidf_score"])
        for tid in info["Topic"].tolist():
            pairs = topic_model.get_topic(int(tid))
            if not pairs:
                continue
            for rank, (word, score) in enumerate(pairs, start=1):
                writer.writerow([int(tid), rank, word, float(score)])

    try:
        repr_docs = topic_model.get_representative_docs()
    except Exception as ex:  # pragma: no cover - defensive
        LOGGER.warning("Could not extract representative docs: %s", ex)
        repr_docs = {}
    with open(out_dir / "representative_docs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["topic", "doc_rank", "sentence"])
        for tid, docs in repr_docs.items():
            for rank, doc in enumerate(docs[:n_repr_docs], start=1):
                writer.writerow([int(tid), rank, doc])


def _write_posthoc_for_dir(out_dir: Path) -> None:
    """Run post-hoc rule classifier on exported topic_info.csv (metadata only)."""
    topic_info_path = out_dir / "topic_info.csv"
    if not topic_info_path.exists():
        LOGGER.warning("[POSTHOC] skip: %s not found", topic_info_path)
        return
    try:
        write_posthoc_artifacts(topic_info_path, out_dir, logger=LOGGER)
    except Exception as ex:
        LOGGER.warning("[POSTHOC] classification failed for %s: %s", out_dir, ex)


def _jsonable(obj: Any) -> Any:
    """Make numpy / tuple values JSON-serializable for metrics dumps."""
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    return obj


def _rebuild_summary(compare_root: Path, bo_calls: list[int]) -> None:
    """Rewrite comparison_summary.csv from every per-config metrics.json present."""
    rows: list[dict[str, Any]] = []
    for call in bo_calls:
        metrics_path = compare_root / f"call_{call}" / "metrics.json"
        if not metrics_path.exists():
            continue
        with open(metrics_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        rows.append(
            {
                "bo_call": call,
                "embedding_model": m.get("embedding_model"),
                "n_topics": m.get("n_topics"),
                "coherence_c_v": m.get("coherence_c_v"),
                "topic_diversity": m.get("topic_diversity"),
                "outlier_rate": m.get("outlier_rate"),
                "reported_coherence_c_v": m.get("reported", {}).get("coherence_c_v"),
                "reported_n_topics": m.get("reported", {}).get("n_topics"),
                "elapsed_s": m.get("elapsed_s"),
            }
        )
    if rows:
        rows.sort(key=lambda r: (-(r["coherence_c_v"] or 0.0)))
        pd.DataFrame(rows).to_csv(compare_root / "comparison_summary.csv", index=False)


def run_compare_fit(
    trials_csv: Path,
    bo_calls: list[int],
    run_id: str,
    *,
    paths_config: Path,
    config_path: Path = Path("configs/train.yaml"),
    fit_indices: Path | None = None,
    fit_max_docs: int = 500_000,
    embedding_cache: Path | None = None,
    seed: int = 42,
    stability_runs: int = 0,
    stability_tolerance: float = 3.0,
    stability_collapse_ratio: float = 0.5,
    reduce_outliers: bool = False,
    save_model: bool = False,
    force_refit: bool = False,
) -> Path:
    """Refit each requested BO call on the shared stratified sample; write tables.

    Returns the comparison root directory containing per-config outputs and
    ``comparison_summary.csv``.
    """
    trials_csv = resolve_path(Path(trials_csv))
    paths_cfg = load_config(Path(paths_config))
    train_cfg = load_config(Path(config_path))
    paths = _build_paths(paths_cfg, run_id)

    logs_dir = resolve_path(Path(paths_cfg.get("outputs", {}).get("logs", "logs")))
    import sys

    # If stderr is redirected to the same log path (nohup >> log), skip console handler.
    log_path = logs_dir / f"stage05_compare_{run_id}.log"
    console = not (not sys.stdout.isatty() and not sys.stderr.isatty())
    setup_compare_logging(log_path, console=console)

    compare_root = paths.experiments_dir / "final_compare"
    compare_root.mkdir(parents=True, exist_ok=True)

    LOGGER.info("Stage05 compare-fit start: run_id=%s", run_id)
    LOGGER.info("Trials source: %s", trials_csv)
    LOGGER.info("BO calls to refit: %s", bo_calls)
    if stability_runs > 0:
        LOGGER.info(
            "[COMPARE-FIT] stability gate: %d runs, max_std=%.1f (umap_random_state=seed+i)",
            stability_runs,
            stability_tolerance,
        )
    if reduce_outliers:
        LOGGER.info("[COMPARE-FIT] reduce_outliers enabled (post-fit export)")
    if save_model:
        LOGGER.info("[COMPARE-FIT] save_model enabled (BERTopic native artifact for holdout)")

    inputs_cfg = paths_cfg.get("inputs", {})

    # --- Resolve the prebuilt full-corpus doc store (read-only) -----------------
    corpus_dir_override = inputs_cfg.get("octis_corpus_dir")
    corpus_root = (
        resolve_path(Path(corpus_dir_override)) if corpus_dir_override else paths.octis_dir
    )
    corpus_tsv = corpus_root / "corpus.tsv"
    offsets_file = corpus_offsets_path(corpus_root)
    doc_store = CorpusDocStore(corpus_tsv, offsets_file)
    n_docs_total = len(doc_store)

    n_train_docs = n_docs_total
    meta_path = corpus_metadata_path(corpus_root)
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        n_train_docs = int(meta.get("last-training-doc", n_docs_total))
    LOGGER.info(
        "Doc store: %d total docs (train partition [0, %d))", n_docs_total, n_train_docs
    )

    # --- Resolve cached embeddings memmap (no re-encoding) ----------------------
    embedding_model_name = None
    first_hp, first_reported = _read_trial_hyperparameters(trials_csv, bo_calls[0])
    embedding_model_name = first_reported.get("embedding_model")
    if not embedding_model_name:
        raise ValueError("Could not determine embedding_model from trials CSV.")

    if embedding_cache is not None:
        cache_file = resolve_path(Path(embedding_cache))
    else:
        overrides = (train_cfg.get("embeddings_cache", {}) or {}).get("overrides", {}) or {}
        override_path = overrides.get(embedding_model_name)
        if not override_path:
            raise ValueError(
                f"No embeddings cache override for {embedding_model_name} in {config_path}. "
                "Pass --embedding-cache explicitly."
            )
        cache_file = resolve_path(Path(override_path))
    if not cache_file.exists():
        raise FileNotFoundError(f"Embeddings cache not found: {cache_file}")
    LOGGER.info("Embeddings cache (mmap): %s", cache_file)

    fit_indices_path = resolve_path(Path(fit_indices)) if fit_indices else None
    if fit_indices_path is None:
        cfg_fit_indices = inputs_cfg.get("fit_indices_file")
        fit_indices_path = resolve_path(Path(cfg_fit_indices)) if cfg_fit_indices else None
    eval_indices_cfg = inputs_cfg.get("eval_indices_file")
    eval_indices_path = resolve_path(Path(eval_indices_cfg)) if eval_indices_cfg else None

    # --- Shared one-time load: fit docs/embeddings + eval tokens ----------------
    embeddings_mmap = np.load(cache_file, mmap_mode="r")
    if int(embeddings_mmap.shape[0]) != n_docs_total:
        raise RuntimeError(
            f"Embedding/corpus misalignment: embeddings have {embeddings_mmap.shape[0]} "
            f"rows but corpus has {n_docs_total}."
        )

    with stage_timer("load fit sample (docs + embeddings)"):
        fit_docs, fit_embeddings, _ = _prepare_bertopic_fit_data(
            doc_store,
            embeddings_mmap,
            fit_max_docs=fit_max_docs,
            seed=seed,
            logger=LOGGER,
            n_train=n_train_docs,
            fit_indices_path=fit_indices_path,
        )
    # --- Filter short documents that cause empty-representation clusters ----------
    # Sentences with < MIN_WORDS_FIT words (e.g., "yes.", "no.", "what?") cluster
    # together by embedding similarity but c-TF-IDF can't extract keywords from them.
    # Filter before fitting to prevent these degenerate single-word-utterance topics.
    MIN_WORDS_FIT = 4
    orig_len = len(fit_docs)
    keep_mask = np.array([len(doc.split()) >= MIN_WORDS_FIT for doc in fit_docs])
    fit_docs = [doc for doc, keep in zip(fit_docs, keep_mask) if keep]
    fit_embeddings = fit_embeddings[keep_mask]
    LOGGER.info(
        "Filtered short docs (<=%d words): %d -> %d (removed %d / %.2f%%)",
        MIN_WORDS_FIT - 1,
        orig_len,
        len(fit_docs),
        orig_len - len(fit_docs),
        100.0 * (orig_len - len(fit_docs)) / orig_len,
    )

    fit_dictionary = Dictionary(doc.split() for doc in fit_docs)
    LOGGER.info(
        "Fit-corpus topic filter dictionary: %d docs -> %d tokens",
        len(fit_docs),
        len(fit_dictionary),
    )

    with stage_timer("load stratified eval tokens"):
        tokens_eval: list[list[str]] = []
        if eval_indices_path and eval_indices_path.exists():
            eval_idx = np.asarray(np.load(eval_indices_path), dtype=np.int64)
            in_val = eval_idx[(eval_idx >= n_train_docs) & (eval_idx < n_docs_total)]
            if in_val.size:
                eval_docs = doc_store.fetch_documents(np.unique(in_val))
                tokens_eval = [d.split() for d in eval_docs if d]
        if not tokens_eval:
            raise RuntimeError(
                "No stratified eval tokens available; eval_indices_file missing or empty."
            )
        eval_dictionary = Dictionary(tokens_eval)
    LOGGER.info("Coherence eval tokens: %d docs", len(tokens_eval))

    # --- Resume status + time estimate ------------------------------------------
    pending = []
    for c in bo_calls:
        out_dir = compare_root / f"call_{c}"
        metrics_exist = (out_dir / "metrics.json").exists()
        needs_model = save_model and not _model_is_saved(out_dir)
        if force_refit or not metrics_exist or needs_model:
            pending.append(c)
    done_already = [c for c in bo_calls if c not in pending]
    if done_already:
        LOGGER.info("Resume: %s already complete, skipping.", done_already)
    LOGGER.info(
        "Configs to fit now: %s (%d). Estimated ~12-20 min each on GPU => ~%.1f-%.1f h total.",
        pending,
        len(pending),
        len(pending) * 12 / 60,
        len(pending) * 20 / 60,
    )

    # Build the wrapper once; reuse across configs (docs + embeddings are shared).
    embedding_model = load_embedding_model(embedding_model_name)
    wrapper = BERTopicOctisModelWithEmbeddings(
        embedding_model=embedding_model,
        embedding_model_name=embedding_model_name,
        embeddings=fit_embeddings,
        dataset_as_list_of_strings=fit_docs,
        dataset_as_list_of_lists=None,
        verbose=False,
        calculate_probabilities=False,
        topic_filter_dictionary=fit_dictionary,
    )

    stability_summary_rows: list[dict[str, Any]] = []

    for call in bo_calls:
        out_dir = compare_root / f"call_{call}"
        metrics_exist = (out_dir / "metrics.json").exists()
        needs_model = save_model and not _model_is_saved(out_dir)
        if metrics_exist and not reduce_outliers and not force_refit and not needs_model:
            LOGGER.info("call_%d already done (metrics.json present); skipping.", call)
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        flat_hp, reported = _read_trial_hyperparameters(trials_csv, call)
        LOGGER.info("=== Fitting call_%d (reported coh=%s n=%s) ===",
                    call, reported.get("coherence_c_v"), reported.get("n_topics"))
        config_start = time.perf_counter()

        stability_report: dict[str, Any] | None = None
        topic_model: BERTopic | None = None
        if stability_runs > 0:
            with stage_timer(f"call_{call} stability check ({stability_runs} runs)"):
                stability_report, topic_model = _run_stability_check(
                    wrapper,
                    flat_hp,
                    fit_docs,
                    fit_embeddings,
                    bo_call=call,
                    reported_n_topics=reported.get("n_topics"),
                    n_runs=stability_runs,
                    seed=seed,
                    max_std=stability_tolerance,
                    collapse_ratio=stability_collapse_ratio,
                )
                with open(out_dir / "stability.json", "w", encoding="utf-8") as f:
                    json.dump(_jsonable(stability_report), f, indent=2)
                stability_summary_rows.append(
                    {
                        "bo_call": call,
                        "n_topics_median": stability_report["stats"]["median"],
                        "n_topics_std": stability_report["stats"]["std"],
                        "stability_pass": stability_report["stability_pass"],
                        "refit_collapse": stability_report["refit_collapse"],
                        "reported_n_topics": reported.get("n_topics"),
                    }
                )

        refit_for_metrics = force_refit or not metrics_exist
        if topic_model is None:
            if metrics_exist and reduce_outliers and not refit_for_metrics:
                LOGGER.info("call_%d metrics exist; running reduce_outliers export only.", call)
            elif metrics_exist and needs_model and not refit_for_metrics:
                LOGGER.info("call_%d metrics exist; refitting to save holdout model.", call)
            if topic_model is None:
                with stage_timer(f"call_{call} BERTopic fit (UMAP+HDBSCAN+repr)"):
                    topic_model = _fit_bertopic(
                        wrapper,
                        flat_hp,
                        fit_docs,
                        fit_embeddings,
                        umap_random_state=seed,
                    )

        if refit_for_metrics or not metrics_exist:
            with stage_timer(f"call_{call} metrics (coherence + diversity)"):
                fit_metrics = _compute_fit_metrics(
                    topic_model, fit_dictionary, tokens_eval, eval_dictionary
                )
                coherence = fit_metrics["coherence_c_v"]
                diversity = fit_metrics["topic_diversity"]
                outlier_rate = fit_metrics["outlier_rate"]
                n_topics = int(fit_metrics["n_topics"])

            with stage_timer(f"call_{call} write topic tables"):
                _write_topic_tables(topic_model, out_dir)
                _write_posthoc_for_dir(out_dir)
        else:
            with open(out_dir / "metrics.json", "r", encoding="utf-8") as f:
                existing = json.load(f)
            coherence = float(existing["coherence_c_v"])
            diversity = float(existing["topic_diversity"])
            outlier_rate = float(existing["outlier_rate"])
            n_topics = int(existing["n_topics"])
            _write_posthoc_for_dir(out_dir)

        if reduce_outliers:
            reduced_dir = out_dir / "outliers_reduced"
            reduced_dir.mkdir(parents=True, exist_ok=True)
            with stage_timer(f"call_{call} reduce_outliers + re-export"):
                topic_model = _apply_reduce_outliers(topic_model, fit_docs)
                reduced_metrics = _compute_fit_metrics(
                    topic_model, fit_dictionary, tokens_eval, eval_dictionary
                )
                _write_topic_tables(topic_model, reduced_dir)
                _write_posthoc_for_dir(reduced_dir)
                with open(reduced_dir / "metrics.json", "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "run_id": run_id,
                            "bo_call": call,
                            "embedding_model": embedding_model_name,
                            **reduced_metrics,
                            "reported": reported,
                            "parent_outlier_rate": outlier_rate,
                        },
                        f,
                        indent=2,
                    )
                LOGGER.info(
                    "call_%d outliers_reduced: n_topics=%d outlier %.4f -> %.4f",
                    call,
                    int(reduced_metrics["n_topics"]),
                    outlier_rate,
                    reduced_metrics["outlier_rate"],
                )

        if save_model:
            with stage_timer(f"call_{call} save BERTopic model"):
                _save_compare_model(topic_model, out_dir, embedding_model_name)

        elapsed = time.perf_counter() - config_start
        if refit_for_metrics or not metrics_exist:
            metrics = {
                "run_id": run_id,
                "bo_call": call,
                "embedding_model": embedding_model_name,
                "n_topics": n_topics,
                "coherence_c_v": coherence,
                "topic_diversity": diversity,
                "outlier_rate": outlier_rate,
                "elapsed_s": round(elapsed, 1),
                "fit_docs": len(fit_docs),
                "fit_max_docs": fit_max_docs,
                "hyperparameters": _jsonable(flat_hp),
                "reported": reported,
                "fit_started_at": _utc_now(),
            }
            if stability_report is not None:
                metrics["stability"] = _jsonable(stability_report)
            with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2)
        LOGGER.info(
            "call_%d done: n_topics=%d coherence=%.4f diversity=%.4f outlier=%.4f (%.1fs)",
            call, n_topics, coherence, diversity, outlier_rate, elapsed,
        )
        _rebuild_summary(compare_root, bo_calls)

    if stability_summary_rows:
        pd.DataFrame(stability_summary_rows).to_csv(
            compare_root / "stability_summary.csv",
            index=False,
        )
        LOGGER.info("Stability summary: %s", compare_root / "stability_summary.csv")

    _rebuild_summary(compare_root, bo_calls)
    LOGGER.info("Compare-fit complete. Outputs under: %s", compare_root)
    LOGGER.info("Summary: %s", compare_root / "comparison_summary.csv")
    return compare_root
