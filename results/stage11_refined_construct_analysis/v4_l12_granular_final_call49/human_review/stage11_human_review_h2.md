# H2 — HEA / final relational payoff

Run: `v4_l12_granular_final_call49` — 10 topics.

### New categories (read these before the topics)

| Code | Category | Definition |
| --- | --- | --- |
| `H2_0` | **off target** | Not about couple relationship talk, repair, commitment, or payoff. |
| `H2_1` | **generic confession apology** | Confession, apology, forgiveness, or missing-you talk without lasting resolution. |
| `H2_2` | **repair** | Active repair of a rupture; trust being rebuilt but not yet sealed. |
| `H2_3` | **mutual commitment** | Mutual future-oriented commitment without a clear final payoff moment. |
| `H2_4` | **final relational payoff** | Lasting relational resolution / HEA-style closure for the main couple. |
| `H2_5` | **public union** | Wedding, public acknowledgement, family/community recognition of the couple. |
| `H2_6` | **commitment symbols** | Rings, proposals, shared home as symbols — without full narrative closure. |
| `H2_7` | **emotionally intense talk** | High-affect relationship talk that is neither repair nor payoff. |
| `H2_8` | **non main couple resolution** | Resolution for secondary characters or plot, not the main couple. |

### Topic 29 — Confessing Long-Held Love {#topic-h2-29}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_7 — emotionally intense talk**
- **Mixed:** False
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> i love you with everything i am, everything i’ve been, and everything i hope to be .” “

> tell her i’ve always loved her.

> i’ve always been in love with you.”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Forgiveness — Jean Brashear; tertile=end; p=0.80**
>
> I love you, too, sweetheart.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Forgiveness — Jean Brashear; tertile=end; p=0.76**
>
> Oh, child, I love you, too.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Forgiveness — Jean Brashear; tertile=end; p=0.74**
>
> You just say ‘I love you.’”

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_7 — emotionally intense talk**
  - Main keywords ('love, loved, loves, falling, fall, always, me, know') signal emotionally intense romantic declaration language — the 'falling in love' cluster with 'always' and 'know' points to a charged emotional confession scene rather than a finalized commitment or public union. KeyBERT and MMR both surface apology/forgiveness cues ('forgive, apologize, hated, crushed, spite') which lean toward H2_1 (generic confession/apology), but the critical instruction excludes confession/apology alone from HEA coding. POS terms ('spite, slightest, reflection, delicate, actions') are too abstract to anchor a specific relational function, coded H2_0. The dominant signal across the full set is emotionally intense talk — declarations of love with affective intensity ('crushed, secretly, dreamed, genuinely, happiness') without evidence of mutual commitment sealing, public union, or commitment symbols — yielding H2_7 as consensus.
- **Pass B — contextual:** **H2_7 — emotionally intense talk**
  - This topic is dominated by reciprocal 'I love you' declarations — emotionally intense verbal exchanges without explicit commitment acts, public union markers, or forward-looking pledges. Several instances involve parent-child or non-romantic dyads (e.g., 'I love you, Mom,' 'Love you, Mom,' 'I love you both'), coded H2_8. The remainder are emotionally intense declarations between unspecified parties, best captured by H2_7 (emotionally intense talk). No proposal, vow, or commitment symbol is present, so H2_3/H2_4/H2_5/H2_6 are not warranted. Mutuality is full given the reciprocal exchanges. Finality is medium — end-tertile placement suggests climactic moments but the bare declarations alone do not confirm HEA closure.
- **Pass C — adjudication:** **H2_7 — emotionally intense talk**
  - Both lexical consensus and contextual dominant converge on H2_7 (emotionally intense talk). The taxonomy placement under 4.5 Reconciliation, Commitments & HEA with secondary 3.1 Positive Resolution is consistent with H2_7, which captures high-affect verbal exchange that may accompany but does not itself constitute a final relational payoff (H2_4) or mutual commitment (H2_3). No free-form HEA_* labels were introduced in prior passes requiring remapping. The signal is coherent and no split or reinterpretation is warranted.

