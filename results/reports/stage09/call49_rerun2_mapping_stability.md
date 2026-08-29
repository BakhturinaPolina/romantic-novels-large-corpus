# Stage09 v2.5 full re-run stability (call_49, 348 topics)

- Previous mapping: `results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call49/taxonomy_mappings.json`
- New mapping: `results/stage09_category_mapping/stage1_theory_driven_categories/placeholder_v4_call49_rerun2/taxonomy_mappings.json`

All before/after counts below cover the **same 348 topics** present in both runs, so the two columns are directly comparable.

## Status: complete

Taxonomy stage 1 finished for all 348 topics (Claude Sonnet 4.6, prompt v2.5). Radway stage 2 finished for all 348 topics and is written to
`results/stage09_category_mapping/stage2_radway_functions/placeholder_v4_call49_rerun2/taxonomy_with_radway.json`.

**Stage10 analysis still reads the original `placeholder_v4_call49` mapping** via `topic_lookup.parquet`. Folding this re-run into the notebooks means rebuilding `topic_lookup` and the book analysis frame — a deliberate second pass, not automatic.

Payoff guard still applies: `3.1` has **1** topic after the re-run (below the 3-topic floor), so `AX_payoff_safety_fallback = 4.5 + 4.6` remains the correct H2/H3 construction.

## Radway stage 2 coverage

182 of 348 topics (52.3%) mapped to an R1–R13 function; 166 (47.7%) are background/`none`. Phase split among mapped topics: I = 73, II = 72, III = 37. Confidence: high 157, medium 146, low 45.

| Function | n | Name |
|---|---|---|
| none | 166 | None of the above |
| R8 | 43 | Hero treats heroine tenderly |
| R11 | 19 | Hero declares love and demonstrates commitment |
| R9 | 17 | Heroine responds warmly to hero's tenderness |
| R12 | 16 | Heroine responds sexually and emotionally |
| R1 | 16 | Heroine's social identity is destroyed |
| R3 | 15 | Hero responds ambiguously to heroine |
| R4 | 13 | Heroine interprets hero's behaviour as purely sexual interest |
| R2 | 12 | Heroine reacts antagonistically to the hero |
| R10 | 12 | Heroine reinterprets hero's behaviour as result of previous hurt |
| R7 | 8 | Hero and heroine are physically or emotionally separated |
| R6 | 8 | Hero retaliates or punishes heroine |
| R13 | 2 | Heroine's identity is restored |
| R5 | 1 | Heroine responds with anger or coldness |

## Headline numbers

| Metric | Before | After |
|---|---|---|
| Topics compared | 348 | 348 |
| `uncertain_interpretable` | 30 | 7 |
| Low `evidence_quality` | 163 (46.8%) | 77 (22.1%) |
| `use_in_macro_axes=true` | 75 | 115 |
| Topics on axis-bearing IDs | 152 | 159 |
| Flagged noise | 1 | 3 |

Main category changed for **47 of 348** comparable topics (13.5%).

Evidence-quote compliance: **100.0%** of new mappings open `mapping_reasoning` with `EVIDENCE:`.

`uncertain_interpretable` without an `uncertainty_reason`: **0** (should be 0).

## Axis-bearing coverage

| axis_id   |   n_topics_old |   n_topics_new |   delta | was_empty   | still_empty   |
|:----------|---------------:|---------------:|--------:|:------------|:--------------|
| 2.1       |             18 |             18 |       0 | False       | False         |
| 2.2       |              4 |              4 |       0 | False       | False         |
| 2.3       |              7 |              7 |       0 | False       | False         |
| 2.4       |              0 |              0 |       0 | True        | True          |
| 2.5       |              6 |              7 |       1 | False       | False         |
| 3.1       |              0 |              1 |       1 | True        | False         |
| 3.2       |             12 |             14 |       2 | False       | False         |
| 4.2       |             11 |             14 |       3 | False       | False         |
| 4.3       |             17 |             20 |       3 | False       | False         |
| 4.4       |              8 |              8 |       0 | False       | False         |
| 4.5       |              9 |              8 |      -1 | False       | False         |
| 4.6       |             30 |             30 |       0 | False       | False         |
| 4.7       |              2 |              2 |       0 | False       | False         |
| 5.3a      |              1 |              1 |       0 | False       | False         |
| 6.1a      |              0 |              0 |       0 | True        | True          |
| 6.4       |              1 |              1 |       0 | False       | False         |
| 6.6       |              1 |              1 |       0 | False       | False         |
| 6.7       |              0 |              0 |       0 | True        | True          |
| 7.2       |             13 |             12 |      -1 | False       | False         |
| 7.3       |              9 |              8 |      -1 | False       | False         |
| 7.4       |              2 |              2 |       0 | False       | False         |
| 8.3a      |              1 |              1 |       0 | False       | False         |

## Main-category churn

| old_main                | new_main   |   n |
|:------------------------|:-----------|----:|
| uncertain_interpretable | 8.5        |   4 |
| uncertain_interpretable | 9.2        |   3 |
| uncertain_interpretable | 3.3        |   3 |
| uncertain_interpretable | 4.2        |   2 |
| uncertain_interpretable | 9.4        |   2 |
| uncertain_interpretable | 4.6        |   2 |
| 1.1                     | 3.2        |   1 |
| 9.2                     | 9.1        |   1 |
| 9.4                     | 9.2        |   1 |
| 9.4                     | 9.3        |   1 |
| uncertain_interpretable | 3.1        |   1 |
| uncertain_interpretable | 6.1b       |   1 |
| 8.3b                    | 8.1        |   1 |
| uncertain_interpretable | 7.3        |   1 |
| uncertain_interpretable | 8.3b       |   1 |
| uncertain_interpretable | 8.4        |   1 |
| uncertain_interpretable | 9.3        |   1 |
| 9.2                     | 4.6        |   1 |
| 8.2                     | 4.2        |   1 |
| 10.2                    | 4.3        |   1 |
| 7.3                     | 9.1        |   1 |
| 3.2                     | 4.4        |   1 |
| 4.4                     | 1.7        |   1 |
| 4.5                     | 4.1        |   1 |
| 4.5                     | 4.3        |   1 |
| 4.6                     | 2.5        |   1 |
| 4.6                     | 3.2        |   1 |
| 4.6                     | 3.3        |   1 |
| 4.6                     | 4.3        |   1 |
| 5.1                     | 4.5        |   1 |
| 6.5                     | 4.6        |   1 |
| 7.1                     | 3.2        |   1 |
| 7.1                     | 7.3        |   1 |
| 7.2                     | 7.1        |   1 |
| 7.3                     | 10.1       |   1 |
| 7.3                     | 10.3       |   1 |
| uncertain_interpretable | noise      |   1 |

## Changed topics (first 80)

