#!/usr/bin/env bash
# Run Stage03 v3 embedding + tuning in Docker on a remote Linux machine (CPU-only).
# No sudo required — only Docker Engine (no GPU or nvidia-container-toolkit).
# All jobs run in the foreground (Ctrl+C to stop). Re-run the same command to resume from disk.
#
# Usage (from transfer_bundle root):
#   docker build -t romance-stage03:latest .
#   ./scripts/run_v3_remote_model.sh sample          # once, after CSVs are in place
#   ./scripts/run_v3_remote_model.sh mpnet encode    # CPU encode, resumable (slow)
#   ./scripts/run_v3_remote_model.sh mpnet tune      # after encode finishes (needs GPU for cuML)
#   ./scripts/run_v3_remote_model.sh minilm6 encode
#   ./scripts/run_v3_remote_model.sh minilm6 tune
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

IMAGE="${IMAGE:-romance-stage03:latest}"
DEVICE="${DEVICE:-cpu}"

die() {
  echo "ERROR: $*" >&2
  exit 1
}

require_csvs() {
  local base="data/raw/romance_subdataset_filtered_v3"
  for f in sentences_train.csv sentences_val.csv; do
    [[ -f "$base/$f" ]] || die "Missing $base/$f — copy v3 sentence CSVs manually (see README.md)"
  done
}

DOCKER_RUN_ARGS=(
  -e "CUDA_VISIBLE_DEVICES="
  -e "DEVICE=${DEVICE}"
  -v "$ROOT/data:/app/data"
  -v "$ROOT/results:/app/results"
  -v "$ROOT/logs:/app/logs"
  -v "$ROOT/models:/app/models"
)

docker_run() {
  local tty_args=()
  if [[ -t 1 ]]; then
    tty_args=(-it)
  fi
  docker run --rm "${tty_args[@]}" "${DOCKER_RUN_ARGS[@]}" "$IMAGE" "$@"
}

model_config() {
  case "$1" in
    mpnet)
      MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
      RUN_ID="v3_mpnet_first"
      TRAIN_CONFIG="configs/train_v3_mpnet.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy"
      ENCODE_BATCH=128
      ;;
    minilm6)
      MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
      RUN_ID="v3_minilm6_first"
      TRAIN_CONFIG="configs/train_v3_minilm6.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy"
      ENCODE_BATCH=256
      ;;
    *)
      die "Unknown model '$1'. Use: mpnet | minilm6"
      ;;
  esac
}

cmd_sample() {
  require_csvs
  echo "Generating v3 stratified fit/eval indices..."
  docker_run python3 -m src.stage03_train.cli sample \
    --train-csv data/raw/romance_subdataset_filtered_v3/sentences_train.csv \
    --val-csv data/raw/romance_subdataset_filtered_v3/sentences_val.csv \
    --metadata-train data/raw/romance_subdataset_filtered_v3/subsampling_metadata/romance_subdataset_filtered_v3_train.csv \
    --metadata-val data/raw/romance_subdataset_filtered_v3/subsampling_metadata/romance_subdataset_filtered_v3_val.csv \
    --out-dir data/stage03_samples_v3 --train-target 500000 --val-target 100000 --seed 42
  echo "Done. Indices written to data/stage03_samples_v3/"
}

cmd_encode() {
  local model="$1"
  model_config "$model"
  require_csvs
  echo "CPU encode for $MODEL_NAME (batch=$ENCODE_BATCH, device=$DEVICE)"
  echo "Press Ctrl+C to stop; re-run this command to resume from disk."
  docker_run python3 -m src.stage03_train.cli encode \
    --train-csv data/raw/romance_subdataset_filtered_v3/sentences_train.csv \
    --val-csv data/raw/romance_subdataset_filtered_v3/sentences_val.csv \
    --model-name "$MODEL_NAME" \
    --cache-file "$CACHE_FILE" \
    --batch-size "$ENCODE_BATCH" \
    --device "$DEVICE"
}

cmd_tune() {
  local model="$1"
  model_config "$model"
  echo "BO tuning for $MODEL_NAME (run-id: $RUN_ID)"
  echo "Press Ctrl+C to stop; re-run this command to resume from disk."
  docker_run python3 -m src.stage03_train.cli tune \
    --config "$TRAIN_CONFIG" \
    --run-id "$RUN_ID" \
    --embedding-model "$MODEL_NAME"
}

usage() {
  cat <<EOF
Usage: $0 <command> [model]

Commands:
  sample              Generate v3 fit/eval indices (run once after CSVs are copied)
  <model> encode      Full-corpus embedding encode (foreground, resumable)
  <model> tune        Bayesian optimization tuning (foreground, resumable)

Models: mpnet | minilm6

All jobs run attached to the terminal. Ctrl+C stops the container; re-run the
same command to continue from checkpoint files on disk.

Examples:
  $0 sample
  $0 mpnet encode
  $0 mpnet tune
  $0 minilm6 encode
EOF
}

main() {
  [[ $# -ge 1 ]] || { usage; exit 1; }

  case "$1" in
    sample) cmd_sample ;;
    mpnet|minilm6)
      [[ $# -ge 2 ]] || die "Missing subcommand for $1. Use: encode | tune"
      case "$2" in
        encode) cmd_encode "$1" ;;
        tune)   cmd_tune "$1" ;;
        *) die "Unknown subcommand '$2'. Use: encode | tune" ;;
      esac
      ;;
    -h|--help) usage ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"
