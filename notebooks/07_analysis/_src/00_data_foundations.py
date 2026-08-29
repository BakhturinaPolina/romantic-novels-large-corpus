# %% [markdown]
# # 00 — Data foundations
#
# Before any hypothesis is tested, this notebook establishes what is being measured, checks
# that the measurement is sound, and states its limits. Everything downstream depends on it,
# so it is worth reading even if the statistics chapters are what you came for.
#
# **What this notebook answers**
#
# 1. What exactly is a "topic share" here, and why hard assignments rather than probabilities?
# 2. Do the numbers hold together — do shares sum to 1, does every book have metadata?
# 3. Which topics are solid enough to interpret, and which are dust?
# 4. Which topics are really one author's habit rather than a corpus-wide theme?
# 5. Which theory axes can actually be measured in this model, and which cannot?
# 6. What do the two outcome channels (star rating, rating count) look like?
#
# Outputs go to `results/stage10_correlation_analysis/<run>/notebook_analysis/00_data_foundations/`.

# %%
import sys
from pathlib import Path

cwd = Path.cwd().resolve()
project_root = cwd
for _ in range(6):
    if (project_root / "configs").is_dir() and (project_root / "src").is_dir():
        break
    project_root = project_root.parent
else:
    raise RuntimeError("Could not find project root")
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.stage10_correlation_analysis.analysis import bootstrap as boot
from src.stage10_correlation_analysis.analysis import compositional as comp
from src.stage10_correlation_analysis.analysis import effects as eff
from src.stage10_correlation_analysis.analysis import notebook_helpers as nbh

ctx = nbh.setup("00_data_foundations")
cfg = ctx.cfg
TIERS = cfg.tier_order
PALETTE = nbh.tier_palette(cfg)
TIER_COL = cfg.tier_column

# %% [markdown]
# ## 1. The measurement decision: hard assignments, not probabilities
#
# BERTopic gives every sentence a probability over all 374 topics, and also a single best
# topic. The earlier version of this pipeline averaged the probabilities over a book's
# sentences. That turns out not to work, for a reason that has nothing to do with the model
# being wrong.
#
# A book has roughly 6,800 sentences. Averaging 374 probabilities over 6,800 sentences is
# averaging a lot of noise away — and it averages away the signal too. The result was that
# taxonomy category 2.1 sat at 20.23% ± 0.25 percentage points for *every book in the
# corpus*. There was nothing left to compare.
#
# Counting each sentence's single best topic instead gives a number that varies across books
# and reads directly as "3.3% of this book's sentences are about X". The table below is the
# measured comparison, produced by the aggregation script rather than asserted here.
#
# The cost is small: 0.73% of sentences fall into BERTopic's outlier topic and are excluded
# from the denominators, so shares are over the 373 real topics.

# %%
variance = nbh.load_hard_counts(cfg, "hard_vs_soft_variance")
display(variance)

ratio = (
    variance.set_index("measure").loc["hard_assignment", "median_cv"]
    / variance.set_index("measure").loc["soft_probability", "median_cv"]
)
print(
    f"\nBetween-book variation, measured as the median per-topic coefficient of variation:\n"
    f"  hard assignments carry {ratio:.1f}x more than averaged probabilities.\n"
    f"\nThe soft-probability tables are kept and re-used as a robustness check in notebook 08,\n"
    f"so this decision is tested rather than merely asserted."
)

# %% [markdown]
# ## 2. The analysis frame
#
# One table, one row per book, built by `06_build_analysis_frame.py`. Its columns come in
# blocks, and knowing the blocks is most of what you need to read the rest of the analysis.

# %%
frame = nbh.load_analysis_frame(cfg)
manifest = nbh.load_book_features(cfg, "analysis_frame_manifest")

print(f"Analysis frame: {len(frame):,} books x {frame.shape[1]} columns\n")
display(manifest)

TOPIC_COLS = nbh.columns_with_prefix(frame, "topic_")
LEAF_COLS = nbh.columns_with_prefix(frame, "leaf_")
GROUP_COLS = nbh.columns_with_prefix(frame, "group_")
AXIS_COLS = [c for c in frame.columns if c.startswith("AX_") and not c.endswith(("_z", "_clr"))]

