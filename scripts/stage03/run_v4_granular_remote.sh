#!/usr/bin/env bash
# Run v4 granular Stage03 BO in Docker (foreground, resumable).
# Expects a local MPNet/L6/L12 embedding cache — no HF Hub, no encode step.
#
# Usage (from transfer_bundle root):
#   docker build -t romance-stage03:latest .
#   ./scripts/stage03/run_v4_granular_remote.sh mpnet phase1   # coarse BO (160 calls)
#   ./scripts/stage03/run_v4_granular_remote.sh mpnet phase3   # narrowed BO (100 calls, after Phase 2)
#
# BO uses RAPIDS cuML and requires a GPU. Set USE_GPU=0 only for smoke/debug (will fail on full runs).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

IMAGE="${IMAGE:-romance-stage03:latest}"
USE_GPU="${USE_GPU:-1}"

die() {
  echo "ERROR: $*" >&2
  exit 1
}

require_tune_data() {
  local cache_file="$1"
  local base="data/raw/romance_subdataset_filtered_v3"
  local octis="data/interim/octis/v3_english_only"
  local samples="data/stage03_samples_v3"

  [[ -f "$cache_file" ]] || die "Missing embedding cache: $cache_file"
  [[ -f "$octis/corpus.tsv" ]] || die "Missing $octis/corpus.tsv (bundled or copy manually)"
  [[ -f "$octis/corpus.offsets.npy" ]] || die "Missing $octis/corpus.offsets.npy"
  [[ -f "$samples/fit_indices_seed42.npy" ]] || die "Missing $samples/fit_indices_seed42.npy"
  [[ -f "$samples/eval_indices_seed42.npy" ]] || die "Missing $samples/eval_indices_seed42.npy"
  for f in sentences_train.csv sentences_val.csv; do
    [[ -f "$base/$f" ]] || die "Missing $base/$f — val/train CSVs needed for coherence eval"
  done
}

DOCKER_RUN_ARGS=(
  -v "$ROOT/data:/app/data"
  -v "$ROOT/results:/app/results"
  -v "$ROOT/logs:/app/logs"
  -v "$ROOT/models:/app/models"
)

GPU_ARGS=()
if [[ "$USE_GPU" == "1" ]]; then
  GPU_ARGS=(--gpus all)
  DOCKER_RUN_ARGS+=(
    -e "NVIDIA_VISIBLE_DEVICES=all"
    -e "NVIDIA_DRIVER_CAPABILITIES=compute,utility"
  )
else
  DOCKER_RUN_ARGS+=(-e "CUDA_VISIBLE_DEVICES=")
fi

docker_run() {
  local tty_args=()
  if [[ -t 1 ]]; then
    tty_args=(-it)
  fi
  docker run --rm "${tty_args[@]}" "${GPU_ARGS[@]}" "${DOCKER_RUN_ARGS[@]}" "$IMAGE" "$@"
}

model_phase_config() {
  case "$1:$2" in
    l12:phase1)
      MODEL_NAME="sentence-transformers/all-MiniLM-L12-v2"
      RUN_ID="v4_l12_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_l12_granular_phase1.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__all-MiniLM-L12-v2.npy"
      ;;
    l12:phase3)
      MODEL_NAME="sentence-transformers/all-MiniLM-L12-v2"
      RUN_ID="v4_l12_granular_phase3"
      TRAIN_CONFIG="configs/stage03/train_v4_l12_granular_phase3.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__all-MiniLM-L12-v2.npy"
      ;;
    l6:phase1)
      MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
      RUN_ID="v4_l6_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_l6_granular_phase1.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy"
      ;;
    l6:phase3)
      MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
      RUN_ID="v4_l6_granular_phase3"
      TRAIN_CONFIG="configs/stage03/train_v4_l6_granular_phase3.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy"
      ;;
    mpnet:phase1)
      MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
      RUN_ID="v4_mpnet_granular_phase1"
      TRAIN_CONFIG="configs/stage03/train_v4_mpnet_granular_phase1.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy"
      ;;
    mpnet:phase3)
      MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
      RUN_ID="v4_mpnet_granular_phase3"
      TRAIN_CONFIG="configs/stage03/train_v4_mpnet_granular_phase3.yaml"
      CACHE_FILE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy"
      ;;
    *)
      die "Unknown model/phase '$1 $2'. Use: mpnet|l6|l12 with phase1|phase3"
      ;;
  esac
}

cmd_tune() {
  local model="$1"
  local phase="$2"
  model_phase_config "$model" "$phase"
  require_tune_data "$CACHE_FILE"

  if [[ "$USE_GPU" == "1" ]]; then
    echo "v4 granular BO ($phase): $MODEL_NAME (run-id: $RUN_ID, GPU enabled)"
  else
    echo "WARNING: USE_GPU=0 — full BO will fail without cuML/CUDA"
    echo "v4 granular BO ($phase): $MODEL_NAME (run-id: $RUN_ID, CPU forced)"
  fi
  echo "config: $TRAIN_CONFIG"
  echo "Press Ctrl+C to stop; re-run to resume from checkpoint."
  docker_run python3 -m src.stage03_train.cli tune \
    --config "$TRAIN_CONFIG" \
    --run-id "$RUN_ID" \
    --embedding-model "$MODEL_NAME"
}

usage() {
  cat <<EOF
Usage: $0 <model> <phase>

Models:  mpnet | l6 | l12
Phases:  phase1 (coarse BO) | phase3 (narrowed BO after Phase 2 review)

Examples:
  $0 mpnet phase1
  $0 mpnet phase3

Requires local embedding cache, OCTIS corpus, fit/eval indices, and train+val CSVs.
BO tuning needs a GPU (cuML). Encode is not run by this script.

Environment:
  USE_GPU=1   pass --gpus all to Docker (default)
  IMAGE       Docker image tag (default: romance-stage03:latest)
EOF
}

main() {
  [[ $# -ge 2 ]] || { usage; exit 1; }
  case "$1" in
    -h|--help) usage ;;
    mpnet|l6|l12)
      case "$2" in
        phase1|phase3) cmd_tune "$1" "$2" ;;
        *) die "Unknown phase '$2'. Use: phase1 | phase3" ;;
      esac
      ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"
