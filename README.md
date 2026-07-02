# Romantic Novels NLP Research Pipeline

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Neural topic modeling pipeline for analyzing romance novels and correlating thematic patterns with Goodreads ratings.

**Research Question:** Which thematic patterns differentiate highly-rated romance novels from lower-rated ones?

## Quick Start

```bash
make stage01  # Ingest EPUBs → sentences
make stage02  # Extract character names → stoplist
make stage03  # Train BERTopic models
make all      # Full pipeline
```

## Installation

**Requirements:** Python 3.12+, CUDA 12.x GPU (~6GB VRAM)

```bash
git clone <repo-url> && cd romantic_novels_large_corpus
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-venv.txt
pip install --no-deps octis==1.14.0
python -m spacy download en_core_web_sm
```

Copy `.env.example` → `.env` and set `OPENROUTER_API_KEY` ([get one here](https://openrouter.ai/keys)).

Verify GPU: `python -m src.common.check_gpu_setup`

## Run on another GPU machine (Docker)

To run Stage03 on a second NVIDIA/CUDA-12.x box (e.g. to tune a different embedding model in parallel) without recreating the venv, build a self-contained transfer bundle:

```bash
bash scripts/bundle/make_transfer_bundle.sh   # → transfer_bundle/ (Dockerfile, code, configs, deps)
```

Ship `transfer_bundle/` to the target machine (plus the three sentence CSVs), then `cd transfer_bundle && docker build -t romance-stage03:latest .` and launch with `./scripts/run_v3_remote_model.sh` — **no `.env` setup required**. Docker assets live in [docker/](docker/); build from the repo root with `docker build -f docker/Dockerfile -t romance-stage03:latest .` if you are not using the bundle. Runs are **resumable**: `data/`, `results/`, `logs/`, and `models/` are bind-mounted, and re-running `tune` with the **same `--run-id`** continues from disk — skipping completed data loads, the OCTIS corpus, cached embeddings, and finished models, and resuming the Bayesian-optimization loop from the last completed call. Full instructions and copy-paste run blocks per model: [docker/README.md](docker/README.md).

### Stage03 stratified tuning (large corpus)

For the v2 sentence corpus (~100M rows), BERTopic fits on a **stratified 500k train subsample** and reuses precomputed full-corpus embeddings by index (no re-encoding):

```bash
# 1) Build fit/eval indices once (see docker/README.md for full args)
python -m src.stage03_train.cli sample --train-csv ... --val-csv ... \
  --out-dir data/stage03_samples --train-target 500000 --val-target 100000 --seed 42

# 2) Tune (uses configs/stage03/train_v3.yaml + configs/stage03/paths_stage03_fit_v3.yaml)
python -m src.stage03_train.cli tune --config configs/stage03/train_v3.yaml --run-id <run_id>
```

BO optimizes a **topic-count-penalized coherence** objective (`bo_objective` in `trials_partial.csv`); raw `coherence_c_v` and `n_topics` are logged per call. Stage 04 applies a `min_n_topics` floor before Pareto ranking. Design notes: [stage03_stratified_fit_sample_design.md](results/reports/stage03/stage03_stratified_fit_sample_design.md), [stage03_bertopic_search_space_prior.md](results/reports/stage03/stage03_bertopic_search_space_prior.md).

## Pipeline

| Stage | Name | Description |
|-------|------|-------------|
| 01 | Ingestion | EPUB corpus → sentence CSVs |
| 02 | Preprocessing | Character names → custom stoplist |
| 03 | Modeling | BERTopic + OCTIS hyperparameter optimization |
| 04 | Selection | Pareto-efficient model selection |
| 05 | Final Fit | Retrain winning model |
| 06 | Topic Exploration | Multi-representation analysis |
| 07 | Topic Quality | Noisy topic detection |
| 08 | LLM Labeling | Automated topic naming |
| 09 | Category Mapping | Romance taxonomy classification |
| 10 | Correlation | Statistical hypothesis testing |

## Dataset

17,514 romance EPUBs (2000–2017) from 8,828 authors. Train/val/test split: 12,259 / 2,627 / 2,628.

See `data/raw/romance_subdataset_downloaded_v2_full/SUBSAMPLING_V2.md` for cohort details.

## Documentation

- [SCIENTIFIC_README.md](SCIENTIFIC_README.md) — Methodology, hypotheses, results
- [Taxonomy v2.4 heuristic hardening](results/reports/stage09/taxonomy_v24_heuristic_hardening.md) — 6.1 split, sexual-function lock fix
- [configs/](configs/) — YAML configuration files
- [results/reports/](results/reports/) — Analysis reports

## License

[MIT](LICENSE)

## Citation

```bibtex
@software{romantic_novels_nlp,
  title = {Romantic Novels NLP Research Pipeline},
  author = {Polina},
  year = {2026}
}
```

## Acknowledgments

[BERTopic](https://github.com/MaartenGr/BERTopic) · [OCTIS](https://github.com/MIND-Lab/OCTIS) · [RAPIDS cuML](https://github.com/rapidsai/cuml) · [SentenceTransformers](https://www.sbert.net/)
