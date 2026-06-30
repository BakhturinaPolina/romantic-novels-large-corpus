"""Load Stage 07 topic-quality audit configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from src.common.config import resolve_path

DEFAULT_STAGE07_CONFIG = Path("configs/stage07_topic_quality.yaml")

REPRESENTATIONS_DEFAULT = ("Main", "KeyBERT", "MMR", "POS")


@dataclass
class Stage07Thresholds:
    ultra_tiny_docs: int = 10
    small_docs: int = 30
    low_support_docs: int = 50
    min_content_pos_per_rep: int = 3
    min_coherence_c_v: float = 0.0
    min_representation_diversity: float = 0.5
    min_snippets: int = 2


@dataclass
class Stage07Config:
    representations: tuple[str, ...] = REPRESENTATIONS_DEFAULT
    top_k: int = 10
    snippets_per_topic: int = 6
    thresholds: Stage07Thresholds = field(default_factory=Stage07Thresholds)
    hard_exclude_rules: tuple[str, ...] = (
        "publisher_boilerplate",
        "multilingual_artifact",
        "empty_all_representations",
    )
    soft_review_rules: tuple[str, ...] = (
        "ultra_tiny_topic",
        "small_topic",
        "few_words_all_representations",
        "low_coherence_all_representations",
        "low_diversity_all_representations",
        "possible_character_residue",
        "missing_or_too_few_snippets",
    )


def load_stage07_config(config_path: Path | None = None) -> Stage07Config:
    path = resolve_path(config_path or DEFAULT_STAGE07_CONFIG)
    if not path.is_file():
        return Stage07Config()

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    reps = tuple(str(r) for r in raw.get("representations", REPRESENTATIONS_DEFAULT))
    th = raw.get("thresholds", {})
    thresholds = Stage07Thresholds(
        ultra_tiny_docs=int(th.get("ultra_tiny_docs", 10)),
        small_docs=int(th.get("small_docs", 30)),
        low_support_docs=int(th.get("low_support_docs", 50)),
        min_content_pos_per_rep=int(th.get("min_content_pos_per_rep", 3)),
        min_coherence_c_v=float(th.get("min_coherence_c_v", 0.0)),
        min_representation_diversity=float(th.get("min_representation_diversity", 0.5)),
        min_snippets=int(th.get("min_snippets", 2)),
    )
    return Stage07Config(
        representations=reps,
        top_k=int(raw.get("top_k", 10)),
        snippets_per_topic=int(raw.get("snippets_per_topic", 6)),
        thresholds=thresholds,
        hard_exclude_rules=tuple(str(r) for r in raw.get("hard_exclude_rules", ())),
        soft_review_rules=tuple(str(r) for r in raw.get("soft_review_rules", ())),
    )
