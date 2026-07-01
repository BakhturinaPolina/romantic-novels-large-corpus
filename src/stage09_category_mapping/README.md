# Stage 09: Category mapping

Map Stage08 topic labels to theory-driven taxonomy categories, then optionally to Radway narrative functions for book-level analysis.

## Prerequisites

- **Stage08 topic metadata** — e.g. `results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json`
- **Taxonomy config** — `configs/stage09/romance_corpus_taxonomy_v2.yaml` (v2.1 leaves **2.5**, **7.4**)
- **OpenRouter API key** — for zero-shot classification (`OPENROUTER_API_KEY`)

## Two-stage pipeline

### Stage 1: Theory-driven taxonomy mapping

Map each topic to Romance Corpus Taxonomy v2 leaf categories using zero-shot LLM classification, pre-routing from Stage08 metadata, and domain heuristics.

| Component | Path |
|-----------|------|
| Runner | `stage1_theory_driven_categories/scripts/zeroshot_taxonomy_openrouter.py` |
| Taxonomy loader / heuristics | `stage1_theory_driven_categories/taxonomy_v2.py` |
| Prompts | `stage1_theory_driven_categories/prompts/` |
| Book aggregation | `stage1_theory_driven_categories/scripts/aggregate_taxonomy_by_book.py` |

```bash
python -m src.stage09_category_mapping.stage1_theory_driven_categories.scripts.zeroshot_taxonomy_openrouter \
  --labels-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
  --output-json results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call73/taxonomy_mappings.json \
  --prompt-version v2 \
  --no-snippets
```

Details: [`stage1_theory_driven_categories/README.md`](stage1_theory_driven_categories/README.md)

### Stage 2: Radway narrative functions

Map topics to Radway's 13 narrative functions (R1–R13), merging into the Stage 1 taxonomy JSON.

| Component | Path |
|-----------|------|
| Runner | `stage2_radway_functions/scripts/zeroshot_radway_openrouter.py` |
| Model attach | `stage2_radway_functions/scripts/update_model_with_radway.py` |

```bash
python -m src.stage09_category_mapping.stage2_radway_functions.scripts.zeroshot_radway_openrouter \
  --taxonomy-json results/stage09_category_mapping/stage1_theory_driven_categories/taxonomy_mappings.json \
  --output-json results/stage09_category_mapping/stage2_radway_functions/taxonomy_with_radway.json
```

Details: [`stage2_radway_functions/README.md`](stage2_radway_functions/README.md)

## Directory layout

```
stage09_category_mapping/
├── README.md
├── stage1_theory_driven_categories/
│   ├── taxonomy_v2.py
│   ├── prompts/
│   └── scripts/
└── stage2_radway_functions/
    └── scripts/
```

## Downstream

Stage 10 book aggregation reads Stage 1 book-level proportions (`book_category_proportions.parquet`) and composite indices from `configs/stage09/theory_aligned_index_schema.yaml`.

## Legacy

Hierarchical “natural cluster” experiments (`BERTopic.reduce_topics`, ANOVA on meta-topics) were **not reliable** on this corpus (~300 fine-grained topics, high outlier rate, discourse-heavy clusters). Code archived under [`src/legacy/stage09_natural_clusters/`](../../legacy/stage09_natural_clusters/README.md) — **not used** in the active pipeline.

## References

- Radway, J. (1984). *Reading the Romance*
- BERTopic: https://maartengr.github.io/BERTopic/
