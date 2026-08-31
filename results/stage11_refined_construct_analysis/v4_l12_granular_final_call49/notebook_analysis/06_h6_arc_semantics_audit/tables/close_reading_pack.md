# H6 arc semantics — close-reading pack

## Topic 6 — Whispered Reassurance

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_0 (norm: ARC_0)

> i’ll make sure of it,” he whispered.

> you’ll be fine,” he whispered. “

> quiet, subdued, she nodded and then, “you’ll be safe.”

> *(CELL_D, tertile=end)* Ian stared right back and asked slowly, clearly, enunciating every word, “Who asked you to?”

> *(CELL_D, tertile=middle)* Okay,’ she said, striving for a light tone in the heavy silence. ‘

### Pass A/B/C

- **A lexical:** `ARC_10`
  - All four keyword lists describe speech-act mechanics and vocal/emotional delivery cues (whispered, softly, tentatively, hesitation, drawled, solemnly, eagerly, confessed, mumbled) without anchoring to any specific relational event between a main couple. 'Confessed' and 'tentatively' could hint at disclosure or conflict, but no keyword cluster points clearly to a defined arc function—misunderstanding, conflict, repair, commitment, etc. The vocabulary is generic dialogue-texture language applicable to any scene type. ARC_10 (ambiguous) is therefore the most defensible code across all representations.
- **B contextual:** `ARC_0`
  - Every sentence in this topic is a decontextualized dialogue fragment consisting solely of minimal affirmative or acknowledgment tokens ('Yes,' 'Okay,' 'Oh,' 'she said,' 'she asks,' 'he replies,' etc.) with no surrounding narrative content. There is no identifiable subject matter, no relational dynamic, no character identification, and no arc-relevant content whatsoever. The topic appears to be a BERTopic artifact capturing generic dialogue punctuation and speech-tag patterns rather than any meaningful narrative unit. No sentence can be assigned to the main couple with any confidence, and no relationship state change can be inferred. The topic is uniformly ARC_0 (unrelated) across all narrative positions and should be excluded from H6 arc analyses.
- **C adjudicate:** `ARC_0`
  - The contextual dominant judgment (ARC_0) holds. Taxonomy label 4.6 Emotional Safety, Reassurance & Caretaking and Radway codes R8/R9/R10 (tender hero treatment, heroine's emotional response) describe a general affective register — tenderness and caretaking — rather than a specific arc function that implicates the main couple's relational trajectory. Per critical rules, ARC_7 requires evidence of trust/closeness being *restored or strengthened* (i.e., after rupture), and ARC_8 requires mutual relational commitment/resolution; neither is evidenced here. The Stage11 codes RAX_emotional_reassurance and RAX_tenderness_core confirm a warm tonal quality but do not map to a directional arc event. The taxonomy/Radway/Stage11 labels partially contradict the ARC_0 judgment by suggesting romantic couple involvement, but they do not override it because tenderness alone is insufficient to assign a rising or falling arc role. The lexical consensus of ARC_10 (ambiguous) is understandable but the contextual read of ARC_0 is more defensible: this topic captures ambient emotional texture rather than a couple-level arc beat. Recommended exclusion from H6 hypothesis testing.
- **Action:** EXCLUDE_FROM_HYPOTHESIS

---

## Topic 36 — Eagerly Offering to Help

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_0 (norm: ARC_0)

> of course, i’ll help you.’

> then you’ll let me help,” frances said at once, her expression eager. “

> sure, of course, i’ll help.”

> *(CELL_B, tertile=end)* And you know I’m here to help you in any way I can.”

> *(CELL_D, tertile=middle)* Well make yourself useful,” he said. “

> *(CELL_B, tertile=end)* I’ve got to do something to help.”

### Pass A/B/C

- **A lexical:** `ARC_0`
  - All four keyword lists center on transactional assistance and task-oriented language: 'help, need, assistance, thanks, helped' (Main); 'provided, willing, appreciate, replies, eagerly, requested, task, promptly, sir' (KeyBERT); 'task, options, success, terms, sentence, pleased, excited' (POS); 'mister, promptly, appreciate, eagerly, options, success, intend, insisted, pleased' (MMR). None of these cues implicate the main romantic couple's relationship arc in any way — there is no conflict, disclosure, reconciliation, commitment, or trust dynamic present. The vocabulary is consistent with a service/assistance exchange or procedural interaction entirely unrelated to romantic relationship progression.
- **B contextual:** `ARC_0`
  - Topic 36 consists entirely of generic, decontextualized offers and requests for help ('Can I help you?', 'Let me help you.', 'I'll help.'). These fragments carry no identifiable speaker, recipient, or relational context. There is no evidence that the main romantic couple is implicated in any of these utterances, nor that any romantic relationship state is being changed. The topic appears to be a surface-level linguistic cluster around the word 'help' rather than a meaningful narrative arc element. It is uniformly ARC_0 (unrelated to the main couple's arc) across all three narrative positions, with no variation by tertile. Exclusion from H6 arc analyses is strongly recommended.
- **C adjudicate:** `ARC_0`
  - All three evidence streams — lexical consensus (ARC_0), contextual dominant (ARC_0), and the taxonomy/Radway/Stage11 labels — converge. The taxonomy places this in Emotional Safety, Reassurance & Caretaking, and the Radway codes (R8 hero treats heroine tenderly, R9, R10) describe affective texture rather than a relational arc function. Stage11 codes (RAX_emotional_reassurance, RAX_practical_care, RAX_tenderness_core) similarly capture tone and register, not a structural arc event. Critically, tenderness and caretaking alone do not satisfy ARC_7 (restored trust) or ARC_8 (mutual commitment/resolution) under the strict rules: there is no evidence of trust being repaired or a relational resolution being reached. The topic describes ambient emotional warmth that is not tied to a specific arc transition in the main couple's trajectory. Metadata fully supports the contextual judgment of ARC_0. Exclude from H6 hypothesis testing.
- **Action:** KEEP

---

## Topic 121 — Revealing Plans to The Prince

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_0 (norm: ARC_0)

> she’ll be queen of the roost.” “

> do you think he’ll really go to the king?”

> if i let the prince know what is happening, instead of waiting for them to find out, they’ll know i’ve been out on my own.

> *(CELL_C, tertile=middle)* I am not Prince Charming or a shining Knight on a white horse.

> *(CELL_C, tertile=middle)* Hot as a fever, rattling bones I could just taste it, taste it If it’s not forever, if it’s just tonight Oh it’s still the greatest, the greatest, the greatest Kings of Leon Chapter Ten “You two pieces of shit are worthless you know that?”

> *(CELL_C, tertile=end)* I WILL one day go on a vacation to Disneyland and actually hang with Belle, Beast, Briar, Winter and Ashess.

### Pass A/B/C

- **A lexical:** `ARC_9`
  - Main keywords (king, prince, queen, throne, servant, royal, crown, kingdom, regent) are densely royal/political — no main-couple romantic arc signal, pointing to external political/power-structure conflict (ARC_9). MMR reinforces this with 'threats', 'declared', 'resigned', 'dealing', 'commander' — language of political negotiation and power struggle rather than romantic arc. KeyBERT ('promises', 'reassuring', 'assured', 'resigned', 'reveal', 'planned', 'decision') and POS ('threats', 'reassuring', 'commander', 'promises', 'magical') are more ambiguous — they could belong to any arc stage and lack clear romantic-couple anchoring, hence ARC_10 for those reps. However, the dominant signal across Main and MMR is an external political/institutional conflict context (royal court, power, threats, commanders), making ARC_9 the consensus. Disagreement flagged because KeyBERT and POS lean ARC_10 rather than ARC_9.
- **B contextual:** `ARC_0`
  - Topic 121 clusters around royalty/nobility vocabulary — kings, queens, nobles, rulers — but this is overwhelmingly world-building or external-political context rather than main-couple romantic arc content. BOOK_001 sentences are off-target (pop-culture references, fairy-tale tropes with no couple dynamic). BOOK_002 sentences revolve around a king's treachery/political machinations with no identifiable romantic couple, coded ARC_9 (external plot conflict). BOOK_003 sentences use 'queen' as a title/power dynamic but lack a clear romantic-couple frame; most are off-target social/political framing (ARC_0). BOOK_004 similarly references the king's commands and noble status as background world-building. No sentence clearly depicts a main-couple romantic arc event. ARC_0 is dominant at ~60%; ARC_9 accounts for ~40% (external political conflict). Main-couple probability is very low (~0.10) as the couple, if present, is peripheral to the topic's core signal.
- **C adjudicate:** `ARC_0`
  - Adjudication resolves the conflict between lexical consensus (ARC_9: external_plot_conflict) and contextual dominant (ARC_0: off_target) in favor of ARC_0. The taxonomy placement under 4.3 Secrets, Misunderstandings & Hidden Information with a secondary tag of 10.2 Historical & Period Setting suggests the topic's surface signal is period/setting detail or background intrigue rather than a main-couple dynamic. ARC_9 was likely assigned because conflict-label vocabulary is present, but high conflict-label fidelity is explicitly not equivalent to main-couple conflict. The secondary taxonomy tag (Historical & Period Setting) further supports that the dominant content is world/context material, not a relationship arc beat. ARC_0 (off_target) is therefore the correct single arc_role. Manual review is flagged because the lexical and contextual passes disagreed, and the taxonomy straddles two categories that could, in a different topic, support ARC_1 or ARC_5 — a human reviewer should confirm no main-couple secret/misunderstanding is embedded in the cluster.
- **Action:** REINTERPRET

---

## Topic 130 — Revealing A Secret Plan

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_0 (norm: ARC_0)

> you’ve rumbled my clever plan.’ ‘

> yes, i’ve got a little more planned for this evening.

> we’ve had this planned for months, but i’d almost forgotten about it.

> *(CELL_D, tertile=middle)* She would come out with mad plans and then challenge me into doing them.

> *(CELL_B, tertile=begin)* I had a real and viable plan in place now to turn things around.

> *(CELL_B, tertile=middle)* This plan—it's not going to get you into any trouble at school?” “

### Pass A/B/C

- **A lexical:** `ARC_10`
  - All four keyword lists center on planning and logistics vocabulary: 'plan, plans, planned, planning, tentatively, considering, scenario, urgency, according, part.' Supporting terms like 'madam, sir, reception, results, pumping, veins, forming, hiding, opposite' add situational texture but do not anchor to any specific narrative-arc role for the main couple. There is no clear signal of conflict, misunderstanding, separation, disclosure, repair, commitment, or external plot threat. The dominant semantic field is neutral logistical/procedural planning, making the arc role genuinely unclear across all representations.
- **B contextual:** `ARC_0`
  - Topic 130 is entirely about the word 'plan(s)' and logistical planning language. None of the sentences carry any identifiable romantic-arc function — there is no conflict, disclosure, repair, commitment, or other arc-relevant content. The sentences are decontextualised fragments about making or changing plans, with no clear main-couple relationship dynamic visible. The topic is off-target (ARC_0) across all tertiles and books. Main-couple probability is very low; most sentences are ambiguous as to who is speaking or to whom, and none signal a romantic dyad.
- **C adjudicate:** `ARC_0`
  - Adjudication resolves the Pass A/B tension as follows: the lexical consensus of ARC_10 (unclear arc role) reflects genuine ambiguity in surface tokens, but the contextual dominant of ARC_0 (off_target) is better supported by the taxonomy signal. Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) with secondary 4.2 (Ongoing Courtship & Everyday Relational Bonding) describes content that, while thematically adjacent to romance mechanics, does not map onto a main-couple narrative-arc beat — it is background relational texture or a non-main-couple dynamic. The absence of a clear main-couple anchor (main_couple: false) means no ARC_1–ARC_9 code is warranted. ARC_0 is therefore the correct resolution over ARC_10: the topic is not unclear so much as it is simply off-target for the main-couple arc hypothesis. No construct bucket applies because the topic does not contribute to REFINED_FALLING, REFINED_RISING, or EXTERNAL_PLOT_CONFLICT trajectories. No free-form labels were carried forward.
- **Action:** REINTERPRET

---

## Topic 248 — Arranging A Cover Story

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_10 (norm: ARC_10)

> i can attach myself to callie as a potential suitor, even with the distant cousin story you’ve decided to run with.

> i'll just let hannah know she won't have to watch him after today.

> it means you’ll probably bump into him too if you see more of hannah.’

> *(CELL_B, tertile=begin)* That Hannah’s boyfriend was sleeping with apparently the whole time they were going out?

> *(CELL_B, tertile=begin)* On Hannah’s behalf, and on yours too, even though I didn’t know your name.”

> *(CELL_B, tertile=begin)* Hannah took me to that party as a pity thing, unfortunately.

> *(CELL_B, tertile=begin)* Including that hot guy Hannah had started to introduce me to.

> *(CELL_C, tertile=middle)* Evan,” she says, “that day, last week, I went out to the pond, it was the day after the bear.

> *(CELL_A, tertile=middle)* Anyway, I was totally pissed about that, and about Jess pinching my arm, when Cassie dropped another bomb on me… She said that she is “Falling in love with Jimmy!!!!”

> *(CELL_A, tertile=middle)* Getting all mad because of her relationship with Jimmy… Wishing that they had never started dating… Now I will never see Cassie again!

> *(CELL_A, tertile=middle)* Jess and I rode together, but Cassie said she would meet us there; she was still trying to find the perfect gift for Jimmy.

### Pass A/B/C

- **A lexical:** `ARC_10`
  - Main and POS are dominated by character names (callie, hanna, leslea), a pickpocketing incident, and abstract nouns (concept, notion, options, treatment) with no clear romantic-arc signal — coded ARC_0 (off-target). KeyBERT and MMR carry emotionally loaded cues (crushed, upset, pregnant, admit, overheard, apologize, problems, wasting) that suggest distress and possible disclosure, but the named characters (callie, hanna, sister) point toward a sibling or secondary-character dynamic rather than a confirmed main couple. 'Pregnant' and 'admit' could indicate ARC_5 (disclosure) or ARC_4 (relationship-caused distress), but without clear main-couple anchoring the signal is ambiguous. The split between off-target and distress/disclosure readings across representers, combined with the absence of a confirmed main-couple frame, yields ARC_10 (unclear arc role) as the consensus.
- **B contextual:** `ARC_10`
  - Topic 248 clusters around the name 'Hannah' and secondary character names (Cassie, Jimmy, Jess, Amy). No single main couple is clearly established across sentences. BOOK_001 sentences reference Hannah's cheating boyfriend — a third-party relationship conflict, coded ARC_9. BOOK_003 sentences involve an external rescue/intel operation with no romantic couple visible, coded ARC_9. BOOK_004 sentences reference Cassie and Jimmy as a couple causing distress to a narrator/friend — coded ARC_4 where relationship-caused distress is explicit, and ARC_10 where the role is ambiguous. BOOK_006 sentences reference Hannah in a context suggesting she was a deceased or missing person significant to Ryker, with external threat framing — coded ARC_9 for threat sentences and ARC_10 for descriptive/unclear ones. No code reaches 70%; ARC_10 is the plurality at ~45%, making it the dominant code. Main couple probability is very low (~0.10) as most sentences reference secondary or unclear characters.
- **C adjudicate:** `ARC_10`
  - Both lexical consensus and contextual dominant converge on ARC_10 (unclear_arc_role). The taxonomy placement under 4.3 Secrets, Misunderstandings & Hidden Information suggests latent ARC_1 or ARC_5 signal, but without sufficient topic-word or passage evidence to override the double ARC_10 signal, reinterpretation would be speculative. The secondary taxonomy tag (5.2 Friends, Allies & Social Circles) further muddies main-couple attribution — the topic may center on a social/ally dynamic rather than the protagonist pair, keeping main_couple false. No free-form labels from prior passes require remapping. Manual review is flagged so a human auditor can inspect the raw top-words and representative documents to determine whether the hidden-information theme is clearly tied to the main couple (which would warrant REINTERPRET to ARC_1 or ARC_5) or remains genuinely ambiguous.
- **Action:** KEEP

---

## Topic 256 — Refusing to Let It End

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** ARC_0 (norm: ARC_0)

> no, i’ll get over it.

> i’ll give you some time, but goddamn it, nat, this is not over.”

> it’ll never be over—unless it ends right here right now.

> *(CELL_D, tertile=begin)* I no longer cared which side won or lost, I only wanted it to be over.

> *(CELL_D, tertile=middle)* Perhaps when this is over, you might see another attractive alternative.

> *(CELL_D, tertile=end)* If there are consequences to our lovemaking, then this treasure hunt ends.

### Pass A/B/C

- **A lexical:** `ARC_4`
  - Main keywords ('end', 'over', 'ends', 'ended') strongly suggest termination or breakup language pointing toward ARC_3 (separation/breakup threat). However, KeyBERT, POS, and MMR all add affective-distress cues — 'hurts', 'anxious', 'shouted', 'repeated', 'sending' — that shift the dominant signal toward ongoing emotional suffering within or caused by the relationship (ARC_4: relationship_caused_distress). The pattern of repeated painful interactions ('repeated', 'thursday' as a recurring marker, 'hurts', 'anxious', 'shouted') suggests cyclical distress rather than a clean breakup event. ARC_4 wins by weight of three representers; Main's ARC_3 reading creates mild disagreement.
- **B contextual:** `ARC_0`
  - Topic 256 is dominated by the word 'over' used in highly varied, mostly non-romantic-arc senses: completion of events, wars, tasks, emotional recovery, and social pleasantries. The largest single cluster (ARC_0, ~45%) consists of sentences where 'over' has no clear romantic-arc meaning. A secondary cluster from BOOK_004 uses 'I'm over it / get over it' language that loosely implies emotional recovery/repair (ARC_6, ~25%), but without clear main-couple context. A smaller cluster references external plot events ending (ARC_9, ~20%). Only BOOK_001_1 ('We're over') clearly signals a main-couple breakup threat (ARC_3). Main-couple probability is low (~0.15) because most sentences lack identifiable couple context. No single code reaches 70%, but ARC_0 is dominant at ~45%, so dominant_code is ARC_0.
- **C adjudicate:** `ARC_0`
  - Lexical consensus (ARC_4) reflects surface conflict-label fidelity to taxonomy 4.4 (Conflict, Distance & Breakup Threats), but the contextual dominant code (ARC_0) indicates the topic content does not actually center on the main couple's relationship-caused distress. The taxonomy placement in 4.4 is a label match, not a content match. Because high conflict-label fidelity ≠ main-couple conflict, and the dominant contextual read is off-target, ARC_0 prevails in adjudication. main_couple is set to false accordingly. Manual review is flagged to verify whether any main-couple signal is genuinely present or whether the topic should be excluded from the hypothesis corpus entirely.
- **Action:** REINTERPRET

---

## Topic 286 — Trying to Regain Good Graces

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_0 (norm: ARC_0)

> oh ms. [person], you really should drop by our office more, we miss your good taste around here' blah blah blah.

> i'll not have you and his grace at each other's throats before we arrive at champney court."

> if what you’ve said is to be believed, how am i supposed to get back into her good graces?

> *(CELL_A, tertile=begin)* Widow of a respected insurance agent and former daughter-in-law of a well-known Baptist minister, she’d seemingly shunned the social position and privilege of her past to be with Colton, but this wasn’t the first time Eric had seen her slip on her high-and-mighty act like an expensive fur coat.

> *(CELL_A, tertile=begin)* Eric needed a mentor to teach him how to be an honorable man.

### Pass A/B/C

- **A lexical:** `ARC_0`
  - Main keywords are dominated by proper nouns and names (graceclemens, ruttery, champney, oracle, grâce) with no clear romantic-arc signal; 'blah' and 'tape' add noise. KeyBERT offers 'thrilled', 'embarrassment', 'awkwardly', 'deserve' — mild emotional texture but no identifiable main-couple dynamic; 'dr' and 'continues' are generic. POS and MMR introduce 'desperation', 'embarrassment', 'pregnant', 'pressure', 'decision', 'unable', 'rushing' — these could hint at a distress or stakes situation, but 'pregnant' and 'desperation' without any relational anchoring (no conflict, repair, disclosure, or commitment cues tied to a couple) remain ambiguous. 'Graceful'/'gracefully' across reps likely refers to a character named Grace rather than a quality. The cluster of proper-name noise in Main and the absence of any clear main-couple interaction pattern across all four reps points primarily to off-target content, with POS/MMR being merely unclear rather than arc-relevant. Consensus lands on ARC_0 (off_target) given the name-heavy Main rep and lack of coherent romantic-arc signal, with noted disagreement from POS/MMR which lean ARC_10.
