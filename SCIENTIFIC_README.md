# Scientific Methodology: Romance Novels — Themes × Reader Appreciation

**A Mixed-Methods Computational Analysis**

This document provides an overview of the research methodology and findings. For implementation details, see **`results/reports/`** (markdown reports) and stage-specific documentation in [`src/`](src/).

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

---

## Research Hypotheses

| # | Hypothesis | Operationalization |
|---|------------|-------------------|
| H1 | **Love-over-Sex**: Higher-rated novels emphasize emotional connection over explicit content | `AX_payoff_safety − AX_explicitness` (4.5+3.1 minus 2.3) |
| H2 | **HEA Index**: Stronger "Happily Ever After" signals predict appreciation | `4.5 + 5.3 + 0.5×8.3` (`AX_hea_index`) |
| H3 | **Luxury × Love**: Wealth/glamour appeals mainly when paired with emotional depth | `AX_luxury_composite × AX_payoff_safety` |
| H4 | **Protectiveness vs Possessiveness**: Caring protection valued over jealousy | `AX_protective_care − AX_possessiveness` (4.6 − 4.7) |
| H5 | **Darkness vs Tenderness**: Top-rated novels favor tenderness over dark themes | `(3.2+4.4+7.2+7.3) − (3.1+2.2)` (`AX_dark_vs_tender`) |
| H6 | **Narrative Arc**: Successful romances progress from conflict to resolution | `AX_narrative_arc_repair` — tertile Δ only (begin→end) |

Macro-axis notes (v2.2): Full schema in `configs/stage09/theory_aligned_index_schema.yaml`. Taxonomy v2.2 in `configs/stage09/romance_corpus_taxonomy_v2.yaml`. Three intimacy axes for H1 (exploratory): **`AX_everyday_intimacy_emotional_safety`** (core 4.2+4.6+2.2; low-weight 4.1/8.1/8.2); **`AX_sexual_tension_explicit_intimacy`** (2.1+2.3+2.4+2.5); **`AX_coercion_risk_watchlist`** (7.4+7.2; 4.7 optional context, manual review). Also: `AX_status_power` (6.1+6.6+6.7), `AX_love_over_sex`, `AX_attraction` (2.1), `AX_explicitness` (2.3); H4 uses **4.6/4.7**; H6 requires segment-level tertile deltas.

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

See `results/reports/stage03_stratified_fit_sample_design.md` and `results/reports/stage03_bertopic_search_space_prior.md`.

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
6. Work, Wealth, Status & Institutions — **6.1 de-biased** from billionaire CEO; **6.6 material glamour**, **6.7 aristocracy**
7. Conflict, Risk & Harm
8. Spaces, Time, Activities & Objects — incl. **8.5 movement/transit**
9. Narrative Style & Discourse — **excluded from macro-axes**
10. Subgenre & Plot Engine

**Composite indices** (Stage 10): `luxury_composite` (6.1×0.5 + 6.6 + 6.7 + 5.3 + 8.2 + 8.3), `appearance_presentation` (1.6 + 1.7), `luxury_x_love` for H3.

**Radway's 13 Narrative Functions** (Radway, 1984):
- Phase I (R1–R7): Initial Conflict & Isolation
- Phase II (R8–R10): Turning Point & Recognition
- Phase III (R11–R13): Commitment & Restoration

**Coverage**: 272 topics mapped to Radway functions; 96 classified as background/contextual.

### 4. Statistical Analysis

**Two-Channel Approach**: Separates analysis of:
- **Mass Appeal** (log rating count): What makes books popular/visible?
- **Perceived Quality** (rating mean): What makes readers rate books highly?

**Methods**:
- Bootstrap inference (800 iterations, 95% CI)
- Cross-validation (20 × 5-fold CV)
- Effect sizes (Cliff's δ) for tier comparisons
- Narrative arc analysis via tertile comparisons (begin/middle/end)

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
| 09 Category Mapping | — | Theory-aligned classification |
| 10 Correlation Analysis | `stage10_correlation_analysis` | Statistical hypothesis testing |

See **`results/reports/01_stage_reports/`** for detailed methodology per stage when those files are present in your checkout.

---


## Key Findings

### Mass Appeal (Popularity)

Books with higher rating counts emphasize:
- **Status/dominance themes** (elite profession 6.1, economic security 6.4 — reach axis)
- **Material luxury composite** (fashion, weddings, hotels, historical glamour — not CEO/billionaire topics alone)
- **Emotional safety** (protective care, repair after conflict)
- **Social support** (family, friends, community)

Books with lower rating counts emphasize:
- **Explicit sexual content** (negative association with popularity)

### Perceived Quality (Ratings)

After controlling for popularity, higher-rated books show:
- **More protective caretaking** (positive)
- **More emotional safety** (positive)
- **Less explicit erotica** (negative)
- **Less baseline negative affect** (negative)

### Narrative Arc

Higher-rated books demonstrate better pacing:
- Lower baseline negativity throughout
- Stronger late-story "crisis escalation" (third-act tension)
- Anger/frustration increases toward ending (then resolves)

### Topic-Level Patterns

- **85 discriminative topics** identified (of 342 analyzed)
- **Top-associated themes**: Psychological credibility (fear admissions, emotional delusion), embodied intimacy (affectionate stares, lip biting)
- **Trash-associated themes**: Explicit sexual content, procedural/transition scenes

### Meta-Finding

> Thematic content better explains **popularity** (market reach) than **star ratings** (reader evaluation).

Star ratings likely influenced by factors beyond theme indices (prose quality, pacing, editing, reader expectations).

See **`results/reports/02_findings/hypothesis_testing/`** for detailed statistical results when present.

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
| Stage methodology | `results/reports/01_stage_reports/` |
| Hypothesis testing results | `results/reports/02_findings/hypothesis_testing/` |
| LLM labeling methodology | `results/reports/02_findings/methodology_llm_labeling_and_taxonomy/` |
| Implementation details | [`src/`](src/) stage READMEs |
