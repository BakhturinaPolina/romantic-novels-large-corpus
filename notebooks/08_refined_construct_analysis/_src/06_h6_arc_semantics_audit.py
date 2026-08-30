# %% [markdown]
# # 06 — H6 arc semantics audit (human review)
#
# Main-couple vs non-couple conflict, and topic × position weights \(W_{tkr}\).
# High `4.4` label fidelity ≠ “is it **main-couple** conflict?”
#
# Saved audits + packets only. Rating cells stay blinded; sentence tertiles are visible
# because H6 is position-aware.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

cwd = Path.cwd().resolve()
root = cwd
for _ in range(6):
    if (root / "configs").is_dir() and (root / "src").is_dir():
        break
    root = root.parent
sys.path.insert(0, str(root))

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh
from src.stage11_refined_construct_analysis.analysis import review_display as rd
from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code

ctx = nh.setup("06_h6_arc_semantics_audit")
cfg = ctx.cfg
HYP = "H6"
CODE_COL = "arc_role"

# %% [markdown]
# ## 1. Overview — arc roles with topic labels

# %%
master = nh.load_master(cfg)
h6 = master[master[CODE_COL].notna()].copy()
h6["code_norm"] = h6[CODE_COL].map(normalize_code)
print(f"H6-coded topics: {len(h6)}")

overview = rd.annotation_overview(
    h6,
    CODE_COL,
    extra_cols=["main_couple_prob", "non_couple_prob", "unclear_prob"],
)
display(
    overview[
        [
            "topic",
            "taxonomy",
            "code",
            "code_norm",
            "main_couple_prob",
            "non_couple_prob",
        ]
    ]
)
ctx.save_table(overview, "h6_topic_overview_labeled")
display(h6[CODE_COL].value_counts().head(25).to_frame("n"))
display(h6["code_norm"].value_counts(dropna=False).to_frame("n_norm"))

# %% [markdown]
# ## 2. Lexical vs contextual agreement

# %%
lex = nh.load_audit_jsonl(cfg, HYP, "A")
ctxu = nh.load_audit_jsonl(cfg, HYP, "B")
adj = nh.load_audit_jsonl(cfg, HYP, "C")
lex_idx = rd.audit_index(lex)
ctx_idx = rd.audit_index(ctxu)
adj_idx = rd.audit_index(adj)

agree = rd.agreement_table(h6, lex_idx, ctx_idx, adj_idx, hyp=HYP)
if not agree.empty:
    print(
        f"Lexical–contextual agreement: {agree['agree'].mean():.1%} "
        f"({int(agree['agree'].sum())}/{len(agree)})"
    )
    ctx.save_table(agree, "h6_lexical_contextual_agreement")
    disagree = agree[~agree["agree"]]
    if len(disagree):
        display(
            disagree[
                ["topic", "taxonomy", "code_a", "code_b", "code_c", "rationale_c"]
            ]
        )

# %% [markdown]
# ## 3. Main-couple probabilities
#
# Distribution first; then read low-probability topics that still carry conflict / secrecy
# arc roles — those are the ones most likely to be external plot, not couple arc.

# %%
print(h6[["main_couple_prob", "non_couple_prob", "unclear_prob"]].describe())
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.hist(h6["main_couple_prob"].dropna(), bins=20, color="steelblue", edgecolor="white")
ax.set_title("H6 main_couple_prob")
ctx.save_figure(fig, "h6_main_couple_hist")
plt.show()

low_mc = h6[h6["main_couple_prob"].fillna(0) < 0.4].copy()
print(f"Topics with main_couple_prob < 0.4: {len(low_mc)}")
if len(low_mc):
    display(
        rd.annotation_overview(low_mc, CODE_COL, extra_cols=["main_couple_prob"])[
            ["topic", "taxonomy", "code", "code_norm", "main_couple_prob"]
        ]
    )

# %% [markdown]
# ## 4. Topic × position weights \(W_{tkr}\)

# %%
wtkr = nh.load_w_tkr(cfg)
print(f"W_tkr rows: {len(wtkr)}")
if not wtkr.empty:
    wtkr = wtkr.copy()
    wtkr["code_norm"] = wtkr["construct_code"].map(normalize_code)
    display(
        wtkr.groupby(["tertile", "code_norm"], dropna=False)["weight"]
        .mean()
        .unstack(fill_value=0)
        .round(3)
    )
    ctx.save_table(wtkr, "w_tkr_raw")

# %% [markdown]
# ## 5. Close reading
#
# Force-include low main-couple topics. In the cards, watch tertile tags on sentences:
# rising end-conflict that is non-couple should not feed REFINED_RISING the same way
# main-couple conflict does.

# %%
review_ids = rd.select_review_topics(
    h6,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    force_ids=low_mc["topic_id"].tolist(),
    per_code=3,
    seed=42,
)
packs = rd.show_review_set(
    cfg,
    h6,
    review_ids,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    code_col=CODE_COL,
    max_sentences=10,
)
ctx.save_markdown(
    rd.render_review_markdown(packs, title="H6 arc semantics — close-reading pack"),
    "close_reading_pack",
)
ctx.save_table(
    h6[
        [
            "topic_id",
            "current_topic_label",
            "current_taxonomy_id",
            "current_taxonomy_name",
            "arc_role",
            "code_norm",
            "main_couple_prob",
            "non_couple_prob",
        ]
    ],
    "arc_topic_annotations",
)

# %% [markdown]
# Later: REFINED_FALLING / REFINED_RISING deltas and RARC; EXTERNAL_PLOT_CONFLICT kept
# outside the arc equation.

print("H6 audit review complete.")
