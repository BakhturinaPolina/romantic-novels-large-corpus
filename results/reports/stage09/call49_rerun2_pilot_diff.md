# Stage09 v2.5 pilot diff (30 stratified topics, call_49)

- Previous mapping: `results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call49/taxonomy_mappings.json`
- New mapping: `results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call49_rerun2/pilot/taxonomy_mappings_pilot30.json`

All before/after counts below cover the **same 30 topics** present in both runs, so the two columns are directly comparable.

## Headline numbers

| Metric | Before | After |
|---|---|---|
| Topics compared | 30 | 30 |
| `uncertain_interpretable` | 11 | 4 |
| Low `evidence_quality` | 21 (70.0%) | 9 (30.0%) |
| `use_in_macro_axes=true` | 6 | 10 |
| Topics on axis-bearing IDs | 10 | 14 |
| Flagged noise | 0 | 0 |

Main category changed for **7 of 30** comparable topics (23.3%).

Evidence-quote compliance: **100.0%** of new mappings open `mapping_reasoning` with `EVIDENCE:`.

`uncertain_interpretable` without an `uncertainty_reason`: **0** (should be 0).

## Per-stratum outcome

| stratum                 |   n |   main_changed |   evidence_improved |   still_low_evidence |   still_uncertain |   quotes_evidence |
|:------------------------|----:|---------------:|--------------------:|---------------------:|------------------:|------------------:|
| high_confidence_control |   5 |              0 |                   0 |                    0 |                 0 |                 5 |
| low_evidence_quality    |  10 |              0 |                   8 |                    2 |                 1 |                10 |
| payoff_3_1_candidates   |   5 |              0 |                   3 |                    0 |                 0 |                 5 |
| uncertain_interpretable |  10 |              7 |                   3 |                    7 |                 3 |                10 |

## Axis-bearing coverage

| axis_id   |   n_topics_old |   n_topics_new |   delta | was_empty   | still_empty   |
|:----------|---------------:|---------------:|--------:|:------------|:--------------|
| 2.1       |              0 |              0 |       0 | True        | True          |
| 2.2       |              0 |              0 |       0 | True        | True          |
| 2.3       |              2 |              2 |       0 | False       | False         |
| 2.4       |              0 |              0 |       0 | True        | True          |
| 2.5       |              0 |              0 |       0 | True        | True          |
| 3.1       |              0 |              0 |       0 | True        | True          |
| 3.2       |              2 |              2 |       0 | False       | False         |
| 4.2       |              0 |              2 |       2 | True        | False         |
| 4.3       |              0 |              0 |       0 | True        | True          |
| 4.4       |              0 |              0 |       0 | True        | True          |
| 4.5       |              0 |              0 |       0 | True        | True          |
| 4.6       |              4 |              5 |       1 | False       | False         |
| 4.7       |              0 |              0 |       0 | True        | True          |
| 5.3a      |              0 |              0 |       0 | True        | True          |
| 6.1a      |              0 |              0 |       0 | True        | True          |
| 6.4       |              1 |              1 |       0 | False       | False         |
| 6.6       |              0 |              0 |       0 | True        | True          |
| 6.7       |              0 |              0 |       0 | True        | True          |
| 7.2       |              1 |              1 |       0 | False       | False         |
| 7.3       |              0 |              1 |       1 | True        | False         |
| 7.4       |              0 |              0 |       0 | True        | True          |
| 8.3a      |              0 |              0 |       0 | True        | True          |

## Main-category churn

| old_main                | new_main   |   n |
|:------------------------|:-----------|----:|
| uncertain_interpretable | 4.2        |   2 |
| uncertain_interpretable | 3.3        |   1 |
| uncertain_interpretable | 4.6        |   1 |
| uncertain_interpretable | 6.1b       |   1 |
| uncertain_interpretable | 7.3        |   1 |
| uncertain_interpretable | 9.3        |   1 |

## Changed topics (first 40)

