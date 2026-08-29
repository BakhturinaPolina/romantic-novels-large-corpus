#!/usr/bin/env bash
# Stage09 re-run for the call_49 final model, prompt v2.5 (evidence-hardened) + Radway stage 2.
#
# Usage:
#   scripts/stage09/run_call49_rerun2.sh pilot     # 30 stratified topics, then a diff report
#   scripts/stage09/run_call49_rerun2.sh full      # all 348 topics (resumable)
#   scripts/stage09/run_call49_rerun2.sh radway    # Radway R1-R13 on the new taxonomy mapping
#   scripts/stage09/run_call49_rerun2.sh report    # old-vs-new mapping stability report
#   scripts/stage09/run_call49_rerun2.sh status    # how many topics are already mapped
#   scripts/stage09/run_call49_rerun2.sh all       # full + radway + report
#
# 'full' writes a checkpoint after every topic and skips topics already present in the output
# file, so re-running it after any interruption — including an OpenRouter 402 when credits run
# out — picks up exactly where it stopped.
#
# Both runners read OPENROUTER_API_KEY from the environment only, so this script exports
# it from .env for you. Both are invoked by path but import `src.*`, so PYTHONPATH is set
# here too. The Radway runner does not default to the stage-1 model, so it is passed
# explicitly to keep one model and temperature across both stages.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PY="${PY:-$ROOT/.venv/bin/python}"
MODEL="${STAGE09_MODEL:-anthropic/claude-sonnet-4.6}"
PROMPT_VERSION="${STAGE09_PROMPT_VERSION:-v2.5}"
# The runner's 10s default is sized for Mistral-Nemo's strict limits; Claude via OpenRouter
# tolerates much less, which takes the 348-topic run from ~2h to ~40min.
REQUEST_DELAY="${STAGE09_REQUEST_DELAY:-2.0}"

OLD_RUN="placeholder_v4_call49"
NEW_RUN="placeholder_v4_call49_rerun2"

S09_DIR="results/stage09_category_mapping/stage1_theory_driven_categories"
RADWAY_DIR="results/stage09_category_mapping/stage2_radway_functions/$NEW_RUN"
METADATA="results/stage08_llm_labeling/$OLD_RUN/stage09_input/topic_metadata_v3.json"
OLD_MAPPINGS="$S09_DIR/$OLD_RUN/taxonomy_mappings.json"
NEW_MAPPINGS="$S09_DIR/$NEW_RUN/taxonomy_mappings.json"
PILOT_DIR="$S09_DIR/$NEW_RUN/pilot"
PILOT_METADATA="$PILOT_DIR/topic_metadata_v3_pilot30.json"
PILOT_MAPPINGS="$PILOT_DIR/taxonomy_mappings_pilot30.json"
REPORT_DIR="results/reports/stage09"

if [[ -f .env ]]; then
  set -a; source .env; set +a
fi
if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo "ERROR: OPENROUTER_API_KEY is not set (checked environment and .env)." >&2
  exit 1
fi
export OPENROUTER_API_KEY
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

run_pilot() {
  echo "=== Stage09 pilot: 30 stratified topics, prompt $PROMPT_VERSION ==="
  "$PY" scripts/stage09/build_pilot_subset.py \
    --metadata-json "$METADATA" \
    --current-mappings "$OLD_MAPPINGS" \
    --output-json "$PILOT_METADATA"

  "$PY" src/stage09_category_mapping/stage1_theory_driven_categories/scripts/zeroshot_taxonomy_openrouter.py \
    --labels-json "$PILOT_METADATA" \
    --output-json "$PILOT_MAPPINGS" \
    --prompt-version "$PROMPT_VERSION" \
    --model-name "$MODEL" \
    --temperature 0.0 \
    --request-delay "$REQUEST_DELAY" \
    --no-snippets

  "$PY" scripts/stage09/compare_taxonomy_mappings.py \
    --old-mappings "$OLD_MAPPINGS" \
    --new-mappings "$PILOT_MAPPINGS" \
    --metadata-json "$METADATA" \
    --strata-manifest "$PILOT_DIR/topic_metadata_v3_pilot30.manifest.json" \
    --report-md "$REPORT_DIR/call49_rerun2_pilot_diff.md" \
    --report-csv "$REPORT_DIR/call49_rerun2_pilot_diff.csv" \
    --title "Stage09 v2.5 pilot diff (30 stratified topics, call_49)"

  echo "Review $REPORT_DIR/call49_rerun2_pilot_diff.md before running 'full'."
}

run_full() {
  echo "=== Stage09 full re-run: 348 topics, prompt $PROMPT_VERSION (resumable) ==="
  "$PY" src/stage09_category_mapping/stage1_theory_driven_categories/scripts/zeroshot_taxonomy_openrouter.py \
    --labels-json "$METADATA" \
    --output-json "$NEW_MAPPINGS" \
    --prompt-version "$PROMPT_VERSION" \
    --model-name "$MODEL" \
    --temperature 0.0 \
    --request-delay "$REQUEST_DELAY" \
    --no-snippets \
    --include-source-metadata
}

run_radway() {
  echo "=== Stage09 stage 2: Radway R1-R13 ==="
  mkdir -p "$RADWAY_DIR"
  # --model-name is required: it otherwise defaults to Mistral-Nemo, not the stage-1 model.
  "$PY" src/stage09_category_mapping/stage2_radway_functions/scripts/zeroshot_radway_openrouter.py \
    --taxonomy-json "$NEW_MAPPINGS" \
    --output-json "$RADWAY_DIR/taxonomy_with_radway.json" \
    --model-name "$MODEL" \
    --temperature 0.0 \
    --request-delay "$REQUEST_DELAY" \
    --no-snippets
}

run_report() {
  echo "=== Stage09 mapping stability report (old vs new) ==="
  "$PY" scripts/stage09/compare_taxonomy_mappings.py \
    --old-mappings "$OLD_MAPPINGS" \
    --new-mappings "$NEW_MAPPINGS" \
    --metadata-json "$METADATA" \
    --report-md "$REPORT_DIR/call49_rerun2_mapping_stability.md" \
    --report-csv "$REPORT_DIR/call49_rerun2_mapping_stability.csv" \
    --title "Stage09 v2.5 full re-run stability (call_49, 348 topics)" \
    --max-examples 80
}

run_status() {
  "$PY" - "$METADATA" "$NEW_MAPPINGS" "$RADWAY_DIR/taxonomy_with_radway.json" <<'PYEOF'
import json, sys
from pathlib import Path

def n_topics(path):
    p = Path(path)
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ("mappings", "topics", "results"):
        if isinstance(data, dict) and key in data:
            return len(data[key])
    return len(data) if isinstance(data, (list, dict)) else None

total, mapped, radway = (n_topics(a) for a in sys.argv[1:4])
print(f"topics in metadata      : {total}")
print(f"taxonomy mappings done  : {mapped or 0}")
if total and mapped and mapped < total:
    print(f"remaining               : {total - mapped}  (re-run 'full' to resume)")
print(f"radway mappings done    : {radway or 0}")
PYEOF
}

case "${1:-}" in
  pilot)  run_pilot ;;
  full)   run_full ;;
  radway) run_radway ;;
  report) run_report ;;
  status) run_status ;;
  all)    run_full; run_radway; run_report ;;
  *)      sed -n '2,20p' "$0" >&2; exit 1 ;;
esac