|   topic_id | label                                   | old_main                | new_main   | old_evidence   | new_evidence   |   new_confidence |
|-----------:|:----------------------------------------|:------------------------|:-----------|:---------------|:---------------|-----------------:|
|         21 | Deciding Whether to Stay or Leave       | uncertain_interpretable | 9.2        | low            | low            |             0.62 |
|         30 | Leading A Horse Into The Barn           | uncertain_interpretable | 8.5        | low            | medium         |             0.78 |
|         33 | Werewolf Pack Confrontation             | 7.3                     | 10.1       | low            | medium         |             0.78 |
|         35 | Remarking on Someone's Age              | uncertain_interpretable | 8.4        | low            | low            |             0.62 |
|         43 | Pissed Off and Grumbling                | 3.2                     | 4.4        | low            | medium         |             0.72 |
|         52 | Talking About Dogs and Animals          | uncertain_interpretable | 4.2        | low            | low            |             0.62 |
|         54 | Ordering Food and Dessert               | 8.2                     | 4.2        | medium         | medium         |             0.72 |
|         91 | Arguing Over Guns and Weapons           | 7.2                     | 7.1        | low            | medium         |             0.72 |
|         92 | Heart Pounding With Dread               | 1.1                     | 3.2        | medium         | medium         |             0.78 |
|         97 | Uncomfortable Silence Falls Over Group  | uncertain_interpretable | 9.3        | low            | medium         |             0.62 |
|        103 | Last Honest Conversation Before Parting | 4.4                     | 1.7        | low            | low            |             0.62 |
|        120 | Suggesting Someone Take A Shower        | 8.3b                    | 8.1        | medium         | medium         |             0.78 |
|        121 | Revealing Plans to The Prince           | 10.2                    | 4.3        | medium         | medium         |             0.72 |
|        136 | Declaring Nothing Else Matters          | uncertain_interpretable | 9.4        | low            | low            |             0.62 |
|        138 | Expressing Heartfelt Gratitude          | uncertain_interpretable | 3.1        | low            | medium         |             0.65 |
|        144 | Moving on to The Next Destination       | uncertain_interpretable | 8.5        | low            | medium         |             0.75 |
|        147 | Painting A House to Sell                | uncertain_interpretable | 6.1b       | low            | medium         |             0.72 |
|        160 | Watching Movies Together                | uncertain_interpretable | 4.2        | low            | low            |             0.55 |
|        172 | Reporting to The Security Officer       | 6.5                     | 4.6        | medium         | medium         |             0.75 |
|        181 | Handing Off to Someone Else             | uncertain_interpretable | 9.2        | low            | low            |             0.62 |
|        190 | Offering to Get Someone Cleaned Up      | uncertain_interpretable | 4.6        | low            | low            |             0.52 |
|        204 | Promising to Care For Her Sister        | 5.1                     | 4.5        | medium         | medium         |             0.78 |
|        207 | Reluctant Errand Under Duress           | uncertain_interpretable | 3.3        | low            | low            |             0.55 |
|        211 | Casual Offers and Reassurances          | 9.4                     | 9.2        | low            | low            |             0.62 |
|        214 | Demanding to Know What Happened         | 4.6                     | 4.3        | low            | medium         |             0.72 |
|        215 | Confessing A Run of Bad Luck            | uncertain_interpretable | 3.3        | low            | medium         |             0.62 |
|        219 | Waiting For Him to Appear               | uncertain_interpretable | 9.2        | low            | low            |             0.62 |
|        224 | Encouraging Words From An Angel         | 9.2                     | 4.6        | low            | low            |             0.65 |
|        225 | Directed to Take A Seat                 | uncertain_interpretable | 8.3b       | low            | medium         |             0.72 |
|        227 | Cherishing Memories Before Parting      | 4.6                     | 2.5        | low            | low            |             0.62 |
|        234 | Waiting Just Outside The Door           | uncertain_interpretable | 8.5        | low            | low            |             0.72 |
|        236 | Caught Spying By The Fbi                | 7.3                     | 10.3       | low            | medium         |             0.72 |
|        250 | Deflecting Blame For A Problem          | 9.4                     | 9.3        | low            | low            |             0.65 |
|        251 | Remarking on An Age Gap                 | uncertain_interpretable | 3.3        | low            | low            |             0.62 |
|        252 | Declaring Deadly Seriousness            | 9.2                     | 9.1        | low            | low            |             0.62 |
|        258 | Shouting Above The Crowd                | 7.3                     | 9.1        | low            | low            |             0.62 |
|        259 | Chained to The Forest Gate              | 7.1                     | 7.3        | low            | low            |             0.62 |
|        270 | Told to Expect Your Arrival             | uncertain_interpretable | 8.5        | low            | low            |             0.62 |
|        281 | Told to Calm Down First                 | 4.6                     | 3.2        | low            | low            |             0.62 |
|        285 | Confessing Years of Hatred              | 7.1                     | 3.2        | medium         | high           |             0.78 |
|        312 | Travis Brags Before The Rodeo           | uncertain_interpretable | noise      | low            | low            |             0.62 |
|        319 | Confessing A Costly Mistake             | 4.5                     | 4.3        | medium         | medium         |             0.72 |
|        327 | Crouching Over A Fallen Figure          | uncertain_interpretable | 7.3        | low            | medium         |             0.65 |
|        334 | Confessing Feelings After Three Hours   | 4.5                     | 4.1        | medium         | medium         |             0.78 |
|        336 | Called Out For Being Distracted         | uncertain_interpretable | 9.4        | low            | medium         |             0.72 |
|        340 | Patience Tested Through Small Trials    | uncertain_interpretable | 4.6        | low            | medium         |             0.62 |
|        344 | Fighting His Instincts to Keep Her      | 4.6                     | 3.3        | medium         | low            |             0.65 |

### Reasoning for changed topics

**Topic 21 — Deciding Whether to Stay or Leave**  
`uncertain_interpretable` -> `9.2` (evidence low -> low, confidence 0.62)

> EVIDENCE: "you'll never leave me" — Three snippets all use future-tense vow/threat wording about staying or departing. Shortlist: (1) 9.2 promise/vow/future-tense speech acts — fits the formal pattern of 'i'll stay / i'll leave / you'll never leave'; (2) 4.5 reconciliation/commitment — lost because no apology, reunion, or HEA act is visible, only the speech-act form; (3) 4.4 conflict/breakup threat — lost because no active relational strain or argument is shown. The keywords 'departure, permission, privacy, terms' reinforce a negotiation-of-leaving register rather than a concrete relational event. 9.2 is the best fit as a discourse-level pattern. use_in_macro_axes=false per boundary rules for 9.x; use_in_theory_watchlist=true because the 'never leave me' phrasing may be relevant to possessive-control or commitment patterns.

**Topic 30 — Leading A Horse Into The Barn**  
`uncertain_interpretable` -> `8.5` (evidence low -> medium, confidence 0.78)

> EVIDENCE: "lead bess into the barn, i'll show you how to take the saddle and bridle off" — Three snippets consistently show horse-handling and movement into a barn. Shortlist: 8.5 (movement/transit), 1.5 (physical activity/training), 4.2 (bonding through shared activity). Runner-up 4.2 lost because no relational bonding or courtship function is visible; the instruction is practical, not romantic. Runner-up 1.5 lost because the activity is animal husbandry/transit rather than exercise or athletic movement. 8.5 fits best as movement of a horse into a stable space, with 8.1 as secondary for the domestic barn setting. No hypothesis-relevant evidence present, so macro axes false.

