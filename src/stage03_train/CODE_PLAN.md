# BERTopic Pipeline Code Plan

This file is the implementation blueprint for the new train/eval/test pipeline.

## 1) Implementation Order

1. Create stage03 modular training package (`data_io`, `octis_corpus`, `embeddings`, `tune`, `cli`, `smoke_test`).
2. Create stage04 eval-select package (`pareto_analysis`, `weighted_score`, `cli`).
3. Create stage05 final-fit package (`final_fit`, `cli`).
4. Create stage05b holdout package (`test_runner`, `cli`).
5. Update configs (`paths.yaml`, `train.yaml`, `eval_select.yaml`, `final_fit.yaml`).
6. Update imports in downstream stages that still reference old stage paths.

---

## 2) Files to Create / Modify / Remove

### Create
- `src/stage03_train/__init__.py`
- `src/stage03_train/data_io.py`
- `src/stage03_train/octis_corpus.py`
- `src/stage03_train/embeddings.py`
- `src/stage03_train/bertopic_octis_model.py` (copy from legacy)
- `src/stage03_train/tune.py`
- `src/stage03_train/cli.py`
- `src/stage03_train/smoke_test.py`

- `src/stage04_eval_select/__init__.py`
- `src/stage04_eval_select/pareto_analysis.py` (copy from legacy)
- `src/stage04_eval_select/weighted_score.py`
- `src/stage04_eval_select/cli.py`

- `src/stage05_final_fit/__init__.py`
- `src/stage05_final_fit/final_fit.py`
- `src/stage05_final_fit/cli.py`

- `src/stage05b_test_holdout/__init__.py`
- `src/stage05b_test_holdout/test_runner.py`
- `src/stage05b_test_holdout/cli.py`

- `configs/train.yaml`
- `configs/eval_select.yaml`
- `configs/final_fit.yaml`

### Modify
- `configs/paths.yaml`
- imports in downstream files that reference old stage names
- legacy config files with deprecation comment

### Remove (after migration safety check)
- `src/legacy/stage03_modeling/convert_topics.py`
- `src/legacy/stage03_modeling/test_octis_pipeline.py`
- `src/legacy/stage05_retraining/diagnose_data.py`

---

## 3) Stage03 Contracts

## `data_io.py`

### Function signatures

```python
def clean_sentence(text: str) -> str: ...
def read_split_csv(csv_path: Path, sentence_column: str = "sentence") -> pd.DataFrame: ...
def dataframe_to_docs(df: pd.DataFrame, sentence_column: str = "sentence") -> tuple[list[str], list[list[str]], list[str]]: ...
def load_train_eval(
    train_csv: Path,
    eval_csv: Path,
    sentence_column: str = "sentence",
) -> dict[str, list]:
    ...
```

### Guarantees
- Uses Stage 01 schema (`sentence` lowercase column).
- Never assumes 4-column legacy shape.
- Returns labels as `work_id` strings.

---

## `octis_corpus.py`

### Function signatures

```python
def write_octis_corpus(
    docs_train: list[str],
    labels_train: list[str],
    docs_eval: list[str],
    labels_eval: list[str],
    output_dir: Path,
) -> Path: ...
```

### Output schema
- `corpus.tsv`, tab-separated:
  - column0: document text
  - column1: partition (`train` or `val`)
  - column2: label (`work_<work_id>`)

---

## `embeddings.py`

### Function signatures

```python
def safe_embedding_name(model_name: str) -> str: ...
def get_cache_file(cache_dir: Path, split: str, model_name: str) -> Path: ...
def load_or_compute_embeddings(
    docs: list[str],
    model_name: str,
    cache_dir: Path,
    split: str,
    device: str = "auto",
    batch_size: int = 256,
) -> np.ndarray: ...
```

### Guarantees
- Distinct cache file per split + embedding model.
- Deterministic save/load behavior.

---

## `tune.py`

### Function signatures

```python
def build_search_space(cfg: dict) -> dict: ...
def run_embedding_optimization(...) -> pd.DataFrame: ...
def run_tuning(
    config_path: Path,
    run_id: str,
    embedding_models_override: list[str] | None = None,
) -> Path: ...
```

### Trials schema (`results/experiments/<run_id>/trials.csv`)

Required columns:
- `run_id`
- `trial_id`
- `seed`
- `embedding_model`
- `coherence_c_v`
- `coherence_c_npmi`
- `topic_diversity`
- `outlier_rate`
- `n_topics`
- `stability_score`
- hyperparameter columns:
  - `umap__n_neighbors`
  - `umap__n_components`
  - `umap__min_dist`
  - `hdbscan__min_cluster_size`
  - `hdbscan__min_samples`
  - `vectorizer__min_df`
  - `bertopic__top_n_words`
  - `bertopic__min_topic_size`

---

## 4) Stage04 Contracts

## `weighted_score.py`

### Function signatures

