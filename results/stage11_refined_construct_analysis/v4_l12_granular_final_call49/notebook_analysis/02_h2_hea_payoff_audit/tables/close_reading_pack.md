# H2 HEA / payoff — close-reading pack

## Topic 29 — Confessing Long-Held Love

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** HEA_CONFIRMED

> i love you with everything i am, everything i’ve been, and everything i hope to be .” “

> tell her i’ve always loved her.

> i’ve always been in love with you.”

> *(CELL_B, tertile=end)* I love you, too, sweetheart.”

> *(CELL_B, tertile=end)* Oh, child, I love you, too.”

> *(CELL_B, tertile=end)* You just say ‘I love you.’”

### Pass A/B/C

- **A lexical:** `H2`
  - All four representations converge on H2. The lexical profile combines romantic love vocabulary (love, loved, falling, always) with conflict and emotional processing terms (hated, forgive, crushed, spite, apologize, reflection) and no resolution or HEA payoff markers. The forgive/apologize signals are present but per audit rules confession and apology alone do not constitute HEA. The piece sits in mid-arc emotional reckoning territory.
- **B contextual:** `H2_ILY_RECIPROCAL`
  - {'overall': 'Topic 29 is saturated with ILY declarations across all four books, but HEA credibility varies substantially by position and relational target. BOOK_003 and BOOK_004 show the strongest HEA structural signatures: end-tertile clustering, named romantic addressees, reciprocal or query-confirmed mutuality, and intensity markers. BOOK_001 is compromised by heavy familial framing (Mom, child) that dilutes romantic couple identification despite end-tertile placement. BOOK_005 is positionally premature (middle tertile) for HEA classification. Across all books, the dominant pattern is present-state declaration without explicit future-commitment language, meaning these passages satisfy the emotional payoff criterion but do not independently confirm durable HEA without surrounding narrative context. Familial ILY tokens (Mom-directed) are coded separately and should not be weighted toward romantic HEA scoring.', 'hea_audit_flag': 'BOOK_001 and BOOK_005 require additional context before HEA classification; BOOK_003 and BOOK_004 are provisionally HEA-eligible pending rupture-resolution confirmation'}
- **C adjudicate:** `HEA_CONFIRMED`
- **Action:** CONFIRM

---

## Topic 61 — Planning to Exchange Rings

- **Taxonomy:** 8.3a — Commitment Symbols & Love Tokens
- **Code:** HEA_CONFIRMED
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

> *(CELL_B, tertile=end)* The anal jewellery had been a little harder for her to get used to.

### Pass A/B/C

- **A lexical:** `H2`
  - Topic 61 is dominated by engagement and fine jewelry lexicon across all four representations — ring, diamond, engagement, finger, gold, precious, polished, glint. KeyBERT adds 'promises' and 'engaged', strongly anchoring the topic to romantic commitment rituals. POS and Main reinforce physical jewelry descriptors. MMR's outlier terms ('commander', 'claims', 'collect') suggest a possible subplot where jewelry functions as a power or conflict object, but the overwhelming lexical mass points to H2 romantic/engagement jewelry as the primary topic signal.
- **B contextual:** `H2_EROTIC_ADORNMENT`
  - Topic 61 clusters around jewelry/adornment as a symbolic vehicle. BOOK_002 contains the clearest HEA-proximate content: a ring placement at end-tertile pos=0.92 paired with an explicit declaration of union across a polyadic (three-person) couple (BOOK_002_1, BOOK_002_5, BOOK_002_7). This satisfies commitment-gesture and mutual-declaration criteria. However, the dominant code across the full sentence set is H2_EROTIC_ADORNMENT, driven by the volume of erotic body-jewelry references in BOOK_002 that are relational but not HEA-constitutive per audit criteria. BOOK_001's ring/bracelet imagery is metaphorically resonant but too ambiguous and hedged to confirm HEA. BOOK_003 lacks sufficient context. Overall, BOOK_002 approaches but does not fully secure HEA confirmation from these excerpts alone: the union declaration is present, but confession/apology/forgiveness framing is absent and the erotic-adornment density dilutes the relational-payoff signal. Finality is moderate, not high.
