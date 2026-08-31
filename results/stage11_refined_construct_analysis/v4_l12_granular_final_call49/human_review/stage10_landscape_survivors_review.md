# Landscape survivors review — |δ| ≥ 0.11 + CI excludes 0 (38 topics)

Run: `v4_l12_granular_final_call49` — 38 topics (33 more in high-rated, 5 more in low-rated; 3 unlabeled).

No LLM adjudication. Read evidence, then fill KEEP/DROP/FLAG.

```
Review notes (landscape survivors — effect-size gate)

1. These 38 topics are the only ones with |Cliff's delta| >= 0.11 and a
   bootstrap CI that excludes zero (high vs low rating tier).
2. Read keywords + sentences before trusting the Stage08 label. Three topics
   were never labeled (absent from topic_lookup / Stage08 JSON).
3. Unlabeled survivors (topic 8, 309, 310) were excluded upstream:
   - 8: Stage07 HARD_EXCLUDE publisher_boilerplate
   - 309 / 310: Stage07 soft_review tiny_topic; never routed to Stage08 label
4. Checklist: is the topic interpretable romance content, residual
   discourse/boilerplate, or mixed? Suggest a label if unlabeled.
```

## Unlabeled survivors (why blank in the notebook)

| Topic | Stage07 | Why no Stage08 label |
| --- | --- | --- |
| 8 | HARD_EXCLUDE `publisher_boilerplate` | Excluded before LLM labeling (EPUB copyright / buy-links) |
| 309 | soft_review `tiny_topic` | Soft-excluded; degenerate “she shook her head” cluster |
| 310 | soft_review `tiny_topic` | Soft-excluded; thin “hold / holding” cluster never labeled |

These three are among 25 topics absent from `topic_lookup.parquet` (348 labeled of 374 BERTopic topics), so `LABELS.get(...)` is NaN in `01_topic_landscape`.

## More in high-rated books (33)

### Topic 100 — Promising to Find Her

- **Label:** Promising to Find Her
- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Cliff's delta:** +0.2251 [+0.2034, +0.2449] — small — more in HIGH-rated
- **Mean share:** high 0.798% vs low 0.619% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 360 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** find, meet, needs, ll, see, leave, where, her, can, here
- **KeyBERT:** lingering, sir, thinks, replaced, mister, hiding, ok, urgency, dismissed, uh
- **POS:** urgency, excited, screen, decision, sir
- **MMR:** mister, urgency, dismissed, dealing, lingering, replaced, repeated, planning, screen, expect

**BERTopic representative docs**

> 1. i have a little girl who needs me." "

> 2. we're in the corner of the lot, shielded from the media by a van and a large pickup, but it's still just a matter of time until someone sees her and she gets swarmed.

> 3. if she gets sick or she needs anything…” “i know, d. i got her.”

**Stage-08 / Stage-07 snippets**

> 1. i promise, i’ll bring her right back.”

> 2. i’ll hurry and see if i can catch her.”

> 3. i’ll look until she’s found.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 16 examples from 4 books; ±1 context on 16_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Other packet sentences** (not tagged CELL_A–D)

> 1. [POS_001] I didn’t know I was lonely until I met her. [TARGET] I didn’t know I needed her, and here she is beside me. I glance at Ana, who’s sucking the tip of her index finger.

> 2. [POS_001] I’m going to do just that. [TARGET] Right now, I’m going to find her. Good to see you, Grandpa.” “

> 3. [POS_001] Perhaps you should have some more water,” I offer. [TARGET] Perhaps I should take her home. “ I’m fine.

> 4. [POS_001] We cleared the air. [TARGET] I’m not going to see her again.” Believe me, please.

> 5. [POS_001] Maybe it’s just one drink. “ [TARGET] Let me know when she leaves.” She said she would stay at home.

> 6. [POS_001] Give Ana our love. [TARGET] We’ll come see her tomorrow.” I call Carla to give her the good news. “

> 7. [POS_002] And the last time you two were in a room together, she had you at gunpoint. [TARGET] I don’t want her anywhere near you.” “ But, Christian, she was ill.” “

> 8. [POS_002] I must advise against it, ma’am.” “ [TARGET] She’s here to see me for a reason.” “ I’m supposed to prevent that, ma’am.”

> 9. [POS_002] Folding me into his embrace, he kisses my hair. “ [TARGET] What will you do when you find her?” I ask. “

> 10. [POS_003] And the last time you two were in a room together, she had you at gunpoint. [TARGET] I don’t want her anywhere near you.” “ But, Christian, she was ill.” “

> 11. [POS_003] I must advise against it, ma’am.” “ [TARGET] She’s here to see me for a reason.” “ I’m supposed to prevent that, ma’am.”

> 12. [POS_003] Folding me into his embrace, he kisses my hair. “ [TARGET] What will you do when you find her?” I ask. “

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 91 — Arguing Over Guns and Weapons

- **Label:** Arguing Over Guns and Weapons
- **Taxonomy:** 7.1 — Interpersonal Non-Romantic Conflict
- **Cliff's delta:** +0.1659 [+0.1455, +0.1879] — small — more in HIGH-rated
- **Mean share:** high 0.222% vs low 0.167% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 388 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** gun, shot, shoot, guns, shots, bullet, shooting, bullets, weapon, pistol
- **KeyBERT:** weapons, sir, fired, ought, pointing, aimed, practice, uh, squeeze, intend
- **POS:** weapons, behalf, activity, areas, percent, impressive, period, backs, task, members
- **MMR:** weapons, aimed, erupted, areas, guarantee, declared, arguing, grumbled, ought, cracked

**BERTopic representative docs**

> 1. the gun fired and exploded simultaneously.” “

> 2. and for all i know, j.t.’s gun held the bullet that killed him.” “

> 3. the bullet that killed the guy who fell from the tree and the bullet that killed brad were fired from the same gun.”

**Stage-08 / Stage-07 snippets**

> 1. i’ll be better armed as well.

> 2. i don’t like guns, they’re only for bad things, and all they do are hurt people, so i’ll thank you to get them away from me, now."

> 3. maybe i’ll get a shot with him next.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_thin cells CELL_D; 16 examples from 13 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Devil in Winter — Lisa Kleypas; tertile=end; p=0.62**
>
> We’ll have to offer an explanation of some kind.” “ [TARGET] Tell them someone was cleaning a gun, and it went off accidentally,” Sebastian said. “ Tell them no one was hurt.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Way of the Shadows — Cynthia Eden; tertile=middle; p=0.67**
>
> Yes, she’d been much better prey than he’d expected. “ [TARGET] This gun is for the ones coming to save you.” Because he wasn’t going out of this battle quietly.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Game of Fear — Robin Perini; tertile=begin; p=0.67**
>
> Panicked screams and cries of agony filled the night. [TARGET] Patrick homed in on where the shots had come from and ran that way, his gun at the ready. “ Gabe, get the girls inside and call 9-1-1.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Crossing the Line — Kimberly Kincaid; tertile=begin; p=0.59**
>
> Plus, it’s a pain in the ass to switch up lenses all the time, so I prefer to work with two cameras at once. [TARGET] That way I can go back and forth, depending on what the shot calls for.” “ You have two cameras?” “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Laird's Choice — Remmy Duchene; tertile=end; p=0.48**
>
> Race nodded. " [TARGET] Yeah, X had his team come after me because he was afraid someone else would get gun happy. We weren't best friends but we got along.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Stolen — Bec Botefuhr; tertile=begin; p=0.72**
>
> Well believe it because they were.” “ [TARGET] What about getting shot?” “ I paid him to shoot me.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · The Ninth Step — Barbara Taylor Sissel; tertile=begin; p=0.65**
>
> You wouldn’t keep a gun in the house, I guess. [TARGET] You wouldn’t shoot to kill if the bastards broke in. Well, maybe you’re right.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Held — Jessica Pine; tertile=middle; p=0.67**
>
> By the time I hear the click, it's too late. [TARGET] There’s a gun pointed at the back of my head. " Drive," she says. "

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Destiny Calls — Kathryn Heaney; tertile=begin; p=0.39**
>
> Your commercial is hot and provocative. [TARGET] I love the shot with the chains. How would you use those chains on me?” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · What The Heart Finds — Jessica Gadziala; tertile=middle; p=0.58**
>
> Lena walked over to the kitchen, finding not a simple drip coffee machine, but a drip machine on the side paired with an espresso machine and a frother. “ [TARGET] Do you want a shot in yours?” she asked, putting the coffee grounds into the machine and reaching for the bag of espresso beans. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Coast — Jay McLean; tertile=begin; p=0.40**
>
> Earlier, Dad bought five tubs of ice cream. [TARGET] We threw one against a brick wall, chucked one off a bridge, took a baseball bat to another, and then ran over one with the car. “ You know it’s your grams’s birthday in two weeks,” he said, watching me from across the kitchen table.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Scarred: A 3013 Novella — Susan  Hayes; tertile=middle; p=0.39**
>
> Sabar and I decided we knew better than our elders, and went too far into the jungle alone. [TARGET] We were attacked by a bortax . A nasty-tempered creature, and a fiercely territorial one.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Lyre — Helen Harper; tertile=middle; p=0.48**
>
> Things are going well so far. [TARGET] We’ve been in place for a while and taken a number of shots already. I want to wrap everything up in the next hour or so, before the light becomes too bright.’

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Lyre — Helen Harper; tertile=begin; p=0.56**
>
> Put your hand up!’ ‘ [TARGET] I’m saving my big guns for later,’ she responded. ‘ Against a freaking trip to Greece?’

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Lyre — Helen Harper; tertile=middle; p=0.59**
>
> She perched on the chair and hoped he wasn’t about to say what she thought he was. ‘ [TARGET] When’s the shoot?’ ‘ This afternoon.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Lyre — Helen Harper; tertile=begin; p=0.62**
>
> You are representing the school.’ [TARGET] A hand shot up. ‘ What is it, Garrett?’

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 78 — Swearing War Before He Takes Her

- **Label:** Swearing War Before He Takes Her
- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Cliff's delta:** +0.1650 [+0.1432, +0.1861] — small — more in HIGH-rated
- **Mean share:** high 0.262% vs low 0.209% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 425 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** fight, fighting, war, battle, fought, fights, fighter, win, battles, we
- **KeyBERT:** fought, attacked, weapons, guarded, surely, lets, warned, insisted
- **POS:** increase, accustomed, awhile, worries, edged, century, embarrassing, president, exciting, weapons
- **MMR:** attacked, increase, accustomed, erupted, worries, discussing, century, exciting, weapons, terms

**BERTopic representative docs**

> 1. and i might not fight back!

> 2. and the fight’s over anyway.

> 3. he’s not one to give up a fight, and he doesn’t have a pretty lass like you in his life to distract him from war.”

**Stage-08 / Stage-07 snippets**

> 1. i’ll fight you off.” “

> 2. and if they do, you’ll fight them.

> 3. i’ll start a war before i let him have you,” he murmured.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 16 examples from 4 books; ±1 context on 16_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Other packet sentences** (not tagged CELL_A–D)

> 1. [POS_001] Not my problem , he reminded himself. “ [TARGET] After everything you’ve been through you still want to fight? Are you so anxious to be imprisoned again?”

> 2. [POS_001] What he had to say affected them all. “ [TARGET] I warned you, I will not tolerate fighting.” He turned to the rest of them. “

> 3. [POS_001] And his liege lord is King Edward,” Boyd pointed out. “ [TARGET] So shouldn’t you be fighting for him?” Seton’s face flushed angrily. “

> 4. [POS_001] You expect me to believe that? [TARGET] With all the fighting you’ve done? It’s common for men to take their ‘spoils’ of war.” “

> 5. [POS_002] Come the fuck on, Vega. [TARGET] How am I ever going to win a fight with you if you just fucking die?” Nothing happened and it really did begin to look hopeless.

> 6. [POS_002] Jada’s smoky eyes narrowing and their furious argument— “—I don’t fucking have any, asshole! [TARGET] And even if I did, I wouldn’t give that shit to you—” The fighting. The guards.

> 7. [POS_002] He jerked at his arms and gave Sin a challenging look. “ [TARGET] Let me go and I’ll show you how much longer I can fight.” Sin’s full lips twisted into a smirk and his long lashes lowered over his eyes as they narrowed.

> 8. [POS_002] So many times I thought about how much I wanted that bitch dead and now…” Boyd silently urged himself to just do this, to not care, to simply end it. [TARGET] But… “You’re not fighting me,” he observed. “ Why bother?”

> 9. [POS_002] Sin ignored Boyd’s comment. “ [TARGET] So I guess I won’t get to fight him. Not tonight at least.”

> 10. [POS_003] She did sign me up to fight. [TARGET] If I’m not fighting, maybe there’s no point in me sticking around, ya know?” “ You’re so blind sometimes.

> 11. [POS_003] That’s what that was,” Travis said. “ [TARGET] Shit, I didn’t know you could fight.” Slade had an arm slung around Jessica. “

> 12. [POS_003] Yeah, I do. [TARGET] In fact, I have a fight coming up.” Her back stiffened and she looked down. “

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 309

- **Label:** **UNLABELED** (absent from Stage08 / topic_lookup)
- **Taxonomy:** ?
- **Cliff's delta:** +0.1632 [+0.1406, +0.1840] — small — more in HIGH-rated
- **Mean share:** high 0.090% vs low 0.070% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 127 docs
- **Stage07 exclusion:** [SOFT_REVIEW:tiny_topic] 309_shook_head_she_her (next=stage08_quality_adjudication)

**Four keyword representations** (BERTopic / labeling)

- **Main:** —
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. she shook her head. “

> 2. she shook her head. “

> 3. she shook her head. “

**Stage-08 / Stage-07 snippets**

> 1. she shook her head. “

> 2. she shook her head in disbelief. “

> 3. she shook her head in dismay. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 87 — Threatening Death As A Warning

- **Label:** Threatening Death As A Warning
- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Cliff's delta:** +0.1620 [+0.1419, +0.1833] — small — more in HIGH-rated
- **Mean share:** high 0.407% vs low 0.319% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 394 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** kill, killed, dead, die, killing, alive, died, you, murder, going
- **KeyBERT:** sentence, promises, admit, violently, repeat, commander, attempt, weapons, survived, handled
- **POS:** commander, percent, creatures, period, promises, weapons, sentence, issue, ye, wound
- **MMR:** survived, commander, witnessed, handled, weapons, attacked, intend, sentence, wound, problems

**BERTopic representative docs**

> 1. but i didn’t kill him.”

> 2. so it’s kill me or go back and be killed, is that it?

> 3. krav maga is all about kill or be killed, and you’re going down, little man.”

**Stage-08 / Stage-07 snippets**

> 1. you’ll have to kill me first.” “

> 2. perhaps i’ll kill him right now.”

> 3. if i go and later learn you’ve gone behind my back and done exactly what i’m about to warn you not to do, i’ll kill you in a slow, unmerciful, and painful way.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · Divine Savior — Kathi S. Barton; tertile=end; p=0.66**
>
> He probably meant to kill Brenda as well, but he never returned before Shade had to kill her. [TARGET] Then he was going to kill the three of you together. Aaron, we need to kill this being before he harms another of our mates.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Highlander Most Wanted — Maya Banks; tertile=begin; p=0.69**
>
> His eyes were fierce, yet when he spoke his voice was quiet and resolute. “ [TARGET] So that I could kill him now for all he has done to you.” Another tear crept over her eyelid and slipped unchecked down her cheek.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Tolerance — D.H. Sidebottom; tertile=begin; p=0.60**
>
> The familiar hatred began to bubble inside me. “ [TARGET] They are all dead because of what I did.” Carter was quiet for a moment.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Atlantis Dark Tides — Allie Burton; tertile=begin; p=0.70**
>
> I didn’t use the knife against him again. [TARGET] I didn’t want to kill him or wound him mortally, I just wanted to get away. Kicking out my heel, I aimed for his groin.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Indigo Spell — Rachel Carrington; tertile=middle; p=0.69**
>
> Arista rejoined the conversation. “ [TARGET] Could you kill him should that become necessary?” A cold chill ran down Athena’s spine. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Cera's Place — Elizabeth McKenna; tertile=begin; p=0.63**
>
> He was a great man, a brave man. [TARGET] He saved my life and died because of it.” Jake fell silent, remembering what he wished he could forget.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Vulcan's Woman — Jennifer LaRose; tertile=middle; p=0.64**
>
> Do I need to say more?” “ [TARGET] What I killed was not a man.” “ It was!

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Natural Attraction — Catherine Haustein; tertile=end; p=0.65**
>
> He was a good man. [TARGET] I didn’t expect him to die so soon.” Granny lowered her head. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Becoming Bea — Leslie Gould; tertile=end; p=0.44**
>
> It wasn’t like I could buy the bookstore, not with Ben working there. [TARGET] Of course, I could fire him. But I suspected the Schmidts were thinking of selling it soon and moving in with one of their children, and I imagined they’d offer it to Ben first. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Balancing Act — Jill  Blake; tertile=end; p=0.57**
>
> Eva pulled a couple mugs from the cabinet and turned on the kettle. “ [TARGET] I don’t have the killer instinct.” Angie washed her hands at the kitchen sink. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · To Redeem a Rake — Christi Caldwell; tertile=end; p=0.57**
>
> I could kill you.” [TARGET] I want to kill him for having broken Daphne’s heart and for having known her body and… The buzz of whispers ricocheted about the club, dimly penetrating his fury. With alacrity, he released Tennyson suddenly and the blackguard collapsed in his seat, sucking in great, gasping breaths. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Sugar Pine Trail — RaeAnne Thayne; tertile=middle; p=0.44**
>
> If I had only kept my mouth shut for once, Dylan and I would have been sitting by a luxury hotel pool in Doha having drinks with a couple of beautiful junior officers in bikinis. [TARGET] Instead, he signed up to head into the field and ended up being the target of a twelve-year-old suicide bomber.” His voice was hollow, filled with regret, and it took all of her strength to keep her fingers curled together on her lap instead of reaching out to comfort him. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · L.A. Cinderella — Amanda  Berry; tertile=middle; p=0.38**
>
> Why, I’m here for you. [TARGET] To slay whatever needs to be slayed. To lay whatever needs to be laid.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Because of Rebecca — Leanne Tyler; tertile=end; p=0.50**
>
> I don’t have your money,” he gritted through clenched teeth. “ [TARGET] Sure you do or you wouldn’t have skedaddled out of town after I cut you.” “ I tell you I’m not the man you’re looking for.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · Virtual Love — Kim Malone Scott; tertile=end; p=0.44**
>
> If I never have to look at another bowl of soup or porridge again I’ll be content. [TARGET] Getting hit by a car was no picnic but I’m not dying. This food is making me feel like I have one foot in the grave already.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · What About Now — Grace R. Duncan; tertile=middle; p=0.57**
>
> I can’t wait to see it.” “ [TARGET] If I don’t kill him and he doesn’t set the damned ship on fire first,” Braden muttered. Rafe snickered. “

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 119 — Offering to Keep Her Safe

