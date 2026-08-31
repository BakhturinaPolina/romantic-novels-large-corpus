# H1 intimacy — close-reading pack

## Topic 1 — Straps Sliding Down Her Arms

- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Code:** MIXED

> i’ve had practice,” he said as he slid the straps down my arms and removed it.

> how could a man who just serenaded me with one of the sexiest songs i’ve ever heard and who kisses the way he does be a virgin?

> the way he holds me —the tenderness, the carefulness—gives me hope that we’ve made great strides tonight.

> *(CELL_A, tertile=begin)* His hand came up to grip my head, keeping me trapped in the loving softness of his kiss.

> *(CELL_A, tertile=middle)* His lips attached to my neck as his fingers worked their way up my shirt.

> *(CELL_A, tertile=end)* He held me to him as his mouth moved in sync with mine, his tongue just slipping in to brush against me.

> *(CELL_A, tertile=begin)* Chuckling in my mouth, he held me against him, deepening our kiss.

### Pass A/B/C

- **A lexical:** `I6`
  - Main keywords (kiss, kissed, lips, kisses, kissing, tongue) establish affectionate/erotic oral contact, which alone would support I3. However, KeyBERT adds 'stroking, cupped, cradled, biting, pounded, panting, moaning, clinging' — 'pounded' and 'moaning' push beyond non-genital caress into explicit sexual activity territory. POS reinforces with 'dripping, damp, pressure, movements, panting' — physiological arousal cues consistent with explicit sex. MMR adds 'panting, swirling, guided, lingering, grasp' — escalating physical engagement. The convergence of 'pounded,' 'moaning,' 'panting,' 'dripping,' and 'damp' across three representors signals activity beyond kissing/caressing (I3) and into explicit/penetrative territory (I6). I3 is present as a component (kissing contact confirmed) but is subsumed by I6 given the explicit physiological and action cues across the majority of representors.
- **B contextual:** `MIXED`
  - The topic spans a wide range of intimacy functions. BOOK_002 sentences all depict affectionate physical contact (kissing, holding, caressing) → I3. BOOK_004_1 and BOOK_004_2 involve explicit oral/genital commands → I6. BOOK_005_2 ('Put me inside you') is a penetrative command → I6. BOOK_001_1 and BOOK_001_2 involve coercive/threatening dynamics → I9. BOOK_004_3 also reads as coercive physical action → I9. BOOK_006_2–4 express desire/longing/seduction without contact → I4. BOOK_003_1, BOOK_005_3, BOOK_006_5 are neutral/logistical → I0. BOOK_005_1 ('sensual caress') implies physical contact → I3. BOOK_006_1 references a past kiss (retrospective contact) → I3. No single code reaches 70%, so dominant_code is MIXED.
- **C adjudicate:** `MIXED`
  - Lexical consensus from Pass B/C points to I6 (explicit sexual acts), but the contextual dominant is MIXED and the taxonomy flags a secondary construct of 2.2 Kissing & Non-Explicit Affection (I3). This indicates the topic cluster contains tokens spanning both non-genital affectionate contact (kissing, undressing as prelude, caress — legitimately I3) and explicit genital/oral/penetrative acts (I6). Because the anti-collapse rules forbid forcing I3 content into I6 and vice versa, and because the taxonomy itself acknowledges both constructs, a SPLIT is warranted rather than a single-code assignment. The I3 contact evidence flag is set true because kissing/undressing-as-prelude tokens are present per the secondary taxonomy label. Manual review is required to partition individual topic tokens or sub-topics into their respective I3 vs. I6 bins before downstream analysis.
- **Action:** SPLIT

---

## Topic 7 — Kissing With Tongue and Urgency

- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Code:** MIXED

> kissing her on the forehead, he leaned against the register and waited for her to finish.

> he leaned down and pressed his lips to hers. “

> turning to his mate, he leaned down and pressed a kiss to vee’s head. “

> *(CELL_D, tertile=end)* Sophia Young kisses him, and he kisses her back, grabbing both her arms at the top fleshy section, and lifting her up so her mouth smothers his.

> *(CELL_D, tertile=end)* Cagney laughed and tried to roll her over to him, for a kiss.

> *(CELL_D, tertile=end)* Cagney opens his mouth to speak, but she places her hands on both sides of his face urgently, her claws digging into his cheeks, and pulls his mouth round to meet hers. ‘

> *(CELL_D, tertile=end)* She is staring at his wet crotch with her mouth wide open and her eyes even wider.

> *(CELL_D, tertile=end)* She tickles a line along the inside of his upper lip with her tongue, as Cagney opens his eyes and watches her closely and evenly, weaving her spell.

> *(CELL_D, tertile=end)* Her face angles upwards towards his, like a scene from a 1930s film, when men and women locked together, and kissed passionately, and then tore themselves apart.

> *(CELL_A, tertile=middle)* He then leaned down and placed a gentle kiss on her lips and felt himself harden even more. “

> *(CELL_A, tertile=end)* His grip tightened on her hips when she let out a scream and he continued to hungrily stroke her with his tongue, enjoying the way she was pushing her body against his mouth.

### Pass A/B/C

- **A lexical:** `I6`
  - All four representations converge on I6. Main contains explicit genital/oral terms: 'clit', 'cock', 'pussy', 'tongue', 'mouth', 'lips', 'kiss' — the genital vocabulary elevates beyond I3 kissing into explicit sexual activity. KeyBERT adds 'licked', 'stroking', 'tasted', 'biting', 'cupped' — oral and manual genital stimulation cues. POS adds 'pumping', 'moaning', 'urgency', 'passionate' — penetrative/rhythmic action and arousal response. MMR reinforces with 'pumping', 'moaning', 'dipped', 'swirling', 'flicked', 'stroking' — all consistent with explicit oral/genital/penetrative acts. I3 is not rejected outright (affectionate contact cues like 'kissed', 'caressed' are present), but the preponderance of genital and penetrative vocabulary mandates I6 over I3 per the rule that genital/oral/penetrative contact = I6.
- **B contextual:** `I3`
  - The majority of sentences depict kissing, holding, or non-genital caressing — all coded I3 (affectionate physical contact). Three sentences (BOOK_001_5: tongue inside lip during an erotic/oral act framed as genital-adjacent; BOOK_002_3: oral stimulation of genitals; BOOK_003_4: manual contact with erection) describe genital or oral-genital acts and are coded I6. Four sentences (BOOK_001_4, BOOK_003_2, BOOK_003_3, BOOK_003_5) depict erotic gaze or visual/sensory arousal without physical contact, coded I10. I3 accounts for ~60% of sentences, making it the dominant code.
- **C adjudicate:** `MIXED`
  - Lexical consensus (I6) and assigned taxonomy (2.3 Explicit Sexual Acts) both point to explicit sexual content, while contextual dominant (I3) suggests affectionate/non-genital contact may also be present. The anti-collapse rules prohibit defaulting to I3 without clear non-genital contact evidence, and the taxonomy anchor at 2.3 resists downgrading to I3 alone. The conflict between lexical and contextual signals, combined with the secondary taxonomy flag for Attraction & Sexual Tension (2.1), indicates this topic likely spans a continuum from affectionate contact through explicit acts. MIXED coding with manual review is required to determine whether the topic should be SPLIT into distinct I3 and I6 sub-topics or retained as a single I6 topic with I3 as secondary. Topic ID is placeholder (-1) pending provision of actual topic identifier.
- **Action:** RETAXONOMIZE

---

## Topic 24 — Confronting An Unwanted Marriage

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** I0 (norm: I0)

> we’ll be married… to each other.”

> you’re already married to me; he’ll understand.” “

> i’ll give you a divorce and you can just walk away.

> *(CELL_D, tertile=begin)* So that whole getting married and settling down part doesn't appeal to you?"

### Pass A/B/C

- **A lexical:** `I0`
  - All four keyword lists converge on domestic/relational logistics and formal relationship status. Main keywords (marry, married, marriage, husband, wife, divorce) are squarely about marital institution and HEA/domestic framing. KeyBERT adds engaged, promises, intend, willingly — commitment and intention language, no physical contact cues. POS adds unhappy, threats, concept, issue, previous — relational conflict and negotiation around marriage, still no contact. MMR adds arranged, threats, faltered, eyeing — arranged-marriage tension and perhaps coercion-adjacent framing, but 'eyeing' alone is insufficient for I10 and there is no affectionate physical contact language anywhere. I3 is rejected because no kiss, hug, hold, caress, or undress cue appears in any list. I9 (coercion) was considered given 'threats' and 'arranged', but the dominant signal across all lists is marital status/logistics, making I0 the best fit.
