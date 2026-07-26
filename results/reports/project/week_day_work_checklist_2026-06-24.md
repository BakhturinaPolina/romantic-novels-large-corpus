# Week day-work checklist (v4 granular — cross-embedding winner)

**Week of:** 2026-06-24 · **Updated:** 2026-07-26  
**Ultimate goal:** Compare Pareto-efficient configs across **L12, L6, MPNet** → pick stable **ultimate embedding + hyperparam winner** (same `eval_select_granular.yaml` gates + Pareto Phase 2 stability per model).  
**Legacy:** Placeholder call-73 taxonomy track paused ([strategy memo](../call73/placeholder_v4_call73_analysis_strategy.md) — historical only).  
**L12 status:** Phase 1 done (10 Pareto calls; Stage04 winner **call 142**); Pareto Phase 2 done — **3/10 stable**; stable shortlist **calls 73, 49, 11** (leader **call 73**, c_v 0.657) → [`v4_l12_granular_phase2_pareto/final_compare/`](../../experiments/v4_l12_granular_phase2_pareto/final_compare/).  
**L6 status:** Phase 1 done (160/160); Stage04 dry-run **19 Pareto calls** (Stage04 winner **call 110**); Pareto Phase 2 done — **19/19 stable**; compare-fit leader **call 16** (c_v 0.703) → [`v4_l6_granular_phase2_pareto/final_compare/`](../../experiments/v4_l6_granular_phase2_pareto/final_compare/).  
**MPNet status:** Phase 1 done (160/160); Stage04 dry-run **17 Pareto calls** (Stage04 winner **call 33**, collapsed in Phase 2); Pareto Phase 2 done — **13/17 stable**; compare-fit leader **call 131** (c_v 0.700, 87 topics) → [`v4_mpnet_granular_phase2_pareto/final_compare/`](../../experiments/v4_mpnet_granular_phase2_pareto/final_compare/).  
**Phase 3 narrowed BO:** **Deferred** until three-way stable shortlist comparison chooses embedding + hyperparams.

---

## Sequential GPU schedule (one machine)

| Step | Command | ETA | Status |
|------|---------|-----|--------|
| — | L12 Phase 1 + Stage04 dry-run + Pareto Phase 2 | — | **Done** |
| — | L6 Phase 1 + dry-run + Pareto Phase 2 | ~22 h compare-fit | **Done** |
| 1 | [`run_v4_granular_phase1.sh l6`](../../scripts/stage03/run_v4_granular_phase1.sh) | **~2–2.5 days** | **Done** |
| 2 | [`run_v4_granular_phase1_dryrun.sh l6`](../../scripts/stage04/run_v4_granular_phase1_dryrun.sh) | ~10 s | **Done** |
| 3 | [`run_v4_pareto_phase2.sh l6`](../../scripts/stage03/run_v4_pareto_phase2.sh) | **~22 h** (19 calls) | **Done** |
| 4 | [`run_v4_granular_phase1.sh mpnet`](../../scripts/stage03/run_v4_granular_phase1.sh) / embed-local tune | **~2–2.5 days** | **Done** |
| 5 | [`run_v4_granular_phase1_dryrun.sh mpnet`](../../scripts/stage04/run_v4_granular_phase1_dryrun.sh) | ~10 s | **Done** |
| 6 | [`run_v4_pareto_phase2.sh mpnet`](../../scripts/stage03/run_v4_pareto_phase2.sh) | **~15–20 h** (17 calls) | **Done** |
| 7 | [`run_v4_pareto_phase2.sh l12`](../../scripts/stage03/run_v4_pareto_phase2.sh) | **~12–14 h** (10 Pareto calls) | **Done** |
| **Total GPU** | | — | **Schedule complete** |

**Day work (CPU):** three-way selection notebooks + cross-embedding decision memo. GPU free for Stage05 final-fit / Phase 3 only after winner pick.

---

## This week — day work

