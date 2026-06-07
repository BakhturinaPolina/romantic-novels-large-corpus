# Stage03 Docker Runbook (Parallel GPU)

This runbook packages stage03 so you can run on another NVIDIA machine without creating a new virtualenv.

Everything needed to build the image lives in the self-contained **`transfer_bundle/`** folder (Dockerfile, compose file, `requirements*.txt`, `src/`, `configs/`, `Makefile`, `.env.example`, and this README). Regenerate it any time the code or Dockerfile changes:

```bash
bash scripts/make_transfer_bundle.sh
```

Ship `transfer_bundle/` to the target machine; carry the data CSVs and a filled-in `.env` separately (see step 3).

## v3 English-Only Corpus (Recommended)

The v3 corpus removes 460 non-English books (Spanish, Portuguese, French, etc.) for cleaner topic modeling. Statistics:

| Split | v2 Sentences | v3 Sentences | Removed |
|-------|-------------|-------------|---------|
| Train | 82,114,042 | 80,230,272 | 2.3% |
| Val | 17,709,782 | 17,198,034 | 2.9% |
| Test | 18,238,772 | 17,475,960 | 4.2% |
| **Total** | **118,062,596** | **114,904,266** | **2.7%** |

## 1) Prerequisites on the target machine

- Linux + NVIDIA GPU
- NVIDIA driver compatible with CUDA 12.x
- Docker Engine + Docker Compose v2
- `nvidia-container-toolkit` installed and configured

Quick check:

```bash
docker run --rm --gpus all nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04 nvidia-smi
```

## 2) Build image

From repo root (uses `docker/Dockerfile`):

```bash
docker build -f docker/Dockerfile -t romance-stage03:latest .
```

From inside the shipped bundle (its root is the build context):

```bash
cd transfer_bundle
docker build -t romance-stage03:latest .
```

## Second laptop: exact startup (v3 English-only corpus)

Run these on the second laptop after copying `transfer_bundle/` from the flash drive:

```bash
cd ~/romance_parallel
rsync -a /media/$USER/<FLASH_DRIVE>/transfer_bundle/ ./

# Copy v3 sentence CSVs from flash drive (~9 GB total):
cp /media/$USER/<FLASH_DRIVE>/sentences_train.csv data/raw/romance_subdataset_filtered_v3/
cp /media/$USER/<FLASH_DRIVE>/sentences_val.csv data/raw/romance_subdataset_filtered_v3/
cp /media/$USER/<FLASH_DRIVE>/sentences_test.csv data/raw/romance_subdataset_filtered_v3/

cp .env.example .env   # then edit .env and paste your HF_TOKEN
docker build -t romance-stage03:latest .
```

### Step 1: Build v3 OCTIS corpus (~15 minutes)

```bash
docker run --rm --gpus all \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  romance-stage03:latest \
  python3 -c "
from pathlib import Path
from src.stage03_train.octis_corpus import write_octis_corpus_from_csvs
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('v3_corpus')

print('Building v3 OCTIS corpus from English-only sentences...')
corpus_path, offsets_path, n_train, n_eval = write_octis_corpus_from_csvs(
    Path('data/raw/romance_subdataset_filtered_v3/sentences_train.csv'),
    Path('data/raw/romance_subdataset_filtered_v3/sentences_val.csv'),
    Path('data/interim/octis/v3_english_only'),
    logger=logger,
)
print(f'Done! {n_train:,} train + {n_eval:,} eval = {n_train + n_eval:,} total rows')
"
```

### Step 2: Build v3 embeddings (~4 days per model)

