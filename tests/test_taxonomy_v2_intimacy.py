"""Tests for Everyday Intimacy & Emotional Safety taxonomy v2 wiring."""

from __future__ import annotations

import unittest

from src.stage09_category_mapping.taxonomy_v2 import (
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
            spec["taxonomy_ids"],
            ["4.1", "4.2", "4.6", "2.2", "8.1", "8.2"],
        )
        self.assertIn("2.3", spec["exclude_taxonomy_ids"])

    def test_prompt_block_includes_enriched_nodes(self) -> None:
        block = taxonomy_block_for_prompt()
        self.assertIn("4.2", block)
        self.assertIn("Everyday Intimacy", block)
        self.assertIn("courtship", block.lower())

    def test_fallback_domestic_life_routes_to_bonding(self) -> None:
        self.assertEqual(fallback_main_category(["domestic_life"]), "4.2")

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

    def test_all_taxonomy_nodes_have_valid_ids(self) -> None:
        nodes = load_taxonomy_nodes()
        valid = valid_taxonomy_ids()
        for node in nodes:
            self.assertIn(node["id"], valid)


if __name__ == "__main__":
    unittest.main()