|   topic_id | label                                  | old_main                | new_main   | old_evidence   | new_evidence   |   new_confidence |
|-----------:|:---------------------------------------|:------------------------|:-----------|:---------------|:---------------|-----------------:|
|         52 | Talking About Dogs and Animals         | uncertain_interpretable | 4.2        | low            | low            |             0.62 |
|         97 | Uncomfortable Silence Falls Over Group | uncertain_interpretable | 9.3        | low            | medium         |             0.62 |
|        147 | Painting A House to Sell               | uncertain_interpretable | 6.1b       | low            | medium         |             0.72 |
|        160 | Watching Movies Together               | uncertain_interpretable | 4.2        | low            | low            |             0.55 |
|        190 | Offering to Get Someone Cleaned Up     | uncertain_interpretable | 4.6        | low            | low            |             0.55 |
|        251 | Remarking on An Age Gap                | uncertain_interpretable | 3.3        | low            | low            |             0.62 |
|        327 | Crouching Over A Fallen Figure         | uncertain_interpretable | 7.3        | low            | medium         |             0.65 |

### Reasoning for changed topics

**Topic 52 — Talking About Dogs and Animals**  
`uncertain_interpretable` -> `4.2` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i'll be taking the dogs out for their afternoon walk, so there'll be some peace and quiet for you" — Keywords source used as secondary. Shortlist: (1) 4.2 everyday relational bonding — characters sharing domestic/outdoor routines; (2) 8.2 public/leisure/outdoor space — camping/bear context; (3) 9.3 humor/banter — the dog intelligence claim has a light register. Runner-up 8.2 lost because the relational interaction between characters (offering peace and quiet, discussing the dog's intelligence) suggests a bonding function rather than pure location description. 9.3 lost because humor is incidental, not dominant. No kiss, desire, conflict, or commitment visible, so use_in_macro_axes=false. The axis_hint no_hypothesis_signal is confirmed by snippets.

**Topic 97 — Uncomfortable Silence Falls Over Group**  
`uncertain_interpretable` -> `9.3` (evidence low -> medium, confidence 0.62)

> EVIDENCE: "the other guests in the group, two couples it would seem, had stopped talking and began to shuffle uncomfortably" — Snippets show a group social scene with tense silence and physical discomfort. Shortlist: (1) 9.3 humor/banter/light register — this is the inverse of light register, but 9.3 covers register tone broadly; (2) 4.4 conflict/distance — no main-couple conflict is visible, just ambient group tension; (3) 1.1 body reactions — shuffling and breath are bodily but secondary to the social atmosphere. Runner-up 4.4 lost because no main-couple relational strain is shown; the silence is a group social atmosphere beat. 9.3 is imperfect as it covers light register, but as a discourse/register flag it is the closest fit for a tonal atmosphere marker. Secondary 1.1 captures the physical discomfort signals. No hypothesis-relevant evidence visible, so macro false.

**Topic 147 — Painting A House to Sell**  
`uncertain_interpretable` -> `6.1b` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "slap on some paint and get it listed with a real-estate agent" — Snippet 3 clearly shows a property-sale plan. Shortlist: 6.1b (generic business/institutional logistics), 6.4 (economic precarity), 8.2 (public/leisure space). 6.4 lost because no rent, debt, or can't-afford vocabulary appears; this is a sale plan, not financial distress. 8.2 lost because the property is an object of transaction, not a leisure or public setting being visited. Snippet 1 ('paint yourself black… I will do anything for you') is ambiguous but snippet 3 anchors the topic in property logistics. No romantic mechanics, no axis-bearing content, so use_in_macro_axes=false.

**Topic 160 — Watching Movies Together**  
`uncertain_interpretable` -> `4.2` (evidence low -> low, confidence 0.55)

> EVIDENCE: "we've been watching movies" — This snippet from the keyword source confirms shared leisure activity. Runner-up 8.2 (public/leisure space) lost because the relational companionship function, however weak, edges out pure location framing. Runner-up uncertain_interpretable was considered because snippet 2 ('watching him closely for any reaction') suggests surveillance rather than bonding, creating thematic tension; however, snippet 3 anchors the topic in shared movie-watching as a leisure activity. The axis hint is no_hypothesis_signal and no courtship, care, or commitment evidence is visible, so use_in_macro_axes=false. Evidence quality is low because only one snippet clearly supports the bonding/leisure reading and the other two introduce ambiguity.

**Topic 190 — Offering to Get Someone Cleaned Up**  
`uncertain_interpretable` -> `4.6` (evidence low -> low, confidence 0.55)

