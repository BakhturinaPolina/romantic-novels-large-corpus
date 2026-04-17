# Stage 02: Preprocessing

Text preparation for downstream modeling: character-aware stoplist enrichment via BookNLP, plus a lightweight config CLI for future cleaning and segmentation work.

## Status

- **`extract_character_names_booknlp.py`** — implemented: builds per-work plain text from sentence CSVs, runs [BookNLP](https://github.com/booknlp/booknlp), extracts person-name phrases from `.book` and `.entities`, merges new lines into `custom_stoplist.txt` with a timestamped backup.
- **`main.py`** — placeholder CLI that prints configured paths (full sentence cleaning / token pipeline not implemented here yet).

## BookNLP: character names and stoplist

Runs on **`sentences_train.csv`** (or override). BookNLP expects a `.txt` input per work; the script materializes UTF-8 files under a timestamped run directory, then merges extracted surface forms into the custom stoplist used by later stages.

### Requirements

- Project `requirements.txt` (includes `booknlp`, `torch`, `spacy`, etc.).
- spaCy: `python -m spacy download en_core_web_sm`
- GPU: recommended for BookNLP `big` model; use `--require-gpu` to fail if CUDA is unavailable.

### Usage

From the project root:

```bash
python -m src.stage02_preprocessing.extract_character_names_booknlp --config configs/paths.yaml
```

Common options:

- `--dry-run` — only writes `txt_input/` and `manifest.json` under the run folder (no PyTorch import).
- `--run-id NAME` — fixed subdirectory under `booknlp_character_runs_parent` for resumable batches; omit for `run_<UTC_with_microseconds>/`.
- `--overwrite-run` — delete an existing `--run-id` directory before starting.
- `--sentences-csv PATH` — override [`configs/paths.yaml`](../../configs/paths.yaml) `inputs.sentences_train_csv`.
- `--no-merge-stoplist` — keep BookNLP outputs under `data/interim/` only; do not modify `data/processed/custom_stoplist.txt`.
- `--limit-books N`, `--work-ids 1,2,3`, `--max-rows N` — debugging and subsets.
- `--model big|small`, `--pipeline entity,quote,coref` (default) — BookNLP parameters; full notebook-style pipeline can add `supersense,event` via `--pipeline`.
- `--export-character-summary`, `--export-per-free-tokens`, `--also-nom-per`, `--flush-names-every K` — optional side outputs (see script `--help`).

Paths are configured under `inputs` in [`configs/paths.yaml`](../../configs/paths.yaml): `sentences_train_csv`, `booknlp_character_runs_parent`, `booknlp_model_path`, `custom_stoplist`.

### Run layout (under `data/interim/booknlp_character_runs/`)

| Artifact | Description |
|----------|-------------|
| `manifest.json` | Run metadata, work_ids, pipeline string |
| `txt_input/w{id}.txt` | One reconstructed book text per `work_id` |
| `booknlp_work.ckpt` | Completed `work_id` lines (resume) |
| `booknlp/w{id}/` | BookNLP outputs (`*.book`, `*.entities`, `*.tokens`, …) |
| `names_per_book.csv` | Per-book extraction stats (append; deduped by `work_id` on resume) |
| `all_names_so_far.txt` | Sorted union of name phrases (refreshed during run) |
| `merged_manifest.json` | Torch/CUDA, BookNLP version, stoplist merge counts |

Stoplist merge (default): backs up `custom_stoplist.txt` to `custom_stoplist.txt.bak_<timestamp>`, appends deduplicated new lines, and copies the merged file into the run directory.

## Config-only entrypoint

```bash
python -m src.stage02_preprocessing.main --config configs/paths.yaml
```

## Inputs and outputs (summary)

| Role | Path (from `configs/paths.yaml`) | Description |
|------|----------------------------------|-------------|
| Sentences (train) | `inputs.sentences_train_csv` | Rows: `work_id`, `chapter_*`, `sentence_index`, `sentence` |
| Stoplist | `inputs.custom_stoplist` | Grows with BookNLP-derived names + existing entries |
| BookNLP runs | `inputs.booknlp_character_runs_parent` | Timestamped or `--run-id` subfolders |
| Model cache | `inputs.booknlp_model_path` | Optional BookNLP weight downloads |

Legacy paths such as `chapters.csv` remain in `paths.yaml` for compatibility with older modeling entrypoints; the v2 sentence tables live under `romance_v2_sentences_dir`.

## Module structure

```
stage02_preprocessing/
├── main.py
├── extract_character_names_booknlp.py
└── README.md
```

## See also

- [Stage 01: sentence CSVs](../stage01_ingestion/README.md) — upstream EPUB → `sentences_*.csv`
- [Methodology report](../../results/reports/01_stage_reports/stage02_preprocessing/stage02_preprocessing_methodology.md) — research rationale (may predate BookNLP script; align with this README for tooling)
