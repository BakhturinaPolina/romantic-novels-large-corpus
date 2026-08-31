"""H3 manual freeze: emotional vs material dichotomy topic lists + worksheet seeding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import pandas as pd

from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code
from src.stage11_refined_construct_analysis.config import Stage11Config

# Dichotomy + confounders (plan-aligned review scope — not the full H3 audit pool)
BUCKET_ORDER: Tuple[str, ...] = (
    "emotional",
    "material",
    "appearance_status",
)

H3_EMOTIONAL_CODES: Set[str] = {"S1", "S2", "S3", "S4"}
H3_MATERIAL_CODES: Set[str] = {"S8", "S9"}
H3_APPEARANCE_STATUS_CODES: Set[str] = {"S12", "S13", "S14", "S15"}

H3_MANUAL_FREEZE_CODES: Set[str] = (
    H3_EMOTIONAL_CODES | H3_MATERIAL_CODES | H3_APPEARANCE_STATUS_CODES | {"S0", "S10", "S16", "MIXED"}
)

VALID_DECISIONS = {"KEEP", "REMOVE"}
VALID_YN = {"yes", "no", ""}
VALID_FUNCTION = {
    "emotional",
    "material_money",
    "material_housing",
    "appearance_status",
    "other",
    "",
}


def bucket_for_code(code: Any) -> Optional[str]:
    canon = normalize_code(code) if code is not None else None
    if canon in H3_EMOTIONAL_CODES:
        return "emotional"
    if canon in H3_MATERIAL_CODES:
        return "material"
    if canon in H3_APPEARANCE_STATUS_CODES:
        return "appearance_status"
    return None


def default_freeze_path(cfg: Stage11Config) -> Path:
    custom = cfg.section("h3_manual_freeze_path", default=None)
    if custom:
        p = Path(custom)
        return p if p.is_absolute() else cfg.root / p
    return cfg.output_path("human_review_dir") / "h3_manual_freeze.json"


def decisions_worksheet_path(cfg: Stage11Config) -> Path:
    return cfg.output_path("human_review_dir") / "h3_manual_freeze_decisions.json"


def load_construct_coverage_ids(cfg: Stage11Config) -> Dict[str, List[int]]:
    """Preferred IDs from construct_coverage composites/atoms (strict coverage)."""
    path = cfg.output_path("constructs_dir") / "construct_coverage.json"
    out: Dict[str, List[int]] = {
        "emotional": [],
        "material": [],
        "appearance_status": [],
    }
    if not path.exists():
        return out
    data = json.loads(path.read_text(encoding="utf-8"))
    atoms = data.get("atoms") or {}
    composites = data.get("composites") or {}

    emo = (composites.get("RAX_h3_emotional_side") or {}).get("topic_ids")
    if not emo:
        emo = (atoms.get("RAX_emotional_security") or {}).get("topic_ids") or []
        emo = list(emo) + list(
            (atoms.get("RAX_commitment_security") or {}).get("topic_ids") or []
        )
    if emo:
        out["emotional"] = sorted({int(x) for x in emo})

    mat = (composites.get("RAX_h3_material_side") or {}).get("topic_ids")
    if not mat:
        mat = list((atoms.get("RAX_material_provision") or {}).get("topic_ids") or [])
        mat += list((atoms.get("RAX_housing_security") or {}).get("topic_ids") or [])
    if mat:
        out["material"] = sorted({int(x) for x in mat})

    app = (composites.get("RAX_social_presentation") or {}).get("topic_ids")
    if not app:
        app = list((atoms.get("RAX_appearance_grooming") or {}).get("topic_ids") or [])
        app += list((atoms.get("RAX_status_display") or {}).get("topic_ids") or [])
        app += list((atoms.get("RAX_workplace_status") or {}).get("topic_ids") or [])
    if app:
        out["appearance_status"] = sorted({int(x) for x in app})
    return out


def resolve_h3_freeze_topic_ids(cfg: Stage11Config, master: pd.DataFrame) -> List[int]:
    """Union coverage atoms with all master topics coded in the dichotomy set.

    Includes non-strict S8/S9 near-misses (e.g. 22, 174) so humans can review
    the material side exhaustively for the emotional-vs-material question.
    Drops coverage orphans whose live security_code is no longer in-scope.
    """
    by_bucket = load_construct_coverage_ids(cfg)
    seen: Set[int] = set()
    ordered: List[int] = []
    code_by_tid: Dict[int, str] = {}
    if "security_code" in master.columns and "topic_id" in master.columns:
        for _, row in master.iterrows():
            tid = int(row["topic_id"])
            code = normalize_code(row.get("security_code")) or str(row.get("security_code") or "")
            code_by_tid[tid] = code

    def _add(tid: int) -> None:
        if tid not in seen and tid >= 0:
            seen.add(tid)
            ordered.append(tid)

    for bucket in BUCKET_ORDER:
        for tid in by_bucket.get(bucket) or []:
            _add(int(tid))

    want = H3_EMOTIONAL_CODES | H3_MATERIAL_CODES | H3_APPEARANCE_STATUS_CODES
    for tid, code in code_by_tid.items():
        if code in want:
            _add(tid)

    # Keep only topics with a live dichotomy bucket (drop stale coverage orphans).
    return [tid for tid in ordered if bucket_for_code(code_by_tid.get(tid)) is not None]


def seed_decisions_worksheet(df: pd.DataFrame) -> Dict[str, Any]:
    decisions = []
    for _, row in df.iterrows():
        tid = int(row["topic_id"])
        code = normalize_code(row.get("security_code")) or str(row.get("security_code") or "")
        bucket = bucket_for_code(code) or ""
        function_suggest = {
            "emotional": "emotional",
            "material": "material_money" if code == "S8" else "material_housing",
            "appearance_status": "appearance_status",
        }.get(bucket, "")
        decisions.append(
            {
                "topic_id": tid,
                "topic_label": row.get("current_topic_label"),
                "suggested_code": code,
                "decision": "",  # KEEP | REMOVE
                "final_code": code,
                "relationship_directed": "",  # yes | no
                "function": function_suggest,  # emotional | material_money | material_housing | appearance_status | other
                "notes": "",
            }
        )
    return {
        "hypothesis": "H3",
        "frozen": False,
        "n_topics": len(decisions),
        "decisions": decisions,
        "instructions": (
            "Fill decision (KEEP|REMOVE), relationship_directed (yes|no), "
            "function (emotional|material_money|material_housing|appearance_status|other), "
            "and final_code for KEEP rows. "
            "Set frozen=true and save as h3_manual_freeze.json to apply (when wired)."
        ),
    }
