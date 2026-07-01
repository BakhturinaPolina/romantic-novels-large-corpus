"""Unit tests for Stage03 BO topic-count penalty metrics."""

from __future__ import annotations

import unittest

from src.stage03_train.tune import (
    CoherenceWithTopicPenalty,
    RawCoherenceMetric,
    TopicCountMetric,
    _build_bo_metrics,
)


class TopicCountPenaltyTests(unittest.TestCase):
    def test_topic_count_metric(self) -> None:
        metric = TopicCountMetric()
        self.assertEqual(metric.score({"topics": [["a"], ["b"], ["c"]]}), 3.0)
        self.assertEqual(metric.score({"topics": None}), 0.0)
        self.assertEqual(metric.score({}), 0.0)

    def test_penalty_at_floor_is_zero(self) -> None:
        metric = CoherenceWithTopicPenalty(
            texts=[["romance", "love"], ["heart", "kiss"]],
            min_n_topics=20,
            penalty_weight=0.15,
        )
        coherence = RawCoherenceMetric(
            texts=[["romance", "love"], ["heart", "kiss"]]
        )
        topics = [[f"word{i}", f"term{i}"] for i in range(20)]
        output = {"topics": topics}
        self.assertAlmostEqual(metric.score(output), coherence.score(output))

    def test_penalty_linear_shortfall_two_topics(self) -> None:
        texts = [["romance", "love"], ["heart", "kiss"]]
        metric = CoherenceWithTopicPenalty(
            texts=texts,
            min_n_topics=20,
            penalty_weight=0.15,
        )
        coherence = RawCoherenceMetric(texts=texts)
        output = {"topics": [["alpha", "beta"], ["gamma", "delta"]]}
        raw = coherence.score(output)
        shortfall = (20 - 2) / 20
        expected = raw - 0.15 * shortfall
        self.assertAlmostEqual(metric.score(output), expected)

    def test_build_bo_metrics_enabled(self) -> None:
        cfg = {
            "optimization": {
                "topic_count_penalty": {
                    "enabled": True,
                    "min_n_topics": 20,
                    "weight": 0.15,
                }
            }
        }
        primary, extras = _build_bo_metrics(cfg, [["a"], ["b"]])
        self.assertEqual(primary.info()["name"], "CoherenceWithTopicPenalty")
        self.assertEqual([m.info()["name"] for m in extras], [
            "TopicDiversity",
            "TopicCount",
            "RawCoherence",
        ])

    def test_build_bo_metrics_disabled(self) -> None:
        cfg = {"optimization": {"topic_count_penalty": {"enabled": False}}}
        primary, extras = _build_bo_metrics(cfg, [["a"], ["b"]])
        self.assertEqual(primary.info()["name"], "Coherence")
        self.assertEqual([m.info()["name"] for m in extras], ["TopicDiversity"])


if __name__ == "__main__":
    unittest.main()
