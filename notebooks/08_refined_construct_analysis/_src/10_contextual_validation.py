# %% [markdown]
# # 10 — Contextual validation (unblind)
#
# After annotations and axes are frozen, **unblind** sampling cells and inspect whether
# the same construct means the same thing in high- vs low-rated books.

# %%
import json
import sys
from pathlib import Path

import pandas as pd

cwd = Path.cwd().resolve()
root = cwd
for _ in range(6):
    if (root / "configs").is_dir() and (root / "src").is_dir():
        break
    root = root.parent
sys.path.insert(0, str(root))

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh

ctx = nh.setup("10_contextual_validation")
cfg = ctx.cfg

# %% [markdown]
# ## Unblind cell key

# %%
cell_key = nh.load_cell_key(cfg)
print(json.dumps(cell_key, indent=2)[:2000])
ctx.save_markdown(json.dumps(cell_key, indent=2), "cell_key_unblinded")

meanings = cfg.section("evidence", "cell_meanings")
cell_tbl = pd.DataFrame(
    [{"cell": k, "meaning": v} for k, v in meanings.items()]
)
display(cell_tbl)
ctx.save_table(cell_tbl, "cell_meanings")

# %% [markdown]
# ## Construct × rating: code distributions from Pass B (now interpretable)

# %%
# For each hypothesis, summarise Pass B dominant codes — cells were blinded during coding.
rows = []
for hyp in ("H1", "H2", "H3", "H4", "H5", "H6"):
    b = nh.load_audit_jsonl(cfg, hyp, "B")
    if b.empty:
        continue
    for _, r in b.iterrows():
        resp = r.get("response") or {}
        if not isinstance(resp, dict):
            resp = {}
        rows.append(
            {
                "hypothesis": hyp,
                "topic_id": r.get("topic_id"),
                "dominant_code": resp.get("dominant_code") or r.get("code"),
                "mixed": resp.get("mixed_topic") or (str(r.get("code")) == "MIXED"),
                "meaning_differs_across_cells": resp.get("meaning_differs_across_cells"),
            }
        )
summary = pd.DataFrame(rows)
if not summary.empty:
    display(
        summary.groupby(["hypothesis", "meaning_differs_across_cells"], dropna=False)
        .size()
        .rename("n")
        .reset_index()
    )
    ctx.save_table(summary, "pass_b_cell_stability_flags")

# %% [markdown]
# ## High vs low construct × high vs low rating (book-level)

# %%
frame = nh.load_refined_frame(cfg, "strict")
usable = frame[frame["analysable"].fillna(True)] if "analysable" in frame.columns else frame
constructs = [
    c
    for c in (
        "RAX_nonexplicit_affection",
        "RAX_explicit_sex",
        "RAX_h2_strict",
        "RAX_emotional_security",
        "RAX_status_display",
        "RAX_external_protection",
        "RAX_relational_darkness",
        "RARC",
    )
    if c in usable.columns
]

cell_rows = []
for c in constructs:
    q_lo, q_hi = usable[c].quantile(0.25), usable[c].quantile(0.75)
    for tier in ("high_rate", "low_rate"):
        for level, mask in (
            ("high_construct", usable[c] >= q_hi),
            ("low_construct", usable[c] <= q_lo),
        ):
            sub = usable.loc[mask & (usable["rating_class"] == tier), c]
            cell_rows.append(
                {
                    "construct": c,
                    "cell": f"{level}×{tier}",
                    "n_books": int(len(sub)),
                    "mean_share": float(sub.mean()) if len(sub) else float("nan"),
                }
            )
cells = pd.DataFrame(cell_rows)
display(cells)
ctx.save_table(cells, "construct_x_rating_cells")

print(
    "Interpretive questions for close reading (use human_review packets):\n"
    "- Is material provision in low-rated books mostly status expenditure?\n"
    "- Does high-rated explicit content co-occur with more aftercare/negotiation?\n"
    "- Does 'protection' in low-rated books look more like control?"
)