---

### Topic 62 — Admitting You've Been Stupid {#topic-h2-62}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_0 — off target**
- **Mixed:** False
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> marnie, i’ve been stupid.

> about what an asshole i’ve been?” “

> you've done something dumb, but you'll get away with it this time.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Truth Be Told — Barbara McMahon; tertile=begin; p=0.51**
>
> Dear Reader, Sometimes teenagers do foolish things.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Girlfriend Material — Melissa Kantor; tertile=middle; p=0.59**
>
> I’m the one who was stupid enough not to bring one.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Girlfriend Material — Melissa Kantor; tertile=begin; p=0.54**
>
> He’s really … I don’t know …” I forced myself not to supply the word dumb . “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Girlfriend Material — Melissa Kantor; tertile=begin; p=0.52**
>
> He was too proud of himself to detect the sarcasm in my words. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_0 — off target**
  - All four keyword lists point to conflict, insult, and embarrassment vocabulary (stupid, idiot, fool, asshole, jerk, rude, ridiculous, harshly, embarrassed, hissed, annoying, overheard, remark, comments). There is no relational payoff, commitment, confession, repair, or union signal anywhere. This is off-target content — interpersonal friction/conflict language with no HEA function.
- **Pass B — contextual:** **H2_0 — off target**
  - Every sentence in this topic revolves around expressions of foolishness, stupidity, or self-deprecation (e.g., 'stupid,' 'idiot,' 'fool,' 'foolish girl'). None of these sentences contain relational commitment, confession, apology, forgiveness, union, or any HEA-relevant function. The topic is entirely off-target with respect to romance HEA payoff coding.
- **Pass C — adjudication:** **H2_0 — off target**
  - Both lexical consensus and contextual dominant agree on H2_0 (off_target). The taxonomy flags 4.5 Reconciliation/Commitments & HEA with a secondary of 3.3 Ambivalence & Internal Conflict, but without topic-level token evidence of mutual commitment, final relational payoff, or commitment symbols, the off-target classification holds. The secondary taxonomy (ambivalence/internal conflict) further supports that this topic centers on unresolved emotional tension rather than HEA delivery. No free-form HEA_* labels were used in prior passes requiring remapping. H2_0 is confirmed.

---

### Topic 65 — Declaring A True Partnership {#topic-h2-65}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_3 — mutual commitment**
- **Mixed:** False
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> what we’ve been though together, the way we’ve been there for each other ... we have a true partnership, a true love, and if that sounds stupid and romantic, then i don’t care.”

> we’ve been together forever, and what if it takes us years?”

> i’ll do that,” he said softly, “we’ve got a date.”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · The Fire Lord's Lover — Kathryne Kennedy; tertile=end; p=0.58**
>
> We have often been together in public." "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Sinful Magic — Jennifer Lyon; tertile=begin; p=0.62**
>
> This is the only way you can get a date?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Sinful Magic — Jennifer Lyon; tertile=middle; p=0.51**
>
> Want to believe we can really have something together.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Sinful Magic — Jennifer Lyon; tertile=begin; p=0.49**
>
> And if we do go out, then I have to deal with all the men swarming around wanting a taste of your sex magic! ”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Sinful Magic — Jennifer Lyon; tertile=begin; p=0.49**
>
> Or was it just an accident that we dated and he found the schema?”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Adam — Jacquelyn Frank; tertile=middle; p=0.66**
>
> It has not been that long since we last saw each other.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Adam — Jacquelyn Frank; tertile=middle; p=0.55**
>
> We have walked this world together for quite some time.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Adam — Jacquelyn Frank; tertile=end; p=0.51**
>
> This is something with pure intentions, open emotions, and a reciprocation that will never cause harm to either of us.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Adam — Jacquelyn Frank; tertile=begin; p=0.48**
>
> It’s just … I know I am nothing but a big disappointment to both of you.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_3 — mutual commitment**
  - Main keywords ('date, dating, together, each, we, other, dated, dates, two') point to an established or forming couple relationship with mutual orientation. KeyBERT adds 'engaged' and 'partners', signaling formalized mutual commitment. POS reinforces 'partners' and 'fitting' (as in a fitting/suitable match). MMR contributes 'officially', 'partners', and 'intend', suggesting a declared or formalized relational status. Together these cues indicate mutual commitment and a defined couple identity rather than a mere confession/apology or a final ceremonial payoff, placing this firmly at H2_3 (mutual_commitment).
