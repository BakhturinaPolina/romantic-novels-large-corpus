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

Each hypothesis was pre-registered in `configs/stage09/theory_aligned_index_schema.yaml` with a primary axis, then tested as specified. A **result** requires all three of: the predicted direction, a bootstrap confidence interval excluding zero, and |Cliff's δ| ≥ 0.11. The threshold was set before the tests ran; with roughly 5,000 books per tier (low 5,389 · mid 5,524 · high 5,086; analysis frame n = 15,999 books, 8,263 authors) statistical significance alone separates almost nothing.

Stage 10 tested taxonomy-leaf composites directly. Stage 11 (17 contextual-audit notebooks in [`notebooks/08_refined_construct_analysis/`](notebooks/08_refined_construct_analysis/)) froze a dictionary of contextually validated constructs and re-tested. The **Stage 11 column is the final confirmatory source**; NB13 also publishes a [post-freeze claim hierarchy](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/post_freeze_claim_hierarchy.csv) (confirmatory / qualified / open / unmeasurable / unsupported) and a [robustness traffic light](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/robustness_traffic_light.csv) that gates the component-level claims below.

| # | Hypothesis | Stage 10 (taxonomy baseline) | Stage 11 (contextually refined) |
|---|---|---|---|
| H1 | **Love-over-Sex** | **Contradicted** (δ = −0.029) | **Directional** (δ = +0.099), below gate |
| H2 | **HEA Index** | **Directional** (δ = +0.027) | **Unmeasurable** after strict HEA refinement |
| H3 | **Material display** | **Contradicted** (δ = −0.146) | **Unmeasurable** after material-side freeze |
| H4 | **Protectiveness vs Possessiveness** | **Directional** (δ = +0.090) | **Thin / inconclusive** (δ = +0.090); protection atom is single-topic |
| H5 | **Darkness vs Tenderness** | **No reliable effect** (δ = +0.012) | **Contradicted** (δ = −0.031) |
| H6 | **Narrative Arc** | **Partly supported** (δ = +0.044) | **Contradicted** (δ = −0.053) |

Stage 10 tests: [`notebooks/07_analysis/05_hypothesis_tests.ipynb`](notebooks/07_analysis/05_hypothesis_tests.ipynb). Stage 11 final verdicts: [`final_verdict_table.md`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/final_verdict_table.md). Side-by-side comparison: [`stage10_vs_final_side_by_side.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/stage10_vs_final_side_by_side.csv).

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

**Analysis frame (Stage 10 / Stage 11):** one work with a missing Goodreads rating is dropped, leaving **n = 15,999 books** and **8,263 authors** in the confirmatory frame. Tier splits are **low = 5,389 · mid = 5,524 · high = 5,086** (NB13 [`sanity_summary.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/sanity_summary.csv), [`tier_sizes.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/tier_sizes.csv)).

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

**Refined constructs** (Stage 11): The 17 contextual-audit notebooks (`notebooks/08_refined_construct_analysis/`) replaced taxonomy-leaf composites with dictionary-driven constructs validated by close reading. Topics were re-coded for contextual function (e.g. a "kiss" topic may serve emotional reassurance, not explicit sex); constructs whose topic mass could not survive the audit were frozen as **unmeasurable** (H2, H3) or **thin** (H4 protection atom). The refined dictionary and measurement gates are in `results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/07_refined_construct_dictionary/` and `08_refined_axes_validity/`.

**Radway's 13 Narrative Functions** (Radway, 1984):
- Phase I (R1–R7): Initial Conflict & Isolation
- Phase II (R8–R10): Turning Point & Recognition
- Phase III (R11–R13): Commitment & Restoration

**Coverage**: Radway stage 2 is complete for call_49 and folded into `topic_lookup.parquet` (182 of 348 topics on R1–R13, 166 background). The Stage 10 hypothesis notebooks still test taxonomy leaves and theory axes; Radway phase analysis is available as a follow-on. See `results/reports/stage09/call49_rerun2_mapping_stability.md`.

### 4. Statistical Analysis

Design and rationale: [`configs/stage10/final_analysis.yaml`](configs/stage10/final_analysis.yaml). Stage 10 walkthrough: [`notebooks/07_analysis/`](notebooks/07_analysis/). Stage 11 refined tests: [`notebooks/08_refined_construct_analysis/13_final_statistical_tests.ipynb`](notebooks/08_refined_construct_analysis/13_final_statistical_tests.ipynb).

**Hard topic assignments, not soft probabilities.** A book's measure for a topic is the share of its sentences whose argmax topic is that topic — read directly as "3.3% of this book's sentences". Averaging 374 probabilities over ~6,000 sentences per book leaves a median per-topic coefficient of variation of 0.087; hard counts give 0.898, roughly 10× more between-book signal, at the cost of the 0.74% of sentences assigned to the outlier topic. The soft tables are retained as a robustness comparison.

**Compositional data.** Shares sum to one, so every effect is a *relative reallocation* of narrative attention, never an absolute amount. Raw shares for description, ranks for tier tests, centred log-ratio (CLR) for regression, explicit log-ratios for the balance hypotheses (H1, H4).

**Two outcome channels, analysed separately:**
- **Perceived quality** — `average_rating_weighted_mean`, Bayesian-shrunk as `(v·R + m·C)/(v + m)` with `m` = 263 (corpus median rating count) and `C` = 3.910; fit weighted by `v/(v+m)`
- **Reach** — `log1p(ratings_count_sum)`

They correlate at only Pearson r = **0.206** shrunk (**0.124** raw), Spearman ρ = 0.156 shrunk — under 5% shared variance, which is the empirical justification for not collapsing them into one "success" variable (NB16 [`channel_correlations.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/16_refined_goodreads_quality_reach/tables/channel_correlations.csv)).

