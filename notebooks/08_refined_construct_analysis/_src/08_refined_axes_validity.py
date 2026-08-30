# %% [markdown]
# # 08 — Refined axes validity
#
# Build atomic constructs and test coverage / coherence **before** seeing outcomes.
# Prefer components when composites disagree (same rule as Stage 10 NB05).

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

cwd = Path.cwd().resolve()
root = cwd
for _ in range(6):
    if (root / "configs").is_dir() and (root / "src").is_dir():
        break
    root = root.parent
sys.path.insert(0, str(root))

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh

ctx = nh.setup("08_refined_axes_validity")
cfg = ctx.cfg

# %%
frame = nh.load_refined_frame(cfg, mode="strict")
manifest = pd.read_parquet(cfg.output_path("book_features_dir") / "refined_frame_manifest.parquet")
display(manifest.sort_values("nonzero_books", ascending=False).head(40))
ctx.save_table(manifest, "construct_coverage")

# %% [markdown]
# ## Atomic construct distributions (no outcome conditioning)

# %%
atoms = [
    c
    for c in frame.columns
    if c.startswith("RAX_")
    and not c.startswith("RAX_h")
    and "begin" not in c
    and "end" not in c
]
usable = frame[frame.get("analysable", True) == True] if "analysable" in frame.columns else frame
summary = pd.DataFrame(
    {
        "construct": atoms,
        "pct_nonzero": [(usable[c] > 0).mean() * 100 for c in atoms],
        "mean": [usable[c].mean() for c in atoms],
        "median": [usable[c].median() for c in atoms],
        "p90": [usable[c].quantile(0.9) for c in atoms],
    }
).sort_values("mean", ascending=False)
display(summary.round(4))
ctx.save_table(summary, "atomic_construct_summary")

# %% [markdown]
# ## Inter-construct correlations

# %%
top = summary.head(12)["construct"].tolist()
corr = usable[top].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
ax.set_title("Refined construct correlations (top coverage)")
ctx.save_figure(fig, "construct_correlations")
plt.show()
ctx.save_table(corr.reset_index(), "construct_correlations")

# %% [markdown]
# ## Strict vs weighted agreement

# %%
strict = nh.load_refined_frame(cfg, "strict")
weighted = nh.load_refined_frame(cfg, "weighted")
common = [c for c in atoms if c in weighted.columns]
agree = []
for c in common:
    r = np.corrcoef(strict[c].fillna(0), weighted[c].fillna(0))[0, 1]
    agree.append({"construct": c, "corr_strict_weighted": float(r)})
agree_df = pd.DataFrame(agree).sort_values("corr_strict_weighted")
display(agree_df)
ctx.save_table(agree_df, "strict_vs_weighted_agreement")

# %% [markdown]
# ## Author concentration (top construct)

# %%
if "author_id" in usable.columns and top:
    c0 = top[0]
    by_auth = usable.groupby("author_id")[c0].mean().sort_values(ascending=False)
    print(f"Top construct {c0}: top author mean={by_auth.iloc[0]:.4f}, median author={by_auth.median():.4f}")
    print(f"Share of books from singleton authors: {(usable.groupby('author_id').size() == 1).mean():.1%}")

print("Validity checks complete — proceed to hypothesis tests in notebook 09.")
