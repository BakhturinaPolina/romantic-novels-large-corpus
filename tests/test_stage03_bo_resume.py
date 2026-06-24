"""Regression tests for Stage03 BO checkpoint/resume helpers."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.stage03_train.bo_resume import (
    best_params_from_bo,
    bo_calls_done,
    build_bo_resume_seed,
    is_bo_complete,
    load_bo_checkpoint,
    project_result_to_trials,
    sync_trials_partial_from_checkpoint,
    write_trials_partial_csv,
)


def _sample_payload(*, n_calls: int = 2, total: int = 5) -> dict:
    return {
        "metric_name": "Coherence",
        "extra_metric_names": ["0_TopicDiversity"],
        "number_of_call": total,
        "current_call": n_calls - 1,
        "f_val": [0.4 + 0.1 * i for i in range(n_calls)],
        "x_iters": {
            "umap__n_neighbors": [11 + i for i in range(n_calls)],
            "umap__n_components": [4 + i for i in range(n_calls)],
            "vectorizer__min_df": [0.01 * (i + 1) for i in range(n_calls)],
        },
        "dict_model_runs": {
            "Coherence": {f"iteration_{i}": [0.4 + 0.1 * i] for i in range(n_calls)},
            "0_TopicDiversity": {f"iteration_{i}": [0.5 + 0.05 * i] for i in range(n_calls)},
        },
    }


class BoResumeTests(unittest.TestCase):
    def test_build_bo_resume_seed_shape_and_sign(self) -> None:
        payload = _sample_payload(n_calls=3)
        x0, y0, k = build_bo_resume_seed(payload)
        self.assertEqual(k, 3)
        self.assertEqual(len(y0), 3)
        self.assertAlmostEqual(y0[0], 0.4)
        self.assertAlmostEqual(y0[1], 0.5)
        self.assertAlmostEqual(y0[2], 0.6)
        self.assertEqual(set(x0.keys()), set(payload["x_iters"].keys()))
        for name in x0:
            self.assertEqual(len(x0[name]), 3)

    def test_is_bo_complete(self) -> None:
        payload = _sample_payload(n_calls=5, total=5)
        self.assertTrue(is_bo_complete(payload, number_of_calls=5))
        self.assertFalse(is_bo_complete(_sample_payload(n_calls=2, total=5), number_of_calls=5))

    def test_best_params_from_bo_picks_max(self) -> None:
        payload = _sample_payload(n_calls=3)
        best = best_params_from_bo(payload)
        self.assertEqual(best["umap__n_neighbors"], 13)

    def test_project_result_to_trials_round_trip(self) -> None:
        payload = _sample_payload(n_calls=2, total=5)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = project_result_to_trials(
                payload,
                run_id="smoke_run",
                model_idx=1,
                model_name="sentence-transformers/all-MiniLM-L12-v2",
                train_csv=root / "train.csv",
                eval_csv=root / "eval.csv",
                test_csv=root / "test.csv",
                seed=42,
                stability_score=0.0,
            )
            self.assertEqual(len(rows), 2)
            required = {
                "run_id",
                "trial_id",
                "embedding_model",
                "coherence_c_v",
                "topic_diversity",
                "umap__n_neighbors",
            }
            self.assertTrue(required.issubset(rows[0].keys()))
            self.assertEqual(rows[0]["bo_call"], 0)
            self.assertEqual(rows[1]["bo_call"], 1)

            partial_csv = root / "trials_partial.csv"
            write_trials_partial_csv(partial_csv, rows)
            df = pd.read_csv(partial_csv)
            self.assertEqual(len(df), 2)

    def test_sync_idempotent_on_reproject(self) -> None:
        payload = _sample_payload(n_calls=2, total=5)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result_json = root / "result.json"
            partial_csv = root / "trials_partial.csv"
            with open(result_json, "w", encoding="utf-8") as f:
                json.dump(payload, f)

            rows1, done1, total1 = sync_trials_partial_from_checkpoint(
                result_json,
                partial_csv,
                run_id="smoke_run",
                model_idx=1,
                model_name="sentence-transformers/all-MiniLM-L12-v2",
                train_csv=root / "train.csv",
                eval_csv=root / "eval.csv",
                test_csv=root / "test.csv",
                seed=42,
                stability_score=0.0,
            )
            rows2, done2, total2 = sync_trials_partial_from_checkpoint(
                result_json,
                partial_csv,
                run_id="smoke_run",
                model_idx=1,
                model_name="sentence-transformers/all-MiniLM-L12-v2",
                train_csv=root / "train.csv",
                eval_csv=root / "eval.csv",
                test_csv=root / "test.csv",
                seed=42,
                stability_score=0.0,
            )
            self.assertEqual(len(rows1), 2)
            self.assertEqual(rows1, rows2)
            self.assertEqual(done1, 2)
            self.assertEqual(total1, 5)
            self.assertEqual(done2, 2)
            self.assertEqual(total2, 5)
            self.assertEqual(len(pd.read_csv(partial_csv)), 2)

    def test_load_bo_checkpoint_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(load_bo_checkpoint(Path(tmp) / "missing.json"))

    def test_bo_calls_done_from_f_val(self) -> None:
        self.assertEqual(bo_calls_done(_sample_payload(n_calls=4)), 4)

    def test_project_result_with_topic_penalty_extras(self) -> None:
        payload = {
            "metric_name": "CoherenceWithTopicPenalty",
            "extra_metric_names": [
                "0_TopicDiversity",
                "1_TopicCount",
                "2_RawCoherence",
            ],
            "number_of_call": 3,
            "current_call": 1,
            "f_val": [0.33, 0.41],
            "x_iters": {"umap__n_neighbors": [11, 24]},
            "dict_model_runs": {
                "CoherenceWithTopicPenalty": {
                    "iteration_0": [0.33],
                    "iteration_1": [0.41],
                },
                "0_TopicDiversity": {"iteration_0": [0.9], "iteration_1": [0.85]},
                "1_TopicCount": {"iteration_0": [2.0], "iteration_1": [25.0]},
                "2_RawCoherence": {"iteration_0": [0.48], "iteration_1": [0.44]},
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = project_result_to_trials(
                payload,
                run_id="v2_run",
                model_idx=1,
                model_name="sentence-transformers/all-MiniLM-L12-v2",
                train_csv=root / "train.csv",
                eval_csv=root / "eval.csv",
                test_csv=root / "test.csv",
                seed=42,
                stability_score=0.0,
            )
        self.assertEqual(len(rows), 2)
        self.assertAlmostEqual(rows[0]["coherence_c_v"], 0.48)
        self.assertAlmostEqual(rows[0]["bo_objective"], 0.33)
        self.assertAlmostEqual(rows[0]["n_topics"], 2.0)
        self.assertAlmostEqual(rows[1]["coherence_c_v"], 0.44)
        self.assertAlmostEqual(rows[1]["bo_objective"], 0.41)
        self.assertAlmostEqual(rows[1]["n_topics"], 25.0)

    def test_project_result_with_multi_run_topic_stability(self) -> None:
        payload = {
            "metric_name": "CoherenceWithTopicPenalty",
            "extra_metric_names": [
                "0_TopicDiversity",
                "1_TopicCount",
                "2_RawCoherence",
            ],
            "number_of_call": 3,
            "current_call": 0,
            "f_val": [0.55],
            "x_iters": {"umap__n_neighbors": [18]},
            "dict_model_runs": {
                "CoherenceWithTopicPenalty": {"iteration_0": [0.55, 0.54, 0.56]},
                "0_TopicDiversity": {"iteration_0": [0.9, 0.88, 0.91]},
                "1_TopicCount": {"iteration_0": [36.0, 37.0, 35.0]},
                "2_RawCoherence": {"iteration_0": [0.62, 0.61, 0.63]},
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = project_result_to_trials(
                payload,
                run_id="v3_run",
                model_idx=1,
                model_name="sentence-transformers/all-MiniLM-L12-v2",
                train_csv=root / "train.csv",
                eval_csv=root / "eval.csv",
                test_csv=root / "test.csv",
                seed=42,
                stability_score=0.0,
                topic_stability_cfg={
                    "max_n_topics_std": 3.0,
                    "collapse_ratio": 0.5,
                },
            )
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["n_topics"], 36.0)
        self.assertAlmostEqual(rows[0]["n_topics_min"], 35.0)
        self.assertAlmostEqual(rows[0]["n_topics_max"], 37.0)
        self.assertAlmostEqual(rows[0]["n_topics_std"], 0.816496580927726, places=5)
        self.assertEqual(rows[0]["n_topics_runs"], 3)
        self.assertTrue(rows[0]["topic_stability_pass"])

    def test_project_result_with_granular_extra_metrics(self) -> None:
        payload = {
            "metric_name": "CoherenceWithTopicPenalty",
            "extra_metric_names": [
                "0_TopicDiversity",
                "1_TopicCount",
                "2_RawCoherence",
                "3_OutlierRate",
                "4_LargestTopicShare",
                "5_MedianTopicSize",
                "6_P10TopicSize",
                "7_P90TopicSize",
                "8_TinyTopicsLt25",
                "9_TinyTopicsLt50",
            ],
            "number_of_call": 2,
            "current_call": 1,
            "f_val": [0.5, 0.55],
            "x_iters": {
                "vectorizer__min_df": [5, 8],
                "hdbscan__cluster_selection_method": ["eom", "leaf"],
            },
            "dict_model_runs": {
                "CoherenceWithTopicPenalty": {"iteration_0": [0.5], "iteration_1": [0.55]},
                "0_TopicDiversity": {"iteration_0": [0.9], "iteration_1": [0.88]},
                "1_TopicCount": {"iteration_0": [120.0], "iteration_1": [250.0]},
                "2_RawCoherence": {"iteration_0": [0.6], "iteration_1": [0.62]},
                "3_OutlierRate": {"iteration_0": [0.12], "iteration_1": [0.15]},
                "4_LargestTopicShare": {"iteration_0": [0.08], "iteration_1": [0.06]},
                "5_MedianTopicSize": {"iteration_0": [80.0], "iteration_1": [95.0]},
                "6_P10TopicSize": {"iteration_0": [30.0], "iteration_1": [35.0]},
                "7_P90TopicSize": {"iteration_0": [200.0], "iteration_1": [220.0]},
                "8_TinyTopicsLt25": {"iteration_0": [5.0], "iteration_1": [3.0]},
                "9_TinyTopicsLt50": {"iteration_0": [10.0], "iteration_1": [8.0]},
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = project_result_to_trials(
                payload,
                run_id="v4_run",
                model_idx=1,
                model_name="sentence-transformers/all-MiniLM-L12-v2",
                train_csv=root / "train.csv",
                eval_csv=root / "eval.csv",
                test_csv=root / "test.csv",
                seed=42,
                stability_score=0.0,
            )
        self.assertEqual(len(rows), 2)
        self.assertAlmostEqual(rows[0]["outlier_rate"], 0.12)
        self.assertAlmostEqual(rows[0]["largest_topic_share"], 0.08)
        self.assertAlmostEqual(rows[0]["median_topic_size"], 80.0)
        self.assertAlmostEqual(rows[0]["n_tiny_topics_lt25"], 5.0)
        self.assertEqual(rows[0]["vectorizer__min_df"], 5)
        self.assertEqual(rows[1]["hdbscan__cluster_selection_method"], "leaf")

    def test_project_result_single_run_topic_std_is_zero(self) -> None:
        payload = {
            "metric_name": "Coherence",
            "extra_metric_names": ["0_TopicCount"],
            "number_of_call": 1,
            "current_call": 0,
            "f_val": [0.5],
            "x_iters": {"umap__n_neighbors": [12]},
            "dict_model_runs": {
                "Coherence": {"iteration_0": [0.5]},
                "0_TopicCount": {"iteration_0": [42.0]},
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = project_result_to_trials(
                payload,
                run_id="single_run",
                model_idx=1,
                model_name="sentence-transformers/all-MiniLM-L12-v2",
                train_csv=root / "train.csv",
                eval_csv=root / "eval.csv",
                test_csv=root / "test.csv",
                seed=42,
                stability_score=0.0,
            )
        self.assertEqual(rows[0]["n_topics_runs"], 1)
        self.assertAlmostEqual(rows[0]["n_topics_std"], 0.0)
        self.assertNotIn("coherence_c_npmi", rows[0])
        self.assertNotIn("outlier_rate", rows[0])


if __name__ == "__main__":
    unittest.main()
