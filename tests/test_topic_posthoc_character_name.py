"""Unit tests for character_name_cluster and publisher name_keywords rules."""

from __future__ import annotations

import unittest

import pandas as pd

from src.common.topic_posthoc.rules import (
    NOISE_ACTION,
    PosthocRulesConfig,
    classify_topic_row,
    load_rules_config,
    rule_character_name_cluster,
    rule_publisher_boilerplate,
)


class CharacterNameClusterRuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = load_rules_config()

    def test_flags_name_topic(self) -> None:
        row = pd.Series(
            {
                "Topic": 28,
                "Count": 729,
                "Name": "28_kate_maggie_emma_sarah",
                "Representation": "['kate', 'maggie', 'emma', 'sarah']",
                "Representative_Docs": "['kate opened her eyes.']",
            }
        )
        self.assertTrue(rule_character_name_cluster(row, self.cfg))
        result = classify_topic_row(row, self.cfg)
        self.assertIn("character_name_cluster", result["posthoc_flags"])
        self.assertEqual(result["content_type"], "character_name")
        self.assertTrue(result["exclude_from_axes"])

    def test_does_not_flag_door_car_topic(self) -> None:
        row = pd.Series(
            {
                "Topic": 0,
                "Count": 8454,
                "Name": "0_door_car_open_room",
                "Representation": "['door', 'car', 'open', 'room', 'opened']",
                "Representative_Docs": "['he opened the door.']",
            }
        )
        self.assertFalse(rule_character_name_cluster(row, self.cfg))

    def test_publisher_name_keywords_fallback(self) -> None:
        row = pd.Series(
            {
                "Topic": 14,
                "Count": 1146,
                "Name": "14_chapter_book_books_read",
                "Representation": "['chapter', 'book', 'books', 'read', 'author']",
                "Representative_Docs": "['she turned the page.']",
            }
        )
        words = ["chapter", "book", "books", "read", "author"]
        self.assertTrue(rule_publisher_boilerplate(words, "", self.cfg))
        result = classify_topic_row(row, self.cfg)
        self.assertIn("publisher_boilerplate", result["posthoc_flags"])
        self.assertEqual(result["suggested_action"], NOISE_ACTION)


if __name__ == "__main__":
    unittest.main()
