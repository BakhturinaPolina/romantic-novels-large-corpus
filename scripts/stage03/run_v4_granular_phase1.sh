#!/usr/bin/env bash
# Run v4 granular Phase 1 BO for one embedding model (foreground, resumable).
#
# Usage (from repo root):
#   ./scripts/stage03/run_v4_granular_phase1.sh l12
#   ./scripts/stage03/run_v4_granular_phase1.sh l6
#   ./scripts/stage03/run_v4_granular_phase1.sh mpnet
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

die() {
  echo "ERROR: $*" >&2
  exit 1
}

model_config() {
  case "$1" in
    l12)
      MODEL_NAME="sentence-transformers/all-MiniLM-L12-v2"
      RUN_ID="v4_l12_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_l12_granular_phase1.yaml"
      ;;
    l6)
      MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
      RUN_ID="v4_l6_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_l6_granular_phase1.yaml"
      ;;
    mpnet)
      MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
      RUN_ID="v4_mpnet_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_mpnet_granular_phase1.yaml"
      ;;
    *)
      die "Unknown model '$1'. Use: l12 | l6 | mpnet"
      ;;
  esac
}

[[ $# -ge 1 ]] || die "Usage: $0 <l12|l6|mpnet>"
model_config "$1"

echo "v4 granular Phase 1 BO: $MODEL_NAME (run-id: $RUN_ID)"
echo "config:      $TRAIN_CONFIG"
echo "console log: logs/${RUN_ID}_console.log"
echo "pipeline log:logs/stage03_${RUN_ID}.log"
echo "ETA: ~2-2.5 days GPU (pilot10 median ~15 min/call after startup)"
echo ""
echo "Press Ctrl+C to stop; re-run to resume from checkpoint."

export PYTHONUNBUFFERED=1
mkdir -p logs

exec "$PY" -u -m src.stage03_train.cli tune \
  --config "$TRAIN_CONFIG" \
  --run-id "$RUN_ID" \
  --embedding-model "$MODEL_NAME" \
  2>&1 | tee -a "logs/${RUN_ID}_console.log"
