"""Unit tests for character name cleaning (seed lexicon + NER)."""

from __future__ import annotations

import unittest

from src.common.character_name_cleaning.lexicon import load_lexicon
from src.common.character_name_cleaning.patterns import classify_snake_glued_token
from src.common.character_name_cleaning.seed_pass import (
    character_name_ratio,
    classify_topic_by_ratio,
    clean_topic_words,
    replace_seed_names_in_snippet,
)


class CharacterNameCleaningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lexicon = load_lexicon()

    def test_title_preservation_lord_ashford(self) -> None:
        text = "Lord Ashford looked at her."
        out = replace_seed_names_in_snippet(text, self.lexicon)
        self.assertIn("Lord [person]", out)
        self.assertNotIn("Ashford", out)

    def test_captain_wyatt_title_preserved(self) -> None:
        text = "Captain Wyatt's jaw tightened."
        out = replace_seed_names_in_snippet(text, self.lexicon)
        self.assertIn("Captain [person]", out)
        self.assertNotIn("Wyatt", out)

    def test_bare_captain_unchanged(self) -> None:
        text = "The captain's jaw tightened."
        out = replace_seed_names_in_snippet(text, self.lexicon)
        self.assertEqual(text, out)

    def test_bare_role_tokens_unchanged(self) -> None:
        for text in ("yes, sir", "the doctor", "my lord"):
            self.assertEqual(text, replace_seed_names_in_snippet(text, self.lexicon))

    def test_snippet_seed_replace_aiden(self) -> None:
        text = "Aiden looked at her."
        out = replace_seed_names_in_snippet(text, self.lexicon)
        self.assertEqual("[person] looked at her.", out)

    def test_topic_word_removal_kate_doctor_kept(self) -> None:
        words = [
            {"word": "kate", "score": 0.1},
            {"word": "doctor", "score": 0.05},
            {"word": "fear", "score": 0.03},
        ]
        cleaned, removed, _ = clean_topic_words(words, self.lexicon)
        kept = [w["word"] for w in cleaned]
        self.assertNotIn("kate", kept)
        self.assertIn("doctor", kept)
        self.assertIn("kate", removed)

    def test_ambiguous_rose_with_bouquet_kept(self) -> None:
        words = [
            {"word": "rose", "score": 0.1},
            {"word": "bouquet", "score": 0.08},
            {"word": "vase", "score": 0.05},
        ]
        cleaned, removed, reviews = clean_topic_words(words, self.lexicon)
        kept = [w["word"] for w in cleaned]
        self.assertIn("rose", kept)
        self.assertNotIn("rose", removed)
        self.assertTrue(any(r["word"] == "rose" for r in reviews))

    def test_ambiguous_rose_with_calvert_surname_removed(self) -> None:
        words = [
            {"word": "rose", "score": 0.1},
            {"word": "calvert", "score": 0.08},
        ]
        cleaned, removed, reviews = clean_topic_words(words, self.lexicon)
        kept = [w["word"] for w in cleaned]
        self.assertIn("rose", kept)
        self.assertIn("calvert", removed)
        self.assertTrue(any(r["word"] == "rose" for r in reviews))

    def test_ratio_thresholds(self) -> None:
        high = [{"word": "kate", "score": 1}, {"word": "emma", "score": 1}]
        mid = [{"word": "kate", "score": 1}, {"word": "door", "score": 1}, {"word": "car", "score": 1}, {"word": "open", "score": 1}]
        low = [
            {"word": "door", "score": 1},
            {"word": "car", "score": 1},
            {"word": "open", "score": 1},
            {"word": "room", "score": 1},
            {"word": "stairs", "score": 1},
            {"word": "kate", "score": 1},
        ]

        self.assertGreaterEqual(character_name_ratio(high, self.lexicon), 0.5)
        r_mid = character_name_ratio(mid, self.lexicon)
        self.assertGreaterEqual(r_mid, 0.2)
        self.assertLess(r_mid, 0.5)
        self.assertLess(character_name_ratio(low, self.lexicon), 0.2)

        self.assertEqual(
            classify_topic_by_ratio(0.6, self.lexicon, names_removed=2)["content_type"],
            "character_name",
        )
        self.assertTrue(
            classify_topic_by_ratio(0.6, self.lexicon, names_removed=2)["exclude_from_axes"]
        )
        contaminated = classify_topic_by_ratio(0.3, self.lexicon, names_removed=1)
        self.assertEqual(contaminated["content_type"], "scene")
        self.assertFalse(contaminated["exclude_from_axes"])
        self.assertIn("name_contaminated_review", contaminated["posthoc_flags"])

    def test_plural_kincaids_removed(self) -> None:
        lex = self.lexicon
        extended = type(lex)(
            keep_role_tokens=lex.keep_role_tokens,
            high_confidence_names=lex.high_confidence_names | frozenset({"kincaid"}),
            ambiguous_review=lex.ambiguous_review,
            surname_review=lex.surname_review,
            flower_co_words=lex.flower_co_words,
            ratio_character_name_cluster=lex.ratio_character_name_cluster,
            ratio_name_contaminated_review=lex.ratio_name_contaminated_review,
            person_placeholder=lex.person_placeholder,
            extend_lexicon_from_topics=False,
        )
        words = [{"word": "kincaids", "score": 0.1}, {"word": "ranch", "score": 0.05}]
        _, removed, _ = clean_topic_words(words, extended)
        self.assertIn("kincaids", removed)

    def test_roses_kept_in_flower_topic(self) -> None:
        words = [
            {"word": "roses", "score": 0.1},
            {"word": "bouquet", "score": 0.08},
            {"word": "vase", "score": 0.05},
        ]
        cleaned, removed, _ = clean_topic_words(words, self.lexicon)
        kept = [w["word"] for w in cleaned]
        self.assertIn("roses", kept)
        self.assertNotIn("roses", removed)

    def test_snake_case_abby_donovan_review(self) -> None:
        reason = classify_snake_glued_token("abby_donovan", self.lexicon)
        self.assertIn(reason, ("snake_glued_seed_component", "snake_glued_review"))


if __name__ == "__main__":
    unittest.main()
