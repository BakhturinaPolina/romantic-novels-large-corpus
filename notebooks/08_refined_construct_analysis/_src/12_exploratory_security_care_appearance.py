# %% [markdown]
# # 12 — Exploratory security, care & appearance
#
# **All analyses in this notebook are exploratory.** Topic sets are intentionally broader
# than the frozen confirmatory constructs and **do not alter H1–H6 verdicts.**
#
# Questions addressed:
# - How does δ change as we broaden semantic definitions (strict → moderate → broad)?
# - Which kinds of security promises distinguish high-rated romance?
# - Presence vs conditional intensity of themes
# - Danger × protection interaction
# - Emotional security × appearance quadrants
# - Fractional protection weights for mixed violence topics

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

from src.stage11_refined_construct_analysis.analysis import exploratory_security as ex
from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh

ctx = nh.setup("12_exploratory_security_care_appearance")
cfg = ctx.cfg
GATE = nh.effect_gate(cfg)
exp_cfg = ex.load_exploratory_config(root / "configs/stage11/exploratory_security_care_appearance.yaml")
families = exp_cfg["families"]
promise_types = exp_cfg["promise_types"]
presence_threshold = float(exp_cfg.get("presence_threshold", 1e-5))

# %%
frame = nh.load_refined_frame(cfg, "strict")
if "book_id" in frame.columns:
    frame = frame.set_index("book_id")
usable = frame[frame["analysable"].fillna(True)].copy() if "analysable" in frame.columns else frame.copy()
work = usable.reset_index()
if "book_id" not in work.columns and usable.index.name == "book_id":
    work["book_id"] = usable.index

shares = ex.topic_share_matrix(cfg)
master = pd.read_parquet(cfg.output_path("constructs_dir") / "master_annotations.parquet")

frac_cfg = exp_cfg.get("fractional_protection") or {}
frac_topics = frac_cfg.get("candidate_topics") or families["enacted_protection"].get("fractional_topics") or []
frac_weights = ex.build_fractional_protection_weights(
    cfg,
    candidate_topics=frac_topics,
    protection_codes=frac_cfg.get("protection_codes"),
)
weights_path = ctx.tables_dir / "exploratory_protection_weights.json"
ex.save_fractional_weights_json(frac_weights, weights_path)
print(f"Fractional protection weights saved → {weights_path}")
display(pd.Series(frac_weights, name="W_t_protection").sort_values(ascending=False))

# %%
work_exp = ex.add_topic_set_columns(work, shares, families, fractional_weights=frac_weights)

def _test(df, feat, hyp, label=""):
    return nh.test_axis(
        df,
        feat,
        hyp,
        label=label,
        measurement_gate="viable",
        effect_gate=GATE,
        expected_sign=None,
        n_replicates=400,
        seed=42,
    )

trajectories = ex.trajectory_effects(work_exp, families, test_fn=_test)
display(trajectories.round(4))
ctx.save_table(trajectories, "strict_moderate_broad_trajectories")

# Trajectory plot — skip unmeasurable (0-topic) points; never plot δ=0 for empty sets
fig, ax = plt.subplots(figsize=(10, 5))
level_order = ["strict", "moderate", "broad"]
for family in trajectories["family"].unique():
    sub = trajectories[trajectories["family"] == family].set_index("level").reindex(level_order)
    y = sub["cliffs_delta"].astype(float)
    if y.isna().all():
        continue
    ax.plot(level_order, y, marker="o", label=family)
    mask = y.notna()
    if mask.any():
        lo = sub["ci_low"].astype(float)
        hi = sub["ci_high"].astype(float)
        xs = [i for i, m in enumerate(mask) if m]
        ax.fill_between(
            xs,
            lo[mask].to_numpy(),
            hi[mask].to_numpy(),
            alpha=0.12,
        )