| # | Task | Status | Link / artifact |
|---|------|--------|-----------------|
| 1 | [Stage05] Save placeholder models (top-5) | **Done** (legacy) | [`placeholder_v4_models/final_compare/`](../../experiments/placeholder_v4_models/final_compare/) |
| 2 | [Stage07] Post-hoc + topic quality | **Done** (legacy) | [`placeholder_v4_call73/`](../../stage07_topic_quality/placeholder_v4_call73/) |
| 3 | [Stage04] Dry-run v4 granular selection (L12) | **Done** | Winner **call 142** → [`v4_l12_granular_phase1_dryrun/`](../../selection/v4_l12_granular_phase1_dryrun/) |
| 4 | [Stage04] Selection notebooks (v4 L12/L6/MPNet) | **Next** | [`notebooks/04_selection/`](../../notebooks/04_selection/) + [`selection_notebooks_v4_granular.yaml`](../../../configs/stage04/selection_notebooks_v4_granular.yaml) (MPNet dry-run paths already wired) |
| 5 | [Meta] Cross-embedding stable shortlist decision | **Next** | Compare L12 {73,49,11} vs L6 leader **16** vs MPNet {131,21,149,…} → pick ultimate embedding + call |
| 6 | [Stage05b] Holdout smoke test | **Done** (legacy) | [`v4_l12_granular_final_call73`](../../experiments/v4_l12_granular_final_call73/) |
| 7–10 | Stage06–09 / final-fit call 73 | **Done** (legacy) | Placeholder track; re-run on ultimate winner after #5 |
| — | [Meta] L12 Phase 1 + Pareto Phase 2 | **Done** | 3/10 stable → [`v4_l12_granular_phase2_pareto/`](../../experiments/v4_l12_granular_phase2_pareto/) |
| — | [Meta] L6 Phase 1 + Pareto Phase 2 | **Done** | 19/19 stable → [`v4_l6_granular_phase2_pareto/`](../../experiments/v4_l6_granular_phase2_pareto/) |
| — | [Meta] MPNet Phase 1 BO | **Done** | 160/160; [`trials_partial.csv`](../../experiments/v4_mpnet_granular_phase1/opt_1_sentence-transformers__paraphrase-mpnet-base-v2/trials_partial.csv) |
| — | [Meta] MPNet Stage04 dry-run | **Done** | 17 Pareto; winner **call 33** → [`v4_mpnet_granular_phase1_dryrun/`](../../selection/v4_mpnet_granular_phase1_dryrun/) |
| — | [Meta] MPNet **Pareto** Phase 2 | **Done** | 13/17 stable; leader **call 131** → [`v4_mpnet_granular_phase2_pareto/final_compare/`](../../experiments/v4_mpnet_granular_phase2_pareto/final_compare/) |
| — | [Meta] Phase 3 narrowed BO | **Deferred** | After three-way decision (#5) |

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
| [Stage05] compare-fit resume with `--reduce-outliers` | **Done** | Skip when `metrics.json` + `outliers_reduced/` exist; GPU cleanup between stability seeds |

---

## Completed since last update

| Item | Status | Link |
|------|--------|------|
| MPNet Phase 1 BO (160/160) | **Done** | [`v4_mpnet_granular_phase1/`](../../experiments/v4_mpnet_granular_phase1/) |
| MPNet Stage04 dry-run (17 Pareto; winner call 33) | **Done** | [`v4_mpnet_granular_phase1_dryrun/`](../../selection/v4_mpnet_granular_phase1_dryrun/) |
| MPNet Pareto Phase 2 (13/17 stable) | **Done** | [`stability_summary.csv`](../../experiments/v4_mpnet_granular_phase2_pareto/final_compare/stability_summary.csv) |
| Stage05 GPU OOM + resume skip fixes | **Done** | `compare_fit.py` (free models between seeds; skip completed + reduced) |

---

## MPNet stable shortlist (Pareto Phase 2)

Top by compare-fit coherence among **stability_pass=True**:

| Call | c_v | diversity | n_topics | notes |
|------|-----|-----------|----------|-------|
| **131** | **0.700** | 0.306 | 87 | coherence leader |
| **21** | 0.696 | 0.349 | 99 | |
| **149** | 0.692 | 0.408 | 105 | |
| **20** | 0.686 | 0.439 | 104 | |
| **156** | 0.681 | 0.587 | 83 | |
| **133** | 0.676 | 0.652 | 171 | more granular |
| **147** | 0.653 | 0.703 | 88 | |
| **116** | 0.634 | 0.728 | 216 | |
| **80** | 0.628 | 0.756 | 210 | |
| **38** | 0.542 | 0.951 | 444 | diversity / topic-count extreme |

Collapsed (4/17): **33** (Stage04 winner), **72**, **83**, **140**. Full: [`comparison_summary.csv`](../../experiments/v4_mpnet_granular_phase2_pareto/final_compare/comparison_summary.csv).

---

## L12 stable shortlist (Pareto Phase 2)

| Call | c_v | diversity | n_topics | stability |
|------|-----|-----------|----------|-----------|
| **73** | **0.657** | 0.669 | 329 | Pass |
| **49** | 0.654 | 0.686 | 373 | Pass |
| **11** | 0.516 | 0.959 | 387 | Pass |

7/10 Pareto calls failed stability. Stage04 winner **call 142** excluded. → [`comparison_summary.csv`](../../experiments/v4_l12_granular_phase2_pareto/final_compare/comparison_summary.csv).

---

## Cross-embedding snapshot (stable leaders)

| Embedding | Stable / Pareto | Leader call | c_v | n_topics | diversity |
|-----------|-----------------|-------------|-----|----------|-----------|
| L6 | 19/19 | **16** | **0.703** | (see compare) | — |
| MPNet | 13/17 | **131** | 0.700 | 87 | 0.306 |
| L12 | 3/10 | **73** | 0.657 | 329 | 0.669 |

---

## Next steps

1. **CPU — selection notebooks:** run [`selection_notebooks_v4_granular.yaml`](../../../configs/stage04/selection_notebooks_v4_granular.yaml) for L12 + L6 + MPNet dry-runs (MPNet paths already configured).  
2. **Decision memo:** three-way stable shortlist (coherence vs diversity vs topic count vs stability rate). Candidates to weigh: L6 **16**, MPNet **131** / **133** / **38**, L12 **73**.  
3. **After pick:** Stage05 final-fit + Stage05b holdout on the winner; optional Phase 3 narrowed BO only if shortlist is still ambiguous.  
4. **Optional hardening:** Stage05b coherence fix; post-hoc noise rules before any new Stage08 spend.
