# Stage09 topic metadata input (call 73)

Slim export from Stage08 v3 labels — ready for `--labels-json` in Stage09 taxonomy mapping.

## Included per topic

- `label`, `scene_summary`, `keywords`
- `content_type`, `is_noise`, `exclude_from_axes`
- `sexual_explicitness`, `sexual_function`, `consent_status`
- `snippets` (when present in source enriched export)

## Excluded (derived or review-only)

- `register`, `subgenre_hints`, `axis_hint` — derived in Stage09 via `v3_derived_fields.py`
- `stage07_*`, `rationale`, `representations`, `all_keywords`

## Run Stage09

```bash
python3 -m src.stage09_category_mapping.stage2_theory_driven_categories.scripts.zeroshot_taxonomy_openrouter \
  --labels-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
  --output-json results/stage09_category_mapping/stage2_theory_driven_categories/placeholder_v4_call73/taxonomy_mappings.json \
  --prompt-version v2 \
  --no-snippets
```

Use `--no-snippets` when snippets are already embedded in this JSON (recommended for this bundle).
