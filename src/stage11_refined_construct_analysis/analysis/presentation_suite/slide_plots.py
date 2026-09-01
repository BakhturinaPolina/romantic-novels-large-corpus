"""Storyboard-aligned slide plot functions (v2 deck)."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Literal, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from .plot_helpers import apply_categorical_y_axis, categorical_ylim, categorical_y_positions
from .paths import PresentationPaths, default_paths
from .theme import (
    AXIS_LABEL,
    C_EXPL,
    C_GATE,
    C_NEG,
    C_NEUTRAL,
    C_POS,
    C_SELECTED,
    C_THIN,
    C_UNMEAS,
    EFFECT_GATE,
    HYPOTHESIS_ORDER,
    PANEL_TITLE,
    PresentationMode,
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
    resolve_output_dir,
    save_figure,
    set_title_with_subtitle,
    status_symbol,
)

FOCAL_COMPONENTS = {
    "RAX_emotional_reassurance",
    "RAX_tenderness_core",
    "RAX_appearance_grooming",
}

S08_XLIM = (-0.22, 0.22)
S08_FIGSIZE = (10.5, 6.2)


def _manifest_row(
    figure_id: str,
    slide_id: str,
    figure_name: str,
    level: str,
    sources: Sequence[str],
    measure: str,
    evidence: str,
    warning: str,
    paths: List[Path],
    *,
    render_target: str = "matplotlib",
) -> Dict:
    return {
        "figure_id": figure_id,
        "slide_id": slide_id,
        "figure_name": figure_name,
        "presentation_level": level,
        "notebook_source": "; ".join(sources),
        "table_source": "; ".join(sources),
        "variables_used": measure,
        "statistical_measure": measure,
        "confirmatory_or_exploratory": evidence,
        "measurement_warning": warning,
        "render_target": render_target,
        "output_path": str(paths[0]) if paths else "",
        "output_svg": str(paths[1]) if len(paths) > 1 else "",
        "output_pdf": str(paths[2]) if len(paths) > 2 else "",
    }


def _save_both_modes(
    fig: plt.Figure,
    paths: PresentationPaths,
    stem: str,
    *,
    fixed_canvas: bool = False,
    close: bool = True,
) -> Tuple[List[Path], List[Path]]:
    """Save chart_only to deck figures and review copy to review/figures."""
    chart_paths = save_figure(
        fig, resolve_output_dir(paths, "chart_only"), stem, close=False, fixed_canvas=fixed_canvas
    )
    review_paths = save_figure(
        fig, resolve_output_dir(paths, "review"), stem, close=close, fixed_canvas=fixed_canvas
    )
    return chart_paths, review_paths


def plot_component_effects_presentation(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide08_component_effects",
    mode: PresentationMode = "review",
    fixed_ylim: Tuple[float, float] | None = None,
    highlight_focal: bool = True,
    save: bool = True,
    out_dir: Path | None = None,
) -> Tuple[List[Path], Dict]:
    apply_theme()
    n = len(df)
    fig, ax = plt.subplots(figsize=S08_FIGSIZE, layout="constrained")
    gate_band(ax, orientation="vertical")
    gate_lines(ax, orientation="vertical")

    y = categorical_y_positions(n)
    labels = df["display_label"].fillna(df["label"]).tolist()
    for yi, row in zip(y, df.itertuples()):
        est = row.effect_size
        lo, hi = row.ci_low, row.ci_high
        is_focal = highlight_focal and str(row.feature) in FOCAL_COMPONENTS
        mk = marker_for_gate(str(row.measurement_status))
        color = C_NEUTRAL if (highlight_focal and not is_focal) else C_NEUTRAL
        ax.errorbar(est, yi, xerr=[[est - lo], [hi - est]], fmt="none", color=color, capsize=3, lw=1.2, zorder=2)
        if is_focal and mk.get("facecolors") == C_POS:
            mk = {**mk, "s": 110, "zorder": 4}
        zorder = mk.pop("zorder", 3)
        ax.scatter([est], [yi], **mk, zorder=zorder)
        ax.text(hi + 0.012, yi, format_delta(est), va="center", fontsize=VALUE_LABEL, color=C_NEUTRAL)

    apply_categorical_y_axis(ax, y, labels)
    ax.set_xlabel("Cliff's δ (high-rated − low-rated)", fontsize=AXIS_LABEL)
    ax.set_xlim(*S08_XLIM)
    if fixed_ylim is not None:
        ax.set_ylim(*fixed_ylim)
    apply_presentation_context(
        ax,
        mode=mode,
        title="Specific narrative functions reveal clearer differences",
        subtitle="Confirmatory component effects; shaded band = below prespecified |δ| = 0.11 gate",
    )
    if mode == "review":
        ax.text(0.5, -0.14, "← lower in highly rated", transform=ax.transAxes, ha="center", fontsize=11, color="#666")
        ax.text(0.5, -0.18, "higher in highly rated →", transform=ax.transAxes, ha="center", fontsize=11, color="#666")

    if not save:
        plt.close(fig)
        return [], _manifest_row(stem, "S08", "Component effects", "main", [], "", "", "", [])

    target = out_dir or resolve_output_dir(paths, mode)
    outs = save_figure(fig, target, stem, fixed_canvas=fixed_ylim is not None)
    return outs, _manifest_row(
        stem,
        "S08",
        "Component effects (presentation)",
        "main",
        ["presentation_component_results.csv"],
        "Cliff's δ + 95% CI",
        "confirmatory_component",
        "Open marker = thin measurement; components ≠ parent H confirmation",
        outs,
    )


def plot_context_and_measurement(
    agreement: pd.DataFrame,
    primary: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide06_context_measurement",
    mode: PresentationMode = "review",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig = plt.figure(figsize=(12.5, 5.8), layout="constrained")
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    y = categorical_y_positions(len(agreement))
    pct = agreement["agreement_pct"].to_numpy()
    ax1.barh(y, pct, color=C_POS, height=0.55, alpha=0.85)
    for yi, p in zip(y, pct):
        ax1.text(p + 1.2, yi, f"{p:.0f}%", va="center", fontsize=VALUE_LABEL, fontweight="bold")
    apply_categorical_y_axis(ax1, y, agreement["hypothesis"].tolist())
    ax1.set_xlim(0, 65)
    ax1.set_xlabel("Lexical–contextual agreement (%)", fontsize=AXIS_LABEL)
    ax1.set_title("Contextual agreement", fontsize=PANEL_TITLE, loc="left", fontweight="bold")
    ax1.set_xticks([0, 25, 50])

    ax2.axis("off")
    ax2.set_title("Measurement after refinement", fontsize=PANEL_TITLE, loc="left", fontweight="bold", pad=12)
    for i, h in enumerate(HYPOTHESIS_ORDER):
        row = primary.loc[primary["hypothesis"] == h].iloc[0]
        st = str(row["measurement_status"])
        sym = status_symbol(st)
        ypos = 0.88 - i * 0.14
        emphasize = h in ("H2", "H3")
        fw = "bold" if emphasize else "normal"
        ax2.text(0.05, ypos, h, transform=ax2.transAxes, fontsize=TICK_TEXT, fontweight=fw, va="center")
        ax2.text(
            0.22,
            ypos,
            f"{sym} {st.capitalize()}",
            transform=ax2.transAxes,
            fontsize=TICK_TEXT,
            color=C_NEUTRAL if st != "unmeasurable" else C_UNMEAS,
            fontweight=fw,
            va="center",
        )

    if mode == "review":
        fig.suptitle(
            "Context changed what the topics actually meant",
            fontsize=PANEL_TITLE,
            fontweight="bold",
            x=0.02,
            ha="left",
        )
        fig.text(0.5, 0.02, "Lexical similarity ≠ narrative function", ha="center", fontsize=TICK_TEXT, color=C_NEUTRAL)

    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, stem)
    return outs, _manifest_row(
        stem,
        "S06",
        "Context + measurement combined",
        "main",
        ["presentation_agreement.csv", "presentation_primary_results.csv"],
        "agreement_pct; measurement_status",
        "methodological",
        "H2/H3 unmeasurable — not plotted at δ=0",
        outs,
    )


def plot_primary_verdict_cards(
    primary: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide07_primary_verdict_preview",
    mode: PresentationMode = "review",
) -> Tuple[List[Path], Dict]:
    """Minimal text-table preview; canonical layout is Figma-native."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(12.5, 4.0), layout="constrained")
    ax.axis("off")
    rows = []
    for h in HYPOTHESIS_ORDER:
        row = primary.loc[primary["hypothesis"] == h].iloc[0]
        st = str(row["measurement_status"])
        if st == "unmeasurable":
            delta = "NOT MEASURABLE"
        else:
            delta = format_delta(row["effect_size"])
        rows.append([h, str(row["label"])[:35], st, str(row["verdict"]), delta])
    table = ax.table(
        cellText=rows,
        colLabels=["H", "Construct", "Measurement", "Verdict", "δ"],
        loc="center",
        cellLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(TICK_TEXT)
    table.scale(1.0, 1.8)
    if mode == "review":
        fig.suptitle(
            "H1–H6 primary verdicts (preview — layout in Figma)",
            fontsize=PANEL_TITLE,
            fontweight="bold",
            x=0.02,
            ha="left",
        )
    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, stem)
    return outs, _manifest_row(
        stem,
        "S07",
        "H1–H6 verdict cards (preview)",
        "main",
        ["presentation_primary_results.csv"],
        "Cliff's δ; verdict; measurement_status",
        "confirmatory",
        "H2/H3 categorical unmeasurable; not null at zero",
        outs,
        render_target="figma_native",
    )


