# Stage 04 Selection Notebooks

Exploratory analysis of Bayesian optimization trial results. Mirrors the 100-book pretest workflow in `src/legacy/100_novels_script_legacy_pareto/04_selection/`, adapted for Stage03/Stage04 pipeline outputs.

**Default config: v4 granular three-way compare** (L12 / L6 / MPNet Phase 1, 160 BO calls each) via [`configs/stage04/selection_notebooks_v4_granular.yaml`](../../configs/stage04/selection_notebooks_v4_granular.yaml). Both notebooks expose an `NB_CONFIG` variable in the setup cell; set it to `configs/stage04/selection_notebooks.yaml` for the legacy v3 L12-vs-L6 compare.

## Run order

1. **`04_pareto_efficiency_analysis_v3.ipynb`** — load BO trials per run, apply Stage04 granular filters, run three selection strategies per run, then the pooled cross-embedding Pareto analysis and the Phase 2 stability merge; saves per-run top-k CSVs, cross-model tables, and figures.
2. **`04_hyperparameter_correlation_analysis_v3.ipynb`** — hyperparameter correlation and ML importance on the top-k sets from Notebook 1 (per run, per-run compare, and pooled cross-embedding).

## Configuration modes

| Mode                 | YAML                                                                      | Outputs                                                              |
| -------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Compare** (default) | `runs:` (2+) + `comparison:` block                                        | Per-run dirs **plus** `results/selection/_compare/{comparison.id}/` |
| **Single**           | Top-level `run_id` / `inputs` / `outputs` only, or `runs` with one entry  | `results/selection/{run_id}/notebook_analysis/`                      |

The top-level `run_id` remains the **primary** run for the Stage05 `pareto` CLI.

## Input data (v4 granular)

Per run in `selection_notebooks_v4_granular.yaml`:

| Key | Path pattern |
| --- | --- |
| `trials_partial_csv` | `results/experiments/v4_{model}_granular_phase1/opt_1_*/trials_partial.csv` (160 calls) |
| `eval_select_top_k` | `results/selection/v4_{model}_granular_phase1_dryrun/top_k.csv` (CLI validation) |
| `phase2_compare_dir` | `results/experiments/v4_{model}_granular_phase2_pareto/final_compare` (Phase 2 merge) |

Requires Phase 1 BO + [`run_v4_granular_phase1_dryrun.sh`](../../scripts/stage04/run_v4_granular_phase1_dryrun.sh) per embedding; the Phase 2 section degrades gracefully if `final_compare/` is missing.

## Selection strategies compared (per run)

| Strategy                            | Pre-filter                                        | Pareto             | Ranking                                                                | Output CSV                      |
| ----------------------------------- | ------------------------------------------------- | ------------------ | ---------------------------------------------------------------------- | ------------------------------- |
| **A — Equal weights (legacy)**      | Stage04 granular gates (shared filtered set)      | global + per-model | 0.5×Coherence_norm + 0.5×Topic_Diversity_norm                          | `top_10_equal_weights.csv`      |
| **B — Coherence priority (legacy)** | same                                              | global only        | 0.7×Coherence_norm + 0.3×Topic_Diversity_norm                          | `top_10_coherence_priority.csv` |
| **C — eval_select granular**        | full granular gates (topic count, outlier, share) | global only        | 0.45×c_v + 0.20×diversity + 0.15×topic_floor − 0.10×outlier − 0.10×stab | `top_10_eval_select.csv`        |

Filters mirror `src.stage04_eval_select.cli select` with `eval_select_granular.yaml` (`min_n_topics=50`, `max_n_topics=800`, `max_outlier_rate=0.85`, `max_largest_topic_share=0.25`, `max_n_topics_std=75`) and are applied **per run** before ranking. Note: the `top_10_*.csv` filenames are kept for Stage05 compatibility but hold `selection.top_k` rows (30 under the granular config).

## Cross-embedding sections (Notebook 1)

- **Section 10 — pooled Pareto:** all filtered trials of all runs on shared min-max axes; global + per-embedding fronts; global front ranked with the granular weighted score.
- **Section 11 — Phase 2 merge:** compare-fit vs BO-reported coherence, refit-collapse flags, stable-only cross-embedding Pareto, and the three-way stable shortlist decision table.

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

### Compare mode (`results/selection/_compare/{comparison.id}/`)

```
_compare/v4_l12_l6_mpnet_pareto/
├── figures/
│   ├── selection_funnel_by_run.png
│   ├── pareto_overlay_eval_select.png
│   ├── pooled_pareto_overlay.png
│   ├── phase2_reported_vs_refit_cv.png
│   ├── phase2_stable_pareto_overlay.png
│   ├── hyperparameter_boxplots_eval_select_by_run.png
│   ├── random_forest_importance_coherence_by_run.png
│   └── random_forest_importance_pooled_pareto.png
└── tables/
    ├── selection_funnel_by_run.csv
    ├── compare_metric_snapshot.csv
    ├── winners_by_run_and_strategy.csv
    ├── pooled_pareto_counts_by_run.csv
    ├── pooled_pareto_top_k.csv
    ├── phase2_merged_all_runs.csv
    ├── cross_embedding_stable_shortlist.csv
    ├── correlation_analysis_all_runs.csv
    ├── correlation_analysis_pooled_pareto.csv
    ├── random_forest_importance_all_runs.csv
    └── random_forest_importance_pooled_pareto.csv
```

## Reproduce CLI selection (Strategy C)

```bash
for spec in \
  "v4_l12_granular_phase1_dryrun:results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv" \
  "v4_l6_granular_phase1_dryrun:results/experiments/v4_l6_granular_phase1/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv" \
  "v4_mpnet_granular_phase1_dryrun:results/experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv"
do
  run_id="${spec%%:*}"
  trials="${spec#*:}"
  .venv/bin/python -m src.stage04_eval_select.cli select \
    --trials "$trials" \
    --config configs/stage04/eval_select_granular.yaml \
    --run-id "$run_id"
done
```

## Dependencies

Uses project packages: `src.stage04_eval_select.notebook_io`, `src.legacy.stage04_selection.pareto_analysis`, `src.stage04_eval_select.weighted_score`, `src.common.config`.

Run from project root with the project virtualenv (`.venv/bin/python`).

## Stage05 compare-fit + holdout (pareto top-k)

After Notebook 1 writes `notebook_analysis/top_models/top_10_*.csv`, refit selected BO calls **per run** on the 500k stratified sample and score the v3 test holdout:

```bash
.venv/bin/python -m src.stage05_final_fit.cli pareto \
  --selection-config configs/stage04/selection_notebooks_v4_granular.yaml \
  --paths-config configs/stage03/paths_stage03_fit_v3.yaml \
  --config configs/stage03/train_v3.yaml
```

The `pareto` CLI uses the top-level `run_id`; temporarily set `run_id` and `outputs.top_models_dir` to another run's paths to refit its top-k.

Manual compare-fit for explicit BO calls:

```bash
.venv/bin/python -m src.stage05_final_fit.cli compare \
  --trials results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv \
  --bo-calls 73,49,11 \
  --run-id v4_l12_granular_phase1 \
  --paths-config configs/stage03/paths_stage03_fit_v3.yaml \
  --config configs/stage03/train_v3.yaml \
  --save-model
```
