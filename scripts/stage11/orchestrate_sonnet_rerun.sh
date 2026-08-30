#!/usr/bin/env bash
# Orchestrate Stage 11 Sonnet re-runs: H1 (resume) → H2 → H3 → H4 → H5 → H6.
# After each hypothesis: rebuild master + frame, export human_review, re-run
# relevant notebooks, commit + push.
#
# Usage:
#   bash scripts/stage11/orchestrate_sonnet_rerun.sh
#   START_FROM=H2 bash scripts/stage11/orchestrate_sonnet_rerun.sh
#   MODEL=anthropic/claude-sonnet-4.6 bash scripts/stage11/orchestrate_sonnet_rerun.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

MODEL="${MODEL:-anthropic/claude-sonnet-4.6}"
START_FROM="${START_FROM:-H1}"
PY="${PY:-.venv/bin/python}"
LOG_DIR="$ROOT/logs"
PROGRESS="$LOG_DIR/sonnet_orchestrator_progress.txt"
mkdir -p "$LOG_DIR"

note() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$msg" | tee -a "$PROGRESS"
}

hyp_notebook() {
  case "$1" in
    H1) echo "01_h1_intimacy_audit" ;;
    H2) echo "02_h2_hea_payoff_audit" ;;
    H3) echo "03_h3_security_material_audit" ;;
    H4) echo "04_h4_protection_possession_audit" ;;
    H5) echo "05_h5_darkness_tenderness_audit" ;;
    H6) echo "06_h6_arc_semantics_audit" ;;
    *) echo "" ;;
  esac
}

run_audit() {
  local hyp="$1"
  local resume_flag="$2"   # --no-resume or empty
  local log="$LOG_DIR/${hyp,,}_sonnet_rerun.log"
  note "START AUDIT $hyp model=$MODEL resume_flag='${resume_flag:-resume}' log=$log"
  # shellcheck disable=SC2086
  $PY src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py \
    --hypotheses "$hyp" \
    $resume_flag \
    --model "$MODEL" \
    2>&1 | tee "$log"
  note "DONE AUDIT $hyp"
}

# H5/H6 use a separate pipeline entrypoint
run_audit_h5h6() {
  local hyp="$1"
  local resume_flag="$2"
  local log="$LOG_DIR/${hyp,,}_sonnet_rerun.log"
  note "START AUDIT $hyp (06_run_h5_h6) model=$MODEL log=$log"
  # Prefer dedicated runner if it accepts --model; else use 05 with hyp filter
  if $PY src/stage11_refined_construct_analysis/pipeline/06_run_h5_h6_audits.py --help 2>&1 | grep -q -- '--model'; then
    # shellcheck disable=SC2086
    $PY src/stage11_refined_construct_analysis/pipeline/06_run_h5_h6_audits.py \
      --hypotheses "$hyp" \
      $resume_flag \
      --model "$MODEL" \
      2>&1 | tee "$log"
  else
    # shellcheck disable=SC2086
    $PY src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py \
      --hypotheses "$hyp" \
      $resume_flag \
      --model "$MODEL" \
      2>&1 | tee "$log"
  fi
  note "DONE AUDIT $hyp"
}

post_hyp_update() {
  local hyp="$1"
  local nb
  nb="$(hyp_notebook "$hyp")"
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

  # After H6 also refresh dictionary / validity / tests notebooks
  if [[ "$hyp" == "H6" ]]; then
    for extra in 07_refined_construct_dictionary 08_refined_axes_validity \
                 09_refined_hypothesis_tests 10_contextual_validation 11_refined_robustness; do
      .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=600 \
        --ExecutePreprocessor.kernel_name=python3 \
        "notebooks/08_refined_construct_analysis/${extra}.ipynb" \
        || note "WARN notebook $extra failed"
    done
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
Update Stage 11 ${hyp} Sonnet re-audit and human-review pack.

Refresh master weights, review PDF/markdown, and notebook outputs after ${hyp} Pass A/B/C on ${MODEL}.
EOF
)" || note "WARN commit failed"
    git push origin HEAD || note "WARN push failed"
  fi
  note "POST-UPDATE $hyp complete"
}

should_run() {
  local hyp="$1"
  local order=(H1 H2 H3 H4 H5 H6)
  local started=0
  for h in "${order[@]}"; do
    if [[ "$h" == "$START_FROM" ]]; then started=1; fi
    if [[ $started -eq 1 && "$h" == "$hyp" ]]; then return 0; fi
  done
  return 1
}

# --- main ---
note "Orchestrator start MODEL=$MODEL START_FROM=$START_FROM"

# H1: resume if partial Sonnet run exists; else fresh --no-resume
if should_run H1; then
  n_done=$(wc -l < results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/audits/h1/adjudication.jsonl 2>/dev/null || echo 0)
  n_done=${n_done// /}
  if [[ "${n_done:-0}" -gt 0 && "${n_done:-0}" -lt 98 ]]; then
    note "H1 partial ($n_done/98) → resume"
    run_audit H1 ""
  elif [[ "${n_done:-0}" -ge 98 ]]; then
    note "H1 already complete ($n_done) → skip audit"
  else
    note "H1 empty → fresh --no-resume"
    run_audit H1 "--no-resume"
  fi
  post_hyp_update H1
fi

if should_run H2; then
  run_audit H2 "--no-resume"
  post_hyp_update H2
fi

if should_run H3; then
  run_audit H3 "--no-resume"
  post_hyp_update H3
fi

if should_run H4; then
  run_audit H4 "--no-resume"
  post_hyp_update H4
fi

if should_run H5; then
  run_audit_h5h6 H5 "--no-resume"
  post_hyp_update H5
fi

if should_run H6; then
  run_audit_h5h6 H6 "--no-resume"
  post_hyp_update H6
fi

note "Orchestrator ALL DONE"