def plot_quality_reach_dumbbell(
    df: pd.DataFrame,
    catalog_full: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide10_quality_reach_dumbbell",
    mode: PresentationMode = "review",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    plot_df = df.copy()
    if "delta_gap" not in plot_df.columns:
        plot_df["delta_gap"] = plot_df["quality_delta"] - plot_df["reach_delta"]
    plot_df = plot_df.sort_values("delta_gap", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(11, 6), layout="constrained")
    n_both = int(
        (
            catalog_full.loc[catalog_full["analysis_resolution"] == "taxonomy_leaf"]["quality_gate"].astype(bool)
            & catalog_full.loc[catalog_full["analysis_resolution"] == "taxonomy_leaf"]["reach_gate"].astype(bool)
        ).sum()
    )
    y = categorical_y_positions(len(plot_df))
    for yi, row in zip(y, plot_df.itertuples()):
        qd, rd = row.quality_delta, row.reach_delta
        ax.scatter([qd], [yi], marker="o", s=80, color=C_POS, zorder=3)
        ax.scatter([rd], [yi], marker="s", s=70, color=C_NEG, zorder=3)
        ax.plot([qd, rd], [yi, yi], color="#aaaaaa", lw=1.5, zorder=2)
    ax.axvline(0, color="#888", lw=0.8)
    ax.axvline(EFFECT_GATE, color=C_GATE, ls="--", lw=0.8, alpha=0.7)
    ax.axvline(-EFFECT_GATE, color=C_GATE, ls="--", lw=0.8, alpha=0.7)
    labels = plot_df["short_label"].fillna(plot_df["label"]).tolist()
    apply_categorical_y_axis(ax, y, labels)
    ax.set_xlabel("Cliff's δ (high-rated or high-reach − comparison)", fontsize=AXIS_LABEL)
    apply_presentation_context(
        ax,
        mode=mode,
        title="What makes a book widely read is not what makes it highly rated",
        subtitle="Taxonomy-leaf contrasts; ● quality  ■ reach",
        exploratory=True,
    )
    if mode == "chart_only":
        ax.text(0.02, 0.98, "● QUALITY    ■ REACH", transform=ax.transAxes, fontsize=VALUE_LABEL, va="top", color=C_NEUTRAL)
    elif mode == "review":
        ax.text(
            0.02,
            0.02,
            f"{n_both} leaves cleared the effect gate on both outcomes",
            transform=ax.transAxes,
            fontsize=VALUE_LABEL,
            fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="#f5f5f5", edgecolor=C_NEUTRAL),
        )
    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, stem)
    return outs, _manifest_row(
        stem,
        "S10",
        "Quality vs reach dumbbell",
        "main",
        ["leaf_deltas_both_tierings.csv"],
        "delta_rating; delta_reach",
        "exploratory",
        "Reach ≠ causal marketing; compositional/exploratory framing",
        outs,
    )


