# Romantic Novels NLP Research Pipeline

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A computational research pipeline for analyzing romantic novels using neural topic modeling (BERTopic), LLM-based labeling, and statistical correlation with reader appreciation metrics from Goodreads.

## Primary corpus

**Dataset:** `romance_subdataset_downloaded_v2_full` under **`data/raw/romance_subdataset_downloaded_v2_full/`**.

- **17,514** romance works with verified **EPUB** on disk (cohort from the ~20k design frame; see `subsampling_metadata/romance_subdataset_downloaded_v2_manifest.json` and `SUBSAMPLING_V2.md` in that directory).
- **8,828** distinct authors; publication years **2000–2017** in the current export; time-based **train / val / test**: 12,259 / 2,627 / 2,628.
- Subsample metadata and mirrors of the v2 CSVs: **`data/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata/`**.

Earlier documentation referred to a **retired smaller convenience-sample corpus**; this repository’s main corpus is the v2 full cohort above unless a notebook or report explicitly says otherwise. Downstream sentence counts, matched-book counts, and rating-tier summaries for the v2 run are **`[TBD]`** until stages are re-executed on the new texts.

## Research Question

> Which thematic patterns differentiate highly-rated romance novels from lower-rated ones, and how do these patterns relate to reader appreciation metrics?

## Key Features

- **Neural Topic Modeling**: BERTopic with OCTIS Bayesian hyperparameter optimization
- **GPU Acceleration**: Mandatory RAPIDS cuML (CUDA 12.x) for UMAP and HDBSCAN
- **LLM Topic Labeling**: Automated labeling via OpenRouter API (Mistral-Nemo)
- **Theory-Aligned Categories**: Zero-shot classification to romance taxonomy and Radway narrative functions
- **Statistical Analysis**: Correlation with Goodreads ratings using bootstrap inference

## Installation

### Prerequisites

- Python 3.12+
- CUDA-compatible GPU with CUDA 12.x drivers
- ~6GB VRAM (for quantized LLM inference)

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/romantic_novels_large_corpus.git
cd romantic_novels_large_corpus

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY` (required for Stage 08 LLM labeling and Stage 09 taxonomy/Radway). Get a key at https://openrouter.ai/keys.

Verify GPU setup:
```bash
python -m src.common.check_gpu_setup
```

## Quick Start

```bash
# Run individual stages
make stage01  # Data ingestion
make stage02  # Preprocessing
make stage03  # BERTopic training with OCTIS optimization

# Run full pipeline
make all
```

Or run stages directly:
```bash
python -m src.stage01_ingestion.main --config configs/paths.yaml
python -m src.stage03_modeling.main train --config configs/bertopic.yaml
```

## Documentation

| Resource | Description |
|----------|-------------|
| [SCIENTIFIC_README.md](SCIENTIFIC_README.md) | Full methodology, hypotheses, and results |
| [reports/](reports/) | Stage-by-stage technical reports and findings |
| [configs/](configs/) | YAML configuration files |

## Project Structure

```
romantic_novels_large_corpus/
├── src/                    # Source code (stages 01-10)
├── configs/                # YAML configuration files
├── notebooks/              # Jupyter notebooks by stage
├── data/                   # Raw, interim, processed data
├── results/                # Pipeline outputs
├── reports/                # Technical reports and findings
├── models/                 # Trained BERTopic models
└── scripts/                # Utility scripts
```

## Pipeline Overview

| Stage | Name | Description |
|-------|------|-------------|
| 01 | Ingestion | Load novels and Goodreads metadata |
| 02 | Preprocessing | Text cleaning, tokenization, character name removal |
| 03 | Modeling | BERTopic training with OCTIS optimization |
| 04 | Selection | Pareto-efficient model selection |
| 05 | Retraining | Retrain top models |
| 06 | Topic Exploration | Multi-representation topic analysis |
| 07 | Topic Quality | Noisy topic detection |
| 08 | LLM Labeling | Automated topic labeling |
| 09 | Category Mapping | Theory-aligned taxonomy classification |
| 10 | Correlation Analysis | Statistical hypothesis testing |

See [SCIENTIFIC_README.md](SCIENTIFIC_README.md) for detailed stage documentation.

## Configuration

All settings are in `configs/`:

- `paths.yaml` — Data directories
- `bertopic.yaml` — BERTopic parameters
- `octis.yaml` — Hyperparameter search space
- `selection.yaml` — Model selection criteria
- `labeling.yaml` — LLM labeling settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guidelines
4. Submit a pull request

## License

[MIT License](LICENSE)

## Citation

```bibtex
@software{romantic_novels_nlp,
  title = {Romantic Novels NLP Research Pipeline},
  author = {Polina},
  year = {2025},
  url = {https://github.com/YOUR_USERNAME/romantic_novels_large_corpus}
}
```

## Acknowledgments

- [BERTopic](https://github.com/MaartenGr/BERTopic) — Topic modeling
- [OCTIS](https://github.com/MIND-Lab/OCTIS) — Hyperparameter optimization
- [RAPIDS cuML](https://github.com/rapidsai/cuml) — GPU acceleration
- [SentenceTransformers](https://www.sbert.net/) — Embeddings
- [Mistral](https://mistral.ai/) — LLM labeling
