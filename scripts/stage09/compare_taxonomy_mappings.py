#!/usr/bin/env python
"""Compare two Stage09 taxonomy mapping runs.

Serves both roles the plan needs:

  * pilot review  — a 30-topic disagreement table to read before paying for the full run
  * stability report — the old-vs-new summary for the full 348-topic re-run

Reports category churn, confidence/evidence-quality shifts, axis-bearing coverage deltas,
and whether the v2.5 hardening targets moved (``uncertain_interpretable`` count, low
``evidence_quality`` count, and the previously-empty axis IDs).
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import yaml

EVIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}


def load_mappings(path: Path) -> Dict[str, Dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_axis_ids(taxonomy_path: Path) -> tuple[List[str], List[str]]:
    cfg = yaml.safe_load(taxonomy_path.read_text(encoding="utf-8"))
    return list(cfg.get("axis_bearing_ids") or []), list(cfg.get("exclude_from_axes_ids") or [])


def build_rows(
    old: Dict[str, Dict[str, Any]],
    new: Dict[str, Dict[str, Any]],
    metadata: Optional[Dict[str, Dict[str, Any]]],
    strata: Optional[Dict[str, str]] = None,
) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for tid in sorted(new.keys(), key=int):
        o = old.get(tid, {})
        n = new[tid]
        meta = (metadata or {}).get(tid, {})
        reasoning = str(n.get("mapping_reasoning") or "")
        rows.append({
            "topic_id": int(tid),
            "stratum": (strata or {}).get(tid, "all"),
            "label": meta.get("label") or o.get("source_metadata", {}).get("label", ""),
            "old_main": o.get("main_category_id"),
            "new_main": n.get("main_category_id"),
            "main_changed": o.get("main_category_id") != n.get("main_category_id"),
            "old_secondary": o.get("secondary_category_id"),
            "new_secondary": n.get("secondary_category_id"),
            "old_confidence": o.get("confidence"),
            "new_confidence": n.get("confidence"),
            "old_evidence": o.get("evidence_quality"),
            "new_evidence": n.get("evidence_quality"),
            "old_macro": o.get("use_in_macro_axes"),
            "new_macro": n.get("use_in_macro_axes"),
            "old_noise": o.get("is_noise"),
            "new_noise": n.get("is_noise"),
            "new_uncertainty_reason": n.get("uncertainty_reason"),
            "quotes_evidence": reasoning.strip().startswith("EVIDENCE:"),
            "new_rationale": n.get("rationale"),
            "new_mapping_reasoning": reasoning,
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["evidence_delta"] = (
            df["new_evidence"].str.lower().map(EVIDENCE_ORDER)
            - df["old_evidence"].str.lower().map(EVIDENCE_ORDER)
        )
    return df


def category_counts(mappings: Dict[str, Dict[str, Any]]) -> Counter:
    return Counter(m.get("main_category_id") for m in mappings.values())


def restrict(mappings: Dict[str, Dict[str, Any]], keys: set[str]) -> Dict[str, Dict[str, Any]]:
    """Limit a mapping dict to a shared topic set so before/after columns are comparable.

    Without this, a 30-topic pilot is scored against all 348 previous topics and every
    count looks like it collapsed.
    """
    return {k: v for k, v in mappings.items() if k in keys}


def summarize(
    df: pd.DataFrame,
    old: Dict[str, Dict[str, Any]],
    new: Dict[str, Dict[str, Any]],
    axis_ids: List[str],
) -> Dict[str, Any]:
    old_counts = category_counts(old)
    new_counts = category_counts(new)
    comparable = df[df["old_main"].notna()]

    def frac_low(mappings: Dict[str, Dict[str, Any]]) -> float:
        vals = [str(m.get("evidence_quality", "")).lower() for m in mappings.values()]
        return (sum(v == "low" for v in vals) / len(vals)) if vals else 0.0

    return {
        "n_topics_new": len(new),
        "n_topics_old": len(old),
        "n_comparable": int(len(comparable)),
        "n_main_changed": int(comparable["main_changed"].sum()) if len(comparable) else 0,
        "pct_main_changed": (
            round(100 * comparable["main_changed"].mean(), 1) if len(comparable) else 0.0
        ),
        "uncertain_old": old_counts.get("uncertain_interpretable", 0),
        "uncertain_new": new_counts.get("uncertain_interpretable", 0),
        "noise_old": int(sum(bool(m.get("is_noise")) for m in old.values())),
        "noise_new": int(sum(bool(m.get("is_noise")) for m in new.values())),
        "low_evidence_old": int(sum(str(m.get("evidence_quality", "")).lower() == "low" for m in old.values())),
        "low_evidence_new": int(sum(str(m.get("evidence_quality", "")).lower() == "low" for m in new.values())),
        "pct_low_evidence_old": round(100 * frac_low(old), 1),
        "pct_low_evidence_new": round(100 * frac_low(new), 1),
        "macro_true_old": int(sum(bool(m.get("use_in_macro_axes")) for m in old.values())),
        "macro_true_new": int(sum(bool(m.get("use_in_macro_axes")) for m in new.values())),
        "axis_topics_old": int(sum(old_counts.get(a, 0) for a in axis_ids)),
        "axis_topics_new": int(sum(new_counts.get(a, 0) for a in axis_ids)),
        "pct_quoting_evidence": round(100 * df["quotes_evidence"].mean(), 1) if len(df) else 0.0,
        "uncertain_without_reason": int(
            ((df["new_main"] == "uncertain_interpretable") & df["new_uncertainty_reason"].isna()).sum()
        ),
    }


def axis_coverage_table(
    old: Dict[str, Dict[str, Any]],
    new: Dict[str, Dict[str, Any]],
    axis_ids: List[str],
) -> pd.DataFrame:
    old_counts = category_counts(old)
    new_counts = category_counts(new)
    rows = []
    for aid in axis_ids:
        n_old = old_counts.get(aid, 0)
        n_new = new_counts.get(aid, 0)
        rows.append({
            "axis_id": aid,
            "n_topics_old": n_old,
            "n_topics_new": n_new,
            "delta": n_new - n_old,
            "was_empty": n_old == 0,
            "still_empty": n_new == 0,
        })
    return pd.DataFrame(rows)


def stratum_table(df: pd.DataFrame) -> pd.DataFrame:
    """Per-stratum outcome summary — the pilot's actual pass/fail signal."""
    def evidence_up(g: pd.DataFrame) -> int:
        return int((g["evidence_delta"] > 0).sum())

    rows = []
    for name, g in df.groupby("stratum"):
        rows.append({
            "stratum": name,
            "n": len(g),
            "main_changed": int(g["main_changed"].sum()),
            "evidence_improved": evidence_up(g),
            "still_low_evidence": int((g["new_evidence"].str.lower() == "low").sum()),
            "still_uncertain": int((g["new_main"] == "uncertain_interpretable").sum()),
            "quotes_evidence": int(g["quotes_evidence"].sum()),
        })
    return pd.DataFrame(rows).sort_values("stratum")


