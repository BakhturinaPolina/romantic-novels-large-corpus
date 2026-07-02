#!/usr/bin/env bash
# Stage04 eval-select dry-run on v4 granular Phase 1 BO trials (granular config).
#
# Usage:
#   ./scripts/stage04/run_v4_granular_phase1_dryrun.sh l12
#   ./scripts/stage04/run_v4_granular_phase1_dryrun.sh l6
#   ./scripts/stage04/run_v4_granular_phase1_dryrun.sh mpnet
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
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
      PHASE1_RUN="v4_l12_granular_phase1"
      TRIALS_PATH="results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv"
      ;;
    l6)
      PHASE1_RUN="v4_l6_granular_phase1"
      TRIALS_PATH="results/experiments/v4_l6_granular_phase1/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv"
      ;;
    mpnet)
      PHASE1_RUN="v4_mpnet_granular_phase1"
      TRIALS_PATH="results/experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv"
      ;;
    *)
      die "Unknown model '$1'. Use: l12 | l6 | mpnet"
      ;;
  esac
  SELECTION_RUN_ID="${PHASE1_RUN}_dryrun"
}

[[ $# -ge 1 ]] || die "Usage: $0 <l12|l6|mpnet>"
model_config "$1"

[[ -f "$TRIALS_PATH" ]] || die "Phase 1 trials not found: $TRIALS_PATH (run ./scripts/stage03/run_v4_granular_phase1.sh $1 first)"

"$PY" -m src.stage04_eval_select.cli select \
  --trials "$TRIALS_PATH" \
  --config configs/stage04/eval_select_granular.yaml \
  --run-id "$SELECTION_RUN_ID"
