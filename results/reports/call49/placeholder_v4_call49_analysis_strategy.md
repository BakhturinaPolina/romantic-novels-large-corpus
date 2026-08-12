# Placeholder v4 call 49 — analysis strategy

**Status:** Taxonomy track complete (Stage06–08); full-corpus infer running.
**Date:** 2026-08-12
**Frozen model:** `placeholder_v4_models` / compare-fit **call 49** (`configs/call49/placeholder_v4_frozen_call49.yaml`)
**Full-corpus run_id:** `v4_l12_granular_final_call49`

## Why call 49

Relative to frozen call 73 (329 topics): call 49 has similar coherence (0.654 vs 0.657), more usable topics (~213 vs ~171), better document coverage in usable topics (~110k vs ~105k), and finer H1 sex/escalation splits. See `results/reports/stage04/granularity_four_models/README.md`.

## Pipeline status (2026-08-12)

| Stage | Status | Notes |
|-------|--------|-------|
| Stage05 compare-fit | **done** | 373 topics, c_v 0.635, diversity 0.809, outlier 0.693, stability std 3.56 pass |
| Stage05b holdout | **done** | 17.5M docs scored; `n_topics=0` / c_v=0 in metrics is the same soft-prob quirk as call 73 |
| Stage05 full-corpus infer | **running** (resumed) | Train partial ~19.1M/80M when disk filled; resumed after freeing space |
| Stage06 enrich | **done** | `model_compare_enriched/` + topics JSON |
| Stage06 name cleaning | **done** | 123 NER person tokens |
| Stage07 quality | **done** | 373 topics; hard=1; soft=170 |
| Stage08a adjudication | **done** | 170 packets: 147 pass / 21 exclude_noise / 2 manual_review |
| Stage08 production | **done** | **348 Sonnet labels** (`v3_topic_labeling`) |

### Stage08 label snapshot

- Explicit: 9 | Suggestive: 20 | Affection-only: 12 | None: 307
- Examples: *Straps Sliding Down Her Arms* (explicit), *Kissing With Tongue and Urgency* (explicit), *Cupping and Pinching Her Nipples* (explicit), *Ordering A Gown For Her* (none)

Labels file: `results/stage08_llm_labeling/placeholder_v4_call49/production/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_topic_labeling.json`

### Disk incident

Full disk at ~100% halted Stage08 flush (labels already written) and infer. Freed ~47G caches, then removed unused **MPNet** train_eval embedding cache (~279G) so infer could resume. Monitor:

```bash
df -h /
cat results/experiments/v4_l12_granular_final_call49/full_corpus_infer/sentence_topics_train.parquet.progress.json
tail -f logs/v4_call49_full_corpus_console.log
```

## Related artifacts

| Artifact | Path |
|----------|------|
| Freeze config | `configs/call49/placeholder_v4_frozen_call49.yaml` |
| Post-hoc rules | `configs/call49/topic_posthoc_rules.yaml` |
| Placeholder compare-fit | `results/experiments/placeholder_v4_models/final_compare/call_49/` |
| Full-corpus Stage05 | `results/experiments/v4_l12_granular_final_call49/` |
| Stage05b | `results/evaluation/v4_l12_granular_final_call49/call_49/` |
| Stage06 | `results/stage06_topic_exploration/placeholder_v4_call49/` |
| Name cleaning | `results/stage06_name_cleaning/placeholder_v4_call49/` |
| Stage07 | `results/stage07_topic_quality/placeholder_v4_call49/` |
| Stage08a | `results/stage08a_quality_adjudication/placeholder_v4_call49/` |
| Stage08 production | `results/stage08_llm_labeling/placeholder_v4_call49/production/` |

## Run book

```bash
# GPU overnight (Stage05 + 05b + full-corpus infer) — resumable
nohup ./scripts/stage03/run_v4_call49_full_corpus.sh \
  >> logs/v4_call49_full_corpus_console.log 2>&1 &

# Taxonomy track (already completed for call 49)
bash scripts/stage06/run_stage06_placeholder_v4_call.sh 49
bash scripts/stage06/run_character_name_cleaning.sh 49
CALLS=49 bash scripts/stage07/run_stage07_placeholder_v4_models.sh
.venv/bin/python -m src.stage08_llm_labeling.openrouter_experiments.core.run_quality_adjudication \
  --config configs/stage08/stage08a_quality_adjudication_call49.yaml
.venv/bin/python -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config configs/stage08/stage08_labeling_call49.yaml \
  --no-integrate
```

## Policy

- Accept ~70% outliers; do **not** run `reduce_outliers`.
- Stage08 model: `anthropic/claude-sonnet-4.6`, prompt `v3_topic_labeling`.
- Call 73 remains the prior labeled reference until Stage09 is re-run on call 49.
