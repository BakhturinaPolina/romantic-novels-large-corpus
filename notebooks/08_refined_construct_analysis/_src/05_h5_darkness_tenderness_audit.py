# %% [markdown]
# # 05 — H5 darkness vs tenderness audit (human review)
#
# Focused boundaries only: `7.3` (external?), `3.2` (relational?), tenderness via H1/H4
# reuse. Do **not** fully relabel `7.2` / `4.4` (already high on-label fidelity in Stage 10
# NB07) — those leaves stay as known-good anchors.
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

ctx = nh.setup("05_h5_darkness_tenderness_audit")
cfg = ctx.cfg
HYP = "H5"
CODE_COL = "darkness_code"

# %% [markdown]
# ## 1. Overview — H5-coded topics with labels

# %%
lookup = load_topic_lookup(cfg)
master = nh.load_master(cfg)
h5 = master[master[CODE_COL].notna()].copy()
h5["code_norm"] = h5[CODE_COL].map(normalize_code)
print(f"H5-coded topics: {len(h5)}")

overview = rd.annotation_overview(
    h5, CODE_COL, extra_cols=["main_couple_prob"]
)
display(
    overview[
        ["topic", "taxonomy", "code", "code_norm", "mixed", "main_couple_prob"]
    ]
)
ctx.save_table(overview, "h5_topic_overview_labeled")
display(h5[CODE_COL].value_counts().to_frame("n"))
display(h5["code_norm"].value_counts(dropna=False).to_frame("n_norm"))

skip = set(topics_for_leaves(lookup, ["7.2", "4.4"]))
print(f"Topics deliberately not fully relabelled (7.2∪4.4): {len(skip)}")
print("Skip pool (id — label), first 12:")
for line in rd.labeled_topic_list(lookup, sorted(skip)[:12]):
    print(f"  · {line}")
print(f"Of which appear in H5 audit anyway: {h5['topic_id'].isin(skip).sum()}")

# %% [markdown]
# ## 2. Lexical vs contextual agreement

# %%
lex = nh.load_audit_jsonl(cfg, HYP, "A")
ctxu = nh.load_audit_jsonl(cfg, HYP, "B")
adj = nh.load_audit_jsonl(cfg, HYP, "C")
lex_idx = rd.audit_index(lex)
ctx_idx = rd.audit_index(ctxu)
adj_idx = rd.audit_index(adj)

agree = rd.agreement_table(h5, lex_idx, ctx_idx, adj_idx, hyp=HYP)
if not agree.empty:
    print(
        f"Lexical–contextual agreement: {agree['agree'].mean():.1%} "
        f"({int(agree['agree'].sum())}/{len(agree)})"
    )
    ctx.save_table(agree, "h5_lexical_contextual_agreement")
    disagree = agree[~agree["agree"]]
    if len(disagree):
        display(
            disagree[
                ["topic", "taxonomy", "code_a", "code_b", "code_c", "rationale_c"]
            ]
        )

# %% [markdown]
# ## 3. Tenderness reuse from H1 / H4
#
# These are candidates for `tenderness_core` — verify a sample of labels, not just codes.

# %%
tender_h1 = master[master["intimacy_code"].map(normalize_code).isin(["I1", "I2", "I3"])]
tender_h4 = master[
    master["care_protection_code"].map(normalize_code).isin(["H4_1", "H4_12"])
]
print(f"H1 affection/reassurance candidates for tenderness_core: {len(tender_h1)}")
print(f"H4 reassurance/reciprocal candidates: {len(tender_h4)}")
t1 = rd.annotation_overview(tender_h1.assign(code_norm=tender_h1["intimacy_code"].map(normalize_code)), "intimacy_code")
display(t1[["topic", "taxonomy", "code", "code_norm"]].head(25))
ctx.save_table(
    tender_h1[
        ["topic_id", "current_topic_label", "intimacy_code", "current_taxonomy_id"]
    ],
    "h5_tenderness_from_h1",
)

# %% [markdown]
# ## 4. Focus leaves `7.3` and `3.2`
#
# What to check: is `7.3` danger outside the couple? Is `3.2` relational darkness rather
# than external plot threat? Main-couple probability on the overview is a hint; sentences
# decide.

# %%
focus = h5[h5["current_taxonomy_id"].isin(["7.3", "3.2"])]
focus_ov = rd.annotation_overview(focus, CODE_COL, extra_cols=["main_couple_prob"])
display(
    focus_ov[
        ["topic", "taxonomy", "code", "code_norm", "main_couple_prob"]
    ]
)
ctx.save_table(focus_ov, "h5_focus_leaves")

# %% [markdown]
# ## 5. Close reading

# %%
review_ids = rd.select_review_topics(
    h5,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    force_ids=focus["topic_id"].tolist(),
    per_code=3,
    seed=42,
    show_all_if_n_le=24,
)
packs = rd.show_review_set(
    cfg,
    h5,
    review_ids,
    hyp=HYP,
    lex_idx=lex_idx,
    ctx_idx=ctx_idx,
    adj_idx=adj_idx,
    code_col=CODE_COL,
)
ctx.save_markdown(
    rd.render_review_markdown(
        packs, title="H5 darkness / tenderness — close-reading pack"
    ),
    "close_reading_pack",
)
ctx.save_table(
    h5[
        [
            "topic_id",
            "current_topic_label",
            "current_taxonomy_id",
            "current_taxonomy_name",
            "darkness_code",
            "code_norm",
            "main_couple_prob",
        ]
    ],
    "darkness_topic_annotations",
)

fig, ax = plt.subplots(figsize=(7, 3.5))
vc = h5["code_norm"].fillna("UNMAPPED").value_counts()
ax.bar(vc.index.astype(str), vc.values)
ax.set_title("H5 normalised darkness codes")
plt.xticks(rotation=45, ha="right")
ctx.save_figure(fig, "h5_code_distribution")
plt.show()

print("H5 audit review complete.")
