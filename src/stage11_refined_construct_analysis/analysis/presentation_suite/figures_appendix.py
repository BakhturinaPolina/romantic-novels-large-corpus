"""Appendix presentation figures."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from .evidence_metadata import _read_table
from .figures_main import _manifest_row
from .paths import PresentationPaths, default_paths
from .theme import (
    C_EXPL,
    C_NEG,
    C_NEUTRAL,
    C_POS,
    C_THIN,
    C_UNMEAS,
    EFFECT_GATE,
    apply_theme,
    gate_lines,
    marker_for_gate,
    save_figure,
)


def appendix_richness(paths: PresentationPaths) -> Tuple[List, Dict]:
    cliffs = _read_table(paths.table("14_exploratory_presentation_results", "thematic_richness_cliffs_delta"))
    drivers = _read_table(paths.table("14_exploratory_presentation_results", "thematic_richness_vs_drivers"))
    apply_theme()
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))

    # Panel A: raw vs rarefied taxonomy n_eff
    ax = axes[0]
    feats = ["taxonomy_n_eff", "rare_taxonomy_n_eff"]
    labels = ["Raw taxonomy eᴴ", "Rarefied taxonomy eᴴ"]
    sub = cliffs.set_index("feature").loc[feats]
    y = np.arange(len(feats))[::-1]
    for yi, feat in zip(y, feats):
        r = sub.loc[feat]
        ax.plot([r["ci_low"], r["ci_high"]], [yi, yi], color=C_NEUTRAL, lw=1.6)
        ax.scatter([r["cliffs_delta"]], [yi], color=C_POS, s=70, zorder=3)
        ax.text(
            r["ci_high"] + 0.01,
            yi,
            f"δ={r['cliffs_delta']:.3f}",
            va="center",
            fontsize=9,
        )
    gate_lines(ax)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Cliff's δ (high − low)")
    ax.set_title("A. Unadjusted high–low contrast")
    ax.set_xlim(-0.05, 0.35)

    # Panel B: M1 vs M2 coefficients
    ax = axes[1]
    m = drivers.loc[drivers["term"] == "taxonomy_n_eff"].copy()
    m["model_short"] = m["model"].map(
        {
            "M1_richness_only": "M1: richness + length/year/genre",
            "M2_richness_plus_drivers": "M2: + thematic drivers",
        }
    )
    m = m.reset_index(drop=True)
    y = np.arange(len(m))[::-1]
    labels = []
    for yi, r in zip(y, m.itertuples()):
        ax.plot([r.ci_low, r.ci_high], [yi, yi], color=C_NEUTRAL, lw=1.6)
        ax.scatter([r.coefficient], [yi], color=C_POS, s=70, zorder=3)
        ax.text(
            r.ci_high + 0.0004,
            yi,
            f"β={r.coefficient:.4f}, p={r.p_value:.3g}",
            va="center",
            fontsize=9,
        )
        labels.append(r.model_short)
    ax.axvline(0, color="#888888", lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("OLS coefficient on rating_shrunk (author-clustered SE)")
    ax.set_title("B. Adjusted richness (suppression in M2)")
    fig.suptitle(
        "Thematic richness (exploratory): rarefaction weakens; drivers strengthen raw breadth",
        fontsize=13,
        y=1.02,
    )
    fig.text(
        0.5,
        -0.02,
        "Do not read M2 as “richness null after drivers” — coefficient increases (suppression).",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    outs = save_figure(fig, paths.out_dir, "appendix_richness")
    return outs, _manifest_row(
        "appendix_richness",
        "Thematic richness two-panel",
        "appendix",
        ["thematic_richness_cliffs_delta", "thematic_richness_vs_drivers"],
        "cliffs_delta; M1/M2 taxonomy_n_eff β",
        "exploratory",
        "Suppression — not attenuation",
        outs,
    )


def appendix_danger_protection(paths: PresentationPaths) -> Tuple[List, Dict]:
    ix = _read_table(paths.table("14_exploratory_presentation_results", "danger_x_protection_reused"))
    quad = _read_table(paths.table("14_exploratory_presentation_results", "danger_x_protection_quadrants_reused"))
    # Use moderate specification as primary display
    spec = "moderate + fractional"
    row = ix.loc[ix["protection_index"] == spec].iloc[0]
    q = quad.loc[quad["protection_index"] == spec].copy()

    apply_theme()
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    # Two lines: higher vs lower protection across danger bins
    danger_order = ["lower_danger", "higher_danger"]
    x = np.arange(len(danger_order))
    for prot, color, ls in (
        ("lower_protection", C_NEG, "--"),
        ("higher_protection", C_POS, "-"),
    ):
        means = []
        for d in danger_order:
            m = q.loc[(q["danger_bin"] == d) & (q["protection_bin"] == prot), "mean_rating"]
            means.append(float(m.iloc[0]))
        ax.plot(x, means, color=color, ls=ls, marker="o", lw=2, label=prot.replace("_", " "))
        for xi, yi in zip(x, means):
            ax.text(xi, yi + 0.002, f"{yi:.3f}", ha="center", fontsize=9, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(["Lower danger", "Higher danger"])
    ax.set_ylabel("Mean rating_shrunk")
    ax.set_title("No reliable danger × protection interaction")
    p_int = float(row["z_danger_x_z_protection_p"])
    ax.text(
        0.0,
        1.02,
        f"Exploratory · {spec} · interaction p = {p_int:.2f} "
        f"(strict p={float(ix.loc[ix.protection_index=='strict t119 only','z_danger_x_z_protection_p'].iloc[0]):.2f}; "
        f"broad p={float(ix.loc[ix.protection_index=='broad enacted','z_danger_x_z_protection_p'].iloc[0]):.2f})",
        transform=ax.transAxes,
        fontsize=9,
        color=C_EXPL,
    )
    ax.legend(frameon=False, title="Protection")
    # Keep y-scale honest — avoid magnifying tiny rating differences
    vals = q["mean_rating"].astype(float)
    mid = float(vals.mean())
    ax.set_ylim(mid - 0.08, mid + 0.08)
    outs = save_figure(fig, paths.out_dir, "appendix_danger_protection_interaction")
    return outs, _manifest_row(
        "appendix_danger_protection",
        "Danger × protection interaction",
        "appendix",
        ["danger_x_protection_reused", "danger_x_protection_quadrants_reused"],
        "mean_rating by quadrant; interaction p",
        "exploratory",
        "Interaction n.s. — do not claim synergy",
        outs,
    )


def appendix_security_care_specificity(paths: PresentationPaths) -> Tuple[List, Dict]:
    traj = _read_table(
        paths.table("14_exploratory_presentation_results", "strict_moderate_broad_trajectories_reused")
    )
    families = list(dict.fromkeys(traj["family"]))
    apply_theme()
    n = len(families)
    ncols = 2
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(11, 3.2 * nrows), sharey=True)
    axes = np.atleast_1d(axes).ravel()
    level_x = {"strict": 0, "moderate": 1, "broad": 2}
    for ax, fam in zip(axes, families):
        sub = traj.loc[traj["family"] == fam]
        xs, ys, ylo, yhi = [], [], [], []
        for _, r in sub.iterrows():
            if pd.isna(r["cliffs_delta"]):
                ax.text(level_x[r["level"]], 0.0, "unmeas.", ha="center", color=C_UNMEAS, fontsize=9)
                continue
            xs.append(level_x[r["level"]])
            ys.append(r["cliffs_delta"])
            ylo.append(r["ci_low"])
            yhi.append(r["ci_high"])
            ax.plot([r["ci_low"], r["ci_high"]], [level_x[r["level"]], level_x[r["level"]]], color=C_NEUTRAL, lw=1.3)
            face = "none" if int(r["n_topics"]) <= 1 else C_POS
            ax.scatter(
                [r["cliffs_delta"]],
                [level_x[r["level"]]],
                facecolors=face,
                edgecolors=C_POS,
                s=60,
                zorder=3,
            )
            ax.text(r["ci_high"] + 0.01, level_x[r["level"]], f"n={int(r['n_topics'])}", va="center", fontsize=8)
        ax.axvline(0, color="#888", lw=0.8)
        ax.axvline(EFFECT_GATE, color="#666", ls="--", lw=0.8)
        ax.axvline(-EFFECT_GATE, color="#666", ls="--", lw=0.8)
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(["strict", "moderate", "broad"])
        ax.set_title(fam.replace("_", " "))
        ax.set_xlabel("Cliff's δ")
    for ax in axes[len(families) :]:
        ax.axis("off")
    fig.suptitle(
        "Security/care specificity (exploratory): effect by definition breadth",
        fontsize=13,
        y=1.01,
    )
    fig.tight_layout()
    outs = save_figure(fig, paths.out_dir, "appendix_security_care_specificity")
    return outs, _manifest_row(
        "appendix_security_care",
        "Security/care specificity small multiples",
        "appendix",
        ["strict_moderate_broad_trajectories_reused"],
        "cliffs_delta by strict/moderate/broad",
        "exploratory",
        "Broad protective commitment collapses toward 0",
        outs,
    )


def appendix_promise_functions(paths: PresentationPaths) -> Tuple[List, Dict]:
    pr = _read_table(paths.table("14_exploratory_presentation_results", "promise_type_comparison_reused"))
    pr = pr.sort_values("cliffs_delta").reset_index(drop=True)
    apply_theme()
    fig, ax = plt.subplots(figsize=(11, 6))
    y = np.arange(len(pr))
    for yi, r in pr.iterrows():
        ax.plot([r["ci_low"], r["ci_high"]], [yi, yi], color=C_NEUTRAL, lw=1.5)
        thin = int(r["n_topics"]) <= 2
        face = "none" if thin else C_POS
        ax.scatter([r["cliffs_delta"]], [yi], facecolors=face, edgecolors=C_POS, s=70, zorder=3)
        flag = " ⚠ few topics" if thin else ""
        ax.text(0.28, yi, f"n={int(r['n_topics'])}{flag}", va="center", fontsize=9, color=C_THIN if thin else C_NEUTRAL)
    gate_lines(ax)
    ax.set_yticks(y)
    ax.set_yticklabels(pr["promise_type"].str.replace("_", " "))
    ax.set_xlabel("Cliff's δ")
    ax.set_title("Promise-function effects (exploratory)")
    ax.text(
        0.0,
        1.02,
        "Open markers / flags = bundles with ≤2 topics (e.g. protective commitment n=4 still thin-ish)",
        transform=ax.transAxes,
        fontsize=9,
        color=C_EXPL,
    )
    # Explicitly flag protective_commitment
    for yi, r in pr.iterrows():
        if r["promise_type"] == "protective_commitment":
            ax.text(
                r["ci_low"] - 0.01,
                yi,
                "4-topic bundle",
                ha="right",
                va="center",
                fontsize=8,
                color=C_THIN,
            )
    fig.subplots_adjust(left=0.28)
    outs = save_figure(fig, paths.out_dir, "appendix_promise_functions")
    return outs, _manifest_row(
        "appendix_promise",
        "Promise-function dot-and-whisker",
        "appendix",
        ["promise_type_comparison_reused"],
        "cliffs_delta; n_topics",
        "exploratory",
        "Flag few-topic bundles",
        outs,
    )


def appendix_quality_reach(paths: PresentationPaths) -> Tuple[List, Dict]:
    qr = _read_table(paths.table("14_exploratory_presentation_results", "quality_reach_standardized_betas"))
    long = _read_table(paths.table("14_exploratory_presentation_results", "quality_reach_betas_long"))
    # Focal labels
    focal = {
        "RAX_appearance_grooming",
        "RAX_tenderness_core",
        "RAX_emotional_reassurance",
        "RAX_external_danger_crisis",
        "RAX_external_protection",
        "RLR_emotional_vs_explicit",
    }
    apply_theme()
    fig, ax = plt.subplots(figsize=(8.5, 7))
    ax.axhline(0, color="#888", lw=0.8)
    ax.axvline(0, color="#888", lw=0.8)
    for _, r in qr.iterrows():
        feat = r["feature"]
        # p from long table for opacity
        pq = long.loc[(long["feature"] == feat) & (long["channel"] == "quality"), "p"]
        pval = float(pq.iloc[0]) if len(pq) else 1.0
        alpha = 1.0 if pval < 0.05 else 0.35
        is_focal = feat in focal
        ax.scatter(
            [r["quality"]],
            [r["reach"]],
            s=90 if is_focal else 40,
            color=C_POS if is_focal else "#999999",
            alpha=alpha,
            zorder=3 if is_focal else 2,
        )
        if is_focal:
            ax.annotate(
                feat.replace("RAX_", "").replace("RLR_", ""),
                (r["quality"], r["reach"]),
                textcoords="offset points",
                xytext=(6, 4),
                fontsize=9,
            )
    ax.set_xlabel("Standardized quality β")
    ax.set_ylabel("Standardized reach β")
    ax.set_title("Quality vs reach (exploratory; faded = quality p≥.05)")
    outs = save_figure(fig, paths.out_dir, "appendix_quality_reach")
    return outs, _manifest_row(
        "appendix_quality_reach",
        "Quality versus reach",
        "appendix",
        ["quality_reach_standardized_betas"],
        "quality; reach standardized betas",
        "exploratory",
        "Opacity encodes quality significance",
        outs,
    )


def appendix_function_drift(paths: PresentationPaths) -> Tuple[List, Dict]:
    drift = _read_table(paths.table("10_contextual_validation", "cell_stability_by_hypothesis"))
    apply_theme()
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    # Order by pct_differs desc
    d = drift.sort_values("pct_differs", ascending=True)
    y = np.arange(len(d))
    drifted = d["pct_differs"] * 100
    stable = 100 - drifted
    ax.barh(y, stable, color="#CCCCCC", label="Stable function")
    ax.barh(y, drifted, left=stable, color=C_NEG, label="Drifted function")
    for yi, r in zip(y, d.itertuples()):
        ax.text(
            101,
            yi,
            f"{int(r.n_differs)}/{int(r.n_with_both_high_prev)} ({100 * r.pct_differs:.0f}%)",
            va="center",
            fontsize=10,
        )
    ax.set_yticks(y)
    ax.set_yticklabels(d["hypothesis"])
    ax.set_xlim(0, 125)
    ax.set_xlabel("Share of comparable topics (%)")
    ax.set_title("Contextual function drift (methodological)")
    ax.text(
        0.0,
        1.02,
        "H2 absent from this table (insufficient comparable cells). Exploratory/appendix only.",
        transform=ax.transAxes,
        fontsize=9,
        color="#555555",
    )
    ax.legend(frameon=False, loc="lower right")
    outs = save_figure(fig, paths.out_dir, "appendix_function_drift")
    return outs, _manifest_row(
        "appendix_function_drift",
        "Contextual function drift",
        "appendix",
        ["cell_stability_by_hypothesis"],
        "n_differs / n_with_both_high_prev",
        "methodological",
        "H2 not in table",
        outs,
    )


def appendix_felt_vs_looked(paths: PresentationPaths) -> Tuple[List, Dict]:
    felt = _read_table(paths.table("15_emotion_embodiment_social_world_exploration", "felt_vs_looked_body"))
    apply_theme()
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    # Put logratio first visually
    order = ["felt_vs_looked_logratio", "felt_body", "looked_at_body", "body_interoceptive", "body_vulnerable", "body_markings", "body_external_appearance", "body_grooming"]
    felt = felt.set_index("construct").loc[[c for c in order if c in set(felt["construct"])]].reset_index()
    y = np.arange(len(felt))[::-1]
    for yi, r in zip(y, felt.itertuples()):
        ax.plot([r.ci_low, r.ci_high], [yi, yi], color=C_NEUTRAL, lw=1.5)
        status = str(r.status) if pd.notna(r.status) else "measurable"
        thin = status == "thin" or (pd.notna(r.n_topics) and int(r.n_topics) <= 1)
        face = "none" if thin else C_POS
        ax.scatter([r.cliffs_delta], [yi], facecolors=face, edgecolors=C_POS, s=70, zorder=3)
        nlab = f"n={int(r.n_topics)}" if pd.notna(r.n_topics) else "ratio"
        ax.text(0.20, yi, nlab + (" ⚠" if thin else ""), va="center", fontsize=9)
    gate_lines(ax)
    ax.set_yticks(y)
    ax.set_yticklabels(felt["construct"].str.replace("_", " "))
    ax.set_xlabel("Cliff's δ")
    ax.set_title("Felt vs looked-at embodiment (exploratory / post-hoc)")
    ax.text(
        0.0,
        1.02,
        "Exploratory — open marker = thin / one-topic construct",
        transform=ax.transAxes,
        fontsize=10,
        color=C_EXPL,
        fontweight="bold",
    )
    fig.subplots_adjust(left=0.28)
    outs = save_figure(fig, paths.out_dir, "appendix_felt_vs_looked")
    return outs, _manifest_row(
        "appendix_felt_vs_looked",
        "Felt versus looked-at embodiment",
        "appendix",
        ["felt_vs_looked_body"],
        "cliffs_delta; n_topics",
        "exploratory",
        "body_markings thin",
        outs,
    )


def appendix_ees_three_panel(paths: PresentationPaths) -> Tuple[List, Dict]:
    emotion = _read_table(paths.table("15_emotion_embodiment_social_world_exploration", "emotion_effects"))
    embod = _read_table(paths.table("15_emotion_embodiment_social_world_exploration", "embodiment_effects"))
    social = _read_table(paths.table("15_emotion_embodiment_social_world_exploration", "family_social_effects"))
    # Drop duplicate felt/looked aggregates from embodiment panel (shown in dedicated fig)
    embod = embod.loc[~embod["construct"].isin(["felt_body", "looked_at_body", "felt_vs_looked_logratio"])]

    apply_theme()
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 6.2), sharex=True)
    panels = [
        (axes[0], emotion, "Emotion regulation", "construct"),
        (axes[1], embod, "Embodiment", "construct"),
        (axes[2], social, "Social embeddedness", "construct"),
    ]
    for ax, df, title, col in panels:
        df = df.sort_values("cliffs_delta").reset_index(drop=True)
        y = np.arange(len(df))
        for yi, r in df.iterrows():
            if pd.isna(r["cliffs_delta"]):
                continue
            ax.plot([r["ci_low"], r["ci_high"]], [yi, yi], color=C_NEUTRAL, lw=1.3)
            status = str(r.get("status", "measurable")).lower()
            thin = status == "thin" or (pd.notna(r.get("n_topics")) and float(r["n_topics"]) <= 1)
            face = "none" if thin else C_POS
            ax.scatter([r["cliffs_delta"]], [yi], facecolors=face, edgecolors=C_POS, s=55, zorder=3)
        gate_lines(ax)
        ax.set_yticks(y)
        ax.set_yticklabels(df[col].str.replace("_", " ").str.replace("emotion ", "").str.replace("body ", ""))
        ax.set_title(title)
        ax.set_xlabel("Cliff's δ")
        # Highlight emotion_containment
        if title.startswith("Emotion") and "emotion_containment" in set(df["construct"]):
            idx = df.index[df["construct"] == "emotion_containment"][0]
            ax.get_yticklabels()[list(df.index).index(idx)].set_fontweight("bold")

    fig.suptitle("Exploratory associations with higher ratings", fontsize=14, color=C_EXPL, y=1.02)
    fig.tight_layout()
    outs = save_figure(fig, paths.out_dir, "appendix_ees_three_panel")
    return outs, _manifest_row(
        "appendix_ees",
        "Emotion / embodiment / social three-panel",
        "appendix",
        ["emotion_effects", "embodiment_effects", "family_social_effects"],
        "cliffs_delta including emotion_containment",
        "exploratory",
        "Includes emotion_containment (δ≈0.18)",
        outs,
    )


def appendix_genre_era(paths: PresentationPaths) -> Tuple[List, Dict]:
    ge = _read_table(paths.table("14_exploratory_presentation_results", "genre_era_subgroup_deltas"))
    # Four focal constructs from confirmatory components
    available = set(ge["feature"])
    focal = [
        f
        for f in (
            "RAX_tenderness_core",
            "RAX_appearance_grooming",
            "RAX_external_danger_crisis",
            "RAX_h3_emotional_side",
        )
        if f in available
    ]
    # Overall estimates from component/primary tables
    from .evidence_metadata import load_components

    comps = load_components(paths).set_index("feature")
    apply_theme()
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8), sharex=False)
    axes = axes.ravel()
    for ax, feat in zip(axes, focal):
        sub = ge.loc[ge["feature"] == feat].copy()
        # Prefer genre_group then year bins
        sub = sub.sort_values(["group_type", "group"])
        y = np.arange(len(sub))
        overall = float(comps.loc[feat, "effect_size"]) if feat in comps.index else np.nan
        if pd.notna(overall):
            ax.axvline(overall, color=C_POS, lw=1.5, label=f"overall δ={overall:.3f}")
        ax.axvline(0, color="#888", lw=0.8)
        ax.scatter(sub["cliffs_delta"], y, color="#666666", s=45)
        labels = [f"{r.group_type}:{r.group} (nₕ={int(r.n_high)}, nₗ={int(r.n_low)})" for r in sub.itertuples()]
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_title(feat.replace("RAX_", ""))
        ax.set_xlabel("Cliff's δ")
        if pd.notna(overall):
            ax.legend(frameon=False, fontsize=8, loc="best")
    fig.suptitle("Genre/era subgroup stability (appendix; uncertainty via n, not formal CI)", fontsize=13)
    fig.tight_layout()
    outs = save_figure(fig, paths.out_dir, "appendix_genre_era")
    return outs, _manifest_row(
        "appendix_genre_era",
        "Genre/era stability small multiples",
        "appendix",
        ["genre_era_subgroup_deltas", "component_effects"],
        "subgroup cliffs_delta; overall reference",
        "exploratory",
        "No formal subgroup CIs in source table",
        outs,
    )


def build_appendix_figures(paths: PresentationPaths | None = None) -> List[Dict]:
    paths = paths or default_paths()
    manifest: List[Dict] = []
    for fn in (
        appendix_richness,
        appendix_danger_protection,
        appendix_security_care_specificity,
        appendix_promise_functions,
        appendix_quality_reach,
        appendix_function_drift,
        appendix_felt_vs_looked,
        appendix_ees_three_panel,
        appendix_genre_era,
    ):
        _, row = fn(paths)
        manifest.append(row)
    return manifest
