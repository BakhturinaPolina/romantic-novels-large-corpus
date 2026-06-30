"""Integration tests: run cleaning on call 73 fixtures and validate outputs."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.common.character_name_cleaning.lexicon import load_lexicon
from src.common.character_name_cleaning.pipeline import run_cleaning_pipeline
from src.common.character_name_cleaning.validate import assert_clean_inputs

ROOT = Path(__file__).resolve().parents[1]
CALL = 73
TOPICS_JSON = (
    ROOT
    / f"results/stage06_topic_exploration/placeholder_v4_call{CALL}"
    / "topics_all_representations_placeholder_v4_call.json"
)
REP_CSV = (
    ROOT
    / f"results/experiments/placeholder_v4_models/final_compare/call_{CALL}"
    / "representative_docs.csv"
)
OUT_DIR = ROOT / f"results/stage06_name_cleaning/placeholder_v4_call{CALL}"


@unittest.skipUnless(TOPICS_JSON.is_file(), "call 73 Stage06 topics JSON not present")
@unittest.skipUnless(REP_CSV.is_file(), "call 73 representative_docs.csv not present")
class CharacterNameCleaningCall73Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.paths = run_cleaning_pipeline(
            topics_json=TOPICS_JSON,
            representative_docs_csv=REP_CSV,
            out_dir=OUT_DIR,
        )
        with open(cls.paths["cleaned_topics"], encoding="utf-8") as f:
            cls.cleaned_topics = json.load(f)
        cls.lexicon = load_lexicon()

    def test_artifacts_written(self) -> None:
        for key in ("cleaned_topics", "cleaned_snippets", "ratio_csv", "topic_flags"):
            self.assertTrue(self.paths[key].is_file(), f"missing {key}")

    def test_assert_clean_inputs_passes(self) -> None:
        import pandas as pd

        snippets = pd.read_csv(self.paths["cleaned_snippets"])["sentence"].tolist()
        assert_clean_inputs(
            snippets,
            self.cleaned_topics,
            self.lexicon,
            allow_ambiguous_in_topics=True,
        )

    def test_topic_28_name_cluster_excluded(self) -> None:
        import pandas as pd

        ratio_df = pd.read_csv(self.paths["ratio_csv"])
        row = ratio_df[ratio_df["Topic"] == 28]
        self.assertFalse(row.empty)
        self.assertTrue(bool(row.iloc[0]["exclude_from_axes"]))
        self.assertEqual(row.iloc[0]["content_type"], "character_name")

    def test_topic_0_unchanged_ratio(self) -> None:
        import pandas as pd

        ratio_df = pd.read_csv(self.paths["ratio_csv"])
        row = ratio_df[ratio_df["Topic"] == 0]
        self.assertFalse(row.empty)
        self.assertLess(float(row.iloc[0]["character_name_ratio"]), 0.2)
        self.assertFalse(bool(row.iloc[0]["exclude_from_axes"]))


if __name__ == "__main__":
    unittest.main()
