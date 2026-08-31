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
| `src/stage11_refined_construct_analysis/analysis/presentation_suite/*` | New reproducible figure suite |
| `scripts/stage11/build_presentation_figures.py` | One-command rebuild CLI |
| `tests/stage11/test_presentation_suite.py` | Validation tests |
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

- `pytest tests/stage11/test_presentation_suite.py` — **7 passed**
- H1–H6 present; H2/H3 effect_size NaN; agreement % = n/N; CI ordering; thin flag on external protection; H1 adjusted disagreement flagged; all expected PNG/PDF present

## F. Remaining caveats

- Genre/era source table lacks formal subgroup CIs (n shown; overall δ as reference).
- Danger×protection display uses quadrant means + reported interaction p (full predictive SE bands not in saved tables).
- H2 absent from function-drift table (documented on figure).
- H4 `one_sentence` still says “Primary ratio unmeasurable” while gate=`thin` with δ present — wording inconsistency in NB13 prose left as-is (gate/δ used for figures).

## G. Presentation recommendation (main six)

1. Contextual agreement (30–55%) — `fig01_contextual_agreement`
2. Measurement status (H2/H3 unmeasurable) — `fig02_measurement_status`
3. H1–H6 hybrid verdicts — `fig03_primary_hypothesis_verdicts`
4. Stage 10→11 transition (status band for unmeasurable) — `fig04_stage10_stage11_transition`
5. Component forest + evidence matrix (H1 adj. disagreement; thin protection) — `fig05_component_effects` + `fig05b_component_evidence_matrix`
6. Attention-shift (exploratory) — `fig06_attention_shift`

## H. Claims that should NOT be made

- Broad H1–H6 confirmed
- H2/H3 null/zero effects
- Reliable danger × protection interaction
- Richness null after thematic drivers
- Components confirm parent hypotheses
- Attention/EES confirmatory or causal
- External protection as strongest finding without thin caveat
