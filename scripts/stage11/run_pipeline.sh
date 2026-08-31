#!/usr/bin/env bash
# Stage 11 pipeline: manifests → evidence → stability → spillover → audits → master → frame.
# Pass --dry-run as second arg (or set STAGE11_DRY_RUN=1) to skip OpenRouter calls.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
CONFIG="${1:-configs/stage11/refined_constructs.yaml}"
DRY_FLAG=()
if [[ "${2:-}" == "--dry-run" || "${STAGE11_DRY_RUN:-0}" == "1" ]]; then
  DRY_FLAG=(--dry-run)
fi

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

echo "== Stage 11: candidate manifests =="
"$PY" src/stage11_refined_construct_analysis/pipeline/01_build_candidate_manifests.py --config "$CONFIG"

echo "== Stage 11: evidence packets (lexical+contextual) =="
"$PY" src/stage11_refined_construct_analysis/pipeline/02_build_evidence_packets.py --config "$CONFIG"

echo "== Stage 11: stability pilot =="
"$PY" src/stage11_refined_construct_analysis/pipeline/03_run_stability_pilot.py --config "$CONFIG" "${DRY_FLAG[@]+"${DRY_FLAG[@]}"}"

echo "== Stage 11: spillover triage (H1, H3, H4) =="
"$PY" src/stage11_refined_construct_analysis/pipeline/04_run_spillover_triage.py --config "$CONFIG" --hypotheses H1,H3,H4 "${DRY_FLAG[@]+"${DRY_FLAG[@]}"}"

echo "== Stage 11: Pass A/B/C audits (H1 → H3 → H4 → H2) =="
"$PY" src/stage11_refined_construct_analysis/pipeline/05_run_hypothesis_audits.py --config "$CONFIG" --hypotheses H1,H3,H4,H2 "${DRY_FLAG[@]+"${DRY_FLAG[@]}"}"

echo "== Stage 11: H5 → H6 audits =="
"$PY" src/stage11_refined_construct_analysis/pipeline/06_run_h5_h6_audits.py --config "$CONFIG" "${DRY_FLAG[@]+"${DRY_FLAG[@]}"}"

echo "== Stage 11: master annotation table + W_tk / W_tkr =="
"$PY" src/stage11_refined_construct_analysis/pipeline/07_build_master_table.py --config "$CONFIG"

echo "== Stage 11: refined analysis frame =="
"$PY" src/stage11_refined_construct_analysis/pipeline/08_build_refined_analysis_frame.py --config "$CONFIG"

echo "Done. Notebooks: notebooks/08_refined_construct_analysis/"
echo "Outputs under results/stage11_refined_construct_analysis/"
