#!/usr/bin/env bash
# Apply a filled H4 manual freeze, rebuild constructs, refresh NB04 + NB08–11.
#
# Prerequisites:
#   results/.../human_review/h4_manual_freeze.json with frozen=true and all 26 decisions.
#
# Usage:
#   bash scripts/stage11/apply_h4_manual_freeze.sh
#   SKIP_NOTEBOOKS=1 bash scripts/stage11/apply_h4_manual_freeze.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PY="${PY:-.venv/bin/python}"
SKIP_NOTEBOOKS="${SKIP_NOTEBOOKS:-0}"
CONFIG="${CONFIG:-configs/stage11/refined_constructs.yaml}"
PROGRESS="${PROGRESS:-logs/h4_manual_freeze_apply_progress.txt}"
mkdir -p logs

note() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$msg" | tee -a "$PROGRESS"
}

note "START H4 manual freeze apply"

note "Validate freeze file"
$PY - <<'PY'
from src.stage11_refined_construct_analysis.config import load_stage11_config
from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
    EXPECTED_TOPIC_IDS,
    default_freeze_path,
    load_construct_coverage_ids,
    load_h4_manual_freeze,
    validate_h4_manual_freeze,
)

cfg = load_stage11_config()
path = default_freeze_path(cfg)
data = load_h4_manual_freeze(cfg)
if data is None:
    raise SystemExit(f"Missing freeze file: {path}\nFill h4_manual_freeze_decisions.json, set frozen=true, save as h4_manual_freeze.json")
by_bucket = load_construct_coverage_ids(cfg)
expected = []
for b in ("external_protection", "protective_commitment", "possession_control"):
    expected.extend(by_bucket[b])
expected = sorted(set(expected)) or list(EXPECTED_TOPIC_IDS)
errs = validate_h4_manual_freeze(data, expected_ids=expected, require_frozen=True)
if errs:
    raise SystemExit("Invalid H4 manual freeze:\n  - " + "\n  - ".join(errs))
print(f"OK: {path} ({len(data.get('decisions') or [])} decisions)")
PY

note "Rebuild master + W_tk (07)"
$PY src/stage11_refined_construct_analysis/pipeline/07_build_master_table.py --config "$CONFIG"

note "Rebuild refined analysis frame (08)"
$PY src/stage11_refined_construct_analysis/pipeline/08_build_refined_analysis_frame.py --config "$CONFIG"

if [[ "$SKIP_NOTEBOOKS" == "1" ]]; then
  note "SKIP_NOTEBOOKS=1 — done after construct rebuild"
  exit 0
fi

NBS=(
  04_h4_protection_possession_audit
  07_refined_construct_dictionary
  08_refined_axes_validity
  09_refined_hypothesis_tests
  10_contextual_validation
  11_refined_robustness
)

note "Sync _src → ipynb"
SRC_ARGS=()
for nb in "${NBS[@]}"; do
  SRC_ARGS+=("notebooks/08_refined_construct_analysis/_src/${nb}.py")
done
SRC_ARGS+=("notebooks/08_refined_construct_analysis/_src/00_refinement_foundations.py")
$PY scripts/stage11/percent_to_notebook.py "${SRC_ARGS[@]}" || note "WARN percent_to_notebook partial failure"

note "Execute notebooks 04 + 08–11"
for nb in "${NBS[@]}"; do
  note "  nbconvert ${nb}.ipynb"
  .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=900 \
    --ExecutePreprocessor.kernel_name=python3 \
    "notebooks/08_refined_construct_analysis/${nb}.ipynb" \
    || note "WARN notebook ${nb} failed (continuing)"
done

note "Optional: refresh full human-review PDF (includes updated H4 count)"
$PY scripts/stage11/export_human_review_pdf.py || note "WARN full human_review export failed"

note "DONE H4 manual freeze apply"
