#!/usr/bin/env bash
# Stage 08: label all topics (call 73, v3 natural-voice prompt, cleaned representations).
#
# Usage:
#   scripts/stage08/run_stage08_full_corpus.sh           # resume if partial output exists
#   scripts/stage08/run_stage08_full_corpus.sh --no-resume
#
# Requires OPENROUTER_API_KEY (or .env).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if [[ -f "${ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT}/.env"
  set +a
fi

PY="${ROOT}/.venv/bin/python"
CONFIG="${ROOT}/configs/stage08/stage08_labeling.yaml"
TS="$(date +%Y%m%d_%H%M%S)"
LOG="${ROOT}/logs/stage08_full_corpus_${TS}.log"
mkdir -p "${ROOT}/logs"

RESUME_ARGS=(--resume)
for arg in "$@"; do
  if [[ "$arg" == "--no-resume" ]]; then
    RESUME_ARGS=(--no-resume)
  fi
done

echo "=== Stage 08 full corpus labeling ===" | tee "$LOG"
echo "Config: $CONFIG" | tee -a "$LOG"
echo "Log: $LOG" | tee -a "$LOG"
echo "ETA: ~45–90 min for ~322 topics (rate limit + API latency)" | tee -a "$LOG"

"$PY" -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config "$CONFIG" \
  --label-all-topics \
  --no-integrate \
  "${RESUME_ARGS[@]}" \
  2>&1 | tee -a "$LOG"
