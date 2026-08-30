# H4 protection / possession — close-reading pack

## Topic 293 — Admitting Jealousy Out Loud

- **Taxonomy:** 4.7 — Jealousy & Possessive Romance Conflict
- **Code:** H4_8 (norm: H4_8)
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

- **A lexical:** `H4_8`
  - All four keyword lists converge on jealous/possessive emotional experience. Main is dominated by 'jealous', 'jealousy', 'jealously', 'irrational', 'twinge', 'pang' — classic internal jealousy vocabulary with no external threat actor. KeyBERT adds 'attracted', 'upset', 'emotional', 'concerned', 'warned', 'assured' — emotional arousal and interpersonal tension consistent with jealous reaction, not protective action against an outside threat. POS includes 'ex', 'wound', 'upset', 'reaction', 'foreign', 'advantage' — 'ex' and 'wound' reinforce romantic jealousy triggered by a rival or past relationship, not an external danger. MMR adds 'stirred', 'warned', 'approached', 'wound', 'upset', 'playfully', 'inched' — physical/emotional stirring consistent with jealous arousal. No cues indicate coercive restriction of partner autonomy (ruling out H4_9–H4_11), no external physical/social threat (ruling out H4_5/H4_6), and no mutual care framing. The pattern is squarely jealous possessiveness as an internal emotional state.
- **B contextual:** `H4_8`
  - The overwhelming majority of sentences explicitly name or describe jealousy as an emotional state experienced by or attributed to characters in romantic contexts — classic jealous possessiveness (H4_8). Several sentences frame jealousy as flattering or normative ('a little bit of jealousy looks good on a man'; 'I'm flattered that you're jealous'), and one references 'Dark Ones' being notoriously jealous about soul mates, all consistent with H4_8 (jealous possessiveness as a romantic trope). BOOK_001_10 references a 'possessive attitude going too far,' still best coded H4_8 as it describes jealous/possessive behavior without clear coercive control mechanics. BOOK_001_12 ('likes to feel superior to women') is ambiguous — possibly H4_9/H4_11 territory but lacks enough context, coded H4_13. BOOK_003_1 ('husband shaming me') implies the partner as a source of harm, coded H4_10. No external threat is present; the jealousy is directed at rivals or attributed to partners, confirming threat_source as unclear (rival-based rather than external danger). Claiming language is present throughout (soul mates, possessive attitudes, jealousy over partners).
- **C adjudicate:** `H4_8`
  - Both lexical consensus and contextual dominant converge on H4_8 (jealous_possessiveness), and the taxonomy classification (4.7 Jealousy & Possessive Romance Conflict) is fully consistent with this code. No external threat is evidenced that would warrant H4_5 or H4_6; the tension is partner-directed and rooted in jealousy rather than coercive restriction (H4_9) or paternalistic control (H4_11). The secondary taxonomy tag (4.4 Conflict, Distance & Breakup Threats) reflects relational fallout from jealousy rather than a distinct care/control dynamic, so no split or retaxonomization is needed. H4_8 is retained as the single care_protection_code.
- **Action:** KEEP

---

## Topic 315 — Claiming Her As His Own

- **Taxonomy:** 4.7 — Jealousy & Possessive Romance Conflict
- **Code:** H4_8 (norm: H4_8)
- **Evidence:** exhaustive packet

> henri, should any ask, this woman belongs to my cousin tristan—and to me.”

> everything he was warmed in tristan’s presence, and short of sounding like one of those cards that sang when opened, [person] didn’t know where to begin telling sey how much tristan seemed to fit into him—and around him.

> i'll call tristan right after i get off the phone." "

> besides, i suspect that even if i were cruel enough to hand tristan over, it would gain me little except a lifetime of slavery to george.

> *(CELL_B, tertile=end)* Val’s words slapped at him, forced him to realize a few things he’d rather have ignored.

> *(CELL_B, tertile=begin)* Val was your shot at actually having a real life and you let her waltz right out the door.”

> *(CELL_B, tertile=end)* Val looked at him as if he was out of his mind and that’s exactly how Dev felt. “

> *(CELL_B, tertile=begin)* Val wondered, just a little embarrassed to think that might be true.

> *(CELL_B, tertile=begin)* Devlin Hudson didn’t know it, but Val had already won the first battle for his heart.

> *(CELL_B, tertile=end)* It was as if even knowing that his parents had made up their differences, Dev was still determined to keep himself locked behind the walls Val had almost given up on smashing.

> *(CELL_B, tertile=middle)* His blood boiled as he looked at the computer-generated image of him and Val facing away from each other.

### Pass A/B/C

- **A lexical:** `H4_13`
  - Main keywords are almost entirely character names with 'comfortable' and 'persuaded', offering no clear care/protection signal — coded off_target. KeyBERT, POS, and MMR share a cluster of ambiguous behavioral cues: 'hesitation', 'nudged', 'screaming', 'behavior', 'actions', 'sentence', 'indication', 'ends', 'ribs', 'bothered', 'grumbled', 'studying', 'sounding'. 'Nudged' and 'hesitation' could indicate gentle persuasion or mild pressure; 'ribs' and 'screaming' hint at physical intensity; 'belongs' in MMR edges toward possessive claiming (H4_7), but without corroborating context it is insufficient to confirm. No clear external threat rules out H4_5/H4_6; no unambiguous coercive pattern rules in H4_9. The mix of pressure-adjacent and neutral behavioral vocabulary across three reps yields H4_13 (mixed/unclear) as the most defensible consensus.
- **B contextual:** `H4_0`
  - The overwhelming majority of sentences are character-name references, dialogue fragments, or relational-conflict snippets with no discernible care/protection/control content — coded H4_0 (off-target). BOOK_003_14 ('one of the main reasons Dev had wanted Val to come back to him') hints at possessive claiming (H4_7) but is too brief to confirm coercive intent. BOOK_003_12 ('blood boiled … image of him and Val facing away') suggests jealous/possessive emotional reaction (H4_8). No external threat is present; no systematic restriction or coercion is evidenced. H4_0 dominates at ~90%, well above the 70% threshold.
- **C adjudicate:** `H4_8`
  - Pass A/B yielded a lexical consensus of H4_13 (mixed/unclear) and a contextual dominant of H4_0 (off-target), but the revealed taxonomy — 4.7 Jealousy & Possessive Romance Conflict with a secondary of 5.2 Friends, Allies & Social Circles — provides decisive disambiguation. The topic's core signal is jealousy and possessive conflict directed at the partner within a social-circle context (e.g., rivalry over friends or allies), not an external threat and not mere ambiguity. No external threat actor is evidenced, so H4_5/H4_6 are excluded. The social-circle secondary axis indicates the jealousy is triggered by the partner's relationships with others, which is the defining feature of H4_8 (jealous_possessiveness) rather than outright coercive control (H4_9) or a for-your-own-good framing (H4_11). H4_0 is overridden because the taxonomy confirms the topic is on-target for the jealousy/possessiveness construct family. The prior H4_13 is resolved to H4_8 as the single dominant code.
- **Action:** REINTERPRET

---

## Topic 36 — Eagerly Offering to Help

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_2 (norm: H4_2)

> of course, i’ll help you.’

> then you’ll let me help,” frances said at once, her expression eager. “

> sure, of course, i’ll help.”

> *(CELL_B, tertile=end)* And you know I’m here to help you in any way I can.”

> *(CELL_D, tertile=middle)* Well make yourself useful,” he said. “

> *(CELL_B, tertile=end)* I’ve got to do something to help.”

### Pass A/B/C

- **A lexical:** `H4_2`
  - Main keywords ('help', 'need', 'helping', 'assistance', 'helped', 'let') and KeyBERT keywords ('provided', 'willing', 'requested', 'promptly', 'eagerly', 'appreciate') consistently signal practical, task-oriented assistance being offered or received — the hallmark of H4_2 practical_care. MMR reinforces this with 'promptly', 'appreciate', 'eagerly', 'pleased', 'options', and the deferential address 'mister'/'sir', all pointing to a service or help-giving dynamic. POS keywords ('task', 'options', 'success', 'sentence', 'sadness', 'fault', 'unlikely') are more abstract and emotionally mixed, lacking clear romance-novel care framing, which pulls toward H4_0 off_target for that representation alone. No external threat, no partner restriction, and no possessive or coercive cues are present anywhere. The dominant signal across three of four representations is practical assistance, yielding H4_2 as consensus.
- **B contextual:** `H4_2`
  - The overwhelming majority of sentences are simple offers or expressions of willingness to help ('Can I help you?', 'I'll help you.', 'Sure, I'll be glad to help.'). These represent practical, task-oriented assistance with no emotional depth, no external threat, no possessive or controlling language, and no romantic intensity — fitting H4_2 (practical care). One sentence ('Can I ask you a question?') is purely conversational filler with no care content, coded H4_0 (off-target). No claiming language, no jealousy, no coercion, and no identifiable threat source are present.
- **C adjudicate:** `H4_2`
  - All three passes converge on practical care (H4_2): lexical consensus is H4_2, contextual dominant is H4_2, and the prior H3 decomposition coded this topic as S11 (practical_help_other) with a RETAXONOMIZE action. The taxonomy placement in 4.6 Emotional Safety, Reassurance & Caretaking is inconsistent with this convergence — H4_2 belongs in a practical care/help cluster rather than an emotional reassurance cluster. No external threat is evidenced, ruling out H4_5/H4_6; no partner restriction signals are present, ruling out H4_9–H4_11. The emotional-reassurance signal (H4_1/H4_4) that the 4.6 taxonomy label implies is not supported by either Pass A/B coding or the H3 decomposition. RETAXONOMIZE is therefore confirmed, moving the topic out of 4.6 into the practical care cluster. Manual review remains flagged to verify that the underlying token distribution genuinely reflects practical-help content and that no emotional-reassurance signal was systematically underweighted across passes.
