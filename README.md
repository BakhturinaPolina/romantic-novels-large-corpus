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
