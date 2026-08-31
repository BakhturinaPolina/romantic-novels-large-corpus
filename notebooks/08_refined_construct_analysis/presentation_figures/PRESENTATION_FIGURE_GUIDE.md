# Stage 11 Presentation Figure Guide

Regenerate figures:

```bash
.venv/bin/python scripts/stage11/build_presentation_figures.py
```

Outputs: `results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/presentation_figures/`  
Audit notes: [AUDIT_NOTES.md](AUDIT_NOTES.md) · Manifest: [figure_source_manifest.csv](figure_source_manifest.csv)

Prespecified effect-size gate: `|δ| ≥ 0.11` (not the same as p &lt; .05).

---

## Main presentation sequence (≈15–20 min)

### Figure 1 — `fig01_contextual_agreement`

**Question.** How often did contextual coding agree with lexical cues for H1–H6?

**Result.** Agreement is only 30–55% (H1 54/98=55%; H2 3/10=30%; H3 48/90=53%; H4 24/71=34%; H5 11/22=50%; H6 19/54=35%).

**Interpretation.** Lexical topic cues are an incomplete guide to narrative function; contextual refinement meaningfully changes coding.

**Caveat.** Methodological result — not an outcome-association finding.

**Spoken takeaway.** “Across H1–H6, lexical and contextual readings agreed in only about one-third to one-half of topics — refinement was necessary.”

---

### Figure 2 — `fig02_measurement_status`

**Question.** After refinement, could each primary hypothesis still be measured?

**Result.** H1/H5/H6 viable; H4 thin; H2 and H3 unmeasurable (zero HEA topics; empty material denominator).

**Interpretation.** Measurement repair changed what claims are even possible.

**Caveat.** Do not describe H2/H3 as “null effects.”

**Spoken takeaway.** “Two of the six primary contrasts could no longer be measured validly after contextual freeze.”

---

### Figure 3 — `fig03_primary_hypothesis_verdicts`

**Question.** What is the confirmatory H1–H6 outcome after refinement?

**Result.** H1 directional (δ≈+0.099, below gate); H2/H3 unmeasurable (no point); H4 thin/inconclusive (δ≈+0.090); H5/H6 contradicted (negative δ).

**Interpretation.** None of the six broad primaries clearly clears the full prespecified evidence standard.

**Caveat.** Do not promote components into parent-hypothesis confirmation here.

**Spoken takeaway.** “No broad H1–H6 primary fully survives as a clean confirmatory win — and two are unmeasurable, not null.”

---

### Figure 4 — `fig04_stage10_stage11_transition`

**Question.** How did Stage 10 conclusions change after Stage 11 refinement?

**Result.** Measurable hypotheses change δ (e.g. H1 −0.029→+0.099; H5/H6 flip sign). H2/H3 leave the δ scale into a “not measurable” status band.

**Interpretation.** Refinement changed both estimates and measurability.

**Caveat.** The grey status band is not a δ value.

**Spoken takeaway.** “Contextual refinement didn’t just nudge numbers — it changed what we could legitimately claim.”

---

### Figure 5 — `fig05_component_effects` + `fig05b_component_evidence_matrix`

**Question.** Which specific narrative functions show clearer associations than broad binaries?

**Result.** Notable components: emotional reassurance δ≈+0.136; tenderness ≈+0.135; appearance ≈−0.142; external danger ≈+0.116; external protection ≈+0.160 (thin, 1 topic). Evidence matrix shows H1 unadjusted+/adjusted− disagreement; danger clears |δ| gate but adjusted quality p n.s.

**Interpretation.** Stronger patterns sit at specific functions; large δ ≠ robust multi-criterion evidence.

**Caveat.** Open markers = thin measurement. Components ≠ parent confirmation.

**Spoken takeaway.** “The clearer signals are function-specific — and even large estimates need the evidence matrix, not a single number.”

---

### Figure 6 — `fig06_attention_shift`

**Question.** Where does narrative attention differ for higher-rated vs comparison romance?

**Result.** Exploratory percentage-point shifts include tenderness ≈+0.416 pp; explicit sex ≈−0.186 pp; appearance ≈−0.180 pp.

**Interpretation.** Higher-rated books may devote relatively more attention to tenderness and less to explicit sex/appearance.

**Caveat.** Exploratory / compositional / not causal.

**Spoken takeaway.** “Exploratory attention shifts point to tenderness up and explicit sex/appearance down — labeled exploratory only.”

---

## Appendix figures (supporting)

| Figure | Purpose |
| --- | --- |
| `appendix_richness` | Raw vs rarefied δ; M1/M2 β — **suppression**, not null after drivers |
| `appendix_danger_protection_interaction` | Two-line plot; interaction p≈.51/.24/.22 — no reliable interaction |
| `appendix_security_care_specificity` | Strict→moderate→broad small multiples |
| `appendix_promise_functions` | Dot-whisker + n topics; flag thin bundles |
| `appendix_quality_reach` | Decluttered quadrants; focal labels only |
| `appendix_function_drift` | Stable vs drifted contextual function |
| `appendix_felt_vs_looked` | Embodiment; thin open markers |
| `appendix_ees_three_panel` | Emotion (incl. **containment** δ≈+0.182), embodiment, social |
| `appendix_genre_era` | Subgroup δ with overall reference |

Existing NB14 assets (dose-response, residual diagnostics) remain under `notebook_analysis/14_…/figures/` for appendix use.

---

## Claims that should NOT be made

- Broad H1–H6 “confirmed”
- H2/H3 as null / zero effects
- Danger × protection interaction
- Richness “loses independent information” after drivers (false; suppression)
- Component findings as confirmation of parent hypotheses
- Attention / EES as confirmatory or causal
- External protection as strongest overall finding without thin-measurement caveat
