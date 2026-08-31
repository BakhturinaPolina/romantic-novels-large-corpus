"""Direct Radway Phase I/II/III begin–middle–end trajectories (no LLM).

Primary operationalization uses radway_main_id only.
Sensitivity uses main ∪ secondary assignment.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.stage10_correlation_analysis.analysis.arc import (
    TERTILE_ORDER,
    pivot_tertiles,
    tertile_deltas,
    tertile_profile_by_group,
)
from src.stage10_correlation_analysis.analysis.effects import two_group_effects

PHASE_FEATURES = ("RADWAY_I", "RADWAY_II", "RADWAY_III")
PHASE_TO_IDS = {
    "RADWAY_I": {f"R{i}" for i in range(1, 8)},
    "RADWAY_II": {"R8", "R9", "R10"},
    "RADWAY_III": {"R11", "R12", "R13"},
}
ID_TO_PHASE = {
    rid: phase for phase, ids in PHASE_TO_IDS.items() for rid in ids
}


def load_radway_lookup(
    topic_lookup_path: Path,
    taxonomy_with_radway_path: Optional[Path] = None,
) -> pd.DataFrame:
    """Flat topic → Radway columns; optionally attach other_plausible from JSON."""
    lookup = pd.read_parquet(topic_lookup_path)
    if "topic_id" not in lookup.columns:
        raise KeyError("topic_lookup missing topic_id")
    if taxonomy_with_radway_path is not None and taxonomy_with_radway_path.exists():
        raw = json.loads(taxonomy_with_radway_path.read_text(encoding="utf-8"))
        other: Dict[int, List[str]] = {}
        for key, obj in raw.items():
            if not isinstance(obj, dict):
                continue
            rf = obj.get("radway_functions") or {}
            try:
                tid = int(rf.get("topic_id", key))
            except (TypeError, ValueError):
                continue
            ids = rf.get("radway_other_plausible_ids") or []
            other[tid] = [str(x) for x in ids if x]
        lookup = lookup.copy()
        lookup["radway_other_plausible_ids"] = lookup["topic_id"].map(
            lambda t: other.get(int(t), [])
        )
    return lookup


def _phase_for_ids(ids: Iterable[str]) -> Optional[str]:
    phases = {ID_TO_PHASE[i] for i in ids if i in ID_TO_PHASE}
    if len(phases) == 1:
        return next(iter(phases))
    if not phases:
        return None
    # Multiple phases on one topic: prefer main-driven caller path; for multi, skip
    return None


def topic_phase_map(
    lookup: pd.DataFrame,
    *,
    mode: str = "main",
) -> pd.Series:
    """topic_id → RADWAY_I|II|III (NaN if none).

    mode='main': radway_main_id only.
    mode='main_secondary': if main is none, fall back to secondary; if main set, use main.
    """
    rows: Dict[int, Optional[str]] = {}
    for _, row in lookup.iterrows():
        tid = int(row["topic_id"])
        main = str(row.get("radway_main_id") or "none")
        sec = row.get("radway_secondary_id")
        sec_s = str(sec) if pd.notna(sec) and sec not in (None, "", "none", "None") else None
        if mode == "main":
            phase = ID_TO_PHASE.get(main)
        elif mode == "main_secondary":
            if main in ID_TO_PHASE:
                phase = ID_TO_PHASE[main]
            elif sec_s and sec_s in ID_TO_PHASE:
                phase = ID_TO_PHASE[sec_s]
            else:
                phase = None
        else:
            raise ValueError(f"Unknown mode: {mode}")
        rows[tid] = phase
    return pd.Series(rows, name="radway_phase_feature")


def aggregate_tertile_phases(
    tertile_counts: pd.DataFrame,
    topic_to_phase: pd.Series,
    *,
    id_column: str = "book_id",
    tertile_column: str = "tertile",
    topic_column: str = "topic_id",
    count_column: str = "n_sentences",
) -> pd.DataFrame:
    """Roll topic counts to Radway phases; renormalize within book×tertile over all sentences."""
    frame = tertile_counts.copy()
    frame["feature"] = frame[topic_column].map(topic_to_phase)
    # Keep unmapped rows for denominator (full tertile mass)
    totals = (
        frame.groupby([id_column, tertile_column], as_index=False)[count_column]
        .sum()
        .rename(columns={count_column: "tertile_total"})
    )
    mapped = frame.dropna(subset=["feature"])
    grouped = mapped.groupby(
        [id_column, tertile_column, "feature"], as_index=False
    )[count_column].sum()
    grouped = grouped.merge(totals, on=[id_column, tertile_column], how="left")
    grouped["share"] = grouped[count_column] / grouped["tertile_total"].replace(0, np.nan)
    # Ensure all phase features present for each book×tertile (share 0)
    books = totals[[id_column, tertile_column, "tertile_total"]]
    grid = (
        books.assign(_k=1)
        .merge(pd.DataFrame({"feature": list(PHASE_FEATURES), "_k": 1}), on="_k")
        .drop(columns="_k")
    )
    out = grid.merge(
        grouped[[id_column, tertile_column, "feature", count_column, "share"]],
        on=[id_column, tertile_column, "feature"],
        how="left",
    )
    out[count_column] = out[count_column].fillna(0)
    out["share"] = out["share"].fillna(0.0)
    return out


def run_radway_phase_analysis(
    *,
    tertile_counts: pd.DataFrame,
    lookup: pd.DataFrame,
    analysis_frame: pd.DataFrame,
    out_dir: Path,
    tier_column: str = "rating_class",
    tier_high: str = "high_rate",
    tier_low: str = "low_rate",
) -> Dict[str, Path]:
    """Write tables + figures for main and main_secondary modes."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    paths: Dict[str, Path] = {}

    frame = analysis_frame[[c for c in ("book_id", tier_column, "rating") if c in analysis_frame.columns]].copy()
    frame = frame.drop_duplicates("book_id").set_index("book_id")

    for mode in ("main", "main_secondary"):
        topic_to_phase = topic_phase_map(lookup, mode=mode)
        long = aggregate_tertile_phases(tertile_counts, topic_to_phase)
        wide = pivot_tertiles(long)
        deltas = tertile_deltas(wide, list(PHASE_FEATURES))
        # Overall mean profile
        overall = (
            long.groupby(["feature", "tertile"], observed=True)["share"]
            .agg(mean="mean", median="median", sd="std", n="size")
            .reset_index()
        )
        overall_path = out_dir / f"phase_profile_overall_{mode}.csv"
        overall.to_csv(overall_path, index=False)
        paths[f"overall_{mode}"] = overall_path

        delta_summary = []
        for feat in PHASE_FEATURES:
            col = f"{feat}__end_minus_begin"
            if col not in deltas.columns:
                continue
            vals = deltas[col].dropna()
            delta_summary.append(
                {
                    "feature": feat,
                    "mode": mode,
                    "mean_end_minus_begin": float(vals.mean()),
                    "median_end_minus_begin": float(vals.median()),
                    "share_books_rising": float((vals > 0).mean()),
                    "n_books": int(vals.size),
                }
            )
        delta_df = pd.DataFrame(delta_summary)
        delta_path = out_dir / f"phase_deltas_{mode}.csv"
        delta_df.to_csv(delta_path, index=False)
        paths[f"deltas_{mode}"] = delta_path

        # Tier profiles
        if tier_column in frame.columns:
            group_map = frame[tier_column]
            profile = tertile_profile_by_group(long, group_map, list(PHASE_FEATURES))
            profile_path = out_dir / f"phase_profile_by_tier_{mode}.csv"
            profile.to_csv(profile_path, index=False)
            paths[f"tier_profile_{mode}"] = profile_path

            # Arc index: III − I end−begin movement (genre grammar strength)
            if (
                "RADWAY_III__end_minus_begin" in deltas.columns
                and "RADWAY_I__end_minus_begin" in deltas.columns
            ):
                arc = (
                    deltas["RADWAY_III__end_minus_begin"]
                    - deltas["RADWAY_I__end_minus_begin"]
                ).rename("radway_phase_arc_index")
            else:
                arc = pd.Series(dtype=float, name="radway_phase_arc_index")
            book_feats = deltas.copy()
            book_feats["radway_phase_arc_index"] = arc
            book_feats = book_feats.join(frame, how="left")
            book_path = out_dir / f"book_phase_deltas_{mode}.parquet"
            book_feats.to_parquet(book_path)
            paths[f"book_deltas_{mode}"] = book_path

            effect_cols = [
                c
                for c in book_feats.columns
                if c.endswith("__end_minus_begin") or c == "radway_phase_arc_index"
            ]
            if effect_cols and tier_column in book_feats.columns:
                effects = two_group_effects(
                    book_feats.reset_index(),
                    effect_cols,
                    tier_column,
                    tier_high,
                    tier_low,
                    n_replicates=1000,
                    seed=42,
                )
                effects_path = out_dir / f"phase_tier_effects_{mode}.csv"
                effects.to_csv(effects_path, index=False)
                paths[f"tier_effects_{mode}"] = effects_path

        # Plot overall trajectory
        fig, ax = plt.subplots(figsize=(6.5, 4.0))
        order = list(TERTILE_ORDER)
        for feat, color in zip(
            PHASE_FEATURES, ("#b85c38", "#2a6f7f", "#2f6b3a")
        ):
            sub = overall[overall["feature"] == feat].set_index("tertile").reindex(order)
            ax.plot(order, sub["mean"].to_numpy(), marker="o", label=feat, color=color)
        ax.set_ylabel("Mean share within tertile")
        ax.set_xlabel("Narrative position")
        ax.set_title(f"Radway phase trajectories ({mode})")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig_path = fig_dir / f"radway_phases_overall_{mode}.png"
        fig.savefig(fig_path, dpi=150)
        plt.close(fig)
        paths[f"fig_overall_{mode}"] = fig_path

        # High vs low tier panel
        if tier_column in frame.columns and f"tier_profile_{mode}" in paths:
            profile = pd.read_csv(paths[f"tier_profile_{mode}"])
            fig, axes = plt.subplots(1, 2, figsize=(10, 4.0), sharey=True)
            for ax, tier, title in zip(
                axes,
                (tier_low, tier_high),
                ("Low-rated", "High-rated"),
            ):
                for feat, color in zip(
                    PHASE_FEATURES, ("#b85c38", "#2a6f7f", "#2f6b3a")
                ):
                    sub = profile[
                        (profile["feature"] == feat) & (profile["group"] == tier)
                    ].set_index("tertile").reindex(order)
                    ax.plot(
                        order,
                        sub["mean"].to_numpy(dtype=float),
                        marker="o",
                        label=feat,
                        color=color,
                    )
                ax.set_title(title)
                ax.set_xlabel("Narrative position")
            axes[0].set_ylabel("Mean share")
            axes[0].legend(frameon=False, fontsize=8)
            fig.suptitle(f"Radway phases by rating tier ({mode})", y=1.02)
            fig.tight_layout()
            fig_path = fig_dir / f"radway_phases_by_tier_{mode}.png"
            fig.savefig(fig_path, dpi=150, bbox_inches="tight")
            plt.close(fig)
            paths[f"fig_tier_{mode}"] = fig_path

    summary = {
        "features": list(PHASE_FEATURES),
        "phase_ids": {k: sorted(v) for k, v in PHASE_TO_IDS.items()},
        "outputs": {k: str(v) for k, v in paths.items()},
    }
    summary_path = out_dir / "radway_phases_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    paths["summary"] = summary_path
    return paths
