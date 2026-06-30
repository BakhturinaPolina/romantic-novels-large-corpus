# Placeholder v4 call 73 — frozen analysis strategy

**Status:** Active strategy memo (frozen BO call for taxonomy / Stage08–09).  
**Date:** 2026-06-25  
**Frozen model:** `placeholder_v4_models` / compare-fit **call 73** (`configs/placeholder_v4_frozen_call73.yaml`)

## Related artifacts

| Artifact | Path |
|----------|------|
| Compare-fit model | `results/experiments/placeholder_v4_models/final_compare/call_73/` |
| Enriched model (Stage06) | `.../call_73/model_compare_enriched/` |
| Stage06 topics JSON | `results/stage06_topic_exploration/placeholder_v4_call73/` |
| Stage07 quality table | `results/stage07_topic_quality/placeholder_v4_call73/topic_quality_placeholder_v4_call73.csv` |
| Post-hoc rules | `configs/topic_posthoc_rules.yaml` |
| Outlier / collapse evidence | `results/experiments/v3_minilm12v2_first/final_compare/call_*/outliers_reduced/`, `.../call_59/metrics.json` (`refit_collapse`) |
| Prior taxonomy memo (call_59) | `results/reports/stage08_stage09_taxonomy_improvement_notes_call59.md` |
| Post-hoc limitations | `results/reports/stage03_posthoc_cleaning_limitations_memo.md` |

---

## 1. Why call 73 (not 55)

| | Call 73 (frozen) | Call 55 (reference only) |
|--|------------------|---------------------------|
| Topics | ~330 | 117 |
| Coherence | 0.66 | **0.69** |
| Diversity | **0.67** | 0.28 |
| Usable axes (≥200 docs, not excluded) | **151** (23 core ≥800, 128 mid) | ~116 |
| Tiny tail excluded | 159 | 0 |
| Character-name excluded (post-hoc) | 44 | — |

**Call 73** is frozen for **fine-grained romance scene inventory** and downstream taxonomy work. Call 55 remains a compact reference for BO selection comparisons only.

---

## 2. Outlier strategy (do not chase low outlier rate)

**Observation:** v4 placeholder fits have **~70% hard outliers** (`topic -1`). Forcing assignment (`reduce_outliers`, aggressive HDBSCAN) collapses to **3–9 mega-topics** (v3 call_17, call_3; call_59 stability refit → 3 topics).

**Chosen approach:**

1. **Accept ~70% outliers at compare-fit** — structural for sentence-level HDBSCAN on this corpus.
2. **Treat `-1` as explicit background** in book-level mixtures (K+1), not a failure to fix.
3. **Do not default `reduce_outliers`** — only if stability passes and topic count stays within tolerance.
4. **Soft assignment at inference** — final fit with `calculate_probabilities: true`; Stage09 mixtures via `transform()` on full corpus (see `results/reports/v4_granular_stage05_probabilities.md`).
5. **BO selection** — penalize topic count / reward coherence; **ignore outlier_rate** as a target metric.

---

## 3. Post-hoc cleaning (metadata only)

Rules in `configs/topic_posthoc_rules.yaml` set `exclude_from_axes` without mutating the model:

| Rule | Purpose |
|------|---------|
| `tiny_topic` | Exclude topics &lt;200 docs (159 on call 73) |
| `character_name_cluster` | Exclude name-dominated topics (filtered stoplist) |
| `publisher_boilerplate` | Repr-doc regex + Main-word fallback (`chapter`, `book`, `author`) |
| `multilingual_artifact` | Non-English / short-token garbage |

**Plumbing:** After Stage06, `topic_info.csv` is **synced from `model_compare_enriched`** so rules see semantic Main labels (not stale verb-heavy exports).

**Known limitation (2026-06-25):** The BookNLP/spaCy name stoplist (~72k tokens) includes common scene nouns (`horse`, `dinner`, `dream`). The tightened `character_name_cluster` rule (morphology filter + scene blocklist + 4/4 stoplist hits + ≥2 long tokens) removes verb false positives (T7 smile, T13 laughed) but still flags some scene topics (e.g. T29 horses, T52 dinner). Treat flagged topics as **review queue**, not auto-delete; tune rule or add allowlist before Stage08 spend.

