# Taxonomy v2.3: Axis-Bearing vs Context-Only Design

**Date:** 2026-07-01  
**Config:** `configs/stage09/romance_corpus_taxonomy_v2.yaml` (version 2.3)  
**Measurement schema:** `configs/stage09/theory_aligned_index_schema.yaml` (v2.3)

## Problem

Stage08-derived `axis_hint=everyday_intimacy_emotional_safety` was assigned to ~292/322 topics because `sexual_function=none` defaulted to that axis. Stage09 then mapped weak object/transit/gesture topics to **4.2** (everyday bonding), inflating H1/H4 composites. Post-hoc heuristics also rewrote sexual-tension topics to **1.6** (appearance) when hair/neck/forehead vocabulary appeared.

## Design

1. **Full leaf taxonomy** remains for Stage09 zero-shot classification (doors, coffee, phones, smiles, discourse, subgenre markers).
2. **`axis_bearing_ids`** — narrow allowlist for Stage10 hypothesis macro-axes only.
3. **`uncertain_interpretable`** — safe fallback instead of forcing **4.2**.
4. **Split IDs** — `8.3a` (commitment symbols) vs `8.3b` (ordinary props); `5.3a` (wedding/proposal rituals) vs `5.3b` (parties/gossip).

## Axis-bearing IDs (Stage10)

| Group | IDs |
|-------|-----|
| Sexuality | 2.1, 2.2, 2.3, 2.4, 2.5 |
| Emotions | 3.1 (resolution/payoff only), 3.2 |
| Relationship | 4.2, 4.3, 4.4, 4.5, 4.6, 4.7 |
| HEA ritual | 5.3a |
| Status/wealth | 6.1, 6.4, 6.6, 6.7 |
| Risk | 7.2, 7.3, 7.4 (watchlist) |
| Commitment objects | 8.3a |

## Context-only (macro axes off)

1.x, 4.1, 5.1, 5.2, 5.3b, 6.2, 6.3, 6.5, 7.1, 8.x (except 8.3a as axis low-weight), 9.x, 10.x, `uncertain_interpretable`, `noise`.

## Pilot audit (v2.2 → expected v2.3)

| Topic | Label | v2.2 issue | v2.3 target |
|-------|-------|------------|-------------|
| 0 | Hesitant Arrival | OK (8.5) | 8.5, macro false |
| 2 | Hot Breath / Neck | Heuristic → 1.6 | **2.1** (sexual lock) |
| 4 | Frantic Phone Call | 4.2 inflation | 8.3b or 9.2 |
| 11 | Coffee Mug | 4.2 inflation | 8.1 or 8.3b |
| 14 | Publisher Copyright | OK (noise) | noise |
| 26 | King-Sized Bed | 7.4 watchlist | 7.4 if consent unclear |
| 29 | Horses at Stable | 4.2 inflation | 8.2 or uncertain |

## Code changes

- `taxonomy_v2.py`: sexual-function lock, precarity gate for 6.4, axis-bearing enforcement, fallback `uncertain_interpretable`
- `v3_derived_fields.py`: `axis_hint=no_hypothesis_signal` for `sexual_function=none`
- `taxonomy_mapping_v2.py`: hypothesis-relevance gate, negative/positive examples, deal→6.1 few-shot

## Re-map checklist

```bash
python -m src.stage09_category_mapping.stage1_theory_driven_categories.scripts.zeroshot_taxonomy_openrouter \
  --labels-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
  --output-json results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call73/taxonomy_mappings_v23.json \
  --prompt-version v2
```

Acceptance: topic 2 → 2.1; topics 4/11/29 not 4.2 unless snippets show bonding; zero sexual-lock heuristic contradictions.
