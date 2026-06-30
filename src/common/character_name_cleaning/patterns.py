"""Pattern helpers for snake-case, glued, and plural family name tokens."""

from __future__ import annotations

import re

from src.common.character_name_cleaning.lexicon import CleaningLexicon

SNAKE_OR_GLUED_NAME_PATTERNS = [
    re.compile(r"^[a-z]+_[a-z]+$"),
    re.compile(r"^[a-z]{4,}[a-z]{4,}$"),
]

TITLE_NAME_PATTERN = re.compile(
    r"\b(doctor|dr|sir|lady|lord|duke|duchess|captain|officer|detective)\s+([A-Z][a-z]+)\b",
    re.IGNORECASE,
)


def is_snake_or_glued_name(word: str) -> bool:
    w = word.lower().strip()
    return any(p.match(w) for p in SNAKE_OR_GLUED_NAME_PATTERNS)


def snake_case_parts(word: str) -> list[str]:
    w = word.lower().strip()
    if "_" in w:
        return [p for p in w.split("_") if p]
    return []


def should_remove_plural_family(
    word: str,
    lexicon: CleaningLexicon,
    topic_words_lower: set[str],
) -> bool:
    """Remove pluralized family names (kincaids) but not flower plurals (roses)."""
    w = word.lower().strip()
    if not w.endswith("s") or len(w) < 4:
        return False
    stem = w[:-1]
    if stem not in lexicon.auto_replace_names:
        return False
    if stem == "rose" and lexicon.flower_co_words & topic_words_lower:
        return False
    return True


def should_review_surname(
    word: str,
    lexicon: CleaningLexicon,
    topic_words_lower: set[str],
) -> bool:
    w = word.lower().strip()
    if w not in lexicon.surname_review:
        return False
    name_like = bool(lexicon.auto_replace_names & topic_words_lower)
    ambiguous_like = bool(lexicon.ambiguous_review & topic_words_lower)
    return name_like or ambiguous_like


def classify_snake_glued_token(
    word: str,
    lexicon: CleaningLexicon,
) -> str | None:
    """
    Return removal reason, 'review', or None.

    Auto-remove if a component is in auto_replace_names; else manual review.
    """
    w = word.lower().strip()
    if not is_snake_or_glued_name(w):
        return None
    parts = snake_case_parts(w) or [w]
    if any(p in lexicon.auto_replace_names for p in parts):
        return "snake_glued_seed_component"
    return "snake_glued_review"
