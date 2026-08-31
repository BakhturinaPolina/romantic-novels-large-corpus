# Stage 11 — Refined Construct Analysis

Measurement-correction / post-hoc validation for hypotheses **H1–H6**.

| Stage | Role |
| --- | --- |
| **09** | Descriptive taxonomy |
| **10** (`notebooks/07_analysis/`) | Confirmatory taxonomy baseline — **do not edit in place** |
| **11** (this folder) | Function-specific refined measures |

Prompts are hypothesis-specific (not one giant multi-criterion prompt). Shared evidence packets are built once; Pass A (lexical) / B (contextual) / C (adjudication) run via cheap OpenRouter `mistralai/Mistral-Nemo-Instruct-2407`. See [ACL 2024 long.516](https://aclanthology.org/2024.acl-long.516/) and [POSIX / Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.852/) for why narrow prompts matter.

## Notebooks (run in order)

| Notebook | Purpose |
| --- | --- |
| `00_refinement_foundations` | Freeze mappings, pools, Stage 10 δ, integrity (H2=10; 7.2=12) |
| `01`–`06` | H1–H6 **human close-reading** audits: topic id + label, novel sentences from evidence packets, Pass A/B/C rationales (saved artifacts only; no API). Patterned after Stage 10 `07_qualitative_triangulation`. |
| `07_refined_construct_dictionary` | Freeze \(W_{tk}\) / \(W_{tkr}\) |
| `08_refined_axes_validity` | Coverage / coherence before outcomes |
| `09_refined_hypothesis_tests` | Re-run H1–H6 with Stage 10 stats machinery |
| `10_contextual_validation` | Unblind cells |
| `11_refined_robustness` | OLD \| STRICT \| WEIGHTED panel |
| `12_exploratory_security_care_appearance` | **Exploratory only** — nested security/care/appearance definitions (does not alter H1–H6) |
| `13_final_statistical_tests` | **Confirmatory final** — only reportable H1–H6 inferential results (author-cluster CIs; do not redefine constructs after running) |
| `14_exploratory_presentation_results` | **Exploratory presentation** — reuses NB12 tables; adds thematic richness, waterfall, dose-response, residual Goodreads, genre/era heatmap, examples (does not alter NB13 verdicts) |

Edit `_src/*.py`, then:

```bash
.venv/bin/python scripts/stage11/percent_to_notebook.py notebooks/08_refined_construct_analysis/_src/*.py
```

## Pipeline (API outside notebooks)

```bash
# Full chain (needs OPENROUTER_API_KEY for live audits)
bash scripts/stage11/run_pipeline.sh

# After audits exist: master weights + refined frame
.venv/bin/python src/stage11_refined_construct_analysis/pipeline/07_build_master_table.py
.venv/bin/python src/stage11_refined_construct_analysis/pipeline/08_build_refined_analysis_frame.py
```

Dry-run: `STAGE11_DRY_RUN=1 bash scripts/stage11/run_pipeline.sh`

## Integrity traps (auto-checked)

| Check | Expectation |
| --- | --- |
| H2 pool (`4.5` ∪ `5.3a` ∪ `8.3a`) | **10** topics (not the older 11) |
| Leaf `7.2` | **12** topics (topic 91 → `7.1`) |
| `2.4`, `6.1a`, `6.7` | empty / unmeasurable |

## Blinding

- Rating cells stored as `CELL_A`…`CELL_D`; sealed key unblinds in notebook 10 only.
- Taxonomy / Stage09 rationale hidden until Pass C.
- Narrative position/tertile is visible for H2/H6 Pass B.

Outputs: `results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/`.

## Human-review pack (all topics)

Shared PDF + markdown with **every** audited topic across H1–H6 (labels, old taxonomy leaf, new codes, novel sentences, Pass A/B/C rationales):

```bash
.venv/bin/python scripts/stage11/export_human_review_pdf.py
```

Writes under `results/stage11_refined_construct_analysis/<run_id>/human_review/`:

- `stage11_human_review_all_topics.pdf`
- `stage11_human_review_all_topics.md`
- `stage11_human_review_h{1..6}.md`

### Landscape survivors (Stage10 NB01 gate)

38 topics with `|Cliff's delta| ≥ 0.11` and bootstrap CI excluding zero:

```bash
.venv/bin/python scripts/stage11/export_landscape_survivors_review_pdf.py
```

Writes `stage10_landscape_survivors_review.pdf` / `.md` and `landscape_survivors_decisions.json`.

### H3 + H4 manual freeze (apply both)

```bash
.venv/bin/python scripts/stage11/export_h3_manual_freeze_pdf.py
.venv/bin/python scripts/stage11/export_h4_manual_freeze_pdf.py
# After filling decisions → h3_manual_freeze.json + h4_manual_freeze.json with frozen=true:
bash scripts/stage11/apply_h3_h4_manual_freeze.sh
```

See `human_review/post_freeze_claim_hierarchy.md` for confirmatory vs exploratory claims.

**Claim boundary:** Notebook **13** decides what you can claim. Notebook **12** is the security/care deep-dive source; Notebook **14** reuses it for presentation and adds residual Goodreads / dose-response / attention figures. Neither 12 nor 14 changes H1–H6 confirmatory verdicts.

### H4 manual freeze (26 atom topics)

Lean checklist PDF for external protection + protective commitment + possession/control (no LLM rationales):

```bash
.venv/bin/python scripts/stage11/export_h4_manual_freeze_pdf.py
# After filling decisions → h4_manual_freeze.json with frozen=true:
bash scripts/stage11/apply_h4_manual_freeze.sh

# H3 emotional vs material dichotomy checklist (lean PDF):
.venv/bin/python scripts/stage11/export_h3_manual_freeze_pdf.py
# Outputs: stage11_h3_manual_freeze.pdf/.md + h3_manual_freeze_decisions.json
```

Execute notebooks (outputs saved for GitHub):

```bash
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
  notebooks/08_refined_construct_analysis/*.ipynb
```
