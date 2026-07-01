#!/usr/bin/env bash
# Assemble a self-contained transfer bundle for shipping Stage03 to another Linux machine.
#
# The bundle is a single folder you can rsync to a flash drive and unpack on a
# second box (CPU-only encode is supported; no NVIDIA driver required on target).
# It carries the full Docker build context (Dockerfile,
# compose file, requirements, app code, configs) plus a data/ skeleton with small
# artifacts already filled in and drop folders for large files (.csv, .npy).
#
# Regenerate any time the code/config/Dockerfile changes:
#   bash scripts/bundle/make_transfer_bundle.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUNDLE="${1:-$ROOT/transfer_bundle}"
DOCKER_DIR="$ROOT/docker"

echo "Assembling transfer bundle at: $BUNDLE"
if [[ -d "$BUNDLE" ]]; then
  # Docker-created __pycache__ may be root-owned after prior bundle runs.
  docker run --rm -v "$BUNDLE:/bundle:rw" alpine sh -c 'rm -rf /bundle/* /bundle/.[!.]* /bundle/..?*' \
    2>/dev/null || chmod -R u+w "$BUNDLE" 2>/dev/null || true
  rm -rf "$BUNDLE"
fi
mkdir -p "$BUNDLE"

# Docker build files from docker/ (build context root = bundle root).
cp "$DOCKER_DIR/Dockerfile" "$BUNDLE/"
sed -i '/^COPY \.env\.example \.\//d' "$BUNDLE/Dockerfile"
cp "$DOCKER_DIR/docker-compose.yml" "$BUNDLE/"
sed -i '/^    env_file:/,/^      - \.env/d' "$BUNDLE/docker-compose.yml"
cp "$ROOT/.dockerignore" "$BUNDLE/"

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

# Remote bundle: no Hub credentials or embedding download — encode from local CSVs only.
for cfg in "$BUNDLE"/configs/stage03/train_v3_mpnet.yaml \
           "$BUNDLE"/configs/stage03/train_v3_minilm6.yaml \
           "$BUNDLE"/configs/stage03/train_v4_*_granular_*.yaml; do
  if [[ -f "$cfg" ]]; then
    sed -i 's/^  enabled: true$/  enabled: false/' "$cfg"
    sed -i 's/^  download_if_missing: true$/  download_if_missing: false/' "$cfg"
  fi
done

# Remote-run helper scripts (also copied into bundle scripts/).
mkdir -p "$BUNDLE/scripts"
cp "$ROOT/scripts/stage03/run_v3_remote_model.sh" "$BUNDLE/scripts/"
cp "$ROOT/scripts/stage03/run_v4_granular_remote.sh" "$BUNDLE/scripts/"
chmod +x "$BUNDLE/scripts/run_v3_remote_model.sh" "$BUNDLE/scripts/run_v4_granular_remote.sh"

# ---------------------------------------------------------------------------
# Data payload skeleton (small files copied; large files = drop folders)
# ---------------------------------------------------------------------------
DATA="$BUNDLE/data"
SENTENCES_V3_DIR="$DATA/raw/romance_subdataset_filtered_v3"
METADATA_V3_DIR="$DATA/raw/romance_subdataset_filtered_v3/subsampling_metadata"
SAMPLES_V3_DIR="$DATA/stage03_samples_v3"
OCTIS_V3="$DATA/interim/octis/v3_english_only"
OCTIS_V3_CACHE="$OCTIS_V3/embeddings_cache"

mkdir -p "$SENTENCES_V3_DIR" "$METADATA_V3_DIR" "$SAMPLES_V3_DIR" \
  "$OCTIS_V3" "$OCTIS_V3_CACHE"
mkdir -p "$BUNDLE/results" "$BUNDLE/logs" "$BUNDLE/models"
touch "$BUNDLE/results/.gitkeep" "$BUNDLE/logs/.gitkeep" "$BUNDLE/models/.gitkeep"

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
mkdir -p "$DATA/processed"
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

