"""spaCy NER for snippet and topic-keyword person detection."""

from __future__ import annotations

import logging
import re
from typing import Iterable

from src.common.character_name_cleaning.lexicon import CleaningLexicon

LOGGER = logging.getLogger("character_name_cleaning.ner")

_SPACY_NLP = None

TITLE_NAME_PATTERN = re.compile(
    r"\b(doctor|dr|sir|lady|lord|duke|duchess|captain|officer|detective)\s+([A-Z][a-z]+)\b",
    re.IGNORECASE,
)

_TOKEN_SPLIT = re.compile(r"[\s\-']+")


def get_spacy_nlp():
    """Load en_core_web_sm once with NER enabled."""
    global _SPACY_NLP
    if _SPACY_NLP is not None:
        return _SPACY_NLP
    try:
        import spacy

        nlp = spacy.load("en_core_web_sm")
        if "ner" not in nlp.pipe_names:
            nlp.add_pipe("ner")
        _SPACY_NLP = nlp
        return nlp
    except OSError as exc:
        LOGGER.warning("spaCy model unavailable: %s", exc)
        return None


def _tokenize_entity(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_SPLIT.split(text.strip()) if t]


def person_tokens_from_doc(doc, lexicon: CleaningLexicon) -> set[str]:
    """Extract lowercase person tokens from a parsed spaCy doc."""
    names: set[str] = set()
    if doc is None:
        return names
    for ent in doc.ents:
        if ent.label_ != "PERSON":
            continue
        for tok in _tokenize_entity(ent.text):
            if tok and tok not in lexicon.keep_role_tokens:
                names.add(tok)
    return names


def extract_person_tokens_from_text(
    text: str,
    nlp,
    lexicon: CleaningLexicon,
) -> set[str]:
    if not text or nlp is None:
        return set()
    try:
        return person_tokens_from_doc(nlp(text), lexicon)
    except Exception as exc:
        LOGGER.warning("NER extraction failed: %s", exc)
        return set()


def extract_person_tokens_from_snippets(
    snippets: Iterable[str],
    nlp,
    lexicon: CleaningLexicon,
) -> set[str]:
    names: set[str] = set()
    if nlp is None:
        return names
    for snippet in snippets:
        if not snippet:
            continue
        names |= extract_person_tokens_from_text(snippet, nlp, lexicon)
    return names


def probe_topic_word_is_person(
    word: str,
    nlp,
    lexicon: CleaningLexicon,
) -> bool:
    """Run NER on a minimal probe sentence for a single topic keyword."""
    w = word.strip()
    if not w or len(w) < 2:
        return False
    lower = w.lower()
    if lower in lexicon.never_remove_topic_words:
        return False
    if nlp is None:
        return False

    token = w.title() if w.islower() else w
    sentence = lexicon.ner_probe_template.format(token=token)
    try:
        doc = nlp(sentence)
    except Exception as exc:
        LOGGER.warning("NER probe failed for %r: %s", word, exc)
        return False

    for ent in doc.ents:
        if ent.label_ != "PERSON":
            continue
        ent_tokens = _tokenize_entity(ent.text)
        if lower in ent_tokens or token.lower() in ent_tokens:
            return True
    return False


def build_topic_person_lexicon(
    topic_snippets: dict[int | str, list[str]],
    nlp,
    lexicon: CleaningLexicon,
) -> dict[str, set[str]]:
    """Per-topic PERSON tokens discovered from representative snippets."""
    out: dict[str, set[str]] = {}
    for topic_id, snippets in topic_snippets.items():
        out[str(topic_id)] = extract_person_tokens_from_snippets(
            snippets, nlp, lexicon
        )
    return out


def is_person_topic_word(
    word: str,
    *,
    topic_person_tokens: set[str],
    nlp,
    lexicon: CleaningLexicon,
) -> bool:
    """True if word is a PERSON via snippet context or NER probe."""
    lower = word.lower().strip()
    if not lower or lower in lexicon.never_remove_topic_words:
        return False
    if lower in topic_person_tokens:
        return True
    return probe_topic_word_is_person(word, nlp, lexicon)


def apply_title_name_pattern(text: str, lexicon: CleaningLexicon) -> str:
    """Replace Title Name patterns (Lord Ashford -> Lord [person])."""
    placeholder = lexicon.person_placeholder

    def _repl(match: re.Match[str]) -> str:
        return f"{match.group(1)} {placeholder}"

    return TITLE_NAME_PATTERN.sub(_repl, text)


def ner_replace_persons(text: str, nlp, lexicon: CleaningLexicon) -> str:
    """Replace spaCy PERSON entities with [person]; preserve role tokens."""
    if not text or nlp is None:
        return text

    text = apply_title_name_pattern(text, lexicon)
    placeholder = lexicon.person_placeholder

    try:
        if "ner" not in nlp.pipe_names:
            return text
        doc = nlp(text)
        if not doc.ents:
            return text

        result = text
        for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
            if ent.label_ != "PERSON":
                continue
            span_tokens = _tokenize_entity(ent.text)
            if span_tokens and all(t in lexicon.keep_role_tokens for t in span_tokens):
                continue
            result = result[: ent.start_char] + placeholder + result[ent.end_char :]
        return result
    except Exception as exc:
        LOGGER.warning("NER anonymization failed: %s", exc)
        return text


def clean_snippet_text(
    text: str,
    lexicon: CleaningLexicon,
    *,
    nlp=None,
) -> str:
    """Anonymize snippet via title pattern + spaCy NER."""
    nlp = nlp or get_spacy_nlp()
    text = text.replace("[NAME]", lexicon.person_placeholder)
    if nlp is None:
        return apply_title_name_pattern(text, lexicon)
    return ner_replace_persons(text, nlp, lexicon)
