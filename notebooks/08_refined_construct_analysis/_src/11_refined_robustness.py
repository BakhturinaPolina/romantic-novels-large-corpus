# %% [markdown]
# # 11 — Refined robustness
#
# Attack the new findings: strict / weighted / inclusive coding, author concentration,
# and OLD TAXONOMY | REFINED STRICT | REFINED WEIGHTED effect panels.

# %%
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

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh

ctx = nh.setup("11_refined_robustness")
cfg = ctx.cfg
GATE = nh.effect_gate(cfg)
delta_freeze = cfg.section("stage10_delta_freeze")

# %%
features = [
    "RLR_emotional_vs_explicit",
    "RAX_h2_strict",
    "RLR_emotional_vs_material_security",
    "RLR_protection_vs_control",
    "RLR_darkness_vs_tenderness",
    "RARC",
]

panels = []
for mode in ("strict", "weighted", "inclusive"):
    frame = nh.load_refined_frame(cfg, mode)
    usable = frame[frame["analysable"].fillna(True)] if "analysable" in frame.columns else frame
    cols = [c for c in features if c in usable.columns]
    eff = nh.cliffs_delta_table(usable, cols, n_boot=300, seed=42)
    eff["mode"] = mode
    panels.append(eff)

    # Singleton-author subset
    if "author_id" in usable.columns:
        counts = usable.groupby("author_id").size()
        singletons = counts[counts == 1].index
        sub = usable[usable["author_id"].isin(singletons)]
        if len(sub) > 200:
            eff_s = nh.cliffs_delta_table(sub, cols, n_boot=200, seed=42)
            eff_s["mode"] = f"{mode}_singleton"
            panels.append(eff_s)

panel = pd.concat(panels, ignore_index=True)
display(panel.round(4))
ctx.save_table(panel, "robustness_panel")

# %% [markdown]
# ## OLD | REFINED STRICT | REFINED WEIGHTED

# %%
hyp_map = {
    "H1": ("RLR_emotional_vs_explicit", "H1"),
    "H2": ("RAX_h2_strict", "H2"),
    "H3": ("RLR_emotional_vs_material_security", "H3"),
    "H4": ("RLR_protection_vs_control", "H4"),
    "H5": ("RLR_darkness_vs_tenderness", "H5"),
    "H6": ("RARC", "H6"),
}
rows = []
for hyp, (feat, freeze_key) in hyp_map.items():
    old = delta_freeze.get(freeze_key)
    for mode in ("strict", "weighted"):
        sub = panel[(panel["mode"] == mode) & (panel["feature"] == feat)]
        rows.append(
            {
                "hypothesis": hyp,
                "spec": f"refined_{mode}",
                "cliffs_delta": float(sub.iloc[0]["cliffs_delta"]) if len(sub) else np.nan,
            }
        )
    rows.append({"hypothesis": hyp, "spec": "old_taxonomy", "cliffs_delta": old})
compare = pd.DataFrame(rows)
wide = compare.pivot(index="hypothesis", columns="spec", values="cliffs_delta")
display(wide)
ctx.save_table(wide.reset_index(), "old_vs_refined_panel")

# %%
fig, ax = plt.subplots(figsize=(9, 4.5))
hyps = list(hyp_map.keys())
x = np.arange(len(hyps))
width = 0.25
for i, spec in enumerate(["old_taxonomy", "refined_strict", "refined_weighted"]):
    vals = [wide.loc[h, spec] if h in wide.index and spec in wide.columns else np.nan for h in hyps]
    ax.bar(x + (i - 1) * width, vals, width, label=spec)
ax.axhline(0, color="gray", lw=1)
ax.axhline(GATE, color="red", ls="--", lw=0.8)
ax.axhline(-GATE, color="red", ls="--", lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels(hyps)
ax.set_ylabel("Cliff's δ")
ax.set_title("OLD TAXONOMY | REFINED STRICT | REFINED WEIGHTED")
ax.legend()
ctx.save_figure(fig, "old_vs_refined_bars")
plt.show()

# %% [markdown]
# ## Sign / magnitude / gate stability

# %%
stab = []
for feat in features:
    sub = panel[panel["feature"] == feat]
    if sub.empty:
        continue
    signs = np.sign(sub["cliffs_delta"].dropna())
    stab.append(
        {
            "feature": feat,
            "n_specs": len(sub),
            "sign_stable": bool(len(set(signs)) <= 1),
            "min_abs_delta": float(sub["cliffs_delta"].abs().min()),
            "max_abs_delta": float(sub["cliffs_delta"].abs().max()),
            "any_clears_gate": bool(
                (
                    (sub["cliffs_delta"].abs() >= GATE)
                    & ~((sub["ci_low"] <= 0) & (sub["ci_high"] >= 0))
                ).any()
            ),
        }
    )
stab_df = pd.DataFrame(stab)
display(stab_df)
ctx.save_table(stab_df, "stability_summary")

print(
    "Stage 11 complete as measurement-correction analysis. "
    "Stage 10 remains the confirmatory taxonomy baseline."
)
