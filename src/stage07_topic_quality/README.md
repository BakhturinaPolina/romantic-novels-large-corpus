# Stage 07: Topic Quality Analysis

Deterministic, non-LLM audit to flag technically weak/noisy topics before expensive labeling.

## Philosophy

Stage 07 answers only: **is this topic too weak/noisy to spend LLM money on?**

It does **not** assign romance themes, subgenre labels, or axis categories. Those belong to Stage 08B+.

## Pipeline hierarchy

```text
Stage 07A — Deterministic multi-representation audit
Stage 07B — Manual review artifacts (CSV + JSONL)
Stage 08A — LLM quality adjudication (soft-review topics only)
Stage 08B — Descriptive topic labeling
```

## Usage

```bash
bash scripts/stage07/run_stage07_placeholder_v4_models.sh
bash scripts/stage08/run_stage08a_quality_adjudication.sh
# then Stage 08B labeling with configs/stage08/stage08_labeling.yaml
```

## Config

- [`configs/stage07/stage07_topic_quality.yaml`](../../configs/stage07/stage07_topic_quality.yaml) — thresholds, representation list
- [`configs/call73/topic_posthoc_rules.yaml`](../../configs/call73/topic_posthoc_rules.yaml) — hard/soft posthoc rules

## Outputs (per call)

| File | Description |
|------|-------------|
| `stage07_topic_quality_audit.csv` | Full metrics + snippets + routing |
| `stage07_noise_candidates.csv` | Hard-exclude + soft-review topics |
| `stage07_manual_review_packet.jsonl` | One JSON object per review topic |
| `stage07_manual_decisions.csv` | Hand-editable decision template |
| `topic_quality_placeholder_v4_call{N}.csv` | Legacy alias of audit CSV |

## Key columns

Per representation (`Main`, `KeyBERT`, `MMR`, `POS`):

- `{Rep}_words`, `{Rep}_n_words`, `{Rep}_n_unique_words`
- `{Rep}_n_content_pos` — NOUN/VERB/ADJ keyword count
- `{Rep}_coherence_c_v` — Gensim c_v per topic
- `{Rep}_diversity_simple` — `n_unique / n_words` (redundancy flag)

Routing:

- `hard_exclude_candidate` — obvious garbage (publisher, multilingual, empty reps, etc.)
- `soft_review_candidate` — uncertain; send to Stage 08A
- `recommended_next_step` — `exclude_before_llm` | `stage08_quality_adjudication` | `stage08_labeling`

## Module structure

| File | Purpose |
|------|---------|
| `main.py` | CLI entrypoint |
| `config.py` | Load stage07_topic_quality.yaml |
| `topic_quality_analysis.py` | Metrics, flags, routing |
| `export_audit.py` | Write 07B artifacts |