def plot_richness_evidence_sequence(
    story: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide11_richness_preview",
    mode: PresentationMode = "review",
) -> Tuple[List[Path], Dict]:
    """Minimal CSV preview; canonical layout is Figma-native."""
    apply_theme()
    fig, ax = plt.subplots(figsize=(12.5, 3.5), layout="constrained")
    ax.axis("off")
    rows = []
    for analysis in ("raw_taxonomy_delta", "raw_topic_delta", "rarefied_taxonomy", "controlled_plus_drivers"):
        match = story.loc[story["analysis"] == analysis]
        if match.empty:
            continue
        r = match.iloc[0]
        rows.append([analysis.replace("_", " "), str(r.get("metric", "")), f"{r.get('estimate', '—')}", f"{r.get('p_value', '—')}"])
    table = ax.table(
        cellText=rows,
        colLabels=["Stage", "Metric", "Estimate", "p"],
        loc="center",
        cellLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(TICK_TEXT)
    table.scale(1.0, 1.6)
    if mode == "review":
        fig.suptitle(
            "Richness evidence sequence (preview — layout in Figma)",
            fontsize=PANEL_TITLE,
            fontweight="bold",
            x=0.02,
            ha="left",
        )
        exploratory_tag(ax)
    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, stem)
    return outs, _manifest_row(
        stem,
        "S11",
        "Richness three-stage evidence (preview)",
        "main",
        ["thematic_richness_cliffs_delta", "thematic_richness_ols", "thematic_richness_vs_drivers"],
        "Cliff's δ; OLS β",
        "exploratory",
        "Rarefaction removes raw association; suppression after drivers",
        outs,
        render_target="figma_native",
    )