- **Label:** Offering to Keep Her Safe
- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Cliff's delta:** +0.1598 [+0.1390, +0.1812] — small — more in HIGH-rated
- **Mean share:** high 0.317% vs low 0.262% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 312 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** safe, protect, protection, dangerous, protecting, keep, defend, you, safety, re
- **KeyBERT:** protect, guarded, secure, threat, dangerously, assure, sir, precious
- **POS:** meantime, testing, inevitable, distraction, threat, determination, protect, secure, terms, precious
- **MMR:** guarded, dangerously, affect, inevitable, assure, president, threat, determination, terms, caressed

**BERTopic representative docs**

> 1. i only want to protect you, jess.’

> 2. my job is to protect you, to keep you safe until i can get you back to your home.” “

> 3. it was as if you felt safe in me arms, like you knew i would protect you from anything."

**Stage-08 / Stage-07 snippets**

> 1. come on, i’ll protect you.”

> 2. you’ll protect me?” “

> 3. i can protect you from crystal, but you’ll have to let me.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 16 examples from 4 books; ±1 context on 16_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Other packet sentences** (not tagged CELL_A–D)

> 1. [POS_001] Yed ran close behind her, no way was she getting away with that. " [TARGET] Hey, you can't do that, you're supposed to be protecting me." " Yeah which is exactly what I'll tell the law enforcement when they drop by," Yed yelled as he pursued her to her room.

> 2. [POS_001] In a couple of days, we'll travel topside with covetall. [TARGET] I want to make sure it's safe, then we're heading out." " How do you know we won't get caught?"

> 3. [POS_001] Tiger accepted her hug back and smiled at her. " [TARGET] It's okay Carressy, haven't I always kept you safe? I know, let's play a game," Tiger said. "

> 4. [POS_001] Yed helped her lie down. “ [TARGET] I am your Protector, you have to do what I say.” Ezra nodded and lied down. “

> 5. [POS_001] We are safe, Wallis. [TARGET] I will make sure he keeps you safe too." " He wants me to disobey my oath, but daddy said I shouldn't ever.

> 6. [POS_002] Alarm Lock Corporation ) Safetygard 11 Deadbolt Alarmed Security Lock The safety alarm lock provides secure, full-time locking of emergency exit doors while complying with standard safety, fire, and local building codes. [TARGET] It provides maximum day and night security and a powerful deterrent against pilferage— from within or without—and always remains panicproof. The safety alarm lock provides instant automatic exit in case of an emergency.

> 7. [POS_002] S/A Sub-assembled. [TARGET] safe A substantial, secure container with varying degrees of security and/or fire resistance, used to store valuables against fire or theft. safe deposit A typically key accessed container that requires dual key operation, usually located inside a vault.

> 8. [POS_002] And ask during every service call. [TARGET] Be prepared to talk about the benefits of buying one of your safes—convenience, protection, and peace of mind. Explain that you install and service your safes.

> 9. [POS_002] Sentry Group ) Make sure your customer knows that he or she should tell as few people as possible about the safe. [TARGET] The fewer people who know about a safe, the more security the safe provides. Installing an In-Floor Safe Although procedures differ among manufacturers, most in-floor safes can be installed in an existing concrete floor in the following way ( Fig.

> 10. [POS_002] Be prepared to talk about the benefits of buying one of your safes—convenience, protection, and peace of mind. [TARGET] Explain that you install and service your safes. Even if the person isn’t ready to buy one now, he or she will remember you when he or she is ready to buy.

> 11. [POS_002] Closing the desk drawer all the way pushes the bolt into the locked position. [TARGET] Herein lies the weakness in the desk’s security. The bolt usually needs to be pushed up from under the desk by hand to open most of the drawers.

> 12. [POS_002] To reduce the risk of scratching the car, use a tool guard to cover the tool at the point it contacts the car. [TARGET] Be careful when opening cars that have airbags. They have wires and sensors in the door.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 81 — Mentioning A Brother

- **Label:** Mentioning A Brother
- **Taxonomy:** 5.1 — Family, Kinship & Parenthood
- **Cliff's delta:** +0.1563 [+0.1354, +0.1772] — small — more in HIGH-rated
- **Mean share:** high 0.239% vs low 0.192% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 417 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** brother, brothers, your, my, older, bish, siblings, am, sibling, you
- **KeyBERT:** related, introduce, hi, closely, reminds, worst, mumbled, chuckle, admitted, follows
- **POS:** extent, annoying, task, appropriate, treatment, repeat, backs, exact, affection, bigger
- **MMR:** madam, extent, follows, replies, dismissed, annoying, appropriate, separated, repeat, affection

**BERTopic representative docs**

> 1. it is the same with me and my brothers,’ he said. ‘

> 2. i’m sure you’ve deduced by now that i’m not like my brothers.

> 3. genesis 37:26-28) as far as his brothers were concerned, that was the end of their pesky brother.

**Stage-08 / Stage-07 snippets**

> 1. i have a brother, in case you’ve forgotten.

> 2. i’m sure you’ve deduced by now that i’m not like my brothers.

> 3. i’ve brought my brother with me.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · An Offer From a Gentleman — Julia Quinn; tertile=middle; p=0.70**
>
> But deep within you, in your heart, in your very soul, is the man you were bom to be. [TARGET] You, not someone’s son, not someone’s brother. Just you.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Jaci's Experiment — Bianca D'Arc; tertile=middle; p=0.67**
>
> Nor can I deny Dave the same. [TARGET] He’s closer to me than a brother and he loves you as much as I do.” “ You’re a good man, Michael.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Fighting Fate — Barbara Speak; tertile=end; p=0.79**
>
> I'm not giving you a choice. [TARGET] This is my brother we are talking about." The last thing in the world I ever wanted to do was go to him.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Easy Charm — Kristen Proby; tertile=end; p=0.78**
>
> Okay, so this is how I see it, as an outsider looking in. [TARGET] And keep in mind that I’m your brother too, so there’s that.” “ Oh boy.” “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · The Bitch-Proof Suit — De-ann Black; tertile=begin; p=0.52**
>
> And here is something else: I had been stung my bees before, and although the stings had swelled more than is perhaps usual (I can’t really say for sure), I had never died of them. [TARGET] That was only for my brother, a terrible trap that had been laid for him in his very making--a trap that I had somehow escaped. But as I crossed my eyes until it hurt, in an effort to focus on the bee, logic did not exist.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Stranger — Zoe Archer; tertile=middle; p=0.73**
>
> It’s one thing to find out my dead father is guilty. [TARGET] It’s a whole other thing to suspect my brother, the one who I’ve trusted more than my father since I was a child. “ I didn’t realize . . .

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Fitzwilliam Ebenezer Darcy — Barbara Tiller Cole; tertile=end; p=0.72**
>
> So you see, we will indeed be brothers.” “ [TARGET] Well, I dare say I could not have chosen a better brother for myself. I will be quite honoured to have you in my family, Bingley.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Suddenly Bear — Abby Blake; tertile=begin; p=0.64**
>
> Jayden tried not to laugh. [TARGET] If she knew what his brother was up to, she’d probably be completely embarrassed. “ You’ve got tomorrow off, right?”

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Sanibel Burn — Talyn Scott; tertile=middle; p=0.56**
>
> I’m not Bane. [TARGET] I won’t listen to the Al…your brother–n- law the way he has. I have no respect for male hierarchy in the …family.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · All Through the Night: a holiday story — Maggie Robinson; tertile=middle; p=0.48**
>
> You know how I feel about unfair inheritance laws. [TARGET] To think that my idiot younger brother inherited Archer Hall just because he was a male and then drove it even deeper into the ground than Papa did—it’s offensive, I tell you. Say whatever you will about all those bra-burners, but you must agree they had a point.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · All Through the Night: a holiday story — Maggie Robinson; tertile=middle; p=0.47**
>
> And who knew Harry was so strong? [TARGET] It wasn’t like he advertised himself like his older brothers, Truman and Del, did. Granted, Truman and Del co-owned a construction business, but Harry must be hiding those muscles under the plaid shirts and corduroy jackets he sometimes wore.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · The Color of Forever — Julianne MacLean; tertile=begin; p=0.82**
>
> I think I just need to get my head around the idea of starting over. [TARGET] Tell me about your brother.” Since it was quiet in the bank and there were no customers, Jane was able to tell me that he was forty-seven years old, incredibly fit and good looking. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Bound to Love — Sally Clements; tertile=middle; p=0.42**
>
> His perfect plan lay in pieces like the shards of china at his feet. [TARGET] It had taken a couple of days, and a good few hours hacking into his brother’s old laptop before he worked out what to do. Without money or transport, it took him hours to get close to London again, and long, tedious hours sitting in a truck, listening to country music played at full volume, took their toll.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Just One Taste — C.J. Ellisson; tertile=end; p=0.55**
>
> You know he’d do anything for you.” “ [TARGET] You’re fine with your nephew coming up here?” I decide to dig while I have her on the phone and Cy is not within hearing distance. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · The Ravaged Fairy — Anna Keraleigh; tertile=begin; p=0.75**
>
> she scrunched her nose in distaste. “ [TARGET] But he was like a brother to me. He was about fourteen when he found us and had the cutest smile in all of Ireland.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Heart of a Stripper — Cyndi Harris; tertile=end; p=0.54**
>
> Where others had fallen short, Adam hadn’t. [TARGET] He had truly been more than a best friend to Mitchell; he was more like a brother. He was one person Mitchell knew would never betray him. “

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 310

- **Label:** **UNLABELED** (absent from Stage08 / topic_lookup)
- **Taxonomy:** ?
- **Cliff's delta:** +0.1505 [+0.1264, +0.1731] — small — more in HIGH-rated
- **Mean share:** high 0.160% vs low 0.141% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 127 docs
- **Stage07 exclusion:** [SOFT_REVIEW:tiny_topic] 310_hold_holding_can_let (next=stage08_quality_adjudication)

**Four keyword representations** (BERTopic / labeling)

- **Main:** —
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. i can’t hold you back.

> 2. something to hold on to.” “

> 3. will you hold me?

**Stage-08 / Stage-07 snippets**

> 1. like i was telling you last time, if you are grabbed from behind, you’ll want to hold your sgian like this.”

> 2. we’ll keep you to that.” “

> 3. yeah, we’ll keep it on this program.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 238 — Relaying A Message For Her

- **Label:** Relaying A Message For Her
- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Cliff's delta:** +0.1482 [+0.1249, +0.1695] — small — more in HIGH-rated
- **Mean share:** high 0.423% vs low 0.348% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 170 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** tell, told, what, happened, talk, knows, did, her, wish, about
- **KeyBERT:** promises, behavior, honestly, speaking, possibility
- **POS:** reception, promises, arguing, president, behavior, possibility
- **MMR:** reception, promises, arguing, president, gritted, acted, behavior, thousand, paid, speaking

**BERTopic representative docs**

> 1. did i ever tell you,” she says, “that i used to be late to english every single day, just so i could bump into you on your way to pre-calc?” “

> 2. then i told her my favorite time of day; the one food i wouldn’t eat if someone tied me down and stuck pins in me; which former president i’d like to meet, and why; and what kind of vehicle i drove.

> 3. i explained everything, from the night we hooked up, to the morning after when she acted like it was a mistake, and of course my stupid plan to make her jealous and how she’d told me that she wanted nothing to do with me. “

**Stage-08 / Stage-07 snippets**

> 1. yeah, i’ll tell her,” i reply, the sudden mood change taking me by surprise. “

> 2. i’ll go tell her.”

> 3. well, maybe you’ll get another chance to tell her.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Collaboration — Michelle  Lynn; tertile=middle; p=0.67**
>
> Her voice is almost pleading with me so I pull her arm and we head into the ladies’ room. [TARGET] After ensuring that there is no one else is in here except us, I tell her about everything...the texts, phone calls, video shoot, our date, and even the brief storage-room rendezvous. I also tell her that I honestly have no idea what I’m doing but I love it anyway. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Resist Me — Chelle Bliss; tertile=end; p=0.65**
>
> My heart ached from having to say goodbye. [TARGET] I’d told her I’d be back in a couple of days, but I didn’t know when I’d see her again. With the case wrapping up, I could be buried under a sea of paperwork and court dates. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Stepbrother With Benefits 11 — Mia Clark; tertile=middle; p=0.65**
>
> In the middle of the woods?" [TARGET] I don't think I should tell her what Ethan and I were doing in the middle of the woods just a little earlier after Caleb saw us. But, really, it's the middle of the woods!

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Never — Tara Lain; tertile=end; p=0.68**
>
> I had to kill her, or she would become something far more dangerous than she was now. [TARGET] I opened my mouth to repeat all the lies I’d already told her, but something stopped me. I couldn’t do it.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Tales Of A Drama Queen — Lee Nichols; tertile=middle; p=0.69**
>
> It just goes to show. [TARGET] But she won’t tell you what, specifically, it goes to show, unless you ask. “ What, um, does it show?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Goldie and the Three Bears — Honey Jans; tertile=end; p=0.65**
>
> Tyson growled. “ [TARGET] She said something about that after my time with her after breakfast." " I'm just as guilty, she did the same with me in bed this morning.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Fate's Love — L.A. Cotton; tertile=middle; p=0.65**
>
> Why would Corey and Kade care about Nate?” [TARGET] I knew where she was likely to be going with this, but I wanted to hear her say it. “ Hmm, what?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Stepbrother Untouchable — Colleen Masters; tertile=begin; p=0.66**
>
> Your mom has told me such wonderful things about you,” he says as we shake hands. “ [TARGET] Likewise,” I reply politely, though the truth is that she's told me almost nothing. “ Well, let's sit.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Essence of Time — Liz Crowe; tertile=middle; p=0.58**
>
> You didn’t realize what? [TARGET] That I was the loser who tried to kill her abusive asshole spouse, didn’t quite manage it, then fell head over heels in love with her? Only to get summarily dumped on my ass?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · The Hellion and The Heartbreaker — Jennifer McNare; tertile=end; p=0.57**
>
> His bitter tone reflected his scorn. “ [TARGET] You cast her aside like she was just another one of your meaningless flings, and still she protected you.” Alec watched as Colin visibly sought to control his temper, but it was clearly difficult. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · The Decadia Code — Apryl Baker; tertile=begin; p=0.50**
>
> They are a tricky people to learn, to understand.” “ [TARGET] I’ve never heard of them before,” she’d said. “ How is it you do?” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Door Four — Jasinda Wilder; tertile=middle; p=0.55**
>
> My thighs tremble, and I’m straining against the bonds, wanting to thrust, silently begging her to pay attention to my clit, to touch me where I need it most. [TARGET] But she knows, oh, she knows. Another curling stroke to the delightful, delicious little spot high inside me, just behind my clit, and then she leans forward and touches her lips to my labia.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · A Sure-Fire Cure — Kate Steele; tertile=middle; p=0.51**
>
> It said that she’d understood why my grandfather had to go, that it was only natural to want to be with the person you really loved. [TARGET] She said she was actually glad when the lie between her and Grandpa was over. Grandma told me I was a good person, and that she was ashamed at the way her own son had disowned his child.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Clippings — A.J. Mirag; tertile=begin; p=0.50**
>
> I'm to blame. [TARGET] I should've told them you were mine from the beginning. Now I've made it clear.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Shake, Rattle, and Roll — Stormy Glenn; tertile=begin; p=0.64**
>
> She’ll know you from our picture and give you the key.” “ [TARGET] You told her I was your grandson?” Mickey whispered. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Kissed by Twilight — Kitrisha Rasmussen; tertile=end; p=0.61**
>
> What did you say?” [TARGET] The whole I’d-tell-you-but-I’d-have-to-kill-you shtick ran through her mind. “ I told them I was a professional fortune cookie writer.”

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 372 — Told to Keep Up Strength

