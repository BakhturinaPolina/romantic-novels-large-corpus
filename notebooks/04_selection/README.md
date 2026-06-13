# Stage 04 Selection Notebooks (v3 BO)

Exploratory analysis of Bayesian optimization trial results for the v3 corpus. Mirrors the 100-book pretest workflow in `src/legacy/100_novels_script_legacy_pareto/04_selection/`, adapted for Stage03/Stage04 pipeline outputs.

## Run order

1. **`04_pareto_efficiency_analysis_v3.ipynb`** — load 130 BO calls, run three selection strategies, save top-k CSVs and figures.
2. **`04_hyperparameter_correlation_analysis_v3.ipynb`** — hyperparameter correlation and ML importance on top-k sets from Notebook 1.

## Input data

| File | Description |
|------|-------------|
| `results/experiments/v3_minilm12v2_first/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv` | Primary input: 130 BO calls (one row per call) |
| `results/selection/v3_minilm12v2_first/top_k.csv` | CLI selection output (validation reference) |

Configure paths in [`configs/selection_notebooks.yaml`](../../configs/selection_notebooks.yaml).

## Selection strategies compared

| Strategy | Pre-filter | Pareto | Ranking | Output CSV |
|----------|------------|--------|---------|------------|
| **A — Equal weights (legacy)** | failed-run + 2σ outliers + `n_topics > 0` | global + per-model | 0.5×Coherence_norm + 0.5×Topic_Diversity_norm | `top_10_equal_weights.csv` |
| **B — Coherence priority (legacy)** | same as A | global only | 0.7×Coherence_norm + 0.3×Topic_Diversity_norm | `top_10_coherence_priority.csv` |
| **C — eval_select (current)** | `min_n_topics`, stability gates | global only | 0.4×c_v + 0.4×diversity − 0.1×outlier − 0.1×stability | `top_10_eval_select.csv` |

## Outputs

Written to `results/selection/{run_id}/notebook_analysis/`:

```
notebook_analysis/
├── figures/
├── tables/
└── top_models/
    ├── top_10_equal_weights.csv
    ├── top_10_coherence_priority.csv
    ├── top_10_eval_select.csv
    └── strategy_overlap_summary.csv
```

## Reproduce CLI selection (Strategy C)

```bash
.venv/bin/python -m src.stage04_eval_select.cli select \
  --trials results/experiments/v3_minilm12v2_first/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv \
  --config configs/eval_select.yaml \
  --run-id v3_minilm12v2_first
```

## Dependencies

Uses project packages: `src.legacy.stage04_selection.pareto_analysis`, `src.stage04_eval_select.weighted_score`, `src.common.config`.

Run from project root with the project virtualenv (`.venv/bin/python`).

## Stage05 compare-fit + holdout (pareto top-k)

After Notebook 1 writes `notebook_analysis/top_models/top_10_*.csv`, refit the union of
selected BO calls on the 500k stratified sample and score the v3 test holdout:

```bash
.venv/bin/python -m src.stage05_final_fit.cli pareto \
  --selection-config configs/selection_notebooks.yaml \
  --paths-config configs/paths_stage03_fit_v3.yaml \
  --config configs/train_v3.yaml
```

Outputs:

- Compare-fit tables/metrics: `results/experiments/<run_id>/final_compare/call_<bo_call>/`
- Saved models (for holdout): `.../call_<bo_call>/model_compare/`
- Test metrics: `results/evaluation/<run_id>/call_<bo_call>/test_metrics.json`
- Summary: `results/experiments/<run_id>/final_compare/pareto_holdout_summary.csv`

Manual compare-fit for explicit BO calls:

```bash
.venv/bin/python -m src.stage05_final_fit.cli compare \
  --trials results/experiments/v3_minilm12v2_first/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv \
  --bo-calls 36,105,117 \
  --run-id v3_minilm12v2_first \
  --paths-config configs/paths_stage03_fit_v3.yaml \
  --config configs/train_v3.yaml \
  --save-model
```
