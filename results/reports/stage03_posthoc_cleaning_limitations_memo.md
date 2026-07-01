# Stage03 / Post-hoc Topic Cleaning — Current Limitations

**Status:** Active limitations memo (rules not yet in production pipeline).  
**Reference run:** `stratified_minilm12v2_seed42_v2/final_compare/call_59` (294 topics, 70.9% outlier rate, 432k fit docs).  
**Date:** 2026-06-24

## Scope

“Stage03” in this filename refers to the BO/fit corpus path and shared preprocessing. Limitations span **pre-fit** ([`src/stage03_train/data_io.py`](../../src/stage03_train/data_io.py)) and **post-fit** (Stages 05–07). call_59 is the canonical toy dataset for rule tests.

**Related artifacts**

| Artifact | Path |
|----------|------|
| Toy topic tables | `results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/` |
| Preprocessing gap analysis | [`stage05_preprocessing_analysis.md`](stage05_preprocessing_analysis.md) |
| call_59 taxonomy review | [`stage08_stage09_taxonomy_improvement_notes_call59.md`](stage08_stage09_taxonomy_improvement_notes_call59.md) |
| Debugging plan | [`stage05_debugging_plan.md`](stage05_debugging_plan.md) |
| Post-hoc rule config | [`configs/call73/topic_posthoc_rules.yaml`](../../configs/call73/topic_posthoc_rules.yaml) |
| Rule implementation | [`src/common/topic_posthoc/rules.py`](../../src/common/topic_posthoc/rules.py) |

---

## Implemented (not limitations)

| Rule | Where | Notes |
|------|-------|-------|
| Absolute `min_df` override | Stage05 `compare_fit.py` | Converts proportional BO values to absolute doc count |
| `token_pattern` (2+ alpha) | Stage05, Stage03 wrapper | Reduces single-char and numeric garbage |
| Short-doc filter (`MIN_WORDS_FIT=4`) | Stage05 | Drops degenerate sentences before fit |
| Custom stoplist merge | Stage03/05 | English + `custom_stoplist.txt` |
| Optional `reduce_outliers` | Stage05 CLI `--reduce-outliers` | Reassigns `-1` docs via embeddings; separate export dir |
| Stage07 size / POS / coherence flags | `topic_quality_analysis.py` | Non-destructive `noise_candidate` for small/low-POS topics |
| **P0 post-hoc rule classifier** | `src/common/topic_posthoc/` | Rule-based flags on `topic_info.csv` (metadata only) |

---

## Deferred rules (current limitations)

| Rule category | Status | Evidence in call_59 |
|---------------|--------|---------------------|
| Character-name stoplist preprocessing (`preprocess_character_name`) | **Not ported** | Residual name-like tokens in topics |
| Mojibake fix + Unicode NFKD in `clean_sentence` | **Not ported** | Legacy in [`retrain_models.py`](../../src/legacy/stage05_retraining/retrain_models.py) |
| Residual non-English sentence filter (post-v3) | **Not at fit time** | Topic 0: `sa du ha ne yo…` (10,066 docs) |
| Default `reduce_outliers` on compare-fit | **Optional only** | 70.9% outliers in default `metrics.json` |
| `merge_topics` / `reduce_topics` | **Not in pipeline** | Stage09 README example only |
| Topic word padding (equal-length export) | **Not ported** | Minor export inconsistency vs legacy |
| Stage05b masked holdout metrics | **Future** | Holdout reports raw transform only |
| Shared `normalize_text()` (mojibake + NFKD) | **Follow-up P1** | Duplicated gap vs legacy retrain path |

Post-hoc **flagging** for publisher boilerplate, dialogue adverbs, speech acts, multilingual artifacts, and tiny topics is implemented in `topic_posthoc` but does **not** mutate the BERTopic model or refit assignments.

---

## call_59 anchor topics

| Topic | Count | Pattern | Expected post-hoc class |
|-------|------:|---------|-------------------------|
| 0 | 10,066 | 2-letter / non-English tokens | `multilingual_artifact` |
| 1 | 6,451 | Explicit intimacy scene | `keep` |
| 8 | 1,773 | Dialogue-delivery adverbs | `dialogue_delivery` |
| 21 | 889 | Publisher / copyright blocks | `publisher_boilerplate` |
| 37 | 621 | Werewolves / paranormal | `subgenre_marker` |

Outlier topic **−1** (306,547 docs) is excluded from post-hoc classification. Outlier **reduction** (`reduce_outliers`) is orthogonal to topic-noise rules.

126 of 294 non-outlier topics have **Count &lt; 200** (~43% by count tier).

---

## Recommended priority (later work)

### P0 — Rule-based flagging (implemented)

Multilingual artifact, publisher boilerplate, dialogue-delivery adverbs, speech-act fillers, tiny-topic threshold → `flag_noise` metadata for Stage07/08/09.

Run on existing CSV (no GPU):

```bash
./scripts/legacy/run_topic_posthoc_call59.sh
```

### P1 — Pre-fit normalization (follow-up PR)

Port `preprocess_character_name()` and mojibake/NFKD into shared `normalize_text()` used by Stage03 `clean_sentence` and stoplist loader. Requires corpus rebuild / refit to take effect.

### P2 — Destructive cleaning (winner-only)

`merge_topics` / `reduce_topics` after Stage04 winner selection; re-run Stage05b on cleaned model. Not applied during BO compare-fit (preserves trial comparability).

---

## Pipeline placement

| Stage | Post-hoc role |
|-------|---------------|
| **Stage05 compare-fit** | Export `posthoc_flags.csv` + `posthoc_summary.json` after `topic_info.csv` |
| **Stage05b holdout** | Raw metrics only; no model mutation |
| **Stage06 exploration** | Representation refresh before Stage07 when POS aspects missing |
| **Stage07 quality** | Primary consumer: merge rule flags into `noise_candidate` / `[NOISE:rule_id]` labels |

**Winner path order:** Stage05 compare → Stage04 select → Stage05 final-fit → Stage06 repr refresh → **Stage07 post-hoc** → Stage05b holdout → Stage08/09.

---

## Cross-links

- v4 granular BO outlier metrics: [`granular_bertopic_bo_v4_482079a4.plan.md`](../../.cursor/plans/granular_bertopic_bo_v4_482079a4.plan.md)
- Stage09 noise label convention: `[NOISE_CANDIDATE:` / `[NOISE:` prefixes in `explore_hierarchical_topics.py`
