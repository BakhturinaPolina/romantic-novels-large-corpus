# Stage 11 Presentation Audit Notes

Run: `v4_l12_granular_final_call49`  
Date: 2026-09-01  
Scope: notebooks 13–15 + upstream agreement/gates; presentation redesign only (no threshold/mapping changes).

## Authoritative sources

| Role | Path |
| --- | --- |
| Confirmatory H1–H6 verdicts | `…/13_final_statistical_tests/tables/final_verdict_table.*` |
| Primary δ / CI / quality β | `…/13_…/tables/primary_h1_h6_table.*` |
| Components | `…/13_…/tables/component_effects.*` |
| Stage 10 vs 11 | `…/13_…/tables/stage10_vs_final_side_by_side.*` |
| Spec stability | `…/13_…/tables/robustness_traffic_light.*` |
| Measurement gates | `…/08_refined_axes_validity/tables/headline_measurement_gates.*` + `constructs/construct_coverage.json` |
| Lexical–contextual agreement | `…/0{1–6}_*/tables/h*_lexical_contextual_agreement.csv` |
| Function drift | `…/10_contextual_validation/tables/cell_stability_by_hypothesis.csv` |
| Richness M1/M2 | `…/14_…/tables/thematic_richness_vs_drivers.csv` |
| Attention shift | `…/14_…/tables/attention_waterfall.csv` |
| Danger × protection | `…/14_…/tables/danger_x_protection_reused.csv` |
| EES / embodiment | `…/15_…/tables/{emotion,embodiment,felt_vs_looked_body,family_social}_*.csv` |

## Notebook 14 richness resolution

| Item | Detail |
| --- | --- |
| Inconsistency | Conclusion said richness “no longer carries independent information” in M2; displayed/saved M2 showed larger significant β. |
| Cause | Pre-written null template left in place after numbers showed **suppression** (M1 marginal → M2 stronger), not attenuation. |
| Verified result | M1 `taxonomy_n_eff` β=0.00237 (p=0.065); M2 β=0.00658 (p=1.75e−6). Rarefied OLS p=0.608. Exploratory only. |
| Fix | Prose in `_src/14_exploratory_presentation_results.py` + synced notebook. **Models not recomputed.** |
| Files changed | `_src/14_…py`, `14_exploratory_presentation_results.ipynb` |

## Traceability (core statistics → figures)

| Source file | Variable / row | Statistic | Hypothesis / construct | Figure |
| --- | --- | --- | --- | --- |
| `h*_lexical_contextual_agreement.csv` | `agree` count / n | agreement % | H1–H6 | fig01 |
| `final_verdict_table` + coverage | `measurement_gate`, topic counts | status | H1–H6 | fig02 |
| `primary_h1_h6_table` + `final_verdict_table` | `cliffs_delta`, CI, `final_bucket` | primary δ | H1–H6 | fig03 |
| `stage10_vs_final_side_by_side` | `original_delta`, `refined_delta` | transition | H1–H6 | fig04 |
| `component_effects` + traffic light | δ, CI, `quality_*`, gate | component evidence | components | fig05 / fig05b |
| `attention_waterfall` | `diff_pp` | attention shift | exploratory themes | fig06 |
| `thematic_richness_*` | cliffs / M1–M2 β | richness | exploratory | appendix_richness |
| `danger_x_protection_reused` | interaction p, betas | no interaction | exploratory | appendix_danger_protection |
| `strict_moderate_broad_trajectories_reused` | δ by level | specificity | exploratory | appendix_security_care |
| `promise_type_comparison_reused` | δ, n_topics | promise functions | exploratory | appendix_promise |
| `quality_reach_standardized_betas` | quality/reach β | quadrants | exploratory | appendix_quality_reach |
| `cell_stability_by_hypothesis` | `n_differs` / `n_with_both…` | drift % | H1,H3–H6 | appendix_function_drift |
| `felt_vs_looked_body` / EES tables | δ, CI, status | embodiment / EES | exploratory | appendix_felt_vs_looked, appendix_ees |
| `genre_era_subgroup_deltas` | subgroup δ, n | stability | exploratory | appendix_genre_era |

## Conflicts noted (presentation must follow NB13)

1. NB11 `old_vs_refined_bars.png` plots H2 δ=0 and H3 δ≈0.06; NB13 leaves refined δ blank for unmeasurable — **use NB13**.
2. H1 unadjusted δ &gt; 0 while `quality_beta` &lt; 0 and significant — must be visible in evidence matrix.
3. External danger clears \|δ\|≥0.11 but `quality_p` n.s. — matrix must expose.
4. External protection largest component δ but `thin` (1 topic) — open marker.
5. Emotion containment omitted from NB15 `integrated_summary_effects` — include in appendix EES panel.

## Effect-size gate

Prespecified primary gate: `|δ| >= 0.11` (`notebook_helpers.effect_gate`). Not equivalent to p &lt; 0.05.
