# Stage 08 gold regression (30 topics)

Labeling gold: `call73_gold_30.yaml` (natural labels + scene summaries).  
Categorization gold: `call73_gold_30_categorization.yaml` (sexual_function, consent, routing).

```bash
scripts/stage08/run_stage08_gold_regression.sh
```

Pass criteria:
- ≥80% label token overlap (per-topic threshold 0.35)
- ≥85% `sexual_function` agreement (categorization file)
- 100% routing on topic 14 (publisher noise)
- Zero genre clichés

`register`, `subgenre_hints`, and `axis_hint` are derived in Stage09 — not Stage08 LLM output.