- **B contextual:** `ARC_0`
  - Topic 286 clusters around proper-noun name references (Mrs. Darden, His Grace, Reed, Eric, Dee, Cynda) and brief honorific/address fragments. None of the sentences establish a clear main-couple romantic arc dynamic. BOOK_001–003 sentences involve secondary or peripheral characters (Eric, Dee, Cynda, Colton) with no identifiable main-couple romantic conflict or progression. BOOK_004 sentences are purely honorific address fragments ('Your Grace', 'His Grace') with no arc content. BOOK_005 sentences mention Reed in passing but lack sufficient context to assign a romantic arc role — they read as name-reference fragments rather than arc-bearing narrative moments. The topic appears to be a name/address cluster with no coherent narrative-arc signal, making ARC_0 (off_target) the appropriate dominant code across all tertiles.
- **C adjudicate:** `ARC_0`
  - Both lexical consensus and contextual dominant agree on ARC_0 (off_target). The taxonomy tag 4.3 Secrets/Misunderstandings and secondary 3.2 Negative Emotions might superficially suggest ARC_1 or ARC_4, but the main-couple filter is not satisfied — the topic does not pertain to the primary romantic dyad. Without a main-couple anchor, secrets or distress signals cannot be coded as relationship-arc events. ARC_0 is therefore confirmed. No construct bucket applies, and no manual review is needed.
- **Action:** KEEP

---

## Topic 316 — Snapping Over Money and Control

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** ARC_0 (norm: ARC_0)

> you’ll have to find another way to obtain the tallmadge money,” lucas snapped. “

> stop that, you little fool, otherwise we’ll both be—’ lucas began, and then stopped as one of suzy’s flailing hands caught the side of his mouth.

> they didn’t like it much when they found out, but lucas paid them well, and they’ll get over it.

> *(CELL_B, tertile=middle)* Perhaps you should show Eva to her room,” Lucas finally suggested to Michael. “

> *(CELL_B, tertile=middle)* Unlike Ethan and Jason, who were dark-haired, Aaron and Lucas were more dirty-blonde.

> *(CELL_B, tertile=end)* He watched Lucas Mason as he spoke and was rewarded by an expression of guilt upon his uncle’s face. “

> *(CELL_B, tertile=end)* You have brought this upon us,” Lucas Mason harshly accused his grief stricken nephew. “

> *(CELL_B, tertile=end)* Lucas Mason was not so wise, however, and questioned Rork angrily. “

> *(CELL_B, tertile=end)* The look upon Lucas Mason’s traitorous face mirrored the truth of Rork’s words.

> *(CELL_B, tertile=end)* But as Lucas continued his tirade, Rork reached out to touch his beloved father’s body , only to find it frozen.

### Pass A/B/C

- **A lexical:** `ARC_4`
  - All four keyword lists converge on emotional distress and negative affect within a relationship context. Main keywords (stared, thoughtful, shout, named characters lucas/fallon) suggest interpersonal tension between identifiable parties. KeyBERT supplies the emotional valence: annoyance, groaned, disappointment, failure, pathetic — these are feelings generated by the relationship dynamic rather than an external plot threat or a discrete misunderstanding/escalation event. POS and MMR reinforce this with overlapping terms (shout, failure, annoyance, disappointment, comments, bothered, glared, worries). The cluster describes ongoing relational distress — characters experiencing negative emotional states caused by their relationship — which maps to ARC_4 (relationship_caused_distress). There is no clear repair, commitment, disclosure, or external-plot framing; the dominant signal is sustained emotional suffering/frustration within the couple dynamic.
- **B contextual:** `ARC_0`
  - Topic 316 clusters around the name 'Lucas' (and associated characters Aaron, Kia, Sampson, Rork, Eva, Michael, Ethan, Jason) across multiple books. The sentences are character-identification fragments, spatial/logistical dialogue, and brief action tags with no romantic-couple framing. None of the sentences establish or imply a main romantic couple; they reference male characters (Lucas, Aaron) in what appear to be ensemble or family/group contexts, conflict between non-romantic parties (Lucas Mason vs. Rork), or simple descriptive statements. There is no romantic arc content detectable. All sentences are coded ARC_0 (off_target).
- **C adjudicate:** `ARC_0`
  - Lexical consensus (ARC_4) reflects surface conflict-label fidelity — the topic's tokens map onto distress/conflict vocabulary — but contextual dominant (ARC_0) correctly identifies that the content does not involve the main romantic couple. Taxonomy 4.4 (Conflict, Distance & Breakup Threats) with secondary 7.1 (Interpersonal Non-Romantic Conflict) confirms the conflict is interpersonal but non-romantic, i.e., outside the main-couple dyad. Per the main-couple filter, ARC_4 requires the distress to be caused by the romantic relationship itself; here the distress is either peripheral or involves non-romantic parties. The contextual dominant therefore overrides the lexical consensus. ARC_0 (off_target) is the correct arc_role. No construct bucket applies because the topic does not contribute to the REFINED_FALLING, REFINED_RISING, or EXTERNAL_PLOT_CONFLICT arcs in a main-couple context.
- **Action:** REINTERPRET

---

## Topic 338 — Promising Never to Do That Again

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** ARC_0 (norm: ARC_0)

> but [person], you got to promise me you’ll never do something like that again.

> okay, but i'll warn you — you're making this seem dangerously like a date, [person]." "

> i’ll have to get it approved by [person],” he said, seemingly giving in to my demands.

> *(BOOK_001, POS_001, tertile=middle)* He turned to Wyatt. “

> *(BOOK_001, POS_001, tertile=middle)* Wyatt,” he said. “

> *(BOOK_001, POS_001, tertile=begin)* Now, Wyatt.” “

### Pass A/B/C

- **A lexical:** `ARC_10`
  - The keyword sets are dominated by character names (turner, carley, bray, val), titles (captain, commander), and action/state words (suspicions, talked, yourbrother, bowed, willing, insisted, begging, tightly, delicate, fishing, notion, unsure, disbelief, confusion, pieces, pleased, dangerously, squinted, smacked, scrambled, revealing, choked). 'Suspicions' and 'revealing' could hint at disclosure or conflict, and 'begging/insisted/bowed' could suggest interpersonal tension, but there is no clear signal that the main romantic couple is implicated in any specific arc function. The presence of 'psychic,' 'captain/commander,' and 'yourbrother' suggests an external or ensemble scene. Without sufficient evidence to assign a specific arc role to the main romantic relationship, ARC_10 (ambiguous) is the appropriate consensus code.
- **B contextual:** `ARC_0`
  - Topic 338 is entirely composed of sentence fragments consisting solely of the name 'Wyatt' used as a speech tag, address, or attribution marker (e.g., 'Wyatt said.', 'Wyatt asked.', 'He turned to Wyatt.'). These fragments carry no relational content whatsoever — they are purely dialogic attribution snippets. There is no evidence of romantic couple interaction, relationship state change, or any arc function. The topic appears to be a character-name dialogue-tag cluster, not a narrative arc topic. It is uniformly ARC_0 (unrelated) across all positions and should be excluded from H6 arc analyses.
- **C adjudicate:** `ARC_0`
  - Contextual dominant (ARC_0) is the stronger signal here. The taxonomy labels — Promise/Vow/Future-Tense Speech Acts and Ongoing Courtship & Everyday Relational Bonding — describe relational texture and forward-looking language rather than a discrete arc function (no conflict, no repair, no commitment resolution). Radway R9 (heroine responds warmly to hero's tenderness) and R8 are consistent with ambient courtship bonding, not a structural arc beat. Stage11 RAX_protective_commitment could gesture toward ARC_7 or ARC_8, but without evidence of trust being restored or mutual relational resolution being reached, that label reflects tone rather than arc function. The lexical consensus of ARC_10 (ambiguous) reflects genuine indeterminacy in the word-level signal, but the contextual read — that this topic captures diffuse, ongoing relational warmth and vow-like speech rather than a narratively consequential arc moment — resolves the ambiguity toward ARC_0. The metadata is therefore mixed: Radway/Stage11 labels weakly support some romantic-couple relevance, but none of the taxonomy or Radway codes implicate a rising or falling arc beat with sufficient specificity to include in H6 hypothesis testing. Exclude.
- **Action:** EXCLUDE_FROM_HYPOTHESIS

---

## Topic 346 — Delivering Urgent News in Secret

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_0 (norm: ARC_0)

> let’s go [person] i’ll drive you to it.”

> i hardly think leaving a note telling my father where to find me would’ve been a good idea, but i’m not going to tell james that. “

> i know this is bad, me coming here, especially after the celeb weekly article, but i’ve got some important information about [person].”

> *(CELL_B, tertile=end)* She pointed to James Stevens from The Scoop , who sat in the front row with Scott’s parents. “

### Pass A/B/C

- **A lexical:** `MIXED`
  - Main and KeyBERT point strongly toward ARC_5 (disclosure): 'admit' appears in both, supported by 'willingly', 'chose', 'begged', 'planning', and 'hiding' — all cues of a character being pressed or choosing to reveal something. POS and MMR lean toward ARC_4 (relationship-caused distress): 'suffering', 'strained', 'threatened', 'opposite', 'advantage' suggest emotional or relational pain tied to the couple dynamic rather than a clean disclosure moment. The split between disclosure-pressure cues and distress/strain cues across the four reps prevents a single consensus code, yielding MIXED.
- **B contextual:** `ARC_0`
  - Topic 346 is dominated by name fragments and attribution tags — 'James said.', 'James?', 'Jonathan.', 'James Stevens from The Scoop' — with no narrative content conveying relationship dynamics, conflict, repair, or any romance-arc function. The sentences are essentially decontextualized speaker labels or proper-noun fragments. 'James Stevens from The Scoop' appears to be a journalist character, not a romantic lead. No sentence establishes a main-couple interaction with sufficient context. All sentences are coded ARC_0 (off_target). Main-couple probability is very low (~0.05) given the absence of any relational content.
- **C adjudicate:** `ARC_0`
  - Lexical consensus was MIXED, but contextual dominant is ARC_0 (off_target). Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) with secondary 7.1 (Interpersonal Non-Romantic Conflict) signals that any secret or misunderstanding present is not anchored to the main romantic couple — it is either peripheral character conflict or non-romantic interpersonal tension. Because the main-couple filter fails (main_couple=false), the content does not qualify for ARC_1 through ARC_8. ARC_9 would require an external plot threat bearing on the couple, which is not indicated. The dominant contextual read of off-target content therefore prevails, resolving to ARC_0. No construct bucket applies.
- **Action:** REINTERPRET

---

## Topic 24 — Confronting An Unwanted Marriage

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** MIXED

> we’ll be married… to each other.”

> you’re already married to me; he’ll understand.” “

> i’ll give you a divorce and you can just walk away.

> *(CELL_D, tertile=begin)* So that whole getting married and settling down part doesn't appeal to you?"

### Pass A/B/C

- **A lexical:** `MIXED`
  - Main keywords (marry, married, marriage, husband, wife, divorce, marrying) anchor strongly to formal commitment structures; the presence of 'divorce' pulls toward ARC_3 (separation/breakup threat) but 'marry/marriage/husband/wife' collectively suggest ARC_8 (mutual commitment/final payoff), so Main is coded ARC_8. KeyBERT (engaged, promises, intend, willingly, decide) suggests deliberate commitment-making but 'instincts, suggest, chuckle, uh, remarked' introduce ambiguity and possible misunderstanding framing, coded ARC_1. POS (unhappy, threats, divorce implied via 'ends', 'previous', 'issue', 'concept') signals distress and threat to the relationship, coded ARC_3. MMR (unhappy, threats, arranged, faltered, chased, eyeing) reinforces coercive or contested marriage framing with 'threats', 'arranged', 'faltered', pointing to ARC_3. Two reps land on ARC_3, one on ARC_8, one on ARC_1 — genuine disagreement across commitment-threat-misunderstanding axis yields MIXED.
- **B contextual:** `MIXED`
  - Topic 24 clusters around marriage/wedding language. No single ARC code reaches 70%. ARC_5 (disclosure/revelation of intentions about marriage) is most frequent (~30%), covering sentences where characters express or question desire to marry. ARC_8 (mutual commitment/final payoff) applies to affirmative marriage declarations. ARC_2 (escalation conflict) covers refusals or contested marriages. ARC_4 (relationship-caused distress) applies where marriage is unwanted or coerced. ARC_0 covers third-party references. The spread across codes yields MIXED as dominant. Most sentences involve the main couple or plausible main-couple dyads, giving a moderate-to-high main_couple_prob of 0.65.
- **C adjudicate:** `MIXED`
  - Both Pass A/B converged on MIXED, and the taxonomy anchor (4.4 Conflict, Distance & Breakup Threats with secondary 4.5 Reconciliation) confirms the topic straddles escalating conflict and breakup-threat territory without cleanly resolving into repair or commitment. The dominant signal sits in the falling arc (conflict intensification and relational distance/threat), with only a secondary trace of reconciliation momentum insufficient to shift the bucket to REFINED_RISING. Mapping any free-form labels: 'Conflict' → ARC_2; 'Obstacle' or distance language → ARC_3. MIXED is retained as the arc_role because neither ARC_2 nor ARC_3 alone captures the full topic, and the secondary 4.5 signal prevents a clean single-code assignment. Construct bucket is REFINED_FALLING given the dominant 4.4 taxonomy weight.
- **Action:** REINTERPRET

---

## Topic 29 — Confessing Long-Held Love

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** ARC_8 (norm: ARC_8)

> i love you with everything i am, everything i’ve been, and everything i hope to be .” “

> tell her i’ve always loved her.

> i’ve always been in love with you.”

> *(CELL_B, tertile=end)* I love you, too, sweetheart.”

> *(CELL_B, tertile=end)* Oh, child, I love you, too.”

> *(CELL_B, tertile=end)* You just say ‘I love you.’”

### Pass A/B/C

- **A lexical:** `MIXED`
  - Main keywords ('love, loved, loves, falling, fall, always') point strongly toward mutual romantic commitment/resolution (ARC_8). KeyBERT keywords ('forgive, apologize, hated, crushed, deserve, dreamed') signal an apology/reconciliation dynamic (ARC_6), with 'forgive' and 'apologize' being the clearest repair cues. POS keywords ('spite, delicate, issue, actions, reflection') suggest ongoing relational distress or tension without clear resolution (ARC_4). MMR keywords ('apologize, spite, crushed, reflection, uttered') reinforce the reconciliation/repair reading (ARC_6) but 'spite' and 'crushed' also carry residual conflict/distress. The combination of love-declaration language alongside forgiveness, apology, spite, and crushed feelings indicates a scene where the couple moves through distress and conflict toward reconciliation and possibly commitment — no single code captures all four lists, yielding MIXED.
- **B contextual:** `ARC_10`
- **C adjudicate:** `ARC_8`
  - The lexical consensus (MIXED) and contextual dominant (ARC_10) reflect surface ambiguity, but the convergent metadata strongly resolves this. Taxonomy 4.5 (Reconciliation, Commitments & HEA) with secondary 3.1 (Positive Resolution, Relief & Emotional Payoff) points directly to final relational resolution. Radway R11 ('Hero declares love and demonstrates commitment') is the canonical signal for ARC_8 mutual commitment/final resolution; R12 and R13 (typically hero's tenderness and couple's future orientation) reinforce this. Stage11 codes RAX_emotional_security and RAX_tenderness_core are consistent with post-conflict restored closeness, while RAX_generic_confession_apology suggests a prior repair moment has concluded, leaving the couple in a committed state. Critically, ARC_8 does not require the absence of tenderness or love — it requires evidence of mutual relational commitment/resolution, which R11 directly supplies. The contextual ARC_10 judgment likely arose because the topic blends emotional warmth with commitment signals without a single sharp plot marker, but the Radway and taxonomy layers collectively override that ambiguity. No split is warranted; the topic coheres around a single HEA-adjacent commitment beat. Manual review is not required given strong cross-layer convergence.
- **Action:** REINTERPRET

---

## Topic 37 — Defending A Close Friendship

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_1 (norm: ARC_1)

> i've told you -- we're just good friends.

> and i’ll grant ye i’ve been a bad friend to you.

> but we’ve been friends for a long time.

> *(CELL_D, tertile=middle)* Good, then get out of my face and give me a minute with my friend.”

> *(CELL_D, tertile=middle)* He didn’t have any life-long friends, with the exception of Butch.

> *(CELL_D, tertile=end)* A friend once told me it’s okay to lean on someone,” he said. “

### Pass A/B/C

- **A lexical:** `ARC_0`
  - All four keyword lists point away from main-couple romantic arc dynamics. Main is dominated by 'friends/friendship/friendly/friendships/best friend' vocabulary — social relationship framing, not romantic-couple conflict or progression. KeyBERT adds casual social-interaction words ('playfully', 'parties', 'stalked' in a light sense, 'engaged', 'honestly') with no romantic-arc signal. POS yields ambient social/contextual nouns and adjectives ('parties', 'anxiety', 'suggestion', 'fashioned', 'annoying') that do not map to any specific arc stage. MMR similarly offers social-texture words ('pout', 'admire', 'playfully', 'shout') without a coherent arc trajectory. No cues for misunderstanding, escalation, separation, disclosure, repair, commitment, or external plot conflict between a main couple are present. The topic appears to describe friendship dynamics or a friend-group social context, making it off-target for romance narrative-arc coding.
- **B contextual:** `ARC_1`
  - Topic 37 clusters around the word 'friend' and its variants, predominantly functioning as a misunderstanding or deflection device in romance narratives — one partner insisting the relationship is 'just friendship' when the other perceives or desires more (ARC_1: misunderstanding). Several sentences (BOOK_001_1–6, BOOK_002_1–3, BOOK_003_6) reflect this friend-zone ambiguity between potential main-couple members. BOOK_003_1, BOOK_003_2, and BOOK_003_5 shift toward a separation/breakup-threat register ('We're still friends, right?', 'I'd like to stay friends with you'), coded ARC_3. Several sentences (BOOK_002_4–6, BOOK_003_3–4, BOOK_004_1–2) are clearly off-target, referring to third-party friendships with no main-couple relevance (ARC_0). ARC_1 is the plurality code at ~40%, below the 70% threshold for a single dominant code, but no other code comes close; ARC_1 is returned as dominant given its plurality. Main-couple probability is moderate (~0.50) because roughly half the sentences plausibly involve the main couple's friend-zone dynamic, while the rest are off-target or unclear.
- **C adjudicate:** `ARC_1`
  - Lexical consensus (ARC_0 / off_target) was overridden by contextual dominant (ARC_1 / misunderstanding). The taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information directly corroborates ARC_1: the topic captures concealed information or false impressions that generate relational tension between the main couple, not mere off-target noise. The secondary taxonomy (4.2 Ongoing Courtship) suggests the misunderstanding is embedded in an active courtship phase, consistent with a falling/tension arc rather than a repair or resolution arc. ARC_1 is therefore the correct single code. Construct bucket is REFINED_FALLING because misunderstandings typically drive the couple apart or impede bonding, placing this in the falling/conflict segment of the narrative arc. No free-form labels were carried forward; all prior Pass A/B language has been mapped to ARC_1.
- **Action:** REINTERPRET

---

## Topic 38 — Admitting Shared Pain

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** ARC_10 (norm: ARC_10)

> i’ve seen your pain.

> i've never felt that way before."

> will it make you feel better to know that i’ve got one, too?”

> *(CELL_A, tertile=middle)* That’s what it felt like—that was the exact feeling—and I’m so happy that now you were there.

### Pass A/B/C