```python
def add_stability_penalty(df: pd.DataFrame) -> pd.DataFrame: ...
def apply_weighted_score(
    df: pd.DataFrame,
    w_coherence: float,
    w_diversity: float,
    w_outlier: float,
    w_stability: float,
) -> pd.DataFrame: ...
```

### Ranking policy
1. Keep Pareto-efficient rows on `(coherence_c_v, topic_diversity)`.
2. Rank remaining rows by weighted score.
3. Emit top-k and winner.

### Pareto rationale and active model scope
- Pareto filtering keeps only rows where improving coherence would reduce diversity (or vice versa), matching the required trade-off framing.
- Active Stage03 embedding scope is limited to:
  - `sentence-transformers/all-MiniLM-L12-v2`
  - `sentence-transformers/paraphrase-mpnet-base-v2`
  - `sentence-transformers/paraphrase-MiniLM-L6-v2`
- Rationale from the pretest on a smaller corpus of 100 "billionaire" romance novels:
  - `all-MiniLM-L12-v2` produced the strongest coherence and top combined Pareto score.
  - `paraphrase-mpnet-base-v2` and `paraphrase-MiniLM-L6-v2` provided the best coherence/diversity balance.
  - low-coherence models (`whaleloops/phrase-bert`, `paraphrase-distilroberta-base-v1`, `multi-qa-mpnet-base-cos-v1`) were excluded from active tuning.

## `cli.py`

### Outputs
- `results/selection/<run_id>/winner_config.json`
- `results/selection/<run_id>/top_k.csv`
- `results/selection/<run_id>/selection_report.md`

### `winner_config.json` schema
- `run_id`
- `selected_at`
- `trial_id`
- `embedding_model`
- `selection_metrics` (coherence/diversity/outlier/stability/weighted_score)
- `hyperparameters` (flat dict with `section__name` keys)
- `train_csv`, `eval_csv`, `test_csv`

---

## 5) Stage05 Contracts

## `final_fit.py`

### Function signatures

```python
def load_winner_config(path: Path) -> dict: ...
def fit_policy_train_only(...) -> Path: ...
def fit_policy_train_plus_val(...) -> Path: ...
def run_final_fit(winner_config: Path, policy: str = "both") -> dict[str, Path]: ...
```

### Output layout
- `models/final/<run_id>/train_only/{model.pkl, model_native/, metadata.json}`
- `models/final/<run_id>/train_plus_val/{model.pkl, model_native/, metadata.json}`

---

## 6) Stage05b Contracts

## `test_runner.py`

### Function signatures

```python
def ensure_one_shot(output_metrics_json: Path, allow_rerun: bool = False) -> None: ...
def infer_on_test(...) -> dict: ...
def write_test_report(...) -> Path: ...
def run_holdout_score(...) -> Path: ...
```

### Guardrail
- If `test_metrics.json` exists and `allow_rerun=False`, raise an error.

### Output schema (`test_metrics.json`)
- `run_id`
- `scored_at`
- `model_policy` (`train_only` or `train_plus_val`)
- `n_docs_test`
- `coherence_c_v`
- `coherence_c_npmi`
- `topic_diversity`
- `outlier_rate`
- `n_topics`

---

## 7) CLI Surface

- `python -m src.stage03_train.cli tune --config configs/train.yaml --run-id <id>`
- `python -m src.stage03_train.cli tune --config configs/train.yaml --embedding-model sentence-transformers/all-MiniLM-L12-v2`
- `python -m src.stage03_train.smoke_test --config configs/train.yaml --max-docs 10000`
- `python -m src.stage04_eval_select.cli select --trials <path> --config configs/eval_select.yaml --run-id <id>`
- `python -m src.stage05_final_fit.cli fit --winner <path> --policy both`
- `python -m src.stage05b_test_holdout.cli score --final-model <path> --policy train_only`

---

## 8) Search Space Defaults

- `umap__n_neighbors`: `2..50` (int)
- `umap__n_components`: `2..10` (int)
- `umap__min_dist`: `0.0..0.1` (float)
- `hdbscan__min_cluster_size`: `50..500` (int)
- `hdbscan__min_samples`: `10..100` (int)
- `vectorizer__min_df`: `0.001..0.01` (float)
- `bertopic__top_n_words`: `10..40` (int)
- `bertopic__min_topic_size`: `10..250` (int)

---

## 9) Validation Checklist

- Stage03 smoke test completes.
- Stage03 tuning logs stream to terminal with timestamps and persist to `logs/stage03_<run_id>.log`.
- `results/experiments/<run_id>/run_state.json` updates after each boundary step and each model.
- `trials.csv` is written incrementally after each model and includes required columns.
- `run_manifest.json` and `run_summary.json` are updated with artifact paths and per-step/model durations.
- Re-run with same `run_id` auto-skips already completed corpus/model work and resumes remaining steps.
- Stage04 emits winner config.
- Stage05 emits both artifact trees.
- Stage05b writes test metrics once; second run fails without `--allow-rerun`.
- Downstream imports no longer require old stage names.
