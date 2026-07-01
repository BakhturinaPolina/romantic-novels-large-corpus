#!/usr/bin/env bash
# Stage 08A: LLM quality adjudication for Stage07 soft-review topics.
#
# Usage: bash scripts/stage08/run_stage08a_quality_adjudication.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

exec "$PY" -m src.stage08_llm_labeling.openrouter_experiments.core.run_quality_adjudication \
  --config "configs/stage08/stage08a_quality_adjudication.yaml"
