# Scientific Methodology: Romance Novels — Themes × Reader Appreciation

**A Mixed-Methods Computational Analysis**

This document provides an overview of the research methodology and findings. For implementation details, see **`results/reports/`** (markdown reports) and stage-specific documentation in [`src/`](src/).

The final analysis is a nine-notebook walkthrough in [`notebooks/07_analysis/`](notebooks/07_analysis/), starting from data foundations and ending with robustness. Read [its README](notebooks/07_analysis/README.md) first for the run order and the measurement decisions.

Repository structure note: active pipeline packages stay at the `src/` root, while superseded migration-era modules are archived under `src/legacy/` for reproducibility. Stage utility scripts are colocated inside their stage folders (for example `src/stage02_preprocessing/scripts/`, `src/stage08_llm_labeling/scripts/`, and `src/stage10_correlation_analysis/scripts/`).

---

## Research Objectives

1. **Map topic-model outputs** from modern romance novels to theory-driven themes and test which themes differentiate higher-rated from lower-rated books.

2. **Build explainable indices** to quantify narrative qualities readers value.

3. **Validate findings** against Goodreads metadata (ratings and rating counts).

---

## Research Questions

1. Which theme categories are most prevalent in higher-rated vs lower-rated novels?
2. Does love/commitment/tenderness outweigh explicit sexual content in higher-rated books?
3. Is luxury appealing only when paired with commitment/tenderness?
4. Do protectiveness/care signals predict appreciation better than jealousy/possessiveness?
5. Do miscommunication/negative affect diminish across the book while HEA/repair rises?

