# %% [markdown]
# # 07 — Refined construct dictionary
#
# Combine all audits into topic→construct and topic×position→construct weights.
# **Freeze the dictionary here before looking at refined rating results.**

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
from src.stage11_refined_construct_analysis.analysis.constructs import (
    CODE_TO_RAX,
    COMPOSITE_DEFS,
    LOG_RATIO_DEFS,
    normalize_code,
)

ctx = nh.setup("07_refined_construct_dictionary")
cfg = ctx.cfg

# %%
master = nh.load_master(cfg)
freeze = nh.load_freeze(cfg)
print(json.dumps(freeze, indent=2))
assert freeze.get("frozen") is True, "Dictionary must be frozen via 07_build_master_table.py"

dominance = float(cfg.section("weights", "strict_dominance"))
print(f"Strict dominance threshold: {dominance}")
print(f"Weight design: {freeze.get('weight_design', 'legacy')}")
cov = freeze.get("construct_coverage") or nh.load_construct_coverage(cfg)
if cov:
    ratios = pd.DataFrame(
        [
            {"ratio": k, **{kk: vv for kk, vv in v.items() if kk != "topic_ids"}}
            for k, v in (cov.get("ratios") or {}).items()
        ]
    )
    if not ratios.empty:
        display(ratios)
        ctx.save_table(ratios, "construct_ratio_gates")

# %% [markdown]
# ## Weight matrices

# %%
for mode in ("strict", "weighted", "inclusive"):
    w = nh.load_weights(cfg, mode)
    w = w.copy()
    w["code_norm"] = w["construct_code"].map(normalize_code)
    print(f"\nW_tk_{mode}: {len(w)} rows, {w['topic_id'].nunique()} topics")
    display(w.groupby("construct_family")["construct_code"].nunique().rename("n_codes").to_frame())
    ctx.save_table(w, f"topic_construct_weights_{mode}")

wtkr = nh.load_w_tkr(cfg)
if not wtkr.empty:
    ctx.save_table(wtkr, "topic_construct_weights_tkr")

# %% [markdown]
# ## Code → RAX map (frozen)

# %%
rax_map = (
    pd.DataFrame(
        [{"code": k, "rax": v} for k, vs in CODE_TO_RAX.items() for v in vs]
    )
    .sort_values(["rax", "code"])
    .reset_index(drop=True)
)
display(rax_map.head(40))
ctx.save_table(rax_map, "refined_construct_dictionary")

comp = pd.DataFrame(
    [{"composite": k, "parts": ", ".join(v)} for k, v in COMPOSITE_DEFS.items()]
)
ratios = pd.DataFrame(
    [{"name": k, "numerator": v[0], "denominator": v[1]} for k, v in LOG_RATIO_DEFS.items()]
)
display(comp)
display(ratios)
ctx.save_table(comp, "composite_defs")
ctx.save_table(ratios, "log_ratio_defs")

# %%
# Coverage after normalisation
cov = []
for col, family in [
    ("intimacy_code", "H1"),
    ("hea_code", "H2"),
    ("security_code", "H3"),
    ("care_protection_code", "H4"),
    ("darkness_code", "H5"),
    ("arc_role", "H6"),
]:
    raw = master[col].notna().sum()
    normed = master[col].map(normalize_code).notna().sum()
    cov.append({"hypothesis": family, "raw_coded": int(raw), "normalised_mapped": int(normed)})
cov_df = pd.DataFrame(cov)
display(cov_df)
ctx.save_table(cov_df, "code_normalisation_coverage")

print(
    "\nDictionary frozen. Do not peek at refined rating effects until notebooks 08–09.\n"
    "Stage 09 taxonomy remains descriptive; this table is the hypothesis measurement layer."
)
