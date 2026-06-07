#!/usr/bin/env bash
# Assemble a self-contained transfer bundle for shipping Stage03 to another GPU machine.
#
# The bundle is a single folder you can rsync to a flash drive and unpack on a
# second NVIDIA/CUDA box. It carries the full Docker build context (Dockerfile,
# compose file, requirements, app code, configs) plus a data/ skeleton with small
# artifacts already filled in and drop folders for large files (.csv, corpus, .npy).
#
# Regenerate any time the code/config/Dockerfile changes:
#   bash scripts/make_transfer_bundle.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE="${1:-$ROOT/transfer_bundle}"
DOCKER_DIR="$ROOT/docker"

echo "Assembling transfer bundle at: $BUNDLE"
rm -rf "$BUNDLE"
mkdir -p "$BUNDLE"

# Docker build files from docker/ (build context root = bundle root).
cp "$DOCKER_DIR/Dockerfile" "$BUNDLE/"
cp "$DOCKER_DIR/docker-compose.yml" "$BUNDLE/"
cp "$ROOT/.dockerignore" "$BUNDLE/"
cp "$DOCKER_DIR/.env.example" "$BUNDLE/"

# The runbook becomes the bundle README and is also copied into the image
# (Dockerfile: `COPY README.md ./`).
cp "$DOCKER_DIR/README.md" "$BUNDLE/README.md"

# Python build context referenced by the Dockerfile.
cp "$ROOT/requirements.txt" "$BUNDLE/"
cp "$ROOT/requirements-venv.txt" "$BUNDLE/"
cp "$ROOT/Makefile" "$BUNDLE/"

# Application code + configs (exclude caches so the bundle stays small).
rsync -a --delete \
  --exclude '__pycache__' \
  --exclude '*.py[cod]' \
  "$ROOT/src/" "$BUNDLE/src/"
rsync -a --delete "$ROOT/configs/" "$BUNDLE/configs/"

# ---------------------------------------------------------------------------
# Data payload skeleton (small files copied; large files = drop folders)
# ---------------------------------------------------------------------------
DATA="$BUNDLE/data"
SENTENCES_DIR="$DATA/processed/romance_subdataset_downloaded_v2_sentences"
METADATA_DIR="$DATA/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata"
SAMPLES_DIR="$DATA/stage03_samples"
OCTIS_BASE="$DATA/interim/octis"
OCTIS_SHARED="$OCTIS_BASE/minilm12v2_first"
OCTIS_MPNET="$OCTIS_BASE/mpnet_first/embeddings_cache"
OCTIS_MINILM6="$OCTIS_BASE/minilm6_first/embeddings_cache"
OCTIS_MINILM12_CACHE="$OCTIS_SHARED/embeddings_cache"

mkdir -p "$SENTENCES_DIR" "$METADATA_DIR" "$SAMPLES_DIR" \
  "$OCTIS_SHARED" "$OCTIS_MPNET" "$OCTIS_MINILM6" "$OCTIS_MINILM12_CACHE"
mkdir -p "$BUNDLE/results" "$BUNDLE/logs" "$BUNDLE/models"
touch "$BUNDLE/results/.gitkeep" "$BUNDLE/logs/.gitkeep" "$BUNDLE/models/.gitkeep"

# Small artifacts that ship inside the bundle (~10 MB total).
copy_if_exists() {
  local src="$1"
  local dest="$2"
  if [[ -f "$src" ]]; then
    cp "$src" "$dest"
    echo "  copied $(basename "$src")"
  else
    echo "  WARN: missing $src (skipped)"
  fi
}

echo "Copying small data artifacts..."
copy_if_exists "$ROOT/data/processed/custom_stoplist.txt" "$DATA/processed/custom_stoplist.txt"
for f in romance_subdataset_downloaded_v2_train.csv \
         romance_subdataset_downloaded_v2_val.csv \
         romance_subdataset_downloaded_v2_test.csv \
         romance_subdataset_downloaded_v2_manifest.json; do
  copy_if_exists "$ROOT/data/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata/$f" "$METADATA_DIR/$f"
