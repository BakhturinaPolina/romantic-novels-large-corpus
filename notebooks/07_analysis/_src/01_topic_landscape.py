# %% [markdown]
# # 01 — Topic landscape
#
# **The question**: at the finest granularity the model offers — 373 individual topics — what
# actually differs between books readers rate highly and books they rate poorly?
#
# This is deliberately the least theory-laden chapter. No composites, no hypotheses, no
# taxonomy grouping. Just: take each topic in turn, compare its share of sentences between
# the high-rated and low-rated thirds of the corpus, and see what survives.
#
# Starting here matters. If the theory axes in later chapters show effects that no individual
# topic shows, the axes are manufacturing signal. And if a topic-level effect is strong but
# vanishes once grouped into a taxonomy category, the grouping is what destroyed it. This
# chapter is the reference point for both.
#
# **How to read the results.** With about 5,000 books in each tier, statistical significance
# is nearly free — the interesting question is never "is it significant" but "is it big enough
# to notice". So the reporting order throughout is: effect size first, confidence interval
# second, p-value as a footnote.

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

from src.stage10_correlation_analysis.analysis import compositional as comp
from src.stage10_correlation_analysis.analysis import effects as eff
from src.stage10_correlation_analysis.analysis import notebook_helpers as nbh
from src.stage10_correlation_analysis.analysis import tests as tst

ctx = nbh.setup("01_topic_landscape")
cfg = ctx.cfg
TIERS = cfg.tier_order
TIER_COL = cfg.tier_column
PALETTE = nbh.tier_palette(cfg)
HIGH, LOW = cfg.section("tiers", "headline_contrast")

frame = nbh.load_analysis_frame(cfg).reset_index()
topic_lookup = nbh.load_topic_lookup(cfg)
TOPIC_COLS = nbh.columns_with_prefix(frame, "topic_")
LABELS = nbh.topic_label_map(topic_lookup)

print(f"\n{len(frame):,} books, {len(TOPIC_COLS)} topics.")
print(f"Headline contrast: {HIGH} (n={int((frame[TIER_COL] == HIGH).sum()):,}) "
      f"vs {LOW} (n={int((frame[TIER_COL] == LOW).sum()):,}).")

# %% [markdown]
# ## 1. Which topics are even eligible?
#
# A topic that barely appears cannot support a comparison. Two gates:
#
# - **prevalence** — present in at least 5% of books
# - **mass** — at least 0.05% of sentences on average
#
# As notebook 00 showed, prevalence barely bites at this granularity: a book has ~6,800
# sentences over 373 topics, so nearly every topic appears somewhere in nearly every book.
# The mass gate is what does the filtering, and even it removes only a handful. The real
# filter is the effect-size gate further down, and that is the honest story of this chapter.

# %%
screen = comp.screen_columns(
    frame[TOPIC_COLS],
    min_prevalence=float(cfg.section("screening", "min_prevalence_books")),
    min_mean_share=float(cfg.section("screening", "min_mean_share")),
)
eligible = screen.index[screen["passes_screen"]].tolist()

print(f"eligible topics: {len(eligible)} of {len(TOPIC_COLS)}")
excluded = screen[~screen["passes_screen"]]
if len(excluded):
    show = excluded.copy()
    show["label"] = show.index.map(LABELS)
    print("\nExcluded, and why:")
    display(show[["label", "prevalence", "mean_share", "passes_prevalence", "passes_mean_share"]])

# %% [markdown]
# ## 2. Do the three tiers differ at all? (omnibus)
#
# Before comparing pairs of tiers, ask the blunt question: for each topic, is there *any*
# difference across the three rating tiers? A Kruskal–Wallis test answers that on ranks, so
# it makes no assumption about the shape of the distribution — which matters, because topic
# shares are bounded below at zero and have a long right tail.
#
# Alongside it, **epsilon-squared** gives the share of rank variance explained by tier. One
# caution about its scale: with three equal tiers, even perfect separation only reaches about
# 8/9, because rank variance *within* a tier never goes away. So compare these numbers to
# each other, not to 1.
#
# P-values are corrected with Benjamini–Hochberg across all eligible topics — false discovery
# rate, not familywise error, because 373 tests would make Bonferroni-style control
# pointlessly conservative. Topics are one of five separately corrected families in this
# analysis (topics, leaves, main groups, axes, hypotheses); pooling them would let the large
# topic family consume the small hypothesis family's alpha budget.

