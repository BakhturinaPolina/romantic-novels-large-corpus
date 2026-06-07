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
# v3 English-only filtered corpus (primary)
SENTENCES_V3_DIR="$DATA/raw/romance_subdataset_filtered_v3"
METADATA_V3_DIR="$DATA/raw/romance_subdataset_filtered_v3/subsampling_metadata"
# v2 legacy paths (optional fallback)
SENTENCES_DIR="$DATA/processed/romance_subdataset_downloaded_v2_sentences"
METADATA_DIR="$DATA/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata"
SAMPLES_DIR="$DATA/stage03_samples"
OCTIS_BASE="$DATA/interim/octis"
OCTIS_V3="$OCTIS_BASE/v3_english_only"
OCTIS_SHARED="$OCTIS_BASE/minilm12v2_first"
OCTIS_MPNET="$OCTIS_BASE/mpnet_first/embeddings_cache"
OCTIS_MINILM6="$OCTIS_BASE/minilm6_first/embeddings_cache"
OCTIS_MINILM12_CACHE="$OCTIS_SHARED/embeddings_cache"

mkdir -p "$SENTENCES_V3_DIR" "$METADATA_V3_DIR" "$SENTENCES_DIR" "$METADATA_DIR" "$SAMPLES_DIR" \
  "$OCTIS_V3" "$OCTIS_SHARED" "$OCTIS_MPNET" "$OCTIS_MINILM6" "$OCTIS_MINILM12_CACHE"
mkdir -p "$BUNDLE/results" "$BUNDLE/logs" "$BUNDLE/models" "$BUNDLE/scripts"
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

# v3 metadata (English-only filtered)
copy_if_exists "$ROOT/data/raw/romance_subdataset_filtered_v3/v3_filtering_manifest.json" "$SENTENCES_V3_DIR/v3_filtering_manifest.json"
copy_if_exists "$ROOT/data/raw/romance_subdataset_filtered_v3/language_analysis.csv" "$SENTENCES_V3_DIR/language_analysis.csv"
for f in romance_subdataset_filtered_v3_train.csv \
         romance_subdataset_filtered_v3_val.csv \
         romance_subdataset_filtered_v3_test.csv \
         romance_subdataset_filtered_v3_full.csv; do
  copy_if_exists "$ROOT/data/raw/romance_subdataset_filtered_v3/subsampling_metadata/$f" "$METADATA_V3_DIR/$f"
done

# v2 legacy metadata (fallback)
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

# v3 OCTIS corpus (pre-built, saves ~15 min on target machine)
echo "Copying v3 OCTIS corpus (~8 GB)..."
copy_if_exists "$ROOT/data/interim/octis/v3_english_only/corpus.tsv" "$OCTIS_V3/corpus.tsv"
copy_if_exists "$ROOT/data/interim/octis/v3_english_only/corpus.offsets.npy" "$OCTIS_V3/corpus.offsets.npy"
copy_if_exists "$ROOT/data/interim/octis/v3_english_only/metadata.json" "$OCTIS_V3/metadata.json"

# README files for large payloads and .npy drop zones.
cat > "$DATA/README.md" <<'EOF'
# Stage03 data payload

This tree mirrors the repo `data/` layout expected by `configs/paths_stage03_fit.yaml`
and `configs/train.yaml`. Small files are pre-filled by `scripts/make_transfer_bundle.sh`;
copy the large files listed below before starting Docker.

## v3 English-Only Corpus (Recommended)

The v3 corpus has 460 non-English books removed (2.8% of corpus). Use v3 for cleaner topics.

| Priority | Path | Size (approx.) | Notes |
|----------|------|----------------|-------|
| **Required** | `raw/romance_subdataset_filtered_v3/sentences_train.csv` | ~6.3 GB | v3 English-only train |
| **Required** | `raw/romance_subdataset_filtered_v3/sentences_val.csv` | ~1.4 GB | v3 English-only eval |
| **Required** | `raw/romance_subdataset_filtered_v3/sentences_test.csv` | ~1.4 GB | v3 English-only test |

## Legacy v2 Corpus (Alternative)

| Priority | Path | Size (approx.) | Notes |
|----------|------|----------------|-------|
| Alternative | `processed/romance_subdataset_downloaded_v2_sentences/sentences_train.csv` | ~6.5 GB | v2 train (has non-English) |
| Alternative | `processed/romance_subdataset_downloaded_v2_sentences/sentences_val.csv` | ~1.3 GB | v2 eval |
| Alternative | `processed/romance_subdataset_downloaded_v2_sentences/sentences_test.csv` | ~1.5 GB | v2 test |

## OCTIS Corpus & Embeddings

| Priority | Path | Size (approx.) | Notes |
|----------|------|----------------|-------|
| **Included** | `interim/octis/v3_english_only/corpus.tsv` | 7.3 GB | Pre-built v3 corpus |
| **Included** | `interim/octis/v3_english_only/corpus.offsets.npy` | 744 MB | Byte offsets index |
| **Build on target** | `interim/octis/v3_english_only/embeddings_cache/*.npy` | ~50-140 GB | ~4 days to compute |
| Legacy | `interim/octis/minilm12v2_first/corpus.tsv` | ~7.5 GB | v2 corpus (optional) |
| Legacy | `interim/octis/minilm12v2_first/embeddings_cache/*.npy` | ~143 GB | v2 embeddings |

