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
    set_title_with_subtitle,
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
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    y = np.arange(len(agreement))[::-1]
    pct = agreement["agreement_pct"].to_numpy()
    ax.hlines(y, 0, pct, color="#56B4E9", lw=2)
    ax.scatter(pct, y, color=C_POS, s=70, zorder=3)
    for yi, row in zip(y, agreement.itertuples()):
        ax.text(row.agreement_pct + 1.5, yi, row.label, va="center", fontsize=11, color=C_NEUTRAL)
    ax.set_yticks(y)
    ax.set_yticklabels(agreement["hypothesis"])
    ax.set_xlim(0, 78)
    ax.set_xlabel("Lexical–contextual agreement (%)")
    set_title_with_subtitle(
        ax,
        "Contextual coding often diverged from lexical cues (H1–H6)",
        "Agreement = Pass A (lexical) matches Pass B (contextual) topic codes",
    )
    fig.subplots_adjust(top=0.82)
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
    fig, ax = plt.subplots(figsize=(14.5, 5.2))
    ax.axis("off")
    cols = ["Hypothesis", "Status", "Topics", "Note"]
    col_widths = [0.10, 0.16, 0.18, 0.56]
    cell_text = []
    colors = []
    for _, r in primary.iterrows():
        st = str(r["measurement_status"])
        sym = status_symbol(st)
        note = str(r["measurement_note"])
        # Soft wrap long notes so table cells do not clip
        if len(note) > 52:
            parts, line, n = [], [], 0
            for w in note.split():
                if n + len(w) + 1 > 52 and line:
                    parts.append(" ".join(line))
                    line, n = [w], len(w)
                else:
                    line.append(w)
                    n += len(w) + 1
            if line:
                parts.append(" ".join(line))
            note = "\n".join(parts)
        cell_text.append(
            [
                r["hypothesis"],
                f"{sym} {st.capitalize()}",
                r["n_topics_display"],
                note,
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
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 2.35)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#cccccc")
        if c == 3:
            cell.set_text_props(ha="left", va="center")
        if r == 0:
            cell.set_text_props(fontweight="bold")
            cell.set_height(0.08)
    ax.set_title(
        "Could H1–H6 still be measured after contextual refinement?",
        pad=22,
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
        figsize=(13.5, 6.2),
        gridspec_kw={"width_ratios": [0.55, 1.35, 3.4, 1.35], "wspace": 0.08},
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
        ax_h.text(0.0, yi, r.hypothesis, ha="left", va="center", fontsize=13, fontweight="bold")
        ax_m.text(0.02, yi, f"{status_symbol(st)}  {st}", ha="left", va="center", fontsize=11, color="#444444")
        ax_v.text(0.02, yi, str(r.verdict), ha="left", va="center", fontsize=11, color=C_NEUTRAL)
        if st == "unmeasurable" or pd.isna(r.effect_size):
            ax_e.text(
                0.02,
                yi,
                "Unmeasurable after refinement",
                va="center",
                ha="left",
                fontsize=10,
                color=C_UNMEAS,
                style="italic",
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#e8e8e8", alpha=1.0),
            )
        else:
            lo, hi, est = r.ci_low, r.ci_high, r.effect_size
            ax_e.plot([lo, hi], [yi, yi], color=C_NEUTRAL, lw=1.8, zorder=2)
            mk = marker_for_gate(st)
            ax_e.scatter([est], [yi], zorder=3, **mk)

    gate_lines(ax_e, orientation="vertical")
    ax_e.set_yticks(y)
    ax_e.set_yticklabels([])
    ax_e.set_xlim(-0.22, 0.24)
    ax_e.set_xlabel("Cliff's δ (high − low rating tiers)")
    header_y = len(primary) - 0.28
    ax_h.text(0.0, header_y, "Hyp.", fontsize=10, color="#666666")
    ax_m.text(0.02, header_y, "Measurement", fontsize=10, color="#666666")
    ax_v.text(0.02, header_y, "Verdict", fontsize=10, color="#666666")
    ax_e.set_ylim(-0.7, len(primary) - 0.05)

    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=C_POS, markersize=9, label="Viable"),
        Line2D([0], [0], marker="o", color=C_POS, markerfacecolor="none", markersize=9, label="Thin"),
    ]
    ax_e.legend(handles=legend, loc="upper right", frameon=True, framealpha=0.95, edgecolor="#dddddd")
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
    fig.subplots_adjust(top=0.90, bottom=0.12, left=0.04, right=0.98)
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
    from matplotlib.patches import ConnectionPatch

    primary = primary if primary is not None else load_primaries(paths)
    apply_theme()
    fig, (ax_d, ax_m) = plt.subplots(
        1,
        2,
        figsize=(12.5, 6.8),
        gridspec_kw={"width_ratios": [3.2, 1.35], "wspace": 0.08},
    )
    x0, x1 = 0.0, 1.0

    # Stage-10 left labels: explicit stagger for the dense H5/H6/H2 cluster
    left_offsets: Dict[str, float] = {
        "H5": -0.018,
        "H6": 0.0,
        "H2": 0.018,
        "H1": 0.0,
        "H3": 0.0,
        "H4": 0.0,
    }

    # Stage-11 right labels: larger offsets for near-ties (H1≈H4, H5≈H6)
    right_offsets = {"H1": 0.028, "H4": -0.028, "H5": 0.022, "H6": -0.022}

    # Right panel: categorical slots (independent of Cliff's δ)
    # Ordinal category positions in axes fraction of the right panel
    cat_frac = {"H2": 0.62, "H3": 0.38}
    # Include Stage-10 H3 (δ≈−0.146); keep band clear of measurable Stage-11 range
    y_lo, y_hi = -0.18, 0.22

    def _frac_to_y(frac: float) -> float:
        return y_lo + frac * (y_hi - y_lo)

    for r in primary.itertuples():
        ax_d.scatter([x0], [r.stage10_delta], color="#999999", s=55, zorder=3)
        ax_d.text(
            x0 - 0.07,
            r.stage10_delta + left_offsets.get(r.hypothesis, 0.0),
            r.hypothesis,
            ha="right",
            va="center",
            fontsize=10,
        )
        if str(r.measurement_status) == "unmeasurable" or pd.isna(r.stage11_delta):
            y_cat = _frac_to_y(cat_frac[r.hypothesis])
            ax_m.scatter([0.5], [y_cat], marker="s", color=C_UNMEAS, s=90, zorder=3)
            ax_m.text(
                0.58,
                y_cat,
                r.hypothesis,
                va="center",
                ha="left",
                fontsize=10,
                color=C_UNMEAS,
                fontweight="bold",
            )
            con = ConnectionPatch(
                xyA=(x0, r.stage10_delta),
                coordsA=ax_d.transData,
                xyB=(0.5, y_cat),
                coordsB=ax_m.transData,
                arrowstyle="->",
                color=C_UNMEAS,
                lw=1.4,
                connectionstyle="arc3,rad=0.05",
            )
            fig.add_artist(con)
        else:
            ax_d.plot([x0, x1], [r.stage10_delta, r.stage11_delta], color="#56B4E9", lw=1.5, zorder=2)
            mk = marker_for_gate(str(r.measurement_status))
            ax_d.scatter([x1], [r.stage11_delta], zorder=3, **mk)
            dy = right_offsets.get(r.hypothesis, 0.0)
            ax_d.annotate(
                r.hypothesis,
                xy=(x1, r.stage11_delta),
                xytext=(x1 + 0.14, r.stage11_delta + dy),
                va="center",
                fontsize=10,
                arrowprops=dict(arrowstyle="-", color="#bbbbbb", lw=0.8)
                if abs(dy) > 0.01
                else None,
            )

    gate_lines(ax_d, orientation="horizontal")
    ax_d.set_xticks([x0, x1])
    ax_d.set_xticklabels(["Stage 10\n(original δ)", "Stage 11\n(refined δ)"])
    ax_d.set_ylabel("Cliff's δ")
    ax_d.set_xlim(-0.45, 1.55)
    ax_d.set_ylim(y_lo, y_hi)
    ax_d.set_title("Effect-size transition", fontsize=11, pad=8)

    ax_m.set_xlim(0.0, 1.15)
    ax_m.set_ylim(y_lo, y_hi)
    ax_m.set_xticks([0.5])
    ax_m.set_xticklabels(["Measurement\noutcome"])
    ax_m.set_yticks([])
    ax_m.spines["left"].set_visible(False)
    ax_m.spines["right"].set_visible(False)
    ax_m.spines["top"].set_visible(False)
    ax_m.set_title("Measurement outcome", fontsize=11, pad=8)
    # Category band label (not on the δ axis)
    ax_m.text(
        0.5,
        _frac_to_y(0.88),
        "Unmeasurable\nafter refinement",
        ha="center",
        va="center",
        fontsize=9,
        color=C_UNMEAS,
        style="italic",
    )
    # Light band behind category markers only (right panel; not δ scale)
    band_lo = _frac_to_y(0.28)
    band_hi = _frac_to_y(0.72)
    ax_m.axhspan(band_lo, band_hi, color="#f3f3f3", zorder=0)

    fig.suptitle(
        "Contextual refinement changed both effect estimates and measurability",
        fontsize=13,
        y=0.98,
    )
    fig.text(
        0.5,
        0.01,
        "H2/H3 terminate in the Measurement outcome panel (categorical; not a Cliff's δ).",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    fig.subplots_adjust(top=0.88, bottom=0.12, left=0.08, right=0.96)
    outs = save_figure(fig, paths.out_dir, "fig04_stage10_stage11_transition")
    return outs, _manifest_row(
        "fig04",
        "Stage 10 → Stage 11 transition",
        "main",
        ["stage10_vs_final_side_by_side"],
        "original_delta; refined_delta",
        "confirmatory",
        "H2/H3 endpoint is categorical Measurement outcome, not δ=0",
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
    fig, ax = plt.subplots(figsize=(11, 7.0))
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
    set_title_with_subtitle(
        ax,
        "Component-level associations (not parent-hypothesis confirmation)",
        f"Open markers = thin measurement; dashed |δ|={EFFECT_GATE:g} gate",
    )
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
    ax.legend(handles=legend, loc="lower right", frameon=True, framealpha=0.95, edgecolor="#dddddd")
    ax.set_ylim(-0.8, len(df) - 0.2)
    fig.subplots_adjust(left=0.34, top=0.82)
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
    fig, ax = plt.subplots(figsize=(15.5, 7.4))
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
    col_widths = [0.34, 0.10, 0.10, 0.12, 0.12, 0.11, 0.11]
    cell = []
    for _, r in mat.iterrows():
        viable = str(r.get("measurement_status", "")).lower() == "viable"
        label = str(r.get("label", r.get("feature")))
        cell.append(
            [
                label,
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
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.85)
    # Left-align construct column; ensure wrapping room
    for (r, c), cell_obj in table.get_celld().items():
        cell_obj.set_edgecolor("#cccccc")
        if c == 0 and r > 0:
            cell_obj.set_text_props(ha="left")
            cell_obj.PAD = 0.04
        if r == 0:
            cell_obj.set_text_props(fontweight="bold", va="center")
            cell_obj.set_height(0.09)
    ax.set_title(
        "Evidence matrix: large δ ≠ robust adjusted support",
        pad=20,
        fontsize=14,
    )
    fig.text(
        0.5,
        0.03,
        "H1 primary: unadjusted δ positive, adjusted quality β negative — disagreement is intentional.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    fig.subplots_adjust(bottom=0.10, top=0.90)
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
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    colors = [C_POS if v >= 0 else C_NEG for v in order["diff_pp"]]
    ax.barh(order["label"], order["diff_pp"], color=colors, edgecolor="none")
    ax.axvline(0, color="#666666", lw=1)
    for _, r in order.iterrows():
        x = r["diff_pp"]
        # Near-zero values: park labels to the right of zero to avoid axis collision
        if abs(x) < 0.02:
            ax.text(0.055, r["label"], f"{x:+.3f} pp", va="center", ha="left", fontsize=10, color="#333333")
        elif x >= 0:
            ax.text(x + 0.012, r["label"], f"{x:+.3f} pp", va="center", ha="left", fontsize=10)
        else:
            ax.text(x - 0.012, r["label"], f"{x:+.3f} pp", va="center", ha="right", fontsize=10, color="#333333")
    ax.set_xlabel("Mean share difference (higher-rated − comparison), percentage points")
    set_title_with_subtitle(
        ax,
        "Diverging attention-shift plot",
        "Exploratory association with higher ratings — not a causal effect",
        subtitle_color=C_EXPL,
        subtitle_weight="bold",
    )
    # Extra left margin so negative direct-labels do not collide with y tick labels
    xmin, xmax = float(order["diff_pp"].min()), float(order["diff_pp"].max())
    pad = 0.14
    ax.set_xlim(xmin - pad, xmax + pad)
    fig.subplots_adjust(left=0.30, top=0.82)
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