```bash
# MiniLM-L12 embeddings (384 dim, ~140 GB output)
docker run -d --name romance-v3-embeddings --gpus all --env-file .env \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/results:/app/results" \
  -v "$(pwd)/logs:/app/logs" \
  romance-stage03:latest \
  python3 -c "
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from src.stage03_train.corpus_store import CorpusDocStore, corpus_offsets_path
import torch

# Load v3 corpus
corpus_dir = Path('data/interim/octis/v3_english_only')
corpus_tsv = corpus_dir / 'corpus.tsv'
offsets_file = corpus_offsets_path(corpus_dir)
doc_store = CorpusDocStore(corpus_tsv, offsets_file)
n_docs = len(doc_store)
print(f'Loaded corpus: {n_docs:,} documents')

# Load embedding model
model_name = 'sentence-transformers/all-MiniLM-L12-v2'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer(model_name, device=device)
dim = model.get_sentence_embedding_dimension()
print(f'Model: {model_name} ({dim} dim) on {device}')

# Output path
out_path = corpus_dir / 'embeddings_cache' / f'train_eval_{model_name.replace(\"/\", \"__\")}.npy'
out_path.parent.mkdir(parents=True, exist_ok=True)

# Check for resume
start_idx = 0
if out_path.exists():
    existing = np.load(out_path, mmap_mode='r')
    start_idx = existing.shape[0]
    print(f'Resuming from row {start_idx:,}')

# Preallocate or open existing
if start_idx == 0:
    embeddings = np.memmap(out_path, dtype='float32', mode='w+', shape=(n_docs, dim))
else:
    embeddings = np.memmap(out_path, dtype='float32', mode='r+', shape=(n_docs, dim))

# Encode in batches
batch_size = 512
for i in range(start_idx, n_docs, batch_size):
    end = min(i + batch_size, n_docs)
    docs = doc_store.fetch_documents(list(range(i, end)))
    emb = model.encode(docs, show_progress_bar=False, convert_to_numpy=True)
    embeddings[i:end] = emb
    if (i // batch_size) % 100 == 0:
        embeddings.flush()
        pct = 100 * end / n_docs
        print(f'Progress: {end:,}/{n_docs:,} ({pct:.2f}%)')

embeddings.flush()
print(f'Done! Saved to {out_path}')
"

# Monitor progress
docker logs -f romance-v3-embeddings
```

### Step 3: Generate v3 fit/eval indices

```bash
docker run --rm --gpus all \
  -v "$(pwd)/data:/app/data" \
  romance-stage03:latest \
  python3 -m src.stage03_train.make_fit_sample \
    --train-csv data/raw/romance_subdataset_filtered_v3/sentences_train.csv \
    --val-csv data/raw/romance_subdataset_filtered_v3/sentences_val.csv \
    --metadata-train data/raw/romance_subdataset_filtered_v3/subsampling_metadata/romance_subdataset_filtered_v3_train.csv \
    --metadata-val data/raw/romance_subdataset_filtered_v3/subsampling_metadata/romance_subdataset_filtered_v3_val.csv \
    --out-dir data/stage03_samples_v3 --train-target 500000 --val-target 100000 --seed 42
```

### Step 4: Run BO tuning on v3

After embeddings complete (~4 days), start the BO optimization:

```bash
# Update configs/paths_stage03_fit.yaml to point to v3:
#   sentences_train_csv: data/raw/romance_subdataset_filtered_v3/sentences_train.csv
#   sentences_val_csv: data/raw/romance_subdataset_filtered_v3/sentences_val.csv
#   octis_corpus_dir: data/interim/octis/v3_english_only
#   fit_indices_file: data/stage03_samples_v3/fit_indices_seed42.npy
#   eval_indices_file: data/stage03_samples_v3/eval_indices_seed42.npy

docker run -d --name romance-stage03-v3 --gpus all --env-file .env \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/results:/app/results" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/models:/app/models" \
  romance-stage03:latest \
  python3 -m src.stage03_train.cli tune \
    --config configs/train.yaml \
    --run-id v3_minilm12v2_first \
    --embedding-model sentence-transformers/all-MiniLM-L12-v2

docker logs -f romance-stage03-v3
```

## Legacy v2 workflow (alternative)

For MiniLM-L6, change `RUN_ID=minilm6_first` and `EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L6-v2`.

## 3) What to copy on flash drive

The `transfer_bundle/` folder contains all code/config **plus a `data/` skeleton** with small
artifacts already filled in (fit/eval indices, stoplist, subsampling metadata, OCTIS
`metadata.json`) and **drop folders** for large payloads. See `data/README.md` inside the
bundle for the full checklist.

### Already inside the bundle (no copy needed)

