# Stage08 snippet-trap relabel decision (call 73)

**Date:** 2026-06-30  
**Status:** Adopted — targeted `v3_rep_first` relabel; **production prompt unchanged**

## Problem

`v3_topic_labeling` (snippets-first) labels ~79 topics by paraphrasing the blandest representative snippet — especially future-tense promise clusters (`I'll…`, `we'll…`) — while KeyBERT/MMR/POS keywords (`confessed`, `weapons`, `session`, `threats`, …) describe a broader or heavier shared thread.

Example: Topic 6 was labeled **Plans to Meet Tomorrow** from the barn-scheduling snippet; POS/MMR pointed to **resigned confession / return**.

## Prompt experiment: `v3_rep_first`

Added sibling prompt `v3_rep_first` (keyword thread first; snippets ground the beat):

- `src/stage08_llm_labeling/prompts/v3_rep_first.py`
- `configs/stage08_labeling_rep_first.yaml`
- Evidence blocks in `prompts/blocks/evidence_hierarchy_rep_first.py`, `few_shots_rep_first.py`

## Gold-30 regression (2026-06-30)

| Metric | `v3_topic_labeling` | `v3_rep_first` |
|--------|---------------------|----------------|
| Topics with issues | 19/30 | **17/30** |
| Mean label overlap | 0.451 | **0.502** |
| Sexual function agreement | — | **86.7%** |
| Routing agreement | — | **100%** |

Snippet-trap fixes confirmed on Topics **0, 4, 6, 149** (and partial on **30, 225**).  
Regression example: Topic **248** — rep-first drifted to generic “Muffled Noises” vs gold “Overheard Pleasure Sounds”.

## Decision: do **not** switch whole production prompt

**Keep `configs/stage08_labeling.yaml` → `v3_topic_labeling` for the full 148-topic corpus.**

Rationale:

1. Snippets-first still wins on concrete intimacy beats and discourse/noise routing on the gold panel.
2. Keyword-first fixes polysemous glue clusters but can under-read snippet-grounded sexual beats (T248).
3. Cheaper to relabel a bounded **79-topic snippet-trap panel** than to re-run and re-QA all 322 labels.

## Adopted workflow

1. **Panel:** [`data/stage08_benchmark/call73_snippet_trap_panel.json`](../../data/stage08_benchmark/call73_snippet_trap_panel.json) (79 topics)
2. **Relabel:** `scripts/run_stage08_snippet_trap_relabel.sh` → `v3_rep_first`, output suffix `snippet_trap_rep_first`
3. **Compare:** [`stage08_snippet_trap_rep_first_comparison_call73.csv`](stage08_snippet_trap_rep_first_comparison_call73.csv)
4. **Apply:** merge rep-first labels for panel topics into Stage09 input / topic metadata when building the next taxonomy pass (production JSON remains source of truth until merge)

## Relabel results (2026-06-30)

- **79 topics** labeled with `v3_rep_first` (~14 min, ~$1.75 API)
- **76/79 labels changed** vs production `v3_topic_labeling`
- **Unchanged:** Topics 20, 113, 302 (both prompts agreed)
- **Key fixes:** T6 → Resigned Promise to Return; T0 → Hesitant Arrival at The Entrance; T149 → Cleaning Up After A Mess; T30 → Drinking With Reluctant Enthusiasm (cites `threats` in rationale)

Output: `results/stage08_llm_labeling/placeholder_v4_call73/production/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_rep_first_snippet_trap_rep_first_topics.json`


| Artifact | Path |
|----------|------|
| Production labels | `results/stage08_llm_labeling/placeholder_v4_call73/production/labels_pos_*_v3_topic_labeling.json` |
| Snippet-trap relabel | `results/stage08_llm_labeling/placeholder_v4_call73/production/labels_pos_*_snippet_trap_rep_first*.json` |
| Gold rep-first run | `results/stage08_llm_labeling/gold_regression/gold30_rep_first_report_20260630_221424.csv` |
| A/B script | `scripts/run_stage08_gold_regression_rep_first.sh` |

## Next steps

- [x] Merge snippet-trap rep-first labels into `stage09_input/topic_metadata_v3.json` for the 79 panel topics (2026-06-30)
- [ ] Spot-check relabel diff CSV for over-keyworded labels (POS dumps, missed sexual snippets)
- [ ] Optional: add automatic snippet-trap detector to Stage08 QA for future runs
