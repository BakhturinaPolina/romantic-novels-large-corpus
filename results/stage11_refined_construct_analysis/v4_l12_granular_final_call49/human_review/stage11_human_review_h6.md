# H6 — Arc semantics (main-couple / position)

Run: `v4_l12_granular_final_call49` — 29 topics.

### New categories (read these before the topics)

| Code | Category | Definition |
| --- | --- | --- |
| `ARC_0` | **off target** | Not a narrative-arc role for the main couple (or not arc content). |
| `ARC_1` | **misunderstanding** | Hidden information, secret, or misunderstanding driving the arc. |
| `ARC_2` | **escalation conflict** | Main-couple conflict escalation / falling action. |
| `ARC_3` | **separation breakup threat** | Separation, breakup threat, or rupture of the couple bond. |
| `ARC_4` | **relationship caused distress** | Distress caused by the relationship itself (not purely external plot). |
| `ARC_5` | **disclosure** | Revelation / disclosure that moves the arc toward resolution. |
| `ARC_6` | **repair** | Repair, reconciliation work, conflict resolution in progress. |
| `ARC_7` | **restored trust** | Restored trust / reassurance after rupture. |
| `ARC_8` | **mutual commitment final payoff** | Mutual commitment / final relational payoff (HEA-adjacent arc close). |
| `ARC_9` | **external plot conflict** | External/plot obstacle (antagonist, job, family) not main-couple conflict per se. |
| `ARC_10` | **unclear arc role** | Arc-relevant but role unclear / mixed. |

### Topic 285 — Confessing Years of Hatred {#topic-h6-285}

- **Old taxonomy:** 3.2 — Negative Emotions & Distress
- **New category:** **ARC_2 — escalation conflict**
- **Mixed:** True
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> i’ve hated him for years.

> heath has done a wonderful job with him, but i—well, i’ve hated him for living instead of you.

> ever since this cunt came here, i’ve been, uh, less than balanced, i admit, and remembering things i’ve tried to forget, reasons to hate, reasons to hate, and you’ve become a liar.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Mending Places — Denise Hunter; tertile=middle; p=0.57**
>
> Looking back now, I can see all the hatred I had in me, but at the time it just seemed like everyone was out to get me.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Mending Places — Denise Hunter; tertile=end; p=0.48**
>
> It had been a long time since his presence had evoked disdain.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Really Angelic — Enid Wilson; tertile=middle; p=0.62**
>
> And I hated submitting to your licentious thoughts and advances!” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Really Angelic — Enid Wilson; tertile=end; p=0.60**
>
> You expressed a dislike of both Himins and myself.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_5 — disclosure**
  - Main keywords ('hate', 'hated', 'hates', 'hating', 'hateful', 'myself') point strongly to internalized negative emotion directed at self or partner, suggesting relationship-caused distress (ARC_4). However, KeyBERT and MMR both surface 'admit', 'dislike', 'treated', 'deserve', and 'planning', which collectively signal a moment of confession or acknowledgment — a character admitting feelings (even negative ones like dislike or hatred) to another, consistent with disclosure (ARC_5). POS yields only 'purpose' and 'shock', which are too sparse to anchor a specific arc role (ARC_10). The convergence of 'admit' and 'dislike'/'hated' across KeyBERT and MMR tips the consensus toward ARC_5: a character disclosing previously hidden negative feelings (e.g., 'I hated you' or 'I have to admit I disliked how you treated me'), which is a classic romance-arc disclosure beat. Disagreement is flagged because Main leans ARC_4 and POS is unclear.
- **Pass B — contextual:** **ARC_2 — escalation conflict**
  - Topic 285 is saturated with hatred, loathing, and disdain language ('I hate you', 'hated him', 'loathed him', 'dislike'). All sentences express intense interpersonal hostility, which maps cleanly to ARC_2 (escalation_conflict) — the emotional peak of antagonism between characters. The topic is not about misunderstanding (ARC_1), separation (ARC_3), or external plot (ARC_9); it is the raw expression of conflict-level negative affect. Main-couple attribution is uncertain for roughly half the sentences (many use 'him/her' without clear dyadic context), but several BOOK_003 sentences and BOOK_002_2/3 plausibly involve the main couple, yielding a moderate main_couple_prob of ~0.45. No sentence reaches a repair, disclosure, or commitment register, so ARC_2 dominates at 100%.
- **Pass C — adjudication:** **ARC_2 — escalation conflict**
  - Lexical consensus flagged ARC_5 (disclosure), but the contextual dominant signal is ARC_2 (escalation_conflict), which better captures the taxonomy metadata: Negative Emotions & Distress (3.2) as primary and Interpersonal Non-Romantic Conflict (7.1) as secondary. The secondary taxonomy tag initially pulled toward ARC_5 (a disclosure event can surface distress), but disclosure is not the defining arc function here — the dominant pattern is escalating relational conflict generating distress within the main couple. ARC_2 is therefore the correct resolution. The construct bucket is REFINED_FALLING, consistent with a conflict-escalation phase in the narrative arc. No free-form labels were carried forward; all prior Pass A/B terms are mapped to ARC_2. Manual review is not required given clear contextual dominance.

---

### Topic 37 — Defending A Close Friendship {#topic-h6-37}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_1 — misunderstanding**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> i've told you -- we're just good friends.

> and i’ll grant ye i’ve been a bad friend to you.

> but we’ve been friends for a long time.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · It's All Relative — J.M. Snyder; tertile=middle; p=0.75**
>
> It was only friendship, nothing more, not to me.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Got a Hold on You — Pat White; tertile=middle; p=0.63**
>
> Good, then get out of my face and give me a minute with my friend.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Got a Hold on You — Pat White; tertile=end; p=0.61**
>
> I’m here because I’m worried about a friend.” “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Got a Hold on You — Pat White; tertile=middle; p=0.47**
>
> He didn’t have any life-long friends, with the exception of Butch.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Got a Hold on You — Pat White; tertile=end; p=0.46**
>
> A friend once told me it’s okay to lean on someone,” he said. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_0 — off target**
  - All four keyword lists point away from main-couple romantic arc dynamics. Main is dominated by 'friends/friendship/friendly/friendships/best friend' vocabulary — social relationship framing, not romantic-couple conflict or progression. KeyBERT adds casual social-interaction words ('playfully', 'parties', 'stalked' in a light sense, 'engaged', 'honestly') with no romantic-arc signal. POS yields ambient social/contextual nouns and adjectives ('parties', 'anxiety', 'suggestion', 'fashioned', 'annoying') that do not map to any specific arc stage. MMR similarly offers social-texture words ('pout', 'admire', 'playfully', 'shout') without a coherent arc trajectory. No cues for misunderstanding, escalation, separation, disclosure, repair, commitment, or external plot conflict between a main couple are present. The topic appears to describe friendship dynamics or a friend-group social context, making it off-target for romance narrative-arc coding.
- **Pass B — contextual:** **ARC_1 — misunderstanding**
  - Topic 37 clusters around the word 'friend' and its variants, predominantly functioning as a misunderstanding or deflection device in romance narratives — one partner insisting the relationship is 'just friendship' when the other perceives or desires more (ARC_1: misunderstanding). Several sentences (BOOK_001_1–6, BOOK_002_1–3, BOOK_003_6) reflect this friend-zone ambiguity between potential main-couple members. BOOK_003_1, BOOK_003_2, and BOOK_003_5 shift toward a separation/breakup-threat register ('We're still friends, right?', 'I'd like to stay friends with you'), coded ARC_3. Several sentences (BOOK_002_4–6, BOOK_003_3–4, BOOK_004_1–2) are clearly off-target, referring to third-party friendships with no main-couple relevance (ARC_0). ARC_1 is the plurality code at ~40%, below the 70% threshold for a single dominant code, but no other code comes close; ARC_1 is returned as dominant given its plurality. Main-couple probability is moderate (~0.50) because roughly half the sentences plausibly involve the main couple's friend-zone dynamic, while the rest are off-target or unclear.
- **Pass C — adjudication:** **ARC_1 — misunderstanding**
  - Lexical consensus (ARC_0 / off_target) was overridden by contextual dominant (ARC_1 / misunderstanding). The taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information directly corroborates ARC_1: the topic captures concealed information or false impressions that generate relational tension between the main couple, not mere off-target noise. The secondary taxonomy (4.2 Ongoing Courtship) suggests the misunderstanding is embedded in an active courtship phase, consistent with a falling/tension arc rather than a repair or resolution arc. ARC_1 is therefore the correct single code. Construct bucket is REFINED_FALLING because misunderstandings typically drive the couple apart or impede bonding, placing this in the falling/conflict segment of the narrative arc. No free-form labels were carried forward; all prior Pass A/B language has been mapped to ARC_1.

---

### Topic 94 — Caught in A Lie {#topic-h6-94}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **MIXED**
- **Normalised category:** —
- **Mixed:** True
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> i’ve known him for a long time, and i’m confident that i could tell if he was lying.”

> i’ve lied, therefore i’m a liar.

> i never meant to—” “how can i believe a single thing you say when you’ve already been proven a liar?”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Fiorenza forced marriage — Melanie Milburne; tertile=middle; p=0.69**
>
> I have no reason to lie to you about something like that,’ she said. ‘

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Fiorenza forced marriage — Melanie Milburne; tertile=middle; p=0.68**
>
> You are such a transparent liar,’ he said. ‘

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Fiorenza forced marriage — Melanie Milburne; tertile=begin; p=0.67**
>
> You are not a very convincing liar, Emma,’ he said. ‘

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Conquest Earth; Prince Galen — Angelique Anjou; tertile=middle; p=0.59**
>
> Why don’t you stop being such a baby about it and lie still and I’ll go get something for you?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Conquest Earth; Prince Galen — Angelique Anjou; tertile=middle; p=0.54**
>
> The sinking sensation that swept over him gave the lie to his efforts to convince himself it wasn’t.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_5 — disclosure**
  - Main rep is dominated by deception/truth vocabulary (lie, lied, lying, liar, honest, lies, honesty, truth), which strongly signals a disclosure or confrontation about hidden truths between the main couple — ARC_5 (disclosure). KeyBERT reinforces this with 'apologize' and 'hesitate', consistent with a character revealing or confessing something difficult. POS and MMR introduce formal/authority-register words (president, sir, direct, terms, sentence, threatened) that lack clear romantic-arc anchoring, pointing to ARC_10 (unclear arc role) in isolation. However, the Main rep carries the heaviest semantic weight for topic identity, and the deception-to-truth cluster is the defining signal. Consensus lands on ARC_5 (disclosure) as the dominant arc role, with disagreement flagged because POS/MMR pull toward an unclear or external register.
- **Pass B — contextual:** **ARC_1 — misunderstanding**
  - Topic 94 is overwhelmingly about lying and accusations of lying between characters. The recurring pattern — direct accusations ('You lied to me,' 'Liar'), denials ('I did not lie to you'), and meta-commentary on lying ('You are not a very convincing liar') — maps squarely onto ARC_1 (misunderstanding), where deception or perceived deception creates interpersonal conflict rooted in a breakdown of honest communication. BOOK_001 clearly involves a named dyad (Emma and a male partner), strongly suggesting a main couple. BOOK_002–004 lack sufficient context to confirm main-couple status, so those are coded 'unclear.' Two sentences (BOOK_002_3, BOOK_002_6) are off-topic (literal instruction to lie still; an exclamation unrelated to deception conflict), coded ARC_0. BOOK_003_6 references a philosophical statement about lying and consequences, edging toward ARC_5 (disclosure/truth-telling theme) rather than pure accusation. ARC_1 exceeds 70% and is the clear dominant code.
- **Pass C — adjudication:** **MIXED**
  - Lexical consensus (ARC_5 disclosure) and contextual dominant (ARC_1 misunderstanding) point to overlapping but distinct mechanisms within Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information). Both codes are plausible: the topic likely captures moments where hidden information is either revealed (ARC_5) or withheld/misread in a way that generates misunderstanding (ARC_1). Because neither code fully subsumes the other and the secondary taxonomy flag (4.4 Conflict, Distance & Breakup Threats) adds further ambiguity, a single ARC_# cannot be assigned without loss of fidelity. MIXED is therefore the correct arc_role. The construct bucket is REFINED_FALLING because both disclosure and misunderstanding typically drive relational deterioration in the narrative arc. Manual review is required to inspect representative documents and determine whether disclosure precedes or follows the misunderstanding, which would allow a future SPLIT into two cleaner topic clusters.

---

### Topic 109 — Seeing Past A Guarded Identity {#topic-h6-109}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_5 — disclosure**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> i’ve hardly heard a thing about you.”

> anyone could’ve walked by.

