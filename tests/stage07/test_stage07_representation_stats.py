"""Unit tests for Stage07 multi-representation stats and routing."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.stage07_topic_quality.config import load_stage07_config
from src.stage07_topic_quality.topic_quality_analysis import (
    apply_stage07_routing_flags,
    attach_snippet_columns,
    count_content_pos_words,
    load_topic_snippets,
)


class Stage07RepresentationStatsTests(unittest.TestCase):
    def test_diversity_simple_formula(self) -> None:
        words = ["a", "b", "a", "c"]
        n_unique = len(set(words))
        diversity = n_unique / len(words)
        self.assertAlmostEqual(diversity, 0.75)

    def test_count_content_pos_words_nonempty(self) -> None:
        n = count_content_pos_words(["money", "business", "pay"])
        self.assertGreaterEqual(n, 1)

    def test_attach_snippet_columns(self) -> None:
        df = pd.DataFrame({"Topic": [1, 2]})
        snippets = {1: ["hello", "world"], 2: []}
        out = attach_snippet_columns(df, snippets, snippets_per_topic=3)
        self.assertEqual(int(out.loc[out["Topic"] == 1, "n_snippets_available"].iloc[0]), 2)
        self.assertEqual(out.loc[out["Topic"] == 1, "snippet_1"].iloc[0], "hello")
        self.assertEqual(out.loc[out["Topic"] == 2, "snippet_1"].iloc[0], "")

    def test_routing_hard_exclude_publisher(self) -> None:
        cfg = load_stage07_config()
        df = pd.DataFrame(
            {
                "Topic": [9],
                "Count": [500],
                "Name": ["9_money_job"],
                "posthoc_flags": [["publisher_boilerplate"]],
                "hard_exclude_candidate_posthoc": [True],
                "soft_review_candidate_posthoc": [False],
                "Main_n_words": [10],
                "KeyBERT_n_words": [10],
                "MMR_n_words": [10],
                "POS_n_words": [10],
                "Main_n_content_pos": [8],
                "KeyBERT_n_content_pos": [8],
                "MMR_n_content_pos": [8],
                "POS_n_content_pos": [8],
                "Main_coherence_c_v": [0.5],
                "KeyBERT_coherence_c_v": [0.5],
                "MMR_coherence_c_v": [0.5],
                "POS_coherence_c_v": [0.5],
                "Main_diversity_simple": [0.9],
                "KeyBERT_diversity_simple": [0.9],
                "MMR_diversity_simple": [0.9],
                "POS_diversity_simple": [0.9],
                "n_snippets_available": [6],
            }
        )
        out = apply_stage07_routing_flags(df, cfg)
        self.assertTrue(bool(out.iloc[0]["hard_exclude_candidate"]))
        self.assertEqual(out.iloc[0]["recommended_next_step"], "exclude_before_llm")

    def test_routing_soft_review_small_docs(self) -> None:
        cfg = load_stage07_config()
        df = pd.DataFrame(
            {
                "Topic": [3],
                "Count": [20],
                "Name": ["3_test"],
                "posthoc_flags": [[]],
                "hard_exclude_candidate_posthoc": [False],
                "soft_review_candidate_posthoc": [False],
                "Main_n_words": [10],
                "KeyBERT_n_words": [10],
                "MMR_n_words": [10],
                "POS_n_words": [10],
                "Main_n_content_pos": [8],
                "KeyBERT_n_content_pos": [8],
                "MMR_n_content_pos": [8],
                "POS_n_content_pos": [8],
                "Main_coherence_c_v": [0.5],
                "KeyBERT_coherence_c_v": [0.5],
                "MMR_coherence_c_v": [0.5],
                "POS_coherence_c_v": [0.5],
                "Main_diversity_simple": [0.9],
                "KeyBERT_diversity_simple": [0.9],
                "MMR_diversity_simple": [0.9],
                "POS_diversity_simple": [0.9],
                "n_snippets_available": [6],
            }
        )
        out = apply_stage07_routing_flags(df, cfg)
        self.assertFalse(bool(out.iloc[0]["hard_exclude_candidate"]))
        self.assertTrue(bool(out.iloc[0]["soft_review_candidate"]))
        self.assertEqual(out.iloc[0]["recommended_next_step"], "stage08_quality_adjudication")


if __name__ == "__main__":
    unittest.main()
