# Subdataset sampling: V1 design frame, code layout, and v2 downloaded corpus

This note ties together three artifacts:

1. **`src/subdataset_sampling/`** — Python utilities used to define subsamples, reconcile MD5s, prepare download lists, and (optionally) drive EPUB retrieval.
2. **`data/raw/subsampling_V1/`** — On-disk archive of the **~20k-book stratified design** (train / val / test + full cohort CSVs) produced for the romance pipeline.
3. **`data/raw/romance_subdataset_downloaded_v2_full/`** — **Primary text corpus**: EPUBs laid out by split, plus **`subsampling_metadata/`** mirroring the **downloaded v2** cohort tables and a machine-readable manifest.

Pipeline configuration references the v2 corpus root in `configs/paths.yaml` (`romance_v2_corpus_root`, `romance_v2_subsampling_metadata_dir`).

---

## 1. Code: `src/subdataset_sampling/`

| Module | Role |
|--------|------|
| `create_subdataset_flexible.py` | Stratified sampler (year bin × genre group × engagement tier × rating tier) with modes `inference` / `topic` / `hybrid`; time-ordered **train / val / test** split (default 70% / 15% / 15%, seed 42). Default write location documented in-code: `results/subsampling/` as `romance_subdataset_<N>_{full,train,val,test}.csv`. |
| `prepare_download_list.py` | Scans `results/subsampling/` for split files, merges MD5s from canonical inputs, compares against already-downloaded EPUBs, emits `books_to_download.csv` (and related bookkeeping). |
| `prepare_and_download.py` | Thin workflow: prepare list, then optionally invoke `src/search/download_parallel_direct.py`. |
| `verify_data_consistency.py` | Cross-checks identifiers and titles between subsampling outputs and legacy subset CSVs under `data/processed/`. |
| `run_subdataset_sampling.py` | Legacy entrypoint wired to a **6k-tier-balanced** sampler (`create_subdataset_6000`); kept for older workflows. Prefer `create_subdataset_flexible.py` for the 20k design. |

**Design intent (flexible sampler):** cap corpus size (~20k), reduce pure “most reviewed” bias while keeping enough review text for topic modeling, and hold out **later publication years** for test when using the time split.

---

## 2. Archived design tables: `data/raw/subsampling_V1/`

These files are the **V1 subsampling design** snapshot (stratified ~20k draw + splits), stored under `data/raw/` for stability and clear versioning alongside raw data.

| File | Rows (incl. header) | Approx. works |
|------|---------------------|---------------|
| `romance_subdataset_20000_full.csv` | 20,001 | 20,000 |
| `romance_subdataset_20000_train.csv` | 14,001 | 14,000 |
| `romance_subdataset_20000_val.csv` | 3,001 | 3,000 |
| `romance_subdataset_20000_test.csv` | 3,001 | 3,000 |

Representative columns include: `work_id`, `title`, `author_id`, `publication_year`, Goodreads aggregates (`ratings_count_sum`, `text_reviews_count_sum`, `average_rating_weighted_mean`), `genres_str`, and stratification labels such as `genre_group`, `year_bin`, `engagement_tier`, `rating_tier`.

The **v2 downloaded cohort** was derived from this design frame: works with a resolvable MD5 and at least one EPUB retrieved (see manifest below). Not every design-row has a matching on-disk EPUB, so the downloaded cohort is a **strict subset** of the 20k design.

---

## 3. Downloaded corpus: `data/raw/romance_subdataset_downloaded_v2_full/`

### Layout

- **EPUBs** under `{corpus_root}/{split}/` using the MD5-based naming expected by Stage 01 ingestion (`parse_epub_corpus_to_sentence_csvs.py`).
- **`subsampling_metadata/`** — Cohort tables aligned with the download pass:
  - `romance_subdataset_downloaded_v2_full.csv`
  - `romance_subdataset_downloaded_v2_{train,val,test}.csv`
  - `romance_subdataset_downloaded_v2_manifest.json`

### Manifest summary (`romance_subdataset_downloaded_v2_manifest.json`)

Values below are taken from the manifest checked into the workspace (creation time 2026-04-16 UTC). Absolute paths inside the JSON point to the machine where the cohort was built; the **logical** design input is the same **`romance_subdataset_20000_full.csv`** family as in `subsampling_V1/`.

| Field | Value |
|-------|--------|
| `cohort_n` | 17,514 |
| `on_disk_unique_md5_count` | 19,969 |
| `split_strategy` | `time` |
| `train_frac` / `val_frac` / `seed` | 0.7 / 0.15 / 42 |
| `n_train_v2` / `n_val_v2` / `n_test_v2` | 12,259 / 2,627 / 2,628 |

Row counts in `subsampling_metadata/` CSVs (including header) match **n + 1** for each split and the full table.

**Interpretation:** **`romance_subdataset_downloaded_v2_full`** is the **operational** corpus for Stages 01–03: EPUBs plus metadata for the **17,514** works in the v2 cohort (`cohort_n`). The manifest also records **`on_disk_unique_md5_count`** (19,969 in this export): a scan-level count under the download root, which can differ from `cohort_n` depending on how duplicates, non-EPUB artifacts, and cohort filters were applied when the manifest was written (`matched_only`: false in the checked-in file).

---

## 4. Downstream pointers

- **Sentence extraction:** `data/processed/romance_subdataset_downloaded_v2_sentences/` (`sentences_{train,val,test}.csv`) — produced from the v2 EPUB tree; see `src/stage01_ingestion/README.md`.
- **Power analysis write-up:** [`stage11_power_analysis_report.md`](stage11_power_analysis_report.md) (this folder).

For methodology and hypotheses tied to the v2 scale, see **`SCIENTIFIC_README.md`** at the repository root.