> even people who are close to you, who’ve known you far longer than i have, don’t know any more than what you’ve allowed them to see.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Baby, I'm Yours — Catherine Mann; tertile=middle; p=0.61**
>
> You have to know you’re important to me, too.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Baby, I'm Yours — Catherine Mann; tertile=end; p=0.57**
>
> Just as I know I can depend on you to be mine.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Baby, I'm Yours — Catherine Mann; tertile=middle; p=0.53**
>
> But if you really knew me, you would realize how very much I resented your taking control of my life by calling that inspector.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Vanquished — Hope C. Tarr; tertile=end; p=0.68**
>
> I know not only who you are but what you are.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_5 — disclosure**
  - All four keyword lists converge on identity disclosure. Main keywords ('who, know, am, don, you, are, about, me, anyone, is') form a classic 'who are you / do you know who I am' interrogative cluster signaling identity revelation. KeyBERT ('recognize, hi, fitting') reinforces recognition/identification of a person. POS ('identity, muffled, current, loose') anchors the topic explicitly to 'identity' with 'muffled' suggesting concealment or disguise. MMR ('dealing, identity, playfully, doubted, fitting, muffled, recognize, hi, thinks, loose') adds 'doubted' and 'playfully' alongside 'identity/recognize/muffled', consistent with a scene where a character's identity is hidden or uncertain and then revealed or questioned — a disclosure dynamic. No cues point to external plot threat, breakup, or repair; the dominant signal is identity-based disclosure (ARC_5).
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - Topic 109 clusters around the theme of knowing/not knowing someone's true identity. The largest single code is ARC_10 (unclear arc role), assigned to sentences that are too fragmentary or context-free ('It's me.', 'That would be me.', 'Who is it that wants to know?') to map to a specific narrative arc function. Among the interpretable sentences, ARC_1 (misunderstanding) is the next most common, covering lines where one partner challenges the other's claim to know them ('You don't even know me, not really'; 'You haven't got a clue who I am'). ARC_5 (disclosure) applies where a character reveals or invites revelation of their true self. ARC_2 and ARC_8 each appear once. No single code reaches 70%, but ARC_10 is dominant at ~45%. Main-couple probability is moderate (~0.60) because many sentences are clearly between romantic partners but several are too decontextualised to confirm.
- **Pass C — adjudication:** **ARC_5 — disclosure**
  - Lexical consensus (ARC_5 disclosure) and taxonomy placement (4.3 Secrets, Misunderstandings & Hidden Information) are mutually reinforcing: the topic centers on hidden information that is surfacing or at risk of surfacing between the main couple, which is the definitional core of ARC_5. The contextual dominant ARC_10 (unclear_arc_role) reflects annotator uncertainty about narrative timing rather than a genuine absence of arc signal — the taxonomy anchor resolves that ambiguity in favor of ARC_5. Secondary taxonomy 3.3 (Ambivalence & Internal Conflict) is consistent with ARC_5: a character wrestling internally with whether/how to disclose is a standard precursor to the disclosure event itself, not a competing code. Because disclosure typically destabilizes the relationship before repair, this sits in the REFINED_FALLING construct bucket. No free-form labels were carried forward; ARC_10 is retired as the dominant in light of the stronger lexical and taxonomic evidence.

---

### Topic 121 — Revealing Plans to The Prince {#topic-h6-121}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_0 — off target**
- **Mixed:** False
- **Main-couple prob:** 0.1 | non-couple: 0.8
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> she’ll be queen of the roost.” “

> do you think he’ll really go to the king?”

> if i let the prince know what is happening, instead of waiting for them to find out, they’ll know i’ve been out on my own.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Trust Me — Lesley Pearse; tertile=middle; p=0.49**
>
> I am not Prince Charming or a shining Knight on a white horse.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Trust Me — Lesley Pearse; tertile=middle; p=0.40**
>
> Hot as a fever, rattling bones I could just taste it, taste it If it’s not forever, if it’s just tonight Oh it’s still the greatest, the greatest, the greatest Kings of Leon Chapter Ten “You two pieces of shit are worthless you know that?”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Trust Me — Lesley Pearse; tertile=end; p=0.38**
>
> I WILL one day go on a vacation to Disneyland and actually hang with Belle, Beast, Briar, Winter and Ashess.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Highlander Unchained — Monica McCarty; tertile=begin; p=0.69**
>
> Why did he need her if the king was involved?

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Highlander Unchained — Monica McCarty; tertile=end; p=0.69**
>
> If only I’d realized what the king intended.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Highlander Unchained — Monica McCarty; tertile=begin; p=0.66**
>
> Didn’t you appeal to the king for help?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Highlander Unchained — Monica McCarty; tertile=begin; p=0.66**
>
> Then the king has done something about it?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Highlander Unchained — Monica McCarty; tertile=end; p=0.65**
>
> I should have suspected the king’s treachery.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · d'Argent Honor: Full Circle — Ann Jacobs; tertile=end; p=0.65**
>
> Meanwhile you must learn how best to serve your queen.”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_9 — external plot conflict**
  - Main keywords (king, prince, queen, throne, servant, royal, crown, kingdom, regent) are densely royal/political — no main-couple romantic arc signal, pointing to external political/power-structure conflict (ARC_9). MMR reinforces this with 'threats', 'declared', 'resigned', 'dealing', 'commander' — language of political negotiation and power struggle rather than romantic arc. KeyBERT ('promises', 'reassuring', 'assured', 'resigned', 'reveal', 'planned', 'decision') and POS ('threats', 'reassuring', 'commander', 'promises', 'magical') are more ambiguous — they could belong to any arc stage and lack clear romantic-couple anchoring, hence ARC_10 for those reps. However, the dominant signal across Main and MMR is an external political/institutional conflict context (royal court, power, threats, commanders), making ARC_9 the consensus. Disagreement flagged because KeyBERT and POS lean ARC_10 rather than ARC_9.
- **Pass B — contextual:** **ARC_0 — off target**
  - Topic 121 clusters around royalty/nobility vocabulary — kings, queens, nobles, rulers — but this is overwhelmingly world-building or external-political context rather than main-couple romantic arc content. BOOK_001 sentences are off-target (pop-culture references, fairy-tale tropes with no couple dynamic). BOOK_002 sentences revolve around a king's treachery/political machinations with no identifiable romantic couple, coded ARC_9 (external plot conflict). BOOK_003 sentences use 'queen' as a title/power dynamic but lack a clear romantic-couple frame; most are off-target social/political framing (ARC_0). BOOK_004 similarly references the king's commands and noble status as background world-building. No sentence clearly depicts a main-couple romantic arc event. ARC_0 is dominant at ~60%; ARC_9 accounts for ~40% (external political conflict). Main-couple probability is very low (~0.10) as the couple, if present, is peripheral to the topic's core signal.
- **Pass C — adjudication:** **ARC_0 — off target**
  - Adjudication resolves the conflict between lexical consensus (ARC_9: external_plot_conflict) and contextual dominant (ARC_0: off_target) in favor of ARC_0. The taxonomy placement under 4.3 Secrets, Misunderstandings & Hidden Information with a secondary tag of 10.2 Historical & Period Setting suggests the topic's surface signal is period/setting detail or background intrigue rather than a main-couple dynamic. ARC_9 was likely assigned because conflict-label vocabulary is present, but high conflict-label fidelity is explicitly not equivalent to main-couple conflict. The secondary taxonomy tag (Historical & Period Setting) further supports that the dominant content is world/context material, not a relationship arc beat. ARC_0 (off_target) is therefore the correct single arc_role. Manual review is flagged because the lexical and contextual passes disagreed, and the taxonomy straddles two categories that could, in a different topic, support ARC_1 or ARC_5 — a human reviewer should confirm no main-couple secret/misunderstanding is embedded in the cluster.

---

### Topic 130 — Revealing A Secret Plan {#topic-h6-130}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_0 — off target**
- **Mixed:** False
- **Main-couple prob:** 0.1 | non-couple: 0.8
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> you’ve rumbled my clever plan.’ ‘

> yes, i’ve got a little more planned for this evening.

> we’ve had this planned for months, but i’d almost forgotten about it.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Love Lives — Josie Lloyd; tertile=middle; p=0.54**
>
> She would come out with mad plans and then challenge me into doing them.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · The ABC's of Kissing Boys — Tina Ferraro; tertile=begin; p=0.68**
>
> I had a real and viable plan in place now to turn things around.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · The ABC's of Kissing Boys — Tina Ferraro; tertile=end; p=0.67**
>
> And keeping with the Plan seemed like my only way there.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · The ABC's of Kissing Boys — Tina Ferraro; tertile=middle; p=0.62**
>
> This plan—it's not going to get you into any trouble at school?” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · The ABC's of Kissing Boys — Tina Ferraro; tertile=middle; p=0.57**
>
> I just didn't plan to be around to help make it happen. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_10 — unclear arc role**
  - All four keyword lists center on planning and logistics vocabulary: 'plan, plans, planned, planning, tentatively, considering, scenario, urgency, according, part.' Supporting terms like 'madam, sir, reception, results, pumping, veins, forming, hiding, opposite' add situational texture but do not anchor to any specific narrative-arc role for the main couple. There is no clear signal of conflict, misunderstanding, separation, disclosure, repair, commitment, or external plot threat. The dominant semantic field is neutral logistical/procedural planning, making the arc role genuinely unclear across all representations.
- **Pass B — contextual:** **ARC_0 — off target**
  - Topic 130 is entirely about the word 'plan(s)' and logistical planning language. None of the sentences carry any identifiable romantic-arc function — there is no conflict, disclosure, repair, commitment, or other arc-relevant content. The sentences are decontextualised fragments about making or changing plans, with no clear main-couple relationship dynamic visible. The topic is off-target (ARC_0) across all tertiles and books. Main-couple probability is very low; most sentences are ambiguous as to who is speaking or to whom, and none signal a romantic dyad.
- **Pass C — adjudication:** **ARC_0 — off target**
  - Adjudication resolves the Pass A/B tension as follows: the lexical consensus of ARC_10 (unclear arc role) reflects genuine ambiguity in surface tokens, but the contextual dominant of ARC_0 (off_target) is better supported by the taxonomy signal. Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) with secondary 4.2 (Ongoing Courtship & Everyday Relational Bonding) describes content that, while thematically adjacent to romance mechanics, does not map onto a main-couple narrative-arc beat — it is background relational texture or a non-main-couple dynamic. The absence of a clear main-couple anchor (main_couple: false) means no ARC_1–ARC_9 code is warranted. ARC_0 is therefore the correct resolution over ARC_10: the topic is not unclear so much as it is simply off-target for the main-couple arc hypothesis. No construct bucket applies because the topic does not contribute to REFINED_FALLING, REFINED_RISING, or EXTERNAL_PLOT_CONFLICT trajectories. No free-form labels were carried forward.

---

### Topic 177 — Seeing Past A Hidden Identity {#topic-h6-177}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_1 — misunderstanding**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> you’ll no longer be alex.

> i know they say if you want something bad enough you’ll find any excuse to believe it’s true… but there was something in alex that called to me.

> tell me you understand that, or you’ll be no help to alex.”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Three's a Crowd — Sophie McKenzie; tertile=middle; p=0.58**
>
> In the midst of my pleasure at seeing Alejandro literally backed up against a wall, I felt a pinprick of irritation at Jonno’s inability to see Eve as she was.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Three's a Crowd — Sophie McKenzie; tertile=end; p=0.56**
>
> I couldn’t get what she’d said about Alejandro out of my head.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Three's a Crowd — Sophie McKenzie; tertile=middle; p=0.55**
>
> But Eve was pulling away from me, moving towards Alejandro.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Three's a Crowd — Sophie McKenzie; tertile=middle; p=0.53**
>
> I still couldn’t believe that she had been with Alejandro last night.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · After Their Vows — Michelle Reid; tertile=middle; p=0.76**
>
> I should not have let Alex run my life for me.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · After Their Vows — Michelle Reid; tertile=middle; p=0.76**
>
> It was ironic that he should do this now, when the last person she wanted to think about was Alex. ‘

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_10 — unclear arc role**
  - Main keywords (sullivan, alexx, alexi, eliminate, woo, wanted, wasn, tell) suggest character names and vague action verbs with no clear romantic-arc signal; 'eliminate' and 'woo' are ambiguous without context. KeyBERT (instincts, realise, suffering, unsure) hints at internal emotional uncertainty but does not anchor to a specific arc stage. POS and MMR (dislike, guarded, fears, instincts, percent, movies, sidewalk, reminds, conscious) add hedged negative affect and mundane/observational terms that do not cohere into a recognizable arc role. No single arc stage — misunderstanding, escalation, separation, disclosure, repair, commitment, or external conflict — is clearly dominant across all four lists. All four reps independently land on ARC_10 (unclear arc role).
