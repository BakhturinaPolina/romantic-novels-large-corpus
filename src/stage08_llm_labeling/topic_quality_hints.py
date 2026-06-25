"""Load Stage07 topic quality CSV hints for Stage08 labeling (advisory flags only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

CORE_MIN_DOCS = 800
MID_MIN_DOCS = 200


@dataclass
class TopicHints:
    topic_id: int
    doc_count: int = 0
    content_type: str = "scene"
    posthoc_flags: list[str] = field(default_factory=list)
    posthoc_reason: str = ""
    exclude_from_axes: bool = False
    suggested_action: str = "keep"
    tier: str = "mid"

    def format_for_prompt(self) -> str:
        flags = ", ".join(self.posthoc_flags) if self.posthoc_flags else "(none)"
        return (
            f"doc_count={self.doc_count}, tier={self.tier}, "
            f"stage07_content_type={self.content_type}, posthoc_flags=[{flags}], "
            f"stage07_exclude_from_axes={self.exclude_from_axes} (advisory — do not skip labeling), "
            f"posthoc_reason={self.posthoc_reason or '(none)'}"
        )


def _parse_flags(raw: Any) -> list[str]:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return []
    if isinstance(raw, list):
        return [str(x) for x in raw]
    text = str(raw).strip()
    if not text or text == "[]":
        return []
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
    return [text]


def _tier_for_count(count: int, core_min: int = CORE_MIN_DOCS, mid_min: int = MID_MIN_DOCS) -> str:
    if count >= core_min:
        return "core"
    if count >= mid_min:
        return "mid"
    return "tiny"


def load_topic_quality_hints(
    csv_path: Path | str,
    *,
    core_min_docs: int = CORE_MIN_DOCS,
    mid_min_docs: int = MID_MIN_DOCS,
) -> dict[int, TopicHints]:
    """Load per-topic advisory hints from Stage07 quality CSV."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"Quality CSV not found: {path}")

    df = pd.read_csv(path)
    if "Topic" not in df.columns:
        raise ValueError(f"Quality CSV missing Topic column: {path}")

    hints: dict[int, TopicHints] = {}
    for _, row in df.iterrows():
        topic_id = int(row["Topic"])
        if topic_id == -1:
            continue
        count = int(row.get("Count", 0) or 0)
        exclude = row.get("exclude_from_axes", False)
        if isinstance(exclude, str):
            exclude = exclude.lower() in ("true", "1", "yes")
        else:
            exclude = bool(exclude)
        action = str(row.get("suggested_action", "keep") or "keep").strip().lower()
        hints[topic_id] = TopicHints(
            topic_id=topic_id,
            doc_count=count,
            content_type=str(row.get("content_type", "scene") or "scene"),
            posthoc_flags=_parse_flags(row.get("posthoc_flags")),
            posthoc_reason=str(row.get("posthoc_reason", "") or "").strip(),
            exclude_from_axes=exclude,
            suggested_action=action,
            tier=_tier_for_count(count, core_min_docs, mid_min_docs),
        )
    return hints
