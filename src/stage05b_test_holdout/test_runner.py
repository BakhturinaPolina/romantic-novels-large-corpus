"""One-shot holdout scoring on the test split."""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from bertopic import BERTopic
from gensim.corpora import Dictionary

from src.common.config import load_config, resolve_path
from src.stage03_train.data_io import iter_split_csv_chunks
from src.stage03_train.tune import _coherence_cv, _diversity_adaptive
from src.stage05_final_fit.chunked_transform import streaming_transform_metrics

LOGGER = logging.getLogger("stage05b_holdout")


def ensure_one_shot(output_metrics_json: Path, allow_rerun: bool = False) -> None:
    """Prevent accidental repeated test scoring."""
    if output_metrics_json.exists() and not allow_rerun:
        raise RuntimeError(
            f"Refusing to rerun holdout scoring because metrics file already exists: {output_metrics_json}. "
            "Pass --allow-rerun to override."
        )


def _load_model(final_model_dir: Path) -> BERTopic:
    """Load a BERTopic native artifact from a final-fit or compare-fit directory."""
    candidates = sorted([p for p in final_model_dir.rglob("model_*") if p.is_dir()])
    if not candidates:
        raise FileNotFoundError(f"No BERTopic native model directory found under {final_model_dir}")
    return BERTopic.load(candidates[0])


def _extract_topics(topic_model: BERTopic, top_k: int = 10) -> list[list[str]]:
    topics = []
    if not hasattr(topic_model, "topic_representations_") or not topic_model.topic_representations_:
        return topics
    for tid, items in topic_model.topic_representations_.items():
        if tid == -1:
            continue
        words = []
        for it in items[:top_k]:
            if isinstance(it, tuple) and len(it) > 0:
                words.append(str(it[0]))
            elif isinstance(it, str):
                words.append(it)
        words = [w for w in words if w]
        if words:
            topics.append(words)
    return topics


def _iter_test_doc_batches(
    test_csv: Path,
    *,
    chunk_size: int = 50_000,
    sentence_column: str = "sentence",
) -> Iterator[tuple[list[str], None]]:
    """Yield cleaned test docs in CSV chunks (no precomputed embeddings)."""
    for docs, _labels in iter_split_csv_chunks(
        test_csv,
        sentence_column=sentence_column,
        chunk_size=chunk_size,
    ):
        yield docs, None


def infer_on_test(
    final_model_dir: Path,
    test_csv: Path,
    *,
    batch_size: int = 8192,
    chunk_size: int = 50_000,
    coherence_max_docs: int = 100_000,
) -> dict[str, Any]:
    """Run chunked transform on test split and compute final metrics."""
    LOGGER.info("[HOLDOUT] loading model from %s", final_model_dir)
    topic_model = _load_model(final_model_dir)
    LOGGER.info(
        "[HOLDOUT] chunked test inference: csv=%s batch_size=%d chunk_size=%d coherence_cap=%d",
        test_csv,
        batch_size,
        chunk_size,
        coherence_max_docs,
    )

    partial, coherence_tokens = streaming_transform_metrics(
        topic_model,
        _iter_test_doc_batches(test_csv, chunk_size=chunk_size),
        batch_size=batch_size,
        coherence_max_docs=coherence_max_docs,
        logger=LOGGER,
    )

    topic_words = _extract_topics(topic_model, top_k=10)
    dictionary = Dictionary(coherence_tokens)
    topics_in_vocab = [[w for w in t if w in dictionary.token2id] for t in topic_words]
    topics_in_vocab = [t for t in topics_in_vocab if t]
    coherence_c_v = (
        _coherence_cv(topics_in_vocab, coherence_tokens, dictionary=dictionary)
        if topics_in_vocab and coherence_tokens
        else 0.0
    )
    coherence_c_npmi = 0.0
    if topics_in_vocab and coherence_tokens:
        from gensim.models import CoherenceModel

        coherence_c_npmi = float(
            CoherenceModel(
                topics=topics_in_vocab,
                texts=coherence_tokens,
                dictionary=dictionary,
                coherence="c_npmi",
            ).get_coherence()
        )
    topic_diversity = _diversity_adaptive(topic_words) if topic_words else 0.0

    LOGGER.info(
        "[HOLDOUT] done: n_topics=%d outlier=%.4f coherence=%.4f diversity=%.4f (coherence on %d docs)",
        len(topic_words),
        partial["outlier_rate"],
        coherence_c_v,
        topic_diversity,
        len(coherence_tokens),
    )

    return {
        "n_docs_test": int(partial["n_docs_test"]),
        "coherence_c_v": coherence_c_v,
        "coherence_c_npmi": coherence_c_npmi,
        "coherence_eval_docs": len(coherence_tokens),
        "topic_diversity": topic_diversity,
        "outlier_rate": float(partial["outlier_rate"]),
        "n_topics": len(topic_words),
        "avg_max_topic_prob": float(partial["avg_max_topic_prob"]),
    }


def write_test_report(metrics: dict[str, Any], output_md: Path) -> Path:
    output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Final Test Holdout Report",
        "",
        f"- Documents scored: `{metrics['n_docs_test']}`",
        f"- Coherence c_v: `{metrics['coherence_c_v']:.6f}` (evaluated on {metrics.get('coherence_eval_docs', metrics['n_docs_test'])} docs)",
        f"- Coherence c_npmi: `{metrics['coherence_c_npmi']:.6f}`",
        f"- Topic diversity: `{metrics['topic_diversity']:.6f}`",
        f"- Outlier rate: `{metrics['outlier_rate']:.6f}`",
        f"- Number of topics: `{metrics['n_topics']}`",
        f"- Avg max topic prob: `{metrics['avg_max_topic_prob']:.6f}`",
    ]
    output_md.write_text("\n".join(lines), encoding="utf-8")
    return output_md


def run_holdout_score(
    final_model_dir: Path,
    policy: str,
    run_id: str,
    allow_rerun: bool = False,
    *,
    bo_call: int | None = None,
    batch_size: int = 8192,
    chunk_size: int = 50_000,
    coherence_max_docs: int = 100_000,
) -> Path:
    """Main holdout scoring workflow."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )
    LOGGER.info("[HOLDOUT] start run_id=%s policy=%s bo_call=%s", run_id, policy, bo_call)
    paths_cfg = load_config(Path("configs/paths.yaml"))
    test_csv = resolve_path(Path(paths_cfg["inputs"]["sentences_test_csv"]))
    evaluation_root = resolve_path(Path(paths_cfg["outputs"]["evaluation"])) / run_id
    if bo_call is not None:
        evaluation_root = evaluation_root / f"call_{bo_call}"
    evaluation_root.mkdir(parents=True, exist_ok=True)

    metrics_json = evaluation_root / "test_metrics.json"
    ensure_one_shot(metrics_json, allow_rerun=allow_rerun)

    metrics = infer_on_test(
        final_model_dir,
        test_csv,
        batch_size=batch_size,
        chunk_size=chunk_size,
        coherence_max_docs=coherence_max_docs,
    )
    metrics["run_id"] = run_id
    metrics["model_policy"] = policy
    if bo_call is not None:
        metrics["bo_call"] = bo_call
    metrics["final_model_dir"] = str(final_model_dir)
    metrics["scored_at"] = datetime.utcnow().isoformat() + "Z"
    metrics["batch_size"] = batch_size
    metrics["chunk_size"] = chunk_size

    with open(metrics_json, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    write_test_report(metrics, evaluation_root / "final_topic_report.md")
    LOGGER.info("[HOLDOUT] wrote metrics to %s", metrics_json)
    return metrics_json
