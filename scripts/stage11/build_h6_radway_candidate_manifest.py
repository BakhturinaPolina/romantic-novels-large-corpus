#!/usr/bin/env python3
"""Build outcome-blind H6 Radway candidate manifest; select ~25 new topics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import yaml

from src.stage11_refined_construct_analysis.analysis.radway_phases import load_radway_lookup
from src.stage11_refined_construct_analysis.config import find_project_root


def _as_set(xs) -> Set[str]:
    return {str(x) for x in (xs or [])}


def score_topic(
    row: pd.Series,
    *,
    rising_high: Set[str],
    rising_med: Set[str],
    falling_high: Set[str],
    stage11_rising: Set[int],
    stage11_falling: Set[int],
    taxonomy_falling: Set[str],
    weights: Dict[str, int],
) -> Dict[str, Any]:
    tid = int(row["topic_id"])
    main = str(row.get("radway_main_id") or "none")
    sec = row.get("radway_secondary_id")
    sec_s = str(sec) if pd.notna(sec) and sec not in (None, "", "none", "None") else None
    others = row.get("radway_other_plausible_ids") or []
    if not isinstance(others, list):
        others = list(others) if others is not None else []
    others_s = [str(x) for x in others]
    conf = str(row.get("radway_confidence") or "").lower()
    leaf = str(row.get("taxonomy_main_id") or "")

    priority = rising_high | rising_med | falling_high
    side = "none"
    if main in rising_high or main in rising_med or (sec_s in rising_high) or any(
        o in rising_high for o in others_s
    ):
        side = "rising"
    if main in falling_high or (sec_s in falling_high) or any(o in falling_high for o in others_s):
        side = "falling" if side == "none" else "both"

    score = 0
    parts: Dict[str, int] = {}
    if main in priority:
        parts["radway_main"] = weights["radway_main"]
        score += parts["radway_main"]
    if sec_s and sec_s in priority:
        parts["radway_secondary"] = weights["radway_secondary"]
        score += parts["radway_secondary"]
    if any(o in priority for o in others_s):
        parts["radway_other_plausible"] = weights["radway_other_plausible"]
        score += parts["radway_other_plausible"]
    if tid in stage11_rising or tid in stage11_falling:
        parts["stage11_refined_match"] = weights["stage11_refined_match"]
        score += parts["stage11_refined_match"]
    if leaf in taxonomy_falling:
        parts["taxonomy_relevant"] = weights["taxonomy_relevant"]
        score += parts["taxonomy_relevant"]
    if conf in {"medium", "high"} and (main in priority or (sec_s and sec_s in priority)):
        parts["radway_confidence_medium_high"] = weights["radway_confidence_medium_high"]
        score += parts["radway_confidence_medium_high"]

    # Mild bonus for high-priority rising tags on main (still outcome-blind)
    if main in rising_high:
        parts["rising_high_main_bonus"] = 1
        score += 1

    return {
        "topic_id": tid,
        "score": score,
        "side": side,
        "radway_main_id": main,
        "radway_secondary_id": sec_s,
        "radway_other_plausible_ids": "|".join(others_s),
        "radway_confidence": conf,
        "taxonomy_main_id": leaf,
        "taxonomy_main_name": row.get("taxonomy_main_name"),
        "in_stage11_rising_atoms": tid in stage11_rising,
        "in_stage11_falling_atoms": tid in stage11_falling,
        "score_parts": json.dumps(parts),
    }


def select_new(
    scored: pd.DataFrame,
    existing: Set[int],
    *,
    n_new: int,
    min_rising: int,
    prefer_rising_tags: Set[str],
) -> pd.DataFrame:
    cand = scored[~scored["topic_id"].isin(existing) & (scored["score"] > 0)].copy()
    cand = cand.sort_values(["score", "topic_id"], ascending=[False, True])

    rising_pool = cand[
        cand["radway_main_id"].isin(prefer_rising_tags)
        | cand["side"].isin(["rising", "both"])
    ]
    falling_pool = cand[cand["side"].isin(["falling", "both"])]

    chosen: List[int] = []
    for tid in rising_pool["topic_id"].tolist():
        if len([t for t in chosen if t in set(rising_pool["topic_id"])]) >= min_rising:
            break
        if tid not in chosen:
            chosen.append(int(tid))

    for tid in cand["topic_id"].tolist():
        if len(chosen) >= n_new:
            break
        if tid not in chosen:
            chosen.append(int(tid))

    # If still short on rising after fill, already best-effort
    out = cand[cand["topic_id"].isin(chosen)].copy()
    out["selected_new"] = True
    out["selection_rank"] = out["topic_id"].map({t: i + 1 for i, t in enumerate(chosen)})
    return out.sort_values("selection_rank")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crosswalk", default="configs/stage11/h6_radway_crosswalk.yaml")
    args = parser.parse_args(argv)
    root = find_project_root()
    cw = yaml.safe_load((root / args.crosswalk).read_text(encoding="utf-8"))
    paths = cw["paths"]
    day = root / paths["day_dir"]
    day.mkdir(parents=True, exist_ok=True)

    lookup = load_radway_lookup(
        root / paths["topic_lookup"],
        root / paths["taxonomy_with_radway"],
    )
    cov = json.loads((root / paths["construct_coverage"]).read_text(encoding="utf-8"))
    atoms = cov.get("atoms") or {}
    stage11_rising: Set[int] = set()
    for name in cw["stage11_rising_atoms"]:
        stage11_rising.update(atoms.get(name, {}).get("topic_ids") or [])
    stage11_falling: Set[int] = set()
    for name in cw["stage11_falling_atoms"]:
        stage11_falling.update(atoms.get(name, {}).get("topic_ids") or [])

    h6_summary = json.loads((root / paths["h6_audit_summary"]).read_text(encoding="utf-8"))
    existing = set(int(t) for t in h6_summary.get("topic_ids") or [])

    rising_high = _as_set(cw["rising_priority_high"])
    rising_med = _as_set(cw["rising_priority_medium"])
    falling_high = _as_set(cw["falling_priority_high"])
    taxonomy_falling = _as_set(cw["taxonomy_falling_leaves"])
    weights = {k: int(v) for k, v in cw["score"].items()}

    rows = [
        score_topic(
            row,
            rising_high=rising_high,
            rising_med=rising_med,
            falling_high=falling_high,
            stage11_rising=stage11_rising,
            stage11_falling=stage11_falling,
            taxonomy_falling=taxonomy_falling,
            weights=weights,
        )
        for _, row in lookup.iterrows()
    ]
    scored = pd.DataFrame(rows)
    scored["in_current_h6"] = scored["topic_id"].isin(existing)

    sel_cfg = cw["selection"]
    selected = select_new(
        scored,
        existing,
        n_new=int(sel_cfg["n_new"]),
        min_rising=int(sel_cfg["min_rising_new"]),
        prefer_rising_tags=_as_set(sel_cfg["prefer_rising_radway_tags"]),
    )

    scored = scored.merge(
        selected[["topic_id", "selected_new", "selection_rank"]],
        on="topic_id",
        how="left",
    )
    scored["selected_new"] = scored["selected_new"].fillna(False)
    scored = scored.sort_values(
        ["selected_new", "score", "topic_id"], ascending=[False, False, True]
    )

    out_csv = day / "h6_radway_candidate_manifest.csv"
    scored.to_csv(out_csv, index=False)

    new_ids = selected.sort_values("selection_rank")["topic_id"].tolist()
    ids_path = day / "h6_new_topic_ids.txt"
    ids_path.write_text("\n".join(str(t) for t in new_ids) + "\n", encoding="utf-8")

    meta = {
        "n_scored": int(len(scored)),
        "n_existing_h6": len(existing),
        "n_selected_new": len(new_ids),
        "n_selected_rising_side": int(
            selected["side"].isin(["rising", "both"]).sum()
        ),
        "selected_topic_ids": new_ids,
        "existing_h6_topic_ids": sorted(existing),
        "manifest_csv": str(out_csv.relative_to(root)),
    }
    (day / "h6_radway_candidate_manifest_meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
