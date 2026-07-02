# Taxonomy v2.4: Heuristic Hardening

**Date:** 2026-07-01  
**Config:** `configs/stage09/romance_corpus_taxonomy_v2.yaml` (version 2.4)  
**Prior:** [taxonomy_v23_axis_context_design.md](taxonomy_v23_axis_context_design.md)

## Problem (v2.3 pilot)

Topics **7** (wink) and **23** (love confession) had correct LLM labels (**1.7**, **4.5**) but heuristics forced **2.2** because Stage08 `sexual_function=nonsexual_affection` was in `SEXUAL_LOCK_FUNCTIONS`. Generic business deals mapped to **6.1** (axis-eligible) without romantic status evidence.

## v2.4 changes

1. **Remove `nonsexual_affection` from sexual lock** — promote to 2.2 only with physical-affection vocabulary (kiss/hug/embrace).
2. **`PROTECTED_MAIN_IDS`** — block heuristic promotion to 2.2 for 1.7, 4.5, 4.3, 4.4, 4.6, 7.4, 2.3, 2.5 at medium/high evidence.
3. **Split 6.1 → 6.1a / 6.1b** — elite romantic status (axis) vs generic business negotiation (context).
4. **`exploratory_only_ids: [3.3]`** + **`AX_internal_ambivalence`** for H5/H6 exploratory analysis.
5. **Prompt v2.4** — RWA-aligned purpose statement; wink/confession negative examples; topic-9 few-shot fixed.

## ID migration

| Old | New | Default |
|-----|-----|---------|
| 6.1 | 6.1b | generic deal/contract/payment |
| 6.1 | 6.1a | billionaire/CEO/aristocratic hero status |

## Acceptance targets (pilot30)

| Topic | Expected |
|-------|----------|
| 2 | 2.1 |
| 7 | 1.7, macro false |
| 9 | 6.1b, macro false |
| 23 | 4.5, macro true |
| 4, 11, 29 | not 4.2 |

## Re-map checklist

- [ ] `taxonomy_mappings_v24_pilot30.json` passes acceptance
- [ ] Full call73 re-map (~151 topics)
- [ ] Stage10 aggregation smoke on 6.1a/6.1b columns