- **Pass B — contextual:** **ARC_2 — escalation conflict**
  - Topic 177 clusters around a named third-party figure ('Alex'/'Alejandro') who generates tension, jealousy, and friction between protagonists and their partners. The dominant signal is escalating interpersonal conflict (ARC_2): snapping, jealousy over Alejandro, complaints about Alex, and suspicion. One sentence shows a separation/withdrawal threat (ARC_3: Eve moving toward Alejandro). One shows relationship-caused distress (ARC_4: letting Alex run one's life). A few sentences from BOOK_005 shift to resolution/payoff (ARC_8, ARC_7) and off-target content (ARC_0), diluting but not overriding the dominant ARC_2 signal. ARC_2 reaches ~45%, well above the 70% threshold for a clean dominant code, so MIXED is not triggered; ARC_2 is dominant. Main-couple probability is moderate (~0.50) because many sentences involve a third party ('Alex'/'Alejandro') whose relationship to the main couple is unclear or indirect.
- **Pass C — adjudication:** **ARC_1 — misunderstanding**
  - Lexical consensus was ARC_10 (unclear) and contextual dominant was ARC_2 (escalation_conflict), but the taxonomy metadata resolves the ambiguity: the primary taxonomy is 4.3 Secrets, Misunderstandings & Hidden Information. Hidden information and secrets are the structural driver here, making ARC_1 (misunderstanding) the most precise fit — misunderstandings in romance arcs are canonically rooted in withheld or distorted information between the main couple. ARC_2 may describe a surface symptom (conflict escalates because of the secret/misunderstanding), but the generative mechanism is ARC_1. The secondary taxonomy (3.3 Ambivalence & Internal Conflict) is consistent with ARC_1, as internal ambivalence often underlies why information is withheld. This places the topic firmly in the REFINED_FALLING construct bucket — the relationship is destabilised by the information asymmetry, not yet in repair. No free-form labels were carried forward; ARC_2 from Pass B is superseded by ARC_1 upon taxonomy reveal.

---

### Topic 194 — Promising to Keep A Secret {#topic-h6-194}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_5 — disclosure**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> i’ll keep it a secret,” said lucas.

> i’ll be your dirty little secret,” i joked.

> i’ll leave that secret for him to reveal.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Bachelorette Party — Karen McCullah Lutz; tertile=end; p=0.75**
>
> Maybe you’ll be in charge of all my secrets from now on.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Bachelorette Party — Karen McCullah Lutz; tertile=middle; p=0.73**
>
> Trust me, he’s not hiding any deep dark secrets.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Bachelorette Party — Karen McCullah Lutz; tertile=end; p=0.73**
>
> Keeping God-only-knows-what horrific secret.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Bachelorette Party — Karen McCullah Lutz; tertile=middle; p=0.73**
>
> How else would I find out all of his secrets?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Before the Witches — Karina Cooper; tertile=end; p=0.59**
>
> If I knew that, I’d unlock a giant mystery, wouldn’t I?”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Sold into Marriage — Maxi Shelton; tertile=middle; p=0.52**
>
> Perhaps secret information that he has uncovered, information that would be dangerous to the French.’ ‘

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Sold into Marriage — Maxi Shelton; tertile=begin; p=0.38**
>
> For reasons I cannot disclose I would rather you did not mention the break-in to anyone.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_5 — disclosure**
  - All four keyword lists converge on disclosure dynamics. Main is dominated by secret/secrets/keep/keeping/kept/reveal/secrecy — the core lexicon of hidden information being held or released. KeyBERT reinforces with reveal/revealing/hiding/confessed/identity, pointing to an active moment of disclosure or near-disclosure. POS adds identity/embarrassing/curiosity/ability/pressure, consistent with a character revealing a personal truth (identity, ability) under social or emotional pressure. MMR echoes with guarded/reveal/confessed/hiding/discovered/bury, all signalling information that was concealed and is now surfacing. The cluster is squarely about the act of revealing a kept secret — the defining feature of ARC_5 (disclosure) — rather than the conflict that follows (ARC_2) or the repair that results (ARC_6). No cues strongly indicate external plot threat (ARC_9) or misunderstanding (ARC_1) as the primary frame.
- **Pass B — contextual:** **ARC_5 — disclosure**
  - Topic 194 is overwhelmingly about secrets, secrecy, and the act of keeping or revealing hidden information — the defining features of ARC_5 (disclosure). The vast majority of sentences (17/20) directly reference secrets, secret-keeping, or the threat/promise of disclosure. A meaningful subset (BOOK_006 sentences) clearly involves the main couple, where one or both partners are concealing truths from each other, which is a classic disclosure-tension dynamic. Two sentences (BOOK_005_2, BOOK_005_3) reference dangerous political/external secrets with no romantic-couple framing, coded ARC_9. Main-couple probability is moderate (~0.45) because while BOOK_006 strongly anchors the couple context, many other sentences are ambiguous or clearly non-couple. ARC_5 exceeds 70% threshold, making it the dominant code.
- **Pass C — adjudication:** **ARC_5 — disclosure**
  - Both lexical consensus and contextual dominant converge on ARC_5 (disclosure). Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) directly supports a disclosure event — a character reveals or is confronted with concealed information, which is the canonical ARC_5 trigger. The secondary taxonomy 9.2 (Promise, Vow & Future-Tense Speech Acts) suggests a commitment or pledge may accompany or frame the disclosure, but it does not displace the primary arc role; it is a supporting speech-act layer. Because disclosure typically destabilizes the relationship before repair can occur, this sits in the REFINED_FALLING construct bucket. No conflict between passes; no free-form labels to remap. Main-couple filter passes — the disclosure pertains to the central romantic dyad. No manual review needed.

---

### Topic 214 — Demanding to Know What Happened {#topic-h6-214}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_1 — misunderstanding**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> oh my god, how did this happen?”

> please, tell me precisely what is happening to you.”

> and i need to know what’s going on to some extent so i don’t think the worst.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Midnight Angel — Lisa Kleypas; tertile=end; p=0.71**
>
> Damn you…tell me what happened!”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Midnight Angel — Lisa Kleypas; tertile=middle; p=0.67**
>
> What the hell has she done?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Midnight Angel — Lisa Kleypas; tertile=middle; p=0.70**
>
> What has happened to you?”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_2 — escalation conflict**
  - KeyBERT, POS, and MMR all converge on escalation cues: 'caused/causing' (active harm in progress), 'worst' (peak negative intensity), 'extent' (measuring severity of damage), and 'precisely/honestly' (confrontational demand for truth). Main keywords ('hell, fuck, what happened, going, happening') are emotionally charged interrogatives signaling a heated confrontation or crisis moment — consistent with escalating conflict rather than a calm disclosure or repair scene. The combination of ongoing causation language ('causing', 'caused'), superlative severity ('worst'), and agitated interrogatives points to ARC_2 escalation_conflict as the dominant arc role. Main alone was coded ARC_10 because bare interrogatives without relational context are ambiguous, creating minor disagreement, but the three keyword-extraction methods override toward ARC_2.
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - All sentences in Topic 214 are short, decontextualized interrogative fragments ('What happened?', 'What's going on?', 'What the hell happened?'). They express reactive surprise or demand for information but carry no identifiable narrative arc role on their own — there is no indication of who is speaking, to whom, or in what relational context. No sentence can be reliably linked to a main couple, nor to a specific arc stage such as conflict, disclosure, repair, or commitment. The topic appears to be a BERTopic cluster of generic inquiry/reaction dialogue tags that are off-context for arc coding. ARC_10 (unclear_arc_role) is the appropriate code for all sentences. Main-couple probability is very low (~0.10) because the fragments are generic enough to appear in any character interaction.
- **Pass C — adjudication:** **ARC_1 — misunderstanding**
  - Lexical consensus (ARC_2 escalation_conflict) and contextual dominant (ARC_10 unclear) diverge, but the taxonomy anchor — 4.3 Secrets, Misunderstandings & Hidden Information — is the decisive tie-breaker. Hidden information and secrets are the structural engine of ARC_1 (misunderstanding), not ARC_2 (escalation) or ARC_10 (unclear). ARC_2 would require evidence that conflict is actively intensifying beyond the misunderstanding stage; the secondary taxonomy tag (3.2 Negative Emotions & Distress) is consistent with the emotional fallout of a secret-driven misunderstanding rather than an independent escalation dynamic. ARC_10 is inappropriate because the taxonomy provides sufficient specificity to resolve ambiguity. The topic is main-couple focused (secrets/misunderstandings in romance BERTopic clusters are overwhelmingly dyadic). Construct bucket is REFINED_FALLING because secret-based misunderstandings typically appear in the falling/complication arc phase before disclosure or repair.

---

### Topic 237 — Hiding Someone Before He Arrives {#topic-h6-237}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_5 — disclosure**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> i’ll call jared now.

> jared was just heading off to work but is going to need his shirt so i’ll be right back.”

> you can’t come because if jared catches one glimpse of you, he’ll know.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Once In A Lifetime — Gwynne Forster; tertile=end; p=0.41**
>
> At that, several male heads popped out, one of them being Ronald, Dee’s boyfriend.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Island Song — Alan Chin; tertile=end; p=0.53**
>
> PJ," Garrett says, "how many times are you going to make me ask you to call me Garrett?" "

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Island Song — Alan Chin; tertile=end; p=0.53**
>
> Keep him coming," Garrett tells Madison. "

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Island Song — Alan Chin; tertile=begin; p=0.52**
>
> Something is happening inside Garrett's head, a feeling so bizarre he can't quite place it, can't put a name to it.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Island Song — Alan Chin; tertile=begin; p=0.52**
>
> It's a feeling Garrett can't put into words.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Island Song — Alan Chin; tertile=middle; p=0.52**
>
> The other arm has Garrett in a headlock. "

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Blood of the Beast — Tamela Quijas; tertile=end; p=0.76**
>
> The response appeared to placate Jared. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_4 — relationship caused distress**
  - Main rep leans toward interpersonal conflict via 'wrathfully', 'eyed', and named male characters in apparent confrontation, suggesting ARC_2 escalation. However, KeyBERT, POS, and MMR converge strongly on ARC_4 (relationship-caused distress): POS offers 'distress', 'disbelief', 'disappointed', 'wound', 'fingertips' (physical/emotional hurt); MMR reinforces with 'distress', 'collapsed', 'ripping', 'wound', 'warned'; KeyBERT adds 'worrying', 'distracted', 'privacy' — all pointing to emotional suffering and vulnerability experienced by a character within or because of a relationship dynamic. The physical injury cues ('wound', 'fingertips', 'ripping', 'collapsed') combined with emotional distress markers ('disbelief', 'disappointed', 'worrying') indicate a character in pain — likely relational in origin — rather than a direct escalating confrontation. Consensus falls to ARC_4 by 3-to-1 majority.
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - Topic 237 is dominated by fragmentary dialogue tags and brief action snippets (e.g., 'Jared queried', 'Jared shrugged', 'Garrett feels his face flush', 'Keep him coming') that provide no discernible narrative-arc signal. The sentences are almost entirely decontextualised speech-attribution fragments or minor physical actions. No clear main couple is identifiable across the books — BOOK_001 references a side character's boyfriend, BOOK_002 involves Garrett in unclear social interactions, BOOK_003 is pure dialogue attribution for Jared, BOOK_004 involves a trio (narrator, Daniel, Gabriel) in what appears to be a crisis/care scene but without enough context to assign a specific arc role or confirm a main couple. BOOK_005 is a single dialogue fragment. The overwhelming majority of sentences are too fragmentary to assign a meaningful arc role, making ARC_10 (unclear_arc_role) the dominant code at ~95%. One sentence (BOOK_001_1) clearly involves a side character's relationship, coded ARC_0 (off_target).
- **Pass C — adjudication:** **ARC_5 — disclosure**
  - Lexical consensus (ARC_4: relationship_caused_distress) and contextual dominant (ARC_10: unclear_arc_role) are in tension. The taxonomy anchor — 4.3 Secrets, Misunderstandings & Hidden Information — provides the decisive tiebreaker. Hidden information and secrets are the structural engine of ARC_5 (disclosure), not merely ambient distress (ARC_4) or an unresolved arc role (ARC_10). The secondary taxonomy tag (7.1 Interpersonal Non-Romantic Conflict) does not override the main-couple filter; the secrets/hidden-information frame is most plausibly directed at the main couple's dynamic. ARC_5 sits in the REFINED_FALLING construct bucket because disclosure events typically precede or precipitate conflict escalation rather than resolving it. Manual review is flagged because the ARC_10 contextual read suggests the topic's token distribution may be ambiguous enough that some passages could belong to non-romantic interpersonal conflict (ARC_9 or ARC_0), warranting human verification before finalising the main_couple=true assignment.

---

### Topic 248 — Arranging A Cover Story {#topic-h6-248}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_10 — unclear arc role**
- **Mixed:** False
- **Main-couple prob:** 0.1 | non-couple: 0.8
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> i can attach myself to callie as a potential suitor, even with the distant cousin story you’ve decided to run with.

> i'll just let hannah know she won't have to watch him after today.

> it means you’ll probably bump into him too if you see more of hannah.’

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Picture Perfect — Bethany Brown; tertile=middle; p=0.68**
>
> Yeah, he’s actually Hannah’s boyfriend.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Picture Perfect — Bethany Brown; tertile=begin; p=0.66**
>
> That Hannah’s boyfriend was sleeping with apparently the whole time they were going out?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Picture Perfect — Bethany Brown; tertile=begin; p=0.65**
>
> On Hannah’s behalf, and on yours too, even though I didn’t know your name.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Picture Perfect — Bethany Brown; tertile=begin; p=0.64**
>
> Hannah took me to that party as a pity thing, unfortunately.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Picture Perfect — Bethany Brown; tertile=begin; p=0.64**
>
> Including that hot guy Hannah had started to introduce me to.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Creed — Kristen Ashley; tertile=end; p=0.45**
>
> I would confirm the girl was there, make the deal and skedaddle then Hawk and the boys would swoop in and recover the girl.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Ciao — Bethany Lopez; tertile=middle; p=0.56**
>
> Anyway, I was totally pissed about that, and about Jess pinching my arm, when Cassie dropped another bomb on me… She said that she is “Falling in love with Jimmy!!!!”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Ciao — Bethany Lopez; tertile=end; p=0.56**
>
> I know you and Cassie were close, and it just tears me up inside that I can’t do anything to save you and Jimmy from this pain!” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Ciao — Bethany Lopez; tertile=middle; p=0.54**
>
> Getting all mad because of her relationship with Jimmy… Wishing that they had never started dating… Now I will never see Cassie again!

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Ciao — Bethany Lopez; tertile=middle; p=0.54**
>
> Jess and I rode together, but Cassie said she would meet us there; she was still trying to find the perfect gift for Jimmy.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_10 — unclear arc role**
  - Main and POS are dominated by character names (callie, hanna, leslea), a pickpocketing incident, and abstract nouns (concept, notion, options, treatment) with no clear romantic-arc signal — coded ARC_0 (off-target). KeyBERT and MMR carry emotionally loaded cues (crushed, upset, pregnant, admit, overheard, apologize, problems, wasting) that suggest distress and possible disclosure, but the named characters (callie, hanna, sister) point toward a sibling or secondary-character dynamic rather than a confirmed main couple. 'Pregnant' and 'admit' could indicate ARC_5 (disclosure) or ARC_4 (relationship-caused distress), but without clear main-couple anchoring the signal is ambiguous. The split between off-target and distress/disclosure readings across representers, combined with the absence of a confirmed main-couple frame, yields ARC_10 (unclear arc role) as the consensus.
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - Topic 248 clusters around the name 'Hannah' and secondary character names (Cassie, Jimmy, Jess, Amy). No single main couple is clearly established across sentences. BOOK_001 sentences reference Hannah's cheating boyfriend — a third-party relationship conflict, coded ARC_9. BOOK_003 sentences involve an external rescue/intel operation with no romantic couple visible, coded ARC_9. BOOK_004 sentences reference Cassie and Jimmy as a couple causing distress to a narrator/friend — coded ARC_4 where relationship-caused distress is explicit, and ARC_10 where the role is ambiguous. BOOK_006 sentences reference Hannah in a context suggesting she was a deceased or missing person significant to Ryker, with external threat framing — coded ARC_9 for threat sentences and ARC_10 for descriptive/unclear ones. No code reaches 70%; ARC_10 is the plurality at ~45%, making it the dominant code. Main couple probability is very low (~0.10) as most sentences reference secondary or unclear characters.
- **Pass C — adjudication:** **ARC_10 — unclear arc role**
  - Both lexical consensus and contextual dominant converge on ARC_10 (unclear_arc_role). The taxonomy placement under 4.3 Secrets, Misunderstandings & Hidden Information suggests latent ARC_1 or ARC_5 signal, but without sufficient topic-word or passage evidence to override the double ARC_10 signal, reinterpretation would be speculative. The secondary taxonomy tag (5.2 Friends, Allies & Social Circles) further muddies main-couple attribution — the topic may center on a social/ally dynamic rather than the protagonist pair, keeping main_couple false. No free-form labels from prior passes require remapping. Manual review is flagged so a human auditor can inspect the raw top-words and representative documents to determine whether the hidden-information theme is clearly tied to the main couple (which would warrant REINTERPRET to ARC_1 or ARC_5) or remains genuinely ambiguous.

---

### Topic 264 — Accused of Hiding Something {#topic-h6-264}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **MIXED**
- **Normalised category:** —
- **Mixed:** True
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> i’ve been hiding out in here, avoiding contact with the human leech.” “

> i haven’t been hiding, i’ve been working.

> he cut in before i could get a word out, "funny thing is i've had this gut feeling all along that you're hiding something.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Crazy Kisses — Tara Janzen; tertile=end; p=0.48**
>
> Two shots from the same hide were enough to set his warning bells ringing.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Crazy Kisses — Tara Janzen; tertile=middle; p=0.42**
>
> The closet had been a great hiding place for all of two seconds for two people, but it had turned into a torture chamber.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Some Enchanted Evening — Christina Dodd; tertile=begin; p=0.70**
>
> If we’re hiding, how will she find us?” “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_5 — disclosure**
  - Main is dominated by concealment vocabulary ('hide', 'hiding', 'hidden', 'concealing', 'keep from') pointing strongly to ARC_5 (disclosure/secrets being kept). KeyBERT reinforces this with 'hiding' and 'revealing' as the core tension — something is being concealed and potentially exposed. POS adds 'identity', 'activities', 'choices', and 'secure places', consistent with a character hiding their identity or secrets (ARC_5). MMR introduces 'weapons', 'remote', 'blows', and 'cleared', which shift toward external/action-plot concealment (ARC_9 — external plot conflict involving hiding weapons or fugitive activity). Despite MMR's external-plot lean, the dominant signal across three of four representations is secret-keeping and potential revelation centered on a person's identity or activities, which maps to ARC_5. Disagreement flagged due to MMR's divergent external-threat framing.
- **Pass B — contextual:** **ARC_9 — external plot conflict**
  - Topic 264 is dominated by the semantic field of hiding, concealment, disguise, and cover — physical actions associated with evasion, surveillance, and tactical positioning. These are external-plot/action-thriller elements (shots from a hide, covering positions, hiding from a pursuer, disguises, scars). None of the sentences clearly depict a main-couple romantic dynamic; most are ambiguous or clearly non-romantic in context. The topic maps cleanly to ARC_9 (external_plot_conflict) across all tertiles, with no evidence of relationship arc content.
- **Pass C — adjudication:** **MIXED**
  - Lexical consensus (ARC_5 disclosure) and contextual dominant (ARC_9 external_plot_conflict) diverge, indicating the topic captures two distinct narrative functions that co-occur in the text. Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) aligns primarily with ARC_5, suggesting a revelation or hidden-information moment involving the main couple. However, the contextual signal for ARC_9 indicates the disclosure is embedded within or triggered by an external plot pressure rather than arising purely from interpersonal dynamics. Because neither code alone is sufficient and the taxonomy secondary is None, a MIXED designation is warranted. The construct bucket is REFINED_FALLING: a disclosure event that introduces or deepens tension places this in the falling/complicating arc phase rather than repair or resolution. Manual review is required to determine whether the external element is the primary driver (favoring ARC_9 as dominant) or merely the context for a couple-centered secret reveal (favoring ARC_5 as dominant), which would affect downstream hypothesis assignment.