def plot_attention_shift_short(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide09_attention_shift",
    mode: PresentationMode = "review",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, ax = plt.subplots(figsize=(10, 5.5), layout="constrained")
    y = categorical_y_positions(len(df))
    vals = df["diff_pp"].to_numpy()
    colors = [C_POS if v > 0 else C_NEG for v in vals]
    ax.barh(y, vals, color=colors, height=0.55, alpha=0.85)
    for yi, v in zip(y, vals):
        ax.text(
            v + (0.02 if v >= 0 else -0.02),
            yi,
            format_pp(v),
            va="center",
            ha="left" if v >= 0 else "right",
            fontsize=VALUE_LABEL,
        )
    labels = df["display_label"].fillna(df["label"]).tolist()
    apply_categorical_y_axis(ax, y, labels)
    ax.axvline(0, color="#888", lw=0.8)
    ax.set_xlabel("Mean share difference (percentage points), high-rated − low-rated", fontsize=AXIS_LABEL)
    apply_presentation_context(
        ax,
        mode=mode,
        title="Higher-rated romances devote relatively more space to tenderness",
        subtitle="Exploratory compositional shift — not causal",
        exploratory=True,
    )
    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, stem)
    return outs, _manifest_row(
        stem,
        "S09",
        "Attention allocation shift",
        "main",
        ["attention_waterfall.parquet"],
        "diff_pp compositional",
        "exploratory",
        "Shares are compositional; not causal",
        outs,
    )


def plot_pareto_selection(
    trials: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide04_pareto_selection",
    mode: PresentationMode = "review",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, ax = plt.subplots(figsize=(9, 6.5), layout="constrained")
    invalid = trials.loc[trials.get("valid", True) == False] if "valid" in trials.columns else pd.DataFrame()
    all_pts = trials[~trials["pareto_efficient"]]
    pareto_pts = trials[trials["pareto_efficient"] & ~trials["is_selected"]]
    selected = trials[trials["is_selected"]]
    if not invalid.empty and "topic_diversity" in invalid.columns:
        ax.scatter(
            invalid["topic_diversity"],
            invalid["coherence_c_v"],
            s=8,
            c="#dddddd",
            alpha=0.3,
            zorder=0,
        )
    ax.scatter(all_pts["topic_diversity"], all_pts["coherence_c_v"], s=12, c="#bbbbbb", alpha=0.5, zorder=1)
    ax.scatter(pareto_pts["topic_diversity"], pareto_pts["coherence_c_v"], s=40, c=C_NEUTRAL, alpha=0.6, zorder=2)
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
        ax.annotate(
            "Selected",
            (selected.iloc[0]["topic_diversity"], selected.iloc[0]["coherence_c_v"]),
            xytext=(12, 12),
            textcoords="offset points",
            fontsize=VALUE_LABEL,
            arrowprops=dict(arrowstyle="->", color=C_NEUTRAL),
        )
    ax.set_xlabel("Topic diversity", fontsize=AXIS_LABEL)
    ax.set_ylabel("Coherence (c_v)", fontsize=AXIS_LABEL)
    apply_presentation_context(
        ax,
        mode=mode,
        title="The final topic model was chosen as a trade-off, not by one metric",
        subtitle=f"Bayesian optimization over {len(trials)} configurations",
    )
    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, stem)
    return outs, _manifest_row(
        stem,
        "S04",
        "Pareto model selection",
        "main",
        ["trials.csv"],
        "coherence_c_v vs topic_diversity",
        "methodological",
        "",
        outs,
    )


