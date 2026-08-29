# Stage 10: Correlation Analysis

Turns the final BERTopic model's sentence-level topic assignments into a book-level analysis frame, and provides the statistics library behind the nine notebooks in [`notebooks/07_analysis/`](../../notebooks/07_analysis/).

Active run: **call_49** (`v4_l12_granular_final_call49`) — MiniLM-L12, 374 topics (348 mapped + outliers), 16,000 books.

Config: [`configs/stage10/final_analysis.yaml`](../../configs/stage10/final_analysis.yaml) is the single source of truth for paths, tiers, gates and bootstrap settings.

## Measurement

A book's value for a topic is **the share of its sentences whose argmax topic is that topic** — read directly as "3.3% of this book's sentences". This replaced the earlier soft-probability aggregation, which averaged 374 probabilities over ~6,000 sentences per book and left almost no between-book variance (median per-topic coefficient of variation 0.087, against 0.898 for hard counts). The soft tables are kept under `topic_probabilities/` and used only as a robustness comparison in notebook 08.

Shares are compositional, so all effects are relative reallocations of narrative attention. CLR is used for regression, explicit log-ratios for balance hypotheses.

## Structure

```
stage10_correlation_analysis/
├── data_preparation/
│   ├── 01_data_validation_extraction.py     # topic_lookup.parquet from Stage08 labels + Stage09 mappings
│   ├── 02_book_aggregation.py               # all taxonomy leaves -> shares + axes, with coverage audit
│   ├── 03_generate_topic_probabilities_final.py   # soft probabilities (robustness only)
│   ├── 04_generate_tertile_topic_probs_patched_v3.py
│   ├── 05_aggregate_hard_assignments.py     # DuckDB: book / tertile / chapter hard counts
│   └── 06_build_analysis_frame.py           # book_analysis_frame.parquet
└── analysis/
    ├── config.py            # load final_analysis.yaml, resolve paths
    ├── compositional.py     # CLR, log-ratios, share-sum checks
    ├── axes.py              # build theory axes from the frozen YAML schema, audit coverage
    ├── effects.py           # Cliff's delta, epsilon-squared, Hodges-Lehmann, bootstrap CIs
    ├── tests.py             # Kruskal-Wallis, Mann-Whitney, Holm within family, BH across
    ├── models.py            # OLS/WLS/logistic with author-cluster-robust SEs, VIF, CV check
    ├── reliability.py       # alpha, omega, PCA, split-half, leave-one-out for composites
    ├── bootstrap.py         # cluster bootstrap, leave-one-cluster-out, cluster dominance
    ├── arc.py               # within-book tertile deltas
    ├── qual.py              # sample extreme books, pull sentences via DuckDB
    └── notebook_helpers.py  # setup, output paths, table and figure saving
```

Superseded modules — the soft-probability aggregation and the unused `utils/` statistics and visualization helpers — are archived under `src/legacy/stage10_correlation_analysis/`.

## Run order

```bash
.venv/bin/python src/stage10_correlation_analysis/data_preparation/01_data_validation_extraction.py
.venv/bin/python src/stage10_correlation_analysis/data_preparation/05_aggregate_hard_assignments.py
.venv/bin/python src/stage10_correlation_analysis/data_preparation/02_book_aggregation.py
.venv/bin/python src/stage10_correlation_analysis/data_preparation/06_build_analysis_frame.py
```

Step 05 is a single DuckDB pass over `results/experiments/{run_id}/full_corpus_infer/sentence_topics_*.parquet` (115M rows) and takes a few minutes; the rest are seconds. All paths come from the config, so no arguments are needed.

Invariants — share sums, outlier exclusion, composition integrity, axis non-constancy, tier coverage — are asserted by `pytest tests/stage10/`.

## Outputs

Under `results/stage10_correlation_analysis/{run_id}/`:

| Directory | Contents |
| --- | --- |
| `topic_counts_hard/` | `book_topic_counts`, `tertile_topic_counts`, `chapter_topic_counts`, `book_totals`, `book_topic_word_counts` (word-weighted robustness), `hard_vs_soft_variance` |
| `book_features_hard/` | `book_leaf_shares_{abs,cond}`, `book_group_shares`, `book_axes_{strict,generous}`, `axis_coverage`, `mapping_coverage`, `payoff_guard_verdict`, `book_analysis_frame` |
| `topic_probabilities/` | soft-probability tables, retained for robustness only |
| `notebook_analysis/{nb}/` | `figures/` and `tables/` per notebook |

`book_analysis_frame.parquet` is the spine every notebook reads: 16,000 rows × 592 columns — topic shares, leaf shares (absolute and conditional), main-group shares, 28 axes in raw, z-scored and CLR form, both outcome channels, and all controls.

## Axes and the coverage audit

Axes are built from [`configs/stage09/theory_aligned_index_schema.yaml`](../../configs/stage09/theory_aligned_index_schema.yaml) rather than a parallel Python dict, and a component with no topics **raises** instead of silently evaluating to zero — which is how four axes in the previous version came to be exactly `0.0` without anyone noticing. `axis_coverage.parquet` records, per component, its topic count, mass and a `viable / weak / empty` verdict.

Two consequences are visible in that table and reported rather than hidden:

- `6.1a` (elite romantic status) and `6.7` (aristocracy) are **empty** and `6.6` (material glamour) rests on a single topic holding 0.11% of topic mass — the model has no usable luxury or elite-status vocabulary, so H3 as originally specified is not measurable. `AX_material_social_display` is the reframe actually tested.
- `3.1` is empty by taxonomy v2.4 design, which routes relief into `4.5` and reassurance into `4.6`. The payoff guard therefore defines `AX_payoff_safety_fallback = 4.5 + 4.6` and, because `4.6` is also H4's positive leg, tests H4 with `4.6` residualised on `4.5`. The overlap is documented in `payoff_guard_verdict.parquet` rather than absorbed silently.

Every axis is produced in **strict** (primary mapping only) and **generous** (primary 1.0 + secondary 0.5) variants; their agreement is checked in notebook 04 and again in notebook 08.

## Known caveat: Radway is mapped but not yet in the analysis frame

Radway stage 2 finished for call_49: `results/stage09_category_mapping/stage2_radway_functions/placeholder_v4_call49_rerun2/taxonomy_with_radway.json` (182 of 348 topics on R1–R13). The current `topic_lookup.parquet` and `book_analysis_frame.parquet` still come from the original taxonomy-only mapping, so `radway_*` columns and the schema's `radway_weights` are unused until a rebuild. Details: `results/reports/stage09/call49_rerun2_mapping_stability.md`.

## Dependencies

`pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `duckdb`, `pyarrow`, `matplotlib`, `pyyaml`. Run from the project root with `.venv/bin/python`.
