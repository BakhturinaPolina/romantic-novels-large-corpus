# %% [markdown]
# # 03 — H3 security / material audit (human review)
#
# Functional classification: emotional security vs material/economic security vs status
# display. Classify interaction **function**, not the object mentioned (a gown can be
# status display, gift-as-care, or neither).
#
# Saved Pass A/B/C + evidence packets only; rating cells stay blinded.
# Special focus: leaf `1.6` (appearance) — Stage 10 found it on-label but the H3 question
# is whether appearance content is doing *security* work.

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

ctx = nh.setup("03_h3_security_material_audit")
cfg = ctx.cfg
HYP = "H3"
CODE_COL = "security_code"

# %% [markdown]
# ## 1. Overview — every H3 topic with labels

# %%
master = nh.load_master(cfg)
h3 = master[master[CODE_COL].notna()].copy()
h3["code_norm"] = h3[CODE_COL].map(normalize_code)
print(f"H3-coded topics: {len(h3)}")

overview = rd.annotation_overview(h3, CODE_COL, extra_cols=["secondary_id"])
display(overview[["topic", "taxonomy", "code", "code_norm", "mixed", "agree"]].head(60))
ctx.save_table(overview, "h3_topic_overview_labeled")
display(h3[CODE_COL].value_counts().head(20).to_frame("n"))
display(h3["code_norm"].value_counts(dropna=False).to_frame("n_norm"))

# %% [markdown]
# ## 2. Lexical vs contextual agreement

# %%
lex = nh.load_audit_jsonl(cfg, HYP, "A")
ctxu = nh.load_audit_jsonl(cfg, HYP, "B")
adj = nh.load_audit_jsonl(cfg, HYP, "C")
lex_idx = rd.audit_index(lex)
ctx_idx = rd.audit_index(ctxu)
adj_idx = rd.audit_index(adj)

agree = rd.agreement_table(h3, lex_idx, ctx_idx, adj_idx, hyp=HYP)
if not agree.empty:
    print(
        f"Lexical–contextual agreement: {agree['agree'].mean():.1%} "
        f"({int(agree['agree'].sum())}/{len(agree)})"
    )
    ctx.save_table(agree, "h3_lexical_contextual_agreement")
    disagree = agree[~agree["agree"]]
    print(f"Disagreements: {len(disagree)}")
    display(
        disagree[
            ["topic", "taxonomy", "code_a", "code_b", "code_c", "rationale_a", "rationale_b"]
        ].head(30)
    )

# %% [markdown]
# ## 3. Appearance leaf (`1.6`) functional decomposition
#
# What to check in the cards: is the prose describing bodies/clothes as craft ornament,
# as wealth/status signalling, or as care/security? The object in the sentence is not the
# construct.

# %%
app = h3[h3["current_taxonomy_id"] == "1.6"].copy()
print(f"Appearance topics in H3 audit: {len(app)}")
app_overview = rd.annotation_overview(app, CODE_COL, extra_cols=["secondary_id"])
display(app_overview[["topic", "taxonomy", "code", "code_norm", "mixed", "secondary_id"]])
ctx.save_table(app_overview, "h3_appearance_decomposition")

cross = (
    h3.assign(
        taxonomy=h3.apply(
            lambda r: rd.fmt_leaf(r["current_taxonomy_id"], r["current_taxonomy_name"]),
            axis=1,
        )
    )
    .groupby(["taxonomy", "current_taxonomy_id", "code_norm"], dropna=False)
    .size()
    .rename("n")
    .reset_index()
    .sort_values("n", ascending=False)
)
display(cross.head(40))
ctx.save_table(cross, "h3_taxonomy_vs_code")

# %% [markdown]
# ## 4. Close reading
#
# Priority: appearance topics, disagreements, mixed, then stratified sample by code.

# %%
review_ids = rd.select_review_topics(
    h3,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    force_ids=app["topic_id"].tolist(),
    per_code=3,
    seed=42,
)
packs = rd.show_review_set(
    cfg,
    h3,
    review_ids,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    code_col=CODE_COL,
)
ctx.save_markdown(
    rd.render_review_markdown(packs, title="H3 security / material — close-reading pack"),
    "close_reading_pack",
)
ctx.save_table(
    h3[
        [
            "topic_id",
            "current_topic_label",
            "current_taxonomy_id",
            "current_taxonomy_name",
            "security_code",
            "code_norm",
            "mixed_topic",
        ]
    ],
    "security_topic_annotations",
)

fig, ax = plt.subplots(figsize=(8, 4))
vc = h3["code_norm"].fillna("UNMAPPED").value_counts()
ax.bar(vc.index.astype(str), vc.values)
ax.set_title("H3 normalised security codes")
plt.xticks(rotation=45, ha="right")
ctx.save_figure(fig, "h3_code_distribution")
plt.show()

print("H3 audit review complete.")