def plot_ees_integrated_short(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide12_ees_integrated",
    mode: PresentationMode = "review",
    layout: Literal["integrated", "three_panel"] = "integrated",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    if layout == "three_panel":
        return _plot_ees_three_panel(df, paths, stem=stem, mode=mode)
    return _plot_ees_integrated_forest(df, paths, stem=stem, mode=mode)


def _plot_ees_integrated_forest(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str,
    mode: PresentationMode,
) -> Tuple[List[Path], Dict]:
    domain_order = ["emotion", "embodiment", "social"]
    domain_labels = {"emotion": "EMOTION", "embodiment": "EMBODIMENT", "social": "SOCIAL WORLD"}
    rows: List[pd.Series] = []
    for domain in domain_order:
        sub = df.loc[df["domain"] == domain]
        if sub.empty:
            continue
        header = pd.Series({"domain": domain, "display_label": domain_labels[domain], "is_header": True})
        rows.append(header)
        for _, r in sub.iterrows():
            r = r.copy()
            r["is_header"] = False
            rows.append(r)
    plot_df = pd.DataFrame(rows).reset_index(drop=True)
    plot_rows = plot_df.loc[~plot_df.get("is_header", False)].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(11, 7.5), layout="constrained")
    gate_band(ax, orientation="vertical")
    gate_lines(ax, orientation="vertical")

    y_positions: List[float] = []
    y_labels: List[str] = []
    y_idx = 0
    for _, row in plot_df.iterrows():
        if row.get("is_header"):
            y_positions.append(y_idx)
            y_labels.append(str(row["display_label"]))
            y_idx += 1.2
            continue
        y_positions.append(y_idx)
        y_labels.append(str(row.get("display_label", row.get("construct", ""))))
        est, lo, hi = row["cliffs_delta"], row["ci_low"], row["ci_high"]
        mk = marker_for_gate("thin" if str(row.get("status", "")) == "thin" else "viable")
        ax.errorbar(est, y_idx, xerr=[[est - lo], [hi - est]], fmt="none", color=C_NEUTRAL, capsize=2, lw=1)
        ax.scatter([est], [y_idx], **mk, zorder=3)
        y_idx += 1

    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=TICK_TEXT)
    for i, lbl in enumerate(ax.get_yticklabels()):
        if lbl.get_text() in domain_labels.values():
            lbl.set_fontweight("bold")
            lbl.set_fontsize(PANEL_TITLE)
    ax.invert_yaxis()
    ax.set_xlim(-0.25, 0.25)
    ax.set_xlabel("Cliff's δ", fontsize=AXIS_LABEL)
    apply_presentation_context(
        ax,
        mode=mode,
        title="The exploratory extension shifts the question from topics to narrative experience",
        subtitle="Exploratory, frozen coding — does not change H1–H6 verdicts",
        exploratory=True,
    )
    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, stem)
    return outs, _manifest_row(
        stem,
        "S12",
        "EES integrated forest",
        "main",
        ["emotion_effects", "embodiment_effects", "family_social_effects"],
        "Cliff's δ",
        "exploratory",
        "Frozen LLM coding + human overrides; not confirmatory",
        outs,
    )