- **A lexical:** `MIXED`
  - Main keywords (feel, felt, better, make, good) are too generic to assign a specific arc function — ARC_10. KeyBERT introduces 'hurts,' 'worst,' 'experienced,' suggesting emotional pain or distress, pointing toward ARC_4 (relationship-caused distress). POS keywords ('magical,' 'accustomed,' 'problems,' 'loose') remain ambiguous — ARC_10. MMR is the most informative: 'apologize' and 'admitted' are direct repair/disclosure cues, 'hurts' and 'ticked' suggest prior conflict, and 'magical' hints at positive relational feeling — together these point to ARC_6 (apology/reconciliation/repair). The four representations split between ambiguity (Main, POS), distress (KeyBERT), and repair (MMR), producing genuine disagreement. The most semantically loaded representations (KeyBERT, MMR) suggest a moment of acknowledged hurt followed by apology, but without clear consensus the result is MIXED.
- **B contextual:** `ARC_10`
- **C adjudicate:** `ARC_10`
  - The lexical consensus (MIXED) and contextual dominant (ARC_10) reflect genuine ambiguity. Taxonomy 4.2 (Ongoing Courtship & Everyday Relational Bonding) with secondary 3.2 (Negative Emotions & Distress) pulls in two directions: bonding language suggests movement toward ARC_7 (restored trust) or ARC_8 (commitment), while distress language hints at ARC_4 (relationship-caused distress) or ARC_1 (misunderstanding maintained). The Radway primary code R10 — heroine reinterprets hero's behaviour as result of previous hurt — is pivotal: this is a cognitive/emotional reframing moment, not yet a confirmed repair or disclosure. R10 does not by itself constitute ARC_5 (disclosure/revelation) because the reinterpretation is internal to the heroine, nor ARC_7 because trust restoration requires reciprocal evidence. Stage11 labels (RAX_emotional_reassurance, RAX_emotional_security, RAX_tenderness_core) are consistent with a warm relational moment but per critical rules these do not elevate the code to ARC_7 without evidence of trust being actively restored. The secondary Radway codes R8 and R9 add further ambiguity. On balance, ARC_10 (ambiguous) is the most defensible single code: the topic sits at a liminal point in the arc where reinterpretation is occurring but its relational consequence — repair, continued misunderstanding, or mere bonding — cannot be determined from available evidence. Strict H6 inclusion is 'exclude' because ambiguous topics introduce noise into both rising and falling arc hypotheses. Manual review is required to examine token-level evidence for whether the heroine's reinterpretation is communicated to the hero (which would shift toward ARC_5 or ARC_7) or remains private (which would keep it at ARC_10 or shift toward ARC_1).
- **Action:** REINTERPRET

---

## Topic 43 — Pissed Off and Grumbling

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** MIXED

> this isn’t the first time i’ve pissed him off.”

> we’ve irritated you, have we?” “

> i’ve been pissed at him ever since. “

> *(CELL_B, tertile=begin)* She doesn’t look mad so much as really disappointed. “

> *(CELL_D, tertile=middle)* Tarquin is also pissed, but not as much as me.

> *(CELL_B, tertile=end)* Now I know where his rage comes from.”

### Pass A/B/C

- **A lexical:** `ARC_2`
  - Main is dominated by anger/temper vocabulary (mad, angry, pissed, offend, temper) pointing to active interpersonal conflict escalation — ARC_2. KeyBERT reinforces this with arguing, attacked, insulted, grumbled, suggesting heated confrontation between parties — ARC_2. POS shifts toward emotional suffering and embarrassment (embarrassing, sadness, distress, emotional) with no clear aggressor, leaning toward relationship-caused distress — ARC_4. MMR similarly foregrounds distress, insulted, terribly, wasting, grumbled — still emotionally charged but more suffering-oriented than combative — ARC_4. Disagreement exists between the active-conflict framing (Main, KeyBERT) and the distress/suffering framing (POS, MMR). The preponderance of explicit anger and conflict-action cues across the two most lexically direct representations (Main, KeyBERT) tips consensus to ARC_2 escalation_conflict, as the distress appears to be a product of the conflict rather than a standalone relational wound.
- **B contextual:** `ARC_4`
  - Topic 43 is dominated by expressions of anger, moodiness, and emotional volatility (e.g., 'pissed,' 'angry,' 'rage,' 'temper,' 'moody'). These sentences describe characters experiencing or managing anger/frustration, which maps most closely to ARC_4 (relationship_caused_distress) — emotional distress states that arise within interpersonal dynamics. A minority of sentences (BOOK_002_5, BOOK_003_1, BOOK_003_4, BOOK_004_2) show more active interpersonal conflict or confrontation, coded ARC_2 (escalation_conflict). The main couple cannot be reliably identified from these short, decontextualized snippets — characters named (Louis, Tarquin) are not clearly established as part of a main romantic couple, so main_couple is 'unclear' throughout. Main couple probability is low (~0.25) given the ambiguity. ARC_4 exceeds 70% threshold, making it the dominant code.
- **C adjudicate:** `MIXED`
  - Lexical consensus (ARC_2) and contextual dominant (ARC_4) diverge but are not mutually exclusive: escalating conflict between the main couple (ARC_2) is the surface signal, while the deeper emotional register — relationship-caused distress — is what the contextual read captures (ARC_4). Taxonomy 4.4 'Conflict, Distance & Breakup Threats' anchors the primary signal in ARC_2, but the secondary taxonomy 3.2 'Negative Emotions & Distress' confirms that ARC_4 is a genuine co-present signal rather than noise. Because both codes are substantively supported and neither fully subsumes the other, MIXED is the correct resolution rather than forcing a single code. The construct bucket is REFINED_FALLING: both escalation conflict and relationship-caused distress are falling-arc phenomena occurring before any repair or restoration. Manual review is flagged to verify whether the topic's representative documents lean more heavily toward active conflict dynamics (ARC_2) or toward the emotional suffering the relationship itself generates (ARC_4), which would inform downstream weighting in the hypothesis model.
- **Action:** REINTERPRET

---

## Topic 45 — Reassured Everything Will Be Fine

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_7 (norm: ARC_7)

> we’ll be ok.” “

> nadines : you’ll be ok?

> ok, maybe a zero-tolerance one, but there’s no doubt about it, you’ll be great.

> *(CELL_D, tertile=middle)* I'm fine," Amber replied quietly. "

> *(CELL_D, tertile=begin)* Your wound…'" "I'm fine."

> *(CELL_B, tertile=middle)* Is everything okay?” “

### Pass A/B/C

- **A lexical:** `ARC_7`
  - Main keywords ('fine, okay, everything, right, honey, alright') collectively signal reassurance and calming language directed at a partner. KeyBERT reinforces this with 'assured, assure, smoothly, incredibly,' pointing to active reassurance being given. MMR adds 'assure, assured, acknowledged, appreciate,' further cementing a pattern of one party reassuring the other and trust/closeness being actively restored or strengthened — meeting the ARC_7 threshold. POS ('problems, sir, lord') is too sparse and formal to confirm a romantic context, yielding ARC_10. The three-to-one weight of Main, KeyBERT, and MMR toward reassurance/trust-restoration drives the consensus to ARC_7.
- **B contextual:** `ARC_10`
- **C adjudicate:** `ARC_7`
  - The lexical consensus (ARC_7) and the taxonomy/Radway/Stage11 labels collectively support a restored-trust reading: Taxonomy 4.6 (Emotional Safety, Reassurance & Caretaking) maps directly onto the ARC_7 criterion of trust/closeness being strengthened; Radway R8 (hero treats heroine tenderly) and R9 (hero's inner feelings revealed) are canonical markers of the trust-restoration beat; Stage11 codes RAX_emotional_reassurance and RAX_emotional_security reinforce this. The contextual judgment of ARC_10 (ambiguous) is the outlier. Its ambiguity likely reflects that tenderness and reassurance alone do not guarantee ARC_7 — the critical rule requires evidence that trust is being *restored* rather than merely expressed. However, the secondary taxonomy (9.2 Promise, Vow & Future-Tense Speech Acts) tips the balance: future-oriented vows in a caretaking frame are a strong signal of relational repair/strengthening, not mere affection. On balance, the preponderance of evidence — lexical consensus, three independent metadata streams, and the secondary taxonomy — overrides the contextual ambiguity flag. ARC_7 is the correct resolution. Manual review is recommended to verify that the topic's tokens include explicit repair/restoration language (e.g., 'again,' 'still,' 'always,' 'safe') rather than purely first-instance tenderness, which would collapse back to ARC_10.
- **Action:** REINTERPRET

---

## Topic 46 — Asking Someone to Trust You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_7 (norm: ARC_7)

> you’ll just have to trust me.”

> he’ll trust you if you promise to keep me in sight.” “

> my trust that he’ll bring me to safety.

> *(CELL_D, tertile=begin)* The critics wanted to prove that setting goals, drawing graphs, measuring results and evaluating the performance of individuals was nothing less than taking the place of trusting the Holy Spirit to give increase.

> *(CELL_D, tertile=begin)* Trust us, all we need to do to you can be done here,” one of the other guys said.

### Pass A/B/C

- **A lexical:** `ARC_1`
  - The Main keyword list is the decisive signal here: 'trust, trusted, betrayed, betray, trusting, betrayal' form a tight semantic cluster around broken or withheld trust within a relationship, with the direct-address pronouns 'me' and 'you' anchoring it interpersonally. This pattern — trust vocabulary combined with betrayal and concealment — maps most cleanly to ARC_1 (misunderstanding/secret maintained), where one or both parties are hiding something or a breach of trust is being sustained rather than resolved. There is no repair, apology, or disclosure language (which would push toward ARC_5 or ARC_6). KeyBERT, POS, and MMR lists ('instincts, worries, hesitation, twisting, options, percent, concrete') are largely abstract or procedural and do not independently implicate the romantic arc, hence ARC_10 for those three. The Main list dominates consensus given its direct relational content, yielding ARC_1 overall.
- **B contextual:** `ARC_7`
- **C adjudicate:** `ARC_7`
  - The taxonomy (4.6 Emotional Safety, Reassurance & Caretaking), Radway codes (R8 hero treats heroine tenderly, R9, R10), and Stage11 prior codes (RAX_emotional_reassurance, RAX_emotional_security, RAX_tenderness_core) all converge on a pattern of trust and closeness being actively restored or reinforced between the main couple — the defining criterion for ARC_7. The lexical consensus of ARC_1 is overridden: while the secondary taxonomy flag (4.3 Secrets/Misunderstandings) might surface lexical signals of concealment, the dominant functional pattern across all contextual and metadata signals is one of emotional repair and security-building, not misunderstanding maintenance. ARC_7 requires evidence that trust/closeness is being restored or strengthened, and the Radway R8 tender-treatment code combined with the emotional-safety taxonomy and Stage11 reassurance codes collectively satisfy that criterion. No split is warranted because the secondary ARC_1 signal is subordinate and does not represent a distinct narrative function at comparable weight. Recommended for inclusion in the rising arc bucket for H6 hypothesis testing.
- **Action:** REINTERPRET

---

## Topic 56 — Promising Never to Hurt You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_6 (norm: ARC_6)

> you'll get hurt," he managed to say. "

> you know i’ll never hurt you .”

> i’ll make sure you aren’t hurt.” “

> *(CELL_D, tertile=middle)* It’s all well and good saying you avoid pain by avoiding relationships, but what about the wonderful things you’re avoiding as well?

> *(CELL_D, tertile=end)* He says that he knows it must hurt, but that whatever will be, will be, and that nothing we say or do will resolve things.

> *(CELL_C, tertile=begin)* You didn’t hit me with a sledgehammer last night, did you?” “

> *(CELL_C, tertile=middle)* I didn’t know why I felt hurt, but it stung not to be invited. “

### Pass A/B/C

- **A lexical:** `ARC_4`
  - Across all four keyword lists the dominant lexical cluster centres on pain and harm inflicted within the relationship: 'hurt/hurting/harm/hurts/painful/distress' (Main, KeyBERT, POS, MMR) combined with relational-address terms ('you', 'want', 'don', 'never', 'won') and emotionally charged verbs ('cried', 'insisted', 'assured', 'protect', 'threatened', 'causing'). The pattern — one party causing or fearing causing pain to the other, with assurances and protests — is characteristic of relationship-caused distress (ARC_4): the romantic bond itself is the source of the emotional suffering being expressed. There is no clear evidence of a secret being maintained (ARC_1), an escalating argument (ARC_2), a separation threat (ARC_3), a disclosure (ARC_5), or repair/reconciliation (ARC_6/7/8). 'Threatened' and 'protect' could hint at external danger, but the surrounding pain/harm vocabulary keeps the focus squarely on interpersonal relational distress, not an outside plot threat.
- **B contextual:** `ARC_6`
- **C adjudicate:** `ARC_6`
  - The lexical consensus (ARC_4) reflects surface-level distress vocabulary, but the contextual dominant (ARC_6) is better supported by the full evidence profile. Taxonomy label 4.6 'Emotional Safety, Reassurance & Caretaking' with secondary 9.2 'Promise, Vow & Future-Tense Speech Acts' points toward active relational repair rather than mere suffering — the caretaking and reassurance are directed at mending or stabilizing the bond, not simply expressing pain within it. Radway R8 ('Hero treats heroine tenderly') and R11 (likely hero's capitulation/emotional openness) are canonical reconciliation/repair beats in Radway's arc schema, not distress beats. Stage11 codes RAX_emotional_reassurance and RAX_emotional_security similarly index restoration of safety rather than ongoing deterioration. The combination of tender treatment, future-tense vows, and emotional security language is consistent with a post-conflict repair moment (ARC_6) rather than relationship-caused distress (ARC_4). ARC_4 would require the relationship itself to be the source of ongoing harm with no repair signal; the metadata collectively contradicts that reading. Classifying as ARC_6 (apology/reconciliation/repair) and placing in REFINED_RISING for H6 is the most defensible resolution. No manual review required given strong cross-signal convergence.
- **Action:** REINTERPRET

---

## Topic 94 — Caught in A Lie

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** MIXED

> i’ve known him for a long time, and i’m confident that i could tell if he was lying.”

> i’ve lied, therefore i’m a liar.

> i never meant to—” “how can i believe a single thing you say when you’ve already been proven a liar?”

> *(CELL_B, tertile=middle)* I have no reason to lie to you about something like that,’ she said. ‘

> *(CELL_D, tertile=middle)* Why don’t you stop being such a baby about it and lie still and I’ll go get something for you?”

> *(CELL_D, tertile=middle)* The sinking sensation that swept over him gave the lie to his efforts to convince himself it wasn’t.

### Pass A/B/C

- **A lexical:** `ARC_5`
  - Main rep is dominated by deception/truth vocabulary (lie, lied, lying, liar, honest, lies, honesty, truth), which strongly signals a disclosure or confrontation about hidden truths between the main couple — ARC_5 (disclosure). KeyBERT reinforces this with 'apologize' and 'hesitate', consistent with a character revealing or confessing something difficult. POS and MMR introduce formal/authority-register words (president, sir, direct, terms, sentence, threatened) that lack clear romantic-arc anchoring, pointing to ARC_10 (unclear arc role) in isolation. However, the Main rep carries the heaviest semantic weight for topic identity, and the deception-to-truth cluster is the defining signal. Consensus lands on ARC_5 (disclosure) as the dominant arc role, with disagreement flagged because POS/MMR pull toward an unclear or external register.
- **B contextual:** `ARC_1`
  - Topic 94 is overwhelmingly about lying and accusations of lying between characters. The recurring pattern — direct accusations ('You lied to me,' 'Liar'), denials ('I did not lie to you'), and meta-commentary on lying ('You are not a very convincing liar') — maps squarely onto ARC_1 (misunderstanding), where deception or perceived deception creates interpersonal conflict rooted in a breakdown of honest communication. BOOK_001 clearly involves a named dyad (Emma and a male partner), strongly suggesting a main couple. BOOK_002–004 lack sufficient context to confirm main-couple status, so those are coded 'unclear.' Two sentences (BOOK_002_3, BOOK_002_6) are off-topic (literal instruction to lie still; an exclamation unrelated to deception conflict), coded ARC_0. BOOK_003_6 references a philosophical statement about lying and consequences, edging toward ARC_5 (disclosure/truth-telling theme) rather than pure accusation. ARC_1 exceeds 70% and is the clear dominant code.
- **C adjudicate:** `MIXED`
  - Lexical consensus (ARC_5 disclosure) and contextual dominant (ARC_1 misunderstanding) point to overlapping but distinct mechanisms within Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information). Both codes are plausible: the topic likely captures moments where hidden information is either revealed (ARC_5) or withheld/misread in a way that generates misunderstanding (ARC_1). Because neither code fully subsumes the other and the secondary taxonomy flag (4.4 Conflict, Distance & Breakup Threats) adds further ambiguity, a single ARC_# cannot be assigned without loss of fidelity. MIXED is therefore the correct arc_role. The construct bucket is REFINED_FALLING because both disclosure and misunderstanding typically drive relational deterioration in the narrative arc. Manual review is required to inspect representative documents and determine whether disclosure precedes or follows the misunderstanding, which would allow a future SPLIT into two cleaner topic clusters.
- **Action:** REINTERPRET

---

## Topic 96 — Confessing Long-Standing Worry

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_4 (norm: ARC_4)

> i’ve been worried about you, [person].

> i’ve worried about you since i was twelve.

> i’ve been worried about you.” “

> *(CELL_D, tertile=middle)* You grew up worrying about having your basic needs met.

> *(CELL_D, tertile=middle)* Don't beat yourself up about it.

> *(CELL_B, tertile=begin)* We didn’t want to worry you.”

### Pass A/B/C

- **A lexical:** `ARC_10`
  - All four keyword lists centre on worry, concern, fear, and being bothered ('worry, worried, concern, worrying, concerned, fears, bothering, bothered, assure, problems'). While 'assure' hints at possible reassurance, there is no lexical evidence tying these anxieties specifically to the main romantic relationship — no relational repair, no conflict between the couple, no disclosure, no commitment signal. The worry/concern vocabulary could equally apply to external threats, self-concern, or third-party issues. 'Amusement' and 'sounding' in MMR/POS add tonal ambiguity without clarifying relational function. The topic therefore cannot be confidently assigned to any specific arc stage, making ARC_10 (ambiguous) the appropriate consensus code.
- **B contextual:** `ARC_4`
- **C adjudicate:** `ARC_4`
  - The lexical consensus (ARC_10) reflects surface ambiguity between warmth/tenderness and distress, but the contextual dominant (ARC_4) is better supported by the overall evidence. Taxonomy label 4.6 'Emotional Safety, Reassurance & Caretaking' with secondary 3.2 'Negative Emotions & Distress' is consistent with ARC_4: the tenderness and caretaking present in this topic are responses to relationship-caused distress rather than evidence of restored trust (ARC_7) or mutual commitment (ARC_8). Radway R8 ('Hero treats heroine tenderly') and R9 are plausible surface readings, but tenderness in the context of ongoing relational pain does not constitute trust restoration or resolution — it is better read as emotional management within a distressed relationship. Stage11 codes (RAX_emotional_reassurance, RAX_emotional_security, RAX_tenderness_core) might superficially suggest ARC_7, but per the critical rules, reassurance alone does not qualify as restored trust unless the relationship's closeness is demonstrably being rebuilt. The metadata is therefore 'mixed': taxonomy and Radway labels partially support a rising reading, but the distress secondary and contextual judgment tip the balance to ARC_4 (falling). Manual review is recommended to confirm that the tenderness here is not functioning as a genuine trust-restoration moment (which would warrant ARC_7 reclassification).
- **Action:** REINTERPRET

---

## Topic 100 — Promising to Find Her

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** ARC_10 (norm: ARC_10)

> i promise, i’ll bring her right back.”

> i’ll hurry and see if i can catch her.”

> i’ll look until she’s found.”

> *(CELL_A, tertile=end)* She won’t be able to leave, to rest, to pass over, whatever it is, until we find her.” “

### Pass A/B/C

- **A lexical:** `ARC_10`
  - The keyword sets contain logistical/procedural language (find, meet, needs, leave, where, urgency, decision, dismissed, planning, expect) and social-register markers (sir, mister) without any clear signal of a romantic relationship arc. 'Hiding' and 'replaced' could hint at ARC_1 or ARC_3, but they are isolated cues with no corroborating romantic-couple context. 'Dismissed' and 'urgency' suggest an external or transactional scene rather than a relational one. The overall picture is too ambiguous to assign a specific arc code, making ARC_10 the appropriate consensus.
- **B contextual:** `ARC_10`
- **C adjudicate:** `ARC_10`
  - Lexical and contextual consensus both land on ARC_10 (ambiguous), and the adjudication metadata is genuinely mixed rather than clarifying. The taxonomy label (9.2 Promise, Vow & Future-Tense Speech Acts) and Radway R8 (hero treats heroine tenderly) point toward ARC_7 (restored trust/reassurance) or ARC_8 (mutual commitment), but neither is confirmed without evidence that trust is being *restored* (ARC_7) or that a *relational resolution* is being reached (ARC_8). Promises and vows can appear at any narrative stage — early courtship, mid-arc reassurance, or final resolution — so future-tense speech acts alone do not anchor the arc position. The Stage11 prior code RAX_protective_commitment similarly straddles ARC_7 and ARC_8 without resolving the ambiguity. Radway R11 and R13 as secondary/plausible codes further diffuse the signal. Because the topic cannot be reliably placed in rising (ARC_5–8) or falling (ARC_1–4) without additional positional or contextual evidence, it is excluded from strict H6 hypothesis testing. Manual review is recommended to examine whether the promises/vows occur in a repair context (→ ARC_7) or a final-resolution context (→ ARC_8), which would allow reclassification.
- **Action:** KEEP

---

## Topic 102 — Grief Etched on His Face

- **Taxonomy:** 3.2 — Negative Emotions & Distress
- **Code:** ARC_10 (norm: ARC_10)

> we’ve lost adam,’ she whispered and her fingers traced the contours of grief still etched on his face. ‘

> not only did she have a cool and savvy partner actually in the game with her, the surroundings, the actions were so real that her heart pounded and adrenaline flooded her, almost as if she really was helping adam sabotage a bridge while avoiding capture by nazi soldiers.

> holy hell, adam—i’ve known her long enough to realize she’s thinking about a lot more than a blowjob.” “

> *(CELL_B, tertile=end)* And on that thought, he said, “I talked to Adam a minute ago.

### Pass A/B/C

- **A lexical:** `ARC_10`
  - Main keywords (adam, cain, penn, denver, brother) suggest a scene involving male characters—possibly brothers or rivals—but no clear romantic-relationship function is signaled. KeyBERT offers 'affection, sadness, secretly, blurted, shivered' which hint at emotional distress or concealed feeling, nudging toward ARC_4 (relationship-caused distress) or ARC_1 (secret maintained), but without a clear romantic-couple anchor these remain ambiguous. POS and MMR keywords (distraction, glint, surroundings, instincts, sweeping, pleading, blurted) are largely atmospheric/action-oriented with no definitive romantic-arc signal. The combination of male-character names, possible sibling dynamics, and scattered emotional cues does not resolve to a specific arc function for the main couple, making ARC_10 (ambiguous) the most defensible consensus despite KeyBERT's mild lean toward ARC_4.
- **B contextual:** `ARC_10`
  - Topic 102 is entirely composed of highly truncated sentence fragments centered on a character named 'Adam' — questions, exclamations, brief actions, and dialogue tags ('Adam asked.', 'Adam muttered.', 'Adam sighed.', etc.). These fragments provide no relational context whatsoever: there is no indication of who Adam's romantic partner is, what the relationship state is, or whether any arc-relevant event is occurring. The topic appears to be a character-name anchor topic capturing sentences that mention 'Adam' across multiple books, without any coherent narrative function. Because no romantic relationship can be identified or assessed from these fragments, all sentences are coded ARC_10 (ambiguous) with main_couple=unclear. The topic should be excluded from H6 arc analyses.
- **C adjudicate:** `ARC_10`
  - The lexical and contextual consensus both land on ARC_10 (ambiguous), and adjudication confirms this is the most defensible single code. The supporting metadata is internally mixed: Radway R8 (hero treats heroine tenderly) and Stage11 RAX_protective_commitment point toward a rising/repair function (ARC_7 territory), while RAX_individual_distress and the primary taxonomy label 3.2 Negative Emotions & Distress pull toward a falling arc (ARC_4 or ARC_3). Crucially, neither signal is strong enough to override the other. The tender/protective elements do not clearly evidence trust being *restored* (required for ARC_7), and the distress elements are not clearly tied to relationship deterioration caused by the couple's dynamic (required for ARC_4). The secondary taxonomy label 4.2 Ongoing Courtship & Everyday Relational Bonding further muddies the picture by suggesting routine relational texture rather than a discrete arc event. Because the topic sits at the intersection of distress and tenderness without a clear directional arc function, it cannot be reliably assigned to either the rising or falling construct bucket for H6 hypothesis testing. Manual review of representative documents is required to determine whether the distress is protagonist-internal (→ ARC_9 or ARC_0) or relationally consequential (→ ARC_4 or ARC_7), and whether the tenderness constitutes trust restoration or merely affective warmth.
- **Action:** REINTERPRET

---

## Topic 109 — Seeing Past A Guarded Identity

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_5 (norm: ARC_5)

> i’ve hardly heard a thing about you.”

> anyone could’ve walked by.

> even people who are close to you, who’ve known you far longer than i have, don’t know any more than what you’ve allowed them to see.

> *(CELL_D, tertile=middle)* But if you really knew me, you would realize how very much I resented your taking control of my life by calling that inspector.”

### Pass A/B/C

- **A lexical:** `ARC_5`
  - All four keyword lists converge on identity disclosure. Main keywords ('who, know, am, don, you, are, about, me, anyone, is') form a classic 'who are you / do you know who I am' interrogative cluster signaling identity revelation. KeyBERT ('recognize, hi, fitting') reinforces recognition/identification of a person. POS ('identity, muffled, current, loose') anchors the topic explicitly to 'identity' with 'muffled' suggesting concealment or disguise. MMR ('dealing, identity, playfully, doubted, fitting, muffled, recognize, hi, thinks, loose') adds 'doubted' and 'playfully' alongside 'identity/recognize/muffled', consistent with a scene where a character's identity is hidden or uncertain and then revealed or questioned — a disclosure dynamic. No cues point to external plot threat, breakup, or repair; the dominant signal is identity-based disclosure (ARC_5).
- **B contextual:** `ARC_10`
  - Topic 109 clusters around the theme of knowing/not knowing someone's true identity. The largest single code is ARC_10 (unclear arc role), assigned to sentences that are too fragmentary or context-free ('It's me.', 'That would be me.', 'Who is it that wants to know?') to map to a specific narrative arc function. Among the interpretable sentences, ARC_1 (misunderstanding) is the next most common, covering lines where one partner challenges the other's claim to know them ('You don't even know me, not really'; 'You haven't got a clue who I am'). ARC_5 (disclosure) applies where a character reveals or invites revelation of their true self. ARC_2 and ARC_8 each appear once. No single code reaches 70%, but ARC_10 is dominant at ~45%. Main-couple probability is moderate (~0.60) because many sentences are clearly between romantic partners but several are too decontextualised to confirm.
