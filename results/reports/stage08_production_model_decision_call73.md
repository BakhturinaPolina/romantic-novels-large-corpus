# Stage08 production LLM — call 73 decision

**Date:** 2026-06-25  
**Status:** **Locked**  
**Config:** [`configs/stage08_labeling.yaml`](../../configs/stage08_labeling.yaml)

## Chosen model

**`anthropic/claude-sonnet-4.6`** via OpenRouter (`$3` / `$15` per 1M input/output tokens).

## Rationale

After snippet-aware pilots (5- and 20-topic) comparing sonnet, opus-4.6, mistral-nemo, gemini, and others:

| Criterion | Sonnet 4.6 | Opus 4.6 | Mistral Nemo |
|-----------|:----------:|:--------:|:------------:|
| Snippet grounding (T0–6) | **7/7** | 5/7 | 4/7 (T0 bedroom error) |
| 20-topic head-to-head vs Opus | **9 wins / 5 ties / 6 opus** | Strong discourse taxonomy | Not production-ready |
| Est. full 330-topic cost | **$6.11** | $10.22 | $0.03 |
| Est. wall time (330) | ~45 min | ~59 min | ~33 min |

**Why not Opus:** ~40% more cost for marginal gains — better `content_type` on abstract topics (T5–T9) and T12 scent rescue, but sonnet wins on early romance beats and keyword-trap resistance.

**Why not Mistral Nemo:** ~200× cheaper but systematic snippet misreads (e.g. topic 0 “Bedroom Entrance” on both 5- and 20-topic runs).

## Evidence artifacts

| Run | Path |
|-----|------|
| 5-topic snippet rerun | `results/stage08_llm_labeling/placeholder_v4_call73/labels_pos_openrouter_*_limit5.json` |
| 20-topic measured cost | `labels_pos_openrouter_anthropic_claude-sonnet-4.6_*_limit20.json` (and opus/nemo siblings) |
| Progress + comparison tables | [`stage08_progress.md`](stage08_progress.md) |
| Logs | `logs/stage08_limit20_snippets_*.log` |

## Production run

```bash
bash scripts/run_stage08_placeholder_v4_call.sh 73
```

Uses yaml defaults: v2 prompts, 6 snippets (CSV fallback), 4s rate limit, `resume: true`. Drop `--no-integrate` from the wrapper when labels should be written into the enriched BERTopic model.
