# Stage 04: v3 BO Selection Report — MiniLM-L12 vs MiniLM-L6

**Date:** 2026-06-23  
**Corpus:** v3 English-only (`data/raw/romance_subdataset_filtered_v3/`)  
**Runs:** `v3_minilm12v2_first`, `v3_minilm6_first`  
**Pipeline:** Stage03 OCTIS BO (130 calls) → Stage04 eval-select → selection notebooks  
**Status:** Both BO runs complete; Stage04 CLI + notebook analysis done; Stage05 final compare pending for L6.

---

## 1. Executive summary

| | **L12** (`all-MiniLM-L12-v2`) | **L6** (`paraphrase-MiniLM-L6-v2`) |
|---|---|---|
| BO status | 130/130 calls | 130/130 calls |
| Wall time | ~2.8 h | ~12.4 h |
| `model_runs` per BO call | **1** | **3** |
| Stage04-eligible trials (production) | **55** | **7** |
| Production Stage04 winner | call **117** (37 topics) | call **128** (502 topics) |
| Best BO objective trial | call **117** (c_v 0.647) | call **11** (c_v 0.649, 38 topics) |
| Recommended L6 exploratory pick | — | call **11** (see §5) |

**Headline:** L6 reaches slightly higher coherence at comparable topic counts (~38 topics), but its BO surface is far less stable across random seeds. Production Stage04 gates leave only **7** L6 trials; the default winner (call 128) trades coherence for extreme diversity (502 topics). For exploration, use `configs/eval_select_exploratory_l6.yaml`, which widens the pool to **17** trials and selects call **11** with coherence-biased weights.

**Fair comparison caveat:** L12 was tuned with `model_runs: 1` (stability gate effectively off); L6 used the standard `model_runs: 3`. Funnel counts and winner quality are not directly comparable until L12 is rerun with three fits per call.

---

## 2. Experimental setup

### 2.1 Shared BO configuration

- **Calls:** 130 (seed 42)
- **Fit sample:** 500k stratified train / 100k val (`data/stage03_samples_v3/`, seed 42)
- **Coherence eval:** 100k val sentences
- **Search space:** UMAP, HDBSCAN, vectorizer `min_df`, BERTopic `min_topic_size` / `top_n_words` (see `configs/train_v3*.yaml`)
- **BO objective:** `CoherenceWithTopicPenalty` (topic-count penalty, `min_n_topics: 20`)

### 2.2 Embedding runs

| Run ID | Embedding | Config | `model_runs` |
|--------|-----------|--------|--------------|
| `v3_minilm12v2_first` | `sentence-transformers/all-MiniLM-L12-v2` | `train_v3_resume10_single.yaml` | 1 |
| `v3_minilm6_first` | `sentence-transformers/paraphrase-MiniLM-L6-v2` | `train_v3_minilm6.yaml` | 3 |

Artifacts:

- Trials: `results/experiments/{run_id}/opt_1_*/trials_partial.csv`
- Run summaries: `results/experiments/{run_id}/run_summary.json`

### 2.3 Stage04 production selection (`configs/eval_select.yaml`)

| Gate | Value |
|------|-------|
| `min_n_topics` | 20 |
| `require_topic_stability` | true |
| `max_n_topics_std` | 3.0 |
| Pareto metrics | coherence + diversity (min-max norm) |
| Weights | 0.4 coherence, 0.4 diversity, 0.1 outlier, 0.1 stability |

---

## 3. BO search results

### 3.1 Trial counts and peaks

| Metric | L12 | L6 |
|--------|-----|-----|
| Total BO calls | 130 | 130 |
| Failed fits (c_v = 0) | 9 | 11 |
| `topic_stability_pass` rate | 100% (130/130) | 47% (61/130) |
| Max raw coherence (any trial) | 0.675 (call 19, 2 topics) | 0.728 (call 125, unstable) |
| Best penalized BO objective | 0.647 (call 117) | 0.649 (call 11) |
| Median `n_topics` (valid trials) | 4 | 13 |

L12 converged early (max coherence plateau by call 19). L6 continued finding high-raw-coherence but unstable configurations late in the search (call 125).

### 3.2 Stage04 filter funnel (production)

```
L12:  130 → 55 (n_topics≥20) → 55 (stability) → 55 (std≤3)
L6:   130 → 42 (n_topics≥20) →  7 (stability) →  7 (std≤3)
```

The L6 bottleneck is **`topic_stability_pass`**: 35 of 42 trials with ≥20 topics fail because three independent fits disagree on topic count (`n_topics_std > 3` or collapse below 50% of median). Example: call 2 reports median 190 topics but individual runs ranged 2–208 (std 93.2).

With `model_runs: 1`, L12 always passes stability (`topic_stability_pass` is trivially true when only one fit exists).

### 3.3 Aggregate best trial (`trials.csv`)

| | Coherence c_v | Diversity | n_topics | Outlier rate |
|---|---------------|-----------|----------|--------------|
| L12 | 0.644 | 0.782 | 38 | 0.766 |
| L6 | **0.650** | 0.689 | 38 | 0.783 |