**Topic 33 — Werewolf Pack Confrontation**  
`7.3` -> `10.1` (evidence low -> medium, confidence 0.78)

> EVIDENCE: "take your woman and leave—i'll handle the vaile wolves" — This snippet shows a paranormal creature confrontation (wolves as supernatural threat) with one character sacrificing himself to protect others. Shortlist: 10.1 paranormal subgenre marker, 7.3 external danger/crisis, 4.6 protective caretaking. 7.3 lost as secondary because the paranormal creature vocabulary is the dominant framing rather than a generic crisis. 4.6 lost as main because the protective act is brief and subordinate to the wolf-pack confrontation machinery. Runner-up 7.2 (deliberate threats/violence) is plausible given 'capture' and 'threats' keywords but the scene reads as crisis/danger rather than deliberate coercive harm. 10.1 is context-only so use_in_macro_axes=false; theory watchlist true for paranormal protective-sacrifice pattern.

**Topic 35 — Remarking on Someone's Age**  
`uncertain_interpretable` -> `8.4` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i've always had to pretend to be twenty-two, whatever that meant for the time i was living in" — Snippets consistently reference age, temporal passage, and how time changes people. Shortlist: 8.4 (time/temporal framing), 3.3 (ambivalence/internal conflict), uncertain_interpretable. Runner-up 3.3 lost because the snippets show observation about age and time rather than internal indecision about a relationship choice. Runner-up uncertain_interpretable was considered but 8.4 is nameable: the topic coheres around temporal markers and age-as-time-passage. Keywords like 'decades,' 'reminder,' and 'uncertain' loosely support temporal framing. No hypothesis-relevant romance content is visible, so use_in_macro_axes=false. Evidence quality is low because snippets are sparse and keywords are generic.

**Topic 43 — Pissed Off and Grumbling**  
`3.2` -> `4.4` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "i've been pissed at him ever since" — Three snippets show characters acknowledging they have angered each other and nursing lingering resentment. Shortlist: 4.4 (couple conflict/distancing), 7.1 (non-romantic interpersonal conflict), 3.2 (negative emotions/distress). 7.1 lost because the exchange is mutual and bidirectional ('pissed at him', 'pissed him off', 'irritated you'), suggesting a relational dynamic rather than one-sided antagonism from an external figure. 3.2 lost because the dominant beat is the conflict exchange itself, not internal suffering. Keywords (upset, sadness, distress, embarrassing) reinforce emotional distress as secondary. Stage08 axis_hint is no_hypothesis_signal but snippets show clear relational conflict, so macro axes is warranted.

**Topic 52 — Talking About Dogs and Animals**  
`uncertain_interpretable` -> `4.2` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i'll be taking the dogs out for their afternoon walk, so there'll be some peace and quiet for you" — Keywords source used as secondary. Shortlist: (1) 4.2 everyday relational bonding — characters sharing domestic/leisure routines; (2) 8.2 public/leisure/outdoor space — camping/bear context; (3) uncertain_interpretable — topic is coherent but thin on relational function. 4.2 edges out uncertain_interpretable because the snippets show characters coordinating care and conversation in a shared space, which is everyday companionship. 8.2 is secondary for the outdoor/camping setting. Runner-up uncertain_interpretable lost because the topic is nameable as casual relational interaction even if weak. No axis-bearing evidence visible — no desire, conflict, commitment, or care act — so use_in_macro_axes=false.

**Topic 54 — Ordering Food and Dessert**  
`8.2` -> `4.2` (evidence medium -> medium, confidence 0.72)

> EVIDENCE: "we'll need a hazmat crew to clean up the mess he'll make with the cake" — Snippets show characters ordering food together and joking at a table. Shortlist: 4.2 (ongoing courtship/everyday bonding), 8.2 (public/leisure space), 9.3 (humor/banter). 8.2 lost because the relational shared-meal function slightly dominates the location framing. 9.3 lost because the humor is incidental to the dining scene rather than the dominant register. 4.2 wins as the closest fit for shared companionable activity, but no deepening trust or courtship escalation is visible in snippets, so use_in_macro_axes=false per the hypothesis-relevance gate.

**Topic 91 — Arguing Over Guns and Weapons**  
`7.2` -> `7.1` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "i don't like guns, they're only for bad things, and all they do are hurt people" — One snippet shows a character objecting to weapons while another prepares to arm themselves. Shortlist: 7.1 (interpersonal non-romantic conflict), 7.2 (violence/threats), 4.4 (main-couple conflict). Runner-up 7.2 lost because no actual violence, threat, or coercion occurs — only an argument about weapons. Runner-up 4.4 lost because there is no evidence this is a main-couple romantic dispute. The scene is an interpersonal disagreement about firearms, fitting 7.1. No hypothesis-relevant romantic content is visible, so use_in_macro_axes=false.

**Topic 92 — Heart Pounding With Dread**  
`1.1` -> `3.2` (evidence medium -> medium, confidence 0.78)

> EVIDENCE: "lizzie's heart pounded wildly as she braced herself for the assault" — Two snippets show fear, dread, and internal distress as the dominant beat. Shortlist: 3.2 (negative emotions/distress), 7.3 (external danger/crisis), 1.1 (bodily reaction). 7.3 lost because no concrete external crisis event is described — the danger is anticipated but unnamed, making the emotional state rather than the crisis the semantic center. 1.1 lost because the bodily reaction (pounding heart) is the vehicle for the emotional distress, not the topic's center. Snippet 3 introduces a calming contrast (ceremony, hand in hand) but does not override the dominant fear register. 3.2 is axis-bearing for H5 (darkness/conflict/threat vs tenderness), so use_in_macro_axes=true.

**Topic 97 — Uncomfortable Silence Falls Over Group**  
`uncertain_interpretable` -> `9.3` (evidence low -> medium, confidence 0.62)

> EVIDENCE: "the other guests in the group, two couples it would seem, had stopped talking and began to shuffle uncomfortably" — Three snippets converge on uneasy group silence as the scene's dominant feature. Shortlist: (1) 9.3 humor/banter/register — fits as a register/atmosphere marker, though this is tense rather than light; (2) 4.4 conflict/distance — lost because no main-couple argument or relational strain is visible, just ambient social discomfort; (3) 8.2 public/leisure space — lost because the location is not the topic's subject. 9.3 is the closest available label for a social-register/atmosphere beat that lacks a clearer thematic function. Secondary 1.1 captures the embodied discomfort ('shuffle uncomfortably', 'breaths'). No hypothesis-relevant evidence visible, so macro false.

**Topic 103 — Last Honest Conversation Before Parting**  
`4.4` -> `1.7` (evidence low -> low, confidence 0.62)

> EVIDENCE: "jake, you'll get a copy?" — All three snippets are anchored to the name Jake with no consistent scene content. Runner-up 4.4 (conflict/distance) lost because no relational strain or breakup is visible; runner-up 9.2 (promise/vow speech) lost because the farewell line is isolated and the other snippets are logistical. The keyword set (dump, session, concrete, smirk) does not converge with the snippets at all, suggesting a poorly coherent topic. Classified as character_name_cluster noise. Post-heuristic: main 'noise' -> '1.7'.