def _plot_ees_three_panel(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str,
    mode: PresentationMode,
) -> Tuple[List[Path], Dict]:
    domains = ["emotion", "embodiment", "social"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.5), sharex=True, layout="constrained")
    for ax, domain in zip(axes, domains):
        sub = df.loc[df["domain"] == domain]
        if sub.empty:
            ax.set_visible(False)
            continue
        y = categorical_y_positions(len(sub))
        gate_band(ax, orientation="vertical")
        gate_lines(ax, orientation="vertical")
        for yi, row in zip(y, sub.itertuples()):
            est, lo, hi = row.cliffs_delta, row.ci_low, row.ci_high
            mk = marker_for_gate("thin" if str(row.status) == "thin" else "viable")
            ax.errorbar(est, yi, xerr=[[est - lo], [hi - est]], fmt="none", color=C_NEUTRAL, capsize=2, lw=1)
            ax.scatter([est], [yi], **mk, zorder=3)
        labels = sub["display_label"].fillna(sub["construct"]).tolist()
        apply_categorical_y_axis(ax, y, labels)
        ax.set_title(domain.upper(), fontsize=PANEL_TITLE, fontweight="bold", loc="left")
        ax.set_xlim(-0.25, 0.25)
    axes[1].set_xlabel("Cliff's δ", fontsize=AXIS_LABEL)
    if mode == "review":
        fig.suptitle(
            "EES three-panel (appendix layout)",
            fontsize=PANEL_TITLE,
            fontweight="bold",
            x=0.02,
            ha="left",
        )
    out_dir = resolve_output_dir(paths, mode)
    outs = save_figure(fig, out_dir, f"{stem}_three_panel")
    return outs, _manifest_row(
        f"{stem}_three_panel",
        "S12",
        "EES three-panel appendix",
        "appendix",
        ["emotion_effects", "embodiment_effects", "family_social_effects"],
        "Cliff's δ",
        "exploratory",
        "",
        outs,
    )


def export_component_animation_steps(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    mode: PresentationMode = "chart_only",
) -> List[Path]:
    """Export staged slide08 SVGs with fixed canvas dimensions."""
    from .annotations import load_animation_sequence

    seq = load_animation_sequence("S08", paths)
    if seq.empty:
        return []
    fixed_ylim = categorical_ylim(len(df))
    outputs: List[Path] = []
    features = df["feature"].tolist()
    for _, step in seq.iterrows():
        el = str(step["element_id"])
        if el == "axes":
            sub = df.iloc[0:0]
        else:
            idx = features.index(el) + 1 if el in features else len(features)
            sub = df.iloc[:idx]
        stem = f"slide08_step{int(step['step']):02d}_{el}"
        if sub.empty and el == "axes":
            apply_theme()
            fig, ax = plt.subplots(figsize=S08_FIGSIZE, layout="constrained")
            gate_band(ax, orientation="vertical")
            gate_lines(ax, orientation="vertical")
            ax.set_xlim(*S08_XLIM)
            ax.set_ylim(*fixed_ylim)
            ax.set_xlabel("Cliff's δ (high-rated − low-rated)", fontsize=AXIS_LABEL)
            apply_presentation_context(
                ax,
                mode=mode,
                title="Specific narrative functions reveal clearer differences",
                subtitle=f"Step {int(step['step'])}: axes",
            )
            out_dir = resolve_output_dir(paths, mode)
            outputs.extend(save_figure(fig, out_dir, stem, fixed_canvas=True))
        elif not sub.empty:
            outs, _ = plot_component_effects_presentation(
                sub,
                paths,
                stem=stem,
                mode=mode,
                fixed_ylim=fixed_ylim,
                highlight_focal=True,
            )
            # Re-save with fixed canvas
            apply_theme()
            fig, ax = plt.subplots(figsize=S08_FIGSIZE, layout="constrained")
            gate_band(ax, orientation="vertical")
            gate_lines(ax, orientation="vertical")
            y = categorical_y_positions(len(sub))
            labels = sub["display_label"].fillna(sub["label"]).tolist()
            for yi, row in zip(y, sub.itertuples()):
                est, lo, hi = row.effect_size, row.ci_low, row.ci_high
                is_focal = str(row.feature) in FOCAL_COMPONENTS
                mk = marker_for_gate(str(row.measurement_status))
                ax.errorbar(est, yi, xerr=[[est - lo], [hi - est]], fmt="none", color=C_NEUTRAL, capsize=3, lw=1.2, zorder=2)
                if is_focal and mk.get("facecolors") == C_POS:
                    mk = {**mk, "s":  110}
                zorder = mk.pop("zorder", 3) if "zorder" in mk else 3
                ax.scatter([est], [yi], **mk, zorder=zorder)
                ax.text(hi + 0.012, yi, format_delta(est), va="center", fontsize=VALUE_LABEL, color=C_NEUTRAL)
            apply_categorical_y_axis(ax, y, labels)
            ax.set_xlabel("Cliff's δ (high-rated − low-rated)", fontsize=AXIS_LABEL)
            ax.set_xlim(*S08_XLIM)
            ax.set_ylim(*fixed_ylim)
            apply_presentation_context(
                ax,
                mode=mode,
                title="Specific narrative functions reveal clearer differences",
                subtitle="Confirmatory component effects; shaded band = below prespecified |δ| = 0.11 gate",
            )
            out_dir = resolve_output_dir(paths, mode)
            outputs.extend(save_figure(fig, out_dir, stem, fixed_canvas=True))
    return outputs


