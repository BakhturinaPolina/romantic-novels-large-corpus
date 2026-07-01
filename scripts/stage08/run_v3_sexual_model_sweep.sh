#!/usr/bin/env bash
# Label ~28 sexual/suggestive call73 topics with v3_sexual_precision for model comparison.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

TOPICS="1,2,7,26,40,56,66,70,72,78,84,108,118,123,138,140,152,161,174,210,218,248,257,277,284,292,303,326"
PY="${ROOT}/.venv/bin/python3"
COMMON=(
  -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter
  --stage08-config configs/stage08/stage08_labeling_v3_sexual.yaml
  --topic-ids "$TOPICS"
  --no-integrate
  --no-resume
  --rate-limit-delay 6.0
)

run_model() {
  local model="$1"
  local suffix="$2"
  local extra_delay="${3:-6.0}"
  echo "=== $model (delay ${extra_delay}s) ==="
  "$PY" "${COMMON[@]}" \
    --rate-limit-delay "$extra_delay" \
    --model-name "$model" \
    --output-suffix "v3_sexual_subset_${suffix}" || return 1
}

# Usage: ./scripts/stage08/run_v3_sexual_model_sweep.sh [sonnet|lumimaid|grok|dolphin|compare|all]
case "${1:-compare}" in
  sonnet)   run_model "anthropic/claude-sonnet-4.6" "sonnet" ;;
  lumimaid)
    echo "SKIP: neversleep/llama-3-lumimaid-70b has no OpenRouter endpoints (404 as of 2026-06-29)."
    echo "See https://openrouter.ai/neversleep/llama-3-lumimaid-70b — not currently routable."
    ;;
  grok)     run_model "x-ai/grok-4.20" "grok420" ;;
  dolphin)  run_model "cognitivecomputations/dolphin-mistral-24b-venice-edition:free" "dolphin24b" 45 ;;
  compare)  "$PY" scripts/stage08/compare_v3_sexual_model_labels.py ;;
  all)
    run_model "anthropic/claude-sonnet-4.6" "sonnet" || true
    run_model "x-ai/grok-4.20" "grok420" || true
    run_model "cognitivecomputations/dolphin-mistral-24b-venice-edition:free" "dolphin24b" 45 || true
    "$PY" scripts/stage08/compare_v3_sexual_model_labels.py
    ;;
  *) echo "Unknown key: $1"; exit 1 ;;
esac
