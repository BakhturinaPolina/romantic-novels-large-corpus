"""Main presentation figures (fig01–fig06)."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from .evidence_metadata import build_all_metadata, load_agreement, load_components, load_primaries
from .paths import PresentationPaths, default_paths
from .theme import (
    C_EXPL,
    C_NEG,
    C_NEUTRAL,
    C_POS,
    C_THIN,
    C_UNMEAS,
    EFFECT_GATE,
    HYPOTHESIS_ORDER,
    apply_theme,
    gate_lines,
    marker_for_gate,
    save_figure,
    status_symbol,
)


def _manifest_row(
    figure_id: str,
    figure_name: str,
    level: str,
    sources: Sequence[str],
    measure: str,
    evidence: str,
    warning: str,
    paths: List[Path],
) -> Dict:
    return {
        "figure_id": figure_id,
        "figure_name": figure_name,
        "presentation_level": level,
        "notebook_source": "; ".join(sources),
        "table_source": "; ".join(sources),
        "variables_used": measure,
        "statistical_measure": measure,
        "confirmatory_or_exploratory": evidence,
        "measurement_warning": warning,
        "output_path": str(paths[0]) if paths else "",
    }


def fig01_contextual_agreement(
    paths: PresentationPaths,
    agreement: pd.DataFrame | None = None,
) -> Tuple[List[Path], Dict]:
    agreement = agreement if agreement is not None else load_agreement(paths)
    apply_theme()
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    y = np.arange(len(agreement))[::-1]
    pct = agreement["agreement_pct"].to_numpy()
    ax.hlines(y, 0, pct, color="#56B4E9", lw=2)
    ax.scatter(pct, y, color=C_POS, s=70, zorder=3)
    for yi, row in zip(y, agreement.itertuples()):
        ax.text(row.agreement_pct + 1.5, yi, row.label, va="center", fontsize=11, color=C_NEUTRAL)
    ax.set_yticks(y)
    ax.set_yticklabels(agreement["hypothesis"])
    ax.set_xlim(0, 75)
    ax.set_xlabel("Lexical–contextual agreement (%)")
    ax.set_title("Contextual coding often diverged from lexical cues (H1–H6)")
    ax.text(
        0.0,
        1.02,
        "Agreement = Pass A (lexical) matches Pass B (contextual) topic codes",
        transform=ax.transAxes,
        fontsize=10,
        color="#555555",
    )
    outs = save_figure(fig, paths.out_dir, "fig01_contextual_agreement")
    return outs, _manifest_row(
        "fig01",
        "Contextual agreement H1–H6",
        "main",
        ["01–06 lexical_contextual_agreement"],
        "agreement_pct = n_agree/n_total",
        "methodological",
        "",
        outs,
    )


def fig02_measurement_status(
    paths: PresentationPaths,
    primary: pd.DataFrame | None = None,
) -> Tuple[List[Path], Dict]:
    primary = primary if primary is not None else load_primaries(paths)
    apply_theme()
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.axis("off")
    cols = ["Hypothesis", "Status", "Topics", "Note"]
    cell_text = []
    colors = []
    for _, r in primary.iterrows():
        st = str(r["measurement_status"])
        sym = status_symbol(st)
        cell_text.append(
            [
                r["hypothesis"],
                f"{sym} {st.capitalize()}",
                r["n_topics_display"],
                r["measurement_note"],
            ]
        )
        if st == "viable":
            colors.append(["#ffffff", "#d9f2e6", "#ffffff", "#ffffff"])
        elif st == "thin":
            colors.append(["#ffffff", "#fff2cc", "#ffffff", "#ffffff"])
        else:
            colors.append(["#ffffff", "#eeeeee", "#ffffff", "#ffffff"])
    table = ax.table(
        cellText=cell_text,
        colLabels=cols,
        cellColours=colors,
        colColours=["#f0f0f0"] * 4,
        loc="center",
        cellLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2.0)
    ax.set_title(
        "Could H1–H6 still be measured after contextual refinement?",
        pad=18,
        fontsize=14,
    )
    outs = save_figure(fig, paths.out_dir, "fig02_measurement_status")
    return outs, _manifest_row(
        "fig02",
        "Measurement-status strip",
        "main",
        ["final_verdict_table", "construct_coverage.json"],
        "measurement_status; topic counts",
        "confirmatory",
        "H2/H3 unmeasurable — not zero effects",
        outs,
    )


def fig03_primary_verdicts(
    paths: PresentationPaths,
    primary: pd.DataFrame | None = None,
) -> Tuple[List[Path], Dict]:
    primary = primary if primary is not None else load_primaries(paths)
    apply_theme()
    fig, axes = plt.subplots(
        1,
        4,
        figsize=(12.5, 5.6),
        gridspec_kw={"width_ratios": [0.7, 1.1, 3.2, 1.4]},
        sharey=True,
    )
    ax_h, ax_m, ax_e, ax_v = axes
    y = np.arange(len(primary))[::-1]

    for ax in (ax_h, ax_m, ax_v):
        ax.set_xlim(0, 1)
        ax.axis("off")
        for spine in ax.spines.values():
            spine.set_visible(False)

    for yi, r in zip(y, primary.itertuples()):
        st = str(r.measurement_status)
        ax_h.text(0.05, yi, r.hypothesis, ha="left", va="center", fontsize=13, fontweight="bold")
        ax_m.text(0.05, yi, f"{status_symbol(st)} {st}", ha="left", va="center", fontsize=11, color="#444444")
        ax_v.text(0.05, yi, str(r.verdict), ha="left", va="center", fontsize=11, color=C_NEUTRAL)
        if st == "unmeasurable" or pd.isna(r.effect_size):
            ax_e.text(
                0.0,
                yi,
                "Unmeasurable after refinement",
                va="center",
                ha="left",
                fontsize=11,
                color=C_UNMEAS,
                style="italic",
            )
        else:
            lo, hi, est = r.ci_low, r.ci_high, r.effect_size
            ax_e.plot([lo, hi], [yi, yi], color=C_NEUTRAL, lw=1.8, zorder=2)
            mk = marker_for_gate(st)
            ax_e.scatter([est], [yi], zorder=3, **mk)

    gate_lines(ax_e, orientation="vertical")
    ax_e.set_yticks(y)
    ax_e.set_yticklabels([])
    ax_e.set_xlim(-0.20, 0.22)
    ax_e.set_xlabel("Cliff's δ (high − low rating tiers)")
    ax_h.text(0.05, len(primary) - 0.35, "Hyp.", fontsize=10, color="#666666")
    ax_m.text(0.05, len(primary) - 0.35, "Measurement", fontsize=10, color="#666666")
    ax_v.text(0.05, len(primary) - 0.35, "Verdict", fontsize=10, color="#666666")
    ax_e.set_ylim(-0.6, len(primary) - 0.2)

    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=C_POS, markersize=9, label="Viable"),
        Line2D([0], [0], marker="o", color=C_POS, markerfacecolor="none", markersize=9, label="Thin"),
    ]
    ax_e.legend(handles=legend, loc="lower right", frameon=False)
    fig.suptitle("Primary H1–H6 confirmatory verdicts", fontsize=14, y=0.98)
    fig.text(
        0.5,
        0.01,
        f"Dashed lines: prespecified |δ| ≥ {EFFECT_GATE:g} gate (not statistical significance). "
        "Unmeasurable hypotheses have no point estimate.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    outs = save_figure(fig, paths.out_dir, "fig03_primary_hypothesis_verdicts")
    return outs, _manifest_row(
        "fig03",
        "Primary hypothesis verdicts",
        "main",
        ["final_verdict_table", "primary_h1_h6_table"],
        "cliffs_delta; CI; final_bucket",
        "confirmatory",
        "Unmeasurable not plotted at 0",
        outs,
    )


def fig04_stage10_stage11_transition(
    paths: PresentationPaths,
    primary: pd.DataFrame | None = None,
) -> Tuple[List[Path], Dict]:
    primary = primary if primary is not None else load_primaries(paths)
    apply_theme()
    fig, ax = plt.subplots(figsize=(11, 6.2))
    x0, x1, x_un = 0.0, 1.0, 2.2
    # Place unmeasurable endpoints in a status band below the δ range (not on the δ scale)
    status_ys = {"H2": -0.22, "H3": -0.26}
    ax.axhspan(-0.30, -0.175, color="#f3f3f3", zorder=0)
    ax.text(
        x_un,
        -0.175,
        "status change (not a δ)",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#666666",
    )

    for r in primary.itertuples():
        ax.scatter([x0], [r.stage10_delta], color="#999999", s=55, zorder=3)
        ax.text(x0 - 0.06, r.stage10_delta, r.hypothesis, ha="right", va="center", fontsize=10)
        if str(r.measurement_status) == "unmeasurable" or pd.isna(r.stage11_delta):
            y_end = status_ys[r.hypothesis]
            ax.annotate(
                "",
                xy=(x_un, y_end),
                xytext=(x0, r.stage10_delta),
                arrowprops=dict(arrowstyle="->", color=C_UNMEAS, lw=1.4, connectionstyle="arc3,rad=0.08"),
            )
            ax.scatter([x_un], [y_end], marker="s", color=C_UNMEAS, s=70, zorder=3)
            ax.text(x_un + 0.06, y_end, f"{r.hypothesis} not measurable", va="center", fontsize=9, color=C_UNMEAS)
        else:
            ax.plot([x0, x1], [r.stage10_delta, r.stage11_delta], color="#56B4E9", lw=1.5, zorder=2)
            mk = marker_for_gate(str(r.measurement_status))
            ax.scatter([x1], [r.stage11_delta], zorder=3, **mk)
            ax.text(x1 + 0.05, r.stage11_delta, r.hypothesis, va="center", fontsize=10)

    gate_lines(ax, orientation="horizontal")
    ax.set_xticks([x0, x1, x_un])
    ax.set_xticklabels(["Stage 10\n(original δ)", "Stage 11\n(refined δ)", "Not measurable\nafter refinement"])
    ax.set_ylabel("Cliff's δ")
    ax.set_title("Contextual refinement changed both effect estimates and measurability")
    ax.set_xlim(-0.35, 2.95)
    ax.set_ylim(-0.32, 0.20)
    outs = save_figure(fig, paths.out_dir, "fig04_stage10_stage11_transition")
    return outs, _manifest_row(
        "fig04",
        "Stage 10 → Stage 11 transition",
        "main",
        ["stage10_vs_final_side_by_side"],
        "original_delta; refined_delta",
        "confirmatory",
        "H2/H3 endpoint is categorical, not δ=0",
        outs,
    )


def fig05_component_effects(
    paths: PresentationPaths,
    components: pd.DataFrame | None = None,
) -> Tuple[List[Path], Dict]:
    components = components if components is not None else load_components(paths)
    # Prefer focus components; keep parent grouping
    df = components.loc[components["focus"]].copy()
    if df.empty:
        df = components.copy()
    # Sort within hypothesis by effect
    h_rank = {h: i for i, h in enumerate(HYPOTHESIS_ORDER)}
    df["_h"] = df["hypothesis"].map(h_rank)
    df = df.sort_values(["_h", "effect_size"]).reset_index(drop=True)

    apply_theme()
    fig, ax = plt.subplots(figsize=(11, 6.5))
    y = np.arange(len(df))
    for yi, r in df.iterrows():
        ax.plot([r["ci_low"], r["ci_high"]], [yi, yi], color=C_NEUTRAL, lw=1.5)
        mk = marker_for_gate(str(r["measurement_status"]))
        ax.scatter([r["effect_size"]], [yi], zorder=3, **mk)
    gate_lines(ax, orientation="vertical")
    labels = [f"{r.hypothesis}: {r.label}" for r in df.itertuples()]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Cliff's δ")
    ax.set_title("Component-level associations (not parent-hypothesis confirmation)")
    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=C_POS, markersize=9, label="Viable measure"),
        Line2D(
            [0],
            [0],
            marker="o",
            color=C_POS,
            markerfacecolor="none",
            markersize=9,
            label="Thin measure (e.g. single-topic)",
        ),
    ]
    ax.legend(handles=legend, loc="lower right", frameon=False)
    ax.text(
        0.0,
        1.02,
        f"Open markers = thin measurement; dashed |δ|={EFFECT_GATE:g} gate",
        transform=ax.transAxes,
        fontsize=10,
        color="#555555",
    )
    fig.subplots_adjust(left=0.32)
    outs = save_figure(fig, paths.out_dir, "fig05_component_effects")
    return outs, _manifest_row(
        "fig05",
        "Component-effect forest",
        "main",
        ["component_effects"],
        "cliffs_delta; CI; measurement_gate",
        "confirmatory_component",
        "Thin protection flagged with open marker",
        outs,
    )


def fig05b_component_evidence_matrix(
    paths: PresentationPaths,
    components: pd.DataFrame | None = None,
    primary: pd.DataFrame | None = None,
) -> Tuple[List[Path], Dict]:
    components = components if components is not None else load_components(paths)
    primary = primary if primary is not None else load_primaries(paths)
    # Show focus components + H1 primary for adjusted disagreement
    focus = components.loc[components["focus"]].copy()
    h1 = primary.loc[primary["hypothesis"] == "H1"].copy()
    h1["label"] = "H1 primary ratio (emotional vs explicit)"
    h1["feature"] = h1["feature"]
    rows = []
    # H1 primary first
    for _, r in h1.iterrows():
        rows.append(r)
    for _, r in focus.iterrows():
        rows.append(r)
    mat = pd.DataFrame(rows)

    def _yn(val) -> str:
        if pd.isna(val):
            return "—"
        return "✓" if bool(val) else "✗"

    apply_theme()
    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    ax.axis("off")
    headers = [
        "Construct",
        "Meas.",
        "|δ|≥.11",
        "Adj. sign\naligned?",
        "Adj. p<.05?",
        "Spec.\nstable?",
        "Viable?",
    ]
    cell = []
    for _, r in mat.iterrows():
        viable = str(r.get("measurement_status", "")).lower() == "viable"
        cell.append(
            [
                str(r.get("label", r.get("feature"))),
                str(r.get("measurement_status", "")),
                _yn(r.get("clears_delta_gate")),
                _yn(r.get("adjusted_sign_aligned")),
                _yn(r.get("adjusted_p_lt_05")),
                _yn(r.get("specification_stable")),
                _yn(viable),
            ]
        )
    table = ax.table(
        cellText=cell,
        colLabels=headers,
        loc="center",
        cellLoc="center",
        colColours=["#f0f0f0"] * len(headers),
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.15, 1.7)
    # Left-align construct column
    for i in range(1, len(cell) + 1):
        table[i, 0].set_text_props(ha="left")
    ax.set_title(
        "Evidence matrix: large δ ≠ robust adjusted support",
        pad=16,
        fontsize=14,
    )
    ax.text(
        0.0,
        0.02,
        "H1 primary: unadjusted δ positive, adjusted quality β negative — disagreement is intentional.",
        transform=ax.transAxes,
        fontsize=9,
        color="#555555",
    )
    outs = save_figure(fig, paths.out_dir, "fig05b_component_evidence_matrix")
    return outs, _manifest_row(
        "fig05b",
        "Component evidence matrix",
        "main",
        ["component_effects", "primary_h1_h6_table", "robustness_traffic_light"],
        "clears_delta_gate; adjusted_*; specification_stable",
        "confirmatory_component",
        "Exposes H1 adj. disagreement; danger quality n.s.",
        outs,
    )


def fig06_attention_shift(paths: PresentationPaths) -> Tuple[List[Path], Dict]:
    from .evidence_metadata import _read_table

    att = _read_table(paths.table("14_exploratory_presentation_results", "attention_waterfall"))
    apply_theme()
    order = att.sort_values("diff_pp")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [C_POS if v >= 0 else C_NEG for v in order["diff_pp"]]
    ax.barh(order["label"], order["diff_pp"], color=colors, edgecolor="none")
    ax.axvline(0, color="#666666", lw=1)
    for _, r in order.iterrows():
        x = r["diff_pp"]
        if x >= 0:
            ax.text(x + 0.012, r["label"], f"{x:+.3f} pp", va="center", ha="left", fontsize=10)
        else:
            ax.text(x - 0.012, r["label"], f"{x:+.3f} pp", va="center", ha="right", fontsize=10, color="#333333")
    ax.set_xlabel("Mean share difference (higher-rated − comparison), percentage points")
    ax.set_title("Diverging attention-shift plot")
    ax.text(
        0.0,
        1.02,
        "Exploratory association with higher ratings — not a causal effect",
        transform=ax.transAxes,
        fontsize=10,
        color=C_EXPL,
        fontweight="bold",
    )
    # Extra left margin so negative direct-labels do not collide with y tick labels
    xmin, xmax = float(order["diff_pp"].min()), float(order["diff_pp"].max())
    pad = 0.12
    ax.set_xlim(xmin - pad, xmax + pad)
    fig.subplots_adjust(left=0.28)
    outs = save_figure(fig, paths.out_dir, "fig06_attention_shift")
    return outs, _manifest_row(
        "fig06",
        "Attention-shift diverging bars",
        "main",
        ["attention_waterfall"],
        "diff_pp",
        "exploratory",
        "",
        outs,
    )


def build_main_figures(
    paths: PresentationPaths | None = None,
    frames: Dict[str, pd.DataFrame] | None = None,
) -> Tuple[List[Dict], Dict[str, pd.DataFrame]]:
    paths = paths or default_paths()
    frames = frames or build_all_metadata(paths, write=True)
    agreement = frames["presentation_agreement"]
    primary = frames["presentation_primary_results"]
    components = frames["presentation_component_results"]
    manifest: List[Dict] = []
    for fn, args in (
        (fig01_contextual_agreement, (paths, agreement)),
        (fig02_measurement_status, (paths, primary)),
        (fig03_primary_verdicts, (paths, primary)),
        (fig04_stage10_stage11_transition, (paths, primary)),
        (fig05_component_effects, (paths, components)),
        (fig05b_component_evidence_matrix, (paths, components, primary)),
        (fig06_attention_shift, (paths,)),
    ):
        _, row = fn(*args)
        manifest.append(row)
    return manifest, frames
