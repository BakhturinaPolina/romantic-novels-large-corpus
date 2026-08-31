# %% [markdown]
# # 14 — Exploratory presentation results
#
# **Exploratory analysis. These analyses do not change the confirmatory H1–H6 verdicts
# from Notebook 13.**
#
# Builds on Notebook 12 (security/care/appearance deep-dive): overlapping tables are
# **reused**, not recomputed. New pieces: thematic richness, attention waterfall,
# dose-response curves, residual Goodreads quadrants, genre/era heatmap,
# representative examples.
#
# Stage 10 `06_goodreads_validation` remains the taxonomy-era baseline and is not edited.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

cwd = Path.cwd().resolve()
root = cwd
for _ in range(6):
    if (root / "configs").is_dir() and (root / "src").is_dir():
        break
    root = root.parent
sys.path.insert(0, str(root))

from src.stage10_correlation_analysis.analysis import models as mdl
from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh
from src.stage11_refined_construct_analysis.analysis import presentation as pres
from src.stage11_refined_construct_analysis.analysis import thematic_richness as tr

ctx = nh.setup("14_exploratory_presentation_results")
cfg = ctx.cfg
GATE = nh.effect_gate(cfg)
coverage = nh.load_construct_coverage(cfg)

# %%
frame = nh.load_refined_frame(cfg, "strict")
if "book_id" in frame.columns:
    frame = frame.set_index("book_id")
usable = frame[frame["analysable"].fillna(True)].copy() if "analysable" in frame.columns else frame.copy()
work = usable.reset_index()
work = pres.add_year_bin(work)
work = pres.residualize_outcomes(work)
work = pres.residual_goodreads_quadrants(work)

master = nh.load_master(cfg)

# Load NB12 / NB13 artifacts where available
def try_load(notebook: str, name: str) -> pd.DataFrame:
    try:
        df = pres.load_notebook_table(cfg, notebook, name)
        print(f"  loaded {notebook}/{name} ({len(df):,} rows)")
        return df
    except FileNotFoundError as exc:
        print(f"  missing {notebook}/{name}: {exc}")
        return pd.DataFrame()


nb12_traj = try_load("12_exploratory_security_care_appearance", "strict_moderate_broad_trajectories")
nb12_promise = try_load("12_exploratory_security_care_appearance", "promise_type_comparison")
nb12_forest = try_load("12_exploratory_security_care_appearance", "topic_forest_broad_families")
nb12_presence = try_load("12_exploratory_security_care_appearance", "presence_vs_intensity")
nb12_danger = try_load("12_exploratory_security_care_appearance", "danger_x_protection_interaction")
nb12_danger_quad = try_load("12_exploratory_security_care_appearance", "danger_x_protection_quadrants")
nb12_care_app = try_load("12_exploratory_security_care_appearance", "care_x_appearance_quadrants")
nb13_effects = try_load("13_final_statistical_tests", "final_all_effects")
nb11_stab = try_load("11_refined_robustness", "stability_summary")
nb11_comp = try_load("11_refined_robustness", "headline_component_effects")

# %% [markdown]
# ## Section 1 — What actually differs most?
#
# Forest of refined features (from NB13 when available, else recomputed Cliff's δ).

# %%
HEADLINE = list(pres.HEADLINE_THEMES_FOR_HEATMAP) + [
    "RAX_emotional_reassurance",
    "RAX_repair",
    "RLR_emotional_vs_explicit",
    "RLR_darkness_vs_tenderness",
]
HEADLINE = list(dict.fromkeys(HEADLINE))

if len(nb13_effects):
    forest = nb13_effects[nb13_effects["feature"].isin(HEADLINE)].copy()
else:
    forest = nh.cliffs_delta_table(work, HEADLINE, n_boot=400, seed=42)
    forest["measurement_gate"] = [nh.gate_for_feature(coverage, f) for f in forest["feature"]]

forest = forest.dropna(subset=["cliffs_delta"])
forest = forest[forest.get("measurement_gate", "viable") != "unmeasurable"] if "measurement_gate" in forest.columns else forest
forest = forest.sort_values("cliffs_delta")
display(forest.round(4))
ctx.save_table(forest, "presentation_forest")