- **C adjudicate:** `ARC_5`
  - Lexical consensus (ARC_5 disclosure) and taxonomy placement (4.3 Secrets, Misunderstandings & Hidden Information) are mutually reinforcing: the topic centers on hidden information that is surfacing or at risk of surfacing between the main couple, which is the definitional core of ARC_5. The contextual dominant ARC_10 (unclear_arc_role) reflects annotator uncertainty about narrative timing rather than a genuine absence of arc signal — the taxonomy anchor resolves that ambiguity in favor of ARC_5. Secondary taxonomy 3.3 (Ambivalence & Internal Conflict) is consistent with ARC_5: a character wrestling internally with whether/how to disclose is a standard precursor to the disclosure event itself, not a competing code. Because disclosure typically destabilizes the relationship before repair, this sits in the REFINED_FALLING construct bucket. No free-form labels were carried forward; ARC_10 is retired as the dominant in light of the stronger lexical and taxonomic evidence.
- **Action:** REINTERPRET

---

## Topic 119 — Offering to Keep Her Safe

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_9 (norm: ARC_9)

> come on, i’ll protect you.”

> you’ll protect me?” “

> i can protect you from crystal, but you’ll have to let me.

> *(CELL_D, tertile=begin)* I’m your man for getting you to the point of passing out, if you ever want to take that risk.”

> *(CELL_C, tertile=middle)* At least in LA you’d both have protection; you know my security guys are some of the best in the business.

> *(CELL_C, tertile=end)* I didn’t think security would leave you standing out here like this.’ ‘

### Pass A/B/C

- **A lexical:** `ARC_9`
  - All four keyword lists converge on an external-threat/protection cluster: 'dangerous,' 'threat,' 'protect,' 'guarded,' 'secure,' 'safety,' 'defend,' 'dangerously,' 'inevitable.' The vocabulary describes physical danger and the effort to guard someone from it. There is no lexical signal of relational deterioration, misunderstanding, secret, apology, or mutual commitment between the romantic couple. 'Precious,' 'caressed,' and 'assure' add a tender register but do not implicate the romantic arc itself — they are consistent with a protector-figure responding to external peril. 'President,' 'sir,' and 'terms' reinforce an external-stakes (possibly political/power) framing. Per the rules, external danger that does not itself deteriorate the romantic relationship codes as ARC_9.
- **B contextual:** `ARC_9`
- **C adjudicate:** `ARC_9`
  - Lexical and contextual consensus both land on ARC_9 (external plot conflict), and that judgment is defensible: the topic's core signal appears to be external danger or threat that prompts protective/caretaking behavior from the hero rather than a deterioration or repair of the romantic bond itself. However, the taxonomy label (4.6 Emotional Safety, Reassurance & Caretaking), the Radway codes (R8 hero treats heroine tenderly, R9, R10), and the Stage11 prior codes (RAX_emotional_reassurance, RAX_physical_protection, RAX_protective_commitment, RAX_tenderness_core) all foreground the relational texture of the interaction — tenderness, reassurance, protective commitment — which are hallmarks of ARC_7 (restored trust/reassurance) territory. This creates a genuine tension: the external threat is the precipitating context, but the hero's tender protective response is the dominant narrative content captured by the topic. Under strict ARC rules, external danger that does not itself deteriorate the romantic relationship remains ARC_9, and there is no clear evidence here that trust is being specifically restored (as opposed to simply expressed), so ARC_7 is not warranted. Nevertheless, the metadata signals are strong enough that this topic sits at the ARC_9/ARC_7 boundary and warrants manual review to confirm whether the protective-caretaking moments are purely reactive to external threat or whether they also function as relational repair/reassurance within the couple's arc. Assigned to EXTERNAL_PLOT_CONFLICT construct bucket with external H6 inclusion, pending review.
- **Action:** KEEP

---

## Topic 124 — Scooped Up in A Tight Hug

- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Code:** ARC_7 (norm: ARC_7)

> emma followed suit, and rebecca scooped her up in her arms and hugged her tight.

> he hugged her back.

> i stood up with her and hugged her. “

> *(CELL_A, tertile=begin)* He pulled me into his arms, wrapping me in a tender embrace. “

> *(CELL_C, tertile=begin)* She hugged Luke tightly for a moment, then rested one hand on the German Shepherd’s solid, eighty-pound body and struggled to her feet.

> *(CELL_C, tertile=end)* She seemed a little surprised to see Michael, but delighted too, greeting the boy with a hug.

> *(CELL_C, tertile=end)* Becky tumbled out of the wagon into Sorrel’s arms in a desperate hug.

### Pass A/B/C

- **A lexical:** `ARC_7`
  - All four keyword lists converge on physical expressions of warmth and closeness between characters: 'hug/hugged/hugging/embrace/tightly/tight' (Main), 'affection/greeted/fiercely/welcoming/squeeze/patted' (KeyBERT), 'reassuring/affection/promises' (POS), and 'hugged/reassuring/welcoming/eagerly/fiercely' (MMR). The repeated co-occurrence of 'reassuring' and 'welcoming' with intense physical embrace cues ('fiercely,' 'tightly,' 'enormous') indicates that closeness or trust is being actively restored or reinforced between the couple — not merely a neutral tender moment. This satisfies the ARC_7 threshold of trust/closeness being restored or strengthened, distinguishing it from simple affection (ARC_10) or a standalone commitment gesture (ARC_8).
- **B contextual:** `ARC_10`
- **C adjudicate:** `ARC_7`
  - The contextual dominant flagged ARC_10 (ambiguous), but the full metadata array consistently contradicts that judgment. Taxonomy 2.2 (Kissing & Non-Explicit Affection) combined with 4.6 (Emotional Safety, Reassurance & Caretaking) points to affective bonding with a restorative function, not mere ambiguity. Radway R8 (hero treats heroine tenderly) and R9 together signal a moment where the hero's behavior actively rebuilds or reinforces the heroine's sense of security within the relationship — the defining criterion for ARC_7 (restored trust/reassurance). Stage11 codes RAX_tenderness_core and RAX_nonexplicit_affection further anchor this as relational repair through physical and emotional gentleness rather than neutral or unresolved affect. The lexical consensus (ARC_7) is therefore upheld over the contextual ARC_10: the weight of converging evidence from taxonomy, Radway, and Stage11 all point to trust/closeness being actively restored or strengthened, satisfying the strict ARC_7 criterion. Manual review is recommended because the contextual read did flag ambiguity — reviewers should confirm that the tenderness depicted is directed at the main couple and functions as repair rather than baseline affection.
- **Action:** REINTERPRET

---

## Topic 128 — Confessing How Much You've Missed

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** ARC_7 (norm: ARC_7)

> i’ve missed most of his life already.

> and, god, how i’ve missed this.”

> i’ve come to realize that you are the one thing in my life i don’t want to miss.

> *(CELL_C, tertile=middle)* The suckhead you brought back with you here tonight…I saw it all.”

> *(CELL_C, tertile=end)* While I was in there, I also brought you something I thought you might be missing.”

### Pass A/B/C

- **A lexical:** `ARC_7`
  - Main keywords ('miss,' 'missed,' 'missing,' 'misses,' 'you,' 'too') strongly signal mutual longing and the acknowledgment of absence between two people, which in romance-novel context typically marks a moment of restored or strengthening closeness — characters expressing how much they have missed each other is a classic trust/closeness restoration beat (ARC_7). MMR reinforces this with 'solemnly,' 'breathlessly,' 'thoughtfully,' and 'voices,' suggesting an emotionally weighted, intimate verbal exchange, consistent with a reconciliation or reassurance scene. KeyBERT ('escaped,' 'honestly,' 'solemnly,' 'repeated') is ambiguous — 'escaped' could hint at external conflict or a secret, but without clear relational-deterioration cues it does not override the dominant signal; coded ARC_10. POS ('precious,' 'voices,' 'elevator,' 'pieces') is similarly ambiguous — 'precious' is tender but insufficient alone for ARC_7 without corroborating relational-repair cues; coded ARC_10. The dominant and convergent signal across Main and MMR is mutual emotional acknowledgment of longing/absence leading to restored closeness, supporting ARC_7 as consensus despite partial disagreement from KeyBERT and POS.
- **B contextual:** `ARC_3`
- **C adjudicate:** `ARC_7`
  - The contextual dominant code ARC_3 (separation/distance/breakup threat) is contradicted by the weight of converging metadata signals. Taxonomy 4.5 (Reconciliation, Commitments & HEA), Radway R11 (hero declares love and demonstrates commitment), R10, R9, and Stage11 labels (RAX_emotional_reassurance, RAX_emotional_security, RAX_tenderness_core) all point consistently toward a restoration or strengthening of closeness rather than a threat to the relationship. The lexical consensus ARC_7 aligns with this cluster. ARC_3 may have been triggered by surface-level language of distance or longing that precedes the reassurance moment, but the dominant function of the topic — as triangulated across taxonomy, Radway stage, and prior arc codes — is trust/closeness being actively restored or confirmed, satisfying the ARC_7 criterion. ARC_8 is ruled out because the evidence emphasizes emotional reassurance and security rather than a final mutual commitment resolution. Manual review is flagged because the contextual and lexical codes diverged, suggesting the topic may straddle a transitional beat (post-separation repair) that warrants human verification of narrative position before H6 inclusion.
- **Action:** REINTERPRET

---

## Topic 129 — Accused of Not Caring

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** ARC_4 (norm: ARC_4)

> like they care when they see that smoking-hot bod you’ve got.”

> at the moment, i could’ve cared less.

> you’ve never cared for anyone but yourself.”

> *(CELL_D, tertile=end)* I don’t care about that kind of stuff,” Zander assured him. “

> *(CELL_A, tertile=begin)* I don’t expect you to understand what it is to care about someone else.”

### Pass A/B/C

- **A lexical:** `ARC_4`
  - All four keyword lists converge on emotional distress and hurt within a relationship context. Main: 'care/cared/cares/caring' paired with negations ('don', 'less', 'didn') signals felt neglect or emotional withdrawal — a partner not caring enough, causing distress. KeyBERT: 'cared', 'mattered', 'sadly', 'unhappy', 'wondering' reinforce emotional pain and feeling unimportant to the other person. POS: 'unhappy', 'upset', 'worst', 'circumstances' describe a state of relationship-caused suffering. MMR: 'cared', 'treated', 'fault', 'smacked', 'circumstances', 'veins' suggest grievance over how one was treated, with blame attribution. No keywords indicate external antagonists (ruling out ARC_9), no clear misunderstanding frame (ARC_1), no separation/breakup threat (ARC_3), and no repair or commitment signals. The dominant signal is ongoing emotional distress caused by the relationship dynamic itself — fitting ARC_4 (relationship_caused_distress).
- **B contextual:** `ARC_10`
  - Topic 129 clusters around the word 'care' and its negations ('don't care', 'didn't care', 'cared too much'). The vast majority of sentences are decontextualised fragments — short rhetorical dismissals or ambiguous emotional statements — that cannot be reliably assigned to a specific narrative-arc function or confirmed as main-couple interactions. Three sentences (BOOK_002_5, BOOK_004_6, BOOK_005_4) carry enough relational context to suggest emotional distress tied to a romantic relationship (ARC_4: relationship_caused_distress): Lukas not caring while she cares too much, Jade being told she will always be cared for (implying prior hurt), and a character dying believing they were not cared for. All other sentences lack sufficient context to determine arc role or couple identity, coded ARC_10. ARC_10 dominates at 85%, well above the 70% threshold, making it the dominant code.
- **C adjudicate:** `ARC_4`
  - Lexical consensus (ARC_4: relationship_caused_distress) and taxonomy placement in 4.4 Conflict, Distance & Breakup Threats with secondary 3.2 Negative Emotions & Distress both point to emotionally driven distress arising from within the main-couple relationship. The contextual dominant ARC_10 (unclear_arc_role) reflects Pass B uncertainty, but the taxonomy metadata resolves that ambiguity: the content is not merely unclear — it is distress generated by the relationship dynamic itself, consistent with ARC_4. ARC_3 (separation/breakup threat) was considered but the taxonomy secondary tag (Negative Emotions & Distress) tips the balance toward ARC_4 as the primary signal, with breakup-threat elements as a contributing but not dominant feature. This sits firmly in the REFINED_FALLING construct bucket, representing deterioration of the main-couple bond through internally generated emotional suffering.
- **Action:** REINTERPRET

---

## Topic 157 — Swearing to Save Him From Himself

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** ARC_7 (norm: ARC_7)

> and you’ll get it, i swear,” [person].

> if [person] sees me like this, i'll die."

> and i might be young but i guess that just makes me lucky… i do love him and whether i have your help or not, i have to save him from himself… i know [person], i know what he’ll do, now that he thinks he has lost me.”

> *(CELL_B, tertile=middle)* Sam couldn’t understand it, and that bothered him.

> *(CELL_B, tertile=begin)* What else had Sam witnessed?

> *(CELL_B, tertile=begin)* Sam noticed stuff like that.

### Pass A/B/C

- **A lexical:** `MIXED`
  - Main keywords (samantha, samara, sammi, name, optimism, jonathan) suggest character naming/identification with ambiguous relational valence — ARC_10. KeyBERT (begged, confessed, willing, tense, brief) points toward a disclosure or confession moment — ARC_5. POS (dislike, worries, desperation, embarrassing, gritted) suggests emotional distress tied to the relationship — ARC_4. MMR (confessed, dump, dislike, gritted, worries) blends disclosure cues (confessed) with conflict/threat cues (dump, dislike) — ARC_5 edges out but 'dump' introduces a breakup-threat signal. The combination of confession/disclosure language (confessed, begged, willing) with distress and potential breakup threat (dump, dislike, desperation) across reps prevents a single clean code; MIXED is warranted.
