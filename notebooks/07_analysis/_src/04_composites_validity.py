# %% [markdown]
# # 04 — Theory composites and validity
#
# The first three notebooks worked bottom-up: topics, then taxonomy leaves, then inside the
# leaves. This one works top-down. Romance scholarship makes claims about constructs —
# *love over sex*, *happily-ever-after*, *protective versus possessive love* — and each of
# those has to be turned into a number before it can be tested.
#
# A composite is a weighted combination of taxonomy leaves, defined in
# `configs/stage09/theory_aligned_index_schema.yaml` **before** any outcome was looked at. That
# ordering is the whole point: the axes are not tuned to predict ratings, so notebook 05 can
# test them rather than merely fit them.
#
# **What this notebook does, and why each step is necessary**
#
# 1. Shows every axis definition, and what corpus evidence each rests on.
# 2. Checks whether each axis holds together — a sum of things that do not covary is not a
#    measurement of anything.
# 3. Checks whether the axes are distinct from each other, since several share leaves by
#    construction.
# 4. Reports which hypotheses are testable, which are underpowered, and which are not
#    measurable at all in this model. Notebook 03 showed that leaf-level pooling can cancel
#    signal, so this step is not a formality.
#
# Nothing here touches the rating outcome. That separation is deliberate.

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

from src.stage10_correlation_analysis.analysis import axes as axes_mod
from src.stage10_correlation_analysis.analysis import compositional as comp
from src.stage10_correlation_analysis.analysis import models as mdl
from src.stage10_correlation_analysis.analysis import notebook_helpers as nbh
from src.stage10_correlation_analysis.analysis import reliability as rel

ctx = nbh.setup("04_composites_validity")
cfg = ctx.cfg
SEED = int(cfg.section("inference", "bootstrap", "seed"))

frame = nbh.load_analysis_frame(cfg).reset_index()
topic_lookup = nbh.load_topic_lookup(cfg)
axis_coverage = nbh.load_book_features(cfg, "axis_coverage")
axis_summary = nbh.load_book_features(cfg, "axis_coverage_summary")
axis_definitions = nbh.load_book_features(cfg, "axis_definitions")

AXIS_COLS = [c for c in frame.columns if c.startswith("AX_") and not c.endswith(("_z", "_clr"))]
LEAF_COLS = nbh.columns_with_prefix(frame, "leaf_")
LOG_RATIO_COLS = nbh.columns_with_prefix(frame, "LR_")

print(f"\n{len(AXIS_COLS)} axes built | {len(LOG_RATIO_COLS)} explicit log-ratio forms")
print(f"Schema: {cfg.section('axes', 'schema')}")

# %% [markdown]
# ## 1. What the axes are
#
# Every axis, spelled out. A signed weight means the axis is a *contrast*: `AX_love_over_sex`
# adds the emotional-intimacy leaves and subtracts explicit sex, so a positive value means a
# book leans emotional relative to explicit — not that it contains a lot of either.
#
# `role` separates the six confirmatory axes, which carry the pre-registered hypotheses, from
# the exploratory ones that are described but not used to claim anything.

# %%
display(axis_definitions.sort_values(["role", "axis"]))
ctx.save_table(axis_definitions, "axis_definitions")

confirmatory = axis_definitions[axis_definitions["role"] == "confirmatory"]
print(f"\nConfirmatory axes: {len(confirmatory)}")
for row in confirmatory.itertuples():
    print(f"  {row.hypothesis:<6} {row.axis:<38} {row.definition}")

# %% [markdown]
# ## 2. What each axis actually rests on
#
# A definition is a promise; coverage is what was delivered. `n_topics` is how many of the
# model's 348 mapped topics fall into each component leaf, and the verdict is mechanical:
# three or more topics is *viable*, one or two is *weak*, zero is *empty*.
#
# This table is why the rebuild exists. The previous pipeline emitted four axes as exactly
# `0.0` for every book because their components had no topics, and a column of zeros is
# indistinguishable from a real variable in a regression table.

# %%
display(axis_summary[["axis", "hypothesis", "hypothesis_role", "axis_verdict", "n_components",
                      "n_viable", "n_weak", "n_empty", "total_topics", "empty_leaves"]])
ctx.save_table(axis_summary, "axis_coverage_summary")

verdict_counts = axis_summary["axis_verdict"].value_counts()
print("\nAxis verdicts (an axis is only as strong as its weakest signed leg):")
display(verdict_counts.to_frame("n_axes"))