# %%
omnibus = tst.kruskal_wallis(frame, eligible, TIER_COL, TIERS)
omnibus = tst.adjust_within_family(
    omnibus, "p_value", method=cfg.section("inference", "fdr_method"),
    alpha=float(cfg.section("inference", "fdr_alpha")),
)
omnibus["label"] = omnibus["feature"].map(LABELS)

alpha = float(cfg.section("inference", "fdr_alpha"))
print(f"Topics with any tier difference at BH-FDR q < {alpha}: "
      f"{int(omnibus['q_value_significant'].sum())} of {len(omnibus)}")
print(f"Largest epsilon-squared: {omnibus['epsilon_squared'].max():.4f} "
      f"({omnibus.iloc[0]['label']})")
print(f"Median epsilon-squared:  {omnibus['epsilon_squared'].median():.4f}\n")
print("The gap between those two lines is the point: a great many topics differ detectably,")
print("and almost none differ substantially. Both facts are real and both need reporting.")

display(omnibus.head(15)[["feature", "label", "epsilon_squared", "kw_statistic",
                          "p_value", "q_value"]])

# %% [markdown]
# ## 3. The headline contrast: high-rated versus low-rated
#
# Now the specific comparison the rest of the analysis leans on. **Cliff's delta** is the
# probability that a randomly chosen high-rated book devotes more of its sentences to a topic
# than a randomly chosen low-rated book, minus the reverse. It runs from −1 to +1, needs no
# distributional assumptions, and reads directly as "how often does one exceed the other".
#
# Conventional thresholds (Romano et al. 2006): 0.11 small, 0.28 medium, 0.43 large.
#
# Each delta gets a bootstrap confidence interval, resampling books within tier. The interval
# is the thing to read: an interval that comfortably excludes zero and sits above 0.11 is a
# result, and one that straddles 0.11 is a hint at best. (Author-level clustering enters in
# notebook 08, where the same intervals are recomputed by resampling whole authors.)

# %%
delta_table = eff.two_group_effects(
    frame, eligible, TIER_COL, HIGH, LOW,
    n_replicates=int(cfg.section("inference", "screening_ci_replicates")),
    ci_level=float(cfg.section("inference", "bootstrap", "ci_level")),
    seed=int(cfg.section("inference", "bootstrap", "seed")),
)
delta_table = delta_table.merge(
    omnibus[["feature", "p_value", "q_value", "epsilon_squared"]], on="feature", how="left",
)
delta_table["label"] = delta_table["feature"].map(LABELS)
delta_table["topic_id"] = delta_table["feature"].str.removeprefix("topic_").astype(int)
delta_table = delta_table.merge(
    topic_lookup[["topic_id", "taxonomy_main_id", "taxonomy_main_name", "taxonomy_main_group",
                  "taxonomy_confidence", "taxonomy_evidence_quality", "radway_phase_name"]],
    on="topic_id", how="left",
)

gates = cfg.section("screening", "effect_gates")
counts = {
    name: int((delta_table["cliffs_delta"].abs() >= threshold).sum())
    for name, threshold in gates.items()
}
print("Topics by effect-size band (absolute Cliff's delta):")
for name, threshold in gates.items():
    print(f"  >= {threshold:.2f} ({name.split('_')[-1]:<6}): {counts[name]:>3}")
print(f"\nBootstrap CI excludes zero: {int(delta_table['ci_excludes_zero'].sum())} of {len(delta_table)}")
print("\nThat contrast is the chapter in one line. Nearly every topic differs 'significantly';")
print("only a few dozen differ by enough that a reader would ever notice.")

# %% [markdown]
# ## 4. The screening funnel
#
# Rather than announce a final count of "findings", the funnel shows how many topics survive
# each requirement in turn. It makes visible which gate is actually doing the work — and here
# the statistical gate is nearly free while the effect-size gate removes almost everything.

# %%
funnel, annotated = tst.screening_funnel(
    screen, delta_table,
    min_abs_delta=float(cfg.section("screening", "headline_gate", "min_abs_cliffs_delta")),
    require_ci_excludes_zero=bool(cfg.section("screening", "headline_gate", "require_ci_excludes_zero")),
    alpha=alpha,
)
display(funnel)
ctx.save_table(funnel, "screening_funnel")

