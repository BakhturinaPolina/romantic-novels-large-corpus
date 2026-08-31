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
- **Code:** H4_7 (norm: H4_7)
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

## Topic 24 — Confronting An Unwanted Marriage

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** H4_0 (norm: H4_0)

> we’ll be married… to each other.”

> you’re already married to me; he’ll understand.” “

> i’ll give you a divorce and you can just walk away.

> *(CELL_D, tertile=begin)* So that whole getting married and settling down part doesn't appeal to you?"

### Pass A/B/C

- **A lexical:** `H4_9`
  - The keywords 'marry', 'married', 'marriage', 'husband', 'wife', 'divorce', and 'engaged' suggest a focus on commitment and relationships. 'Unhappy' and 'threats' indicate potential conflict or coercion within these relationships. The absence of an external threat source makes 'H4_9' (coercive control) the most fitting code.
- **B contextual:** `H4_5a`
  - The dominant code is H4_5a (protective commitment) as most sentences discuss marriage or commitment without an external threat. There's no external protection (H4_5, H4_6) or coercive control (H4_9-H4_11) mentioned. The language used also indicates possessive claiming (H4_7) in some sentences.
- **C adjudicate:** `H4_5a`
  - The consensus and dominant codes suggest a focus on protective commitment, not external protection or coercive control. The taxonomy also supports this interpretation.
- **Action:** REINTERPRET

---

## Topic 27 — Racing The Approaching Storm

- **Taxonomy:** 7.3 — Risk, Danger & External Crises
- **Code:** H4_5 (norm: H4_5)

> it’ll be dark before we know it.’’

> i don’t know if i’ll be able to get back here before the storm hits.

> it’s going to rain and we’ll be caught out in the storm.

> *(CELL_D, tertile=end)* Their lips met, and an explosion of passion took them along on a tide, the darkness that surrounded them like a blanket against the rest of the world.

> *(CELL_D, tertile=begin)* Just as they reached the spot a man strode angrily out of a neighbouring field, and even in the poor light his expression could be seen as thunderous.

> *(CELL_D, tertile=begin)* They were still driving, the high hedges making it impossible for them to see anything but the road in front of them.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'rain', 'snow', 'storm', 'dark', 'dangerously' suggest external threats, while 'light', 'sun', 'moon' imply protection from these threats. The terms 'lighting', 'curtain', 'reflection' in KeyBERT, POS, and MMR also support this interpretation.
- **B contextual:** `H4_5a`
  - Most sentences describe external conditions (rain, storm, darkness) or internal states (sunlight, dawn), indicating protective commitment (H4_5a) rather than external protection, possessive claiming, or coercive control.
- **C adjudicate:** `H4_5`
  - The topic discusses physical protection from external threats, which aligns with H4_5. No external threat is mentioned, but the topic focuses on the responsibility and commitment to protect, fitting H4_5a. However, since the taxonomy is about external crises, H4_5 is more appropriate.
- **Action:** KEEP

---

## Topic 33 — Werewolf Pack Confrontation

- **Taxonomy:** 10.1 — Paranormal & Immortal Beings
- **Code:** H4_7 (norm: H4_7)

> i’ll miss you, mr. [person].”

> we’ll buy one on the way down to wolf hole.

> take your woman and leave—i’ll handle the vaile wolves.”

> *(BOOK_002, CELL_A, tertile=end)* Seems odd that whoever is behind this would go after such a powerful wolf.” “

> *(BOOK_003, CELL_B, tertile=middle)* It took all her will not to kick him in the face this time, like Wolf said.

> *(BOOK_003, CELL_B, tertile=middle)* Wolf’s worship was practically a given for anyone wearing the cut, a source of open ridicule from all the members. “

### Pass A/B/C

- **A lexical:** `H4_7`
  - The keywords 'wolves', 'werewolf', 'werewolves', 'pack', 'alpha', 'creatures', 'instincts', 'ripping', 'crouched', 'paced', 'circling', 'dangerously' suggest possessive claiming (H4_7) as the werewolves are protecting their territory and pack from external threats.
- **B contextual:** `H4_5`
  - The sentences primarily discuss the presence and actions of wolves, indicating external protection (H4_5) or protective commitment (H4_5a) towards the characters. There's no possessive claiming or coercive control language.
- **C adjudicate:** `H4_7`
  - The topic's dominant code is H4_7, indicating possessive claiming, which aligns with the taxonomy of 10.1 Paranormal & Immortal Beings and the secondary theme of 7.3 Risk, Danger & External Crises. No external threat is evident, so H4_5a is not applicable. The lexical consensus also supports this code.
- **Action:** KEEP

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
  - The keywords 'fine', 'ok', 'okay', 'alright', 'will', 'assured', 'smoothly' indicate reassurance and tenderness, suggesting a lack of external threat and support for the partner's autonomy.
- **B contextual:** `H4_4`
- **C adjudicate:** `H4_1`
  - The topic's dominant code, H4_4 (emotional support), aligns with the taxonomy's focus on emotional safety and reassurance. The lexical consensus code, H4_1 (reassurance_tenderness), further supports this interpretation. No external threats or possessive/coercive elements are present, so H4_5a (protective_commitment) is not applicable.
- **Action:** KEEP

---

## Topic 56 — Promising Never to Hurt You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_5 (norm: H4_5)

> you'll get hurt," he managed to say. "

> you know i’ll never hurt you .”

> i’ll make sure you aren’t hurt.” “

> *(CELL_D, tertile=middle)* It’s all well and good saying you avoid pain by avoiding relationships, but what about the wonderful things you’re avoiding as well?

> *(CELL_D, tertile=end)* He says that he knows it must hurt, but that whatever will be, will be, and that nothing we say or do will resolve things.

> *(CELL_C, tertile=begin)* You didn’t hit me with a sledgehammer last night, did you?” “

> *(CELL_C, tertile=middle)* I didn’t know why I felt hurt, but it stung not to be invited. “

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'hurt', 'hurting', 'harm', 'threatened', 'causing' indicate external protection (H4_5) as the topic discusses protecting from a partner's harmful actions.
- **B contextual:** `H4_5a`
  - The dominant code is H4_5a (protective commitment) as several sentences express a desire not to hurt someone or express remorse for doing so, without an external threat. There's no possessive claiming or coercive control language, and the threat source is unclear or internal.
- **C adjudicate:** `H4_5`
  - The topic discusses the male character physically protecting the female character from external threats, which aligns with the 'external_protection_physical' code (H4_5).
- **Action:** KEEP

---

## Topic 59 — Mother's Disapproval Looms

- **Taxonomy:** 5.1 — Family, Kinship & Parenthood
- **Code:** H4_4 (norm: H4_4)

> does mama know you’ve left the nursery?”

> didn’t your mom tell you i’ve been having problems?” “

> mum will berate me for leaving graham at “this time”, and i’ll be forced to defend myself, something i’m not used to doing.

> *(BOOK_001, CELL_D, tertile=begin)* Oh, and then there's my mother... maybe we should focus on your bad habits." "

### Pass A/B/C

- **A lexical:** `H4_4`
  - The keywords 'mother', 'mom', 'mama', 'daughter', 'affection', 'taught', 'instructed' suggest emotional support and guidance, indicating H4_4 emotional_support.
- **B contextual:** `H4_0`
  - All sentences refer to mothers or parents in a neutral or affectionate manner, with no indication of external protection, protective commitment, possessive claiming, or coercive control.
- **C adjudicate:** `H4_4`
  - The lexical consensus of H4_4 (emotional_support) aligns with the contextual dominant code H4_0 (off_target), indicating that the topic primarily revolves around emotional support, not physical or external protection, possessive claiming, or coercive control.
- **Action:** RENAME

---

## Topic 68 — Promising to Set Things Straight

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** H4_0 (norm: H4_0)

> i’ll ask him about it,” [person] said, an edge of roughness to his voice, “and set him and the others straight.

> we’ll have to ask [person] dubose to endorse it.” “

> i'll have jack get on it.” “

> *(BOOK_002, CELL_B, tertile=middle)* He planted me right in front of Jack’s face. “

> *(BOOK_002, CELL_B, tertile=middle)* Jack seemed to enjoy it, but I was bored.

> *(BOOK_002, CELL_B, tertile=middle)* How do you want to proceed with Jack?

### Pass A/B/C

- **A lexical:** `H4_5`
  - The Main and KeyBERT keywords ('role', 'poised', 'kindly') suggest protective commitment (H4_5a), while POS and MMR ('threats', 'strangled') indicate external physical protection (H4_5). The consensus is H4_5 as it's the most prominent and the threat is external, with no clear restriction on autonomy.
- **B contextual:** `H4_0`
  - Most sentences are off-target (H4_0) as they do not explicitly show any form of protection, care, or control. The sentence 'Jack certainly likes the ladies, huh?' (BOOK_003_5) is coded as possessive claiming (H4_7) as it suggests a possessive attitude towards Jack. The sentence 'You’re sending Jack with me?' (BOOK_003_6) is coded as protective commitment (H4_5a) as it shows responsibility for Jack's actions without an external threat. The topic is mixed as no single code exceeds 70%.
- **C adjudicate:** `H4_5`
  - The topic resolves around promises of physical protection, with an external threat implied, fitting H4_5.
- **Action:** KEEP

---

## Topic 69 — Visions and Nightmare Warnings

- **Taxonomy:** 10.1 — Paranormal & Immortal Beings
- **Code:** H4_5 (norm: H4_5)

> i want you to check with all the gargoyles to see if they’ve been having any…urr…strange...dreams.”

> i’ve seen this man and his friends in my visions,” i said. “

