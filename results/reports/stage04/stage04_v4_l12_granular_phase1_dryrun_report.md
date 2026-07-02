# Stage 04: v4 L12 Granular Phase 1 Dry-run Report

**Date:** 2026-07-02  
**Run:** `v4_l12_granular_phase1` (160 BO calls, `model_runs=1`)  
**Selection config:** `configs/stage04/eval_select_granular.yaml`  
**Output run-id:** `v4_l12_granular_phase1_dryrun`  
**Script:** `scripts/stage04/run_v4_l12_granular_phase1_dryrun.sh`

---

## 1. Executive summary

| Role | Call | c_v | Diversity | Topics | Weighted score | Notes |
|------|------|-----|-----------|--------|----------------|-------|
| **Stage04 winner** | **142** | 0.625 | 0.866 | 357 | **0.534** | Pareto-efficient; diversity-weighted pick |
| BO objective #1 | 55 | **0.694** | 0.285 | 117 | 0.447 (rank 10) | High coherence, low diversity; Phase 2 **collapse** |
| Frozen analysis | 73 | 0.657 | 0.669 | 329 | 0.509 (rank 8) | Phase 2 **stable**; taxonomy/downstream frozen |
| Phase 2 band pick | 49 | 0.654 | 0.686 | 373 | 0.512 (rank 7) | Stable refit; in Phase 2 shortlist |

**Headline:** Granular Stage04 selection favors high-diversity configs in the 300–400 topic band. The automated winner (**call 142**) was **not** in the Phase 2 stability shortlist (band-based selection, different criteria). **Call 73 remains frozen** for taxonomy and placeholder downstream work per [call 73 strategy memo](../call73/placeholder_v4_call73_analysis_strategy.md).

---

## 2. Experimental setup

### 2.1 Input trials

| Field | Value |
|-------|-------|
| Trials CSV | `results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv` |
| Total BO calls | 160 |
| `model_runs` | 1 (stability columns present but std = 0) |
| Embedding | `sentence-transformers/all-MiniLM-L12-v2` |

### 2.2 Granular selection gates (`eval_select_granular.yaml`)

| Gate | Value |
|------|-------|
| `min_n_topics` | 50 |
| `max_n_topics` | 800 |
| `max_outlier_rate` | 0.85 |
| `max_largest_topic_share` | 0.25 |
| `require_topic_stability` | false |
| `max_n_topics_std` | 75 |
| Pareto metrics | coherence + diversity (min-max norm) |
| Weights | 0.45 coherence, 0.20 diversity, 0.15 topic_count_floor, 0.10 outlier, 0.10 stability |

---

## 3. Filter funnel

```
160 trials (Phase 1 BO)
  └─ min_n_topics ≥ 50          → 115  (45 collapsed mega-topic configs removed)
  └─ max_n_topics ≤ 800         → 115
  └─ outlier_rate ≤ 0.85        → 115
  └─ largest_topic_share ≤ 0.25 → 115
  └─ Pareto-efficient           →  10
  └─ top_k saved                →  10  (all Pareto candidates; config top_k=30)
```

Collapsed trials (2–49 topics with `largest_topic_share` ≈ 0.99) were excluded by the `min_n_topics=50` and `largest_topic_share` gates.

---

## 4. Top-5 ranked trials

| Rank | Call | weighted_score | c_v | diversity | n_topics | outlier | Pareto |
|------|------|----------------|-----|-----------|----------|---------|--------|
| 1 | **142** | 0.534 | 0.625 | 0.866 | 357 | 0.701 | yes |
| 2 | 79 | 0.531 | 0.641 | 0.822 | 309 | 0.712 | yes |
| 3 | 36 | 0.529 | 0.610 | 0.869 | 359 | 0.691 | yes |
| 4 | 26 | 0.527 | 0.572 | 0.942 | 395 | 0.685 | yes |
| 5 | 19 | 0.527 | 0.649 | 0.791 | 301 | 0.730 | yes |

Reference calls:

| Call | Rank | weighted_score | Why not #1 |
|------|------|----------------|------------|
| 55 | 10 | 0.447 | Dominates coherence but diversity 0.285; topic_count_floor plateau at 117 topics |
| 73 | 8 | 0.509 | Balanced but outranked by higher-diversity Pareto configs (142, 79, 36) |

---

## 5. Comparison with Phase 2 stability shortlist

Phase 2 used **band-filtered** candidate selection (`scripts/stage03/granular_select_phase2_candidates.py`), not Stage04 weighted score. Fourteen calls were stability-rerun:

`55, 73, 49, 19, 103, 66, 110, 102, 129, 155, 68, 95, 43, 10`

| Call | Stage04 rank | Phase 2 stability | Refit collapse |
|------|--------------|-------------------|----------------|
| 142 (Stage04 winner) | 1 | **Not selected** | — |
| 55 (BO #1) | 10 | Fail (117→2 topics) | yes |
| 73 (frozen) | 8 | **Pass** (std 7.1) | no |
| 49 | 7 | **Pass** (std 3.6) | no |
| 19 | 5 | Fail (301→5 topics) | yes |

**Interpretation:** Stage04 granular weights optimize the BO trial surface for diversity + granularity. Phase 2 stability reruns identify configs that **survive UMAP seed sweeps**. These are complementary filters — neither alone is sufficient for production model choice.

---

## 6. Recommendations

1. **Taxonomy / placeholder pipeline:** Keep **call 73 frozen** — stable refit, 151 usable axes, full downstream artifacts already built.
2. **Production final-fit candidate:** Call 73 or 49 (Phase 2 stable + high coherence); consider compare-fit on **call 142** if diversity-weighted selection is preferred for the next final model.
3. **Do not promote call 55** despite best BO objective — low diversity and Phase 2 refit collapse.
4. **Phase 3 BO:** Re-run `./scripts/stage03/run_v4_granular_phase3.sh l12` when GPU is free; apply same `eval_select_granular.yaml` when trials exist.
5. **Selection notebooks:** Add `v4_l12_granular_phase1_dryrun` entry to `configs/stage04/selection_notebooks.yaml` before running notebook analysis (checklist task #4).

---

## 7. Artifacts

| Artifact | Path |
|----------|------|
| Helper script | `scripts/stage04/run_v4_l12_granular_phase1_dryrun.sh` |
| Top-K | `results/selection/v4_l12_granular_phase1_dryrun/top_k.csv` |
| Winner config | `results/selection/v4_l12_granular_phase1_dryrun/winner_config.json` |
| Selection report | `results/selection/v4_l12_granular_phase1_dryrun/selection_report.md` |
| Phase 2 candidates | `results/selection/v4_l12_granular_phase1/phase2_candidates.csv` |
| Phase 2 stability | `results/experiments/v4_l12_granular_phase2_stability/final_compare/stability_summary.csv` |