- **Label:** Told to Keep Up Strength
- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Cliff's delta:** +0.1450 [+0.1218, +0.1660] — small — more in HIGH-rated
- **Mean share:** high 0.175% vs low 0.145% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 104 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** strength, stronger, strong, weak, limitations, weaker, than, weakling, need, re
- **KeyBERT:** crushed, gain, uh, tied
- **POS:** feeding, reflection, emotions
- **MMR:** feeding, crushed, gain, proved, reflection, destroyed, tied, emotions, admit, hated

**BERTopic representative docs**

> 1. you’re stronger than this.” “

> 2. you’re stronger than bill was.

> 3. you’re stronger than this!

**Stage-08 / Stage-07 snippets**

> 1. you’ll need to keep up your strength if you’re going to wrestle with that computer.”

> 2. you’ll need your strength, cassia.

> 3. you’ll need your strength.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · A Woman's Worth — Chicki Brown; tertile=middle; p=0.64**
>
> Marc interrupted just long enough to tell her what exercise to do next. “ [TARGET] My body was so weak, yet every time I pushed myself and completed the workout, I felt my strength increasing. I’ll tell you the truth though; I hurt so much the first couple of weeks that I called this handsome fool everything but a child of God.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Backs Against the Wall — Tracey  Ward; tertile=middle; p=0.63**
>
> Blood in the water. “ [TARGET] I tried,” I say, trying to sound strong. To make up for my small mistake. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · The Day of Destiny — Lavinia Collins; tertile=middle; p=0.60**
>
> No one was particularly interested in attacking the huge knight in dark armour on the massive armoured warhorse that was not attacking them, though I did have to strike out a few times with the axe to protect myself. [TARGET] I was not strong, but I was fast and my aim was good, and I was safe. Lancelot was pushing forward hard, and since Gawain could not reach him as Bors and his sons and their men stood between them, he was cutting easily through the lines of men.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · A Siren’s Song — Billi Jean; tertile=end; p=0.64**
>
> We always care for those…” Ajax winced and worked a muscle in his shoulder. “ [TARGET] I was going to say weaker, but hell if she’s not stronger than all of us. But we don’t harm those that love us, Brennan.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Warrior — Zoe Archer; tertile=middle; p=0.49**
>
> Antaeus was the giant in Greek mythology who derived his strength from touching the earth,” she explained quickly. “ [TARGET] He was impossible to defeat, because every time he was thrown down, he rose up even stronger than before. Only Heracles was able to vanquish him by holding him aloft until his strength drained away.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · All That Bleeds — Kimberly Frost; tertile=middle; p=0.75**
>
> I’m normally stronger.” “ [TARGET] Even the strong have weak moments, and you’ve had to be stronger than most.” “ Is that so?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Wild At Heart — Charmaine Ross; tertile=middle; p=0.73**
>
> He still wasn’t ready to listen to anyone with sense, so she spoke in a language she’d hoped might get through. “ [TARGET] If you were going to use your strength against me, you wouldn’t allow me to do this.” She slid her mouth over his, their lips still wet with their previous kiss, before gently sucking.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · On Wings of Desire — Bianca Swan; tertile=end; p=0.42**
>
> You healed Rey completely. [TARGET] All our combined power could do was make him more comfortable, not heal such dreadful damage.” Lana’s eyes glinted a friendly challenge. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · The Arrangement 16: The Ferro Family — H.M. Ward; tertile=end; p=0.37**
>
> An honest man doesn’t use hookers. [TARGET] A good man doesn’t overpower them and force them to his whims. I did.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · At His Service: Part 2 — Suzanne Rock; tertile=begin; p=0.52**
>
> Leo steeled his jaw and reached for his glass of scotch. [TARGET] If he had any hope of maintaining control over the situation, he was going to need some liquid strength. * * * This was insane.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Piqued — Elise Black; tertile=middle; p=0.50**
>
> Take a risk. [TARGET] You’d still be the one with all the power.” “ If I’m a submissive, doesn’t that mean I’m powerless?” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Ruby's Choice — D.F.   Jones; tertile=end; p=0.51**
>
> I don’t want to waste another minute of my life without you by my side. [TARGET] I will stand by you and give you what is within my power to support you. What do you think?”

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Educating Caroline — Patricia Cabot; tertile=middle; p=0.50**
>
> Even badminton seemed a strain sometimes. [TARGET] No, he was not yet strong enough to embark on whatever mission this was that he’d assigned himself. But if he would not listen to the doctor’s words of warning, or his mother’s protestations, or Caroline’s misgivings, however was she to induce him not to go?

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Diplomacy — Zahra Owens; tertile=begin; p=0.35**
>
> In the past few years it had become painfully clear to Lucas that without the right woman on his arm, he could kiss a diplomatic career goodbye. [TARGET] Even in the lower ranks, the invisible masses, you needed the D i p l o m a c y | 17 perfect background to push ahead. In the three years that he had been working for the U.K. Foreign service he had been sent from one menial job to the next, every senior officer telling him he was sure to get ahead because of his pedigree, but being brushed aside every time.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Murphy's Law — Kat Attalla; tertile=middle; p=0.58**
>
> Stockton’s cool description of the pleasure he would take in her death was more than she could quietly accept. [TARGET] She summoned all the strength she could gather from her rapidly weakening body. Without thought to the foolishness or danger, she landed her elbow in his gut. * * * *

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · Bound with Love — Megan Mulry; tertile=middle; p=0.63**
>
> Orchestrating as always, are you?” “ [TARGET] Best to stick with one’s strength, don’t you think, Farleigh? In you go.”

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 55 — Worrying About An Unplanned Pregnancy

- **Label:** Worrying About An Unplanned Pregnancy
- **Taxonomy:** 2.5 — Sexual Negotiation, Safety Preparation & Boundaries
- **Cliff's delta:** +0.1438 [+0.1226, +0.1677] — small — more in HIGH-rated
- **Mean share:** high 0.289% vs low 0.255% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 481 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** baby, pregnant, babies, children, pregnancy, kids, child, have, having, want
- **KeyBERT:** pregnant, tightly, worries, assume, period, willingly, awhile, squeezed, handled, introduce
- **POS:** pregnant, promising, awhile, worries, fashioned, sorts, magical, notion, period, distraction
- **MMR:** pregnant, promising, introduce, worries, fashioned, discussing, notion, assure, draped, ought

**BERTopic representative docs**

> 1. yeah so, i thought you loved kids but just couldn't have any...oh shit, you're pregnant."

> 2. that was before he knew you were pregnant,” calix said. “

> 3. before, you didn’t know you were pregnant.

**Stage-08 / Stage-07 snippets**

> 1. just a little while longer and you'll be holding a baby in your arms.”

> 2. it’s been a while since i’ve taken care of babies, but i’m sure i’ll remember how.”

> 3. just because we slipped up once doesn’t mean you’ll get pregnant.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 13 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Fatal Destiny — Marie Force; tertile=begin; p=0.60**
>
> What does that mean— Hmm ?” “ [TARGET] It’s just, you know, you suffered a miscarriage a few weeks ago, and now you’ve totally changed direction on how you feel about having a baby. I wouldn’t be doing my job if I didn’t ask how you’re doing up here.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Nate — Delores Fossen; tertile=begin; p=0.63**
>
> And they only took ours. [TARGET] They said cooperate or we’d never see our babies again. Our babies, ” he emphasized. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Suited to be a Cowboy — Lorraine Nelson; tertile=end; p=0.65**
>
> If he could live without her after all they’d shared, then he wasn’t the man for her. [TARGET] Somehow, she’d find the will to live without him in her life—baby or no baby. “ I think I’m going to retire early tonight, maybe catch up with a few friends online.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Loving the Country Boy — Mia Ross; tertile=begin; p=0.64**
>
> I figure it’ll come in handy when we’re old and creaky.” “ [TARGET] I can’t wait until the baby comes so you can stop carrying me up and down the stairs,” his wife added. “ And here I thought it was romantic.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · From Friends to Forever — Karen Templeton; tertile=begin; p=0.66**
>
> You’ll be lucky if Billy comes home for Thanksgiving and Christmas, especially if he’s playing college football. [TARGET] A baby at home won’t make much difference to him, but it’ll be great for both of you.” She looked nostalgic as she said it. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · A Playboy's Love Affair — Emily Quinn; tertile=end; p=0.65**
>
> He strode toward her, pointing his forefinger at her in warning. “ [TARGET] If you’re pregnant you have no right to keep me away from my kid, and this time I’ll take you to court if I have to.” “ What, you’re going to take me to court like you didn’t last time?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Rapine: Abducted by the Billionaire — Charlotte Rose; tertile=end; p=0.68**
>
> I can wait. [TARGET] I don’t think I’d want to bring a baby into the picture now to interrupt our fun. “ I’m goi ng to continue taking my pill.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · Miss Millie's Groom — Catherine E. Chapman; tertile=middle; p=0.61**
>
> So you needn’t worry about your little Effie, Millicent. [TARGET] Rest assured, her baby will want for nothing and be thoroughly spoilt by its mother’s employers.” Millie smiled to hear this. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Blackmoore — Julianne Donaldson; tertile=middle; p=0.40**
>
> Generations ago, rooks were here, haunting this tower. [TARGET] The off- spring follow the habits of the parents.” I watched the birds settle, then fly again, then settle with another round of cries. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Geekerella — Ashley Poston; tertile=middle; p=0.49**
>
> It started out as a wrong number, actually. [TARGET] Like you know those Buzzfeed articles where people text the wrong number while going into labor and then these randos show up with diapers and baby formula and they become besties?” “ No, but I’ll take your word that it happened.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Geekerella — Ashley Poston; tertile=middle; p=0.52**
>
> is the price of a small child.” “ [TARGET] Well my firstborn’s already taken by the Dark Lord, so how about we just make one instead?” “ Make it?”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Geekerella — Ashley Poston; tertile=middle; p=0.52**
>
> Sage’s mom puts a hand to her chest. “ [TARGET] You know you can always come here if you need some mothering. Just ask Sage.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Demon Angel — Meljean Brook; tertile=middle; p=0.53**
>
> I heard you come in; I was surprised by the sword. [TARGET] I did not think your babysitters would allow you to carry one around the city.” “ They don’t know,” he said. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · For Sale: Old Manor House — Merabeth James; tertile=end; p=0.39**
>
> I’d like to stay, if you don’t mind. [TARGET] There’s still children there…Toby for one. I’d like to haunt the schoolrooms and maybe make amends for my failings with Breanna and Devon.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Elemental Love — L.M. Somerton; tertile=begin; p=0.45**
>
> The calling has skipped a generation. [TARGET] History dictates that the next born will be unusually powerful and that power will be magnified even further in a male child.” “ There has been no warlock in my family line for over five hundred years, only witches.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Elemental Love — L.M. Somerton; tertile=begin; p=0.52**
>
> I don’t see him as the cornerstone of anything with value or integrity.” “ [TARGET] True, and if the child is born with the power, you and I will need to ensure that Symeon’s gaze remains elsewhere.” Gregory shivered. “

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 56 — Promising Never to Hurt You

- **Label:** Promising Never to Hurt You
- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Cliff's delta:** +0.1378 [+0.1155, +0.1577] — small — more in HIGH-rated
- **Mean share:** high 0.178% vs low 0.155% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 477 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** hurt, hurting, harm, mean, never, won, you, want, don, hurts
- **KeyBERT:** hurts, painful, distress, tightly, threatened, protect, cried, assured, insisted, causing
- **POS:** hurts, distress, painful, possibility, purpose, ye, process
- **MMR:** hurts, distress, tries, intend, deserve, threatened, causing, insisted, tightly, protect

**BERTopic representative docs**

> 1. i know, but you seem sweet and i don’t like the thought of anyone hurting you.” “

> 2. hurting that town would mean hurting you, which would mean i'd hurt katherine and my son.

> 3. by hurting others, you hurt yourself.

**Stage-08 / Stage-07 snippets**

> 1. you'll get hurt," he managed to say. "

> 2. you know i’ll never hurt you .”

> 3. i’ll make sure you aren’t hurt.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 16 examples from 4 books; ±1 context on 16_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Other packet sentences** (not tagged CELL_A–D)

> 1. [POS_001] Are you really all right? [TARGET] I don’t want you to hurt because of me.” She pressed her head against his shoulder and breathed in.

> 2. [POS_001] No, never. [TARGET] I will never hurt you, I promise.” He moved her hair from her eyes and continued to stare at her.

> 3. [POS_001] I want some lovin’ and you’re gonna do it. [TARGET] I don’t wanna have to hurt you.” He glanced back once and saw that she was lumbering toward him.

> 4. [POS_001] Do you have any pain? [TARGET] I don’t want to hurt you again.” He did want to cause her pain, but pleasure too.

> 5. [POS_001] You didn’t get your...you weren’t satisfied. [TARGET] Are you going to hurt me now?” She hated the sound of her voice, the sound of a small child. “

> 6. [POS_001] No, that’s not true, I was overwhelmed period. [TARGET] I didn’t mean to hurt you.” “ Hurt me?

> 7. [POS_002] I can be a mean bastard. [TARGET] I’ll probably say something to hurt you.” She laughed. “

> 8. [POS_002] Assuming it was her they were after, she added, “I’ll go with you willingly. [TARGET] Just please, don’t hurt him.” The brute who’d captured her had given her a queer look. “

> 9. [POS_003] Sin couldn’t help scoffing quietly. “ [TARGET] I don’t think you really care about hurting me. Please stop saying you do.”

> 10. [POS_003] You don’t have to… worry about me. [TARGET] I don’t want to unintentionally hurt you.” Boyd shook his head and frowned slightly. “

> 11. [POS_003] No. [TARGET] But at least I won’t hurt him that way.” “ You think knowing that his partner is locked up for the rest of his life won’t hurt?”

> 12. [POS_003] His lips pulled down into a frown. “ [TARGET] I honestly never meant to hurt you, Hsin. I never would have hurt you on purpose.”

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 193 — Nurse Arranged After Hospital Release

- **Label:** Nurse Arranged After Hospital Release
- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Cliff's delta:** +0.1354 [+0.1155, +0.1556] — small — more in HIGH-rated
- **Mean share:** high 0.129% vs low 0.102% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 215 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** caleb, gage, jeremiah, conrad, mica, said, texting, ignore, went, fooled
- **KeyBERT:** dr, willing, hi, uh, arrange, stares, embarrassment, nearby, speaking, admitted
- **POS:** snaps, hopeful, stares, embarrassment, explanation, evidence, screen, bodies, huge
- **MMR:** prodded, acknowledge, snaps, arrange, collected, hopeful, hovered, stares, embarrassment, climb

**BERTopic representative docs**

> 1. that’s not fair, i’ve never thought of you like that, ty, and gage—” tyler’s eyes narrowed and darkened at the mention of his cousin. “

> 2. gage was cute, but despite the fact that i didn’t acknowledge ruger’s right to give orders, i also didn’t want to get into a huge fight with him. “

> 3. i want caleb goode to treat me like his own personal fuck toy, his dirty secret, his guilty pleasure.

**Stage-08 / Stage-07 snippets**

> 1. and you’ll both stay here, at caleb’s?” “

> 2. i'll arrange for a nurse to come to the house when they release caleb.

