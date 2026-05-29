# Stage03 Docker Runbook (Parallel GPU)

This runbook packages stage03 so you can run on another NVIDIA machine without creating a new virtualenv.

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

From repo root:

```bash
docker build -t romance-stage03:latest .
```

## Second laptop: exact 5-command startup

Run these on the second laptop after copying `transfer_bundle/` from flash drive:

```bash
cd ~/romance_parallel && rsync -a /media/$USER/<FLASH_DRIVE>/transfer_bundle/ ./ && mkdir -p data/interim/octis/minilm12v2_first && rsync -av --ignore-missing-args /media/$USER/<FLASH_DRIVE>/data/interim/octis/minilm12v2_first/corpus.tsv /media/$USER/<FLASH_DRIVE>/data/interim/octis/minilm12v2_first/corpus.offsets.npy /media/$USER/<FLASH_DRIVE>/data/interim/octis/minilm12v2_first/metadata.json data/interim/octis/minilm12v2_first/
cp .env.example .env
docker build -t romance-stage03:latest .
RUN_ID=mpnet_first EMBEDDING_MODEL=sentence-transformers/paraphrase-mpnet-base-v2 docker compose up -d
docker compose logs -f stage03
```

## 3) What to copy on flash drive

### Required data payload

Copy these files from this repo to the target repo under the same relative paths:

- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_train.csv`
- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_val.csv`
- `data/processed/romance_subdataset_downloaded_v2_sentences/sentences_test.csv`

Also copy:

- `.env` (contains `HF_TOKEN` and optional API keys). Keep it private.

### Optional payload (saves about 10 minutes)

If you want to skip re-building the OCTIS corpus metadata on the second machine, also copy:

- `data/interim/octis/minilm12v2_first/corpus.tsv`
- `data/interim/octis/minilm12v2_first/corpus.offsets.npy`
- `data/interim/octis/minilm12v2_first/metadata.json`

### Do not copy for parallel different-model run

Do not copy model-specific caches from MiniLM-L12 when the second machine runs MPNet/L6:

- `data/interim/octis/minilm12v2_first/embeddings_cache/*.npy`
- `data/interim/octis/minilm12v2_first/embeddings_cache/*.progress.json`

## 4) Run detached with docker run

Example (second machine computes MPNet while first machine stays on MiniLM-L12):

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

Logs:

```bash
docker logs -f romance-stage03-mpnet
```

## 5) Run detached with docker compose

Default compose service is configured in `docker-compose.yml`.

Start:

```bash
docker compose up -d --build
```

Override run id or model:

```bash
RUN_ID=minilm_l6_first \
EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L6-v2 \
docker compose up -d --build
```

Stop:

```bash
docker compose down
```

## 6) Parallel strategy

- Machine A: keep current run (`minilm12v2_first`)
- Machine B: run another model (`mpnet_first` or `minilm_l6_first`) with a distinct `--run-id`
- With `embeddings_hub.enabled: true` in `configs/train.yaml`, each machine can upload embeddings to Hugging Face Hub (requires `HF_TOKEN` in `.env`)

## 7) Practical notes

- `paraphrase-mpnet-base-v2` is heavier than MiniLM-L12; if CUDA OOM appears, reduce `embedding_batch_size` in `configs/train.yaml`.
- First image build is large and slow because RAPIDS and PyTorch CUDA wheels are large.
- Keep detached execution (`docker run -d` / `docker compose up -d`) to avoid losing progress on terminal close.
