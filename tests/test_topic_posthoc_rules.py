"""Unit tests for post-hoc topic classification rules (call_59 fixtures)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd

from src.common.topic_posthoc.rules import (
    NOISE_ACTION,
    classify_topic_row,
    classify_topics_from_info,
    load_rules_config,
    write_posthoc_artifacts,
)

CALL59_DIR = Path(
    "results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59"
)
CALL59_TOPIC_INFO = CALL59_DIR / "topic_info.csv"


def _row(topic_id: int) -> pd.Series:
    df = pd.read_csv(CALL59_TOPIC_INFO)
    row = df.loc[df["Topic"] == topic_id].iloc[0]
    return row


@unittest.skipUnless(CALL59_TOPIC_INFO.exists(), "call_59 topic_info.csv not present")
class TopicPosthocCall59Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = load_rules_config()
        cls.full_df = pd.read_csv(CALL59_TOPIC_INFO)

    def test_multilingual_flags_topic_0(self) -> None:
        result = classify_topic_row(_row(0), self.cfg)
        self.assertIn("multilingual_artifact", result["posthoc_flags"])
        self.assertTrue(result["exclude_from_axes"])
        self.assertEqual(result["suggested_action"], NOISE_ACTION)

    def test_multilingual_flags_topic_139(self) -> None:
        result = classify_topic_row(_row(139), self.cfg)
        self.assertIn("multilingual_artifact", result["posthoc_flags"])

    def test_publisher_flags_topic_21(self) -> None:
        result = classify_topic_row(_row(21), self.cfg)
        self.assertIn("publisher_boilerplate", result["posthoc_flags"])

    def test_publisher_flags_true_positives(self) -> None:
        for topic_id in (100, 293):
            result = classify_topic_row(_row(topic_id), self.cfg)
            self.assertIn(
                "publisher_boilerplate",
                result["posthoc_flags"],
                msg=f"topic {topic_id}",
            )

    def test_publisher_no_false_positives(self) -> None:
        for topic_id in (27, 52, 76, 111, 154, 264, 269, 288):
            result = classify_topic_row(_row(topic_id), self.cfg)
            self.assertNotIn(
                "publisher_boilerplate",
                result["posthoc_flags"],
                msg=f"topic {topic_id}",
            )

    def test_emotional_adverb_topics_kept(self) -> None:
        """Topics rich in -ly dialogue adverbs are scene content, not noise."""
        for topic_id in (8, 41):
            result = classify_topic_row(_row(topic_id), self.cfg)
            self.assertEqual(result["posthoc_flags"], [])
            self.assertEqual(result["suggested_action"], "keep")
            self.assertEqual(result["content_type"], "scene")

    def test_colloquial_speech_topics_not_flagged(self) -> None:
        """Colloquial contraction topics are meaningful scene content."""
        for topic_id in (22, 44, 57):
            result = classify_topic_row(_row(topic_id), self.cfg)
            self.assertNotIn("speech_act_filler", result["posthoc_flags"])
            self.assertEqual(result["suggested_action"], "keep")

    def test_tiny_topic_threshold(self) -> None:
        classified = classify_topics_from_info(self.full_df, config_path=None)
        tiny = classified[
            classified["posthoc_flags"].apply(
                lambda flags: isinstance(flags, list) and "tiny_topic" in flags
            )
        ]
        self.assertTrue((tiny["Count"] < 200).all())
        self.assertGreaterEqual(len(tiny), 100)

    def test_no_false_positive_intimacy(self) -> None:
        result = classify_topic_row(_row(1), self.cfg)
        noise_flags = {
            "multilingual_artifact",
            "publisher_boilerplate",
        }
        hit_noise = [f for f in result["posthoc_flags"] if f in noise_flags]
        self.assertEqual(hit_noise, [])
        self.assertEqual(result["suggested_action"], "keep")

    def test_subgenre_marker_topic_37(self) -> None:
        result = classify_topic_row(_row(37), self.cfg)
        self.assertIn("subgenre_marker", result["posthoc_flags"])

    def test_classify_full_call59_smoke(self) -> None:
        classified = classify_topics_from_info(self.full_df, config_path=None)
        non_outlier = classified[classified["Topic"] != -1]
        n_flagged = int((non_outlier["suggested_action"] == NOISE_ACTION).sum())
        fraction = n_flagged / len(non_outlier)
        self.assertGreaterEqual(fraction, 0.40)

        summary = {
            "n_topics": len(non_outlier),
            "n_flagged_noise": n_flagged,
            "flagged_fraction": round(fraction, 4),
        }
        self.assertIn("n_topics", summary)
        self.assertGreater(summary["n_flagged_noise"], 0)

        all_flags = {
            rule
            for flags in non_outlier["posthoc_flags"]
            if isinstance(flags, list)
            for rule in flags
        }
        self.assertNotIn("speech_act_filler", all_flags)
        self.assertNotIn("dialogue_delivery", all_flags)

    def test_write_posthoc_artifacts(self) -> None:
        flags_path, summary_path = write_posthoc_artifacts(CALL59_TOPIC_INFO)
        self.assertTrue(flags_path.exists())
        self.assertTrue(summary_path.exists())
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        self.assertIn("rule_hits", summary)
        self.assertIn("flagged_fraction", summary)
        self.assertGreaterEqual(summary["flagged_fraction"], 0.40)
        self.assertNotIn("speech_act_filler", summary.get("rule_hits", {}))


if __name__ == "__main__":
    unittest.main()
