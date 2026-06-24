#!/usr/bin/env bash
# Run post-hoc topic classification on call_59 topic_info.csv (no GPU).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CALL59_DIR="results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59"
TOPIC_INFO="${CALL59_DIR}/topic_info.csv"

if [[ ! -f "$TOPIC_INFO" ]]; then
  echo "Missing toy dataset: $TOPIC_INFO" >&2
  exit 1
fi

.venv/bin/python - <<'PY'
from pathlib import Path

from src.common.topic_posthoc.rules import write_posthoc_artifacts

topic_info = Path("results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/topic_info.csv")
flags_path, summary_path = write_posthoc_artifacts(topic_info)
print(f"Wrote {flags_path}")
print(f"Wrote {summary_path}")
PY

echo "Done. Inspect ${CALL59_DIR}/posthoc_flags.csv and posthoc_summary.json"
