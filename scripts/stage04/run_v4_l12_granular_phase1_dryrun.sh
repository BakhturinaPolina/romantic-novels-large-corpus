#!/usr/bin/env bash
# Backward-compatible wrapper for L12 Stage04 dry-run.
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/scripts/stage04/run_v4_granular_phase1_dryrun.sh" l12
