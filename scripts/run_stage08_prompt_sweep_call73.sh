#!/usr/bin/env bash
# Stage08 prompt OVAT sweeps for call 73 (Sonnet 4.6, temp=0).
#
# Usage:
#   bash scripts/run_stage08_prompt_sweep_call73.sh phase0b
#   bash scripts/run_stage08_prompt_sweep_call73.sh phase_a
#   bash scripts/run_stage08_prompt_sweep_call73.sh phase_b [BASE_PROMPT_VERSION]
#   bash scripts/run_stage08_prompt_sweep_call73.sh phase_c [FINAL_PROMPT_VERSION]
#
# Requires OPENROUTER_API_KEY.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f "${ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT}/.env"
  set +a
fi

PHASE="${1:-phase0b}"
BASE_PROMPT="${2:-v2}"
CALL=73
MODEL="anthropic/claude-sonnet-4.6"
SWEEP_DIR="${ROOT}/results/stage08_llm_labeling/prompt_sweeps/call73"
SWEEP_OUT="${SWEEP_DIR}/phase_0"
LIMIT=20
TEMP=0.0
mkdir -p "$SWEEP_DIR" "${ROOT}/logs"

_set_phase_out() {
  case "$PHASE" in
    phase0b) SWEEP_OUT="${SWEEP_DIR}/phase_0" ;;
    phase_a|phase_a_resume) SWEEP_OUT="${SWEEP_DIR}/phase_a" ;;
    phase_b) SWEEP_OUT="${SWEEP_DIR}/phase_b" ;;
    phase_c) SWEEP_OUT="${SWEEP_DIR}/phase_c" ;;
    phase_c8) SWEEP_OUT="${SWEEP_DIR}/character_names" ;;
    *) SWEEP_OUT="${SWEEP_DIR}" ;;
  esac
  mkdir -p "$SWEEP_OUT"
}

_skip_if_complete() {
  local suffix="$1"
  local pattern="*${suffix}_limit${LIMIT}.json"
  local match
  match="$(find "$SWEEP_OUT" -maxdepth 1 -name "$pattern" 2>/dev/null | head -1 || true)"
  if [[ -n "$match" ]]; then
    local n
    n="$("$ROOT/.venv/bin/python" -c "import json; print(len(json.load(open('$match'))))")"
    if [[ "$n" -ge "$LIMIT" ]]; then
      echo "[sweep] skip ${suffix} (complete: $match, n=$n)"
      return 0
    fi
    echo "[sweep] removing partial ${suffix} ($match, n=$n)"
    rm -f "$match"
  fi
  return 1
}

_run() {
  local suffix="$1"
  shift
  _set_phase_out
  if [[ "${SKIP_COMPLETE:-0}" == "1" ]] && _skip_if_complete "$suffix"; then
    return 0
  fi
  local log="${ROOT}/logs/stage08_sweep_${suffix}_$(date +%Y%m%d_%H%M%S).log"
  local limit_args=(--limit-topics "$LIMIT")
  if [[ "${NO_TOPIC_LIMIT:-0}" == "1" ]]; then
    limit_args=()
  fi
  echo "[sweep] ${suffix} -> ${SWEEP_OUT} (log: ${log})"
  "$ROOT/.venv/bin/python" -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
    --stage08-config configs/stage08_labeling.yaml \
    --model-dir "results/experiments/placeholder_v4_models/final_compare/call_${CALL}/model_compare_enriched" \
    --topics-json "results/stage06_topic_exploration/placeholder_v4_call${CALL}/topics_all_representations_placeholder_v4_call.json" \
    --quality-csv "results/stage07_topic_quality/placeholder_v4_call${CALL}/topic_quality_placeholder_v4_call${CALL}.csv" \
    --output-dir "$SWEEP_OUT" \
    --model-name "$MODEL" \
    --temperature "$TEMP" \
    ${limit_args[@]+"${limit_args[@]}"} \
    --no-resume \
    --no-integrate \
    "$@" 2>&1 | tee "$log"
}

