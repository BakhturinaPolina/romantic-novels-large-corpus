"""Reproducible Stage 11 presentation-figure suite.

Loads saved notebook analysis tables only — does not re-estimate confirmatory models.
"""

from __future__ import annotations

from .build import build_all, build_all_decks, build_v2
from .paths import PresentationPaths, default_paths
from .evidence_metadata import (
    EFFECT_GATE,
    build_all_metadata,
    load_agreement,
    load_components,
    load_primaries,
)

__all__ = [
    "EFFECT_GATE",
    "PresentationPaths",
    "build_all",
    "build_all_decks",
    "build_v2",
    "build_all_metadata",
    "default_paths",
    "load_agreement",
    "load_components",
    "load_primaries",
]