fig, ax = plt.subplots(figsize=(9, 6))
y = np.arange(len(forest))
lo = forest["ci_low"] if "ci_low" in forest.columns else forest["cliffs_delta"]
hi = forest["ci_high"] if "ci_high" in forest.columns else forest["cliffs_delta"]
ax.errorbar(
    forest["cliffs_delta"],
    y,
    xerr=[forest["cliffs_delta"] - lo, hi - forest["cliffs_delta"]],
    fmt="o",
    color="steelblue",
    capsize=3,
)
ax.axvline(0, color="gray", lw=1)
ax.axvline(GATE, color="red", ls="--", lw=0.8)
ax.axvline(-GATE, color="red", ls="--", lw=0.8)
ax.set_yticks(y)
labels = forest["feature"].tolist()
ax.set_yticklabels(labels)
ax.set_xlabel("Cliff's δ (high vs low rated)")
ax.set_title("What differs most? (exploratory presentation forest)")
ctx.save_figure(fig, "presentation_forest")
plt.show()

# %% [markdown]
# ## Section 2 — Are better romances simply about more things?
#
# **Exploratory question (not a confirmatory finding):**
#
# > Do higher-rated romance novels distribute narrative attention across a broader range
# > of themes, or are they more concentrated around a few dominant themes?
#
# This is different from asking *which* themes differ. Here we ask how *varied* the
# thematic composition of an entire book is.
#
# **Do not count non-zero topics.** Notebook 00 shows the median BERTopic topic is present
# in ~96.5% of books; longer books also get more chances to touch topics. We instead use:
#
# | Measure | Richer book means |
# | --- | --- |
# | Shannon topic entropy \(H\) | higher |
# | Effective number of themes \(e^H\) | higher (presentation-friendly) |
# | Top-10 concentration | lower |
# | Rarefied richness (same sentence budget) | higher |
#
# Three resolutions: **(A)** fine-grained topics, **(B)** taxonomy leaves (**primary**),
# **(C)** renormalized presentation constructs (`ATTENTION_THEMES`).

# %%
work, richness_meta = tr.compute_all_richness(cfg, work, seed=42, length_quantile=0.10)
print("Richness meta:", richness_meta)

metric_cols = [
    c
    for c in (
        "topic_H",
        "topic_n_eff",
        "topic_top10",
        "taxonomy_H",
        "taxonomy_n_eff",
        "taxonomy_top10",
        "construct_H",
        "construct_n_eff",
        "construct_top10",
        "rare_topic_n_eff",
        "rare_taxonomy_n_eff",
        "rare_construct_n_eff",
        "rarefaction_depth",
    )
    if c in work.columns
]
richness_book = work[["book_id", "rating_class", "rating_shrunk", "n_sentences"] + metric_cols].copy()
display(richness_book[metric_cols].describe().round(3))
ctx.save_table(richness_book, "thematic_richness_book_metrics")
pd.Series(richness_meta).to_frame("value").to_csv(
    ctx.tables_dir / "thematic_richness_meta.csv"
)

# %% [markdown]
# ### Plot 1 — Effective theme number by rating tier
#
# Taxonomy \(e^H\) is the headline exploratory measure; topic and top-10 concentration
# sit beside it for context.

# %%
tier_order = ["low_rate", "mid_rate", "high_rate"]
plot_specs = [
    ("taxonomy_n_eff", "Taxonomy effective # (primary)"),
    ("topic_n_eff", "Topic effective #"),
    ("taxonomy_top10", "Taxonomy top-10 concentration"),
]
plot_specs = [(c, t) for c, t in plot_specs if c in work.columns]

fig, axes = plt.subplots(1, len(plot_specs), figsize=(4.2 * max(len(plot_specs), 1), 4.5))
if len(plot_specs) == 1:
    axes = [axes]
for ax, (col, title) in zip(axes, plot_specs):
    sub = work[["rating_class", col]].dropna()
    sub = sub[sub["rating_class"].isin(tier_order)]
    sns.violinplot(
        data=sub,
        x="rating_class",
        y=col,
        order=tier_order,
        inner="box",
        cut=0,
        ax=ax,
        color="steelblue",
    )
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("")
    ax.set_xticklabels(["low", "mid", "high"])
