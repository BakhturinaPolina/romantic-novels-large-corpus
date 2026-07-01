# Stage 03 Stratified Fit Sample: Design and Rationale

**Component:** `src/stage03_train/make_fit_sample.py` (selector), `src/stage03_train/tune.py` (consumer)
**Configuration:** `configs/legacy/train.yaml`, `configs/legacy/paths_stage03_fit.yaml`
**Artifacts:** `data/stage03_samples/fit_indices_seed42.npy`, `eval_indices_seed42.npy`, `sample_manifest_seed42.json`
**Status:** Draft for the methods section of the topic-modeling paper. Index selection completed 2026-06-04 (see `data/stage03_samples/sample_manifest_seed42.json`).

This note documents how Stage 03 chooses the documents on which BERTopic is *fit*, why that choice is stratified rather than random, and how it reuses the existing full-corpus embeddings instead of re-encoding.

---

## 1. Problem: what should the fit corpus be?

The operational corpus is the v2 cohort of **17,514 romance works** (see [`subdataset_sampling_v1_design_and_v2_downloaded_corpus.md`](subdataset_sampling_v1_design_and_v2_downloaded_corpus.md)), parsed to sentence splits of roughly **82M train** and **17.7M val** rows (`data/processed/romance_subdataset_downloaded_v2_sentences/`). BERTopic cannot fit UMAP + HDBSCAN on ~100M points on a single GPU, so the model is **fit on a bounded subsample and then `.transform()`-ed onto the rest**. The subsample size cap is therefore a *clustering* constraint (GPU memory), not an *embedding* constraint.

The question this report answers is **which** ~500,000 sentence rows become the fit corpus.

### 1.1 Why not a global random sample

A uniform random draw of 500k sentences over the combined corpus is biased toward whatever is numerically dominant:

- **Long books** contribute proportionally more sentences, so a handful of long titles can flood the fit set.
- **Prolific authors** (large back-catalogues) are over-represented.
- **Common publication years** (2000-2017 is uneven) dominate.
- **Narrative position** is uncontrolled: opening/description sentences are plentiful, while climax/resolution passages are comparatively rare, so a random draw skews toward book openings.

For a heterogeneous literary corpus this distorts the learned topic space toward the styles of a few long/prolific/recent books.

### 1.2 Why the fit size does not limit the study

The downstream inference (see [`stage11_power_analysis_report.md`](stage11_power_analysis_report.md)) needs **6,000-12,000 books** with topic features to detect quality/reach effects. That requirement is satisfied independently of the fit-sample size: **every** book is assigned topics at `.transform()` time. The 500k fit sample only determines what the model is *trained on*, not how many books enter the analysis.

```mermaid
flowchart LR
  Full["Full corpus ~100M sentences, 17,514 books"]
  Fit["Fit sample 500k stratified train sentences"]
  Model["BERTopic model embedding to UMAP to HDBSCAN to topics"]
  All["Transform ALL sentences of ALL books"]
  Feat["Book-level topic features for 17,514 books"]
  Infer["Power-justified inference 6k to 12k books"]
  Full --> Fit --> Model --> All --> Feat --> Infer
```

---

## 2. Sampling design

The selector draws a **book-balanced, year-aware, author-capped** sample that also spreads rows across **narrative position**.

| Sampling axis | Why it matters | Mechanism |
|---------------|----------------|-----------|
| Book | Prevents long books from flooding the sample | Per-book quota with min/max bounds |
| Narrative position | Captures openings, development, conflict, climax, resolution | 5 within-book position bins from `sentence_index` |
| Publication year | Avoids over-representing common years | Year carried per book; outer stratification axis |
| Author | Stops prolific authors from dominating | Per-author cap after book sampling |
| Genre group | Recorded for audit/coverage | Joined from metadata, logged in manifest |

### 2.1 Quota arithmetic

With ~12,259 training books and a 500,000-row target, the average is

```
500,000 / 12,259  ~  41 rows per book
```

So the sampler does **not** sample purely per-sentence. The per-book quota is

```
per_book_quota = clip( floor(target / n_books), min_rows_per_book, max_rows_per_book )
```

with `min_rows_per_book = 10`, `max_rows_per_book = 80` for the train fit, and the quota is spread across `position_bins = 5` so each book contributes from beginning, middle, and end. The val (coherence) sample uses tighter bounds (`min 5`, `max 40`, `max_rows_per_author 300`) for its 100,000-row target.

### 2.2 Metadata join

The sentence CSVs contain only `work_id, chapter_index, chapter_title, sentence_index, sentence` -- no author or year. `author_name`, `publication_year`, and `genre_group` are joined by `work_id` from the cohort tables under `data/raw/romance_subdataset_downloaded_v2_full/subsampling_metadata/`. Missing joins degrade to `unknown_author` / `unknown_year`, so the selector still runs on fixtures without metadata.

---

## 3. Algorithm (memory-bounded, two streaming passes)

The full train split is ~6.5 GB, so the selector never loads a split into memory. For each split:

1. **Pass 1 (`_book_stats_pass`)** streams the CSV in `chunk_size` chunks, applies `clean_sentence`, drops empty rows, and records per-book `count` and `max(sentence_index)`. It also returns `n_clean` (the partition size in the global index space).
2. **Pass 2 (`select_stratified_indices`)** streams again, assigns each surviving row a 0-based global index, computes its position bin, and performs **reservoir sampling per `(work_id, position_bin)` stratum** up to the per-bin cap. A parallel global reservoir of size `target` supports later top-up.
3. **Post-passes** trim each book to its quota, enforce the per-author cap, top up from the global reservoir if author caps left the sample short, and downsample to the exact target.

