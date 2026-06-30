"""Pre-Stage07 character name cleaning via spaCy NER."""

from src.common.character_name_cleaning.lexicon import CleaningLexicon, load_lexicon
from src.common.character_name_cleaning.ner_pass import (
    clean_snippet_text,
    get_spacy_nlp,
)
from src.common.character_name_cleaning.pipeline import run_cleaning_pipeline
from src.common.character_name_cleaning.seed_pass import (
    character_name_ratio,
    classify_topic_by_ratio,
    clean_topic_words,
)
from src.common.character_name_cleaning.validate import assert_clean_inputs

__all__ = [
    "CleaningLexicon",
    "assert_clean_inputs",
    "character_name_ratio",
    "classify_topic_by_ratio",
    "clean_snippet_text",
    "clean_topic_words",
    "get_spacy_nlp",
    "load_lexicon",
    "run_cleaning_pipeline",
]
