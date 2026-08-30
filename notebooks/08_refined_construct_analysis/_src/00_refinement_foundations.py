# %% [markdown]
# # 00 — Refinement foundations
#
# Freeze the measurement problem **before** solving it. Stage 10 remains the confirmatory
# taxonomy baseline; Stage 11 is post-hoc measurement correction.
#
# This notebook documents source call49 mappings, lookup-derived candidate pools,
# Stage 10 δ freeze, known measurement failures, blinding, and integrity traps
# (H2 pool 10≠11; leaf `7.2` = 12≠13).

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
else:
    raise RuntimeError("project root not found")
sys.path.insert(0, str(root))

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh
from src.stage11_refined_construct_analysis.analysis import review_display as rd
from src.stage11_refined_construct_analysis.lookup import (
    load_topic_lookup,
    run_lookup_integrity,
    topics_for_leaves,
)

ctx = nh.setup("00_refinement_foundations")
cfg = ctx.cfg

# %% [markdown]
# ## 1. Frozen inputs and integrity

# %%
lookup = load_topic_lookup(cfg)
integrity = run_lookup_integrity(cfg, lookup)
integrity.raise_if_failed()
display(pd.DataFrame(integrity.checks))

frozen = nh.load_frozen_inputs(cfg)
print("frozen_inputs keys:", sorted(frozen.keys()) if frozen else "(missing — run 01_build_candidate_manifests.py)")
if frozen:
    ctx.save_markdown(json.dumps(frozen, indent=2), "frozen_inputs_snapshot")

# %% [markdown]
# ## 2. Stage 10 δ freeze (confirmatory baseline — do not overwrite)

# %%
delta_freeze = cfg.section("stage10_delta_freeze")
delta_tbl = pd.DataFrame(
    [{"hypothesis": k, "stage10_cliffs_delta": v} for k, v in delta_freeze.items()]
)
display(delta_tbl)
ctx.save_table(delta_tbl, "stage10_delta_freeze")

# %% [markdown]
# ## 3. Measurement-problem table

# %%
problems = pd.DataFrame(
    [
        {
            "construct_targeted": "explicit sex",
            "old_operationalisation": "2.3 — Explicit Sexual Acts",
            "known_problem": "only ~28% genuinely explicit; kissing/undressing dominate",
            "new_audit": "H1 intimacy",
        },
        {
            "construct_targeted": "HEA / final payoff",
            "old_operationalisation": "4.5 + thin 5.3a + 8.3a",
            "known_problem": "confession/repair ≠ final payoff; thin leaves (1 topic each)",
            "new_audit": "H2 HEA",
        },
        {
            "construct_targeted": "material/social display",
            "old_operationalisation": "1.6 + 8.2 + 5.3a + 8.3a",
            "known_problem": "appearance ≠ material security; 1.6 effect robust on-label",
            "new_audit": "H3 security",
        },
        {
            "construct_targeted": "protectiveness",
            "old_operationalisation": "all 4.6 − 4.7",
            "known_problem": "4.6 mixes reassurance/medical/institutional; 4.7 only 2 topics",
            "new_audit": "H4 protection",
        },
        {
            "construct_targeted": "darkness / tenderness",
            "old_operationalisation": "broad AX_dark_vs_tender",
            "known_problem": "pools relational conflict, violence, external danger, affect",
            "new_audit": "H5 darkness",
        },
        {
            "construct_targeted": "narrative arc",
            "old_operationalisation": "tertile rising − falling leaves",
            "known_problem": "conflict/secrecy may not be main-couple",
            "new_audit": "H6 arc",
        },
    ]
)
display(problems)
ctx.save_table(problems, "measurement_problem_table")

# %% [markdown]
# ## 4. Candidate pools (lookup-derived — never hard-coded counts)

# %%
rows = []
for hyp in ("H1", "H2", "H3", "H4", "H5", "H6"):
    cand = nh.load_candidates(cfg, hyp)
    n = int(cand.get("n_topics") or len(cand.get("topic_ids") or []))
    rows.append(
        {
            "hypothesis": hyp,
            "n_topics": n,
            "name": cand.get("name"),
        }
    )
pool_summary = pd.DataFrame(rows)
display(pool_summary)
ctx.save_table(pool_summary, "candidate_pool_summary")

# H2 explicit assert — print id — label, not bare ids
h2_ids = topics_for_leaves(lookup, ["4.5", "5.3a", "8.3a"])
expected = int(cfg.section("integrity", "h2_expected_n_topics"))
print(f"H2 pool from lookup: {len(h2_ids)} topics (expected {expected})")
assert len(h2_ids) == expected, f"H2 pool size {len(h2_ids)} != {expected}"
print("H2 pool (id — label):")
for line in rd.labeled_topic_list(lookup, h2_ids):
    print(f"  · {line}")

ids_72 = topics_for_leaves(lookup, ["7.2"])
n_72 = len(ids_72)
assert n_72 == int(cfg.section("integrity", "leaf_7_2_expected_n"))
print(f"Leaf 7.2: {n_72} topics (ok). Sample:")
for line in rd.labeled_topic_list(lookup, ids_72[:8]):
    print(f"  · {line}")
if n_72 > 8:
    print(f"  … and {n_72 - 8} more")

# %% [markdown]
# ## 5. Blinding and evidence completeness

# %%
cell_key = nh.load_cell_key(cfg)
print("Cell key sealed until notebook 10. Labels:", list(cell_key.get("labels", cell_key.keys()))[:8])

pkt_dir = cfg.output_path("evidence_packets_dir")
n_packets = len(list(pkt_dir.glob("topic_*.json"))) if pkt_dir.exists() else 0
print(f"Evidence packets on disk: {n_packets}")

audit_counts = []
for hyp in ("H1", "H2", "H3", "H4", "H5", "H6"):
    for pass_name in ("A", "B", "C"):
        df = nh.load_audit_jsonl(cfg, hyp, pass_name)
        audit_counts.append({"hypothesis": hyp, "pass": pass_name, "n": len(df)})
audit_cov = pd.DataFrame(audit_counts)
display(audit_cov.pivot(index="hypothesis", columns="pass", values="n"))
ctx.save_table(audit_cov, "audit_completeness")

print("\nFoundations frozen. Proceed to hypothesis audits 01–06 (no rating peek).")
