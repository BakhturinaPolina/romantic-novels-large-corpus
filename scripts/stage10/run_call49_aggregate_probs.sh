#!/usr/bin/env bash
# Step D: book / chapter / tertile topic probs from call-49 infer parquets.
#
# Does NOT re-run BERTopic. Uses soft probs already in sentence_topics_*.parquet.
#
# Usage:
#   nohup ./scripts/stage10/run_call49_aggregate_probs.sh \
#     >> logs/stage10_call49_aggregate_probs.log 2>&1 &
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

INFER_DIR="${INFER_DIR:-results/experiments/v4_l12_granular_final_call49/full_corpus_infer}"
OUT_DIR="${OUT_DIR:-results/stage10_correlation_analysis/v4_l12_granular_final_call49}"

exec "$PY" "$ROOT/scripts/stage10/aggregate_probs_from_infer.py" \
  --infer-dir "$INFER_DIR" \
  --output-dir "$OUT_DIR" \
  "$@"
