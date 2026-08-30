#!/usr/bin/env bash
# Re-run H3 then H4 with hardened v1.1 prompts (--no-resume), after the live
# Sonnet orchestrator finishes H5/H6 (avoids master/API races).
#
# Usage:
#   bash scripts/stage11/rerun_h3_h4_hardened.sh
#   WAIT=0 bash scripts/stage11/rerun_h3_h4_hardened.sh   # start immediately
#   MODEL=anthropic/claude-sonnet-4.6 bash scripts/stage11/rerun_h3_h4_hardened.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

MODEL="${MODEL:-anthropic/claude-sonnet-4.6}"
WAIT="${WAIT:-1}"
PY="${PY:-.venv/bin/python}"
LOG_DIR="$ROOT/logs"
PROGRESS="$LOG_DIR/h3_h4_hardened_rerun_progress.txt"
mkdir -p "$LOG_DIR"

note() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$msg" | tee -a "$PROGRESS"
}

post_hyp_update() {
  local hyp="$1"
  local nb=""
  case "$hyp" in
    H3) nb="03_h3_security_material_audit" ;;
    H4) nb="04_h4_protection_possession_audit" ;;
  esac
  note "POST-UPDATE $hyp: master + frame + human_review + notebook $nb"
  $PY src/stage11_refined_construct_analysis/pipeline/07_build_master_table.py
  $PY src/stage11_refined_construct_analysis/pipeline/08_build_refined_analysis_frame.py
  $PY scripts/stage11/export_human_review_pdf.py
  if [[ -n "$nb" ]]; then
    $PY scripts/stage11/percent_to_notebook.py \
      "notebooks/08_refined_construct_analysis/_src/${nb}.py" \
      "notebooks/08_refined_construct_analysis/_src/00_refinement_foundations.py" \
      || true
    .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
      --ExecutePreprocessor.timeout=600 \
      --ExecutePreprocessor.kernel_name=python3 \
      "notebooks/08_refined_construct_analysis/${nb}.ipynb" \
      "notebooks/08_refined_construct_analysis/00_refinement_foundations.ipynb" \
      || note "WARN notebook execute failed for $hyp (continuing)"
  fi
  note "GIT commit + push for $hyp"
  git add \
    configs/stage11 \
    scripts/stage11 \
    src/stage11_refined_construct_analysis \
    notebooks/08_refined_construct_analysis \
    results/stage11_refined_construct_analysis \
    ':(exclude)results/stage11_refined_construct_analysis/**/logs/**' \
    || true
  if git diff --cached --quiet; then
    note "Nothing to commit for $hyp"
  else
    git commit -m "$(cat <<EOF
Re-audit Stage 11 ${hyp} with hardened v1.1 Sonnet prompts.

Force codebook IDs via explicit JSON schemas; refresh master, review pack, and notebook.
EOF
)" || note "WARN commit failed"
    git push origin HEAD || note "WARN push failed"
  fi
  note "POST-UPDATE $hyp complete"
}

run_audit() {
  local hyp="$1"
  local log="$LOG_DIR/${hyp,,}_sonnet_hardened_rerun.log"
  note "START AUDIT $hyp model=$MODEL --no-resume log=$log"
  $PY src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py \
    --hypotheses "$hyp" \
    --no-resume \
    --model "$MODEL" \
    2>&1 | tee "$log"
  note "DONE AUDIT $hyp"
}

note "H3/H4 hardened re-run start MODEL=$MODEL WAIT=$WAIT"

if [[ "$WAIT" == "1" ]]; then
  note "Waiting for orchestrate_sonnet_rerun / H5-H6 workers to finish..."
  while pgrep -f 'orchestrate_sonnet_rerun\.sh' >/dev/null 2>&1 \
     || pgrep -f '06_run_h5_h6_audits\.py' >/dev/null 2>&1 \
     || pgrep -f '05_run_hypothesis_audits\.py' >/dev/null 2>&1; do
    sleep 30
  done
  note "Prior Sonnet workers idle — starting H3"
fi

# Sanity: prompts must be v1.1
$PY - <<'PY'
from src.stage11_refined_construct_analysis.config import Stage11Config, load_stage11_config
from src.stage11_refined_construct_analysis.audits.prompts import load_hypothesis_prompt
cfg = load_stage11_config()
for hyp in ("H3", "H4"):
    p = load_hypothesis_prompt(cfg, hyp)
    ver = str(p.get("version"))
    assert ver.startswith("1.1"), f"{hyp} prompt version={ver}, expected 1.1"
    print(f"OK {hyp} prompt v{ver} codes={len(p.get('codes', []))}")
PY

run_audit H3
post_hyp_update H3
run_audit H4
post_hyp_update H4

note "H3/H4 hardened re-run ALL DONE"
