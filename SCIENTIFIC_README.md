# Scientific Methodology: Romance Novels — Themes × Reader Appreciation

**A Mixed-Methods Computational Analysis**

This document provides an overview of the research methodology and findings. For implementation details, see the [`reports/`](reports/) directory and stage-specific documentation in [`src/`](src/).

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
| H1 | **Love-over-Sex**: Higher-rated novels emphasize emotional connection over explicit content | `(commitment + tenderness) − explicit` |
| H2 | **HEA Index**: Stronger "Happily Ever After" signals predict appreciation | `commitment + symbolic_gifts + rituals` |
| H3 | **Luxury × Love**: Wealth appeals only when paired with emotional depth | `luxury × (commitment + tenderness)` |
| H4 | **Protectiveness vs Possessiveness**: Caring protection valued over jealousy | `protectiveness − jealousy` |
| H5 | **Darkness vs Tenderness**: Top-rated novels favor tenderness over dark themes | `(negative_affect + threat) − tenderness` |
| H6 | **Narrative Arc**: Successful romances progress from conflict to resolution | `begin→end: miscomm↓, repair↑`

---

## Dataset

### Corpus (primary): `romance_subdataset_downloaded_v2_full`

The main text corpus lives under **`data/raw/romance_subdataset_downloaded_v2_full/`** (EPUBs plus mirrored subsampling tables). It is the **downloaded subsample v2** cohort: works from the ~20k romance design frame that have a resolvable MD5 and at least one **EPUB** on disk (see **`SUBSAMPLING_V2.md`** and **`subsampling_metadata/romance_subdataset_downloaded_v2_manifest.json`** in that folder).

- **17,514** works (rows in `subsampling_metadata/romance_subdataset_downloaded_v2_full.csv`; matches manifest `cohort_n`)
- **8,828** distinct authors (`author_id` in metadata)
- **Publication years** in this export: 2000–2017 (time-based split; missing years sorted first in train)
- **Genre mix** (metadata `genre_group`): e.g. other, paranormal, mystery, historical, young_adult — not a billionaire-only convenience sample
- **Train / val / test** (time strategy, seed 42): 12,259 / 2,627 / 2,628 EPUBs (`n_train_v2`, `n_val_v2`, `n_test_v2` in manifest)
- After ingestion (Stage 01–02), text is organized **Author → Book → Chapter → Sentence**; sentence totals are produced by the pipeline from ingested EPUBs (not fixed to the older pilot corpus)

### Goodreads-linked metadata (per work, v2 full table)

Each cohort row includes aggregated Goodreads-style fields from the design frame (e.g. `average_rating_weighted_mean`, `ratings_count_sum`). Corpus-wide summaries on the **17,514** works:

- **Mean rating** (unweighted mean of per-work `average_rating_weighted_mean`): **3.91**
- **Range** of per-work mean rating: **1.27–5.00**
- **`ratings_count_sum`**: median **254**, mean **~3.0k** (long-tailed; unlike the old pilot, not all works have very large vote counts)

## Methodology Overview

### 1. Topic Modeling: BERTopic + OCTIS

**Why BERTopic?** Unlike traditional LDA, BERTopic uses BERT embeddings to capture contextual word meanings, producing more interpretable topics for literary analysis.

**Optimization**: Bayesian hyperparameter optimization via OCTIS framework across:
- 6 embedding models (SentenceTransformers)
- UMAP, HDBSCAN, and vectorizer parameters
- 300+ configurations evaluated

**Model Selection**: Pareto efficiency analysis balancing coherence (topic interpretability) and diversity (topic variety). Final model: N topics.

**Character Name Exclusion**: N character names added to stopwords to ensure topics reflect thematic content rather than character co-occurrence.

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

**Romance Corpus Taxonomy** (8 groups, 30+ categories):
1. Embodied & Sensory Experience
2. Sexuality, Attraction & Intimacy
3. Emotions, Cognition & Inner Life
4. Relationship Trajectory (Main Couple)
5. Social World Outside Couple
6. Work, Wealth, Status & Institutions
7. Conflict, Risk & Harm
8. Spaces, Time, Activities & Objects

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

| Stage | Description |
|-------|-------------|
| 01 Ingestion | Load novels and Goodreads metadata |
| 02 Preprocessing | Text cleaning, sentence segmentation, character name removal |
| 03 Modeling | BERTopic training with OCTIS optimization |
| 04 Selection | Pareto-efficient model selection |
| 05 Retraining | Retrain selected models |
| 06 Topic Exploration | Multi-representation analysis |
| 07 Topic Quality | Noisy topic detection |
| 08 LLM Labeling | Automated topic labeling |
| 09 Category Mapping | Theory-aligned classification |
| 10 Correlation Analysis | Statistical hypothesis testing |

See [`reports/01_stage_reports/`](reports/01_stage_reports/) for detailed methodology per stage.

---


## Key Findings

### Mass Appeal (Popularity)

Books with higher rating counts emphasize:
- **Status/dominance themes** (wealth, power, alpha behavior)
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

See [`reports/02_findings/hypothesis_testing/`](reports/02_findings/hypothesis_testing/) for detailed statistical results.

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
| Stage methodology | [`reports/01_stage_reports/`](reports/01_stage_reports/) |
| Hypothesis testing results | [`reports/02_findings/hypothesis_testing/`](reports/02_findings/hypothesis_testing/) |
| LLM labeling methodology | [`reports/02_findings/methodology_llm_labeling_and_taxonomy/`](reports/02_findings/methodology_llm_labeling_and_taxonomy/) |
| Implementation details | [`src/`](src/) stage READMEs |