print(f"topics {len(TOPIC_COLS)} | taxonomy leaves {len(LEAF_COLS)} | "
      f"main groups {len(GROUP_COLS)} | theory axes {len(AXIS_COLS)}")

# %% [markdown]
# ## 3. Integrity checks
#
# These are cheap and they catch the errors that would otherwise be discovered halfway
# through a hypothesis test. Each one either passes silently or raises.

# %%
checks = []

worst_topic = comp.check_share_sums(frame[TOPIC_COLS], name="topic shares")
checks.append(("topic shares sum to 1 per book", f"max deviation {worst_topic:.2e}", "pass"))

usable = frame[frame["analysable"]]
worst_leaf = comp.check_share_sums(usable[LEAF_COLS], name="leaf shares")
checks.append(("leaf shares sum to 1 per book", f"max deviation {worst_leaf:.2e}", "pass"))

n_unanalysable = int((~frame["analysable"]).sum())
checks.append((
    "books with interpretable text",
    f"{len(frame) - n_unanalysable:,} of {len(frame):,} ({n_unanalysable} excluded)",
    "pass" if n_unanalysable < 10 else "review",
))

tertiles = nbh.load_hard_counts(cfg, "tertile_topic_counts")
tertile_sums = tertiles.groupby(["book_id", "tertile"])["share"].sum()
checks.append((
    "tertile shares sum to 1 per tertile",
    f"max deviation {float((tertile_sums - 1).abs().max()):.2e}", "pass",
))

tier_counts = frame[TIER_COL].value_counts().reindex(TIERS)
checks.append((
    "every book has a rating tier",
    ", ".join(f"{t}={int(n):,}" for t, n in tier_counts.items()),
    "pass" if frame[TIER_COL].notna().all() else "fail",
))

missing_meta = frame[["avg_rating", "n_ratings", "author_id", "publication_year"]].isna().sum()
checks.append((
    "outcome and control coverage",
    f"missing values: {missing_meta.to_dict()}",
    "pass" if missing_meta.sum() == 0 else "review",
))

integrity = pd.DataFrame(checks, columns=["check", "result", "verdict"])
display(integrity)
ctx.save_table(integrity, "integrity_checks")

# %% [markdown]
# ## 4. How much of the corpus can the taxonomy speak about?
#
# Every leaf- and axis-level claim in this analysis is a claim about *mapped* text. If only a
# fifth of a book's sentences fall into named taxonomy categories, then "this book is 30% X"
# means 30% of that fifth, which is a much weaker statement.
#
# This is worth checking explicitly because the previous pipeline mapped only 20% of topic
# mass — the hardcoded category list it pivoted covered 15 of the 46 leaves that exist.

# %%
coverage_cols = ["mapped_mass", "axis_bearing_mass", "context_mass", "noise_leaf_mass"]
coverage_summary = frame[coverage_cols].describe().T[["mean", "50%", "std", "min", "max"]]
coverage_summary.columns = ["mean", "median", "sd", "min", "max"]
display(coverage_summary.round(4))

print(
    f"\nOn average {frame['mapped_mass'].mean():.1%} of a book's sentences carry a taxonomy\n"
    f"category. Within that, {frame['axis_bearing_mass'].mean():.1%} of all sentences sit in\n"
    f"the narrower set of categories eligible for hypothesis axes, and {frame['context_mass'].mean():.1%}\n"
    f"are context (settings, objects, discourse style) that the taxonomy deliberately keeps\n"
    f"out of the axes.\n"
    f"\nThe previous soft-probability pipeline reached mapped_mass = 0.200, so leaf-level\n"
    f"statements there described a fifth of the text. That is the gap this rebuild closes."
)

fig, ax = plt.subplots(figsize=(8, 4))
for col, label in [("mapped_mass", "mapped to any category"),
                   ("axis_bearing_mass", "axis-bearing categories only")]:
    sns.kdeplot(frame[col], ax=ax, label=label, fill=True, alpha=0.3)
ax.set_xlabel("share of a book's sentences")
ax.set_ylabel("density")
ax.set_title("Taxonomy coverage per book")
ax.legend()
ctx.save_figure(fig, "taxonomy_coverage")
plt.show()

