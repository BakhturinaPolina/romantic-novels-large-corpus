#!/usr/bin/env bash
# Pareto Phase 2: Stage04 granular select → stability compare-fit on Pareto calls only.
#
# Usage:
#   ./scripts/stage03/run_v4_pareto_phase2.sh l12
#   ./scripts/stage03/run_v4_pareto_phase2.sh l6
#   ./scripts/stage03/run_v4_pareto_phase2.sh mpnet
#   ./scripts/stage03/run_v4_pareto_phase2.sh l12 --dry-run-only
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

PY="${ROOT}/.venv/bin/python"
PATHS_CONFIG="configs/stage03/paths_stage03_fit_v3.yaml"
DRY_RUN_ONLY=false
[[ -x "$PY" ]] || PY=python3

die() {
  echo "ERROR: $*" >&2
  exit 1
}

model_config() {
  case "$1" in
    l12)
      PHASE1_RUN="v4_l12_granular_phase1"
      PHASE2_RUN="v4_l12_granular_phase2_pareto"
      TRAIN_CONFIG="configs/stage03/train_v4_l12_granular_phase1.yaml"
      TRIALS_PATH="results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv"
      ;;
    l6)
      PHASE1_RUN="v4_l6_granular_phase1"
      PHASE2_RUN="v4_l6_granular_phase2_pareto"
      TRAIN_CONFIG="configs/stage03/train_v4_l6_granular_phase1.yaml"
      TRIALS_PATH="results/experiments/v4_l6_granular_phase1/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv"
      ;;
    mpnet)
      PHASE1_RUN="v4_mpnet_granular_phase1"
      PHASE2_RUN="v4_mpnet_granular_phase2_pareto"
      TRAIN_CONFIG="configs/stage03/train_v4_mpnet_granular_phase1.yaml"
      TRIALS_PATH="results/experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv"
      ;;
    *)
      die "Unknown model '$1'. Use: l12 | l6 | mpnet"
      ;;
  esac
  SELECTION_RUN_ID="${PHASE1_RUN}_dryrun"
  TOP_K_CSV="results/selection/${SELECTION_RUN_ID}/top_k.csv"
}

[[ $# -ge 1 ]] || die "Usage: $0 <l12|l6|mpnet> [--dry-run-only]"
MODEL="$1"
shift
for arg in "$@"; do
  case "$arg" in
    --dry-run-only) DRY_RUN_ONLY=true ;;
    *) die "Unknown option: $arg" ;;
  esac
done

model_config "$MODEL"

[[ -f "$TRIALS_PATH" ]] || die "Phase 1 trials not found: $TRIALS_PATH (run ./scripts/stage03/run_v4_granular_phase1.sh $MODEL first)"

echo "Stage04 granular dry-run: $SELECTION_RUN_ID"
"${ROOT}/scripts/stage04/run_v4_granular_phase1_dryrun.sh" "$MODEL"

if [[ "$DRY_RUN_ONLY" == true ]]; then
  echo "Dry-run only; skipping compare-fit."
  exit 0
fi

BO_CALLS=$("$PY" - <<'PY' "$TOP_K_CSV"
import sys
import pandas as pd

path = sys.argv[1]
df = pd.read_csv(path)
if df.empty or "bo_call" not in df.columns:
    sys.exit(1)
if "Pareto_Efficient_All" in df.columns:
    df = df[df["Pareto_Efficient_All"].fillna(False).astype(bool)]
if df.empty:
    sys.exit(1)
print(",".join(str(int(x)) for x in df["bo_call"].tolist()))
PY
) || die "No Pareto calls in $TOP_K_CSV"

echo "Stability compare-fit for $PHASE2_RUN (bo_calls=$BO_CALLS)"
echo "config: $TRAIN_CONFIG | paths: $PATHS_CONFIG"
echo "log: logs/stage05_compare_${PHASE2_RUN}.log"
mkdir -p logs

"$PY" -m src.stage05_final_fit.cli compare \
  --trials "$TRIALS_PATH" \
  --bo-calls "$BO_CALLS" \
  --run-id "$PHASE2_RUN" \
  --paths-config "$PATHS_CONFIG" \
  --config "$TRAIN_CONFIG" \
  --stability-runs 3 \
  --stability-tolerance 75 \
  --reduce-outliers \
  2>&1 | tee -a "logs/stage05_compare_${PHASE2_RUN}.log"
