# Stage 11 — `src/stage11_refined_construct_analysis`

Shared evidence layer, Nemo spillover triage, Pass A/B/C hypothesis audits, master
annotation table, \(W_{tk}\)/\(W_{tkr}\) weights, and refined book-level analysis frame.

Stage 10 (`notebooks/07_analysis/`) remains the confirmatory taxonomy baseline.

## Run

```bash
# Offline / dry-run scaffold
STAGE11_DRY_RUN=1 bash scripts/stage11/run_pipeline.sh

# Live Nemo (requires OPENROUTER_API_KEY in .env)
bash scripts/stage11/run_pipeline.sh

# After audits: master + refined frame
.venv/bin/python src/stage11_refined_construct_analysis/pipeline/07_build_master_table.py
.venv/bin/python src/stage11_refined_construct_analysis/pipeline/08_build_refined_analysis_frame.py
```

Audit order: **H1 → H3 → H4** (reuses H3 `4.6`) **→ H2** → **H5 → H6**.

Config: [`configs/stage11/refined_constructs.yaml`](../../configs/stage11/refined_constructs.yaml).

Primary model: `mistralai/Mistral-Nemo-Instruct-2407` via OpenRouter.
