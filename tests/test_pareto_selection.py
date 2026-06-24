"""Tests for pareto notebook -> Stage05 wiring."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.stage05_final_fit.pareto_selection import collect_bo_calls_from_pareto


class ParetoSelectionTests(unittest.TestCase):
    def test_collect_bo_calls_union(self) -> None:
        top_models_dir = Path("results/selection/v3_minilm12v2_first/notebook_analysis/top_models")
        if not top_models_dir.exists():
            self.skipTest("pareto top_models outputs not present")
        calls = collect_bo_calls_from_pareto(top_models_dir)
        self.assertEqual(calls, [36, 105, 117])


if __name__ == "__main__":
    unittest.main()
