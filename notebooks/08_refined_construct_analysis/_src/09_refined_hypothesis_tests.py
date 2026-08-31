# %% [markdown]
# # 09 — Refined hypothesis tests
#
# Same Stage 10 statistical machinery; new measurements. Side-by-side original vs refined
# δ values are **not** claimed commensurable — they show how conclusions change after
# measurement repair.
#
# Sequence per axis: Cliff's δ → three-tier trend → quality/reach OLS with length+era+genre
# controls and author-cluster-robust SE → measurement-gated verdict.

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

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh

ctx = nh.setup("09_refined_hypothesis_tests")
cfg = ctx.cfg
GATE = nh.effect_gate(cfg)
delta_freeze = cfg.section("stage10_delta_freeze")
coverage = nh.load_construct_coverage(cfg)

# %%
frame = nh.load_refined_frame(cfg, "strict")
if "book_id" in frame.columns:
    frame = frame.set_index("book_id")
usable = frame[frame["analysable"].fillna(True)].copy() if "analysable" in frame.columns else frame.copy()
# Reset index for statsmodels helpers that expect columns
work = usable.reset_index()

FEATURES = [
    # (hyp, feature, label, expected_sign) — expected_sign only for primary hypothesis tests
    ("H1", "RLR_emotional_vs_explicit", "emotional vs explicit ratio", +1),
    ("H1", "RAX_nonexplicit_affection", "non-explicit affection", None),
    ("H1", "RAX_explicit_sex", "explicit sex", None),
    ("H1", "RAX_emotional_reassurance", "emotional reassurance", None),
    ("H2", "RAX_h2_strict", "strict final payoff", +1),
    ("H2", "RAX_h2_broad", "broad HEA/commitment", None),
    ("H2", "RAX_repair", "repair", None),
    ("H3", "RLR_emotional_vs_material_security", "emotional vs material security", +1),
    ("H3", "RAX_h3_emotional_side", "emotional security side", None),
    ("H3", "RAX_h3_material_side", "material provision side", None),
    ("H3", "RAX_appearance_grooming", "appearance / grooming", None),
    ("H3", "RAX_status_display", "status display", None),
    ("H3", "RAX_workplace_status", "workplace status", None),
    ("H3", "RAX_social_presentation", "social presentation (exploratory)", None),
    ("H4", "RLR_protection_vs_control", "protection vs possession", +1),
    ("H4", "RAX_h4_protection_side", "external protection", None),
    ("H4", "RAX_h4_possession_side", "possession / control", None),
    ("H4", "RAX_external_protection", "external protection (atom)", None),
    ("H4", "RAX_protective_commitment", "protective commitment", None),
    ("H4", "RAX_protective_care_broad", "protective care broad (exploratory)", None),
    ("H5", "RLR_darkness_vs_tenderness", "darkness vs tenderness", +1),
    ("H5", "RAX_relational_darkness", "interpersonal/conflict darkness", None),
    ("H5", "RAX_tenderness_core", "tenderness core", None),
    ("H5", "RAX_external_danger_crisis", "external danger / crisis", None),
    ("H5", "RAX_individual_distress", "individual distress", None),
    ("H6", "RARC", "refined arc contrast", +1),
    ("H6", "DELTA_rising", "rising Δ (end−begin)", None),
    ("H6", "DELTA_falling", "falling Δ (end−begin)", None),
]

PRIMARY_FEATURES = {
    "RLR_emotional_vs_explicit",
    "RAX_h2_strict",
    "RLR_emotional_vs_material_security",
    "RLR_protection_vs_control",
    "RLR_darkness_vs_tenderness",
    "RARC",
}

TIERS = ("low_rate", "mid_rate", "high_rate")
results = []
for hyp, feat, label, expected_sign in FEATURES:
    mgate = nh.gate_for_feature(coverage, feat)
    results.append(
        nh.test_axis(
            work,
            feat,
            hyp,
            label=label,
            tiers=TIERS,
            n_replicates=400,
            seed=42,
            measurement_gate=mgate,
            effect_gate=GATE,
            expected_sign=expected_sign,
        )
    )
effects = pd.DataFrame(results)

# FDR (Benjamini–Hochberg) on the six primary hypothesis tests only.
# Component / exploratory p-values remain unadjusted.
from src.stage10_correlation_analysis.analysis import tests as tst

primary_mask = effects["feature"].isin(PRIMARY_FEATURES)
primary = effects.loc[primary_mask].copy()
if len(primary):
    kw_adj = tst.adjust_within_family(primary, "kw_p_value", method="fdr_bh", alpha=0.05)
    effects.loc[primary_mask, "kw_q_value"] = kw_adj["q_value"].to_numpy()
    if "quality_p" in primary.columns:
        q_adj = tst.adjust_within_family(primary, "quality_p", method="fdr_bh", alpha=0.05)
        effects.loc[primary_mask, "quality_q"] = q_adj["q_value"].to_numpy()

display(effects.round(4))
ctx.save_table(effects, "refined_hypothesis_effects")

print(
    "Primary verdicts use expected direction (supported / directionally consistent / "
    "contradicted / no reliable effect), wrapped by measurement gates. "
    "FDR (BH) is applied only to the six primary kw_p / quality_p values; "
    "component analyses are exploratory/unadjusted."
)

