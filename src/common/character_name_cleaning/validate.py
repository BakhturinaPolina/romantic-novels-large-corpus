"""Validate cleaned snippets and topic words contain no seed names or PERSON entities."""

from __future__ import annotations

import re
from typing import Any, Iterable

from src.common.character_name_cleaning.lexicon import CleaningLexicon
from src.common.character_name_cleaning.ner_pass import get_spacy_nlp


def find_seed_name_hits(text: str, lexicon: CleaningLexicon) -> list[str]:
    """Return seed names still present in text."""
    if not text:
        return []
    hits: list[str] = []
    for name in sorted(lexicon.auto_replace_names | lexicon.surname_review, key=len, reverse=True):
        if name in lexicon.keep_role_tokens:
            continue
        if re.search(rf"\b{re.escape(name)}\b", text, re.IGNORECASE):
            hits.append(name)
    return hits


def find_person_entities(text: str, nlp=None) -> list[str]:
    if not text:
        return []
    nlp = nlp or get_spacy_nlp()
    if nlp is None or "ner" not in nlp.pipe_names:
        return []
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]


def assert_clean_inputs(
    snippets: Iterable[str],
    topic_words_by_aspect: dict[str, dict[str, list[dict[str, Any]]]],
    lexicon: CleaningLexicon,
    *,
    nlp=None,
    allow_ambiguous_in_topics: bool = True,
) -> None:
    """
    Raise AssertionError if cleaned inputs still contain auto-replace seed names
    or spaCy PERSON entities in snippets.
    """
    nlp = nlp or get_spacy_nlp()
    errors: list[str] = []

    for i, snippet in enumerate(snippets):
        hits = find_seed_name_hits(snippet, lexicon)
        if hits:
            errors.append(f"snippet[{i}] seed hits: {hits[:5]}")
        persons = find_person_entities(snippet, nlp)
        if persons:
            errors.append(f"snippet[{i}] PERSON entities: {persons[:5]}")

    for aspect, topics in topic_words_by_aspect.items():
        for topic_id, words in topics.items():
            for item in words:
                w = str(item.get("word", "")).lower().strip()
                if not w:
                    continue
                if w in lexicon.keep_role_tokens:
                    continue
                if allow_ambiguous_in_topics and w in lexicon.ambiguous_review:
                    continue
                if w in lexicon.auto_replace_names or w in lexicon.surname_review:
                    errors.append(
                        f"topic {topic_id} aspect {aspect} still has name word: {w}"
                    )

    if errors:
        preview = "\n".join(errors[:20])
        raise AssertionError(
            f"Cleaned inputs failed validation ({len(errors)} issues):\n{preview}"
        )
