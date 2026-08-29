# Stage 05: v4 L12 call 73 — full-corpus final fit and inference

**Date:** 2026-07-01  
**Run ID:** `v4_l12_granular_final_call73`  
**BO call:** 73 (`sentence-transformers/all-MiniLM-L12-v2`)  
**Corpus:** v3 English-only (`data/raw/romance_subdataset_filtered_v3/`)  
**Pipeline:** compare-fit → holdout → full-corpus infer (orchestrated)  
**Status:** Complete (Steps A–C). Step D (Stage10 aggregation) pending.

**Related memos:** [`call73/placeholder_v4_call73_analysis_strategy.md`](../call73/placeholder_v4_call73_analysis_strategy.md), [`v4_granular_stage05_probabilities.md`](v4_granular_stage05_probabilities.md)

---

## 1. Executive summary

Stage 05 turns the frozen BO winner (call 73) into a **production topic model** and assigns topics (+ soft probabilities) to **114.9M sentences** across train, val, and test splits.

| Step | What | Result | Wall time |
|------|------|--------|-----------|
| **A** compare-fit | Refit + stability + save model | 329 topics, c_v 0.657, stability pass | ~51 min |
| **B** holdout | Test-split transform (confirmatory) | 17.5M docs, 0.9% hard outliers, avg max prob 0.55 | ~3 min |
| **C** infer | Full-corpus parquet (train+val+test) | 114.9M docs, ~0.9% outliers per split | ~2 h 11 min |

**Headline:** Call 73 is now **materialized at sentence level** with `calculate_probabilities: true`. This unblocks Stage 09 taxonomy mixtures and Stage 10 book-level correlation work. Fit-sample outlier rate remains ~70% (HDBSCAN structural); inference outlier rate is ~0.9% (cosine-similarity `transform()`).

---

## 2. Role of Stage 05 in the project

```text
Stage03 BO tuning  →  Stage04 selection  →  Stage05 final fit  →  Stage06–09 / Stage10
     (130 calls)         (call 73 winner)      (deploy model)         (analysis)
```

| Stage | Depends on Stage 05 for… |
|-------|---------------------------|
| **Stage 06–07** | Frozen compare-fit model and topic inventory |
| **Stage 08** | Representative sentences per topic (from enriched model) |
| **Stage 09** | Sentence-level soft topic mixtures for theory-driven category mapping |
| **Stage 10** | Book-level and tertile topic probabilities derived from sentence parquets |

Stage 05 is the **deployment boundary**: everything before it operates on BO samples and metrics; everything after it consumes sentence- or book-level topic assignments.

### Call 73 policy (unchanged)

Per the frozen strategy memo:

- **No `--reduce-outliers`** — aggressive reassignment collapses ~330 topics to a handful of mega-topics.
- **`calculate_probabilities: true`** at final fit — enables soft assignments for mixtures.
- **Accept ~70% fit-sample outliers** — HDBSCAN at sentence level; treat `-1` as background at fit time, not a metric to minimize.
- **Primary inference:** train + val + test; **confirmatory holdout:** test-only metrics in Step B.

---

## 3. Experimental setup

### 3.1 Configuration

| Item | Value |
|------|-------|
| Train config | `configs/stage03/train_v4_l12_final_call73.yaml` |
| Paths | `configs/stage03/paths_stage03_fit_v3.yaml` |
| Trials CSV | `results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv` |
| Embedding model | `sentence-transformers/all-MiniLM-L12-v2` |
| Fit sample | 500k stratified train indices (`data/stage03_samples_v3/`, seed 42) |
| `calculate_probabilities` | `true` |
| Transform batch size | 16,384 |
| CSV chunk size | 50,000 |
| Holdout coherence cap | 100,000 docs |

### 3.2 Embedding caches (GPU speed path)

| Split | Cache file |
|-------|------------|
| train + val | `data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__all-MiniLM-L12-v2.npy` |
| test | `data/interim/octis/v3_english_only/embeddings_cache/test_sentence-transformers__all-MiniLM-L12-v2.npy` (~25 GB) |

Precomputed embeddings removed on-the-fly encode from the holdout and infer hot path.

### 3.3 Orchestrator

```bash
nohup ./scripts/stage03/run_v4_call73_full_corpus.sh >> logs/v4_call73_full_corpus_console.log 2>&1 &
```

Steps skip when output markers exist (compare metrics, test metrics, infer summary). Resume is supported for embedding encode (Step 0) and infer chunk shards (Step C).

---

## 4. Results

### 4.1 Step A — compare-fit refit

**Artifacts:** `results/experiments/v4_l12_granular_final_call73/final_compare/call_73/`

| Metric | Value |
|--------|-------|
| Topics | **329** |
| Coherence (c_v) | **0.657** |
| Topic diversity | **0.669** |
| Fit-sample outlier rate | **70.5%** |
| Fit docs | 432,145 (500k cap, after empty-sentence drop) |
| Stability (3 runs) | 318 / 330 / 335 topics, σ = 7.1 — **pass** |
| Elapsed | ~51 min |

**Hyperparameters (call 73):**

| Parameter | Value |
|-----------|-------|
| `umap__n_neighbors` | 5 |
| `umap__n_components` | 7 |
| `umap__min_dist` | 0.0036 |
| `hdbscan__min_cluster_size` | 106 |
| `hdbscan__min_samples` | 28 |
| `hdbscan__cluster_selection_method` | eom |
| `vectorizer__min_df` | 16 |
| `bertopic__top_n_words` | 32 |

Model saved under `final_compare/call_73/model_compare/`.

### 4.2 Step B — test holdout

