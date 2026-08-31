# %% [markdown]
# # 15 — Emotion, embodiment & social world (exploratory)
#
# **Exploratory analysis.** The thematic families examined here were motivated
# partly by patterns observed in the Stage 10 topic landscape and subsequent
# human review. They are therefore post-hoc and do not constitute independent
# hypothesis tests. Topic membership is defined from semantic evidence before
# inspecting within-family rating effects, and all results are interpreted
# primarily through effect sizes, confidence intervals, robustness and semantic
# coherence.
#
# The 38 Stage-10 survivors (`|δ| ≥ .11`, CI excludes zero) are **seeds for
# questions**, not the analysis candidate set. Candidates are retrieved from the
# full ~348 mapped topics (leaf ∪ lexical prototypes), coded rating-blind, then
# frozen before effects.
#
# **This notebook does not alter H1–H6 or NB13 confirmatory verdicts.**

# %%
import json
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

from src.stage11_refined_construct_analysis.analysis import exploratory_ees as ees
from src.stage11_refined_construct_analysis.analysis import exploratory_security as ex
from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh

NOTEBOOK = "15_emotion_embodiment_social_world_exploration"
ctx = nh.setup(NOTEBOOK)
cfg = ctx.cfg
GATE = nh.effect_gate(cfg)

ees_cfg = ees.load_exploratory_ees_config(root / "configs/stage11/exploratory_emotion_embodiment_social_world.yaml")
FROZEN = ees.is_frozen(ees_cfg)
PROVISIONAL = ees.is_provisional(ees_cfg)
print(f"Freeze status : frozen={FROZEN} provisional={PROVISIONAL}")
print(f"Freeze note   : {(ees_cfg.get('freeze_note') or '')[:160]}")

# %% [markdown]
# ## Setup — book frame, shares, tertiles

# %%
frame = nh.load_refined_frame(cfg, "strict")
if "book_id" in frame.columns:
    frame = frame.set_index("book_id")
usable = frame[frame["analysable"].fillna(True)].copy() if "analysable" in frame.columns else frame.copy()
work = usable.reset_index()
if "book_id" not in work.columns and usable.index.name == "book_id":
    work["book_id"] = usable.index

shares = ex.topic_share_matrix(cfg)
tertile_counts = ees.load_tertile_topic_counts(cfg)
master = pd.read_parquet(cfg.output_path("constructs_dir") / "master_annotations.parquet")

ees_dir = Path(ees_cfg.get("outputs", {}).get("ees_dir") or cfg.output_path("ees_exploration_dir"))
if not ees_dir.is_absolute():
    ees_dir = root / ees_dir

candidates = pd.read_csv(ees_dir / "candidate_topics.csv")
codes_path = ees_dir / "semantic_codes.csv"
if codes_path.exists():
    semantic_codes = pd.read_csv(codes_path)
else:
    semantic_codes = pd.DataFrame()
    print("WARNING: semantic_codes.csv missing — run pipeline/10_run_ees_coding.py")

construct_dict = ees.construct_dictionary_frame(ees_cfg)
ctx.save_table(candidates, "candidate_topics")
ctx.save_table(semantic_codes, "semantic_codes")
ctx.save_table(construct_dict, "construct_dictionary")
print(f"Candidates: {len(candidates):,} rows | codes: {len(semantic_codes):,} | dict rows: {len(construct_dict):,}")

if not FROZEN:
    print(
        "\n*** PROVISIONAL FREEZE ***\n"
        "Effects below use YAML seed membership. Re-run after LLM+human freeze "
        "(set frozen: true) before presentation claims.\n"
    )

# %%
work_ees = ees.add_ees_share_columns(work, shares, ees_cfg, level="moderate")
constructs = ees.active_constructs(ees_cfg, level="moderate")
coherence = ees.coherence_table(shares, constructs)
display(coherence)
ctx.save_table(coherence, "construct_robustness")