fig.suptitle("Thematic richness by rating tier (exploratory)", y=1.02)
fig.tight_layout()
ctx.save_figure(fig, "richness_by_rating_tier")
plt.show()

# Tier means for the slide footnote
tier_means = (
    work.loc[work["rating_class"].isin(tier_order)]
    .groupby("rating_class")[
        [c for c in ("taxonomy_n_eff", "topic_n_eff", "construct_n_eff", "taxonomy_top10") if c in work.columns]
    ]
    .mean()
    .reindex(tier_order)
)
display(tier_means.round(2))
ctx.save_table(tier_means.reset_index(), "thematic_richness_tier_means")

# %% [markdown]
# ### Cliff's δ (high vs low)
#
# Positive δ on \(n_{\mathrm{eff}}\) ⇒ a randomly chosen high-rated book tends to be more
# thematically diverse. For top-10 concentration the interesting sign is **negative**
# (less dominated by a few themes).

# %%
cliff_feats = [f for f in tr.RICHNESS_CLIFF_FEATURES if f in work.columns]
rich_cliffs = nh.cliffs_delta_table(work, cliff_feats, n_boot=400, seed=42)
rich_cliffs["note"] = rich_cliffs["feature"].map(
    lambda f: "lower=richer" if "top10" in str(f) else "higher=richer"
)
display(rich_cliffs.round(4))
ctx.save_table(rich_cliffs, "thematic_richness_cliffs_delta")

# %% [markdown]
# ### Length-controlled OLS
#
# Among books of comparable length, era, and genre, does thematic diversity still track
# rating? Author-clustered SEs; reliability weights on quality.

# %%
ols_features = [
    c
    for c in (
        "taxonomy_n_eff",
        "topic_n_eff",
        "construct_n_eff",
        "rare_taxonomy_n_eff",
    )
    if c in work.columns
]
controls = [c for c in ("n_sentences", "publication_year") if c in work.columns]
ols_rows = []
for feat in ols_features:
    fit = mdl.fit_ols(
        work,
        outcome="rating_shrunk",
        predictors=[feat, *controls],
        categorical=("genre_group",) if "genre_group" in work.columns else (),
        cluster="author_id" if "author_id" in work.columns else None,
        weights="reliability" if "reliability" in work.columns else None,
        name=f"richness_{feat}",
    )
    coef = fit.coefficients[fit.coefficients["term"] == feat].iloc[0]
    ols_rows.append(
        {
            "feature": feat,
            "coefficient": float(coef["coefficient"]),
            "std_error": float(coef["std_error"]),
            "p_value": float(coef["p_value"]),
            "ci_low": float(coef["ci_low"]),
            "ci_high": float(coef["ci_high"]),
            "n_obs": fit.n_obs,
            "n_clusters": fit.n_clusters,
            "r_squared": fit.r_squared,
        }
    )
rich_ols = pd.DataFrame(ols_rows)
display(rich_ols.round(4))
ctx.save_table(rich_ols, "thematic_richness_ols")

# %% [markdown]
# ### Rarefaction check
#
# Every eligible book contributes exactly the same number of sentences
# (10th percentile of corpus length). Does taxonomy richness still differ by tier?

# %%
if "rare_taxonomy_n_eff" in work.columns and richness_meta.get("rarefaction_depth"):
    depth = richness_meta["rarefaction_depth"]
    eligible = work.dropna(subset=["rare_taxonomy_n_eff"])
    print(
        f"Rarefaction depth={depth:,} sentences; "
        f"N eligible={len(eligible):,} / {len(work):,}"
    )
    rare_tier = (
        eligible.loc[eligible["rating_class"].isin(tier_order)]
        .groupby("rating_class")[["taxonomy_n_eff", "rare_taxonomy_n_eff", "rare_topic_n_eff"]]
        .mean()
        .reindex(tier_order)
    )
    display(rare_tier.round(3))
    ctx.save_table(rare_tier.reset_index(), "thematic_richness_rarefaction")

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(tier_order))
    wbar = 0.35
    ax.bar(x - wbar / 2, rare_tier["taxonomy_n_eff"], width=wbar, label="full book")
    ax.bar(x + wbar / 2, rare_tier["rare_taxonomy_n_eff"], width=wbar, label="rarefied")
    ax.set_xticks(x)
    ax.set_xticklabels(["low", "mid", "high"])
    ax.set_ylabel("Mean taxonomy $e^H$")
    ax.set_title(f"Full vs rarefied taxonomy richness (depth={depth:,})")
    ax.legend()
    ctx.save_figure(fig, "richness_rarefaction_by_tier")
    plt.show()
