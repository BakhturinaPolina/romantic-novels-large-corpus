# Week day-work checklist (v4 granular — cross-embedding winner)

**Week of:** 2026-06-24 · **Updated:** 2026-07-02  
**Ultimate goal:** Compare Pareto-efficient configs across **L12, L6, MPNet** → pick stable **ultimate embedding + hyperparam winner** (same `eval_select_granular.yaml` gates + Pareto Phase 2 stability per model).  
**Legacy:** Placeholder call-73 taxonomy track paused ([strategy memo](../call73/placeholder_v4_call73_analysis_strategy.md) — historical only).  
**L12 status:** Phase 1 done (10 Pareto calls; Stage04 winner **call 142**); band Phase 2 done ([`phase2_stability`](../../experiments/v4_l12_granular_phase2_stability/)) — superseded by Pareto Phase 2 for cross-model work.  
**Phase 3 narrowed BO:** **Deferred** until all three embeddings complete Pareto + stability comparison.

---

## Sequential GPU schedule (one machine)

| Step | Command | ETA | Status |
|------|---------|-----|--------|
| — | L12 Phase 1 + Stage04 dry-run | — | **Done** |
| 1 | [`run_v4_granular_phase1.sh l6`](../../scripts/stage03/run_v4_granular_phase1.sh) | **~2–2.5 days** | To do |
| 2 | [`run_v4_granular_phase1_dryrun.sh l6`](../../scripts/stage04/run_v4_granular_phase1_dryrun.sh) | ~10 s | Blocked on step 1 |
| 3 | [`run_v4_pareto_phase2.sh l6`](../../scripts/stage03/run_v4_pareto_phase2.sh) | **~8–14 h** | Blocked on step 2 |
| 4 | [`run_v4_granular_phase1.sh mpnet`](../../scripts/stage03/run_v4_granular_phase1.sh) | **~2–2.5 days** | To do |
| 5 | [`run_v4_granular_phase1_dryrun.sh mpnet`](../../scripts/stage04/run_v4_granular_phase1_dryrun.sh) | ~10 s | Blocked on step 4 |
| 6 | [`run_v4_pareto_phase2.sh mpnet`](../../scripts/stage03/run_v4_pareto_phase2.sh) | **~8–14 h** | Blocked on step 5 |
| 7 | [`run_v4_pareto_phase2.sh l12`](../../scripts/stage03/run_v4_pareto_phase2.sh) | **~12–14 h** (all **10** Pareto calls) | To do |
| **Total GPU** | | **~7–10 days** | |

**Day work (CPU, parallel with GPU):** selection notebooks via [`selection_notebooks_v4_granular.yaml`](../../../configs/stage04/selection_notebooks_v4_granular.yaml) after steps 2+5+7; Stage09 full remap can run on API while GPU is busy.

---

## This week — day work

| # | Task | Status | Link / artifact |
|---|------|--------|-----------------|
| 1 | [Stage05] Save placeholder models (top-5) | **Done** (legacy) | [`placeholder_v4_models/final_compare/`](../../experiments/placeholder_v4_models/final_compare/) |
| 2 | [Stage07] Post-hoc + topic quality | **Done** (legacy) | [`placeholder_v4_call73/`](../../stage07_topic_quality/placeholder_v4_call73/) |
| 3 | [Stage04] Dry-run v4 granular selection (L12) | **Done** | [`run_v4_granular_phase1_dryrun.sh`](../../scripts/stage04/run_v4_granular_phase1_dryrun.sh); winner **call 142** → [`v4_l12_granular_phase1_dryrun/`](../../selection/v4_l12_granular_phase1_dryrun/); memo: [`stage04_v4_l12_granular_phase1_dryrun_report.md`](../stage04/stage04_v4_l12_granular_phase1_dryrun_report.md) |
| 4 | [Stage04] Selection notebooks (v4 L12/L6/MPNet) | To do | [`notebooks/04_selection/`](../../notebooks/04_selection/) + [`selection_notebooks_v4_granular.yaml`](../../../configs/stage04/selection_notebooks_v4_granular.yaml) |
| 5 | [Stage05] Compare-fit top v4 trials (granularity inspect) | **Done** (legacy) | Placeholder top-5 sweep |
| 6 | [Stage05b] Holdout smoke test | **Done** (legacy) | [`v4_l12_granular_final_call73`](../../experiments/v4_l12_granular_final_call73/) |
| 7 | [Stage06] Representation refresh → topics JSON | **Done** (legacy) | call 55/73 placeholder |
| 8 | [Stage08] LLM labels | **Done** (legacy) | c8 production on placeholder call 73 |
| 9 | [Stage09] Taxonomy / category mapping | Pilot done | v2.4 pilot30 accepted; full remap optional until ultimate winner chosen |
| 10 | [Stage05] Final compare-fit + infer (call 73) | **Done** (legacy) | [`v4_l12_granular_final_call73/`](../../experiments/v4_l12_granular_final_call73/) |
| — | [Meta] L12 Phase 1 BO | **Done** | 160/160; [`trials_partial.csv`](../../experiments/v4_l12_granular_phase1/opt_1_sentence-transformers__all-MiniLM-L12-v2/trials_partial.csv) |
| — | [Meta] L12 band Phase 2 stability | **Done** (legacy) | [`v4_l12_granular_phase2_stability/`](../../experiments/v4_l12_granular_phase2_stability/) — 14 band picks |
| — | [Meta] L12 **Pareto** Phase 2 | To do | [`run_v4_pareto_phase2.sh l12`](../../scripts/stage03/run_v4_pareto_phase2.sh) → `v4_l12_granular_phase2_pareto/` |
| — | [Meta] L6 Phase 1 BO | To do | [`run_v4_granular_phase1.sh l6`](../../scripts/stage03/run_v4_granular_phase1.sh) |
| — | [Meta] MPNet Phase 1 BO | To do | [`run_v4_granular_phase1.sh mpnet`](../../scripts/stage03/run_v4_granular_phase1.sh) |
| — | [Meta] Phase 3 narrowed BO | **Deferred** | After three-way Pareto + stability comparison |