**Pre-fit (future):** Port `preprocess_character_name` + stoplist into `clean_sentence` — requires refit (`stage03_posthoc_cleaning_limitations_memo.md`).

---

## 4. Weak-topic tiers (call 73, post character-name rule)

| Tier | Count | Action |
|------|-------|--------|
| **Core** (≥800 docs, not excluded) | 23 | Primary taxonomy axes |
| **Mid** (200–799 docs, not excluded) | 128 | Secondary axes / optional merge |
| **Excluded total** | 179 | 159 `tiny_topic` + 44 `character_name_cluster` + 1 `publisher_boilerplate` (T14; overlaps character rule) |
| **Usable for Stage08** | **151** | `exclude_from_axes == false` |
| **Generic dialogue** (T3, T5, T10, T17) | 4 large | Merge candidates in Stage08 |
| **Intimacy overlap** (T1, T2, T70) | 3 | Merge candidates |
| **Character-name queue** | 44 | Manual review; some are scene false positives |

Top usable by size: T1 kissed (5632), T2 kiss (4504), T3 wanted (3707), T5 know/don't tell (2569), T10 whispered (1474).

---

## 5. Next steps to run (call 73 only)

**Immediate (before Stage08 API spend):**

```bash
# Optional: re-sync after rule tweaks
bash scripts/run_stage06_placeholder_v4_call.sh 73
bash scripts/run_stage07_placeholder_v4_models.sh   # default CALLS=73
```

1. **Review character-name queue** — spot-check the 44 flagged topics in [`topic_quality_placeholder_v4_call73.csv`](../stage07_topic_quality/placeholder_v4_call73/topic_quality_placeholder_v4_call73.csv); un-flag scene topics (allowlist or rule tweak in `configs/topic_posthoc_rules.yaml`).
2. **Stage04 dry-run** (~30 min, CPU) — validate granular gates on partial v4 trials (independent of frozen call).
3. **Stage08 LLM** — model pilots done (**Sonnet** locked). **Prompt OVAT sweep** before production ([`stage08_prompting_research_design_call73.md`](stage08_prompting_research_design_call73.md)).
4. **Stage05b holdout** on call_73 (overnight GPU) — full test transform; unblocks inference validation.
5. **Stage09 mixtures** — soft probabilities on full corpus after final fit; **do not** run `compare --reduce-outliers` on call 73.

**Reference only (not frozen):** call 55 compact taxonomy, calls 49/19/68 for BO comparison if Phase 3 narrows.

**Do not run** until needed: `compare --reduce-outliers` on call 73 (collapse risk documented in §2).

---

## 6. Where to document strategy in `results/reports/`

| Topic | Primary doc | Also update |
|-------|-------------|-------------|
| **Frozen call, paths, metrics** | [`configs/placeholder_v4_frozen_call73.yaml`](../../configs/placeholder_v4_frozen_call73.yaml) | This file §1 |
| **Outlier / mixture / no-reduce-outliers policy** | **This file** §2 | [`v4_granular_stage05_probabilities.md`](v4_granular_stage05_probabilities.md) |
| **Post-hoc rules + limitations** | [`stage03_posthoc_cleaning_limitations_memo.md`](stage03_posthoc_cleaning_limitations_memo.md) | `configs/topic_posthoc_rules.yaml` |
| **Stage08 LLM model + prompt sweep** | [`stage08_production_model_decision_call73.md`](stage08_production_model_decision_call73.md), [`stage08_prompting_research_design_call73.md`](stage08_prompting_research_design_call73.md), [`stage08_progress.md`](stage08_progress.md) | `configs/stage08_labeling.yaml` |
| **Weekly execution checklist** | [`week_day_work_checklist_2026-06-24.md`](week_day_work_checklist_2026-06-24.md) | Point all downstream tasks at call 73 |
| **BO selection / Phase 1–3** | [`stage04_v3_l12_l6_bo_selection_report.md`](stage04_v3_l12_l6_bo_selection_report.md) | Dry-run output under `results/selection/` |