def _test(df, feat, hyp, label=""):
    gate = coherence.set_index("construct")["status"].to_dict().get(
        feat.replace("EES_", "").replace("EXP_", ""), "measurable"
    )
    # Map EXP_/EES_ family columns back to construct names for gate
    cname = feat
    for prefix in ("EES_", "EXP_"):
        if cname.startswith(prefix):
            cname = cname[len(prefix):]
            break
    # strip trailing _strict/_moderate/_broad
    for suf in ("_strict", "_moderate", "_broad"):
        if cname.endswith(suf):
            cname = cname[: -len(suf)]
            break
    status = coherence.set_index("construct")["status"].to_dict().get(cname, "measurable")
    return nh.test_axis(
        df,
        feat,
        hyp,
        label=label or feat,
        measurement_gate="unmeasurable" if status == "unmeasurable" else "viable",
        effect_gate=GATE,
        expected_sign=None,
        n_replicates=400,
        seed=42,
    )

# %% [markdown]
# ---
# # Part I — Emotion & embodiment
#
# Narrative emotion **functions** (E0–E11), not mere positive/negative valence.
# Motivating literature (interpretive only): Martínez (2024) on physiological
# narrated perception; emotion-regulation theory as a conceptual guide — codes
# require prose support.

# %%
emotion_families = [
    "emotion_distress_expressed",
    "emotion_physiological_arousal",
    "emotion_physical_vulnerability",
    "emotion_visible_affect",
    "emotion_containment",
    "emotion_coregulation",
    "emotion_physical_comfort",
    "emotion_relief",
    "emotion_rumination",
]

emotion_rows = []
for fam in emotion_families:
    col = f"EES_{fam}"
    if col not in work_ees.columns:
        continue
    status = coherence.set_index("construct").loc[fam, "status"] if fam in coherence["construct"].values else "measurable"
    n_topics = int(coherence.set_index("construct").loc[fam, "n_topics"]) if fam in coherence["construct"].values else 0
    res = _test(work_ees, col, "EES", label=fam)
    share = work_ees[col]
    emotion_rows.append(
        {
            "construct": fam,
            "n_topics": n_topics,
            "status": status,
            "mean_share": float(share.mean()),
            "median_share": float(share.median()),
            "mean_high": res.get("mean_high"),
            "mean_low": res.get("mean_low"),
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
            "ols_beta": res.get("ols_beta") or res.get("quality_beta"),
        }
    )

# Prefer author-cluster CI when available
try:
    ac = nh.cliffs_delta_author_cluster_ci_many(
        work_ees,
        [f"EES_{f}" for f in emotion_families if f"EES_{f}" in work_ees.columns],
        n_replicates=400,
        seed=42,
    )
    emotion_eff = pd.DataFrame(emotion_rows)
    if len(ac):
        ac = ac.copy()
        ac["construct"] = ac["feature"].str.replace("^EES_", "", regex=True)
        emotion_eff = emotion_eff.drop(columns=["cliffs_delta", "ci_low", "ci_high"], errors="ignore").merge(
            ac[["construct", "cliffs_delta", "ci_low", "ci_high"]],
            on="construct",
            how="left",
        )
except Exception as exc:
    print("Author-cluster CI fallback:", exc)
    emotion_eff = pd.DataFrame(emotion_rows)

display(emotion_eff.round(4))
ctx.save_table(emotion_eff, "emotion_effects")

fig, ax = ees.forest_plot(
    emotion_eff.rename(columns={"construct": "construct"}),
    title="Ways emotion appears: high-rated versus low-rated (exploratory)",
)
ctx.save_figure(fig, "emotion_function_forest")
plt.show()

# %% [markdown]
# ### Presence versus intensity (corpus-wide 75th percentile gate)

# %%
presence_rows = []
for fam in emotion_families:
    col = f"EES_{fam}"
    if col not in work_ees.columns:
        continue
    tab = ees.presence_intensity_by_group(work_ees, col)
    presence_rows.append(tab)
presence_emotion = pd.concat(presence_rows, ignore_index=True) if presence_rows else pd.DataFrame()
display(presence_emotion.round(4))
ctx.save_table(presence_emotion, "emotion_presence_intensity")

# %% [markdown]
# ### Emotion over narrative position (begin | middle | end)

# %%
pos_names = list(ees_cfg.get("position_constructs") or [])
pos_constructs = {
    name: constructs.get(name, [])
    for name in pos_names
    if name in constructs
}
traj, pos_effects, delta_frame = ees.position_effects_table(
    tertile_counts,
    pos_constructs,
    work_ees,
    test_fn=_test,
)
display(pos_effects.round(4))
ctx.save_table(pos_effects, "emotion_position_effects")
ctx.save_table(traj, "emotion_position_trajectories")

fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharex=True)
axes = axes.ravel()
for i, feat in enumerate(list(pos_constructs)[:6]):
    ees.trajectory_plot(traj, feature=feat, ax=axes[i], title=feat.replace("emotion_", ""))
for j in range(i + 1, len(axes)):
    axes[j].axis("off")
fig.suptitle("Emotion functions across narrative position (exploratory)")
fig.tight_layout()
ctx.save_figure(fig, "emotion_trajectories")
plt.show()

# %% [markdown]
# ---
# # Part II — Felt body versus looked-at body
#
# Body as medium of lived experience vs body as object of observation.
# Keep B3 (tattoos/scars) separate — Topic 370 is an important exception to
# “more bodily description = lower ratings.”

# %%
body_families = [
    "body_interoceptive",
    "body_vulnerable",
    "body_markings",
    "body_external_appearance",
    "body_grooming",
]
body_rows = []
for fam in body_families:
    col = f"EES_{fam}"
    if col not in work_ees.columns:
        continue
    res = _test(work_ees, col, "EES", label=fam)
    status = coherence.set_index("construct").loc[fam, "status"] if fam in coherence["construct"].values else ""
    n_topics = int(coherence.set_index("construct").loc[fam, "n_topics"]) if fam in coherence["construct"].values else 0
    body_rows.append(
        {
            "construct": fam,
            "n_topics": n_topics,
            "status": status,
            "mean_share": float(work_ees[col].mean()),
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
        }
    )

# Composites + log-ratio
for name in ("felt_body", "looked_at_body", "felt_vs_looked_logratio"):
    col = f"EES_{name}"
    if col not in work_ees.columns:
        continue
    res = _test(work_ees, col, "EES", label=name)
    body_rows.append(
        {
            "construct": name,
            "n_topics": len(constructs.get(name, [])) if name != "felt_vs_looked_logratio" else None,
            "status": coherence.set_index("construct")["status"].to_dict().get(name, ""),
            "mean_share": float(work_ees[col].mean()),
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
        }
    )

embodiment_eff = pd.DataFrame(body_rows)
display(embodiment_eff.round(4))
ctx.save_table(embodiment_eff, "embodiment_effects")

felt_looked = embodiment_eff[
    embodiment_eff["construct"].isin(
        body_families + ["felt_body", "looked_at_body", "felt_vs_looked_logratio"]
    )
].copy()
ctx.save_table(felt_looked, "felt_vs_looked_body")

fig, ax = ees.forest_plot(
    felt_looked[felt_looked["construct"].isin(body_families)],
    title="Felt body vs looked-at body subtypes (exploratory)",
)
ctx.save_figure(fig, "felt_vs_looked_body")
plt.show()

# %% [markdown]
# ---
# # Part III — Family & social embeddedness
#
# Nested measures: family presence (S1–S8), supportive embeddedness, social
# pressure/conflict. Positive δ for family pressure does **not** imply harmony —
# social stakes may matter more than social warmth.

# %%
social_families = [
    "family_presence",
    "supportive_social_embeddedness",
    "social_pressure_conflict",
]
social_rows = []
for fam in social_families:
    col = f"EES_{fam}"
    if col not in work_ees.columns:
        continue
    res = _test(work_ees, col, "EES", label=fam)
    social_rows.append(
        {
            "construct": fam,
            "n_topics": int(coherence.set_index("construct").loc[fam, "n_topics"])
            if fam in coherence["construct"].values
            else 0,
            "status": coherence.set_index("construct").loc[fam, "status"]
            if fam in coherence["construct"].values
            else "",
            "mean_share": float(work_ees[col].mean()),
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
        }
    )
family_social_eff = pd.DataFrame(social_rows)
display(family_social_eff.round(4))
ctx.save_table(family_social_eff, "family_social_effects")

fig, ax = ees.forest_plot(
    family_social_eff,
    title="Family / social embeddedness (exploratory)",
)
ctx.save_figure(fig, "family_social_forest")
plt.show()