survivors = annotated[annotated["passes_all"]].copy()
survivors = survivors.sort_values("cliffs_delta", key=lambda s: s.abs(), ascending=False)
print(f"\n{len(survivors)} topics pass every gate.")

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.barh(funnel["stage"][::-1], funnel["n"][::-1], color="#4f81bd")
for y, (stage, n) in enumerate(zip(funnel["stage"][::-1], funnel["n"][::-1])):
    ax.text(n + 4, y, f"{n}", va="center", fontsize=9)
ax.set_xlabel("topics remaining")
ax.set_title("Screening funnel: the effect-size gate does the filtering")
ctx.save_figure(fig, "screening_funnel")
plt.show()

# %% [markdown]
# ## 5. Leaderboards: what high-rated books do more of, and less of
#
# The two tables below are the substantive result of this chapter. `hodges_lehmann_shift` is
# the typical difference in share between the tiers, expressed in percentage points of a
# book's sentences, so it says how much and not only how reliably.

# %%
report_cols = ["label", "taxonomy_main_id", "taxonomy_main_name", "cliffs_delta",
               "ci_low", "ci_high", "magnitude", "mean_a", "mean_b",
               "hodges_lehmann_shift", "q_value"]


def as_percentage_points(table: pd.DataFrame) -> pd.DataFrame:
    out = table[report_cols].copy()
    out = out.rename(columns={"mean_a": f"mean_{HIGH}_%", "mean_b": f"mean_{LOW}_%",
                              "hodges_lehmann_shift": "typical_shift_pp"})
    for col in [f"mean_{HIGH}_%", f"mean_{LOW}_%", "typical_shift_pp"]:
        out[col] = out[col] * 100.0
    return out.round(4).reset_index(drop=True)


more_in_high = survivors[survivors["cliffs_delta"] > 0]
more_in_low = survivors[survivors["cliffs_delta"] < 0]

print(f"More prominent in HIGH-rated books ({len(more_in_high)} topics pass all gates):")
display(as_percentage_points(more_in_high.head(20)))

print(f"\nMore prominent in LOW-rated books ({len(more_in_low)} topics pass all gates):")
display(as_percentage_points(more_in_low.head(20)))

ctx.save_table(as_percentage_points(more_in_high), "leaderboard_more_in_high")
ctx.save_table(as_percentage_points(more_in_low), "leaderboard_more_in_low")
ctx.save_table(delta_table.sort_values("cliffs_delta", key=lambda s: s.abs(), ascending=False),
               "topic_tier_effects_full")

# %%
top_n = int(cfg.section("plotting", "max_bars"))
plot_data = survivors.reindex(
    survivors["cliffs_delta"].abs().sort_values(ascending=False).index
).head(top_n).copy()
plot_data["display"] = plot_data["label"].fillna(plot_data["feature"]).str.slice(0, 46)

fig, ax = plt.subplots(figsize=(9, 0.34 * len(plot_data) + 1.4))
colours = [PALETTE[HIGH] if d > 0 else PALETTE[LOW] for d in plot_data["cliffs_delta"]]
y = np.arange(len(plot_data))[::-1]
ax.barh(y, plot_data["cliffs_delta"], color=colours)
ax.errorbar(
    plot_data["cliffs_delta"], y,
    xerr=[plot_data["cliffs_delta"] - plot_data["ci_low"],
          plot_data["ci_high"] - plot_data["cliffs_delta"]],
    fmt="none", ecolor="#444444", elinewidth=0.9, capsize=2,
)
ax.set_yticks(y)
ax.set_yticklabels(plot_data["display"], fontsize=8)
ax.axvline(0, color="black", lw=0.8)
for gate_value in (gates["cliffs_delta_small"], -gates["cliffs_delta_small"]):
    ax.axvline(gate_value, color="#888888", ls=":", lw=0.9)
ax.set_xlabel("Cliff's delta  (positive = more in high-rated books)")
ax.set_title(f"The {len(plot_data)} strongest topic-level tier differences\n"
             "dotted lines mark the 'small effect' threshold of 0.11")