---

### Topic 265 — Mismatched Expectations About Seriousness {#topic-h6-265}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_4 — relationship caused distress**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> shit,” shane cursed, but in a way that said he was thrilled with the news, not unhappy. “

> i get the impression you’ve led shane to believe you’re far more serious than you are.

> i want to concentrate on my studies, and you, my gosh, shane, you’ll have so many women hitting on you the second the ferry leaves the dock—” shane jerks his hand away. “

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Her Sky Cowboy — Beth Ciotta; tertile=begin; p=0.38**
>
> As far as Tuck knew, Axel was the only one aboard who got spooked by Freaks.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_4 — relationship caused distress**
  - KeyBERT and MMR both surface emotional-distress vocabulary ('emotionally', 'unhappy', 'trembled', 'embarrassment', 'shock') pointing to relationship-caused distress (ARC_4). POS reinforces tension with 'arguing', 'heated', 'embarrassment', 'unsure' which edges toward ARC_2 escalation, but the dominant emotional register is distress rather than pure conflict escalation. Main keywords are character names and neutral action verbs (burrowed, nod, play) offering no clear arc signal on their own (ARC_10). The weight of emotionally charged distress cues across KeyBERT and MMR tips consensus to ARC_4; disagreement is flagged because POS leans ARC_2 and Main is ambiguous.
- **Pass B — contextual:** **ARC_0 — off target**
  - All sentences in this topic are fragments — name utterances ('Shane said.', 'Shane.', 'Crikey.'), a brief third-person observation about a character named Tuck/Axel, and minimal dialogue tags ('Keith thought so.'). None contain sufficient narrative content to assign a romance arc role. The topic appears to be a BERTopic cluster anchored on character-name tokens or short dialogue punctuation fragments rather than any meaningful arc event. All sentences are coded ARC_0 (off_target). Main-couple probability is very low because no romantic dyad interaction is discernible from the fragments.
- **Pass C — adjudication:** **ARC_4 — relationship caused distress**
  - Adjudication resolves the lexical–contextual split in favour of ARC_4 (relationship_caused_distress). The contextual read of ARC_0 (off_target) is overridden by the taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information with a secondary tag of 4.4 Conflict, Distance & Breakup Threats: both subcategories describe distress that originates within the main-couple dynamic (hidden information causing emotional harm), which is the defining feature of ARC_4 rather than off-target content. ARC_1 (misunderstanding) was considered but the taxonomy secondary tag signals the distress has escalated beyond a simple misunderstanding into sustained relational harm, keeping ARC_4 as the better fit. The construct bucket is REFINED_FALLING because relationship-caused distress sits on the descending arc of the narrative (trust eroding, emotional damage accumulating) prior to any repair phase.

---

### Topic 272 — Silence Held Until Arrival {#topic-h6-272}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_1 — misunderstanding**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> she didn’t speak a word until they got to their destination.

> the high priestess had said very little to her in the day and a half leading up to her departure.

