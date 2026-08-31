#!/usr/bin/env bash
# Apply filled H3 + H4 manual freezes, rebuild constructs, refresh NB03/04 + NB08–11.
#
# Prerequisites:
#   human_review/h3_manual_freeze.json with frozen=true and all decisions filled
#   human_review/h4_manual_freeze.json with frozen=true and all decisions filled
#
# Usage:
#   bash scripts/stage11/apply_h3_h4_manual_freeze.sh
#   SKIP_NOTEBOOKS=1 bash scripts/stage11/apply_h3_h4_manual_freeze.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PY="${PY:-.venv/bin/python}"
SKIP_NOTEBOOKS="${SKIP_NOTEBOOKS:-0}"
CONFIG="${CONFIG:-configs/stage11/refined_constructs.yaml}"
PROGRESS="${PROGRESS:-logs/h3_h4_manual_freeze_apply_progress.txt}"
mkdir -p logs

note() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$msg" | tee -a "$PROGRESS"
}

note "START H3+H4 manual freeze apply"

note "Validate freeze files"
$PY - <<'PY'
from src.stage11_refined_construct_analysis.config import load_stage11_config
from src.stage11_refined_construct_analysis.analysis.h3_manual_freeze import (
    default_freeze_path as h3_path_fn,
    expected_h3_freeze_ids,
    load_h3_manual_freeze,
    validate_h3_manual_freeze,
)
from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
    EXPECTED_TOPIC_IDS,
    default_freeze_path as h4_path_fn,
    load_construct_coverage_ids,
    load_h4_manual_freeze,
    validate_h4_manual_freeze,
)

cfg = load_stage11_config()

h3_path = h3_path_fn(cfg)
h3_data = load_h3_manual_freeze(cfg)
if h3_data is None:
    raise SystemExit(f"Missing H3 freeze file: {h3_path}")
h3_expected = expected_h3_freeze_ids(cfg)
h3_errs = validate_h3_manual_freeze(h3_data, expected_ids=h3_expected, require_frozen=True)
if h3_errs:
    raise SystemExit("Invalid H3 manual freeze:\n  - " + "\n  - ".join(h3_errs))
print(f"OK H3: {h3_path} ({len(h3_data.get('decisions') or [])} decisions)")

h4_path = h4_path_fn(cfg)
h4_data = load_h4_manual_freeze(cfg)
if h4_data is None:
    raise SystemExit(f"Missing H4 freeze file: {h4_path}")
h4_expected = sorted(int(d["topic_id"]) for d in h4_data.get("decisions") or [])
if not h4_expected:
    by_bucket = load_construct_coverage_ids(cfg)
    for b in ("external_protection", "protective_commitment", "possession_control"):
        h4_expected.extend(by_bucket[b])
    h4_expected = sorted(set(h4_expected)) or list(EXPECTED_TOPIC_IDS)
h4_errs = validate_h4_manual_freeze(h4_data, expected_ids=h4_expected, require_frozen=True)
if h4_errs:
    raise SystemExit("Invalid H4 manual freeze:\n  - " + "\n  - ".join(h4_errs))
print(f"OK H4: {h4_path} ({len(h4_data.get('decisions') or [])} decisions)")
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
  03_h3_security_material_audit
  04_h4_protection_possession_audit
  07_refined_construct_dictionary
  08_refined_axes_validity
  09_refined_hypothesis_tests
  10_contextual_validation
  11_refined_robustness
  12_exploratory_security_care_appearance
)

note "Sync _src → ipynb"
SRC_ARGS=()
for nb in "${NBS[@]}"; do
  SRC_ARGS+=("notebooks/08_refined_construct_analysis/_src/${nb}.py")
done
SRC_ARGS+=("notebooks/08_refined_construct_analysis/_src/00_refinement_foundations.py")
$PY scripts/stage11/percent_to_notebook.py "${SRC_ARGS[@]}" || note "WARN percent_to_notebook partial failure"

note "Execute notebooks 03/04 + 07–11"
for nb in "${NBS[@]}"; do
  note "  nbconvert ${nb}.ipynb"
  .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=900 \
    --ExecutePreprocessor.kernel_name=python3 \
    "notebooks/08_refined_construct_analysis/${nb}.ipynb" \
    || note "WARN notebook ${nb} failed (continuing)"
done

note "DONE H3+H4 manual freeze apply"
