"""One-shot holdout scoring on the test split."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from bertopic import BERTopic
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
from octis.evaluation_metrics.diversity_metrics import TopicDiversity

from src.common.config import load_config, resolve_path


def ensure_one_shot(output_metrics_json: Path, allow_rerun: bool = False) -> None:
    """Prevent accidental repeated test scoring."""
    if output_metrics_json.exists() and not allow_rerun:
        raise RuntimeError(
            f"Refusing to rerun holdout scoring because metrics file already exists: {output_metrics_json}. "
            "Pass --allow-rerun to override."
        )


def _load_model(final_model_dir: Path) -> BERTopic:
    # final fit stores a nested embedding folder; locate first model_* directory.
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


def infer_on_test(final_model_dir: Path, test_csv: Path) -> dict[str, Any]:
    """Run transform on test split and compute final metrics."""
    topic_model = _load_model(final_model_dir)
    df = pd.read_csv(test_csv)
    if "sentence" not in df.columns:
        raise ValueError(f"Expected `sentence` column in {test_csv}")
    docs = [" ".join(str(s).replace("\n", " ").split()).strip().lower() for s in df["sentence"].tolist()]
    docs = [d for d in docs if d]
    tokens = [d.split() for d in docs]
    topics_pred, probs = topic_model.transform(docs)

    outlier_rate = float(np.mean(np.array(topics_pred) == -1)) if len(topics_pred) else 0.0
    topic_words = _extract_topics(topic_model, top_k=10)
    dictionary = Dictionary(tokens)
    topics_in_vocab = [[w for w in t if w in dictionary.token2id] for t in topic_words]
    topics_in_vocab = [t for t in topics_in_vocab if t]
    coherence_c_v = 0.0
    coherence_c_npmi = 0.0
    if topics_in_vocab:
        coherence_c_v = float(
            CoherenceModel(topics=topics_in_vocab, texts=tokens, dictionary=dictionary, coherence="c_v").get_coherence()
        )
        coherence_c_npmi = float(
            CoherenceModel(topics=topics_in_vocab, texts=tokens, dictionary=dictionary, coherence="c_npmi").get_coherence()
        )
    topic_diversity = float(TopicDiversity(topk=10).score({"topics": topic_words})) if topic_words else 0.0

    return {
        "n_docs_test": len(docs),
        "coherence_c_v": coherence_c_v,
        "coherence_c_npmi": coherence_c_npmi,
        "topic_diversity": topic_diversity,
        "outlier_rate": outlier_rate,
        "n_topics": len(topic_words),
        "avg_max_topic_prob": float(np.max(probs, axis=1).mean()) if isinstance(probs, np.ndarray) and probs.size else 0.0,
    }


def write_test_report(metrics: dict[str, Any], output_md: Path) -> Path:
    output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Final Test Holdout Report",
        "",
        f"- Documents scored: `{metrics['n_docs_test']}`",
        f"- Coherence c_v: `{metrics['coherence_c_v']:.6f}`",
        f"- Coherence c_npmi: `{metrics['coherence_c_npmi']:.6f}`",
        f"- Topic diversity: `{metrics['topic_diversity']:.6f}`",
        f"- Outlier rate: `{metrics['outlier_rate']:.6f}`",
        f"- Number of topics: `{metrics['n_topics']}`",
    ]
    output_md.write_text("\n".join(lines), encoding="utf-8")
    return output_md


def run_holdout_score(
    final_model_dir: Path,
    policy: str,
    run_id: str,
    allow_rerun: bool = False,
) -> Path:
    """Main holdout scoring workflow."""
    paths_cfg = load_config(Path("configs/paths.yaml"))
    test_csv = resolve_path(Path(paths_cfg["inputs"]["sentences_test_csv"]))
    evaluation_root = resolve_path(Path(paths_cfg["outputs"]["evaluation"])) / run_id
    evaluation_root.mkdir(parents=True, exist_ok=True)

    metrics_json = evaluation_root / "test_metrics.json"
    ensure_one_shot(metrics_json, allow_rerun=allow_rerun)

    metrics = infer_on_test(final_model_dir, test_csv)
    metrics["run_id"] = run_id
    metrics["model_policy"] = policy
    metrics["scored_at"] = datetime.utcnow().isoformat() + "Z"

    with open(metrics_json, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    write_test_report(metrics, evaluation_root / "final_topic_report.md")
    return metrics_json

