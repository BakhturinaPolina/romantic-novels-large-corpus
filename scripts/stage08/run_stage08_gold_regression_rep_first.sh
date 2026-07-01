#!/usr/bin/env bash
# Stage 08 gold regression for v3_rep_first (keyword-thread-first prompt)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"

GOLD_YAML="src/stage08_llm_labeling/golden/call73_gold_30.yaml"
GOLD_CAT_YAML="src/stage08_llm_labeling/golden/call73_gold_30_categorization.yaml"
CONFIG="configs/stage08/stage08_labeling_rep_first.yaml"
TOPIC_IDS="1,2,7,14,26,40,56,66,70,72,78,84,108,118,122,123,138,140,152,161,174,210,218,248,257,277,284,292,303,326"
OUTPUT_SUFFIX="gold30_regression_v3_rep_first"
TS="$(date +%Y%m%d_%H%M%S)"
LOG="logs/stage08_gold_regression_rep_first_${TS}.log"
mkdir -p logs results/stage08_llm_labeling/placeholder_v4_call73/gold_regression

echo "=== Stage 08 gold regression (v3_rep_first) ===" | tee "$LOG"
echo "Log: $LOG" | tee -a "$LOG"

"$PY" -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config "$CONFIG" \
  --topic-ids "$TOPIC_IDS" \
  --output-dir results/stage08_llm_labeling/placeholder_v4_call73/gold_regression \
  --output-suffix "$OUTPUT_SUFFIX" \
  --label-all-topics \
  --no-integrate \
  --no-resume \
  2>&1 | tee -a "$LOG"

LABELS_JSON=$(ls -t results/stage08_llm_labeling/placeholder_v4_call73/gold_regression/*"${OUTPUT_SUFFIX}"*.json 2>/dev/null | head -1)
if [[ -z "${LABELS_JSON:-}" ]]; then
  echo "ERROR: labels JSON not found under results/stage08_llm_labeling/" | tee -a "$LOG"
  exit 1
fi

echo "Validating: $LABELS_JSON" | tee -a "$LOG"
"$PY" -m src.stage08_llm_labeling.openrouter_experiments.tools.validate_label_quality \
  --labels-json "$LABELS_JSON" \
  --gold-yaml "$GOLD_YAML" \
  --gold-categorization-yaml "$GOLD_CAT_YAML" \
  --output-csv "results/stage08_llm_labeling/placeholder_v4_call73/gold_regression/gold30_rep_first_report_${TS}.csv" \
  2>&1 | tee -a "$LOG"