> 3. twenty-three caleb y ou ignore me, and i’ll ignore you .

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_thin cells CELL_C, CELL_D; 10 examples from 10 books; ±1 context on 10_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Westmoreland's Way — Brenda Jackson; tertile=middle; p=0.44**
>
> When he’d graduated from high school, he had refused to go to college. [TARGET] After numerous brushes with the law and butting heads with the parents of a young lady who didn’t want him to be a part of their daughter’s life, Dillon had convinced Bane to get his life together. Everyone was hoping the military would eventually make a man of him.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Breaking Jade — Quil Carter; tertile=end; p=0.56**
>
> Rather quickly. [TARGET] Garrett was kind enough to distract Silas for a few moments as I took you and left, no one stopped me for obvious reasons,” Elish responded, but a moment later I felt the mood change around him. His voice grew colder. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Two Wrongs Make a Right — Bella Emy; tertile=middle; p=0.55**
>
> What made you come to such a conclusion?" " [TARGET] I don't know, I always saw Rohan with Katherine," I mused, pushing on with whatever I have to say, "I know you would never adopt a kid so-" "Maya, it's not-" he tried to interrupt but I threw in before he could, "so you have a son with another woman who must be missing, or must be in prison or must be sick for ages, or must have left you after delivering the kid or-" He managed to cut me in "Wait wait! Why do you come to such conclusions?" "

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · The Vilka's Servant — Pearl Foxx; tertile=end; p=0.54**
>
> A hum vibrated through his chest so loudly Vera both felt and heard the sound . “ [TARGET] I can’t go to a doctor yet because of Gideon, but I think it’s a girl .” “ You need a doctor.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Shrinking Violet — Danielle Joseph; tertile=begin; p=0.56**
>
> You want her to be Helen Keller?" [TARGET] Kayla points to me, like she can't figure out who Gavin's talking about. I don't know why I never thought of Helen Keller before in all my years of losing sleep and throwing up over oral reports. "

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Ervin's Dilemma — Stephani Hecht; tertile=end; p=0.36**
>
> Yes, even when Kylie and Dawson got sick and thin, no wolf would help us. [TARGET] If it wasn’t because we were part-human, then it was because of Braxton’s handicaps.” “ What kind of medical problems does he have?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · A Promise Of Forever — M.E. Brady; tertile=middle; p=0.54**
>
> He wondered if he knew how lucky he was. [TARGET] Brody thought that it was time for him to leave and he bid them both farewell and decided to exit, but not before asking Katelyn if she’d be alright. “ I’m fine; you don’t have to worry about me.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · Brick by Brick — Cate Ashwood; tertile=middle; p=0.52**
>
> He hoped that very much, because even though he still loved Zach and probably always would, Parley wanted him to be happy. [TARGET] He wanted Zach to feel the sweet, innocent love of a child, to know how it felt that in that child’s worldview, the names “Mom” and “Uncle” were the names of God; that a teenage sister depended on him and respected him because he didn’t judge her; that a best friend with her own broken pieces felt safe and secure enough in his presence to be herself and to let herself heal. Parley hoped very much that Zach had experienced all those kinds of love and, perhaps, the more intimate romantic love that came with physical expressions of it.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Cloak & Dagger — G. Avetis; tertile=end; p=0.40**
>
> The voice was inside Janeway’s head, and calm spread over her like a blanket at the words. [TARGET] It was Tialin, of course. But Janeway felt comforted by the telepathic contact in a way that her verbal exchange with Tialin had not permitted.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Heart — Kol Anderson; tertile=end; p=0.53**
>
> Come and dance with me,’ Grace said, grabbing Tom by the arm. [TARGET] He had put Lily down and she was now dancing with Archie, who had been happy to team up with a little person, provided they weren’t one of his siblings. At least if they did something embarrassing, he wasn’t related to them.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 114 — Guns Aimed Across The Room

- **Label:** Guns Aimed Across The Room
- **Taxonomy:** 7.2 — Violence, Threats & Non-Sexual Coercion
- **Cliff's delta:** +0.1307 [+0.1097, +0.1537] — small — more in HIGH-rated
- **Mean share:** high 0.160% vs low 0.120% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 322 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** gun, pistol, rifle, barrel, holster, glock, weapon, guns, holstered, pointed
- **KeyBERT:** weapons, aimed, pointing, flinched, motioned, choked, cocked, intently, ducked, gesturing
- **POS:** partners, commander, distraction, ribs, weapons, suitcase, comfortable
- **MMR:** fired, cocked, trained, sticking, bursting, gesturing, commander, playfully, instinctively, preparing

**BERTopic representative docs**

> 1. rick leveled his gun on phillip. “

> 2. tuck lunged for the gun.

> 3. cole jolted and unholstered his gun.

**Stage-08 / Stage-07 snippets**

> 1. while [person] trussed up the englishman, caroline aimed her gun. “

> 2. barrette renewed his grip on the pistol, and aimed at lilly.

> 3. he was on his back, the chair across his legs, but his gun still aimed at [person]. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_D; thin cells CELL_C; 9 examples from 9 books; ±1 context on 9_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Judgment in Death — J.D. Robb; tertile=middle; p=0.70**
>
> She had a choice to make and made it fast. [TARGET] The weapon seemed to leap in her hand as she fired it, struck the man holding the boy between the eyes. She saw the kid fall, heard with sweet relief his screams of terror and, diving for cover, fired again.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · The Pink Palace — Marlon Mccaulsky; tertile=end; p=0.64**
>
> I busted back, hitting him dead in his chest, right through his heart. [TARGET] Polo jerked back then looked at me in shock before his eyes rolled back in his head and he dropped the gun out of his hand. He then slumped over on the floor as a pool of blood formed underneath him.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Live Wire — Lora Leigh; tertile=middle; p=0.73**
>
> Bailey stood back so John could have the room he needed to check them out. [TARGET] As he brushed against her, she maneuvered her body until his hand brushed against the heavy weight of the gun she was carrying. His head jerked back to her in shock, his gaze narrowing as he felt the weapon before he turned back to the table and began to check the weapons.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Come To The Oaks — Bryan T. Clark; tertile=end; p=0.70**
>
> Love him or hate him, he knew his pa would have Dexter hanged if Dexter killed his only child. [TARGET] Dexter withdrew his pistol from his holster and brought it up to his waist, pointing it directly at Ben. “ Now, why don’t we locate your clothes and go find your friends.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Abiogenesis : Cyberevolution Book I — Kaitlyn O'Connor; tertile=begin; p=0.61**
>
> She'd already dug her fingers into the cut, grasped the locator and yanked it free of the bone before fire poured through her. [TARGET] Gasping at the wave of dizziness that washed over her, she dropped the locator to the pavement, picked up one of the weapons and smashed it with the butt. Blood was gushing from the cut.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · A Beginner's Guide to Rakes — Suzanne Enoch; tertile=begin; p=0.70**
>
> He straightened. [TARGET] Before she could dive for the weapon again, however, he nudged her chair aside with his hip, opened the drawer, removed the pistol, and tossed it out the window. “ There.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Under the Aspens — Elizabeth Sherry; tertile=middle; p=0.70**
>
> He made too much noise to have heard them behind him. [TARGET] Glen motioned for Sher to stay put, then got close enough to put his gun to the back of the guy’s head. “ Down on the floor.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · A Kept Man — Kerry Connor; tertile=end; p=0.73**
>
> Caleb took a step forward. [TARGET] The stranger halted the forward movement by aiming the gun flat at Caleb’s chest. “ Back off, Carpenter.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Piper LeVine, and a Gypsy's Truth — Eris Kelli; tertile=begin; p=0.56**
>
> Seriously?” [TARGET] I grabbed onto the fur behind his neck, and he bulleted down the mountain. We were moving faster than I had ever driven.

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 41 — Gripping Her Neck and Pulling Close

- **Label:** Gripping Her Neck and Pulling Close
- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Cliff's delta:** +0.1307 [+0.1071, +0.1511] — small — more in HIGH-rated
- **Mean share:** high 0.498% vs low 0.298% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 529 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** my, neck, mine, tongue, kissed, her, lips, kiss, mouth, against
- **KeyBERT:** caressed, stroking, instinctively, tasted, biting, glances, smirked, grasp, intently, cradled
- **POS:** moves, squeeze, stares, ankle, ripping, lid, entrance, flushed, thigh, waist
- **MMR:** reaches, laced, tries, moaning, playfully, instinctively, swirling, flush, panting, chased

**BERTopic representative docs**

> 1. it felt great, all slick and soft, and she lifted her head so that when i thrust out the top she could lick and suck at the tip of my cock.

> 2. she whimpered, then she moaned and began rolling her hips pushing forward towards my hardness and then without further warning i placed my swollen cock head on her pulsating wet entrance. “

> 3. my hands grip her waist and she tries to pull them away but i just grip harder, lifting her when she rises and pulling her down when she falls.

**Stage-08 / Stage-07 snippets**

> 1. i could’ve went for some of her pussy too, but right now, ass action was what i ultimately desired. “

> 2. she lifts up on her toes and kisses me, and she’s the sweetest damn thing i’ve ever tasted.

> 3. in my mind i’m pushing her away, but in reality i’ve got one hand on her lower back, pulling her against me, and my other hand gripping the nape of her neck.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_thin cells CELL_C, CELL_D; 10 examples from 10 books; ±1 context on 10_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Black Lace — J.V.K.; tertile=middle; p=0.81**
>
> I like her. [TARGET] She moves her hands up my body, tentatively touching the underside of my breast, her soft cool fingers tracing a lazy path along my skin as our tongues tangle. I move my hand to her breast to stroke the delicate edge of her puckered coral nipple.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Blood Moon — Lisa Kessler; tertile=middle; p=0.82**
>
> I couldn’t resist. [TARGET] My lips caressed her skin and she turned, her mouth meeting mine, kissing me with a tenderness that nearly brought me to my knees. I embraced her, pressing her body tightly against mine.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Second Debt — Pepper Winters; tertile=end; p=0.80**
>
> I had no choice. [TARGET] Her body wriggled against mine as I slipped another finger inside her pussy, rubbing her clit with my thumb. “ You’re so fucking gorgeous…so strong.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Liar — Lia Fairchild; tertile=begin; p=0.82**
>
> She smiled and leaned back again, so I continued. [TARGET] I moved my hands up to her neck and kissed it gently while continuing to knead her sweet-smelling skin. “ That feels so nice, Daniel.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · My Soul to Keep — Melissa Solis; tertile=begin; p=0.77**
>
> Of course.” [TARGET] I press my hand to her stomach, and my pinky finger strokes across something resting in her bellybutton. I look at her, brows lifted to ask the silent question. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · All I Want Is You — Elizabeth Anthony; tertile=begin; p=0.78**
>
> Her lips touched mine, lightly, then with firmer pressure; her tongue darted into my mouth and my pulse began to pound. [TARGET] She toyed with my mouth for a while, licking my teeth and tongue, gently biting the inside of my lip; she pushed back my robe and her hands were on my naked shoulders as I tried to control the aching throb that had started inside me. She lay back suddenly with a little sigh.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Crave — Monica  Murphy; tertile=end; p=0.77**
>
> She feels fucking amazing, surrounding me, all over me until she’s the only thing I can see, hear, smell, taste. [TARGET] I turn my head and bite along her neck, soothing the nips with little flicks of my tongue, and she releases a shuddering sigh, my name falling from her lips. That little sigh spurs me on, and I increase my pace.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Driving Layne — Renea Porter; tertile=middle; p=0.79**
>
> I press my head into her stomach, wrapping my arms around her waist as I inhale her scent. [TARGET] She runs her hands over my head, and then she forces my head back and kisses me with a hand on each side of my face. Pulling her lips off mine, she looks at me and says, “If you ever fucking talk to me the way you did earlier, this will no longer be happening.”

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Highland Wolf Christmas — Terry Spear; tertile=begin; p=0.56**
>
> The man was red-faced and pissed. “ [TARGET] What the hell do you think you’re doing with my girlfriend?” He took a swing at Guthrie.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Pine Tar & Sweet Tea — Kerry Freeman; tertile=begin; p=0.62**
>
> Ashley, stop that! [TARGET] You’ll pull her arms out of her sockets.” Ashley frowned. “

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 287 — Pleading With God Through Struggle

- **Label:** Pleading With God Through Struggle
- **Taxonomy:** 3.4 — Beliefs, Values & Moral Reflection
- **Cliff's delta:** +0.1304 [+0.1081, +0.1526] — small — more in HIGH-rated
- **Mean share:** high 0.391% vs low 0.344% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 141 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** theirs, pout, destination, example, result, reflection, exchange, ye, delicate, process
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. if there’s a hell, then there must be a heaven.”

> 2. god, it was heaven.

> 3. but if i say no, i go on living, have a full life, die a natural death, maybe go to heaven, or hell, which-ever i'm bound for, but your soul goes to..." "hell.

**Stage-08 / Stage-07 snippets**

> 1. if god adopts me, i’ll want to do whatever pleases him.” “

> 2. i’m hoping if you’re facing struggles now that you’ll let god see you through.

> 3. if you are, then you’ll have a special place in hell.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 133 — Holding Back Tears

- **Label:** Holding Back Tears
- **Taxonomy:** 3.2 — Negative Emotions & Distress
- **Cliff's delta:** +0.1294 [+0.1074, +0.1503] — small — more in HIGH-rated
- **Mean share:** high 0.208% vs low 0.168% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 289 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** tears, cry, crying, tear, cheeks, cried, my, shed, eyes, down
- **KeyBERT:** cried, emotional, sadness, emotions, afterward, begged, frantic, harshly, dripping, pressure
- **POS:** pout, dripping, inevitable, sadness, frantic, combination, current, tracks, sidewalk, confusion
- **MMR:** shed, pout, wipe, dripping, bursting, tumbled, frantic, crashing, choked, sidewalk

**BERTopic representative docs**

> 1. i felt like crying.

> 2. i didn’t feel like crying at all.

> 3. i don’t know when i started crying, but tears were streaming down my face.

**Stage-08 / Stage-07 snippets**

> 1. we’ll leave all our tears out to dry on the patio while we swan off to the acropolis!

> 2. they'll also cry foul.

> 3. they’ll tell you that i don’t do crying.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · From Willa, With Love — Coleen Murtagh Paratore; tertile=middle; p=0.69**
>
> I’ll meet you outside,” Will says to me. [TARGET] When he joins me out front, I see his face is wet with tears. Oh, wow, I guess he and Tina really are falling in love.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Sparrow Man — M.R. Pritchard; tertile=end; p=0.71**
>
> Yes, John… John Lewis told me so.” [TARGET] I release a hard shudder and swallow down the remaining tears that are threatening to stream down my face. “ He said I killed you on the day I was born.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Wes' Denial — Joseph Lance Tonlet; tertile=end; p=0.69**
>
> He didn’t answer, but his hold tightened. [TARGET] Nearly from the moment he’d wrapped his legs around me he’d begun crying and tears continued to slide down his cheeks. At my instruction, Pavel drove us around the city rather than back to the hotel.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Coast — Jay McLean; tertile=end; p=0.72**
>
> Tommy!” [TARGET] I wipe at my tears, tears that came on so quickly I had no idea they were there until I tasted them on my lips. “ You’re a stupid head!”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Pants on Fire — Meg Cabot; tertile=end; p=0.75**
>
> And I’d wonder why you did i t.” “Because you were my friend,” I said quickly. [TARGET] The tears weren’t just gathering under my eyelashes now. They were starting to spill out from under them.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · A Knight to Remember — Karin Tabke; tertile=middle; p=0.70**
>
> And there, on the page, is something that does make me laugh, but just a thin, faint, humorless chuckle. [TARGET] And then I weep again, silent tears tracing themselves down my face, plunking hollowly against my robe. Miranda knelt before the Lady Seraphina, a blazing intensity to her gaze. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Undead Have Bunnies, Too — Scarlet Hyacinth; tertile=end; p=0.66**
>
> At least, that was what I guessed it must have said, because the words had been uttered at a very low volume. [TARGET] Truly, one would have thought that such a cry would come as a loud shout, but that wasn’t the case, and I soon found out why. Two small beings stood at the edge of the grove, pointing bows equipped with tiny arrows at me.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · His Rules — Dani Wyatt; tertile=begin; p=0.66**
>
> But I’m losing, I can feel it. [TARGET] A tear fights its way from the corner of my eye and streams down my cheek like a tiny, traitorous river. I flip my head the other way so some of my hair falls to cover the humiliating tears. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Eternal Rider — Larissa Ione; tertile=begin; p=0.55**
>
> There’s a lot at stake, and you’re going to need to do some serious toughening up if you want to survive. [TARGET] A lot of people are going to die before this is over, so dry the tears and deal. Right now you’re the most important human on the planet, so act like it.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Claiming Shayla — Zena Wynn; tertile=middle; p=0.32**
>
> He couldn’t disguise the disgust he felt with his pack and the old ways most, if not all, were clinging to with all their strength. [TARGET] It was a far cry from the shifter values and tenets Conor had mentioned during the reception. His pack really were the throwbacks many accused them of being. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Timeless Sojourn — Jamie Salisbury; tertile=end; p=0.54**
>
> I wouldn’t have missed this for the world.” [TARGET] Fighting back tears, and determined that neither of them see it, I piv oted on my heel to leave. As I did, I almost ran right into Renee.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Revenge — Christine Carminati; tertile=middle; p=0.57**
>
> Sometimes they need building up.” “ [TARGET] So you tear me down to do it.” His voice was like the flat edge of a knife: it didn’t hurt, but all he had to do was turn it and it would slice right through her. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · First to Burn — Anna Richland; tertile=middle; p=0.61**
>
> Jennifer patted her back. “ [TARGET] Babe, if you’re crying, he did something, and it was wrong.” * * * Time heals , Jennifer had spouted at least a dozen times over the past two days.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Dark Stranger the Dream — I.T. Lucas; tertile=begin; p=0.35**
>
> Savagely took the life of Annani’s one great love. [TARGET] The laments sung to mourn Khiann’s passing and to grieve for the great love so tragically lost would become a ritual to be performed every year on the anniversary of his death. Annani’s father called for the big assembly to decide Mortdh’s fate.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Dark Stranger the Dream — I.T. Lucas; tertile=begin; p=0.52**
>
> Why are they chasing me? [TARGET] Dear God, I’m going to die—horrifically—they are going to tear me apart. Her eyes darting frantically in search of help, Syssi could see nothing besides the elusive shadows the moon was casting on her path.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Dark Stranger the Dream — I.T. Lucas; tertile=middle; p=0.51**
>
> A man she’d conjured in her mind. [TARGET] And how devastatingly sad was that?

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 122 — Wound Bleeding and Blood Loss

