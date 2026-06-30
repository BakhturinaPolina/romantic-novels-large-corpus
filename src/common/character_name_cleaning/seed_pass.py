"""Topic keyword cleaning and ratio flags driven by NER."""

from __future__ import annotations

from typing import Any

from src.common.character_name_cleaning.lexicon import CleaningLexicon
from src.common.character_name_cleaning.ner_pass import (
    is_person_topic_word,
    probe_topic_word_is_person,
)


def clean_topic_words(
    words: list[dict[str, Any]],
    lexicon: CleaningLexicon,
    *,
    topic_person_tokens: set[str],
    nlp,
) -> tuple[list[dict[str, Any]], list[str], list[dict[str, str]]]:
    """
    Remove topic keywords detected as PERSON by NER (snippet context or probe).

    Returns (cleaned_words, removed_words, audit_rows).
    """
    cleaned: list[dict[str, Any]] = []
    removed: list[str] = []
    audit: list[dict[str, str]] = []

    for item in words:
        word = str(item.get("word", "")).strip()
        w_lower = word.lower()
        if not w_lower:
            continue

        if w_lower in topic_person_tokens:
            removed.append(w_lower)
            audit.append({"word": w_lower, "reason": "ner_person"})
            continue

        cleaned.append(dict(item))

    return cleaned, removed, audit


def character_name_ratio(
    words: list[dict[str, Any]] | list[str],
    lexicon: CleaningLexicon,
    *,
    topic_person_tokens: set[str],
    nlp,
    original_words: list[dict[str, Any]] | list[str] | None = None,
) -> float:
    """Fraction of topic keywords classified as PERSON by NER."""
    source = original_words if original_words is not None else words
    if not source:
        return 0.0

    n = 0
    total = 0
    for item in source:
        if isinstance(item, dict):
            word = str(item.get("word", "")).strip()
        else:
            word = str(item).strip()
        if not word:
            continue
        lower = word.lower()
        if lower in lexicon.never_remove_topic_words:
            continue
        total += 1
        if is_person_topic_word(
            word,
            topic_person_tokens=topic_person_tokens,
            nlp=nlp,
            lexicon=lexicon,
        ):
            n += 1
    if total == 0:
        return 0.0
    return n / total


def classify_topic_by_ratio(
    ratio: float,
    lexicon: CleaningLexicon,
    *,
    names_removed: int,
) -> dict[str, Any]:
    """Map character_name_ratio to topic flags."""
    flags: list[str] = []
    name_cleaned = names_removed > 0

    if ratio >= lexicon.ratio_character_name_cluster:
        flags.append("possible_character_residue")
        return {
            "character_name_ratio": ratio,
            "posthoc_flags": flags,
            "posthoc_reason": ";".join(flags),
            "exclude_from_axes": False,
            "name_cleaned": name_cleaned,
            "suggested_action": "soft_review",
        }

    if ratio >= lexicon.ratio_name_contaminated_review:
        flags.append("name_contaminated_review")
        return {
            "character_name_ratio": ratio,
            "posthoc_flags": flags,
            "posthoc_reason": ";".join(flags),
            "exclude_from_axes": False,
            "name_cleaned": name_cleaned,
            "suggested_action": "soft_review",
        }

    return {
        "character_name_ratio": ratio,
        "posthoc_flags": flags,
        "posthoc_reason": "",
        "exclude_from_axes": False,
        "name_cleaned": name_cleaned,
        "suggested_action": "keep",
    }
