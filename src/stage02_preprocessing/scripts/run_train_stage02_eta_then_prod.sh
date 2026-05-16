#!/usr/bin/env bash
# Sequential on single GPU: finish ETA sample only (use wait_eta_then_stoplist_sample.sh for production).
set -euo pipefail
cd "$(dirname "$0")/../../.."
PY=".venv/bin/python"
TXT="data/interim/booknlp_character_runs/train_stage02_eta50/txt_input"
SHARDS="data/interim/booknlp_character_runs/train_stage02_shards4/shards"
LOGDIR="logs"
mkdir -p "$LOGDIR"

echo "[$(date -Is)] Starting ETA sample (50 books, resume) ..."
$PY -m src.stage02_preprocessing.extract_character_names_booknlp \
  --config configs/paths.yaml \
  --run-id train_stage02_eta50 \
  --estimate-eta \
  --eta-sample-books 50 \
  --eta-seed 42 \
  --eta-resume \
  --txt-input-dir "$TXT" \
  --no-merge-stoplist \
  2>&1 | tee -a "$LOGDIR/train_stage02_eta50_resume.log"

echo "[$(date -Is)] ETA complete. For stoplist production use:"
echo "  bash src/stage02_preprocessing/scripts/wait_eta_then_stoplist_sample.sh 1500 2"