Memory stays bounded by the reservoirs (~`target` records, integer indices plus small metadata), not by the corpus size.

---

## 4. Output: indices, not new CSVs

The key design decision: the selector emits **row indices into the full train->eval corpus**, not new sentence CSVs.

- `fit_indices_seed42.npy` -- indices into the **train partition** `[0, n_train)`.
- `eval_indices_seed42.npy` -- indices into the **val partition** `[n_train, n_train + n_val)` (offset by `n_train`).
- `sample_manifest_seed42.json` -- counts, per-axis histograms, parameters, and `n_train_clean` / `n_val_clean` / `n_total_clean`.

### 4.1 Index alignment invariant

Both the per-model embedding cache (`train_eval_<model>.npy`) and the OCTIS `corpus.tsv` are built by `iter_split_csv_chunks` in **train-then-eval order**, applying `clean_sentence` and dropping empty rows (`src/stage03_train/embeddings.py`, `src/stage03_train/octis_corpus.py`). The selector iterates the **same CSVs with the same cleaning and order**, so global index `i` denotes the same row in all three artifacts. This is the same invariant the legacy random subsample already relied on (`embeddings[fit_indices]` and `doc_store.fetch_documents(fit_indices)` share one index space).

At run time `tune.py` asserts `embeddings.shape[0] == len(doc_store)` to catch any misalignment before fitting.

### 4.2 Train-only fit via the partition boundary

The fit uses the **train partition only**: `_prepare_bertopic_fit_data` restricts `fit_indices` to `[0, n_train)` (the boundary read from corpus metadata, `last-training-doc`). The val partition is reserved for coherence evaluation, which uses `eval_indices` to gather a **stratified** 100k val sample from the disk-backed store instead of the sequential head of the val CSV.

---

## 5. Embedding reuse (no re-encoding)

Because the fit set is expressed as indices into the full corpus, Stage 03 reuses the existing **full-corpus** embedding `.npy` for each model and gathers `embeddings[fit_indices]`. No sentences are re-encoded for tuning.

- `configs/legacy/train.yaml -> embeddings_cache.overrides` maps each model to its full `train_eval_*.npy` (run-id path convention `data/interim/octis/<run_id>/embeddings_cache/`).
- `configs/legacy/paths_stage03_fit.yaml -> inputs.octis_corpus_dir` points at a prebuilt full `corpus.tsv` so a fresh run skips the ~100M-row corpus rewrite.

This matters because the full embeddings are the expensive artifact (the MiniLM-L12 cache alone is ~143 GB / ~99.8M rows, days of GPU time). They are not made redundant by the fit sample; they are exactly what the eventual full-corpus `.transform()` consumes downstream.

---

## 6. Reproducibility

| Field | Value |
|-------|-------|
| Seed (train fit) | 42 |
| Seed (val eval) | 43 (`seed + 1`) |
| Train target | 500,000 |
| Val target | 100,000 |
| `n_train_clean` | 82,114,042 |
| `n_val_clean` | 17,709,782 |
| `n_total_clean` | 99,823,824 |
| Books sampled (train) | 11,429 (all train books represented in quota) |
| Authors sampled (train) | per manifest `n_authors_sampled` |
| Fit index range | `[13, 82,114,034]` ⊆ train partition `[0, 82,114,042)` |
| Eval index range | `[82,114,047, 99,823,820]` ⊆ val partition |

Re-running with the same seed and the same input CSVs reproduces the index files exactly. The manifest records all caps and per-axis histograms for audit.

---

## 7. Relationship to the Stage 01 corpus design

The Stage 01 subsampling (`subdataset_sampling_v1_design_and_v2_downloaded_corpus.md`) is a **book-level, time-stratified** design (year bin x genre group x engagement tier x rating tier; 70/15/15 time split). This Stage 03 fit sample is a **sentence-level** design *within* the train split, addressing a different failure mode (per-sentence dominance) at a different stage (model fitting). They are complementary: Stage 01 fixes which books are studied; Stage 03 fixes which sentences train the topic model.

---

## 8. Operational notes and downstream

- Build indices once with `python -m src.stage03_train.make_fit_sample ...` (or `python -m src.stage03_train.cli sample ...`). Use `--progress-every 5000000` (default) for `tail -f` visibility; after pass 1 completes, `--resume` skips the stats scan on restart (pass 2 still re-streams from the start).
- Tuning consumes the indices via `configs/legacy/paths_stage03_fit.yaml`; `run_manifest.json` records `fit_indices_file`, `eval_indices_file`, `octis_corpus_dir`, and the `embeddings_overrides` actually used.
- **Stage 05 / full-corpus transform (future):** after a winner is selected, build full-corpus embeddings only for the winning model (or reuse the existing cache if MiniLM-L12 wins) and `.transform()` all sentences to produce the book-level topic features for the power-justified inference. This keeps a single coherent topic space and pays for at most one full-corpus embedding pass.

See also: [`stage03_bertopic_search_space_prior.md`](stage03_bertopic_search_space_prior.md) for the hyperparameter search-space justification.
