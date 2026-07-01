# Stage09 topic metadata input (call 73)

Two JSON bundles for Stage09 and human review.

| File | Purpose |
|------|---------|
| `topic_metadata_v3.json` | Slim Stage09 input (`--labels-json`, use `--no-snippets`) |
| `topic_metadata_v3_review_enriched.json` | Full human review: representations, snippets, rationale |
| `snippet_trap_merge_log.json` | 79-topic merge log (production → `v3_rep_first` snippet-trap overrides) |

**Label sources:** 79 panel topics use `v3_rep_first` relabels (see `data/stage08_benchmark/call73_snippet_trap_panel.json`); all others remain `v3_topic_labeling`. Review bundle includes `label_source: v3_rep_first_snippet_trap` on merged topics.

Regenerate merge after a new snippet-trap run:

```bash
python3 -m src.stage08_llm_labeling.openrouter_experiments.tools.merge_snippet_trap_into_stage09 \
  --panel-json data/stage08_benchmark/call73_snippet_trap_panel.json \
  --overrides-json results/stage08_llm_labeling/placeholder_v4_call73/snippet_trap/labels_pos_*_snippet_trap_rep_first_topics.json \
  --slim-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
  --review-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3_review_enriched.json
```

## Slim bundle (`topic_metadata_v3.json`)

- `label`, `scene_summary`, `keywords`, `snippets`
- `content_type`, `is_noise`, `exclude_from_axes`
- `sexual_explicitness`, `sexual_function`, `consent_status`

Deprecated fields (`register`, `subgenre_hints`, `axis_hint`) are derived in Stage09 via `v3_derived_fields.py`.

## Review bundle (`topic_metadata_v3_review_enriched.json`)

Adds `representations` (KeyBERT, MMR, POS, Main), `all_keywords`, and `rationale` for manual label QA. Not required for taxonomy mapping.

## Run Stage09

```bash
python3 -m src.stage09_category_mapping.stage1_theory_driven_categories.scripts.zeroshot_taxonomy_openrouter \
  --labels-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
  --output-json results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call73/taxonomy_mappings.json \
  --prompt-version v2 \
  --no-snippets
```

Regenerate slim export from review bundle:

```bash
python3 -m src.stage08_llm_labeling.openrouter_experiments.tools.export_stage09_topic_metadata \
  --input-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3_review_enriched.json
```
