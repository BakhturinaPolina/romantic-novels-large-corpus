"""spaCy NER second pass for snippet anonymization."""

from __future__ import annotations

import logging
import re

from src.common.character_name_cleaning.lexicon import CleaningLexicon

LOGGER = logging.getLogger("character_name_cleaning.ner")

_SPACY_NLP = None

TITLE_NAME_PATTERN = re.compile(
    r"\b(doctor|dr|sir|lady|lord|duke|duchess|captain|officer|detective)\s+([A-Z][a-z]+)\b",
    re.IGNORECASE,
)


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


def apply_title_name_pattern(text: str, lexicon: CleaningLexicon) -> str:
    """Replace Title Name patterns before NER (Lord Ashford -> Lord [person])."""
    placeholder = lexicon.person_placeholder

    def _repl(match: re.Match[str]) -> str:
        title = match.group(1)
        return f"{title} {placeholder}"

    return TITLE_NAME_PATTERN.sub(_repl, text)


def ner_replace_persons(text: str, nlp, lexicon: CleaningLexicon) -> str:
    """Replace spaCy PERSON entities with [person]; skip role tokens."""
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
            span_text = ent.text.lower().strip()
            if span_text in lexicon.keep_role_tokens:
                continue
            result = result[: ent.start_char] + placeholder + result[ent.end_char :]
        return result
    except Exception as exc:
        LOGGER.warning("NER anonymization failed: %s", exc)
        return text