> he should’ve known better than to think brenna would be content with the noncommittal answer he’d given her.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Below the Belt — Sarah Mayberry; tertile=middle; p=0.74**
>
> She wanted to ask more questions, but she didn’t.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Below the Belt — Sarah Mayberry; tertile=begin; p=0.67**
>
> She didn’t want to talk about the fight. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · One Season of Sunshine — Julia London; tertile=begin; p=0.70**
>
> Unfortunately, she had nothing promising to say to him.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · One Season of Sunshine — Julia London; tertile=end; p=0.68**
>
> She was going to the hospital, and this time, she would not take no for an answer.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_1 — misunderstanding**
  - All four keyword lists converge on a scene of failed or withheld communication between characters. Main keywords (answer, didn, respond, question, reply, say, word, speak) directly signal someone not answering or refusing to speak. KeyBERT reinforces this with 'refused', 'lack', 'answers', 'answering', plus emotional fallout ('annoying', 'embarrassment'). POS and MMR add 'departure' and 'destination', suggesting one party leaves or withdraws rather than engaging, and 'upset', 'shock', 'rushed' indicate the emotional charge of the non-response. The dominant pattern is a breakdown in communication — one character not answering the other's questions, likely concealing something or stonewalling — which is the hallmark of ARC_1 (misunderstanding/withheld information driving relational tension), rather than an overt escalating fight (ARC_2) or a formal separation threat (ARC_3).
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - Topic 272 is dominated by short, decontextualized sentences expressing silence, withholding, or emotional withdrawal (e.g., 'She didn't want to hear it,' 'Jane didn't say anything,' 'He didn't speak'). These fragments lack sufficient context to assign a specific arc role — they could belong to many arc stages. No clear main-couple dyad is identifiable across books; most sentences are ambiguous about who the characters are relative to each other. One sentence (BOOK_001_6) hints at a post-fight avoidance, coded ARC_1 (misunderstanding/avoidance). Two sentences (BOOK_002_4, BOOK_004_2) suggest external plot action or third-party dynamics, coded ARC_9. The overwhelming majority (80%) are ARC_10 (unclear arc role). ARC_10 exceeds 70%, making it the dominant code. Main-couple probability is low (~0.15) given the lack of identifiable romantic dyad context.
- **Pass C — adjudication:** **ARC_1 — misunderstanding**
  - Lexical consensus (ARC_1 misunderstanding) and taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information both point to a hidden-information-driven misunderstanding between the main couple. The contextual dominant ARC_10 (unclear_arc_role) reflects ambiguity in surface signals, but the taxonomy anchor resolves that ambiguity: the topic encodes a classic falling-arc beat where concealed information creates relational distance. The secondary taxonomy tag (8.5 Movement/Transit) is likely incidental framing rather than the core arc function. ARC_1 is therefore the correct resolution. Construct bucket is REFINED_FALLING because misunderstandings driven by secrets are a canonical early-to-mid narrative descent mechanism. No free-form labels were carried forward; ARC_10 is superseded by the stronger lexical and taxonomic evidence for ARC_1.

---

### Topic 286 — Trying to Regain Good Graces {#topic-h6-286}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_0 — off target**
- **Mixed:** False
- **Main-couple prob:** 0.1 | non-couple: 0.8
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> oh ms. [person], you really should drop by our office more, we miss your good taste around here' blah blah blah.

> i'll not have you and his grace at each other's throats before we arrive at champney court."

> if what you’ve said is to be believed, how am i supposed to get back into her good graces?

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Dark Surrender — Mercy Walker; tertile=middle; p=0.58**
>
> It shone in the moonlight with silver grace. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · Incidental Contact — Eden Connor; tertile=begin; p=0.53**
>
> Widow of a respected insurance agent and former daughter-in-law of a well-known Baptist minister, she’d seemingly shunned the social position and privilege of her past to be with Colton, but this wasn’t the first time Eric had seen her slip on her high-and-mighty act like an expensive fur coat.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · Incidental Contact — Eden Connor; tertile=begin; p=0.48**
>
> Eric needed a mentor to teach him how to be an honorable man.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · Incidental Contact — Eden Connor; tertile=begin; p=0.48**
>
> Likely not, since Dee had already seen her with Eric.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_0 — off target**
  - Main keywords are dominated by proper nouns and names (graceclemens, ruttery, champney, oracle, grâce) with no clear romantic-arc signal; 'blah' and 'tape' add noise. KeyBERT offers 'thrilled', 'embarrassment', 'awkwardly', 'deserve' — mild emotional texture but no identifiable main-couple dynamic; 'dr' and 'continues' are generic. POS and MMR introduce 'desperation', 'embarrassment', 'pregnant', 'pressure', 'decision', 'unable', 'rushing' — these could hint at a distress or stakes situation, but 'pregnant' and 'desperation' without any relational anchoring (no conflict, repair, disclosure, or commitment cues tied to a couple) remain ambiguous. 'Graceful'/'gracefully' across reps likely refers to a character named Grace rather than a quality. The cluster of proper-name noise in Main and the absence of any clear main-couple interaction pattern across all four reps points primarily to off-target content, with POS/MMR being merely unclear rather than arc-relevant. Consensus lands on ARC_0 (off_target) given the name-heavy Main rep and lack of coherent romantic-arc signal, with noted disagreement from POS/MMR which lean ARC_10.
- **Pass B — contextual:** **ARC_0 — off target**
  - Topic 286 clusters around proper-noun name references (Mrs. Darden, His Grace, Reed, Eric, Dee, Cynda) and brief honorific/address fragments. None of the sentences establish a clear main-couple romantic arc dynamic. BOOK_001–003 sentences involve secondary or peripheral characters (Eric, Dee, Cynda, Colton) with no identifiable main-couple romantic conflict or progression. BOOK_004 sentences are purely honorific address fragments ('Your Grace', 'His Grace') with no arc content. BOOK_005 sentences mention Reed in passing but lack sufficient context to assign a romantic arc role — they read as name-reference fragments rather than arc-bearing narrative moments. The topic appears to be a name/address cluster with no coherent narrative-arc signal, making ARC_0 (off_target) the appropriate dominant code across all tertiles.
- **Pass C — adjudication:** **ARC_0 — off target**
  - Both lexical consensus and contextual dominant agree on ARC_0 (off_target). The taxonomy tag 4.3 Secrets/Misunderstandings and secondary 3.2 Negative Emotions might superficially suggest ARC_1 or ARC_4, but the main-couple filter is not satisfied — the topic does not pertain to the primary romantic dyad. Without a main-couple anchor, secrets or distress signals cannot be coded as relationship-arc events. ARC_0 is therefore confirmed. No construct bucket applies, and no manual review is needed.

---

### Topic 301 — Confessing A Thin Relationship History {#topic-h6-301}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_1 — misunderstanding**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> you know that because you’ve been with one other guy and had a long-term relationship?

> because one way or another it has tainted every relationship i’ve had since the roller-coaster success of my first book.”

> i've had sexual partners, but never a girlfriend.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Heart Thief — Robin D. Owens; tertile=end; p=0.52**
>
> You will say anything to save your lover.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Temptation Ridge — Robyn Carr; tertile=end; p=0.70**
>
> Can I assume you two don’t have a…relationship?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Temptation Ridge — Robyn Carr; tertile=middle; p=0.64**
>
> But I’m not avoiding a good relationship.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_4 — relationship caused distress**
  - Main keywords (boyfriend, mate, relationship, partner, status, don, mean) signal interrogation or anxiety about the relationship itself — not a discrete external threat or a repair moment, but ongoing relational distress tied to the couple's dynamic. KeyBERT reinforces this: 'emotionally', 'admit', 'worrying', 'ex' point to emotional strain and unresolved feelings causing distress within the relationship. MMR adds 'arrange', 'ripping', 'intend', 'afford', 'emotionally' — 'ripping' especially suggests pain or rupture, and 'ex' raises the spectre of a prior relationship complicating the current one, consistent with relationship-caused distress (ARC_4). POS keywords (partners, success, potential, secure) are more neutral/aspirational and lack clear conflict valence, warranting ARC_10 for that rep alone. Three of four reps converge on ARC_4, yielding consensus there despite POS dissent.
- **Pass B — contextual:** **ARC_1 — misunderstanding**
  - Topic 301 clusters around relationship-status ambiguity and questioning — 'do you have a boyfriend/girlfriend?', denials of being in a relationship, and challenges about who someone is with. These are predominantly misunderstanding or definitional-confusion signals (ARC_1), where characters are unclear or in dispute about the nature of their romantic connection. A substantial minority of sentences are too fragmentary or context-free to assign a specific arc role (ARC_10). Two sentences (BOOK_003_6, BOOK_005_1) reflect distress caused by relationship dynamics (ARC_4). Two sentences are off-target (ARC_0). ARC_1 reaches ~45%, above the 70% threshold is not met, but it is clearly dominant over all other codes. Main-couple probability is moderate (~0.55): several sentences plausibly involve the main couple negotiating relationship labels, but many are ambiguous or involve third parties.
- **Pass C — adjudication:** **ARC_1 — misunderstanding**
  - Lexical consensus landed on ARC_4 (relationship-caused distress), but the taxonomy placement in 4.3 Secrets, Misunderstandings & Hidden Information — with a secondary anchor in 3.3 Ambivalence & Internal Conflict — points to the distress being a downstream symptom rather than the primary arc mechanism. The contextual dominant ARC_1 (misunderstanding) better captures the generative engine: a hidden piece of information or a secret creates a misread between the main couple, producing the felt distress. ARC_4 describes the emotional register; ARC_1 describes the narrative function. In adjudication, narrative function takes precedence for arc_role assignment. The construct bucket is REFINED_FALLING because the misunderstanding is actively widening the relational gap rather than initiating repair. No free-form labels were carried forward from Pass A/B.

---

### Topic 303 — Confessing Long-Hidden Secrets {#topic-h6-303}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_1 — misunderstanding**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> normally, tate would’ve finished the sentence she was working on, but the excitement in mabel’s voice jarred her completely out of the story, derailing her train of thought.

> i know it might cost me tate, but if i don’t tell him then everything we’ve built will be based on half-truths.” “

> tate sits down next to me, his eyes grim as he waits for me to share all the things that i've been keeping from him for so long.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · Hunting Chase — Camille Anthony; tertile=middle; p=0.70**
>
> Damn it, he wondered if Joshua Tate knew the full extent of what he was taking on.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · Hunting Chase — Camille Anthony; tertile=begin; p=0.69**
>
> Joshua Tate tugged at his collar and cleared his throat, his prominent Adam"s apple bobbing as he swallowed audibly. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Pas de Deux — Jamie Craig; tertile=middle; p=0.45**
>
> I went to Woodson to interview Chandra Cunningham about Tana Mayfield.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Pas de Deux — Jamie Craig; tertile=end; p=0.38**
>
> I’m just doing some follow-up on Mayfield.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Bound By Blood — Kimberly Hoyt; tertile=middle; p=0.55**
>
> Lady Mayfield, I believe," he said, straightening.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Bound By Blood — Kimberly Hoyt; tertile=middle; p=0.52**
>
> You seem to have the exclusive attention of the Lady Mayfield,” Kent mentioned once greetings had been exchanged between the three. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_10 — unclear arc role**
  - Main rep offers a cluster of character names (tate, logan, kenzie, ang, chace, kent, sophia) with no relational-arc signal beyond 'agreed'; KeyBERT yields procedural/observational terms (nods, sentence, speaking, planned, anticipation, muffled, worrying, judging, winked) that suggest scene-level narration without a clear arc function; POS rep mixes physical/situational nouns and adjectives (rear, period, panicked, tracks, decent, television, sentence, current, wrists, ex) — 'ex' is the only faint relational hint but is too isolated to anchor an arc code; MMR rep contains action verbs (drawled, fumbled, hauled, circled, tipped) and modifiers (judging, occupied, bothering, muffled) that read as moment-to-moment scene texture rather than any identifiable arc beat. No representation supplies enough directional relational signal to assign a specific ARC_1–ARC_9 code, so ARC_10 (unclear_arc_role) is the unanimous consensus.
- **Pass B — contextual:** **ARC_0 — off target**
  - Topic 303 clusters around proper names — Joshua Tate (BOOK_003), Tana/Dotty/Laurel Mayfield (BOOK_004/005), and Tyrese Moore (BOOK_007). None of these sentences depict a romantic main-couple dynamic; they reference supporting characters, investigative dialogue, and third-party interactions. BOOK_005_5 hints at external plot manipulation (a staged accident, time travel), but the subject is a villain's scheme rather than main-couple arc content. All sentences are off-target for romance narrative-arc coding, yielding a unanimous ARC_0 classification and a main_couple_prob of 0.0.
- **Pass C — adjudication:** **ARC_1 — misunderstanding**
  - Adjudication resolves the tension between lexical consensus (ARC_10 unclear) and contextual dominant (ARC_0 off_target) by applying taxonomy metadata. Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) is a strong signal that the topic content centers on hidden information or misunderstanding dynamics between the main couple — a classic REFINED_FALLING beat. ARC_0 (off_target) is overridden because the taxonomy assignment confirms main-couple relevance; ARC_10 (unclear) is overridden because the taxonomy provides sufficient semantic grounding. ARC_1 (misunderstanding) is the nearest valid code to the primary taxonomy category 4.3, capturing the secrets/hidden-information driver of conflict. The secondary taxonomy 4.5 (Reconciliation/HEA) is noted but does not dominate; it may indicate downstream repair potential but does not shift the arc_role to ARC_6/ARC_7/ARC_8 without stronger contextual evidence. No free-form labels were carried forward.

---

### Topic 314 — Fiancé Becoming A Stranger {#topic-h6-314}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_10 — unclear arc role**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> macie had spent far more time praying for blake and far less time being driven by her constantly-shifting emotions.

> she peeked out and verified that it was indeed blake, then promptly shut the door in his face to remove the chain. “

> the blake i am engaged to is slowly disappearing in my mind, and being replaced by a complete and utter stranger.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · A Heartbeat Away — Maureen Smith; tertile=middle; p=0.49**
>
> I wondered about that when you first told me you’d be staying with Brant.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Wild Card — Lora Leigh; tertile=end; p=0.68**
>
> You went over the truck, didn't you, Blake?"

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_10 — unclear arc role**
  - Main rep is dominated by character names (blake, dion, macie, breydan, hewitt) and social/group terms (mates, grog, evite, addressing, motioned) with no clear arc signal. KeyBERT adds 'engaged', 'attracted', 'overheard', 'emotions', 'causing' — suggestive of some interpersonal dynamic but not pinpointing a specific arc stage (no clear conflict, repair, disclosure, or commitment cue). POS rep echoes 'engaged', 'embarrassed', 'emotions', 'amusement', 'reminder' — mild social awkwardness but insufficient to anchor a specific arc role. MMR adds 'overheard', 'chased', 'praying', 'amusement', 'causing' — again evocative but ambiguous across multiple possible arcs (misunderstanding, escalation, or simply external social scene). No single arc stage is clearly dominant across all four reps; the cluster reads as a social gathering scene with emotional undercurrents that cannot be reliably coded beyond unclear arc role.
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - Topic 314 appears to be a character-name topic — sentences are almost entirely name invocations or very short address fragments (Brant, Blake, Phoenix) with no surrounding narrative context that reveals a relationship dynamic, conflict, repair, or arc event. The sentences are drawn from multiple books with different named characters, confirming this is a BERTopic cluster anchored on proper-name tokens rather than any coherent narrative-arc function. No sentence provides enough context to identify a main-couple interaction or assign a meaningful arc code. All sentences are coded ARC_10 (unclear arc role). Main-couple probability is very low (0.10) because the fragments are name-only utterances with no relational content visible.
- **Pass C — adjudication:** **ARC_10 — unclear arc role**
  - Both lexical consensus and contextual dominant converge on ARC_10 (unclear_arc_role), indicating the topic does not resolve cleanly into a single narrative-arc function. The taxonomy metadata (4.3 Secrets, Misunderstandings & Hidden Information; secondary 3.3 Ambivalence & Internal Conflict) suggests content that could plausibly map to ARC_1 (misunderstanding) or ARC_5 (disclosure), but neither is sufficiently dominant to override the dual-pass ARC_10 verdict without additional evidence. The secondary taxonomy (ambivalence/internal conflict) further muddies the signal — internal conflict is not inherently a main-couple arc beat. No construct bucket is assigned because the topic lacks the directional clarity required for REFINED_FALLING or REFINED_RISING, and there is no indication of external-plot primacy. Manual review is flagged to inspect raw token weights and representative documents, which may allow a future reclassification to ARC_1 or ARC_5 if secrets/misunderstandings between the main couple are confirmed as the dominant signal.