else:
    print("Rarefaction metrics unavailable — skip.")

# %% [markdown]
# ### Richness vs the right combination
#
# Does taxonomy breadth still predict rating after the main thematic drivers enter?

# %%
drivers = [
    c
    for c in (
        "RAX_h3_emotional_side",
        "RAX_appearance_grooming",
        "RAX_external_danger_crisis",
        "RAX_tenderness_core",
    )
    if c in work.columns
]
driver_rows = []
if "taxonomy_n_eff" in work.columns:
    for name, preds in (
        ("M1_richness_only", ["taxonomy_n_eff", *controls]),
        ("M2_richness_plus_drivers", ["taxonomy_n_eff", *drivers, *controls]),
    ):
        fit = mdl.fit_ols(
            work,
            outcome="rating_shrunk",
            predictors=preds,
            categorical=("genre_group",) if "genre_group" in work.columns else (),
            cluster="author_id" if "author_id" in work.columns else None,
            weights="reliability" if "reliability" in work.columns else None,
            name=name,
        )
        for _, coef in fit.coefficients.iterrows():
            if coef["term"] == "const":
                continue
            driver_rows.append(
                {
                    "model": name,
                    "term": coef["term"],
                    "coefficient": float(coef["coefficient"]),
                    "std_error": float(coef["std_error"]),
                    "p_value": float(coef["p_value"]),
                    "ci_low": float(coef["ci_low"]),
                    "ci_high": float(coef["ci_high"]),
                    "n_obs": fit.n_obs,
                    "r_squared": fit.r_squared,
                }
            )
rich_vs_drivers = pd.DataFrame(driver_rows)
display(rich_vs_drivers.round(4))
ctx.save_table(rich_vs_drivers, "thematic_richness_vs_drivers")

# %% [markdown]
# ### Nonlinear check — rating by richness decile
#
# Decile 1 = thematically narrowest; 10 = richest. Look for linear rise, inverted-U, or flat.

# %%
decile_tbl = tr.richness_decile_table(work, "taxonomy_n_eff", "rating_shrunk", n_bins=10)
if "quality_resid" in work.columns:
    decile_resid = tr.richness_decile_table(work, "taxonomy_n_eff", "quality_resid", n_bins=10)
    decile_tbl = pd.concat([decile_tbl, decile_resid], ignore_index=True)
display(decile_tbl.round(4))
ctx.save_table(decile_tbl, "thematic_richness_deciles")

if len(decile_tbl):
    fig, ax = plt.subplots(figsize=(7, 4))
    for outcome, sub in decile_tbl.groupby("outcome_col"):
        ax.plot(sub["decile"], sub["outcome_mean"], marker="o", label=outcome)
    ax.set_xlabel("Taxonomy richness decile (1=narrow … 10=rich)")
    ax.set_ylabel("Mean outcome")
    ax.set_title("Rating by thematic-richness decile (exploratory)")
    ax.legend()
    ctx.save_figure(fig, "richness_decile_rating")
    plt.show()

# %% [markdown]
# ### Security × richness
#
# Is the pattern “good novels are richer,” or “breadth **with** sustained emotional
# reassurance”?

# %%
quad = tr.richness_security_quadrants(
    work,
    richness_col="taxonomy_n_eff",
    security_col="RAX_h3_emotional_side" if "RAX_h3_emotional_side" in work.columns else "RAX_emotional_reassurance",
    outcome_col="rating_shrunk",
)
display(quad.round(4))
ctx.save_table(quad, "richness_x_security_quadrants")

