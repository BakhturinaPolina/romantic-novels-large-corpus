#!/usr/bin/env bash
# Precompute test-split sentence embeddings (CUDA, resumable).
#
# Usage:
#   ./scripts/stage03/encode_v3_test_embeddings.sh
#   ENCODE_DEVICE=cuda ENCODE_BATCH_SIZE=512 ./scripts/stage03/encode_v3_test_embeddings.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

MODEL_NAME="${MODEL_NAME:-sentence-transformers/all-MiniLM-L12-v2}"
TEST_CSV="${TEST_CSV:-data/raw/romance_subdataset_filtered_v3/sentences_test.csv}"
CACHE_FILE="${CACHE_FILE:-data/interim/octis/v3_english_only/embeddings_cache/test_sentence-transformers__all-MiniLM-L12-v2.npy}"
ENCODE_DEVICE="${ENCODE_DEVICE:-cuda}"
ENCODE_BATCH_SIZE="${ENCODE_BATCH_SIZE:-512}"
CHUNK_SIZE="${CHUNK_SIZE:-50000}"

echo "Encoding test split -> $CACHE_FILE (device=$ENCODE_DEVICE batch=$ENCODE_BATCH_SIZE)"
"$PY" -m src.stage03_train.cli encode-split \
  --csv "$TEST_CSV" \
  --model-name "$MODEL_NAME" \
  --cache-file "$CACHE_FILE" \
  --device "$ENCODE_DEVICE" \
  --batch-size "$ENCODE_BATCH_SIZE" \
  --chunk-size "$CHUNK_SIZE"