**Topic 120 — Suggesting Someone Take A Shower**  
`8.3b` -> `8.1` (evidence medium -> medium, confidence 0.78)

> EVIDENCE: "maybe if you go jump in the shower, you'll feel better" — All three snippets center on shower access as a practical domestic act. Shortlist: 8.1 (domestic space/routine), 4.6 (reassurance/caretaking), 4.2 (relational bonding). 4.6 lost because no active caretaking or emotional reassurance is visible beyond a casual suggestion; 4.2 lost because snippet 3's negotiation of a break from intimacy is too thin to establish courtship bonding as the dominant function. 8.1 wins as the domestic-routine framing dominates. Secondary 8.3b covers the everyday props vocabulary (curtain, suitcase, temperature). Stage08 axis_hint is no_hypothesis_signal, consistent with context-only assignment. use_in_macro_axes=false per boundary rules for 8.x.

**Topic 121 — Revealing Plans to The Prince**  
`10.2` -> `4.3` (evidence medium -> medium, confidence 0.72)

> EVIDENCE: "if i let the prince know what is happening, instead of waiting for them to find out" — This snippet directly shows a character managing hidden information and deciding whether to reveal it, which is the core of 4.3 (secrets/hidden information). Runner-up 6.5 (institutional settings/procedures) lost because the dominant function is the information-management dilemma, not institutional procedure itself. Runner-up 3.3 (ambivalence) lost because the deliberation is specifically about concealed facts rather than free-floating indecision. Keywords 'magical', 'century', 'commander', and 'king/queen/prince' vocabulary in snippets point to a fantasy or historical-adjacent subgenre (10.2 secondary). No main-couple romantic relationship is visible, so use_in_macro_axes=false despite 4.3 being axis-bearing.

**Topic 136 — Declaring Nothing Else Matters**  
`uncertain_interpretable` -> `9.4` (evidence low -> low, confidence 0.62)

> EVIDENCE: "none of it mattered to me anymore" — All three snippets are variants of the same dismissive self-talk formula, suggesting a discourse-level interior monologue pattern rather than a scene with identifiable thematic content. Shortlist: (1) 9.4 interior monologue/self-talk — fits best as a repeated rhetorical particle of dismissal; (2) 3.3 ambivalence — possible if the dismissal signals internal conflict, but no competing desires or relationship choice is visible; (3) uncertain_interpretable — considered but 9.4 is nameable here since the pattern is clearly a self-talk/dismissal register. Runner-up 3.3 retained as secondary because the dismissal could reflect emotional ambivalence. Keywords 'identity, bigger, experience' are too sparse to override the snippet evidence. Stage08 axis_hint is no_hypothesis_signal, consistent with context-only assignment. use_in_macro_axes=false per 9.x rule.

**Topic 138 — Expressing Heartfelt Gratitude**  
`uncertain_interpretable` -> `3.1` (evidence low -> medium, confidence 0.65)

> EVIDENCE: "i want to tell you how much i appreciate everything you've done for me" — All three snippets center sincere gratitude and acknowledgment of effort. Shortlist: 3.1 (emotional payoff/relief), 4.6 (caretaking/reassurance), 4.2 (ongoing bonding). 4.6 lost because nobody is actively protecting or reassuring; the speaker is expressing gratitude, not receiving care. 4.2 lost because the scene is a discrete emotional beat of appreciation, not ongoing courtship or companionship. 3.1 wins as the felt emotional payoff of acknowledged effort. Keywords diverge from snippets (sir, lid, disappointment suggest a different register) lowering confidence, but snippet evidence takes priority per evidence discipline. use_in_macro_axes=true because gratitude/emotional payoff is hypothesis-relevant for H1/H5.

**Topic 144 — Moving on to The Next Destination**  
`uncertain_interpretable` -> `8.5` (evidence low -> medium, confidence 0.75)

> EVIDENCE: "she'd be on the road to some other waterside destination to secure the next sale" — Three snippets all center movement between places: settling in London, disappearing, relocating. Runner-up 3.3 (ambivalence/internal conflict) lost because while there is mild uncertainty ('uncertain about what she leaves'), no relationship choice or competing desires are foregrounded — the topic is about physical/spatial transition, not emotional deliberation. Runner-up 4.2 lost because no relational bonding or courtship function is visible. The 'series' reference in snippet 1 (lovestruck series) is paratext-adjacent but the snippet also contains narrative content, so not noise. 8.5 movement/transit is the most specific context ID that fits; 8.2 public/leisure spaces is secondary given the destination framing. No hypothesis-relevant evidence visible, so macro axes false.

**Topic 147 — Painting A House to Sell**  
`uncertain_interpretable` -> `6.1b` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "slap on some paint and get it listed with a real-estate agent" — The scene centers a practical plan to prepare and sell a property. Shortlist: 6.1b (generic business/institutional logistics), 6.4 (economic precarity), 8.2 (public/leisure space). 6.4 lost because no rent, debt, or can't-afford vocabulary appears; this is a sale plan, not financial distress. 8.2 lost because the property is an object of transaction, not a leisure or public setting being visited. 6.1b wins as the closest fit for generic property/business logistics. Snippet 1 ('paint yourself black… I will do anything for you') is tonally different and may belong to a different context, but snippet 3 anchors the dominant scene function. No romantic mechanics visible; macro axes false.

**Topic 160 — Watching Movies Together**  
`uncertain_interpretable` -> `4.2` (evidence low -> low, confidence 0.55)

> EVIDENCE: "we've been watching movies" — from keywords and snippet 3, shared leisure activity is present. Shortlist: 4.2 (everyday relational bonding/companionship), 8.2 (public/leisure space), uncertain_interpretable. Runner-up 8.2 lost because the relational function of watching together slightly edges out pure location framing. However, snippet 2 ('watching him closely for any reaction') introduces a surveillance or caretaking register that does not fit 4.2 cleanly — this could be 4.6 or 10.3 context. Evidence is too thin and mixed to be confident; no kiss, hug, or courtship act appears, so macro axes are not warranted. Stage08 axis_hint is no_hypothesis_signal, consistent with context-only assignment.

**Topic 172 — Reporting to The Security Officer**  
`6.5` -> `4.6` (evidence medium -> medium, confidence 0.75)

> EVIDENCE: "i'll have an armed officer [person] the room with you at all times" — This snippet shows a security/danger response with armed oversight. Runner-up 7.2 (violence/threats) lost because the scene depicts institutional response to a threat rather than active violence or direct coercion. Runner-up 10.3 (mystery/investigation) lost because the framing is security protocol and crisis management rather than detective investigation. 6.5 is secondary because the scene operates through institutional procedure (police, security officer, reporting chain). No romantic hypothesis signal is present, so use_in_macro_axes=false, but the external-threat mechanic and institutional framing make it theory-watchlist relevant. Post-heuristic: main '7.3' -> '4.6'.

