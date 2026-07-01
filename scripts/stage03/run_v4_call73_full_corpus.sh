#!/usr/bin/env bash
# Full-corpus pipeline for v4 L12 BO call 73:
#   0) precompute test embeddings (CUDA, resumable)
#   A) compare-fit refit + save model (probabilities on, no reduce_outliers)
#   B) Stage05b test holdout (chunked, cached embeddings)
#   C) full-corpus sentence-level inference (train + val + test)
#
# Usage:
#   nohup ./scripts/stage03/run_v4_call73_full_corpus.sh >> logs/v4_call73_full_corpus_console.log 2>&1 &
#
# Env overrides:
#   TRANSFORM_BATCH_SIZE=16384  ENCODE_BATCH_SIZE=512  ENCODE_DEVICE=cuda
#   FORCE=1  RUN_ID=...  SKIP_INHIBIT=1
#
# Resume: steps skip when output markers exist unless FORCE=1.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

RUN_ID="${RUN_ID:-v4_l12_granular_final_call73}"
BO_CALL="${BO_CALL:-73}"
PATHS_CONFIG="${PATHS_CONFIG:-configs/stage03/paths_stage03_fit_v3.yaml}"
TRAIN_CONFIG="${TRAIN_CONFIG:-configs/stage03/train_v4_l12_final_call73.yaml}"
TRIALS_CSV="${TRIALS_CSV:-results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv}"
LOG_DIR="${LOG_DIR:-logs}"
FORCE="${FORCE:-0}"
SKIP_INHIBIT="${SKIP_INHIBIT:-0}"

TRANSFORM_BATCH_SIZE="${TRANSFORM_BATCH_SIZE:-16384}"
ENCODE_BATCH_SIZE="${ENCODE_BATCH_SIZE:-512}"
ENCODE_DEVICE="${ENCODE_DEVICE:-cuda}"
EMBEDDING_MODEL="${EMBEDDING_MODEL:-sentence-transformers/all-MiniLM-L12-v2}"
TEST_CSV="${TEST_CSV:-data/raw/romance_subdataset_filtered_v3/sentences_test.csv}"
TEST_CACHE="${TEST_CACHE:-data/interim/octis/v3_english_only/embeddings_cache/test_sentence-transformers__all-MiniLM-L12-v2.npy}"
TEST_PROGRESS="${TEST_CACHE}.progress.json"

COMPARE_ROOT="results/experiments/${RUN_ID}/final_compare/call_${BO_CALL}"
MODEL_DIR="${COMPARE_ROOT}"
HOLDOUT_METRICS="results/evaluation/${RUN_ID}/call_${BO_CALL}/test_metrics.json"
INFER_SUMMARY="results/experiments/${RUN_ID}/full_corpus_infer/infer_summary.json"

mkdir -p "$LOG_DIR"

die() {
  echo "ERROR: $*" >&2
  exit 1
}

ts() {
  date -Iseconds
}

elapsed_since() {
  local start=$1
  local now
  now=$(date +%s)
  echo $((now - start))
}

fmt_duration() {
  local secs=$1
  printf '%dh %dm %ds' $((secs / 3600)) $(((secs % 3600) / 60)) $((secs % 60))
}

log_eta() {
  local stage="$1"
  local est_hours="$2"
  echo "[$(ts)] ETA hint — ${stage}: ~${est_hours}h wall-clock (GPU-dependent; see progress logs)"
}

run_cmd() {
  if [[ "$SKIP_INHIBIT" == "1" ]] || ! command -v systemd-inhibit >/dev/null 2>&1; then
    "$@"
  else
    systemd-inhibit --what=sleep:idle --who="v4_call73" --why="GPU embedding/inference pipeline" "$@"
  fi
}

pipeline_start=$(date +%s)
echo "================================================================"
echo "[$(ts)] v4 call_${BO_CALL} full-corpus pipeline start"
echo "run_id=${RUN_ID} | config=${TRAIN_CONFIG} | paths=${PATHS_CONFIG}"
echo "transform_batch=${TRANSFORM_BATCH_SIZE} | encode_device=${ENCODE_DEVICE} | encode_batch=${ENCODE_BATCH_SIZE}"
echo "compare_root=${COMPARE_ROOT}"
echo "Tip: disable sleep/suspend while this runs (systemd-inhibit active unless SKIP_INHIBIT=1)."
echo "================================================================"

[[ -f "$TRIALS_CSV" ]] || die "Trials CSV not found: $TRIALS_CSV"
[[ -f "$TRAIN_CONFIG" ]] || die "Train config not found: $TRAIN_CONFIG"

# --- Step 0: test embedding cache (CUDA, resumable) ---------------------------
if [[ "$FORCE" == "1" ]] || [[ ! -f "$TEST_CACHE" ]] || [[ -f "$TEST_PROGRESS" ]]; then
  log_eta "Step 0 test embedding encode (~17.5M sentences, CUDA)" "2-6"
  step_start=$(date +%s)
  echo "[$(ts)] > Step 0 | encode test embeddings -> ${TEST_CACHE}"
  run_cmd "$PY" -m src.stage03_train.cli encode-split \
    --csv "$TEST_CSV" \
    --model-name "$EMBEDDING_MODEL" \
    --cache-file "$TEST_CACHE" \
    --device "$ENCODE_DEVICE" \
    --batch-size "$ENCODE_BATCH_SIZE" \
    --chunk-size 50000 \
    2>&1 | tee "${LOG_DIR}/stage03_encode_test_${RUN_ID}.log"
  step_secs=$(elapsed_since "$step_start")
  echo "[$(ts)] < Step 0 | done in $(fmt_duration "$step_secs")"