# Social-domain richness (≠ NB14 Shannon thematic richness)
domains = ees_cfg.get("social_domains") or {}
work_ees["EES_social_domain_richness"] = ees.social_domain_richness(
    work_ees, shares, domains
).values
sdr = _test(work_ees, "EES_social_domain_richness", "EES", label="social_domain_richness")
sdr_row = pd.DataFrame(
    [
        {
            "construct": "social_domain_richness",
            "mean": float(work_ees["EES_social_domain_richness"].mean()),
            "median": float(work_ees["EES_social_domain_richness"].median()),
            "cliffs_delta": sdr.get("cliffs_delta"),
            "ci_low": sdr.get("ci_low"),
            "ci_high": sdr.get("ci_high"),
            "verdict": sdr.get("verdict"),
            "note": "Count of social domains above corpus p75; not Shannon entropy",
        }
    ]
)
display(sdr_row.round(4))
ctx.save_table(sdr_row, "social_domain_richness")

# %% [markdown]
# ---
# # Part IV — Three pre-registered cross-family tests

# %%
# 12. Embodied distress × interpersonal co-regulation
ix1 = ees.interaction_ols(
    work_ees,
    "EES_embodied_distress",
    "EES_co_regulation",
    name="embodied_distress_x_coregulation",
)
# 13. Family embeddedness × emotional reassurance (coregulation proxy)
ix2 = ees.interaction_ols(
    work_ees,
    "EES_family_presence",
    "EES_emotion_coregulation",
    name="family_x_emotional_reassurance",
)
cross_rows = []
for ix in (ix1, ix2):
    if ix.get("status") != "ok":
        cross_rows.append({"name": ix.get("name"), "status": ix.get("status")})
        continue
    inter = ix.get("interaction") or {}
    cross_rows.append(
        {
            "name": ix.get("name"),
            "status": "ok",
            "beta_interaction": inter.get("beta"),
            "se": inter.get("se"),
            "p": inter.get("p"),
            "ci_low": inter.get("ci_low"),
            "ci_high": inter.get("ci_high"),
            "beta_x": (ix.get("z_x") or {}).get("beta"),
            "beta_y": (ix.get("z_y") or {}).get("beta"),
        }
    )
cross_df = pd.DataFrame(cross_rows)
display(cross_df.round(4))
ctx.save_table(cross_df, "cross_family_interactions")

# 14. Felt × looked-at 2×2 (descriptive)
quad = ees.median_split_quadrants(
    work_ees,
    "EES_felt_body",
    "EES_looked_at_body",
    x_high="high_felt",
    x_low="low_felt",
    y_high="high_looked",
    y_low="low_looked",
)
display(quad.round(4))
ctx.save_table(quad, "felt_looked_quadrants")

# %% [markdown]
# ---
# # Part V — Cognition screen (hard gate: ≥3 coherent topics)

# %%
cog_codes = (ees_cfg.get("code_membership") or {}).get("cognition") or {}
cog_rows = []
n_coherent = 0
for code, tids in cog_codes.items():
    tids = list(tids or [])
    if code in ("generic_off_target",):
        continue
    if not tids:
        cog_rows.append({"code": code, "n_topics": 0, "status": "empty", "cliffs_delta": float("nan")})
        continue
    col = f"EES_tmp_cog_{code}"
    tmp = work_ees.copy()
    tmp[col] = ex._align_series_to_frame(ex.topic_set_share(shares, tids), tmp).values
    res = _test(tmp, col, "EES", label=code)
    coherent = code not in ("generic_off_target",) and len(tids) >= 1
    if coherent and code != "generic_off_target":
        n_coherent += len(tids)
    cog_rows.append(
        {
            "code": code,
            "n_topics": len(tids),
            "topic_ids": ",".join(str(t) for t in tids),
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
        }
    )
cognition_screen = pd.DataFrame(cog_rows)
cognition_screen["family_test_allowed"] = n_coherent >= 3
display(cognition_screen.round(4))
print(f"Coherent cognition topic count (excl. off-target): {n_coherent}")
if n_coherent < 3:
    print("HARD RULE: do not construct/test a cognition family (fewer than 3 coherent topics).")
ctx.save_table(cognition_screen, "cognition_screen")

# %% [markdown]
# ---
# # Part VI — Work / institutional life screen

