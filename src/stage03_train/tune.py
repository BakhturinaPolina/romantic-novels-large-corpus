"""Stage 03 train/eval tuning workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
from octis.dataset.dataset import Dataset
from octis.evaluation_metrics.coherence_metrics import Coherence
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
from octis.optimization.optimizer import Optimizer
from skopt.space.space import Integer, Real

from src.common.config import load_config, resolve_path
from src.stage03_train.bertopic_octis_model import (
    BERTopicOctisModelWithEmbeddings,
    load_embedding_model,
)
from src.stage03_train.data_io import load_train_eval
from src.stage03_train.embeddings import load_or_compute_embeddings
from src.stage03_train.octis_corpus import write_octis_corpus


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


def _compute_metrics(topics: list[list[str]], eval_tokens: list[list[str]]) -> tuple[float, float]:
    if not topics:
        return 0.0, 0.0
    dictionary = Dictionary(eval_tokens)
    topics_in_vocab = [[w for w in topic if w in dictionary.token2id] for topic in topics]
    topics_in_vocab = [t for t in topics_in_vocab if t]
    if not topics_in_vocab:
        coherence = 0.0
    else:
        cm = CoherenceModel(
            topics=topics_in_vocab, texts=eval_tokens, dictionary=dictionary, coherence="c_v"
        )
        coherence = float(cm.get_coherence())
    diversity = float(TopicDiversity(topk=10).score({"topics": topics}))
    return coherence, diversity


def run_tuning(config_path: Path, run_id: str) -> Path:
    """Execute tuning and return trials.csv path."""
    cfg = load_config(config_path)
    paths_cfg = load_config(Path("configs/paths.yaml"))
    paths = _build_paths(paths_cfg, run_id)

    payload = load_train_eval(paths.train_csv, paths.eval_csv, sentence_column=cfg["text"]["sentence_column"])
    docs_train = payload["docs_train"]
    docs_eval = payload["docs_eval"]
    labels_train = payload["labels_train"]
    labels_eval = payload["labels_eval"]
    tokens_eval = payload["tokens_eval"]

    paths.octis_dir.mkdir(parents=True, exist_ok=True)
    paths.experiments_dir.mkdir(parents=True, exist_ok=True)
    write_octis_corpus(docs_train, labels_train, docs_eval, labels_eval, paths.octis_dir)

    octis_dataset = Dataset()
    octis_dataset.load_custom_dataset_from_folder(str(paths.octis_dir))

    docs_all = docs_train + docs_eval
    tokens_all = [d.split() for d in docs_all]
    trials: list[dict[str, Any]] = []
    search_space = build_search_space(cfg)

    for idx, model_name in enumerate(cfg["embedding_models"], start=1):
        cache_dir = paths.octis_dir / "embeddings_cache"
        emb = load_or_compute_embeddings(
            docs_all,
            model_name=model_name,
            cache_dir=cache_dir,
            split="train_eval",
            device=cfg.get("device", "auto"),
            batch_size=int(cfg.get("embedding_batch_size", 256)),
        )
        model = BERTopicOctisModelWithEmbeddings(
            embedding_model=load_embedding_model(model_name),
            embedding_model_name=model_name,
            embeddings=emb,
            dataset_as_list_of_strings=docs_all,
            dataset_as_list_of_lists=tokens_all,
            optimization_results_dir=str(paths.experiments_dir / "optimization"),
            verbose=True,
        )
        model.use_partitions = True

        optimizer = Optimizer()
        npmi_metric = Coherence(texts=[t for t in tokens_eval if t], topk=10, measure="c_v")
        diversity_metric = TopicDiversity(topk=10)
        result = optimizer.optimize(
            model,
            octis_dataset,
            npmi_metric,
            search_space,
            number_of_call=int(cfg["optimization"]["number_of_calls"]),
            model_runs=int(cfg["optimization"].get("model_runs", 1)),
            save_models=True,
            extra_metrics=[diversity_metric],
            save_path=str(paths.experiments_dir / f"opt_{idx}_{model_name.replace('/', '__')}"),
        )

        best_params = {}
        if isinstance(result, dict):
            best_params = result.get("best_params", {}) or result.get("x", {}) or {}
        if not best_params:
            best_params = {}

        output = model.train_model(dataset=octis_dataset, hyperparameters=best_params)
        topics = _topics_from_output(output.get("topics"))
        coherence, diversity = _compute_metrics(topics, tokens_eval)
        outlier_rate = float(np.mean(np.max(output.get("topic-document-matrix", np.zeros((1, 1))), axis=1) == 0))
        stability_score = float(cfg["optimization"].get("default_stability_score", 0.0))

        row: dict[str, Any] = {
            "run_id": run_id,
            "trial_id": f"{run_id}_{idx}",
            "seed": int(cfg["optimization"].get("seed", 42)),
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
        trials.append(row)

    df = pd.DataFrame(trials)
    trials_csv = paths.experiments_dir / "trials.csv"
    df.to_csv(trials_csv, index=False)
    with open(paths.experiments_dir / "run_manifest.json", "w", encoding="utf-8") as f:
        json.dump({"run_id": run_id, "trials": len(df), "trials_csv": str(trials_csv)}, f, indent=2)
    return trials_csv