done
copy_if_exists "$ROOT/data/stage03_samples/fit_indices_seed42.npy" "$SAMPLES_DIR/fit_indices_seed42.npy"
copy_if_exists "$ROOT/data/stage03_samples/eval_indices_seed42.npy" "$SAMPLES_DIR/eval_indices_seed42.npy"
copy_if_exists "$ROOT/data/stage03_samples/sample_manifest_seed42.json" "$SAMPLES_DIR/sample_manifest_seed42.json"
copy_if_exists "$ROOT/data/interim/octis/minilm12v2_first/metadata.json" "$OCTIS_SHARED/metadata.json"

# README files for large payloads and .npy drop zones.
cat > "$DATA/README.md" <<'EOF'
# Stage03 data payload

This tree mirrors the repo `data/` layout expected by `configs/paths_stage03_fit.yaml`
and `configs/train.yaml`. Small files are pre-filled by `scripts/make_transfer_bundle.sh`;
copy the large files listed below before starting Docker.

## Checklist (copy from source machine or flash drive)

| Priority | Path | Size (approx.) | Notes |
|----------|------|----------------|-------|
| **Required** | `processed/romance_subdataset_downloaded_v2_sentences/sentences_train.csv` | ~6.5 GB | Full train split |
| **Required** | `processed/romance_subdataset_downloaded_v2_sentences/sentences_val.csv` | ~1.3 GB | Full eval split |
| **Required** | `processed/romance_subdataset_downloaded_v2_sentences/sentences_test.csv` | ~1.5 GB | Held-out test (stage05b) |
| **Recommended** | `interim/octis/minilm12v2_first/corpus.tsv` | ~7.5 GB | Skips ~100M-row corpus rewrite |
| **Recommended** | `interim/octis/minilm12v2_first/corpus.offsets.npy` | ~760 MB | Required with corpus.tsv |
| **Per model** | `interim/octis/<run_id>/embeddings_cache/train_eval_*.npy` | ~50–143 GB | See drop-folder READMEs |

Already included in the bundle (no action needed):

- `processed/custom_stoplist.txt`
- `raw/.../subsampling_metadata/*.csv` (book metadata for the sampler)
- `stage03_samples/fit_indices_seed42.npy`, `eval_indices_seed42.npy`, `sample_manifest_seed42.json`
- `interim/octis/minilm12v2_first/metadata.json`

## Embedding model → run-id → .npy filename

All three full-corpus caches share the same train→eval row order. Point
`configs/train.yaml` → `embeddings_cache.overrides` at the file you place:

| Embedding model | `--run-id` | Drop folder | Exact `.npy` filename |
|-----------------|------------|-------------|------------------------|
| `sentence-transformers/all-MiniLM-L12-v2` | `minilm12v2_first` | `interim/octis/minilm12v2_first/embeddings_cache/` | `train_eval_sentence-transformers__all-MiniLM-L12-v2.npy` |
| `sentence-transformers/paraphrase-mpnet-base-v2` | `mpnet_first` | `interim/octis/mpnet_first/embeddings_cache/` | `train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy` |
| `sentence-transformers/paraphrase-MiniLM-L6-v2` | `minilm6_first` | `interim/octis/minilm6_first/embeddings_cache/` | `train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy` |

Expected shape: `(99823824, <dim>)` float32 — 82,114,042 train rows + 17,709,782 val rows.

## Quick verify on target machine

```bash
python3 - <<'PY'
from pathlib import Path
import numpy as np
root = Path("data")
for p in [
    root / "stage03_samples/fit_indices_seed42.npy",
    root / "stage03_samples/eval_indices_seed42.npy",
    root / "interim/octis/minilm12v2_first/metadata.json",
]:
    print("OK" if p.exists() else "MISSING", p)
npy = root / "interim/octis/mpnet_first/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy"
if npy.exists():
    a = np.load(npy, mmap_mode="r")
    print("mpnet npy shape", a.shape)
PY
```

