# Week day-work checklist (placeholder pipeline)

**Week of:** 2026-06-24  
**Context:** v4 L12 Phase 1 BO runs at night; day work uses `placeholder_v4_models` (top-5: calls 55, 73, 49, 19, 68) until Phase 3 winner exists.  
**Night track:** `v4_l12_granular_phase1` BO → Phase 2 stability → Phase 3 narrowed BO.

---

## This week — day work

| # | Task | Status | Link / artifact |
|---|------|--------|-----------------|
| 1 | [Stage05] Save placeholder models (top-5) | **Done** | [`placeholder_v4_models/final_compare/`](../experiments/placeholder_v4_models/final_compare/) — calls **55, 73, 49, 19, 68** with `--save-model`; refit topic counts match BO |
| 2 | [Stage07] Post-hoc + topic quality (top-5 calls) | **Done** | [`results/stage07_topic_quality/`](../stage07_topic_quality/) — [`placeholder_v4_summary.json`](../stage07_topic_quality/placeholder_v4_summary.json); script: [`scripts/run_stage07_placeholder_v4_models.sh`](../../scripts/run_stage07_placeholder_v4_models.sh) (`CALLS=55` for single-call refresh) |
| 3 | [Stage04] Dry-run v4 granular selection | **To do** ← **next** | Run: `.venv/bin/python -m src.stage04_eval_select.cli select --trials results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv --config configs/eval_select_granular.yaml --run-id v4_l12_granular_phase1_dryrun` → `results/selection/v4_l12_granular_phase1_dryrun/` |
| 4 | [Stage04] Selection notebooks (v3 L12 vs L6) | To do | [`notebooks/04_selection/`](../../notebooks/04_selection/) + [`configs/selection_notebooks.yaml`](../../configs/selection_notebooks.yaml) |
| 5 | [Stage05] Compare-fit top v4 trials (granularity inspect) | **Done** | Same as #1 — top-5 by `bo_objective` on partial Phase 1 CSV |
| 6 | [Stage05b] Holdout smoke test on placeholder | To do | **call_73** recommended: `placeholder_v4_models/final_compare/call_73/model_compare` (~3–8 h full test; overnight). Stage06 unblocks labeling only, not holdout |
| 7 | [Stage06] Representation refresh → topics JSON | **Partial** | **calls 55 + 73 done** — script [`scripts/run_stage06_placeholder_v4_call.sh`](../../scripts/run_stage06_placeholder_v4_call.sh); enriched: `call_{55,73}/model_compare_enriched/`; topics JSON: [`stage06_topic_exploration/placeholder_v4_call{55,73}/`](../stage06_topic_exploration/) |
| 8 | [Stage08] LLM labels — pilot ~20 topics → full | To do | **call_55** ready (~113 usable topics after Stage07); use `posthoc_reason` / `exclude_from_axes`, not raw `noise_candidate` |
| 9 | [Stage09] Taxonomy / category mapping dry-run | To do | [`src/stage09_category_mapping/`](../../src/stage09_category_mapping/) — needs Stage08 labels |
| — | [Meta] Night GPU: v4 L12 Phase 1 → 2 → 3 | **Doing** | BO log: `logs/stage03_v4_l12_granular_phase1.log` |

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
| Stage06 + Stage07 refresh on call_55 | **Done** | ~90 s Stage06; 4 `noise_candidates` (was 117 false positives) |
| Stage06 + Stage07 refresh on call_73 | **Done** | ~3.5 min Stage06; 163 `noise_candidates` (was 330) |

---

## Stage07 snapshot (placeholder v4)

| Call | Topics | `noise_candidates` | Stage06 enriched? | Quality CSV |
|------|--------|-------------------|-------------------|-------------|
| 55 | 117 | 4 | Yes | [`topic_quality_placeholder_v4_call55.csv`](../stage07_topic_quality/placeholder_v4_call55/topic_quality_placeholder_v4_call55.csv) |
| 73 | 330 | 163 | Yes | [`topic_quality_placeholder_v4_call73.csv`](../stage07_topic_quality/placeholder_v4_call73/topic_quality_placeholder_v4_call73.csv) |
| 49 | 373 | 163 | No | [`topic_quality_placeholder_v4_call49.csv`](../stage07_topic_quality/placeholder_v4_call49/topic_quality_placeholder_v4_call49.csv) |
| 19 | 302 | 131 | No | [`topic_quality_placeholder_v4_call19.csv`](../stage07_topic_quality/placeholder_v4_call19/topic_quality_placeholder_v4_call19.csv) |
| 68 | 395 | 198 | No | [`topic_quality_placeholder_v4_call68.csv`](../stage07_topic_quality/placeholder_v4_call68/topic_quality_placeholder_v4_call68.csv) |

**Caveat:** calls **55** and **73** have POS/KeyBERT aspects in `model_compare_enriched`. For 49/19/68, `noise_candidates` still mixes post-hoc rules with missing-POS flags — prefer `exclude_from_axes` / `posthoc_reason` until Stage06.

---

## Recommended order (remaining this week)

1. **#3 Stage04 dry-run** (~30 min, CPU) — validates granular gates on partial v4 trials  
2. **#6 Stage05b smoke on call_73** (overnight GPU) — full test holdout transform  
3. **#8 Stage08 pilot on call_55** (~10–30 min API) — topics JSON ready at [`placeholder_v4_call55/`](../stage06_topic_exploration/placeholder_v4_call55/)  
4. **#4 Notebooks** (CPU) — parallel with night BO  
5. Optional: Stage06 on call_49 or call_19 if comparing Band C variants  

---

## Next step

**→ Task #3: [Stage04] Dry-run v4 granular selection** (~30 min, no GPU)

```bash
.venv/bin/python -m src.stage04_eval_select.cli select \
  --trials results/experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv \
  --config configs/eval_select_granular.yaml \
  --run-id v4_l12_granular_phase1_dryrun
```

Then **#6 Stage05b** (overnight) or **#8 Stage08 pilot on call_55** when ready to spend API credits.
