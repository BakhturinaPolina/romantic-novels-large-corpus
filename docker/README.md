# Stage03 v3/v4 Transfer Bundle — Docker Runbook

Self-contained folder for Stage03 on another Linux machine:

- **CPU encode** (optional): `./scripts/stage03/run_v3_remote_model.sh mpnet encode`
- **v4 granular BO** (current): `./scripts/stage03/run_v4_granular_remote.sh mpnet phase1`

Regenerate after code or Dockerfile changes:

```bash
bash scripts/bundle/make_transfer_bundle.sh
```

## Corpus (v3 English-only)

Non-English books were removed (460 titles, ~2.7% of sentences). The bundle ships the OCTIS corpus, metadata, stoplist, and stratified fit/eval indices. Copy the three large sentence CSVs separately (~9 GB total) unless they are already on the target machine.

| Split | Sentences |
|-------|-----------|
| Train | 80,230,272 |
| Val   | 17,198,034 |
| Test  | 17,475,960 |

## What is in the bundle

- Docker build context: `Dockerfile`, `docker-compose.yml`, `requirements*.txt`, `src/`, `configs/`
- v3 legacy configs: `train_v3_mpnet.yaml`, `train_v3_minilm6.yaml`
- **v4 granular BO configs:** `train_v4_{mpnet,l6,l12}_granular_phase{1,3}.yaml`, `eval_select_granular.yaml`
- `scripts/stage03/run_v3_remote_model.sh` — CPU encode helper
- `scripts/stage03/run_v4_granular_remote.sh` — v4 granular BO (embeddings must exist locally)
- Pre-built OCTIS corpus under `data/interim/octis/v3_english_only/` (~8 GB)
- v3 subsampling metadata, filtering manifest, custom stoplist
- v3 fit/eval indices under `data/stage03_samples_v3/` (if generated before bundling)
- Drop folder for embedding caches: `data/interim/octis/v3_english_only/embeddings_cache/`

## Copy manually (too large for the bundle)

| File | Size | Needed for |
|------|------|------------|
| `data/raw/.../sentences_train.csv` | ~6.3 GB | First BO data scan |
| `data/raw/.../sentences_val.csv` | ~1.4 GB | Coherence eval (required for BO) |
| `data/raw/.../sentences_test.csv` | ~1.4 GB | Later stages only |
| `embeddings_cache/train_eval_...mpnet....npy` | ~280 GB | MPNet BO (skip if already on target) |

## Prerequisites (target machine)

- Linux, Docker Engine, user in the `docker` group (no sudo)
- **Encode:** CPU-only OK (weeks for MPNet full corpus)
- **v4 granular BO:** NVIDIA GPU + `nvidia-container-toolkit` (cuML UMAP/HDBSCAN)
- **No `.env`, API keys, or HF token** — Hub download disabled in bundled configs

## Quick start — MPNet v4 granular BO (embeddings already present)

```bash
cd transfer_bundle
docker build -t romance-stage03:latest .
chmod +x scripts/stage03/run_v4_granular_remote.sh

# Drop MPNet .npy into data/interim/octis/v3_english_only/embeddings_cache/ if not there yet.
# Ensure train+val CSVs and bundled OCTIS corpus / fit indices are in place.

./scripts/stage03/run_v4_granular_remote.sh mpnet phase1   # 160 calls, model_runs=1
# Re-run same command to resume after interrupt.
```

Phase 3 (after Phase 2 stability review on primary machine):

```bash
./scripts/stage03/run_v4_granular_remote.sh mpnet phase3   # 100 calls, model_runs=3
```

## Quick start — CPU encode only (no embeddings yet)

```bash
./scripts/stage03/run_v3_remote_model.sh sample          # once, if indices not bundled
./scripts/stage03/run_v3_remote_model.sh mpnet encode    # foreground; Ctrl+C to stop; re-run to resume
```

## v4 granular run IDs and configs

| Model | Hub name | Phase 1 run ID | Phase 1 config |
|-------|----------|----------------|----------------|
| MPNet | `paraphrase-mpnet-base-v2` | `v4_mpnet_granular_phase1` | `train_v4_mpnet_granular_phase1.yaml` |
| MiniLM-L6 | `paraphrase-MiniLM-L6-v2` | `v4_l6_granular_phase1` | `train_v4_l6_granular_phase1.yaml` |
| MiniLM-L12 | `all-MiniLM-L12-v2` | `v4_l12_granular_phase1` | `train_v4_l12_granular_phase1.yaml` |

Phase 1: 160 BO calls, `model_runs=1`, coarse search (incl. `hdbscan__cluster_selection_method`, integer `min_df`, no `min_topic_size`).

Phase 3: 100 BO calls, `model_runs=3`, narrowed search + topic stability gate.

Cache filenames (under `embeddings_cache/`):

| Model | Cache file | Approx. size |
|-------|------------|--------------|
| MPNet | `train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy` | ~280 GB |
| MiniLM-L6 | `train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy` | ~140 GB |
| MiniLM-L12 | `train_eval_sentence-transformers__all-MiniLM-L12-v2.npy` | ~140 GB |

Row count: **97,428,306** (train + val).

## Incremental update (target already has data)

If the other laptop already has OCTIS corpus, CSVs, and embeddings, **do not re-copy the full bundle**. Sync only the code layer (~100 MB):

```bash
rsync -av --delete \
  src/ configs/ scripts/ \
  Dockerfile docker-compose.yml .dockerignore \
  requirements.txt requirements-venv.txt Makefile README.md \
  user@other:/path/to/transfer_bundle/
```

Then on target: `docker build -t romance-stage03:latest .` and run BO.

## Resume behavior

Re-run the same command with the same run-id. Bind-mounted `data/`, `results/`, `logs/`, `models/` preserve checkpoints and `results/experiments/<run-id>/`.

## Notes

- First `docker build` is slow (RAPIDS + PyTorch wheels).
- Use `tmux` or `screen` for long BO runs over SSH.
- See `data/README.md` for the full data layout checklist.
