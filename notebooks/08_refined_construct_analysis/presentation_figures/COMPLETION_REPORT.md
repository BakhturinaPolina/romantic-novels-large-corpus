# Stage 11 Presentation Audit — Completion Report

## A. Audit findings

1. **Notebook 14 richness prose contradicted saved M1/M2 models** (null template vs suppression).
2. **NB11 `old_vs_refined_bars.png` encodes H2 as δ=0 and H3 as δ≈+0.06** despite NB13 unmeasurable blanks.
3. **NB13 `primary_h1_h6_forest` / NB14 `presentation_forest` omit unmeasurable rows**, so H2/H3 disappear from confirmatory slides.
4. **H1 unadjusted δ (+)** vs **quality β (−, p&lt;.05)** disagreement was easy to miss in prior forests.
5. **External danger** clears \|δ\|≥.11 but adjusted quality p is n.s.
6. **External protection** largest component δ but thin (1 topic).
7. **Emotion containment** (δ≈+0.182, author-half stable) omitted from NB15 `integrated_summary_effects`.
8. **Danger×protection heatmaps** visually suggest structure despite interaction p≈.51/.24/.22.
9. **“Attention waterfall”** is a diverging bar chart (renamed in new suite).
10. **H4 `one_sentence` said “Primary ratio unmeasurable”** while gate=`thin` with δ≈+0.090 — resolved in integrity cleanup.

## B. Notebook 14 richness resolution

| Item | Detail |
| --- | --- |
| Inconsistency | Conclusion: richness “no longer carries independent information” in M2; table: M2 β larger & significant. |
| Cause | Pre-written null template not updated after seeing suppression. |
| Verified | M1 β=0.00237 (p=0.065) → M2 β=0.00658 (p=1.75e−6); rarefied OLS p=0.608. |
| Fix | Prose only in `_src/14_exploratory_presentation_results.py` + percent sync. Models not recomputed. |

## C. Files changed

| File | Why |
| --- | --- |
| `notebooks/08_refined_construct_analysis/_src/14_exploratory_presentation_results.py` | Correct richness M2 interpretation (suppression) |
| `notebooks/08_refined_construct_analysis/14_exploratory_presentation_results.ipynb` | Synced from `_src` |
| `notebooks/08_refined_construct_analysis/_src/13_final_statistical_tests.py` | H4 `VERDICT_NOTES` + `CLAIM_HIERARCHY` tier wording |
| `notebooks/08_refined_construct_analysis/13_final_statistical_tests.ipynb` | Synced H4 source cells |
| `…/13_…/tables/final_verdict_table.{csv,md,parquet}` | Corrected H4 `one_sentence` only |
| `…/13_…/tables/post_freeze_claim_hierarchy.{csv,parquet}` | H4 primary tier `open` + claim text |
| `src/stage11_refined_construct_analysis/analysis/presentation_suite/*` | Figure suite + provenance validator |
| `scripts/stage11/build_presentation_figures.py` | One-command rebuild CLI |
| `tests/stage11/test_presentation_suite.py` | Structural + numerical provenance tests |
| `notebooks/08_refined_construct_analysis/presentation_figures/*` | AUDIT_NOTES, GUIDE, manifest |
| `results/.../presentation_figures/*` | Generated PNG/PDF + canonical CSVs |

Existing `notebook_analysis/*/figures/` analytical PNGs were **not** overwritten.

## D. Figures created

All under `results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/presentation_figures/` (PNG+PDF).

| Figure | Purpose | Data source | Evidence level |
| --- | --- | --- | --- |
| fig01 | Lexical–contextual agreement | NB01–06 agreement CSVs | methodological |
| fig02 | Measurement status strip | final_verdict + coverage | confirmatory |
| fig03 | H1–H6 hybrid verdicts | primary + verdict tables | confirmatory |
| fig04 | Stage10→11 transition | stage10_vs_final_side_by_side | confirmatory |
| fig05 / fig05b | Component forest + evidence matrix | component_effects + traffic light | confirmatory components |
| fig06 | Attention shift | attention_waterfall | exploratory |
| appendix_* | Richness, interaction, specificity, promise, QR, drift, embodiment, EES, genre/era | NB10/12/14/15 tables | appendix / exploratory |

## E. Statistical checks

- `pytest tests/stage11/test_presentation_suite.py` — **10 passed**
- Provenance: presentation δ/CI/adjusted/agreement/components/transitions match Stage 11 tables; attention `diff_pp` + richness M1/M2 locked; H4 must not say “primary ratio unmeasurable”
- H1–H6 present; H2/H3 effect_size NaN; H4 thin with δ; agreement % = n/N; CI ordering; thin flag on external protection; H1 adjusted disagreement flagged; all expected PNG/PDF present

## F. Remaining caveats

- Genre/era source table lacks formal subgroup CIs (n shown; overall δ as reference) — figure states subgroup point differences are not formal heterogeneity evidence.
- Danger×protection display uses quadrant means + reported interaction p; in-figure note: predictive CI unavailable from saved output.
- H2 absent from function-drift table (documented on figure).

## G. Presentation recommendation (main six)

1. Contextual agreement (30–55%) — `fig01_contextual_agreement`
2. Measurement status (H2/H3 unmeasurable; H4 thin) — `fig02_measurement_status`
3. H1–H6 hybrid verdicts — `fig03_primary_hypothesis_verdicts`
4. Stage 10→11 transition (right-hand Measurement outcome panel for H2/H3) — `fig04_stage10_stage11_transition`
5. Component forest + evidence matrix (H1 adj. disagreement; thin protection) — `fig05_component_effects` + `fig05b_component_evidence_matrix`
6. Attention-shift (exploratory) — `fig06_attention_shift`

## H. Claims that should NOT be made

- Broad H1–H6 confirmed
- H2/H3 null/zero effects
- H4 primary ratio “unmeasurable” (it is thin/inconclusive with δ≈+0.090)
- Reliable danger × protection interaction
- Richness null after thematic drivers
- Components confirm parent hypotheses
- Attention/EES confirmatory or causal
- External protection as strongest finding without thin caveat