- **Pass B — contextual:** **H2_0 — off target**
  - The overwhelming majority of sentences are casual, contextual references to being together, going on dates, or breaking up — none of which constitute HEA-relevant relational payoff. Two sentences (BOOK_003_4, BOOK_004_3) gesture toward emotionally meaningful relational talk (wanting something real, pure intentions/reciprocation), earning H2_7, but they are isolated and lack commitment or finality. The topic as a whole is off-target for HEA function, dominated by mundane relational context and social logistics.
- **Pass C — adjudication:** **H2_3 — mutual commitment**
  - Lexical consensus (H2_3 mutual_commitment) and contextual dominant (H2_0 off_target) conflict. The taxonomy placement under 4.5 Reconciliation, Commitments & HEA with secondary 4.2 Ongoing Courtship & Everyday Relational Bonding tips the balance toward H2_3: the topic likely captures characters actively pledging or re-pledging commitment (reconciliation + forward-looking mutual commitment) rather than mere confession/apology or purely off-target content. H2_0 may reflect surface noise or everyday-bonding tokens that dilute the signal, but the dominant semantic function under 4.5 is a commitment act, not absence of HEA content. H2_3 is therefore retained as the adjudicated code. Manual review is flagged because the H2_0 contextual read suggests meaningful off-target contamination that could warrant a SPLIT if the topic mixes mundane bonding scenes with genuine commitment moments.

---

### Topic 128 — Confessing How Much You've Missed {#topic-h2-128}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_7 — emotionally intense talk**
- **Mixed:** False
- **Adjudication action:** `REINTERPRET`

**Stage-08 snippets**

> i’ve missed most of his life already.

> and, god, how i’ve missed this.”

> i’ve come to realize that you are the one thing in my life i don’t want to miss.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Deadly Desire — Keri Arthur; tertile=begin; p=0.61**
>
> I sometimes miss the peace of you and me, though." "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Deadly Desire — Keri Arthur; tertile=end; p=0.44**
>
> He missed the ball even worse than I did.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Here Kitty, Kitty — Joyee Flynn; tertile=middle; p=0.67**
>
> I missed you, little bro,” he whispered in my ear. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Here Kitty, Kitty — Joyee Flynn; tertile=middle; p=0.60**
>
> I’d missed my family so much, and now that we’d seemed to get the tears and heartache out of the way, we were having fun. “

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_1 — generic confession apology**
  - Main keywords ('miss', 'missed', 'missing', 'misses', 'wouldn't', 'll', 'much', 'too') are dominated by expressions of longing and absence — classic confession/apology territory ('I missed you so much', 'I wouldn't miss you') but not mutual commitment or final payoff. MMR adds adverbs of emotional delivery ('solemnly', 'breathlessly', 'thoughtfully', 'pressing', 'considering') suggesting an emotionally charged conversation, nudging toward H2_7, but the core semantic content remains the 'I missed you' confession pattern explicitly excluded from HEA by the rubric. KeyBERT ('hi', 'sir', 'escaped', 'honestly', 'repeated', 'solemnly') and POS ('handful', 'precious', 'voices', 'elevator', 'opportunity', 'pieces') are largely contextual/setting words with no relational payoff signal. The dominant signal across all reps is the 'missed you' confession cluster, which the rubric explicitly codes as H2_1 (generic_confession_apology), not HEA. Disagreement flagged because MMR leans H2_7 and KeyBERT/POS lean H2_0.