Question 3 turned out not to be answerable in this corpus: the final model contains no luxury or elite-status vocabulary to measure (see [Limitations](#limitations)). It was reframed as *material and social display*, which is measurable, and answered in that form.

---

## Research Hypotheses

Each hypothesis was pre-registered in `configs/stage09/theory_aligned_index_schema.yaml` with a primary axis, then tested as specified. A **result** requires all three of: the predicted direction, a bootstrap confidence interval excluding zero, and |Cliff's δ| ≥ 0.11. The threshold was set before the tests ran; with ~5,000 books per tier, statistical significance alone separates almost nothing.

| # | Hypothesis | As actually tested | Result |
|---|------------|--------------------|--------|
| H1 | **Love-over-Sex**: emotional connection beats explicit content | `AX_love_over_sex`, log-ratio `log((4.5+4.6+2.2+4.2)/2.3)` and difference form | **Contradicted** (δ = −0.050). Emotional safety *and* explicit content are both higher in well-rated books, so the trade-off does not exist as framed |
| H2 | **HEA Index**: explicit happily-ever-after signals predict appreciation | `4.5` alone (primary); `4.5 + 0.8×5.3a + 0.5×8.3a` as the composite | **No reliable effect** (δ = +0.006, CI spans zero). HEA is near-universal in the genre, so it cannot discriminate |
| H3 | **Material and social display** (reframed from Luxury × Love) | `AX_material_social_display` (1.6 + 8.2 + 5.3a + 8.3a) plus its interaction with relational payoff | **Contradicted, reliably** (δ = −0.139, the largest hypothesis-level effect). Display is *lower* in well-rated books, and display × payoff is a substitute rather than a complement |
| H4 | **Protectiveness vs Possessiveness** | `4.6 − 4.7`, log-ratio and difference; `4.6` residualised on `4.5` | **Directionally consistent, below threshold** (δ = +0.093). Protective care carries it; `4.7` has 2 topics and contributes nothing measurable |
| H5 | **Darkness vs Tenderness**, inverted U | `(3.2+4.4+7.2+7.3) − (3.1+2.2+4.6)`, with `3.1` empty, plus a quadratic darkness term | **Inverted U contradicted** (quadratic is convex, p ≈ 0.06). The linear component holds and is much larger in the components than in the composite |
| H6 | **Narrative Arc**: repair rises, conflict falls | Within-book tertile Δ (end − begin) for rising (`4.5`, `4.6`) vs falling (`4.3`, `4.4`, `3.2`) leaves | **Partly supported** (arc index δ = +0.039). Repair rises in 73% of books, but nothing falls — every relational category rises. Renormalising within the relationship group leaves repair rising in 71% while misunderstanding falls |

Full tests, effect sizes and models: [`notebooks/07_analysis/05_hypothesis_tests.ipynb`](notebooks/07_analysis/05_hypothesis_tests.ipynb).

Macro-axis notes (v2.4): Full schema in `configs/stage09/theory_aligned_index_schema.yaml`. Taxonomy v2.4 in `configs/stage09/romance_corpus_taxonomy_v2.yaml`. **Axis-bearing IDs** (narrow allowlist for Stage10 hypotheses) are separate from the full leaf taxonomy used in Stage09 classification — context labels (1.x, 6.1b, 8.x, 9.x, 10.x, `uncertain_interpretable`) are mappable but excluded from macro axes. **`3.3`** is exploratory-only (`AX_internal_ambivalence` for H5/H6). Three intimacy axes for H1 (exploratory): **`AX_everyday_intimacy_emotional_safety`** (core 4.2+4.6+2.2 only); **`AX_sexual_tension_explicit_intimacy`** (2.1+2.3+2.4+2.5); **`AX_coercion_risk_watchlist`** (7.4+7.2; manual review). Also: `AX_status_power` (6.1a+6.6+6.7), `AX_economic_dependency` (6.4), `AX_love_over_sex`, `AX_attraction` (2.1). Stage08 `axis_hint=no_hypothesis_signal` is a weak routing hint only. Design memos: `results/reports/stage09/taxonomy_v23_axis_context_design.md`, `taxonomy_v24_heuristic_hardening.md`.

---

## Dataset

### Corpus (primary): `romance_subdataset_filtered_v3`

The active modeling corpus lives under **`data/raw/romance_subdataset_filtered_v3/`**. It is the **English-only v3** cohort: the downloaded subsample v2 sentence tables with **460 non-English books removed** (language detection, `min_confidence` 0.6; see **`v3_filtering_manifest.json`** and **`language_analysis.csv`**). Upstream EPUBs and the full v2 cohort remain under **`data/raw/romance_subdataset_downloaded_v2_full/`** (see **`SUBSAMPLING_V2.md`**).

- **16,000** works kept (16,460 analyzed; 460 excluded)
- **8,264** distinct authors (`author_id` in metadata)
- **Publication years**: 2000–2017 (time-based split; missing years sorted first in train)
- **Genre mix** (metadata `genre_group`): other (5,756), paranormal (4,522), mystery (2,601), historical (1,765), young_adult (1,356)
- **Train / val / test** (time strategy, seed 42): **11,158 / 2,429 / 2,413** works (`subsampling_metadata/romance_subdataset_filtered_v3_{train,val,test}.csv`)
- **Sentence rows** (Stage 01 schema: `work_id`, chapter fields, `sentence_index`, `sentence`): **80,766,376 / 17,276,277 / 17,547,796** in `sentences_{train,val,test}.csv` (~**115.6M** total)

### Goodreads-linked metadata (per work, v3 full table)

Each cohort row includes aggregated Goodreads-style fields from the design frame (e.g. `average_rating_weighted_mean`, `ratings_count_sum`). Corpus-wide summaries on the **16,000** works:

- **Mean rating** (unweighted mean of per-work `average_rating_weighted_mean`): **3.91**
- **Range** of per-work mean rating: **1.27–5.00**
- **`ratings_count_sum`**: median **263**, mean **~3.0k** (long-tailed; vote counts vary strongly across works)

Metadata tables: `data/raw/romance_subdataset_filtered_v3/subsampling_metadata/romance_subdataset_filtered_v3_full.csv`.

### On-disk layout (Stages 01–05b)

| Location | Content |
|----------|---------|
| `data/raw/romance_subdataset_downloaded_v2_full/` | Source EPUBs and v2 `subsampling_metadata/` (Stage 01 ingestion input) |
| `data/raw/romance_subdataset_filtered_v3/` | v3 `sentences_{train,val,test}.csv`, `v3_filtering_manifest.json`, `subsampling_metadata/` |
| `data/processed/romance_subdataset_downloaded_v2_sentences/` | Original v2 sentence CSVs from Stage 01 (superseded for modeling by v3 paths in `configs/paths.yaml`) |
| `data/interim/booknlp_character_runs/` | Stage 02 name-extraction runs (`spacy_fast_*`, BookNLP `run_*` / shard dirs): checkpoints, manifests, per-split token lists |
| `data/interim/booknlp_models/` | Optional local cache for BookNLP weight files |
| `data/processed/custom_stoplist.txt` | Merged character-name stoplist (timestamped `*.bak_<timestamp>` backups alongside) |
| `data/interim/octis/v3_english_only/` | Pre-built OCTIS `corpus.tsv`, `corpus.offsets.npy`, `metadata.json` for v3 train+eval |
| `data/stage03_samples/` | Stratified fit/eval row indices (`fit_indices_seed42.npy`, `eval_indices_seed42.npy`, manifest) |
| `results/experiments/<run_id>/` | Stage 03 BO trials (`trials.csv`, `run_state.json`, per-model artifacts) |
| `results/selection/<run_id>/` | Stage 04 winner config, `top_k.csv`, `selection_report.md` |
| `models/final/<run_id>/` | Stage 05 refit artifacts (`train_only/`, `train_plus_val/`) |
| `results/evaluation/<run_id>/` | Stage 05b one-shot test holdout metrics |

Stages 01–02 do not write pipeline outputs under `results/` except optional documentation in **`results/reports/`**. Modeling artifacts from Stage 03 onward populate `results/` and `models/` per `configs/paths.yaml`.

## Methodology Overview

### 1. Topic Modeling: BERTopic + OCTIS

**Why BERTopic?** Unlike traditional LDA, BERTopic uses BERT embeddings to capture contextual word meanings, producing more interpretable topics for literary analysis.

**Optimization**: Bayesian hyperparameter optimization via OCTIS framework across:
- 3 Pareto-selected embedding models (SentenceTransformers):
  - `all-MiniLM-L12-v2` (Wang et al., 2020)
  - `paraphrase-mpnet-base-v2` (Yang et al., 2020)
  - `paraphrase-MiniLM-L6-v2` (Wang et al., 2020)
- UMAP, HDBSCAN, and vectorizer parameters
- 300+ configurations evaluated

**Model Selection**: Pareto efficiency analysis balancing coherence and diversity. Embedding priors were informed by a **100-book billionaire pretest**; taxonomy v2 and composite luxury indices were recalibrated for the **multi-genre v3 corpus** (no single billionaire-lifestyle topic expected).

**Fit sampling and search space**: BERTopic is fit on a stratified, train-only ~500k-sentence subsample (book-balanced, year-aware, author-capped, narrative-position-spread) selected as row indices into the full corpus, so the full-corpus embedding caches are reused by index rather than re-encoded; topics are then assigned to all books via `.transform()`. The OCTIS search space is a pretest-informed prior, adjusted for the 500k fit corpus. After an initial stratified run collapsed to 2–3 topics every trial, clustering bounds were narrowed (`hdbscan__min_cluster_size` 50–800, `bertopic__min_topic_size` 50–500) and topic words are filtered against a **fit-corpus** dictionary (not the smaller eval token set), so HDBSCAN clusters are not dropped artificially.

**BO objective and selection guards**: Bayesian optimization maximizes `CoherenceWithTopicPenalty` — vocab-filtered c_v coherence minus a linear shortfall when `n_topics < 20` (weight 0.15, aligned with Stage 04). Per-call checkpoints log raw `coherence_c_v`, `bo_objective`, `n_topics`, and `topic_diversity` in `trials_partial.csv`. Stage 04 drops trials with `n_topics < min_n_topics` (default 20) before Pareto-then-weighted ranking. Empirical pattern from the v2 run: `hdbscan__min_cluster_size` ≈ 65–165 yields many stable topics (often 100–500); values ≳ 180 tend to collapse to &lt; 20 topics despite high coherence.

See `results/reports/stage03/stage03_stratified_fit_sample_design.md` and `results/reports/stage03/stage03_bertopic_search_space_prior.md`.

**Character name exclusion** (Stage 02): Person-like tokens are extracted from sentence CSVs and merged (deduplicated) into `data/processed/custom_stoplist.txt` with a timestamped backup, so topic models can down-weight named-entity co-occurrence alongside generic English stopwords.

Two extractors are implemented in [`src/stage02_preprocessing/`](src/stage02_preprocessing/):

- **Production path — spaCy fast** (`extract_character_names_spacy_fast.py`): scans `sentences_{train,val,test}.csv` in resumable chunks (`--run-id`, `--resume`, `--max-chunks-per-run`); filters by global/book frequency; merges per split into the shared stoplist. Completed runs on the v2 sentence tables (`spacy_fast_full`, `spacy_fast_val`, `spacy_fast_test`) appended **~72.7k** deduplicated tokens total (**69,528** train + **1,254** val + **1,963** test new lines).
- **BookNLP path** (`extract_character_names_booknlp.py`): reconstructs per-work `.txt` from sentence CSVs, runs [BookNLP](https://github.com/booknlp/booknlp) (`entity` pipeline, `small` model by default), and merges `PER` / `PROP` surface forms from `.entities` (optional richer `--pipeline entity,quote,coref`). Supports sharding, ETA probes, and stratified `--stoplist-sample-books` for single-GPU runs.

Post-merge audit: `scripts/audit_stoplist_non_names.py` flags likely non-name entries (Zipf frequency + optional spaCy person probe).

### 2. LLM-Based Topic Labeling

**Challenge**: Topic models produce keyword lists requiring human interpretation. Manual labeling is impractical at scale (N topics).

**Solution**: Zero-shot labeling via Mistral-Nemo-Instruct through OpenRouter API.

**Key Design Decisions**:
- **Representative snippets**: Actual document excerpts provide scene-level context beyond keywords
- **Romance-aware prompts**: Domain-specific instructions for accurate labeling of romantic/erotic content
- **Anti-hallucination constraints**: Hard rules preventing common LLM inference errors

**Result**: N% of topics successfully labeled (/).

### 3. Theory-Aligned Category Mapping

Topics are mapped to two theoretical frameworks via zero-shot classification:

**Romance Corpus Taxonomy v2** (10 groups, 40+ leaf categories; config: `configs/stage09/romance_corpus_taxonomy_v2.yaml`):

1. Embodied & Sensory Experience — incl. **1.6 appearance**, **1.7 gaze/expression**
2. Sexuality, Attraction & Intimacy
3. Emotions, Cognition & Inner Life
4. Relationship Trajectory (Main Couple)
5. Social World Outside Couple
6. Work, Wealth, Status & Institutions — **6.1a** elite romantic status (axis) vs **6.1b** generic business (context); **6.6 material glamour**, **6.7 aristocracy**
7. Conflict, Risk & Harm
8. Spaces, Time, Activities & Objects — incl. **8.5 movement/transit**
9. Narrative Style & Discourse — **excluded from macro-axes**
10. Subgenre & Plot Engine

**Composite indices** (Stage 10): 28 axes built from the schema, including `material_social_display` (the H3 reframe), `appearance_presentation` (1.6 + 1.7), `dark_vs_tender`, `protective_vs_possessive` and `internal_ambivalence` (3.3, exploratory). `luxury_composite` and `luxury_x_love` are retained but rest almost entirely on empty components in this model, so they are reported as unmeasurable rather than as nulls. Every axis is audited for coverage before use in `axis_coverage.parquet`; components with no topics raise rather than silently evaluating to zero.

**Radway's 13 Narrative Functions** (Radway, 1984):
- Phase I (R1–R7): Initial Conflict & Isolation
- Phase II (R8–R10): Turning Point & Recognition
- Phase III (R11–R13): Commitment & Restoration

**Coverage**: Radway stage 2 is complete for call_49 (`placeholder_v4_call49_rerun2`): 182 of 348 topics mapped to R1–R13, 166 background. The Stage 10 notebooks still use the original taxonomy mapping without Radway columns; folding Radway in is a separate rebuild of `topic_lookup` and the analysis frame. See `results/reports/stage09/call49_rerun2_mapping_stability.md`.

### 4. Statistical Analysis

Design and rationale: [`configs/stage10/final_analysis.yaml`](configs/stage10/final_analysis.yaml). Walkthrough: [`notebooks/07_analysis/`](notebooks/07_analysis/).

**Hard topic assignments, not soft probabilities.** A book's measure for a topic is the share of its sentences whose argmax topic is that topic — read directly as "3.3% of this book's sentences". Averaging 374 probabilities over ~6,000 sentences per book leaves a median per-topic coefficient of variation of 0.087; hard counts give 0.898, roughly 10× more between-book signal, at the cost of the 0.74% of sentences assigned to the outlier topic. The soft tables are retained as a robustness comparison.

**Compositional data.** Shares sum to one, so every effect is a *relative reallocation* of narrative attention, never an absolute amount. Raw shares for description, ranks for tier tests, centred log-ratio (CLR) for regression, explicit log-ratios for the balance hypotheses (H1, H4).

**Two outcome channels, analysed separately:**
- **Perceived quality** — `average_rating_weighted_mean`, Bayesian-shrunk as `(v·R + m·C)/(v + m)` with `m` = 263 (corpus median rating count) and `C` = 3.910; fit weighted by `v/(v+m)`
- **Reach** — `log1p(ratings_count_sum)`

They correlate at only r = 0.21 shrunk (0.12 raw), under 5% shared variance, which is the empirical justification for not collapsing them into one "success" variable.

**Multiplicity and effect sizes.** Benjamini–Hochberg within each family separately (348 topics, ~45 leaves, ~11 main groups, 28 axes, 6 hypotheses); Holm within pairwise contrast families. Interpretation is gated on effect size and bootstrap CI, not p-values: at ~5,000 books per tier, 282 of 369 topics survive FDR while only 38 reach |Cliff's δ| ≥ 0.11. Reported as a funnel rather than a p-value list.

**Author and series confounding.** 5,353 of 8,264 authors have a single book, so author fixed effects are infeasible. Cluster-robust standard errors by author, 2,000-replicate cluster bootstrap, leave-one-author-out for headline results, per-topic author-dominance flags, and series as an alternative clustering level.

**Predictive check.** GroupKFold by author, 5 folds × 20 repeats: themes plus controls reach held-out R² = 0.111 against 0.097 for controls alone (length, era, genre). Themes add about 0.014 — real, positive in 99% of folds, and small.

**Narrative arc.** Within-book tertile deltas (begin/middle/end), which remove all book-level confounds by construction, plus a version renormalised within the relationship-leaf group to separate genuine reallocation from the compositional rise that affects every relational category at a book's end.

**Robustness.** Twelve specifications in notebook 08: hard vs soft aggregation, strict vs generous mapping, confidence and evidence-quality exclusions, on-label-only rebuilds from the close-reading audit, word- vs sentence-weighting, four book cohorts, presence-threshold aggregation, author and series clustering, genre and era subgroups, and the renormalised arc.

---

## Pipeline Overview

| Stage | Package | Description |
|-------|---------|-------------|
| 01 Ingestion | `stage01_ingestion` | v2 EPUBs → `sentences_{train,val,test}.csv` under `data/processed/romance_subdataset_downloaded_v2_sentences/` (resume via `.ckpt`); v3 English-only splits derived downstream |
| 02 Preprocessing | `stage02_preprocessing` | Character-name extraction (spaCy fast or BookNLP) on train/val/test → `custom_stoplist.txt`; resumable run dirs under `data/interim/booknlp_character_runs/`; `main.py` cleaning CLI still a stub |
| 03 Modeling | `stage03_train` | Stratified ~500k train fit sample + ~100k eval indices; BERTopic + OCTIS Bayesian optimization (3 embedding models, 120 calls/model); fit on train indices, score coherence/diversity on eval; outputs `results/experiments/<run_id>/trials.csv`; auto-resume via `run_state.json` — `python -m src.stage03_train.cli tune` |
| 04 Selection | `stage04_eval_select` | Drop trials with `n_topics < 20`, then Pareto frontier → weighted score (`0.4×coherence + 0.4×diversity − 0.1×outlier − 0.1×stability`); emits `winner_config.json` — e.g. run `stratified_minilm12v2_seed42_v2` → `all-MiniLM-L12-v2` |
| 05 Final fit | `stage05_final_fit` | Refit winner hyperparameters under two policies: **train-only** and **train+val** → `models/final/<run_id>/{train_only,train_plus_val}/` — `python -m src.stage05_final_fit.cli fit --policy both` |
| 05b Test holdout | `stage05b_test_holdout` | One-shot `.transform()` on `sentences_test.csv` (no refit); `test_metrics.json` + `final_topic_report.md`; refuses rerun unless `--allow-rerun` |
| 06 Topic Exploration | — | Multi-representation analysis |
| 07 Topic Quality | — | Noisy topic detection |
| 08 LLM Labeling | `stage08_llm_labeling` | Automated topic labeling |
| 09 Category Mapping | `stage09_category_mapping` | Zero-shot mapping of topics to taxonomy v2.4 leaves (stage 1) and Radway R1–R13 (stage 2; complete for call_49 under `placeholder_v4_call49_rerun2`) |
| 10 Correlation Analysis | `stage10_correlation_analysis` | Hard-assignment aggregation to book/tertile/chapter, the book analysis frame, and the statistics library behind `notebooks/07_analysis/` |

See **`results/reports/01_stage_reports/`** for detailed methodology per stage when those files are present in your checkout.

---


## Key Findings

From the final model (call_49, 348 mapped topics, 16,000 books). Effects are Cliff's δ for the high-rated vs low-rated contrast, ~5,000 books per tier.

### No hypothesis clears the bar; three unpredicted findings do

Two hypotheses came back reliably in the *opposite* direction (H1, H3), one showed no effect (H2), and three were directionally consistent but below the effect threshold (H4, H5, H6). In each case the composite axis cancelled out, and the leaves beneath it were more informative — so the strongest results are ones the hypothesis frame obscured.

| Finding | Effect | Robustness |
|---|---|---|
| **External violence and threat is the strongest theme signal** (`7.2`, 13 topics). Danger, weapons, captivity and coercion from *outside* the couple | δ = **+0.163** | Holds in every genre and era, under every specification, and among singleton authors (+0.122). The most attacked and least moved result |
| **Character appearance description is a negative marker** (`1.6`, 15 topics). Clothing, hair, physique, self-presentation | δ = **−0.145** | Negative in all nine genre and era subgroups; −0.156 word-weighted; −0.108 among singleton authors. Robust, and the mechanism is unexplained |
| **Moral and value reflection** (`3.4`) | δ = **+0.130** | Stable across every check, but rests on a single topic |
| Family, kinship and parenthood (`5.1`) | δ = +0.101 | — |
| Emotional safety and caretaking (`4.6`, 30 topics) | δ = +0.095 | Halves to +0.042 among singleton authors, so partly an *authorial* rather than book-level effect. H1 and H4 both rest on this leaf |
| Risk, danger and external crisis (`7.3`) | δ = +0.093 | — |
| Couple conflict and breakup threats (`4.4`) | δ = −0.039 | Small, and the only leaf with perfect sign agreement across all twelve specifications |

The distinction between `7.2` and `4.4` is the substantive result: *external* threat is markedly more present in well-rated romance, while the couple quarrelling internally is slightly less present.

### Quality and reach are different questions

Of 45 taxonomy leaves, 7 act on perceived quality only, 10 on reach only, 8 on both with the same sign, 6 with opposite signs, and 14 on neither. At axis level the pattern is the same: violence and coercion is quality-only (standardised β = +0.169 quality against +0.021 reach), material and social display depresses quality (β = −0.172) while barely touching reach, and explicitness is one of the few that lifts both (+0.141 and +0.192). Treating "success" as a single variable would average these apart.

### Themes explain little of the variance, and that is a finding

Themes add roughly 0.014 to held-out R² over length, era and genre alone — positive in 99% of folds, so real, and small. Most of what makes a romance novel well-rated is not what it is about. A corpus of 16,000 books does not buy large effects here; it buys the ability to state confidently that the effects are small.

### Measurement findings that changed the interpretation

Close reading of the headline leaves (notebook 07) found that LLM-assigned taxonomy labels are unevenly faithful, and that Stage09 confidence scores do **not** identify the bad ones:

- `2.3 "Explicit Sexual Acts"` is 72% not explicit — it pools kissing, undressing and embracing with explicit acts. Rebuilt from only the four genuinely explicit topics, its effect flips from +0.027 to **−0.057**. H1's predicted trade-off does exist; it was invisible because of the label
- `1.6 "Character Appearance"` mixes dress and grooming with emotional closeness, photography and flowers
- `7.2` and `4.4` are faithful, which is part of why those results survive everything

Two sampled books turned out not to be romance novels at all (a clothing-history reference work and a WWI military history), which prompted a systematic romance-core-mass detector; restricting to books above 15% romance core changes nothing.

### An unexplained era gradient

Every theme discriminates two to three times more sharply among books published 2000–2004 than among 2010–2014 books (violence: +0.351 vs +0.142; appearance: −0.236 vs −0.138). Since the corpus is 68% 2010–2014, the headline numbers sit near the weaker end of that range. Whether this reflects changing reader behaviour or the rise of noisier self-published ratings cannot be settled here.

Full results, tables and figures: [`notebooks/07_analysis/`](notebooks/07_analysis/) and `results/stage10_correlation_analysis/v4_l12_granular_final_call49/notebook_analysis/`.

---

## Limitations

Stated plainly because several of them bound what the findings can mean.

- **H3 as originally specified is not measurable.** The model has no usable luxury or elite-status vocabulary: one mention each of "estate", "earl" and "gown" across 348 topics, and zero of billionaire, CEO, penthouse, duke, diamond or champagne. `6.1a` and `6.7` have no topics at all and `6.6` has one, holding 0.11% of topic mass. This is a substantive measurement finding about a multi-genre romance corpus at 348 topics, not a null result about reader taste.
- **Taxonomy labels are unevenly faithful**, and confidence scores do not flag the unfaithful ones. Only four leaves have been audited by close reading; one of the four changed sign when rebuilt from verified topics. Extending the audit is the highest-value next step.
- **Thin leaves.** `4.7`, `5.3a`, `6.4`, `6.6`, `8.3a` and `3.4` rest on one or two topics each, so any axis built on them is underpowered by construction. `2.4` (post-sex aftercare) is empty upstream at Stage08, so aftercare cannot be separated from explicit content.
- **Composite axes have low internal reliability.** Summing taxonomy leaves that compete for the same share budget produces composites whose components often disagree; where they do, the components are believed over the composite.
- **Author effects cannot be fully removed.** With 5,353 single-book authors, author fixed effects are infeasible. The `4.6` result in particular halves once multi-book authors are excluded.
- **Ratings are noisy for the 1,909 books with under 30 ratings**, hence shrinkage and weighting; unweighted and `n ≥ 30` fits are reported as sensitivity checks.
- **Shares are compositional.** All effects are relative reallocations of narrative attention. Nothing here says a book contains *more* violence in absolute terms, only that a larger fraction of its sentences do.
- **Radway functions are mapped for call_49 but not yet wired into Stage 10.** The re-run produced `taxonomy_with_radway.json` (182 of 348 topics on R1–R13); the analysis frame still has null `radway_*` columns until `topic_lookup` is rebuilt from it.
- **Associational, not causal.** Ratings are observational and confounded by prose quality, editing, cover, marketing and platform dynamics that no theme measure here captures.

---

## Theoretical Framework

This research draws on:

- **Radway (1984)**: Narrative function analysis of romance fiction
- **Ogas & Gaddam (2011)**: Reader psychology and genre preferences

The category mapping operationalizes these theoretical constructs for quantitative analysis.

---

## References

Bamman, D., Underwood, T., & Smith, N. A. (2013). A Bayesian Mixed Effects Model of Literary Character. *Proceedings of ACL*.

Egger, R., & Yu, J. (2022). A topic modeling comparison between LDA, NMF, Top2Vec, and BERTopic. *Frontiers in Sociology*, 7, 886498.

Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. *arXiv:2203.05794*.

Jiang, A. Q., et al. (2023). Mistral 7B. *arXiv:2310.06825*.

Jockers, M. L. (2013). *Macroanalysis: Digital Methods and Literary History*. University of Illinois Press.

Radway, J. A. (1984). *Reading the Romance: Women, Patriarchy, and Popular Literature*. University of North Carolina Press.

Röder, M., Both, A., & Hinneburg, A. (2015). Exploring the space of topic coherence measures. *WSDM*.

Terragni, S., et al. (2021). OCTIS: Comparing and optimizing topic models is simple! *EACL*.

---

## Further Reading

| Topic | Location |
|-------|----------|
| Stages 01–02 (ingestion, stoplist) | [`src/stage01_ingestion/README.md`](src/stage01_ingestion/README.md), [`src/stage02_preprocessing/README.md`](src/stage02_preprocessing/README.md) |
| Stages 03–05b (train / select / fit / test) | [`src/stage03_train/PIPELINE_OVERVIEW.md`](src/stage03_train/PIPELINE_OVERVIEW.md) |
| Final analysis walkthrough (nine notebooks) | [`notebooks/07_analysis/README.md`](notebooks/07_analysis/README.md) |
| Stage 10 code and design | [`src/stage10_correlation_analysis/README.md`](src/stage10_correlation_analysis/README.md) |
| Stage 09 mapping quality | `results/reports/stage09/` |
| Stage methodology | `results/reports/01_stage_reports/` |
| Hypothesis testing results | `results/reports/02_findings/hypothesis_testing/` |
| LLM labeling methodology | `results/reports/02_findings/methodology_llm_labeling_and_taxonomy/` |
| Implementation details | [`src/`](src/) stage READMEs |
