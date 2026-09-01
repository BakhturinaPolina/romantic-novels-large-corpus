"""Visual regression tests for presentation figures (pytest-mpl)."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from src.stage11_refined_construct_analysis.analysis.presentation_suite.catalogs import build_quality_reach_catalog
from src.stage11_refined_construct_analysis.analysis.presentation_suite.paths import default_paths
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
from src.stage11_refined_construct_analysis.analysis.presentation_suite.theme import (
    AXIS_LABEL,
    C_NEG,
    C_NEUTRAL,
    C_POS,
    C_SELECTED,
    EFFECT_GATE,
    HYPOTHESIS_ORDER,
    TICK_TEXT,
    VALUE_LABEL,
    apply_theme,
    gate_band,
    gate_lines,
    marker_for_gate,
)

pytest.importorskip("pytest_mpl")


@pytest.fixture(scope="module")
def paths():
    p = default_paths()
    if not (p.analysis / "13_final_statistical_tests" / "tables").exists():
        pytest.skip("Stage 11 results not present")
    return p


@pytest.mark.mpl_image_compare(baseline_dir="baseline/presentation", tolerance=15)
def test_slide04_pareto_chart_only(paths):
    apply_theme()
    trials = prepare_pareto_points(paths)
    fig, ax = plt.subplots(figsize=(9, 6.5), layout="constrained")
    all_pts = trials[~trials["pareto_efficient"]]
    pareto_pts = trials[trials["pareto_efficient"] & ~trials["is_selected"]]
    selected = trials[trials["is_selected"]]
    ax.scatter(all_pts["topic_diversity"], all_pts["coherence_c_v"], s=12, c="#bbbbbb", alpha=0.5)
    ax.scatter(pareto_pts["topic_diversity"], pareto_pts["coherence_c_v"], s=40, c=C_NEUTRAL, alpha=0.6)
    if not selected.empty:
        ax.scatter(
            selected["topic_diversity"],
            selected["coherence_c_v"],
            s=200,
            marker="*",
            c=C_SELECTED,
            edgecolors=C_NEUTRAL,
            linewidths=1.5,
        )
    ax.set_xlabel("Topic diversity", fontsize=AXIS_LABEL)
    ax.set_ylabel("Coherence (c_v)", fontsize=AXIS_LABEL)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline/presentation", tolerance=15)
def test_slide06_context_measurement_chart_only(paths):
    apply_theme()
    ctx = prepare_context_measurement(paths)
    agreement, primary = ctx["agreement"], ctx["primary"]
    fig = plt.figure(figsize=(12.5, 5.8), layout="constrained")
    ax1 = fig.add_subplot(1, 2, 1)
    y = categorical_y_positions(len(agreement))
    ax1.barh(y, agreement["agreement_pct"].to_numpy(), color=C_POS, height=0.55, alpha=0.85)
    apply_categorical_y_axis(ax1, y, agreement["hypothesis"].tolist())
    ax1.set_xlim(0, 65)
    ax1.set_xlabel("Lexical–contextual agreement (%)", fontsize=AXIS_LABEL)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.axis("off")
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline/presentation", tolerance=15)
def test_slide08_components_chart_only(paths):
    apply_theme()
    df = prepare_component_effects(paths)
    fig, ax = plt.subplots(figsize=(10.5, 6.2), layout="constrained")
    gate_band(ax, orientation="vertical")
    gate_lines(ax, orientation="vertical")
    y = categorical_y_positions(len(df))
    labels = df["display_label"].fillna(df["label"]).tolist()
    for yi, row in zip(y, df.itertuples()):
        est, lo, hi = row.effect_size, row.ci_low, row.ci_high
        mk = marker_for_gate(str(row.measurement_status))
        ax.errorbar(est, yi, xerr=[[est - lo], [hi - est]], fmt="none", color=C_NEUTRAL, capsize=3, lw=1.2)
        ax.scatter([est], [yi], **mk)
    apply_categorical_y_axis(ax, y, labels)
    ax.set_xlim(-0.22, 0.22)
    ax.set_xlabel("Cliff's δ (high-rated − low-rated)", fontsize=AXIS_LABEL)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline/presentation", tolerance=15)
def test_slide09_attention_chart_only(paths):
    apply_theme()
    df = prepare_attention_shift(paths)
    fig, ax = plt.subplots(figsize=(10, 5.5), layout="constrained")
    y = categorical_y_positions(len(df))
    vals = df["diff_pp"].to_numpy()
    ax.barh(y, vals, color=[C_POS if v > 0 else C_NEG for v in vals], height=0.55, alpha=0.85)
    apply_categorical_y_axis(ax, y, df["display_label"].fillna(df["label"]).tolist())
    ax.axvline(0, color="#888", lw=0.8)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline/presentation", tolerance=15)
def test_slide10_quality_reach_chart_only(paths):
    apply_theme()
    df = prepare_quality_reach_dumbbell(paths)
    plot_df = df.copy()
    plot_df["delta_gap"] = plot_df["quality_delta"] - plot_df["reach_delta"]
    plot_df = plot_df.sort_values("delta_gap", ascending=True).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(11, 6), layout="constrained")
    y = categorical_y_positions(len(plot_df))
    for yi, row in zip(y, plot_df.itertuples()):
        ax.scatter([row.quality_delta], [yi], marker="o", s=80, color=C_POS)
        ax.scatter([row.reach_delta], [yi], marker="s", s=70, color=C_NEG)
        ax.plot([row.quality_delta, row.reach_delta], [yi, yi], color="#aaaaaa", lw=1.5)
    apply_categorical_y_axis(ax, y, plot_df["short_label"].fillna(plot_df["label"]).tolist())
    ax.axvline(0, color="#888", lw=0.8)
    return fig


@pytest.mark.mpl_image_compare(baseline_dir="baseline/presentation", tolerance=15)
def test_slide12_ees_integrated_chart_only(paths):
    apply_theme()
    df = prepare_ees_integrated(paths)
    sub = df.loc[df["domain"] == "emotion"]
    fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
    gate_band(ax, orientation="vertical")
    gate_lines(ax, orientation="vertical")
    y = categorical_y_positions(len(sub))
    labels = sub["display_label"].fillna(sub["construct"]).tolist()
    for yi, row in zip(y, sub.itertuples()):
        est, lo, hi = row.cliffs_delta, row.ci_low, row.ci_high
        mk = marker_for_gate("thin" if str(row.status) == "thin" else "viable")
        ax.errorbar(est, yi, xerr=[[est - lo], [hi - est]], fmt="none", color=C_NEUTRAL, capsize=2, lw=1)
        ax.scatter([est], [yi], **mk)
    apply_categorical_y_axis(ax, y, labels)
    ax.set_xlim(-0.25, 0.25)
    return fig