if len(quad):
    mat = quad.pivot(index="security_bin", columns="richness_bin", values="mean_rating")
    # Prefer a readable order
    row_order = [r for r in ("low_security", "high_security") if r in mat.index]
    col_order = [c for c in ("low_richness", "high_richness") if c in mat.columns]
    mat = mat.reindex(index=row_order, columns=col_order)
    fig, ax = plt.subplots(figsize=(5.5, 4))
    sns.heatmap(mat, annot=True, fmt=".3f", cmap="YlOrRd", ax=ax)
    ax.set_title("Mean rating_shrunk: security × taxonomy richness")
    ctx.save_figure(fig, "richness_x_security_heatmap")
    plt.show()

# %% [markdown]
# ### Exploratory conclusion (thematic richness)
#
# From the executed numbers above (exploratory only — do **not** promote to NB13):
#
# - Taxonomy effective-theme number differs by rating tier (Cliff’s δ ≈ **+.14**), and
#   fine-grained topic \(e^H\) is larger still (δ ≈ **+.24**), with top-10 concentration
#   lower among high-rated books.
# - After controlling for length, year, and genre, **taxonomy** richness is only
#   marginal (M1 `taxonomy_n_eff` β ≈ 0.0024, p ≈ 0.065); **rarefied** taxonomy
#   richness is essentially null (p ≈ 0.61). So length opportunity explains much of
#   the leaf-level association.
# - Once reassurance, appearance, danger, and tenderness enter (M2), raw
#   `taxonomy_n_eff` **strengthens** (β ≈ 0.0066, p &lt; 0.001) — a suppression
#   pattern, not attenuation. Richness therefore carries *more* independent
#   predictive signal after those drivers are held constant. This remains
#   exploratory: rarefaction still nullifies the leaf-level story, and breadth
#   alone is not a confirmatory H1–H6 finding.
#
# **Presentation line:** higher-rated romance differs in *which* themes receive
# attention (and in security/care mixtures); raw taxonomy breadth also shows a
# suppressed partial association after drivers, but rarefied breadth does not
# survive, so “more themes” is not a clean confirmatory claim.

# %% [markdown]
# ## Section 3 — Where does narrative attention move?
#
# Mean theme-share difference (high − low). Shares are compositional: more of one theme
# implies less of something else. This is a **percentage-point** view, not Cliff's δ.

# %%
waterfall = pres.attention_waterfall(work)
display(waterfall.round(4))
ctx.save_table(waterfall, "attention_waterfall")

fig, ax = plt.subplots(figsize=(9, 5.5))
order = waterfall.sort_values("diff_pp")
colors = ["#4c72b0" if v >= 0 else "#c44e52" for v in order["diff_pp"]]
ax.barh(order["label"], order["diff_pp"], color=colors)
ax.axvline(0, color="gray", lw=1)
ax.set_xlabel("Mean share difference (high − low), percentage points")
ax.set_title("Narrative attention shift (compositional view)")
ctx.save_figure(fig, "attention_waterfall")
plt.show()

# %% [markdown]
# ## Section 4 — Security and care (reuse NB12)
#
# Promise-type comparison and topic forest from Notebook 12, plus topic cards
# (id, label, taxonomy, words, example sentence).

# %%
if len(nb12_promise):
    display(nb12_promise.round(4))
    ctx.save_table(nb12_promise, "promise_type_comparison_reused")
if len(nb12_forest):
    display(nb12_forest.round(4))
    ctx.save_table(nb12_forest, "topic_forest_broad_families_reused")
if len(nb12_presence):
    display(nb12_presence.round(4))
    ctx.save_table(nb12_presence, "presence_vs_intensity_reused")

# Topic cards for security-family topics appearing in NB12 forest
card_topics = []
if len(nb12_forest) and "topic_id" in nb12_forest.columns:
    card_topics = sorted({int(t) for t in nb12_forest["topic_id"].dropna().tolist()})
elif len(nb12_promise):
    # fall back: H3 KEEP topics from claim hierarchy
    card_topics = [29, 46, 56, 96, 242, 128, 170, 119]
else:
    card_topics = [29, 46, 56, 96, 242, 119]

