#!/usr/bin/env python3
"""Three-panel H6 triangulation + hard-stop decision note."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from src.stage11_refined_construct_analysis.config import find_project_root


def _stage10_profiles(root: Path) -> pd.DataFrame:
    path = (
        root
        / "results/stage10_correlation_analysis/v4_l12_granular_final_call49"
        / "notebook_analysis/05_hypothesis_tests/tables/H6_tertile_profiles.csv"
    )
    if path.exists():
        return pd.read_csv(path)
    # Fallback: rebuild from within-book shifts is not enough; synthesize empty
    return pd.DataFrame()


def _h6_v2_tertile_means(root: Path, day: Path) -> pd.DataFrame:
    """Mean begin/middle/end shares for rising vs falling from W_tkr × tertile counts."""
    wtkr = pd.read_parquet(day / "W_tkr_h6_v2.parquet")
    tertile = pd.read_parquet(
        root
        / "results/stage10_correlation_analysis/v4_l12_granular_final_call49"
        / "topic_counts_hard/tertile_topic_counts.parquet"
    )
    # Map ARC codes → rising/falling
    rising_codes = {f"ARC_{i}" for i in range(5, 9)}
    falling_codes = {f"ARC_{i}" for i in range(1, 5)}

    def side(code: str) -> str | None:
        c = str(code)
        if c in rising_codes:
            return "RAX_arc_rising"
        if c in falling_codes:
            return "RAX_arc_falling"
        return None

    w = wtkr.copy()
    w["side"] = w["construct_code"].map(side)
    w = w.dropna(subset=["side"])
    # topic×tertile weight for each side
    tw = (
        w.groupby(["topic_id", "tertile", "side"], as_index=False)["weight"]
        .sum()
    )
    merged = tertile.merge(tw, on=["topic_id", "tertile"], how="inner")
    merged["weighted"] = merged["share"] * merged["weight"]
    # book×tertile×side
    book = (
        merged.groupby(["book_id", "tertile", "side"], as_index=False)["weighted"]
        .sum()
        .rename(columns={"weighted": "share"})
    )
    profile = (
        book.groupby(["side", "tertile"], as_index=False)["share"]
        .mean()
        .rename(columns={"side": "feature", "share": "mean"})
    )
    return profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crosswalk", default="configs/stage11/h6_radway_crosswalk.yaml")
    args = parser.parse_args(argv)
    root = find_project_root()
    cw = yaml.safe_load((root / args.crosswalk).read_text(encoding="utf-8"))
    day = root / cw["paths"]["day_dir"]
    fig_dir = day / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    membership = json.loads((day / "h6_v2_membership.json").read_text(encoding="utf-8"))
    baseline = json.loads((day / "baseline_freeze.json").read_text(encoding="utf-8"))
    comparison = json.loads((day / "h6_v2_vs_baseline.json").read_text(encoding="utf-8"))

    order = ["begin", "middle", "end"]
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0), sharey=False)

    # Panel 1: Stage10 taxonomy rising vs falling
    ax = axes[0]
    s10 = _stage10_profiles(root)
    if not s10.empty:
        feat_col = "feature"
        rising_leaves = {"4.5", "4.6", "3.1"}
        falling_leaves = {"4.3", "4.4", "3.2"}
        s10 = s10.copy()
        s10["_feat"] = s10[feat_col].astype(str)
        val_col = "mean" if "mean" in s10.columns else "share"
        for label, leaves, color in (
            ("taxonomy_rising", rising_leaves, "#2f6b3a"),
            ("taxonomy_falling", falling_leaves, "#b85c38"),
        ):
            sub = s10[s10["_feat"].isin(leaves)]
            if sub.empty:
                continue
            means = sub.groupby("tertile")[val_col].mean().reindex(order)
            ax.plot(order, means.to_numpy(dtype=float), marker="o", label=label, color=color)
        ax.legend(frameon=False, fontsize=8)
    else:
        ax.text(0.5, 0.5, "Stage10 profiles unavailable", ha="center", transform=ax.transAxes)
    ax.set_title("Stage 10 taxonomy H6")
    ax.set_xlabel("Narrative position")
    ax.set_ylabel("Mean share")

    # Panel 2: Radway phases
    ax = axes[1]
    rad = pd.read_csv(day / "radway_phases/phase_profile_overall_main.csv")
    for feat, color in zip(
        ("RADWAY_I", "RADWAY_II", "RADWAY_III"),
        ("#b85c38", "#2a6f7f", "#2f6b3a"),
    ):
        sub = rad[rad["feature"] == feat].set_index("tertile").reindex(order)
        ax.plot(order, sub["mean"].to_numpy(dtype=float), marker="o", label=feat, color=color)
    ax.set_title("Radway Phase I/II/III")
    ax.set_xlabel("Narrative position")
    ax.legend(frameon=False, fontsize=8)

    # Panel 3: refined H6-v2
    ax = axes[2]
    try:
        prof = _h6_v2_tertile_means(root, day)
        for feat, color in (("RAX_arc_rising", "#2f6b3a"), ("RAX_arc_falling", "#b85c38")):
            sub = prof[prof["feature"] == feat].set_index("tertile").reindex(order)
            ax.plot(
                order,
                sub["mean"].to_numpy(dtype=float),
                marker="o",
                label=feat.replace("RAX_arc_", ""),
                color=color,
            )
        ax.legend(frameon=False, fontsize=8)
    except Exception as exc:
        ax.text(0.5, 0.5, f"H6-v2 plot error:\n{exc}", ha="center", transform=ax.transAxes, fontsize=8)
    ax.set_title("Refined H6-v2")
    ax.set_xlabel("Narrative position")

    fig.suptitle("H6 triangulation: Stage10 / Radway / refined v2", y=1.02)
    fig.tight_layout()
    fig_path = fig_dir / "h6_three_panel.png"
    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    n_rising = int(membership["n_strict_rising"])
    threshold = int(membership.get("hard_stop_threshold_rising", 3))
    if n_rising >= threshold:
        decision = "keep_h6_v2"
        prose = (
            f"Strict RAX_arc_rising grew from 2 to {n_rising} credible topics "
            f"(≥{threshold}). Retain H6-v2 as the final refined H6 operationalization."
        )
    else:
        decision = "inconclusive_undermeasured"
        prose = (
            "H6 remains undermeasured/inconclusive under strict main-couple semantic validation. "
            f"Strict rising coverage is {n_rising} (<{threshold}); criteria were not weakened. "
            "Radway-phase trajectories remain available as genre-grammar triangulation."
        )

    decision_doc = {
        "decision": decision,
        "prose": prose,
        "n_strict_rising": n_rising,
        "strict_rising_topic_ids": membership["strict_rising_topic_ids"],
        "n_strict_falling": membership["n_strict_falling"],
        "baseline_RARC": baseline.get("RARC"),
        "h6_v2_effects": comparison.get("h6_v2", {}).get("effects"),
        "three_panel_figure": str(fig_path.relative_to(root)),
    }
    (day / "h6_v2_decision.json").write_text(
        json.dumps(decision_doc, indent=2, default=str), encoding="utf-8"
    )
    (day / "H6_V2_DECISION.md").write_text(
        f"# H6-v2 decision\n\n**{decision}**\n\n{prose}\n\n"
        f"- Strict rising topics ({n_rising}): {membership['strict_rising_topic_ids']}\n"
        f"- Figure: `{fig_path.relative_to(root)}`\n",
        encoding="utf-8",
    )

    # Optionally point config at v2 if keeping
    if decision == "keep_h6_v2":
        cfg_path = root / "configs/stage11/refined_constructs.yaml"
        text = cfg_path.read_text(encoding="utf-8")
        if "h6_arc.yaml" in text and "h6_arc_v2.yaml" not in text.split("H6:")[1][:400]:
            # Only update H6 prompt line
            import re

            text2, n = re.subn(
                r"(H6:\n(?:.*\n){0,6}?\s*prompt:\s*)configs/stage11/prompts/h6_arc\.yaml",
                r"\1configs/stage11/prompts/h6_arc_v2.yaml",
                text,
                count=1,
            )
            if n:
                cfg_path.write_text(text2, encoding="utf-8")
                decision_doc["config_prompt_updated"] = True
                (day / "h6_v2_decision.json").write_text(
                    json.dumps(decision_doc, indent=2, default=str), encoding="utf-8"
                )

    print(json.dumps(decision_doc, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
