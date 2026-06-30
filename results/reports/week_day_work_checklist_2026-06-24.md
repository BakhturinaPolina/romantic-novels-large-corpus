# Week day-work checklist (placeholder pipeline)

**Week of:** 2026-06-24  
**Context:** v4 L12 Phase 1 BO runs at night; **frozen downstream analysis uses call 73 only** ([strategy memo](placeholder_v4_call73_analysis_strategy.md), [`configs/placeholder_v4_frozen_call73.yaml`](../../configs/placeholder_v4_frozen_call73.yaml)). Call 55 and other top-5 trials remain BO reference only.  
**Night track:** `v4_l12_granular_phase1` BO (**done** 160/160) → Phase 2 stability → Phase 3 narrowed BO.

---

## This week — day work

| # | Task | Status | Link / artifact |
|---|------|--------|-----------------|
| 1 | [Stage05] Save placeholder models (top-5) | **Done** | [`placeholder_v4_models/final_compare/`](../experiments/placeholder_v4_models/final_compare/) — calls **55, 73, 49, 19, 68** with `--save-model`; refit topic counts match BO |
| 2 | [Stage07] Post-hoc + topic quality | **Done** (call 73 frozen) | [`placeholder_v4_call73/`](../stage07_topic_quality/placeholder_v4_call73/) — **151 usable** / 179 excluded; script default `CALLS=73` |
| 3 | [Stage04] Dry-run v4 granular selection | **To do** ← **next** | Run: `.venv/bin/python -m src.stage04_eval_select.cli select --trials results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv --config configs/eval_select_granular.yaml --run-id v4_l12_granular_phase1_dryrun` → `results/selection/v4_l12_granular_phase1_dryrun/` |
| 4 | [Stage04] Selection notebooks (v3 L12 vs L6) | To do | [`notebooks/04_selection/`](../../notebooks/04_selection/) + [`configs/selection_notebooks.yaml`](../../configs/selection_notebooks.yaml) |
| 5 | [Stage05] Compare-fit top v4 trials (granularity inspect) | **Done** | Same as #1 — top-5 by `bo_objective` on partial Phase 1 CSV |
| 6 | [Stage05b] Holdout smoke test on placeholder | To do | **call_73** recommended: `placeholder_v4_models/final_compare/call_73/model_compare` (~3–8 h full test; overnight). Stage06 unblocks labeling only, not holdout |
| 7 | [Stage06] Representation refresh → topics JSON | **Done** (55, 73) | Script [`run_stage06_placeholder_v4_call.sh`](../../scripts/run_stage06_placeholder_v4_call.sh); **stopwords fix** in [`explore_retrained_model.py`](../../src/stage06_topic_exploration/explore_retrained_model.py) (`update_topics` keeps fitted vectorizer). Enriched: `call_{55,73}/model_compare_enriched/`; JSON: [`stage06_topic_exploration/placeholder_v4_call{55,73}/`](../stage06_topic_exploration/). Calls 49/19/68 still on compare-fit only |
| 8 | [Stage08] LLM labels — pilot ~20 topics → full | **Done** (c8 production) | **322** topics @ `v2_c8_character_names`; axis policy applied (**295** Stage09-included / **27** excluded); production file: [`labels_..._v2_c8_character_names.json`](../stage08_llm_labeling/placeholder_v4_call73/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v2_c8_character_names.json) |
| 9 | [Stage09] Taxonomy / category mapping dry-run | **To do** ← **next (CPU)** | [`src/stage09_category_mapping/`](../../src/stage09_category_mapping/) — c8 labels ready |
| — | [Meta] Night GPU: v4 L12 **Phase 1** BO | **Done** | 160/160 calls; finished 2026-06-26 03:01 UTC; [`trials.csv`](../experiments/v4_l12_granular_phase1/trials.csv); log: `logs/stage03_v4_l12_granular_phase1.log`; best **call 55** (`bo_objective=0.694`, 117 topics) |
| — | [Meta] Night GPU: v4 L12 **Phase 2** stability | **Doing** | Started 2026-06-29; 14 candidates × 3 runs; log: `logs/stage05_compare_v4_l12_granular_phase2_stability.log`; ETA **~18–22 h** |
| — | [Meta] Night GPU: v4 L12 **Phase 3** narrowed BO | To do | After Phase 2 review; `configs/train_v4_l12_granular_phase3.yaml` (100 calls, `model_runs=3`) |