cards = pd.DataFrame([pres.topic_presentation_card(cfg, tid, master) for tid in card_topics[:25]])
display(cards)
ctx.save_table(cards, "security_care_topic_cards")

# %% [markdown]
# ## Section 5 — Appearance
#
# Refined appearance/grooming vs Stage 10 baseline and NB11 robustness variants.

# %%
appearance_rows = []
if len(nb13_effects):
    row = nb13_effects[nb13_effects["feature"] == "RAX_appearance_grooming"]
    if len(row):
        appearance_rows.append(
            {
                "source": "refined_strict_nb13",
                "cliffs_delta": float(row.iloc[0]["cliffs_delta"]),
                "ci_low": float(row.iloc[0]["ci_low"]),
                "ci_high": float(row.iloc[0]["ci_high"]),
                "verdict": row.iloc[0].get("verdict"),
            }
        )
if len(nb11_comp):
    sub = nb11_comp[nb11_comp["feature"].astype(str).str.contains("appearance", case=False, na=False)]
    for _, r in sub.iterrows():
        appearance_rows.append(
            {
                "source": f"nb11:{r.get('spec', r.get('mode', 'component'))}",
                "cliffs_delta": r.get("cliffs_delta"),
                "ci_low": r.get("ci_low"),
                "ci_high": r.get("ci_high"),
                "verdict": r.get("verdict"),
            }
        )
if len(nb11_stab):
    sub = nb11_stab[nb11_stab["feature"].astype(str).str.contains("appearance", case=False, na=False)]
    for _, r in sub.iterrows():
        appearance_rows.append(
            {
                "source": "nb11_stability",
                "cliffs_delta": r.get("min_abs_delta"),
                "ci_low": np.nan,
                "ci_high": np.nan,
                "verdict": f"sign_stable={r.get('sign_stable')}; clears_gate={r.get('any_clears_gate')}",
            }
        )
# Stage 10 freeze retained in config for cross-reference only
_ = cfg.section("stage10_delta_freeze") or {}
appearance_df = pd.DataFrame(appearance_rows)
display(appearance_df)
ctx.save_table(appearance_df, "appearance_summary")

# %% [markdown]
# ## Section 6 — Strict → broad sensitivity (reuse NB12)

# %%
if len(nb12_traj):
    display(nb12_traj.round(4))
    ctx.save_table(nb12_traj, "strict_moderate_broad_trajectories_reused")
    fig, ax = plt.subplots(figsize=(9, 5))
    for family, sub in nb12_traj.groupby("family"):
        sub = sub.set_index("level").reindex(["strict", "moderate", "broad"])
        ax.plot(["strict", "moderate", "broad"], sub["cliffs_delta"], marker="o", label=family)
    ax.axhline(0, color="gray", lw=1)
    ax.axhline(GATE, color="red", ls="--", lw=0.8)
    ax.axhline(-GATE, color="red", ls="--", lw=0.8)
    ax.set_ylabel("Cliff's δ")
    ax.set_title("Strict → moderate → broad (exploratory; from NB12)")
    ax.legend(fontsize=8, ncol=2)
    ctx.save_figure(fig, "strict_moderate_broad_trajectories")
    plt.show()
else:
    print("NB12 trajectories missing — skip Section 6 plot.")

# %% [markdown]
# ## Section 7 — Dose-response curves
#
# Decile of theme share vs residualized quality (after year/length/genre).

# %%
dose = pres.dose_response_panel(work, outcome="quality_resid", n_bins=10)
display(dose.head(20).round(4))
ctx.save_table(dose, "dose_response_curves")

if len(dose):
    features = dose["feature"].unique().tolist()
    n = len(features)
    ncols = 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3.2 * nrows), sharey=False)
    axes = np.atleast_1d(axes).ravel()
    for ax, feat in zip(axes, features):
        sub = dose[dose["feature"] == feat]
        ax.plot(sub["decile"], sub["outcome_mean"], marker="o")
        ax.axhline(0, color="gray", lw=0.8)
        ax.set_title(feat.replace("RAX_", ""), fontsize=9)
        ax.set_xlabel("decile")
        ax.set_ylabel("mean quality_resid")
    for ax in axes[len(features) :]:
        ax.axis("off")
    fig.suptitle("Dose–response: theme decile → residualized quality", y=1.01)
    fig.tight_layout()
    ctx.save_figure(fig, "dose_response_curves")
    plt.show()

