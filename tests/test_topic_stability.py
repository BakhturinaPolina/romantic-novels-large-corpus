"""Unit tests for topic-count stability helpers."""

from __future__ import annotations

import unittest

from src.stage03_train.topic_stability import (
    refit_collapse_flag,
    stability_pass,
    stability_penalty,
    stability_violation,
    topic_run_stats,
)


class TopicStabilityTests(unittest.TestCase):
    def test_stable_counts_pass(self) -> None:
        counts = [36, 37, 35]
        self.assertTrue(stability_pass(counts, max_std=3.0, collapse_ratio=0.5))
        stats = topic_run_stats(counts)
        self.assertAlmostEqual(stats["median"], 36.0)
        self.assertAlmostEqual(stats["std"], 0.816496580927726, places=5)
        self.assertAlmostEqual(stability_violation(counts), 0.0)
        self.assertAlmostEqual(stability_penalty(0.62, counts, weight=0.2), 0.62)

    def test_collapse_fails(self) -> None:
        counts = [45, 2, 44]
        self.assertFalse(stability_pass(counts, max_std=3.0, collapse_ratio=0.5))
        self.assertGreater(stability_violation(counts), 0.0)
        self.assertLess(stability_penalty(0.65, counts, weight=0.2), 0.65)

    def test_high_variance_fails(self) -> None:
        counts = [10, 40, 35]
        self.assertFalse(stability_pass(counts, max_std=3.0, collapse_ratio=0.5))

    def test_single_run_legacy_passes(self) -> None:
        self.assertTrue(stability_pass([36]))
        self.assertAlmostEqual(stability_violation([36]), 0.0)

    def test_refit_collapse_flag(self) -> None:
        self.assertTrue(refit_collapse_flag(2.0, 45.0, collapse_ratio=0.5))
        self.assertFalse(refit_collapse_flag(36.0, 37.0, collapse_ratio=0.5))


if __name__ == "__main__":
    unittest.main()