**Topic 181 — Handing Off to Someone Else**  
`uncertain_interpretable` -> `9.2` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i'll leave it to [person] to continue again now" — Snippets show repeated future-tense delegation speech acts (handing off, approving, being frank). Shortlist: 9.2 (promise/future-tense speech acts), 6.1b (institutional logistics), uncertain_interpretable. 6.1b lost because there is no business deal or contract vocabulary. uncertain_interpretable was considered but 9.2 fits better as the pattern is clearly future-tense delegation wording as a discourse form. Runner-up 6.1b noted in other_plausible_ids. No hypothesis-relevant evidence visible; axis false. Keywords like 'affection' and 'hopeful' do not appear in snippets and cannot override snippet evidence per evidence discipline rules.

**Topic 190 — Offering to Get Someone Cleaned Up**  
`uncertain_interpretable` -> `4.6` (evidence low -> low, confidence 0.52)

> EVIDENCE: "i'll get her cleaned up, said a handsome groom, taking her arm" — One snippet shows a caretaking offer with a relational figure (groom). Runner-up 4.2 (courtship/bonding) lost because the act is a practical cleanup gesture rather than relational bonding or companionship. Runner-up uncertain_interpretable was considered because keywords (sweeping, dump, suitcase, parties) diverge sharply from snippets, but the snippets themselves are coherent enough to name a function. 4.6 wins narrowly as the closest thematic fit for a minor caretaking/reassurance act. Not axis-bearing: no hypothesis-relevant evidence of protection, care depth, or relational repair visible.

**Topic 204 — Promising to Care For Her Sister**  
`5.1` -> `4.5` (evidence medium -> medium, confidence 0.78)

> EVIDENCE: "i'll find a way to care for your mother and your sister" — One snippet shows a direct vow of care for family members framed as a commitment act. Runner-up 4.6 lost because the scene is not primarily local reassurance or caretaking in the moment; it is a forward-looking pledge that marks relationship commitment, placing it at 4.5. Runner-up 9.2 lost because the promise wording here carries real relational weight (future family incorporation) rather than being a discourse-level speech-act pattern. The 'soon you'll be my sister' snippet confirms couple-recognition movement. Keywords (enthusiasm, affection, willing) weakly support a positive relational register but snippets are the primary evidence. Family context (5.1) is secondary. Stage08 axis_hint 'no_hypothesis_signal' is overridden by snippet evidence showing a commitment vow.

**Topic 207 — Reluctant Errand Under Duress**  
`uncertain_interpretable` -> `3.3` (evidence low -> low, confidence 0.55)

> EVIDENCE: "i'll just jump right into it and hold [person] in front of me like a shield" — Snippets show a character grudgingly carrying out an unwanted task while using others as cover, with grumbling and resignation. Shortlist: 3.3 (ambivalence/reluctant compliance), 7.1 (non-romantic conflict/antagonism), 4.3 (secrets/hidden motives). 7.1 lost because no clear antagonistic conflict between named parties is visible — the resistance is internal. 4.3 lost because no withheld information or misunderstanding drives the scene. 3.3 fits best as reluctant internal conflict under duress. No romantic, sexual, or HEA content visible; axis_hint is no_hypothesis_signal; use_in_macro_axes=false.

**Topic 211 — Casual Offers and Reassurances**  
`9.4` -> `9.2` (evidence low -> low, confidence 0.62)

> EVIDENCE: "we've got this, right ab?" — Three snippets show casual reassurance speech acts ('I've got it', 'we've got this'). Shortlist: 9.2 promise/vow speech acts, 9.4 self-talk particles, uncertain_interpretable. 9.4 lost because these are not filler particles or fragmented inner monologue but outward speech acts. uncertain_interpretable was considered but the discourse function is nameable as informal reassurance/promise wording (9.2), even if weak. No romantic, relational, or thematic content is visible, so no primary axis category applies. Stage08 axis_hint is no_hypothesis_signal, consistent with context-only discourse. use_in_macro_axes=false; use_in_theory_watchlist=false given minimal interpretive value.

**Topic 214 — Demanding to Know What Happened**  
`4.6` -> `4.3` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "i need to know what's going on to some extent so i don't think the worst" — This fragment shows a character pressing for hidden information because they fear what they don't know, which is the core of 4.3 (secrets, misunderstandings, hidden information). Shortlist: 4.3 (information asymmetry/withheld truth), 4.4 (conflict/distance), 4.6 (reassurance/caretaking). Runner-up 4.4 lost because the scene is not active conflict between the couple but rather a demand to close an information gap. Runner-up 4.6 lost because the speaker is seeking information, not offering comfort or protection. The fear-of-worst framing adds a 3.2 distress secondary. Evidence is medium: three snippets converge on the same urgent-demand-for-information function, but keywords are sparse and no resolution is visible.

**Topic 215 — Confessing A Run of Bad Luck**  
`uncertain_interpretable` -> `3.3` (evidence low -> medium, confidence 0.62)

> EVIDENCE: "i've had a bit of bad luck at cards lately" — Three snippets converge on a confession of repeated misfortune at cards, with a second character acknowledging it. Shortlist: 3.3 (ambivalence/admission of difficulty), 4.3 (hidden information/secret), 9.4 (self-talk discourse). Runner-up 4.3 lost because the character is openly confessing rather than concealing information — there is no secret or misunderstanding being maintained. Runner-up 9.4 lost because this is substantive dialogue content, not mere discourse particles. 3.3 fits as situational acknowledgment of a difficult streak, though the romantic stakes are not visible in snippets. Axis hint is no_hypothesis_signal and no romantic mechanic is evident, so use_in_macro_axes=false. use_in_theory_watchlist=true as a potential setup for economic precarity or relationship complication.

**Topic 219 — Waiting For Him to Appear**  
`uncertain_interpretable` -> `9.2` (evidence low -> low, confidence 0.62)

> EVIDENCE: "one day he'll appear" — All three snippets are future-tense anticipatory statements about an absent man's return. Shortlist: 9.2 (future-tense speech acts/anticipation), 4.3 (secrets/hidden information about someone), 8.4 (temporal waiting/anticipation). Runner-up 4.3 lost because there is no visible secret or withheld information — just expectation of arrival. Runner-up 8.4 lost because the topic is more about the speech-act pattern of anticipation than temporal framing itself. Keywords (departure, options, terms, explanation, permission) are generic and do not anchor a stronger thematic category. No hypothesis-relevant evidence visible, so macro false.

**Topic 224 — Encouraging Words From An Angel**  
`9.2` -> `4.6` (evidence low -> low, confidence 0.65)

> EVIDENCE: "i'll come back, angel" — from snippet 1 (label source). Shortlist: 4.6 (reassurance/caretaking), 4.5 (commitment/promise), 9.2 (future-tense speech act). 4.5 lost because the promise of return is local reassurance rather than a major commitment or HEA act. 9.2 lost because the dominant function is emotional reassurance and encouragement, not merely the formal wording of a vow. 4.6 wins as the scene centers on verbal reassurance and emotional support. Secondary 9.2 captures the future-tense promise wording. Evidence quality is low because snippets are very short and context is thin; confidence is moderate. use_in_macro_axes=true because reassurance/caretaking is axis-bearing under H4.

