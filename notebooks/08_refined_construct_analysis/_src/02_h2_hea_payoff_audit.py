# %% [markdown]
# # 02 — H2 HEA / final relational payoff audit (human review)
#
# Distinguishes lasting relational resolution from confession, apology, and ordinary repair.
# Thin leaves `5.3a` and `8.3a` (one topic each) get exhaustive evidence packets — read them
# in full below.
#
# This notebook reads **saved** Pass A/B/C outputs only (no OpenRouter). Rating cells stay
# blinded; narrative tertile on sentences is visible because H2 is position-aware.
#
# The pool is small (lookup integrity expects **10** topics from `4.5` ∪ `5.3a` ∪ `8.3a`),
# so every topic is close-read — nothing is sampled away.

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

ctx = nh.setup("02_h2_hea_payoff_audit")
cfg = ctx.cfg
HYP = "H2"
CODE_COL = "hea_code"

# %% [markdown]
# ## 1. The H2 pool — labels, not bare ids
#
# Integrity trap: older docs said 11 topics; lookup must yield **10**.

# %%
lookup = load_topic_lookup(cfg)
h2_ids = topics_for_leaves(lookup, ["4.5", "5.3a", "8.3a"])
assert len(h2_ids) == int(cfg.section("integrity", "h2_expected_n_topics"))

master = nh.load_master(cfg)
h2 = master[master["topic_id"].isin(h2_ids)].copy()
h2["code_norm"] = h2[CODE_COL].map(normalize_code)

overview = rd.annotation_overview(h2, CODE_COL)
display(overview[["topic", "taxonomy", "code", "code_norm", "mixed", "agree"]])
ctx.save_table(overview, "hea_topic_overview_labeled")
ctx.save_table(h2, "hea_topic_annotations")

print("H2 pool (id — label):")
for line in rd.labeled_topic_list(lookup, h2_ids):
    print(f"  · {line}")

# %% [markdown]
# ## 2. Lexical vs contextual agreement + Pass C rationales

# %%
lex = nh.load_audit_jsonl(cfg, HYP, "A")
ctxu = nh.load_audit_jsonl(cfg, HYP, "B")
adj = nh.load_audit_jsonl(cfg, HYP, "C")
lex_idx = rd.audit_index(lex)
ctx_idx = rd.audit_index(ctxu)
adj_idx = rd.audit_index(adj)

agree = rd.agreement_table(h2, lex_idx, ctx_idx, adj_idx, hyp=HYP)
if not agree.empty:
    print(
        f"Lexical–contextual agreement: {agree['agree'].mean():.1%} "
        f"({int(agree['agree'].sum())}/{len(agree)})"
    )
    display(
        agree[
            [
                "topic",
                "taxonomy",
                "code_a",
                "code_b",
                "code_c",
                "agree",
                "action",
                "rationale_c",
            ]
        ]
    )
    ctx.save_table(agree, "h2_lexical_contextual_agreement")

# %% [markdown]
# ## 3. Thin-leaf exhaustive check (`5.3a`, `8.3a`)
#
# One topic each. If either is mostly generic confession / apology rather than final
# relational payoff, the old composite HEA index was mis-measuring those leaves.

# %%
thin = h2[h2["current_taxonomy_id"].isin(["5.3a", "8.3a"])]
print("Thin HEA components — full cards follow in §4:")
display(
    thin.assign(
        topic=thin.apply(
            lambda r: rd.fmt_topic(r["topic_id"], r["current_topic_label"]), axis=1
        ),
        taxonomy=thin.apply(
            lambda r: rd.fmt_leaf(r["current_taxonomy_id"], r["current_taxonomy_name"]),
            axis=1,
        ),
    )[["topic", "taxonomy", "hea_code", "code_norm", "mixed_topic"]]
)
ctx.save_table(thin, "h2_thin_leaves")

# %% [markdown]
# ## 4. Close reading — every H2 topic
#
# What to look for: end-tertile sentences that settle the couple's status (commitment,
# public union, lasting resolution) versus mid-book repair / "I'm sorry" / soft confession
# that the old leaf labels would still have counted as HEA.

# %%
review_ids = rd.select_review_topics(
    h2,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    force_ids=thin["topic_id"].tolist(),
    show_all_if_n_le=12,
)
packs = rd.show_review_set(
    cfg,
    h2,
    review_ids,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    code_col=CODE_COL,
    max_sentences=12,
)
ctx.save_markdown(
    rd.render_review_markdown(packs, title="H2 HEA / payoff — close-reading pack"),
    "close_reading_pack",
)

fig, ax = plt.subplots(figsize=(7, 3.5))
vc = h2["code_norm"].fillna(h2[CODE_COL]).fillna("NULL").astype(str).value_counts()
ax.barh(vc.index[::-1], vc.values[::-1])
ax.set_title("H2 codes (normalised where possible)")
ctx.save_figure(fig, "h2_code_distribution")
plt.show()

# %% [markdown]
# ### Atomic RAX carried forward
#
# Later notebooks treat as separate atoms: repair, mutual_commitment, final_relational_payoff,
# public_union, commitment_symbols, generic_confession_apology. A topic that reads as
# apology-heavy should land on the last of those — not on final payoff.

print("H2 audit review complete. All pool topics close-read.")