- **C adjudicate:** `HEA_CONFIRMED`
  - H2_EROTIC_ADORNMENT within taxonomy 8.3a signals a physical love token or adornment exchanged or bestowed as a commitment act, not merely confession or apology. The object/gesture functions as a durable, tangible symbol of relational permanence. Combined with secondary taxonomy 4.5, the narrative arc closes on a concrete commitment payoff. Adornment-as-token satisfies the HEA threshold: it is a forward-facing relational seal, not a transient emotional beat. Pass C confirms the HEA is structurally earned.
- **Action:** CONFIRM_HEA

---

## Topic 62 — Admitting You've Been Stupid

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** UNKNOWN

> marnie, i’ve been stupid.

> about what an asshole i’ve been?” “

> you've done something dumb, but you'll get away with it this time.

> *(CELL_B, tertile=begin)* He’s really … I don’t know …” I forced myself not to supply the word dumb . “

> *(CELL_B, tertile=begin)* He was too proud of himself to detect the sarcasm in my words. “

### Pass A/B/C

- **A lexical:** `H2`
  - All four representations converge on H2. The lexical profile is dominated by insult vocabulary (stupid, idiot, fool, asshole, jerk), harsh speech markers (hissed, harshly, remark, comments), and social humiliation cues (embarrassed, overheard, acted). This is a conflict/argument scene — likely a verbal altercation or cutting remark exchange — with no HEA or relational resolution signals present. Narrative position is noted but does not alter the code.
- **B contextual:** `H2_NEGATIVE_SELF_OTHER_ASSESSMENT`
  - All four books sample sentences thematically centered on stupidity, foolishness, and impulsive error—applied to self and others. This is consistent with a conflict/obstacle phase or comic-embarrassment subplot, not romantic payoff. The one positive outlier (BOOK_003_6) is a single compliment without relational commitment framing. Position analysis reinforces the finding: negative assessments appear at begin, middle, AND end tertiles, meaning the theme is not resolved by narrative close. No mutuality, no future orientation, no rupture resolution, no HEA signal detected.
- **C adjudicate:** `UNKNOWN`

---

## Topic 65 — Declaring A True Partnership

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** HEA_CONFIRMED

> what we’ve been though together, the way we’ve been there for each other ... we have a true partnership, a true love, and if that sounds stupid and romantic, then i don’t care.”

> we’ve been together forever, and what if it takes us years?”

> i’ll do that,” he said softly, “we’ve got a date.”

> *(CELL_C, tertile=begin)* And if we do go out, then I have to deal with all the men swarming around wanting a taste of your sex magic! ”

> *(CELL_C, tertile=begin)* Or was it just an accident that we dated and he found the schema?”

> *(CELL_C, tertile=end)* This is something with pure intentions, open emotions, and a reciprocation that will never cause harm to either of us.” “

> *(CELL_C, tertile=begin)* It’s just … I know I am nothing but a big disappointment to both of you.

### Pass A/B/C

- **A lexical:** `H2`
  - All four representers converge on H2. The topic centers on active, mutual, ongoing dating with shared identity markers ('we', 'together', 'partners'). 'Officially', 'engaged', 'longest', and 'intend' across KeyBERT and MMR suggest a relationship moving toward or already at committed status. 'Failure' and 'forgetting' introduce reflective or conflictual texture but do not redirect the dominant signal away from an established or formalizing couple dynamic. No HEA payoff markers (proposal resolution, wedding, explicit forever-framing) are present, confirming H2 rather than H3.
- **B contextual:** `H2_ESTABLISHED_TOGETHERNESS`
  - Across all four books the dominant signal is established or developing togetherness, but the corpus is saturated with barriers: a stated breakup (BOOK_003), an unexplained rupture (BOOK_006), self-doubt (BOOK_004_4), and jealousy/conflict (BOOK_003_5). Future-oriented language exists in end-tertile positions (BOOK_003_3, BOOK_004_3) but remains conditional or aspirational rather than declarative. Mutuality is clearest in BOOK_004 but even there the excerpt is a statement of intent, not a confirmed relational resolution. HEA criteria — settled union, resolved rupture, forward-committed payoff — are not met by any excerpt individually or collectively.
- **C adjudicate:** `HEA_CONFIRMED`
- **Action:** PASS_C

---

## Topic 128 — Confessing How Much You've Missed

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** UNKNOWN

> i’ve missed most of his life already.

> and, god, how i’ve missed this.”

