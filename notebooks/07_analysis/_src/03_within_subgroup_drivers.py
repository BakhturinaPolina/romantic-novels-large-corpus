# %% [markdown]
# # 03 — Within-subgroup drivers
#
# Notebook 02 ended on a problem. Twenty-five of the 45 taxonomy leaves *dilute* their member
# topics: the leaf total is much weaker than the strongest topic inside it. The most extreme
# case is `9.2 Promise, Vow & Future-Tense Speech Acts`, where one topic reaches a Cliff's
# delta of 0.225 — the largest topic-level effect in the whole corpus — and the leaf as a whole
# manages 0.038.
#
# That is not a rounding problem. It means the 22 topics inside `9.2` do not behave alike, and
# summing them cancels the signal out. The purpose of this chapter is to look inside such
# categories and say, concretely, which topics carry the difference and which pull against it.
#
# **What this chapter delivers**
#
# 1. For each diluting leaf, the full internal breakdown: every topic, its effect, its size.
# 2. A **driver concentration** measure — is the leaf's signal one topic or a broad tendency?
# 3. A **coherence audit** — do a leaf's topics actually covary across books, i.e. is it one
#    theme at all?
# 4. A **refined subindex** for the worst offenders: the same leaf restricted to the topics
#    that agree, reported as exploratory and clearly flagged as post-hoc.
#
# **The honesty constraint.** Point 4 is selection on an outcome we have already looked at, so
# a refined subindex is guaranteed to look better than the leaf it came from. It is reported as
# a *description of internal structure*, never as a confirmatory result, and notebook 08
# re-checks it under author clustering.

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

from src.stage10_correlation_analysis.analysis import effects as eff
from src.stage10_correlation_analysis.analysis import notebook_helpers as nbh
from src.stage10_correlation_analysis.analysis import reliability as rel
from src.stage10_correlation_analysis.analysis import tests as tst

ctx = nbh.setup("03_within_subgroup_drivers")
cfg = ctx.cfg
TIERS = cfg.tier_order
TIER_COL = cfg.tier_column
PALETTE = nbh.tier_palette(cfg)
HIGH, LOW = cfg.section("tiers", "headline_contrast")
GATE = float(cfg.section("screening", "effect_gates", "cliffs_delta_small"))
SEED = int(cfg.section("inference", "bootstrap", "seed"))
REPLICATES = int(cfg.section("inference", "effect_ci_replicates"))

frame = nbh.load_analysis_frame(cfg).reset_index()
topic_lookup = nbh.load_topic_lookup(cfg)
LABELS = nbh.topic_label_map(topic_lookup)

topic_effects = pd.read_csv(
    cfg.notebook_output_dirs("01_topic_landscape")["tables"] / "topic_tier_effects_full.csv"
)
aggregation = pd.read_csv(
    cfg.notebook_output_dirs("02_taxonomy_structure")["tables"] / "aggregation_gain_loss.csv"
)
leaf_effects = pd.read_csv(
    cfg.notebook_output_dirs("02_taxonomy_structure")["tables"] / "leaf_tier_effects.csv"
)
topic_effects["leaf_id"] = topic_effects["taxonomy_main_id"].astype(str)

print(f"\nLoaded {len(topic_effects)} topic-level effects and {len(leaf_effects)} leaf-level "
      f"effects from the previous two notebooks.")

# %% [markdown]
# ## 1. Which categories need opening up?
#
# A leaf goes on the list if it has at least three topics (so there is something to decompose)
# and either loses most of its topics' signal, or contains at least one topic that clears the
# small-effect gate on its own. The second condition matters: a leaf can look uninteresting at
# leaf level while containing a genuinely strong topic.

# %%
min_topics = 3
targets = aggregation[
    (aggregation["n_topics_tested"] >= min_topics)
    & ((aggregation["retention"] < 0.6) | (aggregation["max_abs_topic_delta"] >= GATE))
].copy()
targets = targets.sort_values("max_abs_topic_delta", ascending=False).reset_index(drop=True)

print(f"{len(targets)} leaves selected for decomposition, out of "
      f"{int((aggregation['n_topics_tested'] >= min_topics).sum())} with {min_topics}+ topics.\n")
display(targets[["leaf_id", "leaf_name", "main_group", "n_topics_tested", "abs_leaf_delta",
                 "max_abs_topic_delta", "retention", "sign_split", "verdict"]].round(3))
ctx.save_table(targets, "decomposition_targets")

