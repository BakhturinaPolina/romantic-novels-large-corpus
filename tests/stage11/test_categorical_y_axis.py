"""Tests for categorical y-axis label ↔ value alignment in presentation plots."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from src.stage11_refined_construct_analysis.analysis.presentation_suite.evidence_metadata import (
    build_all_metadata,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.figures_main import (
    fig01_contextual_agreement,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.paths import default_paths
from src.stage11_refined_construct_analysis.analysis.presentation_suite.plot_helpers import (
    apply_categorical_y_axis,
    assert_label_value_alignment,
    categorical_y_positions,
    extract_barh_label_values,
    extract_scatter_x_at_y,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.slide_data import (
    prepare_attention_shift,
    prepare_component_effects,
    prepare_context_measurement,
    prepare_ees_integrated,
    prepare_quality_reach_dumbbell,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.slide_plots import (
    plot_attention_shift_short,
    plot_component_effects_presentation,
    plot_context_and_measurement,
    plot_ees_integrated_short,
    plot_quality_reach_dumbbell,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.theme import apply_theme


@pytest.fixture(scope="module")
def paths():
    p = default_paths()
    if not (p.analysis / "13_final_statistical_tests" / "tables").exists():
        pytest.skip("Stage 11 results not present")
    return p


@pytest.fixture(scope="module")
def frames(paths):
    return build_all_metadata(paths, write=False)


def _tick_label_value_pairs(ax) -> list[tuple[str, float]]:
    """Map tick labels (top→bottom) to primary x values at each y tick."""
    tick_locs = list(ax.get_yticks())
    tick_labels = [t.get_text() for t in ax.get_yticklabels()]
    loc_to_label = dict(zip(tick_locs, tick_labels))
    # Collect scatter x at each y
    y_to_x: dict[float, float] = {}
    for coll in ax.collections:
        for x, y in coll.get_offsets():
            y_to_x[float(y)] = float(x)
    # barh widths
    for patch in ax.patches:
        if patch.get_height() > 0:
            yi = patch.get_y() + patch.get_height() / 2
            y_to_x[yi] = float(patch.get_width())
    # errorbar lines — use line x data midpoint
    for line in ax.lines:
        xdata, ydata = line.get_xdata(), line.get_ydata()
        if len(xdata) == 2 and len(set(ydata)) == 1:
            y_to_x[float(ydata[0])] = float(np.mean(xdata))
    pairs = []
    for loc in sorted(tick_locs):
        label = loc_to_label.get(loc, "")
        if label and loc in y_to_x:
            pairs.append((label, y_to_x[loc]))
        elif label and y_to_x:
            nearest_y = min(y_to_x.keys(), key=lambda yy: abs(yy - loc))
            pairs.append((label, y_to_x[nearest_y]))
    return pairs


def test_categorical_helper_ordering():
    apply_theme()
    fig, ax = plt.subplots()
    labels = ["A", "B", "C"]
    y = categorical_y_positions(3)
    ax.barh(y, [1, 2, 3])
    apply_categorical_y_axis(ax, y, labels)
    got = [t.get_text() for t in ax.get_yticklabels()]
    assert got == labels
    plt.close(fig)


def test_s06_agreement_label_alignment(paths):
    ctx = prepare_context_measurement(paths)
    agreement = ctx["agreement"]
    apply_theme()
    fig, ax = plt.subplots()
    y = categorical_y_positions(len(agreement))
    ax.barh(y, agreement["agreement_pct"].to_numpy())
    apply_categorical_y_axis(ax, y, agreement["hypothesis"].tolist())
    pairs = _tick_label_value_pairs(ax)
    expected_labels = agreement["hypothesis"].tolist()
    expected_values = agreement["agreement_pct"].tolist()
    assert [p[0] for p in pairs] == expected_labels
    for (_, got), exp in zip(pairs, expected_values):
        assert abs(got - exp) < 0.01
    plt.close(fig)


def test_s08_component_label_alignment(paths):
    df = prepare_component_effects(paths)
    _, _ = plot_component_effects_presentation(df, paths, save=False)
    apply_theme()
    fig, ax = plt.subplots()
    y = categorical_y_positions(len(df))
    labels = df["display_label"].fillna(df["label"]).tolist()
    for yi, row in zip(y, df.itertuples()):
        ax.scatter([row.effect_size], [yi])
    apply_categorical_y_axis(ax, y, labels)
    pairs = _tick_label_value_pairs(ax)
    assert [p[0] for p in pairs] == labels
    for (label, got), row in zip(pairs, df.itertuples()):
        assert label == row.display_label or label == row.label
        assert abs(got - row.effect_size) < 1e-6
    plt.close(fig)


def test_s09_attention_label_alignment(paths):
    df = prepare_attention_shift(paths)
    apply_theme()
    fig, ax = plt.subplots()
    y = categorical_y_positions(len(df))
    vals = df["diff_pp"].to_numpy()
    ax.barh(y, vals)
    labels = df["display_label"].fillna(df["label"]).tolist()
    apply_categorical_y_axis(ax, y, labels)
    pairs = extract_barh_label_values(ax)
    assert [p[0] for p in pairs] == labels
    for (_, got), exp in zip(pairs, vals):
        assert abs(got - exp) < 1e-6
    plt.close(fig)


def test_s10_dumbbell_label_alignment(paths):
    from src.stage11_refined_construct_analysis.analysis.presentation_suite.catalogs import (
        build_quality_reach_catalog,
    )

    df = prepare_quality_reach_dumbbell(paths)
    catalog = build_quality_reach_catalog(paths)
    apply_theme()
    fig, ax = plt.subplots()
    plot_df = df.copy()
    if "delta_gap" not in plot_df.columns:
        plot_df["delta_gap"] = plot_df["quality_delta"] - plot_df["reach_delta"]
    plot_df = plot_df.sort_values("delta_gap", ascending=True).reset_index(drop=True)
    y = categorical_y_positions(len(plot_df))
    for yi, row in zip(y, plot_df.itertuples()):
        ax.scatter([row.quality_delta], [yi])
    labels = plot_df["short_label"].fillna(plot_df["label"]).tolist()
    apply_categorical_y_axis(ax, y, labels)
    pairs = _tick_label_value_pairs(ax)
    assert [p[0] for p in pairs] == labels
    plt.close(fig)


def test_s12_ees_integrated_label_alignment(paths):
    df = prepare_ees_integrated(paths)
    apply_theme()
    fig, ax = plt.subplots()
    sub = df.loc[df["domain"] == "emotion"]
    y = categorical_y_positions(len(sub))
    labels = sub["display_label"].fillna(sub["construct"]).tolist()
    for yi, row in zip(y, sub.itertuples()):
        ax.scatter([row.cliffs_delta], [yi])
    apply_categorical_y_axis(ax, y, labels)
    pairs = _tick_label_value_pairs(ax)
    assert [p[0] for p in pairs] == labels
    plt.close(fig)


def test_fig01_agreement_label_alignment(paths, frames):
    apply_theme()
    agreement = frames["presentation_agreement"]
    fig, ax = plt.subplots()
    y = categorical_y_positions(len(agreement))
    pct = agreement["agreement_pct"].to_numpy()
    ax.scatter(pct, y)
    apply_categorical_y_axis(ax, y, agreement["hypothesis"].tolist())
    pairs = _tick_label_value_pairs(ax)
    assert [p[0] for p in pairs] == agreement["hypothesis"].tolist()
    plt.close(fig)


def test_appendix_richness_panel_a_alignment(paths):
    from src.stage11_refined_construct_analysis.analysis.presentation_suite.evidence_metadata import _read_table

    cliffs = _read_table(paths.table("14_exploratory_presentation_results", "thematic_richness_cliffs_delta"))
    feats = ["taxonomy_n_eff", "rare_taxonomy_n_eff"]
    labels = ["Raw taxonomy eᴴ", "Rarefied taxonomy eᴴ"]
    sub = cliffs.set_index("feature").loc[feats]
    apply_theme()
    fig, ax = plt.subplots()
    y = categorical_y_positions(len(feats))
    for yi, feat in zip(y, feats):
        ax.scatter([sub.loc[feat]["cliffs_delta"]], [yi])
    apply_categorical_y_axis(ax, y, labels)
    pairs = _tick_label_value_pairs(ax)
    assert [p[0] for p in pairs] == labels
    plt.close(fig)