**Multiplicity and effect sizes.** Benjamini–Hochberg within each family separately (348 topics, ~45 leaves, ~11 main groups, 28 axes, 6 hypotheses); Holm within pairwise contrast families. Interpretation is gated on effect size and bootstrap CI, not p-values: with 5,389 / 5,524 / 5,086 books per tier, 282 of 369 topics survive FDR while only 38 reach |Cliff's δ| ≥ 0.11. Reported as a funnel rather than a p-value list.

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
| 11 Refined Construct Analysis | `stage11_refined_construct_analysis` | Contextual audit of H1–H6 operationalizations (17 notebooks); dictionary freeze; refined hypothesis tests; post-freeze claim hierarchy; exploratory emotion/embodiment/social-world and quality-vs-reach analyses |

See **`results/reports/01_stage_reports/`** for detailed methodology per stage when those files are present in your checkout.

---


## Key Findings

From the final model (call_49, 373 modeled / 348 mapped topics, 16,000 works; analysis frame n = 15,999 books, 8,263 authors). Confirmatory effects are Cliff's δ for the high-rated vs low-rated contrast (n_low = 5,389 · n_mid = 5,524 · n_high = 5,086). The **Stage 11 refined constructs (NB13) are the confirmatory source of truth**; Stage 10 leaf effects are retained below as the motivating baseline that prompted the audit.

### No broad H1–H6 hypothesis survives as a clean confirmation

Under Stage 11 refined measurement, two hypotheses became unmeasurable (H2, H3), one is directionally consistent but below the effect gate (H1), one is thin/inconclusive (H4), and two are contradicted (H5, H6). Every broad axis cancelled or thinned once its topic mass was contextually validated; the confirmatory signal that persists is at the *component* level.

| Hyp | Refined feature | δ (Stage 11) | Gate | Verdict |
|---|---|---|---|---|
| H1 | `RLR_emotional_vs_explicit` | **+0.099** | viable | Directional, below gate |
| H2 | `RAX_h2_strict` (final payoff) | — | unmeasurable | Unmeasurable |
| H3 | `RLR_emotional_vs_material_security` | — | unmeasurable | Unmeasurable |
| H4 | `RLR_protection_vs_control` | **+0.090** | thin (1 topic) | Inconclusive |
| H5 | `RLR_darkness_vs_tenderness` | **−0.031** | viable | Contradicted |
| H6 | `RARC` (refined arc contrast) | **−0.053** | viable | Contradicted |