**Artifacts:** `results/evaluation/v4_l12_granular_final_call73/call_73/test_metrics.json`

| Metric | Value |
|--------|-------|
| Test sentences scored | 17,475,960 |
| Hard outlier rate (transform) | **0.91%** |
| Avg max topic probability | **0.550** |
| Coherence / diversity / n_topics in JSON | 0 (see §6) |

Holdout validates that the frozen model **generalizes to unseen books** and produces usable assignments at scale when using cached test embeddings and batch transform.

### 4.3 Step C — full-corpus inference

**Artifacts:** `results/experiments/v4_l12_granular_final_call73/full_corpus_infer/`

| Split | Sentences | Outlier rate | Parquet size | Transform time |
|-------|-----------|--------------|--------------|----------------|
| train | 80,230,272 | 0.89% | ~148 GB | ~94 min |
| val | 17,198,034 | 0.87% | ~32 GB | ~18 min |
| test | 17,475,960 | 0.91% | ~32 GB | ~18 min |
| **Total** | **114,904,266** | ~0.9% | **~211 GB** | **~2 h 11 min** |

Summary: `infer_summary.json` (`finished_at`: 2026-07-01T23:49:25Z)

**Parquet schema (per sentence):**

- Metadata: `work_id`, `chapter_index`, `sentence_index`, `sentence`, `split`
- Hard assignment: `topic` (integer; `-1` = outlier)
- Soft assignment: `max_topic_prob`, `prob_0` … `prob_{K-1}` (329 topics)

---

## 5. Interpreting the two outlier rates

| Phase | Outlier rate | Mechanism |
|-------|--------------|-----------|
| **Compare-fit** (500k sample) | ~70% | HDBSCAN cluster membership during fit — most sentences are not cluster cores |
| **Full-corpus infer** (115M) | ~0.9% | BERTopic `transform()` via cosine similarity — nearly all sentences receive a topic label + soft probs |

These numbers are **not contradictory**. The project treats fit-time outliers as structural background and relies on soft inference for downstream mixtures (see call 73 strategy §2).

---

## 6. Operational notes

### 6.1 Run history

1. **First infer attempt** (single streaming ParquetWriter): stalled at ~53% train; later killed. Partial file lacked a valid Parquet footer after disk-full event — **not recoverable**.
2. **Restart** with resumable chunk-shard writer (`sentence_topics_{split}.partial/`, `.progress.json`): completed successfully.
3. **Duplicate orchestrator launch** (19:01): killed to avoid concurrent writes to the same output directory.

### 6.2 Disk

Full infer outputs require **~220 GB**. Peak usage reached **~96%** of the 1.8 TB data partition during the run; **~103 GB** free after completion.

### 6.3 Monitoring

Infer logs contain tqdm ANSI codes — use `grep -a` or read `.progress.json`:

```bash
cat results/experiments/v4_l12_granular_final_call73/full_corpus_infer/sentence_topics_train.parquet.progress.json
grep -a "train csv chunks" logs/stage05_infer_corpus_v4_l12_granular_final_call73.log | tail -1
```

### 6.4 Known issue — holdout metric fields

`test_metrics.json` reports `coherence_c_v: 0`, `topic_diversity: 0`, `n_topics: 0`. Transform and outlier/probability metrics are valid; topic-count and coherence fields need a follow-up fix in the streaming holdout path. **Use compare-fit metrics (§4.1) for coherence/diversity/topic count.**

---

## 7. Downstream next steps (Step D)

Book-level aggregation (manual / next run):

```bash
# Book-level topic probabilities
python src/stage10_correlation_analysis/data_preparation/03_generate_topic_probabilities_final.py

# Tertile topic probabilities
python src/stage10_correlation_analysis/data_preparation/04_generate_tertile_topic_probs_patched_v3.py
```

Inputs: `full_corpus_infer/sentence_topics_{train,val,test}.parquet`  
Strategy memo: [`call73/placeholder_v4_call73_analysis_strategy.md`](../call73/placeholder_v4_call73_analysis_strategy.md)

Stage 09 taxonomy mapping can proceed in parallel using Stage 08 labels + these sentence-level mixtures.

---

## 8. Artifact index

| Artifact | Path |
|----------|------|
| Compare-fit metrics | `results/experiments/v4_l12_granular_final_call73/final_compare/call_73/metrics.json` |
| Saved model | `results/experiments/v4_l12_granular_final_call73/final_compare/call_73/model_compare/` |
| Holdout metrics | `results/evaluation/v4_l12_granular_final_call73/call_73/test_metrics.json` |
| Sentence parquets | `results/experiments/v4_l12_granular_final_call73/full_corpus_infer/sentence_topics_*.parquet` |
| Infer summary | `results/experiments/v4_l12_granular_final_call73/full_corpus_infer/infer_summary.json` |
| Orchestrator log | `logs/v4_call73_full_corpus_console.log` |
| Infer log | `logs/stage05_infer_corpus_v4_l12_granular_final_call73.log` |
| Config | `configs/stage03/train_v4_l12_final_call73.yaml` |
| Run script | `scripts/stage03/run_v4_call73_full_corpus.sh` |

---

## 9. Conclusion

Stage 05 for call 73 is **complete**. The project now has:

1. A **stability-validated** 329-topic BERTopic model with soft probabilities enabled.
2. **Confirmatory holdout** evidence that transform works on 17.5M unseen sentences (~0.9% hard outliers).
3. A **115M-row sentence-level topic dataset** (~211 GB) spanning the full v3 English corpus.

This is the primary quantitative substrate for romance scene inventory analysis, taxonomy validation (Stage 09), and correlational work (Stage 10).
