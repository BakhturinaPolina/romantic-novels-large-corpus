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


if __name__ == "__main__":
    unittest.main()