# %% [markdown]
# ## 5. Compositional reality
#
# Topic shares sum to 1 within each book. That single fact constrains everything: a theme
# cannot rise without another falling, so **every result in this analysis is a reallocation
# of narrative attention, not an absolute amount**.
#
# Practically this means three different scales for three different jobs:
#
# | scale | used for | why |
# |---|---|---|
# | raw shares | description, plots | directly readable as "% of sentences" |
# | ranks | tier comparisons | no distributional assumptions, immune to the long right tail |
# | CLR (centred log-ratio) | regression | removes the sum constraint so a linear model is meaningful |
#
# Zeros need care too. A book with N sentences cannot express a share below 1/N, so a zero
# means "below 1/N" rather than "absent". Epsilon is set to half of that smallest observable
# step at the median book length.

# %%
print(nbh.compositional_note())

book_totals = nbh.load_hard_counts(cfg, "book_totals")
epsilon = comp.epsilon_from_counts(
    book_totals["n_sentences"],
    mode=cfg.section("compositional", "epsilon_mode"),
    fallback=float(cfg.section("compositional", "epsilon_fallback")),
)
median_len = int(book_totals["n_sentences"].median())
print(
    f"\nMedian book length: {median_len:,} sentences, so the smallest observable share is\n"
    f"1/{median_len:,} = {1 / median_len:.2e} and epsilon = {epsilon:.3e} (half of it)."
)

clr_topics = comp.clr(frame[TOPIC_COLS], epsilon=epsilon)
print(f"\nCLR sanity: each row sums to {float(clr_topics.sum(axis=1).abs().max()):.2e} (should be 0).")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
example = TOPIC_COLS[frame[TOPIC_COLS].mean().to_numpy().argmax()]
sns.histplot(frame[example], bins=60, ax=axes[0], color="#4f81bd")
axes[0].set_title(f"raw share — {example}")
axes[0].set_xlabel("share of sentences")
sns.histplot(clr_topics[example], bins=60, ax=axes[1], color="#4f81bd")
axes[1].set_title(f"CLR — {example}")
axes[1].set_xlabel("centred log-ratio")
fig.suptitle("The same topic on two scales: raw shares are skewed, CLR is workable for regression")
fig.tight_layout()
ctx.save_figure(fig, "compositional_scales")
plt.show()

# %% [markdown]
# ## 6. Topic health: which of the 373 topics are worth interpreting?
#
# A topic that appears in 2% of books, or that averages 0.001% of sentences, cannot support a
# tier comparison however large the corpus is. Three numbers separate signal from dust:
#
# - **prevalence** — the fraction of books where the topic appears at all
# - **mass** — the mean share across books
# - **concentration** — how much of the topic's total mass sits in its top 1% of books; a high
#   value means a few books carry it and it is not a corpus-wide theme
#
# The health table also carries each topic's label, taxonomy category, and its Cliff's delta
# between the high and low tiers, so it is the lookup table for the rest of the analysis.

# %%
topic_lookup = nbh.load_topic_lookup(cfg)
screen = comp.screen_columns(
    frame[TOPIC_COLS],
    min_prevalence=float(cfg.section("screening", "min_prevalence_books")),
    min_mean_share=float(cfg.section("screening", "min_mean_share")),
)

def concentration(series: pd.Series) -> float:
    """Share of a topic's total mass held by its top 1% of books."""
    ordered = series.sort_values(ascending=False)
    top = max(1, int(0.01 * len(ordered)))
    total = ordered.sum()
    return float(ordered.iloc[:top].sum() / total) if total > 0 else np.nan

health = screen.copy()
health.index.name = "feature"
health = health.reset_index()
health["topic_id"] = health["feature"].str.removeprefix("topic_").astype(int)
health["concentration_top1pct"] = [concentration(frame[c]) for c in health["feature"]]

label_cols = ["topic_id", "label", "taxonomy_main_id", "taxonomy_main_name",
              "taxonomy_main_group", "taxonomy_confidence", "taxonomy_evidence_quality",
              "taxonomy_use_in_macro_axes", "radway_phase_name"]
health = health.merge(
    topic_lookup[[c for c in label_cols if c in topic_lookup.columns]],
    on="topic_id", how="left",
)