def build_all_slide_figures(paths: PresentationPaths | None = None) -> List[Dict]:
    from .catalogs import build_all_catalogs, build_quality_reach_catalog
    from .slide_data import (
        prepare_attention_shift,
        prepare_component_effects,
        prepare_context_measurement,
        prepare_ees_integrated,
        prepare_pareto_points,
        prepare_primary_verdicts,
        prepare_quality_reach_dumbbell,
        prepare_richness_evidence,
    )

    paths = paths or default_paths()
    paths.ensure_deck_dirs()
    build_all_catalogs(paths, write=True)

    manifest: List[Dict] = []

    trials = prepare_pareto_points(paths)
    for mode in ("chart_only", "review"):
        _, row = plot_pareto_selection(trials, paths, mode=mode)  # type: ignore[arg-type]
    manifest.append(plot_pareto_selection(trials, paths, mode="chart_only")[1])

    ctx = prepare_context_measurement(paths)
    for mode in ("chart_only", "review"):
        plot_context_and_measurement(ctx["agreement"], ctx["primary"], paths, mode=mode)  # type: ignore[arg-type]
    manifest.append(plot_context_and_measurement(ctx["agreement"], ctx["primary"], paths, mode="chart_only")[1])

    primary = prepare_primary_verdicts(paths)
    for mode in ("chart_only", "review"):
        plot_primary_verdict_cards(primary, paths, mode=mode)  # type: ignore[arg-type]
    manifest.append(plot_primary_verdict_cards(primary, paths, mode="chart_only")[1])

    comp = prepare_component_effects(paths)
    for mode in ("chart_only", "review"):
        plot_component_effects_presentation(comp, paths, mode=mode)  # type: ignore[arg-type]
    manifest.append(plot_component_effects_presentation(comp, paths, mode="chart_only")[1])
    export_component_animation_steps(comp, paths, mode="chart_only")

    att = prepare_attention_shift(paths)
    for mode in ("chart_only", "review"):
        plot_attention_shift_short(att, paths, mode=mode)  # type: ignore[arg-type]
    manifest.append(plot_attention_shift_short(att, paths, mode="chart_only")[1])

    qr = prepare_quality_reach_dumbbell(paths)
    catalog_full = build_quality_reach_catalog(paths)
    for mode in ("chart_only", "review"):
        plot_quality_reach_dumbbell(qr, catalog_full, paths, mode=mode)  # type: ignore[arg-type]
    manifest.append(plot_quality_reach_dumbbell(qr, catalog_full, paths, mode="chart_only")[1])

    rich = prepare_richness_evidence(paths)
    for mode in ("chart_only", "review"):
        plot_richness_evidence_sequence(rich, paths, mode=mode)  # type: ignore[arg-type]
    manifest.append(plot_richness_evidence_sequence(rich, paths, mode="chart_only")[1])

    ees = prepare_ees_integrated(paths)
    for mode in ("chart_only", "review"):
        plot_ees_integrated_short(ees, paths, mode=mode, layout="integrated")  # type: ignore[arg-type]
        plot_ees_integrated_short(ees, paths, mode=mode, layout="three_panel")  # type: ignore[arg-type]
    manifest.append(plot_ees_integrated_short(ees, paths, mode="chart_only", layout="integrated")[1])

    return manifest
