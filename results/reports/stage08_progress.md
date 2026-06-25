# Stage08 labeling progress (call 73)

**Last updated:** 2026-06-25 (auto-maintained)  
**Frozen model:** `placeholder_v4_models/final_compare/call_73`  
**Config:** [`configs/stage08_labeling.yaml`](../../configs/stage08_labeling.yaml)  
**Output dir:** [`results/stage08_llm_labeling/placeholder_v4_call73/`](../stage08_llm_labeling/placeholder_v4_call73/)

## Pipeline status

| Step | Status | Notes |
|------|--------|-------|
| Stage06 topics JSON | Done | 322 POS topics in JSON stream |
| Stage07 quality CSV | Done | 330 hints loaded (advisory only) |
| Stage08 v2 prompts + runners | Done | All topics LLM-labeled; no synthetic placeholders |
| Representative snippets | Done | CSV fallback from compare-fit `representative_docs.csv` (enriched model omits `representative_docs_`) |
| Model shootout (5-topic pilots) | **Done** | 14 models + 2×20-topic runs; **7 top picks re-run with snippets** (2026-06-25) |
| Full 330-topic production run | **Not started** | Pick model after shootout |
| Stage09 pre-router | Not started | |

## Design decisions (locked)

- Label **all** topics (~330); Stage07 `exclude_from_axes` is prompt hint only
- No `[NOISE:rule_id]` synthetic labels
- Default rate limit: **4s** between API calls
- `--no-integrate` for JSON-only outputs during pilots

## Model comparison pilots (5 topics: 0–4)

**Baseline quality target:** `mistralai/mistral-nemo` or `claude-opus-4.6`  
**Run:** `bash scripts/run_stage08_placeholder_v4_call.sh 73 --limit-topics 5 --model-name <slug> --no-resume`

| Model | 5-top JSON | Pilot status | Quality note |
|-------|------------|--------------|--------------|
| `mistralai/mistral-nemo` | yes | **done** | **Best cost/quality**; natural labels |
| `mistralai/Mistral-Nemo-Instruct-2407` | 20-top only | done (20) | Similar to nemo; config default |
| `anthropic/claude-opus-4.6` | yes | **done** | Most polished; ~$0.17 / 5 topics |
| `anthropic/claude-sonnet-4.6` | yes | **done** | Strong; near-Opus quality |
| `google/gemini-3-flash-preview` | yes | **done** | Fast, natural labels |
| `google/gemini-2.5-flash-lite` | yes | **done** | Fast, decent |
| `openrouter/owl-alpha` | yes | **done** | Free; surprisingly good on 5-top |
| `anthropic/claude-opus-4.7` | yes | **done** | Similar to 4.6 |
| `anthropic/claude-opus-4.8` | yes | **done** | Similar to 4.6 |
| `deepseek/deepseek-v4-pro` | yes | **done** | Slow (~25s/topic); OK labels |
| `deepseek/deepseek-v4-flash` | yes (+20) | **done** | Keyword-chain risk; slow |
| `xiaomi/mimo-v2.5` | yes | **done** | Poor (`rear`, `moves`, `purse`) |
| `minimax/minimax-m3` | yes | **done** | Poor (raw keywords) |
| `z-ai/glm-5.2` | yes | **done** | Poor (`rear`, `plump`, `moves`) |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | yes | **done** | Poor + very slow |

**Batch 2 (9 models):** completed 2026-06-25 ~02:25, exit 0, ~14 min total.

**Snippet rerun (7 models, with CSV fallback):** completed 2026-06-25 02:28–02:38, exit 0, ~10 min. All runs used `snippets=3` per topic. Sample topic-0 labels: nemo *Hesitant Bedroom Entrance*, sonnet *Doorway Hesitation Before Departure*, gemini *Hesitation at The Doorway*, owl *Doorway Hesitation*, opus 4.6–4.8 all *Hesitant Doorway Pause* / *Hesitation in Doorway*. Log: `logs/stage08_snippet_rerun_20260625_022852.log`.

## Cost / ETA reference (330 topics)

| Tier | Model | Est. cost | Est. time |
|------|-------|-----------|-----------|
| Production pick | `mistralai/mistral-nemo` | **~$0.03** | **~33 min** |
| Fast alt | `gemini-2.5-flash-lite` | ~$0.20 | ~35 min |
| Quality pick | `claude-opus-4.6` | ~$11.50 | ~59 min |

See chat log for full 15-model table.

## Code / git

| Item | Status |
|------|--------|
| `scripts/run_stage08_placeholder_v4_call.sh` | Done |
| v2 prompts + natural-label voice | Done (uncommitted prompt tweaks) |
| `jsonschema` in venv | Installed locally |
| `--no-resume` vs yaml `resume: true` | **Fixed** — YAML no longer overrides explicit CLI |

## Next actions

1. Choose production model → update `configs/stage08_labeling.yaml` (`mistralai/mistral-nemo` still best value)
2. Run full 330: `bash scripts/run_stage08_placeholder_v4_call.sh 73` (drop `--no-integrate` when ready)
3. Stage09 pre-router (minimal)

## Logs

Latest runs: `logs/stage08_llm_labeling_*.log`