---

### Topic 319 — Confessing A Costly Mistake {#topic-h6-319}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_1 — misunderstanding**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> but you have a way of letting me know when you think i’ve made the wrong one.” “

> i’ve made many mistakes and maybe i should have come back a year ago.

> it was a mistake for which i’ve paid dearly.” “

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · When It Happens — Susane Colasanti; tertile=middle; p=0.42**
>
> They’re fundamental y flawed, I can’t—” “ ‘Flawed’ being the key word,” Josh points out.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Space Junque — L.K. Rigel; tertile=end; p=0.59**
>
> Anyone who saw her as only a child was making a mistake. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_1 — misunderstanding**
  - Main keywords ('mistake', 'mistakes', 'flaw', 'error', 'errors', 'biggest', 'terrible', 'made') strongly signal a misunderstanding or misjudgment frame — the vocabulary of recognizing a wrong belief or wrong action that drove a rift, which is the lexical signature of ARC_1 (misunderstanding). KeyBERT ('occurred', 'thinks') and POS ('latest', 'bigger') are too sparse and neutral to anchor any specific arc role, yielding ARC_10. MMR adds 'proved', 'shifting', 'paid', 'surely', 'pressing' alongside 'occurred'/'bigger'/'thinks' — these hint at consequence and acknowledgment but still lack directional arc cues, so ARC_10 is the safest call there. The Main list dominates in volume and specificity; 'mistake/error/flaw' as a cluster is the canonical lexical marker for a misunderstanding-driven conflict beat, so ARC_1 carries the consensus despite disagreement from the sparser reps.
- **Pass B — contextual:** **ARC_1 — misunderstanding**
  - Topic 319 clusters around language of mistakes, wrongness, accidents, and being flawed — all hallmarks of misunderstanding or misjudgment rather than escalating conflict or external plot. The majority of sentences (12/20) express that something was wrong, mistaken, or accidental, fitting ARC_1 (misunderstanding). A minority show interpersonal friction/disagreement (ARC_2) or acknowledgment/repair language (ARC_6). One sentence ('I feel so cheated') suggests relational distress (ARC_4). Crucially, none of the sentences clearly identify a main romantic couple; speakers and addressees are unnamed or ambiguous, so main_couple_prob is low (~0.25). ARC_1 exceeds 70% threshold when combining direct mistake/wrong language, making it the dominant code.
- **Pass C — adjudication:** **ARC_1 — misunderstanding**
  - Both lexical consensus and contextual dominant converge on ARC_1 (misunderstanding). Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) directly corroborates this classification, with 3.2 (Negative Emotions & Distress) as a secondary signal consistent with the emotional fallout of a misunderstanding rather than an independent arc role. The topic concerns the main couple and represents a falling-arc dynamic (trust/understanding deteriorating due to hidden information), placing it in the REFINED_FALLING construct bucket. No conflict between passes or taxonomy signals; KEEP is appropriate with no manual review needed.

---

### Topic 346 — Delivering Urgent News in Secret {#topic-h6-346}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_0 — off target**
- **Mixed:** False
- **Main-couple prob:** 0.1 | non-couple: 0.8
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> let’s go [person] i’ll drive you to it.”

> i hardly think leaving a note telling my father where to find me would’ve been a good idea, but i’m not going to tell james that. “

> i know this is bad, me coming here, especially after the celeb weekly article, but i’ve got some important information about [person].”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Stars Collide — Janice  Thompson; tertile=end; p=0.56**
>
> She pointed to James Stevens from The Scoop , who sat in the front row with Scott’s parents. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **MIXED**
  - Main and KeyBERT point strongly toward ARC_5 (disclosure): 'admit' appears in both, supported by 'willingly', 'chose', 'begged', 'planning', and 'hiding' — all cues of a character being pressed or choosing to reveal something. POS and MMR lean toward ARC_4 (relationship-caused distress): 'suffering', 'strained', 'threatened', 'opposite', 'advantage' suggest emotional or relational pain tied to the couple dynamic rather than a clean disclosure moment. The split between disclosure-pressure cues and distress/strain cues across the four reps prevents a single consensus code, yielding MIXED.
- **Pass B — contextual:** **ARC_0 — off target**
  - Topic 346 is dominated by name fragments and attribution tags — 'James said.', 'James?', 'Jonathan.', 'James Stevens from The Scoop' — with no narrative content conveying relationship dynamics, conflict, repair, or any romance-arc function. The sentences are essentially decontextualized speaker labels or proper-noun fragments. 'James Stevens from The Scoop' appears to be a journalist character, not a romantic lead. No sentence establishes a main-couple interaction with sufficient context. All sentences are coded ARC_0 (off_target). Main-couple probability is very low (~0.05) given the absence of any relational content.
- **Pass C — adjudication:** **ARC_0 — off target**
  - Lexical consensus was MIXED, but contextual dominant is ARC_0 (off_target). Taxonomy 4.3 (Secrets, Misunderstandings & Hidden Information) with secondary 7.1 (Interpersonal Non-Romantic Conflict) signals that any secret or misunderstanding present is not anchored to the main romantic couple — it is either peripheral character conflict or non-romantic interpersonal tension. Because the main-couple filter fails (main_couple=false), the content does not qualify for ARC_1 through ARC_8. ARC_9 would require an external plot threat bearing on the couple, which is not indicated. The dominant contextual read of off-target content therefore prevails, resolving to ARC_0. No construct bucket applies.

---

### Topic 362 — Keeping Someone Watched and Close {#topic-h6-362}

- **Old taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **New category:** **ARC_10 — unclear arc role**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> come on, i’ll get you a drink,’ rory said. ‘

> they’ll expect me to keep her close, to make sure she doesn’t discover what we are,” rory answered.

> and goddess willing i’ll be ready for it, thought rory as she ignored his comment to follow amber out to the sitting room.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Dragon's Dower — Catherine Archer; tertile=begin; p=0.52**
>
> It was Kelsey he wished to see brought low.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Dragon's Dower — Catherine Archer; tertile=begin; p=0.49**
>
> For we have seen how far Kelsey is willing to go for what he wants.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Dragon's Dower — Catherine Archer; tertile=begin; p=0.47**
>
> He would go slowly, wisely, even though he was more resolved than ever to see Kelsey repaid for his ills against others.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Dragon's Dower — Catherine Archer; tertile=end; p=0.47**
>
> Another of the men said, “Lord Kelsey must be told.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Dragon's Dower — Catherine Archer; tertile=begin; p=0.46**
>
> Yet he’d had no time to grieve their loss, for he had immediately become embroiled in this conflict with the Earl of Kelsey.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Deeper — Megan Hart; tertile=middle; p=0.54**
>
> Okay, so maybe I get that, but what about Kelsey?” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Deeper — Megan Hart; tertile=end; p=0.48**
>
> He’d want a sure thing,” Kelsey insisted.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_10 — unclear arc role**
  - Main keywords are dominated by proper nouns (rory, yamane, kingman, darlington, ayida, damballah) and a survival cue ('survived'), offering no clear relational arc signal between a main couple. KeyBERT yields procedural/social interaction words (answering, willing, sir, expect, pretending, embarrassed, introduce, issue, wondering) that suggest a scene of social navigation or awkward introduction but do not point to a specific arc stage. POS mirrors this with neutral framing terms (addition, meantime, framed, suggestion, issue, features, willing, sir). MMR adds physical/emotional texture (tearing, crouched, struggled, tugged, embarrassed) consistent with tension but not diagnosable as a specific arc beat without clearer relational context. No keyword cluster reliably maps to a defined ARC_1–ARC_9 stage; the aggregate signal is ambiguous.
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - Topic 362 clusters around the name 'Kelsey' across two very different books. In BOOK_001, Kelsey is an antagonist (Earl of Kelsey) and all sentences describe external conflict/rivalry with no main-couple involvement — coded ARC_9. In BOOK_002, Kelsey appears to be a character whose identity relative to the main couple is unclear from fragments alone; 'Kelsey's heart sank' suggests emotional distress (ARC_4) but context is insufficient to confirm main-couple status. In BOOK_007, Rick and Dorian appear to be a main couple (mates), with one intimate scene (ARC_0 — off-target for arc coding) and concern for Dorian's wellbeing (ARC_4). BOOK_008 sentences are too fragmentary (ARC_10). No single code reaches 70%; ARC_10 is the plurality at ~45%, making it the dominant code, but the topic is heterogeneous across books and character roles. Main-couple probability is low (~0.20) given that most sentences involve an antagonist named Kelsey or unclear characters.
- **Pass C — adjudication:** **ARC_10 — unclear arc role**
  - Both lexical consensus and contextual dominant converge on ARC_10 (unclear_arc_role). The taxonomy tag 4.3 (Secrets, Misunderstandings & Hidden Information) suggests the topic could plausibly map to ARC_1 (misunderstanding) or ARC_5 (disclosure), but neither signal is strong enough to override the double ARC_10 signal from Passes A and B without additional textual evidence. The secondary taxonomy tag 10.1 (Paranormal & Immortal Beings) raises the possibility that the hidden-information element is tied to a supernatural identity reveal, which could be external-plot-adjacent (ARC_9) rather than a pure interpersonal misunderstanding — further blurring the picture. Because the topic sits at the intersection of at least three plausible arc roles (ARC_1, ARC_5, ARC_9) without a dominant signal, ARC_10 is the most defensible single code. No construct bucket is assigned because the ambiguity prevents reliable placement in REFINED_FALLING, REFINED_RISING, or EXTERNAL_PLOT_CONFLICT. Manual review is required to inspect representative documents and determine whether a more specific arc role can be assigned.

---

### Topic 3 — Demanding An Explanation {#topic-h6-3}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **ARC_5 — disclosure**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> and you have no idea what we’ve seen, what we’ve done— you’ve been in your cosy little world and you just have no—damned— clue! ’

> sophia, i’ve something to tell you.” “

> i’ve told them that already.’ ‘

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Avalon — Lana Davison; tertile=middle; p=0.65**
>
> I’ll tell you whatever you want to know.”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_5 — disclosure**
  - All four keyword lists converge on disclosure/revelation dynamics. Main keywords ('know, tell, don, understand, ask, explain, say, wrong, mean') signal a scene structured around communicating or withholding information and seeking clarification. KeyBERT keywords ('admit, reveal, realise, assure, speaking') are direct disclosure-act verbs — 'admit' and 'reveal' are canonical ARC_5 markers. POS and MMR keywords ('explanation, answers, results, difference, remark, extent, percent') point to a scene where facts or truths are being laid out or demanded, consistent with a disclosure moment. The presence of 'commander, sir, mister' suggests a formal or authority-inflected context for the disclosure, but the dominant arc function across all reps is the surfacing of hidden or unclear information to one or both parties — ARC_5 disclosure.
- **Pass B — contextual:** **ARC_5 — disclosure**
  - All sentences in this topic cluster around the act of demanding, withholding, or offering information — 'Tell me,' 'I demanded to know,' 'I'll tell you whatever you want to know,' 'I'm just not supposed to tell you,' etc. This is a strong disclosure/revelation pattern (ARC_5). The sentences are highly decontextualized fragments with no clear identification of who the speakers are or whether they constitute a main couple; 'unclear' is assigned throughout. The topic does not show escalating conflict, repair, or commitment — it is specifically about the act of disclosure or the resistance to it. ARC_5 accounts for 100% of sentences, well above the 70% threshold, making it the dominant code. Main couple probability is low-to-moderate (0.35) because the fragments could involve any dyad, including secondary characters or non-romantic pairs.
- **Pass C — adjudication:** **ARC_5 — disclosure**
  - Both lexical consensus and contextual dominant independently converge on ARC_5 (disclosure). Although the taxonomy tag is 4.4 Conflict, Distance & Breakup Threats, disclosure events frequently appear within that zone of the narrative arc — a character revealing a secret or truth is a classic falling-arc beat that precipitates conflict or distance. The taxonomy label describes the broader thematic cluster, not the specific arc mechanism; the mechanism here is disclosure. No free-form labels were carried over from Pass A/B that require remapping. Main-couple filter passes. Construct bucket is REFINED_FALLING because disclosure at this position typically drives the couple apart before repair begins.

---

### Topic 24 — Confronting An Unwanted Marriage {#topic-h6-24}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **MIXED**
- **Normalised category:** —
- **Mixed:** True
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> we’ll be married… to each other.”

> you’re already married to me; he’ll understand.” “