ctx.save_figure(fig, "top_topic_effects")
plt.show()

# %% [markdown]
# ## 6. Effect versus prominence
#
# A useful sanity check: are the discriminating topics the big ones or the small ones? If all
# the effects sat on tiny topics, the story would be about marginal detail rather than about
# what these books are mostly made of.

# %%
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.scatter(annotated["mean_share"] * 100, annotated["cliffs_delta"],
           s=18, alpha=0.45, color="#9e9e9e", label="all eligible topics")
ax.scatter(survivors["mean_share"] * 100, survivors["cliffs_delta"],
           s=34, alpha=0.9, color="#4f81bd", label="passes all gates")
ax.axhline(0, color="black", lw=0.8)
for gate_value in (gates["cliffs_delta_small"], -gates["cliffs_delta_small"]):
    ax.axhline(gate_value, color="#888888", ls=":", lw=0.9)
ax.set_xscale("log")
ax.set_xlabel("mean share of a book's sentences (%), log scale")
ax.set_ylabel("Cliff's delta")
ax.set_title("Discriminating topics are spread across the size range")
ax.legend()

for _, row in survivors.head(8).iterrows():
    ax.annotate(str(row["label"])[:30], (row["mean_share"] * 100, row["cliffs_delta"]),
                fontsize=7, xytext=(4, 3), textcoords="offset points")
ctx.save_figure(fig, "effect_vs_prominence")
plt.show()

# %% [markdown]
# ## 7. Is the difference a gradient or a cliff?
#
# "High-rated books do more of X" could mean two quite different things: X rises steadily
# from low to mid to high, or X is flat across low and mid and then jumps. A steady gradient
# is the stronger and more interpretable claim, so it is worth separating.
#
# Spearman's rho against the tier index (0, 1, 2) measures monotone trend. A topic with a
# large Cliff's delta *and* a monotone gradient is the most trustworthy kind of result here.

# %%
trend = tst.compare_tier_trend(frame, eligible, TIER_COL, TIERS)
trend["label"] = trend["feature"].map(LABELS)

combined = survivors[["feature", "label", "cliffs_delta", "magnitude"]].merge(
    trend[["feature", "spearman_rho", "direction"]], on="feature", how="left",
)
combined["monotone_and_consistent"] = (
    np.sign(combined["spearman_rho"]) == np.sign(combined["cliffs_delta"])
) & (combined["spearman_rho"].abs() >= 0.05)

n_mono = int(combined["monotone_and_consistent"].sum())
print(f"{n_mono} of {len(combined)} surviving topics show a monotone gradient across all "
      f"three tiers\nin the same direction as the high-vs-low contrast.")
display(combined.sort_values("spearman_rho", key=lambda s: s.abs(), ascending=False).head(15))
ctx.save_table(combined, "surviving_topics_trend")

# %%
panel = survivors.head(6)["feature"].tolist()
fig, axes = plt.subplots(2, 3, figsize=(14, 7), sharex=True)
for ax, col in zip(axes.ravel(), panel):
    means = frame.groupby(TIER_COL, observed=True)[col].mean().reindex(TIERS) * 100
    sems = (frame.groupby(TIER_COL, observed=True)[col].sem().reindex(TIERS) * 100)
    ax.errorbar(range(len(TIERS)), means.to_numpy(), yerr=sems.to_numpy(),
                marker="o", color="#4f81bd", capsize=3)
    ax.set_xticks(range(len(TIERS)))
    ax.set_xticklabels([cfg.section("tiers", "labels")[t] for t in TIERS], fontsize=8)
    ax.set_title(str(LABELS.get(col, col))[:40], fontsize=9)
    ax.set_ylabel("% of sentences", fontsize=8)
fig.suptitle("The six strongest topics across all three tiers: gradient or cliff?")
fig.tight_layout()
ctx.save_figure(fig, "tier_gradients")
plt.show()

# %% [markdown]
# ## 8. Are the tier contrasts internally consistent?
#
# A last check before moving up a level. If high beats low, high should also beat mid and mid
# should beat low. Where that ordering breaks, the topic is not tracking rating in any simple
# way, and grouping it into a composite later would blur rather than sharpen.
#
# Holm correction is applied *within* each topic's set of three contrasts — a small family
# where controlling the familywise error rate is affordable — while Benjamini–Hochberg
# already handled the 373-topic family above.