- `configs/train.yaml`, `configs/paths_stage03_fit.yaml` (stratified fit + embedding overrides)
- `data/stage03_samples/fit_indices_seed42.npy`, `eval_indices_seed42.npy`, `sample_manifest_seed42.json`
- `data/processed/custom_stoplist.txt`
- `data/raw/.../subsampling_metadata/*.csv` (book metadata)
- `data/interim/octis/minilm12v2_first/metadata.json`
- Empty drop folders with READMEs:
  - `data/interim/octis/mpnet_first/embeddings_cache/` → MPNet `.npy`
  - `data/interim/octis/minilm6_first/embeddings_cache/` → MiniLM-L6 `.npy`
  - `data/interim/octis/minilm12v2_first/embeddings_cache/` → MiniLM-L12 `.npy` (if running L12)

Also create `.env` from `.env.example` (contains `HF_TOKEN`). Keep it private; never bake it into the image.

### Required large payload (copy separately)

Copy these files to the target machine under the same relative paths inside `data/`:

- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_train.csv`
- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_val.csv`
- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_test.csv`

### Recommended payload (saves ~10 minutes)

If you want to skip re-building the OCTIS corpus metadata on the second machine, also copy:

- `data/interim/octis/minilm12v2_first/corpus.tsv`
- `data/interim/octis/minilm12v2_first/corpus.offsets.npy`

This corpus is shared by all three embedding models.

### Per-model embedding `.npy` (drop into bundle folders)

Place each model's **full** `train_eval_*.npy` in its drop folder (exact filenames matter):

| Model | Drop folder | Filename |
|-------|-------------|----------|
| MPNet | `data/interim/octis/mpnet_first/embeddings_cache/` | `train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy` |
| MiniLM-L6 | `data/interim/octis/minilm6_first/embeddings_cache/` | `train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy` |
| MiniLM-L12 | `data/interim/octis/minilm12v2_first/embeddings_cache/` | `train_eval_sentence-transformers__all-MiniLM-L12-v2.npy` |

All three caches share the same full train→eval row order (~99.8M rows), so the bundled
`fit_indices_seed42.npy` / `eval_indices_seed42.npy` work for every model.

Do **not** copy another model's in-progress `.progress.json` partial caches unless you intend
to resume that exact encoding job on the same machine.

## 3b) Stratified fit-sample run that reuses full `.npy` caches

The default `configs/train.yaml` now tunes on a **stratified, train-only** fit sample and
**reuses precomputed full-corpus embeddings** (no re-encoding). To use it:

1. Build the fit/eval indices once on the host (CPU-only, streams the full CSVs):

```bash
python -m src.stage03_train.make_fit_sample \
  --train-csv data/processed/romance_subdataset_downloaded_v2_sentences/sentences_train.csv \
  --val-csv data/processed/romance_subdataset_downloaded_v2_sentences/sentences_val.csv \
  --metadata-train data/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata/romance_subdataset_downloaded_v2_train.csv \
  --metadata-val data/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata/romance_subdataset_downloaded_v2_val.csv \
  --out-dir data/stage03_samples --train-target 500000 --val-target 100000 --seed 42
```

2. Place each model's **full** `train_eval_*.npy` under its run-id cache dir
   (`data/interim/octis/<run_id>/embeddings_cache/`) and point
   `configs/train.yaml -> embeddings_cache.overrides` at them. The three caches share
   the same full train->eval row order, so indices gathered for one are valid for all.

3. Reuse a prebuilt full `corpus.tsv` by setting
   `configs/paths_stage03_fit.yaml -> inputs.octis_corpus_dir` (e.g.
   `data/interim/octis/minilm12v2_first`) to skip the ~100M-row corpus rewrite.

Mount `data/stage03_samples` (it lives under the already-mounted `data/`). The run will
fail fast with a clear error if a configured override `.npy` is missing or its row count
does not match the corpus.

## 4) Run detached with `docker run` (resumable)

Run **detached** (`-d`) so the job survives terminal/SSH disconnects. All four host
folders (`data`, `results`, `logs`, `models`) are bind-mounted, so every checkpoint
is written to the host and the run is **resumable**: re-running the same command (same
`--run-id`) continues from disk instead of restarting (see step 5). Pick a **distinct
`--run-id` per model** so parallel machines never collide.

### Block A — MPNet (`paraphrase-mpnet-base-v2`)

```bash
docker run -d --name romance-stage03-mpnet --gpus all --env-file .env \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/results:/app/results" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/models:/app/models" \
  romance-stage03:latest \
  python3 -m src.stage03_train.cli tune \
    --config configs/train.yaml \
    --run-id mpnet_first \
    --embedding-model sentence-transformers/paraphrase-mpnet-base-v2