# %%
work_codes = (ees_cfg.get("code_membership") or {}).get("work") or {}
work_rows = []
coherent_work = 0
for code, tids in work_codes.items():
    tids = list(tids or [])
    if not tids:
        work_rows.append({"code": code, "n_topics": 0, "cliffs_delta": float("nan"), "verdict": "empty"})
        continue
    col = f"EES_tmp_work_{code}"
    tmp = work_ees.copy()
    tmp[col] = ex._align_series_to_frame(ex.topic_set_share(shares, tids), tmp).values
    res = _test(tmp, col, "EES", label=code)
    if code != "generic_logistics":
        coherent_work += len(tids)
    work_rows.append(
        {
            "code": code,
            "n_topics": len(tids),
            "topic_ids": ",".join(str(t) for t in tids),
            "cliffs_delta": res.get("cliffs_delta"),
            "ci_low": res.get("ci_low"),
            "ci_high": res.get("ci_high"),
            "verdict": res.get("verdict"),
        }
    )
work_screen = pd.DataFrame(work_rows)
display(work_screen.sort_values("cliffs_delta").round(4))
ctx.save_table(work_screen, "work_screen")
if coherent_work >= 3:
    fig, ax = ees.forest_plot(
        work_screen.dropna(subset=["cliffs_delta"]).rename(columns={"code": "construct"}),
        title="Work / institutional screen (exploratory)",
    )
    ctx.save_figure(fig, "work_screen_forest")
    plt.show()
else:
    print("Fewer than 3 coherent work topics — category-level controlled tests skipped.")

# %% [markdown]
# ---
# # Part VII — Safeguards: author-half stability + integrated summary

# %%
stability_feats = [
    f"EES_{c}"
    for c in (
        emotion_families
        + body_families
        + social_families
        + ["felt_body", "looked_at_body", "felt_vs_looked_logratio", "social_domain_richness"]
    )
    if f"EES_{c}" in work_ees.columns
]
stability = ees.author_split_stability(
    work_ees,
    stability_feats,
    test_fn=_test,
    seed=int(ees_cfg.get("author_split_seed", 42)),
)
stability["construct"] = stability["construct"].str.replace("^EES_", "", regex=True)
display(stability.round(4))
ctx.save_table(stability, "author_split_stability")

# Strict → moderate → broad for key families
traj_key = {
    k: v
    for k, v in (ees_cfg.get("families") or {}).items()
    if k in (
        "emotion_distress_expressed",
        "emotion_physiological_arousal",
        "emotion_coregulation",
        "body_external_appearance",
        "body_interoceptive",
        "family_presence",
    )
}
breadth = ex.trajectory_effects(work_ees, traj_key, test_fn=_test, hyp="EES")
display(breadth.round(4))
ctx.save_table(breadth, "strict_moderate_broad_robustness")

# %% [markdown]
# ### Integrated presentation figure
#
# Candidate claim (only if broader frozen constructs confirm it):
# higher-rated romances move **inward** into felt emotional/physical experience and
# **outward** into family/social stakes, while giving less attention to generic
# visual attractiveness.

# %%
summary_constructs = [
    "emotion_distress_expressed",
    "emotion_physiological_arousal",
    "emotion_coregulation",
    "emotion_physical_comfort",
    "emotion_visible_affect",
    "body_interoceptive",
    "body_vulnerable",
    "body_markings",
    "body_external_appearance",
    "body_grooming",
    "family_presence",
    "supportive_social_embeddedness",
    "social_pressure_conflict",
    "felt_body",
    "looked_at_body",
]
parts = []
for src in (emotion_eff, embodiment_eff, family_social_eff):
    if len(src):
        parts.append(src[["construct", "cliffs_delta", "ci_low", "ci_high"]].copy())
integrated = pd.concat(parts, ignore_index=True)
integrated = integrated[integrated["construct"].isin(summary_constructs)].drop_duplicates("construct")
display(integrated.round(4))
ctx.save_table(integrated, "integrated_summary_effects")

fig, ax = ees.forest_plot(
    integrated,
    title="What higher-rated romance emphasizes (exploratory integrated view)",
)
ctx.save_figure(fig, "integrated_summary")
plt.show()

# %% [markdown]
# ## Outputs checklist
#
# Tables and figures under
# `results/.../notebook_analysis/15_emotion_embodiment_social_world_exploration/`.
#
# Next steps: run `pipeline/10_run_ees_coding.py` (live LLM), human-freeze
# `code_membership` / `families`, set `frozen: true`, then re-execute this notebook.

# %%
print("Done.")
print(f"Tables → {ctx.tables_dir.relative_to(root)}")
print(f"Figures → {ctx.figures_dir.relative_to(root)}")
print(f"Provisional freeze: {PROVISIONAL} | frozen={FROZEN}")
