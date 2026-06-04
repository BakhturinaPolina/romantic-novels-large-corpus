"""Stage 03 train/eval tuning workflow."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
from octis.evaluation_metrics.metrics import AbstractMetric
from octis.optimization.optimizer import Optimizer
from skopt.space.space import Integer, Real

from src.common.config import load_config, resolve_path
from src.common.logging import setup_logging
from src.stage03_train.bertopic_octis_model import (
    BERTopicOctisModelWithEmbeddings,
    load_embedding_model,
)
from src.stage03_train.corpus_store import (
    CorpusDocStore,
    corpus_offsets_path,
    load_octis_dataset_metadata_only,
)
from src.stage03_train.bo_resume import (
    best_params_from_bo,
    bo_calls_done,
    is_bo_complete,
    load_bo_checkpoint,
    make_resumable_optimizer_class,
    restore_optimizer_skopt_state,
    sync_trials_partial_from_checkpoint,
)
from src.stage03_train.data_io import load_eval_tokens_chunked, load_train_eval
from src.stage03_train.embeddings import compute_embeddings_from_csvs, get_cache_file
from src.stage03_train.embeddings_hub import load_project_dotenv
from src.stage03_train.octis_corpus import write_octis_corpus_from_csvs


@dataclass
class TunePaths:
    train_csv: Path
    eval_csv: Path
    test_csv: Path
    octis_dir: Path
    experiments_dir: Path


def _build_paths(paths_cfg: dict[str, Any], run_id: str) -> TunePaths:
    inputs = paths_cfg.get("inputs", {})
    outputs = paths_cfg.get("outputs", {})
    train_csv = resolve_path(Path(inputs["sentences_train_csv"]))
    eval_csv = resolve_path(Path(inputs["sentences_val_csv"]))
    test_csv = resolve_path(Path(inputs["sentences_test_csv"]))
    octis_base = resolve_path(Path(inputs.get("octis_dataset", "data/interim/octis")))
    exp_base = resolve_path(Path(outputs.get("experiments", "results/experiments")))
    return TunePaths(
        train_csv=train_csv,
        eval_csv=eval_csv,
        test_csv=test_csv,
        octis_dir=octis_base / run_id,
        experiments_dir=exp_base / run_id,
    )


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def _write_trials(trials_csv: Path, rows: list[dict[str, Any]]) -> None:
    df = pd.DataFrame(rows)
    df.to_csv(trials_csv, index=False)


def _default_state(run_id: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "started_at": _utc_now(),
        "updated_at": _utc_now(),
        "completed": False,
        "steps": {},
        "models": {},
    }


def _load_state(run_state_json: Path, run_id: str) -> dict[str, Any]:
    if not run_state_json.exists():
        return _default_state(run_id)
    with open(run_state_json, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if payload.get("run_id") != run_id:
        return _default_state(run_id)
    return payload


def _save_state(run_state_json: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = _utc_now()
    _write_json(run_state_json, state)


def _step_completed(state: dict[str, Any], step_name: str) -> bool:
    return state.get("steps", {}).get(step_name, {}).get("status") == "completed"


def _mark_step(
    state: dict[str, Any],
    step_name: str,
    *,
    status: str,
    duration_s: float | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    entry = state.setdefault("steps", {}).setdefault(step_name, {})
    entry["status"] = status
    if status == "running":
        entry["started_at"] = _utc_now()
    if status == "completed":
        entry["completed_at"] = _utc_now()
    if duration_s is not None:
        entry["duration_s"] = round(float(duration_s), 3)
    if details:
        merged = dict(entry.get("details", {}))
        merged.update(details)
        entry["details"] = merged


def _mark_model(
    state: dict[str, Any],
    model_name: str,
    *,
    status: str,
    duration_s: float | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    entry = state.setdefault("models", {}).setdefault(model_name, {})
    entry["status"] = status
    if status == "running":
        entry["started_at"] = _utc_now()
    if status in {"completed", "skipped"}:
        entry["completed_at"] = _utc_now()
    if duration_s is not None:
        entry["duration_s"] = round(float(duration_s), 3)
    if details:
        merged = dict(entry.get("details", {}))
        merged.update(details)
        entry["details"] = merged


def _safe_outlier_rate(topic_document_matrix: Any) -> float:
    matrix = np.asarray(topic_document_matrix)
    if matrix.ndim != 2 or matrix.shape[0] == 0:
        return 1.0
    return float(np.mean(np.max(matrix, axis=1) == 0))


def _prepare_bertopic_fit_data(
    doc_store: CorpusDocStore,
    embeddings: np.ndarray,
    *,
    fit_max_docs: int | None,
    seed: int,
    logger: Any,
) -> tuple[Any, np.ndarray, int]:
    """Subsample docs/embeddings when the full corpus exceeds GPU UMAP capacity."""
    n_total = len(doc_store)
    if fit_max_docs is None or n_total <= fit_max_docs:
        return doc_store, embeddings, n_total

    rng = np.random.default_rng(seed)
    fit_indices = np.sort(rng.choice(n_total, size=fit_max_docs, replace=False))
    logger.info(
        "BERTopic fit subsample: %d / %d docs (bertopic_fit_max_docs=%d)",
        fit_max_docs,
        n_total,
        fit_max_docs,
    )
    step_start = time.perf_counter()
    fit_docs = doc_store.fetch_documents(fit_indices)
    fit_embeddings = np.asarray(embeddings[fit_indices], dtype=np.float32)
    logger.info(
        "BERTopic fit subsample materialized in %.2fs (embeddings shape=%s)",
        time.perf_counter() - step_start,
        fit_embeddings.shape,
    )
    return fit_docs, fit_embeddings, n_total


def build_search_space(cfg: dict[str, Any]) -> dict[str, Any]:
    """Build skopt search space from config."""
    s = cfg["search_space"]
    return {
        "umap__n_neighbors": Integer(s["umap__n_neighbors"][0], s["umap__n_neighbors"][1]),
        "umap__n_components": Integer(s["umap__n_components"][0], s["umap__n_components"][1]),
        "umap__min_dist": Real(s["umap__min_dist"][0], s["umap__min_dist"][1]),
        "hdbscan__min_cluster_size": Integer(
            s["hdbscan__min_cluster_size"][0], s["hdbscan__min_cluster_size"][1]
        ),
        "hdbscan__min_samples": Integer(s["hdbscan__min_samples"][0], s["hdbscan__min_samples"][1]),
        "vectorizer__min_df": Real(s["vectorizer__min_df"][0], s["vectorizer__min_df"][1]),
        "bertopic__top_n_words": Integer(s["bertopic__top_n_words"][0], s["bertopic__top_n_words"][1]),
        "bertopic__min_topic_size": Integer(
            s["bertopic__min_topic_size"][0], s["bertopic__min_topic_size"][1]
        ),
    }


def _topics_from_output(output_topics: Any) -> list[list[str]]:
    if output_topics is None:
        return []
    if isinstance(output_topics, np.ndarray):
        topics = []
        for row in output_topics.tolist():
            words = [w for w in row if isinstance(w, str) and w]
            if words:
                topics.append(words)
        return topics
    return [list(t) for t in output_topics if t]


def _data_load_cache_valid(
    state: dict[str, Any],
    *,
    train_csv: Path,
    eval_csv: Path,
    chunk_size: int,
) -> bool:
    """True when prior data_load counts can be reused for the same CSV inputs."""
    if not _step_completed(state, "data_load"):
        return False
    details = state.get("steps", {}).get("data_load", {}).get("details", {})
    return (
        str(details.get("train_csv", "")) == str(train_csv)
        and str(details.get("eval_csv", "")) == str(eval_csv)
        and int(details.get("csv_chunk_size", -1)) == chunk_size
        and "n_train_docs" in details
        and "n_eval_docs" in details
    )


def _optimize_with_resume(
    optimizer: Optimizer,
    *,
    model: Any,
    octis_dataset: Any,
    npmi_metric: Coherence,
    search_space: dict[str, Any],
    optimization_dir: Path,
    number_of_calls: int,
    model_runs: int,
    save_models: bool,
    diversity_metric: TopicDiversity,
    random_state: int | bool,
    logger: Any,
) -> Any:
    """
    Run OCTIS BO, resuming from ``optimization_dir/result.json`` when present.

    Uses ``_restore_parameters`` + in-memory model injection so embeddings are
    preserved. ``optimize(x0=, y0=)`` is avoided because OCTIS rejects it when
    ``number_of_calls <= len(search_space)`` (smoke configs hit this).
    """
    optimization_dir.mkdir(parents=True, exist_ok=True)
    result_json = optimization_dir / "result.json"
    checkpoint = load_bo_checkpoint(result_json)
    stability_seed = random_state if isinstance(random_state, int) else False

    optimize_kwargs: dict[str, Any] = {
        "number_of_call": number_of_calls,
        "model_runs": model_runs,
        "save_models": save_models,
        "extra_metrics": [diversity_metric],
        "save_path": str(optimization_dir),
        "save_step": 1,
        "random_state": stability_seed,
    }

    if checkpoint is None:
        logger.info("Starting BO optimization (%d calls): %s", number_of_calls, optimization_dir)
        return optimizer.optimize(
            model,
            octis_dataset,
            npmi_metric,
            search_space,
            **optimize_kwargs,
        )

    done = bo_calls_done(checkpoint)
    if is_bo_complete(checkpoint, number_of_calls=number_of_calls):
        logger.info(
            "BO checkpoint complete (%d/%d calls); skipping optimize: %s",
            done,
            number_of_calls,
            result_json,
        )
        return checkpoint

    logger.info(
        "Resuming BO from checkpoint (%d/%d calls done): %s",
        done,
        number_of_calls,
        result_json,
    )
    res, opt = restore_optimizer_skopt_state(optimizer, checkpoint)
    optimizer.model = model
    optimizer.dataset = octis_dataset
    optimizer.metric = npmi_metric
    optimizer.extra_metrics = [diversity_metric]
    optimizer.number_of_call = number_of_calls

    if optimizer.number_of_previous_calls >= optimizer.number_of_call:
        from octis.optimization.optimizer_evaluation import OptimizerEvaluation

        return OptimizerEvaluation(optimizer, BO_results=res)

    return optimizer._optimization_loop(opt)


def _best_params_from_optimize_result(result: Any, optimization_dir: Path) -> dict[str, Any]:
    """Extract best hyperparameters from OptimizerEvaluation or checkpoint JSON."""
    if isinstance(result, dict):
        params = best_params_from_bo(result)
        if params:
            return params
        return result.get("best_params", {}) or result.get("x", {}) or {}

    if hasattr(result, "func_vals") and hasattr(result, "x_iters"):
        f_vals = list(result.func_vals)
        if not f_vals:
            return {}
        best_idx = int(np.argmax(f_vals))
        return {name: result.x_iters[name][best_idx] for name in sorted(result.x_iters.keys())}

    checkpoint = load_bo_checkpoint(optimization_dir / "result.json")
    if checkpoint:
        return best_params_from_bo(checkpoint)
    return {}


def _coherence_cv(
    topics: list[list[str]],
    eval_tokens: list[list[str]],
    dictionary: Dictionary | None = None,
) -> float:
    """Vocabulary-filtered gensim ``c_v`` coherence (robust to short topics).

    Unlike OCTIS ``Coherence(topk=...)`` this never raises on topics shorter than
    a fixed ``topk`` and never collapses to a constant: it drops out-of-vocabulary
    words, drops empty topics, then lets gensim use each topic's available words.
    """
    if not topics:
        return 0.0
    dictionary = dictionary if dictionary is not None else Dictionary(eval_tokens)
    topics_in_vocab = [[w for w in topic if w in dictionary.token2id] for topic in topics]
    topics_in_vocab = [t for t in topics_in_vocab if t]
    if not topics_in_vocab:
        return 0.0
    cm = CoherenceModel(
        topics=topics_in_vocab, texts=eval_tokens, dictionary=dictionary, coherence="c_v"
    )
    return float(cm.get_coherence())


def _diversity_adaptive(topics: list[list[str]]) -> float:
    """TopicDiversity with an adaptive ``topk`` capped by the shortest topic."""
    min_topic_len = min((len(t) for t in topics if t), default=0)
    if min_topic_len == 0:
        return 0.0
    diversity_topk = max(1, min(10, min_topic_len))
    return float(TopicDiversity(topk=diversity_topk).score({"topics": topics}))


class AdaptiveCVCoherence(AbstractMetric):
    """OCTIS-compatible optimized metric: vocab-filtered ``c_v`` coherence.

    Replaces ``Coherence(topk=1, measure='c_v')`` which is degenerate (always 1.0
    for single-word topics). Builds the gensim ``Dictionary`` once and reuses it
    for every BO call, and shares ``_coherence_cv`` with the final trials.csv
    computation so BO optimizes exactly the reported metric.
    """

    def __init__(self, texts: list[list[str]]):
        super().__init__()
        self._texts = [t for t in texts if t]
        self._dictionary = Dictionary(self._texts) if self._texts else Dictionary([[""]])

    def info(self) -> dict[str, str]:
        return {"name": "Coherence"}

    def score(self, model_output: dict[str, Any]) -> float:
        topics = model_output.get("topics")
        if not topics:
            return 0.0
        return _coherence_cv(topics, self._texts, self._dictionary)


class AdaptiveTopicDiversity(AbstractMetric):
    """OCTIS-compatible extra metric: adaptive-``topk`` topic diversity."""

    def info(self) -> dict[str, str]:
        return {"name": "TopicDiversity"}

    def score(self, model_output: dict[str, Any]) -> float:
        topics = model_output.get("topics")
        if not topics:
            return 0.0
        return _diversity_adaptive(topics)


def _compute_metrics(topics: list[list[str]], eval_tokens: list[list[str]]) -> tuple[float, float]:
    if not topics:
        return 0.0, 0.0
    coherence = _coherence_cv(topics, eval_tokens)
    diversity = _diversity_adaptive(topics)
    return coherence, diversity


def run_tuning(
    config_path: Path,
    run_id: str,
    embedding_models_override: list[str] | None = None,
    paths_config: Path | None = None,
) -> Path:
    """Execute tuning and return trials.csv path."""
    started_at = time.perf_counter()
    cfg = load_config(config_path)
    paths_cfg_path = paths_config or Path(cfg.get("paths_config", "configs/paths.yaml"))
    paths_cfg = load_config(paths_cfg_path)
    paths = _build_paths(paths_cfg, run_id)
    logs_dir = resolve_path(Path(paths_cfg.get("outputs", {}).get("logs", "logs")))
    load_project_dotenv()
    logger = setup_logging(logs_dir=logs_dir, log_file=f"stage03_{run_id}.log")
    logger.info("Stage03 run start: run_id=%s config=%s", run_id, config_path)
    hub_cfg = cfg.get("embeddings_hub")

    paths.octis_dir.mkdir(parents=True, exist_ok=True)
    paths.experiments_dir.mkdir(parents=True, exist_ok=True)
    run_state_json = paths.experiments_dir / "run_state.json"
    run_summary_json = paths.experiments_dir / "run_summary.json"
    trials_csv = paths.experiments_dir / "trials.csv"
    manifest_json = paths.experiments_dir / "run_manifest.json"
    log_file = logs_dir / f"stage03_{run_id}.log"

    state = _load_state(run_state_json, run_id)
    _save_state(run_state_json, state)

    text_cfg = cfg.get("text", {})
    sentence_column = text_cfg.get("sentence_column", "sentence")
    chunk_size = int(text_cfg.get("csv_chunk_size", 50_000))
    coherence_eval_max_docs = text_cfg.get("coherence_eval_max_docs")
    if coherence_eval_max_docs is not None:
        coherence_eval_max_docs = int(coherence_eval_max_docs)
    bertopic_fit_max_docs = text_cfg.get("bertopic_fit_max_docs")
    if bertopic_fit_max_docs is not None:
        bertopic_fit_max_docs = int(bertopic_fit_max_docs)

    step_start = time.perf_counter()
    if _data_load_cache_valid(
        state,
        train_csv=paths.train_csv,
        eval_csv=paths.eval_csv,
        chunk_size=chunk_size,
    ):
        details = state["steps"]["data_load"]["details"]
        n_train_docs = int(details["n_train_docs"])
        n_eval_docs = int(details["n_eval_docs"])
        logger.info(
            "Reusing cached data_load counts (train=%d, eval=%d); loading eval tokens only",
            n_train_docs,
            n_eval_docs,
        )
        tokens_eval = load_eval_tokens_chunked(
            paths.eval_csv,
            sentence_column=sentence_column,
            chunk_size=chunk_size,
            max_docs=coherence_eval_max_docs,
            logger=logger,
        )
        data_duration = time.perf_counter() - step_start
        _mark_step(
            state,
            "data_load",
            status="completed",
            duration_s=data_duration,
            details={
                "n_train_docs": n_train_docs,
                "n_eval_docs": n_eval_docs,
                "coherence_eval_docs": len(tokens_eval),
                "csv_chunk_size": chunk_size,
                "train_csv": str(paths.train_csv),
                "eval_csv": str(paths.eval_csv),
                "reused_counts": True,
            },
        )
        _save_state(run_state_json, state)
        logger.info(
            "Data scan completed in %.2fs (train=%d, eval=%d, coherence_tokens=%d, reused counts)",
            data_duration,
            n_train_docs,
            n_eval_docs,
            len(tokens_eval),
        )
    else:
        _mark_step(state, "data_load", status="running")
        _save_state(run_state_json, state)
        logger.info(
            "Scanning train/eval splits (chunk_size=%d) from %s and %s",
            chunk_size,
            paths.train_csv,
            paths.eval_csv,
        )
        try:
            payload = load_train_eval(
                paths.train_csv,
                paths.eval_csv,
                sentence_column=sentence_column,
                chunk_size=chunk_size,
                coherence_eval_max_docs=coherence_eval_max_docs,
                logger=logger,
            )
        except Exception as ex:
            _mark_step(state, "data_load", status="failed", details={"error": str(ex)})
            _save_state(run_state_json, state)
            raise
        n_train_docs = int(payload["n_train_docs"])
        n_eval_docs = int(payload["n_eval_docs"])
        tokens_eval = payload["tokens_eval"]
        data_duration = time.perf_counter() - step_start
        _mark_step(
            state,
            "data_load",
            status="completed",
            duration_s=data_duration,
            details={
                "n_train_docs": n_train_docs,
                "n_eval_docs": n_eval_docs,
                "coherence_eval_docs": len(tokens_eval),
                "csv_chunk_size": chunk_size,
                "train_csv": str(paths.train_csv),
                "eval_csv": str(paths.eval_csv),
            },
        )
        _save_state(run_state_json, state)
        logger.info(
            "Data scan completed in %.2fs (train=%d, eval=%d, coherence_tokens=%d)",
            data_duration,
            n_train_docs,
            n_eval_docs,
            len(tokens_eval),
        )

    corpus_tsv = paths.octis_dir / "corpus.tsv"
    offsets_file = corpus_offsets_path(paths.octis_dir)
    if _step_completed(state, "octis_corpus_written") and corpus_tsv.exists() and offsets_file.exists():
        logger.info("Skipping OCTIS corpus write (already completed): %s", corpus_tsv)
        n_train_docs = int(
            state.get("steps", {})
            .get("octis_corpus_written", {})
            .get("details", {})
            .get("n_train_docs", n_train_docs)
        )
        n_eval_docs = int(
            state.get("steps", {})
            .get("octis_corpus_written", {})
            .get("details", {})
            .get("n_eval_docs", n_eval_docs)
        )
    else:
        step_start = time.perf_counter()
        _mark_step(state, "octis_corpus_written", status="running")
        _save_state(run_state_json, state)
        _corpus_path, _offsets, n_train_docs, n_eval_docs = write_octis_corpus_from_csvs(
            paths.train_csv,
            paths.eval_csv,
            paths.octis_dir,
            sentence_column=sentence_column,
            chunk_size=chunk_size,
            logger=logger,
        )
        corpus_duration = time.perf_counter() - step_start
        _mark_step(
            state,
            "octis_corpus_written",
            status="completed",
            duration_s=corpus_duration,
            details={
                "corpus_tsv": str(corpus_tsv),
                "corpus_offsets": str(offsets_file),
                "n_train_docs": n_train_docs,
                "n_eval_docs": n_eval_docs,
            },
        )
        _save_state(run_state_json, state)
        logger.info("OCTIS corpus ready in %.2fs: %s", corpus_duration, corpus_tsv)

    doc_store = CorpusDocStore(corpus_tsv, offsets_file)
    n_docs_total = len(doc_store)
    logger.info("Disk-backed document store: %d documents", n_docs_total)

    step_start = time.perf_counter()
    _mark_step(state, "octis_dataset_load", status="running")
    _save_state(run_state_json, state)
    octis_dataset = load_octis_dataset_metadata_only(paths.octis_dir)
    dataset_duration = time.perf_counter() - step_start
    _mark_step(
        state,
        "octis_dataset_load",
        status="completed",
        duration_s=dataset_duration,
        details={"octis_dir": str(paths.octis_dir), "metadata_only": True},
    )
    _save_state(run_state_json, state)
    logger.info("OCTIS metadata loaded in %.2fs (corpus not loaded into RAM)", dataset_duration)
    existing_rows: list[dict[str, Any]] = []
    if trials_csv.exists():
        try:
            existing_rows = pd.read_csv(trials_csv).to_dict(orient="records")
            logger.info("Loaded existing trials for resume: %d rows", len(existing_rows))
        except Exception as ex:  # pragma: no cover
            logger.warning("Could not read existing trials.csv (%s), starting fresh.", ex)

    trials_by_model: dict[str, dict[str, Any]] = {}
    for row in existing_rows:
        model_key = str(row.get("embedding_model", ""))
        if model_key and model_key not in trials_by_model:
            trials_by_model[model_key] = row

    search_space = build_search_space(cfg)
    selected_models = embedding_models_override or cfg["embedding_models"]
    logger.info("Selected embedding models: %s", selected_models)

    for idx, model_name in enumerate(selected_models, start=1):
        model_step_start = time.perf_counter()
        model_state = state.get("models", {}).get(model_name, {})
        already_done = (
            model_state.get("status") in {"completed", "skipped"} and model_name in trials_by_model
        )
        if already_done:
            _mark_model(
                state,
                model_name,
                status="skipped",
                details={"reason": "existing_model_result"},
            )
            _save_state(run_state_json, state)
            logger.info("Skipping model %s (already completed in prior run)", model_name)
            continue

        logger.info("Starting model %d/%d: %s", idx, len(selected_models), model_name)
        _mark_model(state, model_name, status="running")
        _save_state(run_state_json, state)
        cache_dir = paths.octis_dir / "embeddings_cache"
        cache_file = get_cache_file(cache_dir, "train_eval", model_name)
        cache_hit = cache_file.exists()
        logger.info("Embedding cache %s for %s", "hit" if cache_hit else "miss", model_name)
        emb = compute_embeddings_from_csvs(
            paths.train_csv,
            paths.eval_csv,
            model_name=model_name,
            cache_file=cache_file,
            sentence_column=sentence_column,
            chunk_size=chunk_size,
            device=cfg.get("device", "auto"),
            batch_size=int(cfg.get("embedding_batch_size", 256)),
            logger=logger,
            hub_cfg=hub_cfg,
            run_id=run_id,
        )
        fit_docs, fit_embeddings, n_docs_total = _prepare_bertopic_fit_data(
            doc_store,
            emb,
            fit_max_docs=bertopic_fit_max_docs,
            seed=int(cfg["optimization"].get("seed", 42)),
            logger=logger,
        )
        model = BERTopicOctisModelWithEmbeddings(
            embedding_model=load_embedding_model(model_name),
            embedding_model_name=model_name,
            embeddings=fit_embeddings,
            dataset_as_list_of_strings=fit_docs,
            dataset_as_list_of_lists=tokens_eval,
            optimization_results_dir=str(paths.experiments_dir / "optimization"),
            verbose=True,
        )
        model.use_partitions = True

        optimizer = make_resumable_optimizer_class()()
        # Vocab-filtered c_v coherence (shared with trials.csv via _coherence_cv).
        # Replaces Coherence(topk=1, measure="c_v"), which was degenerate (always
        # 1.0 for single-word topics) and turned the BO objective into a constant.
        npmi_metric = AdaptiveCVCoherence(texts=tokens_eval)
        diversity_metric = AdaptiveTopicDiversity()
        optimization_dir = paths.experiments_dir / f"opt_{idx}_{model_name.replace('/', '__')}"
        result_json = optimization_dir / "result.json"
        trials_partial_csv = optimization_dir / "trials_partial.csv"
        opt_seed = int(cfg["optimization"].get("seed", 42))
        stability_score = float(cfg["optimization"].get("default_stability_score", 0.0))
        number_of_calls = int(cfg["optimization"]["number_of_calls"])

        def _on_bo_call_complete(current_call: int, _res: Any) -> None:
            """Persist ``trials_partial.csv`` and log progress after each BO call."""
            rows, done, total = sync_trials_partial_from_checkpoint(
                result_json,
                trials_partial_csv,
                run_id=run_id,
                model_idx=idx,
                model_name=model_name,
                train_csv=paths.train_csv,
                eval_csv=paths.eval_csv,
                test_csv=paths.test_csv,
                seed=opt_seed,
                stability_score=stability_score,
            )
            latest = rows[-1] if rows else {}
            logger.info(
                "BO call %d/%d complete: coherence=%s diversity=%s "
                "(partial trials=%d) -> %s",
                done,
                total or number_of_calls,
                latest.get("coherence_c_v"),
                latest.get("topic_diversity"),
                len(rows),
                trials_partial_csv,
            )
            model_state = state.get("models", {}).get(model_name, {})
            details = dict(model_state.get("details", {}))
            details["bo_calls_done"] = done
            details["bo_calls_total"] = total or number_of_calls
            _mark_model(state, model_name, status="running", details=details)
            _save_state(run_state_json, state)

        optimizer.on_call_complete = _on_bo_call_complete

        partial_rows, bo_done, bo_total = sync_trials_partial_from_checkpoint(
            result_json,
            trials_partial_csv,
            run_id=run_id,
            model_idx=idx,
            model_name=model_name,
            train_csv=paths.train_csv,
            eval_csv=paths.eval_csv,
            test_csv=paths.test_csv,
            seed=opt_seed,
            stability_score=stability_score,
        )
        if partial_rows:
            logger.info(
                "Recovered %d partial BO trial(s) from checkpoint (%d/%d calls): %s",
                len(partial_rows),
                bo_done,
                number_of_calls,
                trials_partial_csv,
            )
        _mark_model(
            state,
            model_name,
            status="running",
            details={
                "embedding_cache_file": str(cache_file),
                "embedding_cache_hit": cache_hit,
                "optimization_dir": str(optimization_dir),
                "bo_calls_done": bo_done,
                "bo_calls_total": number_of_calls,
                "trials_partial_csv": str(trials_partial_csv),
            },
        )
        _save_state(run_state_json, state)

        result = _optimize_with_resume(
            optimizer,
            model=model,
            octis_dataset=octis_dataset,
            npmi_metric=npmi_metric,
            search_space=search_space,
            optimization_dir=optimization_dir,
            number_of_calls=number_of_calls,
            model_runs=int(cfg["optimization"].get("model_runs", 1)),
            save_models=bool(cfg["optimization"].get("save_models", False)),
            diversity_metric=diversity_metric,
            random_state=opt_seed,
            logger=logger,
        )

        _, bo_done, bo_total = sync_trials_partial_from_checkpoint(
            result_json,
            trials_partial_csv,
            run_id=run_id,
            model_idx=idx,
            model_name=model_name,
            train_csv=paths.train_csv,
            eval_csv=paths.eval_csv,
            test_csv=paths.test_csv,
            seed=opt_seed,
            stability_score=stability_score,
        )

        best_params = _best_params_from_optimize_result(result, optimization_dir)
        if not best_params:
            best_params = {}

        output = model.train_model(dataset=octis_dataset, hyperparameters=best_params)
        topics = _topics_from_output(output.get("topics"))
        coherence, diversity = _compute_metrics(topics, tokens_eval)
        outlier_rate = _safe_outlier_rate(output.get("topic-document-matrix", np.zeros((1, 1))))
        stability_score = float(cfg["optimization"].get("default_stability_score", 0.0))

        row: dict[str, Any] = {
            "run_id": run_id,
            "trial_id": f"{run_id}_{idx}",
            "seed": opt_seed,
            "embedding_model": model_name,
            "coherence_c_v": coherence,
            "coherence_c_npmi": np.nan,
            "topic_diversity": diversity,
            "outlier_rate": outlier_rate,
            "n_topics": len(topics),
            "stability_score": stability_score,
            "train_csv": str(paths.train_csv),
            "eval_csv": str(paths.eval_csv),
            "test_csv": str(paths.test_csv),
        }
        row.update(best_params)
        trials_by_model[model_name] = row
        _write_trials(trials_csv, list(trials_by_model.values()))

        model_duration = time.perf_counter() - model_step_start
        _mark_model(
            state,
            model_name,
            status="completed",
            duration_s=model_duration,
            details={
                "trial_id": row["trial_id"],
                "optimization_dir": str(optimization_dir),
                "coherence_c_v": coherence,
                "topic_diversity": diversity,
                "outlier_rate": outlier_rate,
                "bo_calls_done": bo_done,
                "bo_calls_total": bo_total,
                "trials_partial_csv": str(trials_partial_csv),
            },
        )
        _save_state(run_state_json, state)
        logger.info(
            "Completed %s in %.2fs (coherence=%.4f diversity=%.4f outlier=%.4f)",
            model_name,
            model_duration,
            coherence,
            diversity,
            outlier_rate,
        )

        manifest_payload = {
            "run_id": run_id,
            "updated_at": _utc_now(),
            "trials": len(trials_by_model),
            "selected_models": selected_models,
            "completed_models": [
                name for name, meta in state.get("models", {}).items() if meta.get("status") == "completed"
            ],
            "skipped_models": [
                name for name, meta in state.get("models", {}).items() if meta.get("status") == "skipped"
            ],
            "trials_csv": str(trials_csv),
            "run_state_json": str(run_state_json),
            "run_summary_json": str(run_summary_json),
            "log_file": str(log_file),
        }
        _write_json(manifest_json, manifest_payload)

    _mark_step(
        state,
        "manifest_write",
        status="completed",
        duration_s=time.perf_counter() - started_at,
        details={"manifest_json": str(manifest_json)},
    )
    state["completed"] = True
    _save_state(run_state_json, state)

    final_manifest = {
        "run_id": run_id,
        "completed_at": _utc_now(),
        "trials": len(trials_by_model),
        "selected_models": selected_models,
        "completed_models": [
            name for name, meta in state.get("models", {}).items() if meta.get("status") == "completed"
        ],
        "skipped_models": [
            name for name, meta in state.get("models", {}).items() if meta.get("status") == "skipped"
        ],
        "trials_csv": str(trials_csv),
        "run_state_json": str(run_state_json),
        "run_summary_json": str(run_summary_json),
        "log_file": str(log_file),
    }
    _write_json(manifest_json, final_manifest)
    _write_json(
        run_summary_json,
        {
            "run_id": run_id,
            "started_at": state.get("started_at"),
            "finished_at": _utc_now(),
            "elapsed_s": round(time.perf_counter() - started_at, 3),
            "steps": state.get("steps", {}),
            "models": state.get("models", {}),
            "artifacts": {
                "trials_csv": str(trials_csv),
                "run_manifest_json": str(manifest_json),
                "run_state_json": str(run_state_json),
                "log_file": str(log_file),
            },
        },
    )
    logger.info("Stage03 run finished in %.2fs. trials.csv=%s", time.perf_counter() - started_at, trials_csv)
    return trials_csv