Source: NB13 [`primary_h1_h6_table.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/primary_h1_h6_table.csv), [`final_verdict_table.md`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/final_verdict_table.md).

### Component-level effects that clear the gate

Six refined narrative-function components have |δ| ≥ 0.11 with CIs excluding zero. Interpret each as a component association, **not** as confirmation of its parent hypothesis:

| Component | δ | 95% CI | Robustness | Note |
|---|---|---|---|---|
| Appearance / grooming (`RAX_appearance_grooming`) | **−0.142** | [−0.170, −0.114] | ✓ strong | Clothes, hair, physique, self-presentation. Negative in every genre and era subgroup |
| External protection (`RAX_external_protection`) | **+0.160** | [+0.133, +0.188] | ⚠ thin / provisional | Enacted rescue/defence from outside danger. **One topic (t119)** — open marker |
| Emotional reassurance (`RAX_emotional_reassurance`) | **+0.136** | [+0.105, +0.168] | ✓ strong (H1 component) | Comfort, holding, "you're safe" beats |
| Tenderness core (`RAX_tenderness_core`) | **+0.135** | [+0.104, +0.165] | ✓ strong (H5 component) | Nuzzling, gentle touch, soft affect |
| External danger / crisis (`RAX_external_danger_crisis`) | **+0.116** | [+0.089, +0.143] | ✓ strong (H5 component; qualified) | Threat, weapons, chases from outside the couple |
| Explicit sex (`RAX_explicit_sex`) | −0.075 | [−0.104, −0.044] | ⚠ moderate | Directional, below gate |

Source: NB13 [`component_effects.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/component_effects.csv), [`robustness_traffic_light.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/robustness_traffic_light.csv).

Composite axes cancel because their components compete for the same compositional budget: H5 darkness-vs-tenderness composite δ = −0.031 hides tenderness core +0.135 *and* external danger +0.116. The composite tests the balance; the components test the components. Both are informative when reported honestly.

### Quality and reach are different questions

Rebuilt on 76 refined Stage 11 features against Bayesian-shrunk rating (quality) and `log1p(ratings_count_sum)` (reach). Channel pattern counts (NB16 [`channel_pattern_counts.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/16_refined_goodreads_quality_reach/tables/channel_pattern_counts.csv)):

| Pattern | n features |
|---|---|
| Both same sign | 22 |
| Reach only | 22 |
| Quality only | 14 |
| Neither | 11 |
| Opposite signs | 7 |

**Largest trade-offs** (opposite signs — the same theme moves quality and reach in opposite directions):

- Grooming / self-presentation: appreciation β = **−0.152** vs reach β = **+0.070** — the appearance signal that depresses ratings actively lifts reach
- Non-explicit affection: appreciation β = **+0.055** vs reach β = **−0.065**
- Body grooming (EES): appreciation β = **−0.117** vs reach β = **+0.064**

**Appreciation-specific** (quality-only): enacted protection (β = **+0.109**), emotional co-regulation, body markings, felt-vs-looked-at body, cognitive rumination — all move ratings without moving reach.

**Reach-specific** (reach-only): explicit sex (β = **+0.083**), relational darkness (β = **+0.088**), hierarchy/power, looked-at body — content that grows audience without lifting appreciation.

**Dual-channel same sign** (economic pressure, transactional business talk, generic logistics all negative on both; emotion containment, felt body positive on both) show the coarse ceiling / floor patterns that cross both channels.

