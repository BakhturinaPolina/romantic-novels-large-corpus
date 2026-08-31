"""H3 manual freeze: emotional vs material dichotomy topic lists + worksheet seeding."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import pandas as pd

from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code
from src.stage11_refined_construct_analysis.config import Stage11Config

LOGGER = logging.getLogger("stage11.h3_manual_freeze")

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
            "Set frozen=true and save as h3_manual_freeze.json to apply."
        ),
    }


def load_h3_manual_freeze(cfg: Stage11Config) -> Optional[Dict[str, Any]]:
    path = default_freeze_path(cfg)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"H3 freeze file must be a JSON object: {path}")
    return data


def expected_h3_freeze_ids(cfg: Stage11Config) -> List[int]:
    """Topic IDs from the decisions worksheet (preferred) or construct coverage union."""
    ws = decisions_worksheet_path(cfg)
    if ws.exists():
        data = json.loads(ws.read_text(encoding="utf-8"))
        ids = [int(d["topic_id"]) for d in data.get("decisions") or []]
        if ids:
            return sorted(set(ids))
    freeze = load_h3_manual_freeze(cfg)
    if freeze:
        ids = [int(d["topic_id"]) for d in freeze.get("decisions") or []]
        if ids:
            return sorted(set(ids))
    return []


def validate_h3_manual_freeze(
    data: Mapping[str, Any],
    *,
    expected_ids: Optional[Sequence[int]] = None,
    require_frozen: bool = True,
) -> List[str]:
    """Return list of validation errors (empty = OK)."""
    errors: List[str] = []
    if require_frozen and not data.get("frozen"):
        errors.append("frozen must be true before applying")
    decisions = data.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        errors.append("decisions must be a non-empty list")
        return errors

    expected = set(int(x) for x in (expected_ids or []))
    seen: Set[int] = set()
    for i, d in enumerate(decisions):
        if not isinstance(d, dict):
            errors.append(f"decisions[{i}] is not an object")
            continue
        try:
            tid = int(d["topic_id"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"decisions[{i}] missing topic_id")
            continue
        seen.add(tid)
        decision = str(d.get("decision") or "").strip().upper()
        if decision not in VALID_DECISIONS:
            errors.append(f"topic {tid}: decision must be KEEP or REMOVE (got {decision!r})")
            continue
        rel = str(d.get("relationship_directed") or "").strip().lower()
        func = str(d.get("function") or "").strip().lower()
        if rel not in VALID_YN or rel == "":
            errors.append(f"topic {tid}: relationship_directed must be yes or no")
        if func not in VALID_FUNCTION or func == "":
            errors.append(f"topic {tid}: function must be set")
        if decision == "KEEP":
            final = normalize_code(d.get("final_code")) or str(d.get("final_code") or "").strip()
            if not final:
                errors.append(f"topic {tid}: KEEP requires final_code")
            elif final == "S0":
                errors.append(f"topic {tid}: use REMOVE instead of KEEP with S0")
            elif final not in H3_MANUAL_FREEZE_CODES and not str(final).startswith("S"):
                errors.append(f"topic {tid}: invalid final_code {final!r}")

    if expected:
        missing = sorted(expected - seen)
        extra = sorted(seen - expected)
        if missing:
            errors.append(f"missing topic_ids: {missing}")
        if extra:
            errors.append(f"unexpected topic_ids: {extra}")
    return errors


def freeze_overrides(data: Mapping[str, Any]) -> Dict[int, Dict[str, str]]:
    """Map topic_id → {decision, final_code, action_tag} for master application."""
    out: Dict[int, Dict[str, str]] = {}
    for d in data.get("decisions") or []:
        tid = int(d["topic_id"])
        decision = str(d.get("decision") or "").strip().upper()
        if decision == "REMOVE":
            out[tid] = {
                "decision": "REMOVE",
                "final_code": "S0",
                "action_tag": "H3:HUMAN_REMOVE",
            }
        elif decision == "KEEP":
            final = normalize_code(d.get("final_code")) or str(d.get("final_code") or "").strip()
            out[tid] = {
                "decision": "KEEP",
                "final_code": final,
                "action_tag": "H3:HUMAN_KEEP",
            }
    return out


def _patch_h3_family_props(row: Mapping[str, Any], final_code: str) -> str:
    """Rewrite H3 Pass-B proportions so W_tk admits the human final_code."""
    raw = row.get("family_proportions_json")
    if isinstance(raw, dict):
        blob = dict(raw)
    elif isinstance(raw, str) and raw.strip():
        try:
            blob = json.loads(raw)
        except json.JSONDecodeError:
            blob = {}
    else:
        blob = {}
    if final_code == "S0":
        blob["H3"] = {}
    else:
        blob["H3"] = {final_code: 1.0}
    return json.dumps(blob)


def apply_h3_manual_freeze_to_master(
    master: pd.DataFrame,
    cfg: Stage11Config,
    *,
    freeze_data: Optional[Mapping[str, Any]] = None,
) -> pd.DataFrame:
    """Override security_code from a frozen human decision file.

    No-op if the freeze file is missing or frozen=false.
    """
    data = freeze_data if freeze_data is not None else load_h3_manual_freeze(cfg)
    if not data or not data.get("frozen"):
        return master

    expected = expected_h3_freeze_ids(cfg)
    errors = validate_h3_manual_freeze(
        data, expected_ids=expected or None, require_frozen=True
    )
    if errors:
        raise ValueError("Invalid H3 manual freeze:\n  - " + "\n  - ".join(errors))

    overrides = freeze_overrides(data)
    if not overrides:
        return master

    df = master.copy()
    if "adjudication_actions" not in df.columns:
        df["adjudication_actions"] = [[] for _ in range(len(df))]

    n_keep = n_remove = 0
    for idx, row in df.iterrows():
        tid = int(row["topic_id"])
        ov = overrides.get(tid)
        if not ov:
            continue
        final = ov["final_code"]
        df.at[idx, "security_code"] = final
        df.at[idx, "family_proportions_json"] = _patch_h3_family_props(row, final)
        actions = row.get("adjudication_actions")
        if isinstance(actions, list):
            new_actions = list(actions) + [ov["action_tag"]]
        elif isinstance(actions, str) and actions:
            new_actions = [actions, ov["action_tag"]]
        else:
            new_actions = [ov["action_tag"]]
        df.at[idx, "adjudication_actions"] = new_actions
        if ov["decision"] == "REMOVE":
            n_remove += 1
        else:
            n_keep += 1

    LOGGER.info(
        "Applied H3 manual freeze: KEEP=%d REMOVE=%d (of %d overrides)",
        n_keep,
        n_remove,
        len(overrides),
    )
    return df
