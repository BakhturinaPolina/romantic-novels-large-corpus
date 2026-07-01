# Stage 03 BERTopic Search Space: A Pretest-Informed Prior

**Component:** `src/stage03_train/tune.py` (`build_search_space`)
**Configuration:** `configs/legacy/train.yaml` (`search_space`)
**Status:** Draft for the methods section of the topic-modeling paper.

This note justifies the Bayesian-optimization search space used for Stage 03 BERTopic tuning on the large romance corpus. The ranges are derived from a smaller pretest, then **shifted and widened** for the larger, more heterogeneous corpus. The previous best configuration is used as a **prior**, not as a fixed answer.

---

## 1. Pretest evidence (smaller billionaire-romance corpus)

The embedding-model shortlist and the parameter prior come from a Pareto analysis on a smaller corpus of **100 "billionaire" romance novels** (an earlier, separate project). That pretest is referenced across this repo (`SCIENTIFIC_README.md`, `src/stage03_train/PIPELINE_OVERVIEW.md`, `src/stage03_train/CODE_PLAN.md`); its raw trial logs are **not** vendored into this repository, so the values below are reproduced from the pretest report.

### 1.1 Selected configuration

The selected model was **`paraphrase-mpnet-base-v2`, iteration 0**, with C_V coherence = **0.463**, topic diversity = **0.82**, and the best equal-weight combined score.

| Parameter | Pretest best |
|-----------|--------------|
| embedding model | `paraphrase-mpnet-base-v2` |
| `bertopic__min_topic_size` | 127 |
| `bertopic__top_n_words` | 31 |
| `hdbscan__min_cluster_size` | 494 |
| `hdbscan__min_samples` | 28 |
| `umap__min_dist` | 0.058 |
| `umap__n_components` | 10 |
| `umap__n_neighbors` | 11 |
| `vectorizer__min_df` | 0.007 |

### 1.2 Importance and trade-offs

The pretest reported the most influential parameters as `umap__min_dist`, `vectorizer__min_df`, `hdbscan__min_cluster_size`, `bertopic__min_topic_size`, and `umap__n_components`, with a clear coherence/diversity trade-off:

- Larger `min_topic_size` improved coherence but reduced diversity.
- Larger `umap__min_dist` improved diversity but reduced coherence.

The three embedding models kept for Stage 03 (`all-MiniLM-L12-v2`, `paraphrase-mpnet-base-v2`, `paraphrase-MiniLM-L6-v2`) are the Pareto-efficient shortlist from this pretest; low-coherence candidates were excluded.

---

## 2. Why not freeze the pretest values

The pretest optimum is a strong starting point but should not be frozen, because the large corpus differs in **scale** and **heterogeneity**:

- Several parameters are **absolute counts**, not fractions. `min_topic_size = 127` and `hdbscan__min_cluster_size = 494` mean something different on a 500,000-row fit corpus than on a small pilot. In HDBSCAN, larger `min_cluster_size` merges small clusters into fewer, more stable ones; `min_samples` controls conservativeness. In BERTopic, `min_topic_size` sets the minimum topic size and typically must grow with corpus size.
- The pretest best for `umap__n_components` (10) and `hdbscan__min_cluster_size` (494) sat **at or near the old upper bounds** (10 and 500), suggesting the optimizer wanted to go higher but could not.

So the corpus optimum may shift, especially for the scale-sensitive clustering parameters.

---

## 3. Revised search space

The space keeps the pretest optimum inside each range but expands upward for scale-sensitive parameters. This is implemented in `configs/legacy/train.yaml`; `build_search_space` maps count parameters to skopt `Integer` and continuous parameters to `Real` with no logic change.

| Parameter | Old range | New range | Pretest anchor | Reason |
|-----------|-----------|-----------|----------------|--------|
| `umap__n_neighbors` | 2-50 | **10-75** | 11 | Very small values over-fragment a huge heterogeneous corpus; larger values preserve more global structure. |
| `umap__n_components` | 2-10 | **5-15** | 10 (at old max) | Old best hit the ceiling; allow more embedding dimensions. |
| `umap__min_dist` | 0.0-0.1 | **0.02-0.15** | 0.058 | Keep the old center; allow more spread for thematic diversity. |
| `hdbscan__min_cluster_size` | 50-500 | **300-3000** | 494 (near old max) | 500 likely too low for 500k fit docs; allow larger, more stable clusters. |
| `hdbscan__min_samples` | 10-100 | **10-150** | 28 | Do not force high; keep broad but allow more conservative clustering. |
| `vectorizer__min_df` | 0.001-0.01 | **0.002-0.015** | 0.007 | Keep the old center; widen modestly (see Section 4). |
| `bertopic__top_n_words` | 10-40 | **20-50** | 31 | Low importance and scale-insensitive; literary topics benefit from more words for interpretation. |
| `bertopic__min_topic_size` | 10-250 | **100-1500** | 127 | 250 too restrictive for a large fit sample; allow larger minimum topics. |

### 3.1 Most consequential changes

```yaml
hdbscan__min_cluster_size: [300, 3000]
bertopic__min_topic_size:  [100, 1500]
umap__n_components:        [5, 15]
umap__n_neighbors:         [10, 75]
```

Both `hdbscan__min_cluster_size` and `bertopic__min_topic_size` are likely under-scaled for a 500,000-row fit corpus; the pretest already hinted at this (best `min_cluster_size = 494` was almost at the old maximum of 500).

---

## 4. Note on `vectorizer__min_df`

`vectorizer__min_df` is a fraction of fit documents. On 500,000 fit rows:

- `0.002` -> a term must appear in ~1,000 documents.
- `0.015` -> a term must appear in ~7,500 documents.

The chosen range **[0.002, 0.015]** keeps the pretest center (0.007 ~ 3,500 docs) while admitting somewhat rarer terms at the low end. This is a deliberate compromise: it preserves robust high-level themes while reducing the risk of erasing rarer motifs, settings, professions, or subgenre markers. If rare-motif detection later becomes a priority, a lower fractional range (e.g. `[0.0002, 0.005]`) or integer document counts could be substituted; if only robust large-scale structure is needed, the current range is conservative and defensible.

---

## 5. Fit/eval protocol context

These ranges are searched while fitting on the **stratified 500k train sample** (train partition only) and scoring coherence/diversity on a **stratified 100k val sample**; see [`stage03_stratified_fit_sample_design.md`](stage03_stratified_fit_sample_design.md). During tuning, `bertopic.calculate_probabilities = false` (full document-by-topic probability matrices are unnecessary for OCTIS coherence/diversity selection and expensive at this scale); the outlier rate is computed from hard topic labels (`-1`). Probability matrices, if ever needed, are a Stage 05 concern.

The optimizer runs 120 BO calls per model (`configs/legacy/train.yaml -> optimization.number_of_calls`).

---

## 6. Bottom line

Use the pretest configuration as a **prior**, not a final answer. It is most reliable for `umap__min_dist`, `top_n_words`, and the embedding-model shortlist. For the large corpus, expand the ranges for `hdbscan__min_cluster_size`, `bertopic__min_topic_size`, `umap__n_components`, and `umap__n_neighbors`, because corpus scale and heterogeneity may move the optimum substantially -- especially for the clustering-size parameters. Bayesian optimization still explores the full revised space.