## Already included in the bundle (no copy needed):

- `processed/custom_stoplist.txt`
- `raw/romance_subdataset_filtered_v3/v3_filtering_manifest.json`
- `raw/romance_subdataset_filtered_v3/language_analysis.csv`
- `raw/romance_subdataset_filtered_v3/subsampling_metadata/*.csv`
- `interim/octis/v3_english_only/corpus.tsv`, `corpus.offsets.npy`, `metadata.json`
- `stage03_samples/fit_indices_seed42.npy`, `eval_indices_seed42.npy` (v2 indices)

## v3 Row Counts

| Split | Sentences | Books |
|-------|-----------|-------|
| Train | 80,230,272 | 11,158 |
| Val   | 17,198,034 | 2,429 |
| Test  | 17,475,960 | 2,413 |
| **Total** | **114,904,266** | **16,000** |

See also `README.md` (Docker runbook) at the bundle root for build commands.
EOF

cat > "$SENTENCES_DIR/README.md" <<'EOF'
# Legacy v2 Sentence CSVs (alternative)

These are the original v2 files with non-English content. Prefer v3 instead.

Copy these files if using v2:
- `sentences_train.csv` (~6.5 GB)
- `sentences_val.csv` (~1.3 GB)
- `sentences_test.csv` (~1.5 GB)

Schema: `work_id, chapter_index, chapter_title, sentence_index, sentence`
EOF

cat > "$SENTENCES_V3_DIR/README.md" <<'EOF'
# v3 English-Only Sentence CSVs (recommended)

Copy these files from source machine or flash drive:
- `sentences_train.csv` (~6.3 GB, 80.2M sentences)
- `sentences_val.csv` (~1.4 GB, 17.2M sentences)
- `sentences_test.csv` (~1.4 GB, 17.5M sentences)

Schema: `work_id, chapter_index, chapter_title, sentence_index, sentence`

v3 has 460 non-English books removed (Spanish, Portuguese, French, etc.).
See `language_analysis.csv` and `v3_filtering_manifest.json` for details.
EOF

cat > "$OCTIS_V3/README.md" <<'EOF'
# v3 English-Only OCTIS Corpus (pre-built)

This folder contains the pre-built v3 English-only corpus:

- `corpus.tsv` (7.3 GB, 97,428,306 rows)
- `corpus.offsets.npy` (744 MB)
- `metadata.json`

Row breakdown: 80,230,272 train + 17,198,034 eval

If files are missing, rebuild with:

```bash
python -c "
from pathlib import Path
from src.stage03_train.octis_corpus import write_octis_corpus_from_csvs
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('v3')

write_octis_corpus_from_csvs(
    Path('data/raw/romance_subdataset_filtered_v3/sentences_train.csv'),
    Path('data/raw/romance_subdataset_filtered_v3/sentences_val.csv'),
    Path('data/interim/octis/v3_english_only'),
    logger=logger,
)
"
```

Build time: ~10-15 minutes on SSD.
EOF

cat > "$OCTIS_SHARED/README.md" <<'EOF'
# Legacy v2 OCTIS corpus (alternative)

Copy to skip rebuilding `corpus.tsv` (~10 min saved on startup):

- `corpus.tsv` (~7.5 GB)
- `corpus.offsets.npy` (~760 MB)
- `metadata.json` (already in bundle)

This is the v2 corpus with non-English content. Prefer building v3 instead.
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
touch "$OCTIS_V3/.keep"
touch "$OCTIS_MPNET/.keep"
touch "$OCTIS_MINILM6/.keep"
touch "$OCTIS_MINILM12_CACHE/.keep"
touch "$SENTENCES_DIR/.keep"
touch "$SENTENCES_V3_DIR/.keep"

echo
echo "Done. Bundle contents:"
find "$BUNDLE" -maxdepth 1 -mindepth 1 -printf '  %f\n' | sort
echo
echo "Data skeleton:"
find "$BUNDLE/data" -type f | sort | sed 's|^|  |'
echo
echo "Bundle size: $(du -sh "$BUNDLE" | cut -f1)"
echo
echo "Next steps (v3 English-only workflow):"
echo "  1. Copy v3 CSVs into data/raw/romance_subdataset_filtered_v3/"
echo "     - sentences_train.csv (~6.3 GB)"
echo "     - sentences_val.csv (~1.4 GB)"
echo "     - sentences_test.csv (~1.4 GB)"
echo "  2. Build v3 OCTIS corpus on target machine (~15 min)"
echo "  3. Build v3 embeddings on target machine (~4 days)"
echo "  4. cp .env.example .env && set HF_TOKEN"
echo "  5. Follow README.md inside the bundle"
echo
echo "See README.md for exact copy-paste commands."