> i’ve had so many nightmares about it, and him in particular, that i wouldn’t know what was real and what was my imagination anymore.

> *(BOOK_003, CELL_A, tertile=begin)* I pretend as if the nightmares that haunt my sleep don’t exist. “

> *(BOOK_003, CELL_A, tertile=begin)* Wondering how I’m ever going to go back to sleep after that dream, I hear Reed say, “That bad, huh?”

> *(BOOK_003, CELL_A, tertile=middle)* It occurs to me that this is just like the first dreams I began having right after I found out what Alfred had done to my uncle.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'nightmares', 'threats', and 'chased' suggest an external threat, while 'promises' and 'secured' indicate protective commitment. The topic does not restrict autonomy.
- **B contextual:** `H4_1`
  - Most sentences discuss dreams and nightmares, indicating a focus on emotional states rather than external threats. The use of 'your dream will be fulfilled' and 'dream to feel your skin against mine' suggests reassurance and tenderness, fitting H4_1. Sentences like 'This nightmare had to end' and 'Nightmares' indicate a desire to protect from negative emotional states, fitting H4_5a.
- **C adjudicate:** `H4_5`
  - The topic revolves around external physical protection, with the character pledging to protect their partner from paranormal threats, fulfilling the criteria for H4_5.
- **Action:** KEEP

---

## Topic 73 — Quick Remarks Before Moving on

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** H4_0 (norm: H4_0)

> hell, yeah, i’ll just pretend [person] is runnin’ after me to give me a kiss.”

> he’ll be dead before we get there,” [person] hisses, “yeah.

> we’ll try to be quick,” vincent says as he looks around at the group and then finally at michael. “

> *(BOOK_001, CELL_B, tertile=begin)* Mike looked surprised. "

> *(BOOK_001, CELL_B, tertile=begin)* Mike instantly paled. "

> *(BOOK_002, CELL_B, tertile=end)* She spoke to Michael. “

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'looked', 'nods', 'glances', 'winked', 'comments', 'identity', 'hopeful', 'admire' suggest a protective commitment from the characters towards each other, without any external threat or partner restriction.
- **B contextual:** `H4_0`
  - Most sentences are neutral (H4_0) as they simply mention or address Mike/Michael. Some sentences show possessive claiming (H4_7) but there's no external threat or protective commitment, and no coercive control is present.
- **C adjudicate:** `H4_5a`
  - The topic's dominant code is H4_0 (off_target), but the lexical consensus is H4_5a (protective commitment). The topic discusses promises and vows, which align with the taxonomy of 9.2 Promise, Vow & Future-Tense Speech Acts. Therefore, it's appropriate to keep the topic and assign it the care_protection_code H4_5a.
- **Action:** KEEP

---

## Topic 78 — Swearing War Before He Takes Her

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_0 (norm: H4_0)

> i’ll fight you off.” “

> and if they do, you’ll fight them.

> i’ll start a war before i let him have you,” he murmured.

> *(CELL_D, tertile=middle)* Well, if the other man thought he was about to give him a fight over Sabina, he was wrong; Sabina was an independent woman of twenty-five, not a possession for two men to fight over as if she were the prize! ‘

> *(CELL_A, tertile=begin)* I don’t want to fight, but you’ve left me with no other choice.”

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'fight', 'fighting', 'war', 'battle', 'fought', 'attacked', 'weapons' indicate external physical protection (H4_5).
- **B contextual:** `H4_0`
  - Most sentences express a desire to avoid fighting or arguing, which is coded as H4_0 (off_target). Some sentences mention fighting, but without a clear external threat, they are also coded as H4_0. A few sentences imply possessive claiming (H4_7), but they are not the majority.
- **C adjudicate:** `H4_5`
  - The topic discusses external physical protection, with an external threat evidenced.
- **Action:** KEEP

---

## Topic 82 — Touch Her and Your Family Suffers

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_7 (norm: H4_7)

> that you’ll die if i didn’t touch you?

> one touch and you’ll never know lonely again .

> oh, i’ll touch her alright and you both will do as i say or your family will suffer.

> *(CELL_D, tertile=middle)* I’m careful to avoid her touch for fear it will set me ablaze.”

> *(CELL_D, tertile=end)* And tell those other girls that if they don’t keep their distance, I will scratch their faces.” “

> *(CELL_D, tertile=end)* I wish I could say it was touching and moving, but I hate funerals.

### Pass A/B/C

- **A lexical:** `H4_7`
  - The keywords 'touch', 'touched', 'suck', 'want', 'you', 'dick', 'pussy', 'cock' suggest possessive claiming (H4_7) as they imply sexual ownership or desire for control over the partner's body. The words 'begged', 'warned', 'hurt' from KeyBERT and MMR lists further emphasize this, showing a push for control or dominance in the sexual context.
- **B contextual:** `H4_0|MIXED`
  - The dominant code is H4_0 (off_target) as most sentences do not explicitly express care, protection, or commitment. H4_4 (emotional_support) appears in a few sentences, and H4_7 (possessive_claiming) is present in some possessive statements. H4_5a (protective_commitment) appears in one sentence, and H4_9 (coercive_control) is present in one threatening statement. However, these do not dominate the topic.
- **C adjudicate:** `H4_7`
  - The contextual dominant code H4_0 (off_target) indicates that the topic does not fit well under the provided taxonomy. However, the lexical consensus code H4_7 (possessive_claiming) is a better fit for the topic's content, which revolves around possessive behaviors and claims in a romantic context. Therefore, the topic should be renamed to better reflect its content.
- **Action:** RENAME

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

## Topic 96 — Confessing Long-Standing Worry

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> i’ve been worried about you, [person].

> i’ve worried about you since i was twelve.

> i’ve been worried about you.” “

> *(CELL_D, tertile=middle)* You grew up worrying about having your basic needs met.

> *(CELL_D, tertile=middle)* Don't beat yourself up about it.

> *(CELL_B, tertile=begin)* We didn’t want to worry you.”

### Pass A/B/C

- **A lexical:** `H4_4`
  - The keywords 'worry', 'worried', 'concern', 'bother', 'fears', 'problems' indicate emotional distress, while 'assure' suggests emotional support. There's no external or partner threat mentioned, and the topic doesn't restrict or support autonomy.
- **B contextual:** `H4_1`
  - The dominant code is H4_1 (reassurance_tenderness) as most sentences express concern or reassurance, with no external or partner threat present. There's no possessive claiming or coercive control language.
- **C adjudicate:** `H4_1`
  - The topic's dominant code is H4_1, indicating reassurance and tenderness, which aligns with the taxonomy of Emotional Safety, Reassurance & Caretaking.
- **Action:** KEEP

---

## Topic 100 — Promising to Find Her

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** H4_0 (norm: H4_0)

> i promise, i’ll bring her right back.”

> i’ll hurry and see if i can catch her.”

> i’ll look until she’s found.”

> *(CELL_A, tertile=end)* She won’t be able to leave, to rest, to pass over, whatever it is, until we find her.” “

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'find', 'meet', 'needs', 'can', 'here' suggest a protective commitment without an external threat.
- **B contextual:** `H4_5a`
  - The dominant code is H4_5a (protective commitment) as the sentences primarily express determination to find or protect someone without any external threat mentioned. There's no possessive claiming language used, and the threat source is unclear or nonexistent.
- **C adjudicate:** `H4_5a`
  - The topic revolves around promises and vows of protection, which aligns with the 'protective commitment' construct under the 'Promise, Vow & Future-Tense Speech Acts' taxonomy. There's no evidence of an external threat, so H4_5a is the appropriate code.
- **Action:** KEEP

---

## Topic 102 — Grief Etched on His Face

- **Taxonomy:** 3.2 — Negative Emotions & Distress
- **Code:** H4_0 (norm: H4_0)

> we’ve lost adam,’ she whispered and her fingers traced the contours of grief still etched on his face. ‘

> not only did she have a cool and savvy partner actually in the game with her, the surroundings, the actions were so real that her heart pounded and adrenaline flooded her, almost as if she really was helping adam sabotage a bridge while avoiding capture by nazi soldiers.

> holy hell, adam—i’ve known her long enough to realize she’s thinking about a lot more than a blowjob.” “

> *(CELL_B, tertile=end)* And on that thought, he said, “I talked to Adam a minute ago.

### Pass A/B/C

- **A lexical:** `H4_1`
  - The keywords 'affection', 'emotional', 'stares', and 'secretly' suggest tender and reassuring interactions, indicating 'reassurance_tenderness' (H4_1). There are no cues suggesting external threats or possessive/coercive behaviors.
- **B contextual:** `H4_5a`
  - Most sentences show protective commitment (H4_5a) as characters express care, ask questions, or show concern for each other. No external or partner threat is present, and there's no possessive claiming language.
- **C adjudicate:** `H4_5a`
  - The topic's dominant code is H4_5a, indicating protective commitment, as the character expresses responsibility for the partner's safety and well-being without an external threat being evidenced. The topic's taxonomy is 3.2 Negative Emotions & Distress, suggesting that the protective commitment is not excessive or coercive, thus fitting the H4_5a code.
- **Action:** KEEP

---

## Topic 107 — Gritted Teeth and Clenched Fists

- **Taxonomy:** 1.1 — Body Parts & Physical Reactions
- **Code:** H4_0 (norm: H4_0)

> christian gritted just hoping billy’d have the balls to start the fight for once ‘stead of just running his flapper. “

> chapter fourteen cerne gritted his teeth and clenched his fists.

> he gritted out. "