Residual quadrants (after removing length/era/genre controls): 4,383 "stars" (high quality, high reach), 3,617 "hidden gems" (high quality, low reach), 3,617 "popular but poor," 4,382 "low-low" (NB16 [`residual_quadrant_counts.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/16_refined_goodreads_quality_reach/tables/residual_quadrant_counts.csv)). Treating "success" as one variable would average these apart.

Source: NB16 [`presentation_quality_reach_shortlist.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/16_refined_goodreads_quality_reach/tables/presentation_quality_reach_shortlist.csv) and [`synthesis_quality_reach.md`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/16_refined_goodreads_quality_reach/tables/synthesis_quality_reach.md).

### Themes explain little of the variance, and that is a finding

Themes add roughly 0.014 to held-out R² over length, era and genre alone — positive in 99% of folds, so real, and small. Most of what makes a romance novel well-rated is not what it is about. A corpus of 16,000 books does not buy large effects here; it buys the ability to state confidently that the effects are small.

### Measurement findings that changed the interpretation

Close reading of the headline leaves (Stage 10 notebook 07 and Stage 11 NB01–NB06) found that LLM-assigned taxonomy labels are unevenly faithful, and that Stage 09 confidence scores do **not** identify the bad ones. Contextual agreement rates by hypothesis: **H1 55%, H2 30%, H3 53%, H4 34%, H5 50%, H6 35%** — lexical cues frequently changed meaning in context. Concrete cases:

- `2.3 "Explicit Sexual Acts"` is 72% not explicit — it pools kissing, undressing and embracing with explicit acts. Rebuilt from only the four genuinely explicit topics, the leaf effect flips from +0.027 to −0.057; the Stage 11 refined `RAX_explicit_sex` (12 topics) settles at δ = −0.075
- `1.6 "Character Appearance"` mixes dress and grooming with emotional closeness, photography and flowers; the refined `RAX_appearance_grooming` isolates the grooming/self-presentation subset (δ = −0.142)
- `7.2 "External Threat"` and `4.4 "Couple Conflict"` are ~92–100% faithful, which is part of why those results survive everything

Two sampled books turned out not to be romance novels at all (a clothing-history reference work and a WWI military history), which prompted a systematic romance-core-mass detector; restricting to books above 15% romance core changes nothing.

### An unexplained era gradient

Every theme discriminates two to three times more sharply among books published 2000–2004 than among 2010–2014 books (Stage 10 leaves: violence +0.351 vs +0.142; appearance −0.236 vs −0.138). Since the corpus is 68% 2010–2014, the headline numbers sit near the weaker end of that range. Whether this reflects changing reader behaviour or the rise of noisier self-published ratings cannot be settled here.

### Stage 10 leaf baseline (motivating context)

Before refinement, taxonomy-leaf effects gave the following headlines. These are retained as a historical baseline that motivated the Stage 11 audit; where a Stage 11 refined component replaces or contradicts a Stage 10 leaf, the refined value governs.

| Stage 10 leaf | δ | Fate after Stage 11 |
|---|---|---|
| External violence and threat (`7.2`, 12 topics) | **+0.152** | Survives as refined `RAX_external_danger_crisis` (+0.116) — same signal, cleaner measurement |
| Character appearance (`1.6`, 15 topics) | **−0.147** | Survives as refined `RAX_appearance_grooming` (−0.142) — subset that is actually grooming/self-presentation |
| Moral and value reflection (`3.4`) | **+0.130** | Rests on a single topic; not carried into the refined dictionary |
| Interpersonal non-romantic conflict (`7.1`) | +0.104 | Not refined as a hypothesis-linked component |
| Family, kinship and parenthood (`5.1`) | +0.097 | Reappears in NB15 as `EES_family_presence` δ = +0.046 (exploratory) |
| Emotional safety and caretaking (`4.6`, 30 topics) | +0.092 | Splits into `RAX_emotional_reassurance` (+0.136, strong) and neutral practical care |
| Couple conflict and breakup threats (`4.4`) | −0.031 | Absorbed into `RAX_relational_darkness` (+0.065, directional) |

Full Stage 10 results, tables and figures: [`notebooks/07_analysis/`](notebooks/07_analysis/) and `results/stage10_correlation_analysis/v4_l12_granular_final_call49/notebook_analysis/`.

### Stage 11: contextual refinement changed the conclusions

Stage 11 audited every hypothesis operationalization by close-reading the topics that composed each construct, re-coding them for contextual function, and freezing a validated dictionary before re-running the tests. The results differ from Stage 10 in three ways:

1. **Two hypotheses became unmeasurable.** H2 (HEA) lost its topic mass under strict final-payoff operationalization. H3 (material display) lost its material side after the economic/status topics were frozen as contextually unfaithful. These are not null results — they are measurement findings about what a 373-topic model at this granularity can and cannot distinguish. Do not report them as δ = 0.

2. **Three hypotheses changed direction.** H1 flipped from contradicted (δ = −0.029) to directionally positive (+0.099) once the emotional-vs-explicit ratio was rebuilt from contextually verified topics. H5 and H6 moved from near-zero / partly-supported to contradicted (−0.031 and −0.053).

3. **Component-level signals persisted.** The strongest topic-level effects (external danger δ = +0.116, appearance/grooming δ = −0.142, tenderness δ = +0.135, emotional reassurance δ = +0.136) survived refinement and remain robust across specifications. These are confirmatory *component* effects, not confirmation of the parent H1–H6 hypotheses.

The post-freeze claim hierarchy (confirmatory / qualified / open / unmeasurable / unsupported), robustness traffic light, and full Stage 10 vs Stage 11 side-by-side are in [`results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/).

### Exploratory extensions (NB14 attention shifts, NB15 EES post-hoc)

Below are **exploratory** patterns from Stage 11 auxiliary notebooks. They do not change any H1–H6 verdict and are not confirmatory.

**Attention shifts (NB14, [`attention_waterfall.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/14_exploratory_presentation_results/tables/attention_waterfall.csv))** — compositional reallocation of narrative attention between the high-rated and low-rated tiers, in percentage-point units of book-share:

- Tenderness core: **+0.416 pp**
- Relational darkness / conflict: +0.148 pp
- Emotional reassurance / security: +0.068 pp
- Enacted protection: +0.055 pp
- External danger: +0.030 pp
- Appearance / grooming: **−0.180 pp**
- Explicit sex: **−0.186 pp**

