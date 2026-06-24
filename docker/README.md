# Stage03 v3 Transfer Bundle — Docker Runbook

Self-contained folder for running Stage03 v3 **CPU embedding encode** (and optional BO tuning) on another Linux machine. MiniLM-L12 tuning is already complete on the primary laptop and is not part of this runbook.

Regenerate the bundle after code or Dockerfile changes:

```bash
bash scripts/make_transfer_bundle.sh
```

## Corpus (v3 English-only)

Non-English books were removed (460 titles, ~2.7% of sentences). The bundle ships the OCTIS corpus, metadata, stoplist, and stratified fit/eval indices. You must copy the three large sentence CSVs separately (~9 GB total).

| Split | Sentences |
|-------|-----------|
| Train | 80,230,272 |
| Val   | 17,198,034 |
| Test  | 17,475,960 |

## What is in the bundle

- Docker build context: `Dockerfile`, `docker-compose.yml`, `requirements*.txt`, `src/`, `configs/`
- `configs/train_v3_mpnet.yaml`, `configs/train_v3_minilm6.yaml`, `configs/paths_stage03_fit_v3.yaml`
- `scripts/run_v3_remote_model.sh` — encode + tune helper (no sudo)
- Pre-built OCTIS corpus under `data/interim/octis/v3_english_only/` (~8 GB)
- v3 subsampling metadata, filtering manifest, custom stoplist
- v3 fit/eval indices under `data/stage03_samples_v3/` (if generated before bundling)
- Empty drop folder for embedding caches: `data/interim/octis/v3_english_only/embeddings_cache/`

## Copy manually (too large for the bundle)

Place these under `data/raw/romance_subdataset_filtered_v3/` on the target machine:

| File | Size |
|------|------|
| `sentences_train.csv` | ~6.3 GB |
| `sentences_val.csv` | ~1.4 GB |
| `sentences_test.csv` | ~1.4 GB |

Source on the primary machine:

```
data/raw/romance_subdataset_filtered_v3/sentences_{train,val,test}.csv
```

## Prerequisites (target machine)

- Linux, Docker Engine
- User in the `docker` group (run Docker **without** sudo)
- Enough RAM/disk for CPU embedding encode (no GPU or `nvidia-container-toolkit` required)
- **No `.env` file, API keys, or Hugging Face token** — public sentence-transformers models download automatically; encode runs from local CSVs only

`scripts/run_v3_remote_model.sh` runs containers **without** `--gpus all` and forces `device=cpu` for encode. BO tuning still uses RAPIDS cuML and needs a GPU machine (or run tuning elsewhere after copying the `.npy` cache).

## Quick start

Unpack the bundle, copy the three CSVs, then:

```bash
cd transfer_bundle
docker build -t romance-stage03:latest .
chmod +x scripts/run_v3_remote_model.sh

# Once, after CSVs are in place (indices may already be in the bundle):
./scripts/run_v3_remote_model.sh sample

# Pick one model per machine — MPNet OR MiniLM-L6 (CPU encode; resumable):
./scripts/run_v3_remote_model.sh mpnet encode   # foreground; Ctrl+C to stop

# After encode finishes (CPU: much slower than GPU; weeks+ depending on hardware):
./scripts/run_v3_remote_model.sh mpnet tune    # requires GPU for cuML UMAP/HDBSCAN

# To resume after interrupt: re-run the same command (checkpoints on disk)
./scripts/run_v3_remote_model.sh mpnet encode
```

Replace `mpnet` with `minilm6` on the second machine. Use a **distinct model per machine** — both write to the same cache directory but different `.npy` filenames.

## Models and run IDs

| Model | Hub name | Run ID | Cache file (under `embeddings_cache/`) | Approx. size |
|-------|----------|--------|------------------------------------------|--------------|
| MPNet | `sentence-transformers/paraphrase-mpnet-base-v2` | `v3_mpnet_first` | `train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy` | ~280 GB |
| MiniLM-L6 | `sentence-transformers/paraphrase-MiniLM-L6-v2` | `v3_minilm6_first` | `train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy` | ~140 GB |

Row count for all caches: **97,428,306** (train + val).

If CUDA OOM during MPNet encode on a GPU box, lower `ENCODE_BATCH` in the script (128 → 64). On CPU-only hosts, reduce batch size if you hit RAM pressure.

## Resume behavior

Stage03 resumes automatically from disk — no `--resume` flag. Re-run the same command with the same run-id. Bind-mounted folders (`data/`, `results/`, `logs/`, `models/`) preserve:

- Chunked embedding `.npy` progress
- OCTIS corpus (pre-built in bundle)
- BO trials in `results/experiments/<run-id>/`

## Parallel strategy

- **Machine 1:** `./scripts/run_v3_remote_model.sh mpnet encode` → `mpnet tune`
- **Machine 2:** `./scripts/run_v3_remote_model.sh minilm6 encode` → `minilm6 tune`

Copy `data/stage03_samples_v3/` between machines if you generate indices on only one box.

## Notes

- First `docker build` is slow (RAPIDS + PyTorch wheels in the image; encode still runs on CPU).
- Encode and tune run **in the foreground** (logs stream to the terminal; Ctrl+C stops the job). Re-run the same command to resume from disk. Use `tmux` or `screen` if you need the session to survive SSH disconnect.
- See `data/README.md` inside the bundle for the full data layout checklist.