# %% [markdown]
# ## 2. Driver concentration: one topic or many?
#
# For each target leaf, two complementary numbers:
#
# - **driver share** — the fraction of the leaf's total topic-level signal (summed absolute
#   deltas) held by its single strongest topic. Near 1 means the leaf is really one topic
#   wearing a category's name.
# - **agreement** — the fraction of the leaf's topic-level signal pointing the same way as the
#   leaf's own effect. Near 0.5 means the topics contradict each other and the leaf total is
#   an artefact of which side happened to be larger.
#
# Both are computed with topic mass as the weight, because a large topic pulling one way
# outweighs a tiny topic pulling the other.

# %%
rows = []
for row in targets.itertuples():
    members = topic_effects[topic_effects["leaf_id"] == row.leaf_id].copy()
    if members.empty:
        continue
    members["mass"] = members[["mean_a", "mean_b"]].mean(axis=1)
    members["signal"] = members["cliffs_delta"].abs() * members["mass"]
    total_signal = float(members["signal"].sum())
    leaf_sign = np.sign(row.cliffs_delta) if row.cliffs_delta != 0 else 1.0
    agreeing = float(members.loc[np.sign(members["cliffs_delta"]) == leaf_sign, "signal"].sum())

    strongest = members.reindex(members["cliffs_delta"].abs().sort_values(ascending=False).index)
    rows.append({
        "leaf_id": row.leaf_id,
        "leaf_name": row.leaf_name,
        "main_group": row.main_group,
        "n_topics": int(len(members)),
        "leaf_delta": row.cliffs_delta,
        "driver_share": float(strongest.iloc[0]["signal"] / total_signal) if total_signal else np.nan,
        "top3_driver_share": float(strongest.head(3)["signal"].sum() / total_signal) if total_signal else np.nan,
        "agreement": agreeing / total_signal if total_signal else np.nan,
        "strongest_topic": strongest.iloc[0]["label"],
        "strongest_delta": float(strongest.iloc[0]["cliffs_delta"]),
        "n_above_gate": int((members["cliffs_delta"].abs() >= GATE).sum()),
        "n_opposing_above_gate": int(
            ((members["cliffs_delta"].abs() >= GATE)
             & (np.sign(members["cliffs_delta"]) != leaf_sign)).sum()
        ),
    })

concentration = pd.DataFrame(rows).sort_values("agreement").reset_index(drop=True)
concentration["structure"] = np.where(
    concentration["agreement"] >= 0.8, "coherent",
    np.where(concentration["agreement"] >= 0.6, "mixed", "contradictory"),
)

display(concentration.round(3))
ctx.save_table(concentration, "driver_concentration")

print(f"\ncoherent (topics broadly agree)       : {int((concentration['structure'] == 'coherent').sum())}")
print(f"mixed                                 : {int((concentration['structure'] == 'mixed').sum())}")
print(f"contradictory (topics pull both ways) : {int((concentration['structure'] == 'contradictory').sum())}")
print("\nA contradictory leaf is not a failed measurement — it is evidence that the taxonomy")
print("category bundles distinguishable narrative behaviours. That is a finding about the")
print("taxonomy, and it is the reason the axes in notebook 04 are built from leaves that")
print("survive this check rather than from every leaf that exists.")

# %% [markdown]
# ## 3. Coherence audit: do a leaf's topics covary at all?
#
# The previous section asked whether topics agree about *rating*. This one asks something more
# basic: do they even co-occur? If a category's topics appear in unrelated books, then adding
# their shares together produces a number with no single referent.
#
# Three measures, from `analysis/reliability.py`:
#
# - **Cronbach's alpha** — internal consistency of the topics as a scale
# - **PC1 explained** — how much of the topics' joint variation is one dimension
# - **mean pairwise correlation** — the plainest version of the same question
#
# Caution: topic shares are compositional and mutually constrained, which pushes correlations
# *down* mechanically. So low values here should be read as "no evidence of a shared
# dimension" rather than as proof of independence, and the comparison across leaves is more
# informative than any single value.