else
  echo "[$(ts)] Step 0 skipped ($TEST_CACHE exists; set FORCE=1 to re-encode)"
fi

[[ -f "$TEST_CACHE" ]] || die "Test embedding cache missing: $TEST_CACHE"

# --- Step A: compare-fit refit + stability + save model -----------------------
if [[ "$FORCE" == "1" ]] || [[ ! -f "${COMPARE_ROOT}/metrics.json" ]] || [[ ! -d "${COMPARE_ROOT}/model_compare" ]]; then
  log_eta "Step A compare-fit refit + stability (call_${BO_CALL})" "1.0-1.5"
  step_start=$(date +%s)
  echo "[$(ts)] > Step A | compare-fit refit bo_call=${BO_CALL} (probabilities=true, no reduce_outliers)"
  run_cmd "$PY" -m src.stage05_final_fit.cli compare \
    --trials "$TRIALS_CSV" \
    --bo-calls "$BO_CALL" \
    --run-id "$RUN_ID" \
    --paths-config "$PATHS_CONFIG" \
    --config "$TRAIN_CONFIG" \
    --stability-runs 3 \
    --stability-tolerance 75 \
    --save-model \
    2>&1 | tee "${LOG_DIR}/stage05_compare_${RUN_ID}.log"
  step_secs=$(elapsed_since "$step_start")
  echo "[$(ts)] < Step A | done in $(fmt_duration "$step_secs")"
else
  echo "[$(ts)] Step A skipped (metrics + model exist; set FORCE=1 to refit)"
fi

[[ -d "${COMPARE_ROOT}/model_compare" ]] || die "Step A model not found: ${COMPARE_ROOT}/model_compare"

# --- Step B: Stage05b test holdout (cached embeddings) ------------------------
if [[ "$FORCE" == "1" ]] || [[ ! -f "$HOLDOUT_METRICS" ]]; then
  log_eta "Step B Stage05b test holdout (cached embeddings, ~17.5M)" "5-10"
  step_start=$(date +%s)
  echo "[$(ts)] > Step B | holdout scoring on test split"
  run_cmd "$PY" -m src.stage05b_test_holdout.cli score \
    --final-model "$MODEL_DIR" \
    --policy train_plus_val \
    --run-id "$RUN_ID" \
    --bo-call "$BO_CALL" \
    --train-config "$TRAIN_CONFIG" \
    --batch-size "$TRANSFORM_BATCH_SIZE" \
    --chunk-size 50000 \
    --coherence-max-docs 100000 \
    2>&1 | tee "${LOG_DIR}/stage05b_holdout_${RUN_ID}.log"
  step_secs=$(elapsed_since "$step_start")
  echo "[$(ts)] < Step B | done in $(fmt_duration "$step_secs")"
else
  echo "[$(ts)] Step B skipped ($HOLDOUT_METRICS exists; set FORCE=1 to rerun)"
fi

# --- Step C: full-corpus sentence inference -----------------------------------
if [[ "$FORCE" == "1" ]] || [[ ! -f "$INFER_SUMMARY" ]]; then
  log_eta "Step C full-corpus infer (train+val+test ~115M, mmap embeddings)" "12-36"
  step_start=$(date +%s)
  echo "[$(ts)] > Step C | chunked transform train,val,test -> parquet"
  run_cmd "$PY" -m src.stage05_final_fit.cli infer-corpus \
    --model-dir "$MODEL_DIR" \
    --run-id "$RUN_ID" \
    --paths-config "$PATHS_CONFIG" \
    --config "$TRAIN_CONFIG" \
    --splits train,val,test \
    --batch-size "$TRANSFORM_BATCH_SIZE" \
    --chunk-size 50000 \
    2>&1 | tee "${LOG_DIR}/stage05_infer_corpus_${RUN_ID}.log"
  step_secs=$(elapsed_since "$step_start")
  echo "[$(ts)] < Step C | done in $(fmt_duration "$step_secs")"
else
  echo "[$(ts)] Step C skipped ($INFER_SUMMARY exists; set FORCE=1 to rerun)"
fi

# --- Step D: downstream aggregation pointers ----------------------------------
echo "[$(ts)] Step D (manual / next night): book-level + tertile aggregation"
echo "  Sentence parquet: results/experiments/${RUN_ID}/full_corpus_infer/sentence_topics_{train,val,test}.parquet"
echo "  Book probs: src/stage10_correlation_analysis/data_preparation/03_generate_topic_probabilities_final.py"
echo "  Tertile probs: src/stage10_correlation_analysis/data_preparation/04_generate_tertile_topic_probs_patched_v3.py"
echo "  Strategy memo: results/reports/placeholder_v4_call73_analysis_strategy.md"

total_secs=$(elapsed_since "$pipeline_start")
echo "================================================================"
echo "[$(ts)] Pipeline finished in $(fmt_duration "$total_secs")"
echo "Test cache:  ${TEST_CACHE}"
echo "Compare-fit: ${COMPARE_ROOT}/metrics.json"
echo "Holdout:     ${HOLDOUT_METRICS}"
echo "Infer:       ${INFER_SUMMARY}"
echo "================================================================"
