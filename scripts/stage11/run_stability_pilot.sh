#!/usr/bin/env bash
# Pre-batch prompt stability pilot (10–15 hard topics; two phrasings / two models).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
CONFIG="${CONFIG:-configs/stage11/refined_constructs.yaml}"

EXTRA=()
if [[ "${DRY_RUN:-0}" == "1" ]]; then
  EXTRA+=(--dry-run)
fi
if [[ "${LEXICAL_ONLY:-0}" == "1" ]]; then
  EXTRA+=(--lexical-only)
fi

# Prefer .env OPENROUTER_API_KEY when present (do not require it for dry-run).
if [[ -f "${ROOT}/.env" ]]; then
  # shellcheck disable=SC1091
  set -a
  source "${ROOT}/.env"
  set +a
fi

"$PY" src/stage11_refined_construct_analysis/pipeline/03_run_stability_pilot.py \
  --config "$CONFIG" \
  "${EXTRA[@]}"
