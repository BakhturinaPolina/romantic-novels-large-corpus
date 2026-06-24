#!/usr/bin/env bash
# v4 L12 granular pilot: 10 BO calls with full console + file logging.
#
# Monitor (separate terminal):
#   tail -f logs/v4_l12_granular_pilot10_console.log | grep --line-buffered -E 'Stage03|BO call|TRAIN|ERROR|WARNING|coherence|n_topics|outlier|ETA'
#   tail -f logs/stage03_v4_l12_granular_pilot10.log
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || { echo "Missing .venv; create venv first." >&2; exit 1; }

RUN_ID="v4_l12_granular_pilot10"
CONFIG="configs/train_v4_l12_granular_pilot10.yaml"
CONSOLE_LOG="logs/${RUN_ID}_console.log"
PIPELINE_LOG="logs/stage03_${RUN_ID}.log"

mkdir -p logs results/experiments

echo "=== v4 L12 granular pilot (10 BO calls) ==="
echo "run_id:      ${RUN_ID}"
echo "config:      ${CONFIG}"
echo "console log: ${CONSOLE_LOG}"
echo "pipeline log:${PIPELINE_LOG}"
echo "trials:      results/experiments/${RUN_ID}/opt_*/trials_partial.csv"
echo ""
echo "ETA (from v3 L12 timing): ~12-16 min/call → ~2.0-2.7 h for 10 calls"
echo "                          + ~10-20 min startup (data scan, 500k subsample)"
echo "                          → plan ~2.5-3.0 h wall clock total"
echo ""
echo "Press Ctrl+C to stop; re-run this script to resume from checkpoint."
echo ""

export PYTHONUNBUFFERED=1

exec "$PY" -u -m src.stage03_train.cli tune \
  --config "$CONFIG" \
  --run-id "$RUN_ID" \
  --embedding-model "sentence-transformers/all-MiniLM-L12-v2" \
  2>&1 | tee -a "$CONSOLE_LOG"