See also `README.md` (Docker runbook) at the bundle root.
EOF

cat > "$SENTENCES_DIR/README.md" <<'EOF'
# Sentence CSVs (required, large)

Copy these three files from the source machine:

- `sentences_train.csv` (~6.5 GB)
- `sentences_val.csv` (~1.3 GB)
- `sentences_test.csv` (~1.5 GB)

Schema: `work_id, chapter_index, chapter_title, sentence_index, sentence`

These must match the corpus the embedding `.npy` caches were built from.
EOF

cat > "$OCTIS_SHARED/README.md" <<'EOF'
# Shared OCTIS full corpus (recommended)

Copy to skip rebuilding `corpus.tsv` (~10 min saved on startup):

- `corpus.tsv` (~7.5 GB)
- `corpus.offsets.npy` (~760 MB)
- `metadata.json` (already in bundle)

`configs/paths_stage03_fit.yaml` points `octis_corpus_dir` here. This corpus is
**embedding-model-agnostic** — all three models reuse the same files.
EOF

cat > "$OCTIS_MPNET/README.md" <<'EOF'
# Drop folder: MPNet full-corpus embeddings

**Model:** `sentence-transformers/paraphrase-mpnet-base-v2`  
**Run id:** `mpnet_first`  
**Place your ready file here (exact name):**

```
train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy
```

Expected: float32 array shape `(99823824, 768)`.

Configured in `configs/train.yaml` → `embeddings_cache.overrides`.
EOF

cat > "$OCTIS_MINILM6/README.md" <<'EOF'
# Drop folder: MiniLM-L6 full-corpus embeddings

**Model:** `sentence-transformers/paraphrase-MiniLM-L6-v2`  
**Run id:** `minilm6_first`  
**Place your ready file here (exact name):**

```
train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy
```

Expected: float32 array shape `(99823824, 384)`.

Configured in `configs/train.yaml` → `embeddings_cache.overrides`.
EOF

cat > "$OCTIS_MINILM12_CACHE/README.md" <<'EOF'
# Drop folder: MiniLM-L12 full-corpus embeddings (optional on this machine)

**Model:** `sentence-transformers/all-MiniLM-L12-v2`  
**Run id:** `minilm12v2_first`  
**Place your ready file here (exact name):**

```
train_eval_sentence-transformers__all-MiniLM-L12-v2.npy
```

Expected: float32 array shape `(99823824, 384)`.

Only needed if this laptop runs the MiniLM-L12 model. MPNet / MiniLM-L6 laptops
can ignore this folder.
EOF

# Touch drop-folder markers so empty dirs survive rsync/tar.
touch "$OCTIS_MPNET/.keep"
touch "$OCTIS_MINILM6/.keep"
touch "$OCTIS_MINILM12_CACHE/.keep"
touch "$SENTENCES_DIR/.keep"

echo
echo "Done. Bundle contents:"
find "$BUNDLE" -maxdepth 1 -mindepth 1 -printf '  %f\n' | sort
echo
echo "Data skeleton:"
find "$BUNDLE/data" -type f | sort | sed 's|^|  |'
echo
echo "Bundle size: $(du -sh "$BUNDLE" | cut -f1)"
echo
echo "Next steps:"
echo "  1. Copy large CSVs into data/processed/romance_subdataset_downloaded_v2_sentences/"
echo "  2. Copy corpus.tsv + corpus.offsets.npy into data/interim/octis/minilm12v2_first/ (optional)"
echo "  3. Drop your .npy files into data/interim/octis/mpnet_first/embeddings_cache/"
echo "     and data/interim/octis/minilm6_first/embeddings_cache/"
echo "  4. cp .env.example .env && set HF_TOKEN"
echo "  5. Follow README.md inside the bundle"