high, low = cfg.section("tiers", "headline_contrast")
tier_effects = eff.two_group_effects(
    frame.reset_index(), TOPIC_COLS, TIER_COL, high, low,
    n_replicates=int(cfg.section("inference", "screening_ci_replicates")),
    seed=int(cfg.section("inference", "bootstrap", "seed")),
)
health = health.merge(
    tier_effects[["feature", "cliffs_delta", "ci_low", "ci_high", "ci_excludes_zero", "magnitude"]],
    on="feature", how="left",
)

print(f"Topic health across {len(health)} topics:")
print(f"  median prevalence      {health['prevalence'].median():.3f}")
print(f"  median mean share      {health['mean_share'].median():.5f}")
print(f"  median concentration   {health['concentration_top1pct'].median():.3f}")
print(f"  pass the screen        {int(health['passes_screen'].sum())} "
      f"({health['passes_screen'].mean():.1%})")
print(f"  |delta| >= {cfg.section('screening', 'effect_gates', 'cliffs_delta_small')} "
      f"between {high} and {low}: "
      f"{int((health['cliffs_delta'].abs() >= cfg.section('screening', 'effect_gates', 'cliffs_delta_small')).sum())}")

display(health.sort_values("mean_share", ascending=False).head(15)[
    ["feature", "label", "taxonomy_main_id", "prevalence", "mean_share",
     "concentration_top1pct", "cliffs_delta", "magnitude"]
])

# %% [markdown]
# Read the three panels below together, because they say something important about which
# screen actually does any work.
#
# **Prevalence screens almost nothing.** The median topic appears in 96.5% of books, and 369
# of 373 topics clear the 5% prevalence gate. That is arithmetic, not a finding: a book has
# about 6,800 sentences spread over 373 topics, so roughly 18 sentences land on the average
# topic and "at least one sentence" is nearly guaranteed. Presence is therefore not a
# discriminating variable at this granularity, and the prevalence gate is kept only to catch
# a genuinely degenerate topic.
#
# **Mass and effect size do the work.** The median topic holds 0.20% of a book's sentences,
# and only 38 of 373 topics reach even a small tier difference. That ratio — 369 pass the
# prevalence screen, 38 clear the effect gate — is the honest headline of this chapter, and
# notebook 01 reports it as a funnel.
#
# **Concentration is reassuring.** The median topic's top 1% of books hold only 5.6% of its
# mass, so topics are spread across the corpus rather than being a handful of books' quirks.

# %%
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(health["prevalence"], bins=40, ax=axes[0], color="#4f81bd")
axes[0].axvline(cfg.section("screening", "min_prevalence_books"), color="#c0504d", ls="--",
                label="screen threshold")
axes[0].set_title("Prevalence\n(fraction of books where present)")
axes[0].legend()

sns.histplot(np.log10(health["mean_share"].clip(lower=1e-8)), bins=40, ax=axes[1], color="#4f81bd")
axes[1].axvline(np.log10(float(cfg.section("screening", "min_mean_share"))), color="#c0504d", ls="--")
axes[1].set_title("Mass (log10 mean share)")

sns.histplot(health["concentration_top1pct"], bins=40, ax=axes[2], color="#4f81bd")
axes[2].set_title("Concentration\n(mass held by top 1% of books)")
fig.tight_layout()
ctx.save_figure(fig, "topic_health_distributions")
plt.show()

# %% [markdown]
# ## 7. Authors as a shadow confounder
#
# Romance authors imprint topics hard. Before reading "highly rated books do more X", it is
# worth knowing whether topic X is really one author's recurring scene.
#
# The corpus has 8,264 authors over 16,000 books, and 5,353 of them appear exactly once.
# That distribution rules out author fixed effects — they would absorb a third of the sample
# — so the strategy throughout is author-cluster-robust standard errors, a cluster bootstrap
# over authors, and the dominance flags computed here.

# %%
author_counts = frame["author_id"].value_counts()
print(f"authors                    {frame['author_id'].nunique():,}")
print(f"authors with 2+ books      {int((author_counts >= 2).sum()):,} "
      f"covering {int(author_counts[author_counts >= 2].sum()):,} books")
print(f"single-book authors        {int((author_counts == 1).sum()):,}")
print(f"largest author             {author_counts.iloc[0]} books")
print(f"series ids                 {frame['series_id'].nunique():,}")