> *(BOOK_001, CELL_D, tertile=end)* I feel on the verge of snapping,” she declared, and made a growling sound. “

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'growl', 'clenched', 'tightened', 'tensed', and 'his' suggest physical tension and external protection, as the character is preparing for or reacting to an external threat.
- **B contextual:** `H4_13`
  - All sentences describe physical reactions (clenching jaw, groaning) without any context of external protection, protective commitment, possessive claiming, or coercive control.
- **C adjudicate:** `H4_5`
  - The topic discusses physical protection from external threats, which aligns with H4_5. There's no evidence of an internal threat or possessive behavior, so H4_5a, H4_7, or H4_9 are not applicable.
- **Action:** KEEP

---

## Topic 117 — Blamed and Threatened Into Compliance

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_1 (norm: H4_1)

> i feel like it’s all my fault.” “

> but you’ll only have yourself to blame if i get picked up.

> all this is your fault and if you don’t do exactly what i tell you…well, you know what’ll happen.”

> *(BOOK_004, CELL_D, tertile=begin)* Not your fault -- and, trust me, hang around long enough and there will be a trail of broken dates with me due to overtime, cases getting hot, or being called away in the middle of the night because some crackhead thinks he can get off a carrying charge in exchange for telling me something."

> *(BOOK_005, CELL_B, tertile=begin)* Would it make it any better if I went and told him it was my fault?”

> *(BOOK_005, CELL_B, tertile=end)* It wasn’t his problem or his fault, because he’d done nothing wrong.

> *(BOOK_005, CELL_B, tertile=middle)* After all, it was my fault I was too ass-over-end drunk to drive in the first place.”

### Pass A/B/C

- **A lexical:** `H4_11`
  - The keyword lists repeatedly mention 'fault', 'blamed', 'harshly', and 'wound', indicating a partner's blame and harsh treatment, which restricts the protagonist's autonomy.
- **B contextual:** `H4_1`
  - Most sentences express reassurance and emotional support (H4_1), with a few instances of possessive claiming (H4_7) and unclear or mixed codes (H4_13). No external or partner threats are present, and there's no claiming language used.
- **C adjudicate:** `H4_1`
  - The topic's dominant code is H4_1, indicating reassurance and tenderness, which aligns with the contextual dominant code. The lexical consensus code H4_11, 'for your own good control', is not dominant and does not require a change in the care_protection_code.
- **Action:** RENAME

---

## Topic 119 — Offering to Keep Her Safe

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_5 (norm: H4_5)

> come on, i’ll protect you.”

> you’ll protect me?” “

> i can protect you from crystal, but you’ll have to let me.

> *(CELL_D, tertile=begin)* I’m your man for getting you to the point of passing out, if you ever want to take that risk.”

> *(CELL_C, tertile=middle)* At least in LA you’d both have protection; you know my security guys are some of the best in the business.

> *(CELL_C, tertile=end)* I didn’t think security would leave you standing out here like this.’ ‘

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'protect', 'protection', 'dangerous', 'threat', 'secure', 'guard' indicate external protection (H4_5) as the dominant theme. There's no mention of possessive claiming or coercive control, and the protection seems to support autonomy rather than restrict it.
- **B contextual:** `H4_5a`
  - All sentences express protective commitment without an external threat, hence H4_5a.
- **C adjudicate:** `H4_5a`
  - The topic discusses the character's commitment to protecting their partner, with no external threat mentioned, fitting H4_5a.
- **Action:** KEEP

---

## Topic 121 — Revealing Plans to The Prince

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** H4_6 (norm: H4_6)

> she’ll be queen of the roost.” “

> do you think he’ll really go to the king?”

> if i let the prince know what is happening, instead of waiting for them to find out, they’ll know i’ve been out on my own.

> *(CELL_C, tertile=middle)* I am not Prince Charming or a shining Knight on a white horse.

> *(CELL_C, tertile=middle)* Hot as a fever, rattling bones I could just taste it, taste it If it’s not forever, if it’s just tonight Oh it’s still the greatest, the greatest, the greatest Kings of Leon Chapter Ten “You two pieces of shit are worthless you know that?”

> *(CELL_C, tertile=end)* I WILL one day go on a vacation to Disneyland and actually hang with Belle, Beast, Briar, Winter and Ashess.

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The Main and MMR lists mention 'king', 'prince', 'queen', and 'regent', suggesting a hierarchical structure where the characters have responsibilities and make decisions ('promises', 'decision'). The KeyBERT and POS lists emphasize reassurance ('reassuring', 'assured'), which aligns with protective commitment (H4_5a). There's no external threat mentioned, so the threat source is 'none'. The protective commitment supports autonomy as it's about fulfilling responsibilities, not restricting actions.
- **B contextual:** `H4_6`
  - The dominant code is H4_6 (external protection_social_legal) as many sentences mention the king's involvement or protection. H4_2 (practical_care) is also prominent, with the queen giving orders. H4_7 (possessive_claiming) appears once, and H4_9 (coercive_control) appears once in a context of torture. The rest are off-target (H4_0) or mixed.
- **C adjudicate:** `H4_6`
  - The topic revolves around protecting the protagonist's secret identity, which is threatened by external forces, fitting H4_6 (external_protection_social_legal).
- **Action:** KEEP

---

## Topic 122 — Wound Bleeding and Blood Loss

- **Taxonomy:** 1.2 — Pain, Injury & Physical Vulnerability
- **Code:** H4_0 (norm: H4_0)

> whenever innocent blood is spilt, it’ll be my father’s blood… and you’ll find me there.

> offer her the meat in the sack from the palm of your hand and she’ll not draw blood.

> i know head wounds bleed a lot, but you want to keep most of your blood inside your body where it’ll do you some good.

> *(BOOK_004, CELL_A, tertile=end)* The blood would only serve to make the ropes more slippery if she could loosen them enough to pull a hand free.

> *(BOOK_004, CELL_A, tertile=end)* Too much blood, its bitter copper scent filling her head, overloading her senses.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'blood', 'bleeding', 'bleed', 'veins', 'lost', 'drinking', 'everywhere', 'lot', 'need', 'your' suggest a physical injury or harm, indicating an external threat. The use of 'need' and 'your' also suggests a protective or caring context, fitting H4_5 (external protection, physical).
- **B contextual:** `H4_0`
  - The dominant code is H4_0 (off_target) as most sentences do not explicitly mention any form of protection, care, or control. The presence of blood is merely descriptive and does not indicate any specific protective or possessive action. H4_5 (external_protection_physical) is present in some sentences, but not dominant. H4_5a (protective_commitment) appears once, and H4_6 (external_protection_social_legal) appears once as well. There is no possessive claiming or coercive control language present.
- **C adjudicate:** `H4_5`
  - The lexical consensus and contextual dominant both point to external physical protection, which is supported by the taxonomy. The topic discusses protecting the protagonist from physical harm caused by external threats.
- **Action:** KEEP

---

## Topic 128 — Confessing How Much You've Missed

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** H4_1 (norm: H4_1)

> i’ve missed most of his life already.

> and, god, how i’ve missed this.”

> i’ve come to realize that you are the one thing in my life i don’t want to miss.

> *(CELL_C, tertile=middle)* The suckhead you brought back with you here tonight…I saw it all.”

> *(CELL_C, tertile=end)* While I was in there, I also brought you something I thought you might be missing.”

### Pass A/B/C

- **A lexical:** `H4_1`
  - The keywords 'miss', 'misses', 'missing', 'much', 'you', 'too' suggest a longing or yearning for someone, indicating reassurance and tenderness (H4_1). There are no external or partner threats mentioned, and the sentiment supports the partner's autonomy.
- **B contextual:** `H4_1`
  - All sentences express missing someone, indicating reassurance and tenderness (H4_1), with no external or partner threat, and no possessive or coercive language.
- **C adjudicate:** `H4_1`
  - The topic revolves around expressions of love, comfort, and reassurance, which align with the 'reassurance_tenderness' code (H4_1). There's no evidence of external threats or coercive control.
- **Action:** KEEP

---

## Topic 148 — Banished From The Ranch

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_0 (norm: H4_0)

> if he gets off on a technicality, we’ll let jesse kill him.

> just promise you’ll take time to consider visiting tyler once in a while.” “

> you’re never to set foot on tyler land again, and if i catch you anywhere near my horses, i’ll whip you within an inch of your life.”

> *(BOOK_002, CELL_B, tertile=end)* Gray wanted to tell her to have some faith, but who was he to talk?

> *(BOOK_002, CELL_B, tertile=end)* Two years earlier, or maybe even as recently as a couple of weeks before, Gray might have responded with a threat, or by telling Mariah’s father exactly what he thought of parents who put themselves first, always.

> *(BOOK_002, CELL_B, tertile=end)* Gray rapped out the summary, making it clear that what happened next wasn’t open to discussion.

> *(BOOK_002, CELL_B, tertile=end)* In the process of trying to save the world from the terrorists’ threat and gain justice for Ken and his family, Gray had lost sight of some of the other people involved.

> *(BOOK_002, CELL_B, tertile=begin)* The SAC would be furious that Gray had disobeyed orders, but he’d be forced to send a team up to the cabin.

> *(BOOK_004, CELL_A, tertile=end)* Ohhhhhhhhhhhhhhh, Jessssssssssssssssssssssssiiiiiiiiiiiicccaaaaaaaaaaaaa!”

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'knew', 'said', 'actions', 'instructed' suggest a protective commitment from the characters without an external threat.
- **B contextual:** `H4_13`
  - Most sentences are ambiguous or lack clear context for specific codes, hence marked as mixed (H4_13). Some sentences imply possessive claiming (H4_7) but lack external threat or clear commitment. One sentence (BOOK_002_2) hints at coercive control (H4_9) with a threat of action from the character's past.