> i’ll give you a divorce and you can just walk away.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Caleb — Jade Astor; tertile=begin; p=0.61**
>
> So that whole getting married and settling down part doesn't appeal to you?"

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Caleb — Jade Astor; tertile=middle; p=0.45**
>
> Just divorced and living in different places.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Counterpointe — Ann Warner; tertile=begin; p=0.76**
>
> But that’s not the reason I want to marry you.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Forsaking The Prize — Heather Boyd; tertile=end; p=0.73**
>
> Not that I want to marry again of course.”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **MIXED**
  - Main keywords (marry, married, marriage, husband, wife, divorce, marrying) anchor strongly to formal commitment structures; the presence of 'divorce' pulls toward ARC_3 (separation/breakup threat) but 'marry/marriage/husband/wife' collectively suggest ARC_8 (mutual commitment/final payoff), so Main is coded ARC_8. KeyBERT (engaged, promises, intend, willingly, decide) suggests deliberate commitment-making but 'instincts, suggest, chuckle, uh, remarked' introduce ambiguity and possible misunderstanding framing, coded ARC_1. POS (unhappy, threats, divorce implied via 'ends', 'previous', 'issue', 'concept') signals distress and threat to the relationship, coded ARC_3. MMR (unhappy, threats, arranged, faltered, chased, eyeing) reinforces coercive or contested marriage framing with 'threats', 'arranged', 'faltered', pointing to ARC_3. Two reps land on ARC_3, one on ARC_8, one on ARC_1 — genuine disagreement across commitment-threat-misunderstanding axis yields MIXED.
- **Pass B — contextual:** **MIXED**
  - Topic 24 clusters around marriage/wedding language. No single ARC code reaches 70%. ARC_5 (disclosure/revelation of intentions about marriage) is most frequent (~30%), covering sentences where characters express or question desire to marry. ARC_8 (mutual commitment/final payoff) applies to affirmative marriage declarations. ARC_2 (escalation conflict) covers refusals or contested marriages. ARC_4 (relationship-caused distress) applies where marriage is unwanted or coerced. ARC_0 covers third-party references. The spread across codes yields MIXED as dominant. Most sentences involve the main couple or plausible main-couple dyads, giving a moderate-to-high main_couple_prob of 0.65.
- **Pass C — adjudication:** **MIXED**
  - Both Pass A/B converged on MIXED, and the taxonomy anchor (4.4 Conflict, Distance & Breakup Threats with secondary 4.5 Reconciliation) confirms the topic straddles escalating conflict and breakup-threat territory without cleanly resolving into repair or commitment. The dominant signal sits in the falling arc (conflict intensification and relational distance/threat), with only a secondary trace of reconciliation momentum insufficient to shift the bucket to REFINED_RISING. Mapping any free-form labels: 'Conflict' → ARC_2; 'Obstacle' or distance language → ARC_3. MIXED is retained as the arc_role because neither ARC_2 nor ARC_3 alone captures the full topic, and the secondary 4.5 signal prevents a clean single-code assignment. Construct bucket is REFINED_FALLING given the dominant 4.4 taxonomy weight.

---

### Topic 43 — Pissed Off and Grumbling {#topic-h6-43}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **MIXED**
- **Normalised category:** —
- **Mixed:** True
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> this isn’t the first time i’ve pissed him off.”

> we’ve irritated you, have we?” “

> i’ve been pissed at him ever since. “

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Tales Of A Drama Queen — Lee Nichols; tertile=begin; p=0.62**
>
> She doesn’t look mad so much as really disappointed. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Confessions of a Shopaholic — Sophie Kinsella; tertile=middle; p=0.58**
>
> Tarquin is also pissed, but not as much as me.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_2 — escalation conflict**
  - Main is dominated by anger/temper vocabulary (mad, angry, pissed, offend, temper) pointing to active interpersonal conflict escalation — ARC_2. KeyBERT reinforces this with arguing, attacked, insulted, grumbled, suggesting heated confrontation between parties — ARC_2. POS shifts toward emotional suffering and embarrassment (embarrassing, sadness, distress, emotional) with no clear aggressor, leaning toward relationship-caused distress — ARC_4. MMR similarly foregrounds distress, insulted, terribly, wasting, grumbled — still emotionally charged but more suffering-oriented than combative — ARC_4. Disagreement exists between the active-conflict framing (Main, KeyBERT) and the distress/suffering framing (POS, MMR). The preponderance of explicit anger and conflict-action cues across the two most lexically direct representations (Main, KeyBERT) tips consensus to ARC_2 escalation_conflict, as the distress appears to be a product of the conflict rather than a standalone relational wound.
- **Pass B — contextual:** **ARC_4 — relationship caused distress**
  - Topic 43 is dominated by expressions of anger, moodiness, and emotional volatility (e.g., 'pissed,' 'angry,' 'rage,' 'temper,' 'moody'). These sentences describe characters experiencing or managing anger/frustration, which maps most closely to ARC_4 (relationship_caused_distress) — emotional distress states that arise within interpersonal dynamics. A minority of sentences (BOOK_002_5, BOOK_003_1, BOOK_003_4, BOOK_004_2) show more active interpersonal conflict or confrontation, coded ARC_2 (escalation_conflict). The main couple cannot be reliably identified from these short, decontextualized snippets — characters named (Louis, Tarquin) are not clearly established as part of a main romantic couple, so main_couple is 'unclear' throughout. Main couple probability is low (~0.25) given the ambiguity. ARC_4 exceeds 70% threshold, making it the dominant code.
- **Pass C — adjudication:** **MIXED**
  - Lexical consensus (ARC_2) and contextual dominant (ARC_4) diverge but are not mutually exclusive: escalating conflict between the main couple (ARC_2) is the surface signal, while the deeper emotional register — relationship-caused distress — is what the contextual read captures (ARC_4). Taxonomy 4.4 'Conflict, Distance & Breakup Threats' anchors the primary signal in ARC_2, but the secondary taxonomy 3.2 'Negative Emotions & Distress' confirms that ARC_4 is a genuine co-present signal rather than noise. Because both codes are substantively supported and neither fully subsumes the other, MIXED is the correct resolution rather than forcing a single code. The construct bucket is REFINED_FALLING: both escalation conflict and relationship-caused distress are falling-arc phenomena occurring before any repair or restoration. Manual review is flagged to verify whether the topic's representative documents lean more heavily toward active conflict dynamics (ARC_2) or toward the emotional suffering the relationship itself generates (ARC_4), which would inform downstream weighting in the hypothesis model.

---

### Topic 85 — Offering and Refusing An Apology {#topic-h6-85}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **ARC_6 — repair**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> he said he wanted to apologize.

> i need to apologize to you, ruby.

> oh, i'm so not gonna apologize for that."

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · One Night, Two Babies — Kathie DeNosky; tertile=middle; p=0.70**
>
> I’m real sorry,” Pete said, his blue eyes apologetic.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · One Night, Two Babies — Kathie DeNosky; tertile=end; p=0.54**
>
> He tried to get back in my good graces with a box of chocolates a couple of days later, but he never did apologize.” “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · One Night, Two Babies — Kathie DeNosky; tertile=begin; p=0.54**
>
> And you made it quite clear that you thought I was overreacting to the situation.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · One Night, Two Babies — Kathie DeNosky; tertile=end; p=0.53**
>
> Between Cornelia, Emily Taylor and Helen Washburn, I’ve been apologized to every day this week.”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_6 — repair**
  - All four keyword lists converge on repair behavior between the main couple. Main is saturated with apology-act vocabulary ('sorry', 'apologize', 'apology', 'apologizing', 'apologized', 'owe', 'apologise'), which is the canonical lexical signature of ARC_6 (repair). KeyBERT reinforces this with 'apology', 'apologize', 'forgive', 'fault', and 'embarrassed', indicating acknowledgment of wrongdoing and a bid for reconciliation. POS adds 'apology', 'behalf', 'distress', and 'circumstances', consistent with a formal or emotionally charged repair scene. MMR echoes 'apology', 'forgive', 'behalf', 'distress', and 'circumstances', with 'overheard' and 'snorted' suggesting interpersonal tension being addressed rather than escalating. The presence of 'forgive' across KeyBERT and MMR confirms the repair frame rather than mere escalation or disclosure. No cues point to final restored trust (ARC_7) or commitment payoff (ARC_8); the focus is on the act of apologizing itself, placing this squarely in ARC_6.
