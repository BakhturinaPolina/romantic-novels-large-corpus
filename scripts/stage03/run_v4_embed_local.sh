#!/usr/bin/env bash
# v4 granular: resumable MPNet/L6/L12 embedding download + encode + Phase 1 BO (.venv).
#
# Checkpoints:
#   encode — <cache>.npy.progress.json (row offset)
#   tune   — results/experiments/<run_id>/run_state.json + opt_*/result.json + trials_partial.csv
#
# Usage:
#   ./scripts/stage03/run_v4_embed_local.sh mpnet download   # HF mirror (optional)
#   ./scripts/stage03/run_v4_embed_local.sh mpnet encode     # GPU encode, resumable
#   ./scripts/stage03/run_v4_embed_local.sh mpnet eta-watch
#   ./scripts/stage03/run_v4_embed_local.sh mpnet tune      # start/resume BO
#   ./scripts/stage03/run_v4_embed_local.sh mpnet tune-status
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
[[ -x "$PYTHON" ]] || PYTHON="$(command -v python3)"

die() {
  echo "ERROR: $*" >&2
  exit 1
}

model_config() {
  case "$1" in
    l12)
      MODEL_NAME="sentence-transformers/all-MiniLM-L12-v2"
      RUN_ID="v4_l12_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_l12_granular_phase1.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__all-MiniLM-L12-v2.npy"
      HUB_RUN_ID="v3_minilm12v2_first"
      ENCODE_BATCH=256
      ENCODE_DEVICE="${ENCODE_DEVICE:-cuda}"
      NEED_GB=145
      ;;
    l6)
      MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
      RUN_ID="v4_l6_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_l6_granular_phase1.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy"
      HUB_RUN_ID="v3_minilm6_first"
      ENCODE_BATCH=256
      ENCODE_DEVICE="${ENCODE_DEVICE:-cuda}"
      NEED_GB=145
      ;;
    mpnet)
      MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
      RUN_ID="v4_mpnet_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_mpnet_granular_phase1.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy"
      HUB_RUN_ID="v3_mpnet_first"
      ENCODE_BATCH=128
      ENCODE_DEVICE="${ENCODE_DEVICE:-cuda}"
      NEED_GB=280
      ;;
    *)
      die "Unknown model '$1'. Use: l12 | l6 | mpnet"
      ;;
  esac
  LOG="$ROOT/logs/v4_embeddings_${1}.log"
  PID_FILE="$ROOT/logs/v4_embeddings_${1}.pid"
  CONSOLE_LOG="$ROOT/logs/${RUN_ID}_console.log"
  TUNE_LOG="$ROOT/logs/stage03_${RUN_ID}.log"
  TUNE_PID_FILE="$ROOT/logs/${RUN_ID}.pid"
  EXP_DIR="$ROOT/results/experiments/${RUN_ID}"
}

require_csvs() {
  local base="data/raw/romance_subdataset_filtered_v3"
  for f in sentences_train.csv sentences_val.csv; do
    [[ -f "$base/$f" ]] || die "Missing $base/$f"
  done
}

check_disk() {
  local need_kb avail_kb
  need_kb=$((NEED_GB * 1024 * 1024))
  avail_kb=$(df -Pk "$(dirname "$ROOT/$CACHE_FILE")" | awk 'NR==2 {print $4}')
  if [[ "$avail_kb" -lt "$need_kb" ]]; then
    die "Need ~${NEED_GB}GB free for MPNet cache; only $((avail_kb / 1024 / 1024))GB available on $(dirname "$ROOT/$CACHE_FILE")"
  fi
}

