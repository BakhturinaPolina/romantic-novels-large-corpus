#!/usr/bin/env bash
# Full-corpus pipeline for v4 L12 BO call 49 (wrapper around call-73 orchestrator).
#
# Usage:
#   nohup ./scripts/stage03/run_v4_call49_full_corpus.sh >> logs/v4_call49_full_corpus_console.log 2>&1 &
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

export RUN_ID="${RUN_ID:-v4_l12_granular_final_call49}"
export BO_CALL="${BO_CALL:-49}"

exec "$ROOT/scripts/stage03/run_v4_call73_full_corpus.sh" "$@"
