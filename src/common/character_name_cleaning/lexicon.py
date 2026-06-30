"""Cleaning configuration (role tokens + thresholds; names from NER only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

from src.common.config import resolve_path

DEFAULT_CONFIG = Path("configs/character_name_cleaning.yaml")


@lru_cache(maxsize=1)
def _english_stopwords() -> frozenset[str]:
    try:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

        return frozenset(w.lower() for w in ENGLISH_STOP_WORDS)
    except ImportError:
        return frozenset()


@dataclass
class CleaningLexicon:
    keep_role_tokens: frozenset[str] = field(default_factory=frozenset)
    ratio_character_name_cluster: float = 0.50
    ratio_name_contaminated_review: float = 0.20
    person_placeholder: str = "[person]"
    ner_probe_template: str = "{token} walked into the room and looked around."

    @property
    def never_remove_topic_words(self) -> frozenset[str]:
        """Function words and role/status tokens never stripped from topic keywords."""
        return _english_stopwords() | self.keep_role_tokens


def load_lexicon(config_path: Path | None = None) -> CleaningLexicon:
    path = resolve_path(config_path or DEFAULT_CONFIG)
    if not path.exists():
        raise FileNotFoundError(f"Character name cleaning config not found: {path}")

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    def _lower_set(key: str) -> frozenset[str]:
        items = raw.get(key) or []
        return frozenset(str(x).lower().strip() for x in items if str(x).strip())

    thresholds = raw.get("ratio_thresholds") or {}
    return CleaningLexicon(
        keep_role_tokens=_lower_set("keep_role_tokens"),
        ratio_character_name_cluster=float(
            thresholds.get("character_name_cluster", 0.50)
        ),
        ratio_name_contaminated_review=float(
            thresholds.get("name_contaminated_review", 0.20)
        ),
        person_placeholder=str(raw.get("person_placeholder", "[person]")),
        ner_probe_template=str(
            raw.get(
                "ner_probe_template",
                "{token} walked into the room and looked around.",
            )
        ),
    )