**Topic 225 — Directed to Take A Seat**  
`uncertain_interpretable` -> `8.3b` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "just take a seat in my chair, and i'll be right there" — All snippets show a simple directive to sit and wait, with chairs as the central prop. Shortlist: 8.3b (everyday prop/scene mechanic), 8.2 (public/leisure space), uncertain_interpretable. Runner-up 8.2 lost because no location setting dominates — the focus is the prop (chair) and the act of waiting, not a named public space. Runner-up uncertain_interpretable lost because the topic is coherent and nameable as an ordinary prop/scene-mechanic interaction. 8.3b fits as the most specific context ID for everyday props serving as scene mechanics only. No hypothesis-relevant evidence visible; macro axes false.

**Topic 227 — Cherishing Memories Before Parting**  
`4.6` -> `2.5` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i'll be taking these memories with me and pulling them out when i'm missing everyone so much" — This snippet shows a character cherishing relational bonds before parting, which is ongoing courtship/bonding (4.2). Runner-up 4.5 lost because no proposal, reconciliation, or explicit love declaration occurs; the departure is emotionally significant but not a commitment act. Runner-up 4.6 lost because the care expressed is diffuse and mutual rather than one partner actively reassuring or caretaking the other. The amnesia thread (snippets 1-2) adds a secondary distress/vulnerability note (3.2) but does not override the dominant parting-bonding function. Stage08 axis_hint is no_hypothesis_signal and no explicit romance mechanic is visible, so use_in_macro_axes=false. Evidence quality is low because snippets are short and the relational context is ambiguous. Post-heuristic: main '4.2' -> '2.5'.

**Topic 234 — Waiting Just Outside The Door**  
`uncertain_interpretable` -> `8.5` (evidence low -> low, confidence 0.72)

> EVIDENCE: "i'll wait for you outside" — (from snippet 2, label source). Shortlist: 8.5 (waiting/threshold/transit), 4.2 (courtship bonding), uncertain_interpretable. Runner-up 4.2 lost because no bonding, shared activity, or emotional closeness appears in any snippet; the character is simply positioning themselves outside. Runner-up uncertain_interpretable lost because the spatial-transition function is nameable even if thin. Keywords 'anxious' and 'destination' could hint at emotional or purposive content but no snippet confirms a relational or thematic function beyond waiting outside. Stage08 axis_hint is no_hypothesis_signal, consistent with context-only assignment. use_in_macro_axes=false per boundary rules for 8.x.

**Topic 236 — Caught Spying By The Fbi**  
`7.3` -> `10.3` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "he suspected he would've been released earlier in the day if not for the fbi" — Snippet shows FBI detention tied to an investigation. Shortlist: 10.3 (mystery/investigation machinery), 7.3 (external danger/crisis), 7.2 (deliberate threat/coercion). 7.2 lost because the detention appears procedural/investigative rather than a direct violent threat. 7.3 is secondary because the FBI involvement frames an external crisis around the character. 10.3 wins as the dominant subgenre machinery — surveillance, spying accusation, federal investigation. Runner-up 6.5 (institutional procedures) lost because the investigative/suspense function is more specific than generic institutional procedure. No romantic content visible, so use_in_macro_axes=false.

**Topic 250 — Deflecting Blame For A Problem**  
`9.4` -> `9.3` (evidence low -> low, confidence 0.65)

> EVIDENCE: "how's that my issue?" — from keywords and snippets. Shortlist: 9.3 (banter/deflection register), 4.4 (conflict/blame between characters), 3.3 (ambivalence/indecision). The snippets show short deflecting remarks trading blame, which is a discourse pattern of light-register blame-deflection rather than serious relational conflict. 4.4 lost as main because the tone is deflecting/banter rather than genuine breakup-threat or emotional withdrawal; it is retained as secondary for the mild tension. 3.3 lost because no internal indecision is visible — the characters are deflecting outward, not deliberating internally. 9.3 fits best as a discourse-level pattern of blame-deflection with mild anxiety. Stage08 axis_hint is no_hypothesis_signal, consistent with context-only assignment. use_in_macro_axes=false; use_in_theory_watchlist=true as a discourse pattern worth noting.

**Topic 251 — Remarking on An Age Gap**  
`uncertain_interpretable` -> `3.3` (evidence low -> low, confidence 0.62)

> EVIDENCE: "their age difference was outrageous, which prompted her to ask, 'but why now, your grace?'" — This snippet shows a character questioning a significant age gap in what appears to be a romantic or quasi-romantic context, suggesting ambivalence or internal conflict (3.3). Runner-up 4.2 lost because there is no courtship bonding act visible; the question is one of hesitation and uncertainty. Runner-up 1.6 lost because the aging descriptions are not primarily about appearance/grooming but about structural and relational age. The axis_hint is no_hypothesis_signal and evidence is thin across snippets, so use_in_macro_axes=false despite 3.3 being exploratory-axis-eligible.

**Topic 252 — Declaring Deadly Seriousness**  
`9.2` -> `9.1` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i've never been more fucking serious in my life" — All three snippets are variants of the same emphatic speech-act formula, suggesting a discourse cluster around a repeated verbal intensity marker. Shortlist: (1) 9.1 dialogue delivery/speech tags — fits because the topic captures how something is said (with fierce conviction) rather than what is being said; (2) 9.4 interior monologue/self-talk — lost because these are spoken declarations, not internal fragments; (3) uncertain_interpretable — considered because no subject matter is visible, but the discourse function (emphatic assertion of seriousness) is nameable as a speech-delivery pattern, so 9.1 is preferred over uncertain_interpretable. Keywords (comments, spite, issue, members) add no thematic signal. No hypothesis-relevant content visible, so macro false.

**Topic 258 — Shouting Above The Crowd**  
`7.3` -> `9.1` (evidence low -> low, confidence 0.62)

> EVIDENCE: "she barely heard herself, everything except for her connection to him seemed like background noise" — Shortlist: 9.1 (speech/vocal delivery mechanics), 7.3 (external crisis/danger), 3.2 (distress). The shouting and vocal strain vocabulary ('shouted', 'lungs', 'gasp') point to 9.1 as the discourse-level function. Runner-up 7.3 is plausible given 'creatures', 'crowd', 'pounding' suggesting chaotic danger, but no clear crisis event is described in snippets — only the vocal/sensory experience of shouting. 3.2 lost because distress is not the dominant beat; the character is shouting urgently, not suffering internally. The paranormal keyword 'creatures' is noted but insufficient to override. Context-only category, macro false.

**Topic 259 — Chained to The Forest Gate**  
`7.1` -> `7.3` (evidence low -> low, confidence 0.62)

> EVIDENCE: "miss [person], it appears you've chained yourself to the door of white pines" — This snippet directly describes a protest action: chaining to a door after living in a tree. Shortlist: 7.3 (external crisis/risk), 7.1 (interpersonal conflict with authority), 5.3b (community/social event). 7.3 wins because the protest creates an external crisis situation involving risk and confrontation with institutional authority. 7.1 lost because the conflict is not clearly between named interpersonal antagonists but rather a person vs. institution. 5.3b lost because this is not a social gathering or gossip event. No romantic mechanics are visible; axis false. The 'surprise in the woods' snippet adds an outdoor/public setting dimension but no romantic function.

