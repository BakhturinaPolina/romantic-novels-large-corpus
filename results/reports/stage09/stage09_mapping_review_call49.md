# Stage09 taxonomy mapping review — placeholder v4 call 49

**Date:** 2026-08-12
**Output:** `results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call49/taxonomy_mappings.json`
**Prompt / taxonomy:** v2 / v2.4 (+ coercion sexual-context gate)
**Verdict:** **pass** — Stage10 book aggregation complete. T112 precarity remapped to 6.4.

## Coverage

| Check | Result |
|-------|--------|
| Topics mapped | **348 / 348** (matches Stage08 bundle) |
| `secondary == main` | 0 |
| `is_noise` | 1 (T15 deferred-conversation / email paratext) |
| Confidence | medium 234 / high 114 |
| Evidence quality | low 163 / medium 160 / high 25 |
| `use_in_macro_axes` | 74 / 348 (21.3%) |

## Leaf distribution (top)

| Leaf | n | % | Role |
|------|---|---|------|
| 4.6 caretaking / emotional safety | 30 | 8.6 | everyday intimacy axis |
| uncertain_interpretable | 30 | 8.6 | weak / mixed topics (intended) |
| 9.2 promise / future speech | 22 | 6.3 | discourse-heavy |
| 1.7 nonverbal cues | 20 | 5.7 | context |
| 2.1 sexual tension | 18 | 5.2 | sexual axis |
| 4.3 secrets / misunderstanding | 17 | 4.9 | relational |
| 7.2 violence / non-sexual coercion | 13 | 3.7 | coercion watchlist |
| 4.2 courtship / bonding | 11 | 3.2 | everyday intimacy |
| 2.3 explicit sex | 7 | 2.0 | sexual axis |
| 7.4 sexual coercion | 2 | 0.6 | coercion watchlist |

Axis leaf totals: everyday `{4.2,4.6,2.2}` = **45**; sexual `{2.1,2.3,2.4,2.5}` = **31**; coercion `{7.2,7.4}` = **15**.

## Checks that passed

**Coercion gate (this session’s fix):** all 5 Stage08 `coercion_watchlist` topics routed correctly:

| Topic | Label | Stage08 sex | Main |
|-------|-------|-------------|------|
| 78 | Swearing War Before He Takes Her | none | **7.2** (was forced 7.4) |
| 82 | Touch Her and Your Family Suffers | none | **7.2** (sec 7.4) |
| 117 | Blamed and Threatened Into Compliance | none | **7.2** |
| 199 | Shoved to His Knees | explicit | **7.4** |
| 294 | Accepting Whatever Punishment Is Deserved | none | **7.2** |

**Explicit / sexual locks:** 8/9 explicit topics → 2.3 (or 2.5 contraception / 7.4 coercion). T230 postsex → 2.3 with 2.4 secondary (acceptable for `postsex_arousal`).

**Content-type routing:** discourse → mostly 9.x; subgenre_marker → mostly 10.1; scene → thematic mix. No mass dump into 4.2.

**Heuristic overrides (25):** sexual-function locks (T1/T7 → 2.3), appearance demotions (T18 → 1.6), coercion gate — behave as designed.

## Issues (severity)

### Fixed — T112 economic precarity

Was demoted 6.4→8.3b; `PRECARITY_TERMS` now includes `job`/`unemployment`/`employment`. Offline remap restored **main=6.4** (sec 6.2, macro=true). Covered by `test_job_loss_keeps_6_4`.

### Low — 4.6 over-reach (~5–8 topics)

Caretaking is the modal leaf. Most 4.6 labels are correct (fever check, keep safe, forehead peck on a child). Stretchy ones: T214 *Demanding to Know What Happened*, T273 *Mentor Gives Firm Instructions*, T277 *Promising to Handle The Lawyer*, T307 *Hauling Someone Up The Stairs* (conf 0.52–0.65). Macro is **false** on these, so they do not inflate the everyday-intimacy axis — leave unless a gold panel is planned.

### Low — T345 *Older Man Trading Shelter For Sex* → 7.4

Correct coercive/exploitative read; `sex_without_commitment` + economic secondary 6.4. Keep.

## Downstream (done)

- Stage10 `topic_lookup.parquet`, book taxonomy props, and indices under `results/stage10_correlation_analysis/v4_l12_granular_final_call49/`
- Manual review HTML/JSON enriched with Stage09 taxonomy badges for print
