# %% [markdown]
# # 10 — Contextual validation (unblind)
#
# After annotations and axes are frozen, **unblind** sampling cells and test whether
# the same topic performs the same function in high- vs low-rated books.
#
# Method: join Pass B `sentence_codes` to evidence-packet `sid→cell`, aggregate
# per-cell code proportions, then compare high-prevalence/high-tier vs
# high-prevalence/low-tier. No re-prompting; Pass B never saw ratings.

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

meanings = cell_key.get("meanings") or cfg.section("evidence", "cell_meanings")
cell_tbl = pd.DataFrame([{"cell": k, "meaning": v} for k, v in meanings.items()])
display(cell_tbl)
ctx.save_table(cell_tbl, "cell_meanings")

# %% [markdown]
# ## Cell-level code stability from stored sentence codes

# %%
stability = nh.cell_code_stability(cfg)
display(stability.head(20))
ctx.save_table(stability, "pass_b_cell_stability_flags")

if not stability.empty:
    by_hyp = (
        stability.groupby("hypothesis")
        .agg(
            n_topics=("topic_id", "nunique"),
            n_with_both_high_prev=(
                "meaning_differs_high_prevalence",
                lambda s: int(s.notna().sum()),
            ),
            n_differs=(
                "meaning_differs_high_prevalence",
                lambda s: int((s == True).sum()),  # noqa: E712
            ),
            pct_differs=(
                "meaning_differs_high_prevalence",
                # Comparable-only rate: n_differs / n_with_both_high_prev
                # (NaN non-comparable cells must not count as False).
                lambda s: (
                    float((s == True).sum() / s.notna().sum())  # noqa: E712
                    if s.notna().any()
                    else float("nan")
                ),
            ),
        )
        .reset_index()
    )
    display(by_hyp.round(4))
    ctx.save_table(by_hyp, "cell_stability_by_hypothesis")

    drifted = stability[stability["meaning_differs_high_prevalence"] == True]  # noqa: E712
    if not drifted.empty:
        show = drifted[
            [
                "hypothesis",
                "topic_id",
                "high_prev_high_tier_code",
                "high_prev_low_tier_code",
                "pass_b_dominant",
            ]
        ]
        display(show)
        ctx.save_table(show, "topics_with_high_prev_code_drift")
    print(
        f"Topics with comparable high-prevalence cells: "
        f"{int(stability['meaning_differs_high_prevalence'].notna().sum())}; "
        f"dominant-code drift: "
        f"{int((stability['meaning_differs_high_prevalence'] == True).sum())}"  # noqa: E712
    )
else:
    print("No sentence_codes × cell joins available.")

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
        "RAX_appearance_grooming",
        "RAX_status_display",
        "RAX_external_protection",
        "RAX_external_danger_crisis",
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
    "- When a topic is strongly present, does its function match in high- vs low-rated books?\n"
    "- Is appearance/grooming distinct from status display in both rating tiers?\n"
    "- Does 'protection' in low-rated books look more like control?"
)
