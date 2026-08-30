# %% [markdown]
# # 04 — H4 protection vs possession audit (human review)
#
# Decomposes `4.6` care and exhaustively inspects both `4.7` topics.
# **Protection requires an external threat**; partner-as-danger → control, not protection.
#
# Saved audits + packets only; rating cells stay blinded.

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
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup, topics_for_leaves

ctx = nh.setup("04_h4_protection_possession_audit")
cfg = ctx.cfg
HYP = "H4"
CODE_COL = "care_protection_code"

# %% [markdown]
# ## 1. Overview — labels with codes

# %%
lookup = load_topic_lookup(cfg)
master = nh.load_master(cfg)
h4 = master[master[CODE_COL].notna()].copy()
h4["code_norm"] = h4[CODE_COL].map(normalize_code)
print(f"H4-coded topics: {len(h4)}")

overview = rd.annotation_overview(h4, CODE_COL)
display(overview[["topic", "taxonomy", "code", "code_norm", "mixed", "agree"]])
ctx.save_table(overview, "h4_topic_overview_labeled")
display(h4[CODE_COL].value_counts().to_frame("n"))
display(h4["code_norm"].value_counts(dropna=False).to_frame("n_norm"))

# %% [markdown]
# ## 2. Lexical vs contextual agreement

# %%
lex = nh.load_audit_jsonl(cfg, HYP, "A")
ctxu = nh.load_audit_jsonl(cfg, HYP, "B")
adj = nh.load_audit_jsonl(cfg, HYP, "C")
lex_idx = rd.audit_index(lex)
ctx_idx = rd.audit_index(ctxu)
adj_idx = rd.audit_index(adj)

agree = rd.agreement_table(h4, lex_idx, ctx_idx, adj_idx, hyp=HYP)
if not agree.empty:
    print(
        f"Lexical–contextual agreement: {agree['agree'].mean():.1%} "
        f"({int(agree['agree'].sum())}/{len(agree)})"
    )
    ctx.save_table(agree, "h4_lexical_contextual_agreement")
    disagree = agree[~agree["agree"]]
    if len(disagree):
        display(
            disagree[
                ["topic", "taxonomy", "code_a", "code_b", "code_c", "rationale_c"]
            ]
        )

# %% [markdown]
# ## 3. Exhaustive `4.7` review (only two topics)
#
# Read both cards in full. What would falsify "protection"? Sentences where the threat is
# the partner, or where the act is claiming / restricting rather than shielding from outside.

# %%
ids_47 = topics_for_leaves(lookup, ["4.7"])
j47 = master[master["topic_id"].isin(ids_47)].copy()
j47["code_norm"] = j47[CODE_COL].map(normalize_code)
j47_ov = rd.annotation_overview(j47, CODE_COL, extra_cols=["secondary_id"])
display(j47_ov[["topic", "taxonomy", "code", "code_norm", "secondary_id"]])
print("4.7 topics (id — label):")
for line in rd.labeled_topic_list(lookup, ids_47):
    print(f"  · {line}")
ctx.save_table(j47_ov, "h4_47_exhaustive")

# %% [markdown]
# ## 4. Current `4.6` code mass
#
# Reassurance / medical / institutional care should not all count as protectiveness.

# %%
care = h4[h4["current_taxonomy_id"] == "4.6"]
print(f"Current 4.6 topics in H4 audit: {len(care)}")
by = (
    care.assign(
        topic=care.apply(
            lambda r: rd.fmt_topic(r["topic_id"], r["current_topic_label"]), axis=1
        )
    )
    .groupby("code_norm", dropna=False)
    .size()
    .rename("n")
    .reset_index()
    .sort_values("n", ascending=False)
)
display(by)
ctx.save_table(by, "h4_46_code_mass")

# %% [markdown]
# ## 5. Close reading
#
# Force-include both `4.7` topics; otherwise disagreements / mixed / stratified sample.

# %%
review_ids = rd.select_review_topics(
    h4,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    force_ids=ids_47,
    per_code=3,
    seed=42,
)
packs = rd.show_review_set(
    cfg,
    h4,
    review_ids,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    code_col=CODE_COL,
    max_sentences=12,
)
ctx.save_markdown(
    rd.render_review_markdown(
        packs, title="H4 protection / possession — close-reading pack"
    ),
    "close_reading_pack",
)
ctx.save_table(
    h4[
        [
            "topic_id",
            "current_topic_label",
            "current_taxonomy_id",
            "current_taxonomy_name",
            "care_protection_code",
            "code_norm",
            "mixed_topic",
        ]
    ],
    "care_protection_topic_annotations",
)

fig, ax = plt.subplots(figsize=(8, 4))
vc = h4["code_norm"].fillna("UNMAPPED").value_counts()
ax.bar(vc.index.astype(str), vc.values)
ax.set_title("H4 normalised protection/possession codes")
plt.xticks(rotation=45, ha="right")
ctx.save_figure(fig, "h4_code_distribution")
plt.show()

# %% [markdown]
# Primary refined contrast later: external_protection / (possessive_claiming +
# coercive_control). If either side stays extremely sparse → H4 underpowered.

print("H4 audit review complete.")