> EVIDENCE: "i'll get her cleaned up, said a handsome groom, taking her arm" — Three snippets converge on offers to clean/freshen someone up, with one involving a groom assisting a woman. Shortlist: 4.6 (caretaking/reassurance), 4.2 (everyday relational bonding), uncertain_interpretable. 4.6 wins narrowly because the act is one character attending to another's physical state — a minor caretaking gesture. 4.2 lost because there is no broader courtship or bonding context visible. Keywords (sweeping, dump, suitcase, parties) diverge from snippets and are not used as primary evidence. No hypothesis-relevant axis signal is present, so use_in_macro_axes=false. Evidence quality is low because snippets are very short and the keywords do not corroborate the caretaking reading.

**Topic 251 — Remarking on An Age Gap**  
`uncertain_interpretable` -> `3.3` (evidence low -> low, confidence 0.62)

> EVIDENCE: "their age difference was outrageous, which prompted her to ask, 'but why now, your grace?'" — This snippet shows a character questioning/challenging an age-gap relationship, suggesting hesitation or ambivalence (3.3). Runner-up 4.4 lost because no active conflict or breakup threat is visible; the question is more uncertain than combative. Runner-up 4.2 lost because no bonding or courtship act is present. The structural-aging snippets (metal stained with weather, bone structure) are thematically incoherent with the relational snippet, lowering confidence. 3.3 is exploratory-only, so use_in_macro_axes=false. use_in_theory_watchlist=true because age-gap dynamics are theory-relevant for H5/H6.

**Topic 327 — Crouching Over A Fallen Figure**  
`uncertain_interpretable` -> `7.3` (evidence low -> medium, confidence 0.65)

> EVIDENCE: "the wings lifted and spread behind her" — Paranormal creature vocabulary (wings) combined with crouching over a fallen figure signals a danger/crisis scene in a paranormal setting. Shortlist: 7.3 (risk/danger/crisis), 7.2 (violence/threats), 4.6 (caretaking over fallen person). 7.2 lost because no deliberate harm or threat act is visible — the crouching is ambiguous protective or predatory posture. 4.6 lost because no reassurance or care language appears; the scene is tense and watchful rather than nurturing. 7.3 wins as the best fit for a tense physical crisis moment. Keywords 'growl' and 'squeeze' reinforce creature/tension register. Runner-up 4.6 placed in other_plausible_ids. Not axis-bearing because no hypothesis-relevant romantic function is visible in snippets.


## Still-low evidence quality after re-run

5 topics kept the same category and still report low evidence quality.

|   topic_id | label                                     | new_main                | new_uncertainty_reason                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----------:|:------------------------------------------|:------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         40 | Resigned Acknowledgment of Disappointment | uncertain_interpretable | Snippets are fragmentary exclamations and a foraging reference ('find some morels') with no identifiable narrative or thematic domain; the Stage08 label 'Resigned Acknowledgment of Disappointment' is not supported by the visible text, and no setting, relationship function, or emotional content can be reliably named.                                                                                               |
|        150 | Curious Replies and Deflections           | 9.1                     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
|        180 | Comparing Sizes and Spaces                | uncertain_interpretable | The topic clusters size-comparison language across heterogeneous referents (rooms, bodies, crowds) with no dominant thematic function — not a setting, not appearance, not a social event, not a relationship beat. No single context ID captures the cross-domain size-comparison register.                                                                                                                                |
|        187 | Admitting Everything Has Gone Wrong       | uncertain_interpretable | Snippets show acknowledgment of failure ('we've messed up everything') and claims of competence ('I've got things handled'), but no subject matter is visible — the domain could be romantic conflict, workplace crisis, family trouble, or something else entirely. Keywords like 'pregnant' and 'emotional' hint at possible relationship stakes but do not appear in any snippet, making the thematic center unnameable. |
|        221 | Caught Off Guard By Surprises             | uncertain_interpretable | Snippets show surprise/unexpectedness as a surface register but reveal no coherent thematic domain — one snippet is about money, one about avoiding surprises, one is a historical/formal register comment. No setting, relationship function, emotional arc, or genre context can be reliably named from this evidence.                                                                                                    |