- **Action:** RETAXONOMIZE

---

## Topic 46 — Asking Someone to Trust You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> you’ll just have to trust me.”

> he’ll trust you if you promise to keep me in sight.” “

> my trust that he’ll bring me to safety.

> *(CELL_D, tertile=begin)* The critics wanted to prove that setting goals, drawing graphs, measuring results and evaluating the performance of individuals was nothing less than taking the place of trusting the Holy Spirit to give increase.

> *(CELL_D, tertile=begin)* Trust us, all we need to do to you can be done here,” one of the other guys said.

### Pass A/B/C

- **A lexical:** `H4_13`
  - Main keywords (trust, trusted, betrayed, betray, betrayal) center on a breach-of-trust dynamic without specifying whether the betrayer is an external party or the partner, making the threat source ambiguous. KeyBERT terms (instincts, willingly, worries, warned, deserve, admit) suggest internal deliberation and emotional reckoning around trust decisions, but do not resolve the direction of harm. POS and MMR terms (instincts, worries, twisting, hesitation, options, heal) reinforce a sense of psychological conflict and weighing of choices, consistent with processing a betrayal. No clear external threat (ruling out H4_5/H4_6), no explicit partner restriction (ruling out H4_9–H4_11), and no possessive claiming (ruling out H4_7/H4_8). The cluster sits at the intersection of emotional vulnerability and relational rupture without sufficient cues to resolve into a single clean code, warranting H4_13 (mixed/unclear).
- **B contextual:** `H4_1`
  - The overwhelming majority of sentences in this topic revolve around the concept of interpersonal trust — asking whether someone trusts another, affirming trust, or urging trust. These expressions of trust function as reassurance and relational tenderness (H4_1), reflecting emotional openness and vulnerability between characters rather than any external threat, possessive claiming, or coercive dynamic. The off-target sentences (H4_0) include a theological/organizational critique about goal-setting and the Holy Spirit, a vague threatening statement by unnamed 'guys' that lacks romance-novel care/protection framing, a question about being alone in a hotel room (ambiguous but not clearly care-coded), a question about sharing joy with no trusted person (grief/isolation, not care), a simple character descriptor ('trustworthy'), and a self-description of respectability — none of these map to any H4 care/protection code. No claiming language, no external threat, no coercive control is present.
- **C adjudicate:** `H4_1`
  - Pass A/B yielded a lexical consensus of H4_13 (mixed_unclear), but the contextual dominant is H4_1 (reassurance_tenderness), and the taxonomy placement under 4.6 Emotional Safety, Reassurance & Caretaking is unambiguous. The secondary taxonomy signal (4.3 Secrets, Misunderstandings & Hidden Information) explains why lexical signals appeared mixed — hidden information contexts often surface vocabulary that looks like conflict or control, but the functional dynamic here is one character offering emotional reassurance and tenderness to another, consistent with trust-building (S3 from the H3 decomposition). No external threat is evidenced, so H4_5/H4_6 are excluded. No partner restriction or coercion is evidenced, so H4_9–H4_11 are excluded. The H3 construct 'trust' maps cleanly onto H4_1 as the mechanism by which reassurance and tenderness operate in this topic. REINTERPRET from H4_13 to H4_1 is warranted; no split is needed.
- **Action:** REINTERPRET

---

## Topic 56 — Promising Never to Hurt You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> you'll get hurt," he managed to say. "

> you know i’ll never hurt you .”

> i’ll make sure you aren’t hurt.” “

> *(CELL_D, tertile=end)* He says that he knows it must hurt, but that whatever will be, will be, and that nothing we say or do will resolve things.

> *(CELL_D, tertile=middle)* It’s all well and good saying you avoid pain by avoiding relationships, but what about the wonderful things you’re avoiding as well?

### Pass A/B/C

- **A lexical:** `H4_1`
  - Main keywords 'hurt, hurting, harm, mean, never, won't, want' form a classic reassurance register — denials of intent to harm and pledges of non-harm. KeyBERT adds 'assured, protect, cried' alongside 'painful/distress', pointing to emotional comfort and soothing after distress rather than an external threat or partner restriction. POS 'distress, painful, possibility, purpose' reinforce an emotional-processing, reassurance context. MMR 'deserve, intend, causing, assured, protect' continue the pattern of a speaker disclaiming harmful intent and offering comfort. No external threat actor is identifiable, no controlling or possessive language appears, and the overall cluster maps most cleanly to reassurance_tenderness (H4_1): acknowledgment of pain, denial of intent to cause it, and emotional soothing.
- **B contextual:** `MIXED`
  - Topic 56 centres on the theme of hurt — fear of being hurt, reassurances of not hurting, and emotional pain in relationships. No single code reaches 70%. The largest cluster is H4_1 (reassurance/tenderness): pledges such as 'I'd never do anything to hurt you', 'I'll be careful not to hurt him', 'You haven't hurt me' are gentle relational reassurances. H4_4 (emotional support) covers sentences about emotional pain and encouragement (e.g., 'Don't give him the satisfaction'). H4_10 (partner as danger) applies where physical harm from a partner is explicitly feared ('Did you think he'd hit me?', 'Pushed me down the stairs?', 'Are you going to hurt me?'). H4_9 (coercive control) covers emotional blackmail and accusatory manipulation ('You're only doing it to hurt me', 'How can you emotionally blackmail me'). H4_13 (mixed/unclear) is used for ambiguous hurt references without clear directionality. No external threat is present; where threat exists it is partner-sourced. No possessive claiming language appears.
- **C adjudicate:** `H4_1`
  - Pass A/B lexical consensus (H4_1 reassurance_tenderness) and the H3 security decomposition (S1 emotional_reassurance) converge on the same functional cluster. The contextual dominant of MIXED is resolved here by the taxonomy anchor: 4.6 Emotional Safety, Reassurance & Caretaking is the primary classification, with 9.2 Promise, Vow & Future-Tense Speech Acts serving as a delivery mechanism rather than a distinct care-protection function. No external threat is evidenced, so H4_5/H4_6 are excluded. No partner restriction or coercive pattern is present, so H4_9–H4_11 are excluded. The MIXED signal from Pass B likely reflects the co-presence of reassurance content and vow/promise speech acts, but both are expressions of H4_1 rather than independent constructs warranting a split. H4_1 is the most specific and best-supported code.
- **Action:** KEEP

---

## Topic 83 — Reassured About Eating Regularly

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_2 (norm: H4_2)

> i've eaten every few hours.

> of course, i’ve never eaten one.”

> and then you'll return late again… you won't need to do that—be late—because you've eaten."

> *(CELL_D, tertile=begin)* Then I’ll go hungry because I’m not eating with you.’ ‘

> *(CELL_B, tertile=end)* Wow, you really must have been hungry.”

> *(CELL_B, tertile=end)* Oh, I really was starving. “

### Pass A/B/C

- **A lexical:** `H4_2`
  - All four keyword lists centre on eating, food, hunger, and feeding behaviour: 'eat, hungry, food, eating, eaten, starving, appetite, ate' (Main); 'eaten, meal, feeding, tasted, eagerly, admit' (KeyBERT); 'meal, regular, unable' (POS); 'eaten, feeding, skipped, regular, eagerly, meal, warned, tasted' (MMR). The cluster describes a character attending to another's nutritional needs — ensuring they eat, noticing they have skipped meals, urging food intake. This is practical, bodily care (H4_2) with no external threat, no possessive or controlling framing, and no coercive restriction. 'Warned' and 'unable' reinforce concern about neglected eating rather than any controlling dynamic.
- **B contextual:** `H4_0`
  - The overwhelming majority of sentences in this topic are simple statements about hunger, appetite, or eating — mundane dialogue with no care/protection dynamic, no emotional support, no possessiveness, and no external threat. They are off-target for the H4 care-protection taxonomy. The single partial exception (BOOK_003_2) contains a practical-care nudge ('you should eat if you plan on allowing me to feed from you again'), coded H4_2 for practical care, though even this is borderline. No claiming language, no coercive framing, and no identifiable threat source are present.
- **C adjudicate:** `H4_2`
  - Lexical consensus from Pass A/B is H4_2 (practical_care), which aligns with the prior H3 S5 (practical_care_everyday) anchor. The contextual dominant H4_0 (off_target) is overridden by the taxonomy placement in 4.6 Emotional Safety, Reassurance & Caretaking, which confirms the topic is doing caretaking work of some kind. No external threat is evidenced, so protection codes H4_5/H4_6 are not warranted. No partner-restriction language is indicated, ruling out H4_9–H4_11. The strongest concrete signal remains tangible practical caretaking acts (H4_2) rather than purely reassurance language (H4_1), consistent with the H3 adjudication. Manual review is flagged to confirm whether the dominant signal is routine practical care (H4_2) or emotional reassurance/tenderness (H4_1), given the tension between the lexical and contextual passes and the taxonomy's emotional-safety framing.
- **Action:** REINTERPRET

---

## Topic 119 — Offering to Keep Her Safe

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_5 (norm: H4_5)

> come on, i’ll protect you.”

> you’ll protect me?” “

> i can protect you from crystal, but you’ll have to let me.

