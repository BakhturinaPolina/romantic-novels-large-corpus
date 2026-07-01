# Stage09 topic metadata input (call 73)

Two JSON bundles for Stage09 and human review.

| File | Purpose |
|------|---------|
| `topic_metadata_v3.json` | Slim Stage09 input (`--labels-json`, use `--no-snippets`) |
| `topic_metadata_v3_review_enriched.json` | Full human review: representations, snippets, rationale |

## Slim bundle (`topic_metadata_v3.json`)

- `label`, `scene_summary`, `keywords`, `snippets`
- `content_type`, `is_noise`, `exclude_from_axes`
- `sexual_explicitness`, `sexual_function`, `consent_status`

Deprecated fields (`register`, `subgenre_hints`, `axis_hint`) are derived in Stage09 via `v3_derived_fields.py`.

## Review bundle (`topic_metadata_v3_review_enriched.json`)

Adds `representations` (KeyBERT, MMR, POS, Main), `all_keywords`, and `rationale` for manual label QA. Not required for taxonomy mapping.

## Run Stage09

```bash
python3 -m src.stage09_category_mapping.stage2_theory_driven_categories.scripts.zeroshot_taxonomy_openrouter \
  --labels-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
  --output-json results/stage09_category_mapping/stage2_theory_driven_categories/placeholder_v4_call73/taxonomy_mappings.json \
  --prompt-version v2 \
  --no-snippets
```

Regenerate slim export from review bundle:

```bash
python3 -m src.stage08_llm_labeling.openrouter_experiments.tools.export_stage09_topic_metadata \
  --input-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3_review_enriched.json
```