weak_axes = axis_summary[axis_summary["axis_verdict"] == "weak"]
print(f"\n{len(weak_axes)} axes are weak. Which leg is thin, per axis:")
for row in weak_axes.itertuples():
    thin = axis_coverage[
        (axis_coverage["axis"] == row.axis) & (axis_coverage["verdict"].isin(["weak", "empty"]))
    ]
    detail = ", ".join(f"{r.leaf_id} ({r.n_topics} topics, {r.verdict})" for r in thin.itertuples())
    print(f"  {row.axis:<40} {detail}")

# %% [markdown]
# ## 3. Do the axes hold together?
#
# An axis that sums several leaves is implicitly claiming those leaves measure one thing. That
# claim is testable, and notebook 03 gave a concrete reason to test it: pooling topics inside a
# leaf frequently cancelled their signal, so pooling leaves into an axis might do the same.
#
# Four checks, each answering a different question:
#
# | check | question | reading |
# |---|---|---|
# | Cronbach's alpha | do components covary? | conventionally 0.6+ is acceptable |
# | McDonald's omega | same, allowing unequal weights | preferred where weights differ |
# | PC1 explained | is it one dimension or several? | 0.4+ with same-sign loadings |
# | leave-one-out sign stability | does one component carry it? | 0.9+ means no |
#
# An important caveat on the numbers themselves: these are compositional shares, which are
# mechanically pushed toward *negative* correlation because they compete for the same total.
# Alpha and omega are therefore biased downward here, and a "questionable" verdict means "not
# demonstrated to be one dimension" rather than "shown to be incoherent". Single-component
# axes are labelled `atomic`: reliability is undefined for them, not failed.

# %%
schema = axes_mod.load_axis_schema(cfg.input_path("axis_schema", required=True))
composites = axes_mod.load_composites(cfg.input_path("taxonomy_config", required=True))
specs = axes_mod.resolve_axes(schema, composites, additional=cfg.section("axes", "additional"))

thresholds = (schema.get("global", {}) or {}).get("reliability_thresholds", {}) or {}
alpha_threshold = float(thresholds.get("cronbach_alpha_min", 0.60))
omega_threshold = float(thresholds.get("omega_min", 0.65))

validity_rows = []
for name, spec in specs.items():
    if name not in frame.columns or not spec.leaf_weights:
        continue
    members = [f"leaf_{leaf}" for leaf in spec.leaf_weights if f"leaf_{leaf}" in frame.columns]
    if not members:
        continue
    # Reliability is about shared variance, so signed legs are flipped to a common direction
    # first; otherwise a contrast axis would score as incoherent by construction.
    block = pd.DataFrame({
        col: frame[col] * np.sign(spec.leaf_weights[col.removeprefix("leaf_")])
        for col in members
    })
    weights = {col: abs(spec.leaf_weights[col.removeprefix("leaf_")]) for col in members}
    report = rel.axis_validity_report(
        block, name, weights=weights,
        alpha_threshold=alpha_threshold, omega_threshold=omega_threshold,
    )
    report["hypothesis"] = ",".join(spec.hypothesis) or "-"
    report["hypothesis_role"] = spec.hypothesis_role
    report["n_signed_negative"] = int(sum(1 for w in spec.leaf_weights.values() if w < 0))
    validity_rows.append(report)

validity = pd.DataFrame(validity_rows)
validity = validity.sort_values(["hypothesis_role", "verdict", "axis"]).reset_index(drop=True)

display(validity[["axis", "hypothesis", "hypothesis_role", "n_components", "cronbach_alpha",
                  "mcdonald_omega", "pc1_explained", "pc1_all_same_sign",
                  "min_sign_stability", "verdict"]].round(3))
ctx.save_table(validity, "axis_validity")

print("\nVerdict counts:")
display(validity["verdict"].value_counts().to_frame("n_axes"))
print(
    "Confirmatory axes and their verdicts:\n"
    + "\n".join(
        f"  {r.hypothesis:<6} {r.axis:<40} {r.verdict} "
        f"(alpha {r.cronbach_alpha:.2f}, PC1 {r.pc1_explained:.2f})"
        if pd.notna(r.cronbach_alpha) else
        f"  {r.hypothesis:<6} {r.axis:<40} {r.verdict}"
        for r in validity[validity["hypothesis_role"] == "confirmatory"].itertuples()
    )
)

