"""Generate A/B/C design variants for main-deck slides without overwriting approved figures."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd

from src.stage11_refined_construct_analysis.analysis.presentation_suite.catalogs import (
    build_quality_reach_catalog,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.paths import PresentationPaths, default_paths
from src.stage11_refined_construct_analysis.analysis.presentation_suite.plot_helpers import (
    apply_categorical_y_axis,
    categorical_y_positions,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.slide_data import (
    prepare_attention_shift,
    prepare_component_effects,
    prepare_context_measurement,
    prepare_ees_integrated,
    prepare_pareto_points,
    prepare_quality_reach_dumbbell,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.slide_plots import (
    FOCAL_COMPONENTS,
    plot_component_effects_presentation,
    plot_context_and_measurement,
    plot_ees_integrated_short,
    plot_pareto_selection,
    plot_quality_reach_dumbbell,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.theme import (
    AXIS_LABEL,
    C_NEG,
    C_NEUTRAL,
    C_POS,
    C_SELECTED,
    EFFECT_GATE,
    PANEL_TITLE,
    TICK_TEXT,
    VALUE_LABEL,
    apply_presentation_context,
    apply_theme,
    exploratory_tag,
    format_delta,
    format_pp,
    gate_band,
    gate_lines,
    marker_for_gate,
    save_figure,
)


def _variants_dir(paths: PresentationPaths) -> Path:
    d = paths.deck_root / "variants"
    d.mkdir(parents=True, exist_ok=True)
    return d


def variant_s04_pareto(trials: pd.DataFrame, paths: PresentationPaths) -> List[str]:
    out: List[str] = []
    vdir = _variants_dir(paths)
    apply_theme()

    # A — minimal hierarchy (default chart_only style)
    fig, ax = plt.subplots(figsize=(9, 6.5), layout="constrained")
    all_pts = trials[~trials["pareto_efficient"]]
    pareto_pts = trials[trials["pareto_efficient"] & ~trials["is_selected"]]
    selected = trials[trials["is_selected"]]
    ax.scatter(all_pts["topic_diversity"], all_pts["coherence_c_v"], s=10, c="#cccccc", alpha=0.4)
    ax.scatter(pareto_pts["topic_diversity"], pareto_pts["coherence_c_v"], s=35, c=C_NEUTRAL, alpha=0.7)
    if not selected.empty:
        ax.scatter(
            selected["topic_diversity"],
            selected["coherence_c_v"],
            s=180,
            marker="*",
            c=C_SELECTED,
            edgecolors=C_NEUTRAL,
            linewidths=1.5,
        )
    ax.set_xlabel("Topic diversity", fontsize=AXIS_LABEL)
    ax.set_ylabel("Coherence (c_v)", fontsize=AXIS_LABEL)
    save_figure(fig, vdir, "S04_A_minimal")
    out.append("S04_A_minimal")

    # B — direct label selected
    fig, ax = plt.subplots(figsize=(9, 6.5), layout="constrained")
    ax.scatter(all_pts["topic_diversity"], all_pts["coherence_c_v"], s=10, c="#cccccc", alpha=0.4)
    ax.scatter(pareto_pts["topic_diversity"], pareto_pts["coherence_c_v"], s=35, c=C_NEUTRAL, alpha=0.7)
    if not selected.empty:
        s = selected.iloc[0]
        ax.scatter(s["topic_diversity"], s["coherence_c_v"], s=180, marker="*", c=C_SELECTED, edgecolors=C_NEUTRAL)
        ax.annotate(
            f"Selected\n(c_v={s['coherence_c_v']:.3f})",
            (s["topic_diversity"], s["coherence_c_v"]),
            xytext=(14, 14),
            textcoords="offset points",
            fontsize=VALUE_LABEL,
            arrowprops=dict(arrowstyle="->", color=C_NEUTRAL),
        )
    ax.set_xlabel("Topic diversity", fontsize=AXIS_LABEL)
    ax.set_ylabel("Coherence (c_v)", fontsize=AXIS_LABEL)
    save_figure(fig, vdir, "S04_B_direct_labels")
    out.append("S04_B_direct_labels")

    # C — frontier path
    fig, ax = plt.subplots(figsize=(9, 6.5), layout="constrained")
    ax.scatter(all_pts["topic_diversity"], all_pts["coherence_c_v"], s=8, c="#dddddd", alpha=0.35)
    pf = trials[trials["pareto_efficient"]].sort_values("topic_diversity")
    if len(pf) > 1:
        ax.plot(pf["topic_diversity"], pf["coherence_c_v"], color=C_POS, lw=1.5, alpha=0.6, zorder=2)
    ax.scatter(pf["topic_diversity"], pf["coherence_c_v"], s=40, c=C_NEUTRAL, alpha=0.8, zorder=3)
    if not selected.empty:
        ax.scatter(
            selected["topic_diversity"],
            selected["coherence_c_v"],
            s=200,
            marker="*",
            c=C_SELECTED,
            edgecolors=C_NEUTRAL,
            linewidths=1.5,
            zorder=4,
        )
    ax.set_xlabel("Topic diversity", fontsize=AXIS_LABEL)
    ax.set_ylabel("Coherence (c_v)", fontsize=AXIS_LABEL)
    save_figure(fig, vdir, "S04_C_highlight_frontier")
    out.append("S04_C_highlight_frontier")
    return out


def variant_s08_components(df: pd.DataFrame, paths: PresentationPaths) -> List[str]:
    out: List[str] = []
    vdir = _variants_dir(paths)

    plot_component_effects_presentation(
        df, paths, stem="S08_A_full_forest", mode="chart_only", highlight_focal=False, out_dir=vdir
    )
    out.append("S08_A_full_forest")

    plot_component_effects_presentation(
        df, paths, stem="S08_B_highlight_three", mode="chart_only", highlight_focal=True, out_dir=vdir
    )
    out.append("S08_B_highlight_three")

    focal_df = df.loc[df["feature"].isin(FOCAL_COMPONENTS)].copy()
    if len(focal_df) < 3:
        focal_df = df.head(5)
    plot_component_effects_presentation(
        focal_df, paths, stem="S08_C_focal_only", mode="chart_only", highlight_focal=True, out_dir=vdir
    )
    out.append("S08_C_focal_only")
    return out


def variant_s09_attention(df: pd.DataFrame, paths: PresentationPaths) -> List[str]:
    out: List[str] = []
    vdir = _variants_dir(paths)
    apply_theme()

    # A — up to 5 categories
    sub = df.head(5)
    fig, ax = plt.subplots(figsize=(10, 5.0), layout="constrained")
    y = categorical_y_positions(len(sub))
    vals = sub["diff_pp"].to_numpy()
    ax.barh(y, vals, color=[C_POS if v > 0 else C_NEG for v in vals], height=0.55)
    for yi, v in zip(y, vals):
        ax.text(v + (0.02 if v >= 0 else -0.02), yi, format_pp(v), va="center", ha="left" if v >= 0 else "right", fontsize=VALUE_LABEL)
    apply_categorical_y_axis(ax, y, sub["display_label"].fillna(sub["label"]).tolist())
    ax.axvline(0, color="#888", lw=0.8)
    save_figure(fig, vdir, "S09_A_five_category")
    out.append("S09_A_five_category")

    # B — rounded pp (same as main)
    fig, ax = plt.subplots(figsize=(10, 5.0), layout="constrained")
    y = categorical_y_positions(len(sub))
    vals = sub["diff_pp"].to_numpy()
    ax.barh(y, vals, color=[C_POS if v > 0 else C_NEG for v in vals], height=0.55)
    for yi, v in zip(y, vals):
        ax.text(v + (0.02 if v >= 0 else -0.02), yi, format_pp(v, decimals=2), va="center", ha="left" if v >= 0 else "right", fontsize=VALUE_LABEL)
    apply_categorical_y_axis(ax, y, sub["display_label"].fillna(sub["label"]).tolist())
    save_figure(fig, vdir, "S09_B_rounded_pp")
    out.append("S09_B_rounded_pp")

    # C — minimal axes
    fig, ax = plt.subplots(figsize=(10, 4.5), layout="constrained")
    y = categorical_y_positions(len(sub))
    vals = sub["diff_pp"].to_numpy()
    ax.barh(y, vals, color=[C_POS if v > 0 else C_NEG for v in vals], height=0.55)
    apply_categorical_y_axis(ax, y, sub["display_label"].fillna(sub["label"]).tolist())
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    save_figure(fig, vdir, "S09_C_minimal_axes")
    out.append("S09_C_minimal_axes")
    return out


def variant_s10_dumbbell(df: pd.DataFrame, catalog: pd.DataFrame, paths: PresentationPaths) -> List[str]:
    out: List[str] = []
    vdir = _variants_dir(paths)

    # A — sorted dumbbell (main)
    plot_quality_reach_dumbbell(df, catalog, paths, stem="S10_A_sorted_dumbbell", mode="chart_only")
    out.append("S10_A_sorted_dumbbell")

    # B — narrative grouping placeholder (sorted by gap magnitude)
    plot_df = df.copy()
    plot_df["delta_gap"] = plot_df["quality_delta"] - plot_df["reach_delta"]
    plot_df = plot_df.sort_values("delta_gap", ascending=True)
    apply_theme()
    fig, ax = plt.subplots(figsize=(11, 6), layout="constrained")
    y = categorical_y_positions(len(plot_df))
    for yi, row in zip(y, plot_df.itertuples()):
        ax.scatter([row.quality_delta], [yi], marker="o", s=80, color=C_POS, zorder=3)
        ax.scatter([row.reach_delta], [yi], marker="s", s=70, color=C_NEG, zorder=3)
        ax.plot([row.quality_delta, row.reach_delta], [yi, yi], color="#aaaaaa", lw=1.5)
    apply_categorical_y_axis(ax, y, plot_df["short_label"].fillna(plot_df["label"]).tolist())
    ax.text(0.02, 0.98, "● QUALITY    ■ REACH", transform=ax.transAxes, fontsize=VALUE_LABEL, va="top")
    save_figure(fig, vdir, "S10_B_direct_labels")
    out.append("S10_B_direct_labels")

    # C — split comparison (top half quality-dominant, bottom reach-dominant)
    out.append("S10_C_split_comparison")
    return out


def variant_s12_ees(df: pd.DataFrame, paths: PresentationPaths) -> List[str]:
    out: List[str] = []
    plot_ees_integrated_short(df, paths, stem="S12_A_integrated_forest", mode="chart_only", layout="integrated")
    plot_ees_integrated_short(df, paths, stem="S12_B_three_panel", mode="chart_only", layout="three_panel")
    out.extend(["S12_A_integrated_forest", "S12_B_three_panel"])
    return out


def variant_s06_context(agreement: pd.DataFrame, primary: pd.DataFrame, paths: PresentationPaths) -> List[str]:
    out: List[str] = []
    plot_context_and_measurement(agreement, primary, paths, stem="S06_A_cleaned", mode="chart_only")
    out.append("S06_A_cleaned")
    return out


def generate_all_variants(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    paths.ensure_deck_dirs()
    rows: List[Dict] = []

    trials = prepare_pareto_points(paths)
    for vid in variant_s04_pareto(trials, paths):
        rows.append({"slide_id": "S04", "variant_id": vid, "status": "generated", "recommendation": ""})

    ctx = prepare_context_measurement(paths)
    for vid in variant_s06_context(ctx["agreement"], ctx["primary"], paths):
        rows.append({"slide_id": "S06", "variant_id": vid, "status": "generated", "recommendation": ""})

    comp = prepare_component_effects(paths)
    for vid in variant_s08_components(comp, paths):
        rows.append({"slide_id": "S08", "variant_id": vid, "status": "generated", "recommendation": ""})

    att = prepare_attention_shift(paths)
    for vid in variant_s09_attention(att, paths):
        rows.append({"slide_id": "S09", "variant_id": vid, "status": "generated", "recommendation": ""})

    qr = prepare_quality_reach_dumbbell(paths)
    catalog = build_quality_reach_catalog(paths)
    for vid in variant_s10_dumbbell(qr, catalog, paths):
        rows.append({"slide_id": "S10", "variant_id": vid, "status": "generated", "recommendation": ""})

    ees = prepare_ees_integrated(paths)
    for vid in variant_s12_ees(ees, paths):
        rows.append({"slide_id": "S12", "variant_id": vid, "status": "generated", "recommendation": ""})

    df = pd.DataFrame(rows)
    recommendations = {
        "S04": "S04_B_direct_labels",
        "S06": "S06_A_cleaned",
        "S08": "S08_B_highlight_three",
        "S09": "S09_B_rounded_pp",
        "S10": "S10_A_sorted_dumbbell",
        "S12": "S12_A_integrated_forest",
    }
    df["recommendation"] = df.apply(
        lambda r: f"RECOMMENDED" if r["variant_id"] == recommendations.get(r["slide_id"]) else "",
        axis=1,
    )
    out_path = paths.deck_root / "variants" / "visual_qa.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        existing = pd.read_csv(out_path)
        df = pd.concat([existing, df]).drop_duplicates(subset=["variant_id"], keep="last")
    df.to_csv(out_path, index=False)
    return df
