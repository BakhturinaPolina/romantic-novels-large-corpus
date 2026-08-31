#!/usr/bin/env python3
"""Auto-flag ambiguous H6-v2 audits and freeze membership JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import yaml

from src.stage11_refined_construct_analysis.audits.runner import (
    PASS_FILES,
    audit_dir,
    load_jsonl,
)
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    find_project_root,
    load_stage11_config,
)

RISING = {"ARC_5", "ARC_6", "ARC_7", "ARC_8"}
FALLING = {"ARC_1", "ARC_2", "ARC_3", "ARC_4"}
EXTERNAL = {"ARC_9"}


def _code(row: Dict[str, Any]) -> str:
    resp = row.get("response") or {}
    return str(row.get("code") or resp.get("arc_role") or resp.get("dominant_code") or "ARC_10")


def _main_couple(row: Dict[str, Any]) -> bool:
    resp = row.get("response") or {}
    if "main_couple" in resp:
        v = resp["main_couple"]
        if isinstance(v, bool):
            return v
        return str(v).lower() in {"yes", "true", "1"}
    prob = resp.get("main_couple_prob")
    try:
        return float(prob) >= 0.5
    except (TypeError, ValueError):
        return False


def _rec_inclusion(row: Dict[str, Any]) -> str:
    resp = row.get("response") or {}
    rec = str(resp.get("recommended_strict_h6_inclusion") or "").lower()
    if rec in {"rising", "falling", "external", "exclude"}:
        return rec
    code = _code(row)
    if code in RISING:
        return "rising"
    if code in FALLING:
        return "falling"
    if code in EXTERNAL:
        return "external"
    return "exclude"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--crosswalk", default="configs/stage11/h6_radway_crosswalk.yaml")
    args = parser.parse_args(argv)

    root = find_project_root()
    cfg = load_stage11_config(args.config)
    cw = yaml.safe_load((root / args.crosswalk).read_text(encoding="utf-8"))
    day = root / cw["paths"]["day_dir"]
    new_ids = {
        int(x)
        for x in (day / "h6_new_topic_ids.txt").read_text(encoding="utf-8").split()
        if x.strip()
    }
    baseline = json.loads((day / "baseline_freeze.json").read_text(encoding="utf-8"))
    existing = set(baseline.get("restored_sonnet_audits", {}).get("topic_ids") or [])

    adj_path = audit_dir(cfg, "H6") / PASS_FILES["C"]
    ctx_path = audit_dir(cfg, "H6") / PASS_FILES["B"]
    adj = {int(r["topic_id"]): r for r in load_jsonl(adj_path)}
    ctx = {int(r["topic_id"]): r for r in load_jsonl(ctx_path)}

    # Manifest for Radway tags on new topics
    import pandas as pd

    man = pd.read_csv(day / "h6_radway_candidate_manifest.csv")
    man_by = man.set_index("topic_id")

    rising_topics: List[int] = []
    falling_topics: List[int] = []
    external_topics: List[int] = []
    excluded_new: List[int] = []
    flagged: List[Dict[str, Any]] = []
    membership_rows: List[Dict[str, Any]] = []

    all_ids = sorted(existing | new_ids)
    for tid in all_ids:
        row_c = adj.get(tid)
        row_b = ctx.get(tid)
        if row_c is None:
            continue
        code = _code(row_c)
        mc = _main_couple(row_c)
        if not mc and row_b is not None:
            mc = _main_couple(row_b)
        bucket = _rec_inclusion(row_c)
        action = str((row_c.get("response") or {}).get("action") or row_c.get("action") or "KEEP")
        is_new = tid in new_ids

        # Strict inclusion rules
        include_rising = code in RISING and mc and action != "EXCLUDE_FROM_HYPOTHESIS"
        include_falling = code in FALLING and mc and action != "EXCLUDE_FROM_HYPOTHESIS"
        include_external = code in EXTERNAL and action != "EXCLUDE_FROM_HYPOTHESIS"

        if include_rising:
            rising_topics.append(tid)
            side = "rising"
        elif include_falling:
            falling_topics.append(tid)
            side = "falling"
        elif include_external:
            external_topics.append(tid)
            side = "external"
        else:
            side = "exclude"
            if is_new:
                excluded_new.append(tid)

        # Flags
        reasons = []
        if code in {"MIXED", "ARC_10", "ARC_0"} or action == "EXCLUDE_FROM_HYPOTHESIS":
            reasons.append(f"ambiguous_code={code}")
        if is_new and bucket == "rising":
            reasons.append("high_impact_rising_candidate")
        if is_new and tid in man_by.index:
            rmain = str(man_by.loc[tid].get("radway_main_id") or "")
            rising_tags = {"R9", "R10", "R11", "R13"}
            falling_tags = {"R2", "R3", "R5", "R6", "R7"}
            if rmain in rising_tags and side != "rising":
                reasons.append(f"radway_rising_tag_but_audit={side}/{code}")
            if rmain in falling_tags and side != "falling":
                reasons.append(f"radway_falling_tag_but_audit={side}/{code}")
        if (row_c.get("response") or {}).get("manual_review_required"):
            reasons.append("manual_review_required")
        if (row_c.get("response") or {}).get("metadata_supports_contextual") == "contradict":
            reasons.append("metadata_contradicts_contextual")

        if reasons:
            flagged.append(
                {
                    "topic_id": tid,
                    "is_new": is_new,
                    "code": code,
                    "side": side,
                    "main_couple": mc,
                    "reasons": reasons,
                }
            )

        membership_rows.append(
            {
                "topic_id": tid,
                "source": "new_radway_day" if is_new else "restored_sonnet_29",
                "arc_role": code,
                "main_couple": mc,
                "strict_side": side,
                "action": action,
                "included_strict": side in {"rising", "falling", "external"},
            }
        )

    membership = {
        "frozen_rule": (
            "Strict rising = ARC_5–8 with main_couple evidence; "
            "falling = ARC_1–4 with main_couple; no criterion weakening."
        ),
        "n_restored_29": len(existing),
        "n_new_audited": len(new_ids & set(adj)),
        "strict_rising_topic_ids": sorted(set(rising_topics)),
        "strict_falling_topic_ids": sorted(set(falling_topics)),
        "strict_external_topic_ids": sorted(set(external_topics)),
        "n_strict_rising": len(set(rising_topics)),
        "n_strict_falling": len(set(falling_topics)),
        "excluded_new_topic_ids": sorted(excluded_new),
        "members": membership_rows,
        "flagged_for_human_review": flagged,
        "hard_stop_threshold_rising": 3,
        "baseline_rising_n": 2,
    }
    out = day / "h6_v2_membership.json"
    out.write_text(json.dumps(membership, indent=2), encoding="utf-8")

    # Human review markdown for flagged only
    lines = [
        "# H6-v2 Radway-day human review (flagged only)",
        "",
        f"Strict rising topics: {membership['n_strict_rising']} "
        f"{membership['strict_rising_topic_ids']}",
        f"Strict falling topics: {membership['n_strict_falling']}",
        f"Flagged cases: {len(flagged)}",
        "",
    ]
    for f in flagged:
        lines.append(
            f"- **Topic {f['topic_id']}** ({'new' if f['is_new'] else 'baseline'}): "
            f"code={f['code']} side={f['side']} main_couple={f['main_couple']} — "
            + "; ".join(f["reasons"])
        )
    review_path = day / "h6_v2_human_review_flagged.md"
    review_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: membership[k] for k in membership if k != "members"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