At similar topic granularity (~38 topics), L6 shows marginally higher coherence and lower diversity.

---

## 4. Stage04 production winners

### 4.1 L12 — call 117 (recommended)

| Metric | Value |
|--------|-------|
| Trial ID | `v3_minilm12v2_first_1_call_117` |
| Coherence c_v | 0.647 |
| Topic diversity | 0.797 |
| n_topics | 37 |
| Weighted score | 0.578 |

Key hyperparameters: `umap__n_neighbors=18`, `umap__n_components=11`, `hdbscan__min_cluster_size=777`, `bertopic__min_topic_size=478`.

Notebook strategy overlap (top-3 only in practice): all three strategies (equal weights, coherence priority, eval_select) agree on calls **117, 105, 36**.

Outputs: `results/selection/v3_minilm12v2_first/`

### 4.2 L6 — call 128 (production CLI; not recommended for final fit)

| Metric | Value |
|--------|-------|
| Trial ID | `v3_minilm6_first_1_call_128` |
| Coherence c_v | 0.590 |
| Topic diversity | 0.880 |
| n_topics | **502** |
| Weighted score | 0.588 |

Call 128 wins production Stage04 because it dominates diversity on the **3-point Pareto frontier** among only 7 eligible trials—not because it maximizes coherence. The BO-best trial **call 11** (c_v 0.649, 38 topics) ranks third on weighted score within that tiny pool.

Outputs: `results/selection/v3_minilm6_first/`

---

## 5. Exploratory L6 selection

**Config:** `configs/eval_select_exploratory_l6.yaml`

| Setting | Production | Exploratory moderate |
|---------|------------|----------------------|
| `require_topic_stability` | true | **false** |
| `max_n_topics_std` | 3.0 | **15.0** |
| Weights (coh / div) | 0.4 / 0.4 | **0.7 / 0.15** |
| Eligible trials | 7 | **17** |
| Winner | call 128 | **call 11** |

Top trials in the 17-trial exploratory pool:

| Call | c_v | n_topics | std | Notes |
|------|-----|----------|-----|-------|
| **11** | **0.649** | 38 | 1.41 | BO-best; matches aggregate `trials.csv` |
| 74 | 0.646 | 56 | 2.16 | Stable |
| 24 | 0.644 | 42 | 1.89 | Stable |

```bash
.venv/bin/python -m src.stage04_eval_select.cli select \
  --trials results/experiments/v3_minilm6_first/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv \
  --config configs/eval_select_exploratory_l6.yaml \
  --run-id v3_minilm6_first
```

Use exploratory outputs for notebook review only; prefer call **11** or **24** for Stage05 unless stability is revalidated.

---

## 6. Notebook analysis infrastructure

Multi-run comparison support added for L12 vs L6:

| Asset | Path |
|-------|------|
| Notebook config | `configs/selection_notebooks.yaml` |
| Shared helpers | `src/stage04_eval_select/notebook_io.py` |
| Pareto notebook | `notebooks/04_selection/04_pareto_efficiency_analysis_v3.ipynb` |
| Hyperparameter notebook | `notebooks/04_selection/04_hyperparameter_correlation_analysis_v3.ipynb` |
| Compare outputs (after notebook run) | `results/selection/_compare/l12_vs_l6/` |

Per-run notebook outputs exist for L12 (`results/selection/v3_minilm12v2_first/notebook_analysis/`). Re-run both notebooks to refresh L6 figures and cross-model comparison tables.

---

## 7. Recommendations

1. **Stage05 L12:** Proceed with call **117** (production winner, aligned with BO and all notebook strategies).
2. **Stage05 L6:** Use call **11** (BO-best, ~38 topics), not call 128. Optionally compare-fit calls 11, 24, 74.
3. **Fair embedding comparison:** Rerun L12 with `model_runs: 3` (`configs/train_v3.yaml`) before drawing conclusions about embedding quality from Stage04 funnels.
4. **MPNet (`v3_mpnet`):** Still pending; use same production Stage04 gates once BO completes.
5. **Selection notebooks:** Run pareto → hyperparameter notebooks with `runs:` in `selection_notebooks.yaml` to populate `_compare/l12_vs_l6/`.

---

## 8. File index

| Description | Path |
|-------------|------|
| L12 trials | `results/experiments/v3_minilm12v2_first/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv` |
| L6 trials | `results/experiments/v3_minilm6_first/opt_1_sentence-transformers__paraphrase-MiniLM-L6-v2/trials_partial.csv` |
| L12 winner | `results/selection/v3_minilm12v2_first/winner_config.json` |
| L6 winner (production) | `results/selection/v3_minilm6_first/winner_config.json` |
| L12 notebook analysis | `results/selection/v3_minilm12v2_first/notebook_analysis/` |
| Production eval-select | `configs/eval_select.yaml` |
| Exploratory L6 eval-select | `configs/eval_select_exploratory_l6.yaml` |

---

*Generated from Stage03/04 pipeline outputs on the v3 English-only romance sentence corpus.*