- **Label:** Wound Bleeding and Blood Loss
- **Taxonomy:** 1.2 — Pain, Injury & Physical Vulnerability
- **Cliff's delta:** +0.1290 [+0.1075, +0.1496] — small — more in HIGH-rated
- **Mean share:** high 0.148% vs low 0.117% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 310 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** blood, bleeding, bleed, veins, lost, drinking, everywhere, lot, need, your
- **KeyBERT:** veins, wound, dripping, carved, spilled, pressure, dr, spilling, concerned, asks
- **POS:** internal, veins, activity, creatures, fading, distraction, dripping, quality, drawer, circumstances
- **MMR:** internal, veins, prompted, carved, activity, creatures, spilled, circumstances, sounding, paid

**BERTopic representative docs**

> 1. my blood for your blood.

> 2. blood on the windshield.

> 3. and i get to take blood?

**Stage-08 / Stage-07 snippets**

> 1. whenever innocent blood is spilt, it’ll be my father’s blood… and you’ll find me there.

> 2. offer her the meat in the sack from the palm of your hand and she’ll not draw blood.

> 3. i know head wounds bleed a lot, but you want to keep most of your blood inside your body where it’ll do you some good.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_thin cells CELL_D; 14 examples from 12 books; ±1 context on 14_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Always Look Twice — Emily March; tertile=begin; p=0.74**
>
> Then I ran to the car and drove home. [TARGET] I had blood all over me and I needed to get it off.’’ ‘‘ Of course you did,’’ Annabelle said in a soothing tone.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Dark Warrior Untamed — Alexis Morgan; tertile=end; p=0.62**
>
> Fine. [TARGET] The blood would only serve to make the ropes more slippery if she could loosen them enough to pull a hand free. It was time to figure out what was going on with her captors.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Sanibel Burn — Talyn Scott; tertile=begin; p=0.74**
>
> Then….No, that wasn’t right. [TARGET] At least, he didn’t think so, blood in the wrong place. He could hammer nails with it; build a new house in seconds.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Fashionably Dead Down Under — Robyn Peterman; tertile=middle; p=0.71**
>
> The smells were divine and I wished for the umpteenth time I could still eat food. “ [TARGET] I’d offer you some blood, but we don’t keep it on hand,” he said. “ I assume from your rosy cheek color and the smell of sex you are both quite satisfied.” “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · The Sun Sword — Lexxie Couper; tertile=middle; p=0.68**
>
> You’re wrong. [TARGET] Your blood feeds the death of the heart and only your blood will nourish the heart’s savior!” He shut the old woman’s insane cries from his head, rounded the bend and headed for his ship.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · A Darker Shade of Dead — Bianca D'Arc; tertile=end; p=0.71**
>
> They didn’t bleed much, she noticed absently, though the glass made long, deep gouges into their skin. [TARGET] It looked like the majority of blood they’d possessed when living had already drained out of their previous grievous injuries. Sandra made it to the door and turned the handle.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_014 · Quinn — J.C. Cliff; tertile=begin; p=0.61**
>
> Good. [TARGET] I don’t care if they fucking bleed to death out here, but they probably won’t, not unless I hit a main artery in his leg. “ I would be scared to breathe if I were you.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · Hard-Hearted Highlander — Julia London; tertile=middle; p=0.59**
>
> He said those words to Cailean, knowing them to be true, but at the same moment, his heart was searching for any idea of how to end this engagement. [TARGET] His blood churned with the discomfort of being at odds with what his family needed of him and what he wanted. He shoved a hand through his unkempt hair and looked wildly about, avoiding Cailean’s gaze.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · All Summer Long — Susan Mallery; tertile=begin; p=0.73**
>
> She drew in a breath. “ [TARGET] You know, there really can be blood your first time. I grabbed the blanket and took it with me, then I went to the police.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · The Antichrists — Mark A. Roeder; tertile=middle; p=0.55**
>
> If a man lies with a man as one lies with a woman, both of them have done what is detestable. [TARGET] They must be put to death; their blood will be on their own heads." Again, these are not my words, but the words of the Bible, Leviticus 20:13.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Tell Me Not To Go — Victoria De La O; tertile=middle; p=0.27**
>
> His child never made it that far though, because at twenty-one weeks, a baby can’t survive on its own. [TARGET] It may have a heart and lungs and a brain, but it is not viable. But I guess that biological truth doesn’t mean shit when you created that heart, those lungs, and that brain. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Tell Me Not To Go — Victoria De La O; tertile=middle; p=0.56**
>
> My stomach aches watching them lay it all out there. [TARGET] They might as well be bleeding from their chests. Sam and I scramble out the front door to give them some privacy.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · Waiting for Ethan — Diane  Barnes; tertile=end; p=0.41**
>
> My reflection in the vanity mirror scares me. [TARGET] My bloodshot eyes are half the size as usual, and my skin has a distinctive greenish tint. A wave of nausea hits, and I collapse in front of the toilet.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · Waiting for Ethan — Diane  Barnes; tertile=begin; p=0.72**
>
> He looks down at his chest and then looks me in the eye. “ [TARGET] Blood from the last girl I helped.” His eye contact does not waver.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 244 — Confessing A Shattered Heart

- **Label:** Confessing A Shattered Heart
- **Taxonomy:** 3.2 — Negative Emotions & Distress
- **Cliff's delta:** +0.1283 [+0.1056, +0.1490] — small — more in HIGH-rated
- **Mean share:** high 0.136% vs low 0.113% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 167 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** heart, broken, broke, hearts, heartbroken, my, break, breaking, yer, shattered
- **KeyBERT:** affection, emotional, heal, memories, engaged, glued, suffering, terrified, attached, pieces
- **POS:** results, value, reminder, affection, edges, terrified, current, emotional, permission, pieces
- **MMR:** glued, heal, shaped, suffering, affection, attached, emotional, pieces, sank, memories

**BERTopic representative docs**

> 1. you know what they say, my hearts.” “

> 2. you could break a lot of hearts.”

> 3. a million hearts just broke, west."

**Stage-08 / Stage-07 snippets**

> 1. i’ve been heartbroken, truly shattered since leaving you behind in cleveland .

> 2. and actually it’s pretty handy you love me since i’ve already had my heart smashed around like day old potatoes once this year.”

> 3. it’s always been the way i’ve protected my heart, though i never thought about the hearts of the women i used.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Off Limits — Sawyer Bennett; tertile=end; p=0.64**
>
> I don't know what to say to this news, because frankly, I don't understand it. [TARGET] I only know that my heart is hurting immensely for this man who has apparently suffered so much. " I can understand if that freaks you out and you want to break things off," Nix says hesitantly.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · The Dark Light of Day — T.M. Frazier; tertile=end; p=0.65**
>
> Just his presence seemed to make things lighter. [TARGET] It was funny to think that someone so emotionally heavy on my heart could actually make things lighter. Georgia must have slept in, too, because it was already seven– thirty, and she hadn’t come into my room to ask for her usual Saturday morning pancakes.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · The Highlander's Bargain — Barbara Longley; tertile=middle; p=0.63**
>
> I dinna ken whom this Shakespeare fellow might be, but when it comes to you, my very breath is a testament to the love I bear you, lass. [TARGET] How is it you are no’ aware my heart beats solely for you?” “ See?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Down to My Soul — Kennedy Ryan; tertile=middle; p=0.64**
>
> MY MASTER PLAN is working. [TARGET] My heart almost fell right out of my chest when she said that. She’s never referenced our future that way.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Misfortune Cookie — Michele Gorman; tertile=end; p=0.58**
>
> Squeezing my friend back, I think about my fortune cookie. [TARGET] Following your heart will pay off in the near future . I suppose maybe it will.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Ruin — C.J.  Scott; tertile=end; p=0.70**
>
> Chapter Thirty-Three She has absolutely no idea what she does to me… She’s my medicine, my cure, my everything. [TARGET] If only hearts could heal that way — through someone else’s beating. Weston “There you go.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Heights of Desire — Mara White; tertile=end; p=0.68**
>
> Yes?” [TARGET] I say my heart swelling with pain and love simultaneously. “ Tell him that you’ll wait for him.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · Best Man for the Bridesmaid — Jennifer Faye; tertile=end; p=0.53**
>
> Of course not. [TARGET] It would never be Miss Follow-Your-Heart’s fault that something went wrong and everyone else had to pick up the pieces. But he wasn’t going to spoil his sister’s wedding by picking a fight with her best friend.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Echoes at Dawn — Maya Banks; tertile=end; p=0.59**
>
> You’ve given people a new lease on life. [TARGET] You saved a child who would otherwise be dead right now and you risked your own life to do it because your heart is too soft for you to say no even though it might have meant your own death. “ You have no idea of the things I’ve done, the choices I’ve made.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Her Demonic Angel — Felicity Heaton; tertile=end; p=0.55**
>
> I did not make you love Veiron, and did not make Veiron love you. [TARGET] That sickening emotion was destined to bloom between you. I merely gave you both a helping hand.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Next of Kin — Sue Welfare; tertile=end; p=0.47**
>
> No.’ ‘ [TARGET] And what about emotionally? How would you say he was?’ ‘

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · What Happens in the Alps... — T.A.   Williams; tertile=end; p=0.45**
>
> I don’t see why not. [TARGET] I’ve been going through some tough times and it’s only now that I’m coming back to life. I’ve been locked up inside my head for the last two years and the fact that I’m coming out of it now is definitely in part thanks to you.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Fracture — K.L.  Hughes; tertile=end; p=0.47**
>
> He felt the barrel jamming into the back of his skull. ' [TARGET] Like a broken toy, broken boy, here ends your fractured little life .' A terrible pause. '

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · The Angry Dove and the Assassin — Stephani Hecht; tertile=end; p=0.51**
>
> What’s going on?” [TARGET] Chris asked, getting right to the heart of the matter. Grey pointed to the bodies. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Healed Beginnings — Diana DeRicci; tertile=middle; p=0.65**
>
> Just his fucking luck. [TARGET] The last thing he wanted was to have his heart broken. Looked like he didn’t have a choice in the matter. * * * *

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Moon Dance — V.J. Chambers; tertile=middle; p=0.59**
>
> Enoch pulled away, resting a meaty hand on each of Cole’s shoulders. “ [TARGET] So, you had a change of heart after you saw what we did in California?” “ I did,” said Cole. “

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 166 — Heart Skipping With Fear

- **Label:** Heart Skipping With Fear
- **Taxonomy:** 1.1 — Body Parts & Physical Reactions
- **Cliff's delta:** +0.1266 [+0.1048, +0.1494] — small — more in HIGH-rated
- **Mean share:** high 0.273% vs low 0.212% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 248 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** veins, hopeful, frantic, ribs, excited, unable
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. when you find yourself in the thick of it, your heart starts the auspicious troubles of chance | charlie cochet 120 pounding so hard it feels like it’s gonna burst out of your chest, and your stomach gets so full of butterflies you just might be sick.

> 2. my heart threatens to stop beating at first, then i hear my heartbeat in my ears.

> 3. my heartbeat starts racing.

**Stage-08 / Stage-07 snippets**

> 1. i silently gasped as my heart skipped several beats. “

> 2. my heart skipped a beat and i decided i wanted to hear no more.

> 3. my heart pounded wildly at the thought of baring myself in front of others. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 76 — Demanding to Be Heard

- **Label:** Demanding to Be Heard
- **Taxonomy:** 9.1 — Dialogue Delivery & Speech Tags
- **Cliff's delta:** +0.1266 [+0.1018, +0.1463] — small — more in HIGH-rated
- **Mean share:** high 0.258% vs low 0.234% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 433 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** fishing, folks, options, quality, exact, latest, explanation, notes, voices, emotions
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. just listen to me.

> 2. if only you'd listen—" "i've been listening to you drivel on about geoffrey saunders for as long as i care to," burke said. "

> 3. he just wouldn’t listen, that’s all.

**Stage-08 / Stage-07 snippets**

> 1. that’s what i’ve heard.”

> 2. did you hear a word i’ve been saying?”

> 3. no, i’ve still heard nothing.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 128 — Confessing How Much You've Missed

- **Label:** Confessing How Much You've Missed
- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Cliff's delta:** +0.1264 [+0.1046, +0.1480] — small — more in HIGH-rated
- **Mean share:** high 0.133% vs low 0.115% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 298 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** miss, missed, missing, much, ve, you, too, misses, wouldn, ll
- **KeyBERT:** hi, sir, escaped, honestly, repeated, solemnly
- **POS:** handful, precious, voices, elevator, opportunity, pieces
- **MMR:** solemnly, breathlessly, thoughtfully, handful, voices, sounding, elevator, repeated, considering, pressing

**BERTopic representative docs**

> 1. i’ve missed being adored. ‘

> 2. i've missed you all so much.” “

> 3. i’ve missed you around here.”

**Stage-08 / Stage-07 snippets**

> 1. i’ve missed most of his life already.

> 2. and, god, how i’ve missed this.”

> 3. i’ve come to realize that you are the one thing in my life i don’t want to miss.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 5 examples from 4 books; ±1 context on 5_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Other packet sentences** (not tagged CELL_A–D)

> 1. [POS_001] I can’t wait to get you naked.” [TARGET] I can’t believe how much I missed you. “ Come on.

> 2. [POS_002] I can’t wait to get you naked.” [TARGET] I can’t believe how much I missed you. “ Come on.

> 3. [POS_003] Suddenly, the time that seems to stretch out evaporates and I wish I had more time with her. “ [TARGET] I missed you these last two weeks.” Her small voice breaks our silence. “

> 4. [POS_004] I nod my head with a steady rush of tears down my cheeks, “It’s best that way. [TARGET] You won’t miss me as much when I’m gone.” “ You are so fucking selfish.

> 5. [POS_004] She rounds the corner, taking two big strides to her I scoop her little body into my arms and squeeze her as tight as I can without hurting her. “ [TARGET] I missed you so fucking much,” I admit. “ I missed you too, Memph.”

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 204 — Promising to Care For Her Sister

- **Label:** Promising to Care For Her Sister
- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Cliff's delta:** +0.1250 [+0.1044, +0.1453] — small — more in HIGH-rated
- **Mean share:** high 0.156% vs low 0.138% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 206 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** sister, sisters, your, my, little, sis, gon, sisterly, is, says
- **KeyBERT:** asks, assume, willing, uh, hi, speaking
- **POS:** enthusiasm, equipment, direct, affection, latest, permission, willing
- **MMR:** introduce, equipment, direct, affection, treated, spending, asks, speaking, willing, expect

**BERTopic representative docs**

> 1. what is your sister’s name?”

> 2. this is cora tonnu, my sister."

> 3. you're like me with my sisters." "

**Stage-08 / Stage-07 snippets**

> 1. i’ll need to finish dressing and leave a note for my sister.”

> 2. yes, and soon you’ll be my sister.

> 3. i’ll find a way to care for your mother and your sister.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 12 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · 'Til Death Do Us Part — Barbara C. Doyle; tertile=begin; p=0.70**
>
> he demanded. “ [TARGET] You have not been paying close attention to your sister’s problems lately, have you?” “ If you’re talking about those nasty memento mori gifts she has been receiving, you’re wrong.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Morgan's Gift: The Hunted Book 4 — Jennifer Ryan; tertile=end; p=0.76**
>
> You owe me big-time, and it’s going to cost you a cool million. [TARGET] That is, if you want your sister back.” “ You just got out of jail.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · A Royal Fortune — Judy Duarte; tertile=begin; p=0.64**
>
> Thank you for that. [TARGET] I just hope your sister and the rest of your family does, too.” “ We’re aware of how the paparazzi creates stories out of nothing.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Galatea's Revenge — Kelly McClymer; tertile=begin; p=0.68**
>
> A slight blush appeared upon the girl's cheek, but Juliet ignored the sign that her words had been unwelcome. " [TARGET] Let me return the favor and introduce you to my sisters. Rosaline and Helena, this is Miss Hopkins.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Lady and The Duke — Olivia Kelly; tertile=end; p=0.72**
>
> She's supposed to be home, taking care of my nephew, not following me to Town and hovering. [TARGET] Having an older sister is a great pain in the arse." " That's a horrible thing to say!"

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Fireworks — Lindsey Gray; tertile=end; p=0.69**
>
> The dresses, of course! [TARGET] See, this is why I’m glad I have a little sister to remind me of these things.” Sophie smiled as Shannon began to beam.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Keep Me Safe — Maya Banks; tertile=middle; p=0.70**
>
> Any of it. [TARGET] And you shouldn’t have to choose between a stranger and your sister.” His eyes suddenly blazed, his fury bursting through her mind.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · The Unimaginable — Dina Silver; tertile=end; p=0.69**
>
> He cocked his head to the side, his eyes downturned. “ [TARGET] Your sister and your family deserve to have you back with them. And safe.” “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Blood Spirit — Gabrielle Bisset; tertile=middle; p=0.64**
>
> She sat beside her on the bed and smiled. " [TARGET] You're just like my sister was. I never could say no to her either." "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Turning Back — J.A. Huss; tertile=end; p=0.56**
>
> And every one of them is married but me. [TARGET] My baby sister, Keren, she already has three kids and she’s twenty-four. So—you’re wrong.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Turning Back — J.A. Huss; tertile=end; p=0.60**
>
> Is this why you like to share? [TARGET] It’s something you’re used to—growing up with all those siblings.” I shrug. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Turning Back — J.A. Huss; tertile=end; p=0.42**
>
> They disappeared into the bedroom. [TARGET] Told us girls to play dolls. I can even remember those dolls.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Cera's Place — Elizabeth McKenna; tertile=middle; p=0.48**
>
> My parents died before the war. [TARGET] My sister’s still there with her husband, who’s a copper, and their three kids. My father was also a copper, before he was a politician.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Inhale — Kendall Grey; tertile=begin; p=0.49**
>
> The OWT woman’s lips curled into a slight, taunting smile as if to say, “Check.” [TARGET] Yeah, well, there’d be no checkmate, sister. Big funding or not, Zoe wouldn’t be upstaged by this woman or anyone else.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Inhale — Kendall Grey; tertile=begin; p=0.66**
>
> Man, those blue eyes and that flowery scent… She was the sort of woman he’d dreamed of having as a teenager. [TARGET] Like a best mate’s sister. Hot, but off-limits.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Inhale — Kendall Grey; tertile=middle; p=0.44**
>
> Tell Incendius Gavin says hello.” “ [TARGET] Fuck you, Sentinel.” The Fyre twisted within his grip, but Gavin held him steady as he willed his hydrogen and oxygen molecules into the shape of a cannon within his sternum.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 226 — Eyes Closed on Command