- **B contextual:** `ARC_0`
  - Topic 157 is a character-name topic centered entirely on the name 'Sam' appearing in minimal sentence fragments (dialogue tags, address forms, brief attributions). The sentences contain no relational content, no couple dynamics, no conflict, no disclosure, no commitment — they are purely syntactic/attribution fragments. The one marginally notable sentence ('Sam, being Sam, meant he didn't tell me') hints at a withheld secret but lacks sufficient context to confirm romantic-couple implication. Across all three narrative positions the topic functions identically as a character-name anchor with no arc function. It should be excluded from H6 arc analyses.
- **C adjudicate:** `ARC_7`
  - The lexical consensus (MIXED) and contextual dominant (ARC_0) are overridden by the convergent weight of the metadata signals. Taxonomy 4.5 (Reconciliation, Commitments & HEA), Radway R11 (hero declares love and demonstrates commitment), R9, and R13, together with Stage11 codes RAX_emotional_reassurance and RAX_emotional_security, all point consistently toward a trust-restoration and reassurance function within the main romantic relationship. ARC_7 (restored trust/reassurance) is the best fit: the topic captures a moment where closeness and security are being actively rebuilt or affirmed between the couple, satisfying the ARC_7 criterion that trust/closeness is being restored or strengthened — not merely that tenderness is present. ARC_8 is not warranted because the evidence emphasises reassurance and emotional security rather than a final mutual commitment or resolution. The contextual judgment of ARC_0 is contradicted by the metadata; the topic is clearly couple-centric. Recommended for inclusion in the rising arc bucket for H6 hypothesis testing.
- **Action:** REINTERPRET

---

## Topic 175 — Gentleman Offers Steadying Support

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_7 (norm: ARC_7)

> the occurrences of the day were too full of interest to leave elizabeth much attention for any of these new friends; and she could do nothing but think, and think with wonder, of mr. [person]'s civility, and, above all, of his wishing her to be acquainted with his sister.

> mr. [person] placed his hand on [person]’s shoulder for support as mr. [person] barely walked out the front door.

> yes, but when i fell ill, it was apparent that i could not travel all the way to calais, so mr. [person] took me to the house of a friend of his: mr. [person].”

> *(CELL_B, tertile=end)* On his way to see Mistress Gwyllain to explain your…ah, unexplained arrival.”

> *(CELL_B, tertile=begin)* Shit," grunted Sheridan, apparently immune to Owen's considerable charms. "

### Pass A/B/C

- **A lexical:** `ARC_4`
  - Main keywords (mr, bingley, miss, georgiana, bennet, pemberley) point to secondary characters and social settings from Pride and Prejudice, suggesting peripheral or ensemble content with no clear romantic-arc signal — coded ARC_0. However, KeyBERT, POS, and MMR all converge on emotional distress vocabulary: 'worrying,' 'uncomfortably,' 'distress,' 'longing,' 'struggling,' 'passionate,' 'concerned,' 'injured,' and 'consumed' collectively indicate relationship-caused emotional suffering or anxiety rather than external threat, conflict escalation, or trust repair. The absence of reconciliation, disclosure, or commitment cues rules out ARC_5–ARC_8. The distress appears internally relational (longing, uncomfortably, passionate, consumed) rather than externally driven, pointing to ARC_4. Disagreement is flagged because Main alone would yield ARC_0, while the three semantic/contextual representations consistently signal ARC_4.
- **B contextual:** `ARC_10`
- **C adjudicate:** `ARC_7`
  - The lexical consensus (ARC_4) flags relationship-caused distress, and the contextual judgment (ARC_10) flags ambiguity, but the supporting metadata strongly points away from both. Taxonomy 4.6 (Emotional Safety, Reassurance & Caretaking) combined with Radway R8 (hero treats heroine tenderly) and Stage11 RAX_emotional_reassurance collectively describe a scene in which the hero actively soothes or shelters the heroine within the romantic relationship — a pattern that satisfies the ARC_7 criterion of trust/closeness being restored or strengthened, not merely expressed. ARC_4 would require evidence that the relationship itself is the source of distress; tender caretaking is the opposite dynamic. ARC_10 is unwarranted given the convergent metadata signal. The secondary Radway R9 and plausible R3 are consistent with a repair/reassurance beat rather than an escalating conflict. The secondary taxonomy (5.2 Friends, Allies & Social Circles) introduces mild ambiguity about whether the caretaking is dyadic or social, which is the primary reason manual review is flagged — if the reassurance is directed outward to allies rather than between the couple, the code could revert to ARC_10 or ARC_0. Absent that disconfirmation, ARC_7 is the best-supported single code, and the topic belongs in the rising (ARC_5–8) bucket for H6.
- **Action:** REINTERPRET

---

## Topic 177 — Seeing Past A Hidden Identity

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_1 (norm: ARC_1)

> you’ll no longer be alex.

> i know they say if you want something bad enough you’ll find any excuse to believe it’s true… but there was something in alex that called to me.

> tell me you understand that, or you’ll be no help to alex.”

> *(CELL_B, tertile=middle)* In the midst of my pleasure at seeing Alejandro literally backed up against a wall, I felt a pinprick of irritation at Jonno’s inability to see Eve as she was.

> *(CELL_B, tertile=end)* I couldn’t get what she’d said about Alejandro out of my head.

> *(CELL_B, tertile=middle)* I still couldn’t believe that she had been with Alejandro last night.

> *(CELL_B, tertile=middle)* It was ironic that he should do this now, when the last person she wanted to think about was Alex. ‘

### Pass A/B/C

- **A lexical:** `ARC_10`
  - Main keywords (sullivan, alexx, alexi, eliminate, woo, wanted, wasn, tell) suggest character names and vague action verbs with no clear romantic-arc signal; 'eliminate' and 'woo' are ambiguous without context. KeyBERT (instincts, realise, suffering, unsure) hints at internal emotional uncertainty but does not anchor to a specific arc stage. POS and MMR (dislike, guarded, fears, instincts, percent, movies, sidewalk, reminds, conscious) add hedged negative affect and mundane/observational terms that do not cohere into a recognizable arc role. No single arc stage — misunderstanding, escalation, separation, disclosure, repair, commitment, or external conflict — is clearly dominant across all four lists. All four reps independently land on ARC_10 (unclear arc role).
- **B contextual:** `ARC_2`
  - Topic 177 clusters around a named third-party figure ('Alex'/'Alejandro') who generates tension, jealousy, and friction between protagonists and their partners. The dominant signal is escalating interpersonal conflict (ARC_2): snapping, jealousy over Alejandro, complaints about Alex, and suspicion. One sentence shows a separation/withdrawal threat (ARC_3: Eve moving toward Alejandro). One shows relationship-caused distress (ARC_4: letting Alex run one's life). A few sentences from BOOK_005 shift to resolution/payoff (ARC_8, ARC_7) and off-target content (ARC_0), diluting but not overriding the dominant ARC_2 signal. ARC_2 reaches ~45%, well above the 70% threshold for a clean dominant code, so MIXED is not triggered; ARC_2 is dominant. Main-couple probability is moderate (~0.50) because many sentences involve a third party ('Alex'/'Alejandro') whose relationship to the main couple is unclear or indirect.
- **C adjudicate:** `ARC_1`
  - Lexical consensus was ARC_10 (unclear) and contextual dominant was ARC_2 (escalation_conflict), but the taxonomy metadata resolves the ambiguity: the primary taxonomy is 4.3 Secrets, Misunderstandings & Hidden Information. Hidden information and secrets are the structural driver here, making ARC_1 (misunderstanding) the most precise fit — misunderstandings in romance arcs are canonically rooted in withheld or distorted information between the main couple. ARC_2 may describe a surface symptom (conflict escalates because of the secret/misunderstanding), but the generative mechanism is ARC_1. The secondary taxonomy (3.3 Ambivalence & Internal Conflict) is consistent with ARC_1, as internal ambivalence often underlies why information is withheld. This places the topic firmly in the REFINED_FALLING construct bucket — the relationship is destabilised by the information asymmetry, not yet in repair. No free-form labels were carried forward; ARC_2 from Pass B is superseded by ARC_1 upon taxonomy reveal.
- **Action:** REINTERPRET

---

## Topic 210 — Expelled For Pursuing A Relationship

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** MIXED

> she’ll be back,” [person] to explain.

> we’ll not last long like this,” [person] said quietly.

> if you pursue a relationship with [person], you’ll be expelled from motherhouse ireland, removed from your triad, and cast out from our way of life.

> *(CELL_B, tertile=begin)* And, she’d reasoned, if pop star Jessica Simpson could resist the delectable Nick Lachey until their wedding night, she could certainly resist John.

> *(CELL_B, tertile=end)* Besides, if there was one thing she’d come to know about Zeke, it was that he was able to make every audience member feel connected to him.

> *(CELL_B, tertile=end)* Patrick huffed, as though he couldn’t believe Zeke had the audacity to claim that he—the up-by-his-boot-straps, self-made founder of a publishing empire—had anything in common with a bad-boy rock star.

> *(CELL_B, tertile=middle)* As a waiter moved away with their plates, John said, “By the way, I saw that Scarlet was linked to Zeke Woodlow in today’s gossip columns.

> *(CELL_B, tertile=end)* Unfortunately, a celebrity of Zeke’s caliber has an image to maintain and a publicity machine that needs to be fed—with the right kind of publicity, of course.” “

> *(CELL_C, tertile=begin)* The Hole was owned by a man named Peter Rabbit to the chagrin of his wife, Petra.

> *(CELL_B, tertile=begin)* Some would think that when swimming in the depths of one’s own grief, one could forget what it was that made them so unhappy, but tell that to Nathaniel.

> *(CELL_B, tertile=middle)* Either way, there was something exhilarating about being with Nathaniel, especially being with him in his lair.

> *(CELL_B, tertile=middle)* For the life of him, Nathaniel didn’t know how Mr. Harrington was a part of his beauteous bride-to-be’s biological makeup.

> *(CELL_B, tertile=begin)* Nathaniel had come to understand and grudgingly accept that fact.

### Pass A/B/C

- **A lexical:** `ARC_6`
  - KeyBERT and MMR both surface 'forgive,' 'afterward,' and 'instincts,' pointing toward a repair attempt following friction. MMR adds 'unwilling' and 'annoyance,' suggesting resistance to reconciliation but still within a repair arc. POS keywords ('disappointment,' 'annoyance,' 'unwilling,' 'distraction') lean toward ongoing relational distress (ARC_4), and Main keywords ('didn,' 'decided,' named characters) suggest a tense interpersonal moment that could read as misunderstanding (ARC_1). However, the convergence of 'forgive' and 'afterward' across two representors, combined with 'possibility' (of resolution) and 'proved,' tips the balance toward ARC_6 (repair) as the dominant arc role — a post-conflict moment where forgiveness and reconciliation are being negotiated, even if reluctantly.
- **B contextual:** `MIXED`
  - Topic 210 spans multiple books and narrative threads. BOOK_008 sentences dominate numerically and consistently reference a past relationship with 'Nick' that has ended or is being discussed as over, coding as ARC_3 (separation/breakup threat). BOOK_009 shows a couple in active conflict (Drake slamming out), coding as ARC_2. BOOK_006 involves emotional distress around Nathaniel and a bride-to-be, coding as ARC_4 or ARC_10 where context is insufficient. BOOK_002 sentences involve celebrity gossip and publicity concerns around Zeke, largely external/off-couple (ARC_9). BOOK_004_1 is entirely off-target (ARC_0). No single code reaches 70%, so dominant_code is MIXED. Main couple probability is moderate (~0.60) given that roughly half the sentences clearly reference a named romantic pair.
- **C adjudicate:** `MIXED`
  - Lexical consensus (ARC_6 repair) and contextual dominant (MIXED) diverge. Taxonomy 4.4 (Conflict, Distance & Breakup Threats) with secondary 5.1 (Family, Kinship & Parenthood) suggests the topic straddles active repair attempts and ongoing separation/breakup threat pressures — likely a moment where the couple is trying to reconcile but family-related conflict is simultaneously threatening the relationship. ARC_6 alone undersells the destabilising breakup-threat dimension; MIXED (ARC_6 + ARC_3) is the most defensible resolution. The family secondary axis does not redirect this to ARC_9 (external plot conflict) because the distress is relational and couple-facing rather than purely external. Construct bucket is REFINED_FALLING because repair is incomplete and breakup threat remains active, placing this in the descending/trough zone of the arc rather than the recovery upswing. Manual review is flagged to confirm whether family pressure is an external driver (ARC_9 component) or purely a relational stressor absorbed into the couple dynamic.
- **Action:** REINTERPRET

---

## Topic 214 — Demanding to Know What Happened

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_1 (norm: ARC_1)

> oh my god, how did this happen?”

> please, tell me precisely what is happening to you.”

> and i need to know what’s going on to some extent so i don’t think the worst.

> *(CELL_D, tertile=end)* Damn you…tell me what happened!”

> *(CELL_D, tertile=middle)* What the hell has she done?”

> *(CELL_D, tertile=middle)* What has happened to you?”

### Pass A/B/C

- **A lexical:** `ARC_2`
  - KeyBERT, POS, and MMR all converge on escalation cues: 'caused/causing' (active harm in progress), 'worst' (peak negative intensity), 'extent' (measuring severity of damage), and 'precisely/honestly' (confrontational demand for truth). Main keywords ('hell, fuck, what happened, going, happening') are emotionally charged interrogatives signaling a heated confrontation or crisis moment — consistent with escalating conflict rather than a calm disclosure or repair scene. The combination of ongoing causation language ('causing', 'caused'), superlative severity ('worst'), and agitated interrogatives points to ARC_2 escalation_conflict as the dominant arc role. Main alone was coded ARC_10 because bare interrogatives without relational context are ambiguous, creating minor disagreement, but the three keyword-extraction methods override toward ARC_2.
- **B contextual:** `ARC_10`
  - All sentences in Topic 214 are short, decontextualized interrogative fragments ('What happened?', 'What's going on?', 'What the hell happened?'). They express reactive surprise or demand for information but carry no identifiable narrative arc role on their own — there is no indication of who is speaking, to whom, or in what relational context. No sentence can be reliably linked to a main couple, nor to a specific arc stage such as conflict, disclosure, repair, or commitment. The topic appears to be a BERTopic cluster of generic inquiry/reaction dialogue tags that are off-context for arc coding. ARC_10 (unclear_arc_role) is the appropriate code for all sentences. Main-couple probability is very low (~0.10) because the fragments are generic enough to appear in any character interaction.
- **C adjudicate:** `ARC_1`
  - Lexical consensus (ARC_2 escalation_conflict) and contextual dominant (ARC_10 unclear) diverge, but the taxonomy anchor — 4.3 Secrets, Misunderstandings & Hidden Information — is the decisive tie-breaker. Hidden information and secrets are the structural engine of ARC_1 (misunderstanding), not ARC_2 (escalation) or ARC_10 (unclear). ARC_2 would require evidence that conflict is actively intensifying beyond the misunderstanding stage; the secondary taxonomy tag (3.2 Negative Emotions & Distress) is consistent with the emotional fallout of a secret-driven misunderstanding rather than an independent escalation dynamic. ARC_10 is inappropriate because the taxonomy provides sufficient specificity to resolve ambiguity. The topic is main-couple focused (secrets/misunderstandings in romance BERTopic clusters are overwhelmingly dyadic). Construct bucket is REFINED_FALLING because secret-based misunderstandings typically appear in the falling/complication arc phase before disclosure or repair.
- **Action:** REINTERPRET

---

## Topic 237 — Hiding Someone Before He Arrives

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_5 (norm: ARC_5)

> i’ll call jared now.

> jared was just heading off to work but is going to need his shirt so i’ll be right back.”

> you can’t come because if jared catches one glimpse of you, he’ll know.

> *(CELL_C, tertile=end)* At that, several male heads popped out, one of them being Ronald, Dee’s boyfriend.

> *(CELL_A, tertile=end)* PJ," Garrett says, "how many times are you going to make me ask you to call me Garrett?" "

> *(CELL_A, tertile=begin)* Something is happening inside Garrett's head, a feeling so bizarre he can't quite place it, can't put a name to it.

### Pass A/B/C

- **A lexical:** `ARC_4`
  - Main rep leans toward interpersonal conflict via 'wrathfully', 'eyed', and named male characters in apparent confrontation, suggesting ARC_2 escalation. However, KeyBERT, POS, and MMR converge strongly on ARC_4 (relationship-caused distress): POS offers 'distress', 'disbelief', 'disappointed', 'wound', 'fingertips' (physical/emotional hurt); MMR reinforces with 'distress', 'collapsed', 'ripping', 'wound', 'warned'; KeyBERT adds 'worrying', 'distracted', 'privacy' — all pointing to emotional suffering and vulnerability experienced by a character within or because of a relationship dynamic. The physical injury cues ('wound', 'fingertips', 'ripping', 'collapsed') combined with emotional distress markers ('disbelief', 'disappointed', 'worrying') indicate a character in pain — likely relational in origin — rather than a direct escalating confrontation. Consensus falls to ARC_4 by 3-to-1 majority.
- **B contextual:** `ARC_10`
  - Topic 237 is dominated by fragmentary dialogue tags and brief action snippets (e.g., 'Jared queried', 'Jared shrugged', 'Garrett feels his face flush', 'Keep him coming') that provide no discernible narrative-arc signal. The sentences are almost entirely decontextualised speech-attribution fragments or minor physical actions. No clear main couple is identifiable across the books — BOOK_001 references a side character's boyfriend, BOOK_002 involves Garrett in unclear social interactions, BOOK_003 is pure dialogue attribution for Jared, BOOK_004 involves a trio (narrator, Daniel, Gabriel) in what appears to be a crisis/care scene but without enough context to assign a specific arc role or confirm a main couple. BOOK_005 is a single dialogue fragment. The overwhelming majority of sentences are too fragmentary to assign a meaningful arc role, making ARC_10 (unclear_arc_role) the dominant code at ~95%. One sentence (BOOK_001_1) clearly involves a side character's relationship, coded ARC_0 (off_target).
- **C adjudicate:** `ARC_5`
  - Lexical consensus (ARC_4: relationship_caused_distress) and contextual dominant (ARC_10: unclear_arc_role) are in tension. The taxonomy anchor — 4.3 Secrets, Misunderstandings & Hidden Information — provides the decisive tiebreaker. Hidden information and secrets are the structural engine of ARC_5 (disclosure), not merely ambient distress (ARC_4) or an unresolved arc role (ARC_10). The secondary taxonomy tag (7.1 Interpersonal Non-Romantic Conflict) does not override the main-couple filter; the secrets/hidden-information frame is most plausibly directed at the main couple's dynamic. ARC_5 sits in the REFINED_FALLING construct bucket because disclosure events typically precede or precipitate conflict escalation rather than resolving it. Manual review is flagged because the ARC_10 contextual read suggests the topic's token distribution may be ambiguous enough that some passages could belong to non-romantic interpersonal conflict (ARC_9 or ARC_0), warranting human verification before finalising the main_couple=true assignment.
- **Action:** REINTERPRET

---

## Topic 240 — Unsure How to Offer Comfort

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_7 (norm: ARC_7)

> oh my god, sean!

> sean pursed his lips, unsure he was equal to the task of comforting [person].

> sean held out his hand and added; “now if you’ll excuse me i have a beautiful woman waiting to have breakfast with me.”

> *(CELL_B, tertile=begin)* Oh,” I said, thinking fast, watching as Seth started to show Liam how to use another nearby machine, while the Tiffanys and Brittanys gathered round, looking more worshipful than ever.

> *(CELL_B, tertile=end)* You need to stop nipping at him and face the fact that when Shon goes under, he’s off limits, one breath away from being a hostile at our backs.” “

### Pass A/B/C

- **A lexical:** `ARC_10`
  - The keyword sets contain character names (sean, jaime, bryan, yseult, morrissey) and dialogue/reaction cues (answered, said, looked, mumbled, solemnly, absently, winced, patted, shivered, ducked) alongside emotional/cognitive states (anxious, unsure, conscious, distracted, curious). None of these cues point clearly to a specific arc function: there is no evidence of conflict escalation, disclosure, reconciliation, commitment, separation, or trust restoration between a main romantic couple. The 'repressive' and 'brogue' terms add cultural/atmospheric color without arc specificity. The overall picture is of a scene involving interpersonal interaction and mild tension/anxiety, but the romantic arc function cannot be determined from lexical evidence alone, making ARC_10 (ambiguous) the appropriate consensus code.
- **B contextual:** `ARC_0`
  - Every sentence in this topic is a degenerate fragment consisting solely of a character name ('Sean') followed by a dialogue tag or brief action ('asked.', 'said,', 'shrugged.', 'met his gaze.', etc.) with no surrounding context. The topic appears to be a BERTopic artifact capturing a character-name/dialogue-attribution pattern rather than any meaningful narrative content. There is no evidence of romantic relationship dynamics, no identifiable main couple, and no relationship state change. The topic is uniformly ARC_0 (unrelated to the main couple arc) across all narrative positions and should be excluded from H6 arc analyses.
- **C adjudicate:** `ARC_7`
  - The lexical consensus (ARC_10) and contextual dominant (ARC_0) both suggest ambiguity or irrelevance to the main couple arc, but the full metadata package strongly contradicts that reading. Taxonomy 4.6 (Emotional Safety, Reassurance & Caretaking) with secondary 4.2 (Ongoing Courtship & Everyday Relational Bonding), Radway R8 (Hero treats heroine tenderly) and R9, and Stage11 codes RAX_emotional_security and RAX_protective_commitment all converge on a topic that is actively functioning within the romantic relationship — specifically around the restoration or reinforcement of closeness and safety between the couple. Per the critical rules, ARC_7 requires evidence that trust or closeness is being restored or strengthened, not merely that tenderness is present. However, RAX_emotional_security and RAX_protective_commitment, combined with R8/R9 and taxonomy 4.6, collectively indicate that the topic depicts the hero actively providing reassurance and safety to the heroine in a relational context — which meets the ARC_7 threshold of trust/closeness being strengthened. ARC_0 is therefore rejected: the topic is couple-facing. ARC_10 is also rejected because the metadata converges clearly enough to resolve ambiguity. The contextual dominant was likely misled by surface-level absence of explicit conflict-repair language, but the functional role is rising-arc relational reinforcement. Manual review is flagged because the lexical and contextual passes diverged significantly from the metadata-supported resolution.
- **Action:** REINTERPRET

---

## Topic 247 — Promising You Will Not Be Alone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** ARC_7 (norm: ARC_7)

> if we make it through this alone, we’ll just be better at being alone.”

> you’ll never be alone.

> before you say no, i want you to know i’ll be alone mostly.

> *(CELL_B, tertile=end)* If I went out alone, it seemed I felt surrounded by people who couldn’t speak to me.

> *(CELL_B, tertile=begin)* I promise you, you will never be alone again so long as I live.”

> *(CELL_B, tertile=begin)* I’ve pictured this so many times in my mind, I don’t want to wake up and find I’m alone again.” “

### Pass A/B/C

- **A lexical:** `ARC_3`
  - Main keywords ('alone', 'solitude', 'rather', 'prefer', 'don', 'live here') strongly suggest a character expressing a desire for separation or withdrawal — classic separation/distance language. MMR reinforces this with 'chose', 'insisted', 'planned', 'preferred', 'circumstances', 'fault' — implying a deliberate decision about the relationship's continuation under difficult conditions, pointing to a breakup threat or distancing dynamic. KeyBERT's 'upset' and 'praying' suggest emotional distress consistent with relational strain (ARC_4), but the dominant signal across Main and MMR is one of chosen separation or threatened departure. POS terms ('options', 'terms', 'circumstances', 'attempt', 'fault') are ambiguous on their own but align with a negotiation or confrontation about the relationship's future. The weight of evidence favors ARC_3 (separation/distance/breakup threat) as the consensus, with minor disagreement from KeyBERT (ARC_4) and POS (ARC_10).
- **B contextual:** `ARC_4`
- **C adjudicate:** `ARC_7`
  - The lexical consensus (ARC_3) and contextual dominant (ARC_4) both point toward distress or deterioration, but the full metadata picture contradicts that reading. Taxonomy 4.6 (Emotional Safety, Reassurance & Caretaking) with secondary 9.2 (Promise/Vow/Future-Tense Speech Acts) describes a scene in which the hero actively works to soothe and secure the heroine — not to threaten or distance. Radway R8 (hero treats heroine tenderly) is the primary Radway code, which is a canonical marker of trust restoration, not conflict escalation. Stage11 codes RAX_emotional_reassurance and RAX_emotional_security further confirm a restorative, not deteriorating, relational function. ARC_4 (relationship-caused distress) would require the relationship itself to be the source of harm; here the relationship is the vehicle of repair. ARC_3 (separation/breakup threat) is unsupported by any of the secondary labels. The convergence of tender treatment, reassurance, caretaking, and future-tense vows maps most precisely onto ARC_7 (restored trust/reassurance), where closeness is being actively rebuilt or reinforced. Manual review is flagged because the lexical signal diverges from the contextual/metadata signal, suggesting the topic may contain surface-level distress language that is functionally resolved within the same narrative moment — a potential SPLIT candidate if token-level inspection reveals a distinct distress sub-cluster.
- **Action:** REINTERPRET

---

## Topic 264 — Accused of Hiding Something

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** MIXED

> i’ve been hiding out in here, avoiding contact with the human leech.” “

> i haven’t been hiding, i’ve been working.

> he cut in before i could get a word out, "funny thing is i've had this gut feeling all along that you're hiding something.

> *(CELL_C, tertile=end)* Two shots from the same hide were enough to set his warning bells ringing.

> *(CELL_C, tertile=middle)* The closet had been a great hiding place for all of two seconds for two people, but it had turned into a torture chamber.

### Pass A/B/C

- **A lexical:** `ARC_5`
  - Main is dominated by concealment vocabulary ('hide', 'hiding', 'hidden', 'concealing', 'keep from') pointing strongly to ARC_5 (disclosure/secrets being kept). KeyBERT reinforces this with 'hiding' and 'revealing' as the core tension — something is being concealed and potentially exposed. POS adds 'identity', 'activities', 'choices', and 'secure places', consistent with a character hiding their identity or secrets (ARC_5). MMR introduces 'weapons', 'remote', 'blows', and 'cleared', which shift toward external/action-plot concealment (ARC_9 — external plot conflict involving hiding weapons or fugitive activity). Despite MMR's external-plot lean, the dominant signal across three of four representations is secret-keeping and potential revelation centered on a person's identity or activities, which maps to ARC_5. Disagreement flagged due to MMR's divergent external-threat framing.
- **B contextual:** `ARC_9`
  - Topic 264 is dominated by the semantic field of hiding, concealment, disguise, and cover — physical actions associated with evasion, surveillance, and tactical positioning. These are external-plot/action-thriller elements (shots from a hide, covering positions, hiding from a pursuer, disguises, scars). None of the sentences clearly depict a main-couple romantic dynamic; most are ambiguous or clearly non-romantic in context. The topic maps cleanly to ARC_9 (external_plot_conflict) across all tertiles, with no evidence of relationship arc content.
- **C adjudicate:** `MIXED`
  - Lexical consensus (ARC_5 disclosure) and contextual dominant (ARC_9 external_plot_conflict) diverge, indicating the topic captures two distinct narrative functions that co-occur in the text. Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) aligns primarily with ARC_5, suggesting a revelation or hidden-information moment involving the main couple. However, the contextual signal for ARC_9 indicates the disclosure is embedded within or triggered by an external plot pressure rather than arising purely from interpersonal dynamics. Because neither code alone is sufficient and the taxonomy secondary is None, a MIXED designation is warranted. The construct bucket is REFINED_FALLING: a disclosure event that introduces or deepens tension places this in the falling/complicating arc phase rather than repair or resolution. Manual review is required to determine whether the external element is the primary driver (favoring ARC_9 as dominant) or merely the context for a couple-centered secret reveal (favoring ARC_5 as dominant), which would affect downstream hypothesis assignment.
- **Action:** REINTERPRET

---

## Topic 265 — Mismatched Expectations About Seriousness

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_4 (norm: ARC_4)

> shit,” shane cursed, but in a way that said he was thrilled with the news, not unhappy. “

> i get the impression you’ve led shane to believe you’re far more serious than you are.

> i want to concentrate on my studies, and you, my gosh, shane, you’ll have so many women hitting on you the second the ferry leaves the dock—” shane jerks his hand away. “

> *(CELL_B, tertile=begin)* As far as Tuck knew, Axel was the only one aboard who got spooked by Freaks.

### Pass A/B/C

- **A lexical:** `ARC_4`
  - KeyBERT and MMR both surface emotional-distress vocabulary ('emotionally', 'unhappy', 'trembled', 'embarrassment', 'shock') pointing to relationship-caused distress (ARC_4). POS reinforces tension with 'arguing', 'heated', 'embarrassment', 'unsure' which edges toward ARC_2 escalation, but the dominant emotional register is distress rather than pure conflict escalation. Main keywords are character names and neutral action verbs (burrowed, nod, play) offering no clear arc signal on their own (ARC_10). The weight of emotionally charged distress cues across KeyBERT and MMR tips consensus to ARC_4; disagreement is flagged because POS leans ARC_2 and Main is ambiguous.
- **B contextual:** `ARC_0`
  - All sentences in this topic are fragments — name utterances ('Shane said.', 'Shane.', 'Crikey.'), a brief third-person observation about a character named Tuck/Axel, and minimal dialogue tags ('Keith thought so.'). None contain sufficient narrative content to assign a romance arc role. The topic appears to be a BERTopic cluster anchored on character-name tokens or short dialogue punctuation fragments rather than any meaningful arc event. All sentences are coded ARC_0 (off_target). Main-couple probability is very low because no romantic dyad interaction is discernible from the fragments.
- **C adjudicate:** `ARC_4`
  - Adjudication resolves the lexical–contextual split in favour of ARC_4 (relationship_caused_distress). The contextual read of ARC_0 (off_target) is overridden by the taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information with a secondary tag of 4.4 Conflict, Distance & Breakup Threats: both subcategories describe distress that originates within the main-couple dynamic (hidden information causing emotional harm), which is the defining feature of ARC_4 rather than off-target content. ARC_1 (misunderstanding) was considered but the taxonomy secondary tag signals the distress has escalated beyond a simple misunderstanding into sustained relational harm, keeping ARC_4 as the better fit. The construct bucket is REFINED_FALLING because relationship-caused distress sits on the descending arc of the narrative (trust eroding, emotional damage accumulating) prior to any repair phase.
- **Action:** REINTERPRET

---

## Topic 272 — Silence Held Until Arrival

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_1 (norm: ARC_1)

> she didn’t speak a word until they got to their destination.

> the high priestess had said very little to her in the day and a half leading up to her departure.

> he should’ve known better than to think brenna would be content with the noncommittal answer he’d given her.

> *(CELL_B, tertile=end)* She was going to the hospital, and this time, she would not take no for an answer.

### Pass A/B/C

- **A lexical:** `ARC_1`
  - All four keyword lists converge on a scene of failed or withheld communication between characters. Main keywords (answer, didn, respond, question, reply, say, word, speak) directly signal someone not answering or refusing to speak. KeyBERT reinforces this with 'refused', 'lack', 'answers', 'answering', plus emotional fallout ('annoying', 'embarrassment'). POS and MMR add 'departure' and 'destination', suggesting one party leaves or withdraws rather than engaging, and 'upset', 'shock', 'rushed' indicate the emotional charge of the non-response. The dominant pattern is a breakdown in communication — one character not answering the other's questions, likely concealing something or stonewalling — which is the hallmark of ARC_1 (misunderstanding/withheld information driving relational tension), rather than an overt escalating fight (ARC_2) or a formal separation threat (ARC_3).
- **B contextual:** `ARC_10`
  - Topic 272 is dominated by short, decontextualized sentences expressing silence, withholding, or emotional withdrawal (e.g., 'She didn't want to hear it,' 'Jane didn't say anything,' 'He didn't speak'). These fragments lack sufficient context to assign a specific arc role — they could belong to many arc stages. No clear main-couple dyad is identifiable across books; most sentences are ambiguous about who the characters are relative to each other. One sentence (BOOK_001_6) hints at a post-fight avoidance, coded ARC_1 (misunderstanding/avoidance). Two sentences (BOOK_002_4, BOOK_004_2) suggest external plot action or third-party dynamics, coded ARC_9. The overwhelming majority (80%) are ARC_10 (unclear arc role). ARC_10 exceeds 70%, making it the dominant code. Main-couple probability is low (~0.15) given the lack of identifiable romantic dyad context.
- **C adjudicate:** `ARC_1`
  - Lexical consensus (ARC_1 misunderstanding) and taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information both point to a hidden-information-driven misunderstanding between the main couple. The contextual dominant ARC_10 (unclear_arc_role) reflects ambiguity in surface signals, but the taxonomy anchor resolves that ambiguity: the topic encodes a classic falling-arc beat where concealed information creates relational distance. The secondary taxonomy tag (8.5 Movement/Transit) is likely incidental framing rather than the core arc function. ARC_1 is therefore the correct resolution. Construct bucket is REFINED_FALLING because misunderstandings driven by secrets are a canonical early-to-mid narrative descent mechanism. No free-form labels were carried forward; ARC_10 is superseded by the stronger lexical and taxonomic evidence for ARC_1.
- **Action:** REINTERPRET

---

## Topic 285 — Confessing Years of Hatred

- **Taxonomy:** 3.2 — Negative Emotions & Distress
- **Code:** ARC_2 (norm: ARC_2)

> i’ve hated him for years.

> heath has done a wonderful job with him, but i—well, i’ve hated him for living instead of you.

> ever since this cunt came here, i’ve been, uh, less than balanced, i admit, and remembering things i’ve tried to forget, reasons to hate, reasons to hate, and you’ve become a liar.

> *(CELL_C, tertile=middle)* Looking back now, I can see all the hatred I had in me, but at the time it just seemed like everyone was out to get me.

> *(CELL_C, tertile=end)* It had been a long time since his presence had evoked disdain.

> *(CELL_B, tertile=middle)* And I hated submitting to your licentious thoughts and advances!” “

### Pass A/B/C

- **A lexical:** `ARC_5`
  - Main keywords ('hate', 'hated', 'hates', 'hating', 'hateful', 'myself') point strongly to internalized negative emotion directed at self or partner, suggesting relationship-caused distress (ARC_4). However, KeyBERT and MMR both surface 'admit', 'dislike', 'treated', 'deserve', and 'planning', which collectively signal a moment of confession or acknowledgment — a character admitting feelings (even negative ones like dislike or hatred) to another, consistent with disclosure (ARC_5). POS yields only 'purpose' and 'shock', which are too sparse to anchor a specific arc role (ARC_10). The convergence of 'admit' and 'dislike'/'hated' across KeyBERT and MMR tips the consensus toward ARC_5: a character disclosing previously hidden negative feelings (e.g., 'I hated you' or 'I have to admit I disliked how you treated me'), which is a classic romance-arc disclosure beat. Disagreement is flagged because Main leans ARC_4 and POS is unclear.
- **B contextual:** `ARC_2`
  - Topic 285 is saturated with hatred, loathing, and disdain language ('I hate you', 'hated him', 'loathed him', 'dislike'). All sentences express intense interpersonal hostility, which maps cleanly to ARC_2 (escalation_conflict) — the emotional peak of antagonism between characters. The topic is not about misunderstanding (ARC_1), separation (ARC_3), or external plot (ARC_9); it is the raw expression of conflict-level negative affect. Main-couple attribution is uncertain for roughly half the sentences (many use 'him/her' without clear dyadic context), but several BOOK_003 sentences and BOOK_002_2/3 plausibly involve the main couple, yielding a moderate main_couple_prob of ~0.45. No sentence reaches a repair, disclosure, or commitment register, so ARC_2 dominates at 100%.
- **C adjudicate:** `ARC_2`
  - Lexical consensus flagged ARC_5 (disclosure), but the contextual dominant signal is ARC_2 (escalation_conflict), which better captures the taxonomy metadata: Negative Emotions & Distress (3.2) as primary and Interpersonal Non-Romantic Conflict (7.1) as secondary. The secondary taxonomy tag initially pulled toward ARC_5 (a disclosure event can surface distress), but disclosure is not the defining arc function here — the dominant pattern is escalating relational conflict generating distress within the main couple. ARC_2 is therefore the correct resolution. The construct bucket is REFINED_FALLING, consistent with a conflict-escalation phase in the narrative arc. No free-form labels were carried forward; all prior Pass A/B terms are mapped to ARC_2. Manual review is not required given clear contextual dominance.
- **Action:** REINTERPRET

---

## Topic 301 — Confessing A Thin Relationship History

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_1 (norm: ARC_1)

> you know that because you’ve been with one other guy and had a long-term relationship?

> because one way or another it has tainted every relationship i’ve had since the roller-coaster success of my first book.”

> i've had sexual partners, but never a girlfriend.

> *(CELL_A, tertile=end)* Can I assume you two don’t have a…relationship?”

> *(CELL_C, tertile=end)* You will say anything to save your lover.

> *(CELL_A, tertile=middle)* But I’m not avoiding a good relationship.

### Pass A/B/C

- **A lexical:** `ARC_4`
  - Main keywords (boyfriend, mate, relationship, partner, status, don, mean) signal interrogation or anxiety about the relationship itself — not a discrete external threat or a repair moment, but ongoing relational distress tied to the couple's dynamic. KeyBERT reinforces this: 'emotionally', 'admit', 'worrying', 'ex' point to emotional strain and unresolved feelings causing distress within the relationship. MMR adds 'arrange', 'ripping', 'intend', 'afford', 'emotionally' — 'ripping' especially suggests pain or rupture, and 'ex' raises the spectre of a prior relationship complicating the current one, consistent with relationship-caused distress (ARC_4). POS keywords (partners, success, potential, secure) are more neutral/aspirational and lack clear conflict valence, warranting ARC_10 for that rep alone. Three of four reps converge on ARC_4, yielding consensus there despite POS dissent.
- **B contextual:** `ARC_1`
  - Topic 301 clusters around relationship-status ambiguity and questioning — 'do you have a boyfriend/girlfriend?', denials of being in a relationship, and challenges about who someone is with. These are predominantly misunderstanding or definitional-confusion signals (ARC_1), where characters are unclear or in dispute about the nature of their romantic connection. A substantial minority of sentences are too fragmentary or context-free to assign a specific arc role (ARC_10). Two sentences (BOOK_003_6, BOOK_005_1) reflect distress caused by relationship dynamics (ARC_4). Two sentences are off-target (ARC_0). ARC_1 reaches ~45%, above the 70% threshold is not met, but it is clearly dominant over all other codes. Main-couple probability is moderate (~0.55): several sentences plausibly involve the main couple negotiating relationship labels, but many are ambiguous or involve third parties.
- **C adjudicate:** `ARC_1`
  - Lexical consensus landed on ARC_4 (relationship-caused distress), but the taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information — with a secondary anchor in 3.3 Ambivalence & Internal Conflict — points to the distress being a downstream symptom rather than the primary arc mechanism. The contextual dominant ARC_1 (misunderstanding) better captures the generative engine: a hidden piece of information or a secret creates a misread between the main couple, producing the felt distress. ARC_4 describes the emotional register; ARC_1 describes the narrative function. In adjudication, narrative function takes precedence for arc_role assignment. The construct bucket is REFINED_FALLING because the misunderstanding is actively widening the relational gap rather than initiating repair. No free-form labels were carried forward from Pass A/B.
- **Action:** REINTERPRET

---

## Topic 303 — Confessing Long-Hidden Secrets

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_1 (norm: ARC_1)

> normally, tate would’ve finished the sentence she was working on, but the excitement in mabel’s voice jarred her completely out of the story, derailing her train of thought.

> i know it might cost me tate, but if i don’t tell him then everything we’ve built will be based on half-truths.” “

> tate sits down next to me, his eyes grim as he waits for me to share all the things that i've been keeping from him for so long.

> *(CELL_A, tertile=middle)* Damn it, he wondered if Joshua Tate knew the full extent of what he was taking on.

> *(CELL_A, tertile=begin)* Joshua Tate tugged at his collar and cleared his throat, his prominent Adam"s apple bobbing as he swallowed audibly. “

> *(CELL_B, tertile=middle)* I went to Woodson to interview Chandra Cunningham about Tana Mayfield.

> *(CELL_B, tertile=middle)* You seem to have the exclusive attention of the Lady Mayfield,” Kent mentioned once greetings had been exchanged between the three. “

### Pass A/B/C

- **A lexical:** `ARC_10`
  - Main rep offers a cluster of character names (tate, logan, kenzie, ang, chace, kent, sophia) with no relational-arc signal beyond 'agreed'; KeyBERT yields procedural/observational terms (nods, sentence, speaking, planned, anticipation, muffled, worrying, judging, winked) that suggest scene-level narration without a clear arc function; POS rep mixes physical/situational nouns and adjectives (rear, period, panicked, tracks, decent, television, sentence, current, wrists, ex) — 'ex' is the only faint relational hint but is too isolated to anchor an arc code; MMR rep contains action verbs (drawled, fumbled, hauled, circled, tipped) and modifiers (judging, occupied, bothering, muffled) that read as moment-to-moment scene texture rather than any identifiable arc beat. No representation supplies enough directional relational signal to assign a specific ARC_1–ARC_9 code, so ARC_10 (unclear_arc_role) is the unanimous consensus.
- **B contextual:** `ARC_0`
  - Topic 303 clusters around proper names — Joshua Tate (BOOK_003), Tana/Dotty/Laurel Mayfield (BOOK_004/005), and Tyrese Moore (BOOK_007). None of these sentences depict a romantic main-couple dynamic; they reference supporting characters, investigative dialogue, and third-party interactions. BOOK_005_5 hints at external plot manipulation (a staged accident, time travel), but the subject is a villain's scheme rather than main-couple arc content. All sentences are off-target for romance narrative-arc coding, yielding a unanimous ARC_0 classification and a main_couple_prob of 0.0.
- **C adjudicate:** `ARC_1`
  - Adjudication resolves the tension between lexical consensus (ARC_10 unclear) and contextual dominant (ARC_0 off_target) by applying taxonomy metadata. Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) is a strong signal that the topic content centers on hidden information or misunderstanding dynamics between the main couple — a classic REFINED_FALLING beat. ARC_0 (off_target) is overridden because the taxonomy assignment confirms main-couple relevance; ARC_10 (unclear) is overridden because the taxonomy provides sufficient semantic grounding. ARC_1 (misunderstanding) is the nearest valid code to the primary taxonomy category 4.3, capturing the secrets/hidden-information driver of conflict. The secondary taxonomy 4.5 (Reconciliation/HEA) is noted but does not dominate; it may indicate downstream repair potential but does not shift the arc_role to ARC_6/ARC_7/ARC_8 without stronger contextual evidence. No free-form labels were carried forward.
- **Action:** REINTERPRET

---

## Topic 305 — Confessing A Lifelong Regret

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** ARC_7 (norm: ARC_7)

> i know that now, and i’ll go to my grave regretting what i did to you.” “

> come on in, you’ll no doubt regret it.

> you’ll regret that.’ ‘

> *(CELL_B, tertile=middle)* You are surely not intending to imply that you are beginning to regret this marriage already?’ ‘

> *(CELL_B, tertile=end)* I fear that my careless remarks must have been the cause of that outburst.

### Pass A/B/C

- **A lexical:** `ARC_4`
  - Across all four keyword lists, the dominant signals are regret (regret, regretted, regrets, regretting, regrettable), emotional distress (fears, upset, embarrassing), and relational missteps (fumbled, handled, acted, remark, decision). The presence of 'promise' and 'assure' suggests the relationship is implicated — a promise or commitment has been broken or mishandled, generating distress. 'Drift,' 'ended,' and 'unable' reinforce a sense of relational damage caused by the couple's own dynamic rather than external forces. This pattern — internal regret and distress stemming from relationship-related decisions and actions — maps to ARC_4 (relationship-caused distress). There is no clear disclosure event (ARC_5), no escalating argument (ARC_2), and no repair/reconciliation (ARC_6), making ARC_4 the best fit across all representations.
- **B contextual:** `ARC_10`
- **C adjudicate:** `ARC_7`
  - The lexical consensus (ARC_4) and contextual dominant (ARC_10) diverge, but the convergent weight of the supporting metadata resolves the ambiguity toward ARC_7. Radway R10 ('heroine reinterprets hero's behaviour as result of previous hurt') is a canonical trust-restoration mechanism: the heroine's cognitive reframing of the hero's past actions is precisely what ARC_7 requires — closeness and trust are being rebuilt through new understanding, not merely expressed. R11 (hero's behaviour explained/excused) and R13 (heroine accepts hero) reinforce this trajectory. Taxonomy 4.5 (Reconciliation, Commitments & HEA) places the topic firmly in the rising arc family, and Stage11 labels RAX_emotional_reassurance, RAX_emotional_security, and RAX_tenderness_core all index the restoration of relational safety rather than ongoing distress. The ARC_4 lexical signal likely reflects residual distress vocabulary (the wound being reinterpreted) rather than active relationship-caused harm; the ARC_10 contextual judgment reflects genuine surface ambiguity but is overridden by the Radway/taxonomy/Stage11 convergence. Because the adjudication pivots on interpretive inference rather than explicit textual evidence, manual review is flagged. Assigned to REFINED_RISING for H6 inclusion as rising.
- **Action:** REINTERPRET

---

## Topic 314 — Fiancé Becoming A Stranger

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_10 (norm: ARC_10)

> macie had spent far more time praying for blake and far less time being driven by her constantly-shifting emotions.

> she peeked out and verified that it was indeed blake, then promptly shut the door in his face to remove the chain. “

> the blake i am engaged to is slowly disappearing in my mind, and being replaced by a complete and utter stranger.

> *(CELL_A, tertile=middle)* I wondered about that when you first told me you’d be staying with Brant.

### Pass A/B/C

- **A lexical:** `ARC_10`
  - Main rep is dominated by character names (blake, dion, macie, breydan, hewitt) and social/group terms (mates, grog, evite, addressing, motioned) with no clear arc signal. KeyBERT adds 'engaged', 'attracted', 'overheard', 'emotions', 'causing' — suggestive of some interpersonal dynamic but not pinpointing a specific arc stage (no clear conflict, repair, disclosure, or commitment cue). POS rep echoes 'engaged', 'embarrassed', 'emotions', 'amusement', 'reminder' — mild social awkwardness but insufficient to anchor a specific arc role. MMR adds 'overheard', 'chased', 'praying', 'amusement', 'causing' — again evocative but ambiguous across multiple possible arcs (misunderstanding, escalation, or simply external social scene). No single arc stage is clearly dominant across all four reps; the cluster reads as a social gathering scene with emotional undercurrents that cannot be reliably coded beyond unclear arc role.
- **B contextual:** `ARC_10`
  - Topic 314 appears to be a character-name topic — sentences are almost entirely name invocations or very short address fragments (Brant, Blake, Phoenix) with no surrounding narrative context that reveals a relationship dynamic, conflict, repair, or arc event. The sentences are drawn from multiple books with different named characters, confirming this is a BERTopic cluster anchored on proper-name tokens rather than any coherent narrative-arc function. No sentence provides enough context to identify a main-couple interaction or assign a meaningful arc code. All sentences are coded ARC_10 (unclear arc role). Main-couple probability is very low (0.10) because the fragments are name-only utterances with no relational content visible.
- **C adjudicate:** `ARC_10`
  - Both lexical consensus and contextual dominant converge on ARC_10 (unclear_arc_role), indicating the topic does not resolve cleanly into a single narrative-arc function. The taxonomy metadata (4.3 Secrets, Misunderstandings & Hidden Information; secondary 3.3 Ambivalence & Internal Conflict) suggests content that could plausibly map to ARC_1 (misunderstanding) or ARC_5 (disclosure), but neither is sufficiently dominant to override the dual-pass ARC_10 verdict without additional evidence. The secondary taxonomy (ambivalence/internal conflict) further muddies the signal — internal conflict is not inherently a main-couple arc beat. No construct bucket is assigned because the topic lacks the directional clarity required for REFINED_FALLING or REFINED_RISING, and there is no indication of external-plot primacy. Manual review is flagged to inspect raw token weights and representative documents, which may allow a future reclassification to ARC_1 or ARC_5 if secrets/misunderstandings between the main couple are confirmed as the dominant signal.
- **Action:** KEEP

---

## Topic 362 — Keeping Someone Watched and Close

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_10 (norm: ARC_10)

> come on, i’ll get you a drink,’ rory said. ‘

> they’ll expect me to keep her close, to make sure she doesn’t discover what we are,” rory answered.

> and goddess willing i’ll be ready for it, thought rory as she ignored his comment to follow amber out to the sitting room.

> *(CELL_B, tertile=begin)* For we have seen how far Kelsey is willing to go for what he wants.”

> *(CELL_B, tertile=begin)* He would go slowly, wisely, even though he was more resolved than ever to see Kelsey repaid for his ills against others.

> *(CELL_B, tertile=begin)* Yet he’d had no time to grieve their loss, for he had immediately become embroiled in this conflict with the Earl of Kelsey.

### Pass A/B/C

- **A lexical:** `ARC_10`
  - Main keywords are dominated by proper nouns (rory, yamane, kingman, darlington, ayida, damballah) and a survival cue ('survived'), offering no clear relational arc signal between a main couple. KeyBERT yields procedural/social interaction words (answering, willing, sir, expect, pretending, embarrassed, introduce, issue, wondering) that suggest a scene of social navigation or awkward introduction but do not point to a specific arc stage. POS mirrors this with neutral framing terms (addition, meantime, framed, suggestion, issue, features, willing, sir). MMR adds physical/emotional texture (tearing, crouched, struggled, tugged, embarrassed) consistent with tension but not diagnosable as a specific arc beat without clearer relational context. No keyword cluster reliably maps to a defined ARC_1–ARC_9 stage; the aggregate signal is ambiguous.
- **B contextual:** `ARC_10`
  - Topic 362 clusters around the name 'Kelsey' across two very different books. In BOOK_001, Kelsey is an antagonist (Earl of Kelsey) and all sentences describe external conflict/rivalry with no main-couple involvement — coded ARC_9. In BOOK_002, Kelsey appears to be a character whose identity relative to the main couple is unclear from fragments alone; 'Kelsey's heart sank' suggests emotional distress (ARC_4) but context is insufficient to confirm main-couple status. In BOOK_007, Rick and Dorian appear to be a main couple (mates), with one intimate scene (ARC_0 — off-target for arc coding) and concern for Dorian's wellbeing (ARC_4). BOOK_008 sentences are too fragmentary (ARC_10). No single code reaches 70%; ARC_10 is the plurality at ~45%, making it the dominant code, but the topic is heterogeneous across books and character roles. Main-couple probability is low (~0.20) given that most sentences involve an antagonist named Kelsey or unclear characters.
- **C adjudicate:** `ARC_10`
  - Both lexical consensus and contextual dominant converge on ARC_10 (unclear_arc_role). The taxonomy tag 4.3 (Secrets, Misunderstandings & Hidden Information) suggests the topic could plausibly map to ARC_1 (misunderstanding) or ARC_5 (disclosure), but neither signal is strong enough to override the double ARC_10 signal from Passes A and B without additional textual evidence. The secondary taxonomy tag 10.1 (Paranormal & Immortal Beings) raises the possibility that the hidden-information element is tied to a supernatural identity reveal, which could be external-plot-adjacent (ARC_9) rather than a pure interpersonal misunderstanding — further blurring the picture. Because the topic sits at the intersection of at least three plausible arc roles (ARC_1, ARC_5, ARC_9) without a dominant signal, ARC_10 is the most defensible single code. No construct bucket is assigned because the ambiguity prevents reliable placement in REFINED_FALLING, REFINED_RISING, or EXTERNAL_PLOT_CONFLICT. Manual review is required to inspect representative documents and determine whether a more specific arc role can be assigned.
- **Action:** KEEP

---

## Topic 319 — Confessing A Costly Mistake

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_1 (norm: ARC_1)

> but you have a way of letting me know when you think i’ve made the wrong one.” “

> i’ve made many mistakes and maybe i should have come back a year ago.

> it was a mistake for which i’ve paid dearly.” “

> *(CELL_D, tertile=middle)* They’re fundamental y flawed, I can’t—” “ ‘Flawed’ being the key word,” Josh points out.

### Pass A/B/C

- **A lexical:** `ARC_1`
  - Main keywords ('mistake', 'mistakes', 'flaw', 'error', 'errors', 'biggest', 'terrible', 'made') strongly signal a misunderstanding or misjudgment frame — the vocabulary of recognizing a wrong belief or wrong action that drove a rift, which is the lexical signature of ARC_1 (misunderstanding). KeyBERT ('occurred', 'thinks') and POS ('latest', 'bigger') are too sparse and neutral to anchor any specific arc role, yielding ARC_10. MMR adds 'proved', 'shifting', 'paid', 'surely', 'pressing' alongside 'occurred'/'bigger'/'thinks' — these hint at consequence and acknowledgment but still lack directional arc cues, so ARC_10 is the safest call there. The Main list dominates in volume and specificity; 'mistake/error/flaw' as a cluster is the canonical lexical marker for a misunderstanding-driven conflict beat, so ARC_1 carries the consensus despite disagreement from the sparser reps.
- **B contextual:** `ARC_1`
  - Topic 319 clusters around language of mistakes, wrongness, accidents, and being flawed — all hallmarks of misunderstanding or misjudgment rather than escalating conflict or external plot. The majority of sentences (12/20) express that something was wrong, mistaken, or accidental, fitting ARC_1 (misunderstanding). A minority show interpersonal friction/disagreement (ARC_2) or acknowledgment/repair language (ARC_6). One sentence ('I feel so cheated') suggests relational distress (ARC_4). Crucially, none of the sentences clearly identify a main romantic couple; speakers and addressees are unnamed or ambiguous, so main_couple_prob is low (~0.25). ARC_1 exceeds 70% threshold when combining direct mistake/wrong language, making it the dominant code.
- **C adjudicate:** `ARC_1`
  - Both lexical consensus and contextual dominant converge on ARC_1 (misunderstanding). Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) directly corroborates this classification, with 3.2 (Negative Emotions & Distress) as a secondary signal consistent with the emotional fallout of a misunderstanding rather than an independent arc role. The topic concerns the main couple and represents a falling-arc dynamic (trust/understanding deteriorating due to hidden information), placing it in the REFINED_FALLING construct bucket. No conflict between passes or taxonomy signals; KEEP is appropriate with no manual review needed.
- **Action:** KEEP

---

## Topic 232 — Conversation Cut Short By Arrival

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** ARC_10 (norm: ARC_10)

> dex had come in and gabe's conversation with her, the longest conversation that they'd had in the couple of weeks he'd been back, was over.

> gabe leaned down so he wouldn’t be overheard. “

> i'll tell you right now falan and gabe are the only people on my team that i'd stake my career— or my balls —on."

> *(CELL_C, tertile=end)* Have Remy or the boys been out to question you again or give you more information about Joshua’s attack?”

> *(CELL_A, tertile=end)* He almost told her to call him Gabe, but he knew his name would sound way too good coming from her full lips.

> *(CELL_A, tertile=end)* Her name fit her, Gabe had found himself thinking one too many times.

> *(CELL_A, tertile=begin)* Gabe pretended to tackle Zach as he pulled the microphone from his hand, but he instantly sobered as he turned to Chase and Chloe. “

> *(CELL_A, tertile=end)* Her face got red then and she said angrily, "So, Gabe knew and didn't clue me in?

### Pass A/B/C

- **A lexical:** `ARC_10`
  - The keyword sets present a tense, emotionally charged conversation between named characters (gabe, nick, elwoods) with cues of physical tension (trembling, squeezed, cringed, groaned, pained, stroking) and emotional complexity (longing, instincts, awareness, distracted, impatiently, overheard). However, the signals are mixed: 'longing' and 'stroking' suggest intimacy or desire, while 'cringed,' 'impatiently,' 'problems,' and 'overheard' suggest friction or discomfort. There is insufficient evidence to pin this to a specific arc function—it could be a tense romantic conversation (ARC_2), a moment of withheld information (ARC_1), or simply an emotionally loaded scene without clear arc movement. The ambiguity across all four representations warrants ARC_10.
- **B contextual:** `ARC_10`
  - Topic 232 consists entirely of truncated dialogue attribution fragments centered on the name 'Gabe' (e.g., 'Gabe said.', 'Gabe murmured.', 'Gabe blinked.'). These are speech-tag sentence stubs with no recoverable semantic content about the romantic relationship or any arc function. The topic appears to be a BERTopic artifact capturing a character-name dialogue-attribution pattern rather than a meaningful narrative theme. No relationship state change can be inferred, no arc role can be assigned, and main-couple involvement cannot be confirmed. All sentences are coded ARC_10 (ambiguous) across all tertiles. The topic should be excluded from H6 arc analysis.
- **C adjudicate:** `ARC_10`
  - All metadata signals converge on ARC_10. Taxonomy 4.2 (Ongoing Courtship & Everyday Relational Bonding) describes routine relational interaction without a clear directional arc function. Radway R3 (hero responds ambiguously to heroine) is definitionally ambiguous — it neither advances nor retreats the relationship in a codeable direction. Radway R7 and R2 as secondary/plausible codes add mild reassurance and recognition flavors but do not tip the balance toward ARC_7 (restored trust) or ARC_5 (disclosure), as no trust rupture or revelation is implied. Stage11 prior code RAX_emotional_reassurance could suggest ARC_7, but ARC_7 requires evidence of trust being restored after damage; everyday tenderness or ambiguous warmth does not meet that threshold per the critical rules. Lexical and contextual consensus both land on ARC_10. No directional arc function is reliably attributable, so the topic is excluded from H6 strict inclusion buckets.
- **Action:** KEEP

---

## Topic 293 — Admitting Jealousy Out Loud

- **Taxonomy:** 4.7 — Jealousy & Possessive Romance Conflict
- **Code:** ARC_4 (norm: ARC_4)
- **Evidence:** exhaustive packet

> the concept of jealousy is foreign to them.

> but this jealousy of yours is gonna ruin what you’ve got with j.d.” “i know.” “

> we’ve been around the markets and —’ as she enthused away, i couldn’t help but feel jealous.

> should i be jealous of this cayden?”

> *(CELL_B, tertile=middle)* I've always maintained that a little bit of jealousy looks good on a man. "

> *(CELL_B, tertile=end)* Well, of course I'm jealous," I frowned, poking him in the chest. "

> *(CELL_B, tertile=end)* She was also extremely irate over the fact that her boyfriend was using me to make her jealous—without my permission, as I've told you a couple of times.

> *(CELL_B, tertile=end)* I'm flattered that you're jealous, but you should know by now that no other woman could begin to compare with you.

> *(CELL_B, tertile=end)* This is not arrogance talking, this is not jealousy, it is simply a matter of facts."

> *(CELL_B, tertile=middle)* I debated staying where I was, standing firm for ethical reasons, but the thought that she'd be in the closed, womb-like confines of the trailer alone with Raphael was enough to spike my jealousy count off the chart.

> *(CELL_B, tertile=begin)* Not to mention you repeatedly batted your eyelashes at me in an obvious attempt to make him jealous.

> *(CELL_B, tertile=middle)* I didn't mind a little bit of a possessive attitude, but he was taking things a bit too far. "

> *(CELL_B, tertile=begin)* I bet you're one of those men who likes to feel superior to women," Roxy said suspiciously.

### Pass A/B/C

- **A lexical:** `ARC_4`
  - All four keyword lists converge on relationship-caused emotional distress. Main keywords ('jealous', 'jealousy', 'jealously', 'irrational', 'twinge', 'pang') directly name the internal emotional pain triggered by the romantic relationship. KeyBERT adds 'attracted', 'upset', 'emotional', 'concerned', 'warned', 'assured', pointing to relational anxiety and distress rather than a rupture or conflict escalation. POS keywords ('ex', 'wound', 'upset', 'reaction', 'emotional') reinforce that a past relationship or rival is causing the protagonist relational pain. MMR keywords ('stirred', 'emotional', 'wound', 'upset', 'warned') similarly describe an emotionally stirred, distressed state. The jealousy is framed as irrational/internal (not an overt fight or breakup threat), placing this squarely in ARC_4 (relationship-caused distress) rather than ARC_2 (conflict escalates) or ARC_3 (separation threat).
- **B contextual:** `ARC_4`
- **C adjudicate:** `ARC_4`
  - All convergent signals align with ARC_4. Taxonomy 4.7 (Jealousy & Possessive Romance Conflict) and secondary 4.4 (Conflict, Distance & Breakup Threats) both sit squarely within the falling arc cluster. Radway R2 (heroine reacts antagonistically to hero) is a canonical ARC_4 marker — the distress originates from within the romantic relationship itself, not from an external threat. R5 and R7 are plausible secondary colorings but do not displace the primary ARC_4 reading; R7 in particular would require evidence of trust restoration, which jealousy/possessive conflict does not supply. Stage11 prior codes RAX_emotional_security and RAX_possessive_claiming reinforce relationship-internal tension rather than external plot conflict. Lexical and contextual consensus both independently arrived at ARC_4. No contradictions exist across any metadata layer. Assign to REFINED_FALLING for H6 hypothesis testing.
- **Action:** KEEP

---

## Topic 3 — Demanding An Explanation

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** ARC_5 (norm: ARC_5)

> and you have no idea what we’ve seen, what we’ve done— you’ve been in your cosy little world and you just have no—damned— clue! ’

> sophia, i’ve something to tell you.” “

> i’ve told them that already.’ ‘

> *(CELL_B, tertile=middle)* I’ll tell you whatever you want to know.”

> *(CELL_B, tertile=middle)* Well, you know what I mean.” “

> *(CELL_D, tertile=end)* No—no, I don’t admit that.’

### Pass A/B/C

- **A lexical:** `ARC_5`
  - All four keyword lists converge on disclosure/revelation dynamics. Main keywords ('know, tell, don, understand, ask, explain, say, wrong, mean') signal a scene structured around communicating or withholding information and seeking clarification. KeyBERT keywords ('admit, reveal, realise, assure, speaking') are direct disclosure-act verbs — 'admit' and 'reveal' are canonical ARC_5 markers. POS and MMR keywords ('explanation, answers, results, difference, remark, extent, percent') point to a scene where facts or truths are being laid out or demanded, consistent with a disclosure moment. The presence of 'commander, sir, mister' suggests a formal or authority-inflected context for the disclosure, but the dominant arc function across all reps is the surfacing of hidden or unclear information to one or both parties — ARC_5 disclosure.
- **B contextual:** `ARC_5`
  - All sentences in this topic cluster around the act of demanding, withholding, or offering information — 'Tell me,' 'I demanded to know,' 'I'll tell you whatever you want to know,' 'I'm just not supposed to tell you,' etc. This is a strong disclosure/revelation pattern (ARC_5). The sentences are highly decontextualized fragments with no clear identification of who the speakers are or whether they constitute a main couple; 'unclear' is assigned throughout. The topic does not show escalating conflict, repair, or commitment — it is specifically about the act of disclosure or the resistance to it. ARC_5 accounts for 100% of sentences, well above the 70% threshold, making it the dominant code. Main couple probability is low-to-moderate (0.35) because the fragments could involve any dyad, including secondary characters or non-romantic pairs.
- **C adjudicate:** `ARC_5`
  - Both lexical consensus and contextual dominant independently converge on ARC_5 (disclosure). Although the taxonomy tag is 4.4 Conflict, Distance & Breakup Threats, disclosure events frequently appear within that zone of the narrative arc — a character revealing a secret or truth is a classic falling-arc beat that precipitates conflict or distance. The taxonomy label describes the broader thematic cluster, not the specific arc mechanism; the mechanism here is disclosure. No free-form labels were carried over from Pass A/B that require remapping. Main-couple filter passes. Construct bucket is REFINED_FALLING because disclosure at this position typically drives the couple apart before repair begins.
- **Action:** KEEP

---

## Topic 194 — Promising to Keep A Secret

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** ARC_5 (norm: ARC_5)

> i’ll keep it a secret,” said lucas.

> i’ll be your dirty little secret,” i joked.

> i’ll leave that secret for him to reveal.

> *(CELL_C, tertile=middle)* Perhaps secret information that he has uncovered, information that would be dangerous to the French.’ ‘

> *(CELL_C, tertile=begin)* For reasons I cannot disclose I would rather you did not mention the break-in to anyone.

### Pass A/B/C

- **A lexical:** `ARC_5`
  - All four keyword lists converge on disclosure dynamics. Main is dominated by secret/secrets/keep/keeping/kept/reveal/secrecy — the core lexicon of hidden information being held or released. KeyBERT reinforces with reveal/revealing/hiding/confessed/identity, pointing to an active moment of disclosure or near-disclosure. POS adds identity/embarrassing/curiosity/ability/pressure, consistent with a character revealing a personal truth (identity, ability) under social or emotional pressure. MMR echoes with guarded/reveal/confessed/hiding/discovered/bury, all signalling information that was concealed and is now surfacing. The cluster is squarely about the act of revealing a kept secret — the defining feature of ARC_5 (disclosure) — rather than the conflict that follows (ARC_2) or the repair that results (ARC_6). No cues strongly indicate external plot threat (ARC_9) or misunderstanding (ARC_1) as the primary frame.
- **B contextual:** `ARC_5`
  - Topic 194 is overwhelmingly about secrets, secrecy, and the act of keeping or revealing hidden information — the defining features of ARC_5 (disclosure). The vast majority of sentences (17/20) directly reference secrets, secret-keeping, or the threat/promise of disclosure. A meaningful subset (BOOK_006 sentences) clearly involves the main couple, where one or both partners are concealing truths from each other, which is a classic disclosure-tension dynamic. Two sentences (BOOK_005_2, BOOK_005_3) reference dangerous political/external secrets with no romantic-couple framing, coded ARC_9. Main-couple probability is moderate (~0.45) because while BOOK_006 strongly anchors the couple context, many other sentences are ambiguous or clearly non-couple. ARC_5 exceeds 70% threshold, making it the dominant code.
- **C adjudicate:** `ARC_5`
  - Both lexical consensus and contextual dominant converge on ARC_5 (disclosure). Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) directly supports a disclosure event — a character reveals or is confronted with concealed information, which is the canonical ARC_5 trigger. The secondary taxonomy 9.2 (Promise, Vow & Future-Tense Speech Acts) suggests a commitment or pledge may accompany or frame the disclosure, but it does not displace the primary arc role; it is a supporting speech-act layer. Because disclosure typically destabilizes the relationship before repair can occur, this sits in the REFINED_FALLING construct bucket. No conflict between passes; no free-form labels to remap. Main-couple filter passes — the disclosure pertains to the central romantic dyad. No manual review needed.
