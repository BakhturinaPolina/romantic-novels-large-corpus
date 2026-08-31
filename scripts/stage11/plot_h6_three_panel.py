#!/usr/bin/env python3
"""Three-panel H6 triangulation: Stage10 taxonomy / Radway phases / refined H6-v2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.stage10_correlation_analysis.analysis.arc import (  # noqa: E402
    TERTILE_ORDER,
    aggregate_tertile_leaves,
)
from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    find_project_root,
    load_stage11_config,
)


def _mean_profile(long: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    sub = long[long["feature"].isin(features)]
    return (
        sub.groupby(["feature", "tertile"], observed=True)["share"]
        .mean()
        .reset_index()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--day-dir",
        default=(
            "results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/"
            "h6_radway_day"
        ),
    )
    args = parser.parse_args(argv)
    root = find_project_root()
    cfg = load_stage11_config(args.config)
    day = root / args.day_dir
    fig_dir = day / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    tertile = pd.read_parquet(
        root
        / "results/stage10_correlation_analysis/v4_l12_granular_final_call49"
        / "topic_counts_hard/tertile_topic_counts.parquet"
    )
    lookup = pd.read_parquet(
        root
        / "results/stage10_correlation_analysis/v4_l12_granular_final_call49"
        / "taxonomy_radway_eda/topic_lookup.parquet"
    )

    # Panel 1: Stage10 taxonomy rising vs falling leaf bundles
    rising_leaves = ["4.5", "4.6", "3.1"]
    falling_leaves = ["4.3", "4.4", "3.2"]
    topic_to_leaf = lookup.set_index("topic_id")["taxonomy_main_id"].astype(str)
    leaf_long = aggregate_tertile_leaves(tertile, topic_to_leaf)
    # Bundle
    leaf_long = leaf_long.copy()
    leaf_long["bundle"] = leaf_long["feature"].map(
        lambda x: "tax_rising"
        if str(x) in rising_leaves
        else "tax_falling"
        if str(x) in falling_leaves
        else None
    )
    tax = (
        leaf_long.dropna(subset=["bundle"])
        .groupby(["book_id", "tertile", "bundle"], as_index=False)["share"]
        .sum()
        .rename(columns={"bundle": "feature"})
    )
    tax_prof = _mean_profile(tax, ["tax_rising", "tax_falling"])

    # Panel 2: Radway phases (already computed)
    rad = pd.read_csv(day / "radway_phases" / "phase_profile_overall_main.csv")

    # Panel 3: refined H6 via W_tkr × tertile shares
    wtkr_path = day / "W_tkr_h6_v2.parquet"
    if not wtkr_path.exists():
        wtkr_path = cfg.output_path("constructs_dir") / "W_tkr.parquet"
    wtkr = pd.read_parquet(wtkr_path)
    # Map construct codes to rising/falling
    rising_codes = {"ARC_5", "ARC_6", "ARC_7", "ARC_8", "RAX_arc_rising"}
    falling_codes = {"ARC_1", "ARC_2", "ARC_3", "ARC_4", "RAX_arc_falling"}
    wtkr = wtkr.copy()
    wtkr["side"] = wtkr["construct_code"].map(
        lambda c: "h6_rising"
        if str(c) in rising_codes
        else "h6_falling"
        if str(c) in falling_codes
        else None
    )
    w_side = (
        wtkr.dropna(subset=["side"])
        .groupby(["topic_id", "tertile", "side"], as_index=False)["weight"]
        .sum()
    )
    # book×tertile×topic share * weight → side share
    tt = tertile.merge(w_side, on=["topic_id", "tertile"], how="inner")
    tt["mass"] = tt["share"] * tt["weight"]
    # renormalize? use raw weighted mass mean across books
    book_side = (
        tt.groupby(["book_id", "tertile", "side"], as_index=False)["mass"]
        .sum()
        .rename(columns={"mass": "share", "side": "feature"})
    )
    h6_prof = _mean_profile(book_side, ["h6_rising", "h6_falling"])

    order = list(TERTILE_ORDER)
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0), sharey=False)

    def _plot(ax, prof, features, colors, title, ylabel=False):
        for feat, color in zip(features, colors):
            sub = prof[prof["feature"] == feat].set_index("tertile").reindex(order)
            ax.plot(order, sub["share"].to_numpy(dtype=float), marker="o", color=color, label=feat)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Narrative position")
        if ylabel:
            ax.set_ylabel("Mean share")
        ax.legend(frameon=False, fontsize=8)

    _plot(
        axes[0],
        tax_prof,
        ["tax_rising", "tax_falling"],
        ("#2f6b3a", "#b85c38"),
        "Stage 10 taxonomy H6",
        ylabel=True,
    )
    # Radway uses column name 'mean'
    rad_plot = rad.rename(columns={"mean": "share"})
    _plot(
        axes[1],
        rad_plot,
        ["RADWAY_I", "RADWAY_II", "RADWAY_III"],
        ("#b85c38", "#2a6f7f", "#2f6b3a"),
        "Radway Phase I / II / III",
    )
    _plot(
        axes[2],
        h6_prof,
        ["h6_rising", "h6_falling"],
        ("#2f6b3a", "#b85c38"),
        "Refined H6-v2 (W_tkr)",
    )
    fig.suptitle("H6 triangulation: taxonomy · Radway · refined", y=1.02)
    fig.tight_layout()
    out = fig_dir / "h6_three_panel.png"
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)

    # Decision note
    membership_path = day / "h6_v2_membership.json"
    vs_path = day / "h6_v2_vs_baseline.json"
    membership = (
        json.loads(membership_path.read_text(encoding="utf-8"))
        if membership_path.exists()
        else {}
    )
    vs = json.loads(vs_path.read_text(encoding="utf-8")) if vs_path.exists() else {}
    n_rising = int(membership.get("n_strict_rising") or 0)
    if n_rising >= 3:
        decision = (
            f"KEEP H6-v2: strict rising grew to {n_rising} topics "
            f"{membership.get('strict_rising_topic_ids')}."
        )
        status = "keep"
    else:
        decision = (
            "H6 remains undermeasured/inconclusive under strict main-couple semantic "
            f"validation (strict rising={n_rising} < 3). Do not weaken criteria. "
            "Retain Radway-phase plots as genre-trajectory evidence."
        )
        status = "inconclusive"

    note = {
        "status": status,
        "decision": decision,
        "n_strict_rising": n_rising,
        "three_panel": str(out.relative_to(root)),
        "vs_baseline": vs,
    }
    (day / "h6_v2_decision.json").write_text(json.dumps(note, indent=2, default=str), encoding="utf-8")
    (day / "h6_v2_decision.md").write_text(
        f"# H6-v2 hard stop\n\n**Status:** `{status}`\n\n{decision}\n\n"
        f"Figure: `{out.relative_to(root)}`\n",
        encoding="utf-8",
    )
    print(json.dumps(note, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
