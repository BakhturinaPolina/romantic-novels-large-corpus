"""Load Stage07 topic quality CSV hints for Stage08 labeling (advisory flags only)."""

from __future__ import annotations

import json
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
    stage07_flags: list[str] = field(default_factory=list)
    stage07_reason: str = ""
    recommended_next_step: str = "stage08_labeling"
    hard_exclude_candidate: bool = False
    soft_review_candidate: bool = False
    exclude_from_axes: bool = False
    suggested_action: str = "keep"
    tier: str = "mid"
    # Legacy fields
    content_type: str = ""
    posthoc_flags: list[str] = field(default_factory=list)
    posthoc_reason: str = ""

    def format_for_prompt(self) -> str:
        flags = ", ".join(self.stage07_flags) if self.stage07_flags else "(none)"
        return (
            f"doc_count={self.doc_count}, tier={self.tier}, "
            f"stage07_flags=[{flags}], recommended_next_step={self.recommended_next_step}, "
            f"hard_exclude_candidate={self.hard_exclude_candidate}, "
            f"soft_review_candidate={self.soft_review_candidate} "
            f"(advisory — do not skip labeling unless pipeline filter applies), "
            f"stage07_reason={self.stage07_reason or '(none)'}"
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
    return [p for p in text.replace("|", ";").split(";") if p]


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

        def _bool(val: Any) -> bool:
            if isinstance(val, str):
                return val.lower() in ("true", "1", "yes")
            return bool(val)

        stage07_flags = _parse_flags(row.get("stage07_flags"))
        if not stage07_flags:
            stage07_flags = _parse_flags(row.get("posthoc_flags"))

        hard_exclude = _bool(row.get("hard_exclude_candidate", False))
        if not hard_exclude:
            hard_exclude = _bool(row.get("exclude_from_axes", False))

        soft_review = _bool(row.get("soft_review_candidate", False))

        hints[topic_id] = TopicHints(
            topic_id=topic_id,
            doc_count=count,
            stage07_flags=stage07_flags,
            stage07_reason=str(row.get("stage07_reason", row.get("posthoc_reason", "")) or "").strip(),
            recommended_next_step=str(
                row.get("recommended_next_step", "stage08_labeling") or "stage08_labeling"
            ),
            hard_exclude_candidate=hard_exclude,
            soft_review_candidate=soft_review,
            exclude_from_axes=hard_exclude,
            suggested_action=str(row.get("suggested_action", "keep") or "keep").strip().lower(),
            tier=_tier_for_count(count, core_min_docs, mid_min_docs),
            content_type=str(row.get("content_type", "") or ""),
            posthoc_flags=stage07_flags,
            posthoc_reason=str(row.get("posthoc_reason", "") or "").strip(),
        )
    return hints


def load_quality_adjudication_results(
    jsonl_path: Path | str,
) -> dict[int, dict[str, Any]]:
    """Load Stage 08A adjudication results keyed by topic_id."""
    path = Path(jsonl_path)
    if not path.is_file():
        return {}
    out: dict[int, dict[str, Any]] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            out[int(row["topic_id"])] = row
    return out


def topic_ids_for_labeling(
    quality_hints: dict[int, TopicHints],
    adjudication: dict[int, dict[str, Any]] | None = None,
    *,
    skip_hard_exclude: bool = True,
    require_08a_pass: bool = True,
    label_all_topics: bool = False,
) -> set[int]:
    """Return topic IDs that should proceed to Stage 08B labeling."""
    if label_all_topics:
        return set(quality_hints.keys())

    allowed: set[int] = set()
    for topic_id, hints in quality_hints.items():
        if skip_hard_exclude and hints.hard_exclude_candidate:
            continue
        if hints.soft_review_candidate and require_08a_pass:
            adj = (adjudication or {}).get(topic_id)
            if adj is None:
                continue
            if adj.get("llm_quality_decision") != "pass_to_labeling":
                continue
        allowed.add(topic_id)
    return allowed


def filter_topics_dict(
    topics: dict[int, list[str]],
    quality_hints: dict[int, TopicHints] | None,
    adjudication: dict[int, dict[str, Any]] | None = None,
    *,
    skip_hard_exclude: bool = True,
    require_08a_pass: bool = True,
    label_all_topics: bool = False,
) -> dict[int, list[str]]:
    """Filter a topic_id -> keywords map for Stage 08B."""
    if label_all_topics or quality_hints is None:
        return topics
    allowed = topic_ids_for_labeling(
        quality_hints,
        adjudication,
        skip_hard_exclude=skip_hard_exclude,
        require_08a_pass=require_08a_pass,
        label_all_topics=False,
    )
    return {tid: kws for tid, kws in topics.items() if tid in allowed}
