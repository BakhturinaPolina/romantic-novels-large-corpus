# %% [markdown]
# # 13 — Final statistical tests
#
# **Single source of truth for reportable inferential results.**
#
# This notebook contains only the tests prepared for the thesis / paper / presentation.
# It does **not** fish new topics. Constructs are frozen (H3/H4 manual freeze applied).
#
# > Once this notebook runs, do **not** redefine constructs because of its results.
# > Notebook 14 is for interpretation and presentation only.

# %% [markdown]
# ## Section 0 — Final frozen analysis definition
#
# | Item | Value |
# | --- | --- |
# | Corpus | ~16,000 analysable books (v3 English romance) |
# | Topic model | Stage 05 final fit (`v4_l12_granular_final_call49`) |
# | Primary outcome | `rating_shrunk` |
# | Secondary outcome | `log_n_ratings` (discriminant; not H1–H6 support) |
# | Effect gate | \(\lvert\delta\rvert \ge 0.11\) |
# | Controls | `log_pages`, `n_sentences`, `publication_year`, `genre_group` |
# | Uncertainty | author-cluster bootstrap CI for δ; cluster-robust SE for OLS |
# | FDR family | six primary H1–H6 tests only (BH) |
# | Freeze | `human_review/h3_manual_freeze.json`, `h4_manual_freeze.json` |
# | Claim hierarchy | `human_review/post_freeze_claim_hierarchy.md` |

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cwd = Path.cwd().resolve()
root = cwd
for _ in range(6):
    if (root / "configs").is_dir() and (root / "src").is_dir():
        break
    root = root.parent
sys.path.insert(0, str(root))

from src.stage10_correlation_analysis.analysis import tests as tst
from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh
from src.stage11_refined_construct_analysis.analysis import presentation as pres

ctx = nh.setup("13_final_statistical_tests")
cfg = ctx.cfg
GATE = nh.effect_gate(cfg)
coverage = nh.load_construct_coverage(cfg)
delta_freeze = cfg.section("stage10_delta_freeze")

N_BOOT = 400  # author-cluster replicates for final CIs
SEED = 42

# %% [markdown]
# ## Section 1 — Data and outcome sanity check

# %%
frame = nh.load_refined_frame(cfg, "strict")
if "book_id" in frame.columns:
    frame = frame.set_index("book_id")
usable = frame[frame["analysable"].fillna(True)].copy() if "analysable" in frame.columns else frame.copy()
work = usable.reset_index()

sanity = pd.DataFrame(
    [
        {"metric": "n_books", "value": float(len(work))},
        {
            "metric": "n_authors",
            "value": float(work["author_id"].nunique()) if "author_id" in work.columns else float("nan"),
        },
        {
            "metric": "rating_shrunk_mean",
            "value": float(work["rating_shrunk"].mean()) if "rating_shrunk" in work.columns else float("nan"),
        },
        {
            "metric": "rating_shrunk_median",
            "value": float(work["rating_shrunk"].median()) if "rating_shrunk" in work.columns else float("nan"),
        },
        {
            "metric": "quality_reach_corr",
            "value": float(work["rating_shrunk"].corr(work["log_n_ratings"]))
            if {"rating_shrunk", "log_n_ratings"} <= set(work.columns)
            else float("nan"),
        },
    ]
)
tier_counts = (
    work["rating_class"].value_counts().rename_axis("tier").reset_index(name="n")
    if "rating_class" in work.columns
    else pd.DataFrame()
)
display(sanity)
display(tier_counts)
ctx.save_table(sanity, "sanity_summary")
if len(tier_counts):
    ctx.save_table(tier_counts, "tier_sizes")

# %% [markdown]
# ## Sections 2–9 — Primary H1–H6 + inferential stack
#
# Cliff's δ (ordering), author-cluster CI, Kruskal–Wallis + ε², Spearman tier trend,
# adjusted OLS with author-cluster SE. FDR only on the six primaries.

# %%
PRIMARY = [
    ("H1", "RLR_emotional_vs_explicit", "emotional vs explicit ratio", +1),
    ("H2", "RAX_h2_strict", "strict final payoff", +1),
    ("H3", "RLR_emotional_vs_material_security", "emotional vs material security", +1),
    ("H4", "RLR_protection_vs_control", "protection vs possession", +1),
    ("H5", "RLR_darkness_vs_tenderness", "darkness vs tenderness", +1),
    ("H6", "RARC", "refined arc contrast", +1),
]

