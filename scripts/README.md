# Scripts

Bash wrappers and small Python helpers, grouped by pipeline stage. Prefer these over long copy-paste command blocks.

## Layout

| Folder | Purpose |
|--------|---------|
| [`bundle/`](bundle/) | `make_transfer_bundle.sh` — ship Stage03 to remote machines |
| [`stage03/`](stage03/) | BO tuning, v3 embed, v4 granular phases, call73 full-corpus infer |
| [`stage06/`](stage06/) | Topic exploration refresh + character-name cleaning |
| [`stage07/`](stage07/) | Topic quality audit batch |
| [`stage08/`](stage08/) | LLM labeling, prompt sweeps, gold regression, snippet-trap relabel |
| [`data/`](data/) | Corpus prep utilities (v3 English filter) |
| [`legacy/`](legacy/) | Superseded pilots and one-off experiments |

## Common entry points

```bash
# Transfer bundle
bash scripts/bundle/make_transfer_bundle.sh

# Remote / Docker Stage03
./scripts/stage03/run_v3_remote_model.sh mpnet encode
./scripts/stage03/run_v4_granular_remote.sh mpnet phase1

# Placeholder v4 call 73 downstream
bash scripts/stage06/run_stage06_placeholder_v4_call.sh 73
bash scripts/stage07/run_stage07_placeholder_v4_models.sh
bash scripts/stage08/run_stage08_placeholder_v4_call.sh 73

# Stage08 snippet-trap panel
bash scripts/stage08/run_stage08_snippet_trap_relabel.sh
```

Transfer bundles flatten remote helpers to `./scripts/run_v3_remote_model.sh` at bundle root (see `bundle/make_transfer_bundle.sh`).