# %% [markdown]
# **This is the most consequential result in the notebook, so it needs saying plainly.**
#
# Every multi-component axis comes out `questionable`: Cronbach's alpha is close to zero (and
# negative for `AX_love_over_sex`), and PC1 explains 25–56% of the components' joint variation.
# Not one composite demonstrates that its taxonomy leaves measure a single underlying dimension.
#
# Two things are going on, and they have opposite implications.
#
# *Part of it is mechanical.* These are shares of the same finite text. If a book spends more
# sentences on emotional safety it has fewer left for explicit sex, so components are pushed
# toward negative correlation whatever the underlying themes do. A contrast axis such as
# `AX_love_over_sex` is *designed* around that opposition, so a negative alpha there is close to
# expected and is not evidence of a problem.
#
# *Part of it is substantive, and consistent with notebook 03.* Pooling topics inside a leaf
# cancelled signal in 25 of 45 leaves. Pooling leaves into an axis is the same operation one
# level up, and it behaves the same way. Romance themes in this corpus do not come in bundles
# that rise and fall together; they trade off against each other.
#
# **What follows for the hypothesis tests.** Composites are still reported, because they are
# what the pre-registered schema specifies and suppressing them after seeing the reliability
# numbers would be its own kind of dishonesty. But they are reported *alongside* their strongest
# single component and, for the balance hypotheses, alongside the log-ratio form, which does not
# assume the legs covary at all. Where the composite and its components disagree, the components
# are believed. This is stated now, before any outcome has been looked at, so it cannot be
# mistaken for choosing whichever form gave the desired answer.

# %% [markdown]
# ## 4. Which component is load-bearing?
#
# For the confirmatory axes, drop each component in turn and see how much the axis changes. A
# correlation near 1 after dropping a component means that component was decoration; a low
# correlation means the axis *is* that component with extra steps.
#
# This is stated rather than hidden because two of the hypotheses rest on it. `AX_hea_index`
# weights three leaves, but `5.3a` and `8.3a` hold one topic each, so the axis is very close to
# leaf `4.5` alone — which is why notebook 05 reports `4.5` as H2's primary test.

# %%
loo_frames = []
for row in validity[validity["hypothesis_role"] == "confirmatory"].itertuples():
    spec = specs.get(row.axis)
    if spec is None or not spec.leaf_weights:
        continue
    members = [f"leaf_{leaf}" for leaf in spec.leaf_weights if f"leaf_{leaf}" in frame.columns]
    if len(members) < 2:
        continue
    block = frame[members]
    weights = {col: spec.leaf_weights[col.removeprefix("leaf_")] for col in members}
    table = rel.leave_one_out_stability(block, weights)
    table.insert(0, "axis", row.axis)
    table.insert(1, "hypothesis", row.hypothesis)
    table["n_topics_in_component"] = table["dropped_component"].map(
        lambda c: int(axis_coverage.loc[
            (axis_coverage["axis"] == row.axis)
            & (axis_coverage["leaf_id"] == c.removeprefix("leaf_")), "n_topics"
        ].max() if len(axis_coverage) else np.nan)
    )
    loo_frames.append(table)

if loo_frames:
    loo = pd.concat(loo_frames, ignore_index=True)
    display(loo[["axis", "hypothesis", "dropped_component", "weight", "n_topics_in_component",
                 "corr_with_full", "sign_flip_rate", "sign_stable"]].round(4))
    ctx.save_table(loo, "leave_one_component_out")

    critical = loo[loo["corr_with_full"] < 0.9]
    print(f"\n{len(critical)} components are load-bearing (dropping them changes the axis "
          f"materially):")
    for row in critical.itertuples():
        print(f"  {row.axis:<40} depends on {row.dropped_component} "
              f"(r = {row.corr_with_full:.3f} without it)")
else:
    loo = pd.DataFrame()
    print("No confirmatory axis has two or more measurable components.")

# %% [markdown]
# ## 5. Are the axes distinct from one another?
#
# Several axes deliberately share leaves. Leaf `4.6` (emotional safety and caretaking) sits in
# H1's numerator, in H4's positive leg, and in the payoff-safety fallback. If two axes are
# nearly the same variable, putting both in a model produces unstable coefficients that look
# like findings.
#
# Spearman correlations on the raw axes, with pairs above 0.85 flagged.

# %%
axis_corr = rel.axis_correlation_matrix(frame[AXIS_COLS], method="spearman")
redundant = rel.redundancy_flags(axis_corr, threshold=0.85)

