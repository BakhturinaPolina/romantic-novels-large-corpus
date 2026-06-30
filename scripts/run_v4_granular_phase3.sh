#!/usr/bin/env bash
# Phase 3: narrowed BO with in-run stability (model_runs=3).
#
# Usage:
#   ./scripts/run_v4_granular_phase3.sh l12
#   ./scripts/run_v4_granular_phase3.sh l6
#   ./scripts/run_v4_granular_phase3.sh mpnet
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

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
      PHASE3_RUN="v4_l12_granular_phase3"
      TRAIN_CONFIG="configs/train_v4_l12_granular_phase3.yaml"
      ;;
    l6)
      MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
      PHASE3_RUN="v4_l6_granular_phase3"
      TRAIN_CONFIG="configs/train_v4_l6_granular_phase3.yaml"
      ;;
    mpnet)
      MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
      PHASE3_RUN="v4_mpnet_granular_phase3"
      TRAIN_CONFIG="configs/train_v4_mpnet_granular_phase3.yaml"
      ;;
    *)
      die "Unknown model '$1'. Use: l12 | l6 | mpnet"
      ;;
  esac
}

[[ $# -ge 1 ]] || die "Usage: $0 <l12|l6|mpnet>"
model_config "$1"

echo "v4 granular Phase 3 BO: $MODEL_NAME (run-id: $PHASE3_RUN)"
echo "config:       $TRAIN_CONFIG"
echo "console log:  logs/${PHASE3_RUN}_console.log"
echo "pipeline log: logs/stage03_${PHASE3_RUN}.log"
echo "ETA: ~4-6 days GPU (100 calls × 3 model_runs; ~45-60 min/call after startup)"
echo ""
echo "Press Ctrl+C to stop; re-run to resume from checkpoint."

export PYTHONUNBUFFERED=1
mkdir -p logs

exec "$PY" -u -m src.stage03_train.cli tune \
  --config "$TRAIN_CONFIG" \
  --run-id "$PHASE3_RUN" \
  --embedding-model "$MODEL_NAME" \
  2>&1 | tee -a "logs/${PHASE3_RUN}_console.log"
