"""Stage07 integration: post-hoc rules merged into topic quality table."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from src.stage07_topic_quality.topic_quality_analysis import (
    build_topic_quality_table,
    merge_posthoc_flags,
)

CALL59_TOPIC_INFO = Path(
    "results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/topic_info.csv"
)


@unittest.skipUnless(CALL59_TOPIC_INFO.exists(), "call_59 topic_info.csv not present")
class Stage07PosthocIntegrationTests(unittest.TestCase):
    def test_merge_posthoc_flags_from_topic_info(self) -> None:
        topic_info = pd.read_csv(CALL59_TOPIC_INFO)
        quality_df = topic_info[topic_info["Topic"] != -1][
            ["Topic", "Count", "Name", "Representation"]
        ].copy()
        quality_df["noise_candidate"] = False
        quality_df["noise_reason"] = ""
        quality_df["inspection_label"] = quality_df["Name"]

        merged = merge_posthoc_flags(quality_df, topic_info_path=CALL59_TOPIC_INFO)
        self.assertIn("posthoc_reason", merged.columns)
        self.assertIn("exclude_from_axes", merged.columns)
        flagged = merged[merged["noise_candidate"]]
        self.assertGreater(len(flagged), 100)
        topic0 = merged.loc[merged["Topic"] == 0].iloc[0]
        self.assertTrue(topic0["noise_candidate"])
        self.assertIn("multilingual_artifact", topic0["posthoc_reason"])

    def test_build_topic_quality_table_with_posthoc(self) -> None:
        topic_info = pd.read_csv(CALL59_TOPIC_INFO)
        mock_model = MagicMock()
        mock_model.get_topic_info.return_value = topic_info

        quality_df = build_topic_quality_table(
            mock_model,
            docs_tokens=[["hello", "world"]],
            dictionary=MagicMock(),
            min_size=200,
            min_pos_words=0,
            min_pos_coherence=-1.0,
            top_k=10,
            topic_info_path=CALL59_TOPIC_INFO,
        )
        self.assertIn("posthoc_reason", quality_df.columns)
        self.assertGreater(int(quality_df["noise_candidate"].sum()), 100)


if __name__ == "__main__":
    unittest.main()