# Post-freeze claim hierarchy (H3/H4 manual freeze applied)
CLAIM_HIERARCHY = [
    ("confirmatory", "H3", "RAX_h3_emotional_side", "Emotional reassurance/security positively associated with rating quality"),
    ("confirmatory", "H3", "RAX_appearance_grooming", "Appearance/grooming description negatively associated with rating quality"),
    ("qualified", "H5", "RAX_external_danger_crisis", "External danger positively associated with ratings"),
    ("open", "H4", "RAX_external_protection", "Is enacted protection within danger the attractive feature? (thin: 1 topic)"),
    ("unsupported", "H4", "RAX_protective_commitment", "Generic protective promises do not distinguish high-rated romance"),
    ("unmeasurable", "H3", "RLR_emotional_vs_material_security", "Material/economic security not cleanly captured at topic level"),
    ("unmeasurable", "H4", "RLR_protection_vs_control", "Protective commitment atom empty; protection side thin"),
]
claims_rows = []
for tier, hyp, feat, claim in CLAIM_HIERARCHY:
    row = effects[effects["feature"] == feat]
    delta = float(row.iloc[0]["cliffs_delta"]) if len(row) else float("nan")
    gate = row.iloc[0]["measurement_gate"] if len(row) else "missing"
    verdict = row.iloc[0]["verdict"] if len(row) else "missing"
    claims_rows.append(
        {
            "claim_tier": tier,
            "hypothesis": hyp,
            "feature": feat,
            "claim": claim,
            "measurement_gate": gate,
            "cliffs_delta": delta,
            "verdict": verdict,
        }
    )
claims_df = pd.DataFrame(claims_rows)
display(claims_df.round(4))
ctx.save_table(claims_df, "post_freeze_claim_hierarchy")
print(
    "H3 primary ratio and H4 protective commitment are unmeasurable after strict manual freeze; "
    "report emotional security + appearance (H3) and possession + exploratory protection (H4)."
)
# Compact δ view (backward-compatible table name)
delta_view = effects[
    [
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
        "reach_beta",
        "reach_p",
        "verdict",
    ]
].copy()
display(delta_view.round(4))
ctx.save_table(delta_view, "refined_hypothesis_delta_view")

# %% [markdown]
# ## Side-by-side with Stage 10 primary δ

# %%
side = []
mapping = {
    "H1": ("RLR_emotional_vs_explicit", delta_freeze.get("H1")),
    "H2": ("RAX_h2_strict", delta_freeze.get("H2")),
    "H3": ("RLR_emotional_vs_material_security", delta_freeze.get("H3")),
    "H4": ("RLR_protection_vs_control", delta_freeze.get("H4")),
    "H5": ("RLR_darkness_vs_tenderness", delta_freeze.get("H5")),
    "H6": ("RARC", delta_freeze.get("H6")),
}
for hyp, (feat, old) in mapping.items():
    row = effects[effects["feature"] == feat]
    refined = float(row.iloc[0]["cliffs_delta"]) if len(row) else np.nan
    side.append(
        {
            "hypothesis": hyp,
            "original_delta": old,
            "refined_feature": feat,
            "refined_delta": refined,
            "measurement_gate": row.iloc[0]["measurement_gate"] if len(row) else "missing",
            "refined_verdict": row.iloc[0]["verdict"] if len(row) else "missing",
        }
    )
side_df = pd.DataFrame(side)
display(side_df)
ctx.save_table(side_df, "stage10_vs_stage11_side_by_side")

# %%
plot_df = effects.dropna(subset=["cliffs_delta"]).copy()
plot_df = plot_df[plot_df["measurement_gate"] != "unmeasurable"]
plot_df = plot_df.sort_values("cliffs_delta")
fig, ax = plt.subplots(figsize=(9, 7))
y = np.arange(len(plot_df))
colors = [
    "#c44e52" if g == "thin" else "steelblue" for g in plot_df["measurement_gate"]
]
ax.barh(y, plot_df["cliffs_delta"], color=colors, alpha=0.85)
ax.errorbar(
    plot_df["cliffs_delta"],
    y,
    xerr=[
        plot_df["cliffs_delta"] - plot_df["ci_low"],
        plot_df["ci_high"] - plot_df["cliffs_delta"],
    ],
    fmt="none",
    ecolor="black",
    capsize=2,
)
ax.axvline(0, color="gray", lw=1)
ax.axvline(GATE, color="red", ls="--", lw=0.8)
ax.axvline(-GATE, color="red", ls="--", lw=0.8)
ax.set_yticks(y)
ax.set_yticklabels(
    [f"{r.hypothesis}:{r.feature}" for r in plot_df.itertuples()], fontsize=8
)
ax.set_xlabel("Cliff's δ (high vs low rated)")
ax.set_title("Stage 11 refined measures (red = thin measurement)")
ctx.save_figure(fig, "refined_effects_forest")
plt.show()

print(
    f"Effect gate |δ|≥{GATE} with CI excluding 0. "
    "Unmeasurable axes are excluded from the forest; thin axes are flagged in red. "
    "Components take precedence when they disagree with composites."
)