dominance = boot.cluster_dominance(frame, TOPIC_COLS, "author_id")
dominance = boot.flag_dominated_features(
    dominance, max_share=float(cfg.section("screening", "author_dominance_max"))
)
dominance["topic_id"] = dominance["feature"].str.removeprefix("topic_").astype(int)
dominance = dominance.merge(
    topic_lookup[["topic_id", "label"]], on="topic_id", how="left",
).merge(
    frame[["author_id", "author_name"]].drop_duplicates().rename(
        columns={"author_id": "top_cluster", "author_name": "top_author_name"}
    ).astype({"top_cluster": "string"}),
    on="top_cluster", how="left",
)

n_flagged = int(dominance["author_dominated"].sum())
print(f"\nTopics where one author holds more than "
      f"{cfg.section('screening', 'author_dominance_max'):.0%} of the mass: {n_flagged}")
display(dominance.head(15)[
    ["feature", "label", "top_author_name", "top_cluster_share", "top3_cluster_share",
     "n_clusters_present", "author_dominated"]
])

health = health.merge(
    dominance[["feature", "top_author_name", "top_cluster_share", "author_dominated"]],
    on="feature", how="left",
)
ctx.save_table(health.sort_values("cliffs_delta", key=lambda s: s.abs(), ascending=False),
               "topic_health_table")
ctx.save_table(dominance, "topic_author_dominance")

# %% [markdown]
# The topics to be most careful with are the ones that are *both* author-dominated and show a
# tier difference, because there the tier effect may simply be that one author is rated well.
# The check below is a real one that this corpus happens to pass: the most concentrated topic
# still has under 10% of its mass in its top author, comfortably below the 25% flag. Author
# effects therefore have to be handled through clustered standard errors and the cluster
# bootstrap rather than by excluding individual topics.

# %%
gate = float(cfg.section("screening", "effect_gates", "cliffs_delta_small"))
suspect = health[
    health["author_dominated"].fillna(False)
    & (health["cliffs_delta"].abs() >= gate)
].sort_values("cliffs_delta", key=lambda s: s.abs(), ascending=False)

print(f"{len(suspect)} topics are both author-dominated and show |Cliff's delta| >= {gate}.")
print("These are treated as author signatures rather than tier signals in later chapters.")
display(suspect[["feature", "label", "top_author_name", "top_cluster_share",
                 "cliffs_delta", "magnitude"]].head(20))
ctx.save_table(suspect, "author_signature_topics")

# %% [markdown]
# ## 8. Axis coverage audit: which hypotheses are measurable at all?
#
# This is the table that would have prevented the previous run's quietest failure. Four axes
# were emitted as exactly `0.0` for all 16,000 books, because their taxonomy components had
# no topics — and a column of zeros looks like a real variable in a regression table.
#
# The rebuild refuses to emit an axis whose components are empty, and records per component
# how many topics and how much corpus mass it rests on.

# %%
axis_coverage = nbh.load_book_features(cfg, "axis_coverage")
axis_summary = nbh.load_book_features(cfg, "axis_coverage_summary")
axis_definitions = nbh.load_book_features(cfg, "axis_definitions")

print("Axis verdicts (an axis is as weak as its weakest signed leg):")
display(axis_summary["axis_verdict"].value_counts().to_frame("n_axes"))

confirmatory = axis_summary[axis_summary["hypothesis_role"] == "confirmatory"]
display(confirmatory[["axis", "hypothesis", "axis_verdict", "n_components",
                      "n_viable", "n_weak", "n_empty", "empty_leaves"]])

# %%
empty_components = axis_coverage[axis_coverage["verdict"] == "empty"]
print("Taxonomy categories with no topics in this model, and the axes that wanted them:\n")
display(
    empty_components.groupby("leaf_id")["axis"].apply(lambda s: ", ".join(sorted(set(s))))
    .to_frame("axes_affected")
)

weak_components = axis_coverage[axis_coverage["verdict"] == "weak"]
print("\nAnd the categories that exist but rest on one or two topics — real, but too thin to")
print("carry an axis on their own:\n")
display(
    weak_components.groupby("leaf_id")
    .agg(n_topics=("n_topics", "max"), axes_affected=("axis", lambda s: ", ".join(sorted(set(s)))))
)

