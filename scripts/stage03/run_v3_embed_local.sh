#!/usr/bin/env bash
# Run v3 embedding encode + Stage03 BO tuning locally (.venv, no Docker).
#
# Both encode and tune are resumable: re-run the same command with the same run-id.
# Checkpoints: .npy.progress.json (encode), run_state.json + result.json (tune).
#
# Usage:
#   ./scripts/stage03/run_v3_embed_local.sh minilm6 encode
#   ./scripts/stage03/run_v3_embed_local.sh minilm6 tune          # start or resume BO
#   ./scripts/stage03/run_v3_embed_local.sh minilm6 tune-status
#   ./scripts/stage03/run_v3_embed_local.sh minilm6 tune-logs
#   ./scripts/stage03/run_v3_embed_local.sh minilm6 eta-watch
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
    minilm6)
      MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
      RUN_ID="v3_minilm6_first"
      TRAIN_CONFIG="configs/stage03/train_v3_minilm6.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy"
      ENCODE_BATCH=256
      LOG="$ROOT/logs/v3_embeddings_minilm6.log"
      PID_FILE="$ROOT/logs/v3_embeddings_minilm6.pid"
      TUNE_LOG="$ROOT/logs/stage03_${RUN_ID}.log"
      TUNE_PID_FILE="$ROOT/logs/stage03_${RUN_ID}.pid"
      EXP_DIR="$ROOT/results/experiments/${RUN_ID}"
      ;;
    mpnet)
      MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
      RUN_ID="v3_mpnet_first"
      TRAIN_CONFIG="configs/stage03/train_v3_mpnet.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy"
      ENCODE_BATCH=128
      LOG="$ROOT/logs/v3_embeddings_mpnet.log"
      PID_FILE="$ROOT/logs/v3_embeddings_mpnet.pid"
      TUNE_LOG="$ROOT/logs/stage03_${RUN_ID}.log"
      TUNE_PID_FILE="$ROOT/logs/stage03_${RUN_ID}.pid"
      EXP_DIR="$ROOT/results/experiments/${RUN_ID}"
      ;;
    *)
      die "Unknown model '$1'. Use: minilm6 | mpnet"
      ;;
  esac
}

require_csvs() {
  local base="data/raw/romance_subdataset_filtered_v3"
  for f in sentences_train.csv sentences_val.csv; do
    [[ -f "$base/$f" ]] || die "Missing $base/$f"
  done
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
    "$ROOT/scripts/stage03/embed_v3_eta.sh" "$model"
    exit 0
  fi

  mkdir -p "$ROOT/logs"
  rm -f "$ROOT/logs/.embed_eta_${model}.state"

  echo "Starting local encode: $MODEL_NAME"
  echo "Log: $LOG"
  echo "Batch size: $ENCODE_BATCH (no Hugging Face Hub)"
  echo "ETA: $ROOT/scripts/stage03/embed_v3_eta.sh $model --watch"

  nohup "$PYTHON" -u - <<PY >> "$LOG" 2>&1 &
import logging
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("$ROOT")
sys.path.insert(0, str(ROOT))

from src.stage03_train.embeddings import compute_embeddings_from_csvs

def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("embed")

log("v3 embedding job start")
log(f"Model: $MODEL_NAME")
log(f"Train CSV: data/raw/romance_subdataset_filtered_v3/sentences_train.csv")
log(f"Val CSV: data/raw/romance_subdataset_filtered_v3/sentences_val.csv")
log(f"Output: $CACHE_FILE")

cache_file = ROOT / "$CACHE_FILE"
cache_file.parent.mkdir(parents=True, exist_ok=True)

compute_embeddings_from_csvs(
    ROOT / "data/raw/romance_subdataset_filtered_v3/sentences_train.csv",
    ROOT / "data/raw/romance_subdataset_filtered_v3/sentences_val.csv",
    model_name="$MODEL_NAME",
    cache_file=cache_file,
    batch_size=$ENCODE_BATCH,
    logger=logger,
)
log(f"Done: {cache_file}")
PY
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
  "$ROOT/scripts/stage03/embed_v3_eta.sh" "$model"
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
    die "Embedding cache not ready: $CACHE_FILE — run '$0 $model encode' first"
  fi

  mkdir -p "$ROOT/logs"
  echo "Starting/resuming BO tuning: $MODEL_NAME"
  echo "Run-id: $RUN_ID (same id required for resume)"
  echo "Log: $TUNE_LOG"
  echo "State: $EXP_DIR/run_state.json"
  echo "Re-run '$0 $model tune' after any stop to continue from checkpoint."

  # Pipeline logger writes to TUNE_LOG; avoid duplicate lines via shell redirect.
  nohup "$PYTHON" -m src.stage03_train.cli tune \
    --config "$TRAIN_CONFIG" \
    --run-id "$RUN_ID" \
    --embedding-model "$MODEL_NAME" \
    > /dev/null 2>&1 &
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

steps = state.get("steps", {})
for name, step in steps.items():
    print(f"  step {name}: {step.get('status')}")

models = state.get("models", {})
for name, mstate in models.items():
    details = mstate.get("details", {})
    bo = ""
    if "bo_calls_done" in details:
        bo = f" BO {details['bo_calls_done']}/{details.get('bo_calls_total', '?')}"
    print(f"  model {name}: {mstate.get('status')}{bo}")

opt_dirs = sorted(exp.glob("opt_*"))
for opt in opt_dirs:
    partial = opt / "trials_partial.csv"
    result = opt / "result.json"
    if partial.exists():
        lines = partial.read_text().strip().splitlines()
        n = max(0, len(lines) - 1)
        print(f"  {opt.name}: partial_trials={n} result_json={'yes' if result.exists() else 'no'}")
    elif result.exists():
        print(f"  {opt.name}: result_json=yes")

trials = exp / "trials.csv"
if trials.exists():
    lines = trials.read_text().strip().splitlines()
    print(f"  trials.csv: {max(0, len(lines) - 1)} row(s)")
PY
}

cmd_tune_logs() {
  local model="$1"
  model_config "$model"
  tail -f "$TUNE_LOG"
}

usage() {
  cat <<EOF
Usage: $0 <model> <command>

Models: minilm6 | mpnet

Encode:
  encode       Start/resume full-corpus embeddings (background)
  eta          One-line embed progress + ETA
  eta-watch    Refresh embed ETA every 60s
  logs         tail -f encode log
  status       embed pid + ETA snapshot

Tune (resumable — re-run 'tune' with the same run-id):
  tune         Start/resume Stage03 BO tuning (background)
  tune-status  pid + run_state / BO checkpoint summary
  tune-logs    tail -f tuning log
EOF
}

main() {
  [[ $# -ge 2 ]] || { usage; exit 1; }
  case "$2" in
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
