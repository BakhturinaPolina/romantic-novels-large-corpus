"""Unit tests for NER-based character name cleaning."""

from __future__ import annotations

import unittest

from src.common.character_name_cleaning.lexicon import load_lexicon
from src.common.character_name_cleaning.ner_pass import (
    clean_snippet_text,
    extract_person_tokens_from_text,
    get_spacy_nlp,
    probe_topic_word_is_person,
)
from src.common.character_name_cleaning.seed_pass import (
    character_name_ratio,
    classify_topic_by_ratio,
    clean_topic_words,
)


@unittest.skipUnless(get_spacy_nlp() is not None, "spaCy en_core_web_sm not installed")
class CharacterNameCleaningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lexicon = load_lexicon()
        cls.nlp = get_spacy_nlp()

    def test_title_preservation_lord_ashford(self) -> None:
        text = "Lord Ashford looked at her."
        out = clean_snippet_text(text, self.lexicon, nlp=self.nlp)
        self.assertIn("Lord [person]", out)
        self.assertNotIn("Ashford", out)

    def test_bare_captain_unchanged(self) -> None:
        text = "The captain's jaw tightened."
        out = clean_snippet_text(text, self.lexicon, nlp=self.nlp)
        self.assertEqual(text, out)

    def test_bare_role_tokens_unchanged(self) -> None:
        for text in ("yes, sir", "the doctor", "my lord"):
            self.assertEqual(text, clean_snippet_text(text, self.lexicon, nlp=self.nlp))

    def test_snippet_ner_replaces_person(self) -> None:
        text = "Kate opened her eyes and smiled."
        out = clean_snippet_text(text, self.lexicon, nlp=self.nlp)
        self.assertNotIn("Kate", out)
        self.assertIn("[person]", out)

    def test_scene_words_not_removed_from_topics(self) -> None:
        words = [
            {"word": "hand", "score": 0.1},
            {"word": "eyes", "score": 0.08},
            {"word": "door", "score": 0.05},
        ]
        cleaned, removed, _ = clean_topic_words(
            words,
            self.lexicon,
            topic_person_tokens=set(),
            nlp=self.nlp,
        )
        self.assertEqual(len(cleaned), 3)
        self.assertEqual(removed, [])

    def test_topic_word_removed_when_in_snippet_person_context(self) -> None:
        words = [
            {"word": "kate", "score": 0.1},
            {"word": "door", "score": 0.05},
        ]
        cleaned, removed, audits = clean_topic_words(
            words,
            self.lexicon,
            topic_person_tokens={"kate"},
            nlp=self.nlp,
        )
        kept = [w["word"] for w in cleaned]
        self.assertNotIn("kate", kept)
        self.assertIn("kate", removed)
        self.assertEqual(audits[0]["reason"], "ner_snippet_context")

    def test_topic_word_probe_ner_for_name(self) -> None:
        self.assertTrue(probe_topic_word_is_person("Elizabeth", self.nlp, self.lexicon))
        self.assertFalse(probe_topic_word_is_person("door", self.nlp, self.lexicon))

    def test_ratio_thresholds(self) -> None:
        person_tokens = {"kate", "emma"}
        high = [{"word": "kate", "score": 1}, {"word": "emma", "score": 1}]
        low = [
            {"word": "door", "score": 1},
            {"word": "car", "score": 1},
            {"word": "open", "score": 1},
            {"word": "room", "score": 1},
            {"word": "stairs", "score": 1},
            {"word": "kate", "score": 1},
        ]
        self.assertGreaterEqual(
            character_name_ratio(
                high,
                self.lexicon,
                topic_person_tokens=person_tokens,
                nlp=self.nlp,
            ),
            0.5,
        )
        self.assertLess(
            character_name_ratio(
                low,
                self.lexicon,
                topic_person_tokens=person_tokens,
                nlp=self.nlp,
            ),
            0.2,
        )
        self.assertEqual(
            classify_topic_by_ratio(0.6, self.lexicon, names_removed=2)["content_type"],
            "character_name",
        )

    def test_extract_person_from_snippet(self) -> None:
        tokens = extract_person_tokens_from_text(
            "Jacob told Darcy that Elizabeth was waiting.",
            self.nlp,
            self.lexicon,
        )
        self.assertIn("jacob", tokens)
        self.assertIn("darcy", tokens)
        self.assertIn("elizabeth", tokens)


if __name__ == "__main__":
    unittest.main()
