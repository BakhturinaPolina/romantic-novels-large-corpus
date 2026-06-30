"""Seed-lexicon pass: snippet replacement and topic word removal."""

from __future__ import annotations

import re
from typing import Any

from src.common.character_name_cleaning.lexicon import CleaningLexicon
from src.common.character_name_cleaning.patterns import (
    TITLE_NAME_PATTERN,
    classify_snake_glued_token,
    should_remove_plural_family,
    should_review_surname,
)

_POSSESSIVE_SUFFIX = r"('s|'s|’s)?"


def _role_alt_pattern(lexicon: CleaningLexicon) -> str:
    roles = sorted(lexicon.keep_role_tokens, key=len, reverse=True)
    return "|".join(re.escape(r) for r in roles)


def replace_seed_names_in_snippet(text: str, lexicon: CleaningLexicon) -> str:
    """Replace seed names in snippet text; preserve titles before names."""
    if not text:
        return text

    placeholder = lexicon.person_placeholder
    names = sorted(lexicon.auto_replace_names, key=len, reverse=True)
    role_pat = _role_alt_pattern(lexicon)

    # Title + capitalized name (Lord Ashford -> Lord [person])
    text = TITLE_NAME_PATTERN.sub(
        lambda m: f"{m.group(1)} {placeholder}",
        text,
    )

    for name in names:
        if name in lexicon.keep_role_tokens:
            continue
        text = re.sub(
            rf"\b({role_pat})\s+{re.escape(name)}{_POSSESSIVE_SUFFIX}\b",
            lambda m: f"{m.group(1)} {placeholder}{m.group(2) or ''}",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            rf"\b{re.escape(name)}{_POSSESSIVE_SUFFIX}\b",
            lambda m: f"{placeholder}{m.group(1) or ''}",
            text,
            flags=re.IGNORECASE,
        )

    for surname in sorted(lexicon.surname_review, key=len, reverse=True):
        text = re.sub(
            rf"\b({role_pat})\s+{re.escape(surname)}{_POSSESSIVE_SUFFIX}\b",
            lambda m: f"{m.group(1)} {placeholder}{m.group(2) or ''}",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            rf"\b{re.escape(surname)}{_POSSESSIVE_SUFFIX}\b",
            lambda m: f"{placeholder}{m.group(1) or ''}",
            text,
            flags=re.IGNORECASE,
        )

    return text


def clean_topic_words(
    words: list[dict[str, Any]],
    lexicon: CleaningLexicon,
) -> tuple[list[dict[str, Any]], list[str], list[dict[str, str]]]:
    """
    Remove seed names from topic keyword lists; flag ambiguous tokens.

    Returns (cleaned_words, removed_words, review_rows).
    """
    cleaned: list[dict[str, Any]] = []
    removed: list[str] = []
    reviews: list[dict[str, str]] = []

    topic_words_lower = {
        str(item.get("word", "")).lower().strip()
        for item in words
        if str(item.get("word", "")).strip()
    }

    for item in words:
        word = str(item.get("word", "")).strip()
        w_lower = word.lower()

        if w_lower in lexicon.keep_role_tokens:
            cleaned.append(dict(item))
            continue

        if w_lower in lexicon.auto_replace_names:
            removed.append(w_lower)
            continue

        if should_remove_plural_family(w_lower, lexicon, topic_words_lower):
            removed.append(w_lower)
            continue

        snake_reason = classify_snake_glued_token(w_lower, lexicon)
        if snake_reason == "snake_glued_seed_component":
            removed.append(w_lower)
            continue
        if snake_reason == "snake_glued_review":
            entry = dict(item)
            entry["needs_manual_name_review"] = True
            cleaned.append(entry)
            reviews.append({"word": w_lower, "reason": "snake_glued_review"})
            continue

        if should_review_surname(w_lower, lexicon, topic_words_lower):
            removed.append(w_lower)
            continue

        if w_lower in lexicon.ambiguous_review:
            entry = dict(item)
            entry["needs_manual_name_review"] = True
            cleaned.append(entry)
            reviews.append({"word": w_lower, "reason": "ambiguous_review"})
            continue

        cleaned.append(dict(item))

    return cleaned, removed, reviews


def character_name_ratio(
    words: list[dict[str, Any]] | list[str],
    lexicon: CleaningLexicon,
    *,
    original_words: list[dict[str, Any]] | list[str] | None = None,
) -> float:
    """Fraction of topic words that were high-confidence seed names (pre-cleaning)."""
    source = original_words if original_words is not None else words
    if not source:
        return 0.0

    n = 0
    total = 0
    for item in source:
        if isinstance(item, dict):
            word = str(item.get("word", "")).lower().strip()
        else:
            word = str(item).lower().strip()
        if not word or word in lexicon.keep_role_tokens:
            continue
        total += 1
        if word in lexicon.auto_replace_names:
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
        flags.append("character_name_cluster")
        return {
            "character_name_ratio": ratio,
            "content_type": "character_name",
            "posthoc_flags": flags,
            "posthoc_reason": ";".join(flags),
            "exclude_from_axes": True,
            "name_cleaned": name_cleaned,
            "suggested_action": "flag_noise",
        }

    if ratio >= lexicon.ratio_name_contaminated_review:
        flags.append("name_contaminated_review")
        return {
            "character_name_ratio": ratio,
            "content_type": "scene",
            "posthoc_flags": flags,
            "posthoc_reason": ";".join(flags),
            "exclude_from_axes": False,
            "name_cleaned": name_cleaned,
            "suggested_action": "keep",
        }

    return {
        "character_name_ratio": ratio,
        "content_type": "scene",
        "posthoc_flags": flags,
        "posthoc_reason": "",
        "exclude_from_axes": False,
        "name_cleaned": name_cleaned,
        "suggested_action": "keep",
    }


def clean_snippet_text(
    text: str,
    lexicon: CleaningLexicon,
    *,
    nlp=None,
    run_ner: bool = True,
) -> str:
    """Full snippet cleaning: seed pass then optional spaCy NER."""
    from src.common.character_name_cleaning.ner_pass import ner_replace_persons

    text = replace_seed_names_in_snippet(text, lexicon)
    text = text.replace("[NAME]", lexicon.person_placeholder)
    if run_ner and nlp is not None:
        text = ner_replace_persons(text, nlp, lexicon)
    return text