def _md_table(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False)


def write_report(
    path: Path,
    title: str,
    summary: Dict[str, Any],
    axis_df: pd.DataFrame,
    df: pd.DataFrame,
    old_path: Path,
    new_path: Path,
    max_examples: int,
) -> None:
    changed = df[df["main_changed"] & df["old_main"].notna()].copy()

    lines: List[str] = [
        f"# {title}",
        "",
        f"- Previous mapping: `{old_path}`",
        f"- New mapping: `{new_path}`",
        "",
        f"All before/after counts below cover the **same {summary['n_topics_new']} topics** "
        "present in both runs, so the two columns are directly comparable.",
        "",
        "## Headline numbers",
        "",
        "| Metric | Before | After |",
        "|---|---|---|",
        f"| Topics compared | {summary['n_topics_old']} | {summary['n_topics_new']} |",
        f"| `uncertain_interpretable` | {summary['uncertain_old']} | {summary['uncertain_new']} |",
        f"| Low `evidence_quality` | {summary['low_evidence_old']} ({summary['pct_low_evidence_old']}%) | {summary['low_evidence_new']} ({summary['pct_low_evidence_new']}%) |",
        f"| `use_in_macro_axes=true` | {summary['macro_true_old']} | {summary['macro_true_new']} |",
        f"| Topics on axis-bearing IDs | {summary['axis_topics_old']} | {summary['axis_topics_new']} |",
        f"| Flagged noise | {summary['noise_old']} | {summary['noise_new']} |",
        "",
        f"Main category changed for **{summary['n_main_changed']} of {summary['n_comparable']}** "
        f"comparable topics ({summary['pct_main_changed']}%).",
        "",
        f"Evidence-quote compliance: **{summary['pct_quoting_evidence']}%** of new mappings open "
        "`mapping_reasoning` with `EVIDENCE:`.",
        "",
        f"`uncertain_interpretable` without an `uncertainty_reason`: "
        f"**{summary['uncertain_without_reason']}** (should be 0).",
        "",
    ]

    if df["stratum"].nunique() > 1:
        lines += [
            "## Per-stratum outcome",
            "",
            _md_table(stratum_table(df)),
            "",
        ]

    lines += [
        "## Axis-bearing coverage",
        "",
        _md_table(axis_df),
        "",
        "## Main-category churn",
        "",
    ]

    if changed.empty:
        lines.append("No main-category changes.")
    else:
        churn = (
            changed.groupby(["old_main", "new_main"]).size()
            .reset_index(name="n").sort_values("n", ascending=False)
        )
        lines.append(_md_table(churn))
        lines += ["", f"## Changed topics (first {max_examples})", ""]
        cols = ["topic_id", "label", "old_main", "new_main", "old_evidence", "new_evidence", "new_confidence"]
        lines.append(_md_table(changed[cols].head(max_examples)))
        lines += ["", "### Reasoning for changed topics", ""]
        for _, r in changed.head(max_examples).iterrows():
            lines += [
                f"**Topic {r['topic_id']} — {r['label']}**  ",
                f"`{r['old_main']}` -> `{r['new_main']}` "
                f"(evidence {r['old_evidence']} -> {r['new_evidence']}, confidence {r['new_confidence']})",
                "",
                f"> {r['new_mapping_reasoning']}",
                "",
            ]

    unchanged_low = df[(~df["main_changed"]) & (df["new_evidence"].str.lower() == "low")]
    lines += [
        "",
        "## Still-low evidence quality after re-run",
        "",
        f"{len(unchanged_low)} topics kept the same category and still report low evidence quality.",
        "",
    ]
    if not unchanged_low.empty:
        lines.append(_md_table(unchanged_low[["topic_id", "label", "new_main", "new_uncertainty_reason"]].head(max_examples)))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--old-mappings", type=Path, required=True)
    ap.add_argument("--new-mappings", type=Path, required=True)
    ap.add_argument("--metadata-json", type=Path, default=None, help="Optional, for topic labels")
    ap.add_argument("--taxonomy-config", type=Path, default=Path("configs/stage09/romance_corpus_taxonomy_v2.yaml"))
    ap.add_argument("--strata-manifest", type=Path, default=None, help="Pilot manifest, for a per-stratum breakdown")
    ap.add_argument("--report-md", type=Path, required=True)
    ap.add_argument("--report-csv", type=Path, default=None)
    ap.add_argument("--title", type=str, default="Stage09 mapping comparison")
    ap.add_argument("--max-examples", type=int, default=40)
    args = ap.parse_args()

    old_full = load_mappings(args.old_mappings)
    new = load_mappings(args.new_mappings)
    old = restrict(old_full, set(new.keys()))
    metadata = json.loads(args.metadata_json.read_text(encoding="utf-8")) if args.metadata_json else None
    axis_ids, _ = load_axis_ids(args.taxonomy_config)

    strata: Optional[Dict[str, str]] = None
    if args.strata_manifest:
        manifest = json.loads(args.strata_manifest.read_text(encoding="utf-8"))
        strata = {tid: name for name, ids in manifest.get("strata", {}).items() for tid in ids}

    df = build_rows(old, new, metadata, strata)
    summary = summarize(df, old, new, axis_ids)
    axis_df = axis_coverage_table(old, new, axis_ids)

    write_report(
        args.report_md, args.title, summary, axis_df, df,
        args.old_mappings, args.new_mappings, args.max_examples,
    )
    if args.report_csv:
        args.report_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.report_csv, index=False)

    print(json.dumps(summary, indent=2))
    print(f"\nReport -> {args.report_md}")
    if args.report_csv:
        print(f"Per-topic CSV -> {args.report_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