- **Label:** Eyes Closed on Command
- **Taxonomy:** 3.3 — Ambivalence & Internal Conflict
- **Cliff's delta:** +0.1250 [+0.1016, +0.1439] — small — more in HIGH-rated
- **Mean share:** high 0.187% vs low 0.139% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 183 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** drift, wrists, plastic, anticipation, tense, narrow, faces, closed
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. i blink rapidly, trying to wrest the salty water from my eyes.

> 2. lights began to blink inside the chamber, so i closed my eyes.

> 3. i blink my eyes open against bright lights.

**Stage-08 / Stage-07 snippets**

> 1. i closed my eyes as it all hit me at once.

> 2. keep your eyes closed until i tell you to do otherwise.” “

> 3. feeling tired all of a sudden, i closed my eyes.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 230 — Tongue and Hands After Climax

- **Label:** Tongue and Hands After Climax
- **Taxonomy:** 2.3 — Explicit Sexual Acts
- **Cliff's delta:** +0.1249 [+0.1041, +0.1454] — small — more in HIGH-rated
- **Mean share:** high 0.084% vs low 0.072% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 179 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** jace, sawyer, jacen, link, quent, hawkes, binds, parker, mate
- **KeyBERT:** flinched, nerves, smirked, nods, emotions, moaning, wound, sucked, dared, reaction
- **POS:** sucks, makeshift, contrast, addition, handful, internal, actual, exquisite, desperation, choices
- **MMR:** moaning, makeshift, dared, testing, heaved, swirling, choices, grumbled, shed, laying

**BERTopic representative docs**

> 1. 116 the link that binds dawn h. hawkes

> 2. thankfully, jace was proved wrong when his mate 101 the link that binds dawn h. hawkes slammed open the door.

> 3. 137 the link that binds dawn h. hawkes * * * * finding the closet debra had pointed him to, jace grabbed hold of his mate and pushed him inside, slamming the door shut behind them.

**Stage-08 / Stage-07 snippets**

> 1. jacen palms the curve of liam’s ass as his tongue delves back into jacen’s mouth, into the same hot cavern that his hardened cock had ridden to an exquisite climax not so very long ago, darting in and out of it, moaning when jacen sucks on it, then pushes back for more of liam’s sweetness.

> 2. [person] up into the contact, grabbing a handful of jacen’s hair and moaning loudly as jacen nips and sucks and marks him, leaving a dark bruise. “

> 3. sawyer made a choice because of choices that i’ve made and he...it was too much for him.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_D; thin cells CELL_C; 9 examples from 8 books; ±1 context on 9_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · The Winter King — C.L. Wilson; tertile=end; p=0.62**
>
> Clearly, Blazing judged Falcon and found him lacking.” [TARGET] She switched her glare to her brother, and added, “Maybe he should have spent more time trying to emulate Roland’s noble qualities—like honor, generosity, and self-sacrifice—instead of murdering, thieving, and whoring his way to the sword’s hiding place!” “ You traitorous little bitch!”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · The Winter King — C.L. Wilson; tertile=end; p=0.55**
>
> He looked like he wanted to hit something. [TARGET] For a moment, she thought it might be her, but Falcon hadn’t become that much like their father yet. “ I didn’t mean for Hillje to happen, all right?

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Entangled Souls — Felicia Tatum; tertile=middle; p=0.60**
>
> If I hadn’t been so distressed over the Cade situation, I probably would have stopped to laugh and take a picture. [TARGET] Wiping my palms on my pants, I twisted the knob and greeted Cade before I even saw him. “ Cade, are you okay?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Seduce Me — Ryan Michele; tertile=end; p=0.79**
>
> Dad shut the fuck up!” [TARGET] Jace yells and Rhys slams his fist into his gut. “ What do these men want, Jace?” “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Skin Game — Ava Gray; tertile=end; p=0.45**
>
> If they saw a chance, they'd take Serrano out, but they were hamstrung by not knowing where he'd stashed Mia. [TARGET] Reyes thought he had some failsafe in place--if the guards didn't hear from Serrano at a certain time, they'd kill her and clean up the scene. Therefore, the primary objective was to get into security and make copies of the logs.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Taste — Mickie B. Ashling; tertile=end; p=0.56**
>
> [TARGET] Epilogue “Well, my Corbin, everything worked out,” Camille purred next to him. “ We broke them, and we have a Redwood prince.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Isherwood — Missy Welsh; tertile=begin; p=0.47**
>
> There, at the end of the driveway, was a gray-colored wolf. [TARGET] Cas stared, trying to get a feel for the other's intentions, rank, anything that could tell him whether to stay and chat or run fast. With the wind not in Cas's favor, he could only speculate.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · From Venice with Love — Alison Roberts; tertile=begin; p=0.58**
>
> Because of the trouble he’d unwittingly caused for her? [TARGET] For another, long moment Nico kept staring, unsure of how to unravel the conflicting emotions being stirred in his own gut. Why did he feel such a strong urge to try and help this prickly, complicated woman?

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · The Prince's Psalm — Eric Shaw Quinn; tertile=end; p=0.43**
>
> Lost his mind, maybe, but not his face.” “ [TARGET] Baal and Dagon,” the guard swore. “ This is our lucky day, isn’t it?” “

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 162 — Struggling to Catch Breath

- **Label:** Struggling to Catch Breath
- **Taxonomy:** 1.1 — Body Parts & Physical Reactions
- **Cliff's delta:** +0.1242 [+0.1006, +0.1480] — small — more in HIGH-rated
- **Mean share:** high 0.276% vs low 0.218% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 250 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** breaths, lungs, internal, gasp, moaning, stool, exchange, insides, sentence, damp
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. but i can breathe now.”

> 2. didn’t seem to breathe.

> 3. and i can’t breathe.

**Stage-08 / Stage-07 snippets**

> 1. ragged, unsteady breaths grated from my lungs.

> 2. we’ll just stop moving until you catch your breath.

> 3. you’ll have to hold your breath through the thick of it.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 124 — Scooped Up in A Tight Hug

- **Label:** Scooped Up in A Tight Hug
- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Cliff's delta:** +0.1240 [+0.1024, +0.1437] — small — more in HIGH-rated
- **Mean share:** high 0.192% vs low 0.164% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 308 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** hug, hugged, hugging, gave, tightly, tight, arms, hugs, quick, embrace
- **KeyBERT:** hugged, affection, greeted, fiercely, tightly, cried, squeeze, patted, nods, welcoming
- **POS:** reassuring, sweep, decades, affection, enormous, measure, promises, sideways, crowd, huge
- **MMR:** hugged, reassuring, welcoming, bo, eagerly, heaved, fiercely, strolled, fluttered, draped

**BERTopic representative docs**

> 1. jane hugged him. “

> 2. he hugged her back. “

> 3. brandy hugged her. “

**Stage-08 / Stage-07 snippets**

> 1. emma followed suit, and rebecca scooped her up in her arms and hugged her tight.

> 2. he hugged her back.

> 3. i stood up with her and hugged her. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 16 examples from 4 books; ±1 context on 16_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Other packet sentences** (not tagged CELL_A–D)

> 1. [POS_001] But, John, it’s been a year.” [TARGET] Walking over to him, she put her arms around his waist and hugged him. “ John, I want to believe there were people in your life before I found you who are looking for you.

> 2. [POS_001] Nah.” [TARGET] She patted his leg and leaned more into the comfort of his embrace. “ I’m a bad influence.

> 3. [POS_001] His throat worked, and when he glanced over at her, a whisper of vulnerability touched his features. [TARGET] She wanted to lay her head on his shoulder and hug him. To touch warm skin and breathe in his spicy scent, which teased her senses even now.

> 4. [POS_001] You always were the cleanest one in the family.” [TARGET] Jasmine wrapped her arms around him in a tight hug. “ Thank you, Mitch.” “

> 5. [POS_001] Nestling against John even more, Gretchen got the response she wanted. [TARGET] He hugged her even tighter and kissed her forehead. “ You know, I don’t think I ever told you how wonderful dinner was,” Gretchen said. “

> 6. [POS_002] Yes,” Colin whispered. [TARGET] Amanda put her arm around him and gave him a hug. “ It’s perfectly normal to have doubts and questions.

> 7. [POS_003] She’s tiny and her raven-colored hair is dusted with gray. [TARGET] Mia flings her arms around her neck and hugs her tightly. “ Who’s that?”

> 8. [POS_003] Mia squeals with delight and runs toward me, abandoning her cartload of luggage. [TARGET] Throwing her arms around my neck, she hugs me tightly. “ I’ve missed you,” she says. “

> 9. [POS_003] Kate,” I mutter, to be polite. [TARGET] Elliot hugs Ana, holding her for a moment too long. “ Hi, Ana,” he says, all fucking smiles. “

> 10. [POS_003] She beams at both of us. [TARGET] He hugs her tightly and thaws immediately. “ Happy birthday, darling,” she says softly, closing her eyes in his embrace. “

> 11. [POS_003] Thank you.” [TARGET] I give her a hug and she hugs me back. “ I knew it would make you laugh.”

> 12. [POS_004] She’s tiny and her raven-colored hair is dusted with gray. [TARGET] Mia flings her arms around her neck and hugs her tightly. “ Who’s that?”

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 370 — Tattoos Revealed and Judged

- **Label:** Tattoos Revealed and Judged
- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Cliff's delta:** +0.1193 [+0.0982, +0.1397] — small — more in HIGH-rated
- **Mean share:** high 0.066% vs low 0.049% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 106 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** tattoo, tattoos, tattooed, parlor, sleeve, ink, tracing, covered, neck, shirt
- **KeyBERT:** reveal, revealing, fingertips, worn, evidence, absently
- **POS:** sleeve, visits, contrast, pattern, percent, sized, lighting, elbows, anxious, issue
- **MMR:** sleeve, absently, contrast, elbows, revealing, distracted, evidence, worn, emotions, stretched

**BERTopic representative docs**

> 1. the man on her right sported a tattoo sleeve on one arm and splashes of bright red highlights contrasted with the rest of his spiky black hair.

> 2. he traced travis's tattoo absently, admiring its bold lines and the taut muscles beneath the ink.

> 3. there’s a giant black flag behind the bar with the death layer mc colors and rockers, just like bane’s massive back tattoo.

**Stage-08 / Stage-07 snippets**

> 1. if she says she’s disgusted by the tattoos, my dick will deflate so fast it’ll be some sort of record.

> 2. whatever crucial moments we’ll have from now on, all of them will go into this one tattoo.

> 3. you can tell your boss he’ll never win, and i’ve got the tattoo to prove it.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_D; 12 examples from 11 books; ±1 context on 12_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Beneath This Mask — Meghan March; tertile=begin; p=0.70**
>
> The tangles of black were interspersed with sections dyed deep red and purple. [TARGET] Tattoos started at her shoulders and continued down to her wrists. Some were words, others intricate black and gray drawings.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Mad World — Kate L. Mary; tertile=end; p=0.54**
>
> I yank his sleeve up and see that he’s right. [TARGET] The bullet left a two inch streak across his left bicep, right under the Confederate flag tattoo. “ It looks okay.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Landon's Obsession- Sara Hess — Sara Hess; tertile=end; p=0.73**
>
> With his foot he dragged the blanket up and over us. [TARGET] I found the energy to lazily trace the tattoo on his chest. “ If I ever get brave enough, I want you to draw a tattoo just for me.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Absinthe of Malice — Rhys Ford; tertile=end; p=0.58**
>
> The sunken hollow of his cheeks was at odds with the pink, fleshy bags beneath his hard, glittering eyes. [TARGET] His messy crop of hair was more wiry silver than black, and as Miki tugged at the sweatshirt’s hood, he pulled apart the top’s zipper, exposing a patchwork quilt of mottled blue tattoos running down his crepe-like wattle and spotted neck. Including one that looked so much like the one Miki had on his arm it shocked him speechless to see it.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Guarded Secrets — Leann Harris; tertile=middle; p=0.69**
>
> That’s him. [TARGET] When I peeked out the window, I noticed the guy had this really nasty-looking snake tattooed on his forearm.” She handed the picture back to Dave.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · The Fly House — Misty Paquette / Misty Provencher; tertile=begin; p=0.53**
>
> You're okay with the paps snapping photos of my bumper stickers? [TARGET] I've got some new ones on there..." When her bumper was full, she'd started tattooing the back panels of her decrepit Dodge Ram and slowly, the stickers had consumed her ride’s whole tailgate. They were starting to slop over onto the back panels.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Starting Over — Jen Silver; tertile=middle; p=0.72**
>
> Each ear had several piercings with a recent one at the edge of one eyebrow. [TARGET] The sleeveless top she wore revealed tattoos on each shoulder and a larger one down her left arm. But it was the dark circles under her eyes that made her look worse than Ellie felt. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · His Young Queen — Tiff P. Raine; tertile=begin; p=0.61**
>
> How had she forgotten the square cut of his goateed jaw? [TARGET] And had her subconscious seriously neglected to add the thickness of his inked neck to her many dreams, and that gorgeous tattoo of the Grim Reaper holding up a royal flush? It stretched from below his left ear to disappear under his shirt.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Loving the Highlander — Janet Chapman; tertile=end; p=0.40**
>
> �Faol. [TARGET] T�as. Falbh,� he added, waving the wolf toward the exit of the pool, then walking through the towering trees himself.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Just One Kiss — Susan Mallery; tertile=end; p=0.11**
>
> This edition published by arrangement with Harlequin Books S.A. ® and ™ are trademarks of the publisher. [TARGET] Trademarks indicated with ® are registered in the United States Patent and Trademark Office, the Canadian Trade Marks Office and in other countries. www.Harlequin.com

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Just One Kiss — Susan Mallery; tertile=middle; p=0.63**
>
> Gideon looked like a dozen other guys Justice knew. [TARGET] Scarred, tattooed and dangerous. He had a scar by his eyebrow, but Justice was sure there were others.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Christmas with the Houstons — D. Kelly; tertile=end; p=0.59**
>
> He’s been wanting to get the kids’ names tattooed on him somewhere for a while so I got him a gift certificate to go see Ben. [TARGET] He’s had my name tattooed on his arm since our freshman year of college. I thought he was crazy, but I don’t think I’d ever seen him more proud of something. “

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 187 — Admitting Everything Has Gone Wrong

- **Label:** Admitting Everything Has Gone Wrong
- **Taxonomy:** uncertain_interpretable — Interpretable but Not Axis-Safe
- **Cliff's delta:** +0.1176 [+0.0934, +0.1387] — small — more in HIGH-rated
- **Mean share:** high 0.252% vs low 0.218% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 219 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** addition, occasional, regular, task, emotional, pregnant
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. i don’t think i could handle that.” “

> 2. i don’t know if i can handle it right now.”

> 3. i don’t know how you handle it all.”

**Stage-08 / Stage-07 snippets**

> 1. i’ve got things handled here.

> 2. it’ll be handled by then.”

> 3. we’ve messed up everything.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 168 — Ready to Begin When Told

- **Label:** Ready to Begin When Told
- **Taxonomy:** 9.2 — Promise, Vow & Future-Tense Speech Acts
- **Cliff's delta:** +0.1124 [+0.0916, +0.1356] — small — more in HIGH-rated
- **Mean share:** high 0.363% vs low 0.337% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 246 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** fitting, sentence, sir
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. please, just let me finish.

> 2. i’ll just finish up here first.”

> 3. now you have to finish it or it will be finished for you.” “

**Stage-08 / Stage-07 snippets**

> 1. but i’ll start first.

> 2. we’ll start there and see where it goes.”

> 3. we’ll let you know when we’re done,” [person] said.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 143 — Complaining About Family Pressure

- **Label:** Complaining About Family Pressure
- **Taxonomy:** 5.1 — Family, Kinship & Parenthood
- **Cliff's delta:** +0.1120 [+0.0888, +0.1332] — small — more in HIGH-rated
- **Mean share:** high 0.346% vs low 0.304% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 271 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** family, parents, your, families, my, are, our, we, know, part
- **KeyBERT:** admit, experience, folks, dealing
- **POS:** failure, slightest, folks, distress, typical, options, strained, disappointed, member, extended
- **MMR:** failure, distress, compared, survived, options, dealing, provided, strained, members, pressure

