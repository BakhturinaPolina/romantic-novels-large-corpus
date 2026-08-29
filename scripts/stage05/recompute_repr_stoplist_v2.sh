#!/usr/bin/env bash
# Recompute topic representations for the Phase 2 shortlist with the cleaned
# stoplist (data/processed/custom_stoplist.txt). Original exports untouched;
# new tables land in final_compare/call_N/repr_stoplist_v2/.
#
# Usage:
#   ./scripts/stage05/recompute_repr_stoplist_v2.sh          # all 4 candidates
#   ./scripts/stage05/recompute_repr_stoplist_v2.sh l6_16    # single candidate
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
PY="${ROOT}/.venv/bin/python"
PATHS_CONFIG="configs/stage03/paths_stage03_fit_v3.yaml"

# candidate: run_id | train_config | trials_csv | bo_call | umap_seed (median export seed from stability.json)
declare -A CAND
CAND[l6_16]="v4_l6_granular_phase2_pareto|configs/stage03/train_v4_l6_granular_phase1.yaml|results/experiments/v4_l6_granular_phase1/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv|16|42"
CAND[mpnet_131]="v4_mpnet_granular_phase2_pareto|configs/stage03/train_v4_mpnet_granular_phase1.yaml|results/experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv|131|44"
CAND[mpnet_133]="v4_mpnet_granular_phase2_pareto|configs/stage03/train_v4_mpnet_granular_phase1.yaml|results/experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv|133|43"
CAND[l12_73]="v4_l12_granular_phase2_pareto|configs/stage03/train_v4_l12_granular_phase1.yaml|results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv|73|42"
CAND[l12_49]="v4_l12_granular_phase2_pareto|configs/stage03/train_v4_l12_granular_phase1.yaml|results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv|49|42"
CAND[l12_11]="v4_l12_granular_phase2_pareto|configs/stage03/train_v4_l12_granular_phase1.yaml|results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv|11|42"
CAND[mpnet_38]="v4_mpnet_granular_phase2_pareto|configs/stage03/train_v4_mpnet_granular_phase1.yaml|results/experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv|38|43"
ORDER=(l6_16 l12_73 mpnet_131 mpnet_133 l12_49 l12_11 mpnet_38)

TARGETS=("${ORDER[@]}")
if [[ $# -ge 1 ]]; then
  TARGETS=("$@")
fi

for key in "${TARGETS[@]}"; do
  [[ -n "${CAND[$key]:-}" ]] || { echo "Unknown candidate '$key' (use: ${ORDER[*]})" >&2; exit 1; }
  IFS='|' read -r RUN_ID TRAIN_CONFIG TRIALS CALL SEED <<< "${CAND[$key]}"
  echo ""
  echo "=== [$key] run=$RUN_ID call=$CALL umap_seed=$SEED ($(date +%H:%M:%S)) ==="
  "$PY" -m src.stage05_final_fit.scripts.recompute_topic_representations \
    --trials "$TRIALS" \
    --bo-call "$CALL" \
    --run-id "$RUN_ID" \
    --paths-config "$PATHS_CONFIG" \
    --config "$TRAIN_CONFIG" \
    --umap-seed "$SEED"
done

echo ""
echo "All done. Outputs: results/experiments/<run>/final_compare/call_N/repr_stoplist_v2/"
