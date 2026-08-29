# Stage 10 Final Analysis Notebooks

Nine notebooks answering the research questions and hypotheses in [`SCIENTIFIC_README.md`](../../SCIENTIFIC_README.md) from the final model, **call_49** (`v4_l12_granular_final_call49`, 348 topics, 16,000 books).

Config: [`configs/stage10/final_analysis.yaml`](../../configs/stage10/final_analysis.yaml). Statistics live in [`src/stage10_correlation_analysis/analysis/`](../../src/stage10_correlation_analysis/analysis/) so the notebooks stay readable; each section opens with plain-language markdown saying what is measured and why.

Structure follows [`topic_analysis_all_STRUCTURE.md`](topic_analysis_all_STRUCTURE.md).

## Run order

Run in order — 00 validates the frame that all later notebooks read, and 08 depends on the topic adjudication made in 07.

| Notebook | What it does |
| --- | --- |
| `00_data_foundations.ipynb` | Validates the analysis frame; hard-vs-soft variance comparison; compositional and topic-health diagnostics; author dominance; axis coverage audit. |
| `01_topic_landscape.ipynb` | What differs across rating tiers at the finest granularity (348 topics): effect sizes, FDR, screening funnel, leaderboards. |
| `02_taxonomy_structure.ipynb` | Main taxonomy groups, then a subgroup panel per group; where aggregation amplifies or dilutes signal. |
| `03_within_subgroup_drivers.ipynb` | The individual topics that explain subgroup differences, plus a subgroup coherence audit. |
| `04_composites_validity.ipynb` | Theory axis construction and validity (alpha, omega, PCA, split-half, leave-one-out), inter-correlations, VIF, strict vs generous mapping, testability verdicts. |
| `05_hypothesis_tests.ipynb` | H1–H6 with effect sizes, cluster-robust models, arc analysis and a predictive check. |
| `06_goodreads_validation.ipynb` | Quality (`rating_shrunk`) vs reach (`log_n_ratings`) as two separate channels; quadrant plots. |
| `07_qualitative_triangulation.ipynb` | Close reading targeted by the indices; label-fidelity audit of the headline leaves; corpus contamination check. |
| `08_robustness.ipynb` | Twelve specifications: mapping sensitivity, on-label-only rebuilds, word weighting, cohorts, author and series clustering, genre and era subgroups, arc renormalisation. |

Outputs land in `results/stage10_correlation_analysis/v4_l12_granular_final_call49/notebook_analysis/{notebook}/{figures,tables}/`.

## Prerequisites

The notebooks read prepared tables, not the 115M-row sentence parquets. Build them once, in order:

```bash
cd /path/to/romantic_novels_large_corpus
.venv/bin/python src/stage10_correlation_analysis/data_preparation/01_data_validation_extraction.py
.venv/bin/python src/stage10_correlation_analysis/data_preparation/05_aggregate_hard_assignments.py
.venv/bin/python src/stage10_correlation_analysis/data_preparation/02_book_aggregation.py
.venv/bin/python src/stage10_correlation_analysis/data_preparation/06_build_analysis_frame.py
```

Step 05 is a DuckDB pass over `results/experiments/v4_l12_granular_final_call49/full_corpus_infer/sentence_topics_*.parquet` and takes a few minutes; the rest are seconds. Notebook 07 also queries those parquets directly for sentence extracts.

Invariants are checked by `pytest tests/stage10/`.

## Editing the notebooks

Sources are percent-format Python in [`_src/`](_src/), which is what to edit and review. Convert and run:

```bash
.venv/bin/python scripts/stage10/percent_to_notebook.py notebooks/07_analysis/_src/05_hypothesis_tests.py
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=7200 notebooks/07_analysis/05_hypothesis_tests.ipynb
```

Pass `notebooks/07_analysis/_src/*.py` to convert all nine at once. Notebook 08 takes about 5 minutes to execute; the rest are faster.

## Measurement choices worth knowing before reading

- **Hard topic assignments**, not soft probabilities. Averaging 374 probabilities over ~7,000 sentences leaves a median per-topic coefficient of variation of 0.087; hard counts give 0.898, roughly 10x more between-book signal, and read directly as "3.3% of this book's sentences". Soft probabilities are kept as a robustness comparison in notebook 08.
- **Shares are compositional.** Every effect is a relative reallocation of narrative attention, never an absolute amount. Raw shares for description, ranks for tier tests, CLR for regression, explicit log-ratios for balance hypotheses.
- **Two outcome channels.** Quality and reach correlate at r = 0.21 shrunk, 0.12 raw — under 5% shared variance — so they are analysed separately rather than combined into one "success" variable.
- **Effect sizes, not p-values.** With ~5,000 books per tier almost everything is significant. A finding requires |Cliff's delta| >= 0.11 alongside a bootstrap interval excluding zero; the threshold was set before the tests ran.
- **Author clustering.** 5,353 of 8,264 authors have one book, so author fixed effects are infeasible. Cluster-robust SEs, cluster bootstrap and leave-one-author-out are used instead.

## Headline results

Full verdicts are in notebook 08. In short: no hypothesis clears the effect gate on its primary axis, while three findings the hypothesis frame obscured do — external violence and threat (`7.2`, delta +0.16), character appearance description (`1.6`, −0.15) and moral reflection (`3.4`, +0.13). Notebook 07's label audit changed the sign of the explicit-sex result, which is the main reason to read it before 08.
