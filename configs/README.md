# Configuration files

YAML configs grouped by pipeline stage. **`paths.yaml`** at repo root holds shared data paths (v3 corpus).

## Active layout

| Folder | Purpose |
|--------|---------|
| [`call73/`](call73/) | Frozen placeholder v4 BO call 73 bundle + post-hoc rules |
| [`stage03/`](stage03/) | BERTopic BO tuning (v3 + v4 granular + final call73) |
| [`stage04/`](stage04/) | Eval-select weights + selection notebook paths |
| [`stage06/`](stage06/) | Character-name cleaning |
| [`stage07/`](stage07/) | Topic quality audit thresholds |
| [`stage08/`](stage08/) | LLM labeling, lexicon, gold subsets, 08a adjudication |
| [`stage09/`](stage09/) | Taxonomy v2 + theory-aligned index schema |
| [`legacy/`](legacy/) | Superseded v2 pipeline and one-off pilots — not used for current v3/call73 work |

## Common entry points

```bash
# Stage03 BO (v3 English corpus)
python -m src.stage03_train.cli tune --config configs/stage03/train_v3.yaml --run-id <id>

# Stage03 final fit (call 73 winner)
python -m src.stage05_final_fit.cli infer-corpus \
  --config configs/stage03/train_v4_l12_final_call73.yaml ...

# Stage08 production labeling
python -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config configs/stage08/stage08_labeling.yaml

# Frozen call 73 analysis anchor
configs/call73/placeholder_v4_frozen_call73.yaml
```

Cross-references inside YAML use full paths from repo root (e.g. `paths_config: configs/stage03/paths_stage03_fit_v3.yaml`).

Run helpers: [`scripts/README.md`](../scripts/README.md). Tests: [`tests/README.md`](../tests/README.md).
