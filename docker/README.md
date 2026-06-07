# Stage03 Docker Runbook (Parallel GPU)

This runbook packages stage03 so you can run on another NVIDIA machine without creating a new virtualenv.

Everything needed to build the image lives in the self-contained **`transfer_bundle/`** folder (Dockerfile, compose file, `requirements*.txt`, `src/`, `configs/`, `Makefile`, `.env.example`, and this README). Regenerate it any time the code or Dockerfile changes:

```bash
bash scripts/make_transfer_bundle.sh
```

Ship `transfer_bundle/` to the target machine; carry the data CSVs and a filled-in `.env` separately (see step 3).

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

## Second laptop: exact startup (stratified tuning)

Run these on the second laptop after copying `transfer_bundle/` from the flash drive:

```bash
cd ~/romance_parallel
rsync -a /media/$USER/<FLASH_DRIVE>/transfer_bundle/ ./

# Large files (not inside the bundle) — copy from flash drive or rsync from source:
#   data/processed/romance_subdataset_downloaded_v2_sentences/sentences_{train,val,test}.csv
#   data/interim/octis/minilm12v2_first/corpus.{tsv,offsets.npy}   # optional, saves ~10 min
#   data/interim/octis/mpnet_first/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy
#   data/interim/octis/minilm6_first/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy

cp .env.example .env   # then edit .env and paste your HF_TOKEN
docker build -t romance-stage03:latest .

# MPNet (uses pre-placed .npy under data/interim/octis/mpnet_first/embeddings_cache/)
RUN_ID=mpnet_first EMBEDDING_MODEL=sentence-transformers/paraphrase-mpnet-base-v2 docker compose up -d
docker compose logs -f stage03
```

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