> i’ve come to realize that you are the one thing in my life i don’t want to miss.

> *(CELL_B, tertile=middle)* I’d missed my family so much, and now that we’d seemed to get the tears and heartache out of the way, we were having fun. “

### Pass A/B/C

- **A lexical:** `H2`
  - All four representers converge on H2. The topic is saturated with longing and mutual missing, set in a high-tension confined-space moment (elevator), with emotional weight markers (solemnly, breathlessly, precious, pieces) and deliberation signals (considering, thoughtfully, opportunity) that confirm mid-narrative yearning. No HEA payoff markers—no commitment, union, or resolution language—are present anywhere in the lexical set. Confession/missing-you alone does not qualify as HEA per audit rules.
- **B contextual:** `H2_MISS_REUNION_ROMANTIC`
  - {'HEA_verdict': 'NO_CONFIRMED_HEA_IN_SAMPLE', 'explanation': "Per audit rules, 'I missed you' expressions — even mutual, even at end-tertile — do not constitute HEA or final relational payoff on their own. BOOK_004 comes closest: six romantic-miss sentences, four in the end tertile including pos=0.99, with explicit reciprocity ('not as much as I missed you'). This pattern is consistent with a reunion arc converging on resolution, but the captured sentences contain no commitment language, no explicit togetherness declaration, and no forward-facing relational security. BOOK_003 has a named romantic target (Avery) and an end-tertile miss at pos=0.93, but the surrounding sentences are family-reunion dominated, diluting romantic finality. BOOK_007 is a single mid-narrative miss with no payoff evidence. BOOK_002 and BOOK_006 contain only literal or non-romantic miss usages. BOOK_001 is a neutral absence statement. The dominant pattern across the topic is emotional reunion signaling — a necessary but not sufficient condition for HEA under the operative audit standard.", 'position_pattern': 'Romantic-miss sentences cluster in CELL_B books; end-tertile concentration in BOOK_004 is the strongest positional signal of narrative convergence. CELL_C and CELL_D books show non-romantic or ambiguous miss usage with no HEA-relevant positioning.', 'flag_for_full_text_review': ['BOOK_004', 'BOOK_003']}
- **C adjudicate:** `UNKNOWN`

---

## Topic 157 — Swearing to Save Him From Himself

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** HEA_CONDITIONAL_TRAJECTORY

> and you’ll get it, i swear,” [person].

> if [person] sees me like this, i'll die."

> and i might be young but i guess that just makes me lucky… i do love him and whether i have your help or not, i have to save him from himself… i know [person], i know what he’ll do, now that he thinks he has lost me.”

> *(CELL_B, tertile=middle)* Sam couldn’t understand it, and that bothered him.

> *(CELL_B, tertile=begin)* What else had Sam witnessed?

> *(CELL_B, tertile=begin)* Sam noticed stuff like that.

### Pass A/B/C

- **A lexical:** `H2`
  - All four representations converge on H2. KeyBERT and MMR both surface 'confessed' alongside tension markers (tense, gritted, begged, dump, worries), indicating a conflict/confession arc that is mid-story rather than resolved. POS adds desperation and dislike, reinforcing unresolved emotional stakes. Main keywords show optimism and enthusiasm but no HEA payoff language (no reunion, commitment, or relational resolution). Confession alone does not qualify as HEA per audit rules, so H2 is the correct placement.
- **B contextual:** `H2_NAME_INVOCATION`
  - Across all 21 sentences the signal is dominated by name-calling fragments and character-trait observations. The only relational action present is apology (BOOK_008), which per audit rules is explicitly excluded from HEA qualification without a paired acceptance/forgiveness beat. The highest-position fragment (BOOK_006_3, pos=0.97) offers an internal recognition moment but no couple-level commitment or togetherness declaration. Position patterns show high-probability scores cluster around name invocations rather than payoff language, suggesting the model is firing on character salience rather than romantic resolution content. Topic 157 does not meet HEA/HFN threshold.
- **C adjudicate:** `HEA_CONDITIONAL_TRAJECTORY`
- **Action:** H2_NAME_INVOCATION in the second tertile with primary taxonomy 4.5 confirms a named-character commitment anchor mid-narrative. Secondary 3.3 flags residual ambivalence still active at this position, meaning the HEA is asserted but not yet fully resolved. Confession, apology, or 'I missed you' framing must be ruled out as the sole payoff driver; the name invocation must carry forward-facing relational weight (promise, claim, or mutual re-anchoring) to qualify. If the invocation functions as a pivot that closes the ambivalence arc rather than merely acknowledging it, the HEA trajectory is intact.