```

Logs / resume this exact run:

```bash
docker logs -f romance-stage03-mpnet     # follow logs
docker start -a romance-stage03-mpnet    # resume after a stop/crash (same run-id, same mounts)
```

### Block B — MiniLM-L6 (`paraphrase-MiniLM-L6-v2`)

```bash
docker run -d --name romance-stage03-minilm-l6 --gpus all --env-file .env \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/results:/app/results" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/models:/app/models" \
  romance-stage03:latest \
  python3 -m src.stage03_train.cli tune \
    --config configs/train.yaml \
    --run-id minilm_l6_first \
    --embedding-model sentence-transformers/paraphrase-MiniLM-L6-v2
```

Logs / resume this exact run:

```bash
docker logs -f romance-stage03-minilm-l6
docker start -a romance-stage03-minilm-l6
```

### Block C — `docker compose` variant

Override the run id and model via environment variables; the service stays detached
and is set to `restart: unless-stopped`, so it auto-restarts (and auto-resumes) after
a crash or reboot.

```bash
# MPNet
RUN_ID=mpnet_first \
EMBEDDING_MODEL=sentence-transformers/paraphrase-mpnet-base-v2 \
docker compose up -d --build

# MiniLM-L6
RUN_ID=minilm_l6_first \
EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L6-v2 \
docker compose up -d --build

docker compose logs -f stage03   # follow logs
docker compose down              # stop (progress is preserved on the host)
```

On a brand-new `run-id`, the Hub cache path may not exist yet. That is expected: Stage03 will fall back to local embedding compute, then upload the generated `.npy` when finished.

## 5) Resume & progress safety

Resume is **automatic and built into Stage03** — there is no `--resume` flag. To resume,
re-run the **exact same command with the same `--run-id`**. Because `data/`, `results/`,
`logs/`, and `models/` are bind-mounted to the host, all checkpoints survive container
exit, crash, or reboot. On re-run, Stage03 reads `results/experiments/<run-id>/run_state.json`
and the on-disk artifacts and **skips already-completed work**:

- **`data_load`** — cached row counts are reused instead of re-scanning ~100M rows.
- **OCTIS corpus** — `corpus.tsv` / `corpus.offsets.npy` are reused if already written.
- **Embeddings** — chunked `.npy` cache resumes mid-model (only missing chunks recompute).
- **Bayesian optimization** — the BO loop re-seeds from `result.json` (`x0`/`y0`) and continues at the next call instead of restarting at `Current call: 0`; per-call progress is persisted to `trials_partial.csv`.
- **Completed models** — any model already finished in `trials.csv` is skipped.

Practical resume tips:

- `docker run`: after a stop, `docker start -a <name>` re-runs the original command in the same container (same run-id) and resumes. To rebuild the command, `docker rm <name>` first, then re-issue the `docker run` block above verbatim.
- `docker compose`: `restart: unless-stopped` already auto-resumes; otherwise `docker compose up -d` again.
- Keep the **same `--run-id`** — changing it starts a fresh run from scratch.

## 6) Parallel strategy

- Machine A: keep current run (`minilm12v2_first`)
- Machine B: run another model (`mpnet_first`) with a distinct `--run-id`
- Machine C: run a third model (`minilm_l6_first`) with its own `--run-id`
- With `embeddings_hub.enabled: true` in `configs/train.yaml`, each machine can upload embeddings to Hugging Face Hub (requires `HF_TOKEN` in `.env`), which is how results from the machines converge.

## 7) Practical notes

- `paraphrase-mpnet-base-v2` (768-dim) is the heaviest of the three; if CUDA OOM appears for the **MPNet** run, reduce `embedding_batch_size` in `configs/train.yaml`.
- `paraphrase-MiniLM-L6-v2` (384-dim) is the lightest and rarely OOMs; if it does, lower `embedding_batch_size` the same way for the **MiniLM-L6** run.
- First image build is large and slow because RAPIDS and PyTorch CUDA wheels are large.
- Keep detached execution (`docker run -d` / `docker compose up -d`) to avoid losing progress on terminal close; combined with the same `--run-id`, any interruption is resumable.