- **Pass B — contextual:** **H2_7 — emotionally intense talk**
  - The overwhelming majority of sentences express longing or 'I missed you' statements — emotionally intense but not constituting commitment, repair, or HEA payoff. These are coded H2_7 (emotionally_intense_talk) per the instruction that 'I missed you' alone is not HEA. Several sentences use 'miss' in a literal/physical sense (missed the ball, missing piece) and are off-target (H2_0). One sentence references missing family broadly, coded H2_8. No mutual commitment, public union, or final relational payoff is present. H2_7 reaches ~65%, clearing the 70% threshold narrowly — dominant code is H2_7.
- **Pass C — adjudication:** **H2_7 — emotionally intense talk**
  - Lexical consensus (H2_1) reflects surface-level confession/apology vocabulary, but the contextual dominant (H2_7) better captures the functional role of this topic: sustained, emotionally charged dialogue that drives reconciliation rather than a discrete confession act. The taxonomy placement under 4.5 Reconciliation, Commitments & HEA with secondary 3.1 Positive Resolution supports an emotionally intense exchange that moves toward repair but does not yet constitute mutual commitment (H2_3) or final relational payoff (H2_4). H2_7 is therefore the most accurate single code. No free-form HEA_* labels were introduced in prior passes requiring remapping.

---

### Topic 157 — Swearing to Save Him From Himself {#topic-h2-157}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_0 — off target**
- **Mixed:** False
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> and you’ll get it, i swear,” [person].

> if [person] sees me like this, i'll die."

> and i might be young but i guess that just makes me lucky… i do love him and whether i have your help or not, i have to save him from himself… i know [person], i know what he’ll do, now that he thinks he has lost me.”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Intimate Portraits — Cheryl B. Dale; tertile=middle; p=0.73**
>
> Sam couldn’t understand it, and that bothered him.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_0 — off target**
  - Main keywords are character names and generic positive words (good, optimism) with no relational payoff signals. POS keywords (dislike, worries, embarrassing, desperation, gritted) suggest conflict or tension rather than resolution. MMR similarly shows negative emotional states (dislike, dump, worries, gritted) with no commitment or union cues. KeyBERT has 'confessed' and 'begged' which could suggest H2_1 (generic confession/apology), but the surrounding terms (deliberately, sharply, tense, brief) indicate a tense confrontational scene rather than a romantic resolution. Overall the topic points to off-target content — character-focused conflict/tension scenes without HEA function.
