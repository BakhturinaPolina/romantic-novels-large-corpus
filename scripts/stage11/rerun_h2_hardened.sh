#!/usr/bin/env bash
# Wait for the H3–H6 hardened re-run to finish, then re-run H2 with v1.1 prompts.
#
# Usage:
#   bash scripts/stage11/rerun_h2_hardened.sh
#   WAIT=0 bash scripts/stage11/rerun_h2_hardened.sh   # start immediately

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

MODEL="${MODEL:-anthropic/claude-sonnet-4.6}"
WAIT="${WAIT:-1}"
PY="${PY:-.venv/bin/python}"
LOG_DIR="$ROOT/logs"
PROGRESS="$LOG_DIR/h2_hardened_rerun_progress.txt"
mkdir -p "$LOG_DIR"

note() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$msg" | tee -a "$PROGRESS"
}

note "H2 hardened re-run start MODEL=$MODEL WAIT=$WAIT"

if [[ "$WAIT" == "1" ]]; then
  note "Waiting for H3–H6 hardened workers to finish..."
  while pgrep -f 'rerun_h3_h6_hardened\.sh' >/dev/null 2>&1 \
     || pgrep -f '06_run_h5_h6_audits\.py' >/dev/null 2>&1 \
     || pgrep -f '05_run_hypothesis_audits\.py' >/dev/null 2>&1; do
    sleep 30
  done
  note "Prior workers idle — starting H2"
fi

$PY - <<'PY'
from src.stage11_refined_construct_analysis.config import load_stage11_config
from src.stage11_refined_construct_analysis.audits.prompts import load_hypothesis_prompt
from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code, rax_for_code
cfg = load_stage11_config()
p = load_hypothesis_prompt(cfg, "H2")
assert str(p.get("version")).startswith("1.1"), p.get("version")
assert normalize_code("HEA") == "H2_4"
assert rax_for_code("H2_4") == ["RAX_final_relational_payoff"]
assert rax_for_code("H2_2") == ["RAX_repair"]
print(f"OK H2 prompt v{p['version']} codes={len(p.get('codes', []))}")
PY

note "START AUDIT H2 model=$MODEL --no-resume"
$PY src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py \
  --hypotheses H2 \
  --no-resume \
  --model "$MODEL" \
  2>&1 | tee "$LOG_DIR/h2_sonnet_hardened_rerun.log"
note "DONE AUDIT H2"

note "POST-UPDATE H2: master + frame + human_review + notebook"
$PY src/stage11_refined_construct_analysis/pipeline/07_build_master_table.py
$PY src/stage11_refined_construct_analysis/pipeline/08_build_refined_analysis_frame.py
$PY scripts/stage11/export_human_review_pdf.py
$PY scripts/stage11/percent_to_notebook.py \
  notebooks/08_refined_construct_analysis/_src/02_h2_hea_payoff_audit.py \
  notebooks/08_refined_construct_analysis/_src/00_refinement_foundations.py \
  || true
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  notebooks/08_refined_construct_analysis/02_h2_hea_payoff_audit.ipynb \
  notebooks/08_refined_construct_analysis/00_refinement_foundations.ipynb \
  || note "WARN notebook execute failed for H2 (continuing)"

note "GIT commit + push for H2"
git add \
  configs/stage11 \
  scripts/stage11 \
  src/stage11_refined_construct_analysis \
  tests/stage11 \
  notebooks/08_refined_construct_analysis \
  results/stage11_refined_construct_analysis \
  ':(exclude)results/stage11_refined_construct_analysis/**/logs/**' \
  || true
if git diff --cached --quiet; then
  note "Nothing to commit for H2"
else
  git commit -m "$(cat <<EOF
Re-audit Stage 11 H2 with hardened v1.1 prompts and aligned RAX map.

Force H2_0–H2_8 codebook IDs; fix H2↔RAX off-by-one; refresh master and review pack.
EOF
)" || note "WARN commit failed"
  git push origin HEAD || note "WARN push failed"
fi

note "H2 hardened re-run ALL DONE"
