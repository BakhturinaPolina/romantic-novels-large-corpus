"""Load Stage08 labeling lexicon from YAML config."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from src.common.config import load_config

DEFAULT_LEXICON_PATH = Path("configs/stage08_labeling_lexicon.yaml")


@lru_cache(maxsize=1)
def load_labeling_lexicon(path: str | None = None) -> dict[str, Any]:
    cfg_path = Path(path) if path else DEFAULT_LEXICON_PATH
    if not cfg_path.is_file():
        return {}
    return load_config(cfg_path)


def explicit_sexual_terms(path: str | None = None) -> set[str]:
    lex = load_labeling_lexicon(path)
    return {str(t).lower() for t in lex.get("explicit_sexual_terms", [])}


def forbidden_neutral_words(path: str | None = None) -> set[str]:
    lex = load_labeling_lexicon(path)
    return {str(t).lower() for t in lex.get("forbidden_neutral_violation_words", [])}


def family_relation_terms(path: str | None = None) -> set[str]:
    lex = load_labeling_lexicon(path)
    return {str(t).lower() for t in lex.get("family_relation_terms", [])}