# %%
coherence_rows = []
for row in concentration.itertuples():
    members = topic_effects[topic_effects["leaf_id"] == row.leaf_id]["feature"].tolist()
    members = [c for c in members if c in frame.columns]
    if len(members) < 2:
        continue
    block = frame[members]
    corr = block.corr(method="spearman").to_numpy()
    off_diagonal = corr[~np.eye(len(members), dtype=bool)]
    pca = rel.pca_structure(block, n_components=2)
    coherence_rows.append({
        "leaf_id": row.leaf_id,
        "leaf_name": row.leaf_name,
        "n_topics": len(members),
        "cronbach_alpha": rel.cronbach_alpha(block),
        "pc1_explained": float(pca.loc[0, "explained_variance_ratio"]) if len(pca) else np.nan,
        "pc1_all_same_sign": bool(pca.loc[0, "all_loadings_same_sign"]) if len(pca) else False,
        "mean_pairwise_r": float(np.mean(off_diagonal)),
        "max_pairwise_r": float(np.max(off_diagonal)),
        "share_negative_pairs": float(np.mean(off_diagonal < 0)),
    })

coherence = pd.DataFrame(coherence_rows).sort_values("mean_pairwise_r", ascending=False)
display(coherence.round(4))
ctx.save_table(coherence, "leaf_coherence_audit")

merged = concentration.merge(
    coherence[["leaf_id", "cronbach_alpha", "pc1_explained", "mean_pairwise_r"]],
    on="leaf_id", how="left",
)
print(
    "\nPut sections 2 and 3 together. A leaf whose topics neither co-occur (low mean pairwise\n"
    "correlation) nor agree about rating (agreement near 0.5) is a label, not a construct.\n"
    "A leaf whose topics disagree about rating but do co-occur is more interesting: the same\n"
    "narrative territory handled in ways readers evaluate differently."
)
ctx.save_table(merged, "structure_and_coherence")

# %% [markdown]
# ## 4. Inside the categories: the driver tables
#
# The detail behind the summaries. For each target leaf, every member topic with its own
# effect, sorted so drivers appear first and opponents last. `mass_pp` is the topic's mean
# share of a book's sentences in percentage points, so a large delta on a tiny topic is
# visibly distinguishable from a large delta on a substantial one.

# %%
detail_frames = []
for row in concentration.head(8).itertuples():
    members = topic_effects[topic_effects["leaf_id"] == row.leaf_id].copy()
    members["mass_pp"] = members[["mean_a", "mean_b"]].mean(axis=1) * 100
    members["shift_pp"] = members["hodges_lehmann_shift"] * 100
    members["role"] = np.where(
        np.sign(members["cliffs_delta"]) == np.sign(row.leaf_delta), "with the leaf", "against"
    )
    members["leaf_id"] = row.leaf_id
    members["leaf_name"] = row.leaf_name
    members = members.reindex(members["cliffs_delta"].sort_values(ascending=False).index)

    print(f"\n{'=' * 100}")
    print(f"{row.leaf_id}  {row.leaf_name}")
    print(f"leaf delta {row.leaf_delta:+.3f} | {row.n_topics} topics | "
          f"agreement {row.agreement:.2f} | structure {row.structure}")
    print("=" * 100)
    display(members[["label", "mass_pp", "cliffs_delta", "ci_low", "ci_high", "magnitude",
                     "shift_pp", "role", "q_value"]].round(4).reset_index(drop=True))
    detail_frames.append(members)

drivers = pd.concat(detail_frames, ignore_index=True)
ctx.save_table(drivers, "within_leaf_topic_detail")

