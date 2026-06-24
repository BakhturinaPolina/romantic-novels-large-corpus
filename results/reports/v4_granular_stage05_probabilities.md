# v4 Granular BO — Stage05 final fit with soft probabilities

After Phase 3 selection, run the winning configuration with `calculate_probabilities: true`
so book-level topic mixtures can use HDBSCAN soft assignments (cuML `prediction_data=True`
is already set in the default HDBSCAN hyperparameters).

## 1. Override probabilities for the final fit

Copy the winner hyperparameters into a one-off config or set in the compare-fit / final-fit
YAML block:

```yaml
bertopic:
  calculate_probabilities: true
```

## 2. Compare-fit refit (stability-validated winner)

```bash
.venv/bin/python -m src.stage05_final_fit.cli compare \
  --trials results/experiments/v4_l12_granular_phase3/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv \
  --bo-calls <WINNER_BO_CALL> \
  --run-id v4_l12_granular_final \
  --stability-runs 3 \
  --stability-tolerance 75 \
  --reduce-outliers
```

Set `calculate_probabilities: true` in the train config used by compare-fit, or patch
`configs/train_v4_*_granular_phase3.yaml` for the final run only.

## 3. Stage04 selection (granular gates)

```bash
.venv/bin/python -m src.stage04_eval_select.cli select \
  --trials results/experiments/v4_l12_granular_phase3/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv \
  --config configs/eval_select_granular.yaml \
  --run-id v4_l12_granular_phase3
```

## Notes

- BO tuning keeps `calculate_probabilities: false` (hard `-1` outlier rate is cheaper).
- Final model only: enable probabilities for Stage09 book-level mixtures and Stage10 correlation work.
- Requires GPU (cuML UMAP/HDBSCAN) for fit; encode remains CPU-friendly via transfer bundle scripts.
