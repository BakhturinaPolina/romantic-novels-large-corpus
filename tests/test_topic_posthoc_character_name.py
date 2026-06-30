"""Publisher post-hoc rule tests (character_name_cluster moved to name cleaning)."""

from __future__ import annotations

import unittest

import pandas as pd

from src.common.topic_posthoc.rules import (
    NOISE_ACTION,
    classify_topic_row,
    load_rules_config,
    rule_publisher_boilerplate,
)


class PublisherPosthocRuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = load_rules_config()

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

    def test_door_car_topic_not_character_name(self) -> None:
        row = pd.Series(
            {
                "Topic": 0,
                "Count": 8454,
                "Name": "0_door_car_open_room",
                "Representation": "['door', 'car', 'open', 'room', 'opened']",
                "Representative_Docs": "['he opened the door.']",
            }
        )
        result = classify_topic_row(row, self.cfg)
        self.assertNotIn("character_name_cluster", result["posthoc_flags"])


if __name__ == "__main__":
    unittest.main()
