"""Unit tests for post-hoc topic classification rules."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.common.topic_posthoc.rules import (
    HARD_EXCLUDE_ACTION,
    SOFT_REVIEW_ACTION,
    classify_topic_row,
    classify_topics_from_info,
    load_rules_config,
    rule_multilingual_artifact,
    rule_publisher_boilerplate,
    write_posthoc_artifacts,
)


def _synthetic_row(**kwargs: object) -> pd.Series:
    defaults = {
        "Topic": 1,
        "Count": 500,
        "Name": "1_money_job_pay",
        "Representation": "['money', 'job', 'pay', 'business', 'deal']",
        "KeyBERT": "['money', 'job']",
        "MMR": "['pay', 'deal']",
        "POS": "['money', 'business', 'pay']",
        "Representative_Docs": "['she negotiated the contract.']",
    }
    defaults.update(kwargs)
    return pd.Series(defaults)


@unittest.skipUnless(
    Path(
        "results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/topic_info.csv"
    ).exists(),
    "call_59 topic_info.csv not present",
)
class TopicPosthocRulesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = load_rules_config()

    def test_multilingual_artifact_short_tokens(self) -> None:
        row = _synthetic_row(
            Topic=0,
            Representation="['ab', 'cd', 'ef', 'gh', 'ij', 'kl']",
            Representative_Docs="['x']",
        )
        result = classify_topic_row(row, self.cfg)
        self.assertIn("multilingual_artifact", result["posthoc_flags"])
        self.assertEqual(result["suggested_action"], HARD_EXCLUDE_ACTION)
        self.assertTrue(result["exclude_from_axes"])

    def test_publisher_boilerplate_in_repr_docs(self) -> None:
        row = _synthetic_row(
            Topic=21,
            Representative_Docs="['copyright 2010 publisher harpercollins']",
        )
        result = classify_topic_row(row, self.cfg)
        self.assertIn("publisher_boilerplate", result["posthoc_flags"])
        self.assertEqual(result["suggested_action"], HARD_EXCLUDE_ACTION)

    def test_publisher_name_keywords_fallback(self) -> None:
        words = ["chapter", "book", "books", "read", "author"]
        self.assertTrue(rule_publisher_boilerplate(words, "", self.cfg))

    def test_scene_topic_kept(self) -> None:
        row = _synthetic_row(Topic=1)
        result = classify_topic_row(row, self.cfg)
        self.assertEqual(result["posthoc_flags"], [])
        self.assertEqual(result["suggested_action"], "keep")

    def test_tiny_topic_is_soft_review(self) -> None:
        row = _synthetic_row(Topic=5, Count=50)
        result = classify_topic_row(row, self.cfg)
        self.assertIn("tiny_topic", result["posthoc_flags"])
        self.assertEqual(result["suggested_action"], SOFT_REVIEW_ACTION)
        self.assertFalse(result["exclude_from_axes"])
        self.assertTrue(result["soft_review_candidate"])

    def test_classify_smoke_on_stub_fixture(self) -> None:
        path = Path(
            "results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/topic_info.csv"
        )
        classified = classify_topics_from_info(pd.read_csv(path), config_path=None)
        non_outlier = classified[classified["Topic"] != -1]
        self.assertGreater(len(non_outlier), 0)
        all_flags = {
            rule
            for flags in non_outlier["posthoc_flags"]
            if isinstance(flags, list)
            for rule in flags
        }
        self.assertNotIn("subgenre_marker", all_flags)
        self.assertNotIn("procedural_transition", all_flags)

    def test_write_posthoc_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            df = pd.DataFrame(
                [
                    _synthetic_row(Topic=1),
                    _synthetic_row(
                        Topic=2,
                        Count=10,
                        Representative_Docs="['copyright notice']",
                    ),
                ]
            )
            csv_path = Path(tmp) / "topic_info.csv"
            df.to_csv(csv_path, index=False)
            flags_path, summary_path = write_posthoc_artifacts(csv_path, Path(tmp))
            self.assertTrue(flags_path.exists())
            self.assertTrue(summary_path.exists())
            with open(summary_path, encoding="utf-8") as f:
                summary = json.load(f)
            self.assertIn("n_hard_exclude", summary)


if __name__ == "__main__":
    unittest.main()
