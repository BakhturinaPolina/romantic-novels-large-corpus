# Stage 02: Preprocessing

Text preparation for downstream modeling: character-aware stoplist enrichment via BookNLP, plus a lightweight config CLI for future cleaning and segmentation work.

## Status

- **`extract_character_names_booknlp.py`** — implemented: builds per-work plain text from sentence CSVs, runs [BookNLP](https://github.com/booknlp/booknlp), extracts person-name phrases (default fast path from `.entities`), merges new lines into `custom_stoplist.txt` with a timestamped backup.
- **`main.py`** — placeholder CLI that prints configured paths (full sentence cleaning / token pipeline not implemented here yet).

## BookNLP: character names and stoplist

Runs on **`sentences_train.csv`** (or override). BookNLP expects a `.txt` input per work; the script materializes UTF-8 files under a timestamped run directory, then merges extracted surface forms into the custom stoplist used by later stages.

The txt materialization step now streams the CSV incrementally (chunked ingestion + append writes), so it no longer builds one giant in-memory table first.

Default execution is now **fast entity-only mode**:
- `--pipeline entity` (default)
- `--model small` (default)

You can still opt into richer but slower outputs with `--pipeline entity,quote,coref`.

### Requirements

- Project `requirements.txt` (includes `booknlp`, `torch`, `spacy`, etc.).
- spaCy: `python -m spacy download en_core_web_sm`
- GPU: recommended for BookNLP `big` model; use `--require-gpu` to fail if CUDA is unavailable.

### Usage

From the project root:

```bash
python -m src.stage02_preprocessing.extract_character_names_booknlp --config configs/paths.yaml
```

Fast spaCy alternative (`.venv`) for quick stoplist generation:

Quick probe (small sample, no stoplist merge):

```bash
.venv/bin/python -m src.stage02_preprocessing.extract_character_names_spacy_fast \
  --config configs/paths.yaml \
  --max-rows 20000 \
  --limit-books 200 \
  --no-merge-stoplist
```

Full extraction (train split, merges into `custom_stoplist.txt`):

```bash
.venv/bin/python -m src.stage02_preprocessing.extract_character_names_spacy_fast \
  --config configs/paths.yaml
```

**Full corpus timing (train split):** ~82.1M sentences / ~11,429 books. At ~400–800 sentences/s with `n_process=4`, expect **~29–57 hours** total. Use a fixed `--run-id` and resume in night batches (see below).

**Resumable full run (recommended for overnight batches):**

```bash
# Night batch 1 (example: ~200 chunks ≈ 20M rows, ~1–3 h depending on hardware)
.venv/bin/python -m src.stage02_preprocessing.extract_character_names_spacy_fast \
  --config configs/paths.yaml \
  --run-id spacy_fast_full \
  --n-process 4 \
  --max-chunks-per-run 200

# Next nights: same --run-id, auto-resumes from checkpoint
.venv/bin/python -m src.stage02_preprocessing.extract_character_names_spacy_fast \
  --config configs/paths.yaml \
  --run-id spacy_fast_full \
  --resume \
  --n-process 4 \
  --max-chunks-per-run 200
```

Incremental artifacts under `data/interim/booknlp_character_runs/<run-id>/`:
- `spacy_state.json` — aggregate token counts (flushed every `--flush-every-chunks`, default 5)
- `spacy_chunk.ckpt` — last completed chunk index + rows scanned
- `all_names_so_far.txt` — current filtered token list (updated on flush)
- `run_summary.json` — `complete: false` until the full CSV is processed

When the CSV is fully scanned, the script writes `names_per_book.csv` and merges `custom_stoplist.txt`. If extraction finished earlier without merge, run:

```bash
.venv/bin/python -m src.stage02_preprocessing.extract_character_names_spacy_fast \
  --config configs/paths.yaml \
  --run-id spacy_fast_full \
  --merge-stoplist-only
```

**Val and test splits** (merge new tokens into the same `custom_stoplist.txt`):

Train is already in `spacy_fast_full/`. Run val then test with separate run dirs (~18M sentences each, ~6–10 h per split at typical speed):

```bash
# Validation split
PYTHONUNBUFFERED=1 .venv/bin/python -m src.stage02_preprocessing.extract_character_names_spacy_fast \
  --config configs/paths.yaml \
  --split val \
  --run-id spacy_fast_val \
  --n-process 4 \
  --max-chunks-per-run 200 \
  --heartbeat-every-docs 5000 \
  --flush-every-chunks 1

# Held-out test split (add --resume on later nights if batched)
PYTHONUNBUFFERED=1 .venv/bin/python -m src.stage02_preprocessing.extract_character_names_spacy_fast \
  --config configs/paths.yaml \
  --split test \
  --run-id spacy_fast_test \
  --n-process 4 \
  --max-chunks-per-run 200 \
  --heartbeat-every-docs 5000 \
  --flush-every-chunks 1
```

Artifacts: `data/interim/booknlp_character_runs/spacy_fast_val/` and `spacy_fast_test/`. Each completed run appends deduplicated tokens to `data/processed/custom_stoplist.txt`.

### Audit likely non-name stoplist entries

Use this helper after a merge to review likely lexical words (non-names) that slipped into the stoplist.
By default it audits only the newest additions: `custom_stoplist.txt - custom_stoplist.txt.bak_20260520_080905`.

```bash
.venv/bin/python src/stage02_preprocessing/scripts/audit_stoplist_non_names.py \
  --target-delta new \
  --zipf-threshold 4.0 \
  --top-n 100
```

Output:
- Writes CSV to `data/processed/stoplist_non_name_audit_<timestamp>.csv`.
- Prints top `likely_non_name` suspects to stdout.

Interpretation:
- `looks_like_common_word=true` means high common-word frequency (`wordfreq` Zipf >= threshold).
- `spacy_person_in_context=false` (when `--enable-spacy-probe`) means spaCy does not recognize the token as a person in a simple context.
- Start manual review with rows where `likely_non_name=true`.

Common options:

- `--dry-run` — only writes `txt_input/` and `manifest.json` under the run folder (no PyTorch import).
- `--run-id NAME` — fixed subdirectory under `booknlp_character_runs_parent` for resumable batches; omit for `run_<UTC_with_microseconds>/`.
- `--overwrite-run` — delete an existing `--run-id` directory before starting.
- `--sentences-csv PATH` — override [`configs/paths.yaml`](../../configs/paths.yaml) `inputs.sentences_train_csv`.
- `--no-merge-stoplist` — keep BookNLP outputs under `data/interim/` only; do not modify `data/processed/custom_stoplist.txt`.
- `--limit-books N`, `--work-ids 1,2,3`, `--work-ids-file PATH`, `--max-rows N` — debugging, subsets, and shard execution.
- `--streaming`, `--chunk-size N` — control CSV chunk ingestion behavior for txt build (pipeline is incremental by default).
- `--model big|small` (default `small`), `--pipeline ...` (default `entity`) — BookNLP parameters.
- `--export-character-summary`, `--export-per-free-tokens`, `--also-nom-per`, `--flush-names-every K` — optional side outputs (see script `--help`).
- `--log-file NAME`, `--no-progress` — configure persistent log filename under `outputs.logs` (`logs/` by default) and disable tqdm progress bar when needed.
- `--estimate-eta --eta-sample-books N --eta-seed S` — benchmark a sample of books and save projected runtime to `eta_estimate.json`.
- `--eta-resume` — skip ETA books that already have valid `eta_sample` artifacts.
- `--txt-input-dir PATH` — reuse prebuilt `txt_input` (skip ~10 min full-corpus txt rebuild).
- `--stoplist-sample-books N [--stoplist-sample-seed S]` — process only `N` books stratified by txt length (recommended on single GPU).
- `--plan-shards --num-shards N [--start-shard I --end-shard J] [--print-only]` — generate balanced shard files and ready-to-run shard commands.

Paths are configured under `inputs` in [`configs/paths.yaml`](../../configs/paths.yaml): `sentences_train_csv`, `booknlp_character_runs_parent`, `booknlp_model_path`, `custom_stoplist`.
Run logs are also written to `outputs.logs` from [`configs/paths.yaml`](../../configs/paths.yaml) (defaults to `logs/`, gitignored).

### Run layout (under `data/interim/booknlp_character_runs/`)

| Artifact | Description |
|----------|-------------|
| `manifest.json` | Run metadata, work_ids, pipeline string |
| `txt_input/w{id}.txt` | One reconstructed book text per `work_id` |
| `booknlp_work.ckpt` | Completed `work_id` lines (resume) |
| `booknlp/w{id}/` | BookNLP outputs (`*.book`, `*.entities`, `*.tokens`, …) |
| `names_per_book.csv` | Per-book extraction stats (append; deduped by `work_id` on resume) |
| `all_names_so_far.txt` | Sorted union of name phrases (refreshed during run) |
| `run_summary.json` | Runtime counters, latency stats, slowest books, failed `work_id` reasons |
| `failed_work_ids.csv` | Tabular list of failures and reason codes (when failures occur) |
| `eta_estimate.json` | Runtime projection generated by `--estimate-eta` |
| `shards/work_ids_shard_*.txt` | Work-id lists generated by `--plan-shards` |
| `merged_manifest.json` | Torch/CUDA, BookNLP version, stoplist merge counts |

Stoplist merge (default): backs up `custom_stoplist.txt` to `custom_stoplist.txt.bak_<timestamp>`, appends deduplicated new lines, and copies the merged file into the run directory.

## Monitoring and bottleneck tracking

- Terminal: timestamped log lines plus a tqdm progress bar over `work_id` processing.
- Persistent logs: each run writes to `logs/stage02_booknlp_<run_id>.log` unless overridden via `--log-file`.
- Per-book timing: BookNLP runtime is tracked and summarized in `run_summary.json` (`avg`, `median`, top slowest books).
- Failure accounting: missing txt/artifact issues are recorded with reason codes and saved for post-run triage.

## Parallel sharding recipes

Plan shards (example: 4 workers):

```bash
python -m src.stage02_preprocessing.extract_character_names_booknlp \
  --config configs/paths.yaml \
  --run-id train_stage02 \
  --plan-shards \
  --num-shards 4
```

Run shard 0 on GPU 0:

```bash
CUDA_VISIBLE_DEVICES=0 python -m src.stage02_preprocessing.extract_character_names_booknlp \
  --config configs/paths.yaml \
  --run-id train_stage02_shard_000 \
  --work-ids-file data/interim/booknlp_character_runs/train_stage02/shards/work_ids_shard_000.txt \
  --shard-index 0 \
  --shard-count 4
```

Repeat for shard indices `1..3` (different GPUs or machines).

## ETA estimation

Estimate runtime from a sampled subset:

```bash
python -m src.stage02_preprocessing.extract_character_names_booknlp \
  --config configs/paths.yaml \
  --run-id train_eta_probe \
  --estimate-eta \
  --eta-sample-books 50
```

The script prints mean/median runtime and full-corpus confidence range, and writes `eta_estimate.json` in the run directory.

Reuse existing texts (fast):

```bash
.venv/bin/python -m src.stage02_preprocessing.extract_character_names_booknlp \
  --config configs/paths.yaml \
  --run-id train_stage02_eta50 \
  --estimate-eta --eta-sample-books 50 --eta-resume \
  --txt-input-dir data/interim/booknlp_character_runs/train_stage02_eta50/txt_input \
  --no-merge-stoplist
```

## Stratified stoplist sample (single-GPU friendly)

When full-corpus BookNLP would take weeks on one GPU, sample by length then shard:

```bash
# Plan 2 shards x 750 books = 1500 total (example)
.venv/bin/python -m src.stage02_preprocessing.extract_character_names_booknlp \
  --config configs/paths.yaml \
  --run-id train_stoplist_sample_1500 \
  --plan-shards --num-shards 2 \
  --stoplist-sample-books 1500 \
  --txt-input-dir data/interim/booknlp_character_runs/train_stage02_eta50/txt_input

# Or wait for ETA then auto-plan+run:
bash src/stage02_preprocessing/scripts/wait_eta_then_stoplist_sample.sh 1500 2
```

Writes `stoplist_sample_manifest.json` with bin counts and selected `work_id`s.

## Runtime estimates (train corpus)

<!-- ETA-RUNTIME-START -->

Measured on **RTX 2070 Max-Q**, `entity` + `small`, `sentences_train.csv` (~11,429 `work_id`s with prebuilt `txt_input`).

**Status:** 50-book ETA in progress (`train_stage02_eta50`). Early samples (2 books) averaged **~205 s/book** (~3.4 min), driven by long books (e.g. 67k–95k words).

| Metric | Early partial (n=2) | Interpretation |
|--------|---------------------|----------------|
| Mean | ~205 s/book | Full corpus ≈ **650+ h (~27 d)** on 1 GPU if typical |
| Median | TBD (see `eta_estimate.json`) | If **30–60 s** → ~4–8 d full corpus may be feasible |
| Decision | **Use `--stoplist-sample-books 1500`** | ~**85 h (~3.5 d)** at early mean; refine after ETA completes |

When `data/interim/booknlp_character_runs/train_stage02_eta50/eta_estimate.json` exists, compare `runtime_median_s` vs `runtime_mean_s` and `projected_full_corpus_hours` (95% CI). If mean stays **≥180 s/book**, prefer stratified sampling or external GPU; do not commit to full 11k-book run on one card without that check.

<!-- ETA-RUNTIME-END -->

## Recommended train-first workflow

1. Run Stage02 on `sentences_train.csv` first and merge stoplist updates.
2. Validate topic quality and only then decide whether to process `val/test`.
3. Keep split artifacts separate (`all_names_train.txt`, `all_names_val.txt`, `all_names_test.txt`) and optionally publish a union list (`all_names_union.txt`) for production convenience.

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
