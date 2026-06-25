# Stage08 labeling progress (call 73)

**Last updated:** 2026-06-25  
**Production LLM:** **`anthropic/claude-sonnet-4.6`** — see [`stage08_production_model_decision_call73.md`](stage08_production_model_decision_call73.md)  
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
| Model shootout (5-topic pilots) | **Done** | 14 models; **7 top picks re-run with snippets** (2026-06-25) |
| Model shootout (20-topic pilots) | **Done** | opus-4.6, sonnet-4.6, mistral-nemo (snippet-aware, 2026-06-25) |
| Full 330-topic production run | **Not started** | Model locked: **claude-sonnet-4.6** (~$6.11 est.) |
| Stage09 pre-router | Not started | |

## Design decisions (locked)

- Label **all** topics (~330); Stage07 `exclude_from_axes` is prompt hint only
- No `[NOISE:rule_id]` synthetic labels
- Default rate limit: **4s** between API calls
- `--no-integrate` for JSON-only outputs during pilots

## Snippet-aware quality comparison (5 topics: 0–4)

**Ground truth from snippets:** T0 = ride/taxi travel transition (not bedroom); T1 = tender temple/lip kisses; T2 = forehead/neck closeness; T3 = interior love/hate swing; T4 = phone-call follow-up.

### Labels by model

| Topic | mistral-nemo | claude-sonnet-4.6 | gemini-3-flash | owl-alpha | opus-4.6 | opus-4.7 | opus-4.8 |
|-------|--------------|-------------------|----------------|-----------|----------|----------|----------|
| **0** | Hesitant **Bedroom** Entrance ❌ | Doorway Hesitation Before Departure ✓ | Hesitation at The Doorway | Doorway Hesitation | Hesitant Doorway Pause | Hesitating Near Doorway | Hesitation in Doorway |
| **1** | Hesitant **Forearm** Caress ❌ | Tender Kiss on Lips ✓ | Tender Kiss and Physical Touch | Tentative Touch and Kissing | Gentle Lean-in Kiss | Tentative Lean-in Kiss | Tentative Touch Before Kiss |
| **2** | Anticipatory Forehead Touch | Close Physical Proximity and Touch | Close Physical Proximity and Anticipation | Forehead Touch and Neck Caress | Close Physical Anticipation | Anticipatory Touch at Waist | Anticipatory Skin Caress |
| **3** | **Argument** About Feelings ❌ | Conflicted Feelings Toward Loved One ✓ | Conflicting Feelings and Affection | Conflicted Affection and Resentment | Internal Fears and Choices (discourse) | Inner Conflict Over Choices | Conflicted Feelings and Choices |
| **4** | Unclear Relationship Feelings | Phone Call Follow-Up ✓ | Phone Call Logistics and Instructions | Phone Calls and Contact Attempts | Phone Calls and Practical Errands | Phone Call Follow-Up Plans | Phone Call Follow-Up |

### Tier ranking (snippet-aware pilots)

| Tier | Model | Notes |
|------|-------|-------|
| **1** | `anthropic/claude-sonnet-4.6` | Best snippet grounding; richest metadata; no schema errors |
| **1** | `anthropic/claude-opus-4.6` | Tied best accuracy; good `discourse` on T3 |
| **2** | `google/gemini-3-flash-preview` | Solid; minor keyword drift on T0 summary |
| **2** | `mistralai/mistral-nemo` | Best value; T0 bedroom hallucination + T1 label/summary mismatch |
| **3** | `openrouter/owl-alpha` | Free; keyword-chain risk on T0/T1 summaries (excluded from 20-top batch) |
| **3** | `anthropic/claude-opus-4.7` | Near 4.6; wrongly sets `exclude_from_axes` on T3 |
| **4** | `anthropic/claude-opus-4.8` | Over-excludes T3–4; no gain over 4.6 |

### Cross-cutting scores

