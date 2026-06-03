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

## Second laptop: exact 5-command startup

Run these on the second laptop after copying `transfer_bundle/` from the flash drive:

```bash
cd ~/romance_parallel && rsync -a /media/$USER/<FLASH_DRIVE>/transfer_bundle/ ./ && mkdir -p data/interim/octis/minilm12v2_first && rsync -av --ignore-missing-args /media/$USER/<FLASH_DRIVE>/data/interim/octis/minilm12v2_first/corpus.tsv /media/$USER/<FLASH_DRIVE>/data/interim/octis/minilm12v2_first/corpus.offsets.npy /media/$USER/<FLASH_DRIVE>/data/interim/octis/minilm12v2_first/metadata.json data/interim/octis/minilm12v2_first/
cp .env.example .env   # then edit .env and paste your HF_TOKEN
docker build -t romance-stage03:latest .
RUN_ID=mpnet_first EMBEDDING_MODEL=sentence-transformers/paraphrase-mpnet-base-v2 docker compose up -d
docker compose logs -f stage03
```

## 3) What to copy on flash drive

The `transfer_bundle/` folder already contains all code/config. Alongside it, copy the **data** (which is intentionally *not* baked into the image):

### Required data payload

Copy these files to the target machine under the same relative paths:

- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_train.csv`
- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_val.csv`
- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_test.csv`

Also copy:

- `.env` (contains `HF_TOKEN` and optional API keys). Keep it private; never bake it into the image.

### Optional payload (saves about 10 minutes)

If you want to skip re-building the OCTIS corpus metadata on the second machine, also copy:

- `data/interim/octis/minilm12v2_first/corpus.tsv`
- `data/interim/octis/minilm12v2_first/corpus.offsets.npy`
- `data/interim/octis/minilm12v2_first/metadata.json`

### Do not copy for parallel different-model run

Do not copy model-specific caches from MiniLM-L12 when the second machine runs MPNet/L6:

- `data/interim/octis/minilm12v2_first/embeddings_cache/*.npy`
- `data/interim/octis/minilm12v2_first/embeddings_cache/*.progress.json`

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
