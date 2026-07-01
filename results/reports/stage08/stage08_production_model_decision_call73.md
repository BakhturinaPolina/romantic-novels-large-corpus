# Stage08 production LLM — call 73 decision

**Date:** 2026-06-25  
**Status:** **Model locked; prompt sweep in progress**  
**Config:** [`configs/stage08/stage08_labeling.yaml`](../../configs/stage08/stage08_labeling.yaml)

> **Update (2026-06-25):** Sonnet remains the production model. **Prompt locked:** `v2_s1_snippets_first` @ temp=0.0 (Phase C passed on 31-topic panel).

## Recommended path (default)

**`anthropic/claude-sonnet-4.6`** for the full ~330-topic run, then **manual review of ~10% discourse/noise topics**.

| Item | Detail |
|------|--------|
| Model | `anthropic/claude-sonnet-4.6` (yaml default) |
| Est. cost | **~$6.11** / 330 topics |
| Est. time | ~45 min (+ review) |
| Why | Best snippet grounding on romance beats; ~40% cheaper than Opus |

**Post-run QA (~10% manual review):** After the full JSON is written, spot-check topics flagged as hard cases — roughly the discourse / noise / paratext tail where Opus did better in the 20-topic pilot:

- `content_type` in `discourse`, `noise`, `paratext`
- `is_noise: true` or `exclude_from_axes: true` (model-assigned, not Stage07-only)
- Stage07 `posthoc_reason` hints (e.g. `publisher_boilerplate`, `character_name_cluster`)
- Sonnet-specific misses from pilots (e.g. T12 scent cluster called noise; abstract T5–T9)

At ~330 topics, expect **~30–35 labels** in this review queue (~10%). Fix labels in JSON (or re-run individual topics with `--limit-topics` + `--no-resume` on a subset) before Stage09.

## Premium path (if budget allows)

**`anthropic/claude-opus-4.6`** for the full run — skip or shrink manual review.

| Item | Detail |
|------|--------|
| Model | `anthropic/claude-opus-4.6` (`--model-name` override) |
| Est. cost | **~$10.22** / 330 topics |
| Est. time | ~59 min |
| Why | Stronger `content_type` / `exclude_from_axes` on abstract topics; rescues edge clusters (e.g. T12 scent) |

```bash
bash scripts/stage08/run_stage08_placeholder_v4_call.sh 73 \
  --model-name anthropic/claude-opus-4.6
```

Trade-off: +~$4 and +~15 min vs sonnet; marginal gains on core intimacy scenes (T0–T4), clearer wins on discourse taxonomy.

## Not chosen

| Model | Reason |
|-------|--------|
| `mistralai/mistral-nemo` | ~200× cheaper but systematic snippet misreads (T0 “Bedroom” on 5- and 20-topic runs) |
| `openrouter/owl-alpha` | Free pilots only; keyword-chain risk on summaries |

## Pilot summary (20 topics, snippets)

| Criterion | Sonnet 4.6 | Opus 4.6 |
|-----------|:----------:|:--------:|
| Snippet grounding (T0–6) | **7/7** | 5/7 |
| Head-to-head (20-top) | **9 wins**, 5 ties | 6 wins |
| Discourse / noise calibration | Weaker (e.g. T12 → noise) | **Stronger** |
| Measured 20-top cost | $0.37 | $0.62 |

## Evidence artifacts

| Run | Path |
|-----|------|
| Sonnet 20-top | `results/stage08_llm_labeling/placeholder_v4_call73/model_sweep/limit20/labels_pos_openrouter_anthropic_claude-sonnet-4.6_*_limit20.json` |
| Opus 20-top | `labels_pos_openrouter_anthropic_claude-opus-4.6_*_limit20.json` |
| Comparison tables | [`stage08_progress.md`](stage08_progress.md) |
| Logs | `logs/stage08_limit20_snippets_*.log` |

## Production commands

**Default (sonnet + manual review):**

```bash
bash scripts/stage08/run_stage08_placeholder_v4_call.sh 73
```

Uses yaml defaults: v2 prompts, 6 snippets (CSV fallback), 4s rate limit, `resume: true`. Drop `--no-integrate` from the wrapper when labels should be written into the enriched BERTopic model.

**Review filter (after run):** inspect JSON entries where `content_type` ∉ `{scene}` or `is_noise` is true; cross-check against Stage07 `quality_csv` posthoc flags.