---

## Topic 167 — Planning A Wedding Reception

- **Taxonomy:** 5.3a — Romantic Social Rituals & Public Couple Recognition
- **Code:** HEA_PUBLIC_UNION
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

- **A lexical:** `H2`
  - All four representations converge on H2. The lexical field is dominated by wedding-event vocabulary (wedding, bride, groom, bridal, ceremony, bridesmaids, reception, invitation, destination, planning, preparing, arranged). This signals a wedding-planning or wedding-day context situated in the middle tertile of a romance narrative — the relational payoff is being set up or enacted but the story has not yet closed. No HEA/HFN terminus is confirmed by the lexicon alone; the wedding machinery is present but 'jitters' and preparatory terms (planning, preparing, arrange) suggest the event is imminent or in-progress rather than concluded and settled. H2 is the appropriate code: the romantic arc is advancing toward commitment but the final relational resolution has not been delivered.
- **B contextual:** `H2_WEDDING_CEREMONY`
  - All 20 sentences cluster tightly in the middle tertile (pos 0.41–0.45), forming a dense wedding-scene block. The ceremony proceeds (vows, kiss, reception) but interiority passages reveal the bride's ambivalence, the rushed/unconventional nature of the arrangement, and a 'sealed bargain' framing suggesting a marriage-of-convenience setup. Community acceptance (BOOK_001_19) and post-ceremony reception (BOOK_001_14) confirm the union is completed, but the emotional HEA resolution—genuine mutual love, not just legal marriage—almost certainly lies in the latter tertile of the book. Per audit rules, ceremony completion mid-book is a structural milestone, not a final relational payoff.
- **C adjudicate:** `HEA_PUBLIC_UNION`
  - H2_WEDDING_CEREMONY is a structurally definitive public couple-recognition event. Under 5.3a, a wedding ceremony constitutes the canonical HEA anchor: it is a socially ratified, witnessed, forward-looking commitment that exceeds confession, apology, forgiveness, or reunion affect alone. The secondary taxonomy 5.1 reinforces kinship formation (new family unit created), which corroborates rather than displaces the romantic payoff. No disqualifying signals present. HEA confirmed.
- **Action:** CONFIRM_HEA

---

## Topic 204 — Promising to Care For Her Sister

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** CONDITIONAL_HEA — qualifies under 4.5 only if romantic commitment is narratively terminal and structurally independent of the 5.1 sibling-concern arc; if romantic resolution is contingent on or conflated with sibling repair, reclassify primary to 5.1 and downgrade 4.5 to secondary with HEA_UNCONFIRMED status.

> i’ll need to finish dressing and leave a note for my sister.”

> yes, and soon you’ll be my sister.

> i’ll find a way to care for your mother and your sister.” “

> *(CELL_D, tertile=middle)* My sister’s still there with her husband, who’s a copper, and their three kids.

> *(CELL_A, tertile=begin)* You have not been paying close attention to your sister’s problems lately, have you?” “

> *(CELL_A, tertile=begin)* Your sister mentioned in passing that you are something of a recluse.” “

> *(CELL_A, tertile=end)* You mock your sister, but you will admit that she has great talents.” “

> *(CELL_A, tertile=end)* I realize that you are concerned for your sister’s happiness.

### Pass A/B/C

- **A lexical:** `H1`
  - Topic 204 centers on sisterly/sibling relational content with affection markers, but the surrounding lexical field (introduce, direct, permission, willing, expect, speaking, assume) frames the scene as negotiation, facilitation, or early contact rather than HEA resolution. Affection is present but not consummated as a final relational payoff. H1 — relational content without HEA — is the consensus across three of four reps, with Main as the sole H2 outlier driven by surface sibling-label density rather than payoff structure.