---

## Week 2 — hardening

| Task | Status | Notes |
|------|--------|-------|
| [Config] `configs/placeholder_pipeline.yaml` | To do | Single swap file: run_id, trials path, model dirs, winner path |
| [Scripts] `scripts/run_downstream_placeholder.sh` | To do | Chain Stage04→05→05b→06→07→08 smoke |
| [Post-hoc] `dialogue_delivery` + `speech_act_filler` rules | To do | [`src/common/topic_posthoc/rules.py`](../../src/common/topic_posthoc/rules.py); anchors in [`stage03_posthoc_cleaning_limitations_memo.md`](stage03_posthoc_cleaning_limitations_memo.md) |
| [Stage08] Filter `[NOISE:rule_id]` before LLM spend | To do | Use Stage07 `posthoc_reason` columns |
| [Stage03/05] P1 pre-fit: mojibake/NFKD + character-name preprocessing | To do | [`src/stage03_train/data_io.py`](../../src/stage03_train/data_io.py) |
| [Stage05] `final_fit` dry-run with v3 `winner_config.json` | To do | [`results/selection/v3_minilm12v2_first/winner_config.json`](../selection/v3_minilm12v2_first/winner_config.json) |

---

## Completed this session (not in original Notion list)

| Item | Status | Link |
|------|--------|------|
| Fix compare-fit `vectorizer__min_df` int coercion (v4 BO) | **Done** | Commit `7e84dcd`; [`src/stage05_final_fit/compare_fit.py`](../../src/stage05_final_fit/compare_fit.py) |
| Stage07 batch script for placeholder v4 (top-5) | **Done** | [`scripts/run_stage07_placeholder_v4_models.sh`](../../scripts/run_stage07_placeholder_v4_models.sh) |
| Compare-fit calls 49 + 19 (complete top-5 sweep) | **Done** | [`placeholder_v4_models/final_compare/`](../experiments/placeholder_v4_models/final_compare/) |
| Stage06 placeholder script + list-aspect extraction fix | **Done** | [`scripts/run_stage06_placeholder_v4_call.sh`](../../scripts/run_stage06_placeholder_v4_call.sh); [`explore_retrained_model.py`](../../src/stage06_topic_exploration/explore_retrained_model.py) |
| Stage06 `update_topics` stopwords regression fix | **Done** | [`explore_retrained_model.py`](../../src/stage06_topic_exploration/explore_retrained_model.py) — pass fitted `vectorizer_model` / `ctfidf_model` / `representation_model`; bare `update_topics(docs)` had reset to default CountVectorizer (pronouns/names leaked into Main) |
| Stage06 + Stage07 refresh on call_55 (post-fix) | **Done** | Stage06 ~298 s; Main c_v 0.435; **1** `noise_candidate` (T10 publisher); logs: `logs/stage06_placeholder_v4_call55.log` |
| Stage06 + Stage07 refresh on call_73 (post-fix + character rule) | **Done** | 151 usable, 44 character_name, 159 tiny; logs: `logs/stage06_placeholder_v4_call73_rerun.log` |
| Frozen call 73 strategy memo | **Done** | [`placeholder_v4_call73_analysis_strategy.md`](placeholder_v4_call73_analysis_strategy.md) |
| v4 L12 Phase 1 BO (160/160) | **Done** | [`v4_l12_granular_phase1/`](../experiments/v4_l12_granular_phase1/); top-5 unchanged: calls **55, 73, 49, 19, 68** |
| Stage08 full c8 + axis policy (call 73) | **Done** | 322 labels; 20 `Character Name Artifact`; 4 manual overrides (T57,79,95,111); limit20 spot-check: [`placeholder_v4_call73_c8_rerun/`](../stage08_llm_labeling/placeholder_v4_call73_c8_rerun/) |
| Phase 2 script fix (v3 paths + PYTHONPATH) | **Done** | [`scripts/run_v4_granular_phase2.sh`](../../scripts/run_v4_granular_phase2.sh) |