ax.axhline(0, color="gray", lw=1)
ax.axhline(GATE, color="red", ls="--", lw=0.8)
ax.axhline(-GATE, color="red", ls="--", lw=0.8)
ax.set_ylabel("Cliff's δ (high vs low rated)")
ax.set_title("Exploratory: strict → moderate → broad trajectories")
ax.legend(fontsize=8, bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
ctx.save_figure(fig, "trajectory_plot")
plt.show()

# %% [markdown]
# ## Per-topic forest (broad enacted protection + emotional security)

# %%
forest_frames = []
for family, level in [("enacted_protection", "broad"), ("emotional_security", "broad")]:
    tids = families[family].get(level) or []
    forest = ex.topic_level_forest(shares, work, tids, master, test_fn=_test)
    forest.insert(0, "family", family)
    forest_frames.append(forest)
forest_all = pd.concat(forest_frames, ignore_index=True)
display(forest_all.sort_values("cliffs_delta", ascending=False).round(4))
ctx.save_table(forest_all, "topic_forest_broad_families")

# %%
# Promise-type comparison table
promise_rows = []
for pname, tids in promise_types.items():
    tids = list(tids or [])
    if len(tids) == 0:
        promise_rows.append(
            {
                "promise_type": pname,
                "n_topics": 0,
                "cliffs_delta": float("nan"),
                "ci_low": float("nan"),
                "ci_high": float("nan"),
                "verdict": "unmeasurable",
                "note": "zero topics",
            }
        )
        continue
    col = f"EXP_promise_{pname}"
    tmp = work.copy()
    share = ex.topic_set_share(shares, tids)
    tmp[col] = ex._align_series_to_frame(share, tmp).values
    res = _test(tmp, col, "EXP", label=pname.replace("_", " "))
    promise_rows.append(
        {
            "promise_type": pname,
            "n_topics": len(tids),
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
            "note": "",
        }
    )
promise_df = pd.DataFrame(promise_rows).sort_values("cliffs_delta", ascending=False)
display(promise_df.round(4))
ctx.save_table(promise_df, "promise_type_comparison")

fig, ax = plt.subplots(figsize=(8, 5))
plot_p = promise_df.dropna(subset=["cliffs_delta"]).sort_values("cliffs_delta")
y = np.arange(len(plot_p))
ax.barh(y, plot_p["cliffs_delta"], color="steelblue", alpha=0.85)
ax.errorbar(
    plot_p["cliffs_delta"],
    y,
    xerr=[
        plot_p["cliffs_delta"] - plot_p["ci_low"],
        plot_p["ci_high"] - plot_p["cliffs_delta"],
    ],
    fmt="none",
    ecolor="black",
    capsize=2,
)
ax.set_yticks(y)
ax.set_yticklabels(plot_p["promise_type"], fontsize=9)
ax.axvline(0, color="gray")
ax.set_xlabel("Cliff's δ")
ax.set_title("Exploratory: promise/function types vs rating")
plt.tight_layout()
ctx.save_figure(fig, "promise_type_forest")
plt.show()

# %% [markdown]
# ## Protective-commitment +.210 audit (exploratory)
#
# The promise-type **protective_commitment** δ ≈ +.21 uses four deliberately selected
# topics. Family-level `protective_commitment` is empty at strict (unmeasurable),
# moderate ≈ +.17, and **broad (~14 topics) collapses to ~0**. Specific promise forms
# matter; “promises of protection” as a broad category do not.
#
# Fractional enacted-protection weights come from H4 Pass-B *sampled* contextual
# sentences — not a full-topic census. Mixed violence topics (e.g. 87) can contain
# protective speech without being clean protection topics.

# %%
pc_tids = list(promise_types.get("protective_commitment") or [])
pc_audit = ex.topic_level_forest(shares, work, pc_tids, master, test_fn=_test)
pc_audit.insert(0, "bundle", "promise_protective_commitment")
# Bundle-level δ for reference
pc_bundle = promise_df[promise_df["promise_type"] == "protective_commitment"]
if len(pc_bundle):
    pc_audit["bundle_cliffs_delta"] = float(pc_bundle.iloc[0]["cliffs_delta"])
display(pc_audit.round(4))
ctx.save_table(pc_audit, "protective_commitment_topic_audit")

# Fractional weights with Pass-B caveat
frac_tbl = (
    pd.Series(frac_weights, name="W_t_protection")
    .rename_axis("topic_id")
    .reset_index()
    .sort_values("W_t_protection", ascending=False)
)
frac_tbl["note"] = "Pass-B sampled sentences; not full-topic census"
display(frac_tbl.round(4))
ctx.save_table(frac_tbl, "fractional_protection_weights_table")

# Topic-id overlap: broad enacted protection vs RAX_external_danger_crisis
broad_prot = list(families.get("enacted_protection", {}).get("broad") or [])
danger_tids = ex.construct_topic_ids_from_w_tk(cfg, "RAX_external_danger_crisis")
overlap_df = ex.protection_danger_topic_overlap(broad_prot, danger_tids)
overlap_df["protection_topic_ids"] = ",".join(str(t) for t in sorted(broad_prot))
overlap_df["danger_topic_ids"] = ",".join(str(t) for t in danger_tids)
display(overlap_df)
ctx.save_table(overlap_df, "protection_danger_topic_overlap")
print(
    "Conceptual caveat: even with empty topic-id overlap, mixed violence topics "
    "receiving fractional protection weight may co-occur with danger discourse."
)

# %% [markdown]
# ## Presence vs conditional intensity

# %%
presence_rows = []
for family in families:
    for level in ("strict", "moderate", "broad"):
        col = f"EXP_{family}_{level}"
        if col not in work_exp.columns:
            continue
        s = work_exp.set_index("book_id")[col] if "book_id" in work_exp.columns else work_exp[col]
        stats = ex.presence_and_intensity(s, threshold=presence_threshold)
        presence_rows.append({"family": family, "level": level, **stats})
presence_df = pd.DataFrame(presence_rows)
display(presence_df.round(4))
ctx.save_table(presence_df, "presence_vs_intensity")

# %% [markdown]
# ## Danger × protection interaction
#
# Predictors are **z-scored** so coefficients are readable. The presentation artifact
# is the median-split 2×2 (does protection help more when danger is high?).

# %%
import seaborn as sns

interaction_rows = []
quad_frames = []
prot_specs = [
    ("EXP_enacted_protection_strict", "strict t119 only"),
    ("EXP_enacted_protection_moderate", "moderate + fractional"),
    ("EXP_enacted_protection_broad", "broad enacted"),
]
for prot_col, label in prot_specs:
    if prot_col not in work_exp.columns:
        continue
    tmp = work_exp.copy()
    tmp[prot_col] = tmp[prot_col].fillna(0.0)
    inter = ex.danger_protection_interaction(
        tmp.set_index("book_id") if "book_id" in tmp.columns else tmp,
        protection_col=prot_col,
    )
    row = {"protection_index": label, "protection_col": prot_col}
    for term in ("z_danger", "z_protection", "z_danger_x_z_protection"):
        payload = inter.get(term) or {}
        row[f"{term}_beta"] = payload.get("beta")
        row[f"{term}_se"] = payload.get("se")
        row[f"{term}_p"] = payload.get("p")
    interaction_rows.append(row)
    q = ex.danger_protection_quadrants(
        tmp,
        protection_col=prot_col,
        protection_label=label,
    )
    if len(q):
        quad_frames.append(q)

interaction_df = pd.DataFrame(interaction_rows)
display(interaction_df.round(4))
ctx.save_table(interaction_df, "danger_x_protection_interaction")

quad_all = pd.concat(quad_frames, ignore_index=True) if quad_frames else pd.DataFrame()
display(quad_all.round(4))
ctx.save_table(quad_all, "danger_x_protection_quadrants")

# Heatmaps for strict and moderate
for label in ("strict t119 only", "moderate + fractional"):
    sub = quad_all[quad_all["protection_index"] == label] if len(quad_all) else pd.DataFrame()
    if sub.empty:
        continue
    mat = sub.pivot(index="danger_bin", columns="protection_bin", values="mean_rating")
    row_order = [r for r in ("lower_danger", "higher_danger") if r in mat.index]
    col_order = [c for c in ("lower_protection", "higher_protection") if c in mat.columns]
    mat = mat.reindex(index=row_order, columns=col_order)
    fig, ax = plt.subplots(figsize=(5.5, 4))
    sns.heatmap(mat, annot=True, fmt=".3f", cmap="YlOrRd", ax=ax)
    ax.set_title(f"Mean rating: danger × protection ({label})")
    safe = label.replace(" ", "_").replace("+", "plus")
    ctx.save_figure(fig, f"danger_x_protection_heatmap_{safe}")
    plt.show()
# %% [markdown]
# ## Emotional security × appearance quadrants

# %%
if "EXP_emotional_security_strict" in work_exp.columns and "EXP_appearance_strict" in work_exp.columns:
    quad_df = ex.quadrant_summary(
        work_exp.set_index("book_id") if "book_id" in work_exp.columns else work_exp,
        "EXP_emotional_security_strict",
        "EXP_appearance_strict",
    )
    display(quad_df.round(4))
    ctx.save_table(quad_df, "care_x_appearance_quadrants")

# %% [markdown]
# ## Fractional protection vs strict t119-only

# %%
compare_rows = []
for col in [
    "EXP_enacted_protection_strict",
    "EXP_enacted_protection_moderate",
    "RAX_external_protection",
]:
    if col not in work_exp.columns:
        continue
    res = _test(work_exp, col, "H4", label=col)
    compare_rows.append(
        {
            "index": col,
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
        }
    )
frac_compare = pd.DataFrame(compare_rows)
display(frac_compare.round(4))
ctx.save_table(frac_compare, "fractional_vs_strict_protection")
print("Exploratory notebook complete — results do not modify confirmatory H1–H6 verdicts.")
