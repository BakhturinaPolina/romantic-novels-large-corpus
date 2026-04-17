# Stage 01: Data Ingestion

EPUB-based ingestion for the **romance subsample downloaded v2** cohort: resolve on-disk EPUBs, extract chapter-ordered body text, segment sentences with spaCy, and write train / val / test sentence CSVs plus checkpoints for resume.

## Status

- **`parse_epub_corpus_to_sentence_csvs.py`** — primary implementation (v2 EPUB → sentence tables).
- **`main.py`** — small CLI that prints paths from `configs/paths.yaml` (no corpus I/O).

## v2 EPUB corpus → sentence CSVs

**Corpus root:** `data/raw/romance_subdataset_downloaded_v2_full/` — EPUBs under `{corpus_root}/{split}/{md5}.epub` with cohort definitions and mirrors in `subsampling_metadata/` (see `SUBSAMPLING_V2.md` in that directory).

### Requirements

- `EbookLib`, `beautifulsoup4`, `pandas`, `tqdm`, `spacy` (see project `requirements.txt`).
- spaCy English model: `python -m spacy download en_core_web_sm`

### Usage

From the project root:

```bash
python -m src.stage01_ingestion.parse_epub_corpus_to_sentence_csvs \
  --corpus-root data/raw/romance_subdataset_downloaded_v2_full \
  --metadata-dir data/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata \
  --output-dir data/processed/romance_subdataset_downloaded_v2_sentences \
  --spacy-model en_core_web_sm \
  --overwrite
```

Optional flags:

- `--limit N` — process only the first *N* rows per split (debug).
- `--workers K` — reserved; only single-process mode is implemented (`K` must be `1`).
- Omit `--overwrite` to **resume**: progress is tracked per split in `sentences_<split>.ckpt` (one `work_id` per line, written only after that book’s rows are flushed to disk). On startup, any sentence rows for `work_id` values not in the checkpoint are removed (the book that was in progress is re-parsed).

**Resume:** run the same command **without** `--overwrite`. Do not delete `sentences_*.ckpt` while a run is in progress.

**Checkpoint without `.ckpt` yet** (sentence file exists but no `.ckpt`): the first resume pass infers completed works from the CSV; if more than one `work_id` appears, the **last** `work_id` in file order is treated as possibly incomplete and dropped so it can be re-parsed. A single-work file cannot be distinguished this way; use `--overwrite` if that one work was partial.

### Outputs

Written to `--output-dir` (default `data/processed/romance_subdataset_downloaded_v2_sentences/`):

| File | Description |
|------|-------------|
| `sentences_train.csv` | One row per sentence, split **train′** |
| `sentences_val.csv` | Split **val′** |
| `sentences_test.csv` | Split **test′** |
| `sentences_train.ckpt`, `sentences_val.ckpt`, `sentences_test.ckpt` | Completed `work_id` values (resume checkpoints) |
| `parse_errors.csv` | Missing EPUBs, read failures, or empty extraction (`work_id`, `md5`, `epub_path`, `error`) |

### Row schema (sentence CSVs)

| Column | Description |
|--------|-------------|
| `work_id` | Join key to `romance_subdataset_downloaded_v2_{train,val,test,full}.csv` in `subsampling_metadata/` |
| `chapter_index` | Contiguous index (from 0) over spine XHTML documents that yielded non-empty body text |
| `chapter_title` | First non-empty `h1` / `h2` / `h3` text in that chapter’s HTML, else empty |
| `sentence_index` | 0-based index within `(work_id, chapter_index)` |
| `sentence` | Sentence text (spaCy sentencizer on flattened body text) |

### Processing notes

- Chapters follow **`book.spine`** order; each spine entry resolves to a manifest item via **id** or **href** fallback.
- Only `ITEM_DOCUMENT` items are used; `script` / `style` nodes are stripped before text extraction.
- Rows with no EPUB on disk are recorded in `parse_errors.csv` only (no sentence rows).

### Reference CLI (paths only)

```bash
python -m src.stage01_ingestion.main --config configs/paths.yaml
```

## Configured paths

v2 roots and sentence directory are listed under `inputs` in [`configs/paths.yaml`](../../configs/paths.yaml) (`romance_v2_corpus_root`, `romance_v2_subsampling_metadata_dir`, `romance_v2_sentences_dir`, `sentences_train_csv`, etc.). Aggregated Goodreads-style fields for the design frame live in the subsampling CSVs beside the EPUB cohort.

## Downstream

Sentence CSVs feed **Stage 02** (e.g. BookNLP character extraction on `sentences_train.csv`) and later topic-modeling stages. Character-name stoplist enrichment is implemented in [`../stage02_preprocessing/extract_character_names_booknlp.py`](../stage02_preprocessing/extract_character_names_booknlp.py), not in this stage.

## Module structure

```
stage01_ingestion/
├── main.py
├── parse_epub_corpus_to_sentence_csvs.py
└── README.md
```

## See also

- [Stage 02: preprocessing / BookNLP stoplist](../stage02_preprocessing/README.md)
- [Methodology report](../../results/reports/01_stage_reports/stage01_ingestion/stage01_data_ingestion_methodology.md) — research rationale and data decisions
