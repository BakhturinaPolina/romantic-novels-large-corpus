"""Storyboard-aligned slide plot functions (v2 deck)."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

from .annotations import load_annotations
from .paths import PresentationPaths, default_paths
from .theme import (
    C_EXPL,
    C_GATE,
    C_NEG,
    C_NEUTRAL,
    C_POS,
    C_THIN,
    C_UNMEAS,
    EFFECT_GATE,
    HYPOTHESIS_ORDER,
    apply_theme,
    exploratory_tag,
    format_delta,
    gate_band,
    gate_lines,
    marker_for_gate,
    save_figure,
    set_title_with_subtitle,
    status_symbol,
    verdict_card_style,
)


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
        "output_path": str(paths[0]) if paths else "",
        "output_svg": str(paths[1]) if len(paths) > 1 else "",
        "output_pdf": str(paths[2]) if len(paths) > 2 else "",
    }


def plot_component_effects_presentation(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide08_component_effects",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    gate_band(ax, orientation="vertical")
    gate_lines(ax, orientation="vertical")

    y = np.arange(len(df))[::-1]
    for yi, row in zip(y, df.itertuples()):
        est = row.effect_size
        lo, hi = row.ci_low, row.ci_high
        mk = marker_for_gate(str(row.measurement_status))
        ax.errorbar(est, yi, xerr=[[est - lo], [hi - est]], fmt="none", color=C_NEUTRAL, capsize=3, lw=1.2, zorder=2)
        ax.scatter([est], [yi], **mk, zorder=3)
        ax.text(hi + 0.012, yi, format_delta(est), va="center", fontsize=10, color=C_NEUTRAL)

    labels = df["display_label"].fillna(df["label"]).tolist()
    ax.set_yticks(y)
    ax.set_yticklabels(labels[::-1])
    ax.set_xlabel("Cliff's δ (high-rated − low-rated)")
    ax.set_xlim(-0.22, 0.22)
    set_title_with_subtitle(
        ax,
        "Specific narrative functions reveal clearer differences",
        "Confirmatory component effects; shaded band = below prespecified |δ| = 0.11 gate",
    )
    ax.text(0.5, -0.12, "← lower in highly rated", transform=ax.transAxes, ha="center", fontsize=9, color="#666")
    ax.text(0.5, -0.16, "higher in highly rated →", transform=ax.transAxes, ha="center", fontsize=9, color="#666")
    fig.subplots_adjust(top=0.82, bottom=0.18)
    outs = save_figure(fig, paths.deck_figures, stem)
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
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.8), gridspec_kw={"width_ratios": [1.1, 0.9]})

    # Left: agreement bars
    y = np.arange(len(agreement))[::-1]
    pct = agreement["agreement_pct"].to_numpy()
    ax1.barh(y, pct, color="#56B4E9", height=0.55, alpha=0.85)
    for yi, p in zip(y, pct):
        ax1.text(p + 1.2, yi, f"{p:.0f}%", va="center", fontsize=10)
    ax1.set_yticks(y)
    ax1.set_yticklabels(agreement["hypothesis"])
    ax1.set_xlim(0, 65)
    ax1.set_xlabel("Lexical–contextual agreement (%)")
    ax1.set_title("Contextual agreement", fontsize=12, loc="left", fontweight="bold")

    # Right: measurement status
    ax2.axis("off")
    ax2.set_title("Measurement after refinement", fontsize=12, loc="left", fontweight="bold", pad=12)
    for i, h in enumerate(HYPOTHESIS_ORDER):
        row = primary.loc[primary["hypothesis"] == h].iloc[0]
        st = str(row["measurement_status"])
        sym = status_symbol(st)
        ypos = 0.88 - i * 0.14
        color = C_UNMEAS if st == "unmeasurable" else C_THIN if st == "thin" else C_POS
        ax2.text(0.05, ypos, h, transform=ax2.transAxes, fontsize=12, fontweight="bold", va="center")
        ax2.text(0.22, ypos, f"{sym} {st.capitalize()}", transform=ax2.transAxes, fontsize=11, color=color, va="center")

    fig.suptitle("Context changed what the topics actually meant", fontsize=14, fontweight="bold", y=1.02, x=0.02, ha="left")
    fig.text(0.5, 0.02, "Lexical similarity ≠ narrative function", ha="center", fontsize=11, fontweight="bold", color=C_NEUTRAL)
    fig.subplots_adjust(top=0.88, bottom=0.1, wspace=0.35)
    outs = save_figure(fig, paths.deck_figures, stem)
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
    stem: str = "slide07_primary_verdict_cards",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, axes = plt.subplots(2, 3, figsize=(12.5, 6.5))
    axes = axes.flatten()
    verdict_map = {
        "directional_only": "DIRECTIONAL",
        "inconclusive": "THIN / INCONCLUSIVE",
        "contradicted": "CONTRADICTED",
        "not_supported": "NOT SUPPORTED",
        "clears_gate": "DIRECTIONAL",
    }
    for ax, h in zip(axes, HYPOTHESIS_ORDER):
        row = primary.loc[primary["hypothesis"] == h].iloc[0]
        st = str(row["measurement_status"])
        styles = verdict_card_style(st if st == "unmeasurable" else row["verdict"])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        rect = FancyBboxPatch(
            (0.02, 0.02), 0.96, 0.96,
            boxstyle="round,pad=0.02",
            facecolor=styles["facecolor"],
            edgecolor=styles["edgecolor"],
            linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(0.5, 0.82, h, ha="center", fontsize=14, fontweight="bold", color=styles["color"])
        ax.text(0.5, 0.62, str(row["label"])[:40], ha="center", fontsize=9, color="#555", wrap=True)
        if st == "unmeasurable":
            ax.text(0.5, 0.38, "NOT MEASURABLE", ha="center", fontsize=11, fontweight="bold", color=C_UNMEAS)
        else:
            vlabel = verdict_map.get(str(row["verdict"]), str(row["verdict"]).upper())
            ax.text(0.5, 0.42, vlabel, ha="center", fontsize=10, fontweight="bold", color=styles["color"])
            ax.text(0.5, 0.22, format_delta(row["effect_size"]), ha="center", fontsize=12, color=C_NEUTRAL)
            if not bool(row.get("clears_delta_gate", False)):
                ax.text(0.5, 0.08, "below gate", ha="center", fontsize=8, color="#888")
    fig.suptitle(
        "None of the six broad hypotheses produced a clean confirmatory win",
        fontsize=14, fontweight="bold", y=1.02, x=0.02, ha="left",
    )
    fig.subplots_adjust(top=0.88, hspace=0.35, wspace=0.2)
    outs = save_figure(fig, paths.deck_figures, stem)
    return outs, _manifest_row(
        stem,
        "S07",
        "H1–H6 verdict cards",
        "main",
        ["presentation_primary_results.csv"],
        "Cliff's δ; verdict; measurement_status",
        "confirmatory",
        "H2/H3 categorical unmeasurable; not null at zero",
        outs,
    )


def plot_quality_reach_dumbbell(
    df: pd.DataFrame,
    catalog_full: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide10_quality_reach_dumbbell",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, ax = plt.subplots(figsize=(11, 6))
    n_both = int(
        (
            catalog_full.loc[catalog_full["analysis_resolution"] == "taxonomy_leaf"]["quality_gate"].astype(bool)
            & catalog_full.loc[catalog_full["analysis_resolution"] == "taxonomy_leaf"]["reach_gate"].astype(bool)
        ).sum()
    )
    y = np.arange(len(df))[::-1]
    for yi, row in zip(y, df.itertuples()):
        qd = row.quality_delta
        rd = row.reach_delta
        ax.scatter([qd], [yi], marker="o", s=80, color=C_POS, zorder=3, label="Quality" if yi == y[0] else "")
        ax.scatter([rd], [yi], marker="s", s=70, color=C_NEG, zorder=3, label="Reach" if yi == y[0] else "")
        ax.plot([qd, rd], [yi, yi], color="#aaaaaa", lw=1.5, zorder=2)
    ax.axvline(0, color="#888", lw=0.8)
    ax.axvline(EFFECT_GATE, color=C_GATE, ls="--", lw=0.8, alpha=0.7)
    ax.axvline(-EFFECT_GATE, color=C_GATE, ls="--", lw=0.8, alpha=0.7)
    labels = df["short_label"].fillna(df["label"]).tolist()
    ax.set_yticks(y)
    ax.set_yticklabels(labels[::-1])
    ax.set_xlabel("Cliff's δ (high-rated or high-reach − comparison)")
    set_title_with_subtitle(
        ax,
        "What makes a book widely read is not what makes it highly rated",
        "Taxonomy-leaf contrasts; squares = reach, circles = quality (rating)",
    )
    ax.legend(loc="lower right", frameon=False)
    ax.text(
        0.02, 0.02,
        f"{n_both} leaves cleared the effect gate on both outcomes",
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round", facecolor="#fff8e6", edgecolor=C_THIN),
    )
    exploratory_tag(ax)
    fig.subplots_adjust(top=0.82)
    outs = save_figure(fig, paths.deck_figures, stem)
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
    stem: str = "slide11_richness_evidence",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    panels = [
        ("RAW", ["raw_taxonomy_delta", "raw_topic_delta"]),
        ("EQUAL SENTENCE BUDGET", ["rarefied_taxonomy"]),
        ("AFTER THEMATIC DRIVERS", ["controlled_plus_drivers"]),
    ]
    for ax, (title, keys) in zip(axes, panels):
        ax.axis("off")
        ax.text(0.5, 0.92, title, ha="center", fontsize=11, fontweight="bold", transform=ax.transAxes)
        lines = []
        for k in keys:
            row = story.loc[story["analysis"] == k]
            if row.empty:
                continue
            r = row.iloc[0]
            if k.startswith("raw"):
                lines.append(f"{r['metric']}\nδ ≈ {format_delta(r['estimate'])}")
            elif k == "rarefied_taxonomy":
                lines.append(f"Rarefied taxonomy richness\np ≈ {r['p_value']:.2f}")
            else:
                lines.append(f"Raw taxonomy richness strengthens\nβ ≈ {r['estimate']:.4f}\np < .001\n\nSUPPRESSION")
        rect = FancyBboxPatch(
            (0.05, 0.08), 0.9, 0.82,
            boxstyle="round,pad=0.02",
            facecolor="#f8f8f8",
            edgecolor="#cccccc",
            transform=ax.transAxes,
        )
        ax.add_patch(rect)
        ax.text(0.5, 0.45, "\n\n".join(lines), ha="center", va="center", fontsize=10, transform=ax.transAxes, zorder=2)
    fig.suptitle(
        "Better-rated books are not simply \"about more things\"",
        fontsize=14, fontweight="bold", y=1.05, x=0.02, ha="left",
    )
    fig.text(
        0.5, 0.02,
        "Which themes receive attention appears more interpretable than raw thematic breadth alone.",
        ha="center", fontsize=10, fontweight="bold", color=C_NEUTRAL,
    )
    exploratory_tag(axes[-1])
    fig.subplots_adjust(top=0.78, bottom=0.15, wspace=0.25)
    outs = save_figure(fig, paths.deck_figures, stem)
    return outs, _manifest_row(
        stem,
        "S11",
        "Richness three-stage evidence",
        "main",
        ["thematic_richness_cliffs_delta", "thematic_richness_ols", "thematic_richness_vs_drivers"],
        "Cliff's δ; OLS β",
        "exploratory",
        "Rarefaction removes raw association; suppression after drivers",
        outs,
    )


def plot_attention_shift_short(
    df: pd.DataFrame,
    paths: PresentationPaths,
    *,
    stem: str = "slide09_attention_shift",
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, ax = plt.subplots(figsize=(10, 5.5))
    y = np.arange(len(df))[::-1]
    vals = df["diff_pp"].to_numpy()
    colors = [C_POS if v > 0 else C_NEG for v in vals]
    ax.barh(y, vals, color=colors, height=0.55, alpha=0.85)
    for yi, v in zip(y, vals):
        ax.text(v + (0.02 if v >= 0 else -0.02), yi, f"{v:+.3f} pp", va="center", ha="left" if v >= 0 else "right", fontsize=9)
    labels = df["display_label"].fillna(df["label"]).tolist()
    ax.set_yticks(y)
    ax.set_yticklabels(labels[::-1])
    ax.axvline(0, color="#888", lw=0.8)
    ax.set_xlabel("Mean share difference (percentage points), high-rated − low-rated")
    set_title_with_subtitle(
        ax,
        "Higher-rated romances devote relatively more space to tenderness",
        "Exploratory compositional shift — not causal",
    )
    exploratory_tag(ax)
    fig.subplots_adjust(top=0.82)
    outs = save_figure(fig, paths.deck_figures, stem)
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
) -> Tuple[List[Path], Dict]:
    apply_theme()
    fig, ax = plt.subplots(figsize=(9, 6.5))
    all_pts = trials[~trials["pareto_efficient"]]
    pareto_pts = trials[trials["pareto_efficient"]]
    selected = trials[trials["is_selected"]]
    ax.scatter(
        all_pts["topic_diversity"],
        all_pts["coherence_c_v"],
        s=12,
        c="#bbbbbb",
        alpha=0.5,
        label="All trials",
        zorder=1,
    )
    ax.scatter(
        pareto_pts["topic_diversity"],
        pareto_pts["coherence_c_v"],
        s=40,
        c=C_POS,
        alpha=0.7,
        label="Pareto-efficient",
        zorder=2,
    )
    if not selected.empty:
        ax.scatter(
            selected["topic_diversity"],
            selected["coherence_c_v"],
            s=200,
            marker="*",
            c=C_THIN,
            edgecolors=C_NEUTRAL,
            linewidths=1,
            label="Selected model",
            zorder=4,
        )
        ax.annotate(
            "Selected model",
            (selected.iloc[0]["topic_diversity"], selected.iloc[0]["coherence_c_v"]),
            xytext=(12, 12),
            textcoords="offset points",
            fontsize=10,
            arrowprops=dict(arrowstyle="->", color=C_NEUTRAL),
        )
    ax.set_xlabel("Topic diversity")
    ax.set_ylabel("Coherence (c_v)")
    set_title_with_subtitle(
        ax,
        "The final topic model was chosen as a trade-off, not by one metric",
        f"Bayesian optimization over {len(trials)} configurations",
    )
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.subplots_adjust(top=0.82)
    outs = save_figure(fig, paths.deck_figures, stem)
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
) -> Tuple[List[Path], Dict]:
    apply_theme()
    domains = ["emotion", "embodiment", "social"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.5), sharex=True)
    for ax, domain in zip(axes, domains):
        sub = df.loc[df["domain"] == domain]
        if sub.empty:
            ax.set_visible(False)
            continue
        y = np.arange(len(sub))[::-1]
        gate_band(ax, orientation="vertical")
        gate_lines(ax, orientation="vertical")
        for yi, row in zip(y, sub.itertuples()):
            est, lo, hi = row.cliffs_delta, row.ci_low, row.ci_high
            mk = marker_for_gate("thin" if str(row.status) == "thin" else "viable")
            ax.errorbar(est, yi, xerr=[[est - lo], [hi - est]], fmt="none", color=C_NEUTRAL, capsize=2, lw=1)
            ax.scatter([est], [yi], **mk, zorder=3)
        labels = sub["display_label"].fillna(sub["construct"]).tolist()
        ax.set_yticks(y)
        ax.set_yticklabels(labels[::-1], fontsize=9)
        ax.set_title(domain.upper(), fontsize=11, fontweight="bold", loc="left")
        ax.set_xlim(-0.25, 0.25)
    axes[1].set_xlabel("Cliff's δ")
    fig.suptitle(
        "The exploratory extension shifts the question from topics to narrative experience",
        fontsize=13, fontweight="bold", y=1.02, x=0.02, ha="left",
    )
    fig.text(0.5, 0.02, "Exploratory, frozen coding — does not change H1–H6 verdicts", ha="center", fontsize=9, color=C_EXPL)
    fig.subplots_adjust(top=0.82, bottom=0.12, wspace=0.45)
    outs = save_figure(fig, paths.deck_figures, stem)
    return outs, _manifest_row(
        stem,
        "S12",
        "EES integrated short",
        "main",
        ["emotion_effects", "embodiment_effects", "family_social_effects"],
        "Cliff's δ",
        "exploratory",
        "Frozen LLM coding + human overrides; not confirmatory",
        outs,
    )


def export_component_animation_steps(
    df: pd.DataFrame,
    paths: PresentationPaths,
) -> List[Path]:
    """Export staged slide08 SVGs for PowerPoint/Gamma build sequences."""
    from .annotations import load_animation_sequence

    seq = load_animation_sequence("S08", paths)
    if seq.empty:
        return []
    outputs: List[Path] = []
    features = df["feature"].tolist()
    for _, step in seq.iterrows():
        el = str(step["element_id"])
        if el == "axes":
            sub = df.iloc[0:0]
        else:
            idx = features.index(el) + 1 if el in features else len(features)
            sub = df.iloc[:idx]
        if sub.empty and el == "axes":
            apply_theme()
            fig, ax = plt.subplots(figsize=(10.5, 6.2))
            gate_band(ax, orientation="vertical")
            gate_lines(ax, orientation="vertical")
            ax.set_xlim(-0.22, 0.22)
            ax.set_xlabel("Cliff's δ (high-rated − low-rated)")
            set_title_with_subtitle(
                ax,
                "Specific narrative functions reveal clearer differences",
                f"Step {int(step['step'])}: axes",
            )
            fig.subplots_adjust(top=0.82, bottom=0.18)
            outputs.extend(save_figure(fig, paths.deck_figures, f"slide08_step{int(step['step']):02d}_{el}"))
        elif not sub.empty:
            outs, _ = plot_component_effects_presentation(
                sub, paths, stem=f"slide08_step{int(step['step']):02d}_{el}"
            )
            outputs.extend(outs)
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
    outs, row = plot_pareto_selection(trials, paths)
    manifest.append(row)

    ctx = prepare_context_measurement(paths)
    outs, row = plot_context_and_measurement(ctx["agreement"], ctx["primary"], paths)
    manifest.append(row)

    primary = prepare_primary_verdicts(paths)
    outs, row = plot_primary_verdict_cards(primary, paths)
    manifest.append(row)

    comp = prepare_component_effects(paths)
    outs, row = plot_component_effects_presentation(comp, paths)
    manifest.append(row)
    export_component_animation_steps(comp, paths)

    att = prepare_attention_shift(paths)
    outs, row = plot_attention_shift_short(att, paths)
    manifest.append(row)

    qr = prepare_quality_reach_dumbbell(paths)
    catalog_full = build_quality_reach_catalog(paths)
    outs, row = plot_quality_reach_dumbbell(qr, catalog_full, paths)
    manifest.append(row)

    rich = prepare_richness_evidence(paths)
    outs, row = plot_richness_evidence_sequence(rich, paths)
    manifest.append(row)

    ees = prepare_ees_integrated(paths)
    outs, row = plot_ees_integrated_short(ees, paths)
    manifest.append(row)

    return manifest