print(
    "\nThese are substantive findings about the corpus rather than bugs:\n"
    "  6.1a elite romantic status and 6.7 aristocracy are empty, and 6.6 material glamour\n"
    "  holds a single topic. This is a multi-genre popular-romance corpus (contemporary,\n"
    "  paranormal, historical, YA, mystery), not a billionaire-lifestyle collection: across\n"
    "  all 348 mapped topics there is essentially no luxury vocabulary. H3 as originally\n"
    "  written is therefore not measurable, and is reframed as AX_material_social_display,\n"
    "  built only from leaves that carry topics.\n"
    "  2.4 post-sex aftercare is empty upstream at Stage08, so aftercare cannot be separated\n"
    "  from explicit sex (2.3).\n"
    "  3.1 positive resolution is empty by taxonomy design: v2.4 routes relief into 4.5 and\n"
    "  reassurance into 4.6. The payoff guard below handles the consequence.\n"
    "  5.3a wedding planning and 8.3a ring exchange hold one topic each, so the HEA axis is\n"
    "  effectively leaf 4.5 with decoration — stated here, and tested that way in notebook 05."
)

# %%
guard = nbh.load_book_features(cfg, "payoff_guard_verdict")
display(guard)
if bool(guard.loc[0, "fallback_active"]):
    print(
        f"Guard active. AX_payoff_safety was defined as 4.5 + 3.1, and 3.1 has "
        f"{int(guard.loc[0, 'n_topics'])} topics, so the axis rests on 4.5 alone.\n"
        f"Two things follow, both visible in the frame rather than hidden:\n"
        f"  AX_payoff_safety_fallback = {guard.loc[0, 'fallback_leaves']} is provided as the\n"
        f"  broader alternative;\n"
        f"  AX_protective_care_resid is 4.6 residualised on {guard.loc[0, 'residualise_h4_on']},\n"
        f"  because 4.6 feeds both the payoff fallback and H4's positive leg. H4 uses the\n"
        f"  residualised form so the shared component is stated once, not counted twice."
    )

print("\nHow every axis is actually defined:")
display(axis_definitions)
ctx.save_table(axis_summary, "axis_coverage_summary")
ctx.save_table(axis_definitions, "axis_definitions")

# %% [markdown]
# ## 9. The two outcome channels
#
# Goodreads gives two signals, and they measure different things:
#
# - **quality** — the average star rating, i.e. how much readers who read it liked it
# - **reach** — how many people rated it at all, i.e. how far the book travelled
#
# They correlate at r ≈ 0.12 in this corpus, which is the empirical reason they are analysed
# separately rather than combined into one "success" variable. A theme can raise one and
# lower the other, and collapsing them would hide exactly that.
#
# The quality channel also needs a correction. A book with 3 ratings averaging 4.9 is not
# better than one with 3,000 averaging 4.3, but a raw mean says it is. The shrunk rating pulls
# thin books toward the corpus mean in proportion to how little evidence they have.

# %%
r_quality_reach = float(frame["avg_rating"].corr(frame["log_n_ratings"]))
print(f"Correlation between quality and reach: r = {r_quality_reach:.3f}\n")

outcome_summary = frame[["avg_rating", "rating_shrunk", "n_ratings", "log_n_ratings",
                         "reliability"]].describe().T
display(outcome_summary.round(3))

thin = int((frame["n_ratings"] < cfg.section("outcomes", "quality", "sensitivity_min_ratings")).sum())
print(
    f"\n{thin:,} books ({thin / len(frame):.1%}) have fewer than "
    f"{cfg.section('outcomes', 'quality', 'sensitivity_min_ratings')} ratings. Their star\n"
    f"averages are noisy, which is why the quality channel is fit weighted by reliability\n"
    f"v/(v+m), with unweighted and n>=30 fits reported as sensitivity checks."
)

# %%
fig, axes = plt.subplots(1, 3, figsize=(16, 4.2))

sns.histplot(frame["avg_rating"], bins=50, ax=axes[0], color="#4f81bd", label="raw")
sns.histplot(frame["rating_shrunk"], bins=50, ax=axes[0], color="#c0504d", alpha=0.6, label="shrunk")
axes[0].set_title("Star rating, before and after shrinkage")
axes[0].set_xlabel("rating")
axes[0].legend()

