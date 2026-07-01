"""Regression tests for Stage03 run_state resume gating."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.stage03_train.tune import (
    _data_load_cache_valid,
    _load_state,
    _step_completed,
    _write_trials,
)


def _model_should_skip(
    state: dict,
    model_name: str,
    trials_by_model: dict[str, dict],
) -> bool:
    """Mirror the skip gate in ``run_tuning`` for unit testing."""
    model_state = state.get("models", {}).get(model_name, {})
    return model_state.get("status") in {"completed", "skipped"} and model_name in trials_by_model


class RunStateResumeTests(unittest.TestCase):
    def test_step_completed(self) -> None:
        state = {"steps": {"octis_corpus_written": {"status": "completed"}}}
        self.assertTrue(_step_completed(state, "octis_corpus_written"))
        self.assertFalse(_step_completed(state, "data_load"))

    def test_data_load_cache_valid_requires_paths(self) -> None:
        train = Path("/data/train.csv")
        eval_csv = Path("/data/eval.csv")
        state = {
            "steps": {
                "data_load": {
                    "status": "completed",
                    "details": {
                        "train_csv": str(train),
                        "eval_csv": str(eval_csv),
                        "csv_chunk_size": 50_000,
                        "n_train_docs": 100,
                        "n_eval_docs": 20,
                    },
                }
            }
        }
        self.assertTrue(
            _data_load_cache_valid(state, train_csv=train, eval_csv=eval_csv, chunk_size=50_000)
        )
        self.assertFalse(
            _data_load_cache_valid(
                state, train_csv=Path("/other/train.csv"), eval_csv=eval_csv, chunk_size=50_000
            )
        )

    def test_model_skip_when_completed_and_in_trials(self) -> None:
        model = "sentence-transformers/all-MiniLM-L12-v2"
        state = {"models": {model: {"status": "completed"}}}
        trials = {model: {"embedding_model": model, "coherence_c_v": 0.5}}
        self.assertTrue(_model_should_skip(state, model, trials))

    def test_model_not_skipped_when_running_without_trials_row(self) -> None:
        model = "sentence-transformers/all-MiniLM-L12-v2"
        state = {"models": {model: {"status": "running", "details": {"bo_calls_done": 2}}}}
        self.assertFalse(_model_should_skip(state, model, {}))

    def test_load_state_wrong_run_id_resets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "run_state.json"
            path.write_text('{"run_id": "other", "steps": {}, "models": {}}', encoding="utf-8")
            state = _load_state(path, "expected")
            self.assertEqual(state["run_id"], "expected")
            self.assertFalse(state.get("steps"))

    def test_trials_csv_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "trials.csv"
            rows = [
                {
                    "run_id": "r1",
                    "trial_id": "r1_1",
                    "embedding_model": "m1",
                    "coherence_c_v": 0.5,
                }
            ]
            _write_trials(csv_path, rows)
            loaded = pd.read_csv(csv_path).to_dict(orient="records")
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0]["embedding_model"], "m1")


if __name__ == "__main__":
    unittest.main()
