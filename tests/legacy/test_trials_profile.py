"""Tests for type-aware trials_partial.csv profiling."""

from __future__ import annotations

import unittest

import pandas as pd

from src.legacy.stage04_selection.trials_profile import (
    TRIALS_COLUMN_ROLES,
    normalize_trials_partial_df,
    summarize_trials_by_role,
    trials_schema_overview,
)


def _sample_trials(n: int = 5) -> pd.DataFrame:
    rows = []
    for i in range(n):
        rows.append(
            {
                "run_id": "run_a",
                "trial_id": f"run_a_1_call_{i}",
                "bo_call": i,
                "seed": 42,
                "embedding_model": "sentence-transformers/all-MiniLM-L12-v2",
                "coherence_c_v": 0.5 + i * 0.01,
                "bo_objective": 0.4 + i * 0.01,
                "topic_diversity": 0.7,
                "n_topics": 10 + i,
                "stability_score": 0.0,
                "train_csv": "/tmp/train.csv",
                "eval_csv": "/tmp/eval.csv",
                "test_csv": "/tmp/test.csv",
                "n_topics_min": 10 + i,
                "n_topics_max": 10 + i,
                "n_topics_std": 0.0,
                "n_topics_runs": 1,
                "topic_stability_pass": True,
                "bertopic__min_topic_size": 100 + i,
                "bertopic__top_n_words": 30,
                "hdbscan__min_cluster_size": 50,
                "hdbscan__min_samples": 5,
                "umap__min_dist": 0.05,
                "umap__n_components": 10,
                "umap__n_neighbors": 15,
                "vectorizer__min_df": 0.005,
            }
        )
    return pd.DataFrame(rows)


class TestTrialsProfile(unittest.TestCase):
    def test_schema_covers_all_expected_columns(self) -> None:
        df = _sample_trials()
        self.assertEqual(set(TRIALS_COLUMN_ROLES.keys()), set(df.columns))

    def test_normalize_drops_deprecated_empty_columns(self) -> None:
        df = _sample_trials()
        df["coherence_c_npmi"] = float("nan")
        df["outlier_rate"] = float("nan")
        cleaned = normalize_trials_partial_df(df)
        self.assertNotIn("coherence_c_npmi", cleaned.columns)
        self.assertNotIn("outlier_rate", cleaned.columns)

    def test_bo_index_summary_is_not_distribution(self) -> None:
        df = _sample_trials()
        bo = summarize_trials_by_role(df)["bo_index"]
        self.assertNotIn("mean", bo.columns)
        self.assertTrue(bo.loc[0, "sequential_0_to_n_minus_1"])

    def test_bo_run_count_uses_value_counts_not_distribution(self) -> None:
        df = _sample_trials()
        summary = summarize_trials_by_role(df)["bo_run_count"]
        self.assertIn("model_runs_per_bo_call", summary.columns)
        self.assertNotIn("mean", summary.columns)
        self.assertEqual(int(summary.iloc[0]["trial_count"]), 5)

    def test_stability_std_skips_distribution_for_single_run(self) -> None:
        df = _sample_trials()
        summary = summarize_trials_by_role(df)["stability_std"]
        self.assertIn("note", summary.columns)
        self.assertNotIn("mean", summary.columns)

    def test_metrics_have_distribution_stats(self) -> None:
        df = _sample_trials()
        metrics = summarize_trials_by_role(df)["metrics"]
        row = metrics.loc[metrics["column"] == "coherence_c_v"].iloc[0]
        self.assertEqual(row["non_null"], 5)
        self.assertAlmostEqual(row["min"], 0.5)

    def test_overview_row_count_matches_columns(self) -> None:
        df = _sample_trials()
        overview = trials_schema_overview(df)
        self.assertEqual(len(overview), df.shape[1])


if __name__ == "__main__":
    unittest.main()
