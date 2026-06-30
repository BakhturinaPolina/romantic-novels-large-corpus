"""Load and resolve character-name cleaning lexicons from YAML config."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from src.common.config import resolve_path

DEFAULT_CONFIG = Path("configs/character_name_cleaning.yaml")


@dataclass
class CleaningLexicon:
    keep_role_tokens: frozenset[str] = field(default_factory=frozenset)
    high_confidence_names: frozenset[str] = field(default_factory=frozenset)
    ambiguous_review: frozenset[str] = field(default_factory=frozenset)
    surname_review: frozenset[str] = field(default_factory=frozenset)
    flower_co_words: frozenset[str] = field(default_factory=frozenset)
    ratio_character_name_cluster: float = 0.50
    ratio_name_contaminated_review: float = 0.20
    person_placeholder: str = "[person]"
    extend_lexicon_from_topics: bool = True
    topic_derived_names: frozenset[str] = field(default_factory=frozenset)

    @property
    def auto_replace_names(self) -> frozenset[str]:
        """High-confidence names minus ambiguous words (ambiguous wins)."""
        return self.high_confidence_names | self.topic_derived_names - self.ambiguous_review

    @property
    def full_seed_lexicon(self) -> frozenset[str]:
        return self.auto_replace_names | self.surname_review


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
        high_confidence_names=_lower_set("high_confidence_names"),
        ambiguous_review=_lower_set("ambiguous_review"),
        surname_review=_lower_set("surname_review"),
        flower_co_words=_lower_set("flower_co_words"),
        ratio_character_name_cluster=float(
            thresholds.get("character_name_cluster", 0.50)
        ),
        ratio_name_contaminated_review=float(
            thresholds.get("name_contaminated_review", 0.20)
        ),
        person_placeholder=str(raw.get("person_placeholder", "[person]")),
        extend_lexicon_from_topics=bool(raw.get("extend_lexicon_from_topics", True)),
    )
