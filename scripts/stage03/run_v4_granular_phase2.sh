#!/usr/bin/env bash
# Phase 2: band-filter Phase 1 trials, then stability compare-fit reruns.
#
# Usage:
#   ./scripts/stage03/run_v4_granular_phase2.sh l12
#   ./scripts/stage03/run_v4_granular_phase2.sh l6
#   ./scripts/stage03/run_v4_granular_phase2.sh mpnet
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

PY="${ROOT}/.venv/bin/python"
PATHS_CONFIG="configs/stage03/paths_stage03_fit_v3.yaml"
[[ -x "$PY" ]] || PY=python3

die() {
  echo "ERROR: $*" >&2
  exit 1
}

model_config() {
  case "$1" in
    l12)
      PHASE1_RUN="v4_l12_granular_phase1"
      PHASE2_RUN="v4_l12_granular_phase2_stability"
      TRAIN_CONFIG="configs/stage03/train_v4_l12_granular_phase1.yaml"
      TRIALS_GLOB="results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv"
      ;;
    l6)
      PHASE1_RUN="v4_l6_granular_phase1"
      PHASE2_RUN="v4_l6_granular_phase2_stability"
      TRAIN_CONFIG="configs/stage03/train_v4_l6_granular_phase1.yaml"
      TRIALS_GLOB="results/experiments/v4_l6_granular_phase1/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv"
      ;;
    mpnet)
      PHASE1_RUN="v4_mpnet_granular_phase1"
      PHASE2_RUN="v4_mpnet_granular_phase2_stability"
      TRAIN_CONFIG="configs/stage03/train_v4_mpnet_granular_phase1.yaml"
      TRIALS_GLOB="results/experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv"
      ;;
    *)
      die "Unknown model '$1'. Use: l12 | l6 | mpnet"
      ;;
  esac
}

[[ $# -ge 1 ]] || die "Usage: $0 <l12|l6|mpnet>"
model_config "$1"

TRIALS_PATH=$(ls -1 $TRIALS_GLOB 2>/dev/null | head -1)
[[ -n "$TRIALS_PATH" && -f "$TRIALS_PATH" ]] || die "Phase 1 trials not found: $TRIALS_GLOB"

CANDIDATES_CSV="results/selection/${PHASE1_RUN}/phase2_candidates.csv"
"$PY" scripts/stage03/granular_select_phase2_candidates.py \
  --trials "$TRIALS_PATH" \
  --run-id "$PHASE1_RUN" \
  --output "$CANDIDATES_CSV"

BO_CALLS=$("$PY" - <<'PY' "$CANDIDATES_CSV"
import sys
import pandas as pd
df = pd.read_csv(sys.argv[1])
if df.empty or "bo_call" not in df.columns:
    sys.exit(1)
print(",".join(str(int(x)) for x in df["bo_call"].tolist()))
PY
) || die "No Phase 2 candidates selected from $CANDIDATES_CSV"

echo "Stability compare-fit for $PHASE2_RUN (bo_calls=$BO_CALLS)"
echo "config: $TRAIN_CONFIG | paths: $PATHS_CONFIG"
echo "log: logs/stage05_compare_${PHASE2_RUN}.log"
"$PY" -m src.stage05_final_fit.cli compare \
  --trials "$TRIALS_PATH" \
  --bo-calls "$BO_CALLS" \
  --run-id "$PHASE2_RUN" \
  --paths-config "$PATHS_CONFIG" \
  --config "$TRAIN_CONFIG" \
  --stability-runs 3 \
  --stability-tolerance 75 \
  --reduce-outliers
