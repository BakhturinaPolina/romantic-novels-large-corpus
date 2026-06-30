"""Validate NER-cleaned snippets and topic words."""

from __future__ import annotations

from typing import Any, Iterable

from src.common.character_name_cleaning.lexicon import CleaningLexicon
from src.common.character_name_cleaning.ner_pass import (
    extract_person_tokens_from_text,
    get_spacy_nlp,
    is_person_topic_word,
)


def assert_clean_inputs(
    snippets: Iterable[str],
    topic_words_by_aspect: dict[str, dict[str, list[dict[str, Any]]]],
    lexicon: CleaningLexicon,
    *,
    nlp=None,
) -> None:
    """Raise AssertionError if cleaned inputs still contain spaCy PERSON spans."""
    nlp = nlp or get_spacy_nlp()
    if nlp is None:
        raise RuntimeError("spaCy NER required for validation")

    errors: list[str] = []

    for i, snippet in enumerate(snippets):
        persons = extract_person_tokens_from_text(snippet, nlp, lexicon)
        if persons:
            errors.append(f"snippet[{i}] PERSON tokens: {sorted(persons)[:5]}")

    for aspect, topics in topic_words_by_aspect.items():
        for topic_id, words in topics.items():
            for item in words:
                w = str(item.get("word", "")).strip()
                if not w:
                    continue
                if is_person_topic_word(
                    w,
                    topic_person_tokens=set(),
                    nlp=nlp,
                    lexicon=lexicon,
                ):
                    errors.append(
                        f"topic {topic_id} aspect {aspect} still has PERSON word: {w}"
                    )

    if errors:
        preview = "\n".join(errors[:20])
        raise AssertionError(
            f"Cleaned inputs failed NER validation ({len(errors)} issues):\n{preview}"
        )