- **C adjudicate:** `H4_5a`
  - The topic's dominant code is mixed (H4_13), but the lexical consensus is H4_5a, indicating a protective commitment. There's no evidence of an external threat, so H4_5a is the most appropriate code. The topic should be reinterpreted to reflect this.
- **Action:** REINTERPRET

---

## Topic 157 — Swearing to Save Him From Himself

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** H4_1 (norm: H4_1)

> and you’ll get it, i swear,” [person].

> if [person] sees me like this, i'll die."

> and i might be young but i guess that just makes me lucky… i do love him and whether i have your help or not, i have to save him from himself… i know [person], i know what he’ll do, now that he thinks he has lost me.”

> *(CELL_B, tertile=middle)* Sam couldn’t understand it, and that bothered him.

> *(CELL_B, tertile=begin)* What else had Sam witnessed?

> *(CELL_B, tertile=begin)* Sam noticed stuff like that.

### Pass A/B/C

- **A lexical:** `H4_1`
  - The keywords 'good', 'optimism', 'willing', 'enthusiasm' suggest reassurance and tenderness, indicating protective commitment (H4_1). There's no external threat or partner restriction, so threat_source is 'none' and autonomy_effect is 'supports'.
- **B contextual:** `H4_0`
  - Most sentences are calls or mentions of the character's name, Sam, which do not indicate any form of protection, commitment, claiming, or control. The sentence 'Sam knows him' suggests protective commitment, but it's not dominant. The sentence 'Sam was pretty softhearted' indicates practical care. The sentences starting with 'I'm sorry, Sam' show emotional support. There's no external threat or possessive claiming, so the threat source is 'none'. There's no language indicating possessive claiming.
- **C adjudicate:** `H4_1`
  - The topic discusses tender and reassuring moments between characters, which aligns with the 'reassurance_tenderness' code (H4_1). There's no evidence of external threats or possessive/coercive behaviors, so other codes like H4_5, H4_5a, H4_7, or H4_9 are not applicable.
- **Action:** KEEP

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
- **Code:** H4_5 (norm: H4_5)

> you’ll also report this to your regional security officer, yes?”

> i’ll have an armed officer [person] the room with you at all times, and i’ll watch through the glass.” “

> i’ve called the police, i’ll have you know.”

> *(CELL_B, tertile=end)* Do you think being worried over another officer’s absence justifies a breach in regulations?”

> *(CELL_B, tertile=end)* I give an order, and because I’m your superior officer, you are supposed to obey it.” “

### Pass A/B/C

- **A lexical:** `H4_5`
  - The Main, KeyBERT, POS, and MMR keywords all revolve around protection and law enforcement, indicating external protection (H4_5). There's no mention of a partner as a threat or control, so the threat source is external. The topic doesn't restrict or support autonomy, making the autonomy effect neutral.
- **B contextual:** `H4_5`
  - The dominant code is H4_5 (external protection physical) as the sentences primarily discuss calling the police, indicating a physical threat. H4_5a (protective commitment) is used once when the character tells the police what they were told to say, showing commitment to protecting someone. H4_1 (reassurance tenderness) is used once when a character says there's no reason to call the police, trying to reassure. H4_9 (coercive control) is used when a superior officer tries to control a subordinate, and H4_7 (possessive claiming) is used once when a character asks about a cop boyfriend. The threat source is external as the police are called due to external threats. There's no claiming language used in these sentences.
- **C adjudicate:** `H4_5`
  - The topic discusses physical protection from external threats, aligning with H4_5.
- **Action:** KEEP

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

## Topic 181 — Handing Off to Someone Else

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** H4_0 (norm: H4_0)

> i’ll leave it to [person] to continue again now”. “

> i’ll get [person] to approve the field trip.” “

> and i’ll be frank.

> *(BOOK_004, CELL_B, tertile=middle)* Finally Fran had him cut off, long before he was really drunk, and when he complained she just told him it was a longwalk home for himondark roads, ifhe got obnoxious about it.

> *(BOOK_006, CELL_B, tertile=end)* The thought of Frank coming to the house when I wasn’t there alarmed me.

### Pass A/B/C

- **A lexical:** `H4_7`
  - The Main and KeyBERT keywords ('wife', 'come', 'quickly') suggest possessive claiming, as does the MMR keyword 'stalked'. The POS keywords like 'affection' and 'behavior' support this, as they could indicate possessive behavior. The threat source is the partner, and the autonomy effect is restriction, as possessive claiming can limit the partner's autonomy.
- **B contextual:** `H4_13`
  - Most sentences are mixed or unclear (H4_13), with a few instances of protective commitment (H4_5a), external protection (H4_6), possessive claiming (H4_7), and emotional support (H4_4). No external threats or coercive control are present.
- **C adjudicate:** `H4_7`
  - The topic's dominant code is H4_13, indicating mixed or unclear signals, but the lexical consensus is H4_7, which is possessive claiming. This suggests that while there are mixed signals, the possessive claiming aspect is prominent and should be the primary care/protection code.
- **Action:** RENAME

---

## Topic 223 — Coordinating Security Against A Threat

- **Taxonomy:** 7.3 — Risk, Danger & External Crises
- **Code:** H4_0 (norm: H4_0)

> i’ll give aidan a call, so he doesn’t send out the cavalry.”

> there’ll be extra men on the gate,” [person] promised. “

> but we have a gut feeling that since [person]’s been such a thorn in the side of these people, if they think they’re going to get him, he’ll pull in the other accomplices.

> *(CELL_A, tertile=end)* Maybe if I go with Matt it will teach him not to take me for granted,” Alice said. “

> *(CELL_A, tertile=middle)* With time running short, the girls chalked Paddy and then left Cameron to do the clipping on his own while they brought Belladonna in from the field. “

> *(CELL_A, tertile=begin)* Lexington House had most of the Western boys and Matt Garrett, an Australian eventer who could be annoyingly full of himself.

### Pass A/B/C

- **A lexical:** `H4_7`
  - Keywords like 'matt', 'matty', 'mattie', 'connor', 'aidan', 'stephon' suggest possessive claiming. 'Partners' and 'options' imply a focus on relationships, while 'insisted', 'inevitable', and 'claims' indicate a strong, potentially possessive stance.
- **B contextual:** `H4_0`
  - Most sentences are off-target (H4_0) as they do not explicitly discuss protection, care, or commitment. The two sentences coded as protective commitment (H4_5a) show Alice's intention to teach Matt a lesson, not necessarily to protect him. The sentence coded as possessive claiming (H4_7) shows Alice using Matt as a pawn in her game, not claiming him possessively. There is no external or partner threat mentioned, and no claiming language is used.
- **C adjudicate:** `H4_7`
  - The lexical consensus and contextual dominant codes both point to possessive claiming, as the text discusses a character's desire to assert ownership over another. There's no evidence of an external threat, so H4_5 or H4_6 don't apply, and H4_5a is not appropriate as there's no safety or welfare pledge.
- **Action:** KEEP

---

## Topic 236 — Caught Spying By The Fbi

- **Taxonomy:** 10.3 — Mystery, Suspense & Investigation
- **Code:** H4_5 (norm: H4_5)

> like i’ve caught you spying.

> he suspected he would've been released earlier in the day if not for the fbi.

> you’ve been spying on me all that time?” “

> *(BOOK_001, CELL_D, tertile=begin)* He was a closer, a realist, and the reason I'd created the department in the first place. "

> *(BOOK_002, CELL_A, tertile=middle)* If the CIA has nothing on him, I just look like a crazy person out for revenge.” “

> *(BOOK_002, CELL_A, tertile=middle)* Have them do a search—we’ll stay here and try to get more of a read on our informant.” “

> *(BOOK_003, CELL_B, tertile=end)* Well, I suppose I do have some investigative skills of my own.”

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'fbi', 'agent', 'investigation', 'spy', 'detective', 'spying', 'undercover', 'agents', 'investigator', 'agency' suggest external protection, specifically physical, as the main theme of this topic. The other keyword lists ('KeyBERT', 'POS', 'MMR') also support this interpretation with words like 'capture', 'evidence', and 'escaped', indicating a scenario where external protection is necessary.
- **B contextual:** `H4_5a`
  - Most sentences discuss investigative actions or roles, with no external or partner threat mentioned, fitting 'protective commitment' (H4_5a).
- **C adjudicate:** `H4_5`
  - The dominant code H4_5a (protective commitment) is resolved to H4_5 (external protection physical) as there is an external threat mentioned in the context, fitting the taxonomy of Mystery, Suspense & Investigation and Risk, Danger & External Crises.
- **Action:** KEEP

---

## Topic 238 — Relaying A Message For Her

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** H4_4 (norm: H4_4)

> yeah, i’ll tell her,” i reply, the sudden mood change taking me by surprise. “

> i’ll go tell her.”

> well, maybe you’ll get another chance to tell her.”

> *(BOOK_001, CELL_B, tertile=middle)* But she won’t tell you what, specifically, it goes to show, unless you ask. “

> *(BOOK_002, CELL_D, tertile=begin)* If I’d known that, I wouldn’t have done so much around here,” she teased.

> *(BOOK_002, CELL_D, tertile=middle)* She said she was actually glad when the lie between her and Grandpa was over.

### Pass A/B/C

- **A lexical:** `H4_4`
  - The keywords 'tell', 'told', 'talk', 'knows', 'happened', and 'wish' suggest a desire for emotional support and understanding, which is reflected in the 'emotional_support' code (H4_4). The keyword 'promises' in KeyBERT and 'behavior' in POS and MMR suggest a commitment to maintaining a certain standard, which aligns with 'protective_commitment' (H4_5a). However, there are no cues indicating an external threat, so the consensus code is 'emotional_support' (H4_4).
