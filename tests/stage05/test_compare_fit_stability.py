"""Unit tests for compare-fit stability gating (mocked fits, no GPU)."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from src.stage05_final_fit import compare_fit


class CompareFitMinDfCoercionTests(unittest.TestCase):
    def test_coerce_integer_min_df_from_float_whole_number(self) -> None:
        self.assertEqual(compare_fit._coerce_vectorizer_min_df(19.0), 19)
        self.assertIsInstance(compare_fit._coerce_vectorizer_min_df(19.0), int)

    def test_coerce_legacy_proportional_min_df(self) -> None:
        self.assertAlmostEqual(
            compare_fit._coerce_vectorizer_min_df(0.01485), 0.01485
        )


class CompareFitProbabilitiesFlagTests(unittest.TestCase):
    def test_read_calculate_probabilities_default_false(self) -> None:
        self.assertFalse(compare_fit._read_calculate_probabilities({}))

    def test_read_calculate_probabilities_from_config(self) -> None:
        cfg = {"bertopic": {"calculate_probabilities": True}}
        self.assertTrue(compare_fit._read_calculate_probabilities(cfg))
        cfg_false = {"bertopic": {"calculate_probabilities": False}}
        self.assertFalse(compare_fit._read_calculate_probabilities(cfg_false))


class CompareFitStabilityTests(unittest.TestCase):
    def test_run_stability_check_pass(self) -> None:
        with patch.object(compare_fit, "_fit_bertopic", return_value=MagicMock()):
            with patch.object(compare_fit, "_count_topics", side_effect=[36, 37, 35]):
                report, model = compare_fit._run_stability_check(
                    MagicMock(),
                    {"umap__n_neighbors": 18},
                    ["doc one", "doc two"],
                    np.zeros((2, 8), dtype=np.float32),
                    bo_call=117,
                    reported_n_topics=37.0,
                    n_runs=3,
                    seed=42,
                    max_std=3.0,
                    collapse_ratio=0.5,
                )
        self.assertTrue(report["stability_pass"])
        self.assertFalse(report["refit_collapse"])
        self.assertAlmostEqual(report["stats"]["median"], 36.0)
        self.assertIsNotNone(model)

    def test_run_stability_check_collapse(self) -> None:
        with patch.object(compare_fit, "_fit_bertopic", return_value=MagicMock()):
            with patch.object(compare_fit, "_count_topics", side_effect=[45, 2, 44]):
                report, _model = compare_fit._run_stability_check(
                    MagicMock(),
                    {"umap__n_neighbors": 14},
                    ["doc"],
                    np.zeros((1, 8), dtype=np.float32),
                    bo_call=3,
                    reported_n_topics=45.0,
                    n_runs=3,
                    seed=42,
                    max_std=3.0,
                    collapse_ratio=0.5,
                )
        self.assertFalse(report["topic_stability_pass"])
        self.assertFalse(report["stability_pass"])

    def test_run_stability_check_refit_collapse_vs_bo(self) -> None:
        with patch.object(compare_fit, "_fit_bertopic", return_value=MagicMock()):
            with patch.object(compare_fit, "_count_topics", side_effect=[2, 3, 2]):
                report, _model = compare_fit._run_stability_check(
                    MagicMock(),
                    {"umap__n_neighbors": 14},
                    ["doc"],
                    np.zeros((1, 8), dtype=np.float32),
                    bo_call=3,
                    reported_n_topics=45.0,
                    n_runs=3,
                    seed=42,
                    max_std=3.0,
                    collapse_ratio=0.5,
                )
        self.assertTrue(report["refit_collapse"])
        self.assertFalse(report["stability_pass"])


if __name__ == "__main__":
    unittest.main()