# v3 stratified fit/eval indices (small; avoids regenerate on target if present)
for f in fit_indices_seed42.npy eval_indices_seed42.npy sample_manifest_seed42.json; do
  copy_if_exists "$ROOT/data/stage03_samples_v3/$f" "$SAMPLES_V3_DIR/$f"
done

# v3 OCTIS corpus (pre-built, saves ~15 min on target machine)
echo "Copying v3 OCTIS corpus (~8 GB)..."
copy_if_exists "$ROOT/data/interim/octis/v3_english_only/corpus.tsv" "$OCTIS_V3/corpus.tsv"
copy_if_exists "$ROOT/data/interim/octis/v3_english_only/corpus.offsets.npy" "$OCTIS_V3/corpus.offsets.npy"
copy_if_exists "$ROOT/data/interim/octis/v3_english_only/metadata.json" "$OCTIS_V3/metadata.json"

cat > "$DATA/README.md" <<'EOF'
# Stage03 v3 data payload

Mirrors the repo `data/` layout expected by `configs/stage03/paths_stage03_fit_v3.yaml`
and `configs/stage03/train_v3_*.yaml`. Small files are pre-filled by
`scripts/bundle/make_transfer_bundle.sh`; copy the large files listed below before
starting Docker.

## Copy manually (required)

| Path | Size (approx.) | Notes |
|------|----------------|-------|
| `raw/romance_subdataset_filtered_v3/sentences_train.csv` | ~6.3 GB | v3 English-only train |
| `raw/romance_subdataset_filtered_v3/sentences_val.csv` | ~1.4 GB | v3 English-only eval |
| `raw/romance_subdataset_filtered_v3/sentences_test.csv` | ~1.4 GB | v3 English-only test |

## Included in the bundle

| Path | Size (approx.) | Notes |
|------|----------------|-------|
| `processed/custom_stoplist.txt` | small | BERTopic stoplist |
| `raw/romance_subdataset_filtered_v3/v3_filtering_manifest.json` | small | Filtering audit |
| `raw/romance_subdataset_filtered_v3/language_analysis.csv` | ~1.3 MB | Per-book language stats |
| `raw/romance_subdataset_filtered_v3/subsampling_metadata/*.csv` | small | Book metadata |
| `interim/octis/v3_english_only/corpus.tsv` | ~7.3 GB | Pre-built OCTIS corpus |
| `interim/octis/v3_english_only/corpus.offsets.npy` | ~744 MB | Byte offsets |
| `interim/octis/v3_english_only/metadata.json` | small | Row counts |
| `stage03_samples_v3/fit_indices_seed42.npy` | ~4 MB | Stratified fit sample (if bundled) |
| `stage03_samples_v3/eval_indices_seed42.npy` | ~1 MB | Stratified eval sample |
| `stage03_samples_v3/sample_manifest_seed42.json` | small | Sample manifest |

## Build on target (embedding caches)

| Path | Size (approx.) | Notes |
|------|----------------|-------|
| `interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy` | ~280 GB | MPNet — copy if already encoded elsewhere |
| `interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy` | ~140 GB | MiniLM-L6 — copy if already encoded elsewhere |
| `interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__all-MiniLM-L12-v2.npy` | ~140 GB | MiniLM-L12 — copy if already encoded elsewhere |

Encode (CPU, slow): `./scripts/run_v3_remote_model.sh mpnet encode` — skip if `.npy` already present.

## v4 granular BO (current Stage03 search)

Configs: `configs/stage03/train_v4_*_granular_phase{1,3}.yaml` (Hub disabled in bundle).

| Model | Phase 1 run ID | Phase 3 run ID |
|-------|----------------|----------------|
| MPNet | `v4_mpnet_granular_phase1` | `v4_mpnet_granular_phase3` |
| MiniLM-L6 | `v4_l6_granular_phase1` | `v4_l6_granular_phase3` |
| MiniLM-L12 | `v4_l12_granular_phase1` | `v4_l12_granular_phase3` |

Tune (needs GPU): `./scripts/run_v4_granular_remote.sh mpnet phase1`