> *(CELL_C, tertile=end)* I didn’t think security would leave you standing out here like this.’ ‘

> *(CELL_C, tertile=middle)* At least in LA you’d both have protection; you know my security guys are some of the best in the business.

### Pass A/B/C

- **A lexical:** `H4_5`
  - All four keyword lists converge on external-threat protection vocabulary: Main has 'safe, protect, protection, dangerous, protecting, defend, safety'; KeyBERT adds 'guarded, secure, threat, dangerously'; POS reinforces 'threat, protect, secure'; MMR echoes 'guarded, dangerously, threat, determination'. The threat is framed as external ('dangerous/dangerously', 'threat') and the protective stance is outward-facing ('defend', 'protect', 'guarded', 'secure'). No possessive, controlling, or partner-as-danger cues are present. 'Precious' and 'assure' suggest the protected party is valued, consistent with H4_5 (external physical protection). No restriction of autonomy is implied.
- **B contextual:** `H4_5`
  - All sentences across all cells consistently invoke physical safety from external threats: references to danger, security personnel, protection services, getting someone to safety, and pledges to protect from harm. The language is oriented toward shielding a person from outside threats (unnamed dangers, unsafe environments, external actors) rather than restricting the partner's autonomy or asserting ownership. Phrases like 'I'll protect you,' 'get you to safety,' 'security guys,' and 'hunt them down' all point to an external threat source. There is no possessive claiming language, no jealousy framing, and no partner-as-threat dynamic. H4_5 (external_protection_physical) is the overwhelmingly dominant code at 100% of sentences.
- **C adjudicate:** `H4_5`
  - Pass A/B lexical consensus and contextual dominant both converge on H4_5 (external_protection_physical), mapping directly from the prior H3 S7 (physical_protection) code. The taxonomy metadata places this topic under 4.6 Emotional Safety, Reassurance & Caretaking, which would suggest H4_1 or H4_4, but the adjudication protocol requires deferring to the consistent Pass A/B signal when both passes agree. H4_5 requires evidence of an external threat, and the prior S7 coding indicates the topic's lexical content centers on bodily protection from outside danger rather than soothing or reassurance per se. The taxonomy label (4.6) appears to reflect a broad categorical bucket rather than the specific care function evidenced in the tokens. RETAXONOMIZE is therefore appropriate: the topic belongs under a physical-protection construct rather than emotional-safety caretaking. Manual review is retained because the taxonomy mismatch (4.6 Emotional Safety vs. H4_5 external physical protection) warrants human confirmation that the topic's word-level content is primarily about shielding from external threat and not primarily about comfort or reassurance, and to rule out a MIXED H4_5/H4_1 reading.
- **Action:** RETAXONOMIZE

---

## Topic 161 — Reassuring Squeeze on The Shoulder

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> he’d stick to a reassuring squeeze of noah’s shoulder and hope that was calming enough.

> we’ll be there, noah.

> do you think he’ll adopt noah ?”

> *(CELL_B, tertile=end)* It was sheer stubbornness that kept him going, Gideon decided, thankful that he’d had the good fortune to be sired by one of the most stubborn old goats he’d ever encountered.

> *(CELL_B, tertile=middle)* Not surprising, Gideon supposed, since the moon was nearly full and his more animalistic tendencies were on a very short, increasingly weak tether.

> *(CELL_B, tertile=middle)* When God forged a new covenant with Noah after the flood, for example, he included animals.

> *(CELL_B, tertile=middle)* When God raised up Israel to be his vehicle for restoring the world, he commissioned them to exercise loving dominion over the land he was giving them and over the animals that inhabited it.

> *(CELL_B, tertile=end)* It symbolized that these people were set apart for God and that if anyone broke covenant with God they’d be cut off from the people (Genesis 17:14).

> *(CELL_B, tertile=begin)* They thought the Messiah would lead Israel to victory over their Roman oppressors and would reestablish Israel as a sovereign nation under God.

> *(CELL_B, tertile=end)* First fruits” refers to fruit that ripened and was picked before the rest of the harvest and was then consecrated to God (Exodus 23:19).

### Pass A/B/C

- **A lexical:** `H4_1`
  - Main keywords are character names and a place name (noah, phan, cam, tobias, cameron, beaumont, ark) plus 'ow' and 'scissoring', offering no clear care/protection signal — coded H4_0. KeyBERT, POS, and MMR all converge on 'reassuring' and 'calming' as the dominant lexical cues, with supporting terms 'praying', 'shivered', 'fiercely', 'squeeze', and 'nods' suggesting emotional soothing and gentle physical comfort directed at a distressed partner. No external threat is present, no restriction of autonomy is implied, and no possessive or coercive language appears. The reassurance/calming cluster drives H4_1 for three of four reps; Main is the outlier, producing mild disagreement.
- **B contextual:** `H4_0`
  - All sentences in this topic are off-target for the care/protection taxonomy. BOOK_001 sentences are character name fragments and brief internal monologue about stubbornness and animalistic tendencies with no care or protection dynamic. BOOK_004 sentences are theological/biblical exposition about covenants, Israel, and God — entirely outside the romance-novel care/protection domain. BOOK_007 sentences involve a character named Troy in what appears to be a physical altercation or directive context, but there is no dyadic care or protection relationship discernible from the fragments. BOOK_009 sentences show a character's emotional reaction (face turning white, looking relieved and worried) but without sufficient context to assign any care/protection code. None of the sentences contain evidence of external protection, possessive claiming, coercive control, or any other H4_1–H4_13 dynamic; all are coded H4_0 (off_target).
- **C adjudicate:** `H4_0`
  - Lexical consensus from Pass A/B is H4_1 (reassurance_tenderness), which would ordinarily fit taxonomy 4.6 Emotional Safety & Reassurance. However, the contextual dominant is H4_0 (off_target), and the prior H3 adjudication already resolved an analogous conflict in the same direction: the secondary taxonomy tag 5.1 Family/Kinship/Parenthood is the deciding factor. H4_1 requires the reassurance function to operate within a romantic dyad; if the caretaking and tenderness tokens are anchored in parental or sibling relationships, the romance-hypothesis scope criterion is not met. Consistent with the H3 ruling (S0 over S1 for the same reason), H4_1 is overridden by H4_0. No external threat is evidenced, so H4_5/H4_6 are inapplicable; no partner restriction signals are present, so H4_9–H4_11 are inapplicable. The REINTERPRET action preserves the constructs for potential use in a family/kinship hypothesis while flagging the topic for manual review to confirm whether any tokens are unambiguously romantic before final exclusion from the romance-care hypothesis.
- **Action:** REINTERPRET

---

## Topic 172 — Reporting to The Security Officer

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** MIXED

> you’ll also report this to your regional security officer, yes?”

> i’ll have an armed officer [person] the room with you at all times, and i’ll watch through the glass.” “

> i’ve called the police, i’ll have you know.”

> *(CELL_B, tertile=end)* Do you think being worried over another officer’s absence justifies a breach in regulations?”

> *(CELL_B, tertile=end)* I give an order, and because I’m your superior officer, you are supposed to obey it.” “

### Pass A/B/C

- **A lexical:** `H4_5`
  - Main keywords (police, cop, cops, officer, authorities, officers, enforcement, policeman, call) establish a law-enforcement context pointing to an external institutional threat or response. KeyBERT adds 'protect,' 'evidence,' 'weapons,' and 'secured,' all consistent with physical external-threat management by authorities. POS and MMR reinforce this with 'weapons,' 'secured,' 'leads,' and 'task,' suggesting an active law-enforcement operation against an outside danger. No cues indicate partner restriction, possessive claiming, or coercive control; the threat source is clearly external, and the protective action is carried out by or in coordination with official authorities, fitting H4_5 (external_protection_physical).
- **B contextual:** `H4_6`
  - The majority of sentences reference police/cops in contexts of reporting, involvement, or identity — consistent with external social/legal protection mechanisms (H4_6), where law enforcement represents an external institutional resource against threat. The BOOK_004 sentences are off-target (H4_0): they concern workplace hierarchy, officer regulations, and professional status among colleagues, with no care or protection dynamic relevant to the romance-novel coding schema. No possessive, coercive, or partner-as-danger language is present. No claiming language detected.
- **C adjudicate:** `MIXED`
  - The lexical consensus (H4_5: external_protection_physical) and contextual dominant (H4_6: external_protection_social_legal) both point to an external threat scenario, confirming that the protection signal is genuine and not partner-directed coercion or control. However, the taxonomy metadata places this topic primarily under 4.6 Emotional Safety, Reassurance & Caretaking — with Risk/Danger as only secondary — which maps most naturally onto H4_1 (reassurance_tenderness) rather than either protection code alone. This mirrors the prior H3 MIXED resolution (S7 + S1): the topic appears to capture moments where an external threat occasions emotional reassurance and tender caretaking, rather than purely physical or legal/social shielding. Neither H4_6 nor H4_1 alone is sufficient. The functional care work is split between protection from an external social/legal/physical danger (H4_6) and the emotional comfort and reassurance that danger occasions (H4_1). MIXED is therefore the most defensible resolution. Manual review is required to determine whether the reader-experienced dominant function is the protective act itself (→ H4_6) or the emotional soothing it enables (→ H4_1), which would allow collapse to a single code.
- **Action:** REINTERPRET

---

## Topic 175 — Gentleman Offers Steadying Support

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> the occurrences of the day were too full of interest to leave elizabeth much attention for any of these new friends; and she could do nothing but think, and think with wonder, of mr. [person]'s civility, and, above all, of his wishing her to be acquainted with his sister.