COMPONENTS = [
    ("H1", "RAX_emotional_reassurance", "emotional reassurance", None),
    ("H1", "RAX_explicit_sex", "explicit sex", None),
    ("H1", "RAX_nonexplicit_affection", "non-explicit affection", None),
    ("H3", "RAX_h3_emotional_side", "emotional security side", None),
    ("H3", "RAX_h3_material_side", "material provision side", None),
    ("H3", "RAX_appearance_grooming", "appearance / grooming", None),
    ("H4", "RAX_external_protection", "external protection (atom)", None),
    ("H4", "RAX_protective_commitment", "protective commitment", None),
    ("H4", "RAX_h4_possession_side", "possession / control", None),
    ("H5", "RAX_tenderness_core", "tenderness core", None),
    ("H5", "RAX_external_danger_crisis", "external danger / crisis", None),
    ("H5", "RAX_individual_distress", "individual distress", None),
    ("H5", "RAX_relational_darkness", "relational darkness", None),
    ("H6", "DELTA_rising", "rising Δ (end−begin)", None),
    ("H6", "DELTA_falling", "falling Δ (end−begin)", None),
]

PRIMARY_FEATURES = {f for _, f, _, _ in PRIMARY}

print("Running primary + component test_axis battery…")
all_specs = PRIMARY + COMPONENTS
results = []
for hyp, feat, label, expected_sign in all_specs:
    mgate = nh.gate_for_feature(coverage, feat)
    results.append(
        nh.test_axis(
            work,
            feat,
            hyp,
            label=label,
            n_replicates=N_BOOT,
            seed=SEED,
            measurement_gate=mgate,
            effect_gate=GATE,
            expected_sign=expected_sign,
        )
    )
effects = pd.DataFrame(results)

# Author-cluster bootstrap CIs (final displayed uncertainty for δ)
print("Author-cluster bootstrap CIs for δ…")
feat_list = [f for _, f, _, _ in all_specs if nh.gate_for_feature(coverage, f) != "unmeasurable"]
cluster_ci = nh.cliffs_delta_author_cluster_ci_many(
    work,
    feat_list,
    n_replicates=N_BOOT,
    seed=SEED,
)
ci_map = cluster_ci.set_index("feature") if len(cluster_ci) else pd.DataFrame()
effects["book_boot_ci_low"] = effects["ci_low"]
effects["book_boot_ci_high"] = effects["ci_high"]
author_lo, author_hi = [], []
for _, row in effects.iterrows():
    feat = row["feature"]
    if row.get("measurement_gate") == "unmeasurable" or feat not in ci_map.index:
        author_lo.append(float("nan"))
        author_hi.append(float("nan"))
        continue
    author_lo.append(float(ci_map.loc[feat, "ci_low"]))
    author_hi.append(float(ci_map.loc[feat, "ci_high"]))
effects["ci_low"] = author_lo
effects["ci_high"] = author_hi
# Recompute gated verdicts with author-cluster CIs
effects["verdict"] = [
    nh.gated_verdict(
        float(r["cliffs_delta"]) if pd.notna(r["cliffs_delta"]) else float("nan"),
        float(r["ci_low"]) if pd.notna(r["ci_low"]) else float("nan"),
        float(r["ci_high"]) if pd.notna(r["ci_high"]) else float("nan"),
        measurement_gate=str(r.get("measurement_gate") or "unknown"),
        effect_gate=GATE,
        expected_sign=r.get("expected_sign") if pd.notna(r.get("expected_sign")) else None,
    )
    for _, r in effects.iterrows()
]

# FDR on six primaries only
primary_mask = effects["feature"].isin(PRIMARY_FEATURES)
primary = effects.loc[primary_mask].copy()
if len(primary):
    kw_adj = tst.adjust_within_family(primary, "kw_p_value", method="fdr_bh", alpha=0.05)
    effects.loc[primary_mask, "kw_q_value"] = kw_adj["q_value"].to_numpy()
    if "quality_p" in primary.columns:
        q_adj = tst.adjust_within_family(primary, "quality_p", method="fdr_bh", alpha=0.05)
        effects.loc[primary_mask, "quality_q"] = q_adj["q_value"].to_numpy()

ctx.save_table(effects, "final_all_effects")
ctx.save_table(cluster_ci, "author_cluster_delta_ci")

