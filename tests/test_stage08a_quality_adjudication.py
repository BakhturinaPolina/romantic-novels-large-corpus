"""Unit tests for Stage 08A quality adjudication prompt formatting."""

from __future__ import annotations

import unittest

from src.stage08_llm_labeling.prompts.adjudication.stage08a_quality_adjudication import (
    PROMPT_VERSION,
    QUALITY_ADJUDICATION_SCHEMA,
    format_all_keywords,
    format_user_prompt,
)
from src.stage08_llm_labeling.topic_quality_hints import (
    TopicHints,
    topic_ids_for_labeling,
)


class Stage08aQualityAdjudicationTests(unittest.TestCase):
    def test_schema_has_required_fields(self) -> None:
        required = set(QUALITY_ADJUDICATION_SCHEMA["required"])
        self.assertIn("llm_quality_decision", required)
        self.assertIn("content_status", required)

    def test_format_user_prompt_evidence_priority_order(self) -> None:
        packet = {
            "topic_id": 9,
            "n_assigned_docs": 100,
            "n_snippets_available": 2,
            "stage07_flags": ["possible_character_residue"],
            "stage07_reason": "possible_character_residue",
            "recommended_next_step": "stage08_quality_adjudication",
            "representations": {
                "Main": {"words": ["kate", "emma", "said"]},
                "KeyBERT": {"words": ["trembling", "pinned"]},
                "MMR": {"words": ["promises", "pinned"]},
                "POS": {"words": ["embarrassment", "promises"]},
            },
            "snippets": ["He counted the cash.", "The contract was signed."],
        }
        text = format_user_prompt(packet)
        snippets_pos = text.index("### 1. SNIPPETS")
        keybert_pos = text.index("### 2. KeyBERT")
        main_pos = text.index("### 6. Main")
        self.assertLess(snippets_pos, keybert_pos)
        self.assertLess(keybert_pos, main_pos)
        self.assertIn("trembling", text)
        self.assertIn("ALL KEYWORDS", text)

    def test_format_all_keywords_excludes_main(self) -> None:
        reps = {
            "Main": {"words": ["kate", "only_in_main"]},
            "KeyBERT": {"words": ["trembling", "pinned"]},
            "MMR": {"words": ["promises", "pinned"]},
            "POS": {"words": ["embarrassment"]},
        }
        combined = format_all_keywords(reps)
        self.assertIn("trembling", combined)
        self.assertIn("promises", combined)
        self.assertNotIn("kate", combined)
        self.assertNotIn("only_in_main", combined)

    def test_prompt_version_set(self) -> None:
        self.assertEqual(PROMPT_VERSION, "v2_snippets_first_ignore_names")

    def test_topic_ids_for_labeling_filters_hard_exclude(self) -> None:
        hints = {
            1: TopicHints(topic_id=1, hard_exclude_candidate=True),
            2: TopicHints(topic_id=2, soft_review_candidate=False),
            3: TopicHints(
                topic_id=3,
                soft_review_candidate=True,
            ),
        }
        adjudication = {3: {"llm_quality_decision": "pass_to_labeling"}}
        allowed = topic_ids_for_labeling(
            hints,
            adjudication,
            skip_hard_exclude=True,
            require_08a_pass=True,
        )
        self.assertNotIn(1, allowed)
        self.assertIn(2, allowed)
        self.assertIn(3, allowed)

    def test_soft_review_without_08a_excluded(self) -> None:
        hints = {
            5: TopicHints(topic_id=5, soft_review_candidate=True),
        }
        allowed = topic_ids_for_labeling(
            hints,
            {},
            require_08a_pass=True,
        )
        self.assertNotIn(5, allowed)


if __name__ == "__main__":
    unittest.main()