# %% [markdown]
# ## Section 8 — Interactions
#
# Reuse NB12 danger×protection (z-scored OLS + median-split 2×2) and care×appearance.
# Conflict×repair removed: strict `RAX_repair` has no meaningful variation.

# %%
if len(nb12_danger):
    display(nb12_danger.round(4))
    ctx.save_table(nb12_danger, "danger_x_protection_reused")
if len(nb12_danger_quad):
    display(nb12_danger_quad.round(4))
    ctx.save_table(nb12_danger_quad, "danger_x_protection_quadrants_reused")
    # Presentation heatmap: strict t119
    sub = nb12_danger_quad[nb12_danger_quad["protection_index"] == "strict t119 only"]
    if len(sub):
        mat = sub.pivot(index="danger_bin", columns="protection_bin", values="mean_rating")
        row_order = [r for r in ("lower_danger", "higher_danger") if r in mat.index]
        col_order = [c for c in ("lower_protection", "higher_protection") if c in mat.columns]
        mat = mat.reindex(index=row_order, columns=col_order)
        fig, ax = plt.subplots(figsize=(5.5, 4))
        sns.heatmap(mat, annot=True, fmt=".3f", cmap="YlOrRd", ax=ax)
        ax.set_title("Mean rating: danger × protection (strict t119; from NB12)")
        ctx.save_figure(fig, "danger_x_protection_heatmap_presentation")
        plt.show()
if len(nb12_care_app):
    display(nb12_care_app.round(4))
    ctx.save_table(nb12_care_app, "care_x_appearance_reused")

# %% [markdown]
# ## Section 9 — Quality versus reach (refined constructs)
#
# Standardised betas on both channels; quadrant labels.

# %%
qr_feats = [f for f in HEADLINE if f in work.columns and nh.gate_for_feature(coverage, f) != "unmeasurable"]
betas = pres.standardized_two_channel_betas(work, qr_feats)
if len(betas):
    wide = betas.pivot(index="feature", columns="channel", values="beta_std").reset_index()
    if {"quality", "reach"} <= set(wide.columns):
        wide["quadrant"] = [
            pres.classify_quality_reach_quadrant(float(q), float(r))
            for q, r in zip(wide["quality"], wide["reach"])
        ]
    display(wide.round(4))
    ctx.save_table(wide, "quality_reach_standardized_betas")
    ctx.save_table(betas, "quality_reach_betas_long")

    fig, ax = plt.subplots(figsize=(7.5, 6))
    ax.axhline(0, color="gray", lw=0.8)
    ax.axvline(0, color="gray", lw=0.8)
    ax.scatter(wide["reach"], wide["quality"], s=40)
    for _, r in wide.iterrows():
        ax.annotate(str(r["feature"]).replace("RAX_", "").replace("RLR_", ""), (r["reach"], r["quality"]), fontsize=7)
    ax.set_xlabel("Standardised β → reach")
    ax.set_ylabel("Standardised β → quality")
    ax.set_title("Refined constructs: quality vs reach")
    ctx.save_figure(fig, "quality_reach_quadrants")
    plt.show()

# %% [markdown]
# ## Section 10 — Residual Goodreads quadrants
#
# Better/worse rated than expected × more/less reached than expected
# (after year, length, genre).

# %%
quad_counts = work["residual_quadrant"].value_counts().rename_axis("quadrant").reset_index(name="n")
display(quad_counts)
ctx.save_table(quad_counts, "residual_quadrant_counts")

theme_means = pres.quadrant_theme_means(work, list(pres.ATTENTION_THEMES[i][0] for i in range(len(pres.ATTENTION_THEMES))))
display(theme_means.round(5))
ctx.save_table(theme_means, "residual_quadrant_theme_means")

# Cliff's δ of themes: stars vs popular_but_poor as a presentation contrast
from src.stage10_correlation_analysis.analysis.effects import cliffs_delta