| Dimension | nemo | sonnet | gemini | owl | opus 4.6 |
|-----------|:----:|:------:|:------:|:---:|:--------:|
| Snippet grounding | Fair | **Excellent** | Good | Mixed | **Excellent** |
| Keyword-chain resistance | Poor | **Strong** | Good | Poor | **Strong** |
| Label ↔ summary consistency | Broken T1 | ✓ | ✓ | Mostly | ✓ |
| `content_type` accuracy | all scene | all scene | all scene | all scene | T3 discourse ✓ |

**Production picks:** value → `mistralai/mistral-nemo`; quality/cost → `anthropic/claude-sonnet-4.6`; max polish → `anthropic/claude-opus-4.6`.

## Model comparison pilots (all models)

**Run:** `bash scripts/run_stage08_placeholder_v4_call.sh 73 --limit-topics N --model-name <slug> --no-resume`

| Model | 5-top | 20-top (snippets) | Quality note |
|-------|-------|-------------------|--------------|
| `mistralai/mistral-nemo` | yes | **done** | Best cost/quality; T0 still “Bedroom” on 20-top |
| `anthropic/claude-opus-4.6` | yes | **done** | Most polished; T0 “Doorway Arrival” on 20-top |
| `anthropic/claude-sonnet-4.6` | yes | **done** | Strong; T0 correct on 20-top |
| `google/gemini-3-flash-preview` | yes | — | Fast, natural |
| `openrouter/owl-alpha` | yes | — | Free; excluded from 20-top batch |
| Others (batch 2) | yes | — | See logs |

**Snippet rerun (7 models):** 2026-06-25 02:28–02:38, exit 0. Log: `logs/stage08_snippet_rerun_20260625_022852.log`.

## Cost / ETA reference

OpenRouter **list prices** (Jun 2026, per 1M tokens): opus-4.6 $5/$25; sonnet-4.6 $3/$15; mistral-nemo $0.02/$0.03.  
CLI prints measured token usage + extrapolated 330-topic cost after each run.

### Measured (20 topics, snippets, 2026-06-25)

| Model | Prompt / completion tokens | 20-top cost | Per topic | **Est. 330-top** | Wall time (20) |
|-------|---------------------------|-------------|-----------|------------------|----------------|
| `anthropic/claude-opus-4.6` | 99,967 / 4,793 | **$0.62** | $0.031 | **$10.22** | ~4 min |
| `anthropic/claude-sonnet-4.6` | 100,092 / 4,673 | **$0.37** | $0.019 | **$6.11** | ~4 min |
| `mistralai/mistral-nemo` | 92,431 / 2,711 | **$0.002** | $0.0001 | **$0.03** | ~3 min |

Log: `logs/stage08_limit20_snippets_*.log`  
JSONs: `labels_pos_openrouter_{opus-4.6,claude-sonnet-4.6,mistral-nemo}_*_limit20.json`

### Full-run ETA (330 topics, 4s rate limit)

| Model | Est. cost | Est. time |
|-------|-----------|-----------|
| `mistralai/mistral-nemo` | **$0.03** | ~33 min |
| `anthropic/claude-sonnet-4.6` | **$6.11** | ~45 min |
| `anthropic/claude-opus-4.6` | **$10.22** | ~59 min |

## Code / git

| Item | Status |
|------|--------|
| `scripts/run_stage08_placeholder_v4_call.sh` | Done |
| CSV snippet fallback + `--no-resume` fix | Done |
| Per-run API usage + cost estimate in CLI summary | Done |
| v2 prompts + natural-label voice | Done (uncommitted prompt tweaks) |

**Production model (locked 2026-06-25):** `anthropic/claude-sonnet-4.6` — [`stage08_production_model_decision_call73.md`](stage08_production_model_decision_call73.md).

## Next actions

1. Run full 330: `bash scripts/run_stage08_placeholder_v4_call.sh 73`
2. Stage09 pre-router (minimal)

## Logs

Latest runs: `logs/stage08_llm_labeling_*.log`, `logs/stage08_limit20_*.log`
