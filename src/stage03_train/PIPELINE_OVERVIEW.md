# BERTopic Train / Eval / Test Pipeline Overview

This document describes the new BERTopic workflow in simple words.

The idea is:

- **Training stage** = model-building lab. We try embeddings + Bayesian tuning here.
- **Eval stage** = model selection gate. We choose the winner using the validation split.
- **Test stage** = final exam. We run once on held-out test and freeze results.

We keep `sentences_val.csv` filename, but treat it as the **eval** split by role.

## Folder Structure

- `src/stage03_train/` → build candidates on train, score candidates on eval.
- `src/stage04_eval_select/` → Pareto-then-weighted selection.
- `src/stage05_final_fit/` → refit selected winner (train-only and train+val artifacts).
- `src/stage05b_test_holdout/` → one-shot final holdout scoring on test.

---

## Stage 03 (Train): Scripts and Responsibilities

### `data_io.py`

**What it does**
- Reads Stage 01 sentence CSVs with the real schema:
  - `work_id, chapter_index, chapter_title, sentence_index, sentence`
- Cleans text (newline/whitespace normalization + lowercase).
- Returns both raw docs and tokenized docs.

**Inputs**
- `sentences_train.csv`
- `sentences_val.csv`

**Outputs**
- In-memory:
  - `docs_train`, `tokens_train`
  - `docs_val`, `tokens_val`
  - label arrays for traceability (`work_id`-based)

**Kept from legacy**
- Text cleanup logic from old `src/stage03_modeling/bertopic_runner.py`.

**Added**
- Correct handling of 5-column Stage 01 schema.
- Explicit split-aware loading (train and val separately).

---

### `octis_corpus.py`

**What it does**
- Writes OCTIS `corpus.tsv` with correct partition labels.
- Rows from train are marked `train`; rows from val are marked `val`.

**Inputs**
- `docs_train`, `docs_val`, `labels_train`, `labels_val`.

**Outputs**
- `data/interim/octis/<run_id>/corpus.tsv`

**Kept from legacy**
- OCTIS dataset-generation approach.

**Added**
- Fix for hard-coded `partition='train'` bug.
- Split-aware corpus generation for eval-safe scoring.

---

### `embeddings.py`

**What it does**
- Loads embedding models.
- Computes and caches embeddings to `.npy`.
- Reuses cached arrays for speed.

**Inputs**
- doc lists for train and val
- embedding model name

**Outputs**
- `data/interim/octis/<run_id>/embeddings_cache/{split}_{embedding}.npy`

**Kept from legacy**
- Embedding model caching strategy from Stage 03/05.

**Added**
- Separate cache files by split.
- Cleaner reusable API for train/eval/test scripts.

---

### `bertopic_octis_model.py`

**What it does**
- BERTopic + OCTIS wrapper used by tuning.

**Kept from legacy**
- Moved directly from old `src/stage03_modeling/bertopic_octis_model.py`.

**Added**
- Import path moved to new stage package.

---

### `tune.py`

**What it does**
- Runs embedding loop + Bayesian optimization.
- Trains on train split, evaluates candidate metrics on eval split.
- Produces one row per trial in a trials table.

**Inputs**
- `configs/train.yaml`
- split CSVs
- octis corpus/embeddings cache

**Outputs**
- `results/experiments/<run_id>/trials.csv`
- optional per-trial artifacts in `results/experiments/<run_id>/artifacts/`

**Kept from legacy**
- Existing OCTIS optimizer usage.
- Main hyperparameter search space (UMAP/HDBSCAN/vectorizer/BERTopic).

**Added**
- Stable machine-readable trial schema.
- `outlier_rate` and `stability_score` columns.
- Explicit run IDs.

---

### `cli.py`

**What it does**
- User entrypoint for Stage 03.

**Command**
- `python -m src.stage03_train.cli tune --config configs/train.yaml --run-id <id>`

---

### `smoke_test.py`

**What it does**
- Fast dry-run with a subset to validate plumbing before full tuning.

**Kept from legacy**
- Purpose of `test_octis_pipeline.py`.

**Added**
- Uses the new modular code paths.

---

## Stage 04 (Eval Select): Scripts and Responsibilities

### `pareto_analysis.py`

**What it does**
- Existing Pareto/data-cleaning utilities.

**Kept from legacy**
- Moved from `src/stage04_selection/pareto_analysis.py`.

---

### `weighted_score.py`

**What it does**
- Computes weighted score after Pareto filtering.
- Formula:
  - `w1*coherence + w2*diversity - w3*outlier_rate - w4*stability_penalty`

**Inputs**
- `trials.csv`
- `configs/eval_select.yaml`

**Outputs**
- weighted columns in ranked table

---

### `cli.py`

**What it does**
- Applies Pareto-then-weighted ranking.
- Emits winner config used by Stage 05.

**Inputs**
- `results/experiments/<run_id>/trials.csv`

**Outputs**
- `results/selection/<run_id>/winner_config.json`
- `results/selection/<run_id>/top_k.csv`
- `results/selection/<run_id>/selection_report.md`

---

## Stage 05 (Final Fit): Scripts and Responsibilities

### `final_fit.py`

**What it does**
- Refit winner in two policies:
  - train-only
  - train+val

**Inputs**
- `winner_config.json`
- split sentence CSVs

**Outputs**
- `models/final/<run_id>/train_only/...`
- `models/final/<run_id>/train_plus_val/...`

**Kept from legacy**
- Retraining internals from old `src/stage05_retraining/retrain_models.py`.

**Added**
- Policy-aware output layout.
- One place to build both final artifacts.

---

### `cli.py`

**Command**
- `python -m src.stage05_final_fit.cli fit --winner <path> --policy both`

---

## Stage 05b (Test Holdout): Scripts and Responsibilities

### `test_runner.py`

**What it does**
- Loads selected final artifact.
- Infers topics on `sentences_test.csv` only (no fitting).
- Computes final holdout metrics.

**Inputs**
- model artifact from stage05
- `sentences_test.csv`

**Outputs**
- `results/evaluation/<run_id>/test_metrics.json`
- `results/evaluation/<run_id>/final_topic_report.md`

**Added**
- One-shot guardrail: refuses rerun if metrics file exists unless `--allow-rerun`.

---

### `cli.py`

**Command**
- `python -m src.stage05b_test_holdout.cli score --final-model <path> --policy train_only`

---

## Configuration Map

- `configs/train.yaml`:
  - embedding models
  - tuning search space
  - trial count and seeds
- `configs/eval_select.yaml`:
  - Pareto controls
  - weighted ranking coefficients
- `configs/final_fit.yaml`:
  - default fit policy
  - output paths
- `configs/paths.yaml`:
  - train/val/test split file paths
  - run output roots

---

## Legacy Items Kept vs Deprecated

Kept (moved/reused):
- BERTopic OCTIS wrapper
- Pareto utilities
- core retraining implementation

Deprecated:
- old stage03 script-style runner
- old stage04 monolithic CLI
- old stage05 pareto-csv-only loading path