## v3 row counts

| Split | Sentences | Books |
|-------|-----------|-------|
| Train | 80,230,272 | 11,158 |
| Val   | 17,198,034 | 2,429 |
| Test  | 17,475,960 | 2,413 |
| **Total** | **114,904,266** | **16,000** |

Train+val OCTIS rows (embedding cache length): **97,428,306**.
EOF

cat > "$SENTENCES_V3_DIR/README.md" <<'EOF'
# v3 English-only sentence CSVs

Copy these files manually from the primary machine or flash drive:

- `sentences_train.csv` (~6.3 GB, 80.2M sentences)
- `sentences_val.csv` (~1.4 GB, 17.2M sentences)
- `sentences_test.csv` (~1.4 GB, 17.5M sentences)

Schema: `work_id, chapter_index, chapter_title, sentence_index, sentence`

See `language_analysis.csv` and `v3_filtering_manifest.json` for filtering details.
EOF

cat > "$OCTIS_V3/README.md" <<'EOF'
# v3 English-only OCTIS corpus (pre-built)

- `corpus.tsv` (~7.3 GB, 97,428,306 rows)
- `corpus.offsets.npy` (~744 MB)
- `metadata.json`

Row breakdown: 80,230,272 train + 17,198,034 eval.

If files are missing, rebuild after copying sentence CSVs:

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  romance-stage03:latest \
  python3 -c "
from pathlib import Path
from src.stage03_train.octis_corpus import write_octis_corpus_from_csvs
import logging
logging.basicConfig(level=logging.INFO)
write_octis_corpus_from_csvs(
    Path('data/raw/romance_subdataset_filtered_v3/sentences_train.csv'),
    Path('data/raw/romance_subdataset_filtered_v3/sentences_val.csv'),
    Path('data/interim/octis/v3_english_only'),
    logger=logging.getLogger('v3'),
)
"
```
EOF

cat > "$OCTIS_V3_CACHE/README.md" <<'EOF'
# Drop folder: v3 full-corpus embeddings

Corpus: `data/interim/octis/v3_english_only` (97,428,306 train+eval rows)

| Model | Filename | Shape |
|-------|----------|-------|
| MPNet | `train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy` | (97428306, 768) |
| MiniLM-L6 | `train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy` | (97428306, 384) |

Run `./scripts/run_v3_remote_model.sh mpnet encode` or `minilm6 encode` from the bundle root.
EOF

cat > "$SAMPLES_V3_DIR/README.md" <<'EOF'
# v3 stratified fit/eval indices

If `fit_indices_seed42.npy` is already in this folder (bundled from the primary machine),
skip regeneration. Otherwise, after copying sentence CSVs:

```bash
./scripts/run_v3_remote_model.sh sample
```

Referenced by `configs/stage03/paths_stage03_fit_v3.yaml`.
EOF

touch "$OCTIS_V3/.keep"
touch "$OCTIS_V3_CACHE/.keep"
touch "$SAMPLES_V3_DIR/.keep"
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
echo "Manual copy required on target machine:"
echo "  data/raw/romance_subdataset_filtered_v3/sentences_train.csv (~6.3 GB)"
echo "  data/raw/romance_subdataset_filtered_v3/sentences_val.csv   (~1.4 GB)"
echo "  data/raw/romance_subdataset_filtered_v3/sentences_test.csv  (~1.4 GB)"
echo
echo "Then on target:"
echo "  docker build -t romance-stage03:latest ."
echo "  ./scripts/run_v3_remote_model.sh sample          # if indices not bundled"
echo "  ./scripts/run_v3_remote_model.sh mpnet encode  # skip if .npy already present"
echo "  ./scripts/run_v4_granular_remote.sh mpnet phase1 # v4 granular BO (needs GPU)"
echo
echo "Incremental update (data already on target): rsync only src/ configs/ scripts/"
echo "  Dockerfile docker-compose.yml requirements*.txt Makefile README.md — then docker build."
echo
echo "See README.md inside the bundle."
