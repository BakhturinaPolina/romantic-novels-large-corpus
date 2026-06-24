# Stage 04 Selection Notebooks (v3 BO)

Exploratory analysis of Bayesian optimization trial results for the v3 corpus. Mirrors the 100-book pretest workflow in `src/legacy/100_novels_script_legacy_pareto/04_selection/`, adapted for Stage03/Stage04 pipeline outputs.

Supports **single-run** (one embedding) or **multi-run compare** (e.g. L12 vs L6) via `configs/selection_notebooks.yaml`.

## Run order

1. `**04_pareto_efficiency_analysis_v3.ipynb`** — load BO trials per run, apply Stage04 filters, run three selection strategies, save per-run top-k CSVs and figures; optional cross-model comparison tables/figures.
2. `**04_hyperparameter_correlation_analysis_v3.ipynb**` — hyperparameter correlation and ML importance on top-k sets from Notebook 1 (per run + compare).

## Configuration modes


| Mode                 | YAML                                                                     | Outputs                                                             |
| -------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| **Single** (default) | Top-level `run_id` / `inputs` / `outputs` only, or `runs` with one entry | `results/selection/{run_id}/notebook_analysis/`                     |
| **Compare**          | `runs:` (2+) + `comparison:` block                                       | Per-run dirs **plus** `results/selection/_compare/{comparison.id}/` |


Set `comparison.id` and `comparison.base_dir` for cross-model artifacts. The top-level `run_id` remains the **primary** run for Stage05 `pareto` CLI.

### L12 vs L6 example

`configs/selection_notebooks.yaml` ships with both:

- `v3_minilm12v2_first` (L12, `all-MiniLM-L12-v2`)
- `v3_minilm6_first` (L6, `paraphrase-MiniLM-L6-v2`)

Comparison outputs: `results/selection/_compare/l12_vs_l6/`

**Caveat:** L12 was tuned with `model_runs: 1`; L6 uses `model_runs: 3`. Stability-filter funnel counts are not directly comparable until L12 is rerun with the standard config.

## Input data


| Run                   | trials_partial_csv                                                                                             |
| --------------------- | -------------------------------------------------------------------------------------------------------------- |
| `v3_minilm12v2_first` | `results/experiments/v3_minilm12v2_first/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv`    |
| `v3_minilm6_first`    | `results/experiments/v3_minilm6_first/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv` |


Optional CLI reference: `results/selection/{run_id}/top_k.csv`

Configure paths in `[configs/selection_notebooks.yaml](../../configs/selection_notebooks.yaml)`.

## Selection strategies compared


| Strategy                            | Pre-filter                                  | Pareto             | Ranking                                               | Output CSV                      |
| ----------------------------------- | ------------------------------------------- | ------------------ | ----------------------------------------------------- | ------------------------------- |
| **A — Equal weights (legacy)**      | Stage04 gates (shared filtered set per run) | global + per-model | 0.5×Coherence_norm + 0.5×Topic_Diversity_norm         | `top_10_equal_weights.csv`      |
| **B — Coherence priority (legacy)** | same                                        | global only        | 0.7×Coherence_norm + 0.3×Topic_Diversity_norm         | `top_10_coherence_priority.csv` |
| **C — eval_select (current)**       | `min_n_topics`, stability gates             | global only        | 0.4×c_v + 0.4×diversity − 0.1×outlier − 0.1×stability | `top_10_eval_select.csv`        |


Filters are applied **per run** before ranking (important when `model_runs` or stability differ).

## Outputs

### Per run (`results/selection/{run_id}/notebook_analysis/`)

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

### Compare mode (`results/selection/_compare/{id}/`)

```
_compare/l12_vs_l6/
├── figures/
│   ├── selection_funnel_by_run.png
│   ├── pareto_overlay_eval_select.png
│   ├── hyperparameter_boxplots_eval_select_by_run.png
│   └── random_forest_importance_coherence_by_run.png
└── tables/
    ├── selection_funnel_by_run.csv
    ├── compare_metric_snapshot.csv
    ├── winners_by_run_and_strategy.csv
    ├── correlation_analysis_all_runs.csv
    └── random_forest_importance_all_runs.csv
```

## Reproduce CLI selection (Strategy C)

```bash
for spec in \
  "v3_minilm12v2_first:results/experiments/v3_minilm12v2_first/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv" \
  "v3_minilm6_first:results/experiments/v3_minilm6_first/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv"
do
  run_id="${spec%%:*}"
  trials="${spec#*:}"
  .venv/bin/python -m src.stage04_eval_select.cli select \
    --trials "$trials" \
    --config configs/eval_select.yaml \
    --run-id "$run_id"
done
```

## Dependencies

Uses project packages: `src.stage04_eval_select.notebook_io`, `src.legacy.stage04_selection.pareto_analysis`, `src.stage04_eval_select.weighted_score`, `src.common.config`.

Run from project root with the project virtualenv (`.venv/bin/python`).

## Stage05 compare-fit + holdout (pareto top-k)

After Notebook 1 writes `notebook_analysis/top_models/top_10_*.csv`, refit selected BO calls **per run** on the 500k stratified sample and score the v3 test holdout:

```bash
# L12 (primary run_id in selection_notebooks.yaml)
.venv/bin/python -m src.stage05_final_fit.cli pareto \
  --selection-config configs/selection_notebooks.yaml \
  --paths-config configs/paths_stage03_fit_v3.yaml \
  --config configs/train_v3.yaml
```

For L6, temporarily set top-level `run_id` and `outputs.top_models_dir` to the L6 paths (or add a `selection_notebooks_minilm6.yaml`), then rerun `pareto`.

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

