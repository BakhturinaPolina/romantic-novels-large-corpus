#!/usr/bin/env bash
# Resume Stage08 prompt sweep: Phase A (skip complete) -> score -> Phase B -> score -> Phase C.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
SWEEP_DIR="${ROOT}/results/stage08_llm_labeling/prompt_sweeps/call73"
LOG="${ROOT}/logs/stage08_sweep_resume_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -a "$LOG") 2>&1

echo "=== Phase A resume ==="
bash scripts/run_stage08_prompt_sweep_call73.sh phase_a_resume

echo "=== Score Phase A + 0b ==="
"$ROOT/.venv/bin/python" scripts/score_stage08_prompt_sweep.py --sweep-dir "$SWEEP_DIR" --panel pilot20

WINNER="$("$ROOT/.venv/bin/python" - <<'PY'
import json
from pathlib import Path
p = Path("results/stage08_llm_labeling/prompt_sweeps/call73/scores/sweep_scores_summary.json")
rows = json.loads(p.read_text())
# Exclude temp ablations from structural winner; prefer prompt variants
candidates = [r for r in rows if "sweep_S" in r["file"] or "sweep_D2b" in r["file"]]
if not candidates:
    candidates = rows
best = max(candidates, key=lambda r: r["score"])
print(best["file"].split("sweep_")[1].split("_limit")[0] if "sweep_" in best["file"] else "v2")
PY
)"
echo "Phase A best suffix: $WINNER (using v2 structural baseline for Phase B conceptual variants)"

echo "=== Phase B ==="
bash scripts/run_stage08_prompt_sweep_call73.sh phase_b

echo "=== Score Phase B ==="
"$ROOT/.venv/bin/python" scripts/score_stage08_prompt_sweep.py --sweep-dir "$SWEEP_DIR" --panel pilot20

FINAL_PROMPT="$("$ROOT/.venv/bin/python" - <<'PY'
import json
from pathlib import Path
p = Path("results/stage08_llm_labeling/prompt_sweeps/call73/scores/sweep_scores_summary.json")
rows = json.loads(p.read_text())
candidates = [r for r in rows if "sweep_C" in r["file"]]
if not candidates:
    candidates = [r for r in rows if "sweep_S" in r["file"]]
best = max(candidates, key=lambda r: r["score"])
name = best["file"]
if "v2_c" in name:
    import re
    m = re.search(r"(v2_c\d+_[a-z_]+)", name)
    print(m.group(1) if m else "v2")
elif "v2_s" in name:
    import re
    m = re.search(r"(v2_s\d+_[a-z_]+)", name)
    print(m.group(1) if m else "v2")
else:
    print("v2")
PY
)"
echo "Phase C prompt: $FINAL_PROMPT"

echo "=== Phase C (30-topic panel) ==="
bash scripts/run_stage08_prompt_sweep_call73.sh phase_c "$FINAL_PROMPT"

echo "=== Final score (full30) ==="
"$ROOT/.venv/bin/python" scripts/score_stage08_prompt_sweep.py --sweep-dir "$SWEEP_DIR" --panel full30

echo "=== Done. Log: $LOG ==="