- **Action:** KEEP

---

## Topic 242 — Trading Forgiveness For Old Wrongs

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** ARC_6 (norm: ARC_6)

> not if you’ll forgive him.” “

> he’ll never forgive you.

> okay, how’s this — i’ll forgive you for summer if you forgive me for kabir.” “

> *(CELL_B, tertile=begin)* Any man delivering such a speech to the lady he had planned to marry—a lady who had waited faithfully for him—should have had the grace to appear remorseful, or at least apologetic.

### Pass A/B/C

- **A lexical:** `ARC_6`
  - All four keyword lists converge on apology and forgiveness as the dominant signals. Main contains 'forgive,' 'forgiveness,' 'forgiven,' 'forgiving,' and the pleading 'please, can, hope' — classic repair-seeking language. KeyBERT reinforces this with 'apology,' 'fault,' 'willing,' and 'harshly/terribly/hurts' (acknowledging harm done). POS adds 'apology,' 'treatment,' 'actions,' and 'emotions,' pointing to a reckoning with past behavior. MMR echoes 'apology,' 'fault,' 'harshly,' 'treatment,' and 'spite,' all consistent with one party acknowledging wrongdoing and seeking reconciliation. There is no evidence of trust being fully restored (which would push toward ARC_7) or of mutual commitment/resolution (ARC_8); the focus is squarely on the act of seeking and granting forgiveness, which is the defining feature of ARC_6.
