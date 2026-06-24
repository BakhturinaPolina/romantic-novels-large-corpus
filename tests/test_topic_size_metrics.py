"""Tests for topic-size distribution helpers."""

from __future__ import annotations

import unittest

import numpy as np

from src.stage03_train.topic_size_metrics import topic_floor_score, topic_size_stats_from_counts


class TopicSizeMetricsTests(unittest.TestCase):
    def test_stats_from_counts(self) -> None:
        sizes = np.array([10, 30, 100, 200, 500])
        stats = topic_size_stats_from_counts(sizes, n_fit_docs=1000)
        self.assertAlmostEqual(stats["largest_topic_share"], 0.5)
        self.assertAlmostEqual(stats["median_topic_size"], 100.0)
        self.assertEqual(stats["n_tiny_topics_lt25"], 1.0)
        self.assertEqual(stats["n_tiny_topics_lt50"], 2.0)

    def test_topic_floor_score(self) -> None:
        self.assertAlmostEqual(topic_floor_score(25), 0.5)
        self.assertAlmostEqual(topic_floor_score(50), 1.0)
        self.assertAlmostEqual(topic_floor_score(300), 1.0)
        self.assertAlmostEqual(topic_floor_score(600), 0.85)
        self.assertAlmostEqual(topic_floor_score(900), 0.5)


if __name__ == "__main__":
    unittest.main()
