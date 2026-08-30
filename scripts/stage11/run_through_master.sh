#!/usr/bin/env bash
# Wait for H1–H4 live audits, then H5→H6, then master table.
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

echo "[$(date -Iseconds)] waiting for H1–H4 audit process / completion…" | tee -a "$LOG/chain.log"

# Wait until H2 adjudication has 10 rows (last in H1→H3→H4→H2 order)
while true; do
  n2=$($PY -c "from pathlib import Path; p=Path('$OUT/audits/h2/adjudication.jsonl'); print(sum(1 for l in p.open() if l.strip()) if p.exists() else 0)")
  n1=$($PY -c "from pathlib import Path; p=Path('$OUT/audits/h1/adjudication.jsonl'); print(sum(1 for l in p.open() if l.strip()) if p.exists() else 0)")
  n3=$($PY -c "from pathlib import Path; p=Path('$OUT/audits/h3/adjudication.jsonl'); print(sum(1 for l in p.open() if l.strip()) if p.exists() else 0)")
  n4=$($PY -c "from pathlib import Path; p=Path('$OUT/audits/h4/adjudication.jsonl'); print(sum(1 for l in p.open() if l.strip()) if p.exists() else 0)")
  echo "[$(date +%H:%M:%S)] adjud H1=$n1 H3=$n3 H4=$n4 H2=$n2" | tee -a "$LOG/chain.log"
  if [[ "$n1" -ge 90 && "$n3" -ge 70 && "$n4" -ge 30 && "$n2" -ge 10 ]]; then
    break
  fi
  # If audit process died early, exit wait with message
  if ! pgrep -f '05_run_hypothesis_audits.py' >/dev/null; then
    echo "WARN: 05_run_hypothesis_audits not running (H1=$n1 H3=$n3 H4=$n4 H2=$n2)" | tee -a "$LOG/chain.log"
    # continue waiting only if incomplete; if process dead and incomplete, try resume
    if [[ "$n2" -lt 10 ]]; then
      echo "Resuming H1–H4 audits…" | tee -a "$LOG/chain.log"
      $PY -u src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py \
        --config configs/stage11/refined_constructs.yaml \
        --hypotheses H1,H3,H4,H2 \
        >> "$LOG/audits_live.log" 2>&1 || true
    fi
  fi
  sleep 60
done

echo "[$(date -Iseconds)] H1–H4 complete; ensuring H5/H6 evidence packets…" | tee -a "$LOG/chain.log"
# Wait for h5h6 evidence rebuild if still running
while pgrep -f 'h5h6_rebuild_ids|02b_rebuild_evidence_incremental.py --topic-ids-file' >/dev/null 2>&1; do
  echo "waiting for H5/H6 packets…" | tee -a "$LOG/chain.log"
  sleep 30
done
# Rebuild any still-missing
$PY -u src/stage11_refined_construct_analysis/pipeline/02b_rebuild_evidence_incremental.py \
  --topic-ids-file "$OUT/candidates/h5h6_rebuild_ids.txt" \
  --skip-existing-with-sentences \
  >> "$LOG/evidence_h5h6.log" 2>&1

echo "[$(date -Iseconds)] H5 → H6 audits…" | tee -a "$LOG/chain.log"
$PY -u src/stage11_refined_construct_analysis/pipeline/06_run_h5_h6_audits.py \
  >> "$LOG/audits_h5h6.log" 2>&1

echo "[$(date -Iseconds)] master table + weights…" | tee -a "$LOG/chain.log"
$PY -u src/stage11_refined_construct_analysis/pipeline/07_build_master_table.py \
  >> "$LOG/master_table.log" 2>&1

echo "[$(date -Iseconds)] DONE through master table" | tee -a "$LOG/chain.log"