---

## Week 2 — hardening

| Task | Status | Notes |
|------|--------|-------|
| [Config] `configs/placeholder_pipeline.yaml` | To do | Single swap file for downstream chain |
| [Scripts] `scripts/run_downstream_placeholder.sh` | To do | Chain Stage04→05→05b→06→07→08 smoke |
| [Post-hoc] `dialogue_delivery` + `speech_act_filler` rules | To do | [`src/common/topic_posthoc/rules.py`](../../src/common/topic_posthoc/rules.py) |
| [Stage08] Filter `[NOISE:rule_id]` before LLM spend | To do | Use Stage07 `posthoc_reason` columns |
| [Stage03/05] P1 pre-fit: mojibake/NFKD + character-name preprocessing | To do | [`src/stage03_train/data_io.py`](../../src/stage03_train/data_io.py) |
| [Stage05b] Fix holdout coherence scoring (`n_topics=0`) | To do | [`test_metrics.json`](../../evaluation/v4_l12_granular_final_call73/call_73/test_metrics.json) |
| [Stage10] Book aggregation smoke | To do | After taxonomy on ultimate winner |

---

## Completed since last update

| Item | Status | Link |
|------|--------|------|
| Stage04 L12 dry-run + memo | **Done** | [`v4_l12_granular_phase1_dryrun/`](../../selection/v4_l12_granular_phase1_dryrun/); [`stage04_v4_l12_granular_phase1_dryrun_report.md`](../stage04/stage04_v4_l12_granular_phase1_dryrun_report.md) |
| Pareto Phase 2 + dry-run scripts | **Done** | [`run_v4_pareto_phase2.sh`](../../scripts/stage03/run_v4_pareto_phase2.sh), [`run_v4_granular_phase1_dryrun.sh`](../../scripts/stage04/run_v4_granular_phase1_dryrun.sh) |
| v4 three-way notebook config | **Done** | [`selection_notebooks_v4_granular.yaml`](../../../configs/stage04/selection_notebooks_v4_granular.yaml) |

---

## L12 Pareto frontier (Stage04 dry-run)

| Rank | Call | weighted_score | c_v | diversity | n_topics |
|------|------|----------------|-----|-----------|----------|
| 1 | **142** | 0.534 | 0.625 | 0.866 | 357 |
| 2 | 79 | 0.531 | 0.641 | 0.822 | 309 |
| 8 | 73 | 0.509 | 0.657 | 0.669 | 329 |
| 10 | 55 | 0.447 | 0.694 | 0.285 | 117 |

Full list: [`top_k.csv`](../../selection/v4_l12_granular_phase1_dryrun/top_k.csv) (10 Pareto-efficient trials).

---

## Next step

**→ Start L6 Phase 1:** `./scripts/stage03/run_v4_granular_phase1.sh l6`  
Then chain steps 2–3 from the GPU schedule above. L12 Pareto Phase 2 (step 7) can run last or in a gap before MPNet if the GPU queue allows.