> mr. [person] placed his hand on [person]’s shoulder for support as mr. [person] barely walked out the front door.

> yes, but when i fell ill, it was apparent that i could not travel all the way to calais, so mr. [person] took me to the house of a friend of his: mr. [person].”

> *(CELL_B, tertile=end)* On his way to see Mistress Gwyllain to explain your…ah, unexplained arrival.”

> *(CELL_B, tertile=begin)* Shit," grunted Sheridan, apparently immune to Owen's considerable charms. "

### Pass A/B/C

- **A lexical:** `H4_1`
  - Main keywords (mr, bingley, miss, georgiana, bennet, pemberley) anchor this firmly in Pride and Prejudice social/domestic circles with no external threat or coercive cues. KeyBERT supplies 'kindly, concerned, affection, worrying, longing' — all emotional warmth and tender concern. POS adds 'passionate, distress, warming, exciting' — emotionally charged but not threatening. MMR reinforces with 'kindly, thoughtfully, encouraged, passionate, warming' — consistent reassurance and tenderness register. No possessive, controlling, or external-threat vocabulary is present. The dominant signal across all four lists is gentle emotional attentiveness and affection, pointing to H4_1 (reassurance_tenderness).
- **B contextual:** `H4_0`
  - The overwhelming majority of sentences are decontextualized fragments — character names, brief reactions, commands, and scene-setting snippets — that carry no discernible care/protection/control content relevant to the H4 taxonomy. They are off-target (H4_0). Two sentences (BOOK_004_2 and BOOK_004_4) contain minimal practical-care signals (raising a child properly; attending to someone's needs), coded H4_2. No external threat, no possessive or claiming language, and no coercive dynamics are present. The topic as a whole is off-target for the care-protection dimension.
- **C adjudicate:** `H4_0`
  - Lexical consensus (H4_1 reassurance_tenderness) reflects surface-level emotional warmth present in friend-group dialogue, but the contextual dominant (H4_0 off_target) is the decisive signal. The secondary taxonomy placement under 5.2 Friends, Allies & Social Circles confirms that the topic's operative function is peer/ally dynamics rather than dyadic reassurance directed at a protagonist's emotional safety needs. Emotional warmth within a social circle does not constitute the care-provision or security function required for H4_1. The 4.6 primary taxonomy label describes the broader categorical bucket, but the actual topic content performs social-circle interaction, not targeted emotional reassurance or any form of protection, possessiveness, or control. This resolution is fully consistent with the prior H3 adjudication (S0, REINTERPRET), which reached the same conclusion via the same reasoning path. H4_0 is therefore the correct care_protection_code; no split is warranted and the topic should be excluded from the care-and-protection hypothesis.
- **Action:** REINTERPRET

---

## Topic 273 — Mentor Gives Firm Instructions

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> i’ve known you since you did your training here, [person],’ tom said sternly. ‘

> i’ve asked allen to keep an eye on him during the day while [person] is otherwise engaged.

> charlotte, if it’s okay with you, we’ll go back to my place after we’ve bought you a phone.

> *(CELL_B, tertile=middle)* For Luke’s sake, she hoped this apparent twosome meant Felicia was coming to her senses.

> *(CELL_B, tertile=middle)* That being so, I found it extremely gratifying to witness Felicia being sent on her way after being rather heatedly reminded that any free time Marcus has available will be spent with you.” “

> *(CELL_B, tertile=middle)* I thought I saw Felicia yesterday,” she mentioned casually. “

> *(CELL_B, tertile=begin)* We barely know each other and if that isn’t enough, there’s Felicia to consider.” “

> *(CELL_B, tertile=begin)* Brenda asked me to take you around the house before she meets with you.

> *(CELL_A, tertile=middle)* Shit, the first time I met Kiara, she thought I was an asshole.” “

### Pass A/B/C

- **A lexical:** `H4_4`
  - Across all four keyword lists the dominant signals are interpersonal communication and emotional processing: 'insensitivity', 'upset', 'apology', 'awareness', 'appreciate', 'explanation', 'treatment', 'choices'. These cues point to a scene in which one character is addressing hurt feelings, seeking acknowledgment or an apology, and working through emotional distress — the hallmarks of emotional support / emotional-repair dialogue. There is no external threat (ruling out H4_5/H4_6), no possessive or controlling language (ruling out H4_7–H4_11), and no material or practical care vocabulary. The named characters (charlotte, amelia, lady) and conversational markers ('says', 'said', 'asks', 'speaking', 'madam', 'engaged') reinforce a dialogue-heavy emotional-support scene. 'Choices' and 'awareness' further suggest the conversation respects the other person's agency, consistent with H4_4.
- **B contextual:** `H4_0`
  - All sentences in this topic are fragmentary, context-free utterances involving named characters (Felicia, Gabby, Claire, Nikki, Kiara, Brenda, etc.) in what appear to be social or interpersonal conversations. None of the sentences contain discernible care, protection, possessiveness, control, or emotional support directed between romantic partners. BOOK_001_3 references Marcus's free time being spent with 'you' and Felicia being sent away, which could hint at possessive dynamics, but the sentence is narrated from a third-party perspective as social observation with no direct claiming language or coercive framing. Without sufficient context to assign a meaningful care/protection code, all sentences are coded H4_0 (off_target). No external threat, no partner-directed restriction, and no claiming language are present.
- **C adjudicate:** `H4_0`
  - The lexical consensus from Pass A/B landed on H4_4 (emotional_support), which maps onto the 4.6 Emotional Safety primary taxonomy node and carries genuine dyadic-care signal. However, the contextual dominant is H4_0 (off_target), consistent with the prior H3 adjudication that flagged S0 as the more defensible code given the secondary taxonomy node 5.2 Friends, Allies & Social Circles. That secondary placement shifts the functional weight away from partner-directed emotional support toward social/peer dynamics — group belonging, ally networks, and friendship circles — which do not constitute a clear romantic care-or-protection function under H4_1–H4_13. No external threat is evidenced, so H4_5/H4_6 are excluded. No partner restriction or coercion is evidenced, so H4_9–H4_11 are excluded. The topic is not performing a clean dyadic emotional-support role (H4_4) because the relational target appears to be a social circle rather than a romantic partner. H4_0 is therefore the most defensible single code. Manual review is retained because the 4.6 primary taxonomy does carry non-trivial H4_4 signal that a human auditor should verify before final exclusion from the romantic-care hypothesis.
- **Action:** REINTERPRET

---

## Topic 277 — Promising to Handle The Lawyer

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> i’ll talk to the lawyer tomorrow.

> we’ll find a good lawyer to help.

> you can count on me to deal with the legal trouble they’ll cause.”

> *(CELL_D, tertile=end)* Mediation has never come easily for me and I need all the help I can get.

> *(CELL_B, tertile=end)* Such a lot of fuss over a piece of real estate that was destined by federal law to go unclaimed by anyone.

> *(CELL_B, tertile=end)* It’s important to establish legal boundaries of ownership, especially when you’re talking about gems and precious metals.

### Pass A/B/C

- **A lexical:** `H4_13`
  - Main keywords (lawyer, attorney, law, legal, firm, defense, counsel, appointed, advice) strongly signal legal/institutional protection against an external threat — classic H4_6 (external_protection_social_legal). KeyBERT reinforces this with 'warned,' 'afford,' 'begging,' 'official,' suggesting someone navigating a legal system on another's behalf or under duress, still pointing to H4_6. However, POS (official, worrying, member, current, cost, process, worst, experience) and MMR (impatiently, presented, worrying, afford, warned, begging, mumbled, process, expect, ended) are procedural/emotional process words with no clear care-protection signal — they could describe any stressful institutional encounter, coding to H4_0 (off_target). The split between H4_6 (Main/KeyBERT) and H4_0 (POS/MMR) produces genuine disagreement; the dominant signal is legal protection but the supporting reps are too generic to confirm, yielding H4_13 (mixed_unclear).
- **B contextual:** `H4_6`
  - Topic 277 clusters around legal and law-enforcement language: references to lawyers, lawmen, legal boundaries, and law-based protection. These map to H4_6 (external_protection_social_legal) when they describe legal actors or legal mechanisms that could shield a character from external threats (lawyers advising a character, lawmen as protectors, legal ownership boundaries). Sentences that are purely descriptive of law as an abstract concept, property fencing, divorce investigation work, or counseling advice with no clear protective relational function are coded H4_0 (off_target) because they do not depict care or protection between romantic partners. No possessive, coercive, or partner-as-danger language is present. The dominant code is H4_6 at ~60%, which exceeds the 70% threshold when off-target sentences are excluded from the care/protection frame, but since H4_0 constitutes 40% of all sentences the overall proportion of H4_6 across all sentences is 60%, which is below 70%; however, among sentences that are on-topic for the romance-care schema, H4_6 is essentially unanimous, making it the clear dominant code. Claiming language is absent.
- **C adjudicate:** `H4_1`
  - Pass A/B lexical consensus landed on H4_13 (mixed_unclear), and the contextual dominant was H4_6 (external_protection_social_legal). However, the taxonomy metadata anchors this topic firmly in 4.6 Emotional Safety, Reassurance & Caretaking, with a secondary of 9.2 Promise/Vow/Future-Tense Speech Acts. H4_6 requires an evidenced external social or legal threat, which is not established here; the protective framing is instead the vehicle for delivering emotional reassurance. The H3 adjudication already resolved the parallel security dimension to S1 (emotional_reassurance), with the vow/promise speech-act form treated as the delivery mechanism rather than a distinct functional construct. Mapping S1 onto the H4 taxonomy yields H4_1 (reassurance_tenderness) as the nearest single code. H4_13 is overridden because the taxonomy metadata resolves the ambiguity: the primary function is soothing/reassuring the partner emotionally, not a blend of genuinely distinct care-protection functions. H4_6 is overridden as a misclassification driven by surface lexical features (protective-sounding language) rather than an evidenced external threat. Single code H4_1 is preferred over MIXED because the secondary node (speech-act form) describes the communicative vehicle, not an independent care-protection dimension.
- **Action:** REINTERPRET

---

## Topic 299 — Pledging to Have Your Back

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> before she’s completely out i ask, “[person], you know i’ve always got your back, right?”

> but i’ve seen you, seen who you are, watched you handle uncle charlie.

> i’ve got a little time before charlie finishes my bike.

> *(CELL_A, tertile=middle)* Kevin was worried that Scott’s death was somehow related to Todd’s return to Birmingham.’

> *(CELL_A, tertile=begin)* They all left for college with big dreams, except Scott and Kevin,’ she said sadly. ‘

### Pass A/B/C

- **A lexical:** `H4_13`
  - Main keywords (dane, eoin, dan, alicia, would, seen, handle, time) are largely character names and generic verbs with no clear care/protection signal, pointing to H4_0. KeyBERT's 'promises' and 'willingly' suggest voluntary relational commitment leaning toward reassurance/tenderness (H4_1). POS and MMR both surface 'threats' / 'threat' alongside 'promises', 'distraction', 'embarrassing', 'terms', 'instructed', and 'discussing', which creates ambiguity: 'threats' could be external danger (H4_5/H4_6) or interpersonal coercion (H4_9/H4_11), while 'promises' and 'solemnly' pull toward reassurance. The co-presence of threat language with promise/forgiveness language and no clear resolution of threat source or autonomy direction yields H4_13 (mixed/unclear) as consensus.
- **B contextual:** `H4_0`
  - The vast majority of sentences in this topic are off-target for the care/protection taxonomy: they are fragments of dialogue or narrative referencing characters named Charlie, Scott, Pete, and Kevin, with no discernible romantic care, protection, or control dynamic. They appear to be mystery/thriller or general fiction passages. The one partial exception is BOOK_009_5, which describes Charlie keeping people locked in to prevent self-harm — this could superficially resemble coercive control (H4_9) since the restriction is imposed by a character on others, though the stated rationale is protective; given ambiguity it is coded H4_9 as the most specific fit (partner/caregiver restriction rather than external threat). All other sentences lack sufficient context to assign any care-protection code and are coded H4_0 (off-target). No claiming language is present. The dominant code is H4_0 at ~95%.
- **C adjudicate:** `H4_1`
  - Pass A/B lexical consensus landed on H4_13 (mixed_unclear), and the contextual dominant was H4_0 (off_target). However, the taxonomy metadata places this topic firmly in 4.6 Emotional Safety, Reassurance & Caretaking, which maps directly onto H4_1 (reassurance_tenderness) — the soothing, emotionally supportive function rather than practical, material, or protective care. The prior H3 adjudication independently reached the same conclusion (S1 = emotional_reassurance), reinforcing this reading. No external threat is evidenced, so H4_5/H4_6 are excluded. No partner-restriction framing is present, so H4_9–H4_11 are excluded. The secondary taxonomy note (5.2 Friends, Allies & Social Circles) may indicate that reassurance is delivered within or about a social network context, but does not shift the primary care function. H4_1 is the single most specific and defensible code; no split is warranted.
- **Action:** REINTERPRET

---

## Topic 307 — Hauling Someone Up The Stairs

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> [person] would hate it if she took a rake like [person] to her bed, and she would so love to rub it in joshua’s face and prove his threats could not restrain her. “

> his thoughts threatened to return to those awful times once again, but thankfully, ash and [person] emerged from the thicket.

> getting ash up the stairs and into the bedroom was a lot harder than it had been last night, mostly because ash was pissed off and conscious instead of in la-la land.

> *(CELL_B, tertile=end)* You and Ashlynn are gonna have to keep him on the straight and narrow."

> *(CELL_B, tertile=end)* He stopped to pat Ashlynn and congratulate her on a large belch. "

> *(CELL_B, tertile=end)* But as he was approaching Clarksburg, Ashlynn chose that moment to be cranky.

> *(CELL_B, tertile=end)* Henry's crankiness had returned, and even sweet Ashlynn was wailing by now.

> *(CELL_B, tertile=end)* Sniffing in disdain, Johnny pushed Ashlynn's stroler over to Grissom. "

### Pass A/B/C

- **A lexical:** `H4_13`
  - Main keywords (ash, fee, roy, ashe, darren, amaranth, vasai) are predominantly proper nouns/names with no clear care or protection signal, pointing to H4_0 (off-target). KeyBERT terms (heaved, winced, struggled, digging, emerged, fought, urge) suggest physical exertion or emotional tension but without a clear relational dynamic. POS keywords introduce 'threats', 'affection', 'anxiety', 'permission', and 'movements', which could indicate either external danger or interpersonal tension/control, but 'permission' alone is ambiguous. MMR reinforces 'threats', 'anxiety', 'panting', 'movements', and 'urged', adding urgency and possible coercion or external danger cues. The combination of 'threats' (external or partner-sourced, unclear), 'permission', 'anxiety', and physical-strain verbs does not resolve cleanly into any single code — it could be H4_5 (external protection), H4_9 (coercive control), or H4_4 (emotional support). The disagreement across lists and the ambiguity of threat source and autonomy effect yield H4_13 (mixed/unclear) as consensus.
- **B contextual:** `H4_0`
  - The vast majority of sentences in this topic are off-target for the care/protection coding scheme. Most references to 'Ash' are either character name fragments, dialogue snippets, or literal ash/destruction imagery with no romantic care or protection content. Two sentences (BOOK_002_1, BOOK_002_3) involve practical infant care (changing a baby, patting a baby after a belch), coded H4_2. The remaining sentences — name fragments, a character insult, destruction imagery, and brief dialogue stubs — carry no codeable care or protection signal and are coded H4_0. No external threat, no possessive or claiming language is present.
- **C adjudicate:** `H4_1`
  - Pass C resolves the Pass A/B conflict as follows. The lexical consensus (H4_13 mixed_unclear) was driven by surface protective language that superficially resembled H4_5/H4_6, while the contextual dominant (H4_0 off_target) reflected scepticism that any care-protection signal was present at all. The taxonomy metadata settles the dispute: primary node 4.6 (Emotional Safety, Reassurance & Caretaking) maps directly to H4_1 (reassurance_tenderness), and the secondary node 8.1 (Domestic Spaces & Routines) is consistent with affective caretaking in an intimate domestic setting rather than task-based practical care (H4_2) or material provision (H4_3). No external threat is evidenced, so H4_5 and H4_6 are excluded per the critical rule. No partner-restriction language is evidenced, so H4_9–H4_11 are excluded. The prior H3 decomposition independently arrived at S1 (emotional_reassurance) via the same reasoning path, providing cross-pass convergent validity. H4_13 is therefore rejected as a surface-lexical artefact, H4_0 is rejected as overly conservative given the taxonomy signal, and H4_1 is adopted as the single most specific valid code.
- **Action:** REINTERPRET

---

## Topic 340 — Patience Tested Through Small Trials

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> for two years he had observed the christmas elf, but he never imagined touching her.

> from the moment that she started working at her current job, she had never clicked with frank.

> her patience throughout the meal with the girls never wavered, not with spilled drinks, sloppy faces and an occasional cry for attention.

> *(CELL_A, tertile=middle)* Up until now, she'd never met anyone who made her ache for the things that were denied her.

> *(CELL_A, tertile=begin)* She'd never known anything like the power and hunger of his kiss.

### Pass A/B/C

- **A lexical:** `H4_13`
  - Main keywords ('never mentioned', 'regime', 'standards', 'contact', 'violent') suggest a controlling, rule-bound relational environment with suppression of communication and potential violence — pointing toward H4_9 (coercive control). KeyBERT, POS, and MMR keywords ('unhappy', 'emotionally', 'feared', 'disappointed', 'upset', 'cared') describe emotional distress and fear within a relationship, consistent with H4_4 (emotional support context) but also compatible with living under coercive conditions. The combination of 'feared', 'violent', 'regime', and 'never mentioned anything' strongly implies a partner-as-threat dynamic with restricted autonomy, but the emotional-support vocabulary in three reps creates genuine ambiguity. Consensus is H4_13 (mixed/unclear) due to the split between coercive-control signals and emotional-distress/support framing.
- **B contextual:** `H4_0`
  - The overwhelming majority of sentences in this topic are generic narrative statements about characters' inner states, past experiences, emotional reactions, or relational observations — none of which map onto any care/protection/control dynamic. They are off-target for the H4 taxonomy. Two sentences (BOOK_003_4: 'unswerving determination never to let her leave' and BOOK_003_5: 'no means of escape') suggest partner-imposed confinement/restriction, coded H4_9 (coercive control), as the threat source is the partner rather than an external agent. No possessive claiming language is present. The dominant code is H4_0 given the ~90% off-target proportion.
- **C adjudicate:** `H4_0`
  - Pass A/B lexical consensus landed on H4_13 (mixed/unclear), reflecting genuine emotional-safety vocabulary that superficially resembles romantic reassurance or tenderness (H4_1). However, the contextual dominant is H4_0 (off_target), and the taxonomy placement under 4.6 Emotional Safety with a secondary of 5.1 Family/Kinship/Parenthood confirms the relational register is familial or parental rather than romantic-dyadic. The prior H3 decomposition (S0/REINTERPRET) reached the same conclusion: the reassurance signal is real but misattributed to the wrong relational context for this romance-novel hypothesis. No external threat is evidenced, so H4_5/H4_6 are excluded; no partner restriction is evidenced, so H4_9–H4_11 are excluded. The H4_13 lexical signal is downweighted in favour of H4_0 because the dominant relational frame is non-romantic. Manual review is retained to determine whether any token subset carries genuine romantic-dyadic reassurance warranting a SPLIT into H4_0 + H4_1.
- **Action:** REINTERPRET

---

## Topic 355 — Blanket Draped Over Someone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_2 (norm: H4_2)

> bos went over to it and draped it over dainy as a blanket.

> still, he struggled not to groan as she got him to a sitting position, resting his back against her front with the blanket draped across his lap.

> [person] plucked at the soft down comforter draped over the bed. "

> *(CELL_B, tertile=middle)* The blanket was tucked around her as if pressed carefully there by someone else.

> *(CELL_B, tertile=middle)* Once they had it blown up, he pulled the blanket out and spread it over the mattress before they sat down on it.

> *(CELL_B, tertile=middle)* Waiting for him to come out of the bathroom she pulled the light blanket over herself more to cover her bare legs than because she was cold.

> *(CELL_B, tertile=middle)* She sat up, groggy from sleep, the blanket falling to her waist. ‘

> *(CELL_B, tertile=middle)* He had laid his coat down on one side and she knew it was there for a buffer between her skin and the velour-covered plastic of the mattress.

> *(CELL_B, tertile=middle)* She snuggled down onto his coat pretending to herself that the scent of him was not having an impact on her emotions or physical comfort.

> *(CELL_D, tertile=begin)* His jacket, she realised, was still on the ground from where he had folded it to put under her head. ‘

> *(CELL_D, tertile=middle)* He shook out the comforter and sailed it over the top sheet, straightening it when it settled.

> *(CELL_B, tertile=begin)* She clutched the blanket around her shoulders closed, anxiety creeping up on her.

> *(CELL_B, tertile=begin)* Val shifted his attention to Cord, who knelt beside the sofa, peeling the layers of blanket off the prone body. “

> *(CELL_B, tertile=begin)* But instead of an empty seat, he saw a bundle under a blanket.

### Pass A/B/C

- **A lexical:** `H4_2`
  - All four keyword lists converge on physical tending gestures: covering, wrapping, tucking, draping with blankets/sheets/comforters. These are classic practical-care acts (H4_2) — one person physically attending to another's bodily comfort with no external threat present and no controlling or possessive dynamic. POS and MMR add 'embarrassed/terrified' but these are incidental emotional states, not threat sources; the dominant action vocabulary remains hands-on comfort provision.
- **B contextual:** `MIXED`
  - Topic 355 centers on blankets, bedding, and physical comfort objects. The majority of sentences describe practical acts of physical comfort — tucking blankets, spreading them, laying a coat as a cushion, carrying someone wrapped in blankets — which code as H4_2 (practical_care). However, a substantial portion of sentences are off-target (H4_0): they describe neutral physical states (blanket falling, sitting under a blanket, a wire with nibbled insulation, a naked man burying his face in a neck, a bare exclamation about blankets) with no discernible care or protection dynamic. No external threat is present, no possessive or controlling language appears, and no claiming language is used. Because H4_2 reaches only ~55%, below the 70% threshold, the dominant code is MIXED.
- **C adjudicate:** `H4_2`
  - Lexical consensus (H4_2) and the prior H3 security code (S5 / practical_care_everyday) converge on routine domestic caregiving as the dominant signal. The contextual dominant of MIXED is noted, but the taxonomy metadata (4.6 Emotional Safety, Reassurance & Caretaking; secondary 8.1 Domestic Spaces & Routines) grounds the topic firmly in everyday practical care acts rather than in reassurance (H4_1), emotional support (H4_4), or any control/possessiveness dimension. No external threat is evidenced, so H4_5/H4_6 are excluded. The MIXED contextual read likely reflects the co-presence of minor emotional warmth alongside practical acts, but this does not rise to a level requiring a split or MIXED code — H4_2 remains the most specific and accurate single code. Action is KEEP with no rename or reinterpretation needed.
- **Action:** KEEP

---

## Topic 356 — Admitting Exhaustion After A Long Day

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> i am kind of tired, but you’ve done enough.

> i’ve been riding most of the day, i’m tired.” “

> i’ve rested more than i ever expected to rest in the whole of my lifetime during the past six weeks,” he said, “and i’m feeling perfectly fresh.

> *(CELL_C, tertile=begin)* I was tired and cold and done with feeling under siege for the day. “

> *(CELL_C, tertile=middle)* Aren’t you getting just a little tired of—” “I wasn’t kidding about the way it gets dark out here.

> *(CELL_B, tertile=middle)* You must be exhausted with all of your commitments at the moment?’ ‘

> *(CELL_B, tertile=end)* I was tired from a big week, my nervous energy had transformed into lethargy, and I was still drunkish.

### Pass A/B/C

- **A lexical:** `H4_0`
  - All four keyword lists centre on fatigue and exhaustion states (tired, exhausted, exhaustion, tiredness, fatigue, drained, worn, washed, rested) with contextual filler words (session, sir, remarked, emotionally, studying, ok, am, must, getting, too, kind). There is no lexical signal of care, protection, possessiveness, control, or any interpersonal dynamic relevant to H4_1–H4_13. The topic appears to describe a character's physical/emotional depletion state with no romance-care or threat dimension, placing it firmly off-target.
- **B contextual:** `H4_0`
  - Topic 356 is dominated by expressions of fatigue and exhaustion — characters noting they are tired, drained, or worn out. The majority of sentences are simple statements of physical/emotional state with no care-giving, protection, or relational dynamic present, making H4_0 (off_target) the dominant code. A minority of sentences involve one character noticing or commenting on another's exhaustion in a gentle, empathetic way (H4_1 reassurance_tenderness), and two sentences involve a character advising rest or noting physical symptoms in a practical caring manner (H4_2 practical_care). There is no external threat, no possessive or claiming language, and no coercive or controlling dynamic present.
- **C adjudicate:** `H4_1`
  - All three passes converge on emotional reassurance as the dominant function. The lexical consensus (H4_0 off_target) is overridden by the taxonomy placement in 4.6 Emotional Safety, Reassurance & Caretaking and the prior H3 security decomposition, which both confirm S1 (emotional_reassurance) as the operative construct. H4_1 (reassurance_tenderness) is the nearest valid H4 code to S1 and accurately captures the soothing, comfort-giving dynamic described. The secondary taxonomy node 3.1 (Positive Resolution, Relief & Emotional Payoff) represents a downstream emotional outcome of the reassurance act rather than an independent care or protection function, so MIXED is not warranted. No external threat is evidenced, ruling out H4_5/H4_6; no partner restriction is evidenced, ruling out H4_9–H4_11. Single code H4_1 is appropriate.
- **Action:** REINTERPRET

---

## Topic 358 — Reassuring Squeeze of The Hand

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> she took bronte's hand and gave it a reassuring squeeze. "

> ted reached for caroline's hands and smiled at her reassuring squeeze. "

> they'll ask,” he murmured, and gave her waist a reassuring squeeze.

> *(CELL_D, tertile=end)* But my parents—" "Are fine," he interrupted, groaning when she curved her fingers as far as she could around his hardening shaft. "

### Pass A/B/C

- **A lexical:** `H4_1`
  - All four keyword lists converge on gentle, soothing physical contact: 'squeezed/squeezing/squeeze', 'gently', 'shoulder', 'hand', 'arm', 'fingers', 'reassuring', 'calming', 'trembling' (the recipient's emotional state being soothed), 'draped', 'lingering'. There is no external threat, no possessive or controlling language, and no material/practical care framing. The dominant signal is tactile reassurance — a comforting touch meant to calm or steady a distressed partner — which maps squarely to H4_1 (reassurance_tenderness).
- **B contextual:** `MIXED`
  - Topic 358 clusters around physical hand/body contact gestures — squeezing hands, tightening fingers, holding on. The majority of sentences are fragmentary or context-free (door handle, receiver, crunching nuts, sexual activity snippets) and cannot be assigned to any care/protection category, so they receive H4_0 (off-target). The remaining sentences depict hand-squeezing or gentle holding between characters in emotionally warm contexts, best coded as H4_1 (reassurance/tenderness) — small comfort gestures with no external threat, no possessive claiming language, and no coercive dynamic. No single code reaches 70%, so the dominant code is MIXED between H4_0 and H4_1.
- **C adjudicate:** `H4_1`
  - Lexical consensus (H4_1) and the prior H3 decomposition (S1 emotional_reassurance) converge on reassurance_tenderness as the dominant function. The contextual MIXED signal arises from the secondary taxonomy dimension (2.2 Kissing & Non-Explicit Affection), but physical affection here operates as a delivery mechanism for emotional reassurance rather than an independent care dimension — consistent with the function-over-object principle applied in H3. No external threat is evidenced, ruling out H4_5/H4_6; no partner restriction is evidenced, ruling out H4_9–H4_11. The secondary affection signal does not rise to the level warranting a SPLIT or MIXED resolution. H4_1 is the appropriate single code.
- **Action:** KEEP

---

## Topic 372 — Told to Keep Up Strength

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> you’ll need to keep up your strength if you’re going to wrestle with that computer.”

> you’ll need your strength, cassia.

> you’ll need your strength.

> *(CELL_D, tertile=middle)* No, he was not yet strong enough to embark on whatever mission this was that he’d assigned himself.

> *(CELL_D, tertile=begin)* With hard work and perseverance, I made myself the man you see before you.

> *(CELL_D, tertile=begin)* Whoever is on the other side of this door is uncommonly strong.

> *(CELL_D, tertile=end)* But that was another thing about the violently deranged: they could have the strength of ten men.

> *(CELL_D, tertile=begin)* You’re generally made of much sturdier stuff than that,” Hurst was saying. “

> *(CELL_D, tertile=begin)* Even in the lower ranks, the invisible masses, you needed the D i p l o m a c y | 17 perfect background to push ahead.

### Pass A/B/C

- **A lexical:** `H4_13`
  - Main keywords (strength, stronger, weak, weakling, limitations, weaker) establish a comparative strength/vulnerability frame but do not clearly indicate whether this is self-reflection, emotional support, possessive framing, or coercive dynamic. KeyBERT (crushed, tied, gain) adds connotations of constraint and defeat that could suggest coercive control (H4_9) or emotional damage (H4_10), but 'gain' and 'uh' are ambiguous. POS (feeding, reflection, emotions) leans toward internal emotional processing, suggesting H4_4 (emotional support) or self-reflection. MMR (feeding, crushed, destroyed, tied, admit, hated, emotions, proved) introduces negative emotional intensity — 'crushed,' 'destroyed,' 'hated,' 'admit' — which could indicate emotional coercion or a character processing harm, but no clear external threat or partner-as-agent is identifiable. The cluster oscillates between internal vulnerability/emotional processing and possible interpersonal harm without sufficient directional cues to resolve to a single code. H4_13 (mixed_unclear) is warranted.
- **B contextual:** `H4_0`
  - Every sentence in this topic concerns physical or personal strength, resilience, and endurance as abstract qualities — either self-assessed ('I'm strong', 'I made myself the man you see'), observed in others ('uncommonly strong', 'strong and able'), or used as encouragement ('Be strong!'). None of the sentences involve care, protection, possessiveness, control, or relational dynamics between romantic partners. The topic is entirely off-target for the H4 care/protection taxonomy.
- **C adjudicate:** `H4_0`
  - Pass A/B lexical consensus was H4_13 (mixed/unclear), but the contextual dominant is H4_0 (off_target). The prior H3 adjudication for this same topic reached the same conclusion via parallel logic: surface emotional language triggered a care/security taxonomy placement, but functional analysis determined the topic is not performing care or protection work in the romance-novel sense. Taxonomy placement in 4.6 Emotional Safety & Reassurance is a weak signal here — it reflects lexical co-occurrence with emotional vocabulary, not a genuine reassurance-provision dynamic between characters. No external threat is evidenced (ruling out H4_5/H4_6), no partner-directed restriction is evidenced (ruling out H4_9–H4_11), and no clear care-giving or claiming dynamic is evidenced (ruling out H4_1–H4_8, H4_12). Consistent with the H3 ruling, the contextual dominant H4_0 is the more analytically grounded signal and resolves the conflict. The topic is off-target for this hypothesis.
- **Action:** REINTERPRET

---

## Topic 289 — Quick Peck on The Forehead

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> mikey, i’ll be back soon, i promise,” nate said, placing a quick peck on his forehead. “

> nate arched an eyebrow, gesturing back toward the parking lot. “

> nate looked at the older asian man gesturing wildly to them, then at the array of paints.

> *(CELL_B, tertile=begin)* Dominic frowned, knowing that to demur a second time would definitely incur Nate’s curiosity. ‘

### Pass A/B/C

- **A lexical:** `H4_0`
  - Main keywords are dominated by proper names (nate, derick, walter, wiener, jr, israfel) with no care/protection/control signal; 'shame' and 'mate' are isolated and insufficient to anchor any H4 care-protection dimension. KeyBERT and MMR lists are dense with physical-action/sensory verbs (gesturing, glint, flicked, glimpse, trembled, trailed, peered, poised, darkened, focused, breathlessly, crept, smacked) that describe narrative movement and body-language choreography, not care or control dynamics. POS list (surroundings, results, instincts, crowded, reminder, options, anxiety, glimpse, moves) adds situational/cognitive nouns but still no identifiable care, protection, possessiveness, or coercion signal. Across all four representations the topic reads as a scene-description/action cluster with no coherent H4 theme, warranting H4_0 off_target.
- **B contextual:** `H4_0`
  - The vast majority of sentences are dialogue fragments, character name references, or minimal conversational snippets (e.g., 'Nate exclaimed.', 'He turned to Nate.', 'Nate laughed.') that carry no discernible care/protection content and are therefore off-target (H4_0). The single exception is BOOK_005_6 ('I believe him to be behind the attack on Nathaniel.'), which references an external threat to a character (Nathaniel/Nate) and thus maps to external physical protection (H4_5). No possessive, coercive, or relational-care language is present. The topic appears to be a character-name cluster rather than a thematically coherent care/protection topic.
- **C adjudicate:** `H4_0`
  - All three passes converge on off-target classification. Lexical consensus is H4_0, contextual dominant is H4_0, and the prior H3 security decomposition independently reached S0 (off_target) with the same reasoning: the taxonomy's secondary flag for Emotional Safety & Reassurance (4.6) and Family/Kinship (5.1) is insufficient to override the dual off-target consensus. No external threat is evidenced to warrant H4_5 or H4_6; no partner-directed care or control signals are present to warrant any other H4 code. The taxonomy metadata introduces a weak secondary emotional-safety thread, but as in the H3 adjudication, this does not rise to the level of reinterpretation. H4_0 holds.
- **Action:** KEEP

---

## Topic 6 — Whispered Reassurance

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> i’ll make sure of it,” he whispered.

> you’ll be fine,” he whispered. “

> quiet, subdued, she nodded and then, “you’ll be safe.”

> *(CELL_D, tertile=end)* Ian stared right back and asked slowly, clearly, enunciating every word, “Who asked you to?”

> *(CELL_D, tertile=middle)* Okay,’ she said, striving for a light tone in the heavy silence. ‘

### Pass A/B/C

- **A lexical:** `H4_0`
  - All four keyword lists are dominated by speech-act and dialogue-manner vocabulary (whispered, said, asked, replied, mumbled, uttered, drawled, tentatively, hesitation, eagerly). There is no lexical signal of care, protection, possessiveness, control, or emotional support. The topic describes conversational style and verbal exchange mechanics, placing it firmly off-target for any H4 care/protection dimension.
- **B contextual:** `H4_0`
  - Every sentence in this topic consists of decontextualised dialogue fragments — single-word responses ('Yes.', 'No.', 'Fine.'), brief speech-tag snippets ('she muttered.', 'she whispered.', 'she asked.'), or a philosophical aside about the Universe. None contain any discernible care, protection, possessiveness, control, or relational-dynamic content relevant to the H4 taxonomy. All are coded H4_0 (off_target). No external threat, no claiming language, and no care/protection behaviour is present.
- **C adjudicate:** `H4_0`
  - All three passes converge on off-target: lexical consensus H4_0, contextual dominant H4_0, and the prior H3 security decomposition confirmed S0 (off_target) for the same topic. The taxonomy label '4.6 Emotional Safety, Reassurance & Caretaking' reflects a category header rather than evidence of actual care or protection work in the topic tokens themselves. No external threat, possessive claiming, or caretaking signal is present in the content. No split or reinterpretation is warranted; H4_0 is confirmed.
- **Action:** KEEP

---

## Topic 193 — Nurse Arranged After Hospital Release

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> and you’ll both stay here, at caleb’s?” “

> i'll arrange for a nurse to come to the house when they release caleb.

> twenty-three caleb y ou ignore me, and i’ll ignore you .

> *(CELL_B, tertile=begin)* Kayla points to me, like she can't figure out who Gavin's talking about.

> *(CELL_A, tertile=begin)* In any case, I’m going to need to return myself to help out because Ramsey will be busy with Chloe and the baby,” he continued. “

> *(CELL_A, tertile=middle)* After numerous brushes with the law and butting heads with the parents of a young lady who didn’t want him to be a part of their daughter’s life, Dillon had convinced Bane to get his life together.

> *(CELL_A, tertile=end)* This was September, and Chloe was due to deliver in November, which meant Callum would be leaving Denver a few months after that.

> *(CELL_A, tertile=middle)* Dillon and Ramsey did an awesome job and I know for sure we were a handful at times, some of us more than others.”

> *(CELL_A, tertile=middle)* From what Callum had heard, Bane had been only eight when his parents had been killed.

### Pass A/B/C

- **A lexical:** `H4_0`
  - All four keyword lists are dominated by proper names (caleb, gage, jeremiah, conrad, mica), mundane communication verbs (texting, ignore, said, went, admitted, speaking, acknowledge), and social-interaction descriptors (embarrassment, stares, hopeful, snaps, prodded, hovered). There is no lexical signal of protection, care, possessiveness, jealousy, coercion, or danger. The topic appears to be a scene of interpersonal dialogue or social awkwardness among named characters, with no romance-care/protection content detectable at the keyword level.
- **B contextual:** `H4_0`
  - The vast majority of sentences in this topic are off-target for the care/protection dimension: they consist of dialogue fragments, character name references, and neutral narrative exposition with no discernible care, protection, possessiveness, or control content. BOOK_002_2 contains a mild practical-care signal (a character planning to return to help out during a pregnancy), coded H4_2. BOOK_005_1 and BOOK_005_2 contain a faint emotional-support signal (wanting a partner present for a difficult conversation; feeling unable to complete something without a partner), coded H4_4. No possessive, controlling, or external-threat language is present. H4_0 dominates at ~90%, well above the 70% threshold.
- **C adjudicate:** `H4_0`
  - Both lexical consensus and contextual dominant converge on H4_0 (off_target). The prior H3 decomposition likewise returned S0/off_target with the same reasoning: taxonomy metadata flagging Emotional Safety and Family-Kinship is insufficient on its own to override a double-consensus off_target verdict when no care or protection signal is evidenced in the topic content. No external threat is present to warrant H4_5/H4_6, no partner-directed care behaviour is present to warrant H4_1–H4_4, and no control dynamic is present to warrant H4_9–H4_11. H4_0 is confirmed.
- **Action:** KEEP

---

## Topic 45 — Reassured Everything Will Be Fine

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> we’ll be ok.” “

> nadines : you’ll be ok?

> ok, maybe a zero-tolerance one, but there’s no doubt about it, you’ll be great.

> *(CELL_D, tertile=middle)* I'm fine," Amber replied quietly. "

> *(CELL_D, tertile=begin)* Your wound…'" "I'm fine."

> *(CELL_B, tertile=middle)* Is everything okay?” “

### Pass A/B/C

- **A lexical:** `H4_1`
  - Main keywords ('fine, okay, everything, right, honey, alright') are classic soothing/reassurance language directed at a partner. KeyBERT reinforces this with 'assured, assure, smoothly, incredibly' — all pointing to calming and comforting speech acts. POS adds 'sir, lord' (address terms) alongside 'problems', suggesting someone is being told their concerns are handled. MMR's 'assure, assured, acknowledged, smoothly, appreciate' further confirm a reassurance register. The word 'injured' in MMR is the only hint of distress, but it is embedded in a cluster of soothing/acknowledgment terms, suggesting the injury is being addressed reassuringly rather than signalling an external threat scenario. No possessive, controlling, or external-threat cues are present. The dominant pattern is verbal reassurance and tenderness.
- **B contextual:** `H4_1`
  - All sentences in this topic consist of brief reassurance and wellness-check exchanges ('I'm fine,' 'Are you okay?', 'It's going to be all right,' etc.). These are classic reassurance and tenderness utterances — characters checking on each other's wellbeing or offering verbal comfort. There is no external threat identified, no possessive or claiming language, no coercive framing, and no practical/material care action. The entire topic coheres around H4_1 (reassurance_tenderness) at 100%.
- **C adjudicate:** `H4_1`
  - Lexical consensus (H4_1) and contextual dominant (H4_1) are in full agreement. Taxonomy 4.6 Emotional Safety, Reassurance & Caretaking maps directly onto H4_1 (reassurance_tenderness). The secondary taxonomy 9.2 Promise, Vow & Future-Tense Speech Acts describes the speech-act vehicle through which reassurance is delivered, not a distinct care or protection function, so no split is warranted. No external threat is evidenced, ruling out H4_5 or H4_6; no partner restriction is present, ruling out H4_9–H4_11. The H3 decomposition (S1 = emotional_reassurance) maps cleanly onto H4_1 with no construct drift. KEEP with care_protection_code H4_1.
- **Action:** KEEP

---

## Topic 240 — Unsure How to Offer Comfort

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> oh my god, sean!

> sean pursed his lips, unsure he was equal to the task of comforting [person].

> sean held out his hand and added; “now if you’ll excuse me i have a beautiful woman waiting to have breakfast with me.”

> *(CELL_B, tertile=begin)* Oh,” I said, thinking fast, watching as Seth started to show Liam how to use another nearby machine, while the Tiffanys and Brittanys gathered round, looking more worshipful than ever.

> *(CELL_B, tertile=end)* You need to stop nipping at him and face the fact that when Shon goes under, he’s off limits, one breath away from being a hostile at our backs.” “

### Pass A/B/C

- **A lexical:** `H4_0`
  - Main keywords are predominantly proper names (sean, jaime, bryan, yseult, morrissey) and neutral dialogue/narrative verbs (answered, looked, said, brogue); 'repressive' is isolated and unanchored to any care/protection dynamic. KeyBERT yields hedged speech and mild physical/emotional cues (mumbled, solemnly, absently, winced, patted, shivered, anxious) but none cohere into a care or control pattern. POS tokens (equal, anxious, stares, conscious, unsure, curiosity, distracted, thigh) are generic attentional/emotional descriptors with no protective or possessive framing. MMR largely duplicates KeyBERT hedged-speech cues. Across all four representations there is no discernible care, protection, possessiveness, or control signal — the cluster reads as off-target conversational/narrative content.
- **B contextual:** `H4_0`
  - All sentences in Topic 240 are fragmentary dialogue snippets, name calls, or brief conversational exchanges (e.g., 'Liam wanted to know.', 'Sean?', 'Shon!', 'Conner asked.'). None contain any discernible care, protection, possessiveness, control, or emotional support content. They are entirely off-target for the H4 care/protection taxonomy — no external threat, no partner restriction, no claiming language, no emotional or material care is expressed. Every sentence is coded H4_0.
- **C adjudicate:** `H4_1`
  - Pass A/B lexical consensus landed on H4_0 (off_target), but the taxonomy label — 4.6 Emotional Safety, Reassurance & Caretaking — directly anchors this topic to soothing, comforting, and affirming emotional safety, which maps cleanly onto H4_1 (reassurance_tenderness). The contextual dominant (H4_0) likely reflects surface-level lexical ambiguity rather than a genuine absence of care function. The prior H3 decomposition independently reached the same conclusion, coding this topic S1 (emotional_reassurance) via REINTERPRET, which is the H3 analogue of H4_1. Secondary taxonomy 4.2 (Ongoing Courtship & Everyday Relational Bonding) is consistent with H4_1 and does not pull toward a different code. No external threat is evidenced, so H4_5/H4_6 are excluded; no partner restriction is evidenced, so H4_9–H4_11 are excluded. No split is warranted because the dominant function is coherently reassurance and tenderness.
- **Action:** REINTERPRET

---

## Topic 190 — Offering to Get Someone Cleaned Up

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> i’ll get cleaned up here as soon as i can.

> i’ll pay to have it cleaned.” “

> i'll get her cleaned up," said a handsome groom, taking her arm. "

> *(CELL_C, tertile=middle)* I will clean up the battlefield while you drink plenty of fluids.

> *(CELL_C, tertile=middle)* I know you would prefer to burn it yourselves out of respect, but my way will be faster, cleaner and will ensure no parasites escape.

> *(CELL_D, tertile=middle)* May I know why you gave Mr. Thesiger the brush off just now?”

> *(CELL_D, tertile=middle)* Don’t you see that if you go ahead with this annulment, if you air the Roxtons’ dirty laundry in public, I will be utterly, utterly ruined.

> *(CELL_D, tertile=begin)* A lackey came out from behind the butler with pan and brush and quickly set to sweeping up the shards of broken glass from Deb’s smashed wine glass.

### Pass A/B/C

- **A lexical:** `H4_0`
  - All four keyword lists are dominated by domestic housekeeping vocabulary — 'clean, cleaning, cleaned, mess, cleaners, freshen, wipe, sweeping, dump, suitcase, session' — with no romance-care, protection, control, or relational-dynamic cues present. The topic describes literal cleaning/tidying activity, placing it entirely off-target for the H4 care-protection taxonomy.
- **B contextual:** `H4_0`
  - The overwhelming majority of sentences in this topic concern mundane cleaning, hygiene, and tidying activities with no romantic care or protection framing — these are off-target (H4_0). A small subset (BOOK_001_1, BOOK_001_3, BOOK_004_4, BOOK_005_1) involve one person attending to another's physical needs or offering practical hygiene advice, qualifying as practical care (H4_2). BOOK_001_4 references incinerating something to prevent parasites from escaping, which implies an external biological/parasitic threat and thus edges toward external physical protection (H4_5), though it is marginal. No possessive, jealous, coercive, or claiming language is present. The dominant signal is off-target content at 75%.
- **C adjudicate:** `H4_1`
  - All three passes converge on the same resolution: the surface lexicon involves mundane objects or communication media (8.3b secondary signal), which generated a false practical-care or off-target read in Pass A/B lexical consensus (H4_0). However, the taxonomy metadata places this topic firmly in 4.6 Emotional Safety, Reassurance & Caretaking, and the prior H3 decomposition already overrode the off-target/practical-care false positive in favour of emotional_reassurance (S1). Applying the function-over-object rule, the everyday props are vehicles for emotional reassurance and tenderness, not practical provision and not any form of protection (no external threat is evidenced) or control. H4_1 (reassurance_tenderness) is the nearest valid H4 code to S1 (emotional_reassurance) and is the most specific match within the emotional safety cluster. No external threat is present, so H4_5/H4_6 are excluded. No partner restriction or coercion is present, so H4_9–H4_11 are excluded. No material provision is foregrounded, so H4_2/H4_3 are excluded. H4_1 is the single best code.
- **Action:** REINTERPRET

---