**BERTopic representative docs**

> 1. would you like to see your parents again?"

> 2. what do you know about your parents?” “

> 3. do you know either of my parents?

**Stage-08 / Stage-07 snippets**

> 1. and i've no sense of family.

> 2. you’ve flown in the face of tradition with your family, you’ve bucked the system.

> 3. be sure to tell my parents that this is who i’ve had to deal with for the past month.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Second of All — Genevieve Dewey; tertile=begin; p=0.66**
>
> We demand they come true and everyone else falls in line or we make them fall in line. [TARGET] Now, the fact you’ve come here tells me you haven’t forgotten what’s most important in life, and that’s family. Nothing should come before your loyalty to your family.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · The Best of Intentions — Renee   Peterson; tertile=begin; p=0.59**
>
> Eventually Aunt Liza and he reconciled and he moved his family here to Louisiana. [TARGET] My parents tried to stay together for me, but a year later they divorced. My dad got involved in some shady business dealings that made him a fortune, but created a lot of enemies.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Desert Flower — C.P. Lesley; tertile=middle; p=0.67**
>
> But as I stood in the middle of Harley Street, I was exactly that all alone. [TARGET] I have no hard feelings toward my aunt and uncle, though; they’re still my family. They gave me an opportunity by bringing me to London, and for that I will forever be grateful.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · The Florentine Bridge — Vanessa Carnevale; tertile=middle; p=0.68**
>
> You’re here now,’ I say, squeezing his hand. [TARGET] I can’t help thinking about my own parents and how I still haven’t told them how much I miss them, how much they mean to me, how much I wish I had handled things better. I make a mental note to call them as soon as we return to Florence.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · The Sins of the Mother — Danielle Steel; tertile=begin; p=0.65**
>
> That’s a hard one. [TARGET] You’re lucky you have parents who like each other so much. But I can see that it would make you feel left out.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Sheikh's Destiny — Olivia Gates; tertile=end; p=0.65**
>
> But you were not only right in predicting the outcome of me ‘shredding your ironclad control,’ but in anticipating what I’d do, even if I discovered your plot prematurely. [TARGET] You knew me well enough to realize that even if I kept saying I don’t care about my family, I do. Even if I don’t care about tradition, they do.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Dianthe Rising — J.B.  Miller; tertile=end; p=0.68**
>
> Consider it as starting a new adventure in a new home with your mates. [TARGET] You have your own family now and it’s time to move on.” Chucking me under my chin, he added, “I don’t know how much longer we would all have been able to fit in.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_014 · You May Kiss the Bride — Lisa Berne; tertile=end; p=0.68**
>
> I’m hardly in a position to be judging you! [TARGET] Besides, you’re being realistic, and you’re thinking of your family.” “ That’s it.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Dreamspell — Tamara Leigh; tertile=end; p=0.49**
>
> Her heart tugged. [TARGET] These boys needed a mother to care for them and see to those things a village woman with her own children would care nothing of. But not me, Lark reminded herself.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Dreamspell — Tamara Leigh; tertile=end; p=0.50**
>
> Remembering what he had done the morning he found his squire strung from a tree, he told himself it was better that the truth of the betrayal die with the betrayer. [TARGET] No family ought to suffer such dishonor, not even a family that boasted one such as Annyn Bretanne. Thus, he had falsified—and now felt the brunt of God’s displeasure.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Avion — Eve Langlais; tertile=end; p=0.36**
>
> Wanna bet it tastes like chicken?” [TARGET] With the danger behind them, the cyborgs returned to their usual carefree bantering, some scowling, some smiling, but all together, all individuals and yet part of a family. A family on its way home.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · A Siren’s Song — Billi Jean; tertile=end; p=0.58**
>
> Can you send me back to her, now?” “ [TARGET] As you wish, but remember, your loyalty still remains with me, as well as your new…family.” Family?

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · The King's Mistress — Terri Brisbin; tertile=end; p=0.62**
>
> She still did not trust him. “ [TARGET] My mother reminded me of two cousins in my father’s family who might be of a mind to come and live here. So that you may have your own companions when she leaves.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · The Mudlark — Delle Jacobs; tertile=middle; p=0.42**
>
> How fortunate that his grandfather had had the foresight to protect it from his mother's extravagance. [TARGET] Still, even with the small competence from his mother's estate and his commission, he would be hard put to support a family. He dreamed odd dreams as he slept, dreams of an elfin creature that enchanted him, led him where she would, while he followed, willingly, no, not willingly, helplessly.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Best Lesbian Erotica 2011 — Kathleen Warnock; tertile=end; p=0.33**
>
> NO CLIMBING INTO VATS. [TARGET] CHILDREN MUST BE ACCOMPANIED BY AN ADULT AT ALL TIMES. “ Should we wait for the next one?” “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Ridge — Adriane Leigh; tertile=middle; p=0.49**
>
> Not that I didn’t have a choice, I was just choosing to make the right one. [TARGET] A kid deserved both parents in his life, and Amy and I weren’t bad together; we were good enough. We could raise a kid.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 248 — Arranging A Cover Story

- **Label:** Arranging A Cover Story
- **Taxonomy:** 4.3 — Secrets, Misunderstandings & Hidden Information
- **Cliff's delta:** +0.1110 [+0.0926, +0.1312] — small — more in HIGH-rated
- **Mean share:** high 0.098% vs low 0.088% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 164 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** callie, hanna, sister, said, pickpocketed, emulating, leslea, afternooner
- **KeyBERT:** behavior, overheard, crushed, upset, pregnant, admit, dr, problems, considering, ok
- **POS:** concept, activities, notion, treatment, potential, tracks, options, behavior, ex, lack
- **MMR:** concept, wasting, activities, overheard, feeding, treatment, crushed, apologize, behavior, problems

**BERTopic representative docs**

> 1. she saw me at the toy store and helped me play with the dollhouses there, and then she came here to get her face painted, too, but then she went to talk to miss hannah, you know, my teacher from sunday school.”

> 2. hannah chafed at the notion that she had to tell that lying, cheating scum anything, but she was not in a position to argue with holly, and part of her treatment and recovery was to come clean with everyone who had ever mattered to her.

> 3. i don’t like leaving her to do this on her own,” conner said, both relieved there was a plan and frustrated that he wasn’t going to be on hand to make sure hannah got out of the lab. “

**Stage-08 / Stage-07 snippets**

> 1. i can attach myself to callie as a potential suitor, even with the distant cousin story you’ve decided to run with.

> 2. i'll just let hannah know she won't have to watch him after today.

> 3. it means you’ll probably bump into him too if you see more of hannah.’

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_D; 11 examples from 10 books; ±1 context on 10_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Ciao — Bethany Lopez; tertile=middle; p=0.56**
>
> Doesn’t being there make him think of me? [TARGET] Anyway, I was totally pissed about that, and about Jess pinching my arm, when Cassie dropped another bomb on me… She said that she is “Falling in love with Jimmy!!!!” What??

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Step — Cindy Paterson; tertile=begin; p=0.72**
>
> Why , Rayne? [TARGET] Why did they want you to be Hannah?” “ I . . .

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Nemesis — Lisa Clark O'Neill; tertile=middle; p=0.61**
>
> I got a real good look at it the other night.” [TARGET] Kathleen frowned, not quite ready to be cavalier about the harrowing situation Sadie’d found herself in with those intruders. But before she could delve into it further, a curvaceous brunette approached their table.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Revenge — Shelly Bell; tertile=middle; p=0.71**
>
> Could she? [TARGET] Last night she’d felt guilty for indirectly leading Hannah to her apartment. “ Honestly, I—” Her cell buzzed in her pocket. “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Picture Perfect — Bethany Brown; tertile=begin; p=0.66**
>
> Shit.” “ [TARGET] That Hannah’s boyfriend was sleeping with apparently the whole time they were going out? And dumped me when he saw me for the first time in a year?” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · The Dark Djinn — J.J. Timmins; tertile=end; p=0.58**
>
> I don’t want to, but it’s there.” [TARGET] Tara thought of her own feelings for Zach, which were there even when she didn’t want them to be. She said, “I know what you mean.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Watermelon Summer — Anna Hess; tertile=end; p=0.49**
>
> Not that Jacob was my boyfriend, but he'd promised Arvil he'd ask me on a date soon, right?) [TARGET] Yet, despite her feelings, Kat had been kind enough to keep her opinion about Jacob to herself after her first few warnings were ignored, so it seemed catty for me to pick at Drew's behavior. All of these thoughts spun through my head in a matter of seconds, and my words petered out before I could launch into my request—that Kat whip her boyfriend into shape or ask him to leave. "

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Never Always Sometimes — Adi Alsaid; tertile=end; p=0.58**
>
> She’d tensed up a little, the way she did when Julia said hi at school, those handful of times when they stood by making small talk. [TARGET] Gretchen had admitted to jealousy, but she’d insisted that she didn’t want Dave and Julia to stop being friends because of her. If it hadn’t been for Julia, the two of them might not be together at all.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Creed — Kristen Ashley; tertile=end; p=0.45**
>
> Now that was done, I was to meet the contact tonight and he would take me to where they held their stock of available humans. [TARGET] I would confirm the girl was there, make the deal and skedaddle then Hawk and the boys would swoop in and recover the girl. Easy.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Creed — Kristen Ashley; tertile=middle; p=0.48**
>
> You won’t regret it,” I promised Knight. “ [TARGET] Get me the details on Amy. Two minutes, Creed and I are on the road.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · The Warrior’s Pet — Stephanie West; tertile=begin; p=0.41**
>
> The Warrior's Pet Stephanie West

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 276 — Asking For A Moment

- **Label:** Asking For A Moment
- **Taxonomy:** 9.4 — Interior Monologue Particles & Self-Talk
- **Cliff's delta:** +0.1101 [+0.0930, +0.1304] — small — more in HIGH-rated
- **Mean share:** high 0.083% vs low 0.081% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 148 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** enthusiasm, benefit, appropriate, stares, affection, disappointed, sentence, amusement, emotional, ability
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. aiden’s private and professional lives collide when dawn's newest patient gets in trouble with the law.

> 2. to comprehend the events that had at some point unraveled right under his nose while he’d aimed desperately to spare aiden from harm.

> 3. he spoke to his pot, like he’d spoken to his knife or cutting board or whatever, every time he said something directed at ezra.

**Stage-08 / Stage-07 snippets**

> 1. i’ll be okay, i just need a minute,” aiden whispered.

> 2. aiden, i’ll let you know what transpires.

> 3. aiden asked, then quickly added, “god, sorry, lip zipped, swear, i’ll shut up.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

## More in low-rated books (5)

### Topic 218 — Resenting Someone More Attractive

- **Label:** Resenting Someone More Attractive
- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Cliff's delta:** -0.1453 [-0.1666, -0.1238] — small — more in LOW-rated
- **Mean share:** high 0.402% vs low 0.468% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 192 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** handsome, gorgeous, cute, beautiful, adorable, attractive, looked, man, good, looking
- **KeyBERT:** attractive, mister, highly, merely, intended, considered, poised, described, strangely, excited
- **POS:** attractive, mister, makeshift, potential, decent, features, intended, worst, comfortable, huge
- **MMR:** attractive, mister, makeshift, poised, dangerously, dangling, described, earned, snatched, built

**BERTopic representative docs**

> 1. he was a handsome and honorable man.

> 2. he really was a handsome man.

> 3. how could i even begin to like someone who was:  a) gorgeous, thereby making me, someone who until now was considered pretty decent looking, seem, at best, perfectly average, and, at worst, like the sibling who got beaten with the ugly stick;  b) paid huge bucks to roll around in the sand making out with equally gorgeous girls while i donned a hideous fluorescent orange apron, an equally hideous lime green baseball cap with an assortment of stuffed fruit dangling from the center in a makeshift pom-pom, and honed my smoothie- making skills for six bucks an hour;  c) a veteran of rehab, probably attended more 12-step programs than all the boy bands from the nineties combined, thought nothing of totaling a hundred-thousand-dollar sports car, and even managed to expose his pearly whites in his mug shots so that he looked like someone making a dentyne commercial instead of a criminal about to begin two hundred hours of community service, while i followed the rules or never caused my parents a day of worry, and yet they wouldn‘t even let me spend one lousy summer in europe, for god‘s sake.

**Stage-08 / Stage-07 snippets**

> 1. the human in charge of maintaining his harem was moderately dishevelled from the panic, but he was, as always, poised and visually attractive.

> 2. i think he’s still trying to prove that he is mister attractive and can make anyone fall in love with him.’ ‘

> 3. how could i even begin to like someone who was:  a) gorgeous, thereby making me, someone who until now was considered pretty decent looking, seem, at best, perfectly average, and, at worst, like the sibling who got beaten with the ugly stick;  b) paid huge bucks to roll around in the sand making out with equally gorgeous girls while i donned a hideous fluorescent orange apron, an equally hideous lime green baseball cap with an assortment of stuffed fruit dangling from the center in a makeshift pom-pom, and honed my smoothie- making skills for six bucks an hour;  c) a veteran of rehab, probably attended more 12-step programs than all the boy bands from the nineties combined, thought nothing of totaling a hundred-thousand-dollar sports car, and even managed to expose his pearly whites in his [person] shots so that he looked like someone making a dentyne commercial instead of a criminal about to begin two hundred hours of community service, while i followed the rules or never caused my parents a day of worry, and yet they wouldn‘t even let me spend one lousy summer in europe, for god‘s sake.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Destined for a Vampire — M. Leighton; tertile=begin; p=0.64**
>
> As I lay there, listening vigilantly, I began to fantasize about seeing Bo again —touching him, talking to him. [TARGET] I thought of his silky dark hair, his nearly-black walnut eyes, his perfectly-carved lips. It gave me cold chills just to think of feeling those lips on mine and hearing his voice again.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · One More Chance — Juan Miguel Sevilla; tertile=begin; p=0.69**
>
> I wouldn’t be able to resist him. [TARGET] Not now, when he not only remained the most fun person I had ever known, but so freaking gorgeous. Just his body alone was a wonder.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · An Unnatural Vice — K.J. Charles; tertile=begin; p=0.64**
>
> His hair was too long, and fell over his forehead; he seemed to be striving for the goatee Nathaniel had vaguely expected without having the wherewithal to achieve it; his plain coat was a little worn at the cuffs. [TARGET] He was the sort of man one would have passed in the street without noticing, except for his eyes. They were grey, large and luminous, almond-shaped with winging brows, and remarkably intent.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Ocean Submerged — MEL D; tertile=middle; p=0.58**
>
> She’s not ready and she’s staying with me,” I said, standing up to face the asshole that was getting under my skin. [TARGET] He looked like one of those sick motherfuckers who got caught on Dateline with Chris Hansen for preying on underage children. Thank God I was taller than he was because if I had to look up at him, I probably would have punched him in the face just because of that.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Slow Hands — Leslie Kelly; tertile=middle; p=0.67**
>
> Then he was there, beside her, all tan and masculine, wearing a loose-fitting T-shirt, swim trunks and leather flip-flops. [TARGET] He even had beautiful legs and feet for a man. She didn’t know what to say, so she said nothing, waiting for some sign from him.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Doc Featherstone's Return — Stephani Hecht; tertile=middle; p=0.63**
>
> Ash was nothing short of beautiful. [TARGET] Even while underweight and pale, he had an attraction that was both alluring and erotic at the same time. His pale skin made his dark lashes stand out all the more as they nearly fanned his cheekbones.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Brian's Mate — Hollis Shiloh; tertile=begin; p=0.54**
>
> Nope, I’m good.” [TARGET] The look he shot Brian was light and warm and friendly, but it held something different now, something warm and kindled, hotter than any habanero.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · Keeping His Commandments — Elle Keating; tertile=middle; p=0.67**
>
> So like me he had put in a lot of hours today. [TARGET] Although he appeared a little disheveled, probably due to the long day, with his tie loosened and his hair slightly rumpled he still looked handsome. “ No, it just seems to come naturally.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Bed of Roses — Nora Roberts; tertile=end; p=0.69**
>
> He shared those deep, midnight blue eyes with Parker, but though Laurel had known him all her life, she could rarely read what was behind them. [TARGET] He was, in her opinion, too handsome for his own good, too smooth for anyone else’s. He was also unflinchingly loyal, quietly generous, and annoyingly overprotective.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · When Passion Lies — J.K. Beck; tertile=middle; p=0.48**
>
> And he sure as hell hadn’t moved here so he could watch politicos trample all over a case. [TARGET] He’d look the other way for a lot of things. But not this.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Bad Boy Blake — Lorraine Nelson; tertile=begin; p=0.53**
>
> Big and broad, he stood about six feet, four inches to her six feet, one inch in heels. [TARGET] In tight jeans and black leather jacket, she found him rugged and handsome with a charm all his own, his bad-boy image and relaxed smile a real turn-on. When he’d asked her to dance for him, his voice tingled along her spine as if nimble fingers were at work.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Room for Just a Little Bit More — Beth Ehemann; tertile=end; p=0.50**
>
> Looking sharper than I’d ever seen him in his black tuxedo with a black vest underneath, slightly different from his groomsmen, who wore ice blue vests under their jackets. [TARGET] Brody stood tall, calm and cool as ever, until we locked eyes. That’s when the mood shifted from light to intense.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Cat's Quill — Anne Barwell; tertile=end; p=0.46**
>
> The only constant was the moon, staring down at him, not full but half. [TARGET] Just as he was now, not a part of this world but drawn to it, tied to it on some level because of his relationship with Cathal. They'd only known each other a short time, yet on some level it felt like a lifetime.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Marci's Desire — Sara Luck; tertile=middle; p=0.54**
>
> It’s a miracle I’m able to drift off and dream. [TARGET] Mateo Espinoza is the most attractive man I have ever seen this close up—and I would know, because I’ve seen some pretty damn good-looking men in my life. When you have brothers who play professional sports and when you spend your life working in a male-dominated industry, you’re bound to see enough perfect male specimens to curl your toes.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Once an Heiress — Elizabeth Boyce; tertile=begin; p=0.50**
>
> He was a boorish lout, even if he was devilishly good-looking. [TARGET] Handsome men were the worst sort, anyway — they knew they were in short supply, and were always insufferably full of themselves. Lily started to turn toward her promised dance partner.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Holding On To Love — A.E. Neal; tertile=begin; p=0.58**
>
> And I did, but someone needed to tell that to my body. [TARGET] Brody didn’t look like any guy I had ever seen before, but his intense green eyes, muscular body and mussed chestnut hair made me want to forget my preconceived notions of him. “ Yeah, I get it.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 197 — Lingering Farewell Kiss