# %%
n_panels = min(6, len(concentration))
panel_leaves = concentration.reindex(
    concentration["n_topics"].sort_values(ascending=False).index
).head(n_panels)

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.ravel()
for ax, row in zip(axes, panel_leaves.itertuples()):
    members = topic_effects[topic_effects["leaf_id"] == row.leaf_id].copy()
    members = members.reindex(members["cliffs_delta"].sort_values().index)
    y = np.arange(len(members))
    colours = [PALETTE[HIGH] if d > 0 else PALETTE[LOW] for d in members["cliffs_delta"]]
    ax.barh(y, members["cliffs_delta"], color=colours)
    ax.errorbar(members["cliffs_delta"], y,
                xerr=[members["cliffs_delta"] - members["ci_low"],
                      members["ci_high"] - members["cliffs_delta"]],
                fmt="none", ecolor="#333333", elinewidth=0.7, capsize=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels([str(v)[:34] for v in members["label"]], fontsize=6.5)
    ax.axvline(0, color="black", lw=0.8)
    ax.axvline(row.leaf_delta, color="#7030a0", ls="-", lw=1.6, label="leaf total")
    for gate_value in (GATE, -GATE):
        ax.axvline(gate_value, color="#888888", ls=":", lw=0.8)
    ax.set_title(f"{row.leaf_id} {str(row.leaf_name)[:30]}\nagreement {row.agreement:.2f}",
                 fontsize=8.5)
    ax.tick_params(axis="x", labelsize=7)
    ax.legend(fontsize=6.5, loc="lower right")

for ax in axes[len(panel_leaves):]:
    ax.axis("off")
fig.suptitle("Inside the biggest categories: purple line is the leaf total, bars are its topics\n"
             "where bars straddle zero, the leaf total is a cancellation artefact", y=1.0)
fig.tight_layout()
ctx.save_figure(fig, "within_leaf_forest_panels")
plt.show()

# %% [markdown]
# ## 5. Refined subindices — exploratory
#
# For the contradictory leaves, what happens if the category is split into the topics that
# agree and the topics that oppose, and each half is measured on its own?
#
# **This is post-hoc.** The split is chosen using the same tier contrast it is then evaluated
# on, so the two halves are *guaranteed* to separate more than the leaf did. The number worth
# reading is not the effect size but the pair of labels: what do the agreeing topics have in
# common, and what do the opposing ones? That is a description of internal structure, and it
# is the kind of claim that the qualitative close readings in notebook 07 can check.

# %%
refined_rows = []
subindex_columns = {}
for row in concentration[concentration["structure"] != "coherent"].itertuples():
    members = topic_effects[topic_effects["leaf_id"] == row.leaf_id].copy()
    members = members[members["feature"].isin(frame.columns)]
    if len(members) < 4:
        continue
    leaf_sign = np.sign(row.leaf_delta) if row.leaf_delta != 0 else 1.0
    with_leaf = members.loc[np.sign(members["cliffs_delta"]) == leaf_sign, "feature"].tolist()
    against = members.loc[np.sign(members["cliffs_delta"]) != leaf_sign, "feature"].tolist()
    if len(with_leaf) < 2 or len(against) < 2:
        continue

    name_with = f"sub_{row.leaf_id}_aligned"
    name_against = f"sub_{row.leaf_id}_opposed"
    subindex_columns[name_with] = frame[with_leaf].sum(axis=1)
    subindex_columns[name_against] = frame[against].sum(axis=1)

    refined_rows.append({
        "leaf_id": row.leaf_id,
        "leaf_name": row.leaf_name,
        "leaf_delta": row.leaf_delta,
        "n_aligned": len(with_leaf),
        "n_opposed": len(against),
        "aligned_topics": "; ".join(str(LABELS.get(c, c))[:30] for c in with_leaf[:4]),
        "opposed_topics": "; ".join(str(LABELS.get(c, c))[:30] for c in against[:4]),
    })

if subindex_columns:
    sub_frame = pd.concat([frame[[TIER_COL]], pd.DataFrame(subindex_columns, index=frame.index)],
                          axis=1)
    sub_effects = eff.two_group_effects(
        sub_frame, list(subindex_columns), TIER_COL, HIGH, LOW,
        n_replicates=REPLICATES, seed=SEED,
    )
    refined = pd.DataFrame(refined_rows)
    for suffix, label in [("aligned", "aligned"), ("opposed", "opposed")]:
        lookup = sub_effects.set_index("feature")
        refined[f"{label}_delta"] = [
            float(lookup.loc[f"sub_{lid}_{suffix}", "cliffs_delta"])
            for lid in refined["leaf_id"]
        ]
    refined["separation"] = refined["aligned_delta"] - refined["opposed_delta"]
    refined = refined.sort_values("separation", key=lambda s: s.abs(), ascending=False)

    display(refined[["leaf_id", "leaf_name", "leaf_delta", "aligned_delta", "opposed_delta",
                     "separation", "n_aligned", "n_opposed"]].round(4))
    print("\nWhat the two halves contain:")
    display(refined[["leaf_id", "aligned_topics", "opposed_topics"]])
    ctx.save_table(refined, "refined_subindices_exploratory")
    ctx.save_table(sub_effects, "refined_subindex_effects")
else:
    refined = pd.DataFrame()
    print("No leaf had at least two topics on each side; no refined subindices built.")

# %% [markdown]
# ## 6. The single strongest topic in the corpus, in context
#
# Worth one section on its own. `9.2 Promise, Vow & Future-Tense Speech Acts` has the largest
# topic-level effect anywhere in this analysis and almost none of it survives aggregation. The
# breakdown below is the clearest single illustration of why this chapter exists.

# %%
strongest_row = topic_effects.reindex(
    topic_effects["cliffs_delta"].abs().sort_values(ascending=False).index
).iloc[0]
host_leaf = str(strongest_row["leaf_id"])

print(f"Strongest topic anywhere: {strongest_row['label']!r}")
print(f"  Cliff's delta {strongest_row['cliffs_delta']:+.3f} "
      f"[{strongest_row['ci_low']:.3f}, {strongest_row['ci_high']:.3f}]")
print(f"  taxonomy leaf {host_leaf} — {strongest_row['taxonomy_main_name']}")

host = leaf_effects[leaf_effects["leaf_id"].astype(str) == host_leaf]
if len(host):
    print(f"  the leaf as a whole: delta {float(host.iloc[0]['cliffs_delta']):+.3f} "
          f"({host.iloc[0]['n_topics']} topics)")

siblings = topic_effects[topic_effects["leaf_id"] == host_leaf].copy()
siblings["mass_pp"] = siblings[["mean_a", "mean_b"]].mean(axis=1) * 100
siblings = siblings.reindex(siblings["cliffs_delta"].sort_values(ascending=False).index)
display(siblings[["label", "mass_pp", "cliffs_delta", "ci_low", "ci_high", "magnitude"]]
        .round(4).reset_index(drop=True))

fig, ax = plt.subplots(figsize=(9, 0.3 * len(siblings) + 1.6))
y = np.arange(len(siblings))[::-1]
colours = [PALETTE[HIGH] if d > 0 else PALETTE[LOW] for d in siblings["cliffs_delta"]]
ax.barh(y, siblings["cliffs_delta"], color=colours)
ax.errorbar(siblings["cliffs_delta"], y,
            xerr=[siblings["cliffs_delta"] - siblings["ci_low"],
                  siblings["ci_high"] - siblings["cliffs_delta"]],
            fmt="none", ecolor="#333333", elinewidth=0.8, capsize=1.5)
ax.set_yticks(y)
ax.set_yticklabels([str(v)[:44] for v in siblings["label"]], fontsize=7.5)
ax.axvline(0, color="black", lw=0.8)
if len(host):
    ax.axvline(float(host.iloc[0]["cliffs_delta"]), color="#7030a0", lw=1.8,
               label="leaf total")
    ax.legend(fontsize=8)
ax.set_xlabel("Cliff's delta  (positive = more in high-rated books)")
ax.set_title(f"Leaf {host_leaf}: promises and vows\n"
             "one topic is the strongest effect in the corpus; the category total is near zero")
ctx.save_figure(fig, "strongest_topic_in_context")
plt.show()

# %% [markdown]
# ## 7. What this chapter changes for the rest of the analysis
#
# Three consequences, all acted on downstream.

# %%
summary = pd.DataFrame([
    ("leaves decomposed", f"{len(concentration)}"),
    ("coherent leaves", f"{int((concentration['structure'] == 'coherent').sum())}"),
    ("mixed leaves", f"{int((concentration['structure'] == 'mixed').sum())}"),
    ("contradictory leaves", f"{int((concentration['structure'] == 'contradictory').sum())}"),
    ("most one-topic-driven leaf",
     f"{concentration.loc[concentration['driver_share'].idxmax(), 'leaf_id']} "
     f"(driver share {concentration['driver_share'].max():.2f})"),
    ("strongest topic overall", f"{strongest_row['label']} "
                                f"(delta {strongest_row['cliffs_delta']:+.3f}, leaf {host_leaf})"),
    ("refined subindices built", f"{len(refined)} (exploratory only)"),
], columns=["item", "value"])
display(summary)
ctx.save_table(summary, "chapter_summary")

print(
    "\nConsequences carried forward:\n"
    "  1. Axes in notebook 04 are validated with alpha, omega and PCA on their components\n"
    "     before use, precisely because leaf-level aggregation has been shown to cancel.\n"
    "  2. Where a hypothesis rests on a contradictory leaf, the hypothesis test in notebook 05\n"
    "     reports the leaf form as primary and the topic-level detail alongside it, rather\n"
    "     than quietly substituting whichever version is stronger.\n"
    "  3. The close readings in notebook 07 are sampled on the axes, and the aligned/opposed\n"
    "     splits found here are what they are asked to interpret.\n"
)
print("Next: 04_composites_validity.ipynb — building the theory axes and testing whether they")
print("hold together well enough to carry a hypothesis.")
