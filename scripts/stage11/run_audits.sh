#!/usr/bin/env bash
# Spillover triage + Pass A/B/C for H1–H4 (Nemo). Usage:
#   scripts/stage11/run_audits.sh              # live OpenRouter (loads .env)
#   scripts/stage11/run_audits.sh --dry-run    # deterministic offline artifacts
#   scripts/stage11/run_audits.sh --dry-run --limit 5
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
CONFIG="${STAGE11_CONFIG:-configs/stage11/refined_constructs.yaml}"

# Load OpenRouter key from repo .env when present (never echo the value).
if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

DRY=()
LIMIT=()
HYPS="H1,H3,H4,H2"
RESUME=(--no-resume)
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=(--dry-run); shift ;;
    --limit) LIMIT=(--limit "$2"); shift 2 ;;
    --hypotheses) HYPS="$2"; shift 2 ;;
    --config) CONFIG="$2"; shift 2 ;;
    --resume) RESUME=(); shift ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ ${#DRY[@]} -eq 0 && -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo "OPENROUTER_API_KEY missing (set in .env or environment)" >&2
  exit 1
fi

echo "== Spillover triage (H1, H3) =="
"$PY" src/stage11_refined_construct_analysis/pipeline/04_run_spillover_triage.py \
  --config "$CONFIG" --hypotheses H1,H3 "${DRY[@]+"${DRY[@]}"}"

echo "== Pass A/B/C (${HYPS}) =="
"$PY" src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py \
  --config "$CONFIG" --hypotheses "$HYPS" "${DRY[@]+"${DRY[@]}"}" "${LIMIT[@]+"${LIMIT[@]}"}" "${RESUME[@]+"${RESUME[@]}"}"

echo "Audits written under results/stage11_refined_construct_analysis/*/audits/"
