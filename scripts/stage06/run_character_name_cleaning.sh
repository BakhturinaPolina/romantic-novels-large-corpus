#!/usr/bin/env bash
# Pre-Stage07 character name cleaning for v4 placeholder models.
#
# Usage:
#   bash scripts/stage06/run_character_name_cleaning.sh 73
#
# Outputs:
#   results/stage06_name_cleaning/placeholder_v4_call<N>/
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

CALL="${1:-73}"
PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

exec "$PY" -m src.common.character_name_cleaning.cli "$CALL"
