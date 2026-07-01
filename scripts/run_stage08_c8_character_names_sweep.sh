#!/usr/bin/env bash
# A/B sweep: v2_s1_snippets_first vs v2_c8_character_names on character-name gold panel.
#
# Usage:
#   bash scripts/run_stage08_c8_character_names_sweep.sh
#
# Promotion criteria (21-topic panel):
#   - No regression on regression guards (0,1,2,4,5,12,13)
#   - Improves name-artifact stratum vs baseline
#   - Preserves stage07 overrides (29,52,93) as scenes
#   - name_label_ok >= baseline
#
# Requires OPENROUTER_API_KEY. Cost ~$0.35–0.70 (~36 API calls).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f "${ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT}/.env"
  set +a
fi

CALL=73
MODEL="anthropic/claude-sonnet-4.6"
SWEEP_DIR="${ROOT}/results/stage08_llm_labeling/prompt_sweeps/call73"
SWEEP_OUT="${SWEEP_DIR}/character_names"
TEMP=0.0
TOPIC_IDS="0,1,2,4,5,12,13,29,52,93,122,124,132,160,175,180,215,226,266,302,316"
mkdir -p "$SWEEP_OUT" "${ROOT}/logs"

_skip_if_complete() {
  local suffix="$1"
  local pattern="*${suffix}_topics.json"
  local match
  match="$(find "$SWEEP_OUT" -maxdepth 1 -name "$pattern" 2>/dev/null | head -1 || true)"
  if [[ -n "$match" ]]; then
    local n expected
    expected=21
    n="$("$ROOT/.venv/bin/python" -c "import json; print(len(json.load(open('$match'))))")"
    if [[ "$n" -ge "$expected" ]]; then
      echo "[c8-sweep] skip ${suffix} (complete: $match, n=$n)"
      return 0
    fi
    echo "[c8-sweep] removing partial ${suffix} ($match, n=$n)"
    rm -f "$match"
  fi
  return 1
}

_run() {
  local suffix="$1"
  shift
  if [[ "${SKIP_COMPLETE:-1}" == "1" ]] && _skip_if_complete "$suffix"; then
    return 0
  fi
  local log="${ROOT}/logs/stage08_c8_sweep_${suffix}_$(date +%Y%m%d_%H%M%S).log"
  echo "[c8-sweep] ${suffix} -> ${SWEEP_OUT} (log: ${log})"
  "$ROOT/.venv/bin/python" -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
    --stage08-config configs/stage08_labeling.yaml \
    --model-dir "results/experiments/placeholder_v4_models/final_compare/call_${CALL}/model_compare_enriched" \
    --topics-json "results/stage06_topic_exploration/placeholder_v4_call${CALL}/topics_all_representations_placeholder_v4_call.json" \
    --quality-csv "results/stage07_topic_quality/placeholder_v4_call${CALL}/topic_quality_placeholder_v4_call${CALL}.csv" \
    --output-dir "$SWEEP_OUT" \
    --model-name "$MODEL" \
    --temperature "$TEMP" \
    --topic-ids "$TOPIC_IDS" \
    --no-resume \
    --no-integrate \
    "$@" 2>&1 | tee "$log"
}

_find_labels() {
  local suffix="$1"
  find "$SWEEP_OUT" -maxdepth 1 -name "*${suffix}_topics.json" 2>/dev/null | head -1
}

_score_one() {
  local path="$1"
  "$ROOT/.venv/bin/python" scripts/score_stage08_prompt_sweep.py \
    --sweep-dir "$SWEEP_DIR" \
    --panel character_name \
    --labels "$path"
}

echo "[c8-sweep] Character-name A/B panel (${TOPIC_IDS})"

_run sweep_c8_baseline \
  --prompt-version v2_s1_snippets_first \
  --output-suffix sweep_c8_baseline

_run sweep_c8 \
  --prompt-version v2_c8_character_names \
  --output-suffix sweep_c8

BASELINE_JSON="$(_find_labels sweep_c8_baseline)"
C8_JSON="$(_find_labels sweep_c8)"

if [[ -z "$BASELINE_JSON" || -z "$C8_JSON" ]]; then
  echo "[c8-sweep] ERROR: expected output JSONs not found in ${SWEEP_OUT}" >&2
  exit 1
fi

echo ""
echo "=== Baseline (v2_s1_snippets_first) ==="
_score_one "$BASELINE_JSON"

echo ""
echo "=== C8 (v2_c8_character_names) ==="
_score_one "$C8_JSON"

echo ""
echo "[c8-sweep] Side-by-side metrics:"
"$ROOT/.venv/bin/python" - <<PY
import importlib.util
import json
from pathlib import Path

root = Path("${ROOT}")
spec = importlib.util.spec_from_file_location(
    "score_stage08_prompt_sweep",
    root / "scripts/score_stage08_prompt_sweep.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

gold = json.loads(
    (root / "data/stage08_benchmark/call73_panel_character_name_v1.json").read_text()
)
panel_ids = [int(k) for k in gold["topics"]]
for label, path in [
    ("baseline", "${BASELINE_JSON}"),
    ("c8", "${C8_JSON}"),
]:
    r = mod.score_labels(Path(path), gold, panel_ids)
    print(
        f"  {label:8}  score={r['score']:.4f}  routing={r['routing_accuracy']:.4f}  "
        f"name_artifact={r['name_artifact_routing']}  name_label_ok={r['name_label_ok']}"
    )
PY

echo ""
echo "[c8-sweep] Done."
echo "  Baseline: ${BASELINE_JSON}"
echo "  C8:       ${C8_JSON}"