print(f"Axis pairs correlated at |rho| >= 0.85: {len(redundant)}")
if len(redundant):
    display(redundant.round(3))
ctx.save_table(redundant, "redundant_axis_pairs")
ctx.save_table(axis_corr.reset_index().rename(columns={"index": "axis"}), "axis_correlations")

fig, ax = plt.subplots(figsize=(13, 11))
short = [c.removeprefix("AX_") for c in axis_corr.columns]
sns.heatmap(axis_corr.to_numpy(), cmap="RdBu_r", center=0, vmin=-1, vmax=1,
            xticklabels=short, yticklabels=short, ax=ax,
            cbar_kws={"label": "Spearman rho"}, square=True, linewidths=0.3)
ax.tick_params(labelsize=7)
ax.set_title("Axis correlations — dark blocks are axes that share taxonomy leaves")
ctx.save_figure(fig, "axis_correlation_matrix")
plt.show()

# %% [markdown]
# ## 6. Can the confirmatory axes go into one model together?
#
# Variance inflation factors, computed on the CLR-transformed axes that notebook 05 actually
# regresses. A VIF above 10 means the coefficient is not separately identified from the others.
# Where that happens, the hypothesis is tested one axis at a time instead of jointly.

# %%
confirmatory_axes = [
    a for a in axis_summary.loc[axis_summary["hypothesis_role"] == "confirmatory", "axis"]
    if a in frame.columns
]
clr_names = [f"{a}_clr" for a in confirmatory_axes if f"{a}_clr" in frame.columns]

vif = mdl.variance_inflation(frame, clr_names)
vif["predictor"] = vif["predictor"].str.removesuffix("_clr")
vif["separately_identified"] = vif["vif"] < 10
display(vif.round(3))
ctx.save_table(vif, "axis_vif")

print(f"\nAxes with VIF >= 10: {int((~vif['separately_identified']).sum())}")
print("Where an axis is not separately identified, notebook 05 tests it in its own model")
print("rather than jointly, and says so in the results table.")

# %% [markdown]
# ## 7. The distributions the hypotheses will be tested on
#
# Contrast axes are centred near zero by construction, and both tails matter: a book at the
# negative end of `AX_love_over_sex` is explicitly sexual relative to its emotional content,
# not merely low on something. Worth looking at before the tests, so no result later comes as
# a distributional surprise.

# %%
panel = confirmatory_axes[:6]
fig, axes = plt.subplots(2, 3, figsize=(15, 7))
for ax, col in zip(axes.ravel(), panel):
    sns.histplot(frame[col], bins=60, ax=ax, color="#4f81bd")
    ax.axvline(float(frame[col].mean()), color="#c0504d", ls="--", lw=1, label="mean")
    ax.set_title(col.removeprefix("AX_"), fontsize=9)
    ax.set_xlabel("axis value (share units)", fontsize=8)
    ax.legend(fontsize=7)
for ax in axes.ravel()[len(panel):]:
    ax.axis("off")
fig.suptitle("Confirmatory axis distributions — contrast axes straddle zero by design")
fig.tight_layout()
ctx.save_figure(fig, "confirmatory_axis_distributions")
plt.show()

axis_stats = frame[confirmatory_axes].describe().T[["count", "mean", "std", "min", "50%", "max"]]
axis_stats.columns = ["n", "mean", "sd", "min", "median", "max"]
display(axis_stats.round(4))
ctx.save_table(axis_stats.reset_index().rename(columns={"index": "axis"}), "axis_distributions")

# %% [markdown]
# ## 8. Log-ratio forms for the balance hypotheses
#
# H1 and H4 are stated as balances — "love **over** sex", "protective **versus** possessive" —
# and for compositional data the natural expression of a balance is a log-ratio, not a
# difference:
#
# \[ \text{LR} = \log\frac{\sum \text{numerator leaves} + \varepsilon}{\sum \text{denominator leaves} + \varepsilon} \]
#
# The log-ratio is scale-free, exactly antisymmetric (swapping the legs flips the sign), and
# unaffected by the rest of the composition. The difference form is kept alongside it because
# it is easier to read in percentage points; both are reported in notebook 05, and agreement
# between them is itself a robustness check.

# %%
for col in LOG_RATIO_COLS:
    print(f"{col}: mean {frame[col].mean():+.3f}, sd {frame[col].std():.3f}, "
          f"range [{frame[col].min():+.2f}, {frame[col].max():+.2f}]")