**Emotion / embodiment / social-world exploration (NB15, [`integrated_summary_effects.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/15_emotion_embodiment_social_world_exploration/tables/integrated_summary_effects.csv))** — dictionary-driven post-hoc constructs; provisional pending human freeze:

- **Body grooming** δ = **−0.130** (approaches gate; consistent with grooming-as-negative signal)
- **Body markings** δ = **+0.098** (scars, tattoos as narrative-relevant embodiment)
- **Supportive social embeddedness** δ = **+0.078** (friend-group, chosen-family beats)
- **Felt body** δ = +0.064 vs **looked-at body** δ = −0.063 — a first-person interoceptive/vulnerable body reads positively; a third-person appraised body reads negatively
- **Visible affect** δ = +0.070, **co-regulation** δ = +0.068, **physiological arousal** δ = +0.067 — the emotion cluster of high-rated romance is expressive and interactive
- **Family presence** δ = +0.046 (below gate but consistent)

**Thematic richness (NB14 [`thematic_richness_cliffs_delta.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/14_exploratory_presentation_results/tables/thematic_richness_cliffs_delta.csv))** shows a positive tier-level rating association for taxonomy diversity (n_eff) but very weak two-channel adjusted β = +0.009 quality / +0.043 reach — richness reads primarily as a reach signal in the adjusted model.

Labelled **EXPLORATORY** because: NB15 constructs are provisional pending human freeze; NB14 attention shifts are tier-mean descriptive statistics without hypothesis pre-registration; both are excluded from confirmatory claims about H1–H6.

---

## Limitations

Stated plainly because several of them bound what the findings can mean.

- **H3 as originally specified is not measurable.** The model has no usable luxury or elite-status vocabulary: one mention each of "estate", "earl" and "gown" across 348 topics, and zero of billionaire, CEO, penthouse, duke, diamond or champagne. `6.1a` and `6.7` have no topics at all and `6.6` has one, holding 0.11% of topic mass. This is a substantive measurement finding about a multi-genre romance corpus at 348 topics, not a null result about reader taste.
- **Taxonomy labels are unevenly faithful**, and confidence scores do not flag the unfaithful ones. Stage 11 audited all six hypothesis families by close reading; two hypotheses (H2, H3) became unmeasurable and one (H1) changed sign when rebuilt from verified topics. The audit is documented in `notebooks/08_refined_construct_analysis/` (NB01–NB06).
- **Thin leaves.** `4.7`, `5.3a`, `6.4`, `6.6`, `8.3a` and `3.4` rest on one or two topics each, so any axis built on them is underpowered by construction. `2.4` (post-sex aftercare) is empty upstream at Stage08, so aftercare cannot be separated from explicit content.
- **Composite axes have low internal reliability.** Summing taxonomy leaves that compete for the same share budget produces composites whose components often disagree; where they do, the components are believed over the composite.
- **Author effects cannot be fully removed.** With 5,353 single-book authors, author fixed effects are infeasible. The `4.6` result in particular halves once multi-book authors are excluded.
- **Ratings are noisy for the 1,909 books with under 30 ratings**, hence shrinkage and weighting; unweighted and `n ≥ 30` fits are reported as sensitivity checks.
- **Shares are compositional.** All effects are relative reallocations of narrative attention. Nothing here says a book contains *more* violence in absolute terms, only that a larger fraction of its sentences do.
- **Radway functions are mapped into `topic_lookup` for call_49** (182 of 348 topics on R1–R13) but the H1–H6 notebooks still analyse taxonomy leaves; a Radway-phase chapter has not been run.
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
| Stage 11 refined construct analysis | [`notebooks/08_refined_construct_analysis/README.md`](notebooks/08_refined_construct_analysis/README.md), [`final_verdict_table.md`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/final_verdict_table.md), [`post_freeze_claim_hierarchy.csv`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/13_final_statistical_tests/tables/post_freeze_claim_hierarchy.csv), [`synthesis_quality_reach.md`](results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/notebook_analysis/16_refined_goodreads_quality_reach/tables/synthesis_quality_reach.md) |
| Presentation deck v2 (20 main + 14 appendix slides) | [`results/presentation/final_v2/slides/`](results/presentation/final_v2/slides/), review notebook [`notebooks/09_presentation/00_presentation_review.ipynb`](notebooks/09_presentation/00_presentation_review.ipynb) |
| Stage 09 mapping quality | `results/reports/stage09/` |
| Stage methodology | `results/reports/01_stage_reports/` |
| Hypothesis testing results | `results/reports/02_findings/hypothesis_testing/` |
| LLM labeling methodology | `results/reports/02_findings/methodology_llm_labeling_and_taxonomy/` |
| Implementation details | [`src/`](src/) stage READMEs |
