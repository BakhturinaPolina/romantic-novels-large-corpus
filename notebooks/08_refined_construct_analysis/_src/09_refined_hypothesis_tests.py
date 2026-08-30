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
    ("H1", "RLR_emotional_vs_explicit", "emotional vs explicit ratio"),
    ("H1", "RAX_nonexplicit_affection", "non-explicit affection"),
    ("H1", "RAX_explicit_sex", "explicit sex"),
    ("H1", "RAX_emotional_reassurance", "emotional reassurance"),
    ("H2", "RAX_h2_strict", "strict final payoff"),
    ("H2", "RAX_h2_broad", "broad HEA/commitment"),
    ("H2", "RAX_repair", "repair"),
    ("H3", "RLR_emotional_vs_material_security", "emotional vs material security"),
    ("H3", "RAX_h3_emotional_side", "emotional security side"),
    ("H3", "RAX_h3_material_side", "material provision side"),
    ("H3", "RAX_appearance_grooming", "appearance / grooming"),
    ("H3", "RAX_status_display", "status display"),
    ("H3", "RAX_workplace_status", "workplace status"),
    ("H3", "RAX_social_presentation", "social presentation (exploratory)"),
    ("H4", "RLR_protection_vs_control", "protection vs possession"),
    ("H4", "RAX_h4_protection_side", "external protection"),
    ("H4", "RAX_h4_possession_side", "possession / control"),
    ("H5", "RLR_darkness_vs_tenderness", "darkness vs tenderness"),
    ("H5", "RAX_relational_darkness", "relational darkness"),
    ("H5", "RAX_tenderness_core", "tenderness core"),
    ("H5", "RAX_external_danger_crisis", "external danger / crisis"),
    ("H5", "RAX_individual_distress", "individual distress"),
    ("H6", "RARC", "refined arc contrast"),
    ("H6", "DELTA_rising", "rising Δ (end−begin)"),
    ("H6", "DELTA_falling", "falling Δ (end−begin)"),
]

TIERS = ("low_rate", "mid_rate", "high_rate")
results = []
for hyp, feat, label in FEATURES:
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
        )
    )
effects = pd.DataFrame(results)
display(effects.round(4))
ctx.save_table(effects, "refined_hypothesis_effects")

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
