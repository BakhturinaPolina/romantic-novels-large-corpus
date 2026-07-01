"""Stage07 integration: post-hoc rules merged into topic quality table."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from src.stage07_topic_quality.topic_quality_analysis import (
    build_topic_quality_table,
    merge_posthoc_flags,
)


class Stage07PosthocIntegrationTests(unittest.TestCase):
    def test_merge_posthoc_flags_hard_exclude(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            topic_info = pd.DataFrame(
                [
                    {
                        "Topic": 0,
                        "Count": 500,
                        "Name": "0_ab_cd_ef",
                        "Representation": "['ab', 'cd', 'ef', 'gh', 'ij', 'kl']",
                        "Representative_Docs": "['x']",
                    },
                    {
                        "Topic": 1,
                        "Count": 500,
                        "Name": "1_money_job",
                        "Representation": "['money', 'job', 'pay']",
                        "Representative_Docs": "['she signed the deal.']",
                    },
                ]
            )
            csv_path = Path(tmp) / "topic_info.csv"
            topic_info.to_csv(csv_path, index=False)

            quality_df = topic_info.copy()
            quality_df["noise_candidate"] = False
            quality_df["noise_reason"] = ""
            quality_df["inspection_label"] = quality_df["Name"]

            merged = merge_posthoc_flags(quality_df, topic_info_path=csv_path)
            topic0 = merged.loc[merged["Topic"] == 0].iloc[0]
            self.assertTrue(bool(topic0["hard_exclude_candidate_posthoc"]))
            topic1 = merged.loc[merged["Topic"] == 1].iloc[0]
            self.assertFalse(bool(topic1["hard_exclude_candidate_posthoc"]))

    def test_build_topic_quality_table_has_routing_columns(self) -> None:
        topic_info = pd.DataFrame(
            [
                {
                    "Topic": 1,
                    "Count": 500,
                    "Name": "1_money_job",
                    "Representation": "['money', 'job']",
                }
            ]
        )
        mock_model = MagicMock()
        mock_model.get_topic_info.return_value = topic_info

        with patch(
            "src.stage07_topic_quality.topic_quality_analysis.extract_all_topics",
            return_value={
                "Main": {1: [{"word": "money", "score": 0.1}]},
                "KeyBERT": {1: [{"word": "job", "score": 0.1}]},
                "MMR": {1: [{"word": "pay", "score": 0.1}]},
                "POS": {1: [{"word": "money", "score": 0.1}]},
            },
        ), patch(
            "src.stage07_topic_quality.topic_quality_analysis.compute_coherence_per_representation",
            return_value=pd.DataFrame(
                {
                    "Topic": [1],
                    "Main_coherence_c_v": [0.5],
                    "KeyBERT_coherence_c_v": [0.5],
                    "MMR_coherence_c_v": [0.5],
                    "POS_coherence_c_v": [0.5],
                }
            ),
        ):
            with tempfile.TemporaryDirectory() as tmp:
                csv_path = Path(tmp) / "topic_info.csv"
                topic_info.to_csv(csv_path, index=False)
                quality_df = build_topic_quality_table(
                    mock_model,
                    docs_tokens=[["money", "job"]],
                    dictionary=MagicMock(),
                    topic_info_path=csv_path,
                )
        self.assertIn("hard_exclude_candidate", quality_df.columns)
        self.assertIn("soft_review_candidate", quality_df.columns)
        self.assertIn("recommended_next_step", quality_df.columns)
        self.assertIn("stage07_flags", quality_df.columns)


if __name__ == "__main__":
    unittest.main()
