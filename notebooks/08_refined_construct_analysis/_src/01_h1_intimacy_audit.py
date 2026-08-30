# %% [markdown]
# # 01 — H1 intimacy audit (human review)
#
# What kind of intimacy does each candidate topic actually contain? This notebook reads
# **saved** Pass A/B/C outputs and evidence packets only (no OpenRouter). Rating cells stay
# blinded (`CELL_*`).
#
# Everything so far in Stage 11 that touched H1 was a code attached to a topic id. Here the
# check is the same one Stage 10 NB07 made for taxonomy leaves: **does the prose read the
# way the code says it should?**
#
# Evidence is not cherry-picked. Packets were built once (keywords + high-confidence
# sentences); Pass A scores lexical cues, Pass B scores sentences, Pass C adjudicates.
# Close-reading below always includes disagreements / mixed / manual-review topics, then a
# stratified sample so large pools stay readable.

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

ctx = nh.setup("01_h1_intimacy_audit")
cfg = ctx.cfg
HYP = "H1"
CODE_COL = "intimacy_code"

# %% [markdown]
# ## 1. Which topics were audited, and how are they coded?
#
# Overview shows **topic id — label** and **taxonomy id — name** for every H1-coded topic.
# The question to keep in mind while reading: is this kissing / affection / explicit sex /
# something else — or a mix the old `2.3` leaf would have collapsed?

# %%
master = nh.load_master(cfg)
h1 = master[master[CODE_COL].notna()].copy()
h1["code_norm"] = h1[CODE_COL].map(normalize_code)
print(f"H1-coded topics: {len(h1)}")

overview = rd.annotation_overview(h1, CODE_COL)
display(overview[["topic", "taxonomy", "code", "code_norm", "mixed", "agree"]])
ctx.save_table(overview, "h1_topic_overview_labeled")

print("\nCode mass (raw → normalised):")
display(h1[CODE_COL].value_counts().rename("n").to_frame())
display(h1["code_norm"].value_counts(dropna=False).rename("n_norm").to_frame())

# %% [markdown]
# ## 2. Lexical vs contextual agreement
#
# Pass A never sees sentences; Pass B never sees the public label. Disagreement is the
# interesting case — it usually means keywords and prose pull in different directions.

# %%
lex = nh.load_audit_jsonl(cfg, HYP, "A")
ctxu = nh.load_audit_jsonl(cfg, HYP, "B")
adj = nh.load_audit_jsonl(cfg, HYP, "C")
lex_idx = rd.audit_index(lex)
ctx_idx = rd.audit_index(ctxu)
adj_idx = rd.audit_index(adj)

agree = rd.agreement_table(h1, lex_idx, ctx_idx, adj_idx, hyp=HYP)
if not agree.empty:
    rate = agree["agree"].mean()
    print(
        f"Lexical–contextual agreement: {rate:.1%} "
        f"({int(agree['agree'].sum())}/{len(agree)})"
    )
    ctx.save_table(agree, "h1_lexical_contextual_agreement")
    disagree = agree[~agree["agree"]].copy()
    print(f"Disagreements to read first: {len(disagree)}")
    display(
        disagree[
            ["topic", "taxonomy", "code_a", "code_b", "code_c", "rationale_a", "rationale_b"]
        ].head(40)
    )
else:
    print("No Pass A/B rows loaded.")

# %% [markdown]
# ## 3. Old taxonomy leaf vs new intimacy code
#
# Where does the Stage 09 leaf assignment land after functional re-coding? A leaf that
# splinters across many intimacy codes is a measurement failure worth quoting from below.

# %%
cross = (
    h1.assign(
        taxonomy=h1.apply(
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
ctx.save_table(cross, "h1_taxonomy_vs_code")

fig, ax = plt.subplots(figsize=(8, 4))
vc = h1["code_norm"].fillna("NULL").value_counts()
ax.bar(vc.index.astype(str), vc.values)
ax.set_title("H1 normalised intimacy codes")
ax.set_ylabel("topics")
plt.xticks(rotation=45, ha="right")
ctx.save_figure(fig, "h1_code_distribution")
plt.show()

# %% [markdown]
# ## 4. Close reading
#
# For each selected topic: keywords, Stage-08 snippets, novel sentences (blinded cell /
# anon book), and Pass A/B/C rationales. What would falsify the assigned code? Prose that
# is mostly dialogue tags, setting, or non-intimate action under an intimacy label —
# or explicit genital content still coded as light affection.

# %%
review_ids = rd.select_review_topics(
    h1,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    per_code=3,
    seed=42,
)
packs = rd.show_review_set(
    cfg,
    h1,
    review_ids,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    code_col=CODE_COL,
)
ctx.save_markdown(
    rd.render_review_markdown(packs, title="H1 intimacy — close-reading pack"),
    "close_reading_pack",
)
ctx.save_table(
    h1[
        [
            "topic_id",
            "current_topic_label",
            "current_taxonomy_id",
            "current_taxonomy_name",
            "intimacy_code",
            "code_norm",
            "mixed_topic",
            "lexical_context_agreement",
        ]
    ],
    "intimacy_topic_annotations",
)

# %% [markdown]
# ### What to take from the cards
#
# - Prefer Pass C when A and B disagree, but only if the sentences support it.
# - `MIXED` / `SPLIT` topics should not enter a single strict intimacy weight without a
#   secondary construct — check whether the prose really is two scenes glued together.
# - No rating effects are examined here; that wait until notebooks 09–11.

print("H1 audit review complete. Tables + close_reading_pack.md written.")