- **B contextual:** `H4_13`
  - Most sentences involve withholding or revealing information, which is unclear or mixed in nature. One sentence ('I should've told them you were mine from the beginning') indicates possessive claiming.
- **C adjudicate:** `H4_4`
  - The topic's lexical consensus of H4_4 (emotional_support) aligns with the contextual dominant of H4_13 (mixed/unclear), indicating a balance of care and protection themes. The taxonomy of 'Promise, Vow & Future-Tense Speech Acts' supports this interpretation, as the topic discusses emotional support in the context of future commitments.
- **Action:** KEEP

---

## Topic 239 — Keeping Someone Guarded and Entertained

- **Taxonomy:** 5.2 — Friends, Allies & Social Circles
- **Code:** H4_0 (norm: H4_0)

> i’ve always marveled at the artwork in that book, [person].

> if trent wanted him to know the story, he would’ve told him. “

> between the three of us, we’ll keep [person] guarded and entertained.”

> *(BOOK_001, CELL_D, tertile=middle)* He’d renewed several advantageous acquaintances, particularly that of Lord Grey.

> *(BOOK_001, CELL_D, tertile=begin)* I say, he’s an ambitious sort of fellow and he’d be looking for an earl’s daughter at the very least.

> *(BOOK_003, CELL_C, tertile=begin)* His best friend Gareth ran the mine and took care of the men while he was away.

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'misjudged', 'denied', 'assume', 'embarrassment', 'disappointment', 'unlikely', 'painful' suggest a situation where the characters are taking responsibility for their actions or feelings, without an external threat. This is indicative of protective commitment (H4_5a).
- **B contextual:** `H4_13`
  - Most sentences are neutral or unclear, with no specific protection, care, or commitment mentioned. The sentence 'Austin couldn’t show up uninvited either, as tempting as that might be.' (BOOK_005_5) hints at protective commitment without an external threat, hence H4_5a.
- **C adjudicate:** `H4_5a`
  - The topic's dominant code is mixed (H4_13), but the lexical consensus (H4_5a) indicates a clear protective commitment. This is supported by the taxonomy's secondary category of 'Emotional Safety, Reassurance & Caretaking'. Therefore, the topic should be renamed to reflect this protective commitment.
- **Action:** RENAME

---

## Topic 240 — Unsure How to Offer Comfort

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> oh my god, sean!

> sean pursed his lips, unsure he was equal to the task of comforting [person].

> sean held out his hand and added; “now if you’ll excuse me i have a beautiful woman waiting to have breakfast with me.”

> *(CELL_B, tertile=begin)* Oh,” I said, thinking fast, watching as Seth started to show Liam how to use another nearby machine, while the Tiffanys and Brittanys gathered round, looking more worshipful than ever.

> *(CELL_B, tertile=end)* You need to stop nipping at him and face the fact that when Shon goes under, he’s off limits, one breath away from being a hostile at our backs.” “

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'answered', 'looked', 'said', 'mumbled', 'willing', 'shivered', 'assume', 'anxious', 'stares', 'conscious', 'distracted' suggest a scenario where characters are showing protective commitment (H4_5a) towards each other, without any external threat.
- **B contextual:** `H4_13`
  - Most sentences are unclear or off-topic (H4_13), with no specific care, protection, or commitment mentioned. The sentence 'You need to stop nipping at him and face the fact that when Shon goes under, he’s off limits, one breath away from being a hostile at our backs.' (BOOK_003_2) indicates coercive control (H4_9), but it's the only instance. The sentences mentioning names repeatedly (BOOK_005_1 to BOOK_005_6) suggest possessive claiming (H4_7), but they are not the majority.
- **C adjudicate:** `H4_5a`
  - The topic's dominant code is mixed (H4_13), but the lexical consensus is clear (H4_5a). The topic primarily revolves around emotional safety and reassurance, with no external threat mentioned. Therefore, it's resolved to H4_5a.
- **Action:** REINTERPRET

---

## Topic 247 — Promising You Will Not Be Alone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_1 (norm: H4_1)

> if we make it through this alone, we’ll just be better at being alone.”

> you’ll never be alone.

> before you say no, i want you to know i’ll be alone mostly.

> *(CELL_B, tertile=end)* If I went out alone, it seemed I felt surrounded by people who couldn’t speak to me.

> *(CELL_B, tertile=begin)* I promise you, you will never be alone again so long as I live.”

> *(CELL_B, tertile=begin)* I’ve pictured this so many times in my mind, I don’t want to wake up and find I’m alone again.” “

### Pass A/B/C

- **A lexical:** `H4_1`
  - The keywords 'alone', 'solitude', 'prefer', 'chose', 'insisted' suggest the character's preference for being alone, indicating reassurance and tenderness (H4_1) without any external threat or restriction of autonomy.
- **B contextual:** `H4_0`
  - Most sentences express loneliness or being alone, with no external threat or protective commitment mentioned. A few sentences hint at wanting to be alone or not being alone, but they do not specify any external protection or possessive claiming.
- **C adjudicate:** `H4_1`
  - The topic's dominant code is H4_0 (off_target), but the lexical consensus is H4_1 (reassurance_tenderness). The topic primarily revolves around emotional safety and reassurance, with no evidence of external threats or possessive/coercive behaviors. Therefore, it is appropriate to keep the topic and assign it the care_protection_code H4_1.
- **Action:** KEEP

---

## Topic 249 — Threatened With Arrest and Jail

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_6 (norm: H4_6)

> i'll pull you off just before we make the arrest.

> do anything remotely similar to that again, and you’ll find yourself on your way to jail.”

> maybe they’ll come see you in prison, though i doubt it.” “

> *(BOOK_002, CELL_A, tertile=middle)* If they were caught, they would face stiff penalties, including jail time.

> *(BOOK_002, CELL_A, tertile=begin)* He believes the man may have been taken prisoner or murdered by my ex-husband or a member of his personal security.”

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'jail', 'arrested', 'prison', 'bail', 'arrest', 'crime', 'prisoner', 'criminal', 'prisoners', 'parole' indicate external threats to the character's freedom and safety, thus triggering H4_5 (external_protection_physical).
- **B contextual:** `H4_6`
  - The dominant code is H4_6 (external_protection_social_legal) as many sentences discuss legal actions, prison, and penalties. H4_9 (coercive_control) is also present, indicating attempts to restrict the partner's actions. H4_1 (reassurance_tenderness) and H4_5a (protective_commitment) are present but less frequent.
- **C adjudicate:** `H4_6`
  - The topic discusses the protagonist's actions to protect their partner from external social and legal threats, fitting the H4_6 code.
- **Action:** KEEP

---

## Topic 258 — Shouting Above The Crowd

- **Taxonomy:** 9.1 — Dialogue Delivery & Speech Tags
- **Code:** H4_1 (norm: H4_1)

> christine shouted after him.

> show me she’s safe,” she shouted. “

> she shouted in excitement the way she had before, but this time, she barely heard herself, everything except for her connection to him seemed like background noise.

> *(BOOK_001, CELL_A, tertile=begin)* He wanted to pound inside her and hear her scream for more.

> *(BOOK_002, CELL_B, tertile=begin)* She yelled, too, though she knew they could not hear her.

> *(BOOK_001, CELL_A, tertile=middle)* He pulled back and she almost screamed.

### Pass A/B/C

- **A lexical:** `H4_9`
  - The keywords 'screamed', 'yelled', 'shouted', 'screaming', 'shrieked', 'noise', 'heard' indicate a partner's loud and aggressive behavior, which is coercive and restricts the other person's autonomy.
- **B contextual:** `H4_1`
  - The dominant code is H4_1 (reassurance_tenderness) as most sentences involve screaming or shouting, which can be seen as an expression of strong emotion or distress. There is no external threat mentioned, so the threat source is 'none'. There is no possessive claiming language used, so claiming_language is false.
- **C adjudicate:** `H4_1`
  - The topic discusses reassuring and tender interactions between characters, which aligns with H4_1. There's no evidence of external threats, so H4_5 or H4_6 are not applicable. H4_5a is not suitable as there's no responsibility pledge without an external threat.
- **Action:** KEEP

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
- **Code:** H4_5a (norm: H4_5a)

> i’ll talk to the lawyer tomorrow.

> we’ll find a good lawyer to help.

> you can count on me to deal with the legal trouble they’ll cause.”

> *(CELL_D, tertile=end)* Mediation has never come easily for me and I need all the help I can get.

> *(CELL_B, tertile=end)* Such a lot of fuss over a piece of real estate that was destined by federal law to go unclaimed by anyone.

> *(CELL_B, tertile=end)* It’s important to establish legal boundaries of ownership, especially when you’re talking about gems and precious metals.

### Pass A/B/C

- **A lexical:** `H4_6`
  - The keywords 'lawyer', 'attorney', 'legal', 'firm', 'counsel', 'advice' suggest a need for external protection in a social/legal context. 'Worried', 'worrying', 'cost', 'afford' imply external threats, while 'impatiently', 'expect' suggest a process in progress, not restricting autonomy.
- **B contextual:** `H4_5a`
  - The dominant code is H4_5a (protective commitment) as most sentences refer to the character being a lawyer or lawman, indicating a commitment to protect without an external threat. There's no possessive claiming or coercive control language, and the threat source is unclear or nonexistent.
- **C adjudicate:** `H4_5a`
  - The topic discusses the character's commitment to protect their partner without any external threat mentioned, hence it's classified as 'protective commitment' (H4_5a).
- **Action:** RENAME

---

## Topic 282 — Struggling to Surrender Control

- **Taxonomy:** 3.3 — Ambivalence & Internal Conflict
- **Code:** H4_9 (norm: H4_9)

> trusting someone meant allowing herself to be vulnerable to them, letting them into the inner sanctum of her most private emotional places—places she had kept guarded for so long… it was time she got up, instead of allowing her thoughts to roam such dangerous byways. ‘

> her father is accustomed to calling the shots and didn't make things easy for her in the beginning, but now she's earned his trust and confidence.

> despite that logic and the fact that he’d done everything he could think of to ensure her safety within the dangerous circumstances surrounding her, he couldn’t outrun the growing certainty that he was playing it wrong, taking advantage of someone who deserved better, who shouldn’t be part of his world.

> *(BOOK_001, CELL_B, tertile=middle)* Right then she would have given everything she possessed to have been able to tell him she loved him, that he could trust her, but it wasn’t possible.

> *(BOOK_001, CELL_B, tertile=middle)* She had been right to suspect there was a woman behind Joel’s attitude, but she could never have suspected this. ‘

> *(BOOK_001, CELL_B, tertile=begin)* To have an affair with Joel would no doubt be an incredible experience, but it would break her own rules, because if he were to be believed—and she had no reason to doubt him—there was no future in it.

> *(BOOK_001, CELL_B, tertile=middle)* Only with women who can’t be trusted to do what’s in their own best interests,’ he responded as he pushed through the kitchen door.

> *(BOOK_001, CELL_B, tertile=middle)* It was strange reasoning for a man who had implied his faith in women was scant because they only saw him as a money machine.

### Pass A/B/C

- **A lexical:** `H4_4`
  - The keywords 'trust', 'trusted', 'trusting', 'assured', 'promises' indicate emotional support and reassurance, suggesting H4_4 emotional_support.
- **B contextual:** `H4_9`
  - The dominant code is H4_9 (coercive control) as many sentences revolve around trust issues and suspicion, with partners being the source of threat.
- **C adjudicate:** `H4_9`
  - The topic's dominant code, H4_9 (coercive control), is appropriate given the contextual clues of the romance novel. The character's behavior exhibits patterns of isolation, intimidation, and restriction of their partner's autonomy, which aligns with the definition of coercive control. The lexical consensus code, H4_4 (emotional support), is not the dominant theme in this context and does not accurately represent the core dynamics of the relationship.
- **Action:** REINTERPRET

---

## Topic 299 — Pledging to Have Your Back

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_5a (norm: H4_5a)

> before she’s completely out i ask, “[person], you know i’ve always got your back, right?”

> but i’ve seen you, seen who you are, watched you handle uncle charlie.

> i’ve got a little time before charlie finishes my bike.

> *(CELL_A, tertile=middle)* Kevin was worried that Scott’s death was somehow related to Todd’s return to Birmingham.’

> *(CELL_A, tertile=begin)* They all left for college with big dreams, except Scott and Kevin,’ she said sadly. ‘

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'promises', 'tries', 'willingly' suggest protective commitment without an external threat.
- **B contextual:** `H4_13`
  - Most sentences express concern or uncertainty about a character named Charlie, with no clear external threat or possessive language.
- **C adjudicate:** `H4_5a`
  - The topic discusses the character's commitment to protecting their partner, with no external threat mentioned. This aligns with H4_5a - protective commitment.
- **Action:** KEEP

---

## Topic 307 — Hauling Someone Up The Stairs

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> [person] would hate it if she took a rake like [person] to her bed, and she would so love to rub it in joshua’s face and prove his threats could not restrain her. “

> his thoughts threatened to return to those awful times once again, but thankfully, ash and [person] emerged from the thicket.

> getting ash up the stairs and into the bedroom was a lot harder than it had been last night, mostly because ash was pissed off and conscious instead of in la-la land.

> *(CELL_B, tertile=end)* You and Ashlynn are gonna have to keep him on the straight and narrow."

> *(CELL_B, tertile=end)* He stopped to pat Ashlynn and congratulate her on a large belch. "

> *(CELL_B, tertile=end)* But as he was approaching Clarksburg, Ashlynn chose that moment to be cranky.

> *(CELL_B, tertile=end)* Henry's crankiness had returned, and even sweet Ashlynn was wailing by now.

> *(CELL_B, tertile=end)* Sniffing in disdain, Johnny pushed Ashlynn's stroler over to Grissom. "

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'threats', 'heaved', 'struggled', 'fought', 'urged', 'anxiety', 'panting', 'movements' suggest external physical threats, indicating external protection (H4_5).
- **B contextual:** `H4_0`
  - Most sentences are neutral (H4_0), with a few showing protective commitment (H4_5a) and external protection (H4_6). There's no external threat or possessive claiming language.
- **C adjudicate:** `H4_5`
  - The topic discusses physical protection provided by an external source, such as a character protecting their partner from an external threat.
- **Action:** KEEP

---

## Topic 324 — Searching For A Missing Person

- **Taxonomy:** 7.3 — Risk, Danger & External Crises
- **Code:** H4_5a (norm: H4_5a)

> i’ll go for a drive to look for him.

> i’ll go find him.”

> when we’re done here, we’ll go search his office at marshall, and check his next of kin.

> *(CELL_D, tertile=end)* You could find out if you’d stop hiding away in your house and go see him.”

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'find', 'search', 'locate', 'know', 'did', 'if' from Main, along with 'address', 'hi', 'decide', 'wondering' from KeyBERT, and 'address', 'screen' from POS and MMR, suggest a character's determination to find someone or something, indicating protective commitment without an external threat.
- **B contextual:** `H4_5`
  - The dominant code is H4_5 (external protection, physical) as the sentences primarily express concern about the whereabouts of someone, indicating a physical threat or danger. There's one instance of H4_6 (external protection, social/legal) where the person is at the office, suggesting a social or legal context. There's no possessive claiming or coercive control language present.
- **C adjudicate:** `H4_5a`
  - The dominant code H4_5 (external_protection_physical) is not appropriate as there's no external threat mentioned in the text. The lexical consensus H4_5a (protective_commitment) better represents the character's pledge to protect their partner without an external threat.
- **Action:** RENAME

---

## Topic 329 — Laying Down The Rules

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_0 (norm: H4_0)

> and if you continue to disobey our rules, we’ll erase you.

> if you don’t know the rules already, you’ll be eager to learn after the first tornado season.” “

> we’ll play by my rules.”

> *(BOOK_001, CELL_B, tertile=end)* There are laws that the FirstFamilies must follow, GreatLord.”

> *(BOOK_002, CELL_C, tertile=middle)* And actual y, according to your parity rule, you have to arrange for it.

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The keywords 'rules', 'apply', 'used' suggest protective commitment (H4_5a) without an external threat. 'Those' and 'everyone' imply the rules apply to everyone, not just the protagonist, further supporting H4_5a.
- **B contextual:** `H4_0`
  - The majority of sentences discuss rules, laws, or regulations, which fall under the 'off_target' category (H4_0). A few sentences mention laws that the FirstFamilies must follow (H4_6), and one sentence discusses consequences for not following rules (H4_9). There is no possessive claiming or coercive control language present.
- **C adjudicate:** `H4_5a`
  - The consensus code 'H4_5a' was chosen as it reflects the character's commitment to protecting their partner without an external threat being explicitly stated. The dominant code 'H4_0' was off-target, as it indicates the topic is off the main theme of the study.
- **Action:** RENAME

---

## Topic 335 — Killer Targets Someone Alone

- **Taxonomy:** 7.3 — Risk, Danger & External Crises
- **Code:** H4_0 (norm: H4_0)

> i’ll try,” derek replied and turned to make the hour walk back home.

> i’ll hang around while you take a look at it tonight,” [person] said, his own gaze also glued to camilla’s limbs. “

> he knows that the killer got derek while he was alone, and he wouldn’t do that to his pregnant wife, because she’ll go shit wild and start a rampage.

> *(CELL_B, tertile=begin)* That was when Jenna realized that Lars the Heartless was Baruk’s raider, the one who’d driven them here.

> *(CELL_B, tertile=end)* Baruk could hope that, for his own, good, Lars would accept Stella into his life and make the best of it.

> *(CELL_B, tertile=end)* Lars was leading a party that was looking for Jenna in the woods, and the orcs that had stayed behind were turning every nook and cranny upside down for clues.

### Pass A/B/C

- **A lexical:** `H4_5a`
  - Keywords like 'cultivating', 'promising', 'acknowledged' suggest protective commitment (H4_5a) without an external threat. 'Pregnant' and 'upset' imply emotional support (H4_4) but do not indicate a threat.
- **B contextual:** `H4_0`
  - Most sentences show neutral or reassuring interactions, with no external threat or possessive claiming language.
- **C adjudicate:** `H4_5a`
  - The topic discusses the character's commitment to protect their partner, with no external threat mentioned. This aligns with H4_5a - protective commitment.
- **Action:** REINTERPRET

---

## Topic 338 — Promising Never to Do That Again

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** H4_0 (norm: H4_0)

> but [person], you got to promise me you’ll never do something like that again.

> okay, but i'll warn you — you're making this seem dangerously like a date, [person]." "

> i’ll have to get it approved by [person],” he said, seemingly giving in to my demands.

> *(BOOK_001, POS_001, tertile=middle)* He turned to Wyatt. “

> *(BOOK_001, POS_001, tertile=middle)* Wyatt,” he said. “

> *(BOOK_001, POS_001, tertile=begin)* Now, Wyatt.” “

### Pass A/B/C

- **A lexical:** `H4_5a`
  - The Main and POS keywords ('turner', 'carley', 'bray', 'captain', 'psychic', 'suspicions', 'talked', 'val', 'yourbrother') and KeyBERT ('bowed', 'willing', 'commander', 'insisted', 'dangerously', 'begging', 'tightly', 'delicate') suggest a situation where characters are protective of each other, with 'commander' and 'captain' implying a position of authority. The MMR keywords ('dangerously', 'commander', 'squinted', 'fishing', 'smacked', 'notion', 'scrambled', 'revealing', 'choked', 'bowed') hint at tension and danger, but no external threat is explicitly stated. Therefore, the consensus code is H4_5a, protective commitment, as characters are showing responsibility and care for each other without an external threat.
- **B contextual:** `H4_0`
  - The dominant code is H4_0 (off_target) as most sentences do not explicitly show any form of protection, care, or control. H4_5a (protective_commitment) is present in one sentence where Brant shows concern for the protagonist's safety. H4_6 (external_protection_social_legal) and H4_7 (possessive_claiming) appear once each, indicating external threats and possessive language respectively. H4_9 (coercive_control) is present in multiple sentences, showing a partner as a source of threat.
- **C adjudicate:** `H4_5a`
  - The topic revolves around promises and vows of protection, which are future-tense speech acts. There's no evidence of an external threat, so H4_5a (protective commitment) is the most fitting code.
- **Action:** KEEP

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
- **Code:** H4_2 (norm: H4_2)

> i am kind of tired, but you’ve done enough.

> i’ve been riding most of the day, i’m tired.” “

> i’ve rested more than i ever expected to rest in the whole of my lifetime during the past six weeks,” he said, “and i’m feeling perfectly fresh.

> *(CELL_C, tertile=begin)* I was tired and cold and done with feeling under siege for the day. “

> *(CELL_C, tertile=middle)* Aren’t you getting just a little tired of—” “I wasn’t kidding about the way it gets dark out here.

> *(CELL_B, tertile=middle)* You must be exhausted with all of your commitments at the moment?’ ‘

> *(CELL_B, tertile=end)* I was tired from a big week, my nervous energy had transformed into lethargy, and I was still drunkish.

### Pass A/B/C

- **A lexical:** `H4_2`
  - The keywords 'tired', 'exhausted', 'fatigue', 'drained', 'worn' indicate a state of physical exhaustion, which is a form of practical care (H4_2). There's no external threat or possessive/coercive behavior mentioned, hence 'none' for threat source and 'neutral' for autonomy effect.
- **B contextual:** `H4_2`
  - All sentences express concern or recognition of the character's tiredness, with no external threat, possessive language, or coercive control present.
- **C adjudicate:** `H4_2`
  - The topic's dominant code is H4_2, indicating practical care, which aligns with the taxonomy of Emotional Safety, Reassurance & Caretaking. No external threat or control dynamics are evident, so H4_5a is not applicable.
- **Action:** KEEP

---

## Topic 358 — Reassuring Squeeze of The Hand

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_5a (norm: H4_5a)

> she took bronte's hand and gave it a reassuring squeeze. "

> ted reached for caroline's hands and smiled at her reassuring squeeze. "

> they'll ask,” he murmured, and gave her waist a reassuring squeeze.

> *(CELL_D, tertile=end)* But my parents—" "Are fine," he interrupted, groaning when she curved her fingers as far as she could around his hardening shaft. "

### Pass A/B/C

- **A lexical:** `H4_1`
  - The use of words like 'reassuring', 'gently', 'calming', and 'trembling' indicate tenderness and emotional support (H4_1), with no external or partner threat present.
- **B contextual:** `H4_5a`
  - The dominant code is H4_5a (protective commitment) as most sentences involve characters physically holding or squeezing another's hand, indicating a protective or reassuring gesture. There's no external threat or possessive language, so the threat source is 'none'.
- **C adjudicate:** `H4_5a`
  - The topic's dominant code, H4_5a, represents protective commitment, which aligns with the taxonomy of Emotional Safety, Reassurance & Caretaking. There's no evidence of an external threat, so H4_5 or H4_6 are not applicable.
- **Action:** KEEP

---

## Topic 363 — Asking The Sheriff For Help

- **Taxonomy:** 10.3 — Mystery, Suspense & Investigation
- **Code:** H4_0 (norm: H4_0)

> sheriff, if you could give us a key and point us in the right direction, we’ll be on our way.” “

> i’ll do something—maybe i’ll run for sheriff.

> sheriff, i appreciate your concern and i hope that means you’ll put all your energies into finding this guy.

> *(BOOK_004, CELL_A, tertile=begin)* This is so much bigger than anyone knows… The sheriff glances around nervously. “

> *(BOOK_004, CELL_A, tertile=begin)* Upon closer inspection, I swear both he and Sheriff McGraw look positively white. “

> *(BOOK_004, CELL_A, tertile=begin)* Nearly two hours later, after I’ve nibbled on several iced oatmeal cookies and drunk eight glasses of sweet tea, Sheriff McGraw finally waddles in through the parlor doors.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The use of words like 'sheriff', 'deputies', 'jail', 'weapons', and 'hailed' suggests a physical external threat, warranting the H4_5 code for external protection (physical).
- **B contextual:** `H4_0`
  - The sentences primarily discuss the role and actions of a sheriff, with no specific protective, possessive, or coercive actions mentioned. The sentence 'There’s a posse out hunting for you.' (BOOK_006_1) implies external protection, but it's the only instance.
- **C adjudicate:** `H4_5`
  - The dominant code H4_0 (off_target) indicates that the topic does not primarily focus on care or protection. However, the lexical consensus of H4_5 (external_protection_physical) suggests that there is a significant aspect of external protection present in the topic. Given the taxonomy of Mystery, Suspense & Investigation, it's likely that this protection involves safeguarding from external threats.
- **Action:** REINTERPRET

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

## Topic 114 — Guns Aimed Across The Room

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_0 (norm: H4_0)

> while [person] trussed up the englishman, caroline aimed her gun. “

> barrette renewed his grip on the pistol, and aimed at lilly.

> he was on his back, the chair across his legs, but his gun still aimed at [person]. “

> *(CELL_A, tertile=begin)* With a sealed hand, Eve turned back Mills's jacket, saw his weapon still holstered. "

> *(CELL_A, tertile=middle)* The weapon seemed to leap in her hand as she fired it, struck the man holding the boy between the eyes.

> *(CELL_A, tertile=end)* She said it quickly, because she'd seen his hand tighten on his weapon. "

> *(CELL_A, tertile=end)* She said it quietly, urgently, as he lifted his weapon and placed it to the pulse at his throat.

> *(CELL_D, tertile=middle)* He forced his focus from her, lifted the camera and shot off a few frames in a row.

> *(CELL_B, tertile=begin)* Lifting the weapon, she set it on its lowest setting and carefully sited it along the cut, firing off one quick burst.

> *(CELL_B, tertile=begin)* Coming upon him from behind, she placed the barrel of her weapon against the center of his back, directly over his heart. “

> *(CELL_B, tertile=begin)* She clotheslined the second with an extended arm, grabbing his weapon from his slackened grip even as he executed a flip.

> *(CELL_B, tertile=begin)* Lifting the weapon with an effort, she fired off several warning shots.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'gun', 'pistol', 'rifle', 'barrel', 'weapon', 'guns', 'cocked', 'fired', 'pointed', 'aimed' indicate external physical threats, thus H4_5.
- **B contextual:** `H4_5`
  - All sentences describe physical actions involving weapons, indicating external protection.
- **C adjudicate:** `H4_5`
  - The topic discusses the character's physical protection of their partner from external threats, aligning with the H4_5 code.
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

## Topic 173 — Waiting For Him to Wake

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_0 (norm: H4_0)

> it’s after him so you’ll just have to wait until he wakes up to get your answer.”

> it'll put him to sleep."

> yeah, i guess i’ll have to wait and see when he wakes up.

> *(CELL_A, tertile=end)* Could he count on not waking him when he lifted him from that warm bed?

> *(CELL_A, tertile=middle)* He’d awakened to this darkness, and so far he hadn’t been able to work up the nerve to move.

> *(CELL_A, tertile=end)* He’d awakened to this darkness, and so far he hadn’t been able to work up the nerve to move.

> *(CELL_A, tertile=end)* He’d awakened to this darkness, and so far he hadn’t been able to work up the nerve to move.

> *(CELL_D, tertile=middle)* He looked fresh, rejuvenated, as though their little fling from last night hadn't permanently affected his energy.

> *(CELL_D, tertile=middle)* He used to jog the property's perimeter every morning, before breakfast.

> *(CELL_B, tertile=middle)* He's sleeping for longer periods of time at night now,” Jacob said. “

### Pass A/B/C

- **A lexical:** `H4_0`
  - All four keyword lists centre on sleep states and waking (sleep, asleep, wake, awoke, slept, woke, tired, sleeping, drifted), physical sensations (panting, pounding, warmed, temperature), and incidental scene-setting (bedside, tv, rear, departure, scrambled). There is no lexical signal of care, protection, threat, jealousy, or control. The vocabulary describes ordinary nocturnal/rest scenes with no romance-care dimension, placing the topic firmly off-target for the H4 taxonomy.
- **B contextual:** `H4_0`
  - All sentences in this topic describe sleep states, fatigue, wakefulness, and monitoring of whether a person is asleep. There is no care, protection, possessiveness, control, or relational dynamic expressed — the content is purely observational or descriptive of physical sleep/rest states. None of the sentences contain romance-relevant care-protection content, making H4_0 (off_target) the correct code throughout.
- **C adjudicate:** `H4_0`
  - All three passes converge on off-target (H4_0). Lexical consensus, contextual dominant, and the prior H3 S0 ruling all agree that this topic performs a temporal/structural narrative function rather than any care or protection function. The taxonomy primary label 'Emotional Safety, Reassurance & Caretaking' is a surface-level mismatch: the topic content is about time and seasons as narrative framing devices, not about a character delivering reassurance or care to a partner. No external threat is evidenced (ruling out H4_5/H4_6), no partner restriction is present (ruling out H4_9–H4_11), and no affective care exchange is depicted (ruling out H4_1–H4_4, H4_12). The secondary taxonomy label '8.4 Time, Seasons & Temporal Framing' accurately describes the topic's actual function. KEEP with H4_0 is the correct resolution; no split or reinterpretation is warranted.
- **Action:** KEEP

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

- **A lexical:** `H4_1`
  - The keywords 'trust', 'trusted', 'betrayed', 'betray', 'trusting', and 'you' indicate a focus on trust and its breach, suggesting reassurance and tenderness (H4_1). There are no external threats or possessive/coercive elements mentioned.
- **B contextual:** `H4_1`
  - The sentences primarily discuss trust, with no external threats or possessive claiming language.
- **C adjudicate:** `H4_1`
  - The topic's dominant and consensus codes both indicate H4_1, which aligns with the taxonomy of Emotional Safety, Reassurance & Caretaking. The topic focuses on providing emotional comfort and reassurance, with no evidence of external threats or coercive control.
- **Action:** KEEP

---

## Topic 190 — Offering to Get Someone Cleaned Up

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** H4_2 (norm: H4_2)

> i’ll get cleaned up here as soon as i can.

> i’ll pay to have it cleaned.” “

> i'll get her cleaned up," said a handsome groom, taking her arm. "

> *(CELL_C, tertile=middle)* I will clean up the battlefield while you drink plenty of fluids.

> *(CELL_C, tertile=middle)* I know you would prefer to burn it yourselves out of respect, but my way will be faster, cleaner and will ensure no parasites escape.

> *(CELL_D, tertile=middle)* May I know why you gave Mr. Thesiger the brush off just now?”

> *(CELL_D, tertile=middle)* Don’t you see that if you go ahead with this annulment, if you air the Roxtons’ dirty laundry in public, I will be utterly, utterly ruined.

> *(CELL_D, tertile=begin)* A lackey came out from behind the butler with pan and brush and quickly set to sweeping up the shards of broken glass from Deb’s smashed wine glass.

### Pass A/B/C

- **A lexical:** `H4_2`
  - The keywords 'clean', 'cleaning', 'cleaned', 'mess', 'freshen', 'wipe', 'sweeping', 'dump', 'provide', 'assured', 'planned' indicate practical care (H4_2) without any external threat or possessive/coercive behavior.
- **B contextual:** `H4_2`
- **C adjudicate:** `H4_2`
  - The topic's dominant code is H4_2, indicating practical care, which aligns with the taxonomy of Emotional Safety, Reassurance & Caretaking. No external threat or control dynamics are evident, so H4_5a is not applicable.
- **Action:** KEEP

---

## Topic 91 — Arguing Over Guns and Weapons

- **Taxonomy:** 7.1 — Interpersonal Non-Romantic Conflict
- **Code:** H4_5 (norm: H4_5)

> i’ll be better armed as well.

> i don’t like guns, they’re only for bad things, and all they do are hurt people, so i’ll thank you to get them away from me, now."

> maybe i’ll get a shot with him next.

> *(BOOK_001, CELL_A, tertile=end)* Tell them someone was cleaning a gun, and it went off accidentally,” Sebastian said. “

> *(BOOK_001, CELL_A, tertile=end)* The boy came here the night of the shooting, ranting about having killed you.

> *(BOOK_003, CELL_B, tertile=end)* I called his name and that's when I saw the gun on the ground.

> *(BOOK_003, CELL_B, tertile=end)* Yeah, X had his team come after me because he was afraid someone else would get gun happy.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'gun', 'shot', 'shoot', 'guns', 'shots', 'bullet', 'shooting', 'bullets', 'weapon', 'pistol' along with 'weapons', 'fired', 'aimed', 'practice', 'squeeze', 'intend' suggest external physical protection or threat.
- **B contextual:** `H4_5`
  - The dominant code is H4_5 (external protection physical) as many sentences discuss protecting from external threats like shooters. H4_5a (protective commitment) is also present, showing responsibility without an external threat. H4_9 (coercive control) appears in a few sentences, indicating a partner as a danger. There's no possessive claiming or jealous possessiveness, and no mixed or unclear codes reach 70%.
- **C adjudicate:** `H4_5`
  - The topic discusses external physical protection, with evidence of an external threat, such as 'He shielded her from the incoming bullet'.
- **Action:** KEEP

---

## Topic 51 — Locked Up By A Vampire

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_5 (norm: H4_5)

> you’ve kept me locked up—” “in the best room money can buy…” “i haven’t seen the outside world in two weeks—” “you’re a vampire,” he said, frowning a bit. “

> they can turn me back into a vampire, and i’d binge until i’ve made up for every day i haven’t fed.

> and you’ve never even considered being with a vampire?

> *(BOOK_001, CELL_B, tertile=end)* Of course there was a vampire story mixed in there and I love some vampire action.

> *(BOOK_001, CELL_B, tertile=end)* There is one short m/f scene where a woman is being sucked dry by a vampire during sex but its no big deal.

> *(BOOK_001, CELL_B, tertile=end)* Top2Bottom Reviews Reviews for THIRST say: Lisa Worrall has crafted a smart and interesting story of soul deep connection and love against a backdrop of vampires, retribution and loss.

> *(BOOK_004, CELL_A, tertile=middle)* The vampire didn’t want to be a murderer, as I once suspected.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords 'vampire', 'vampires', 'vamp', 'vamps', 'vampyre', 'blood', 'wraith', 'wraiths', 'creatures', 'feeding', 'threats' suggest external physical threats from vampires to humans, triggering H4_5 (external protection - physical).
- **B contextual:** `H4_5`
  - The dominant code is H4_5 (external protection physical) as many sentences mention vampires, which are external threats. There's no possessive claiming or coercive control language used.
- **C adjudicate:** `H4_5`
  - The topic discusses the hero physically protecting the heroine from an external threat, fitting the H4_5 code.
- **Action:** KEEP

---

## Topic 184 — Racing to Stop A Spreading Fire

- **Taxonomy:** 7.3 — Risk, Danger & External Crises
- **Code:** H4_5 (norm: H4_5)

> you’ve got the fire.

> it looks like we’ve got an arson and a murder on our hands.” “

> we’ve got to get down to the fire station and get rolling before that fire starts to spread.”

> *(CELL_D, tertile=middle)* He’d already called and checked in, and there were no raging fires that needed to be put out, but he still wanted to get there quickly.

> *(CELL_C, tertile=middle)* Her body was on fire, and Ransom had the equipment to put it out.

> *(CELL_C, tertile=begin)* You’re still making sure the gas line to the stove is off when you leave, right?” “

> *(CELL_C, tertile=end)* This news trumped everything else on folks’ minds: what people got for Christmas, holiday vacation stories, the one-hundred-year-old Methodist church destroyed by arson fire, and even the first snowfall Sienna had seen in fifty years.

> *(CELL_C, tertile=begin)* The redhead had the power to take the incident from the frying pan to the fire.

### Pass A/B/C

- **A lexical:** `H4_5`
  - The keywords and phrases in all lists (Main, KeyBERT, POS, MMR) revolve around fire and its effects, indicating a threat (external in this case, as it's not a partner). However, there's no indication of any protective action or commitment, making it 'neutral' in terms of autonomy effect.
- **B contextual:** `H4_5`
  - The dominant code is H4_5 (external protection, physical) as many sentences refer to fire, which is an external threat. There's also some practical care (H4_2) and protective commitment (H4_5a) present, but not as prevalent.
- **C adjudicate:** `H4_5`
  - The topic discusses physical protection from external threats, aligning with the lexical and contextual dominant codes.
- **Action:** KEEP

---

## Topic 294 — Accepting Whatever Punishment Is Deserved

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** H4_9 (norm: H4_9)

> then i guess i’ll just have to accept your punishment.” “

> you’ll be punished.” “

> i’ll take whatever punishment i deserve, but i won’t give him up.” “

> *(BOOK_001, CELL_D, tertile=begin)* I’ll need somebody to heel the ladder if I come down with a victim.”

> *(BOOK_002, CELL_B, tertile=middle)* If I had known that I was going to be treated in this fashion…” “What would you have done?”

> *(BOOK_003, CELL_C, tertile=middle)* Did the light spankings he gave while they were in the throws of passion count as browbeating?

> *(BOOK_004, CELL_B, tertile=begin)* That I am happy to say shall be a fitting punishment for you both.” “

> *(BOOK_004, CELL_B, tertile=end)* All this coming from the man who had decapitated my mother and tried to rape me.

### Pass A/B/C

- **A lexical:** `H4_9`
  - The keywords 'punish', 'punished', 'raped', 'rape', 'rapist', 'violently', 'warned', 'refused' and 'deserve' indicate coercive control by a partner, restricting the autonomy of the other person.
- **B contextual:** `H4_9`
  - The dominant code is H4_9 (coercive control) as the sentences repeatedly mention punishment, which suggests a pattern of controlling behavior from a partner.
- **C adjudicate:** `H4_9`
  - The topic's dominant code is H4_9, indicating coercive control, which aligns with the taxonomy of Violence, Threats & Non-Sexual Coercion. No external threat is mentioned, so H4_5a is not applicable. The topic does not fit other care/control codes, so renaming is appropriate.
- **Action:** RENAME

---