- **Label:** Lingering Farewell Kiss
- **Taxonomy:** 2.2 — Kissing & Non-Explicit Affection
- **Cliff's delta:** -0.1313 [-0.1534, -0.1101] — small — more in LOW-rated
- **Mean share:** high 0.221% vs low 0.269% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 208 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** kiss, kissed, kissing, wanted, hadn, kisses, her, she, never, he
- **KeyBERT:** sentence, willing, sticking, lingering, anticipation, handful, urgency, curiosity, honestly, reaction
- **POS:** departure, urgency, repeat, spite, handful, separate, curiosity, sadness, sentence, anticipation
- **MMR:** departure, urgency, witnessed, spite, wipe, lingering, stirred, sentence, anticipation, parted

**BERTopic representative docs**

> 1. a kiss…” she’d kissed danny.

> 2. was he really kissing her?

> 3. he wanted to kiss her, in spite of the fact that kissing her was undoubtedly one of the most ill-considered ideas he had ever had.

**Stage-08 / Stage-07 snippets**

> 1. in an attempt to take away the sting of her hasty departure, she went to lirzhan and kissed him — no quick peck on the cheek, but a lingering touch of mouth against mouth as she tried to show that she was leaving because she had to, not because she wanted to. “

> 2. from what i’ve heard, she’s just lying around on her back, waiting for true love’s kiss.”

> 3. and that they’ve only kissed.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Romancing Mister Bridgerton — Julia Quinn; tertile=middle; p=0.81**
>
> He shouldn’t have kissed Penelope. [TARGET] It didn’t matter that he’d wanted to kiss her, even though he hadn’t even realized that he wanted to until right before she’d mentioned it. He still shouldn’t have kissed her .

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Two Timing the Boss — Christine Warner; tertile=middle; p=0.78**
>
> It had been a kiss. [TARGET] Though exciting, hot, and bone melting for her, it might have been an ordinary, even forgettable kiss for him. Farah brushed aside her fantasies and scanned the email, taking mental notes.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Night Thief — Lisa Kessler; tertile=begin; p=0.75**
>
> What was she thinking? [TARGET] Perhaps his kiss still had her off-balance, making her forget her mission was to rob him, not enjoy his company. Kane Bordeaux proved more intoxicating than French wine.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Getting His Hopes Up — Erin Nicholas; tertile=begin; p=0.76**
>
> She’d wrapped her arms around his neck and pressed her body to his as if she really was madly in love with him. [TARGET] And she was now kissing him as if maybe she’d forgotten she had never done more than smile at him across a bar. She seemed to remember a moment later.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Sensual Submission: Pursuit — Andre SanThomas; tertile=end; p=0.78**
>
> Adam groaned as she kissed him back. [TARGET] Her kiss was almost tentative, as if she wasn’t sure what she was doing, and that turned him on even more. He drew her tight up against him and she moaned again.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Dizzy — Nyrae Dawn; tertile=end; p=0.65**
>
> If he’d changed his mind, he would have said something, right? [TARGET] And now as much as the warmth of his lips is the most perfect thing ever, I just can’t kiss someone who doesn’t want more from me. The weight settles deeper down than just my chest.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Lawyer Up — Kate Allure; tertile=end; p=0.70**
>
> Two weeks had gone by since the final settlement filing and not a word. [TARGET] Clearly their kiss hadn’t wowed him, but Pat thought he would at least have approved of how she “solved the problem.” Thinking she might run into him or that he might even seek her out to compliment her creativity, Pat had dressed to impress every day right down to her sexy pumps.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · A Gentleman's Game — Theresa Romain; tertile=middle; p=0.76**
>
> To see him differently. [TARGET] To keep kissing him as though she had never liked anything so much, as though she were helpless to stop. As though she were drunk on the pleasure of it.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Stilettos and Steel — Jeri Estes; tertile=end; p=0.58**
>
> Now grab your mink, it’s chilly outside.” [TARGET] As if she hadn’t heard a word I said, she said to me tenderly, “Kiss me,” “We’ll never get out of here,” I growled. I grabbed her and kissed her long and passionately.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Stilettos and Steel — Jeri Estes; tertile=begin; p=0.65**
>
> Sex is just business. [TARGET] I knew that my girl would never kiss a trick; that would be intimate. “ If she’s gonna work, it might as well be with you.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Savage Savior — Charleigh Rose; tertile=middle; p=0.53**
>
> Mom kicked me out when I was eleven because I didn’t get along with her ex-boyfriend. [TARGET] I didn’t get along with her ex-boyfriend because he tried to touch me twice while I was asleep. It was all a big mess.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Blindsided — Kaylea Cross; tertile=end; p=0.72**
>
> Need you,” he muttered, leaning in to close his teeth on the sensitive juncture of her neck and shoulder. [TARGET] He wanted to nip and lick and kiss every inch of her, eat her right up. Khalia pushed firmly on his shoulder, trying to get him to turn onto his back, and he relented with a frustrated sigh.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · The Sheik Who Loved Me — Loreth Anne White; tertile=middle; p=0.62**
>
> She’s in bed.” [TARGET] David spontaneously kissed her on the cheek. “ She asked me to kiss you goodnight.” “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Miss Match — Wendy Toliver; tertile=end; p=0.48**
>
> Oh, WOW. [TARGET] All the kisses I’ve watched over and over again on TV shows or in movies, all the articles I’ve read on what kisses really mean and what type should be given in specific situations, all the times I’ve spied on people making out in the halls and under the bleachers…none of it matters anymore. Because I’m not Miss Match.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · Rebound — Mercy Walker; tertile=end; p=0.57**
>
> He laughs, "I'm not kidding, you were like The Terminator." [TARGET] I remember something and frown, "I'm pretty sure the last time you called me that, you also said I was a bitch and kissing me was a mistake." His mouth hangs open for a second.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · Rebound — Mercy Walker; tertile=middle; p=0.59**
>
> He just stopped." [TARGET] I can hear the tears I won't look at, "Did you kiss him goodbye?" I shake my head, "I couldn’t.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 104 — Stepping Out of Panties and Jeans

- **Label:** Stepping Out of Panties and Jeans
- **Taxonomy:** 2.1 — Attraction & Sexual Tension
- **Cliff's delta:** -0.1296 [-0.1491, -0.1056] — small — more in LOW-rated
- **Mean share:** high 0.339% vs low 0.414% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 353 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** jeans, pants, shirt, zipper, panties, button, buttons, bra, undid, pulled
- **KeyBERT:** ankles, ankle, stumbled, dangling, crouched, tugged, fumbled, loose, purse, loosened
- **POS:** ankles, ankle, snaps, edges, items, nearest, movement, thigh, waist
- **MMR:** fumbled, plucked, ankle, loosened, snaps, tearing, hitched, dangling, ripping, instinctively

**BERTopic representative docs**

> 1. he tugged on the pants, pulling them down, and genna kicked them off along with her shoes, leaving her in nothing but her black bra and lacy underwear.

> 2. i reached for the buttons on his jeans.

> 3. pants,” she repeated, reaching down, her fingers fumbling on the button of her jeans. “

**Stage-08 / Stage-07 snippets**

> 1. she looked into his gaze as she took her panties to her ankles and stepped out.

> 2. deliberately julie ignored the order, and instead crouched down to remove the shorts dangling around her ankles and to untie her shoes.

> 3. once on her porch, she shed his t shirt and threw that at him too, he fumbled trying to quickly get it off his face.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Deception — Lisa Clark O'Neill; tertile=end; p=0.76**
>
> Wind whistled down the passageway, but did little to cool the heat which engulfed him. [TARGET] His hands slid under her jacket, over her gently rounded hips, fingers bunching the silky blouse she wore until it slipped free of the waistband of her skirt. The skin beneath it was satiny smooth, warm to the touch.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Mirage Beyond Flames — Melinda De Ross; tertile=middle; p=0.66**
>
> She grazed her teeth over his throat and a rough moan escaped his lips. [TARGET] Encouraged, she stroked his strong torso, then pulled his T-shirt over his head and threw it on the floor. When he felt her hot tongue over his chest, tasting his nipples, any shadow of control left him.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Lincoln Hospital — Cassia Brightmore; tertile=middle; p=0.72**
>
> They all fucking want it, fucking whores,” he mumbled. [TARGET] He got his jeans down to his ankles and no matter how hard she bucked, she felt the tip of him at her entrance and she began to scream, not caring if he cut her. Suddenly, his weight was lifted off her and a gush of cold air hit her.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Jago — Catherine Lievens; tertile=middle; p=0.67**
>
> He stopped only once he was in his room. [TARGET] He quickly stripped and neatly folded his clothes, climbed on his bed, pulled the covers over his head and shifted. The world around him became bigger, larger, and he pushed his nose under his pillow.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Alien Embrace — Tracy St. John; tertile=begin; p=0.78**
>
> His breath puffed in her ear faster. [TARGET] He pulled at her shirt, untucking it from the skirt’s waistband, allowing his hands access to the flesh of her torso. He jerked her bra up towards her neck, spilling her heavy breasts out.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Sleeping with the Frenemy — K.T. Grant; tertile=begin; p=0.69**
>
> When Deborah tried to cross her legs, the belly chain got caught and pinched her stomach. [TARGET] She hissed and tried to shift in a way that wouldn't be too risqué since her skirt was quite short and at Gen's urging, she had gone commando: no bra or thong. “ What is it, dearling?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Hardcore Cowboys — Stacey Espino; tertile=middle; p=0.74**
>
> She wasn’t sure what would happen when all that wanton energy collected in her cunt, but she hoped the Carson brothers were experienced enough to guide her through it. [TARGET] Once Samantha was free of her shirt, Cord bent over and pushed her pants down her hips until they dropped to the floor at her ankles. She hadn’t noticed his tattoo.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Frosh: First Blush — Monica B. Wagner; tertile=begin; p=0.76**
>
> But her dress slid down, too, covering her upper thighs a bit, and she was driving him crazy. [TARGET] His jeans felt tighter and tighter by his hips, and he watched how her panties rolled down her calves and onto the carpet. She reached back and unhooked her strapless bra, then tossed it over some box.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Wildest Dreams — Kristen Ashley; tertile=middle; p=0.67**
>
> Yes, yes, yes. [TARGET] My hands went to his sweater at the back, clenching in, pulling up as his fingers went to the gusset of my undies, yanking them free. “ Hurry,” I whispered. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · In the Shadow of the Heron — Carrie-Anne O'Driscoll; tertile=begin; p=0.50**
>
> Carina was her old self again. [TARGET] With the movements of a professional stripper, she pulled her top over her head, her shorts slowly down and stood there in a tight, bright red bikini, which hid very little of her perfectly proportioned figure. She put on a beaming smile, moved her hips coquettishly and said: “I’m going swimming.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Just Breathe — Martha Sweeney; tertile=begin; p=0.56**
>
> Brittany suddenly jumped at his free hand as he swung back to give another excruciating blow. [TARGET] He flicked her off his arm like she was an ant, and during that brief moment of distraction, I was able to clip him in his groin with my right knee. Dean slumped to the floor wailing in pain.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Surviving You — Dawn A. Keane; tertile=begin; p=0.66**
>
> With a swift unclipping of my bra, his hands were on me, kneading, grasping, hungry. [TARGET] I unbuttoned his jeans and I slid my hand down his boxers; my jeans were also gone in a flash. Logan’s tongue plunged deeply into my mouth;, the passion devoured me, shock waves shooting through my whole body.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Bon Voyage — Michelle Betham; tertile=begin; p=0.63**
>
> The last thing she needed to be thinking about tonight was her mother. [TARGET] And then, almost as though she were acting on some kind of auto-pilot, Aimee slowly slipped her dress down over her breasts, letting it slide down past her hips until it fell to the floor and she kicked it away, suddenly feeling quite exposed as she stood there – in front of Danny Johnson – in just her underwear and her strappy high heels. Although, the underwear was pretty good stuff, she had to admit.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Bon Voyage — Michelle Betham; tertile=begin; p=0.64**
>
> Could’ve been a real ego-batterer that.’ [TARGET] Aimee smiled too, not really knowing what to do next so she moved away from him, quickly pulling herself back together, grabbing her scattered clothes up off the cabin floor and hurriedly dressing. ‘ Aimee…’ She turned to look at him, running her fingers through her hair.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Echoes — Michelle Rowen; tertile=middle; p=0.63**
>
> Lucky you.” [TARGET] He pulled a clean handkerchief out of the pocket of his jeans and used it to wipe at the wound on Ethan’s head. “ Is he really going to be okay?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · Calling California — J.P. Grider; tertile=middle; p=0.59**
>
> My erection pulses in rhythm with her heart beat and I can no longer keep myself from being inside her. [TARGET] Ripping open the packet I'd tossed on the bed, I quickly slide it on before pulling on the string of her panties and tearing the fabric right off. Her legs naturally rise and fold around my waist, and with no effort at all, as if my body were designed for the sole purpose of making love to Calista Parker, I slip inside her and lose myself in Heaven.

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 8

- **Label:** **UNLABELED** (absent from Stage08 / topic_lookup)
- **Taxonomy:** ?
- **Cliff's delta:** -0.1167 [-0.1382, -0.0949] — small — more in LOW-rated
- **Mean share:** high 0.480% vs low 0.578% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 1453 docs
- **Stage07 exclusion:** [HARD_EXCLUDE:publisher_boilerplate] 8_book_chapter_books_read (next=exclude_before_llm)

**Four keyword representations** (BERTopic / labeling)

- **Main:** —
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. no part of this e-book may be reproduced or shared by any electronic or mechanical means, including but not limited to printing, file sharing, and e-mail, without prior written permission from delaney diamond.

> 2. read excerpts from these books and more on water​brook​multnomah.​com !

> 3. if you find a siren-bookstrand e-book being sold or shared illegally, please let us know at legal@sirenbookstrand.com a siren publishing book imprint: erotic romance manlove an unexpected mate copyright © 2013 by aj jarrett e-book isbn: 978-1-62740-433-4 first e-book publication: august 2013 cover design by harris channing all cover art and logo copyright © 2013 by siren publishing, inc. all rights reserved: this literary work may not be reproduced or transmitted in any form or by any means, including electronic or photographic reproduction, in whole or in part, without express written permission.

**Stage-08 / Stage-07 snippets**

> 1. i’ve promised the paper will do everything it can to keep everyone safe.

> 2. writing can give that, i’ve found.

> 3. to @rhymewithme, thank you for sharing your story on the last chapter of a and d. as i’ve continuously said, it made me happy that the last phrase made an impact on you to take a plunge.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---

### Topic 233 — Blush Creeping Up Her Cheeks

- **Label:** Blush Creeping Up Her Cheeks
- **Taxonomy:** 1.7 — Facial Expression & Non-Sexual Nonverbal Cues
- **Cliff's delta:** -0.1130 [-0.1322, -0.0915] — small — more in LOW-rated
- **Mean share:** high 0.092% vs low 0.109% (n_high=5086, n_low=5390)
- **BERTopic cluster size:** 172 docs

**Four keyword representations** (BERTopic / labeling)

- **Main:** remark, feminine, embarrassed, magical, embarrassing, realization, ankles, flush, embarrassment, precious
- **KeyBERT:** —
- **POS:** —
- **MMR:** —

**BERTopic representative docs**

> 1. a blush crept to emma’s cheeks. “

> 2. a blush so faint she’d nearly missed it had crept over the carved slash of his cheeks.

> 3. so when you said i looked like bait ...' a blush crept up her cheeks and her hair fell forward with a tilt of her head to conceal the embarrassed infusion. '

**Stage-08 / Stage-07 snippets**

> 1. so when you said i looked like bait ...' a blush crept up her cheeks and her hair fell forward with a tilt of her head to conceal the embarrassed infusion. '

> 2. she’s probably laughing at me because i’ve blushed, but it doesn’t matter. “

> 3. i don’t think i’ve ever seen her blush. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---