primary_table = effects.loc[primary_mask].copy()
primary_view = primary_table[
    [
        c
        for c in [
            "hypothesis",
            "feature",
            "label",
            "measurement_gate",
            "cliffs_delta",
            "ci_low",
            "ci_high",
            "kw_p_value",
            "kw_q_value",
            "epsilon_squared",
            "spearman_rho",
            "quality_beta",
            "quality_p",
            "quality_q",
            "quality_ci_low",
            "quality_ci_high",
            "verdict",
        ]
        if c in primary_table.columns
    ]
].copy()
display(primary_view.round(4))
ctx.save_table(primary_view, "primary_h1_h6_table")

# %%
fig, ax = plt.subplots(figsize=(8, 4.5))
plot_p = primary_view.dropna(subset=["cliffs_delta"]).copy()
plot_p = plot_p[plot_p["measurement_gate"] != "unmeasurable"]
if len(plot_p):
    y = np.arange(len(plot_p))
    ax.errorbar(
        plot_p["cliffs_delta"],
        y,
        xerr=[
            plot_p["cliffs_delta"] - plot_p["ci_low"],
            plot_p["ci_high"] - plot_p["cliffs_delta"],
        ],
        fmt="o",
        color="steelblue",
        capsize=3,
    )
    ax.axvline(0, color="gray", lw=1)
    ax.axvline(GATE, color="red", ls="--", lw=0.8)
    ax.axvline(-GATE, color="red", ls="--", lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(plot_p["hypothesis"] + ": " + plot_p["feature"])
    ax.set_xlabel("Cliff's δ (author-cluster CI)")
    ax.set_title("Primary H1–H6 (measurable only)")
    ctx.save_figure(fig, "primary_h1_h6_forest")
plt.show()

# %% [markdown]
# ## Section 10 — Component / secondary analysis
#
# Not part of the primary FDR family. Confirmatory claim atoms (emotional security,
# appearance) sit here alongside thin / exploratory components.

# %%
component_mask = ~effects["feature"].isin(PRIMARY_FEATURES)
components = effects.loc[component_mask].copy()
display(components[
    [
        c
        for c in [
            "hypothesis",
            "feature",
            "label",
            "measurement_gate",
            "cliffs_delta",
            "ci_low",
            "ci_high",
            "spearman_rho",
            "quality_beta",
            "quality_p",
            "verdict",
        ]
        if c in components.columns
    ]
].round(4))
ctx.save_table(components, "component_effects")

CLAIM_HIERARCHY = [
    ("confirmatory", "H3", "RAX_h3_emotional_side", "Emotional reassurance/security positively associated with rating quality"),
    ("confirmatory", "H3", "RAX_appearance_grooming", "Appearance/grooming description negatively associated with rating quality"),
    ("qualified", "H5", "RAX_external_danger_crisis", "External danger positively associated with ratings"),
    ("open", "H4", "RAX_external_protection", "Is enacted protection within danger the attractive feature? (thin: 1 topic)"),
    ("unsupported", "H4", "RAX_protective_commitment", "Generic protective promises do not distinguish high-rated romance"),
    ("unmeasurable", "H3", "RLR_emotional_vs_material_security", "Material/economic security not cleanly captured at topic level"),
    ("open", "H4", "RLR_protection_vs_control", "Primary protection-vs-possession ratio thin/provisional (t119); directionally positive but below gate"),
]
claims_rows = []
for tier, hyp, feat, claim in CLAIM_HIERARCHY:
    row = effects[effects["feature"] == feat]
    claims_rows.append(
        {
            "claim_tier": tier,
            "hypothesis": hyp,
            "feature": feat,
            "claim": claim,
            "measurement_gate": row.iloc[0]["measurement_gate"] if len(row) else "missing",
            "cliffs_delta": float(row.iloc[0]["cliffs_delta"]) if len(row) else float("nan"),
            "verdict": row.iloc[0]["verdict"] if len(row) else "missing",
        }
    )
claims_df = pd.DataFrame(claims_rows)
display(claims_df.round(4))
ctx.save_table(claims_df, "post_freeze_claim_hierarchy")

# %% [markdown]
# ## Section 11 — H6 arc panel

# %%
arc_cols = [
    c
    for c in [
        "RAX_arc_rising_begin",
        "RAX_arc_rising_end",
        "RAX_arc_falling_begin",
        "RAX_arc_falling_end",
        "DELTA_rising",
        "DELTA_falling",
        "RARC",
    ]
    if c in work.columns
]
arc_medians = work[arc_cols].median().rename("median").to_frame()
arc_medians["mean"] = work[arc_cols].mean()
display(arc_medians.round(5))
ctx.save_table(arc_medians.reset_index().rename(columns={"index": "feature"}), "h6_arc_medians")

h6_feats = effects[effects["hypothesis"] == "H6"].copy()
display(h6_feats[
    [c for c in ["feature", "label", "cliffs_delta", "ci_low", "ci_high", "quality_beta", "quality_p", "verdict"] if c in h6_feats.columns]
].round(4))
ctx.save_table(h6_feats, "h6_arc_effects")

# %% [markdown]
# ## Section 12 — Secondary Goodreads reach (discriminant)
#
# Same final constructs against `log_n_ratings`. **Not** part of H1–H6 support verdicts.

# %%
reach_view = effects[
    [
        c
        for c in [
            "hypothesis",
            "feature",
            "label",
            "measurement_gate",
            "reach_beta",
            "reach_p",
            "cliffs_delta",
            "quality_beta",
            "verdict",
        ]
        if c in effects.columns
    ]
].copy()
reach_view = reach_view[reach_view["measurement_gate"] != "unmeasurable"]
display(reach_view.round(4))
ctx.save_table(reach_view, "reach_secondary_effects")

# %% [markdown]
# ## Section 13 — Robustness traffic-light (from NB11; no re-run)

# %%
try:
    stab = pres.load_notebook_table(cfg, "11_refined_robustness", "stability_summary")
    traffic = pres.traffic_light_from_stability(stab, gate=GATE)
    display(traffic)
    ctx.save_table(traffic, "robustness_traffic_light")
except FileNotFoundError as exc:
    print(f"NB11 stability_summary not found ({exc}); skipping traffic-light.")
    traffic = pd.DataFrame()

# %% [markdown]
# ## Section 14 — Final verdict table
#
# Supported / directional / contradicted / unmeasurable / inconclusive — presentation source of truth.

# %%
VERDICT_NOTES = {
    "H1": "Primary emotional-vs-explicit contrast under refined measurement.",
    "H2": "Strict HEA/final-payoff operationalisation; broad HEA remains exploratory.",
    "H3": "Primary ratio unmeasurable after material-side freeze; report emotional security (+) and appearance (−) as confirmatory components.",
    "H4": "Primary protection-vs-possession ratio is thin/provisional (protection atom t119 only); δ≈+0.090, directionally positive but below gate → inconclusive. Possession side viable; commitment atom unmeasurable; protection×danger exploratory (NB14).",
    "H5": "Darkness-vs-tenderness primary plus qualified external-danger component.",
    "H6": "Refined arc contrast (RARC) and begin→end deltas; no mixed-effects extension.",
}
final_verdict = pres.final_verdict_rows(primary_view, claim_notes=VERDICT_NOTES)
display(final_verdict)
ctx.save_table(final_verdict, "final_verdict_table")

md_lines = [
    "# Final H1–H6 verdicts (Notebook 13)",
    "",
    "Source of truth for confirmatory claims. Exploratory patterns belong in Notebook 14.",
    "",
]
for _, r in final_verdict.iterrows():
    md_lines.append(
        f"- **{r['hypothesis']}** [{r['final_bucket']}]: {r['one_sentence']} "
        f"(δ={r['cliffs_delta'] if pd.notna(r['cliffs_delta']) else '—'}; "
        f"gate={r['measurement_gate']}; raw={r['verdict_raw']})"
    )
ctx.save_markdown("\n".join(md_lines) + "\n", "final_verdict_table")

# Side-by-side Stage 10 freeze vs refined primary δ
side = []
mapping = {h: (f, delta_freeze.get(h)) for h, f, _, _ in PRIMARY}
for hyp, (feat, old) in mapping.items():
    row = effects[effects["feature"] == feat]
    side.append(
        {
            "hypothesis": hyp,
            "original_delta": old,
            "refined_feature": feat,
            "refined_delta": float(row.iloc[0]["cliffs_delta"]) if len(row) else np.nan,
            "measurement_gate": row.iloc[0]["measurement_gate"] if len(row) else "missing",
            "refined_verdict": row.iloc[0]["verdict"] if len(row) else "missing",
        }
    )
side_df = pd.DataFrame(side)
display(side_df)
ctx.save_table(side_df, "stage10_vs_final_side_by_side")

print(
    "Notebook 13 complete. Do not redefine constructs from these results. "
    "Use Notebook 14 for presentation / exploratory interpretation."
)