pairs = [("LR_H1_love_over_sex", "AX_love_over_sex"),
         ("LR_H4_protective_versus_possessive", "AX_protective_vs_possessive")]
pairs = [(lr, ax) for lr, ax in pairs if lr in frame.columns and ax in frame.columns]

fig, axes = plt.subplots(1, len(pairs), figsize=(6.5 * len(pairs), 4.6))
axes = np.atleast_1d(axes)
agreement_rows = []
for ax, (lr_col, ax_col) in zip(axes, pairs):
    rho = float(frame[lr_col].corr(frame[ax_col], method="spearman"))
    ax.scatter(frame[ax_col], frame[lr_col], s=4, alpha=0.12, color="#4f81bd")
    ax.set_xlabel(f"{ax_col.removeprefix('AX_')} (difference form)")
    ax.set_ylabel(f"{lr_col} (log-ratio form)")
    ax.set_title(f"Spearman rho = {rho:.3f}", fontsize=10)
    agreement_rows.append({"log_ratio": lr_col, "difference_axis": ax_col, "spearman_rho": rho})
fig.suptitle("Two ways of writing the same balance: do they order books the same way?")
fig.tight_layout()
ctx.save_figure(fig, "log_ratio_vs_difference")
plt.show()

display(pd.DataFrame(agreement_rows).round(4))
ctx.save_table(pd.DataFrame(agreement_rows), "log_ratio_agreement")

# %% [markdown]
# ## 9. Strict versus generous mapping
#
# Each topic gets a primary taxonomy category, and 239 of the 348 topics also get a secondary.
# The **strict** axes use primary assignments only; the **generous** axes add secondary
# assignments at half weight.
#
# If a conclusion depends on which variant is used, it depends on Stage 09's judgement calls
# about ambiguous topics rather than on the corpus. High agreement here is what licenses using
# strict as primary throughout; notebook 08 re-runs the hypothesis tests under generous.

# %%
strict = nbh.load_book_features(cfg, "book_axes_strict").set_index("book_id")
generous = nbh.load_book_features(cfg, "book_axes_generous").set_index("book_id")
shared = [c for c in strict.columns if c in generous.columns]

mapping_rows = []
for col in shared:
    left, right = strict[col], generous[col].reindex(strict.index)
    valid = pd.concat([left, right], axis=1).dropna()
    if len(valid) < 100 or valid.iloc[:, 0].std() == 0 or valid.iloc[:, 1].std() == 0:
        continue
    mapping_rows.append({
        "axis": col,
        "spearman_rho": float(valid.iloc[:, 0].corr(valid.iloc[:, 1], method="spearman")),
        "pearson_r": float(valid.iloc[:, 0].corr(valid.iloc[:, 1])),
        "mean_strict": float(valid.iloc[:, 0].mean()),
        "mean_generous": float(valid.iloc[:, 1].mean()),
    })

mapping = pd.DataFrame(mapping_rows).sort_values("spearman_rho")
mapping["robust_to_mapping"] = mapping["spearman_rho"] >= 0.90

print(f"Axes compared: {len(mapping)}")
print(f"  median Spearman rho between variants: {mapping['spearman_rho'].median():.3f}")
print(f"  axes below rho 0.90:                  {int((~mapping['robust_to_mapping']).sum())}")
display(mapping.round(4))
ctx.save_table(mapping, "strict_vs_generous_mapping")

fig, ax = plt.subplots(figsize=(9, 4.6))
ordered = mapping.sort_values("spearman_rho")
ax.barh(ordered["axis"].str.removeprefix("AX_"), ordered["spearman_rho"], color="#4f81bd")
ax.axvline(0.90, color="#c0504d", ls="--", lw=1, label="robustness threshold 0.90")
ax.set_xlim(0, 1.02)
ax.set_xlabel("Spearman rho between strict and generous mapping")
ax.tick_params(labelsize=7)
ax.set_title("How much does each axis depend on secondary category assignments?")
ax.legend(fontsize=8)
ctx.save_figure(fig, "strict_vs_generous_mapping")
plt.show()

# %% [markdown]
# ## 10. Testability verdicts
#
# The gate before notebook 05. Each hypothesis gets one of four statuses, and the reasoning is
# recorded so a reader can disagree with the judgement rather than having to reverse-engineer
# it.

# %%
def axis_row(axis_name):
    match = validity[validity["axis"] == axis_name]
    return match.iloc[0] if len(match) else None


