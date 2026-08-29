"""Tests for Everyday Intimacy & Emotional Safety taxonomy v2 wiring."""

from __future__ import annotations

import unittest

from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
    apply_domain_heuristics,
    composite_index_spec,
    fallback_main_category,
    load_taxonomy_nodes,
    taxonomy_block_for_prompt,
    valid_taxonomy_ids,
)


class TaxonomyV2IntimacyTests(unittest.TestCase):
    def test_composite_index_spec(self) -> None:
        spec = composite_index_spec("everyday_intimacy_emotional_safety")
        self.assertEqual(
            spec["core_taxonomy_ids"],
            ["4.2", "4.6", "2.2"],
        )
        self.assertNotIn("optional_low_weight_context", spec)
        self.assertIn("2.3", spec["exclude_taxonomy_ids"])

    def test_prompt_block_includes_enriched_nodes(self) -> None:
        block = taxonomy_block_for_prompt()
        self.assertIn("4.2", block)
        self.assertIn("courtship", block.lower())

    def test_fallback_domestic_life_routes_to_context(self) -> None:
        self.assertEqual(fallback_main_category(["domestic_life"]), "8.1")

    def test_intimacy_subtag_reroutes_setting_only_mapping(self) -> None:
        result = {
            "main_category_id": "8.1",
            "secondary_category_id": None,
        }
        meta = {
            "primary_categories": ["romance_core"],
            "secondary_categories": ["intimacy:courtship_ritual"],
            "keywords": ["date", "dinner", "tomorrow"],
            "label": "Confirming A Date Plan",
            "scene_summary": "Characters confirm whether their outing counts as a date.",
        }
        out = apply_domain_heuristics(result, meta)
        self.assertEqual(out["main_category_id"], "4.1")
        self.assertEqual(out["secondary_category_id"], "8.1")

    def test_emotional_safety_subtag_reroutes_to_4_6(self) -> None:
        result = {
            "main_category_id": "8.1",
            "secondary_category_id": None,
        }
        meta = {
            "primary_categories": ["romance_core"],
            "secondary_categories": ["intimacy:emotional_safety"],
            "keywords": ["reassure", "okay", "safe"],
            "label": "Reassurance That Things Will Be Okay",
            "scene_summary": "One character reassures the other that things will work out.",
        }
        out = apply_domain_heuristics(result, meta)
        self.assertEqual(out["main_category_id"], "4.6")

    def test_nonsexual_coercion_routes_to_7_2(self) -> None:
        result = {
            "main_category_id": "7.2",
            "secondary_category_id": "7.4",
        }
        meta = {
            "keywords": ["threat", "family", "comply"],
            "label": "Touch Her and Your Family Suffers",
            "scene_summary": "A threatening figure forces compliance by threatening family harm.",
            "sexual_explicitness": "none",
            "sexual_function": "consent_boundary",
            "consent_status": "coercion_watchlist",
        }
        out = apply_domain_heuristics(result, meta)
        self.assertEqual(out["main_category_id"], "7.2")
        self.assertEqual(out["secondary_category_id"], "7.4")

    def test_coercion_secondary_is_deduped(self) -> None:
        result = {
            "main_category_id": "7.3",
            "secondary_category_id": "7.2",
        }
        meta = {
            "keywords": ["threat", "comply"],
            "label": "Blamed and Threatened Into Compliance",
            "scene_summary": "A character issues a veiled threat to force obedience.",
            "sexual_explicitness": "none",
            "sexual_function": "none",
            "consent_status": "coercion_watchlist",
        }
        out = apply_domain_heuristics(result, meta)
        self.assertEqual(out["main_category_id"], "7.2")
        self.assertIsNone(out["secondary_category_id"])

    def test_job_loss_keeps_6_4(self) -> None:
        result = {
            "main_category_id": "6.4",
            "secondary_category_id": "6.2",
        }
        meta = {
            "keywords": ["addition", "anxiety", "pathetic"],
            "label": "Desperate Need For A Job",
            "scene_summary": "A character expresses urgent anxiety about losing work.",
            "snippets": [
                "i want this job so badly.",
                "i've lost my job, and i'm not going to find another one.",
            ],
            "sexual_explicitness": "none",
            "sexual_function": "none",
            "consent_status": "not_applicable",
        }
        out = apply_domain_heuristics(result, meta)
        self.assertEqual(out["main_category_id"], "6.4")

    def test_sexual_coercion_stays_7_4(self) -> None:
        result = {
            "main_category_id": "2.3",
            "secondary_category_id": None,
        }
        meta = {
            "keywords": ["knees", "forced", "exposed"],
            "label": "Shoved to His Knees",
            "scene_summary": "A man forces another to his knees in a coercive sexual act.",
            "sexual_explicitness": "explicit",
            "sexual_function": "explicit_contact",
            "consent_status": "coercion_watchlist",
        }
        out = apply_domain_heuristics(result, meta)
        self.assertEqual(out["main_category_id"], "7.4")
        self.assertEqual(out["secondary_category_id"], "2.3")

    def test_all_taxonomy_nodes_have_valid_ids(self) -> None:
        nodes = load_taxonomy_nodes()
        valid = valid_taxonomy_ids()
        for node in nodes:
            self.assertIn(node["id"], valid)


if __name__ == "__main__":
    unittest.main()