# %%
contrasts = [tuple(c) for c in cfg.section("tiers", "contrasts")]
pairwise = tst.pairwise_mann_whitney(
    frame, survivors["feature"].tolist(), TIER_COL, contrasts, holm_within_feature=True,
)
pairwise["label"] = pairwise["feature"].map(LABELS)

wide = pairwise.pivot_table(
    index="feature", columns=["group_a", "group_b"], values="cliffs_delta",
)
wide.columns = [f"{a}_vs_{b}" for a, b in wide.columns]
wide["consistent_ordering"] = (
    (np.sign(wide[f"{HIGH}_vs_{LOW}"]) == np.sign(wide[f"{HIGH}_vs_mid_rate"]))
    & (np.sign(wide[f"{HIGH}_vs_{LOW}"]) == np.sign(wide[f"mid_rate_vs_{LOW}"]))
)
wide["label"] = wide.index.map(LABELS)

print(f"{int(wide['consistent_ordering'].sum())} of {len(wide)} surviving topics order the "
      f"three tiers consistently.")
display(wide.reindex(wide[f"{HIGH}_vs_{LOW}"].abs().sort_values(ascending=False).index).head(15))
ctx.save_table(pairwise, "pairwise_tier_contrasts")
ctx.save_table(wide.reset_index(), "tier_ordering_consistency")

# %% [markdown]
# ## 9. Where do the discriminating topics sit in the taxonomy?
#
# This is the bridge to notebook 02. If the surviving topics were scattered evenly across the
# taxonomy, grouping them would be pointless. If they cluster in a few main groups, then the
# taxonomy is capturing something real and the grouped analysis should show it too.

# %%
by_group = (
    survivors.groupby("taxonomy_main_group", dropna=False)
    .agg(n_surviving=("feature", "size"),
         mean_delta=("cliffs_delta", "mean"),
         n_positive=("cliffs_delta", lambda s: int((s > 0).sum())),
         n_negative=("cliffs_delta", lambda s: int((s < 0).sum())))
)
eligible_by_group = (
    delta_table.groupby("taxonomy_main_group", dropna=False)["feature"].size()
    .rename("n_eligible")
)
by_group = by_group.join(eligible_by_group, how="right").fillna({"n_surviving": 0})
by_group["survival_rate"] = by_group["n_surviving"] / by_group["n_eligible"]
by_group = by_group.sort_values("n_surviving", ascending=False)

display(by_group.round(3))
ctx.save_table(by_group.reset_index(), "survivors_by_main_group")

print(
    "\nRead the split between n_positive and n_negative carefully. A group where surviving\n"
    "topics point in both directions cannot be summarised by its total share — the grouped\n"
    "measure would cancel out. Notebook 02 tests exactly that, and notebook 03 goes back\n"
    "inside any group where the grouped signal is weaker than its individual topics."
)

# %%
summary = pd.DataFrame([
    ("topics tested", f"{len(eligible)} of {len(TOPIC_COLS)} passed prevalence and mass screens"),
    ("any tier difference (BH-FDR)", f"{int(omnibus['q_value_significant'].sum())} topics"),
    ("small effect or larger", f"{counts['cliffs_delta_small']} topics (|delta| >= 0.11)"),
    ("medium effect or larger", f"{counts['cliffs_delta_medium']} topics (|delta| >= 0.28)"),
    ("passes every gate", f"{len(survivors)} topics"),
    ("of those, more in high-rated", f"{len(more_in_high)}"),
    ("of those, more in low-rated", f"{len(more_in_low)}"),
    ("monotone across all three tiers", f"{n_mono} of {len(survivors)}"),
    ("consistent tier ordering", f"{int(wide['consistent_ordering'].sum())} of {len(wide)}"),
    ("strongest single topic", f"{survivors.iloc[0]['label']} "
                               f"(delta = {survivors.iloc[0]['cliffs_delta']:+.3f})"),
], columns=["item", "value"])
display(summary)
ctx.save_table(summary, "chapter_summary")

print("\n" + nbh.compositional_note())
print("\nNext: 02_taxonomy_structure.ipynb — the same question one level up, at main groups")
print("and their subgroups, where individual topics are pooled into theory categories.")
