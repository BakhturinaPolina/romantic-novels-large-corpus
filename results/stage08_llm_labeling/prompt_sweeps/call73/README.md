# Stage08 prompt sweeps — call 73

Historical **v2 OVAT** prompt experiments (20-topic pilot panel, temp=0). Production labeling uses **`v3_topic_labeling`**; see [`placeholder_v4_call73/README.md`](../../placeholder_v4_call73/README.md).

## Layout

| Folder | Contents |
|--------|----------|
| [`phase_0/`](phase_0/) | Temperature ablation (D2a temp=0.35, D2b temp=0) |
| [`phase_a/`](phase_a/) | Structural OVAT (S1–S7: snippets-first, snippet count, keywords, stage07, few-shots, field order) |
| [`phase_b/`](phase_b/) | Conceptual OVAT (C1–C7: discourse, noise, snippet grounding, …) |
| [`phase_c/`](phase_c/) | 30-topic validation runs (phase_c full panel) |
| [`character_names/`](character_names/) | C8 vs v2_s1 A/B on 21-topic name panel |
| [`v3_rep_first/`](v3_rep_first/) | **2026-06-30** snippet-trap A/B (`v3_rep_first` vs production); merged into `stage09_input` |
| [`scores/`](scores/) | Aggregated sweep score summaries |

## v3_rep_first snippet-trap (not a v2 sweep)

Same workflow as production: gold-30 A/B + 79-topic panel relabel + merge into Stage09 input. **Did not replace** production prompt — see [`results/reports/stage08/stage08_snippet_trap_rep_first_decision_call73.md`](../../../reports/stage08/stage08_snippet_trap_rep_first_decision_call73.md).

| Artifact | Path |
|----------|------|
| Panel relabel (79 topics) | `v3_rep_first/labels_pos_*_snippet_trap_rep_first_topics.json` |
| Gold-30 A/B | `v3_rep_first/labels_pos_*_gold30_regression_v3_rep_first_topics.json` |
| Merge log | `v3_rep_first/snippet_trap_merge_log.json` |
| Merged Stage09 input | [`placeholder_v4_call73/stage09_input/topic_metadata_v3.json`](../../placeholder_v4_call73/stage09_input/topic_metadata_v3.json) |

Re-run panel relabel:

```bash
scripts/stage08/run_stage08_snippet_trap_relabel.sh
# copies refreshed artifacts here via post-step (see script)
```

## Score historical sweeps

```bash
python scripts/stage08/score_stage08_prompt_sweep.py --sweep-dir results/stage08_llm_labeling/prompt_sweeps/call73
```

## Run new OVAT sweeps

```bash
bash scripts/stage08/run_stage08_prompt_sweep_call73.sh phase_a   # -> phase_a/
bash scripts/stage08/run_stage08_prompt_sweep_call73.sh phase_b   # -> phase_b/
bash scripts/stage08/run_stage08_prompt_sweep_call73.sh phase_c8  # -> character_names/
```

Design doc: [`results/reports/stage08/stage08_prompting_research_design_call73.md`](../../../reports/stage08/stage08_prompting_research_design_call73.md)
