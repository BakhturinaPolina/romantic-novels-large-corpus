#!/usr/bin/env bash
# Rebuild contextual evidence packets, then restart live Nemo audits + QA.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
OUT="$ROOT/results/stage11_refined_construct_analysis/v4_l12_granular_final_call49"
LOG="$OUT/logs"
mkdir -p "$LOG"

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

echo "[$(date -Iseconds)] incremental evidence rebuild…" | tee -a "$LOG/recovery.log"
"$PY" -u src/stage11_refined_construct_analysis/pipeline/02b_rebuild_evidence_incremental.py \
  --skip-existing-with-sentences \
  2>&1 | tee -a "$LOG/evidence_rebuild.log"

echo "[$(date -Iseconds)] evidence rebuild done; starting audits…" | tee -a "$LOG/recovery.log"
echo "" >> "$LOG/audits_live.log"
echo "==== $(date -Iseconds) RESTARTED after contextual packet rebuild ====" >> "$LOG/audits_live.log"

"$PY" -u src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py \
  --config configs/stage11/refined_constructs.yaml \
  --hypotheses H1,H3,H4,H2 \
  --no-resume \
  2>&1 | tee -a "$LOG/audits_live.log"

echo "[$(date -Iseconds)] audits finished" | tee -a "$LOG/recovery.log"