cmd_download() {
  local model="$1"
  model_config "$model"
  mkdir -p "$ROOT/logs"
  echo "HF download: $MODEL_NAME -> $CACHE_FILE (hub_run_id=$HUB_RUN_ID)"
  echo "Log: $LOG"
  "$PYTHON" -u - <<PY | tee -a "$LOG"
import logging
import sys
from pathlib import Path

ROOT = Path("$ROOT")
sys.path.insert(0, str(ROOT))

from src.stage03_train.embeddings_hub import (
    load_project_dotenv,
    try_download_from_hub,
    hub_relpath,
    get_hf_token,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("embed_download")
load_project_dotenv(ROOT)

cache = ROOT / "$CACHE_FILE"
repo = "RuthonField/romance-v2-train-eval-embeddings"
hub_path = hub_relpath("$HUB_RUN_ID", cache.name)

if cache.exists() and not Path(str(cache) + ".progress.json").exists():
    print(f"Cache already complete: {cache} ({cache.stat().st_size} bytes)")
    raise SystemExit(0)

if not get_hf_token():
    raise SystemExit("HF_TOKEN not set in .env — cannot download; use 'encode' instead.")

ok = try_download_from_hub(repo, hub_path, cache, logger=logger)
if ok:
    print(f"Download OK: {cache} ({cache.stat().st_size} bytes)")
else:
    print("Hub miss — run './scripts/stage03/run_v4_embed_local.sh $model encode' to build cache locally.")
    raise SystemExit(1)
PY
}

cmd_encode() {
  local model="$1"
  model_config "$model"
  require_csvs

  if [[ -f "$PID_FILE" ]]; then
    local old_pid
    old_pid=$(cat "$PID_FILE")
    if kill -0 "$old_pid" 2>/dev/null; then
      die "Encode already running (pid $old_pid). Use: $0 $model status | logs | eta-watch"
    fi
  fi

  if [[ -f "$ROOT/$CACHE_FILE" ]] && [[ ! -f "$ROOT/${CACHE_FILE}.progress.json" ]]; then
    echo "Cache already complete: $CACHE_FILE"
    "$ROOT/scripts/stage03/embed_v3_eta.sh" "$model" 2>/dev/null || true
    exit 0
  fi

  # Fresh encode needs ~NEED_GB free; resume reuses the already-allocated .npy.
  if [[ ! -f "$ROOT/$CACHE_FILE" ]]; then
    check_disk
  fi
  mkdir -p "$ROOT/logs"
  rm -f "$ROOT/logs/.embed_eta_${model}.state"

  echo "Starting GPU encode: $MODEL_NAME (batch=$ENCODE_BATCH device=$ENCODE_DEVICE)"
  echo "Log: $LOG"
  echo "ETA: $ROOT/scripts/stage03/embed_v3_eta.sh $model --watch"

  nohup "$PYTHON" -u -m src.stage03_train.cli encode \
    --train-csv data/raw/romance_subdataset_filtered_v3/sentences_train.csv \
    --val-csv data/raw/romance_subdataset_filtered_v3/sentences_val.csv \
    --model-name "$MODEL_NAME" \
    --cache-file "$CACHE_FILE" \
    --batch-size "$ENCODE_BATCH" \
    --device "$ENCODE_DEVICE" \
    >> "$LOG" 2>&1 &
  echo $! > "$PID_FILE"
  echo "Started pid $(cat "$PID_FILE")"
  sleep 3
  "$ROOT/scripts/stage03/embed_v3_eta.sh" "$model" || true
}

cmd_eta() {
  "$ROOT/scripts/stage03/embed_v3_eta.sh" "$1"
}

cmd_eta_watch() {
  "$ROOT/scripts/stage03/embed_v3_eta.sh" "$1" --watch
}

cmd_logs() {
  model_config "$1"
  tail -f "$LOG"
}

cmd_status() {
  local model="$1"
  model_config "$model"
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      echo "Encode running (pid $pid)"
    else
      echo "Encode not running (stale pid $pid)"
    fi
  else
    echo "Encode not running (no pid file)"
  fi
  "$ROOT/scripts/stage03/embed_v3_eta.sh" "$model" || true
}

tune_already_complete() {
  model_config "$1"
  [[ -f "$EXP_DIR/run_state.json" ]] || return 1
  "$PYTHON" - <<PY
import json
from pathlib import Path
state = json.loads(Path("$EXP_DIR/run_state.json").read_text())
trials = Path("$EXP_DIR/trials.csv")
raise SystemExit(0 if state.get("completed") and trials.exists() else 1)
PY
}

cmd_tune() {
  local model="$1"
  model_config "$model"

  if [[ -f "$TUNE_PID_FILE" ]]; then
    local old_pid
    old_pid=$(cat "$TUNE_PID_FILE")
    if kill -0 "$old_pid" 2>/dev/null; then
      die "Tuning already running (pid $old_pid). Use: $0 $model tune-status | tune-logs"
    fi
  fi

  if tune_already_complete "$model"; then
    echo "Tuning already complete for run-id $RUN_ID"
    cmd_tune_status "$model"
    exit 0
  fi

  if [[ ! -f "$ROOT/$CACHE_FILE" ]] || [[ -f "$ROOT/${CACHE_FILE}.progress.json" ]]; then
    die "Embedding cache not ready: $CACHE_FILE — run '$0 $model download' or '$0 $model encode' first"
  fi

  mkdir -p "$ROOT/logs"
  echo "Starting/resuming v4 Phase 1 BO: $MODEL_NAME"
  echo "Run-id: $RUN_ID"
  echo "Pipeline log: $TUNE_LOG"
  echo "Console log:  $CONSOLE_LOG"
  echo "State: $EXP_DIR/run_state.json"
  echo "Re-run '$0 $model tune' after any stop to resume from checkpoint."

  nohup "$PYTHON" -u -m src.stage03_train.cli tune \
    --config "$TRAIN_CONFIG" \
    --run-id "$RUN_ID" \
    --embedding-model "$MODEL_NAME" \
    >> "$CONSOLE_LOG" 2>&1 &
  echo $! > "$TUNE_PID_FILE"
  echo "Started pid $(cat "$TUNE_PID_FILE")"
  sleep 2
  cmd_tune_status "$model" || true
}

cmd_tune_status() {
  local model="$1"
  model_config "$model"

  if [[ -f "$TUNE_PID_FILE" ]]; then
    local pid
    pid=$(cat "$TUNE_PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      echo "Tuning running (pid $pid)"
    else
      echo "Tuning not running (stale pid $pid)"
    fi
  else
    echo "Tuning not running (no pid file)"
  fi

  "$PYTHON" - <<PY
import json
from pathlib import Path

exp = Path("$EXP_DIR")
state_path = exp / "run_state.json"
if not state_path.exists():
    print("No run_state.json yet.")
    raise SystemExit(0)

state = json.loads(state_path.read_text())
print(f"Run-id: {state.get('run_id')} completed={state.get('completed')}")

for name, step in state.get("steps", {}).items():
    print(f"  step {name}: {step.get('status')}")

for name, mstate in state.get("models", {}).items():
    details = mstate.get("details", {})
    bo = ""
    if "bo_calls_done" in details:
        bo = f" BO {details['bo_calls_done']}/{details.get('bo_calls_total', '?')}"
    print(f"  model {name}: {mstate.get('status')}{bo}")

for opt in sorted(exp.glob("opt_*")):
    partial = opt / "trials_partial.csv"
    if partial.exists():
        n = max(0, len(partial.read_text().strip().splitlines()) - 1)
        print(f"  {opt.name}: partial_trials={n}")
PY
}

cmd_tune_logs() {
  local model="$1"
  model_config "$model"
  tail -f "$TUNE_LOG"
}

usage() {
  cat <<EOF
Usage: $0 <l12|l6|mpnet> <command>

  download     Try HF Hub mirror (hub_run_id in train_v4_* yaml)
  encode       Start/resume full-corpus embeddings (background, GPU)
  eta / eta-watch / logs / status   — encode progress
  tune         Start/resume v4 Phase 1 BO (background)
  tune-status / tune-logs           — BO progress
EOF
}

main() {
  [[ $# -ge 2 ]] || { usage; exit 1; }
  case "$2" in
    download) cmd_download "$1" ;;
    encode) cmd_encode "$1" ;;
    eta) cmd_eta "$1" ;;
    eta-watch) cmd_eta_watch "$1" ;;
    logs) cmd_logs "$1" ;;
    status) cmd_status "$1" ;;
    tune) cmd_tune "$1" ;;
    tune-status) cmd_tune_status "$1" ;;
    tune-logs) cmd_tune_logs "$1" ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"