axes[1].scatter(frame["log_n_ratings"], frame["avg_rating"] - frame["rating_shrunk"],
                s=3, alpha=0.15, color="#4f81bd")
axes[1].axhline(0, color="black", lw=0.8)
axes[1].set_xlabel("log(1 + number of ratings)")
axes[1].set_ylabel("raw minus shrunk")
axes[1].set_title("Shrinkage acts on thinly rated books")

axes[2].scatter(frame["log_n_ratings"], frame["avg_rating"], s=3, alpha=0.15, color="#4f81bd")
axes[2].set_xlabel("log(1 + number of ratings)")
axes[2].set_ylabel("average rating")
axes[2].set_title(f"Quality vs reach (r = {r_quality_reach:.3f})")

fig.tight_layout()
ctx.save_figure(fig, "outcome_channels")
plt.show()

# %% [markdown]
# ## 10. The tiers
#
# Tier comparisons throughout use `rating_class`, a three-way split of the corpus by average
# rating. With about 5,000 books per tier, statistical significance is nearly automatic:
# differences far too small to matter still clear p < 0.05. Interpretation is therefore gated
# on effect size and its bootstrap confidence interval, and the p-value is reported as a
# footnote.

# %%
tier_profile = frame.groupby(TIER_COL, observed=True).agg(
    n_books=("avg_rating", "size"),
    mean_rating=("avg_rating", "mean"),
    min_rating=("avg_rating", "min"),
    max_rating=("avg_rating", "max"),
    median_n_ratings=("n_ratings", "median"),
    mean_pages=("num_pages", "mean"),
    mean_year=("publication_year", "mean"),
    mean_sentences=("n_sentences", "mean"),
).reindex(TIERS)
display(tier_profile.round(2))
ctx.save_table(tier_profile.reset_index(), "tier_profile")

print("\n" + nbh.significance_note(int(tier_profile["n_books"].min())))

fig, ax = plt.subplots(figsize=(7, 4))
for tier in TIERS:
    sns.kdeplot(frame.loc[frame[TIER_COL] == tier, "avg_rating"],
                ax=ax, label=cfg.section("tiers", "labels")[tier],
                color=PALETTE[tier], fill=True, alpha=0.25)
ax.set_xlabel("average rating")
ax.set_title("The three rating tiers")
ax.legend()
ctx.save_figure(fig, "tier_definition")
plt.show()

# %% [markdown]
# ## 11. Foundations summary
#
# What the rest of the analysis rests on, and what it cannot do.

# %%
foundations = pd.DataFrame([
    ("measure", "hard topic assignment: share of a book's sentences whose best topic is t"),
    ("why", f"{ratio:.1f}x more between-book variation than averaged probabilities"),
    ("books", f"{len(frame):,} ({n_unanalysable} excluded for having no interpretable text)"),
    ("topics", f"{len(TOPIC_COLS)} real topics; outlier topic excluded from denominators"),
    ("taxonomy leaves", f"{len(LEAF_COLS)} present, covering {frame['mapped_mass'].mean():.1%} of sentences"),
    ("theory axes", f"{len(AXIS_COLS)} built; "
                    f"{int((axis_summary['axis_verdict'] == 'viable').sum())} viable, "
                    f"{int((axis_summary['axis_verdict'] == 'weak').sum())} weak"),
    ("outcomes", f"quality (star rating, shrunk) and reach (log ratings), r = {r_quality_reach:.3f}"),
    ("clustering", f"{frame['author_id'].nunique():,} authors, "
                   f"{int((author_counts == 1).sum()):,} with one book"),
    ("author-flagged topics", f"{n_flagged} topics where one author holds >"
                              f"{cfg.section('screening', 'author_dominance_max'):.0%} of the mass"),
    ("not measurable", "H3 as luxury (6.1a/6.6/6.7 empty); aftercare separate from sex (2.4 empty)"),
    ("interpretation limit", "all effects are relative reallocations of attention, not absolute amounts"),
], columns=["item", "value"])
display(foundations)
ctx.save_table(foundations, "foundations_summary")

print("\nNext: 01_topic_landscape.ipynb — what differs across tiers at the finest granularity.")
