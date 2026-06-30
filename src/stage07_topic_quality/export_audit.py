"""Write Stage 07B audit artifacts for manual review and downstream LLM stages."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger("stage07.export_audit")

REPRESENTATIONS = ("Main", "KeyBERT", "MMR", "POS")


def _parse_flags(value: Any) -> list[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    text = str(value).strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
    return [p for p in text.replace("|", ";").split(";") if p]


def _row_representations(row: pd.Series) -> dict[str, dict[str, Any]]:
    reps: dict[str, dict[str, Any]] = {}
    for rep in REPRESENTATIONS:
        words = row.get(f"{rep}_words")
        if isinstance(words, str):
            try:
                words = json.loads(words.replace("'", '"'))
            except (json.JSONDecodeError, ValueError):
                words = [w.strip() for w in words.strip("[]").split(",") if w.strip()]
        if not isinstance(words, list):
            words = []
        reps[rep] = {
            "words": words,
            "n_words": int(row.get(f"{rep}_n_words", 0) or 0),
            "n_unique_words": int(row.get(f"{rep}_n_unique_words", 0) or 0),
            "n_content_pos": int(row.get(f"{rep}_n_content_pos", 0) or 0),
            "coherence_c_v": row.get(f"{rep}_coherence_c_v"),
            "diversity_simple": row.get(f"{rep}_diversity_simple"),
        }
    return reps


def _row_snippets(row: pd.Series, *, max_snippets: int = 6) -> list[str]:
    snippets: list[str] = []
    for i in range(1, max_snippets + 1):
        col = f"snippet_{i}"
        if col in row.index:
            text = str(row.get(col, "") or "").strip()
            if text:
                snippets.append(text)
    return snippets


def build_review_packet(row: pd.Series) -> dict[str, Any]:
    """One JSON object for manual review / Stage 08A."""
    topic_id = int(row["Topic"])
    flags = _parse_flags(row.get("stage07_flags"))
    return {
        "topic_id": topic_id,
        "n_assigned_docs": int(row.get("Count", 0) or 0),
        "n_snippets_available": int(row.get("n_snippets_available", 0) or 0),
        "representations": _row_representations(row),
        "snippets": _row_snippets(row),
        "stage07_flags": flags,
        "stage07_reason": str(row.get("stage07_reason", "") or ""),
        "hard_exclude_candidate": bool(row.get("hard_exclude_candidate")),
        "soft_review_candidate": bool(row.get("soft_review_candidate")),
        "recommended_next_step": str(row.get("recommended_next_step", "") or ""),
    }


def write_stage07_audit_artifacts(
    quality_df: pd.DataFrame,
    out_dir: Path,
    *,
    model_tag: str = "placeholder_v4_call73",
) -> dict[str, Path]:
    """Write four Stage 07B artifacts; return paths."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    audit_path = out_dir / "stage07_topic_quality_audit.csv"
    noise_path = out_dir / "stage07_noise_candidates.csv"
    packet_path = out_dir / "stage07_manual_review_packet.jsonl"
    decisions_path = out_dir / "stage07_manual_decisions.csv"
    legacy_quality = out_dir / f"topic_quality_{model_tag}.csv"
    legacy_noise = out_dir / f"topic_noise_candidates_{model_tag}.csv"

    quality_df.to_csv(audit_path, index=False)
    quality_df[quality_df["noise_candidate"]].to_csv(noise_path, index=False)
    quality_df.to_csv(legacy_quality, index=False)
    quality_df[quality_df["noise_candidate"]].to_csv(legacy_noise, index=False)

    review_df = quality_df[
        quality_df["hard_exclude_candidate"] | quality_df["soft_review_candidate"]
    ]
    with open(packet_path, "w", encoding="utf-8") as f:
        for _, row in review_df.iterrows():
            f.write(json.dumps(build_review_packet(row), ensure_ascii=False) + "\n")

    decisions = quality_df[["Topic", "recommended_next_step"]].copy()
    decisions.rename(columns={"Topic": "topic_id"}, inplace=True)
    decisions["manual_decision"] = ""
    decisions["manual_note"] = ""
    decisions.to_csv(decisions_path, index=False)

    paths = {
        "audit_csv": audit_path,
        "noise_candidates_csv": noise_path,
        "manual_review_packet": packet_path,
        "manual_decisions_csv": decisions_path,
        "legacy_quality_csv": legacy_quality,
        "legacy_noise_csv": legacy_noise,
    }
    logger.info("Wrote Stage07 audit artifacts to %s", out_dir)
    return paths