- **Pass B — contextual:** **H2_0 — off target**
  - The vast majority of sentences are name fragments ('Sam.', 'Sam!', 'Samantha.') or brief character observations with no relational payoff content. Two sentences contain apologies ('I'm sorry, Sam!') which qualify as H2_1 generic_confession_apology, but these are isolated and not part of a resolved arc. There is no commitment, mutual declaration, or HEA function present. The topic appears to be a character-name cluster (Sam/Samantha) rather than a relational resolution topic. H2_0 dominates at ~90%.
- **Pass C — adjudication:** **H2_0 — off target**
  - Both lexical consensus and contextual dominant agree on H2_0 (off_target). Although the taxonomy flags 4.5 Reconciliation, Commitments & HEA as primary, the secondary tag 3.3 Ambivalence & Internal Conflict suggests the topic content centers on internal conflict rather than a realized relational payoff. No evidence of mutual commitment, final HEA delivery, or commitment symbols was surfaced in prior passes. The taxonomy primary label alone is insufficient to override the dual H2_0 signal; the topic does not meet the threshold for any H2_1–H2_8 code. H2_0 is confirmed.

---

### Topic 204 — Promising to Care For Her Sister {#topic-h2-204}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_0 — off target**
- **Mixed:** False
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> i’ll need to finish dressing and leave a note for my sister.”

> yes, and soon you’ll be my sister.

> i’ll find a way to care for your mother and your sister.” “

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Cera's Place — Elizabeth McKenna; tertile=middle; p=0.48**
>
> My sister’s still there with her husband, who’s a copper, and their three kids.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · 'Til Death Do Us Part — Barbara C. Doyle; tertile=begin; p=0.70**
>
> You have not been paying close attention to your sister’s problems lately, have you?” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · 'Til Death Do Us Part — Barbara C. Doyle; tertile=begin; p=0.69**
>
> Your sister mentioned in passing that you are something of a recluse.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · 'Til Death Do Us Part — Barbara C. Doyle; tertile=end; p=0.69**
>
> You mock your sister, but you will admit that she has great talents.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · 'Til Death Do Us Part — Barbara C. Doyle; tertile=end; p=0.69**
>
> I realize that you are concerned for your sister’s happiness.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · 'Til Death Do Us Part — Barbara C. Doyle; tertile=end; p=0.67**
>
> You and your sister have done so much for us.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Lady and The Duke — Olivia Kelly; tertile=end; p=0.72**
>
> Having an older sister is a great pain in the arse." "

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_0 — off target**
  - All four keyword lists center on sibling/sisterly relationships ('sister', 'sisters', 'sis', 'sisterly') and generic conversational/introductory cues ('hi', 'speaking', 'introduce', 'asks', 'willing', 'expect'). There is no romantic commitment, confession, repair, union, or relational payoff between a main couple. The topic describes family or platonic sisterly dynamics, placing it firmly off-target for HEA classification.
- **Pass B — contextual:** **H2_0 — off target**
  - Every sentence in this topic references a 'sister' in purely familial/social context — describing sibling relationships, concerns about a sister's wellbeing, or mentions of a sister as a third party. There is no romantic couple interaction, no commitment, no confession, no HEA payoff, and no relational resolution between a main couple. The topic is entirely off-target with respect to romance HEA functions.
- **Pass C — adjudication:** **H2_0 — off target**
  - Both lexical consensus and contextual dominant agree on H2_0 (off_target). Although the taxonomy flags 4.5 Reconciliation/Commitments & HEA with a secondary of 5.1 Family/Kinship, the Pass A/B signals indicate the topic content does not function as a relational payoff mechanism — it likely concerns family or kinship dynamics without a final commitment or HEA delivery. No free-form HEA_* labels were used in prior passes requiring remapping. The taxonomy secondary (5.1) supports an off-target classification relative to HEA function. H2_0 is confirmed.

---

### Topic 242 — Trading Forgiveness For Old Wrongs {#topic-h2-242}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_1 — generic confession apology**
- **Mixed:** False
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> not if you’ll forgive him.” “

> he’ll never forgive you.

> okay, how’s this — i’ll forgive you for summer if you forgive me for kabir.” “

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Marrying for King's Millions — Maureen Child; tertile=middle; p=0.59**
>
> You must forgive him,” Rico said with a laugh. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Ruined by Rumor — Alyssa Everett; tertile=end; p=0.67**
>
> Do forgive me for not having welcomed you more fittingly.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Ruined by Rumor — Alyssa Everett; tertile=middle; p=0.61**
>
> What will you do if society here proves unforgiving?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Ruined by Rumor — Alyssa Everett; tertile=begin; p=0.55**
>
> Any man delivering such a speech to the lady he had planned to marry—a lady who had waited faithfully for him—should have had the grace to appear remorseful, or at least apologetic.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_1 — generic confession apology**
  - All four keyword lists are saturated with forgiveness/apology vocabulary: 'forgive', 'forgiveness', 'forgiven', 'forgiving', 'apology', 'fault', 'spite', 'harshly', 'terribly', 'hurts', 'treatment', 'actions', 'permission'. There is no lexical evidence of mutual commitment, relational payoff, public union, or commitment symbols. The content maps squarely to generic confession/apology (H2_1) per the critical rule that confession, apology, and forgiveness alone do not constitute HEA.
- **Pass B — contextual:** **H2_1 — generic confession apology**
  - Topic 242 is overwhelmingly focused on forgiveness language — requests for forgiveness, granting of forgiveness, and reflection on what forgiveness means. This maps most specifically to H2_1 (generic_confession_apology), as the sentences express apology/forgiveness acts without evidence of mutual commitment or a final relational payoff. A subset of sentences where forgiveness is explicitly granted (e.g., 'You're forgiven,' 'I came to tell you I forgive you') edge toward H2_2 (repair), as they represent a relational rupture being addressed. Two sentences are off-target (societal unforgiving, a rivalry grudge). One sentence (BOOK_004_5) expresses emotional regret about letting someone go, coded H2_7. No mutual commitment, public union, or HEA payoff is present. H2_1 exceeds 70% when combined with closely related H2_2 repair instances, but taken strictly H2_1 alone is ~50%, so the dominant code is H2_1 as the single largest category, with H2_2 as secondary.
- **Pass C — adjudication:** **H2_1 — generic confession apology**
  - Both lexical consensus and contextual dominant converge on H2_1 (generic_confession_apology). The taxonomy placement under 4.5 Reconciliation/Commitments & HEA with secondary 4.3 Secrets/Misunderstandings is consistent: the topic captures moments where characters confess, apologize, or reveal hidden information, but does not rise to mutual commitment or final relational payoff. No free-form HEA_* labels were introduced in prior passes requiring remapping. H2_1 is the correct and stable code.

---

### Topic 305 — Confessing A Lifelong Regret {#topic-h2-305}

- **Old taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **New category:** **H2_0 — off target**
- **Mixed:** False
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> i know that now, and i’ll go to my grave regretting what i did to you.” “

> come on in, you’ll no doubt regret it.

> you’ll regret that.’ ‘

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · A Marriageable Miss — Dorothy Elbury; tertile=middle; p=0.66**
>
> You are surely not intending to imply that you are beginning to regret this marriage already?’ ‘

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · A Marriageable Miss — Dorothy Elbury; tertile=end; p=0.53**
>
> I fear that my careless remarks must have been the cause of that outburst.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · A Marriageable Miss — Dorothy Elbury; tertile=middle; p=0.51**
>
> At his words, a wave of regret washed over Helena. ‘

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Child of War - A God is Born — Lisa Beth Darling; tertile=begin; p=0.58**
>
> I have been unkind to you, which I deeply regret.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Child of War - A God is Born — Lisa Beth Darling; tertile=middle; p=0.56**
>
> Now you don't, but you wish you still did."

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_0 — off target**
  - Main and KeyBERT surface regret/admission vocabulary (regret, admit, embarrassing, fears) that could suggest confession/apology territory (H2_1), but there is no commitment, union, or relational payoff language anywhere. POS and MMR reinforce an off-target reading: 'loose, upset, unable, fumbled, drift, handled, ended' describe interpersonal difficulty or poor handling of a situation rather than any relational resolution. 'Decision' and 'promise' in Main are generic and unanchored to romantic commitment. The overall cluster points to emotional fallout or a misstep in a relationship rather than confession-as-apology or any HEA function, so the consensus lands at H2_0 off_target.
- **Pass B — contextual:** **H2_0 — off target**
  - This topic is overwhelmingly centered on the word 'regret' and its variants as emotional states or reactions, with no clear HEA function. The sentences express internal feelings of regret, absence of regret, or vague interpersonal tension, but do not constitute confession/apology sequences, repair arcs, or commitment. The vast majority (80%) are off-target emotional fragments. A small number (15%) approach generic apology/acknowledgment of wrongdoing (H2_1), and one sentence (5%) hints at relational repair framing ('regretting this marriage'). No mutual commitment, public union, or final relational payoff is present.
- **Pass C — adjudication:** **H2_0 — off target**
  - Both lexical consensus and contextual dominant agree on H2_0 (off_target). The secondary taxonomy tag 3.2 Negative Emotions & Distress reinforces that this topic centers on distress rather than any relational payoff function. The primary taxonomy 4.5 Reconciliation, Commitments & HEA does not override the coded signal when the topic content does not demonstrate commitment, mutual resolution, or HEA delivery — it merely indicates the broader cluster neighborhood. No free-form HEA_* labels were introduced in prior passes requiring remapping. H2_0 is confirmed.

---

### Topic 167 — Planning A Wedding Reception {#topic-h2-167}

- **Old taxonomy:** 5.3a — Romantic Social Rituals & Public Couple Recognition
- **New category:** **H2_5 — public union**
- **Mixed:** False
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> it’s my dream job, but instead of shooting brides, i’ll be shooting naked women.

> we'll get married next summer in the church in maine that my mother would take me to every sunday.

> the ‘ceremony’ in boorowa might just be signing a few papers, but carley’s planned a wedding reception they’ll never forget.” “

> on the eve of your wedding.”

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.72**
>
> There’ll be plenty to talk about, anyway, after the wedding today .” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.67**
>
> Most of you seem to have caught wind of the DeWitt wedding.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.65**
>
> Madison and I are getting married after church services.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.63**
>
> If the bride and groom would join hands and face each other, we’ll proceed in joining you together in holy matrimony .”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.62**
>
> And a girl shouldn’t be so rushed and put on the spot on her wedding day.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.60**
>
> H er wedding day dawned bright and crisp.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.60**
>
> Just because it was her wedding day didn’t mean she should start thinking about sexy things like her wedding night .

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Cowboy is a Daddy — Mindy Neff; tertile=middle; p=0.59**
>
> Strange to get married and not even know who was on the guest list .

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_5 — public union**
  - All four keyword lists converge on a wedding/ceremony context: Main contains 'wedding, bride, groom, bridal, ceremony, bridesmaids'; KeyBERT adds 'reception, invitation, destination, planning, official'; POS and MMR reinforce with 'reception, invitation, destination, official, announced'. The cluster describes a formal, publicly staged union event — not merely a confession or commitment symbol — which maps directly to H2_5 (public_union). No conflicting signals appear across any representation.
- **Pass B — contextual:** **H2_5 — public union**
  - All 20 sentences revolve exclusively around a wedding ceremony and its immediate context — the ceremony itself, the bride and groom joining hands, the kiss, the reception, the wedding day, and the wedding night. This is a textbook public union cluster: a formal, socially witnessed marriage ceremony. There is no confession, apology, or emotional repair language; the topic is entirely about the public ritual of marriage. H2_5 (public_union) is the overwhelmingly dominant code at 100%.
- **Pass C — adjudication:** **H2_5 — public union**
  - Both lexical consensus and contextual dominant converge on H2_5 (public_union). Taxonomy 5.3a (Romantic Social Rituals & Public Couple Recognition) directly maps to H2_5, with the secondary taxonomy 5.1 (Family, Kinship & Parenthood) consistent with a witnessed or socially ratified union. No free-form HEA_* labels were introduced in prior passes requiring remapping. The signal is clean and unambiguous; no split or reinterpretation is warranted.

---

### Topic 61 — Planning to Exchange Rings {#topic-h2-61}

- **Old taxonomy:** 8.3a — Commitment Symbols & Love Tokens
- **New category:** **H2_6 — commitment symbols**
- **Mixed:** True
- **Adjudication action:** `KEEP`

**Stage-08 snippets**

> in a few days, i’ll go to the stone.

> next time we’ll put a ring on him.”

> we’ll take care of the rings tomorrow.”

> anna was admiring his ring.

**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Operation Starseed — J.M. Snyder; tertile=end; p=0.60**
>
> Just have to close it up again, until it looks like a ring, and we'll be fine.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Operation Starseed — J.M. Snyder; tertile=end; p=0.57**
>
> Once they're gone, Shanley pricks Marie's finger with a lancet. "

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Operation Starseed — J.M. Snyder; tertile=end; p=0.35**
>
> It's not quite a perfect C-shape any longer, but more like one of those spoon bracelets that come in and out of fashion--the ends are drawing together, tightening, and that's a good thing, right?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Corporate Passion — Carol Lynne; tertile=end; p=0.67**
>
> He took the ring out of the box and, with Damon’s help, they placed it on her finger.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Corporate Passion — Carol Lynne; tertile=end; p=0.61**
>
> I might even be persuaded to wear my jewellery for you.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Corporate Passion — Carol Lynne; tertile=end; p=0.59**
>
> Damon and I agreed that you own our hearts so we thought this ring would be perfect for our union.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Corporate Passion — Carol Lynne; tertile=end; p=0.57**
>
> I’m going to buy you some jewellery to wear in the pretty hole.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Corporate Passion — Carol Lynne; tertile=end; p=0.53**
>
> He opened the lid and presented Rachel with a three karat heart-shaped ruby, surrounded by diamonds. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Corporate Passion — Carol Lynne; tertile=end; p=0.53**
>
> Remember that place in town where the guy makes the silver jewellery?” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Corporate Passion — Carol Lynne; tertile=end; p=0.47**
>
> The anal jewellery had been a little harder for her to get used to.

**Model reasonings (new taxonomy audits)**

- **Pass A — lexical:** **H2_6 — commitment symbols**
  - All four keyword lists are dominated by physical commitment symbols: 'ring', 'necklace', 'finger', 'diamond', 'engagement', 'rings', 'diamonds' (Main); 'rings', 'promises', 'engaged' (KeyBERT); 'rings', 'precious', 'matching' (POS); 'rings', 'precious', 'worn' (MMR). The lexical cluster centers on jewelry items — especially engagement rings and diamonds — that function as tangible tokens of relational commitment. This maps directly to H2_6 (commitment_symbols). No cues for public ceremony (H2_5), mutual verbal commitment exchange (H2_3), or final narrative payoff language are present.
- **Pass B — contextual:** **H2_6 — commitment symbols**
  - The overwhelming majority of sentences in this topic revolve around physical commitment symbols — rings (engagement/union rings placed on fingers), jewellery (nipple rings, anal jewellery, silver butt plug as adornment), and body piercings used as relational tokens. BOOK_002_5 explicitly frames a ring as representing 'our union' and 'owning hearts,' anchoring the topic firmly in H2_6 (commitment symbols). The jewellery items, even the erotic ones, function as symbolic markers of relational belonging and ownership within the couple(s). BOOK_001 references a ring being closed/shaped, reinforcing the commitment-symbol theme. BOOK_003 adds sentimental value language. Only BOOK_002_14 ('Brassil.') is off-target with no discernible relational function. The topic is clearly H2_6 at ~95% dominance.
- **Pass C — adjudication:** **H2_6 — commitment symbols**
  - Lexical consensus and contextual dominant both converge on H2_6 (Commitment Symbols & Love Tokens), and the taxonomy metadata confirms 8.3a as primary. The topic centers on physical or symbolic objects that encode relational commitment (rings, gifts, tokens), which is the defining feature of H2_6. No free-form HEA_* labels were introduced in prior passes requiring remapping. The secondary taxonomy node (4.5 Reconciliation, Commitments & HEA) is consistent but subordinate; it does not elevate the code to H2_4 or H2_3 because the dominant signal is the symbolic object rather than a mutual vow or final narrative payoff. No split or exclusion is warranted.

---