- **B contextual:** `ARC_6`
- **C adjudicate:** `ARC_6`
  - All converging signals point to ARC_6. The lexical and contextual consensus is reconciliation/repair. Taxonomy 4.5 (Reconciliation, Commitments & HEA) with secondary 4.3 (Secrets/Misunderstandings) is fully consistent: the couple is moving through the repair of a misunderstanding or prior hurt toward restored closeness. Radway R10 (heroine reinterprets hero's behaviour as result of previous hurt) is the canonical reconciliation beat — the heroine's revised understanding of the hero's past pain is the mechanism that enables forgiveness and repair, which is the core of ARC_6. R11 and R9 as secondary/plausible Radway codes reinforce the repair-and-reassurance dynamic without pushing toward ARC_7 (which would require trust already restored) or ARC_8 (which would require final mutual commitment). Stage11 labels RAX_emotional_reassurance, RAX_emotional_security, and RAX_tenderness_core describe the affective texture of reconciliation scenes, not yet the stable post-repair state of ARC_7. The slight ARC_7 adjacency (tenderness, reassurance) does not override the dominant repair/reinterpretation function. No contradiction exists across any metadata layer. Strict H6 inclusion as 'rising' is appropriate: ARC_6 sits squarely in the rising arc band (ARC_5–8) and represents a positive relational trajectory event.
- **Action:** KEEP

---

## Topic 85 — Offering and Refusing An Apology

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** ARC_6 (norm: ARC_6)

> he said he wanted to apologize.

> i need to apologize to you, ruby.

> oh, i'm so not gonna apologize for that."

> *(CELL_D, tertile=end)* He tried to get back in my good graces with a box of chocolates a couple of days later, but he never did apologize.” “

> *(CELL_D, tertile=begin)* And you made it quite clear that you thought I was overreacting to the situation.”

> *(CELL_D, tertile=end)* Between Cornelia, Emily Taylor and Helen Washburn, I’ve been apologized to every day this week.”

### Pass A/B/C

- **A lexical:** `ARC_6`
  - All four keyword lists converge on repair behavior between the main couple. Main is saturated with apology-act vocabulary ('sorry', 'apologize', 'apology', 'apologizing', 'apologized', 'owe', 'apologise'), which is the canonical lexical signature of ARC_6 (repair). KeyBERT reinforces this with 'apology', 'apologize', 'forgive', 'fault', and 'embarrassed', indicating acknowledgment of wrongdoing and a bid for reconciliation. POS adds 'apology', 'behalf', 'distress', and 'circumstances', consistent with a formal or emotionally charged repair scene. MMR echoes 'apology', 'forgive', 'behalf', 'distress', and 'circumstances', with 'overheard' and 'snorted' suggesting interpersonal tension being addressed rather than escalating. The presence of 'forgive' across KeyBERT and MMR confirms the repair frame rather than mere escalation or disclosure. No cues point to final restored trust (ARC_7) or commitment payoff (ARC_8); the focus is on the act of apologizing itself, placing this squarely in ARC_6.
- **B contextual:** `ARC_6`
  - Topic 85 is overwhelmingly characterized by apology and sorry expressions ('I'm sorry', 'I am sorry', 'Did you just apologize?', 'No harm was done'). These are canonical repair gestures following conflict, mapping clearly to ARC_6 (repair). One sentence (BOOK_001_4) references a prior accusation of overreacting, suggesting a misunderstanding context (ARC_1), and two 'Excuse me?' fragments are too ambiguous to code beyond ARC_10. BOOK_001_5 references multiple third-party apologies, suggesting non-main-couple interaction (coded ARC_6 but main_couple=no). BOOK_002 sentences cluster around a clear dyadic apology exchange likely involving the main couple. Overall ARC_6 exceeds 70%, making it the dominant code. Main couple probability is moderate (~0.55) because several sentences are ambiguous or clearly involve secondary characters.
- **C adjudicate:** `ARC_6`
  - Both lexical consensus and contextual dominant converge on ARC_6 (repair). The primary taxonomy tag 4.4 (Conflict, Distance & Breakup Threats) might suggest a falling-arc code such as ARC_2 or ARC_3, but the secondary tag 4.5 (Reconciliation, Commitments & HEA) and the consistent Pass A/B signal indicate the topic captures the turn toward repair rather than the conflict itself. ARC_6 sits in the REFINED_RISING construct bucket: the couple is actively moving from rupture back toward connection. No free-form labels require remapping. No split is warranted because the dominant signal is repair-initiation, with the conflict/distance framing serving as contextual backdrop rather than the topic's core content. Main-couple filter confirmed positive.
- **Action:** KEEP

---

## Topic 126 — Fingertips Stroking Her Cheek

- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Code:** ARC_7 (norm: ARC_7)

> she lifted her chin. “

> he lifted a hand and stroked a finger down her cheek. ‘

> she lifted her hand and caressed his cheek. "

> *(CELL_B, tertile=begin)* He reached out now, stroked his fingers down her cheek to tip her face to his.

> *(CELL_B, tertile=end)* He caught her back to him, spreading his fingers over her uninjured cheek. “

> *(CELL_A, tertile=middle)* His long fingers cradled her cheeks as he gave her a questioning stare. “

> *(CELL_A, tertile=middle)* His face lowered over hers, and his fingertips settled on her jaw, gently adjusting the angle of her head.

> *(CELL_A, tertile=middle)* His fingers slid over the hot surface of her cheek, and he gently pressed her head to his shoulder. “

> *(CELL_A, tertile=middle)* He bent his head, nuzzling his jaw against the pale silk of her palm. “

> *(CELL_A, tertile=end)* His mouth touched her burning forehead and followed the wing of her brow. “

### Pass A/B/C

- **A lexical:** `ARC_7`
  - Main, KeyBERT, and MMR are dominated by intimate tactile gestures directed at the face and body (cheek, chin, lifted, cupped, stroked, caressed, thumb, touched, cradled, swiped) that collectively signal tender physical closeness consistent with trust being restored or reinforced between the couple — qualifying as ARC_7 (restored trust/reassurance). POS introduces 'annoyance' and 'instructions' alongside neutral spatial/body terms, injecting ambiguity about the emotional valence of the scene, hence ARC_10 for that representation. The three-to-one majority of intimate-touch cues pointing to reassuring physical connection drives the consensus to ARC_7.
- **B contextual:** `ARC_7`
- **C adjudicate:** `ARC_7`
  - All converging signals align on ARC_7. Taxonomy 2.2 (Kissing & Non-Explicit Affection) and 1.7 (Facial Expression & Non-Verbal Cues) describe the physical/expressive register through which trust and closeness are being restored — not merely expressed for the first time. Radway R8 (hero treats heroine tenderly) and R9 together indicate a relational repair or deepening dynamic rather than a neutral affective moment, and R12 further supports a reassurance/comfort function. Stage11 codes RAX_nonexplicit_affection and RAX_tenderness_core are consistent with the ARC_7 criterion: tenderness here is instrumentally tied to restoring or strengthening closeness, not simply decorative warmth. The critical-rule threshold for ARC_7 is met because the Radway and Stage11 labels collectively point to a moment where the hero's tender behavior functions to re-establish or consolidate relational trust, not merely to express affection in a stable context. No contradiction exists between lexical consensus, contextual dominant, taxonomy, Radway, and Stage11 — all support REFINED_RISING / ARC_7. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 167 — Planning A Wedding Reception

- **Taxonomy:** 5.3a — Romantic Social Rituals & Public Couple Recognition
- **Code:** ARC_8 (norm: ARC_8)
- **Evidence:** exhaustive packet

> it’s my dream job, but instead of shooting brides, i’ll be shooting naked women.

> we'll get married next summer in the church in maine that my mother would take me to every sunday.

> the ‘ceremony’ in boorowa might just be signing a few papers, but carley’s planned a wedding reception they’ll never forget.” “

> on the eve of your wedding.”

> *(CELL_A, tertile=middle)* There’ll be plenty to talk about, anyway, after the wedding today .” “

> *(CELL_A, tertile=middle)* If the bride and groom would join hands and face each other, we’ll proceed in joining you together in holy matrimony .”

> *(CELL_A, tertile=middle)* And a girl shouldn’t be so rushed and put on the spot on her wedding day.

> *(CELL_A, tertile=middle)* Just because it was her wedding day didn’t mean she should start thinking about sexy things like her wedding night .

> *(CELL_A, tertile=middle)* Strange to get married and not even know who was on the guest list .

### Pass A/B/C

- **A lexical:** `ARC_8`
  - All four keyword lists converge on wedding/marriage ceremony vocabulary: 'wedding, bride, groom, bridal, ceremony, bridesmaids' (Main) signal a formal marriage event; 'planned, invitation, reception, arrange, preparing, planning, official, announced, destination' (KeyBERT/POS/MMR) describe the organized, official nature of the commitment ritual. The presence of 'jitters' (Main) and 'our' suggests the couple's own wedding rather than an external event. Together these cues indicate mutual relational commitment and final resolution — the defining criterion for ARC_8 — rather than merely love or promises in isolation.
- **B contextual:** `ARC_8`
- **C adjudicate:** `ARC_8`
  - All evidence streams converge on ARC_8. Lexical and contextual consensus both code this as mutual commitment/final resolution. The taxonomy label (5.3a Romantic Social Rituals & Public Couple Recognition) directly maps to the public enactment of relational resolution — a hallmark of ARC_8's requirement for mutual commitment rather than mere love or affection. The secondary taxonomy (5.1 Family, Kinship & Parenthood) reinforces a forward-looking, socially embedded union. Radway R11 (hero declares love and demonstrates commitment) is the canonical ARC_8 signal, and R13 (secondary) further supports a finalizing relational gesture. Stage11 prior code RAX_public_union is fully consistent with ARC_8's mutual resolution criterion. No contradictions exist across any metadata dimension. ARC_8 is confirmed without ambiguity; no split or reinterpretation is warranted. Recommended for inclusion in the rising arc bucket for H6 hypothesis testing.
- **Action:** KEEP

---

## Topic 78 — Swearing War Before He Takes Her

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** ARC_9 (norm: ARC_9)

> i’ll fight you off.” “

> and if they do, you’ll fight them.

> i’ll start a war before i let him have you,” he murmured.

> *(CELL_D, tertile=middle)* Well, if the other man thought he was about to give him a fight over Sabina, he was wrong; Sabina was an independent woman of twenty-five, not a possession for two men to fight over as if she were the prize! ‘

> *(CELL_A, tertile=begin)* I don’t want to fight, but you’ve left me with no other choice.”

### Pass A/B/C

- **A lexical:** `ARC_9`
  - All four keyword lists are dominated by external conflict/combat vocabulary: 'fight, fighting, war, battle, fought, battles, fighter, win' (Main); 'attacked, weapons, guarded, warned' (KeyBERT); 'weapons, century, president' (POS); 'attacked, erupted, weapons, terms' (MMR). There is no lexical signal implicating the main romantic relationship — no relational repair, disclosure, commitment, misunderstanding, or couple-specific distress. The topic describes an external plot conflict (warfare/combat) that does not itself deteriorate or advance the romantic arc, satisfying ARC_9.
- **B contextual:** `ARC_9`
- **C adjudicate:** `ARC_9`
  - All signals converge on ARC_9. Lexical and contextual consensus both code this as external plot conflict. Taxonomy 7.2 (Violence, Threats & Non-Sexual Coercion) is a canonical external-danger category that does not inherently implicate romantic-relationship deterioration. The Radway R11 label ('Hero declares love and demonstrates commitment') and Stage11 codes (RAX_external_protection, RAX_relational_darkness) might superficially suggest rising-arc content, but under the critical rules these do not qualify as ARC_7 or ARC_8 without evidence of trust restoration or mutual relational resolution — the commitment here is expressed in the context of protecting against external threat, not repairing the relationship. RAX_relational_darkness is consistent with ARC_9 (external danger casting shadow) rather than ARC_2–4 (internally generated conflict). R6 as a secondary Radway code is plausible but insufficient to override the dominant external-threat framing. The Radway/Stage11 labels therefore support rather than contradict the contextual ARC_9 judgment. No split or reinterpretation is warranted; the topic cleanly belongs in EXTERNAL_PLOT_CONFLICT and should be included in H6 analyses as an external arc element.
- **Action:** KEEP

---