---

## Phase 2 time estimate (L12 stability)

Script: `./scripts/run_v4_granular_phase2.sh l12` — band-filter **14 candidates**, Stage05 compare-fit with **`--stability-runs 3`**, **`--reduce-outliers`** (no `--save-model`).

| Component | Estimate |
|-----------|----------|
| Candidate selection | ~1 min (CPU) |
| One-time setup (mmap embeddings + 432k fit docs) | ~10 min |
| Per candidate | **3 full BERTopic fits** (UMAP seed sweep) + metrics/tables + `reduce_outliers` export |
| Per-candidate fit time | **~15 min** (call 55, 117 topics) – **~28 min** (300–400 topics) – **~37 min** (call 10, 505 topics) — from placeholder compare-fit logs |
| **Total GPU wall time** | **~18–22 h** (14 × ~75–90 min avg); allow **up to ~24 h** if GPU is busy or high–topic-count configs dominate |

Reference: placeholder single compare-fits on this machine — call_55 **934 s**, call_73 **1320 s**, call_49 **1539 s** (`logs/stage05_compare_placeholder_v4_models.log`). Phase 2 triples the fit work per candidate before outlier reduction.

---

## Stage07 snapshot (placeholder v4)

| Call | Topics | `noise_candidates` | `exclude_from_axes` | Stage06 enriched? | Quality CSV |
|------|--------|-------------------|---------------------|-------------------|-------------|
| 55 | 117 | **1** | 1 | Yes (post-fix) | [`topic_quality_placeholder_v4_call55.csv`](../stage07_topic_quality/placeholder_v4_call55/topic_quality_placeholder_v4_call55.csv) |
| 73 | 330 | — | **179** (151 usable) | Yes (frozen) | [`topic_quality_placeholder_v4_call73.csv`](../stage07_topic_quality/placeholder_v4_call73/topic_quality_placeholder_v4_call73.csv) |
| 49 | 373 | 163 | — | No | [`topic_quality_placeholder_v4_call49.csv`](../stage07_topic_quality/placeholder_v4_call49/topic_quality_placeholder_v4_call49.csv) |
| 19 | 302 | 131 | — | No | [`topic_quality_placeholder_v4_call19.csv`](../stage07_topic_quality/placeholder_v4_call19/topic_quality_placeholder_v4_call19.csv) |
| 68 | 395 | 198 | — | No | [`topic_quality_placeholder_v4_call68.csv`](../stage07_topic_quality/placeholder_v4_call68/topic_quality_placeholder_v4_call68.csv) |

**Caveat:** calls **55** and **73** use stopwords-correct `model_compare_enriched` (Main + KeyBERT/MMR/POS). For 49/19/68, run Stage06 with the fixed script before trusting topic JSON; prefer `exclude_from_axes` / `posthoc_reason` over raw `noise_candidate`.

---

## Recommended order (remaining this week)

1. **#9 Stage09 dry-run** on c8 labels (CPU, while GPU runs Phase 2)
2. **#3 Stage04 dry-run** (~30 min, CPU)
3. **#6 Stage05b holdout smoke** on call_73 (overnight GPU after Phase 2, or parallel if VRAM allows)
4. **#4 Notebooks** (CPU)

---

## Next step

**→ Phase 2 running on GPU; day work: Stage09 dry-run on c8 labels** (see [`placeholder_v4_call73_analysis_strategy.md`](placeholder_v4_call73_analysis_strategy.md))