hypotheses = cfg.get("hypotheses", {})
verdict_rows = []
for key in sorted(hypotheses):
    spec_cfg = hypotheses[key]
    axis_name = spec_cfg.get("primary_axis")
    coverage_row = axis_summary[axis_summary["axis"] == axis_name]
    validity_row = axis_row(axis_name)

    n_empty = int(coverage_row.iloc[0]["n_empty"]) if len(coverage_row) else np.nan
    n_viable = int(coverage_row.iloc[0]["n_viable"]) if len(coverage_row) else np.nan
    coverage_verdict = coverage_row.iloc[0]["axis_verdict"] if len(coverage_row) else "missing"

    if spec_cfg.get("level") == "tertile":
        rising = [l for l in spec_cfg.get("rising_leaves", []) if f"leaf_{l}" in frame.columns]
        falling = [l for l in spec_cfg.get("falling_leaves", []) if f"leaf_{l}" in frame.columns]
        status = "testable" if rising and falling else "not measurable"
        reason = (f"within-book design at tertile level; {len(rising)} rising and "
                  f"{len(falling)} falling leaves available")
        coverage_verdict = "tertile-level"
    elif axis_name not in frame.columns:
        status, reason = "not measurable", "axis could not be built from existing topics"
    elif key == "H3":
        status = "reframed"
        reason = ("original luxury formulation has no topics (6.1a, 6.6, 6.7 empty); "
                  "tested as material/social display instead")
    elif coverage_verdict == "weak" and n_viable <= 1:
        status, reason = "underpowered", f"{n_empty} empty and only {n_viable} viable component(s)"
    elif coverage_verdict == "weak":
        status, reason = "testable with caveats", f"{n_viable} viable but {n_empty} empty component(s)"
    else:
        status, reason = "testable", "all components viable"

    verdict_rows.append({
        "hypothesis": key,
        "name": spec_cfg.get("name"),
        "primary_axis": axis_name,
        "coverage_verdict": coverage_verdict,
        "validity_verdict": validity_row["verdict"] if validity_row is not None else "-",
        "n_viable_components": n_viable,
        "n_empty_components": n_empty,
        "status": status,
        "reason": reason,
        "power_note": spec_cfg.get("power_note", ""),
    })

verdicts = pd.DataFrame(verdict_rows)
display(verdicts)
ctx.save_table(verdicts, "hypothesis_testability")

print("\nStatus summary:")
display(verdicts["status"].value_counts().to_frame("n_hypotheses"))

# %%
summary = pd.DataFrame([
    ("axes built", f"{len(AXIS_COLS)}"),
    ("viable coverage", f"{int((axis_summary['axis_verdict'] == 'viable').sum())}"),
    ("weak coverage", f"{int((axis_summary['axis_verdict'] == 'weak').sum())}"),
    ("validity: valid", f"{int((validity['verdict'] == 'valid').sum())}"),
    ("validity: usable, low reliability", f"{int((validity['verdict'] == 'usable_low_reliability').sum())}"),
    ("validity: questionable", f"{int((validity['verdict'] == 'questionable').sum())}"),
    ("validity: atomic (single component)", f"{int((validity['verdict'] == 'atomic').sum())}"),
    ("redundant axis pairs (|rho| >= 0.85)", f"{len(redundant)}"),
    ("axes not separately identified (VIF >= 10)", f"{int((~vif['separately_identified']).sum())}"),
    ("strict vs generous median rho", f"{mapping['spearman_rho'].median():.3f}"),
    ("hypotheses testable", f"{int((verdicts['status'] == 'testable').sum())} of {len(verdicts)}"),
], columns=["item", "value"])
display(summary)
ctx.save_table(summary, "chapter_summary")

print(
    "\nWhat carries into notebook 05:\n"
    "  Confirmatory axes are tested in the form defined in the pre-registered schema, not in\n"
    "  whichever form performs best.\n"
    "  Because no composite passed the reliability checks, each is reported alongside its\n"
    "  strongest single component, and the components are believed where they disagree.\n"
    "  Axes marked atomic or weak carry their power limits into the results table, so a null\n"
    "  result on a one-topic leg is not read as evidence against the theory.\n"
    "  Balance hypotheses are reported in both difference and log-ratio form.\n"
    f"  AX_payoff_safety and AX_hea_index have VIF above 10 (they are both essentially leaf\n"
    f"  4.5), so they are never entered in the same model.\n"
)
print("Next: 05_hypothesis_tests.ipynb — H1 to H6 with effect sizes, models and arc analysis.")