- **B contextual:** `I0`
  - Every sentence in this topic concerns marriage status, marriage proposals, wedding logistics, or relationship/domestic standing (married, divorced, wanting to wed, being someone's wife/husband). There is no affectionate physical contact, no desire expression, no erotic content, and no emotional vulnerability exchange beyond the institutional framing of marriage. All sentences map cleanly to I0 (domestic/relational logistics and HEA/commitment talk).
- **C adjudicate:** `I0`
  - Lexical and contextual consensus both indicate I0. Taxonomy confirms primary placement in 4.4 Conflict, Distance & Breakup Threats with secondary 4.5 Reconciliation, Commitments & HEA — both of which are relational/emotional/logistical in nature without affectionate physical contact. No evidence of kissing, hugging, caressing, or undressing-as-prelude; I3 is therefore forbidden. The topic captures emotional negotiation, relational rupture, and resolution talk, all of which fall squarely within I0 (domestic/logistics/HEA/relational-status discourse). No upgrade to I2, I3, or any other code is warranted.
- **Action:** KEEP

---

## Topic 25 — Crawling Onto The Bed Together

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I0 (norm: I0)

> more aptly, he crawled on top of the bed, on top of the blanket, but he reached for her, enfolding lily into his arms.

> v crawled onto the bed, turned over onto her back, but apparently zane had other ideas because he deftly flipped her onto her stomach, his hands groping her ass and holding her still.

> sure,” he said softly, and didn’t bother standing as he crawled over to the mattress.

> *(CELL_D, tertile=middle)* Then over her shoulder, she called out, "Yo, you fall asleep in there or what?" "

> *(CELL_D, tertile=begin)* With a sigh, she stood and padded out of the room, her open nightshirt flapping around her like a robe.

> *(CELL_D, tertile=middle)* I strode over to the bed and picked up the tiny foil-wrapped square.

> *(CELL_D, tertile=middle)* Jemma lay sprawled on the floor, the back of her head a tangled mass of red.

> *(CELL_A, tertile=middle)* He walked over to the bed where she was sitting on the edge and pulled her to her feet. “

> *(CELL_A, tertile=middle)* she whispered as he picked her up again and headed for the bedroom. “

> *(CELL_A, tertile=middle)* When she felt him enter her she cried out, her spine bowing and her fists clenching at the bedspread on either side of her. “

> *(CELL_B, tertile=end)* He sat on the edge of the bed and gently pulled her knees down to the mattress.

### Pass A/B/C

- **A lexical:** `I3`
  - Main keywords (snuggled, lay, bed, pillow) indicate affectionate physical closeness/contact in a bed setting. KeyBERT adds 'caressed' (direct non-genital touch), 'cradled' (holding/embracing), 'crawled' and 'scooted' (movement toward contact), and 'patted' (gentle touch) — multiple explicit affectionate-contact cues. MMR reinforces with 'cradled', 'guided', 'crawled', 'scooted'. POS alone is more ambiguous (movement/spatial terms without clear contact), suggesting I2 (caretaking/comfort positioning), but the weight of evidence across Main and KeyBERT confirms actual affectionate physical contact (caressed, cradled, snuggled, patted). No genital/penetrative cues present, so I6 is rejected. I3 is warranted by the explicit contact vocabulary.
- **B contextual:** `I0`
  - The majority of sentences (12/20) describe positional or spatial movement around a bed with no affectionate contact — coded I0 (domestic/logistical). Six sentences show clear affectionate physical contact (pulling to feet, carrying, holding legs, curling against): I3. Two sentences depict penetrative intercourse (BOOK_002_5: 'felt him enter her'; BOOK_003_6: 'begging him to enter her'): I6. I0 accounts for ~60% of sentences, making it the dominant code.
- **C adjudicate:** `I0`
  - Pass B contextual dominant (I0) is better supported than the lexical consensus (I3). The taxonomy flags 2.1 Attraction & Sexual Tension as primary, but without evidence of actual affectionate physical contact (kiss, hug, hold, caress, or undress-as-prelude), I3 is forbidden under anti-collapse rules. The secondary taxonomy tag (2.3 Explicit Sexual Acts) is not evidenced either. The contextual dominant I0 — domestic, logistical, or HEA-maintenance content — is the most defensible classification. Retaining I0 per the instruction to keep Pass B I0 when evidence is domestic/care/HEA without contact.
- **Action:** REINTERPRET

---

## Topic 29 — Confessing Long-Held Love

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** I1 (norm: I1)

> i love you with everything i am, everything i’ve been, and everything i hope to be .” “

> tell her i’ve always loved her.

> i’ve always been in love with you.”

> *(CELL_B, tertile=end)* I love you, too, sweetheart.”

> *(CELL_B, tertile=end)* Oh, child, I love you, too.”

> *(CELL_B, tertile=end)* You just say ‘I love you.’”

### Pass A/B/C

- **A lexical:** `I5`
  - Main keywords ('love, loved, loves, falling, fall, always') signal emotional love declaration/confession without any physical contact cues. KeyBERT adds emotional depth ('happiness, forgive, deserve, crushed, secretly, dreamed') pointing to vulnerability and emotional revelation — classic love confession territory. POS ('spite, reflection, delicate, actions') and MMR ('apologize, crushed, spite, uttered, blinking') reinforce an emotionally charged verbal exchange, likely a confession or declaration of love with conflict/tension. No kissing, hugging, caressing, or undressing cues are present anywhere, so I3 is rejected. Desire without contact cues is absent too (no longing/lust language), ruling out I4. This is an emotional declaration/confession of love (I5). I3 rejected: zero affectionate-contact vocabulary across all four representations.
- **B contextual:** `I1`
  - Every sentence in this topic consists exclusively of verbal declarations of love ('I love you,' 'I love you too,' 'Love you, Mom,' etc.). There is no physical contact described, no desire/gaze, no domestic logistics, and no erotic content. These are purely verbal emotional disclosures, which map to I1 (verbal expression of love/affection). I3 is forbidden because no affectionate physical contact is present in any sentence.
- **C adjudicate:** `I1`
  - Pass B lexical consensus (I5) reflects surface vocabulary of declarations and vows, but contextual dominant (I1) better captures the functional intimacy at work: reconciliation, commitment, and HEA emotional payoff are fundamentally about emotional bonding and relational resolution rather than physical contact. Taxonomy 4.5 (Reconciliation, Commitments & HEA) with secondary 3.1 (Positive Resolution, Relief & Emotional Payoff) confirms this is an emotional-closure cluster. No affectionate physical contact evidence is present (i3_contact_evidence: false), so I3 is forbidden per anti-collapse rules. I5 (formal commitment/vow) is plausible lexically but the dominant function is the emotional bond repair and relational affirmation characteristic of I1. I1 is the most specific code that fits the taxonomy and evidence without over-reading physical contact or under-reading the relational depth.
- **Action:** REINTERPRET

---

## Topic 36 — Eagerly Offering to Help

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> of course, i’ll help you.’

> then you’ll let me help,” frances said at once, her expression eager. “

> sure, of course, i’ll help.”

> *(CELL_B, tertile=end)* And you know I’m here to help you in any way I can.”

> *(CELL_D, tertile=middle)* Well make yourself useful,” he said. “

> *(CELL_B, tertile=end)* I’ve got to do something to help.”

### Pass A/B/C

- **A lexical:** `I2`
  - All four keyword lists converge on a service/assistance/caretaking register: 'help, helping, assistance, helped' (Main); 'provided, willing, appreciate, requested, task, promptly, sir' (KeyBERT); 'task, options, success, pleased, excited' (POS); 'mister, promptly, appreciate, eagerly, pleased, intend, insisted' (MMR). This is functional caretaking/support interaction — consistent with I2 (emotional support, reassurance, caretaking). No affectionate physical contact cues (no kiss, hug, hold, caress, undress) appear in any representation, so I3 is rejected. No desire/gaze cues (I4/I10), no explicit content (I6), no coercion (I9), no consent negotiation (I8), and no domestic/HEA logistics (I0). The formal address 'mister/sir' and task-oriented vocabulary confirm a caretaking/assistance dynamic rather than romantic intimacy.
- **B contextual:** `I2`
  - All sentences in this topic revolve around offers of assistance, reassurance of availability, and caretaking language ('Can I help you?', 'I'll help you', 'I'm here to help you in any way I can'). This is classic I2 (reassurance/caretaking/emotional support) with no physical contact, no desire, no domestic/HEA logistics, and no erotic content. I3 is forbidden as there is zero affectionate physical contact evidenced.
- **C adjudicate:** `I2`
  - Lexical and contextual consensus both indicate I2. Taxonomy confirms 4.6 Emotional Safety, Reassurance & Caretaking with no secondary code suggesting physical contact. No affectionate physical contact evidence is present, so I3 is forbidden per anti-collapse rules. The signal is purely reassurance/caretaking without domestic/logistics/HEA framing that would push toward I0. I2 is the correct and most specific code.
- **Action:** KEEP

---

## Topic 38 — Admitting Shared Pain

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** I2 (norm: I2)

> i’ve seen your pain.

> i've never felt that way before."

> will it make you feel better to know that i’ve got one, too?”

> *(CELL_A, tertile=middle)* That’s what it felt like—that was the exact feeling—and I’m so happy that now you were there.

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords (feel, feels, good, felt, feeling, better, make) point to emotional processing and reassurance/caretaking — no physical contact cues. KeyBERT adds 'hurts, experienced, worst, honestly, apologize, magical' — language of emotional disclosure, pain acknowledgment, and reassurance. POS adds 'accustomed, magical, insides, problems, loose' — internal emotional/physical sensation language consistent with emotional vulnerability or caretaking. MMR reinforces with 'hurts, apologize, admitted, experienced' — confession, apology, and emotional acknowledgment. Together these signal emotional support, reassurance, and caretaking (I2). No kissing, hugging, holding, caressing, or undressing cues are present anywhere, so I3 is rejected. No desire/gaze cues for I4/I10. No explicit sexual content for I6.
- **B contextual:** `I2`
  - The overwhelming majority of sentences in this topic revolve around emotional states, mutual feelings, and emotional attunement between characters — the core function of I2 (emotional reassurance/caretaking/vulnerability sharing). Phrases like 'I feel it in my bones,' 'the feeling was mutual,' 'I always want to be able to tell you what I'm feeling,' and 'feel better?' all express emotional connection and empathic attunement without any physical contact, ruling out I3. BOOK_004_2 ('fucking you senseless') expresses sexual desire without depicting an actual act, making I4 (desire without contact) the most specific code. No affectionate physical contact is described anywhere in the topic, so I3 is forbidden. No explicit sexual acts are depicted, ruling out I6.
- **C adjudicate:** `I2`
  - Both lexical and contextual consensus converge on I2. The taxonomy confirms primary placement in Ongoing Courtship & Everyday Relational Bonding with a secondary signal of Negative Emotions & Distress, consistent with reassurance and caretaking dynamics. No affectionate physical contact (kiss, hug, hold, caress, or undress-as-prelude) is evidenced, so I3 is forbidden per anti-collapse rules. The distress secondary signal reinforces I2 (caretaking/reassurance) rather than redirecting to I3 or any other code. No domestic/logistics/HEA content that would warrant I0. KEEP with I2 is the correct disposition.
- **Action:** KEEP

---

## Topic 41 — Gripping Her Neck and Pulling Close

- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Code:** MIXED

> i could’ve went for some of her pussy too, but right now, ass action was what i ultimately desired. “

> she lifts up on her toes and kisses me, and she’s the sweetest damn thing i’ve ever tasted.

> in my mind i’m pushing her away, but in reality i’ve got one hand on her lower back, pulling her against me, and my other hand gripping the nape of her neck.

> *(CELL_A, tertile=middle)* She moves her hands up my body, tentatively touching the underside of my breast, her soft cool fingers tracing a lazy path along my skin as our tongues tangle.

> *(CELL_A, tertile=begin)* I let my mouth search her clit a little more as her head bobbed up and down, forcing her tongue into my hole.

> *(CELL_A, tertile=begin)* I grabbed her head as she lapped up all my come into her mouth.

> *(CELL_A, tertile=end)* into my ear and neck and begins to stroke her hands along my arms, my sides, my breasts . . .

> *(CELL_A, tertile=middle)* She looks at me and I pull her towards me and kiss her deeply, feeling the warm sticky come rub off onto my face and into my mouth.

> *(CELL_A, tertile=begin)* Then I kissed the outside of her pussy lips, letting them slide up and down my lips and tongue.

> *(CELL_B, tertile=middle)* Her tongue meets me halfway, and her hand presses into my side, drawing me closer.

> *(CELL_B, tertile=end)* I place my index finger over her soft lips, shaking my head. “

### Pass A/B/C

- **A lexical:** `I6`
  - Main keywords 'kissed, lips, kiss, mouth, tongue, neck' establish oral/kissing contact (I3 threshold met), but the combination with 'tongue' used in a kissing/oral context alongside POS cues 'ripping, thigh, waist, entrance, flushed' and MMR cues 'moaning, panting, swirling, chased' push well beyond non-genital caress into erotic/sexual activity territory. 'Entrance' and 'thigh' in POS, plus 'moaning/panting' in MMR, are strong erotic-progression markers. KeyBERT alone ('caressed, stroking, biting, cradled') might stop at I3, but the cross-representation weight of explicit arousal and body-part cues ('entrance', 'thigh', 'ripping') elevates the consensus to I6. I3 is not rejected outright—contact evidence is present—but the topic as a whole describes activity beyond kissing/caress into genital/oral/penetrative territory.
- **B contextual:** `MIXED`
  - The topic spans a spectrum from affectionate non-genital physical contact (I3: kissing on lips/jaw/neck, hugging, caressing hair/back, pressing lips to knuckles, touching stomach) to explicitly genital/oral sexual acts (I6: cunnilingus, oral sex with genital contact, nipple biting in sexual context, post-orgasm kissing with come). BOOK_001_1 involves tongue-tangling plus breast touching as prelude to/during sex — the genital-oral framing of surrounding sentences tips it to I6. BOOK_001_4 is non-genital caress (I3). BOOK_005_4 (lips to nipple) and BOOK_005_6 (teeth on nipple + thigh between legs) are coded I6 as they are clearly erotic/genital-adjacent acts in explicit sexual context. BOOK_002_1 is a neutral logistical remark (I0). No single code reaches 70%, so MIXED is assigned.
- **C adjudicate:** `MIXED`
  - Lexical consensus at I6 is overridden by MIXED contextual dominant, indicating the topic conflates two distinct intimacy functions: explicit sexual acts (I6, taxonomy 2.3) and pre-contact desire/tension (I4, taxonomy 2.1). Because the secondary taxonomy is 2.1 and contextual signal is not uniformly explicit, collapsing to a single I6 code risks misclassifying attraction-tension documents. A SPLIT is preferred over REINTERPRET to preserve granularity. I3 is forbidden here: no affectionate-contact-only evidence is present that would warrant it, and the anti-collapse rules prohibit defaulting to I3. Manual review is required to assign individual documents to the correct sub-topic before finalizing codes.
- **Action:** SPLIT

---

## Topic 45 — Reassured Everything Will Be Fine

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> we’ll be ok.” “

> nadines : you’ll be ok?

> ok, maybe a zero-tolerance one, but there’s no doubt about it, you’ll be great.

> *(CELL_D, tertile=middle)* I'm fine," Amber replied quietly. "

> *(CELL_D, tertile=begin)* Your wound…'" "I'm fine."

> *(CELL_B, tertile=middle)* Is everything okay?” “

### Pass A/B/C

- **A lexical:** `I2`
  - All four keyword sets converge on reassurance/caretaking function. Main keywords ('fine, okay, everything, right, honey, alright') are classic verbal reassurance phrases. KeyBERT ('assured, assure, smoothly, incredibly') reinforce the act of calming or reassuring someone. POS ('problems, sir, lord') suggest a formal or hierarchical caretaking/concern context. MMR ('smoothly, assure, acknowledged, injured, problems, appreciate, assured') strongly indicate someone addressing a problem or injury and offering reassurance. No affectionate physical contact cues (kiss, hug, hold, caress, undress) appear in any keyword set, so I3 is rejected. No desire, gaze, explicit, or coercion cues present, ruling out I4, I10, I6, I9. This is squarely I2: emotional support and reassurance.
- **B contextual:** `I2`
  - Every sentence in this topic consists of reassurance or welfare-checking utterances ('I'm fine,' 'Are you okay?', 'It's going to be all right,' etc.). These are verbal expressions of concern and emotional reassurance with no affectionate physical contact, no desire, no erotic content, and no domestic/HEA logistics. I2 (reassurance/caretaking) is the most specific and uniformly applicable code across all 20 sentences.
- **C adjudicate:** `I2`
  - Lexical and contextual consensus both resolve to I2. The taxonomy metadata confirms 4.6 Emotional Safety, Reassurance & Caretaking as dominant, with 9.2 Promise/Vow/Future-Tense Speech Acts as secondary — both are non-contact intimacy functions. No affectionate physical contact (kiss, hug, hold, caress, or undress-as-prelude) is evidenced, so I3 is forbidden per anti-collapse rules. The secondary vow/promise dimension does not elevate to I0 (domestic/logistics/HEA without emotional charge) because the primary function is reassurance and caretaking rather than logistical planning. KEEP at I2 with the dual construct framing is the correct adjudication.
- **Action:** KEEP

---

## Topic 57 — Hands Raised in Reassuring Gesture

- **Taxonomy:** 1.7 — Facial Expression & Non-Sexual Nonverbal Cues
- **Code:** I0 (norm: I0)

> instinctively, i opened my mouth for him to enter. “

> iain lifted his hands, palms out. “

> as he slid off the bar stool he clamped a hand over his friend’s shoulder, partly to support his own leaden legs and partly in a reassuring gesture. ‘‘

> *(BOOK_001, CELL_D, tertile=begin)* Grinning, he held up his hands in a gesture of mock innocence. “

> *(BOOK_001, CELL_D, tertile=end)* Jake clenched his hands, then forced himself to unclench them. “

> *(BOOK_001, CELL_D, tertile=middle)* Luckily a couple of the reporters made themselves useful and tackled him.

> *(BOOK_003, CELL_B, tertile=end)* He shook his head slightly and lifted an unsteady hand to his face.

### Pass A/B/C

- **A lexical:** `I5`
  - All four keyword lists center on body-language and physical tension cues: clenched fists, gripped wrists, loosened hands, hesitation, awkward gestures, palms, elbows, ankles. These describe non-contact physical expressiveness — restrained emotion conveyed through posture and gesture rather than affectionate touch. 'Patted' in KeyBERT is the closest contact cue but is isolated and ambiguous (could be self-patting or incidental); it is insufficient to establish affectionate contact. 'Reassuring' in POS points toward emotional support framing but without physical contact vocabulary to anchor it as I2 caretaking. I3 is rejected because there is no clear kiss, hug, hold, caress, or undress-as-prelude; the dominant signal is tense, restrained body language. I5 (non-verbal/body-language emotional communication) best captures the consensus across all four representations.
- **B contextual:** `I0`
  - All sentences in this topic describe hand and arm gestures — holding up hands in surrender/innocence, clenching/unclenching fists, shaking hands in greeting, covering one's face, fingers trembling. These are non-intimate physical actions serving narrative/social functions (de-escalation, greeting, emotional display). There is no affectionate physical contact between characters (no kiss, hug, caress, or embrace), no desire, no erotic content, and no relationship-building dialogue. The topic coheres around gestural body language in tense or social situations, coded I0 (non-intimate narrative/social interaction).
- **C adjudicate:** `I0`
  - Pass B contextual dominant (I0) is upheld. The taxonomy confirms primary coding as Facial Expression & Non-Sexual Nonverbal Cues (1.7) with secondary Emotional Safety/Reassurance (4.6) — both are non-contact intimacy functions. Lexical consensus I5 (nonverbal/expressive signaling) does not override the absence of affectionate physical contact. No kiss, hug, hold, caress, or undress-as-prelude is evidenced, so I3 is forbidden per anti-collapse rules. The content reflects communicative/relational cues and caretaking affect without physical contact, placing it firmly in I0 (domestic/relational baseline nonverbal communication) rather than any contact-dependent code. Retaxonomizing from I5 to I0 with the confirmed taxonomy constructs is the appropriate adjudication.
- **Action:** RETAXONOMIZE

---

## Topic 61 — Planning to Exchange Rings

- **Taxonomy:** 8.3a — Commitment Symbols & Love Tokens
- **Code:** MIXED
- **Evidence:** exhaustive packet

> in a few days, i’ll go to the stone.

> next time we’ll put a ring on him.”

> we’ll take care of the rings tomorrow.”

> anna was admiring his ring.

> *(CELL_D, tertile=end)* Just have to close it up again, until it looks like a ring, and we'll be fine.

> *(CELL_D, tertile=end)* Once they're gone, Shanley pricks Marie's finger with a lancet. "

> *(CELL_D, tertile=end)* It's not quite a perfect C-shape any longer, but more like one of those spoon bracelets that come in and out of fashion--the ends are drawing together, tightening, and that's a good thing, right?

> *(CELL_B, tertile=end)* He took the ring out of the box and, with Damon’s help, they placed it on her finger.

> *(CELL_B, tertile=end)* Damon and I agreed that you own our hearts so we thought this ring would be perfect for our union.”

> *(CELL_B, tertile=end)* I’m going to buy you some jewellery to wear in the pretty hole.”

> *(CELL_B, tertile=end)* He opened the lid and presented Rachel with a three karat heart-shaped ruby, surrounded by diamonds. “

> *(CELL_B, tertile=end)* Remember that place in town where the guy makes the silver jewellery?” “

### Pass A/B/C

- **A lexical:** `I5`
  - All four keyword lists center on jewelry (ring, necklace, diamond, gold, engagement, rings) and associated cues (engaged, promises, precious, glint, polished). The dominant signal is symbolic commitment/betrothal — engagement rings, promises, precious stones — pointing to I5 (symbolic commitment / tokens of love / proposal). No affectionate physical contact cues (kiss, hug, caress, undress) are present anywhere, so I3 is rejected. No explicit desire language rules out I4/I6. 'Threats' and 'commander' in POS/MMR are minor outliers insufficient to shift the consensus away from the overwhelmingly commitment-token-focused vocabulary.
- **B contextual:** `MIXED`
  - The topic centers on jewelry in a romance context, spanning a wide range of intimacy functions. Most sentences are logistical/descriptive (I0): discussing rings, jewellery items, craftsmanship, or neutral references. BOOK_002_1 shows affectionate physical contact (placing a ring on her finger, I3). BOOK_002_3 implies desire/flirtation without contact (I4). BOOK_002_5 is emotional bonding/reassurance (I2). Several sentences (BOOK_002_6, _9, _10, _11, _13, _15) reference anal plugs, nipple rings, or body jewelry in explicitly sexual/genital contexts (I6). No single code reaches 70%, so the dominant code is MIXED.
- **C adjudicate:** `MIXED`
  - Lexical consensus I5 (emotional vulnerability/declaration) aligns with the taxonomy's primary code 8.3a (Commitment Symbols & Love Tokens) and secondary 4.5 (Reconciliation, Commitments & HEA). The contextual dominant is MIXED, suggesting the topic spans symbolic/material commitment acts (rings, tokens, vows) and verbal/emotional declarations of love or reconciliation — both of which map to I5 without requiring physical affectionate contact. Pass B I0 elements (domestic/HEA logistics) may be present as background but are subordinate to the emotionally charged commitment framing. No evidence of affectionate physical contact (kiss, hug, caress) is indicated by the taxonomy or lexical signal, so I3 is forbidden. The MIXED flag warrants manual review to confirm whether any sub-cluster carries I3 contact evidence or whether the topic should be split into a pure I0 HEA-logistics strand and an I5 declaration/token strand.
- **Action:** RETAXONOMIZE

---

## Topic 62 — Admitting You've Been Stupid

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** I0 (norm: I0)

> marnie, i’ve been stupid.

> about what an asshole i’ve been?” “

> you've done something dumb, but you'll get away with it this time.

> *(CELL_B, tertile=begin)* He’s really … I don’t know …” I forced myself not to supply the word dumb . “

> *(CELL_B, tertile=begin)* He was too proud of himself to detect the sarcasm in my words. “

### Pass A/B/C

- **A lexical:** `I7`
  - All keyword lists converge on verbal conflict and interpersonal hostility: Main contains insults ('stupid', 'idiot', 'fool', 'asshole', 'jerk', 'rude', 'dumb'), KeyBERT adds 'harshly', 'embarrassed', 'comments', POS adds 'annoying', 'remark', MMR adds 'hissed', 'overheard', 'harshly', 'embarrassed'. This is a verbal-conflict/insult cluster (I7). No affectionate physical contact cues are present anywhere, so I3 is rejected. No desire, gaze, consent, coercion, or explicit-sex cues present.
- **B contextual:** `I0`
  - All sentences in this topic revolve around expressions of foolishness, stupidity, or self-deprecation (e.g., 'stupid,' 'idiot,' 'fool,' 'foolish girl'). There is no physical contact, no desire, no intimacy, no consent talk, and no erotic content of any kind. These are purely evaluative/emotional statements about characters' perceived lack of intelligence or judgment — non-intimate narrative/dialogue content coded I0.
- **C adjudicate:** `I0`
  - Pass B contextual dominant (I0) is upheld. Taxonomy 4.5 (Reconciliation, Commitments & HEA) with secondary 3.3 (Ambivalence & Internal Conflict) confirms this cluster centers on relational resolution, future-planning, and emotional settlement rather than any affectionate physical contact. Lexical consensus I7 (likely driven by surface-level emotional vocabulary) is overridden: I7 requires demonstrated vulnerability/disclosure exchange, but the taxonomy anchor is HEA logistics and commitment talk, which maps squarely to I0. No i3-qualifying contact (kiss/hug/hold/caress/undress) is evidenced. Anti-collapse rules prohibit promotion to I3. I0 is the most specific and defensible code given domestic/HEA/reconciliation framing without physical contact evidence.
- **Action:** REINTERPRET

---

## Topic 82 — Touch Her and Your Family Suffers

- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Code:** MIXED

> that you’ll die if i didn’t touch you?

> one touch and you’ll never know lonely again .

> oh, i’ll touch her alright and you both will do as i say or your family will suffer.

> *(CELL_D, tertile=middle)* I’m careful to avoid her touch for fear it will set me ablaze.”

> *(CELL_D, tertile=end)* And tell those other girls that if they don’t keep their distance, I will scratch their faces.” “

> *(CELL_D, tertile=end)* I wish I could say it was touching and moving, but I hate funerals.

### Pass A/B/C

- **A lexical:** `I6`
  - Main contains explicit genital/oral terms (cock, pussy, suck, dick) forcing I6 — this is beyond kissing/caressing into explicit sexual contact. KeyBERT and MMR signal coercive or distressed dynamics (begged, terrified, hurts, warned, prodded, poked, gritted, dislike) pointing toward I9, but the explicit anatomical vocabulary in Main overrides to I6 as the dominant intimacy function. POS alone (dislike, hurts, lack, lady) lacks contact cues and would suggest I4 at most. I3 is rejected: while 'touch/touching/touched' appear in Main, the surrounding explicit genital terms indicate this is full sexual contact (I6), not mere affectionate touch (I3). Consensus lands on I6 given the explicit sexual vocabulary, with a note that coercive/distress cues are present but do not override the explicit-sex classification.
- **B contextual:** `MIXED`
  - The topic clusters around the word 'touch' used in highly varied contexts: (1) mundane/domestic prohibition or permission (I0 — quilts, objects, no intimacy); (2) desire/anticipation of touch without confirmed contact (I4); (3) coercive/threatening touch language (I9 — 'I'll touch her and you'll do as I say', threats of scratching, coercive framing); (4) consent negotiation ('Can I touch you?' — I8); (5) actual affectionate/erotic physical contact — caressing nipples (I3), and emotionally intimate mutual touch ('You let me touch you… not just your body, but you' / 'I touched you' — I3). BOOK_003_4 is the only sentence approaching explicit territory but describes non-genital caress (nipples caressed, not penetrative/oral/genital act), so I3 applies. No single code reaches 70%, yielding MIXED.
- **C adjudicate:** `MIXED`
  - Lexical consensus flagged I6, but the contextual dominant is MIXED and the taxonomy points primarily to 7.2 (Violence, Threats & Non-Sexual Coercion) with a secondary signal of 7.4 (Unwanted or Coercive Sexual Contact). There is no evidence of affectionate physical contact (kiss, hug, caress, consensual undressing), so I3 is forbidden. The I6 lexical signal likely reflects surface-level explicit vocabulary appearing within a coercive or threatening context rather than consensual erotic activity. The correct primary code is therefore coercive/non-consensual contact territory (I9 per the intimacy taxonomy) rather than I6 or I3. Because the topic straddles non-sexual coercion (7.2) and unwanted sexual contact (7.4), a MIXED designation is warranted and the topic should be retaxonomized away from consensual-intimacy codes. Manual review is required to confirm whether the explicit lexical items represent actual sexual acts under coercion (which would keep I9 with a 7.4 secondary tag) or are incidental vocabulary in a predominantly threat/violence context (which would resolve to I9 / 7.2 only).
- **Action:** RETAXONOMIZE

---

## Topic 83 — Reassured About Eating Regularly

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I0 (norm: I0)

> i've eaten every few hours.

> of course, i’ve never eaten one.”

> and then you'll return late again… you won't need to do that—be late—because you've eaten."

> *(CELL_D, tertile=begin)* Then I’ll go hungry because I’m not eating with you.’ ‘

> *(CELL_B, tertile=end)* Wow, you really must have been hungry.”

> *(CELL_B, tertile=end)* Oh, I really was starving. “

### Pass A/B/C

- **A lexical:** `I0`
  - All keyword lists center on eating, food, hunger, and meals (eat, hungry, food, eating, eaten, starving, appetite, meal, feeding, tasted, skipped). These are domestic/sustenance cues with no affectionate physical contact, desire, or erotic content. I3 rejected: no kissing, hugging, caressing, or undressing cues present. Coded I0 as mundane domestic/logistical content.
- **B contextual:** `I0`
  - All sentences in this topic revolve around hunger, eating, food, and feeding (including a vampire-feeding reference). There is no affectionate physical contact, no desire, no erotic content, and no relational negotiation beyond the domestic/logistical act of eating. Every sentence codes as I0 (domestic/logistical/everyday interaction). The vampire-feeding lines (BOOK_003_2, BOOK_003_4, BOOK_003_6) reference a supernatural feeding dynamic but contain no physical intimacy contact in the sentence itself. Dominant code is I0 at 100%.
- **C adjudicate:** `I0`
  - Lexical and contextual consensus both indicate I0. Taxonomy confirms 4.6 Emotional Safety, Reassurance & Caretaking with no secondary code suggesting physical contact. No evidence of affectionate physical contact (kiss, hug, hold, caress, or undress-as-prelude) is present. The content reflects care, reassurance, and emotional support without crossing into I2 (which would require explicit caretaking of a distressed/vulnerable state beyond baseline reassurance) or any higher intimacy code. I0 is the correct and most specific classification. Anti-collapse rules are satisfied: no I3 contact evidence exists.
- **Action:** KEEP

---

## Topic 86 — First Name Used at Last

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** I0 (norm: I0)

> i’ve known you for two whole years, and that is the first time you’ve ever called me by my first name.”

> you’ve outgrown that nickname.” “

> just between you and me, i’ve been working on a catchy superhero name.

> *(CELL_B, tertile=middle)* Doesn't it bother you in the least that you don't really know him?" "

### Pass A/B/C

- **A lexical:** `I2`
  - All keyword sets converge on a scene of identity/name disclosure with emotional vulnerability: 'name, nickname, real, knew' (Main) signal personal revelation; 'embarrassment, flushed, painful, concerned, introduced' (KeyBERT) indicate emotional exposure and social discomfort; 'embarrassment, painful' (POS) reinforce vulnerability; 'embarrassment, flushed, admit, shout, prodded' (MMR) suggest reluctant or pressured self-disclosure. This maps to I2 (emotional vulnerability, reassurance, caretaking through personal revelation). No affectionate physical contact cues (kiss, hug, hold, caress) are present anywhere, so I3 is rejected. No desire/gaze cues for I4/I10, no explicit content for I6, no coercion pattern for I9.
- **B contextual:** `I0`
  - All sentences in this topic revolve exclusively around names — asking for, giving, knowing, or forgetting names. This is purely social/logistical interaction with no affectionate physical contact, desire, emotional vulnerability, or any other intimacy function. I0 (domestic/logistical/neutral social exchange) is the most specific and appropriate code for every sentence. No I3 contact evidence exists anywhere in the topic.
- **C adjudicate:** `I0`
  - Pass B lexical consensus (I2) was driven by caretaking/reassurance surface vocabulary, but the contextual dominant (I0) and taxonomy placement in 4.2 Ongoing Courtship & Everyday Relational Bonding with secondary coding in 9.1 Dialogue Delivery & Speech Tags confirm the functional weight is domestic/logistical talk and routine relational maintenance rather than active emotional support or affectionate physical contact. No affectionate physical contact is evidenced (i3_contact_evidence: false), so I3 is forbidden. No desire-without-contact or erotic gaze signals elevate to I4/I10. The anti-collapse rules require keeping I0 when evidence is domestic/care/HEA talk without contact. I0 is therefore the correct final code.
- **Action:** REINTERPRET

---

## Topic 88 — Checking Her Feverish Temperature

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> no movement, her skin temperature clammy enough to make a ball of fear lodge in his gut. “

> now, [person], how has her temperature been?

> the nippiness that was still molesting her limbs, she hoped, was indeed because of the low temperature and not a foretoken of her entering his residence.

> *(CELL_A, tertile=middle)* Every time he opened her up she felt a surge of wind invade her body and send pricks through her skin.

> *(CELL_A, tertile=begin)* Chills shot up her spine and into her chest, causing her to arch her back, which made her breasts bounce just enough to command attention.

> *(CELL_A, tertile=middle)* The rusted metal felt cold on the back of her thighs, and the persistent wind blew loose strands of her hair directly into the low O’s of smoke she eased from the center of her dry mouth.

> *(CELL_D, tertile=end)* She seemed fidgety and hurried us along, as if the food might get cold.

> *(CELL_D, tertile=end)* Lydia and Simon became visibly pale and shock emanated from them.

> *(CELL_B, tertile=middle)* Pure, fiery heat spread along her legs all the way up to her face. “

> *(CELL_B, tertile=middle)* Her body coiled from the heated friction and the way he seemed to keep hitting her newly found g-spot.

### Pass A/B/C

- **A lexical:** `I4`
  - All four keyword lists converge on internal, embodied arousal/desire: heat, warmth, burned, shivered, melted, flooded, erupted, flared, heaved — classic physiological desire-response vocabulary (flushed cheeks, racing veins, body heat). No affectionate physical contact cues (no kiss, hug, hold, caress, or undress) appear anywhere. I3 is rejected per anti-collapse rules. The atmosphere/temperature framing reinforces desire-without-contact (I4) rather than explicit erotic gaze (I10) or explicit sex (I6).
- **B contextual:** `I5`
  - The overwhelming majority of sentences describe bodily sensations — chills, heat, burning, tingling, aching — that function as somatic/arousal responses rather than affectionate physical contact, explicit sex acts, or domestic/logistical content. These are coded I5 (physical/bodily sensation as intimacy marker). BOOK_003_2 explicitly references hitting a g-spot, indicating penetrative/genital stimulation and is coded I6. Four sentences (BOOK_002_1, BOOK_002_2, BOOK_005_1–3) are non-intimate contextual/action sentences coded I0. No sentence shows affectionate physical contact (kiss, hug, caress, hold), so I3 is not applied and i3_contact_evidence is false. I5 accounts for ~70% of sentences, making it the dominant code.
- **C adjudicate:** `I2`
  - Pass B lexical consensus (I4) reflects desire-adjacent language, but the contextual dominant (I5) and taxonomy metadata (4.6 Emotional Safety, Reassurance & Caretaking; secondary 1.2 Pain, Injury & Physical Vulnerability) together indicate the functional core is caretaking and reassurance rather than unresolved desire or erotic tension. No affectionate physical contact (kiss, hug, hold, caress, undress-as-prelude) is evidenced, so I3 is forbidden per anti-collapse rules. I4 is also inappropriate because the dominant function is not desire-without-contact but rather emotional safety provision in a context of physical vulnerability. I2 (Reassurance/Caretaking) is the most specific applicable code consistent with both the taxonomy metadata and the anti-collapse rules. No manual review required given clear taxonomy guidance.
- **Action:** REINTERPRET

---

## Topic 96 — Confessing Long-Standing Worry

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> i’ve been worried about you, [person].

> i’ve worried about you since i was twelve.

> i’ve been worried about you.” “

> *(CELL_D, tertile=middle)* You grew up worrying about having your basic needs met.

> *(CELL_D, tertile=middle)* Don't beat yourself up about it.

> *(CELL_B, tertile=begin)* We didn’t want to worry you.”

### Pass A/B/C

- **A lexical:** `I2`
  - All four representations center on worry, concern, fear, and reassurance ('assure', 'bothered', 'worries', 'fears', 'concerned'). These cues point to emotional caretaking and reassurance-giving (I2). There is no affectionate physical contact vocabulary (no kiss, hug, hold, caress, or undress), so I3 is rejected. No desire/gaze cues (I4/I10), no explicit content (I6), no coercion (I9), no consent negotiation (I8), and no domestic/HEA logistics (I0). The 'amusement' token is minor and does not shift the dominant function away from anxious concern and reassurance.
- **B contextual:** `I2`
  - Every sentence in this topic revolves around worry, concern, reassurance, and caretaking language ('Don't worry,' 'I was worried about you,' 'Don't beat yourself up'). There is no physical contact of any kind, no desire, no erotic content, and no domestic/HEA logistics. The function is purely emotional reassurance and caretaking, which maps exclusively to I2.
- **C adjudicate:** `I2`
  - Both lexical and contextual consensus converge on I2. The taxonomy assignment (4.6 Emotional Safety, Reassurance & Caretaking with secondary 3.2 Negative Emotions & Distress) is fully consistent with I2: the cluster captures verbal and emotional support, soothing, and caretaking behaviors in response to distress, without evidence of affectionate physical contact (kiss, hug, hold, caress, or undress-as-prelude). Anti-collapse rules confirm I3 is forbidden here. No domestic/logistics/HEA framing that would push toward I0. I2 is the most specific and accurate code.
- **Action:** KEEP

---

## Topic 100 — Promising to Find Her

- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Code:** I0 (norm: I0)

> i promise, i’ll bring her right back.”

> i’ll hurry and see if i can catch her.”

> i’ll look until she’s found.”

> *(CELL_A, tertile=end)* She won’t be able to leave, to rest, to pass over, whatever it is, until we find her.” “

### Pass A/B/C

- **A lexical:** `I0`
  - All keyword lists point to logistical/transactional interaction: 'find, meet, needs, leave, where' (Main) suggest practical navigation or scheduling; 'sir, mister, dismissed, urgency, hiding, replaced' (KeyBERT) indicate formal address, workplace or social hierarchy, and tension around decisions; 'urgency, excited, screen, decision, sir' (POS) reinforce a task-oriented or professional context; 'dismissed, dealing, planning, screen, expect, lingering, replaced' (MMR) confirm procedural/logistical dynamics. No affectionate-contact cues (kiss, hug, hold, caress, undress) are present anywhere. I3 is rejected because there is zero evidence of physical affectionate contact. No desire language rules out I4; no explicit erotic content rules out I6/I10. The dominant function is domestic/logistical/social navigation, coded I0.
- **B contextual:** `I0`
  - All sentences in this topic revolve around locating, finding, retrieving, or managing a third-party female character. The language is logistical and situational — searching for someone, handing her over, keeping her informed, not wanting to lose her as an employee. There is no affectionate physical contact (ruling out I3), no desire or erotic gaze (ruling out I4/I10), no emotional vulnerability or caretaking (ruling out I2), and no sexual content of any kind. The dominant function is purely practical/logistical coordination, coded I0.
- **C adjudicate:** `I0`
  - All three passes converge on I0. The taxonomy confirms the dominant function is Promise/Vow/Future-Tense Speech Acts (9.2), with Emotional Safety/Reassurance as a secondary signal (4.6). Neither category implies affectionate physical contact; they describe verbal or declarative acts oriented toward relational commitment and HEA scaffolding. No lexical or contextual evidence of kissing, hugging, caressing, or undressing. I3 is therefore forbidden per anti-collapse rules. The secondary 4.6 signal could warrant I2 consideration, but reassurance here is embedded within forward-looking vow/promise discourse rather than active caretaking, so I0 remains the most specific and accurate code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 101 — Smoothing Loose Strands of Hair

- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Code:** I3 (norm: I3)

> she smoothed her hair. “

> he reached out, the most fascinating man she’d ever encountered, and smoothed a strand of her hair. “

> he smoothed back a few loose strands of hair at her temple, his gaze roving over her face. “

> *(CELL_B, tertile=middle)* She threaded her fingers through his hair, pressing his face in closer to her aroused flesh. “

> *(CELL_B, tertile=end)* He released her breasts and twined a long, thick lock of her blonde hair around his hand.

> *(CELL_B, tertile=end)* Candy raised her head and smiled down to him as she ran her fingers through his dark hair.

> *(CELL_B, tertile=middle)* By the time he raised his head and drew away from her, she was breathless and panting. “

> *(CELL_B, tertile=end)* a feminine voice chirped as a gorgeous, petite brunette threw herself into JD’s arms. “

> *(CELL_C, tertile=middle)* Sasha moved his hair away from his face and stuck it behind his ear. “

> *(CELL_C, tertile=begin)* She winked at him and was gone a second later, her magenta ponytail bouncing down her back, expertly navigating her way through the crowd.

> *(CELL_C, tertile=middle)* Could probably do with a couple myself,’ Bonnie laughed as he scratched at his thin threads of white hair.’ ‘

### Pass A/B/C

- **A lexical:** `I3`
  - All four keyword sets converge on non-genital affectionate physical contact involving hair. Main: 'stroked, brushed, tucked, fingers, hand, ear, strand/strands' — direct tactile caress of hair. KeyBERT: 'stroking, smoothed, patted, tugged, curled' — explicit gentle touch verbs. POS: 'fingertips, warmth, damp, loose ends' — sensory descriptors of physical contact. MMR: 'stroking, smoothed, absently, breathlessly, clinging, laced' — reinforces tender, intimate physical gesture. The contact is clearly non-genital (hair-touching/caressing), placing this firmly in I3 rather than I6. No erotic-gaze-only (I10) or desire-without-contact (I4) pattern; actual tactile contact is evidenced throughout. I3 is warranted.
- **B contextual:** `MIXED`
  - The topic clusters around hair-touching and physical contact with hair as a recurring motif. Sentences split across several codes: BOOK_001_1 involves pressing face to aroused flesh (genital/oral → I6); BOOK_001_2 involves releasing breasts and handling hair during a sexual encounter (I6 context, genital/breast contact); BOOK_001_3 is a non-genital caress (fingers through hair, I3); BOOK_001_4 implies withdrawal from an intimate act with breathlessness suggesting oral/genital activity (I6); BOOK_001_5 is an erotic gaze/comment on genitalia without contact (I10); BOOK_001_6 is an embrace (I3); BOOK_002_1 is tucking hair behind ear — affectionate touch (I3); BOOK_002_2 is departure/movement, no contact (I0); BOOK_002_3 'stroked it' — ambiguous but in context likely affectionate touch (I3); BOOK_004_1 is self-scratching hair, no intimacy (I0); BOOK_005_1 is self-grooming/emotional recovery (I0); BOOK_006_1–3 are tender hair-tucking/brushing gestures (I3); BOOK_006_4–6 are self-grooming or metaphorical (I0); BOOK_007_1 is stroking hair (I3); BOOK_007_2 is self-grooming (I0); BOOK_007_3 is noticing hair, no contact (I0). No single code reaches 70%, so MIXED.
- **C adjudicate:** `I3`
  - The lexical consensus (I3) and taxonomy assignment (2.2 Kissing & Non-Explicit Affection) both point to affectionate physical contact as the dominant function. The secondary taxonomy (1.6 Character Appearance & Self-Presentation) is consistent with appearance-noticing as a prelude to or accompaniment of non-explicit physical intimacy (e.g., noticing a partner's appearance before or during a kiss/embrace), not as a standalone erotic gaze (I10) or desire-without-contact (I4). The contextual dominant being MIXED reflects the blending of appearance-awareness with contact, but the primary intimacy function is affectionate physical contact. Anti-collapse rules are satisfied: there is positive evidence of kissing/non-genital caress/holding, so I3 is not forbidden. No domestic/logistics/HEA-only signal warrants I0, no explicit genital content warrants I6, and no coercion or consent negotiation is indicated. REINTERPRET is chosen to clarify that appearance description here serves as a framing device for I3 contact rather than an independent I10 or I4 function.
- **Action:** REINTERPRET

---

## Topic 104 — Stepping Out of Panties and Jeans

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I4 (norm: I4)

> she looked into his gaze as she took her panties to her ankles and stepped out.

> deliberately julie ignored the order, and instead crouched down to remove the shorts dangling around her ankles and to untie her shoes.

> once on her porch, she shed his t shirt and threw that at him too, he fumbled trying to quickly get it off his face.

> *(CELL_B, tertile=end)* He grasped the soft white cotton of her thin panties and yanked them down to her ankles.

> *(CELL_B, tertile=begin)* He pulled at her shirt, untucking it from the skirt’s waistband, allowing his hands access to the flesh of her torso.

> *(CELL_B, tertile=middle)* After that, he quickly pulled her clothes on, denying himself further access to her silky flesh. “

> *(CELL_B, tertile=begin)* She tugged the tight fabric down and sucked in her breath as it bunched around her hips.

> *(CELL_B, tertile=begin)* Wearing only her white cotton briefs and T-shirt, she pulled down the covers, sliding under them.

> *(CELL_B, tertile=begin)* She hissed and tried to shift in a way that wouldn't be too risqué since her skirt was quite short and at Gen's urging, she had gone commando: no bra or thong. “

> *(CELL_B, tertile=end)* Deborah asked in wonder as she began pulling off her own clothes. “

> *(CELL_B, tertile=end)* She tugged down her skirt, took off her shoes, and climbed off the car.

### Pass A/B/C

- **A lexical:** `I3`
  - All four representations converge on undressing-as-prelude: Main contains 'jeans, pants, shirt, zipper, panties, button, bra, undid, pulled' — explicit removal of clothing items; KeyBERT adds 'tugged, fumbled, loosened' (manual manipulation of clothing); POS adds 'thigh, waist, snaps, edges' (body-proximate contact points); MMR adds 'fumbled, loosened, snaps, tearing, hitched, ripping' (forceful/urgent undressing actions). The cluster describes the physical act of undressing another person (or being undressed), which per the anti-collapse rules qualifies as 'undress-as-prelude' affectionate/erotic physical contact → I3. There is no genital/oral/penetrative language present, so I6 is not warranted. I3 is confirmed, not rejected.
- **B contextual:** `I6`
  - The overwhelming majority of sentences depict undressing of self or partner in an explicitly sexual context — removing underwear, pants, breeches, shorts with hand-to-genital contact — which constitutes undressing as direct prelude to or part of explicit sexual activity (I6), not merely affectionate undressing (I3). BOOK_001_5 shows an erotic gaze without contact (I10). BOOK_003_2 ('He released her waist') is a brief non-genital physical contact/release gesture coded I3. All other undressing sentences are coded I6 because they are either explicitly genital (BOOK_002_6, BOOK_003_1, BOOK_003_4) or occur within a clearly explicit sexual encounter context where undressing is the immediate prelude to penetrative/oral/genital acts.
- **C adjudicate:** `I4`
  - Lexical consensus (I3) likely reflects surface-level physical description vocabulary, but the taxonomy metadata explicitly places this topic under Attraction & Sexual Tension (2.1) with Character Appearance as secondary — a pairing that signals desire/gaze rather than enacted contact. Contextual dominant I6 is not supported without evidence of genital/oral/penetrative acts. No affectionate physical contact (kiss, hug, hold, caress, undress-as-prelude) is evidenced, so I3 is forbidden per anti-collapse rules. The dominant function is unfulfilled or building desire triggered by appearance, which maps cleanly to I4 (desire without contact). I6 would require explicit sexual act evidence absent here. I4 is the most specific defensible code.
- **Action:** REINTERPRET

---

## Topic 119 — Offering to Keep Her Safe

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> come on, i’ll protect you.”

> you’ll protect me?” “

> i can protect you from crystal, but you’ll have to let me.

> *(CELL_D, tertile=begin)* I’m your man for getting you to the point of passing out, if you ever want to take that risk.”

> *(CELL_C, tertile=middle)* At least in LA you’d both have protection; you know my security guys are some of the best in the business.

> *(CELL_C, tertile=end)* I didn’t think security would leave you standing out here like this.’ ‘

### Pass A/B/C

- **A lexical:** `I2`
  - All four keyword lists center on protection, safety, threat, and guarding ('safe, protect, protection, dangerous, keep, defend, safety', 'protect, guarded, secure, threat, assure, precious', 'threat, determination, protect, secure, precious', 'guarded, dangerously, assure, inevitable, threat, determination'). This is classic reassurance/caretaking/protective-hero function (I2). The single token 'caressed' in MMR is insufficient to establish affectionate physical contact as a topic-level theme — it appears as one outlier word among overwhelmingly protective/security-oriented vocabulary. No kissing, hugging, holding, or undressing cues are present. I3 is rejected: the anti-collapse rule requires actual affectionate physical contact as a dominant cue, which is absent here.
- **B contextual:** `I2`
  - Every sentence in this topic revolves around reassurance of safety, protection pledges, and caretaking language ('I'll protect you,' 'You're safe with me,' 'I have to get you to safety,' 'check you got there safely'). There is no affectionate physical contact described anywhere, ruling out I3. There is no desire, gaze, consent negotiation, coercion, or explicit sexual content. The function is purely emotional reassurance and caretaking, which maps squarely to I2 across all 20 sentences.
- **C adjudicate:** `I2`
  - Lexical and contextual consensus both indicate I2. Taxonomy confirms 4.6 Emotional Safety, Reassurance & Caretaking with no secondary code suggesting physical contact. No affectionate physical contact evidence is present, so I3 is forbidden per anti-collapse rules. The signal is purely reassurance/caretaking without domestic/logistics/HEA framing that would push toward I0. I2 is the correct and most specific code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 124 — Scooped Up in A Tight Hug

- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Code:** I3 (norm: I3)

> emma followed suit, and rebecca scooped her up in her arms and hugged her tight.

> he hugged her back.

> i stood up with her and hugged her. “

> *(CELL_A, tertile=begin)* He pulled me into his arms, wrapping me in a tender embrace. “

> *(CELL_C, tertile=begin)* She hugged Luke tightly for a moment, then rested one hand on the German Shepherd’s solid, eighty-pound body and struggled to her feet.

> *(CELL_C, tertile=end)* She seemed a little surprised to see Michael, but delighted too, greeting the boy with a hug.

> *(CELL_C, tertile=end)* Becky tumbled out of the wagon into Sorrel’s arms in a desperate hug.

### Pass A/B/C

- **A lexical:** `I3`
  - Main is dominated by explicit hug/embrace vocabulary ('hug', 'hugged', 'hugging', 'embrace', 'tightly', 'arms') — direct affectionate physical contact cues, clearly I3. KeyBERT reinforces with 'hugged', 'squeeze', 'patted', 'affection', 'fiercely', 'tightly' — all physical contact markers, I3. MMR confirms with 'hugged', 'draped', 'fiercely', 'welcoming' — physical contact present, I3. POS is more abstract ('reassuring', 'affection', 'promises', 'welcoming', 'crowd') with no direct contact verb, leaning I2 (reassurance/caretaking). Consensus is I3 because three of four representations contain unambiguous affectionate physical contact cues (hugging, embrace, squeeze, patted, draped), satisfying the i3_contact_evidence requirement. I3 is not rejected; it is the most specific applicable code given the explicit hug/embrace lexicon across the majority of representations.
- **B contextual:** `I3`
  - Every sentence in this topic depicts affectionate physical contact in the form of hugging, embracing, or holding — the canonical I3 acts. BOOK_004_6 also includes a kiss, which remains I3 (kissing is non-genital/non-penetrative contact). BOOK_005_2 includes a hug plus a directive to hold a hand, both physical contact acts. No sentence rises to explicit sexual/genital activity (I6), nor is any sentence limited to desire without contact (I4) or purely domestic/logistical talk (I0). I3 is therefore the most specific and correct code for all 20 sentences, yielding a 100% proportion.
- **C adjudicate:** `I3`
  - Lexical and contextual consensus both converge on I3. Taxonomy 2.2 (Kissing & Non-Explicit Affection) is the primary classification, with 4.6 (Emotional Safety, Reassurance & Caretaking) as secondary, consistent with I3 criteria requiring actual affectionate physical contact such as kissing, hugging, holding, or caressing. The secondary emotional-safety dimension does not override the primary contact evidence; it contextualizes the affective register of the contact. No evidence of genital/oral/penetrative acts that would elevate to I6, no coercion (I9), no consent negotiation (I8), no isolated erotic gaze (I10), and no purely domestic/logistical content (I0). Anti-collapse rules are satisfied: I3 is warranted by positive contact evidence, not by default.
- **Action:** KEEP

---

## Topic 128 — Confessing How Much You've Missed

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** I2 (norm: I2)

> i’ve missed most of his life already.

> and, god, how i’ve missed this.”

> i’ve come to realize that you are the one thing in my life i don’t want to miss.

> *(CELL_C, tertile=middle)* The suckhead you brought back with you here tonight…I saw it all.”

> *(CELL_C, tertile=end)* While I was in there, I also brought you something I thought you might be missing.”

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords ('miss', 'missed', 'missing', 'misses') strongly signal emotional longing and verbal expression of absence/yearning — classic I2 (emotional reassurance/vulnerability). KeyBERT adds 'solemnly', 'honestly', 'repeated', suggesting earnest emotional declarations; 'sir' and 'hi' indicate interpersonal address without physical contact cues. POS keywords ('precious', 'voices', 'elevator', 'opportunity', 'pieces') suggest an emotionally charged conversation, possibly in a confined space, with no physical contact implied. MMR reinforces this with 'solemnly', 'breathlessly', 'thoughtfully', 'considering' — all adverbs of emotional tone during speech, not physical action. 'Pressing' could suggest urgency in speech rather than physical contact. No kissing, hugging, caressing, or undressing cues appear in any representation. I3 is rejected: zero affectionate-contact evidence across all four keyword sets. The dominant function is emotional expression of longing and earnest verbal communication, coding to I2.
- **B contextual:** `I2`
  - The overwhelming majority of sentences express longing, missing someone, or emotional yearning for reunion — classic I2 (emotional reassurance/caretaking/attachment expression) with no physical contact described. A few sentences use 'miss' in a non-relational/literal sense (missing a ball, missing a piece) coded I0. BOOK_006_3 references an orgasm in a conditional/instructional frame, indicating desire/anticipation without contact, coded I4. No sentence depicts actual physical contact (kiss, hug, caress), so I3 is forbidden and i3_contact_evidence is false.
- **C adjudicate:** `I2`
  - Both lexical consensus and contextual dominant agree on I2. The taxonomy metadata (4.5 Reconciliation, Commitments & HEA; secondary 3.1 Positive Resolution, Relief & Emotional Payoff) is fully consistent with I2: these constructs center on emotional reassurance, relational repair, and affective payoff without requiring affectionate physical contact. No evidence of kissing, hugging, holding, caressing, or undressing-as-prelude is present, so I3 is forbidden per anti-collapse rules. The content does not resolve to domestic/logistics/HEA talk alone (which would push toward I0), nor to explicit desire without contact (I4). I2 is the most specific and best-supported code.
- **Action:** KEEP

---

## Topic 135 — Waiting As Long As It Takes

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I4 (norm: I4)

> well, golly, i'll hurry as fast as i can.

> i will wait for you, even if you find me stiff with rheumatics, making clothes for my grandchildren, i’ll be waiting for you.’

> i’ve waited forever for you, and i’ll be damned if i’m not going to make sure you enjoy this.” “

> *(CELL_D, tertile=middle)* They will be waitin’ by now, for we have been gone overlong.”

> *(CELL_C, tertile=begin)* If you want to wait for a few minutes, I can pull up their itinerary.” “

### Pass A/B/C

- **A lexical:** `I4`
  - All keyword sets converge on desire/longing without physical contact. Main keywords (wait, hurry, waiting, quick, waited) signal urgent anticipation. KeyBERT confirms 'anticipation' as the dominant semantic. POS adds 'begging, anticipation, embarrassed, clinging' — clinging could suggest physical proximity but is not affectionate contact per se, and 'begging' points to unfulfilled desire rather than enacted intimacy. MMR reinforces 'begging, anticipation, embarrassed, clinging' alongside 'chased' and 'temperature' (arousal cue), all consistent with yearning/desire without consummation. No kissing, hugging, caressing, or undressing cues are present, so I3 is rejected. The cluster describes the emotional and physical tension of wanting/waiting — the hallmark of I4 (desire without contact).
- **B contextual:** `I0`
  - All sentences in this topic revolve around the concept of waiting — either literal waiting, urgency, or scheduling/logistics. There is no affectionate physical contact, no desire expression, no erotic content, and no emotional intimacy beyond neutral interpersonal communication. The topic functions as logistical/temporal coordination (I0). I3 is forbidden as no physical contact is present.
- **C adjudicate:** `I4`
  - Pass B produced a split between I4 (lexical consensus) and I0 (contextual dominant). Adjudication favors I4. The taxonomy metadata confirms primary placement in 2.1 Attraction & Sexual Tension, which is definitionally desire-without-contact territory. The secondary tag (4.5 Reconciliation/HEA) introduces some domestic/commitment coloring that drove the I0 reading, but HEA framing alone does not override the primary attraction signal unless physical contact is evidenced — and no affectionate contact evidence is present (i3_contact_evidence: false). Anti-collapse rules prohibit defaulting to I3 without contact, and the I0 reading is insufficient to override the taxonomy-confirmed attraction function. Final code is I4: desire/tension present, no physical contact realized.
- **Action:** REINTERPRET

---

## Topic 151 — Agreeing to Stop When Asked

- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Code:** I8 (norm: I8)

> stop it, or i’ll be tempted to do something i shouldn’t.”

> as long as i know you'll stop when i've had enough."

> coz i don’t know if i’ll be able to stop myself.

> *(CELL_B, tertile=middle)* Don’t stop,” Dan begged, his voice tight and breathless. “

> *(CELL_B, tertile=middle)* Stevie, no, you don’t have to ...” “Just stop it.”

> *(CELL_B, tertile=middle)* Stop it , he told himself sternly.

### Pass A/B/C

- **A lexical:** `I8`
  - The dominant lexical cluster revolves around stopping, preventing, and being unable — language of restraint, hesitation, and negotiation rather than affectionate physical contact. 'Stop/stopped/stopping/can/want/need' in Main suggest internal conflict about proceeding, which could be desire (I4) but the broader pattern across KeyBERT ('stops, prevent'), POS ('unable, opportunity'), and MMR ('altogether, stops, prevent, unable, answering, opportunity') points strongly to consent negotiation or a pause/refusal dynamic — classic I8 territory. 'Roughly' in MMR adds a coercive edge but is insufficient alone for I9 without stronger coercion cues. No affectionate-contact vocabulary (kiss, hug, hold, caress, undress) is present anywhere, so I3 is rejected. Consensus lands on I8 (consent/negotiation talk) as the most specific fit for a scene where characters are discussing or enacting stopping/preventing an intimate act.
- **B contextual:** `MIXED`
  - The topic clusters around the word 'stop' in intimate contexts. BOOK_002 sentences ('Don't stop,' 'Do you want me to stop?', 'Once I start I won't stop') and BOOK_001_5 ('Don't stop, Dan begged, voice tight and breathless') strongly imply ongoing sexual activity → I6. Sentences framing stopping as a request or negotiation mid-encounter ('Do you want me to stop?', 'You'd better stop then', 'Stop it') function as consent/boundary negotiation → I8. BOOK_001_6 is internal desire-suppression with no contact → I4. BOOK_003 sentences are non-intimate/logistical → I0. BOOK_004_5 is emotional disclosure/caretaking → I2. No sentence describes affectionate physical contact (kiss/hug/caress), so I3 is absent. No single code reaches 70%, yielding MIXED.
- **C adjudicate:** `I8`
  - Lexical consensus (I8) and taxonomy assignment (2.5 Sexual Negotiation, Safety Preparation & Boundaries) are mutually reinforcing. The contextual dominant is MIXED, reflecting the secondary taxonomy signal of attraction/tension (2.1), but the primary function is negotiation and boundary communication — verbal or gestural consent-seeking, safety discussion, or readiness checking prior to physical escalation. No affectionate physical contact (kiss, hug, caress, undress-as-prelude) is evidenced, so I3 is forbidden per anti-collapse rules. The secondary attraction/tension signal does not override the primary I8 classification; it merely explains the MIXED contextual read. I8 is retained as the dominant code. No split is warranted because the secondary signal (I4/I10-adjacent tension) is subordinate and does not constitute a separable topic cluster. Manual review is not required given strong cross-pass consensus.
- **Action:** KEEP

---

## Topic 155 — Stop Running or Be Claimed

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I4 (norm: I4)

> if it gets triggered, i'll"—he corrected himself—"one of us will come running.

> you didn’t mean to, but...if you don’t run right now, i’ll lay claim to you.

> stop running and you’ll find out.” “

> *(CELL_C, tertile=middle)* No sense in running in circles when a straight line will get you there faster.”

> *(CELL_C, tertile=end)* I'm going to have to be the one to run things around here." .

> *(CELL_D, tertile=begin)* I wondered if you had been set adrift as a punishment or were running away from someone.” “

### Pass A/B/C

- **A lexical:** `I9`
  - All keyword sets converge on a pursuit/flight scenario: 'run, running, ran, away, race, fast' (Main) signal flight; 'chased' (KeyBERT, MMR) is the clearest cue of coercive pursuit; 'commander, instincts, warned, planning' (POS/MMR) suggest a threatening authority figure orchestrating the chase; 'poised, scenario, tracks, climb' reinforce a tense, danger-laden physical confrontation. No affectionate contact cues are present anywhere, so I3 is rejected. The dominant intimacy function is coercion/threat (I9): one party is fleeing or being hunted by another in a power-imbalanced, non-consensual dynamic.
- **B contextual:** `I0`
  - All sentences in this topic revolve around the literal or figurative act of running/fleeing — characters escaping danger, being urged not to run, or discussing flight. There is no affectionate physical contact, no desire, no erotic content, and no relationship-building dialogue. The topic functions as plot/action logistics (flight/pursuit), coded I0 throughout.
- **C adjudicate:** `I4`
  - Pass B lexical consensus flagged I9 (coercion), while contextual dominant read I0 (domestic/logistics). Neither is well-supported on adjudication. The taxonomy metadata — 2.1 Attraction & Sexual Tension with secondary 4.7 Jealousy & Possessive Romance Conflict — points to desire and possessive tension as the operative functions. There is no evidence of affectionate physical contact (I3 is forbidden), no explicit sexual act (I6 excluded), and no clear consent negotiation scene (I8 excluded). The coercive framing (I9) likely reflects possessive jealousy rhetoric rather than a discrete coercion event, and the I0 read likely captured surface-level domestic language masking underlying tension. The most specific and defensible code is I4 (desire without contact), with possessive/jealousy dynamics as a secondary construct. Manual review is flagged because the I9 signal from Pass B cannot be fully dismissed without inspecting raw topic tokens for coercive language versus possessive-attraction hyperbole.
- **Action:** REINTERPRET

---

## Topic 156 — Reaching Into The Bedside Drawer

- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Code:** MIXED

> rax stands, slides open the drawer on the bedside table, and takes out a box of condoms.

> i reached over to the bedside cabinet drawer and pulled out a condom; i tore it open and rolled it down my cock.

> he opened the drawer of his bedside table and grabbed a condom, put it on, and was back on top of me in a flash.

> *(CELL_B, tertile=middle)* It was filled with little packets of lube and a variety of condoms.

> *(CELL_B, tertile=middle)* He blindly grabbed one of the lube pillows and tore the cheap plastic open.

> *(CELL_B, tertile=begin)* He came back in, the condom managed, the look on his face grim. “

> *(CELL_B, tertile=begin)* He hooked his fingers into the sides of her panties and tugged them down her legs, then drew back for a moment, opening the condom and rolling it on quickly before he positioned himself between her thighs.

> *(CELL_B, tertile=begin)* It was open, from when he’d taken out the condom and thrown it onto the ground.

> *(CELL_B, tertile=begin)* She’d absolutely benefitted from the acquisition of a box of condoms.

> *(CELL_B, tertile=begin)* She’d been walking around her bedroom in her bra and panties for the past twenty minutes, a tampon on the nightstand, right next to an unopened pregnancy test.

### Pass A/B/C

- **A lexical:** `I6`
  - All four representations converge on explicit sexual preparation/activity. Main keywords (condom, condoms, lube, lubricant, rolled) are unambiguous contraceptive/sexual-lubricant items used in genital/penetrative sex contexts. KeyBERT adds fumbled, popped, fingertips, plastic — physical handling of these items immediately pre-coitus. POS adds inevitable, hopeful, ripping (condom wrapper), buying — anticipatory and preparatory cues. MMR adds ripping, fumbled, reaches, strained — physical actions consistent with condom application. The cluster as a whole describes the logistical/physical preparation for penetrative sex, placing it firmly in I6 (explicit sex or its direct physical prelude involving genital-contact items). I3 is rejected: no affectionate-contact cues (kiss, hug, caress, embrace) are present; the contact implied is genital/penetrative in nature, which falls under I6 not I3.
- **B contextual:** `MIXED`
  - This topic centers on condom and lube logistics surrounding sexual encounters. Sentences split between I8 (consent/safety negotiation — discussing whether to use condoms, acquiring them, virginity disclosure) and I6 (explicit sexual act preparation — rolling on a condom, using lube during intercourse, undressing as direct prelude to penetrative sex). No sentence shows affectionate non-genital contact, so I3 is excluded. Neither I8 nor I6 reaches 70%, yielding MIXED.
- **C adjudicate:** `MIXED`
  - Lexical consensus flagged I6 and taxonomy primary is 2.5 Sexual Negotiation/Safety Preparation, with secondary 2.3 Explicit Sexual Acts. This indicates the topic cluster contains both consent/negotiation language (I8) and explicit sexual content (I6), making a MIXED classification appropriate. I3 is not warranted because no evidence of affectionate non-genital contact (kiss/hug/caress) was surfaced as the dominant signal — the content sits at the boundary of pre-sexual negotiation and explicit acts. The topic should be retaxonomized to reflect the dual I8/I6 construct rather than collapsed into a single code. Manual review is required to determine whether individual documents within the topic can be split cleanly between negotiation-dominant (I8) and act-dominant (I6) instances, or whether the co-occurrence is intrinsic to the cluster.
- **Action:** RETAXONOMIZE

---

## Topic 157 — Swearing to Save Him From Himself

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** I0 (norm: I0)

> and you’ll get it, i swear,” [person].

> if [person] sees me like this, i'll die."

> and i might be young but i guess that just makes me lucky… i do love him and whether i have your help or not, i have to save him from himself… i know [person], i know what he’ll do, now that he thinks he has lost me.”

> *(CELL_B, tertile=middle)* Sam couldn’t understand it, and that bothered him.

> *(CELL_B, tertile=begin)* What else had Sam witnessed?

> *(CELL_B, tertile=begin)* Sam noticed stuff like that.

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords (names, 'good', 'optimism') suggest interpersonal reassurance/emotional exchange. KeyBERT cues ('begged', 'confessed', 'tense', 'willing', 'surely', 'ought') point to emotional negotiation, pleading, and confession — consistent with I2 (reassurance/caretaking/emotional support). POS keywords ('dislike', 'worries', 'enthusiasm', 'embarrassing', 'desperation', 'gritted') reinforce emotional tension and distress-management. MMR ('dislike', 'dump', 'worries', 'confessed', 'enthusiasm', 'gritted') similarly signals conflict-adjacent emotional processing. No affectionate physical contact cues (kiss, hug, caress, undress) appear in any representation, so I3 is rejected. No explicit desire or erotic gaze cues, so I4/I10 are rejected. The dominant signal is emotional reassurance, caretaking, and interpersonal tension resolution.
- **B contextual:** `I0`
  - All sentences in this topic consist solely of character name references ('Sam', 'Samantha', 'Steve'), brief name-calls, apologies, or minimal descriptive statements about a character named Sam. There is no affectionate physical contact, no desire, no erotic content, no consent negotiation, and no domestic/HEA discussion. The topic appears to be a character-name cluster with no intimacy function. All sentences are coded I0 (non-intimate/narrative/logistical).
- **C adjudicate:** `I0`
  - Pass B lexical consensus (I2) reflects caretaking/reassurance language, but contextual dominant (I0) and taxonomy placement in 4.5 Reconciliation, Commitments & HEA indicate the functional weight is on relational resolution, future-planning, and domestic/logistical consolidation rather than affective caretaking per se. No affectionate physical contact (kiss, hug, hold, caress) is evidenced in the topic signal, so I3 is forbidden. I2 is not warranted as the dominant code because the content is not primarily reassurance or caretaking but rather commitment talk and HEA framing. Secondary taxonomy 3.3 Ambivalence & Internal Conflict suggests some unresolved tension, but this does not elevate the code toward I4 (desire without contact) or I8 (consent). I0 is the most specific and accurate code: domestic/logistics/HEA talk without physical contact. No manual review required given clear taxonomy alignment.
- **Action:** RETAXONOMIZE

---

## Topic 161 — Reassuring Squeeze on The Shoulder

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

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

- **A lexical:** `I2`
  - Main keywords include 'scissoring' (a specific sexual act), which would normally point to I6. However, the remaining keyword lists (KeyBERT, POS, MMR) are dominated by emotional-regulation and reassurance cues: 'reassuring', 'calming', 'praying', 'emotions', 'shivered fiercely', 'nods', 'clenched' — all consistent with I2 (emotional support/caretaking). There is no affectionate physical contact vocabulary (no kiss, hug, hold, caress, or undress-as-prelude) across KeyBERT, POS, or MMR, so I3 is rejected. The single 'scissoring' term in Main may be a character name, slang, or noise term given the surrounding proper nouns (Noah, Phan, Cam, Tobias, Cameron, Beaumont, Ark), and it is not corroborated by any erotic or explicit cues in the other three representations. Consensus therefore falls to I2 (reassurance/emotional caretaking), with a noted disagreement flag due to the ambiguous Main signal.
- **B contextual:** `I0`
  - All sentences are non-intimate in function. They consist of character name references, internal monologue about stubbornness/animalistic tendencies, theological/biblical exposition, physical jostling in a conflict context (not affectionate), and brief emotional reactions (confusion, relief). None involve affectionate physical contact, desire, erotic content, or relational intimacy functions. I0 (non-intimate narrative/dialogue) is the most specific applicable code throughout.
- **C adjudicate:** `I2`
  - Pass B produced a split between I2 (lexical consensus) and I0 (contextual dominant). The taxonomy metadata confirms primary placement at 4.6 Emotional Safety, Reassurance & Caretaking with a secondary signal at 5.1 Family, Kinship & Parenthood. Neither axis points to domestic logistics, HEA planning, or affectionate physical contact. The I0 contextual read likely captured surface-level domestic/family framing, but the functional core is reassurance and caretaking — squarely I2. No evidence of physical contact (kiss, hug, hold, caress) is present, so I3 is forbidden. The correct resolution is RETAXONOMIZE to I2 under 4.6, with the 5.1 kinship signal noted as a secondary construct. No manual review required given clean taxonomy alignment.
- **Action:** RETAXONOMIZE

---

## Topic 165 — Confessing Long-Simmering Desire

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I4 (norm: I4)

> my god, i’ve been wanting you all day long, girl!” “

> i’ve been interested in you for a long time.” “

> i just want to be with you and hear more about what you’ve been doing all these years.

> *(CELL_C, tertile=end)* Shyam, I want to push him away, but he’s in everyone, even you!” “

> *(CELL_A, tertile=end)* I hate you more for saying no when I not only need you, but want you.”

### Pass A/B/C

- **A lexical:** `I9`
  - Main keywords ('want', 'need', 'wanting', 'wanted') suggest desire/longing, pointing to I4. However, KeyBERT ('sir') and POS ('unwilling', 'terms', 'comfortable', 'sir') introduce power-differential and reluctance cues. MMR clinches the code with 'unwilling', 'dislike', 'snatched', 'breathlessly', 'terms', 'sir' — a cluster signalling coercion or non-consensual pressure rather than mutual desire or explicit consent negotiation. 'Unwilling' + 'snatched' + 'dislike' + 'sir' (authority/power) = I9 (coercion). I3 is rejected: no affectionate-contact cues (no kiss, hug, hold, caress, or undress-as-prelude) appear in any representation. I8 (consent talk) is rejected because the framing is coercive rather than negotiated. Consensus is I9.
- **B contextual:** `I4`
  - The topic is dominated by expressions of desire, longing, and wanting ('I want you', 'I've wanted you for so long', 'You want me') without any depiction of actual physical contact, placing the majority in I4 (desire without contact). Several sentences express emotional need, reassurance, or caretaking ('I need you', 'I want to be here for you', 'What would I be without you?') coded I2. A few sentences are purely domestic/logistical or neutral ('I want us to be together forever', 'Don't you want pizza?', 'Why would you want my autograph?') coded I0. No affectionate physical contact is described anywhere, so I3 is forbidden. I4 reaches 55%, making it the dominant code.
- **C adjudicate:** `I4`
  - Pass B lexical consensus flagged I9 (coercion), but contextual dominant is I4 (desire without contact). No affectionate physical contact evidence is present, so I3 is forbidden per anti-collapse rules. The taxonomy placement under 2.1 Attraction & Sexual Tension with secondary 4.2 Ongoing Courtship supports I4 as the dominant code. The I9 signal warrants manual review to determine whether coercive dynamics are genuinely present or whether the lexical cues were surface-level false positives (e.g., forceful language of longing rather than actual coercion). If coercion is confirmed on review, reclassify to I9; if only tension/desire, retain I4.
- **Action:** REINTERPRET

---

## Topic 172 — Reporting to The Security Officer

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I0 (norm: I0)

> you’ll also report this to your regional security officer, yes?”

> i’ll have an armed officer [person] the room with you at all times, and i’ll watch through the glass.” “

> i’ve called the police, i’ll have you know.”

> *(CELL_B, tertile=end)* Do you think being worried over another officer’s absence justifies a breach in regulations?”

> *(CELL_B, tertile=end)* I give an order, and because I’m your superior officer, you are supposed to obey it.” “

### Pass A/B/C

- **A lexical:** `I0`
  - All keyword lists center on law enforcement, policing, and procedural/institutional activity (police, cop, officer, authorities, enforcement, evidence, weapons, secured, task, leads). KeyBERT adds 'protect,' 'evidence,' 'weapons,' 'sir,' 'secured' — all procedural/professional cues. POS and MMR reinforce this with 'activity,' 'unwilling partners,' 'task,' 'dealing,' 'stops' — suggesting a law-enforcement scenario, possibly involving reluctant cooperation. No affectionate physical contact cues present anywhere; I3 is rejected. No desire, gaze, consent negotiation, or explicit content cues; I4, I10, I8, I6 are all inapplicable. This is functional/plot-logistics content coded I0.
- **B contextual:** `I0`
  - All sentences in this topic revolve around law enforcement references — calling the police, being a cop, police/officer hierarchy and regulations. There is no romantic, intimate, or physical content of any kind. Every sentence is purely logistical/situational dialogue or narration with no affectionate contact, desire, or emotional intimacy. I0 (non-intimate/domestic/logistical) is the correct and most specific code for all sentences.
- **C adjudicate:** `I0`
  - Both lexical and contextual consensus converge on I0. The taxonomy confirms primary coding as Emotional Safety, Reassurance & Caretaking (4.6) with a secondary dimension of Risk/Danger/External Crises (7.3). There is no evidence of affectionate physical contact (no kissing, hugging, holding, caressing, or undressing-as-prelude), so I3 is forbidden per anti-collapse rules. The content reflects verbal or emotional reassurance and caretaking behaviors — potentially under conditions of external threat — which are characteristic of I0 (domestic/care/relational maintenance) or at most I2 (reassurance/caretaking without contact). Given the lexical consensus is firmly I0 and no contact evidence exists, I0 is the correct and most specific code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 175 — Gentleman Offers Steadying Support

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> the occurrences of the day were too full of interest to leave elizabeth much attention for any of these new friends; and she could do nothing but think, and think with wonder, of mr. [person]'s civility, and, above all, of his wishing her to be acquainted with his sister.

> mr. [person] placed his hand on [person]’s shoulder for support as mr. [person] barely walked out the front door.

> yes, but when i fell ill, it was apparent that i could not travel all the way to calais, so mr. [person] took me to the house of a friend of his: mr. [person].”

> *(CELL_B, tertile=end)* On his way to see Mistress Gwyllain to explain your…ah, unexplained arrival.”

> *(CELL_B, tertile=begin)* Shit," grunted Sheridan, apparently immune to Owen's considerable charms. "

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords (mr, bingley, miss, georgiana, bennet, pemberley) are Pride & Prejudice character/place names suggesting social/domestic context → I0. KeyBERT cues (kindly, concerned, affection, worrying, longing, struggling, injured) point to emotional caretaking and concern for others → I2. POS cues (passionate, distress, warming, exciting) suggest emotional intensity but no physical contact markers → I2. MMR cues (kindly, uncomfortably, passionate, distress, thoughtfully, encouraged, warming, consumed) reinforce emotional support/caretaking register → I2. No affectionate physical contact cues (kiss, hug, hold, caress, undress) appear in any keyword list; I3 is therefore rejected. Consensus lands on I2 (reassurance/caretaking/emotional support) as the dominant signal across three of four representations.
- **B contextual:** `I0`
  - The vast majority of sentences are logistical, social, or narrative references to named characters (Gwyllain, Sheridan, Pippen, Darcy) with no affectionate physical contact depicted. BOOK_001_4 ('save his climax for Gwyllain') and BOOK_003_5 ('Sheridan wanted this') imply desire without any described contact, coded I4. No kissing, hugging, caressing, or other physical contact is present, so I3 is forbidden. The dominant function is domestic/social/logistical interaction (I0).
- **C adjudicate:** `I2`
  - Pass B produced a split between I2 (lexical consensus) and I0 (contextual dominant). Taxonomy metadata confirms the primary construct is 4.6 Emotional Safety, Reassurance & Caretaking with a secondary of 5.2 Friends, Allies & Social Circles. There is no evidence of affectionate physical contact (no kiss, hug, hold, caress, or undress-as-prelude), so I3 is forbidden. The I0 signal likely reflects domestic/logistical framing within a caretaking exchange, but the dominant intimacy function is emotional reassurance rather than pure domestic logistics or HEA planning. I2 is therefore the correct resolution: it is more specific than I0 for content whose primary function is comfort-giving and emotional safety, and it does not require physical contact. No manual review needed.
- **Action:** REINTERPRET

---

## Topic 196 — Promising to Be A Good Team

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** MIXED

> maybe you’ll find out we make a good team in every way.” “

> we’ll nail that game, no problem.”

> we’ll make a good team.”

> *(CELL_D, tertile=begin)* For months now, we’d played that game of chicken with each other, an obvious magnetism between us each time we glanced at each other or ran into the other.

> *(CELL_D, tertile=end)* Like you’d have been playing with maps,” Vendelia scoffed. “

> *(CELL_C, tertile=middle)* You’re going to start playing things straight with Hailey, or I’ll kick your ass.” “

> *(CELL_C, tertile=end)* If you would kindly follow your guides to our play yard, we would like to get started.”

### Pass A/B/C

- **A lexical:** `I0`
  - All keyword sets point to games, strategy, and social/logistical maneuvering (play, game, team, player, video, moves, pieces, president, opportunity, maintain, afford, prove). These cues indicate competitive or strategic interaction — possibly metaphorical power play or literal gaming — with no affectionate physical contact, desire, eroticism, or intimacy-related language. I3 rejected: zero affectionate-contact cues. I4 rejected: no desire language. Consensus is I0 (domestic/logistical/non-intimate interaction or background narrative).
- **B contextual:** `MIXED`
  - The topic centers on 'playing games' — both literally (board/card games, plays, activities) and metaphorically (romantic/power games, flirtation, strategic behavior). No physical contact occurs in any sentence. BOOK_002_1 and the BOOK_006 cluster reference a mutual romantic game with magnetic tension, coded I4 (desire/tension without contact). BOOK_004_1 ('play games with us, big boy') and BOOK_007_1 ('two could play this game') also carry flirtatious/power-dynamic undertones, coded I4. The remaining sentences are logistical, social, or non-intimate uses of 'play/game', coded I0. No sentence meets the I3 threshold (no affectionate physical contact). Neither I0 nor I4 reaches 70%, so the dominant code is MIXED.
- **C adjudicate:** `MIXED`
  - Pass B lexical consensus was I0, but the taxonomy metadata flags a secondary dimension of 2.1 Attraction & Sexual Tension, producing a genuine MIXED signal. The contextual dominant is MIXED, meaning the topic cluster likely contains both low-stakes domestic/relational bonding language (I0) and desire/tension language without confirmed physical contact (I4). No affectionate contact evidence (kiss, hug, caress, undress-as-prelude) is present, so I3 is forbidden per anti-collapse rules. The topic should be retaxonomized to reflect both I4 (desire without contact) and I0 (courtship/bonding/HEA logistics) as co-present constructs, and flagged for manual review to determine whether the cluster should be split or kept as a MIXED unit.
- **Action:** RETAXONOMIZE

---

## Topic 197 — Lingering Farewell Kiss

- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Code:** MIXED

> in an attempt to take away the sting of her hasty departure, she went to lirzhan and kissed him — no quick peck on the cheek, but a lingering touch of mouth against mouth as she tried to show that she was leaving because she had to, not because she wanted to. “

> from what i’ve heard, she’s just lying around on her back, waiting for true love’s kiss.”

> and that they’ve only kissed.”

> *(CELL_A, tertile=middle)* It didn’t matter that he’d wanted to kiss her, even though he hadn’t even realized that he wanted to until right before she’d mentioned it.

> *(CELL_A, tertile=middle)* Although, when he really thought about it, he wasn’t quite sure why he shouldn’t have kissed her .

> *(CELL_A, tertile=middle)* There was something heartbreaking in the way she was gazing at him, as if she might die if he didn’t kiss her.

### Pass A/B/C

- **A lexical:** `I3`
  - Main keywords ('kiss', 'kissed', 'kissing', 'kisses') are unambiguous affectionate physical contact cues, directly satisfying the I3 contact requirement. MMR supports with 'lingering' and 'parted' (lips parting after a kiss), plus 'stirred' suggesting emotional/physical response to contact. KeyBERT and POS lack direct contact words and lean toward anticipatory/emotional states ('anticipation', 'curiosity', 'urgency', 'willing'), which alone would suggest I4 (desire without contact). However, the dominant signal across Main and MMR is actual kissing contact, not merely desired or imagined. I6 is rejected because no genital/oral-sex/penetrative cues appear. Consensus is I3 on the strength of explicit kiss vocabulary in Main and corroborating 'lingering'/'parted' in MMR.
- **B contextual:** `MIXED`
  - The topic centers on kissing — both as desire/anticipation and as actual physical contact. BOOK_001 sentences all describe wanting, regretting, or contemplating a kiss without confirmed contact occurring in the sentence itself → I4 (desire without contact). BOOK_002_1 ('Then he kissed her') is a direct act → I3; BOOK_002_2 is suppressed desire → I4; BOOK_002_3 ('asked me to kiss you goodnight') describes a kiss being relayed/requested and implies it occurred → I3; BOOK_002_4 ('spontaneously kissed her on the cheek') is direct contact → I3. BOOK_003 sentences are anticipation, speculation, and observation of desire → I4. BOOK_004_1 is commentary on kissing as intimacy without contact → I4; BOOK_004_2 ('Kiss me') is a request with no confirmed contact in the sentence → I4 (desire/request); BOOK_004_3 ('hugged and kissed a john') is actual contact → I3; BOOK_004_4 ('give your baby girl a kiss') is a request/question implying habitual contact → I3; BOOK_004_5 (gallant gesture, no contact described) → I4. Split is approximately 30% I3 / 70% I4; no single code reaches 70% threshold → MIXED.
- **C adjudicate:** `MIXED`
  - Lexical consensus I3 is overridden by the MIXED contextual dominant signal. The secondary taxonomy code (4.2 Ongoing Courtship & Everyday Relational Bonding) introduces I0/I4-range content — domestic bonding, courtship logistics, or desire-without-contact — that does not satisfy the anti-collapse rule requiring actual affectionate physical contact for I3 assignment. Without topic terms or representative documents confirming kissing, hugging, holding, caressing, or undressing-as-prelude, i3_contact_evidence cannot be affirmed. The topic appears to straddle I3 and I0/I4, making SPLIT or RETAXONOMIZE the appropriate action. A human reviewer should inspect representative documents to determine whether affectionate contact is genuinely present or whether the I3 lexical signal is driven by courtship/bonding language that mimics intimacy without physical contact.
- **Action:** RETAXONOMIZE

---

## Topic 199 — Shoved to His Knees

- **Taxonomy:** 7.4 — Unwanted or Coercive Sexual Contact
- **Code:** I0 (norm: I0)

> which must’ve totally gotten jacob’s rocks off, given the way he shoved me to my knees and whipped his cock out in no time flat.

> i’ll have the same,” [person]. “

> logan asked, “do you really think you’ll find a candidate at consuela’s party?” “

> *(CELL_B, tertile=middle)* It wouldn’t be the first place he’d look, but Logan didn’t have a reason to lie to him either. “

> *(CELL_B, tertile=middle)* Two nights ago, Jacob had been shot at just because he came too close.

> *(CELL_A, tertile=end)* Xavier had come, and he stood with Lindsay, talking and laughing with her.

> *(CELL_A, tertile=begin)* Give the damn thing back to Xavier and tell him to keep it out of Shiftertown.”

> *(CELL_B, tertile=middle)* Even Kelsey’s annoyance with him for talking to Chloe about their plans for a family seemed particularly couple-like.

> *(CELL_B, tertile=begin)* Kelsey was the only one with whom he’d been less than honest and that had clearly been a necessary evil. “

### Pass A/B/C

- **A lexical:** `I9`
  - All keyword lists converge on coercion/manipulation dynamics: 'threats', 'dared', 'pretended', 'fraud', 'emotional', 'actions', 'claims'. The presence of 'threats' across KeyBERT, POS, and MMR, combined with 'fraud' and 'pretended' in Main/MMR, and 'dared' in KeyBERT/MMR, points clearly to coercive or manipulative interpersonal behavior (I9). No affectionate physical contact cues are present anywhere, so I3 is rejected. No explicit sexual content, so I6 is rejected. The emotional vocabulary ('emotional', 'emotions', 'concerned') is in the context of manipulation/coercion rather than reassurance, so I2 is rejected.
- **B contextual:** `I0`
  - All sentences in this topic involve named characters (Jacob, Logan Grey, Xavier, Kelsey, Kyle) in operational, logistical, or social-background contexts: mission coordination, intelligence gathering, character introductions, and interpersonal logistics. There is no affectionate physical contact, no desire expression, no erotic content, and no intimacy-related function. The topic is purely plot/logistics/character-relationship scaffolding, coded I0 throughout.
- **C adjudicate:** `I0`
  - Lexical consensus flagged I9 (coercive sexual contact), but contextual dominant is I0 (domestic/logistics/HEA). The taxonomy metadata assigns 7.4 Unwanted or Coercive Sexual Contact with no secondary codes, creating a direct conflict between the lexical signal and the contextual reading. Without topic-level word evidence confirming actual coercive or unwanted sexual contact in the cluster, the contextual dominant I0 is retained per anti-collapse rules. I9 requires evidence of coercion or unwanted contact; I0 requires domestic/logistical framing — the contextual pass supports the latter. However, the taxonomy metadata cannot be dismissed outright, so manual review is required to inspect the actual top words and representative documents before finalizing. No affectionate physical contact evidence exists, so I3 is forbidden.
- **Action:** RETAXONOMIZE

---

## Topic 204 — Promising to Care For Her Sister

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** I0 (norm: I0)

> i’ll need to finish dressing and leave a note for my sister.”

> yes, and soon you’ll be my sister.

> i’ll find a way to care for your mother and your sister.” “

> *(CELL_D, tertile=middle)* My sister’s still there with her husband, who’s a copper, and their three kids.

> *(CELL_A, tertile=begin)* You have not been paying close attention to your sister’s problems lately, have you?” “

> *(CELL_A, tertile=begin)* Your sister mentioned in passing that you are something of a recluse.” “

> *(CELL_A, tertile=end)* You mock your sister, but you will admit that she has great talents.” “

> *(CELL_A, tertile=end)* I realize that you are concerned for your sister’s happiness.

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords ('sister', 'sisters', 'sisterly', 'affection') point to familial/relational warmth and caretaking — I2 (emotional support/reassurance within a relationship). POS adds 'affection', 'permission', 'willing', suggesting relational negotiation with emotional warmth, still I2. KeyBERT ('asks', 'assume', 'willing', 'hi', 'speaking') and MMR ('introduce', 'direct', 'equipment', 'spending', 'expect') lean toward logistical/social interaction — I0. No affectionate physical contact cues (no kiss, hug, hold, caress, undress) appear in any representation, so I3 is rejected. The dominant signal across all reps is sisterly relational/emotional interaction without physical contact, making I2 the best consensus code over I0.
- **B contextual:** `I0`
  - Every sentence in this topic refers to sibling relationships (sisters, brothers-in-law, family dynamics) in a purely relational/social/domestic context. There is no affectionate physical contact, no desire, no erotic content, no emotional vulnerability, and no intimacy function beyond ordinary family reference. All sentences code as I0 (domestic/social/logistical/relational talk with no intimacy function).
- **C adjudicate:** `I0`
  - Pass B lexical consensus (I2) reflects caretaking/reassurance language, but the contextual dominant (I0) and taxonomy placement under 4.5 Reconciliation/Commitments/HEA with secondary 5.1 Family/Kinship indicate the functional core is domestic, logistical, or future-planning talk — not affectionate physical contact. No kiss, hug, hold, caress, or undress-as-prelude is evidenced. Anti-collapse rules prohibit I3 without confirmed contact. The I2 signal is subordinate and likely reflects emotional reassurance embedded within commitment/HEA dialogue rather than standalone caretaking. I0 is the correct and most specific code. No manual review required.
- **Action:** REINTERPRET

---

## Topic 208 — Pounded Into The Mattress

- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Code:** I6 (norm: I6)

> you’ve been in this bed before,” i say, glancing back at it. “

> i remain on the edge of the bed, watching him stalk out the door, feeling as if i’ve been shot in the chest.

> had my back not already been off the bed, i would’ve arched right up off it as he mercilessly used his full body strength to pound me into the plush mattress.

> *(CELL_B, tertile=end)* I move us back into the bed and pull the covers over both of us. "

> *(CELL_B, tertile=middle)* I take my shirt and trousers off and then lean down onto the bed. “

> *(CELL_B, tertile=middle)* I kick the door open to my bedroom and I lay her down on the bed.

> *(CELL_D, tertile=end)* I should have been in bed…I wanted to see Papa…He looked over at me and waved…’ He stopped talking, started to shake.

> *(CELL_D, tertile=end)* He wasn’t in the big bed that dominated the room, although the coverlet was rumpled.

> *(CELL_D, tertile=end)* Darren didn’t hog the pillows and kick all the covers from the bed.

> *(CELL_B, tertile=end)* He let himself in and sat down on the edge of the bed near my feet.

### Pass A/B/C

- **A lexical:** `I3`
  - Main keywords (bed, onto, mattress, pillow, covers, off) combined with KeyBERT cues (laying, scooted, stroking, positioned, inched, comfortable) and MMR cues (crawled, climbing, scooted, sits, bedside) collectively indicate physical movement onto a bed with stroking/caressing contact — 'stroking' is a direct affectionate-contact cue, and 'onto/mattress/covers off/laying/positioned' strongly suggest a prelude to or act of intimate physical contact. I3 is warranted because 'stroking' constitutes non-genital caress. POS keywords (snaps, ankles, suitcase, makeshift, destination) are more ambiguous/logistical, suggesting I0 in isolation, which drives the disagreement flag. No explicit genital/penetrative cues present, so I6 is rejected. The contact evidence from 'stroking' prevents I3 rejection.
- **B contextual:** `MIXED`
  - The topic clusters around bedroom/bed settings. Many sentences are purely positional or domestic (sitting on the edge of a bed, lying down alone, references to pillows/covers without another person) → I0. A subset involves affectionate physical contact: pulling covers over both people together (I3), undressing as a prelude to joining someone in bed (I3), picking up someone's hands (I3), laying her down on the bed (I3), pushing someone onto the bed (I3), easing legs onto the bed and pulling duvet (I3), stroking hair and easing both back onto the mattress (I3), leading to the bedroom by hand (I3). No genital/penetrative acts are described, so I6 is not warranted. No single code reaches 70%, yielding MIXED.
- **C adjudicate:** `I6`
  - The taxonomy metadata explicitly flags this as 2.3 Explicit Sexual Acts (primary), with 8.1 Domestic Spaces & Routines as secondary. The lexical consensus of I3 likely reflects surface-level physical-contact vocabulary (kissing, undressing, caressing) that serves as prelude or framing within a scene that escalates to or centers on explicit sexual acts. Under the anti-collapse rules, I3 is reserved for affectionate non-genital contact; when the primary taxonomy code is Explicit Sexual Acts, the correct intimacy code is I6. The MIXED contextual dominant suggests some tokens may be domestic/routine (I0) or non-genital contact (I3), but the dominant function per taxonomy is explicit sexuality. I3 contact evidence is marked false because the taxonomy overrides the lexical signal — the contact described is not merely affectionate but is part of explicit sexual activity. Manual review is required to confirm whether any sub-cluster of tokens genuinely represents standalone I3 moments warranting a SPLIT action.
- **Action:** REINTERPRET

---

## Topic 213 — Choosing Sex Without Commitment

- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Code:** I5 (norm: I5)

> i want very much to make love to you, but i'll be damned if i'll do it in a horror of a room like this.

> yeah, but in a couple of hours, i’ll want sex again.

> i’d rather there was love and friendship and commitment behind it, but if it’s a choice between sex without that stuff, or going home alone, i’ll take the sex, thank you.

> *(CELL_B, tertile=middle)* Sex was a big part of our past, Daisy, but you don't seem to want to talk about that.” “

> *(CELL_B, tertile=middle)* Although we brought each other to perfunctory orgasm in bed that night, we gave each other little pleasure.

> *(CELL_B, tertile=end)* Can’t speak for the others, but with me it’s not just the sex.

> *(CELL_B, tertile=end)* To have him sexually, feeling as I did, would be to take advantage of him; the bedroom door remained closed.

### Pass A/B/C

- **A lexical:** `I4`
  - Main keywords ('sex, love, make, intimate, want, intimacy, meaningless') signal desire and reflection on the meaning of sexual/intimate connection, but no affectionate physical contact cues (kiss, hug, hold, caress, undress) are present — pointing to I4 (desire without contact) rather than I3 or I6. 'Willing' in KeyBERT/POS could hint at consent negotiation (I8), but it is a single weak cue insufficient to override the dominant desire/reflection frame. POS and MMR terms ('inevitable, swimming, gazing, blowing, ability, plastic, concerned') are largely abstract or ambiguous and do not introduce erotic-contact or explicit-sex cues. I3 is rejected because there is no lexical evidence of affectionate physical contact. I6 is rejected because no genital/penetrative/oral cues appear. Consensus lands on I4: desire and longing with reflection on intimacy's meaning, without confirmed physical contact.
- **B contextual:** `I5`
  - The overwhelming majority of sentences reference 'sex' as a concept, topic of conversation, or relational significance — discussing whether sex occurred, what it meant, or whether it will happen. This is meta-discourse about sex rather than depiction of explicit acts, making I5 (sex as relational/emotional topic) the most specific and dominant code. BOOK_002_3 describes an actual sexual act with orgasm and is coded I6. BOOK_002_4 references coerced/forced sex and is coded I9. BOOK_004_1 references a man's interest/desire without contact, coded I4. No affectionate physical contact (kiss, hug, caress) is described in any sentence, so I3 is forbidden and i3_contact_evidence is false.
- **C adjudicate:** `I5`
  - Pass B lexical consensus was I4 (desire without contact), but contextual dominant I5 and the revealed taxonomy (2.5 Sexual Negotiation, Safety Preparation & Boundaries; secondary 3.3 Ambivalence & Internal Conflict) together indicate the cluster centers on negotiation, consent logistics, and internal conflict about proceeding — not mere desire expression and not affectionate physical contact. I3 is forbidden absent contact evidence (i3_contact_evidence: false). I8 (consent talk) is a close competitor, but the taxonomy explicitly frames this as negotiation plus safety preparation plus ambivalence, which maps more precisely to I5 (anticipatory/negotiation phase of sexual encounter) than to I8's narrower consent-communication focus. The secondary construct (ambivalence/internal conflict, 3.3) reinforces I5 over I4, since I4 captures unidirectional desire without the deliberative, boundary-aware quality present here. No collapse to I3 is warranted.
- **Action:** RETAXONOMIZE

---

## Topic 224 — Encouraging Words From An Angel

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> you’ve got this, angel, take it to the house.”

> i’ll come back, angel.

> because i’m thinking i’ll have a hard time finding another angel to handle it.”

> *(CELL_A, tertile=middle)* I most certainly do think the great evil knows about Gabriel."

> *(CELL_A, tertile=begin)* By the gods,” Val hissed as he and Gabriel came upon the creature. “

> *(CELL_B, tertile=begin)* Once, as I stood on the cliffs trying to understand the power I held, trying to comprehend why I would ever want to send my voice a thousand miles away on the wind, he’d told me that I looked like an angel blessed by the Almighty.

> *(CELL_B, tertile=middle)* I took a pleasant interlude of imagining myself nibbling on Evangeline’s ass.

> *(CELL_B, tertile=end)* With Evangeline beneath me I now knew what I’d felt wasn’t even close.

### Pass A/B/C

- **A lexical:** `I0`
  - Main keywords center on angelic/supernatural character types (angel, guardian, archangel, fallen) with no intimacy cues. KeyBERT yields interpersonal tension/assertion words (doubted, insisted, glared, behavior) suggesting conflict or negotiation, not physical contact. POS and MMR are dominated by abstract/structural terms (structure, task, ability, practice, behavior, tv) with no affectionate-contact signals. 'Precious' appears across lists but as a descriptor, not a contact cue. No kissing, hugging, caressing, or undressing cues anywhere. I3 is rejected per anti-collapse rules: zero affectionate physical contact evidence. The topic reads as worldbuilding or character-type discussion (angel mythology) with some interpersonal friction, best coded as general/non-intimate narrative content (I0).
- **B contextual:** `I7`
  - The overwhelming majority of sentences revolve around the word 'angel' used as a descriptor or metaphor (face of an angel, looks like an angel, blessed by the Almighty, evil/Lucifer angel lore), plus supernatural/conflict references to Gabriel, Val, and evil forces. These are best coded I7 (supernatural/religious/mythic framing) as the intimacy function is narrative world-building around angelic/demonic identity rather than any relational intimacy. Two sentences (BOOK_003_5 and BOOK_003_6) express desire/fantasy toward Evangeline without actual physical contact, coded I4. Two sentences (BOOK_004_2, BOOK_004_3) are purely logistical/social with no intimacy function, coded I0. No affectionate physical contact is present anywhere, so I3 is forbidden and i3_contact_evidence is false.
- **C adjudicate:** `I2`
  - Lexical consensus (I0) reflects surface domestic/logistical language, but contextual dominant (I7) and taxonomy metadata (4.6 Emotional Safety, Reassurance & Caretaking; secondary 9.2 Promise, Vow & Future-Tense Speech Acts) together indicate the functional core is verbal reassurance and caretaking rather than neutral domestic logistics. No affectionate physical contact is evidenced, so I3 is forbidden. The content does not rise to explicit vow/commitment ritual (I7 proper) but centers on emotional safety provision and forward-looking reassurance, which maps cleanly to I2. I0 is insufficient because the dominant function is affective caretaking, not mere domestic coordination. I7 is plausible as secondary but the primary intimacy function is reassurance/caretaking (I2), with promise-speech as a vehicle rather than the end in itself.
- **Action:** REINTERPRET

---

## Topic 227 — Cherishing Memories Before Parting

- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Code:** I0 (norm: I0)

> we’ll get your memory back.”

> you’ll be sure and let us know if you have any clearing of your memory, won’t you?” “

> i’ll be taking these memories with me and pulling them out when i’m missing everyone so much.

> *(CELL_C, tertile=end)* The memory of their first night under the stars surged through her, merging past with present sensation until she couldn't remember exactly where she was.

> *(CELL_C, tertile=middle)* Hearing him call her his wife brought memories of the weekend's activities back to vivid life. “

> *(CELL_C, tertile=end)* She remembered all too vividly coming back to whatever bedroom had been hers temporarily only to find her suitcases neatly packed.

> *(CELL_C, tertile=middle)* It may be something he doesn't want to share with anyone else in the world, especially his wonderful little girl whom he's just meeting again.

> *(CELL_D, tertile=end)* Because in about two seconds, he was going to forget about everything but getting off.

> *(CELL_B, tertile=end)* He remembered something that had been really bothering him. “

### Pass A/B/C

- **A lexical:** `I2`
  - All four keyword lists center on memory, forgetting, suffering, and emotional experience ('memories', 'remember', 'forgotten', 'wipe', 'suffering', 'precious', 'painful', 'bedside'). These cues point to emotional support, caretaking, and reassurance — consistent with I2 (emotional intimacy/vulnerability/comfort). 'Bedside' reinforces a caretaking/support context. There are no affectionate physical contact cues (no kiss, hug, hold, caress, or undressing), so I3 is rejected. No desire, gaze, or erotic language rules out I4/I10. No explicit sexual content rules out I6.
- **B contextual:** `I0`
  - All sentences in this topic cluster around the theme of memory, remembering, and recollection — characters thinking about the past, recalling events, or referencing memories. There is no affectionate physical contact, no desire expression, no erotic gaze, no consent talk, and no explicit sexual acts. Even BOOK_002_1 and BOOK_002_2, which reference past intimate experiences, are framed as memory/recollection rather than present physical contact or desire. BOOK_003_2 hints at arousal but describes a cognitive state ('forget about everything but getting off') without any physical contact or explicit act occurring in the sentence. The dominant function is narrative/domestic/backstory — I0 throughout.
- **C adjudicate:** `I0`
  - Pass B lexical consensus was I2 (reassurance/caretaking) and contextual dominant was I0 (domestic/logistics/HEA). The taxonomy metadata assigns primary code 2.5 (Sexual Negotiation, Safety Preparation & Boundaries) with secondary 4.2 (Ongoing Courtship & Everyday Relational Bonding). However, no affectionate physical contact evidence is present (i3_contact_evidence = false), ruling out I3 per anti-collapse rules. The secondary taxonomy axis (4.2) and the contextual dominant (I0) both point to domestic/relational bonding without erotic or physical escalation. The primary taxonomy label '2.5 Sexual Negotiation' could suggest I8, but without consent-negotiation or boundary-setting language in evidence, and given the contextual dominant is I0, the safest adjudicated code is I0. The topic should be retaxonomized away from 2.5 toward 4.2 as the primary construct, reflecting everyday relational bonding and HEA-oriented talk.
- **Action:** RETAXONOMIZE

---

## Topic 230 — Tongue and Hands After Climax

- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Code:** I4 (norm: I4)

> jacen palms the curve of liam’s ass as his tongue delves back into jacen’s mouth, into the same hot cavern that his hardened cock had ridden to an exquisite climax not so very long ago, darting in and out of it, moaning when jacen sucks on it, then pushes back for more of liam’s sweetness.

> [person] up into the contact, grabbing a handful of jacen’s hair and moaning loudly as jacen nips and sucks and marks him, leaving a dark bruise. “

> sawyer made a choice because of choices that i’ve made and he...it was too much for him.

> *(CELL_B, tertile=end)* That took all the defiance out of Serrano, who gazed wildly between Kyra and Reyes. "

> *(CELL_B, tertile=end)* Reyes seemed to come to some realization, and his expression held something like pity as he gazed at Serrano. "

> *(CELL_B, tertile=end)* Reyes wouldn't have been surprised if she'd gone for the bastard with her bare hands, but Apex was a thinker, not a fighter. "

> *(CELL_B, tertile=end)* Reyes thought he had some failsafe in place--if the guards didn't hear from Serrano at a certain time, they'd kill her and clean up the scene.

> *(CELL_A, tertile=end)* She switched her glare to her brother, and added, “Maybe he should have spent more time trying to emulate Roland’s noble qualities—like honor, generosity, and self-sacrifice—instead of murdering, thieving, and whoring his way to the sword’s hiding place!” “

> *(CELL_A, tertile=end)* For a moment, she thought it might be her, but Falcon hadn’t become that much like their father yet. “

> *(CELL_A, tertile=end)* All hint of brotherly affection evaporated from Falcon’s expression, leaving a cold, hard mask.

### Pass A/B/C

- **A lexical:** `I4`
  - Main keywords (binds, mate) suggest tension/bonding dynamics but no affectionate contact cues. KeyBERT offers 'moaning', 'flinched', 'nerves', 'sucked', 'dared' — 'moaning' and 'sucked' could hint at arousal/desire but without clear affectionate-contact framing; 'flinched' and 'nerves' suggest emotional tension rather than physical intimacy. POS keywords ('desperation', 'exquisite', 'internal') reinforce an internal desire/longing register. MMR keywords ('moaning', 'dared', 'testing', 'heaved', 'swirling', 'desperation') collectively point to heightened emotional/physical tension and desire without confirmed affectionate contact. The cluster reads as desire, tension, and emotional intensity — consistent with I4 (desire without confirmed contact). I3 is rejected because no clear kiss, hug, hold, caress, or undress-as-prelude cues are present across any representation.
- **B contextual:** `I0`
  - The overwhelming majority of sentences depict plot action, conflict, character movement, and dialogue with no affectionate physical contact. BOOK_003_4 ('Jasper pulled away, fire and caring in his eyes') implies a prior physical moment and shows emotional caring/caretaking in expression, coded I2. No sentence contains clear affectionate physical contact (kiss, hug, caress) sufficient for I3. No desire, gaze, or explicit sexual content is present. Dominant code is I0 (non-intimate narrative/logistics/conflict).
- **C adjudicate:** `I4`
  - Pass B lexical consensus is I4 (desire without contact) and contextual dominant is I0 (domestic/logistics/HEA). The taxonomy metadata flags 2.3 Explicit Sexual Acts with secondary 2.4 Aftercare & Post-Sex Reflection, but neither Pass B signal nor the anti-collapse rules support I6 or I3 here: no affectionate physical contact evidence is present (i3_contact_evidence=false), and no genital/penetrative act is described. The I0 contextual read likely reflects post-encounter domestic framing (consistent with 2.4 aftercare/reflection), while the I4 lexical signal captures residual desire or anticipatory longing in that same framing. Because the taxonomy points toward explicit-act territory yet the contact evidence is absent and Pass B did not confirm I6, the safest adjudication is I4 (desire without contact) with a retaxonomization away from 2.3. The I0 signal is subordinate and does not override the desire-laden lexical pattern. No collapse into I3 is warranted.
- **Action:** RETAXONOMIZE

---

## Topic 232 — Conversation Cut Short By Arrival

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** I2 (norm: I2)

> dex had come in and gabe's conversation with her, the longest conversation that they'd had in the couple of weeks he'd been back, was over.

> gabe leaned down so he wouldn’t be overheard. “

> i'll tell you right now falan and gabe are the only people on my team that i'd stake my career— or my balls —on."

> *(CELL_C, tertile=end)* Have Remy or the boys been out to question you again or give you more information about Joshua’s attack?”

> *(CELL_A, tertile=end)* He almost told her to call him Gabe, but he knew his name would sound way too good coming from her full lips.

> *(CELL_A, tertile=end)* Her name fit her, Gabe had found himself thinking one too many times.

> *(CELL_A, tertile=begin)* Gabe pretended to tackle Zach as he pulled the microphone from his hand, but he instantly sobered as he turned to Chase and Chloe. “

> *(CELL_A, tertile=end)* Her face got red then and she said angrily, "So, Gabe knew and didn't clue me in?

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords (gabe, nick, conversation, cringed, hand, elwoods) suggest an emotionally charged interpersonal exchange with reassurance/caretaking undertones rather than explicit physical contact. KeyBERT (impatiently, overheard, trembling, trailed, squeezed, groaned, distracted, problems) points to an anxious, tense conversation with emotional support dynamics — 'squeezed' could imply a hand-squeeze but is insufficient alone to confirm affectionate contact without corroborating cues. POS (longing, permission, instincts, awareness, possibilities) and MMR (longing, instincts, stroking, pained, gesture) introduce desire and longing cues that push toward I4, with 'stroking' being the closest contact cue but isolated and ambiguous. Overall, the dominant signal is an emotionally tense conversation with reassurance/caretaking (I2), with some unresolved desire (I4). I3 is rejected because no clear affectionate physical contact (kiss/hug/hold/caress) is confirmed across representations — 'squeezed' and 'stroking' are isolated and insufficient without corroboration. Consensus lands on I2 as the most supported function.
- **B contextual:** `I0`
  - This topic is dominated by references to a character named Gabe/Gabriel — questions directed at him, mentions of his name, social/interpersonal exchanges, and logistical/plot dialogue. Nearly all sentences are non-intimate social or narrative content (I0). The single exception is BOOK_003_4, where the narrator notes his name would 'sound way too good coming from her full lips,' which is a mild internal desire/attraction thought with no physical contact, coded I4. No affectionate physical contact appears anywhere in the set, so I3 is forbidden.
- **C adjudicate:** `I2`
  - Pass B produced a split between I2 (lexical consensus) and I0 (contextual dominant). The taxonomy tag — 4.2 Ongoing Courtship & Everyday Relational Bonding — tips the adjudication toward I2 rather than I0: courtship bonding implies active emotional investment and reassurance exchange, not merely domestic logistics or HEA planning. No affectionate physical contact evidence is present (i3_contact_evidence = false), so I3 is forbidden per anti-collapse rules. I0 would be appropriate only if the dominant signal were domestic/logistics/HEA talk without relational warmth; the taxonomy secondary codes are both None, confirming no erotic or explicit overlay. I2 best captures the reassurance and caretaking function that characterises ongoing courtship bonding at this non-physical register.
- **Action:** REINTERPRET

---

## Topic 240 — Unsure How to Offer Comfort

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> oh my god, sean!

> sean pursed his lips, unsure he was equal to the task of comforting [person].

> sean held out his hand and added; “now if you’ll excuse me i have a beautiful woman waiting to have breakfast with me.”

> *(CELL_B, tertile=begin)* Oh,” I said, thinking fast, watching as Seth started to show Liam how to use another nearby machine, while the Tiffanys and Brittanys gathered round, looking more worshipful than ever.

> *(CELL_B, tertile=end)* You need to stop nipping at him and face the fact that when Shon goes under, he’s off limits, one breath away from being a hostile at our backs.” “

### Pass A/B/C

- **A lexical:** `I2`
  - Cues across all representations point to tense, emotionally charged interpersonal exchange: 'anxious', 'winced', 'shivered', 'mumbled', 'solemnly', 'absently', 'distracted', 'unsure', 'conscious', 'stares'. 'Patted' is the only possible physical-contact word but is a minor reassurance gesture, not affectionate/romantic contact. The character names (sean, jaime, bryan, yseult, morrissey) and 'repressive', 'brogue' suggest a socially or emotionally constrained scene. Overall pattern fits I2 (emotional support/reassurance/caretaking dialogue). I3 rejected: no kissing, hugging, caressing, or undressing cues present; 'patted' alone does not constitute affectionate romantic contact under anti-collapse rules.
- **B contextual:** `I1`
  - All sentences consist of dialogue fragments, character name calls, brief conversational exchanges, and minimal action descriptions (e.g., 'peered around', 'shared a look'). There is no affectionate physical contact, no desire expression, no emotional vulnerability, no domestic/HEA content, and no erotic or sexual content. The topic appears to be a character-name cluster (Liam, Shon, Sean, Conner) with purely interactional/conversational function, coded I1 (social/verbal interaction without intimacy function).
- **C adjudicate:** `I2`
  - Lexical consensus (I2) and taxonomy metadata (4.6 Emotional Safety, Reassurance & Caretaking) align. The contextual dominant I1 (ongoing courtship/bonding) is consistent as a secondary function per 4.2, but the primary signal is reassurance and caretaking without evidence of affectionate physical contact. Anti-collapse rules prohibit elevation to I3 absent contact evidence. I2 is the most specific defensible code. No domestic/logistics/HEA framing that would push to I0, and no desire-without-contact or erotic gaze to warrant I4/I10.
- **Action:** REINTERPRET

---

## Topic 245 — Lip Biting and Nervous Pout

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I4 (norm: I4)

> she bit her lip as she cleaned more sensitive areas, areas her own lover had been hesitant to touch.

> she pushed her lower lip out in an exaggerated pout. “

> come on morgan, that’s hardly fair,” she protested, her lip falling into a pout.

> *(CELL_C, tertile=end)* Katie nibbled her upper lip, crossed and uncrossed her long arms.

### Pass A/B/C

- **A lexical:** `I4`
  - Main/KeyBERT/MMR cluster around self-directed nervous/anxious oral behaviour (lip-biting, chewing, trembling, panting, tugging) — these are signs of internal emotional tension, desire, or anticipation rather than affectionate contact with another person. 'Tasted' in KeyBERT is ambiguous but paired with 'absently' and 'ducked' suggests self-conscious nervous action, not a kiss. POS leans toward I2 (distress, desperation, uncertainty, stool suggesting a scene of caretaking or emotional support), but the dominant signal across three reps is nervous/anticipatory arousal without confirmed physical contact. I3 is rejected because no cue in any rep denotes affectionate physical contact between characters (no kiss, hug, hold, caress, or undressing). The self-biting/lip behaviour is self-directed nervous gesture. Consensus is I4 (desire/longing/anticipation without confirmed contact), acknowledging the POS distress signal as a secondary thread.
- **B contextual:** `I2`
  - All sentences depict self-directed nervous or anxious physical gestures — biting/nibbling/moistening one's own lip, chattering teeth, wincing, crossing arms — that signal emotional tension, vulnerability, or anxiety. These are classic non-contact emotional/somatic cues associated with I2 (emotional caretaking/reassurance context, internal emotional state display). BOOK_002_2 references a prior kiss but the sentence itself only shows the character absently touching her own lip in reflection — no affectionate contact with another person occurs in any sentence, so I3 is forbidden. No desire directed at another (I4), no gaze (I10), no explicit content (I6). I2 is the most specific applicable code for self-soothing/anxiety-display gestures throughout.
- **C adjudicate:** `I4`
  - Pass B produced a split between I4 (lexical consensus) and I2 (contextual dominant). Adjudication favors I4. The taxonomy anchor is 2.1 Attraction & Sexual Tension with a secondary of 1.7 Facial Expression & Non-Sexual Nonverbal Cues — both point to desire/longing communicated through gaze, expression, and body language rather than affectionate physical contact or caretaking. I2 (reassurance/caretaking) is not supported by the taxonomy metadata; any warmth in the cluster is better explained as the emotional valence of unresolved attraction rather than a distinct care function. No affectionate contact evidence is present (i3_contact_evidence: false), so I3 is forbidden per anti-collapse rules. The correct code is I4: desire/longing without physical contact, consistent with both the lexical signal and the taxonomy.
- **Action:** REINTERPRET

---

## Topic 247 — Promising You Will Not Be Alone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I0 (norm: I0)

> if we make it through this alone, we’ll just be better at being alone.”

> you’ll never be alone.

> before you say no, i want you to know i’ll be alone mostly.

> *(CELL_B, tertile=end)* If I went out alone, it seemed I felt surrounded by people who couldn’t speak to me.

> *(CELL_B, tertile=begin)* I promise you, you will never be alone again so long as I live.”

> *(CELL_B, tertile=begin)* I’ve pictured this so many times in my mind, I don’t want to wake up and find I’m alone again.” “

### Pass A/B/C

- **A lexical:** `I0`
  - Main keywords (alone, solitude, want, prefer, rather, live) suggest emotional withdrawal or a character expressing a preference about living situation/circumstances — no affectionate contact cues. KeyBERT (upset, praying) hints at emotional distress and supplication, leaning toward I2 (reassurance/caretaking context), but no physical contact. POS and MMR keywords (options, terms, circumstances, attempt, fault, planned, insisted, chose, preferred) are strongly logistical and negotiation-oriented, pointing to I0 (domestic/logistics/HEA talk or situational decision-making). No erotic, desire, or physical-contact cues anywhere. I3 is rejected: zero affectionate-contact evidence across all representations. Consensus lands on I0 given the dominant weight of circumstance/decision/logistics vocabulary in POS and MMR, with the emotional distress in Main/KeyBERT consistent with a difficult domestic or relational negotiation rather than caretaking intimacy.
- **B contextual:** `I0`
  - This topic clusters around the word 'alone' and related themes of solitude, loneliness, and the desire for companionship. The vast majority of sentences (15/20) are straightforwardly about being alone or isolated — logistical/emotional state descriptions with no intimacy function beyond noting presence or absence, coded I0. A minority (5/20) express emotional reassurance or caretaking — promises not to leave someone alone, concern about a partner being by themselves, longing for togetherness — coded I2. No sentence contains affectionate physical contact, so I3 is forbidden. No desire, gaze, or erotic content is present. I0 dominates at 75%, well above the 70% threshold.
- **C adjudicate:** `I0`
  - All three passes converge on I0. The taxonomy metadata confirms the dominant function is Emotional Safety, Reassurance & Caretaking (4.6) with a secondary of Promise/Vow/Future-Tense Speech Acts (9.2). Neither category implies affectionate physical contact; reassurance and caretaking without touch map to I2 only when somatic comfort is the primary vehicle, but here the lexical and contextual evidence points to verbal/relational safety-building and forward-looking commitments — squarely I0. No kiss, hug, hold, caress, or undress-as-prelude is evidenced, so I3 is forbidden. I2 is not warranted because the dominant signal is promise/vow speech acts rather than somatic caretaking. I0 is retained.
- **Action:** KEEP

---

## Topic 273 — Mentor Gives Firm Instructions

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

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

- **A lexical:** `I2`
  - All four keyword lists converge on emotional/relational communication: 'insensitivity', 'apology', 'upset', 'awareness', 'treatment', 'choices', 'explanation' point to a scene of emotional reckoning, reassurance, or caretaking dialogue between characters (charlotte, amelia, lady). 'Engaged' and 'speaking' reinforce verbal/social interaction. No affectionate physical contact cues (kiss, hug, hold, caress, undress) are present anywhere, so I3 is rejected. No desire/gaze cues (I4/I10), no explicit content (I6), no coercion (I9), no consent negotiation (I8). The dominant function is emotional repair/reassurance (I2).
- **B contextual:** `I0`
  - All sentences in this topic involve social/relational logistics, character references, and interpersonal dialogue about third parties (Felicia, Nikki, Kiara, Gabby, Claire, Celia, Brenda). There is no affectionate physical contact, no desire expression, no erotic content, no consent negotiation, and no coercion. The topic is entirely social/domestic interaction and character-relationship management, coded I0 throughout.
- **C adjudicate:** `I2`
  - Pass B produced a split between I2 (lexical consensus) and I0 (contextual dominant). Taxonomy metadata confirms primary placement at 4.6 Emotional Safety, Reassurance & Caretaking with a secondary signal at 5.2 Friends, Allies & Social Circles. There is no evidence of affectionate physical contact (no kissing, hugging, holding, caressing, or undressing-as-prelude), so I3 is forbidden per anti-collapse rules. The I0 contextual read likely reflects domestic or logistical framing that co-occurs with the caretaking language, but the primary taxonomy anchor is emotional reassurance rather than HEA/domestic logistics. I2 is therefore the more specific and accurate code. The secondary social-circle signal does not override the primary caretaking function. No manual review required given clear taxonomy guidance.
- **Action:** REINTERPRET

---

## Topic 277 — Promising to Handle The Lawyer

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I0 (norm: I0)

> i’ll talk to the lawyer tomorrow.

> we’ll find a good lawyer to help.

> you can count on me to deal with the legal trouble they’ll cause.”

> *(CELL_D, tertile=end)* Mediation has never come easily for me and I need all the help I can get.

> *(CELL_B, tertile=end)* Such a lot of fuss over a piece of real estate that was destined by federal law to go unclaimed by anyone.

> *(CELL_B, tertile=end)* It’s important to establish legal boundaries of ownership, especially when you’re talking about gems and precious metals.

### Pass A/B/C

- **A lexical:** `I0`
  - All keyword lists point to legal/professional context: 'lawyer, attorney, law, legal, firm, defense, counsel, appointed, advice' (Main) establish a courtroom or legal-proceedings setting. KeyBERT adds emotional-logistical cues ('afford, cost, worrying, begging, warned') consistent with stress over legal matters, not intimacy. POS and MMR reinforce procedural/logistical framing ('process, official, cost, experience, worrying'). No affectionate physical contact cues anywhere — I3 is rejected. No desire, gaze, consent, coercion, or explicit content — I4/I6/I8/I9/I10 are all rejected. This is domestic/logistical/situational talk coded I0.
- **B contextual:** `I0`
  - All sentences in this topic revolve around legal/professional roles (lawyers, lawmen, legal boundaries, divorce cases, property law) and practical/logistical discourse. There is no affectionate physical contact, no desire, no emotional intimacy, no erotic content, and no relational negotiation. Every sentence codes as I0 (non-intimate functional/logistical content). The topic is clearly a legal/professional-role cluster.
- **C adjudicate:** `I0`
  - All three passes converge on I0. The taxonomy metadata confirms the dominant function is Emotional Safety, Reassurance & Caretaking (4.6) with a secondary of Promise/Vow/Future-Tense Speech Acts (9.2). Neither category implies affectionate physical contact; reassurance and caretaking language without touch maps to I2 at most, but the lexical and contextual consensus is I0 (domestic/logistics/HEA talk). No evidence of kissing, hugging, holding, caressing, or undressing-as-prelude, so I3 is forbidden. The topic is correctly classified as I0 and should be kept as-is.
- **Action:** KEEP

---

## Topic 289 — Quick Peck on The Forehead

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> mikey, i’ll be back soon, i promise,” nate said, placing a quick peck on his forehead. “

> nate arched an eyebrow, gesturing back toward the parking lot. “

> nate looked at the older asian man gesturing wildly to them, then at the array of paints.

> *(CELL_B, tertile=begin)* Dominic frowned, knowing that to demur a second time would definitely incur Nate’s curiosity. ‘

### Pass A/B/C

- **A lexical:** `I4`
  - No affectionate physical contact cues appear in any keyword list. Main keywords include 'shame' and 'mate' suggesting charged interpersonal tension but no touch. KeyBERT cues ('glint', 'darkened', 'trembled', 'trailed', 'peered', 'focused') point to heightened sensory awareness and erotic/tense gaze rather than contact. POS keywords ('instincts', 'anxiety', 'moves', 'reminder') reinforce internal tension and anticipation. MMR adds 'breathlessly', 'trembled', 'poised', 'crept' — all suggestive of desire and anticipation without consummated contact. The cluster best fits I4 (desire/longing without physical contact). I3 is rejected because no kiss, hug, hold, caress, or undressing cue is present across any representation.
- **B contextual:** `I0`
  - All sentences in this topic consist of dialogue tags, character name references, brief exclamations, and conversational exchanges involving a character named Nate. There is no affectionate physical contact, no desire, no erotic content, no consent negotiation, and no domestic/HEA planning. The content is purely conversational/narrative scaffolding with no intimacy function, making I0 (non-intimate interaction / narrative logistics) the most specific and appropriate code for every sentence.
- **C adjudicate:** `I2`
  - Pass B produced a split between I4 (lexical consensus) and I0 (contextual dominant). Taxonomy metadata resolves this: the primary tag is 4.6 Emotional Safety, Reassurance & Caretaking, which maps directly to I2. I4 (desire without contact) is not supported by the caretaking/reassurance taxonomy frame, and I0 (domestic/logistics/HEA) is too narrow given the explicit emotional-safety primary tag. No affectionate physical contact is evidenced, so I3 is forbidden. I2 is the most specific code consistent with both the taxonomy and the anti-collapse rules: reassurance and caretaking without physical contact = I2. The secondary tag (5.1 Family, Kinship & Parenthood) is consistent with I2 in a familial or partnership caretaking register and does not push toward any other code.
- **Action:** REINTERPRET

---

## Topic 299 — Pledging to Have Your Back

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> before she’s completely out i ask, “[person], you know i’ve always got your back, right?”

> but i’ve seen you, seen who you are, watched you handle uncle charlie.

> i’ve got a little time before charlie finishes my bike.

> *(CELL_A, tertile=middle)* Kevin was worried that Scott’s death was somehow related to Todd’s return to Birmingham.’

> *(CELL_A, tertile=begin)* They all left for college with big dreams, except Scott and Kevin,’ she said sadly. ‘

### Pass A/B/C

- **A lexical:** `I2`
  - Keywords across all representations point to interpersonal negotiation, reassurance, and emotional management: 'promises', 'threats', 'forgive', 'terms', 'discussing', 'distraction', 'embarrassing', 'solemnly', 'instructed'. Named characters (dane, eoin, dan, alicia) suggest a relational scene involving emotional stakes and verbal exchanges. 'Promises' and 'forgive' indicate reassurance/caretaking dynamics (I2). 'Threats' and 'terms' suggest conflict negotiation rather than coercion in a sexual context (no I9 cues). No affectionate physical contact cues (kiss, hug, caress, undress) are present anywhere, so I3 is rejected. No desire/gaze cues for I4/I10. No explicit sexual content for I6. I2 best captures the reassurance, emotional management, and interpersonal negotiation tone.
- **B contextual:** `I0`
  - The topic centers on characters named Charlie, Scott, Pete, and Kevin in narrative/dialogue contexts. The vast majority of sentences involve information exchange, plot logistics, or character references (I0). A subset involves emotional concern, reassurance, or caretaking (e.g., 'Was Charlie all right?', 'Charlie will come home to you', 'Charlie, shh', 'What can I do, Charlie?', 'Afterwards, Charlie cried') coded I2. No sentence contains affectionate physical contact, so I3 is forbidden. No desire, gaze, consent, coercion, or explicit sexual content is present.
- **C adjudicate:** `I2`
  - Pass B produced a split between I2 (lexical consensus) and I0 (contextual dominant). Taxonomy metadata confirms the primary construct is 4.6 Emotional Safety, Reassurance & Caretaking with a secondary of 5.2 Friends, Allies & Social Circles. There is no evidence of affectionate physical contact (no kiss, hug, hold, caress, or undress-as-prelude), so I3 is forbidden. The I0 signal likely reflects domestic/logistical framing within a caretaking exchange, but the dominant intimacy function is emotional reassurance rather than pure domestic logistics or HEA planning. I2 is therefore the correct resolution: it is more specific than I0 for content whose primary function is comfort-giving and emotional safety, and it does not require physical contact. No manual review needed.
- **Action:** REINTERPRET

---

## Topic 305 — Confessing A Lifelong Regret

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** I2 (norm: I2)

> i know that now, and i’ll go to my grave regretting what i did to you.” “

> come on in, you’ll no doubt regret it.

> you’ll regret that.’ ‘

> *(CELL_B, tertile=middle)* You are surely not intending to imply that you are beginning to regret this marriage already?’ ‘

> *(CELL_B, tertile=end)* I fear that my careless remarks must have been the cause of that outburst.

### Pass A/B/C

- **A lexical:** `I2`
  - All four keyword lists center on regret, emotional distress, and interpersonal tension: 'regret/regretted/regrets', 'fears', 'upset', 'embarrassing', 'admit', 'fumbled', 'handled', 'assure'. These cues point to emotional vulnerability, reassurance-seeking, and caretaking dynamics (I2). There is no affectionate physical contact vocabulary (no kiss, hug, hold, caress, or undress), so I3 is rejected. No desire/gaze cues (I4/I10), no explicit content (I6), no coercion (I9), no consent negotiation (I8). The 'promise' and 'decision' terms suggest relational accountability talk, consistent with I2 emotional repair rather than I0 domestic logistics.
- **B contextual:** `I2`
  - All sentences revolve around the emotional theme of regret — expressing, denying, or processing regret within relational contexts (marriage, unkindness, past actions). This is emotional reassurance/caretaking territory (I2): characters are processing emotional vulnerability, guilt, and relational repair without any physical contact, desire, or explicit acts. No affectionate physical contact is present (I3 forbidden), no erotic gaze, no explicit sex, no coercion, and no domestic/logistics/HEA framing. I2 is the most specific applicable code across all sentences.
- **C adjudicate:** `I2`
  - Lexical and contextual consensus both point to I2 (reassurance/caretaking). The taxonomy placement under 4.5 Reconciliation & Commitments with secondary 3.2 Negative Emotions & Distress is consistent with emotional repair and vulnerability exchange rather than affectionate physical contact. No evidence of kissing, hugging, holding, caressing, or undressing-as-prelude is present, so I3 is forbidden per anti-collapse rules. The content does not rise to domestic/logistics/HEA talk (I0), desire without contact (I4), erotic gaze (I10), consent negotiation (I8), or explicit sex (I6). I2 is the most specific and best-supported code.
- **Action:** KEEP

---

## Topic 307 — Hauling Someone Up The Stairs

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> [person] would hate it if she took a rake like [person] to her bed, and she would so love to rub it in joshua’s face and prove his threats could not restrain her. “

> his thoughts threatened to return to those awful times once again, but thankfully, ash and [person] emerged from the thicket.

> getting ash up the stairs and into the bedroom was a lot harder than it had been last night, mostly because ash was pissed off and conscious instead of in la-la land.

> *(CELL_B, tertile=end)* You and Ashlynn are gonna have to keep him on the straight and narrow."

> *(CELL_B, tertile=end)* He stopped to pat Ashlynn and congratulate her on a large belch. "

> *(CELL_B, tertile=end)* But as he was approaching Clarksburg, Ashlynn chose that moment to be cranky.

> *(CELL_B, tertile=end)* Henry's crankiness had returned, and even sweet Ashlynn was wailing by now.

> *(CELL_B, tertile=end)* Sniffing in disdain, Johnny pushed Ashlynn's stroler over to Grissom. "

### Pass A/B/C

- **A lexical:** `I8`
  - Main keywords are character names and place names with no intimacy signal, defaulting to I0. KeyBERT shows physical strain cues ('heaved', 'winced', 'struggled', 'fought', 'urge') suggesting suppressed desire or tension, pointing to I4. POS and MMR both surface 'threats', 'permission', 'anxiety', 'panting', 'movements', 'urged' — the combination of 'threats', 'permission', and 'anxiety' strongly signals consent negotiation or coercive-pressure dynamics, coding to I8. No affectionate physical contact cues (kiss, hug, hold, caress, undress) appear in any keyword list, so I3 is rejected. Consensus lands on I8 driven by the dominant consent/threat/permission cluster across POS and MMR, with acknowledgment of tension/desire undertones from KeyBERT.
- **B contextual:** `I0`
  - This topic clusters around the name/word 'Ash' — either as a character name (Ash, Ashlynn) or as literal ash/burning imagery. The BOOK_002 sentences involve infant caregiving logistics (changing a baby, stroller, crankiness) with no romantic or intimate function. BOOK_005 sentences are brief dialogue/action fragments referencing a character named Ash with no intimacy. BOOK_006 sentences use 'ash' in a supernatural/destruction context. BOOK_007 sentences are bare name utterances. No affectionate physical contact, desire, or any intimacy function is present. All sentences code I0 (domestic/logistical/non-intimate narrative).
- **C adjudicate:** `I2`
  - Pass B lexical consensus was I8 (consent talk) and contextual dominant was I0 (domestic/logistics). Taxonomy metadata reveals the primary construct is 4.6 Emotional Safety, Reassurance & Caretaking with a secondary of 8.1 Domestic Spaces & Routines. Neither consent negotiation nor pure domestic logistics is the dominant signal here — the taxonomy points to reassurance and caretaking as the core intimacy function. I2 (reassurance/caretaking) is the most specific applicable code: there is no affectionate physical contact evidenced (I3 is forbidden), no explicit desire (I4), no erotic gaze (I10), no coercion (I9), and no explicit sex (I6). The domestic secondary construct is consistent with I2 scenes set in home spaces rather than warranting I0. The Pass B I0 reading is overridden by the taxonomy's primary construct of emotional caretaking, which is definitionally I2.
- **Action:** REINTERPRET

---

## Topic 337 — Adjusting to His Presence Inside Her

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I4 (norm: I4)

> he might be miles away, but the sensation of him flooded through her with a comforting force.

> he held, waited, giving her time to stretch, adjust, somehow become accustomed to a man who filled so much of her life and body, more than she’d expected on any level.

> she wasn’t yet accustomed to the drum roll his touch elicited from her body. “

> *(CELL_B, tertile=end)* But he wanted to touch her, to assure himself she was still his.

> *(CELL_B, tertile=middle)* Instead, she discovered that the touch of this man’s skin against hers aroused in her overwhelming tenderness and frantic passion.

> *(CELL_B, tertile=middle)* He didn’t know if he could bear to have her touch him, because the mere thought of her made his blood heat as well as other, less biddable parts.

> *(CELL_B, tertile=middle)* She swayed with the onset of passion and wondered how this man had so quickly accustomed her to his touch.

> *(CELL_D, tertile=begin)* He was laying it on thick—flirting shamelessly with the Miss Tenningtons, who tittered around coquettishly, loving every minute of it and vying against each other in the way only identical twins probably can for his attention.

> *(CELL_B, tertile=end)* It was the hunger for him – for his touch and what it triggered in her – that had entranced her.

> *(CELL_B, tertile=middle)* It seemed like he never could, not once he touched her, felt her respond to him.

### Pass A/B/C

- **A lexical:** `I6`
  - All four representations converge on explicit/erotic sexual activity. Main: 'touch/touching/craved/desire/inside/body' with 'inside' pointing to penetrative context. KeyBERT: 'stroking, pounding, passionate, exquisite, flooded' — 'pounding' is a strong explicit-sex cue, 'stroking' in combination with 'pounding' and 'flooded' indicates genital/penetrative activity rather than mere caress. POS: 'insides, damp, veins, exquisite, exciting' — 'insides' and 'damp' are bodily-arousal/penetrative cues. MMR: 'pounding, stroking, flooded, passionate, veins' reinforce explicit sexual activity. I3 is rejected because while 'stroking' alone could be non-genital caress, the cluster of 'pounding + insides + damp + flooded + inside' collectively signals penetrative/genital activity, placing this firmly in I6 rather than I3. I4 is rejected because there is physical contact described, not merely desire without contact.
- **B contextual:** `I4`
  - The majority of sentences express desire for touch, anticipation of contact, or longing without depicting actual contact in that sentence — coded I4. Several sentences describe actual affectionate/non-genital physical contact (guiding into embrace, hand-holding, fingers awakening need in a non-explicitly-genital framing) — coded I3. Four sentences describe explicit genital/penetrative acts (cock rubbing inside her, finger into folds, contracting around him) — coded I6. One sentence is pure caretaking/comfort — I2. One sentence is neutral/off-topic — I0. I4 is dominant at ~45%, above the 70% threshold.
- **C adjudicate:** `I4`
  - Pass B contextual dominant (I4) overrides lexical consensus (I6). The taxonomy places this in 2.1 Attraction & Sexual Tension with only secondary 2.3 signal, indicating desire and anticipation rather than enacted explicit acts. No affectionate physical contact evidence is present (i3_contact_evidence=false), so I3 is forbidden per anti-collapse rules. I6 would require confirmed genital/oral/penetrative content as the dominant function; here the dominant function is unresolved desire and tension. I4 is the most specific defensible code given the evidence.
- **Action:** REINTERPRET

---

## Topic 340 — Patience Tested Through Small Trials

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> for two years he had observed the christmas elf, but he never imagined touching her.

> from the moment that she started working at her current job, she had never clicked with frank.

> her patience throughout the meal with the girls never wavered, not with spilled drinks, sloppy faces and an occasional cry for attention.

> *(CELL_A, tertile=middle)* Up until now, she'd never met anyone who made her ache for the things that were denied her.

> *(CELL_A, tertile=begin)* She'd never known anything like the power and hunger of his kiss.

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords ('violent', 'regime', 'standards', 'contact', 'never') suggest a coercive or controlling relational dynamic, pointing toward I9. However, KeyBERT ('emotionally', 'disappointed', 'feared', 'unhappy', 'cared'), POS ('emotionally', 'unhappy', 'upset'), and MMR ('emotionally', 'feared', 'cared', 'witnessed') collectively emphasize emotional distress, caretaking concern, and relational unhappiness rather than active coercion or explicit threat. The dominant signal across three of four representations is emotional support/reassurance/caretaking in a difficult relational context, consistent with I2. 'Violent' in Main is noted but not corroborated by the other reps with enough specificity to override to I9. I3 is rejected: no affectionate physical contact cues (kiss, hug, caress, hold) appear in any representation.
- **B contextual:** `MIXED`
  - The topic clusters around negated or counterfactual statements about romantic/emotional experience ('never kissed', 'never in love', 'never felt desire', 'never kept anything from her'). No single code reaches 70%. I4 (desire/longing without contact) and I0 (neutral/relational statements) each account for roughly 30% of sentences. One sentence (BOOK_002_5) references the power of a kiss, qualifying for I3 as it describes affectionate physical contact. Two sentences (BOOK_003_4, BOOK_003_5) suggest coercive confinement (I9). The remainder split across I2 (reassurance/caretaking) and I0 (neutral). Because no single code reaches 70%, the dominant code is MIXED.
- **C adjudicate:** `I2`
  - Lexical consensus and taxonomy both converge on I2 (Emotional Safety, Reassurance & Caretaking). The contextual dominant is MIXED but the secondary taxonomy signal (Family, Kinship & Parenthood) is consistent with I2 caretaking rather than requiring a split. No affectionate physical contact evidence is present, so I3 is forbidden per anti-collapse rules. Domestic/logistics content is insufficient to downgrade to I0. The topic is best retained as I2 with constructs spanning emotional reassurance and kinship-based caretaking.
- **Action:** KEEP

---

## Topic 345 — Older Man Trading Shelter For Sex

- **Taxonomy:** 7.4 — Unwanted or Coercive Sexual Contact
- **Code:** I9 (norm: I9)

> [person] says and then adds, “right.

> mom didn’t talk to me about it, but i’m pretty sure uncle tony would’ve rather handled it a different way, if you know what i mean.” “

> [person] knew that nothing was something, but he had no claims on the boy; in fact, after hearing about jorge’s initiation into sex, it occurred to him that he might be just another older man trading off offers of shelter or a meal or booze in exchange for being fucked senseless.

> *(CELL_B, tertile=end)* Instead of a malfeasant, it was Steve with a loaded pizza and a six-pack of beer—my dream man.

> *(CELL_B, tertile=begin)* Steve’s job was to close Stan McClousky’s operation and get his drugs off the street.

> *(CELL_B, tertile=middle)* If Sinestro had been a member of the Soprano Mafia family, he would have been whacked a long time ago.

> *(CELL_B, tertile=begin)* Although I still want to know how Tony Stark fits those in-line roller skates inside his Iron Man boots, especially when the armor’s folded up and tucked away in his briefcase, which when you think about it is the source of yet another paradox, because even if you assume some ability to condense the volume of the armor into such a containment, how do you deal with the integral mass?

> *(CELL_B, tertile=middle)* He contacted the rulers of the antimatter universe, the Weaponers of Qward, and made a deal to help them in their attempt to conquer the matter universe.

> *(CELL_B, tertile=end)* The Villain in the Iron Mask: Dr. Doom Fantastic Four Comics #1–100 (and other issues).

### Pass A/B/C

- **A lexical:** `I0`
  - All four keyword lists point to a scene of information exchange, social interaction, and domestic/logistical context: 'informant', 'confidential', 'follow', 'asking', 'revealing', 'answering', 'claims', 'contrast', 'exchange', 'meal', 'porch', 'stool', 'decision'. Behavioral cues ('flinched', 'winked', 'grumbled', 'straightened', 'pounded') suggest interpersonal tension or negotiation, not affectionate contact. No kissing, hugging, caressing, or undressing cues are present. I3 is rejected because there is zero affectionate-contact evidence. The scene reads as a conversation/information-gathering interaction (possibly involving a named character 'ilsa' and an 'uncle' or 'informant'), coded I0 (domestic/social/logistical interaction).
- **B contextual:** `I0`
  - All sentences across the three books are non-intimate in function. BOOK_004 sentences reference a character named Steve in casual/logistical/comedic contexts (pizza delivery, law-enforcement job). BOOK_006 sentences are comic-book lore discussions (Dr. Doom, Iron Man, Sinestro, Avengers). BOOK_007 sentences involve interpersonal tension and surveillance around a character named Malcolm and a threat figure named Peter — no affection or intimacy. BOOK_008 sentences are simple name-calls ('Tony?') with no contextual intimacy signal. No affectionate physical contact, desire, or erotic content is present anywhere; I0 (domestic/logistical/non-intimate narrative) is the most specific applicable code throughout.
- **C adjudicate:** `I9`
  - Pass B lexical and contextual consensus landed on I0, but the revealed taxonomy (7.4 Unwanted or Coercive Sexual Contact, secondary 6.4 Economic Precarity/Dependency) overrides that reading. The topic's functional core is coercion or unwanted sexual contact enabled by economic dependency — not domestic/HEA content. No affectionate physical contact evidence exists (I3 is forbidden). The correct intimacy code is I9 (coercion/non-consensual contact), with the economic precarity secondary construct explaining the power asymmetry that enables the coercion. Manual review is flagged because the Pass B I0 signal suggests surface-level lexical ambiguity that a human coder should resolve against the full topic word list.
- **Action:** RETAXONOMIZE

---

## Topic 351 — Warm Greeting Upon Return

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** I0 (norm: I0)

> thank god you’ve come back—and will you look at me, just in time.”

> it is a pleasure to see you again—so soon, madam. ”

> so i’ll see you there,” he said, feeling upbeat for the first time in a long time. “

> *(CELL_D, tertile=begin)* I’ll see you as often as I can,” he said, only making matters worse by reminding the children he wouldn’t be seeing them on a normal basis. “

> *(CELL_D, tertile=middle)* Amber had seen it as a splendid way to say goodbye to the hoards of tourists who crowded Harmony during that season.

### Pass A/B/C

- **A lexical:** `I1`
  - All keyword sets point to a social greeting/pleasantry exchange: Main has 'see, nice, good, glad, again, pleasure, happy, great' — polite social expressions; KeyBERT has 'greeted, mister, madam, replies, warmth, reminds, reaches' — formal address and greeting acts; POS has 'lack, warmth, crowd' — social setting with emotional warmth but no physical contact; MMR reinforces with 'madam, greeted, replies, crowd, ms' — formal social encounter. The 'warmth' here is social/emotional, not physical. 'Reaches' is ambiguous but insufficient alone to establish affectionate contact. No kissing, hugging, caressing, or undressing cues are present. I3 is rejected: no affectionate physical contact evidence. This is a polite social greeting scene coded I1 (social/verbal bonding).
- **B contextual:** `I0`
  - All sentences in this topic revolve around the social/logistical act of seeing or meeting someone — greetings, farewells, and expressions of pleasure at encountering another person. There is no affectionate physical contact, no desire, no erotic content, no emotional vulnerability or reassurance beyond polite social exchange. The topic is purely social/domestic interaction (greetings and partings), coded I0 throughout.
- **C adjudicate:** `I0`
  - Pass B contextual dominant is I0 and taxonomy confirms 4.2 Ongoing Courtship & Everyday Relational Bonding — a category centered on relational maintenance, domestic interaction, and HEA-adjacent talk without requiring affectionate physical contact. Lexical consensus I1 (introductory/greeting language) is consistent with low-intimacy relational bonding rather than any contact-bearing code. No evidence of affectionate physical contact (kiss, hug, hold, caress, or undress-as-prelude) is present, so I3 is forbidden per anti-collapse rules. The taxonomy secondary codes are null, reinforcing a single-domain I0 classification. Keeping I0 is the correct adjudication.
- **Action:** REINTERPRET

---

## Topic 352 — Daring Someone to Try

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I2 (norm: I2)

> you’ll never know unless you give it a try.”

> i’ll try anything once.”

> i’ll do more than try.

> *(CELL_C, tertile=end)* Others have tried and they’ve all failed.

> *(CELL_B, tertile=end)* And I promise I’m going to try.”

> *(CELL_C, tertile=middle)* A new one we’re trying out.

### Pass A/B/C

- **A lexical:** `I2`
  - Keywords 'try/trying/tried/give/want/willing/promising/honestly/uh' collectively signal negotiation, reassurance, or emotional effort — someone attempting to meet another's needs or express willingness. 'Preziosa' (Italian term of endearment) adds an affective/caretaking tone. No lexical cues for physical contact (kiss, hug, hold, caress, undress), explicit desire, or erotic content are present, so I3, I4, and I6 are all rejected. The dominant function is emotional reassurance/caretaking (I2).
- **B contextual:** `I0`
  - All sentences in this topic cluster around the word 'try' used in conversational, motivational, or challenge contexts. There is no affectionate physical contact, no desire expression, no erotic content, no consent negotiation, and no domestic/HEA framing. The sentences are generic dialogue fragments with no intimacy function. I0 (non-intimate/functional dialogue) is the most specific applicable code across all sentences.
- **C adjudicate:** `I2`
  - Pass B produced a split between I2 (lexical consensus) and I0 (contextual dominant). The taxonomy metadata places this under Attraction & Sexual Tension (2.1) with no secondary codes, which does not support I0 (domestic/logistics/HEA). The lexical signal of I2 — reassurance and caretaking language — is more consistent with the 2.1 taxonomy than pure domestic logistics. No affectionate physical contact evidence is present, so I3 is forbidden. I4/I10 are not supported without desire or gaze language. I2 is the most specific defensible code: emotional support and relational caretaking that serves attraction/tension scaffolding without crossing into physical contact. I0 is demoted because the taxonomy explicitly flags relational/attraction function rather than domestic logistics.
- **Action:** REINTERPRET

---

## Topic 355 — Blanket Draped Over Someone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

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

### Pass A/B/C

- **A lexical:** `I2`
  - All four keyword lists center on bedding/covering vocabulary (blanket, blankets, tucked, comforter, wrapped, draped, sheet, curled, folded) combined with emotional cues (terrified, embarrassed) and task-oriented movement words (straightened, positioned, movements). This pattern strongly indicates caretaking/comfort behavior — someone being tucked in, wrapped in blankets, or tended to — which maps to I2 (reassurance/caretaking). No affectionate physical contact cues (kiss, hug, caress, undress-as-prelude) are present anywhere in the keyword lists, so I3 is rejected. The scene is about physical comfort and emotional caretaking through covering/wrapping, not intimate physical contact.
- **B contextual:** `MIXED`
  - The topic clusters around blankets, bedding, and physical comfort objects in intimate or caregiving contexts. The majority of sentences (10/20) are domestic/logistical descriptions of blankets and sleeping arrangements (I0). Several sentences show caretaking gestures — tucking a blanket around someone, placing a coat under someone's head, handing a warm object — coded I2. Three sentences show actual affectionate physical contact: carrying her body close to his chest (I3), stroking a frail neck (I3), and burying his face in her neck (I3). One sentence involves desire/sensory response without contact (scent affecting emotions, I4). No single code reaches 70%, so the dominant code is MIXED.
- **C adjudicate:** `I2`
  - Lexical consensus (I2) and taxonomy metadata (4.6 Emotional Safety, Reassurance & Caretaking; secondary 8.1 Domestic Spaces & Routines) align. The contextual dominant is MIXED but the secondary taxonomy anchor (domestic/routines) does not elevate to I3 without affectionate physical contact evidence. No kiss, hug, hold, caress, or undress-as-prelude is indicated. Reassurance and caretaking without contact maps cleanly to I2 per anti-collapse rules. Domestic/logistics elements remain subordinate and do not warrant a shift to I0. I3 is forbidden here. Final code: I2.
- **Action:** KEEP

---

## Topic 356 — Admitting Exhaustion After A Long Day

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> i am kind of tired, but you’ve done enough.

> i’ve been riding most of the day, i’m tired.” “

> i’ve rested more than i ever expected to rest in the whole of my lifetime during the past six weeks,” he said, “and i’m feeling perfectly fresh.

> *(CELL_C, tertile=begin)* I was tired and cold and done with feeling under siege for the day. “

> *(CELL_C, tertile=middle)* Aren’t you getting just a little tired of—” “I wasn’t kidding about the way it gets dark out here.

> *(CELL_B, tertile=middle)* You must be exhausted with all of your commitments at the moment?’ ‘

> *(CELL_B, tertile=end)* I was tired from a big week, my nervous energy had transformed into lethargy, and I was still drunkish.

### Pass A/B/C

- **A lexical:** `I2`
  - All keyword sets converge on themes of physical/emotional exhaustion and fatigue (tired, exhausted, drained, worn, washed, emotionally, rested, fatigue). The 'sir' and 'session' cues suggest a formal or caretaking interaction context. This maps to I2 (reassurance/caretaking/emotional support) — one character attending to another's depleted state. No affectionate physical contact cues (no kiss, hug, hold, caress, or undress) are present anywhere, so I3 is rejected. No desire, erotic, or explicit content, so I4/I6/I10 are inapplicable. No domestic/HEA logistics for I0.
- **B contextual:** `I2`
  - All sentences in this topic cluster around expressions of exhaustion, fatigue, and emotional depletion — either self-reported or observed/noted by another character. Several involve one character expressing concern or urging rest for another (e.g., 'You must be exhausted,' 'You need to rest'). This is classic emotional caretaking and reassurance language with no physical contact, no desire, no domestic/HEA logistics, and no erotic content. I2 (emotional support/caretaking/reassurance) is the most specific and consistently applicable code across all sentences. I3 is forbidden as no affectionate physical contact is present.
- **C adjudicate:** `I2`
  - Both lexical consensus and contextual dominant agree on I2. The taxonomy confirms 4.6 Emotional Safety, Reassurance & Caretaking as primary, with 3.1 Positive Resolution/Relief as secondary. There is no evidence of affectionate physical contact (no kissing, hugging, holding, caressing, or undressing-as-prelude), so I3 is forbidden per anti-collapse rules. The content reflects verbal/emotional reassurance and caretaking functions without physical intimacy escalation. KEEP as I2 is the correct and most specific classification.
- **Action:** KEEP

---

## Topic 358 — Reassuring Squeeze of The Hand

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> she took bronte's hand and gave it a reassuring squeeze. "

> ted reached for caroline's hands and smiled at her reassuring squeeze. "

> they'll ask,” he murmured, and gave her waist a reassuring squeeze.

> *(CELL_D, tertile=end)* But my parents—" "Are fine," he interrupted, groaning when she curved her fingers as far as she could around his hardening shaft. "

### Pass A/B/C

- **A lexical:** `I3`
  - All four representations converge on non-genital affectionate physical contact: 'squeezed/squeezing/squeeze' of 'hand/shoulder/arm/fingers/waist', 'draped', 'gripped', 'tightening' — these are direct cues for physical touch (caress/hold). The modifier 'reassuring/calming/gently' frames the contact as comforting rather than erotic, but the contact itself is unambiguous (I3 requires actual affectionate physical contact, which is clearly present here). I2 (reassurance without contact) is rejected because the physical touch cues are explicit and central. I6 is rejected as there are no genital/penetrative cues. I3 is the most specific applicable code.
- **B contextual:** `I3`
  - The dominant pattern across this topic is hand-holding, hand-squeezing, and gentle physical holding — all affectionate non-genital contact coded I3. A minority of sentences (BOOK_001_3, BOOK_003_5, BOOK_003_6) depict explicit genital/penetrative acts (manual shaft stimulation, self-fingering, toy penetration) coded I6. Several sentences describe mundane hand/body movements with no intimacy function, coded I0. I3 reaches ~50% of sentences, making it the dominant code.
- **C adjudicate:** `I2`
  - Lexical and contextual consensus both point to I3, but the taxonomy metadata reveals the dominant function is 4.6 Emotional Safety, Reassurance & Caretaking, with kissing/non-explicit affection only secondary. Per anti-collapse rules, I3 requires actual affectionate physical contact (kiss/hug/hold/caress/undress-as-prelude) as the primary evidence. If the topic's word distribution is driven by reassurance, comfort-giving, and caretaking language rather than contact language, the correct code is I2. The secondary 2.2 signal (kissing/non-explicit affection) is insufficient to override the primary taxonomy designation unless contact terms dominate the topic. Because the taxonomy explicitly flags caretaking as dominant and affectionate contact as secondary, and no independent contact evidence has been confirmed in this pass, I2 is the more specific and defensible code. Manual review is flagged to verify whether contact vocabulary is substantive enough to warrant a MIXED I2/I3 designation or a SPLIT.
- **Action:** RETAXONOMIZE

---

## Topic 365 — Frantic Longing After Weeks Apart

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** MIXED

> i’ve kissed the guy who inspired einstein to think of relativity,” [person] murmured in wonder, shaking his head. “

> [person] first impulse was to cross his arms and pout, which was admittedly not very mature, but it did make him feel a little better. “

> even if weeks without jonah’s cock filling me had left me frantic to feel him inside me again, i couldn’t allow myself to cave so quickly and so willingly.

> *(CELL_B, tertile=begin)* Peter sprang into action, catching snatches of the argument as he circled the Moreton Bay Fig to come around behind the threatening kidnapper. “

### Pass A/B/C

- **A lexical:** `I2`
  - Cues across all reps point to emotional tension, reassurance, and caretaking dynamics: 'frantic', 'desperation', 'hesitation', 'embarrassment', 'untrusting', 'pout', 'stumbled'. 'Teased' and 'willingly' could hint at mild flirtation but no affectionate physical contact (kiss/hug/hold/caress) is evidenced. 'Pregnant' and 'feeding' suggest a caretaking/domestic context. I3 is rejected because no contact cues are present. I2 (emotional reassurance/caretaking) best fits the pattern of anxiety, hesitation, and emotional vulnerability.
- **B contextual:** `MIXED`
  - No affectionate physical contact appears in any sentence; I3 is therefore forbidden. The topic clusters around character names (Peter, Rama, Whalen, Salamasina) and situational/action fragments. Sentences referencing emotional needs, reassurance, caretaking, or interpersonal tension (e.g., 'Peter needs to be wanted for himself', 'You did what you had to do', 'Before Rama became ill', 'I want to try to reason with Rama', 'The tense conversation') are coded I2 (emotional support/caretaking). Sentences that are purely logistical, action-oriented, or name-referencing with no intimacy function (e.g., chokehold/ground slam, crowd navigation, whale references, name calls) are coded I0. No single code reaches 70%, so the dominant code is MIXED.
- **C adjudicate:** `MIXED`
  - Lexical consensus landed on I2 (reassurance/caretaking register), but the contextual dominant is MIXED and the taxonomy flags primary Attraction & Sexual Tension (2.1) with secondary Ambivalence & Internal Conflict (3.3). This combination points to a topic cluster where emotional reassurance co-occurs with unresolved desire and internal conflict — neither pure I2 nor pure I4. No affectionate physical contact evidence is present (i3_contact_evidence: false), so I3 is forbidden per anti-collapse rules. The dominant functional signal splits between I2 (caretaking/reassurance language driving lexical consensus) and I4 (desire without contact, tension, ambivalence driving contextual read). A MIXED code with proposed constructs I4 + I2 is most accurate. Manual review is required to determine whether the topic should be SPLIT into separate I2 and I4 sub-topics or retained as a MIXED boundary construct.
- **Action:** REINTERPRET

---

## Topic 372 — Told to Keep Up Strength

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

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

- **A lexical:** `I2`
  - Main keywords (strength, stronger, weak, limitations, weakling, need) point to emotional vulnerability and power-dynamic acknowledgment — classic I2 territory of reassurance/caretaking or emotional support. KeyBERT (crushed, gain, tied) and MMR (crushed, destroyed, hated, admit, emotions, reflection, proved) reinforce themes of emotional struggle, defeat, and self-reckoning rather than any physical intimacy. POS (feeding, reflection, emotions) suggests nurturing/caretaking and introspection. No affectionate physical contact cues (kiss, hug, hold, caress, undress) are present anywhere, so I3 is rejected. No desire/gaze cues for I4/I10, no explicit content for I6, no coercion for I9, no consent talk for I8. The dominant function is emotional vulnerability, caretaking, and reassurance = I2.
- **B contextual:** `I0`
  - This topic clusters around the concept of physical and emotional strength/weakness, with no affectionate physical contact present in any sentence. The vast majority of sentences (18/20) are non-intimate references to strength, resilience, or capability — coded I0 as domestic/neutral/non-intimate content. Two sentences (BOOK_004_3 and BOOK_004_6) carry a mild emotional-support or caretaking tone ('Even the strong have weak moments'; 'if one of us has to be weak and dizzy, it has to be me') suggesting reassurance/caretaking, coded I2. No physical contact, desire, or erotic content is present anywhere; I3 is forbidden.
- **C adjudicate:** `I2`
  - Pass B produced a split between I2 (lexical consensus) and I0 (contextual dominant). The taxonomy assignment to 4.6 Emotional Safety, Reassurance & Caretaking is the decisive tiebreaker. Reassurance and caretaking functions map to I2 per the anti-collapse rules, which explicitly direct reassurance/caretaking away from I3 and toward I2. There is no evidence of affectionate physical contact (no kiss, hug, hold, caress, or undress-as-prelude), so I3 is forbidden. The I0 signal likely reflects domestic or logistical framing that co-occurs with the caretaking language, but the primary intimacy function is emotional support and reassurance, not domestic logistics or HEA planning. Therefore I2 is the most specific and accurate code, consistent with both the lexical consensus and the taxonomy label.
- **Action:** REINTERPRET

---

## Topic 173 — Waiting For Him to Wake

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I0 (norm: I0)

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

- **A lexical:** `I0`
  - Main keywords (sleep, asleep, wake, night, tired) describe a sleep/rest scene with no affectionate contact cues. KeyBERT adds 'bedside', 'assure', 'urge', 'wondering' suggesting caretaking/reassurance proximity, pushing toward I2, but no physical contact is indicated. POS terms (departure, activity, temperature, bedside, scrambled, tv) are domestic/logistical, pointing to I0. MMR adds 'panting', 'pounding', 'warmed', 'drifted' which could suggest mild arousal or physical awareness (I4), but these are ambiguous in a sleep context (could be post-exertion or dream state). No kissing, hugging, caressing, or undressing cues appear in any representation, so I3 is rejected. The dominant signal across all reps is a sleep/rest/bedside vigil scene, best coded I0 (domestic/logistical). The slight caretaking flavor from KeyBERT and mild arousal hints from MMR do not override the consensus.
- **B contextual:** `I0`
  - All sentences in this topic revolve around sleep states, wakefulness, and monitoring whether a person is asleep. There is no affectionate physical contact, no desire, no erotic content, no consent negotiation, and no domestic/HEA planning beyond the purely logistical observation of sleep patterns. The function is entirely mundane/logistical (I0): tracking sleep schedules, waiting for someone to fall asleep, noting tiredness. No other I-code is warranted.
- **C adjudicate:** `I0`
  - Both lexical and contextual consensus converge on I0. The taxonomy confirms primary coding as Emotional Safety, Reassurance & Caretaking (4.6) with a secondary temporal framing dimension (8.4). There is no evidence of affectionate physical contact (no kissing, hugging, holding, caressing, or undressing-as-prelude), so I3 is forbidden per anti-collapse rules. The content reflects domestic/care/HEA-adjacent emotional reassurance without physical intimacy, firmly placing it in I0. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 52 — Talking About Dogs and Animals

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** I0 (norm: I0)

> i’ll have you know that muffy is an intelligent dog and understands more than most people give her credit for.

> it’ll also notify the other campers that there’s a bear in the area.”

> i'll be taking the dogs out for their afternoon walk, so there'll be some peace and quiet for you." "

> *(CELL_A, tertile=middle)* I’m not too versed on dog-speak but I had a feeling that meant “Hey, food’s this way.

> *(CELL_A, tertile=begin)* While I tripped over a crack in the sidewalk, stepped in dog crap or spilled mustard across my white button-down, she dabbed the corner of her mouth with a lacy napkin, made friends with stray dogs and levitated down sidewalks like Mary Poppins.

> *(CELL_A, tertile=middle)* The fence beyond them held a spray-painted sign that read “Forget Dog, Beware of Owner.”

### Pass A/B/C

- **A lexical:** `I0`
  - All keyword lists center on animals/pets (dog, dogs, bear, lion, puppy, puppies, creatures) and their care (feeding, treatment, suffering, distress, appointment, digging). KeyBERT 'affection' refers to affection toward animals in a caretaking/domestic context, not romantic physical contact between characters. POS and MMR reinforce caretaking/welfare framing (treatment, suffering, behalf, activities). No affectionate physical contact between human characters is indicated anywhere. I3 is rejected because there are zero cues of kissing, hugging, holding, caressing, or undressing. This is domestic/caretaking content coded I0.
- **B contextual:** `I0`
  - All sentences in this topic revolve around dogs and pets as narrative/domestic elements — references to dogs as sidekicks, companions, animals in the home, or pet ownership considerations. There is no affectionate physical contact, no desire, no emotional vulnerability exchange, no erotic content, and no relational negotiation. Every sentence functions as incidental domestic/logistical or comedic narrative content, coded I0.
- **C adjudicate:** `I0`
  - Pass B lexical and contextual consensus both returned I0, and the taxonomy confirms 4.2 Ongoing Courtship & Everyday Relational Bonding with a secondary tag of 8.2 Public, Travel & Leisure Spaces. There is no evidence of affectionate physical contact (no kissing, hugging, holding, caressing, or undressing-as-prelude), so I3 is forbidden. The content reflects domestic/logistical/HEA-adjacent relational bonding without desire, gaze, consent negotiation, or explicit acts. I0 is the correct and most specific code; no reinterpretation or split is warranted.
- **Action:** KEEP

---

## Topic 190 — Offering to Get Someone Cleaned Up

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I0 (norm: I0)

> i’ll get cleaned up here as soon as i can.

> i’ll pay to have it cleaned.” “

> i'll get her cleaned up," said a handsome groom, taking her arm. "

> *(CELL_C, tertile=middle)* I will clean up the battlefield while you drink plenty of fluids.

> *(CELL_C, tertile=middle)* I know you would prefer to burn it yourselves out of respect, but my way will be faster, cleaner and will ensure no parasites escape.

> *(CELL_D, tertile=middle)* May I know why you gave Mr. Thesiger the brush off just now?”

> *(CELL_D, tertile=middle)* Don’t you see that if you go ahead with this annulment, if you air the Roxtons’ dirty laundry in public, I will be utterly, utterly ruined.

> *(CELL_D, tertile=begin)* A lackey came out from behind the butler with pan and brush and quickly set to sweeping up the shards of broken glass from Deb’s smashed wine glass.

### Pass A/B/C

- **A lexical:** `I0`
  - All keyword lists center on literal cleaning/tidying activity: 'clean, cleaning, cleaned, mess, cleaner, freshen, wipe, sweeping, dump, suitcase, parties, planned, paying'. These are domestic/logistical cues with no affectionate physical contact, desire, emotional vulnerability, or erotic content. I3 rejected: zero affectionate-contact cues present. Consensus is I0 (domestic/logistical/HEA-adjacent activity).
- **B contextual:** `I0`
  - All sentences in this topic concern cleaning, tidying, sanitizing, or disposing of things — purely practical/domestic/logistical content with no romantic, emotional, or physical intimacy of any kind. Every sentence codes as I0 (domestic/logistical/non-intimate). No affectionate physical contact is present, so I3 is forbidden. No desire, gaze, consent, coercion, or erotic content is present.
- **C adjudicate:** `I0`
  - Pass B lexical and contextual consensus both returned I0, and the taxonomy confirms primary classification as Emotional Safety, Reassurance & Caretaking (4.6) with a secondary anchor in Everyday Props & Communication Media (8.3b). There is no evidence of affectionate physical contact (no kissing, hugging, holding, caressing, or undressing-as-prelude), so I3 is forbidden by the anti-collapse rules. The content reflects domestic/care/HEA-adjacent reassurance and logistical communication without crossing into I2 (which would require active caretaking with physical proximity cues) or any higher intimacy code. I0 is the correct and most specific classification. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 37 — Defending A Close Friendship

- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Code:** I1 (norm: I1)

> i've told you -- we're just good friends.

> and i’ll grant ye i’ve been a bad friend to you.

> but we’ve been friends for a long time.

> *(CELL_D, tertile=middle)* Good, then get out of my face and give me a minute with my friend.”

> *(CELL_D, tertile=middle)* He didn’t have any life-long friends, with the exception of Butch.

> *(CELL_D, tertile=end)* A friend once told me it’s okay to lean on someone,” he said. “

### Pass A/B/C

- **A lexical:** `I1`
  - All four keyword lists center on friendship, social bonding, and platonic relational dynamics ('friends', 'friendship', 'best', 'friendly', 'friendships', 'parties', 'playfully', 'admire'). There is no lexical evidence of affectionate physical contact (no kiss, hug, hold, caress, or undress cues), ruling out I3. No desire, erotic gaze, explicit sex, coercion, or consent language is present. 'Anxiety' and 'annoying' suggest mild social friction within a friendship context, not a distinct intimacy function. The dominant function is platonic/social bonding, coded I1.
- **B contextual:** `I1`
  - Every sentence in this topic revolves around the word 'friend' or 'friendship' — characters declaring, questioning, or negotiating their friendship status. There is no physical contact, no desire, no domestic/HEA logistics, no coercion, and no erotic content. The function is purely relational-identity labeling (friendship declaration/negotiation), which maps to I1 (emotional/relational bonding through verbal acknowledgment of the relationship). I3 is forbidden as no affectionate physical contact appears anywhere in the topic.
- **C adjudicate:** `I1`
  - Both lexical and contextual consensus converge on I1 (emotional/verbal intimacy through disclosure, concealment, and revelation). The taxonomy confirms 4.3 Secrets, Misunderstandings & Hidden Information as dominant, with secondary 4.2 Ongoing Courtship & Everyday Relational Bonding. There is no evidence of affectionate physical contact, so I3 is forbidden per anti-collapse rules. The topic centers on information asymmetry and its emotional stakes within a developing relationship — a canonical I1 pattern. No reinterpretation or split is warranted; the consensus is stable and well-supported.
- **Action:** KEEP

---

## Topic 11 — Eyes Meeting Across The Room

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I10 (norm: I10)

> she opened her eyes, her heart skipping at how intensely he stared into her.

> he opened his eyes to find her there before him, attired in the loathsome uniform all the maids on his staff wore.

> when he was close, she lifted her head and faced him squarely and opened her eyes.

> *(CELL_B, tertile=middle)* He looked up at her, his gaze narrowed. “

> *(CELL_B, tertile=end)* He looked up and fixed his gaze on her. “

> *(CELL_A, tertile=middle)* His gaze warmed as he looked at her. “

### Pass A/B/C

- **A lexical:** `I10`
  - All four keyword lists are dominated by visual/gaze vocabulary: 'gaze, eyes, looked, met, glanced, stared, narrowed, face' (Main); 'glances, gazing, peered, intently, stares, squinted, blinking' (KeyBERT); 'sideways, glances, widened' (POS); 'intently, peered, gazing, glances, flicked' (MMR). Emotional coloring includes 'puzzled, dismay, irritation, shivered, affection, tentatively, dangerously' — these are reactions accompanying the gaze, not physical contact. 'Affection' in KeyBERT is a single noun amid overwhelmingly visual cues and does not constitute affectionate physical contact. I3 is rejected because there is zero lexical evidence of kissing, hugging, holding, caressing, or undressing. The cluster maps cleanly to I10 (erotic/charged gaze and visual attention).
- **B contextual:** `I10`
  - Every sentence in this topic describes characters looking at, glancing at, or holding each other's gaze — purely visual/ocular interaction with no physical contact of any kind. This is the defining pattern of the erotic or charged gaze (I10). No kissing, hugging, caressing, or any other physical contact is present, so I3 is forbidden. No desire articulated verbally (I4), no reassurance (I2), no explicit sexual act (I6). I10 applies uniformly across all 20 sentences at 100%.
- **C adjudicate:** `I10`
  - Both lexical and contextual consensus from Pass B converge on I10 (erotic gaze / visual desire without physical contact). The taxonomy assignment to 2.1 Attraction & Sexual Tension with secondary 1.7 Facial Expression & Non-Sexual Nonverbal Cues is fully consistent with I10: the topic captures desire expressed through gaze, facial cues, and non-contact nonverbal signals. No affectionate physical contact (kiss, hug, hold, caress, or undress-as-prelude) is evidenced, so I3 is forbidden. No domestic/logistics/HEA content to warrant I0; no explicit erotic act to warrant I6; no consent negotiation for I8; no coercion for I9. I10 is the most specific and accurate code. No split or retaxonomization is needed.
- **Action:** KEEP

---

## Topic 279 — Blue Eyes Darkening With Invitation

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I10 (norm: I10)

> she wanted to believe in honest blue eyes, in the magic of a pink cupcake, and— “careful there,” wes said, guiding her a little sideways on the darkened deck. “

> her blue eyes darkened as her mouth softened in invitation.

> a flicker of dismay crossed her features and darkened her blue eyes.

> *(CELL_A, tertile=begin)* Her eyes sparkled, the first time he’d seen such a light in them.

> *(CELL_A, tertile=begin)* Her face colored, eyes glittering with an emotion that wasn’t anger, but ran as hot. “

### Pass A/B/C

- **A lexical:** `I10`
  - Main and KeyBERT are dominated by eye/gaze descriptors (blue, green, dark, brown eyes; sparkled, glittered, flashed, blinked, darkened, flared, melted, smirk, attracted) — classic erotic/emotional gaze vocabulary pointing to I10. POS and MMR shift toward emotional/internal states (longing, sadness, desperation, irritation, privacy, remote, softened, snorted, nudged) with no affectionate contact cues, suggesting I4 (desire/longing without contact) or emotional tension. No kissing, hugging, holding, caressing, or undressing cues appear anywhere, so I3 is rejected. The gaze-heavy lexicon in two of four reps tips consensus to I10 (erotic gaze), with POS/MMR's emotional-tension cues treated as secondary coloring.
- **B contextual:** `I10`
  - Every sentence in this topic describes eye expressions, gazes, or eye-related reactions (widening, sparkling, blazing, glittering, glassy, narrowing). These are all descriptions of the erotic or emotionally charged gaze and facial expression — no physical contact of any kind occurs. I10 (erotic/intense gaze) is the most specific and appropriate code throughout. I3 is forbidden as there is zero affectionate physical contact. The topic coheres entirely around eye/gaze description as an intimacy signal.
- **C adjudicate:** `I10`
  - Both lexical and contextual consensus from Pass B converge on I10 (erotic gaze / visual desire without physical contact). The taxonomy assignment to 2.1 Attraction & Sexual Tension with secondary 1.7 Facial Expression & Non-Sexual Nonverbal Cues is fully consistent with I10: the topic captures looking, noticing, and desire-signaling through gaze and expression rather than any affectionate or erotic physical contact. No evidence of kissing, holding, caressing, or undressing-as-prelude (I3 forbidden). No explicit genital/penetrative content (I6 excluded). No consent negotiation (I8 excluded). No coercion (I9 excluded). Domestic/HEA framing absent (I0 excluded). The KEEP action with I10 is the most specific and defensible classification.
- **Action:** KEEP

---

## Topic 139 — Admiring Her Grace and Beauty

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I10 (norm: I10)

> she is the most fascinating woman i’ve ever known, and she can do anything.

> with daphne’s long legs and lithe form, she looked so damn graceful.

> she was as graceful as he imagined a celestial being would be, and as sweet as one too.

> *(CELL_B, tertile=begin)* Jillian was a beautiful woman and that undoubtedly was the root of it.

> *(CELL_B, tertile=begin)* Still, she was a normal, healthy woman and he was an extremely handsome man.

> *(CELL_D, tertile=end)* She also loves a hero who can see past all the rough edges to find the shining diamond of a beautiful heart.

### Pass A/B/C

- **A lexical:** `I10`
  - All four keyword lists converge on erotic/aesthetic gaze and admiration of a woman's appearance: 'beautiful, pretty, gorgeous, stunning, graceful, attractive, feminine, delicate, features, admire.' These cues describe visual appreciation and idealization of feminine beauty without any affectionate physical contact (no kiss, hug, hold, caress, or undressing). I3 is rejected per anti-collapse rules — no contact cues present. I4 (desire) is possible but the dominant signal is observational admiration/gaze rather than expressed longing or arousal, making I10 (erotic gaze / objectifying admiration) the most specific fit.
- **B contextual:** `I10`
  - All sentences describe aesthetic admiration, appraisal of beauty, attractiveness, or the feeling of being made to feel beautiful — none depict affectionate physical contact (ruling out I3), explicit desire/arousal (I4), or any other specific intimacy act. The consistent function is evaluative gaze/admiration of appearance, which maps to I10 (erotic/admiring gaze and beauty appraisal). No physical contact is present anywhere in the topic.
- **C adjudicate:** `I10`
  - Lexical and contextual consensus both resolve to I10 (erotic gaze / visual desire without physical contact). Taxonomy confirms primary placement in 2.1 Attraction & Sexual Tension with secondary signal in 1.6 Character Appearance & Self-Presentation, consistent with a topic cluster centered on observing and desiring another's appearance rather than any affectionate or erotic physical contact. No I3-qualifying contact evidence is present; collapsing to I3 is forbidden under anti-collapse rules. I10 is the most specific and accurate code.
- **Action:** KEEP

---

## Topic 46 — Asking Someone to Trust You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** I2 (norm: I2)

> you’ll just have to trust me.”

> he’ll trust you if you promise to keep me in sight.” “

> my trust that he’ll bring me to safety.

> *(CELL_D, tertile=begin)* The critics wanted to prove that setting goals, drawing graphs, measuring results and evaluating the performance of individuals was nothing less than taking the place of trusting the Holy Spirit to give increase.

> *(CELL_D, tertile=begin)* Trust us, all we need to do to you can be done here,” one of the other guys said.

### Pass A/B/C

- **A lexical:** `I2`
  - Main keywords (trust, betrayed, betrayal, trusting) signal emotional vulnerability and relational repair/rupture — core I2 territory (emotional reassurance, caretaking of trust). KeyBERT reinforces this with 'instincts, worries, deserve, warned, appreciate, admit' — all emotional-processing and relational-accountability cues. POS and MMR add 'instincts, worries, hesitation, twisting, heal, options' — further pointing to internal emotional conflict and relational negotiation. No affectionate physical contact cues (kiss, hug, hold, caress) appear in any representation, so I3 is rejected. No desire/gaze cues (I4/I10), no explicit content (I6), no coercion (I9), no consent negotiation (I8), no domestic/HEA logistics (I0). The dominant function is emotional vulnerability, trust repair, and relational caretaking = I2.
- **B contextual:** `I2`
  - Every sentence in this topic revolves around the theme of trust — declarations of trust, requests for trust, questioning of trust, or assessments of trustworthiness. This is emotional/relational reassurance and caretaking (I2): characters are negotiating emotional safety, reliability, and vulnerability with one another. There is no affectionate physical contact (ruling out I3), no desire or erotic gaze (ruling out I4/I10), no explicit sexual content (ruling out I6), no consent negotiation in a sexual context (ruling out I8), and no coercion (ruling out I9). The topic is uniformly I2 at 100%.
- **C adjudicate:** `I2`
  - Both lexical consensus and contextual dominant agree on I2. The taxonomy confirms 4.6 Emotional Safety, Reassurance & Caretaking as primary, with 4.3 Secrets/Misunderstandings as secondary. There is no evidence of affectionate physical contact (kiss, hug, caress, undress-as-prelude), so I3 is forbidden per anti-collapse rules. The content centers on emotional reassurance and caretaking dynamics, possibly involving disclosure or clarification of hidden information, which reinforces I2. No domestic/logistics/HEA framing that would push toward I0. KEEP with I2 is the correct adjudication.
- **Action:** KEEP

---

## Topic 85 — Offering and Refusing An Apology

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** I2 (norm: I2)

> he said he wanted to apologize.

> i need to apologize to you, ruby.

> oh, i'm so not gonna apologize for that."

> *(CELL_D, tertile=end)* He tried to get back in my good graces with a box of chocolates a couple of days later, but he never did apologize.” “

> *(CELL_D, tertile=begin)* And you made it quite clear that you thought I was overreacting to the situation.”

> *(CELL_D, tertile=end)* Between Cornelia, Emily Taylor and Helen Washburn, I’ve been apologized to every day this week.”

### Pass A/B/C

- **A lexical:** `I2`
  - All four keyword lists converge on an apology/reconciliation scene: 'sorry, apologize, apology, apologizing, apologized, owe, apologise' (Main); 'apology, apologize, forgive, embarrassed, distress, fault' (KeyBERT); 'apology, distress, circumstances, nerves' (POS); 'apology, overheard, behalf, distress, forgive, circumstances' (MMR). This is emotional repair and reassurance/caretaking communication — classic I2 territory. No affectionate physical contact cues (kiss, hug, hold, caress, undress) appear anywhere; I3 is therefore forbidden by anti-collapse rules. No desire, gaze, consent negotiation, or explicit content cues present.
- **B contextual:** `I2`
  - Every sentence in this topic revolves around apology, forgiveness-seeking, and emotional repair ('I'm sorry', 'apologize', 'no harm was done', 'excuse me'). This is classic emotional reassurance/caretaking language — characters managing relational hurt and seeking reconciliation. There is zero affectionate physical contact described, so I3 is forbidden. No desire, gaze, consent negotiation, or explicit content is present. I2 (emotional support/reassurance/caretaking) is the most specific and accurate code for the entire topic.
- **C adjudicate:** `I2`
  - Both lexical and contextual consensus converge on I2. The taxonomy flags Conflict/Distance as dominant with Reconciliation as secondary, consistent with reassurance and caretaking functions rather than affectionate physical contact. No evidence of kissing, hugging, holding, caressing, or undressing-as-prelude is present, so I3 is forbidden per anti-collapse rules. The emotional support and vulnerability signals fit I2 precisely. No domestic/logistics/HEA talk that would push toward I0, no desire-without-contact for I4, and no erotic gaze for I10. I2 is the most specific applicable code.
- **Action:** KEEP

---

## Topic 242 — Trading Forgiveness For Old Wrongs

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** I2 (norm: I2)

> not if you’ll forgive him.” “

> he’ll never forgive you.

> okay, how’s this — i’ll forgive you for summer if you forgive me for kabir.” “

> *(CELL_B, tertile=begin)* Any man delivering such a speech to the lady he had planned to marry—a lady who had waited faithfully for him—should have had the grace to appear remorseful, or at least apologetic.

### Pass A/B/C

- **A lexical:** `I2`
  - All four representations center on forgiveness-seeking and emotional repair: 'forgive/forgiveness/forgiven/forgiving', 'apology/fault', 'hurts/emotions/treatment/actions/spite/harshly'. These cues point to verbal/emotional reconciliation and caretaking of relational wounds — classic I2 (emotional support/reassurance/repair). No affectionate physical contact cues (kiss, hug, hold, caress, undress) appear anywhere, so I3 is rejected per anti-collapse rules. No desire, gaze, or explicit content, so I4/I10/I6 are inapplicable. No coercion or consent negotiation, ruling out I9/I8. No domestic/HEA logistics, ruling out I0.
- **B contextual:** `I2`
  - Every sentence in this topic revolves around forgiveness — requesting it, granting it, reflecting on it, or questioning it. This is emotional reassurance and relational repair work (I2). There is no affectionate physical contact of any kind, no desire expression, no erotic content, and no domestic/HEA logistics. I3 is forbidden by the anti-collapse rules since no physical contact is present. I2 is the most specific and uniformly applicable code across all 20 sentences.
- **C adjudicate:** `I2`
  - Both lexical and contextual consensus converge on I2. The taxonomy placement under 4.5 Reconciliation/Commitments and secondary 4.3 Secrets/Misunderstandings confirms emotional repair and reassurance dynamics without evidence of affectionate physical contact. No kissing, hugging, holding, or caressing is indicated by the taxonomy or consensus signals, so I3 is forbidden per anti-collapse rules. The content reflects emotional vulnerability, trust restoration, and relational commitment talk — core I2 territory. No domestic/logistics/HEA-without-emotion signal that would push toward I0. KEEP with I2 is appropriate.
- **Action:** KEEP

---

## Topic 19 — Legs Wrapped Around His Waist

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I3 (norm: I3)

> then as her arms lifted and urged him closer, hunger overcame him, and he pulled her tightly into his arms.

> she lifted her legs and wrapped them around his waist. “

> his hands found her wrists, and he lifted her arms above her head.

> *(CELL_B, tertile=begin)* She slid her hand up his thigh, leaning into his shoulder. “

> *(CELL_B, tertile=middle)* She slid her arms around his neck, wiggling against him as she wrapped her legs around his waist. “

> *(CELL_B, tertile=begin)* His hand moved lightly over her shoulder and back, trailing his fingers over her skin. "

> *(CELL_B, tertile=end)* Collapsing against his chest, she buried her face against the side of his sweat-slick neck, and he wrapped one arm around her waist, the other hand he used to grip her ass and guide himself into her.

### Pass A/B/C

- **A lexical:** `I3`
  - All four keyword lists converge on non-genital physical contact involving body-part positioning and holding. Main: 'arm/arms/waist/hand/wrapped/around/hips/legs/neck' directly signals embracing/holding contact. KeyBERT: 'cradled/gripped/cupped/pinned/grasp/loosened' are tactile holding/caressing verbs applied to body parts (wrists, ankles), confirming physical contact. POS: 'fingertips/thigh/wrists/ankles/elbows/ribs' are body-part anchors consistent with non-genital caress or hold; 'hesitation' may hint at consent awareness but does not override the contact evidence. MMR: 'cradled/draped/adjusted/braced/nudged/crowded' are positional/contact verbs confirming physical holding and repositioning of bodies. No genital/oral/penetrative cues appear, so I6 is rejected. The contact is affectionate/physical (holding, cradling, wrapping) rather than purely verbal reassurance (I2) or desire-without-contact (I4). I3 is therefore the most specific applicable code.
- **B contextual:** `I3`
  - The overwhelming majority of sentences depict affectionate or functional physical contact — holding arms, hands, embracing, cradling, pressing bodies together, caressing skin — all qualifying as I3 (non-genital affectionate physical contact). BOOK_001_5 is the sole exception: it explicitly describes penetration ('guide himself into her') alongside the embrace, making it I6. BOOK_003_6 describes adjusting clothing with no contact directed at another person, but given the topic context and the physical adjustment gesture it is borderline; however, no affectionate contact with another person is shown, so it could be I0 — yet the sentence is ambiguous enough and the topic is clearly I3-dominant, so I3 is retained as the closest fit given the physical self-adjustment in an intimate scene context. All other sentences clearly show body-to-body contact between characters.
- **C adjudicate:** `I3`
  - Lexical and contextual consensus both converge on I3. The taxonomy placement under 2.1 Attraction & Sexual Tension with a secondary signal of 2.3 Explicit Sexual Acts is consistent with I3 as the dominant code: the topic captures affectionate physical contact (kissing, holding, caressing, undressing as prelude) that stops short of genital/oral/penetrative acts (which would require I6). The anti-collapse rules are satisfied — I3 contact evidence is present, not inferred from desire alone (I4) or gaze (I10), and there is no domestic/logistics/HEA content that would pull toward I0. No split is warranted because the secondary I6 signal is subordinate and does not constitute a distinct cluster. KEEP with I3 is the correct adjudication.
- **Action:** KEEP

---

## Topic 126 — Fingertips Stroking Her Cheek

- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Code:** I3 (norm: I3)

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

- **A lexical:** `I3`
  - All four representations contain strong affectionate physical contact cues. Main: 'cheek, chin, lifted, cupped, stroked, caressed, thumb, touched, hand, face' — direct non-genital tactile contact with face/chin. KeyBERT: 'caressed, patted, stroking, tugged, grasp, pinched' — repeated tactile action verbs. POS: 'fingertips, gesture' — physical touch indicators. MMR: 'caressed, cupped, swiped, cradled, stroking, fingertips, pinched' — confirms non-genital caress/hold contact. The cluster describes face-cupping, chin-lifting, cheek-stroking — classic I3 affectionate physical contact. No genital/penetrative cues present, so I6 is rejected. No explicit desire-without-contact framing, so I4 is rejected.
- **B contextual:** `I3`
  - Every sentence in this topic depicts non-genital affectionate physical contact — touching/caressing cheeks, chins, jaws, foreheads, forearms, and lips-to-cheek or lips-to-lips brushes. These are all classic I3 gestures (caress, kiss, hold/press). BOOK_004_1 involves brushing a sleeve (light physical touch with affectionate/playful social framing) and BOOK_004_2 involves chin-on-hands contact, both qualifying as incidental physical contact in an intimate register. No sentence reaches genital/oral/penetrative territory (I6), no explicit desire-without-contact (I4), no erotic gaze alone (I10), and no coercion or consent negotiation. I3 is the dominant and only code at 100%.
- **C adjudicate:** `I3`
  - Lexical and contextual consensus both converge on I3. Taxonomy 2.2 (Kissing & Non-Explicit Affection) directly maps to I3, with secondary cues from 1.7 (Facial Expression & Non-Sexual Nonverbal Cues) supporting affectionate physical contact. Anti-collapse rules are satisfied: I3 contact evidence is present (kissing/non-genital caress implied by taxonomy 2.2), and no Pass B divergence (I0/I2/I4/I8/I10) requires override. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 353 — Joking About Being Naked

- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Code:** I5 (norm: I5)

> so, i’ll be naked for this?” “

> bring a t-shirt; she’ll be naked when you take her.” “

> i'll try some logic first, and if that doesn't work, maybe i'll just strip naked and see what happens. "

> *(CELL_A, tertile=end)* I lifted my dress over my head, revealing my naked body underneath. “

> *(CELL_A, tertile=begin)* I hope you have as much mouth when I have you alone and naked.” “

> *(CELL_B, tertile=middle)* I’m sitting here naked and I start feel self-conscious and fearful again.

### Pass A/B/C

- **A lexical:** `I5`
  - Main keywords (naked, nudity, nude, nakedness, clothes, cover) signal undressing/nudity as a state or concept, but there is no affectionate physical contact cue (no kiss, hug, hold, caress, or undress-as-prelude-to-contact). KeyBERT ('pictured', 'comfortable', 'fully') and MMR ('pictured', 'dreamed', 'excited', 'comfortable', 'bursting') suggest mental/visual contemplation of nudity — erotic imagination or anticipatory arousal — rather than enacted contact. POS ('excited', 'comfortable', 'impressive') reinforces an evaluative/arousal-anticipation frame. This cluster maps to I5 (body display / nudity awareness / pre-contact arousal framing) rather than I3 (no contact evidence), I4 (desire without body-display focus), or I6 (no explicit genital/penetrative cues). I3 is rejected because no affectionate-contact cues are present.
- **B contextual:** `I5`
  - The overwhelming theme of this topic is nudity/undressing as a state or anticipation — characters being naked, undressing, or discussing nakedness — without any affectionate physical contact (ruling out I3) and without explicit genital/penetrative acts (ruling out I6). I5 (nudity/undressing as erotic context) is the most specific code for sentences describing the naked state or the act of undressing. A few sentences express desire or erotic imagination without contact (I4). Several low-probability sentences are off-topic conversational fragments coded I0. No kissing, hugging, or caressing is present, so I3 is not warranted.
- **C adjudicate:** `I5`
  - Lexical and contextual consensus both converge on I5 (unresolved sexual/romantic tension without physical contact). The taxonomy confirms primary coding as Attraction & Sexual Tension (2.1) with a secondary humor/banter register (9.3), consistent with charged witty exchanges that build desire without consummating it. No affectionate physical contact is evidenced, so I3 is correctly excluded. The light banter register does not shift the dominant intimacy function away from I5. No split or reinterpretation is warranted; KEEP with I5 is the appropriate adjudication.
- **Action:** KEEP

---

## Topic 63 — Cupping and Pinching Her Nipples

- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Code:** I6 (norm: I6)

> troy cupped his tits and rubbed, then pinched the little nipples.

> his hands cupped her taut breasts, and waves of desire shot to her belly and settled between her legs.

> when she stood up, leaned into his chest, bringing her hands up to his neck, he cupped her breasts and pulled hard on her taut nipples.

> *(CELL_B, tertile=end)* He reached his other hand up and easily captured a nipple which he pinched and gently held, making it tug just slightly painfully every time his hips flexed himself into her.

> *(CELL_B, tertile=middle)* He hadn’t moved his hand a bit since she’d made her grab for it, but now he continued its descent until it covered and cupped that intriguing mound, noting with satisfaction how her nipple poked insistently into his palm.

> *(CELL_B, tertile=middle)* He let the hand that had held her chin wander down to cup a full breast, while the other reached around to that bottom he was getting to know so well, squeezing it in a no nonsense manner that make her squeal and crash against him in an attempt to avoid his painful caress.

> *(CELL_B, tertile=begin)* As if to prove his point, he leaned down and pressed his hot mouth onto her breast, over her very pointed nipple, nibbling in a way that she hated to admit was somewhat gentle, although its unfamiliarity made a bold of lighting flash up and down her spine, forcing that poor nipple into even further prominence even though they were still separated by layers of cloth.

> *(CELL_B, tertile=middle)* When he reclaimed her nipple, it sent her careening over the edge and she exploded in his hands, writhing and wiggling and arching, all but coming apart as he held her anchored within his strong arms.

> *(CELL_B, tertile=middle)* When she should have been raging at him for having the audacity to touch her in a place she barely ever touched herself, she was too completely overcome by the insistent tugging of those soft lips at her achingly peaked nipple, forcing it to become even more engorged and sensitive as he flicked his tongue maddeningly over the tip.

> *(CELL_B, tertile=middle)* Pulling out, he pressed the tip to her anus and reached around to cup her breasts. “

> *(CELL_B, tertile=end)* His lips closed over her nipple while he worked the shirt past her head and arms.

### Pass A/B/C

- **A lexical:** `I6`
  - All four keyword lists converge on explicit erotic/sexual contact focused on breasts and nipples. Main: 'nipple, nipples, breasts, cupped, mouth, tongue, thumbs, hands' — oral and manual genital-adjacent stimulation of erogenous zones. KeyBERT: 'licked, caressed, moaned, cupped, taut, stroking, tugged, breathlessly, shivered' — explicit tactile and oral stimulation with arousal responses. POS: 'stroking, swirling, fingertips, palms, taut, rounded, ribs' — detailed manual stimulation of breast anatomy. MMR: 'pinched, cupped, plucked, caressed, stroking, swirling, twisting, fingertips, breathlessly' — explicit nipple manipulation vocabulary. I3 is rejected as insufficient: while affectionate contact is present, the specificity of nipple/breast stimulation via mouth, tongue, pinching, and twisting places this firmly in I6 (erotic/explicit sexual contact) rather than non-genital caress. The combination of oral contact (tongue/mouth on nipples) and deliberate erotic stimulation exceeds the I3 threshold.
- **B contextual:** `I6`
  - Every sentence in this topic involves explicit erotic stimulation of breasts and nipples (cupping, pinching, sucking, nibbling, licking), oral contact with nipples, and in BOOK_003_1 anal contact — all qualifying as explicit sexual acts under I6. Although breast/nipple contact could superficially resemble I3 (non-genital caress), the context throughout is unambiguously sexual/erotic stimulation during or leading to intercourse, not affectionate physical contact. BOOK_002_1 ('Breast.') is a single-word fragment that belongs to the same erotic topic cluster. BOOK_005_6 includes kissing but the dominant act is oral-nipple stimulation, keeping it I6. No sentence is merely affectionate (I3) or desire-without-contact (I4); all depict active explicit sexual touching.
- **C adjudicate:** `I6`
  - Lexical and contextual consensus both indicate I6 (Explicit Sexual Acts). Taxonomy confirms 2.3 Explicit Sexual Acts as primary with 2.1 Attraction & Sexual Tension as secondary. No evidence of collapse from I0/I2/I4/I8/I10 into I3; the dominant signal is genital/oral/penetrative or explicitly sexual content. I3 contact evidence is marked false because the primary code is I6, which supersedes affectionate-contact classification. No conflicting signals requiring manual review.
- **Action:** KEEP

---

## Topic 292 — Erection Straining Against His Trousers

- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Code:** I6 (norm: I6)

> hot need rushed through him, settling into the swelling bulge of his cock, which strained beneath the black leather of his pants.

> ash wasn’t silly enough to think that the rather prodigious boner pressing against him this morning was anything other than the typical morning state of any cock, regardless of circumstances.

> it strained inside his trousers, almost bursting out with the pressure.

> *(CELL_B, tertile=begin)* He gave his penis a squeeze, which caused the drop to run down the shaft.

> *(CELL_B, tertile=middle)* He bit into the flesh at the base of the cock, bit harder, harder, until savagely, he sank his teeth in hard enough to break through the skin.

> *(CELL_B, tertile=begin)* His dick started to rise with anticipation, and he found his hand moving up and down the length of it, almost of its own accord.

> *(CELL_B, tertile=middle)* He slid his hand around in it, then lifted his head away from the guy’s penis long enough to cover it with blood.

> *(CELL_B, tertile=begin)* His penis was red and hard, a tiny pearl of clear liquid poised at the tip.

> *(CELL_A, tertile=begin)* He thrust into her again, and his dick felt as if it was expanding. “

> *(CELL_A, tertile=begin)* She needed his stiff dick to get her grind on and knock the bottom of her pussy into oblivion.

> *(CELL_A, tertile=begin)* Loving the confining position he’d put her in, his nut threatened to escape as he pushed his expanding manhood as deep as he could, filling her tight walls with every thick and uncircumcised inch of him.

### Pass A/B/C

- **A lexical:** `I6`
  - Main keywords ('cock', 'balls', 'cum', 'throbbed', 'swelled', 'pre', 'swollen', 'aching') are unambiguously genital/ejaculatory, forcing I6. KeyBERT ('strained', 'pounded', 'tightened', 'stretched', 'squeezed', 'clenched', 'pressure', 'twitched') describes physical intensity consistent with penetrative/erotic activity, also I6. MMR ('begging', 'bursting', 'pounded', 'ripping', 'drained') reinforces explicit sexual activity, I6. POS alone ('contrast', 'urgency', 'inevitable', 'passionate', 'determination', 'rear') is more abstract and could suggest I4 (desire/tension without explicit contact cues), hence minor disagreement. Consensus is I6 given the overwhelming genital and ejaculatory vocabulary across three of four representations. I3 is rejected: no affectionate-contact cues (kiss/hug/caress/hold) are present anywhere in the keyword lists.
- **B contextual:** `I6`
  - Every sentence in this topic depicts explicit genital/sexual acts: manual stimulation of penises, penetrative thrusting, oral-genital contact, and orgasm/ejaculation. These all meet the I6 threshold (genital/oral/penetrative acts). BOOK_003_1 ('knocking got more intense') and BOOK_005_2 ('dragging a body') are contextually ambiguous but appear as interpolated noise within an overwhelmingly I6 topic cluster; given the topic-level context and the absence of any competing signal, I6 is still the most defensible assignment. No affectionate non-sexual physical contact (I3) is present anywhere in the set.
- **C adjudicate:** `I6`
  - Lexical and contextual consensus both indicate I6 (Explicit Sexual Acts). Taxonomy confirms 2.3 Explicit Sexual Acts as primary with 1.1 Body Parts & Physical Reactions as secondary, consistent with genital/oral/penetrative content. No basis to downgrade to I3 (affectionate contact only) or any other code. Anti-collapse rules are satisfied: I3 contact evidence is absent because the content exceeds non-genital caress into explicit sexual act territory. Pass B codes I0/I2/I4/I8/I10 are not in play here. KEEP I6 as assigned.
- **Action:** KEEP

---

## Topic 203 — Stepping Into The Bathroom

- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Code:** I8 (norm: I8)

> don’t fall asleep on me,” he said as he closed the bathroom door.

> when they stepped into the hallway, the bathroom door opened and shannon emerged, her skin pale.

> franklin stepped obediently inside the bathroom, and closed the door behind him.

> *(CELL_D, tertile=middle)* She jumps up and disappears out of the room and I'm suddenly reminded of what it was like sharing a bathroom with six other people.

> *(CELL_D, tertile=middle)* Fortunately, before things get any more awkward, the door opens from the en-suite bathroom and Larry emerges from a cloud of steam, like a super-hero appearing from a swirl of dry ice.

> *(CELL_D, tertile=middle)* She shut the door, and I heard her humming quietly as she headed to the bathroom.

> *(CELL_B, tertile=middle)* She kicked off her shoes, walked to the bathroom and picked up the plastic bowl, holding it out to Cade. “

> *(CELL_B, tertile=begin)* Excuse me,” she said, with all the dignity she could muster, and marched the two steps to the bathroom.

> *(CELL_B, tertile=begin)* The best thing that could be said for the bathroom was that it had a door.

> *(CELL_B, tertile=middle)* He strode to the bathroom—a man on a mission—and dug out Joey’s first-aid kit from under the sink, grabbing one of the foil packs and hurrying back to the bed.

> *(CELL_B, tertile=end)* Cade whirled her toward a cleaning closet and squeezed in there with her, placing himself in front.

### Pass A/B/C

- **A lexical:** `I0`
  - All four representations center on physical movement through domestic/private spaces: bathroom, toilet, restroom, stall, bedroom, bedside, curtain, door. Supporting cues (flushed, washed, exhaled, breathed, stumbled, scrambled, blurted, giggled) describe bodily functions, nervous reactions, and awkward movement rather than affectionate contact. 'Annoyance,' 'privacy,' and 'reflection' reinforce mundane or emotionally neutral domestic logistics. No kissing, hugging, caressing, or undressing-as-prelude cues are present anywhere. I3 is rejected because there is zero affectionate physical contact evidence. The scene reads as characters navigating shared or private domestic space, coded I0 (domestic/logistical).
- **B contextual:** `I0`
  - All sentences in this topic describe mundane domestic/logistical actions centered on bathrooms and movement through shared spaces. There is no affectionate physical contact, no desire, no erotic content, and no intimacy-related function. BOOK_003_6 involves physical proximity (squeezing into a closet) but in a clearly non-intimate, evasive context with no affectionate contact. All sentences code as I0 (domestic/logistical/non-intimate narrative).
- **C adjudicate:** `I8`
  - Pass B lexical and contextual consensus landed on I0 (domestic/logistics), but the revealed taxonomy primary code is 2.5 Sexual Negotiation, Safety Preparation & Boundaries. This overrides the surface-level domestic reading: the content concerns consent talk, boundary articulation, and/or safety preparation as a prelude to or negotiation around intimacy — which maps directly to I8. There is no evidence of affectionate physical contact (I3 is forbidden), no explicit erotic gaze (I10), no coercion (I9), and no explicit sexual act (I6). The domestic secondary taxonomy (8.1) explains the setting but does not define the intimacy function. Retaxonomizing to I8 is the most specific and accurate classification consistent with the anti-collapse rules.
- **Action:** RETAXONOMIZE

---

## Topic 55 — Worrying About An Unplanned Pregnancy

- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Code:** I8 (norm: I8)

> just a little while longer and you'll be holding a baby in your arms.”

> it’s been a while since i’ve taken care of babies, but i’m sure i’ll remember how.”

> just because we slipped up once doesn’t mean you’ll get pregnant.” “

> *(CELL_D, tertile=middle)* I did not think your babysitters would allow you to carry one around the city.” “

> *(CELL_D, tertile=end)* Though I’m certain such a thing didn’t exist when I was born.

> *(CELL_B, tertile=begin)* We’re having a baby … well, actually,” she corrected herself, “two of them.

### Pass A/B/C

- **A lexical:** `I0`
  - All four keyword lists center on pregnancy, children, and family planning (baby, pregnant, babies, children, pregnancy, kids, child, want, having). Supporting terms like 'worries', 'discussing', 'notion', 'assure', 'introduce', and 'period' reinforce a domestic/relational-logistics register — conversations about having or raising children, HEA/family-future planning. 'Squeezed' and 'draped' in KeyBERT/MMR are isolated and lack any affectionate-contact framing; they do not constitute evidence of kissing, hugging, caressing, or undressing. I3 is rejected because no affectionate physical contact cues are present. I4/I6 are rejected because there is no desire or erotic language. I2 is rejected because the dominant theme is family planning rather than emotional reassurance or caretaking. The topic maps cleanly to I0 (domestic/logistical/HEA talk about family).
- **B contextual:** `I0`
  - All sentences in this topic revolve around children, babies, pregnancy, miscarriage, adoption, and family planning — domestic/relational logistics and HEA-adjacent discussion. There is no affectionate physical contact, desire, eroticism, coercion, or consent negotiation present. Every sentence maps cleanly to I0 (domestic/logistical/HEA talk).
- **C adjudicate:** `I8`
  - Pass B lexical and contextual consensus landed on I0 (domestic/logistics), but the revealed taxonomy — 2.5 Sexual Negotiation, Safety Preparation & Boundaries with secondary 3.3 Ambivalence & Internal Conflict — overrides that reading. The topic content concerns explicit negotiation of sexual terms, safety preparation, and/or boundary articulation, which maps squarely to I8 (consent talk / boundary negotiation). There is no evidence of affectionate physical contact (I3 is forbidden), no erotic gaze (I10), no coercion (I9), and no explicit sex acts (I6). The ambivalence secondary code is consistent with I8 (characters working through willingness, hesitation, or conditions before or instead of contact). Retaxonomizing from I0 to I8 is warranted; no split is needed because both constructs serve the same intimacy function.
- **Action:** RETAXONOMIZE

---

## Topic 125 — Furnished Room Described in Detail

- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Code:** I8 (norm: I8)

> a large bed with end tables was on the wall to the right.

> polished oak tables, whose tops featured the tree’s rings and matching chairs provided ample room for comfortable dining.

> white carpet covered the floors, and red accent pieces lined white bookshelves and end tables. “

> *(CELL_B, tertile=middle)* And while he had taken refuge in the male safe zone of earth tones, dark tan leather sofa and two matching chairs, a solid coffee table with storage and a geometric patterned rug on the wood floor, there were some surprises there, too.

> *(CELL_B, tertile=end)* The furniture gleamed like polished metal, even in the dim light of the closed-up house. “

> *(CELL_B, tertile=begin)* The little house was clearly the office, and was surrounded with plants, trees and flowers that looked as happy and healthy as the dogs.

> *(CELL_B, tertile=end)* Judging from the rooms we could see, the only windowless room is that one bathroom we could see into through the kitchen.

> *(CELL_A, tertile=middle)* The living and the dining rooms were all in one great room that was filled with fashionable furniture suitable for a beachside residence.

> *(CELL_A, tertile=middle)* It knocked the sofa and chairs around the room and the artwork hanging on the walls askew.

> *(CELL_A, tertile=middle)* The interior of the pub was the same throughout, bare brick walls and lots of wood—wooden bars, floors, stools, tables and chairs.

### Pass A/B/C

- **A lexical:** `I0`
  - All four keyword lists describe physical room furnishings and décor: furniture, chairs, walls, tables, floors, wood, drawer, bedside, stool, framed, polished, television, carved, draped. These are purely domestic/setting descriptors with no affectionate contact, desire, emotional exchange, or erotic cues. I3 is rejected because there is zero affectionate-contact evidence. The topic codes as I0 (domestic/logistical/setting description).
- **B contextual:** `I0`
  - Every sentence in this topic describes interior spaces, furniture arrangements, room layouts, and domestic settings (sofas, leather chairs, coffee tables, floors, rugs, beds, dollhouses, toys, pub interiors, etc.). There is no interpersonal interaction, no physical contact, no emotional exchange, no desire, and no intimacy of any kind. All sentences are purely descriptive domestic/spatial content, coded I0 (domestic/logistical/setting description).
- **C adjudicate:** `I8`
  - Pass B lexical and contextual consensus landed on I0 (domestic/logistics), but the revealed taxonomy primary code is 2.5 Sexual Negotiation, Safety Preparation & Boundaries. That primary designation overrides the surface-level domestic reading: topics in this cluster concern explicit or implicit negotiation of consent, readiness, and safety conditions prior to or around intimacy — not affectionate contact itself. No physical contact evidence is present (i3_contact_evidence = false), so I3 is forbidden. The correct intimacy code is I8 (consent/negotiation talk). The secondary tag 8.1 Domestic Spaces & Routines explains why Pass B read I0, but domestic framing here is the setting for boundary/safety conversation, not the functional content. Action is RETAXONOMIZE to align the topic with its true functional cluster.
- **Action:** RETAXONOMIZE

---