case "$PHASE" in
  phase0b)
    _run D2a_temp035 --prompt-version v2 --output-suffix sweep_D2a_temp035 --temperature 0.35
    _run D2b_temp0 --prompt-version v2 --output-suffix sweep_D2b_temp0 --temperature 0.0
    ;;
  phase_a)
    SKIP_COMPLETE=0
    _run S1 --prompt-version v2_s1_snippets_first --output-suffix sweep_S1
    _run S2_snippets3 --prompt-version v2 --output-suffix sweep_S2_snippets3 --max-snippets 3
    _run S2_snippets8 --prompt-version v2 --output-suffix sweep_S2_snippets8 --max-snippets 8
    _run S3_kw10 --prompt-version v2 --output-suffix sweep_S3_kw10 --num-keywords 10
    _run S4_no_stage07 --prompt-version v2_s4_no_stage07 --output-suffix sweep_S4_no_stage07
    _run S4_emphasize --prompt-version v2_s4_stage07_emphasize --output-suffix sweep_S4_emphasize
    _run S5_no_fewshot --prompt-version v2_s5_no_fewshot --output-suffix sweep_S5_no_fewshot
    _run S5_expanded --prompt-version v2_s5_expanded_fewshot --output-suffix sweep_S5_expanded
    _run S6 --prompt-version v2_s6_label_first --output-suffix sweep_S6
    _run S7 --prompt-version v2_s7_checklist --output-suffix sweep_S7
    ;;
  phase_a_resume)
    SKIP_COMPLETE=1
    _run S1 --prompt-version v2_s1_snippets_first --output-suffix sweep_S1
    _run S2_snippets3 --prompt-version v2 --output-suffix sweep_S2_snippets3 --max-snippets 3
    _run S2_snippets8 --prompt-version v2 --output-suffix sweep_S2_snippets8 --max-snippets 8
    _run S3_kw10 --prompt-version v2 --output-suffix sweep_S3_kw10 --num-keywords 10
    _run S4_no_stage07 --prompt-version v2_s4_no_stage07 --output-suffix sweep_S4_no_stage07
    _run S4_emphasize --prompt-version v2_s4_stage07_emphasize --output-suffix sweep_S4_emphasize
    _run S5_no_fewshot --prompt-version v2_s5_no_fewshot --output-suffix sweep_S5_no_fewshot
    _run S5_expanded --prompt-version v2_s5_expanded_fewshot --output-suffix sweep_S5_expanded
    _run S6 --prompt-version v2_s6_label_first --output-suffix sweep_S6
    _run S7 --prompt-version v2_s7_checklist --output-suffix sweep_S7
    ;;
  phase_b)
    _run C1 --prompt-version v2_c1_discourse_strict --output-suffix sweep_C1
    _run C2 --prompt-version v2_c2_noise_conservative --output-suffix sweep_C2
    _run C3 --prompt-version v2_c3_snippet_grounding --output-suffix sweep_C3
    _run C4 --prompt-version v2_c4_abstract_discourse --output-suffix sweep_C4
    _run C5 --prompt-version v2_c5_merge_ladder --output-suffix sweep_C5
    _run C6 --prompt-version v2_c6_label_antipatterns --output-suffix sweep_C6
    _run C7 --prompt-version v2_c7_discourse_prior --output-suffix sweep_C7
    ;;
  phase_c)
    FINAL_PROMPT="${BASE_PROMPT}"
    TOPIC_IDS="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,31,70,29,52,256,95,221,284,302,188,214"
    NO_TOPIC_LIMIT=1
    _run phase_c_full --prompt-version "$FINAL_PROMPT" --output-suffix sweep_phase_c \
      --topic-ids "$TOPIC_IDS"
    ;;
  phase_c8)
    exec bash "${ROOT}/scripts/run_stage08_c8_character_names_sweep.sh"
    ;;
  *)
    echo "Unknown phase: $PHASE (use phase0b, phase_a, phase_a_resume, phase_b, phase_c, phase_c8)"
    exit 1
    ;;
esac

echo "[sweep] Done. Score with:"
echo "  python scripts/score_stage08_prompt_sweep.py --sweep-dir ${SWEEP_DIR}"