- **Pass B — contextual:** **ARC_6 — repair**
  - Topic 85 is overwhelmingly characterized by apology and sorry expressions ('I'm sorry', 'I am sorry', 'Did you just apologize?', 'No harm was done'). These are canonical repair gestures following conflict, mapping clearly to ARC_6 (repair). One sentence (BOOK_001_4) references a prior accusation of overreacting, suggesting a misunderstanding context (ARC_1), and two 'Excuse me?' fragments are too ambiguous to code beyond ARC_10. BOOK_001_5 references multiple third-party apologies, suggesting non-main-couple interaction (coded ARC_6 but main_couple=no). BOOK_002 sentences cluster around a clear dyadic apology exchange likely involving the main couple. Overall ARC_6 exceeds 70%, making it the dominant code. Main couple probability is moderate (~0.55) because several sentences are ambiguous or clearly involve secondary characters.
- **Pass C — adjudication:** **ARC_6 — repair**
  - Both lexical consensus and contextual dominant converge on ARC_6 (repair). The primary taxonomy tag 4.4 (Conflict, Distance & Breakup Threats) might suggest a falling-arc code such as ARC_2 or ARC_3, but the secondary tag 4.5 (Reconciliation, Commitments & HEA) and the consistent Pass A/B signal indicate the topic captures the turn toward repair rather than the conflict itself. ARC_6 sits in the REFINED_RISING construct bucket: the couple is actively moving from rupture back toward connection. No free-form labels require remapping. No split is warranted because the dominant signal is repair-initiation, with the conflict/distance framing serving as contextual backdrop rather than the topic's core content. Main-couple filter confirmed positive.

---

### Topic 129 — Accused of Not Caring {#topic-h6-129}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **ARC_4 — relationship caused distress**
- **Mixed:** False
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> like they care when they see that smoking-hot bod you’ve got.”

> at the moment, i could’ve cared less.

> you’ve never cared for anyone but yourself.”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Taste Me — Tamara Hogan; tertile=begin; p=0.59**
>
> Lukas didn’t care about her, and she… cared too much.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Bounty of Love — Scotty Cade; tertile=middle; p=0.61**
>
> Sir, I don’t think that’s—” “I don’t care what you think.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Bounty of Love — Scotty Cade; tertile=end; p=0.57**
>
> I don’t care about that kind of stuff,” Zander assured him. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Katie's Hope — Lizzy Ford; tertile=begin; p=0.71**
>
> I don’t expect you to understand what it is to care about someone else.”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_4 — relationship caused distress**
  - All four keyword lists converge on emotional distress and hurt within a relationship context. Main: 'care/cared/cares/caring' paired with negations ('don', 'less', 'didn') signals felt neglect or emotional withdrawal — a partner not caring enough, causing distress. KeyBERT: 'cared', 'mattered', 'sadly', 'unhappy', 'wondering' reinforce emotional pain and feeling unimportant to the other person. POS: 'unhappy', 'upset', 'worst', 'circumstances' describe a state of relationship-caused suffering. MMR: 'cared', 'treated', 'fault', 'smacked', 'circumstances', 'veins' suggest grievance over how one was treated, with blame attribution. No keywords indicate external antagonists (ruling out ARC_9), no clear misunderstanding frame (ARC_1), no separation/breakup threat (ARC_3), and no repair or commitment signals. The dominant signal is ongoing emotional distress caused by the relationship dynamic itself — fitting ARC_4 (relationship_caused_distress).
- **Pass B — contextual:** **ARC_10 — unclear arc role**
  - Topic 129 clusters around the word 'care' and its negations ('don't care', 'didn't care', 'cared too much'). The vast majority of sentences are decontextualised fragments — short rhetorical dismissals or ambiguous emotional statements — that cannot be reliably assigned to a specific narrative-arc function or confirmed as main-couple interactions. Three sentences (BOOK_002_5, BOOK_004_6, BOOK_005_4) carry enough relational context to suggest emotional distress tied to a romantic relationship (ARC_4: relationship_caused_distress): Lukas not caring while she cares too much, Jade being told she will always be cared for (implying prior hurt), and a character dying believing they were not cared for. All other sentences lack sufficient context to determine arc role or couple identity, coded ARC_10. ARC_10 dominates at 85%, well above the 70% threshold, making it the dominant code.
- **Pass C — adjudication:** **ARC_4 — relationship caused distress**
  - Lexical consensus (ARC_4: relationship_caused_distress) and taxonomy placement in 4.4 Conflict, Distance & Breakup Threats with secondary 3.2 Negative Emotions & Distress both point to emotionally driven distress arising from within the main-couple relationship. The contextual dominant ARC_10 (unclear_arc_role) reflects Pass B uncertainty, but the taxonomy metadata resolves that ambiguity: the content is not merely unclear — it is distress generated by the relationship dynamic itself, consistent with ARC_4. ARC_3 (separation/breakup threat) was considered but the taxonomy secondary tag (Negative Emotions & Distress) tips the balance toward ARC_4 as the primary signal, with breakup-threat elements as a contributing but not dominant feature. This sits firmly in the REFINED_FALLING construct bucket, representing deterioration of the main-couple bond through internally generated emotional suffering.

---

### Topic 210 — Expelled For Pursuing A Relationship {#topic-h6-210}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **MIXED**
- **Normalised category:** —
- **Mixed:** True
- **Main-couple prob:** 0.85 | non-couple: 0.1
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> she’ll be back,” [person] to explain.

> we’ll not last long like this,” [person] said quietly.

> if you pursue a relationship with [person], you’ll be expelled from motherhouse ireland, removed from your triad, and cast out from our way of life.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Cause For Scandal — Anna DePalo; tertile=begin; p=0.54**
>
> And, she’d reasoned, if pop star Jessica Simpson could resist the delectable Nick Lachey until their wedding night, she could certainly resist John.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Cause For Scandal — Anna DePalo; tertile=end; p=0.49**
>
> Besides, if there was one thing she’d come to know about Zeke, it was that he was able to make every audience member feel connected to him.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Cause For Scandal — Anna DePalo; tertile=end; p=0.48**
>
> Patrick huffed, as though he couldn’t believe Zeke had the audacity to claim that he—the up-by-his-boot-straps, self-made founder of a publishing empire—had anything in common with a bad-boy rock star.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Cause For Scandal — Anna DePalo; tertile=middle; p=0.44**
>
> As a waiter moved away with their plates, John said, “By the way, I saw that Scarlet was linked to Zeke Woodlow in today’s gossip columns.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Cause For Scandal — Anna DePalo; tertile=end; p=0.40**
>
> Unfortunately, a celebrity of Zeke’s caliber has an image to maintain and a publicity machine that needs to be fed—with the right kind of publicity, of course.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Razor Sharp — Fern Michaels; tertile=begin; p=0.35**
>
> The Hole was owned by a man named Peter Rabbit to the chagrin of his wife, Petra.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Disenchanted — C.K. Farrell; tertile=begin; p=0.53**
>
> Nathaniel was obviously willing to do such a thing.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Disenchanted — C.K. Farrell; tertile=begin; p=0.51**
>
> Some would think that when swimming in the depths of one’s own grief, one could forget what it was that made them so unhappy, but tell that to Nathaniel.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Disenchanted — C.K. Farrell; tertile=middle; p=0.50**
>
> Either way, there was something exhilarating about being with Nathaniel, especially being with him in his lair.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Disenchanted — C.K. Farrell; tertile=middle; p=0.50**
>
> For the life of him, Nathaniel didn’t know how Mr. Harrington was a part of his beauteous bride-to-be’s biological makeup.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Disenchanted — C.K. Farrell; tertile=end; p=0.46**
>
> The expression didn’t go unnoticed by Nathaniel.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Disenchanted — C.K. Farrell; tertile=begin; p=0.42**
>
> Nathaniel had come to understand and grudgingly accept that fact.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_6 — repair**
  - KeyBERT and MMR both surface 'forgive,' 'afterward,' and 'instincts,' pointing toward a repair attempt following friction. MMR adds 'unwilling' and 'annoyance,' suggesting resistance to reconciliation but still within a repair arc. POS keywords ('disappointment,' 'annoyance,' 'unwilling,' 'distraction') lean toward ongoing relational distress (ARC_4), and Main keywords ('didn,' 'decided,' named characters) suggest a tense interpersonal moment that could read as misunderstanding (ARC_1). However, the convergence of 'forgive' and 'afterward' across two representors, combined with 'possibility' (of resolution) and 'proved,' tips the balance toward ARC_6 (repair) as the dominant arc role — a post-conflict moment where forgiveness and reconciliation are being negotiated, even if reluctantly.
- **Pass B — contextual:** **MIXED**
  - Topic 210 spans multiple books and narrative threads. BOOK_008 sentences dominate numerically and consistently reference a past relationship with 'Nick' that has ended or is being discussed as over, coding as ARC_3 (separation/breakup threat). BOOK_009 shows a couple in active conflict (Drake slamming out), coding as ARC_2. BOOK_006 involves emotional distress around Nathaniel and a bride-to-be, coding as ARC_4 or ARC_10 where context is insufficient. BOOK_002 sentences involve celebrity gossip and publicity concerns around Zeke, largely external/off-couple (ARC_9). BOOK_004_1 is entirely off-target (ARC_0). No single code reaches 70%, so dominant_code is MIXED. Main couple probability is moderate (~0.60) given that roughly half the sentences clearly reference a named romantic pair.
- **Pass C — adjudication:** **MIXED**
  - Lexical consensus (ARC_6 repair) and contextual dominant (MIXED) diverge. Taxonomy 4.4 (Conflict, Distance & Breakup Threats) with secondary 5.1 (Family, Kinship & Parenthood) suggests the topic straddles active repair attempts and ongoing separation/breakup threat pressures — likely a moment where the couple is trying to reconcile but family-related conflict is simultaneously threatening the relationship. ARC_6 alone undersells the destabilising breakup-threat dimension; MIXED (ARC_6 + ARC_3) is the most defensible resolution. The family secondary axis does not redirect this to ARC_9 (external plot conflict) because the distress is relational and couple-facing rather than purely external. Construct bucket is REFINED_FALLING because repair is incomplete and breakup threat remains active, placing this in the descending/trough zone of the arc rather than the recovery upswing. Manual review is flagged to confirm whether family pressure is an external driver (ARC_9 component) or purely a relational stressor absorbed into the couple dynamic.

---

### Topic 256 — Refusing to Let It End {#topic-h6-256}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **ARC_0 — off target**
- **Mixed:** False
- **Main-couple prob:** 0.1 | non-couple: 0.8
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> no, i’ll get over it.

> i’ll give you some time, but goddamn it, nat, this is not over.”

> it’ll never be over—unless it ends right here right now.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · The Haunting — Hope C. Tarr; tertile=begin; p=0.45**
>
> I no longer cared which side won or lost, I only wanted it to be over.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · The Bride and the Buccaneer — Darlene Marshall; tertile=middle; p=0.48**
>
> Perhaps when this is over, you might see another attractive alternative.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · The Bride and the Buccaneer — Darlene Marshall; tertile=end; p=0.44**
>
> If there are consequences to our lovemaking, then this treasure hunt ends.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · The Bride and the Buccaneer — Darlene Marshall; tertile=middle; p=0.43**
>
> And here it’s been looming over us this entire time!”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_4 — relationship caused distress**
  - Main keywords ('end', 'over', 'ends', 'ended') strongly suggest termination or breakup language pointing toward ARC_3 (separation/breakup threat). However, KeyBERT, POS, and MMR all add affective-distress cues — 'hurts', 'anxious', 'shouted', 'repeated', 'sending' — that shift the dominant signal toward ongoing emotional suffering within or caused by the relationship (ARC_4: relationship_caused_distress). The pattern of repeated painful interactions ('repeated', 'thursday' as a recurring marker, 'hurts', 'anxious', 'shouted') suggests cyclical distress rather than a clean breakup event. ARC_4 wins by weight of three representers; Main's ARC_3 reading creates mild disagreement.
- **Pass B — contextual:** **ARC_0 — off target**
  - Topic 256 is dominated by the word 'over' used in highly varied, mostly non-romantic-arc senses: completion of events, wars, tasks, emotional recovery, and social pleasantries. The largest single cluster (ARC_0, ~45%) consists of sentences where 'over' has no clear romantic-arc meaning. A secondary cluster from BOOK_004 uses 'I'm over it / get over it' language that loosely implies emotional recovery/repair (ARC_6, ~25%), but without clear main-couple context. A smaller cluster references external plot events ending (ARC_9, ~20%). Only BOOK_001_1 ('We're over') clearly signals a main-couple breakup threat (ARC_3). Main-couple probability is low (~0.15) because most sentences lack identifiable couple context. No single code reaches 70%, but ARC_0 is dominant at ~45%, so dominant_code is ARC_0.
- **Pass C — adjudication:** **ARC_0 — off target**
  - Lexical consensus (ARC_4) reflects surface conflict-label fidelity to taxonomy 4.4 (Conflict, Distance & Breakup Threats), but the contextual dominant code (ARC_0) indicates the topic content does not actually center on the main couple's relationship-caused distress. The taxonomy placement in 4.4 is a label match, not a content match. Because high conflict-label fidelity ≠ main-couple conflict, and the dominant contextual read is off-target, ARC_0 prevails in adjudication. main_couple is set to false accordingly. Manual review is flagged to verify whether any main-couple signal is genuinely present or whether the topic should be excluded from the hypothesis corpus entirely.

---

### Topic 316 — Snapping Over Money and Control {#topic-h6-316}

- **Old taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **New category:** **ARC_0 — off target**
- **Mixed:** False
- **Main-couple prob:** 0.1 | non-couple: 0.8
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> you’ll have to find another way to obtain the tallmadge money,” lucas snapped. “

> stop that, you little fool, otherwise we’ll both be—’ lucas began, and then stopped as one of suzy’s flailing hands caught the side of his mouth.

> they didn’t like it much when they found out, but lucas paid them well, and they’ll get over it.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Heaven and Hell — Kristen Ashley; tertile=end; p=0.47**
>
> Kia, head tipped way back, was looking at Sampson.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · For Love of an Angel — Rosalie Lario; tertile=middle; p=0.59**
>
> Perhaps you should show Eva to her room,” Lucas finally suggested to Michael. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · For Love of an Angel — Rosalie Lario; tertile=middle; p=0.49**
>
> Unlike Ethan and Jason, who were dark-haired, Aaron and Lucas were more dirty-blonde.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Eyes Of Myrl — Faelyn Rose; tertile=end; p=0.64**
>
> He watched Lucas Mason as he spoke and was rewarded by an expression of guilt upon his uncle’s face. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Eyes Of Myrl — Faelyn Rose; tertile=end; p=0.55**
>
> You have brought this upon us,” Lucas Mason harshly accused his grief stricken nephew. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Eyes Of Myrl — Faelyn Rose; tertile=end; p=0.55**
>
> Lucas Mason was not so wise, however, and questioned Rork angrily. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Eyes Of Myrl — Faelyn Rose; tertile=end; p=0.51**
>
> The look upon Lucas Mason’s traitorous face mirrored the truth of Rork’s words.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Eyes Of Myrl — Faelyn Rose; tertile=end; p=0.51**
>
> But as Lucas continued his tirade, Rork reached out to touch his beloved father’s body , only to find it frozen.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **ARC_4 — relationship caused distress**
  - All four keyword lists converge on emotional distress and negative affect within a relationship context. Main keywords (stared, thoughtful, shout, named characters lucas/fallon) suggest interpersonal tension between identifiable parties. KeyBERT supplies the emotional valence: annoyance, groaned, disappointment, failure, pathetic — these are feelings generated by the relationship dynamic rather than an external plot threat or a discrete misunderstanding/escalation event. POS and MMR reinforce this with overlapping terms (shout, failure, annoyance, disappointment, comments, bothered, glared, worries). The cluster describes ongoing relational distress — characters experiencing negative emotional states caused by their relationship — which maps to ARC_4 (relationship_caused_distress). There is no clear repair, commitment, disclosure, or external-plot framing; the dominant signal is sustained emotional suffering/frustration within the couple dynamic.
- **Pass B — contextual:** **ARC_0 — off target**
  - Topic 316 clusters around the name 'Lucas' (and associated characters Aaron, Kia, Sampson, Rork, Eva, Michael, Ethan, Jason) across multiple books. The sentences are character-identification fragments, spatial/logistical dialogue, and brief action tags with no romantic-couple framing. None of the sentences establish or imply a main romantic couple; they reference male characters (Lucas, Aaron) in what appear to be ensemble or family/group contexts, conflict between non-romantic parties (Lucas Mason vs. Rork), or simple descriptive statements. There is no romantic arc content detectable. All sentences are coded ARC_0 (off_target).
- **Pass C — adjudication:** **ARC_0 — off target**
  - Lexical consensus (ARC_4) reflects surface conflict-label fidelity — the topic's tokens map onto distress/conflict vocabulary — but contextual dominant (ARC_0) correctly identifies that the content does not involve the main romantic couple. Taxonomy 4.4 (Conflict, Distance & Breakup Threats) with secondary 7.1 (Interpersonal Non-Romantic Conflict) confirms the conflict is interpersonal but non-romantic, i.e., outside the main-couple dyad. Per the main-couple filter, ARC_4 requires the distress to be caused by the romantic relationship itself; here the distress is either peripheral or involves non-romantic parties. The contextual dominant therefore overrides the lexical consensus. ARC_0 (off_target) is the correct arc_role. No construct bucket applies because the topic does not contribute to the REFINED_FALLING, REFINED_RISING, or EXTERNAL_PLOT_CONFLICT arcs in a main-couple context.

---