contrast_rows = []
stars = work[work["residual_quadrant"] == "stars"]
poor_pop = work[work["residual_quadrant"] == "popular_but_poor"]
gems = work[work["residual_quadrant"] == "hidden_gems"]
for feat, label in pres.ATTENTION_THEMES:
    if feat not in work.columns:
        continue
    for name, a, b in (
        ("stars_vs_popular_but_poor", stars, poor_pop),
        ("hidden_gems_vs_low_low", gems, work[work["residual_quadrant"] == "low_low"]),
    ):
        aa = a[feat].dropna().to_numpy(dtype=float)
        bb = b[feat].dropna().to_numpy(dtype=float)
        if aa.size < 30 or bb.size < 30:
            continue
        contrast_rows.append(
            {
                "contrast": name,
                "feature": feat,
                "label": label,
                "cliffs_delta": float(cliffs_delta(aa, bb)),
                "n_a": int(aa.size),
                "n_b": int(bb.size),
            }
        )
contrast_df = pd.DataFrame(contrast_rows)
display(contrast_df.round(4))
ctx.save_table(contrast_df, "residual_quadrant_theme_deltas")

# %% [markdown]
# ## Section 11 — Genre / era stability heatmap

# %%
heat = pres.subgroup_cliffs_heatmap(work, list(pres.HEADLINE_THEMES_FOR_HEATMAP))
display(heat.head(20).round(4))
ctx.save_table(heat, "genre_era_subgroup_deltas")

if len(heat):
    heat["col"] = heat["group_type"].str.replace("_", " ") + ": " + heat["group"]
    mat = heat.pivot_table(index="feature", columns="col", values="cliffs_delta")
    fig, ax = plt.subplots(figsize=(max(8, 0.7 * mat.shape[1]), max(4, 0.45 * mat.shape[0])))
    sns.heatmap(mat, cmap="RdBu_r", center=0, ax=ax, annot=False)
    ax.set_title("Cliff's δ within genre / era subgroups")
    ctx.save_figure(fig, "genre_era_stability_heatmap")
    plt.show()

# %% [markdown]
# ## Section 12 — Representative books and sentences
#
# Deterministic 2×2 (high/low theme × high/low rating). Sentences from evidence packets
# for the construct's mapped topics — fixed seed, no cherry-picking.

# %%
EXAMPLE_FEATURES = [
    "RAX_appearance_grooming",
    "RAX_h3_emotional_side",
    "RAX_external_danger_crisis",
    "RAX_external_protection",
]
example_books = []
example_sents = []
for feat in EXAMPLE_FEATURES:
    if feat not in work.columns:
        continue
    sampled = pres.sample_theme_book_cells(work, feat, books_per_cell=2, seed=42)
    sampled = sampled.assign(feature=feat)
    example_books.append(sampled.copy())
    # Attach one packet sentence from a KEEP topic when available
    # Appearance KEPT topics / emotional KEEP / danger uses forest topics / protection t119
    topic_map = {
        "RAX_appearance_grooming": [18, 77, 171],
        "RAX_h3_emotional_side": [46, 56, 29],
        "RAX_external_danger_crisis": [],
        "RAX_external_protection": [119],
    }
    tids = list(topic_map.get(feat) or [])
    if not tids and feat == "RAX_external_danger_crisis" and "topic_id" in master.columns:
        # Prefer topics already shown in NB12 forest if available
        if len(nb12_forest) and "topic_id" in nb12_forest.columns:
            tids = [int(t) for t in nb12_forest["topic_id"].dropna().tolist()[:3]]
    for tid in tids[:2]:
        card = pres.topic_presentation_card(cfg, tid, master)
        example_sents.append({"feature": feat, **card})

if example_books:
    books_df = pd.concat(example_books, ignore_index=True)
    display(books_df.head(20))
    ctx.save_table(books_df, "representative_books_2x2")
if example_sents:
    sents_df = pd.DataFrame(example_sents)
    display(sents_df)
    ctx.save_table(sents_df, "representative_topic_sentences")

print(
    "Notebook 14 complete. Exploratory only — does not alter Notebook 13 / H1–H6 verdicts."
)
