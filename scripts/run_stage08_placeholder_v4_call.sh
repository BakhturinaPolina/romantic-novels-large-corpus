#!/usr/bin/env bash
# Stage 08 LLM labeling for a v4 placeholder compare-fit model (default call 73).
#
# Labels ALL topics via OpenRouter; Stage07 exclude_from_axes / posthoc flags are
# advisory hints in the prompt only (no synthetic placeholders, no topic skipping).
#
# Usage:
#   bash scripts/run_stage08_placeholder_v4_call.sh          # call 73, full run
#   bash scripts/run_stage08_placeholder_v4_call.sh 73 --limit-topics 20   # pilot
#
# Requires OPENROUTER_API_KEY in the environment (or .env).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f "${ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT}/.env"
  set +a
fi

CALL="${1:-73}"
shift || true

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

CFG="${ROOT}/configs/stage08_labeling.yaml"
OUT_DIR="${ROOT}/results/stage08_llm_labeling/placeholder_v4_call${CALL}"
LOG_DIR="${ROOT}/logs"

mkdir -p "$OUT_DIR" "$LOG_DIR"
export PYTHONUNBUFFERED=1

echo "[stage08] call=${CALL} | limit-topics via extra args: $*"
echo "[stage08] output labels -> ${OUT_DIR}/"
echo "[stage08] run log (timestamped) -> ${LOG_DIR}/stage08_llm_labeling_<timestamp>.log"
echo "[stage08] per-topic progress also in logger (topic N | label=...)"
echo ""

exec "$PY" -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config "$CFG" \
  --model-dir "results/experiments/placeholder_v4_models/final_compare/call_${CALL}/model_compare_enriched" \
  --topics-json "results/stage06_topic_exploration/placeholder_v4_call${CALL}/topics_all_representations_placeholder_v4_call.json" \
  --quality-csv "results/stage07_topic_quality/placeholder_v4_call${CALL}/topic_quality_placeholder_v4_call${CALL}.csv" \
  --output-dir "results/stage08_llm_labeling/placeholder_v4_call${CALL}" \
  --no-integrate \
  "$@"