**Topic 270 — Told to Expect Your Arrival**  
`uncertain_interpretable` -> `8.5` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i've been expecting you" — from snippets (source: snippet text). Shortlist: (1) 8.5 movement/arrival — fits the threshold greeting; (2) 4.1 first contact — possible if this is a meet-cute, but no romantic framing is visible; (3) uncertain_interpretable — possible given sparse evidence. Runner-up 4.1 lost because no romantic or introductory courtship function is visible; the phrasing is purely logistical announcement of arrival. Keywords 'meantime' and 'worst' provide no thematic signal. Stage08 axis_hint is no_hypothesis_signal, consistent with context-only. 8.5 is the most specific nameable context ID for an arrival/threshold scene. macro_axes false because transit context is not axis-bearing.

**Topic 281 — Told to Calm Down First**  
`4.6` -> `3.2` (evidence low -> low, confidence 0.62)

> EVIDENCE: "i've really helped relax, comfort and ease anger and rage with these guys" — Keywords and snippets converge on emotional distress and calming. Shortlist: 3.2 (negative emotions/distress), 4.6 (reassurance/caretaking), 9.1 (speech delivery). 4.6 lost as main because the focus is on the emotional state itself rather than a partner actively caretaking; the distress is the center. 9.1 lost because the topic is about emotional content, not speech mechanics. Runner-up 3.3 considered for ambivalence but no competing desires are visible — this is anger/urgency being managed. Third snippet 'not been relieved of my post' suggests a professional/institutional context but is too isolated to redirect the mapping. Evidence quality is low given short, decontextualized snippets.

**Topic 285 — Confessing Years of Hatred**  
`7.1` -> `3.2` (evidence medium -> high, confidence 0.78)

> EVIDENCE: "i've hated him for living instead of you" — Three snippets independently show sustained hatred, resentment, and emotional destabilization. Shortlist: 3.2 (negative emotions/distress), 7.1 (interpersonal non-romantic conflict), 4.4 (couple conflict/distance). 4.4 lost because no main-couple romantic relationship is indicated; the hatred is directed at a third party. 7.1 is a strong secondary because the confession is addressed to an antagonistic interpersonal dynamic. 3.2 wins as main because the dominant beat is the character's internal emotional state — years of hatred, imbalance, and buried reasons to despise — rather than an active confrontation scene. Stage08 axis_hint is no_hypothesis_signal and no romantic hypothesis is visible, so use_in_macro_axes=false. Theory watchlist true because the emotional confession pattern is interpretively interesting.

**Topic 312 — Travis Brags Before The Rodeo**  
`uncertain_interpretable` -> `noise` (evidence low -> low, confidence 0.62)

> EVIDENCE: "you'll never find travis" — The three snippets share only the character name Travis; their contexts are unrelated (reunion anticipation, rodeo brag, threat). Keywords like 'elevator', 'wrists', 'tv', 'screen' contradict the rodeo label entirely, confirming this is a name-anchored residual cluster. Runner-up uncertain_interpretable lost because the incoherence stems from topic-model noise around a character name rather than a coherent-but-unnameable semantic domain. Runner-up 9.3 (banter/humor) lost because the snippets do not share a consistent register. is_noise=true is warranted.

**Topic 319 — Confessing A Costly Mistake**  
`4.5` -> `4.3` (evidence medium -> medium, confidence 0.72)

> EVIDENCE: "i've made many mistakes and maybe i should have come back a year ago" — Three snippets converge on a character admitting a costly error with relational consequences. Shortlist: 4.3 (secrets/misunderstandings — past error withheld or unaddressed), 4.5 (reconciliation — confession as repair act), 4.4 (conflict — the mistake caused distance). 4.5 lost because no forgiveness, proposal, or explicit repair resolution occurs; the scene is the admission itself, not the outcome. 4.4 lost because no active argument or breakup threat is visible. 4.3 wins because the dominant function is disclosure of a hidden/unaddressed error that has shaped the relationship. trust_repair and secret_misunderstanding tags apply. Axis-bearing because the confession is hypothesis-relevant for H6 (conflict/miscommunication vs repair).

**Topic 327 — Crouching Over A Fallen Figure**  
`uncertain_interpretable` -> `7.3` (evidence low -> medium, confidence 0.65)

> EVIDENCE: "the wings lifted and spread behind her" — This paranormal detail anchors the scene in a crisis/danger moment with supernatural elements. Shortlist: 7.3 (external crisis/danger), 7.2 (deliberate violence/threat), 4.6 (caretaking over fallen person). 7.2 lost because no deliberate aggressor or explicit threat act is visible — the crouching posture is ambiguous between protective and predatory. 4.6 lost because the scene reads as tense/dangerous rather than reassuring or caretaking. 10.1 is secondary for the paranormal creature vocabulary. No hypothesis-relevant romantic function is clearly visible, so use_in_macro_axes=false despite 7.3 being axis-bearing.

**Topic 334 — Confessing Feelings After Three Hours**  
`4.5` -> `4.1` (evidence medium -> medium, confidence 0.78)

> EVIDENCE: "i've never felt this way before" — This is a direct early-relationship confession after a very short acquaintance, anchoring the scene in first-contact romantic setup (4.1). Runner-up 4.5 lost because this is not a reconciliation, proposal, or HEA commitment — it is an initial declaration of feeling at the very start of a relationship, not a repair or formal commitment act. Runner-up 2.1 lost because the snippet is verbal confession rather than erotic tension or charged physical desire. The third snippet about Caroline's cars adds relational context suggesting ongoing courtship logistics (4.2 secondary). The axis hint says no_hypothesis_signal but the snippet evidence clearly shows early romantic confession relevant to H1/H2, so use_in_macro_axes=true.

**Topic 336 — Called Out For Being Distracted**  
`uncertain_interpretable` -> `9.4` (evidence low -> medium, confidence 0.72)

> EVIDENCE: "hey, man, you've been distracted all morning" — Snippets show characters observing or apologizing for preoccupation, with no visible subject matter for the distraction. Shortlist: 3.3 (ambivalence/internal conflict) lost because no relationship choice or competing desires are visible; uncertain_interpretable lost because the discourse pattern is nameable as a self-talk/interior-state register even if the cause is unknown. 9.4 covers fragmented inner monologue and stylistic markers of internal narration, which fits the repeated distraction-observation pattern. No hypothesis-relevant evidence visible, so macro false and watchlist false.

**Topic 340 — Patience Tested Through Small Trials**  
`uncertain_interpretable` -> `4.6` (evidence low -> medium, confidence 0.62)

