# Stage 08: LLM-Based Topic Labeling

## Overview

Stage 08 generates interpretable labels for BERTopic topics via OpenRouter. Production uses **`v3_topic_labeling`**: snippets-first evidence, all keyword representations (KeyBERT, MMR, POS, Main), character-name rules, and v3 sexual-precision JSON fields — without Stage09 category taxonomy.

**A/B variant:** **`v3_rep_first`** — keyword thread (ALL KEYWORDS + KeyBERT + MMR + POS) defines the label; snippets and Main ground/polish the beat. Use when snippets surface bland "I'll…" glue but alt-reps show a richer shared theme. Config: [`configs/stage08/stage08_labeling_rep_first.yaml`](../../configs/stage08/stage08_labeling_rep_first.yaml).

## Production defaults

See [`configs/stage08/stage08_labeling.yaml`](../../configs/stage08/stage08_labeling.yaml):

| Setting | Value |
|---------|-------|
| Prompt | `v3_topic_labeling` |
| Model | `anthropic/claude-sonnet-4.6` |
| Temperature | 0.05 |
| Max tokens | 350 |
| Pipeline | Stage07 → Stage08A (adjudication) → Stage08B (labeling) |

## Run labeling

```bash
scripts/stage08/run_stage08_placeholder_v4_call.sh
```

Or directly:

```bash
python -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config configs/stage08/stage08_labeling.yaml
```

## Gold regression (30 topics)

Before a full-corpus relabel, run the golden panel:

```bash
scripts/stage08/run_stage08_gold_regression.sh
```

Gold expectations:
- Labeling: [`golden/call73_gold_30.yaml`](golden/call73_gold_30.yaml)
- Categorization: [`golden/call73_gold_30_categorization.yaml`](golden/call73_gold_30_categorization.yaml)

28 intimacy/sexual topics + T14 publisher noise. Character names are ignored in labeling.

## Prompt layout

```
prompts/
  v3_topic_labeling.py      # production (snippets-first)
  v3_rep_first.py           # A/B (keyword-thread-first)
  blocks/                   # composable sections
  adjudication/             # Stage08A
  legacy/                   # v1, v2 sweeps, full taxonomy (repro only)
  schema_v3.json
```

Run rep-first labeling:

```bash
python -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config configs/stage08/stage08_labeling_rep_first.yaml
```

## JSON output (v3 slim)

```json
{
  "label": "Condom And Lube Preparation",
  "scene_summary": "A couple prepares condoms and lubricant from a bedside drawer before sex.",
  "content_type": "scene",
  "exclude_from_axes": false,
  "sexual_explicitness": "explicit",
  "sexual_function": "contraception_preparation",
  "consent_status": "consensual_implied",
  "is_noise": false,
  "rationale": "..."
}
```

Stage09 derives `register`, `subgenre_hints`, and `axis_hint` from these fields via [`v3_derived_fields.py`](v3_derived_fields.py).

## Key modules

- [`labeling_pipeline.py`](labeling_pipeline.py) — prompt build, validation, normalization
- [`generate_labels.py`](generate_labels.py) — topic/representation extraction
- [`openrouter_experiments/core/main_openrouter.py`](openrouter_experiments/core/main_openrouter.py) — CLI
- [`openrouter_experiments/tools/validate_label_quality.py`](openrouter_experiments/tools/validate_label_quality.py) — gold + hallucination checks

Legacy prompts (`v1`, `v2_*` sweeps) remain importable via `prompts/loader.py` for sweep reproducibility.