- **B contextual:** `H2_SIBLING_CONCERN`
  - Topic 204 is saturated with sibling references functioning as (a) character background (BOOK_003_1, BOOK_004_1), (b) plot obstacles or protective imperatives (BOOK_006_3, BOOK_006_5, BOOK_006_6, BOOK_007_5), (c) relational context that defines the protagonist's social world (BOOK_005 cluster), and (d) anticipatory signals of romantic resolution via the sister-in-law trope (BOOK_007_1). Across all three books the sister is a narrative instrument rather than a romantic subject. Position analysis shows end-tertile sentences do not escalate toward HEA language; they sustain sibling-obligation tension or offer mild gratitude. No mutuality, no couple-level commitment, no forward romantic pledge is present. The topic does not meet HEA or HFU criteria.
- **C adjudicate:** `CONDITIONAL_HEA — qualifies under 4.5 only if romantic commitment is narratively terminal and structurally independent of the 5.1 sibling-concern arc; if romantic resolution is contingent on or conflated with sibling repair, reclassify primary to 5.1 and downgrade 4.5 to secondary with HEA_UNCONFIRMED status.`
- **Action:** EVALUATE_HEA_VALIDITY

---

## Topic 242 — Trading Forgiveness For Old Wrongs

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** UNKNOWN

> not if you’ll forgive him.” “

> he’ll never forgive you.

> okay, how’s this — i’ll forgive you for summer if you forgive me for kabir.” “

> *(CELL_B, tertile=begin)* Any man delivering such a speech to the lady he had planned to marry—a lady who had waited faithfully for him—should have had the grace to appear remorseful, or at least apologetic.

### Pass A/B/C

- **A lexical:** `H2`
  - All four representations converge unambiguously on H2. The lexicon is saturated with forgiveness-seeking, wrongdoing acknowledgment, and emotional repair vocabulary (forgive, apology, fault, spite, harshly, hurts, treatment, actions). Per audit rules, confession, apology, and forgiveness alone do not constitute HEA or a final relational payoff. No union, reunion, love-declaration, or commitment language is present across any representation.
- **B contextual:** `H2_forgiveness_process_and_granting`
  - Topic 242 is saturated with forgiveness vocabulary across multiple books and tertile positions, but the construct maps entirely onto the forgiveness-as-process dimension rather than forgiveness-as-gateway-to-reunion. The highest-probability sentences (BOOK_001 cluster, p ≈ 0.77–0.79) are end-positioned and forgiveness-granting, yet none attach to a confirmed couple reunion or future commitment. BOOK_004 comes closest with an internal forgiveness arc and a hope-inflected apology, but BOOK_004_5 undercuts this by framing the outcome as loss ('let someone I love slip away'). BOOK_003 shows social/courtesy forgiveness unrelated to romantic resolution. BOOK_002 and BOOK_006 involve third-party or self-directed doubt. Mutuality is absent throughout; future orientation is speculative at best. HEA/final relational payoff: NOT PRESENT.
- **C adjudicate:** `UNKNOWN`

---

## Topic 305 — Confessing A Lifelong Regret

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** UNKNOWN

> i know that now, and i’ll go to my grave regretting what i did to you.” “

> come on in, you’ll no doubt regret it.

> you’ll regret that.’ ‘

> *(CELL_B, tertile=middle)* You are surely not intending to imply that you are beginning to regret this marriage already?’ ‘

> *(CELL_B, tertile=end)* I fear that my careless remarks must have been the cause of that outburst.

### Pass A/B/C

- **A lexical:** `H2`
  - All four representations converge on H2. The lexical field is dominated by regret morphology, fear, poor handling of a decision, and instability — consistent with mid-narrative emotional conflict or a mistake being processed. No HEA markers (commitment, reunion, mutual declaration, relational resolution) appear in any representation. Confession or regret alone does not qualify as HEA per audit rules.
- **B contextual:** `H2_REGRET_PRESENT_ACTIVE`
  - Topic 305 is saturated with regret as an active, unresolved emotional state. Across all four books the dominant pattern is characters experiencing, expressing, contesting, or guarding against regret—none of which resolves into mutual commitment or forward-facing relational security. Position analysis reinforces this: the latest-positioned fragments (0.78–0.86) remain in conflict, deflection, or self-interrogation. The one denial of regret (BOOK_002_2, pos=0.02) is early and isolated. The one promise of no future regret (BOOK_003_1) is mid-story and unverified. No HEA or HFN signal is detectable.
- **C adjudicate:** `UNKNOWN`

---