> EVIDENCE: "her patience throughout the meal with the girls never wavered, not with spilled drinks, sloppy faces" — This snippet shows active caretaking and emotional steadiness toward children, pointing to 4.6 (caretaking/emotional safety). Runner-up 3.1 lost because the beat is not resolved relief after strain but ongoing patient endurance. Runner-up 4.2 lost because the relational bonding function is not clearly courtship. Snippet 3 hints at restrained romantic longing toward a coworker ('christmas elf'), which adds a faint 2.1 undertone, but the dominant observable function across all three snippets is patient caretaking and resilience. 5.1 is secondary because snippet 2 centers children. Stage08 axis_hint is no_hypothesis_signal and no explicit romantic commitment or explicit sex is present, so use_in_macro_axes=false.

**Topic 344 — Fighting His Instincts to Keep Her**  
`4.6` -> `3.3` (evidence medium -> low, confidence 0.65)

> EVIDENCE: "it goes against all of josh's instincts, but if it means he can keep his mate" — This fragment shows internal conflict between instinct and relational choice, pointing to 3.3 ambivalence. Shortlist: 3.3 (internal conflict suppressing instincts), 4.6 (caretaking/reassurance), 4.2 (ongoing bonding). Runner-up 4.6 lost because no active caretaking or reassurance act is visible; the focus is on Josh's internal suppression of instinct, not on comforting a partner. Runner-up 4.2 lost because the relational bonding is framed through internal conflict rather than shared activity. The 'mate' keyword flags paranormal_instinct. Snippets 2 and 3 show banter/humor (9.3 register) but do not override the dominant internal-conflict beat. 3.3 is exploratory-only, so use_in_macro_axes=false per boundary rules.


## Still-low evidence quality after re-run

54 topics kept the same category and still report low evidence quality.

|   topic_id | label                                     | new_main                | new_uncertainty_reason                                                                                                                                                                                                                                                                                                                                                                    |
|-----------:|:------------------------------------------|:------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|          4 | Refusing to Be Used                       | 3.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         16 | Leaning Over A Chair                      | uncertain_interpretable | Snippets show physical positioning (leaning, sitting) in a shared space with nervous energy keywords, but no dominant thematic function is identifiable — no clear courtship, conflict, care, desire, or other axis-bearing content is visible.                                                                                                                                           |
|         17 | Discussing Rooms and Privacy              | 8.1                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         20 | Warning About Doing Things Right          | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         36 | Eagerly Offering to Help                  | 4.6                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         40 | Resigned Acknowledgment of Disappointment | uncertain_interpretable | Snippets are fragmentary exclamations and a foraging reference ('find some morels') with no identifiable romantic, relational, or thematic domain; the Stage08 label 'Resigned Acknowledgment of Disappointment' is not supported by the visible snippet content, leaving no reliable semantic center to name.                                                                            |
|         44 | Admitting Something Is Hard               | 3.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         50 | Questioning What You Believe              | 3.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         57 | Hands Raised in Reassuring Gesture        | 1.7                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         73 | Quick Remarks Before Moving on            | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         76 | Demanding to Be Heard                     | 9.1                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         80 | Declaring Exactly What You Want           | 9.4                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         93 | Meal Plans Casually Arranged              | 4.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         95 | Acknowledging How Much Has Changed        | 3.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|         99 | Promises About Forgetting                 | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        108 | Exclaiming How Much Better                | 9.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        110 | Promising to Figure It Out                | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        111 | Adding Plans to The Calendar              | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        127 | Photographer Reviewing Pictures           | 1.6                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        130 | Revealing A Secret Plan                   | 4.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        133 | Holding Back Tears                        | 3.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        150 | Curious Replies and Deflections           | 9.1                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        158 | Mentioning A Friend to Family             | 5.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        168 | Ready to Begin When Told                  | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        169 | Mulling Over A Proposal                   | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        173 | Waiting For Him to Wake                   | 4.6                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        176 | Promising A Good Time                     | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        178 | Pitching A New Business Idea              | 6.1b                    |                                                                                                                                                                                                                                                                                                                                                                                           |
|        180 | Comparing Sizes and Spaces                | uncertain_interpretable | The topic clusters size-comparison language across heterogeneous referents (rooms, bodies, crowds) with no dominant thematic function — not a setting, not appearance, not a social event, not a relationship beat. No single context ID captures the cross-domain size-comparison register.                                                                                              |
|        187 | Admitting Everything Has Gone Wrong       | uncertain_interpretable | Snippets show acknowledgment of failure ('we've messed up everything') and claims of competence ('I've got things handled'), but no subject matter is visible — the domain could be romantic conflict, workplace crisis, family trouble, or something else entirely. Keywords (addition, occasional, regular, task, emotional, pregnant) are incoherent and do not resolve the ambiguity. |
|        198 | Leaning Forward With Impatience           | 1.7                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        202 | Eyes Closed in Concentration              | 1.7                     | The snippets show a woman closing her eyes and concentrating, with one snippet referencing chakra energy work, but the thematic function — whether this is emotional regulation, paranormal ability activation, meditation, or internal conflict — cannot be determined from the available evidence. No relationship, conflict, or romance mechanic is visible.                           |
|        206 | Stepping Back Into Line                   | 8.5                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        221 | Caught Off Guard By Surprises             | uncertain_interpretable | Snippets show only surface-level surprise reactions and a money remark with no identifiable romantic, relational, or thematic domain; the scene summary mentions flushed faces and confusion but no coherent narrative function can be named from the available evidence.                                                                                                                 |
|        226 | Eyes Closed on Command                    | 3.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        232 | Conversation Cut Short By Arrival         | 4.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        235 | Directed to Wash Up                       | 8.1                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        238 | Relaying A Message For Her                | 9.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        239 | Keeping Someone Guarded and Entertained   | 5.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        240 | Unsure How to Offer Comfort               | 4.6                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        241 | Calling Someone A Stubborn Idiot          | 1.6                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        257 | Withholding An Answer                     | 9.4                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        268 | Vivid Colors Remarked Upon                | 1.6                     | Snippets show a character remarking on vivid colors and preserved bodies (possibly museum or archaeological context), but no romance-relevant thematic function — no desire, care, conflict, bonding, or danger — is visible. The topic is coherent as sensory observation but cannot be assigned to any specific taxonomy category.                                                      |
|        276 | Asking For A Moment                       | 9.4                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        278 | Irritation Fading Into Distraction        | 3.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        295 | Comparing Sizes of Things                 | uncertain_interpretable | Snippets show size-comparison vocabulary (smaller, bigger, huge) applied to unspecified objects or spaces, but no thematic domain — character appearance, setting, object, or relationship function — can be reliably identified from the fragments alone.                                                                                                                                |
|        317 | Putting on A Brave Face                   | 3.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        323 | Polite Address Under Distress             | 1.6                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        325 | Pouting and Pleading Remarks              | 9.3                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        330 | Curious About Her Cooking Skills          | 4.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        332 | First Time Inside A Grocery Store         | 4.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        351 | Warm Greeting Upon Return                 | 4.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        357 | Arguing Over The Local Club               | 7.1                     |                                                                                                                                                                                                                                                                                                                                                                                           |
|        367 | Sorting Out Concert Tickets               | 4.2                     |                                                                                                                                                                                                                                                                                                                                                                                           |
