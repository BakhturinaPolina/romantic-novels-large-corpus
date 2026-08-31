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

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Escape to Morning — Susan May Warren; tertile=begin; p=0.75**
>
> What should I do here, Miss? [TARGET] I can’t just leave her out there.” She wrapped her arms around the animal and held her close, smelling the forest in her fur.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Blue Dahlia — Nora Roberts; tertile=end; p=0.75**
>
> What they did with her. [TARGET] She won’t be able to leave, to rest, to pass over, whatever it is, until we find her.” “ How?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Divine Savior — Kathi S. Barton; tertile=begin; p=0.75**
>
> And every time she uses her magic, no matter how small, we’ll get closer. [TARGET] You’ll see, we’ll find her for you, for both of us.” Colin hoped so.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Wildly Wedded Wife — Erica Chilson; tertile=end; p=0.70**
>
> How were you and Queen supposed to circumvent it?” “ [TARGET] If we get you out, you’ll go right back to her, won’t you?” Whitt says hopelessly. “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · I Lost My Mobile at the Mall — Wendy Harmer; tertile=middle; p=0.61**
>
> Carmelita is frantically calling. [TARGET] I must make some sort of noise because she hears I am still here. Wherever 'here' is. '

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Echoes From The Past — Grace Brannigan; tertile=begin; p=0.71**
>
> Listen, just tell her Christie’s here," she said urgently. " [TARGET] It's been a long time but I know she’ll see me." " You can’t see her."

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · Born In Secret — Susan Kearney; tertile=end; p=0.78**
>
> He reached over and squeezed her icy hand, offering the gesture in support and unity. “ [TARGET] We’ll find her and bring her home.” Conviction frosted her voice. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · Ace — J.J. Marstead; tertile=end; p=0.67**
>
> We would probably be eating ice cream and talking about baby names. [TARGET] I’m torn that she’s not here right now. I shake my head clear of the thoughts.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Lover Enshrined, part one — J.R. Ward; tertile=end; p=0.68**
>
> Find another place to live. [TARGET] If she doesn’t know how to find you, she can’t turn you in.” “ If I leave town, she’d just go after my mother.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Black Magic — Megan Derr; tertile=middle; p=0.66**
>
> I’ll tell your mom you are here. [TARGET] I believe she’ll be pleasantly surprised to see you.” “ Thanks, Ms. Margaret.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Prince's Gambit — C.S. Pacat; tertile=begin; p=0.45**
>
> ABOUT THE AUTHOR S. U. Pacat is a writer who has lived in a number of different cities, including Tokyo and Perugia. [TARGET] Right now she lives in Australia, where she is working on the third and final book in the Captive Prince trilogy. Follow S.U. Pacat on Twitter @ supacat , or on her blog at www.captiveprince.com .

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Strength of the Mate — Kendall McKenna; tertile=end; p=0.58**
>
> He remembered exactly how it felt when everyone told him they knew what was best for him, like he was incapable of thinking for himself. “ [TARGET] Instead of ordering her around like the big, strong man who always knows what’s best for his woman, why don’t you just try asking her to leave with you, because you want to start a life together someplace that’s safe for you both?” Eric sighed explosively.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Gio's Dream — Carol Lynne; tertile=begin; p=0.49**
>
> Come on. [TARGET] 29 Carol Lynne No one looks the way you do and doesn’t have a string of women surrounding them, unless they don’t want them.” Gio laughed and kissed the top of his head. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Left of the Dial — Heidi Champa; tertile=middle; p=0.53**
>
> She had a studio there that she shared with a couple of other undergrads. [TARGET] I didnt visit her there at all, not willing to risk running into Roger again. The person I was trying to run into was Bryan, but he was never alone.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · A SEAL Forever — Anne Elizabeth; tertile=middle; p=0.57**
>
> The place was fun, and belonging to something as unique as this gym could work miracles. “ [TARGET] I will be checking on you every day to make sure you all are following her direction.” The parole officer stood up. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_015 · Expecting His Alpha's Child — Anya Byrne; tertile=end; p=0.65**
>
> I knocked your ex out before he stepped in, so she survived. [TARGET] She's being held somewhere in the mansion, and she's apparently come to, but I haven't seen her. The other Alpha was really pissed because apparently the guy who shot at us was his son and heir."

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

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Prophecy: Caelestis and Aurorea — Felicity Heaton; tertile=begin; p=0.74**
>
> I won’t give you another chance to reconsider. [TARGET] I don’t want to fight, but you’ve left me with no other choice.” She shook her hands to limber up and didn’t give them the opportunity to start the fight.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Taken — Karice Bolton; tertile=middle; p=0.59**
>
> How I could trip on a curb that I knew was there . [TARGET] I’d never be able to understand how I could fight with the best of them, but my day-to- day coordination was atrocious. “ Should we try looking near the park?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Frayed — Pamela Ann; tertile=begin; p=0.69**
>
> If a person gives up every time shit is thrown their way, the human race wouldn’t have survived. [TARGET] You have to learn how to fight—physically, emotionally, mentally. Face it bravely, even if the pain is too great, the consequences too frightening.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Demencious Saga — Sadie Sins; tertile=end; p=0.59**
>
> Hope she'll only eat the boy and me, and let you just walk away? [TARGET] You can roll over and die like the bastard coward you are, or you can finally take a stand for something and fight.” “ My many gods, I really, truly hate you, you self-righteous bastard of a cat hellspawn,” Feral growled and wrenched his arm free.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Rise of the Fallen — Donya Lynne; tertile=begin; p=0.61**
>
> Aaahhhh, sweet pain waited for him in his hand. [TARGET] He didn’t have to go in search of a fight, did he? The pain he needed was right here.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Once More With Feeling — Megan Crane; tertile=end; p=0.67**
>
> I didn’t want any of it. [TARGET] And I certainly wasn’t going to fight for it any longer. I was going to do something much better.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Not the Leader of the Pack — Annabeth Leong; tertile=begin; p=0.73**
>
> The infamous pack leader from Helena had enough arrogance for twenty alphas. “ [TARGET] That’s what you meant about fighting his battles.” “ It was the least I could do, after everything he did for me.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Beers, Hens and Irishmen — Meghan Quinn; tertile=end; p=0.58**
>
> We rolled around for a bit until Finn came in and broke us up but not until I attacked him as well.” “ [TARGET] Oh Liam, you didn’t fight with Finn again, did you?” Liam just nodded his head. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Out of the Night — Geri Foster; tertile=middle; p=0.61**
>
> I’ve known the man for years. [TARGET] We have fought so many times we know how the other one thinks. But my advantage is he cannot remember how I work because he’s lost his memory.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Out of the Night — Geri Foster; tertile=middle; p=0.53**
>
> A dead man is dead just the same.” [TARGET] He thought back to the beginning of their battle. It had been simple.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · One Call Away — Felice Stevens; tertile=begin; p=0.43**
>
> Oren peered at the screen. [TARGET] I knew that arguing with them wouldn’t help. I spoke to one of your counselors, who said to live my life.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Diamond Sky — Annie Seaton; tertile=middle; p=0.40**
>
> The only thing I haven’t figured out is how you’re getting them off site,’ he said in a slow drawl. ‘ [TARGET] You’ve got me beaten there. I’ve watched you go through the body scanner and I know your bags were X-rayed.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · To Marry McAllister — Carole Mortimer; tertile=middle; p=0.48**
>
> Too mildly, as far as Brice was concerned, sure that there had been a double edge to the other man’s remark. [TARGET] Well, if the other man thought he was about to give him a fight over Sabina, he was wrong; Sabina was an independent woman of twenty-five, not a possession for two men to fight over as if she were the prize! ‘ We have been known to dispose of the odd unwanted Sassenach,’ his grandfather was the one to dryly answer the other man as he stood silhouetted in the now open doorway, light streaming out welcomingly from inside the castle. ‘

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · The Art of Submission — Ella Dominguez; tertile=end; p=0.60**
>
> No… no… this is not happening. [TARGET] I start thrashing and fight ing which takes him by surprise, I think, because before, I would’ve just let him beat me. Fuck that .

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · The Art of Submission — Ella Dominguez; tertile=begin; p=0.76**
>
> Her voice is guarded. “ [TARGET] I don’t want to fight either; I just want to know.” “ You won’t be mad?

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Grace Alive — Natasha House; tertile=middle; p=0.52**
>
> Bree was grabbing at the back of his hair and shaking a little rabbit that was attached to her hand. “ [TARGET] No,” I said not really wanting to beat around the bush about everything. “ I’m sorry, Branson, I can’t hang out with you.”

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

_16 examples from 10 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Faith — Brei Betzold; tertile=end; p=0.91**
>
> Well we’ve been talking, and we want you to tell Drake that when he gets out of the hospital he’s coming here for a little while.” [TARGET] I shook my head at her. “ Nope, not doing it.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Broken Until You — J.R. Grant; tertile=middle; p=0.78**
>
> You’re like my cloned twin.” [TARGET] I shook my head, laughing. “ Right…” Kaya pulled up Atlantic City on her phone and read about a couple of different places that sounded like fun.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Broken Until You — J.R. Grant; tertile=begin; p=0.79**
>
> Sweetie, are you drunk or is that cheap crack you’re smoking?” [TARGET] I shook my head, annoyed. “ You’re completely insane if you think I’m doing a speed date.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Declan + Coraline — J.J. McAvoy; tertile=middle; p=0.91**
>
> All the while saying ‘Cora, wake up, we’re moving to Greece.’ ” [TARGET] She laughed and shook her head. “ My father came in behind her and told her to hush and leave me alone.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Dance For Me — Helena Newbury; tertile=middle; p=0.91**
>
> Is there any way at all I can get out of this?” [TARGET] She grinned and shook her head. “ It’ll be fun.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Hope Breaks — Alice Bello; tertile=middle; p=0.76**
>
> How hadn’t I known about Paula being Ms. Leer’s daughter, or that Paula had a brother? [TARGET] I laughed and shook my head. “ But you’re so nice.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Hope Breaks — Alice Bello; tertile=begin; p=0.76**
>
> Then he leaned in and asked, “I wouldn’t have to show my johnson, would I?” [TARGET] I gulped and shook my head. “ Just have to take off your shirt.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Hope Breaks — Alice Bello; tertile=begin; p=0.80**
>
> You’re shitting me, right?” [TARGET] I shook my head solemnly. “ I shoot romance novel covers.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Tempted — Alana Sapphire; tertile=middle; p=0.72**
>
> When did you start taking the pills?” [TARGET] She sighs and shakes her head in resignation. “ Tuesday.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Dreaming With My Eyes Wide Open — Mary J. Williams; tertile=middle; p=0.72**
>
> Any idea who would do such a thing?” “ [TARGET] No,” Paige shook her head, frowning. “ It doesn’t make any sense.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Dreaming With My Eyes Wide Open — Mary J. Williams; tertile=middle; p=0.89**
>
> The Genie is out of the bottle, Chuck.” [TARGET] She shook her head, frowning. “ You know what?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Dreaming With My Eyes Wide Open — Mary J. Williams; tertile=begin; p=0.95**
>
> Nate asked her silently. [TARGET] She simply shook her head. “ First,” Nate gently herded Jenna back to her friends. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Emerald Knight — Michelle M. Pillow; tertile=middle; p=0.78**
>
> Tell me you sent it from me.” [TARGET] Frowning, Lora shook her head. “ Nay, m’lady.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Not Dreaming of You — Nina Cordoba; tertile=middle; p=0.70**
>
> Alexia, I’m sorry. . . .” [TARGET] Shaking her head, she said, “Don’t, it’s not your fault. There was nothing you or anyone else could have done.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Not Dreaming of You — Nina Cordoba; tertile=begin; p=0.61**
>
> Do you have another shirt in your carry-on?” [TARGET] Shaking her head, she said, “No, just panties.” Yeah, that’s exactly the mental picture he needed to go along with the tits he was now trying hard not to stare at.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Me, Cinderella? — Aubrey Rose; tertile=begin; p=0.68**
>
> A line from one of the books my mother used to read ran through my mind: “… and the prince, tall, dark, and brave, fought off the wolf and chased it into the snowy night. ” [TARGET] I shook my head and the words flew away into the darkness. “ You’re a generous girl,” the man said. “

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

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Dance in the Moonlight — A.L. Kessler; tertile=middle; p=0.72**
>
> Just so they could try to kill me by starvation, fights, and whatever the hell else they threw at me?” “ [TARGET] I thought you had been lying about all that, now I know, now I can protect you.” Sarah begged. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Time Eternal — Lily  Morgan; tertile=begin; p=0.78**
>
> Skyla snorted. “ [TARGET] You mean your safety, right?” “ If you wish, my lady.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Strongheart's Woman — Zeece Lugo; tertile=middle; p=0.74**
>
> My enemies may prove even more deadly to you than yours. [TARGET] I need to know that you’re safe and away, so that I can then deal with my people without any vulnerabilities or liabilities.” Angel nodded her understanding.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · From The Falls — Heather  Renee; tertile=begin; p=0.70**
>
> We have Fates that look out for us and they let us know things that could be very important to us,” Lorelle said as she stepped forward. “ [TARGET] They told us about you and that we would need to protect you.” “ What are you?

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Oceanborne — Katherine Irons; tertile=middle; p=0.76**
>
> We have to go, Elena. [TARGET] I have to get you to safety.” He had to make certain she was all right before he was free to return to his command.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · The Wishing Cup — J.M. Gryffyn; tertile=end; p=0.64**
>
> He will brief you with all the details later when he takes you in. [TARGET] You will be safe and it will be my on-going mission to hunt them down.” He stopped and scanned around the room as he chewed on his lower lip.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Quarantine — Lisabet Sarai; tertile=middle; p=0.72**
>
> Once more Dylan realised that there was a great deal more to Artemis than met the eye. “ [TARGET] The less you know, the safer you’ll be.” She stood, capped the bottle of amber liquid, and stored it away in a cabinet she could barely reach. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Bride Gone Bad — Sabine Starr; tertile=end; p=0.75**
>
> I don’t want to hear another word about secret societies or any of the other malarkey you’ve been feeding me.” “ [TARGET] I’ve done my best to protect you.” He held up the ring and necklace. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Baby Be Mine — Paige Toon; tertile=middle; p=0.56**
>
> The press are going to find out about him sometime, whether you like it or not,’ he states. ‘ [TARGET] At least in LA you’d both have protection; you know my security guys are some of the best in the business. Wouldn’t it be better for Barney to grow up with this life from the start, so he doesn’t know any different?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · As You Are at Christmas — Davalynn Spencer; tertile=end; p=0.31**
>
> He laughed with a full mouth but managed not to spray the poor woman with pancake. “ [TARGET] No, I think Roady may be harmless. Not much of a watchdog, at least not yet.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Taking the Plunge — E.L. Todd; tertile=end; p=0.76**
>
> Now I understand your hesitance. [TARGET] You’re protecting yourself.” She nodded. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · The Devil's Trill Sonata — Matthew J. Metzger; tertile=begin; p=0.43**
>
> and in the police, no less. [TARGET] Isn’t that a hostile environment?” “ Er, no.”

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Married in Black — Christina Cordaire; tertile=begin; p=0.49**
>
> Just let me know if you change your mind. [TARGET] I’m your man for getting you to the point of passing out, if you ever want to take that risk.” His voice was dry and teasing, but the words struck her strangely—as if there were more in them than was revealed on the surface.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Bruised — Sean Michael; tertile=end; p=0.49**
>
> Yeah? [TARGET] Putting the bad guys away would suit you better, wouldn’t it?” He leaned in, took a whiskey and Billy-flavored kiss. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · A Dream of Desire — Nina Rowan; tertile=middle; p=0.42**
>
> In addition to the program we intend to institute, Ian has spoken of taking this campaign nationwide. [TARGET] With the right angle, we can protect the players and institute more safety measures than exist so far. We can also encourage all teams in all contact sports to educate their players for the future.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_015 · The Gessami Residence — Jane GIbson; tertile=end; p=0.35**
>
> Then there are things that leave us feeling completely hopeless, things that are out of our control and leave us wondering how we will ever survive. [TARGET] But one thing that I do know is that we do survive, and good things can still happen… even late in the game. As hard as that is to believe, remarkably it’s true – you just have to be willing to try.

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

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Submit — C.D. Reiss; tertile=middle; p=0.67**
>
> Ms. Faulkner,” she said. “ [TARGET] How are you holding up?” “ Fine.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Big Girls Do It Pregnant — Jasinda Wilder; tertile=end; p=0.68**
>
> But I’m here, just the same, Praying over you, I’m watching over you. [TARGET] I can’t ever hold you close enough, My darling, I can’t ever be strong enough. But I’ll always, always try, I’ll comfort you when you cry.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · A Wilde Night — Savannah Young; tertile=middle; p=0.63**
>
> I completely let loose. [TARGET] I hold Kat as tight as I can without crushing her, but I don’t want to ever let her go. “ How was that?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · A Wilde Night — Savannah Young; tertile=end; p=0.55**
>
> I can’t wait to be in his strong arms again. [TARGET] I feel like time completely stops when he holds me. It’s like we’re in our own little world where no one can touch us.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Tall, Dark And Lethal — Dana Marton; tertile=begin; p=0.63**
>
> She was possibly more than he could handle, although that macho sense of vanity that lived deep down in every man made it hard for him to admit that, even as her fingers jabbed dangerously close to his irises in some freakish self-defense move she must have seen on TV. “ [TARGET] You might want to hang on.” He was already out of the room.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Love, Jamie — A.K.M. Miles; tertile=end; p=0.72**
>
> Thank you. [TARGET] I need you to stay with me, hold me, just for a little. I don’t want to think about what happened.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Love, Jamie — A.K.M. Miles; tertile=end; p=0.72**
>
> I want your hands on me when I come. [TARGET] Then I want to hold you all night long.” Jamie tugged Grant’s head up to look at him as he finished his list of requests.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Knowing Jack — Rachel Curtis; tertile=middle; p=0.67**
>
> You have no right to keep anything from me. [TARGET] If you don’t hand me the phone right now, I’m not going to let you hold onto it. Whatever you say, I’m not in danger from my phone.” “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Hot Pursuit — Suzanne Brockmann; tertile=begin; p=0.48**
>
> I bet you’ll be running with her, and Mindy’ll be showering you with stuffed bunnies at the finish line. [TARGET] Hold that future in your head, kid, aiight?” The boy nodded, turned to go, but then turned back. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Suckcess — Niyah Moore; tertile=begin; p=0.55**
>
> Go ahead and go over,” I said. “ [TARGET] I don’t want you to be stuck at my side. I’ll be right over there with the guys.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Tyburn — Jessica Cale; tertile=middle; p=0.60**
>
> He took a deep breath. “ [TARGET] Just got back…I held it together until he left.” “ Shall I fetch your mercury?” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Storm's Eye: The Rock Star's West Coast Girl — Lisa Gillis; tertile=end; p=0.58**
>
> Before I could actually get away, he clamped onto both wrists. “ [TARGET] I’m sorry, I. Fuck, I’m so sorry…” When I jerked again, he released his hold, and freed, I paused. We were both standing with one leg on each side of the bench.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Viper's Kiss — Shannon Curtis; tertile=end; p=0.64**
>
> He held her tightly. “ [TARGET] God, it feels so good to hold you. I’ve missed you so much.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · When in Doubt, Add Butter — Beth Harbison; tertile=end; p=0.69**
>
> I really just wanted to make sure you were okay.” “ [TARGET] No, no, I have your stuff here and it’s ready, except for tonight’s … Hold on.” I put my hand over the receiver. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · The Wicked Wallflower — Maya Rodale; tertile=end; p=0.50**
>
> My innocence, my word, my heart. [TARGET] And I held back because of this. I was so afraid of this.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Judging Covers: A Novella — Kristen Beairsto; tertile=end; p=0.59**
>
> It wasn’t your fault. [TARGET] I know I was a little distant upstairs, but I’m just trying to hold it together.” He opened his mouth to protest, but she shook her head. “

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

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Nikolai — S.L. Jennings; tertile=begin; p=0.72**
>
> You're safe with me, Vee. [TARGET] No one will ever hurt you again." I wanted to believe him.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Salvation — Ahren Sanders; tertile=middle; p=0.69**
>
> Her small voice cuts me like a knife. “ [TARGET] You’ve become so important that I would hurt anyone that caused you pain. Raven’s life is full of drama.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Blue Waters — India R. Adams; tertile=middle; p=0.58**
>
> Would you believe from the Heavens above?” [TARGET] He pulled me to him with such tenderness it healed a part of my soul I didn’t realize was damaged. His strong hand ran through my hair as if to just get me closer to him.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Defy — L.J. Shen; tertile=end; p=0.61**
>
> And his mom didn’t leave us much choice. [TARGET] But I was hurt, so I’d stabbed him back with my words. Jaime didn’t follow me.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Seducing an Angel — Mary Balogh; tertile=begin; p=0.72**
>
> Maze put on his helmet. “ [TARGET] I’ll come after you if you’re hurt. Try to be aware of what is behind you.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · A Plain, Ordinary Cowboy — Jan  Irving; tertile=end; p=0.82**
>
> Being considerate is fucking me as often as possible.” “ [TARGET] I’m afraid of hurting you.” This moment, he knew he had to be honest.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Purgatory: A Novel of the Civil War — Jeff Mann; tertile=begin; p=0.75**
>
> I want to keep you tied, so I can feel strong and in control. [TARGET] I want to take care of you, protect you, but, yes, I want to hurt you too. There’s been this crazy spirit in me since I was a child; it mixes up kindness with cruelty.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · Fangs with a Heart — Tempeste O'Riley; tertile=middle; p=0.71**
>
> You had ways to stop things at any given point you needed. [TARGET] And I thought you trusted me enough to know I wouldn’t deliberately hurt you.” “ I know that.”

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · What Witches Want — Laura Stamps; tertile=middle; p=0.62**
>
> You mean you had a witch’s night without me?” [TARGET] I didn’t know why I felt hurt, but it stung not to be invited. “ Uh, last I checked, you were fine in the dating department.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · The Soldier's Sister — Debby Giusti; tertile=middle; p=0.64**
>
> He wanted to be proactive and ensure Ted’s situation didn’t become more severe. [TARGET] And he didn’t want anyone else hurt. Stephanie’s bitter words played over in his head.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Wolf Hiding — Toni L.H. Boughton; tertile=end; p=0.54**
>
> Yeah, yeah, I know, but listen-” “Sage, I’ve told you to get me or Suzannah. [TARGET] What would have happened to you if you’d fallen and hurt yourself?” Sage groaned and rolled her eyes. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Best Laid Plans Box Set — Robyn  Kelly; tertile=begin; p=0.49**
>
> Before I can reach it, he takes the phone back. [TARGET] He’s toying with me, and any sympathy I have for his situation disappears. “ Is this your idea of fun?

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Bookends — Jane Green; tertile=middle; p=0.51**
>
> You can’t grow as a person,’ she said sadly, ignoring my joke, ‘when you close yourself off emotionally. [TARGET] It’s all well and good saying you avoid pain by avoiding relationships, but what about the wonderful things you’re avoiding as well? What about the joy and the intimacy and the trust that come with finding someone you love?’ ‘

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Bookends — Jane Green; tertile=end; p=0.57**
>
> He thinks that, however much we love Lucy, and love Lucy and Josh as a couple, it is not our place to interfere. [TARGET] He says that he knows it must hurt, but that whatever will be, will be, and that nothing we say or do will resolve things. It may in fact make things worse.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Venus in Blue Jeans — Meg Benjamin; tertile=begin; p=0.68**
>
> Why would anyone shoot her pet? [TARGET] Why would anyone want to hurt him? What was he doing, anyway?

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · The Love Goddess' Cooking School — Melissa Senate; tertile=end; p=0.73**
>
> And one more thing. [TARGET] That I’m really sorry for hurting you.” Her heart pinged and she sat up in bed, hugging her knees up to her chest. “

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

_16 examples from 15 books; ±1 context on 16_

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

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Abiogenesis : Cyberevolution Book I — Kaitlyn O'Connor; tertile=begin; p=0.61**
>
> She'd already dug her fingers into the cut, grasped the locator and yanked it free of the bone before fire poured through her. [TARGET] Gasping at the wave of dizziness that washed over her, she dropped the locator to the pavement, picked up one of the weapons and smashed it with the butt. Blood was gushing from the cut.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · A Beginner's Guide to Rakes — Suzanne Enoch; tertile=begin; p=0.70**
>
> He straightened. [TARGET] Before she could dive for the weapon again, however, he nudged her chair aside with his hip, opened the drawer, removed the pistol, and tossed it out the window. “ There.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Under the Aspens — Elizabeth Sherry; tertile=middle; p=0.70**
>
> He made too much noise to have heard them behind him. [TARGET] Glen motioned for Sher to stay put, then got close enough to put his gun to the back of the guy’s head. “ Down on the floor.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · A Kept Man — Kerry Connor; tertile=end; p=0.73**
>
> Caleb took a step forward. [TARGET] The stranger halted the forward movement by aiming the gun flat at Caleb’s chest. “ Back off, Carpenter.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Fallen Crest High — Tijan; tertile=end; p=0.62**
>
> You've talked about it for years." [TARGET] Her hand shot out and she pointed at them. Her foot stomped down. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · More Than Miles — Autumn Jones Lake; tertile=end; p=0.45**
>
> Murphy explains what happened and the guys all tell me what a good job I did. [TARGET] I don’t even realize I’m still gripping the Glock, until Wrath pries it out of my hands. He pushes his keys at Murphy. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · More Than Miles — Autumn Jones Lake; tertile=end; p=0.43**
>
> I have to shuffle through a few books and papers before I find the small metal box at the bottom of the drawer that I assume holds the guns. [TARGET] Wrath’s trained me on the Glock before, so I load that one and hold on to it. Murphy will have to handle the Sig.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Confetti at the Cornish Cafe — Phillipa Ashley; tertile=begin; p=0.41**
>
> Blackbeard’s after us!’ [TARGET] A little girl in pirate gear shoots out of the copse and clips Ben. He tries to stay upright but slips on the damp turf and lands smack on his bum in a puddle.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Curse of the Gargoyle — Tara Nina; tertile=middle; p=0.49**
>
> I do need to take a few pictures.” [TARGET] He forced his focus from her, lifted the camera and shot off a few frames in a row. They spent the rest of the day walking the grounds.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Love Turns the Page — Etienne; tertile=end; p=0.53**
>
> Your tenants were awakened by the sound of breaking glass in the kitchen,” Carl said. “ [TARGET] One of the men took a gun out of the nightstand, where he kept it, and both of them went to the kitchen. The intruder shot at them.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · Sucking in San Francisco — Jessica McBrayer; tertile=end; p=0.61**
>
> A few minutes later, a man in a black button-down shirt, jeans, and a jacket walked in. [TARGET] The suit jacket fit tightly over his broad shoulders, pulling under his right arm around the bulge of his gun. His eyes catalogued everyone and what they were doing.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Best Friends With The Billionaire — Coleen Kwan; tertile=middle; p=0.66**
>
> Indignation rose in Cassie. [TARGET] She pushed to her feet, rolling up the magazine as if to use as a defensive weapon. “ No one is going anywhere near my eyebrows.”

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

- **Main:** soul, heaven, god, hell, gods, realms, your, worship, theirs, bible
- **KeyBERT:** promises, willingly, willing, possessed, tries, delicate, bodies, planned, enjoying, destination
- **POS:** theirs, pout, destination, example, result, reflection, exchange, ye, delicate, process
- **MMR:** theirs, pout, destination, dump, judging, promises, reflection, exchange, delicate, bodies

**BERTopic representative docs**

> 1. if there’s a hell, then there must be a heaven.”

> 2. god, it was heaven.

> 3. but if i say no, i go on living, have a full life, die a natural death, maybe go to heaven, or hell, which-ever i'm bound for, but your soul goes to..." "hell.

**Stage-08 / Stage-07 snippets**

> 1. if god adopts me, i’ll want to do whatever pleases him.” “

> 2. i’m hoping if you’re facing struggles now that you’ll let god see you through.

> 3. if you are, then you’ll have a special place in hell.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Dreamspell — Tamara Leigh; tertile=middle; p=0.57**
>
> Ironic, isn’t it? [TARGET] I came here to be whole again and Wynland sends me straight back to hell.” Kennedy didn’t know what possessed her to say what she did next. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Enslave — Felicity Heaton; tertile=end; p=0.50**
>
> Mmm, because I wanted to kiss you again. [TARGET] It seems God has deemed me worthy of having my prayers answered, but had I known the price you would pay… Dios… Varya, I would never have asked him to bring you back to me.” He meant it too.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Bad Blood — Amity Cross; tertile=middle; p=0.62**
>
> We need to go through this intel .” [TARGET] In all the time X had been teaching me to become like him, one thing he’d told me time and time again was that he had no soul, that he was already lost. I didn’t believe that, but what if he believed that by going through with this, I was going to lose mine as well?

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Sinner's Craving — Megan   Elizabeth; tertile=end; p=0.53**
>
> You made me feel disposable and unworthy.” “ [TARGET] I know,” Preacher said gravely. “ None of that is true.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · My Recycled Soul — Lynette Ferreira; tertile=end; p=0.56**
>
> It is possible; don’t you think?” [TARGET] I remain silent, and then I wonder, “That would mean though that I am reincarnated and that souls are incarnated within families?” “ What if they were and my soul belonged to Gerard and yours belonged to Eilish?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Love is Darkness — Caroline Hanson; tertile=end; p=0.53**
>
> Lucas turned his gaze to Marion. “ [TARGET] I understand your eagerness for death, but you must respect the sanctity of ritual. I assume you have something to say before we continue?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Enticing a Dangerous Mate — Anitra Lynn McLeod; tertile=middle; p=0.55**
>
> That snarky tone was the remnant of his long-dead father, the man that no one, no how, could please. [TARGET] Not a soul in all of creation could place more demands upon him than his father had. Once the man was gone, his life truncated in the blink of an eye by a car wreck, Marshal’s relief had been short lived, because his father’s demanding tone had taken up residence in Marshal’s head and kept right on haranguing him no matter what he did.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · The Lady Travelers Guide to Scoundrels and Other Gentlemen — Victoria Alexander; tertile=middle; p=0.59**
>
> Well...yes, I suppose. [TARGET] But only as part of my efforts to save your eternal soul,” she added quickly. “ I can’t imagine you doing it for any other reason.”

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · King and Kingdom — Danielle Bourdon; tertile=middle; p=0.51**
>
> You weren't born into Royalty, Chey. [TARGET] They understand you won't be versed in the same things.” “ And they'll take advantage, right?” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · King and Kingdom — Danielle Bourdon; tertile=middle; p=0.56**
>
> No warning, no capture-and-coerce. [TARGET] You will simply cease to exist, and that will be that.” Aksel wore a no nonsense expression, eyes cool and indifferent to the idea of murder.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · The Don's Daughter — Renee Rose; tertile=end; p=0.57**
>
> I was wrong. [TARGET] I sinned against you, and our mother and our father, God rest his soul.” He spoke in Italian, his voice so achingly familiar.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Don't Say It — Debra Kayn; tertile=begin; p=0.43**
>
> Bianca paused. " [TARGET] How is everything there?" " Okay."

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Finding Jason — Lyndi Lamont; tertile=begin; p=0.40**
>
> Experienced. [TARGET] Will is a simple fellow, and right now, his universe revolves around me. That is enormously appealing.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Finding Jason — Lyndi Lamont; tertile=end; p=0.43**
>
> But every once in a while, I like to be the one in charge, if only in bed. [TARGET] In a place like the Hole In The Wall, we are all equals. There are no masters and no servants, just men.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Heat Under Fire — Andrew  Grey; tertile=middle; p=0.53**
>
> You have a lot of explaining to do and you’d better start now,” Rock growled. “ [TARGET] Bygones can be bygones and confession is good for the soul, so start talking.” “ Yes.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Jaded — Mercy Amare; tertile=begin; p=0.48**
>
> Like seriously, this guy puts THOR to shame. [TARGET] And I'm beginning to wonder if he is a god, because I swear, I just lost the ability to talk. My mouth suddenly feels dry.

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

- **Main:** heart, my, chest, beating, stomach, pounding, racing, pulse, heartbeat, beat
- **KeyBERT:** frantic, anxiety, skipped, danced, strangled, swallowed, pounding, upset, excited, chased
- **POS:** veins, hopeful, frantic, ribs, excited, unable
- **MMR:** pounding, fluttered, veins, strangled, chased, violently, flowing, frantic, ribs, danced

**BERTopic representative docs**

> 1. when you find yourself in the thick of it, your heart starts the auspicious troubles of chance | charlie cochet 120 pounding so hard it feels like it’s gonna burst out of your chest, and your stomach gets so full of butterflies you just might be sick.

> 2. my heart threatens to stop beating at first, then i hear my heartbeat in my ears.

> 3. my heartbeat starts racing.

**Stage-08 / Stage-07 snippets**

> 1. i silently gasped as my heart skipped several beats. “

> 2. my heart skipped a beat and i decided i wanted to hear no more.

> 3. my heart pounded wildly at the thought of baring myself in front of others. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Promises and Piña Coladas — Elizabeth Bemis; tertile=begin; p=0.70**
>
> His wife’s right eye was almost completely swollen shut, and her cheek had turned a horrifying shade of purple. [TARGET] My blood pressure rose, and my breath came in short bursts as I clenched my fists. She introduced herself as Roseanne Boyle and gave her address to the police.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Nordic Bound — Christine    Edwards; tertile=begin; p=0.64**
>
> I peer through the lens and in seconds have her small head locked dead in the center of my crosshairs. [TARGET] My finger is touching the cold metal trigger, slowly beginning to depress, when for reasons that are a mystery to me, I have a sudden change of heart. I decide to warn the girl before I take her life.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Fighting Blind — C.M. Seabrook; tertile=middle; p=0.72**
>
> I stare at the green bottle and lick my lips nervously. [TARGET] My heart races in my chest, and I can feel the familiar pressure of an anxiety attack forming. I don’t know what makes me more nervous, having to tell him about Stefano, or the fact that he’s standing half-naked three feet from me. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Red Moon — R.K. Close; tertile=end; p=0.68**
>
> Suddenly, he turns and faces my direction, and I feel he is looking right at me. [TARGET] My heart is in my throat as I swallow hard and fight the urge to run. His eyes are a brilliant green, but they are ablaze with anger.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Ace — Kate Aaron; tertile=middle; p=0.66**
>
> Our lips met, the most tentative of brushes, before he pulled back, smug now. [TARGET] My skin tingled where we touched and my limbs were shaking but that rising feeling in my chest wasn’t desire, it was panic. His lips parted in a smile and his teeth flashed at me, too white and too damn straight.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Thrasher — K.S.  Smith; tertile=end; p=0.71**
>
> I watched my husband smirk as he began taking the groceries from the bag and unloading them onto the island in our kitchen. [TARGET] When he got to the bag that I’d been waiting for, my heart began to beat faster than normal, and I could feel the nerves building inside of me. I inhaled deeply and held my breath as Duke’s eyes widened.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Fever — Tonya Plank; tertile=begin; p=0.82**
>
> Eyes still focused on the road, no hint of a playfully malicious smile whatsoever. [TARGET] My heart leapt into my throat and lodged there. I couldn’t seem to say anything the rest of the ride.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Step Bride — B.B. Hamel; tertile=end; p=0.82**
>
> Pots and pans banged, and I was pretty sure I heard someone cursing in Spanish. [TARGET] My heart was hammering in my chest, worry wracking my spine. If that box was gone, if they had found what I had stashed in there, then I was done.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Prom Night in Purgatory — Amy Harmon; tertile=begin; p=0.51**
>
> I remember falling. [TARGET] I even remember what you’ve described….the feeling of fighting death. But that’s all.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Prom Night in Purgatory — Amy Harmon; tertile=begin; p=0.69**
>
> The woman who professed to be his sister stood at the side of his bed. “ [TARGET] Your heart monitor started beeping like you were in cardiac arrest. I’m sorry I woke you…It just scared me.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Grind — E.  Davies; tertile=middle; p=0.66**
>
> Finally.” “ [TARGET] Dude, I thought you had a heart attack or something!” Ryan’s heart still thumped as he glared at James.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · His Guilt — Shelley Shepard Gray; tertile=end; p=0.49**
>
> Waneta asked curiously . . . [TARGET] just seconds before panic set in. “ Oh, no!

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Tropical Spice — Sandy Loyd; tertile=begin; p=0.37**
>
> It’s late. [TARGET] I’m beat and starting to see double. Since we can’t visit Mrs. Holloway until tomorrow and we’re not getting anywhere tonight, let’s finish in the morning.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Fairy Godmothers, Inc. — Jenniffer Wardell; tertile=begin; p=0.60**
>
> Who knows, you might even like it.” [TARGET] So, that was what people meant when they talked about a person’s heart skipping a beat. “ But—” She felt a tug on her skirt from Rellie. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · The Morning After Memoirs — Kate  Michaels; tertile=begin; p=0.33**
>
> The brigade-major was killed, and Stretton knocked unconscious, but if he hadn’t been knocked out that morning he would have been up for a court-martial, sure as fate –’. [TARGET] 17 Invalided home, Stretton has the symptoms that Deeping, as a military doctor, would have classified as mild shell-shock – ‘Slight tremor of the hands. Some sleeplessness.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · The Kachina Job — A.J. Marcus; tertile=begin; p=0.72**
>
> O’Flaherty flipped the bacon. “ [TARGET] Your heart missed two beats.” Daniel stared at him. “

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

- **Main:** hear, listen, listening, heard, hearing, me, you, listener, want, can
- **KeyBERT:** overheard, recently, voices, latest, ye, discussing, um, sir
- **POS:** fishing, folks, options, quality, exact, latest, explanation, notes, voices, emotions
- **MMR:** overheard, fishing, discussing, spilling, begging, notes, voices, process, emotions, fault

**BERTopic representative docs**

> 1. just listen to me.

> 2. if only you'd listen—" "i've been listening to you drivel on about geoffrey saunders for as long as i care to," burke said. "

> 3. he just wouldn’t listen, that’s all.

**Stage-08 / Stage-07 snippets**

> 1. that’s what i’ve heard.”

> 2. did you hear a word i’ve been saying?”

> 3. no, i’ve still heard nothing.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Sweet Forty-Two — Andrea Randall; tertile=middle; p=0.70**
>
> Regan’s eyes, though, looked anything but protected. “ [TARGET] Can you just ... hear me out for a second?” I grabbed the fabric of my apron, twisting it around my hands.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Fat Girl — K.L. Montgomery; tertile=end; p=0.67**
>
> I shrug. [TARGET] I've been listening to hard-to-hear things my whole life. If living with my mother hasn't prepared me, I don't know what else would. "

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Her Brother's Keeper — A.J. Downey; tertile=end; p=0.65**
>
> I was trying to impress my dad, and it was wrong, but, Maren,” I yipped when I tried to side step him and he grabbed me by my shoulders to bring me back in line with his gaze. “ [TARGET] Maren, no , you have to listen to me!” he grated and gave me a rough shake.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Chade — Montana Ash; tertile=middle; p=0.64**
>
> He can. [TARGET] So let’s hear what he has to say, hmm?” Cali’s ice-blue eyes narrowed in warning and he watched in awe as the rest of the men shuffled a little before also sitting down.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · The bachelor — Carly Phillips; tertile=middle; p=0.66**
>
> I wouldn’t call you an angel, but you are looking out for me. [TARGET] I appreciate that even if I don’t like what I’m hearing.” A regret-filled smile tilted her lips. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · The bachelor — Carly Phillips; tertile=middle; p=0.70**
>
> Any relationship that resembles your mother and father immediately gets your stamp of disapproval. [TARGET] I’m just not up to hearing it.” Charlotte’s heart hammered in her throat as she walked over to her best friend. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · I Want to Bite on Your Ears — Marcy Jacks; tertile=middle; p=0.62**
>
> Charlie ducked his head. “ [TARGET] Well, it’s hard for me to not hear anything with two sets of ears.” “ Those work?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · I Want to Bite on Your Ears — Marcy Jacks; tertile=end; p=0.62**
>
> The wolf ears on top of Charlie’s head fell down like a kicked dog’s. “ [TARGET] You want me to keep it quiet?” “ Just for now, baby,” Dane said. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · A Home of Her Own — Brenda Novak; tertile=middle; p=0.62**
>
> Rebecca asked, coming to take her son, who was wide awake and demanding to be fed. [TARGET] Now pretty much everyone was listening. “ She has family in the Washington area.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · McKettricks of Texas: Garrett — Linda Lael Miller; tertile=end; p=0.54**
>
> I promise.” “ [TARGET] I don’t know what we’ll do if he won’t listen to you,” Rachel fretted. With that, she nodded a farewell, put on her jacket and hurried away.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Choosing Christmas — Danielle Stewart; tertile=middle; p=0.70**
>
> All he had to do was sign payroll and fire a guy for fooling around with his girlfriend in an empty break room. “ [TARGET] You’re not hearing what I’m saying.” Sean cleared his throat loudly, obviously trying to make sure he had their attention. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Reckless Remedy — Rinelle Grey; tertile=end; p=0.66**
>
> Then again, he’d been understanding and typing it for a few weeks now, he’d simply lacked the vocal ability to make the right sounds. “ [TARGET] You have no idea how long I’ve wanted to hear it.” Amelie squeezed his hand.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Crush du Jour — Micol Ostow; tertile=begin; p=0.41**
>
> A couple at the booth next to us shot me a look. “ [TARGET] No ’unless,’” I repeated, this time at a more reasonable volume. “ It’s just weird.” ”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · The Horseman — Jillian Hart; tertile=begin; p=0.67**
>
> The sharp scrape of the wooden legs against the floor came as harsh as the fear on the woman’s face. “ [TARGET] I’ve heard what they’ve been saying, the two of them, when they think no one can hear. They intend to find a situation for you, and it won’t be a pleasant one.” “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Beneath the Surface — M.A. Stacie; tertile=middle; p=0.65**
>
> He had never skipped work before, so he should make it a day to remember. “ [TARGET] Well, I guess I should have listened to you, huh?” She punched his shoulder.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · The Italian's Passionate Return — Elizabeth Lennox; tertile=end; p=0.60**
>
> I want you. [TARGET] Over and over again, I’ve told you to think about the two of us and our relationship but you’re not hearing me. You keep thinking that it’s only sex between us, or only Dylan that I want.”

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

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · The Blue Room Vol. 5 — Kaiiln Gow; tertile=middle; p=0.64**
>
> Keep this bed warm for me for when I get back. [TARGET] I'm going to miss you every second of the day. I murmur his name involuntarily.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Wolf's Mate — Chantal Fernando; tertile=end; p=0.68**
>
> I tease, burying my face in his neck. “ [TARGET] Are you sure it’s only him who misses me?” “ I’m sure the others miss you too.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Sinner's Craving — Megan   Elizabeth; tertile=middle; p=0.63**
>
> Usually, they did something together to remember him. “ [TARGET] We all miss him,” Bishop murmured. It was unfair the way they lost Rev. So stupid and reckless.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Blueberry — Glenna Thomson; tertile=end; p=0.81**
>
> I just . . . [TARGET] Don’t you miss me at all?” “ Of c-c-c-course.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Here Kitty, Kitty — Joyee Flynn; tertile=middle; p=0.60**
>
> It felt nice. [TARGET] I’d missed my family so much, and now that we’d seemed to get the tears and heartache out of the way, we were having fun. “ It’s been my kitchen since Ty’s ma passed.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Here Kitty, Kitty — Joyee Flynn; tertile=middle; p=0.67**
>
> Waving him over, he smiled widely at me before hugging me. “ [TARGET] I missed you, little bro,” he whispered in my ear. “ I’m glad you’re safe now.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Fatty Patty — Kathleen Irene Paterka; tertile=middle; p=0.75**
>
> We’ve talked every day since he’s been gone, more than we ever do when he’s home. [TARGET] I didn’t count on missing him so much. “ Where are you?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · The End of Our Story — Meg Haston; tertile=middle; p=0.68**
>
> I want to stroke his hair, its sunset colors, the way I did when we were kids and he couldn’t sleep. [TARGET] I miss him being this close. “ Quit being psycho,” he tells the television. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Veil of Midnight — Lara Adrian; tertile=end; p=0.60**
>
> Okay.” “ [TARGET] While I was in there, I also brought you something I thought you might be missing.” He leaned over to the stash of weapons and other assorted supplies he’d retrieved and picked up the silk-and-velvet package that belonged to Renata. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Veil of Midnight — Lara Adrian; tertile=middle; p=0.42**
>
> The bait you laid out to attract Rogue vampires. [TARGET] The suckhead you brought back with you here tonight…I saw it all.” Lex scoffed. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · The Men with the Golden Cuffs — Lexi Blake; tertile=begin; p=0.72**
>
> He took her right hand and pulled it down. “ [TARGET] I think there’s a part of me you missed.” His cock.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Never Never — Colleen Hoover; tertile=middle; p=0.49**
>
> I ask her, just as we’re finishing up our meal. “ [TARGET] Dude, you can’t miss practice again,” Andrew shoots in my direction. “ Coach won’t let you play tomorrow night if you do.”

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · The Emerald Prince — Kayci Morgan; tertile=begin; p=0.54**
>
> But there must be some diplomatic mission you can send me on. [TARGET] Some excuse we can give for my absence.” One of the king’s advisors spoke up. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · Ely Jesse and Robin's Guide to Asexuality — R.J. Seeley; tertile=begin; p=0.60**
>
> Why did you wake up?” “ [TARGET] Because you disappeared.” He replied, then he smiled at me, “I suddenly felt cold and discovered that I actually needed the toilet.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · The Vampire and the P.I. — J.P. Bowie; tertile=begin; p=0.60**
>
> I wonder what is stirring them up. [TARGET] We’re missing something.” He rubbed his temples. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Compromised!: A Pride & Prejudice Variation — J. Dawn King; tertile=end; p=0.49**
>
> Lydia Bennet lifted the loosened curls from her neck with one hand while fanning herself with the other. “ [TARGET] Of all the unattached men in attendance, you are the last one I hoped to find on the balcony.” Fitzwilliam Darcy could remember few times in his life when he had been as miserable.

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

- **Main:** eyes, close, closed, blink, my, open, contacts, opened, eyelids, your
- **KeyBERT:** blinked, blinking, terrified, cried, focusing, afterward, tentatively, wrists, rapidly, narrow
- **POS:** drift, wrists, plastic, anticipation, tense, narrow, faces, closed
- **MMR:** blinking, fluttered, tentatively, instructed, sinking, terrified, wrists, anticipation, faces, pounding

**BERTopic representative docs**

> 1. i blink rapidly, trying to wrest the salty water from my eyes.

> 2. lights began to blink inside the chamber, so i closed my eyes.

> 3. i blink my eyes open against bright lights.

**Stage-08 / Stage-07 snippets**

> 1. i closed my eyes as it all hit me at once.

> 2. keep your eyes closed until i tell you to do otherwise.” “

> 3. feeling tired all of a sudden, i closed my eyes.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Black Lace — J.V.K.; tertile=end; p=0.71**
>
> He takes it from me but has me leave my hands where they are. ' [TARGET] Close your eyes and keep them closed,' he says seriously, and I realise what's coming. He pauses before striking my hands with the cane and I cry out in pain. '

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · The Healing Power of Sugar — C.L. Stone; tertile=middle; p=0.70**
>
> ♥♥♥ A gentle touch on my shoulder woke me. [TARGET] My eyelids parted, taking in the darkness and the ceiling above me as my brain struggled to catch up. “ Miss Sorenson,” said a quiet, yet powerful voice.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Losing Her — Cori Williams; tertile=begin; p=0.62**
>
> I giggled, my breath catching when he pushed in one finger and then two. [TARGET] My eyes closed and my head tipped backwards as he started a slow, torturous rhythm. This had to be a dream—one I didn’t want to wake up from.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Roses in Amber: A Beauty and the Beast story — C.E. Murphy; tertile=middle; p=0.55**
>
> His mouth was not made for kissing. [TARGET] Nothing either of us could do would change that, but our foreheads touched and I closed my eyes, listening to the tandem harshness of our breath and searching for just a little more bravery. He whispered, "Amber," precursor to a familiar question.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Virtual Love — Kim Malone Scott; tertile=middle; p=0.68**
>
> I moan softly as his lips graze my ear. [TARGET] Involuntarily my eyes close as the sensation travels all the way down my spine. He isn’t exaggerating about how much I love it when he pays attention to that area.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Monster Stepbrother — Harlow Grace; tertile=end; p=0.76**
>
> I was desperate to find Maya. [TARGET] I closed my eyes for a moment to gather my thoughts. When I opened them a few moments later, my gaze fell on the rubbish bin.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_014 · Green Valentine — Lili Wilkinson; tertile=end; p=0.74**
>
> I didn’t mean that— I don’t even believe in Dev’s stupid system!’ [TARGET] My eyes filled with tears, and I squeezed them shut, trying to shake them off. When I opened my eyes again, Hiro was gone.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · Chasing Spring — R.S. Grey; tertile=end; p=0.66**
>
> I reached out to grab a card off the top of the deck and everyone shouted. [TARGET] I blinked my eyes again, feeling the same dizziness overtaking me. When I moved to sit back in my seat, a sharp feeling of vertigo overtook over me.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Wild Horses — Linda Byler; tertile=middle; p=0.57**
>
> Keep working. [TARGET] Painfully blinking. Why was a blink so excruciating?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Ascension — S.W. Frank; tertile=end; p=0.41**
>
> Vanna gave a curt nod before pumping several shots into Sophie’s heart, but out of respect, she left her lovely face intact. [TARGET] 28 Legs crossed in a full lotus position, eyes closed, Selange meditated. Her mind and body aligned. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Dragon & Crow 2 — Alex A. Akira; tertile=middle; p=0.47**
>
> Spearing a piece of tuna, he plunged the tasty morsel into his mouth, chewing grumpily as he perused the lengthy list of mail in his inbox. [TARGET] Shit, Tommy, I’m busy, you should have talked to me yesterday... He closed his eyes, feeling the protein trickle though his system. God, he was pretty hungry.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Just To Be With You — Bella Andre; tertile=middle; p=0.65**
>
> Moving his free hand to the nape of her neck, he threaded his fingers into the wet tangle of her hair. “ [TARGET] Open your eyes, sweetheart.” She blinked once, twice, before she was able to focus. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Dying to Have Her — Heather Graham; tertile=middle; p=0.48**
>
> You’re tense. [TARGET] Stop wrinkling up your forehead.” Serena sat still while he worked on her face. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Thief of Hearts: Tempted in Thailand — E.M. Lynley; tertile=middle; p=0.46**
>
> Want a swig? [TARGET] I don’t think there are any glasses in here.” He rattled the remaining items in the box just to verify. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Harvested — Alex Morgan; tertile=begin; p=0.49**
>
> Tori hands Jon a leather jacket and crash helmet. “ [TARGET] The visor’s blacked out so they can’t locate us using your eyes.” He hasn’t a clue what she’s talking about. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · A Comedy of Erinn — Celia Bonaduce; tertile=end; p=0.47**
>
> I always wonder what aliens would think if they saw us at a movie theater before the show begins,” Virginia said. “ [TARGET] All these people staring at a blank screen.” “ Interesting,” Erinn said, and sipped her tea. “

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

_16 examples from 15 books; ±1 context on 16_

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

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Bed Of Roses — Gemma Brocato; tertile=end; p=0.50**
>
> Gunnar shrugged. [TARGET] He didn’t mind bothering Jem if it got him any closer to finding Mal. He joined Sam at the table, dropping down on one of the hard wooden chairs. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Two Hearts in Winter — Donna Fasano; tertile=end; p=0.39**
>
> She was that happy. [TARGET] Oliver picked up his son, and Amelia carried the new kite. The Ferguson’s waved to the crowd as they filed off stage and down the steps. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Deadly Odds — Adrienne Giordano; tertile=end; p=0.43**
>
> I heard him on the phone in his office. [TARGET] Marcia is trying to get his ass moving. What’s this meeting?” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · A DISTANT HEART — Sonali Dev; tertile=end; p=0.40**
>
> You would have to talk to the transplant surgeon about that.” [TARGET] Rahul turned to him with an alertness that had DCP Savant written all over it in block capitals. “ Do you do only postoperative care then?

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Lake Como — Anita Hughes; tertile=middle; p=0.50**
>
> My grandmother used to take me to Santa Cruz and I’d fish off the pier.” “ [TARGET] I always wanted to be Tom Sawyer.” Angus hooked a worm on the rod. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Wynter's Horizon — Dee C. May; tertile=end; p=0.52**
>
> She couldn’t afford to take the stupid chances we did. “ [TARGET] Oh, be quiet, Buffy.” I shot Quinn the nastiest look I could.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Captive In His Castle — P.J. Fox; tertile=end; p=0.50**
>
> I always am.” [TARGET] Belle punched him in the ribs. He laughed.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · The Planet Whisperer — E.E. Montgomery; tertile=end; p=0.39**
>
> Now he’s lonely and craves a relationship Baxter doesn’t want. [TARGET] Then Aidan meets Detective Sam Walters while consulting on a murder investigation and his dreams are suddenly invaded by a man who makes Aidan want to strip faster than an attack by green ants. Too bad Sam is straight.

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

- **Main:** breath, breathe, deep, breathing, took, exhale, sucked, inhaled, lungs, catch
- **KeyBERT:** breaths, lungs, breathed, exhaled, blowing, gasp, terrified, pressure, flowed, rushed
- **POS:** breaths, lungs, internal, gasp, moaning, stool, exchange, insides, sentence, damp
- **MMR:** breaths, lungs, faltered, flowed, moaning, blowing, breathed, terrified, pounded, damp

**BERTopic representative docs**

> 1. but i can breathe now.”

> 2. didn’t seem to breathe.

> 3. and i can’t breathe.

**Stage-08 / Stage-07 snippets**

> 1. ragged, unsteady breaths grated from my lungs.

> 2. we’ll just stop moving until you catch your breath.

> 3. you’ll have to hold your breath through the thick of it.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Eluding Nirvana — V.L. Brock; tertile=end; p=0.73**
>
> Everything felt like I was on the cusp of unconscious. [TARGET] Deep breaths were drawn into my lungs, as I contended with that potent urge to let my head fall forward. Although I couldn’t feel my legs and lights beyond my windshield were distorting and dancing, I smiled at his words while my eyes surrendered to a protracted blink. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Falling for Him — Jessica Roe; tertile=end; p=0.67**
>
> We decided to give things another go.” [TARGET] I can't breathe through the crushing pressure in my chest. I can't breathe.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Game of Vengeance — Amanda K. Byrne; tertile=middle; p=0.79**
>
> He knows it’ll mess me up.” [TARGET] I suck in a breath, blow it out, imagining some of the tension draining away with the exhalation. “ Can you help me get her and Charlie to Colorado today?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Fighting Blind — C.M. Seabrook; tertile=middle; p=0.74**
>
> No.” [TARGET] Closing my eyes, I inhale a slow steady breath. I can’t think when he’s touching me.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · King of Hearts — Cheyenne McCray; tertile=middle; p=0.85**
>
> Do you like it?” [TARGET] I sucked in a deep breath. “ Uh-huh.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · The Last Girl — Kitty Thomas; tertile=end; p=0.70**
>
> I’m scared of what will happen to you if I do.” [TARGET] My breath has gone still and I have to concentrate to get it going again. A single tear slips down my cheek, and I don’t notice it until it drifts into the corner of my mouth and I taste the salt.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · The Darkest Joy — Marata Eros; tertile=begin; p=0.77**
>
> I can do this . [TARGET] I breathe in deeply and exhale slowly. “ Hi.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Song of the Fireflies — J.A. Redmerski; tertile=begin; p=0.72**
>
> And so I did. [TARGET] I took another deep breath and began to tap my fingers against my knees out of nervousness. “ Lissa introduced me to Garrett,” I said. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · The Grey God — Lizzy Ford; tertile=end; p=0.52**
>
> Air? [TARGET] Now you’ll tell me it’s illegal for her to breathe the air down there.” “ It wasn’t air she stole,” the Other replied. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Black Dragon — Vijaya Schartz; tertile=end; p=0.49**
>
> Could Talina do it, for this one man? “ [TARGET] How could they possibly breathe in your city of walls? They are accustomed to the jungle, the animals they love, the fragrance of tropical flowers, the mossy ground under their bare feet...” “There are wide open spaces in Yalta, like the lake.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Where the Grass is Greener — Debbie McGowan; tertile=middle; p=0.53**
>
> But lying in bed together? [TARGET] What would you think if I pulled you close …floating in the air like dust motes in the light? Harrison couldn’t form words.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Breakfast in Bed — Rochelle Alers; tertile=begin; p=0.54**
>
> Hannah pushed to her feet. “ [TARGET] I’m sitting here running my mouth when you need to settle in and unwind. If you want to hang out together, then send me a text.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Stormcrow Castle — Amanda Grange; tertile=end; p=0.68**
>
> I have sent her back to the castle.’ ‘ [TARGET] I feel in need of a breath of air,’ said Anna. ‘ You cannot go on deck, it is not safe.’ ‘

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · The Half-Breed Who Found His Other Half — Scarlet Hyacinth; tertile=begin; p=0.65**
>
> Thank you,” he said. “ [TARGET] I felt like I was choking down there.” He leaned against the banister, staring into the distance. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Black Rook — Kelly Meade; tertile=begin; p=0.64**
>
> Her pupils are dilated,” Dr. Mike said. “ [TARGET] Are you feeling any sort of numbness or shortness of breath?” “ No, just dizzy.” “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Black Rook — Kelly Meade; tertile=end; p=0.48**
>
> Mostly, yes. [TARGET] I let them pass out before things got too heavy. Sometimes they assumed we had sex and bragged to their friends and I never contradicted it.

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

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · The Demon Kiss — Lacey Weatherford; tertile=begin; p=0.72**
>
> I can’t lose you.” [TARGET] He pulled me into his arms, wrapping me in a tender embrace. “ I love you, Dad,” I said, hugging him back, squeezing him really hard since I didn’t know when I would get to see him again. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Entwined with You — Sylvia Day; tertile=middle; p=0.81**
>
> Hi, Monica.” [TARGET] Megumi came forward to give her a hug. “ How are you?” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Resonance — Lina Andersson; tertile=begin; p=0.80**
>
> I’ve missed you.” [TARGET] He gave her a hug, or more like she was giving him one. She still had the ability to surround him and make him feel safe.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Beast of All — J.C. McKenzie; tertile=end; p=0.71**
>
> My wolf popped into my head and gave my brain a nudge. [TARGET] Wick reached out and slid his arm across my shoulders, pulling me in for a side-hug. “ We’ll get him.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · A Modest Proposal — Felicitas Ivey; tertile=end; p=0.64**
>
> Ikkyu’ma laughed, and Leif reluctantly rolled off me and staggered into the cabin, looking for a more comfortable and cleaner place to collapse. [TARGET] Ikkyu’ma helped me up and kissed me, folding me in his arms and rocking me gently. “ Shaku, you will love it there.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · After Sundown — Anna J. McIntyre; tertile=middle; p=0.69**
>
> The realization made him want to howl in frustration. [TARGET] Without considering the total impropriety of his actions, Cole stepped behind Kit and wrapped his arms around her, giving her an affectionate hug, while pressing their bodies together. Instead of pulling her hands from the pumpkin, she squealed in protest. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · After The Deed — Netty Ejike; tertile=end; p=0.62**
>
> Tremendously. [TARGET] Michael turned to her twin sister, gave her a high five, and then they gave their new-found daddy a tight hug. Brad laughed and heaved a huge sigh of relief.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · A Bear's Bear — Toni Griffin; tertile=end; p=0.73**
>
> I'm so glad you guys are here." [TARGET] Matthew hugged his mom, giving her a kiss on the cheek before he turned to his father and hugged him too. " How long can you stay?"

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · The Daddy Spell — Josie Malone; tertile=begin; p=0.58**
>
> She’d think about the accident later, after her head quit hurting. [TARGET] She hugged Luke tightly for a moment, then rested one hand on the German Shepherd’s solid, eighty-pound body and struggled to her feet. Her ribs throbbed in protest.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Desires — R.  Rose; tertile=end; p=0.65**
>
> She and her girlfriends came early.” [TARGET] He hugs his mother and sisters, pumps my hand, cheek-kisses Sondra and slaps Leo on the back. “ Sal, this is not a Catholic church,” his mother complains. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Headlights in the Snow — Sara's Girl; tertile=middle; p=0.64**
>
> I wrapped my arms around his shoulders, just like I always did with Bralix. [TARGET] Again, this felt more intimate, like a hug. He hadn’t taken off flying just yet.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Blood: Episode 1 - Curse — D.S. Wrights; tertile=begin; p=0.49**
>
> Achknowledgements A very special Thank You goes to the one and only Pamela Pulsifer-Swan. [TARGET] First and foremost, hugs and kisses to Gill and Amanda. Thank you to Amy and Ella for your ongoing support!

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Party of Three — Lacey Alexander; tertile=end; p=0.59**
>
> She sat down on the long, sofa-like glider but didn’t set it in motion, instead leaning back against one side arm and pulling her legs up next to her, knees bent. [TARGET] She hugged them lightly as she looked out into the quiet green surroundings, liking the way the trees almost seemed to cocoon the house. Maybe it, again, made her feel safe, and like as long as she was here, her feelings for both men were somehow okay.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · While You Were Dead — C.J. Snyder; tertile=end; p=0.73**
>
> They kept him from holding her close enough, feeling her tension-wrought, shuddering body next to his own. [TARGET] His arms couldn’t get enough and he couldn’t stop crying, kissing her tangled hair, hugging her tighter, closer and whispering, “thank you.” Lizzie didn’t object to the over-long hug, but she was getting a little frustrated by his inattention to her words. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Room For Love — Sophie Pembroke; tertile=middle; p=0.60**
>
> Not good. [TARGET] Uncle Patrick gave Carrie a warm hug on the steps, but Aunt Selena only managed a vague smile as she passed, keeping a good foot of air between her and her husband. Uncle Patrick wasn’t going to give Carrie anything she hadn’t earned, even if Selena agreed to it.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · What About Now — Grace R. Duncan; tertile=middle; p=0.73**
>
> Don’t worry, dear, it’s not a bad thing.” [TARGET] She patted his face, gave Rafe a hug, then took the cuffs from him. He picked up the pledge sheet. “

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

_16 examples from 16 books; ±1 context on 16_

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

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · The Fly House — Misty Paquette / Misty Provencher; tertile=begin; p=0.53**
>
> You're okay with the paps snapping photos of my bumper stickers? [TARGET] I've got some new ones on there..." When her bumper was full, she'd started tattooing the back panels of her decrepit Dodge Ram and slowly, the stickers had consumed her ride’s whole tailgate. They were starting to slop over onto the back panels.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Starting Over — Jen Silver; tertile=middle; p=0.72**
>
> Each ear had several piercings with a recent one at the edge of one eyebrow. [TARGET] The sleeveless top she wore revealed tattoos on each shoulder and a larger one down her left arm. But it was the dark circles under her eyes that made her look worse than Ellie felt. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · His Young Queen — Tiff P. Raine; tertile=begin; p=0.61**
>
> How had she forgotten the square cut of his goateed jaw? [TARGET] And had her subconscious seriously neglected to add the thickness of his inked neck to her many dreams, and that gorgeous tattoo of the Grim Reaper holding up a royal flush? It stretched from below his left ear to disappear under his shirt.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Heart Choice — Robin D. Owens; tertile=middle; p=0.36**
>
> Oh, yes," he said quietly. " [TARGET] I can see the aura of Flair—the trace of the person who did this, but I don't know the trail. It is not—" "Not what?" "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Imperative: A Tale of Pride and Prejudice, Volume 1 — Linda   Wells; tertile=begin; p=0.45**
>
> Richard sniffed and watched. “ [TARGET] But decidedly without the tact.” “ Agreed.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Bodyguard Reunion — Margaret Daley; tertile=end; p=0.39**
>
> She didn’t even complain.” “ [TARGET] Mary has received a lot of publicity over this snakebite, so anything is possible. I won’t rule her out until we discover who is doing this to the Zimmermans.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Guardians of the Heart — Loree Lough; tertile=middle; p=0.27**
>
> Bess , darlin’,” he said, helping her climb over the top rung, “ are you all right?" " [TARGET] Ith only a thmall thplinter. I think I'll thurvive."

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · The Promise — Brenda Joyce; tertile=begin; p=0.69**
>
> I don’t care which one, but the less the guy on the cover is wearing, the better. [TARGET] Tattoos are a plus. Leather is another plus.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Another Chance — Sandra Cuppett; tertile=middle; p=0.35**
>
> She stretched her arm toward the big tepee. “ [TARGET] The skins for the tepee were from previous years.” Jordan looked, then, at the leather covering of the lodge and realized it was real leather hides stitched together, not tarpaulin as she had imagined.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Breaking All the Rules — Kerry Connor; tertile=begin; p=0.67**
>
> He was clearly military, not exactly a rare sight in San Diego. [TARGET] Judging from the tattoo peeking out from his shirt sleeve, a Marine. As she watched, his smile deepened, giving her a glimpse of perfect white teeth.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Doubting Abbey — Samantha Tonge; tertile=middle; p=0.49**
>
> Blade,’ he said and firmly enclosed my small hand in his. [TARGET] He wore black leather gloves and for some reason I wanted to feel his skin, ‘I’m Gemma. Love the outfit.

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

- **Main:** handle, fucked, screw, screwed, messed, deal, can, up, handled, don
- **KeyBERT:** handled, messed, dealt, expect, holds, surely
- **POS:** addition, occasional, regular, task, emotional, pregnant
- **MMR:** messed, handled, addition, pinned, task, holds, emotional, em, pregnant, expect

**BERTopic representative docs**

> 1. i don’t think i could handle that.” “

> 2. i don’t know if i can handle it right now.”

> 3. i don’t know how you handle it all.”

**Stage-08 / Stage-07 snippets**

> 1. i’ve got things handled here.

> 2. it’ll be handled by then.”

> 3. we’ve messed up everything.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Choosing Christmas — Danielle Stewart; tertile=end; p=0.62**
>
> I’m glad you have me all figured out. [TARGET] I’ll go ahead and consider myself fixed now that you’ve shed such light on my psyche.” “ That wasn’t what I was trying to do.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Cutting Out — Mickie B. Ashling; tertile=begin; p=0.59**
>
> You know about Noriko’s ancestry.” “ [TARGET] Tell me again so I know what I’m dealing with.” “ Noriko’s biological grandmother, Mieko, lived and worked in the same okiya , or geisha house, as my grandfather’s mistress, Rieko.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Submission is Not Enough — Lexi Blake; tertile=begin; p=0.68**
>
> Don’t tease me about that. [TARGET] I can handle everything but that.” She sobered a bit. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Unstable — S.E. Hall; tertile=begin; p=0.55**
>
> We’re in paradise, with our best friends, for the wedding of the century if Whitley has anything to say about it. [TARGET] Whatever’s bugging you, it can’t possibly be bad enough to ruin all that, can it?” That’s the thing, I’m not exactly sure what’s troubling me, or why.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · How to Break Up with an Alien — Magan Vernon; tertile=middle; p=0.50**
>
> I didn’t know anyone else that actually read my blog besides people from the internet. “ [TARGET] Yeah, I haven’t been able to keep up with that too much lately.” “ Oh, that sucks.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Twisted Summer — Lucy V. Morgan; tertile=end; p=0.54**
>
> I could use a bright young mind for all my admin. [TARGET] So if you think you can handle a year of my eco crap …” “I can handle it.” My smile grew, and I braved a little kiss, just brushed it over his lips.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Poster Boy — Anne Tenino; tertile=end; p=0.54**
>
> Pretend your arms are glued to the bed,” Toby whispered before kissing Jock’s now-exposed abdomen, tongue swirling into his belly button. “ [TARGET] If you’re a compliant boy now, you can do whatever you want to me later.” Jock shivered from his words and his breath blowing on the skin he’d wetted. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · Get Real — Tellulah Darling; tertile=end; p=0.59**
>
> Javier sounded tired when he said, “You’re not in any position to make requests, Rafael. [TARGET] Thanks to the two of you, I have to do major damage control.” I opened my mouth to protest but he cut me off. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Promise Me Texas — Jodi Thomas; tertile=begin; p=0.51**
>
> They kill game, butcher hogs, and fight until they’re bloody, but most can’t stand it when a lady talks about her monthly time. [TARGET] It’s something they don’t understand and can’t seem to deal with.” “ Oh.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Othrinia's Rain — A.J. Adwen; tertile=begin; p=0.52**
>
> He stares at me, unfazed. “ [TARGET] You aren’t accustomed to a lot of things that you should be.” I lock my knees to keep them from trembling. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Sake Bomb — Sable Jordan; tertile=end; p=0.66**
>
> Won’t even move. [TARGET] Just know it’s gonna piss me off, so you better be able to handle what you get back.” Her gaze darted away, came back to him.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Lionheart — Fran Seen; tertile=end; p=0.47**
>
> I’d stomped on Charlie’s hopes and dreams when I recklessly stormed into his life. [TARGET] I hadn’t meant to, but I crossed our preset boundaries and unhinged the delicate balance of our lives. I was selfish, and I knew it.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Lip Lock — Susanna Carr; tertile=middle; p=0.52**
>
> Glenn paced faster. “ [TARGET] This woman may have taken all of our ideas, which will bring in millions, and all you can say is that you messed up?” Kyle locked eyes with the other man.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Ervin's Dilemma — Stephani Hecht; tertile=begin; p=0.51**
>
> Hey, don’t feel that way about yourself,” Braxton said, his features softening. [TARGET] “I’m just overly bossy and stubborn. Just because you let me get my way doesn’t make you weaker.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Eden's Fire — Samantha Holt; tertile=begin; p=0.44**
>
> Humans have certainly made many mistakes, I guess. [TARGET] We should never have let it get this far, but what does this have to do with me? What sort of protection can you offer if you’re going to leave us to our fate?” “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · What a Rich Woman Wants — Barbara Meyers; tertile=end; p=0.47**
>
> Your father let him oversee the operation in San Salvador against his better judgment. [TARGET] Brad insisted he could handle it, would handle it. “ Brad was the baby of the family.

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

- **Main:** ready, done, start, finish, finished, re, we, starting, are, yet
- **KeyBERT:** sentence, sir, shortly, fitting, planning
- **POS:** fitting, sentence, sir
- **MMR:** fitting, shortly, dealing, gotta, curved, sentence, planning, sir

**BERTopic representative docs**

> 1. please, just let me finish.

> 2. i’ll just finish up here first.”

> 3. now you have to finish it or it will be finished for you.” “

**Stage-08 / Stage-07 snippets**

> 1. but i’ll start first.

> 2. we’ll start there and see where it goes.”

> 3. we’ll let you know when we’re done,” [person] said.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Essentialism: Bridgette & Troy's Story — L.K. Collins; tertile=begin; p=0.73**
>
> The door is shut. [TARGET] We are finished, before we even started. The tears won’t stop.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · A Gentleman's Fate — A.J. Linn; tertile=begin; p=0.76**
>
> She turns to address the investors, smiling graciously. “ [TARGET] Gentlemen, if you’ll excuse me, it looks as though we’re ready to begin.” Turning her attention back to me, she holds out her arm directing me towards the podium. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · A Gentleman's Fate — A.J. Linn; tertile=begin; p=0.64**
>
> She shakes her head no, then steps away for a moment making a call. “ [TARGET] You’re going to have to start it up for me.” So could you get the fuck off of the phone?

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Tempted — Alana Sapphire; tertile=end; p=0.68**
>
> I swear I’ve tried balancing these books a million times. [TARGET] I get halfway through and have to start all over.” “ You’re still not going to tell me anything about the party?” “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Almost Perfect — Julie Ortolon; tertile=begin; p=0.68**
>
> Mama’s voice came from one of the seated silhouettes. “ [TARGET] We haven’t started yet.” “ Yeah, we’re waiting for God to join us,” a younger voice said. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · When It Happens — Susane Colasanti; tertile=begin; p=0.75**
>
> Which is a game I don’t feel like playing. “ [TARGET] I have to get ready,” I say. “ You can’t just barge in here and start ramming into me.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · When It Happens — Susane Colasanti; tertile=middle; p=0.75**
>
> The question is . . . [TARGET] are you ready to do this?” “ Yeah.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Home and Heart — Chris Quinton; tertile=begin; p=0.69**
>
> That's quick. [TARGET] Are you okay to start so soon?" Julie asked worriedly. "

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Full Court Press — Lolah Lace; tertile=end; p=0.59**
>
> I wasn’t sure if Jack was being sarcastic or not. “ [TARGET] I’m going to follow your lead.” I hope that worked for him.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Darkness Possessed — Stephanie Rowe; tertile=end; p=0.74**
>
> Ben managed a nod. " [TARGET] Yeah, well, I'm not ready yet." " We gotta get him back on the horse," Haas said. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Surviving You — Dawn A. Keane; tertile=middle; p=0.47**
>
> Sure am, beautiful. [TARGET] The English school summer holidays start soon so there’s nothing to stop us, if you’re up for it.” Before I can properly respond to that delightful idea, my phone starts to ring.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Beyond the Rising Tide — Sarah Beard; tertile=middle; p=0.54**
>
> He’ll know that I love Kai. [TARGET] I have to pull myself together if I’m going to make it through tonight. “ Right on,” Tyler says.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · The Perfect 10 — Louise Kean; tertile=middle; p=0.68**
>
> When will you start?’ ‘ [TARGET] You leave me the details, we’ll start straight away.’ When Sheldon finally leaves, having disclosed all the necessary information, Cagney sits back in his chair, cracks a nut in one hand, and holds Sophia Young’s photo in the other.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Reason and Romance — Debra White Smith; tertile=end; p=0.54**
>
> I do believe you’ll sort it out if you keep trying, though,” she encouraged. “ [TARGET] I just wish I knew where to begin.” Anna turned her hand up and squeezed Elaina’s fingers. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · The scarlet kimono — Christina Courtenay; tertile=middle; p=0.70**
>
> I’d be happy to teach you. [TARGET] Do you want to begin right now?’ ‘ Why not?’

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Without a Net — Lyn Gala; tertile=end; p=0.67**
>
> [TARGET] Chapter Twenty Two “You ready?” Travis asked. “

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

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Ciao — Bethany Lopez; tertile=middle; p=0.56**
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

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Perpetual Light — Jordan K. Rose; tertile=middle; p=0.47**
>
> Between us, Bess’s fingers search the tangle of bulbs, as if still looking for the burnt-out ones. “ [TARGET] Evan,” she says, “that day, last week, I went out to the pond, it was the day after the bear. After you …” I cannot seem to look at anything but her fingers. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Welcome to the Underworld — Con Template; tertile=middle; p=0.37**
>
> It would always be Yoori. [TARGET] It would only ever be Yoori. “ Get off me.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · East of Redemption — Molly E. Lee; tertile=end; p=0.49**
>
> [TARGET] Easton “YOU THINK BROWNIE is still out there?” Rain asked as she gazed through the window.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Mercury's Orbit — Lia Black; tertile=begin; p=0.38**
>
> He’d been drunk, and full of testosterone. [TARGET] Tammy, a fellow squad leader and the closest thing he had to a friend on the force, had dragged him out, insisting he celebrate the victory by getting laid. He hadn’t, but it was just his luck that he managed to run into someone who’d flirted with him there— on the moon of all places.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Top Men — G.A. Hauser; tertile=middle; p=0.53**
>
> Yes.” “ [TARGET] She’s okay with it, Jeff.” “ Too okay with it.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Fair Play — Janna Shay; tertile=end; p=0.55**
>
> On top of that, they were dancing a little too close, and she was smiling a little too much. [TARGET] Earlier she’d acted the same way with Dave. Damn!

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · Over the Fence — Elke Becker; tertile=begin; p=0.50**
>
> What other choice did she have? [TARGET] Chris had asked her to help with their parents. If she didn’t go, everything would fall on Chris and Kati.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Melting Shadows — Rhea Rhodan; tertile=middle; p=0.40**
>
> Max’s stiff gut turned to water. [TARGET] Delilah . What an ironic cover.

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

- **Main:** aiden, ezra, lex, addie, asher, verra, robert, ye, mused, working
- **KeyBERT:** blinked, promptly, sentence, faintly, stirred, speaking, shock, rushed, lets, emotional
- **POS:** enthusiasm, benefit, appropriate, stares, affection, disappointed, sentence, amusement, emotional, ability
- **MMR:** promptly, faintly, aimed, enthusiasm, wipe, provided, stirred, amusement, cocked, emotional

**BERTopic representative docs**

> 1. aiden’s private and professional lives collide when dawn's newest patient gets in trouble with the law.

> 2. to comprehend the events that had at some point unraveled right under his nose while he’d aimed desperately to spare aiden from harm.

> 3. he spoke to his pot, like he’d spoken to his knife or cutting board or whatever, every time he said something directed at ezra.

**Stage-08 / Stage-07 snippets**

> 1. i’ll be okay, i just need a minute,” aiden whispered.

> 2. aiden, i’ll let you know what transpires.

> 3. aiden asked, then quickly added, “god, sorry, lip zipped, swear, i’ll shut up.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · Midnight's Master — Donna Grant; tertile=middle; p=0.50**
>
> He wasn’t foolish enough to stay near her when she was in this kind of rage. [TARGET] Malcolm’s lips twisted in a rueful smile as he thought about his cousin, Larena, and the MacLeods finding the sword. It was just what he had expected them to do.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · White Tiger — Jennifer Ashley; tertile=middle; p=0.60**
>
> Kendrick stretched his back, the weight of the sword dragging at him. “ [TARGET] You know what happens if I sleep with Addison,” he said to Zander in a low voice. “ And what it will mean.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Trust — Brigham Vaughn; tertile=middle; p=0.67**
>
> Jeremy reached out and touched his knee where it stuck out from the robe. [TARGET] Evan’s skin tingled, but he forced himself to focus on Jeremy’s words as he spoke. “ I love that you said that, but I’m still scared you’re going to freak out when you see it.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Sugar and Ice — Aven Ellis; tertile=end; p=0.53**
>
> An icy cold feeling fills my chest. “ [TARGET] The last break up hit him hard, according to Gavin,” Veronica says knowingly, stroking her cascading locks. “ Paul said that, too,” Madison confirms.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Holed Up — Hank  Edwards; tertile=end; p=0.52**
>
> That could attract the attention of the police, and who knows where that might lead.” [TARGET] Pearce swallowed his anger, forced it into a corner of his brain, and tried to understand what Morgans appearance on the street outside the place he and Mark had holed up in meant. He took a step back, putting more space between them, and glanced up at the windows of the loft.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · The Magic Mirror and the Seventh Dwarf — Tia Nevitt; tertile=begin; p=0.54**
>
> With the minstrel.” [TARGET] Lars and Klaus looked at each other for a moment, dropped what they were holding and headed outside. The visitors were talking to Rudolph and Herr Dieter.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Travis — N. Kuhn; tertile=middle; p=0.80**
>
> Then I can see all of you.” [TARGET] When Aiden arrives, he gives me an up and down glance. “ You should put your hair up, it will set the pearls off better.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Irresistible Force — D.D. Ayres; tertile=end; p=0.62**
>
> How dare you!” [TARGET] Shay looked up slowly in answer to the angry whisper. “ You covered for your boss, didn’t you?

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Bodyguard Reunion — Margaret Daley; tertile=middle; p=0.44**
>
> Each held a gun in their hand. [TARGET] Brody calculated his chances of getting away without being killed and came up with nil. There was nowhere to run at the moment.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · For Now — Janae Mitchell; tertile=begin; p=0.32**
>
> U busy? [TARGET] Malynnn??? R u ignorin me?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Fractured Faith — Kristie Cook; tertile=end; p=0.41**
>
> Over here. ” [TARGET] Owen showed himself standing on the very space on the side of the other mountain where Mom had said to gather my people. Tristan spotted him first and gestured at him.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · The Perfect Find — Tia Williams; tertile=end; p=0.55**
>
> After a moment, she looked at Billie and gestured toward her son. [TARGET] Billie called over to The Baby and sent him running over to Jenna, clutching his iPad. Eric saw the little boy dashing toward them and, just as he was putting the words together to ask Jenna who he was, he went mute.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · A Serving of Scandal — Prue Leith; tertile=end; p=0.49**
>
> But as the lesson progressed he realised that Kate wanted the children to understand where chicken nuggets and fish fingers came from. [TARGET] Oliver kept half an eye on Kyle. Kate, he noticed, once she was satisfied that no damage had been done to the boy, studiously ignored him.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Yesterday's Heroes — Elizabeth Gannon; tertile=middle; p=0.49**
>
> Who am I? [TARGET] Dear Abby all of a sudden? I can’t tell you what you feel for the girl, Bro.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Vegas to Varanasi — Shelly Hickman; tertile=middle; p=0.45**
>
> I can sip it. [TARGET] And Nisha?” She’s halfway to my door when she turns and stops. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · This Same Flower — Augusta Li; tertile=middle; p=0.48**
>
> Patrick looked over at Evan, who sat at the end of the couch, apart from the rest of them, looking dejected and picking at a thread on the bottom of his shirt. [TARGET] Patrick felt like a tool, rejoicing about the upcoming wedding while Evan sat alone, afraid he’d never find anyone to love. He reached over and clasped Evan’s hand. “

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

_16 examples from 16 books; ±1 context on 13_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Clandestine Christmas — Elle James; tertile=middle; p=0.66**
>
> As soon as the rest of the house is asleep, we can meet in the office,” Chase suggested. “ [TARGET] I want to do some web surfing with a few of the names in that book.” “ Hank’s computer guru really is good at digging up interesting facts that have helped contribute to solving cases.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Rori and Jackson — Randi Alexander; tertile=end; p=0.58**
>
> Subscribe to my Newsletter so you can hear all the latest on my upcoming projects. [TARGET] If you liked reading Rori and Jackson, please do me the honor of returning to where you purchased the book, and to Goodreads (if you use that service) and post a review for me. Much appreciated!

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Capturing Forever — Erin Dutton; tertile=begin; p=0.58**
>
> Table of Contents Synopsis Acclaim for Erin Dutton’s Work By the Author Acknowledgments Dedication Prologue Chapter One Chapter Two Chapter Three Chapter Four Chapter Five Chapter Six Chapter Seven Chapter Eight Chapter Nine Chapter Ten Chapter Eleven Chapter Twelve Chapter Thirteen Chapter Fourteen Chapter Fifteen Chapter Sixteen Chapter Seventeen Chapter Eighteen Chapter Nineteen Chapter Twenty Chapter Twenty-one Chapter Twenty-two About the Author Other Erin Dutton Titles Available via Amazon Books Available from Bold Strokes Books

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Blade of Darkness — Dianne Duvall; tertile=middle; p=0.62**
>
> I’m working on a journal article. [TARGET] I just need to check a reference, and you can have the book back.” “ If you can do that here, in the reading room, then it’s no problem.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · The Epic Love Story of Doug and Stephen — Valerie Z. Lewis; tertile=middle; p=0.57**
>
> Now he’s got his wife and fetus and house in West Orange. [TARGET] And even if I blow everyone away with this article, even if I become a fabulously successful writer, I’ll just never have that again.” Stephen leaned back against the headboard and stretched his legs out, staring blankly at the ceiling.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Two Knights of Passion — Mellanie Szereto; tertile=begin; p=0.61**
>
> You do not have resell or distribution rights without the prior written permission of both the publisher and the copyright owner of this book. [TARGET] This book cannot be copied in any format, sold, or otherwise transferred from your computer to another through upload to a file sharing peer to peer program, for free or for a fee, or as a prize in any contest. Such action is illegal and in violation of the U.S. Copyright Law.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · This Ordinary Life — Jennifer Walkup; tertile=end; p=0.61**
>
> You put up with so much when I’m in novel-writing mode, and I thank you for not minding unfolded laundry or leftovers. [TARGET] And to all those whose enthusiasm for my books keeps me writing and excited to share them with you: Thank you, a million times, thank you! I read every reader email, post, or tweet with a huge smile on my face and a heaping dose of gratitude in my heart.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · Bridget Jones's Baby: The Diaries — Helen Fielding; tertile=end; p=0.61**
>
> Bill Sharp! [TARGET] Novelists yourselves, and, of course, distinguished critics: Quick thoughts, what do you make of it?” “ This is the single biggest pile of stinking unreadable shit I’ve ever had the misfortune to plough through,” said Tom O’Shea. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Cry No More — Linda Howard; tertile=begin; p=0.50**
>
> I’m betting he’ll arrive on the eighth. [TARGET] Table of Contents Title Page Dedication Chapter 1 Chapter 2 Chapter 3 Chapter 4 Chapter 5 Chapter 6 Chapter 7 Chapter 8 Chapter 9 Chapter 10 Chapter 11 Chapter 12 Chapter 13 Chapter 14 Chapter 15 Chapter 16 Chapter 17 Chapter 18 Chapter 19 Chapter 20 Chapter 21 Chapter 22 Chapter 23 Chapter 24 Chapter 25 Chapter 26 Chapter 27 Chapter 28 Chapter 29 Chapter 30 About the Author Other Books by Linda Howard Copyright 1 Mexico, 1993 Milla had fallen asleep while the baby was nursing. David Boone stood over his wife and child and watched them, aware of the silly grin on his face, of the fullness in his chest.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Six Degrees of Separation — Taylor V. Donovan; tertile=begin; p=0.63**
>
> Cover design & layout: L.C. Chase, lcchase.com ISBN: 978-1-7349221-1-0 Third edition April, 2020 Also available in paperback: ISBN: 978-1-7349221-3-4 All rights reserved. [TARGET] No part of this book may be reproduced, scanned, or distributed in any printed or electronic form without prior written permission from the author. Reviewers may quote brief passages in a review.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Grace Falls — H.P. Munro; tertile=begin; p=0.40**
>
> All rights reserved. [TARGET] No part of this book may be reproduced or transmitted in any form by any means electrical or mechanical, including photocopy, without permission in writing from the author. ASIN: B00I5UVVN2 All characters within this work are fictitious.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Unearthed — Kora Knight; tertile=begin; p=0.63**
>
> Without you as well, Max could never have turned out so gloriously badass. [TARGET] To all you fantastical book bloggers and reviewers: my labors of love would never even get off the ground if it wasn’t for all the massive time you so generously donate to authors like me. I freaking adore you to the moon and back.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Dark Legacy — Anna DeStefano; tertile=begin; p=0.48**
>
> Dark Legacy Anna Destefano Dorchester Publishing Trade (2011) Tags: Fiction, Romance, Fantasy, Paranormal Maddie Temple finds her life spiraling out of control as the mental link she shares with her twin sister pushes her closer and closer toward madness and her only hope for redemption lies with a psychiatrist who could end her career.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Sounds of Love — Susan Laine; tertile=begin; p=0.49**
>
> No part of this book may be reproduced or transmitted in any form or by any means, electronic or mechanical, including photocopying, recording, or by any information storage and retrieval system without the written permission of the Publisher, except where permitted by law. [TARGET] To request permission and all other inquiries, contact Dreamspinner Press, 382 NE 191st Street #88329, Miami, FL 33179-3899, USA http://www.dreamspinnerpress.com/ ISBN: 978-1-61372-396-8 Printed in the United States of America First Edition March 2012 eBook edition available eBook ISBN: 978-1-61372-397-5 Dedication I dedicate this book to the four generations of my maternal lineage I know by heart—my kind grandmother, my wise mother, my sassy sister, and my as-of-yet unborn niece. Thank you all for granting me the gifts of life and love, for the bonds of womanhood, and for the continued support you have shown me and my new career in writing.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Stubborn Heart — Ken  Murphy; tertile=end; p=0.55**
>
> Table of Contents Title page Copyright Prologue Chapter 1 Chapter 2 Chapter 3 Chapter 4 Chapter 5 Chapter 6 Chapter 7 Chapter 8 Chapter 9 Chapter 10 Chapter 11 Chapter 12 Chapter 13 Chapter 14 Chapter 15 Chapter 16 Chapter 17 Chapter 18 Chapter 19 Chapter 20 Chapter 21 Chapter 22 Chapter 23 Chapter 24 Chapter 25 Chapter 26 Chapter 27 Chapter 28 Epilogue About the Author Also from Dreamspinner Press

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Flawless Danger — Rachel Woods; tertile=end; p=0.52**
>
> This book or any portion thereof may not be reproduced or used in any manner whatsoever without the express written permission of the publisher except for the use of brief quotations in a book review. [TARGET] Printed in the United States of America Editing by Kelly Hartigan of XterraWeb http://editing.xterraweb.com Book cover designed by Deranged Doctor Design ISBN 978-1-943685-04-2 (Kindle)

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

- **Main:** blush, blushed, blushing, cheeks, prettily, embarrassed, crept, face, compliment, rising
- **KeyBERT:** embarrassment, embarrassed, embarrassing, melted, precious, licked, shock, crept, flush, prompted
- **POS:** remark, feminine, embarrassed, magical, embarrassing, realization, ankles, flush, embarrassment, precious
- **MMR:** crept, prompted, ducked, instinctively, feminine, ankles, embarrassment, flush, precious, popped

**BERTopic representative docs**

> 1. a blush crept to emma’s cheeks. “

> 2. a blush so faint she’d nearly missed it had crept over the carved slash of his cheeks.

> 3. so when you said i looked like bait ...' a blush crept up her cheeks and her hair fell forward with a tilt of her head to conceal the embarrassed infusion. '

**Stage-08 / Stage-07 snippets**

> 1. so when you said i looked like bait ...' a blush crept up her cheeks and her hair fell forward with a tilt of her head to conceal the embarrassed infusion. '

> 2. she’s probably laughing at me because i’ve blushed, but it doesn’t matter. “

> 3. i don’t think i’ve ever seen her blush. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Christmastime 1940 — Agnes Irene; tertile=end; p=0.59**
>
> Lillian waved goodbye to them as they climbed into the taxi. [TARGET] She laughed when Red planted a big exaggerated kiss on Izzy’s cheek as they drove off. Lillian watched the red tail lights disappear around the corner with the happy couple inside.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · A Clueless Woman — T.B. Markinson; tertile=middle; p=0.62**
>
> Through the peephole you looked funny. [TARGET] But now …” I motioned to her plunging red dress, stockings, and high heels. “ You look amazing.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Dangerous Passion — Lisa B. Kamps; tertile=begin; p=0.75**
>
> More blood rushed south, and he shifted just the smallest bit. [TARGET] She turned her head in his direction, briefly meeting his eyes before looking away, a hint of blush tingeing her cheeks. She looked up again and leaned slightly forward, her shirt opening even more as she tried to motion for the bartender.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Family Illusions — Bess George; tertile=end; p=0.84**
>
> You were pressed against me from shoulders to knees last night, but you can’t sit beside me? [TARGET] He blushed—a full, flaming blush, his cheeks and ears flooded with red. “ I can’t seem to think when you’re close to me.” “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Nick of Time — Scott D. Pomfret; tertile=middle; p=0.71**
>
> Nick of Time: A Romentics Novel 77 “Certain parts of you prouder than others.” [TARGET] Brent blushed at the thought of his morning wood. “ That’s good,” he said appreciatively. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Once Smitten, Twice Shy — Lori Wilde; tertile=begin; p=0.79**
>
> Her face was burning red again as she felt the telltale flush creep up her neck. [TARGET] No matter how hard she tried to suppress it, he seemed to have a magical ability to make her blush. “ I’ve got two good ears.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Mortal Peril — Clodia Metelli; tertile=end; p=0.66**
>
> If it pleases you, Master.” [TARGET] Gaius was glad to see that, demurely lowered eyes notwithstanding, Achilles was smiling and blushing. As he was helped down, Achilles’ movements were somewhat slow and awkward as he avoided bringing his tender, heated buttocks into contact with the edge of the table.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Welcome to Temptation — Charlotte Hughes; tertile=begin; p=0.80**
>
> The man was totally without scruples, she decided. [TARGET] She was thankful it was dark and he couldn’t see the bright blush on her cheeks. “ Would you like to wash up?”

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Ferus — T.M. Nielsen; tertile=end; p=0.70**
>
> Keiran and Lake materialized after we had exhausted ourselves in the water. [TARGET] The guilty blush that heated her cheeks and his smug smirk provided a detailed description of what they had been doing for the past few hours. “ Nice of you two to join us finally, but I’m hungry,” Dash announced. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Touching Eternity — Airicka Phoenix; tertile=begin; p=0.49**
>
> What?” [TARGET] she demanded defensively, dropping her gaze to the white sundress with large, purple lavenders splattered all over. He closed his eyes, shook his head. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Over the Tracks — Anna Green; tertile=middle; p=0.61**
>
> We’re in the middle of a conversation,” I tell her flatly, pointing between myself and Brendon. [TARGET] She blushes furiously and stutters on her words, making a quick exit. Brendon gives me a harsh look. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Rachel Laine — Jennifer Peel; tertile=end; p=0.81**
>
> That got her attention. [TARGET] Her beautiful brown eyes glimmered and she blushed. “ Not that that’s a reason to pick a school,” I added in. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Marriage at the Millionaire's Command — Anne Oliver; tertile=begin; p=0.69**
>
> He needn’t have worried. [TARGET] Averting her eyes, she swiped at her knees with tense, jerky movements, but he saw the telling blush that stained her cheeks. ‘ It’s my night off,’ she said, her voice husky. ‘

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · The Pharaoh's Concubine — Z.A. Maxfield; tertile=begin; p=0.58**
>
> Dylan didn’t look at him. [TARGET] William caught the blush staining his cheeks and found it funny under the circumstances. “ You’re shorter.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Torched — Chloe Stowe; tertile=begin; p=0.50**
>
> His hands flew to his fly, ripped his own jeans and briefs down and off his legs. [TARGET] As he kneeled there behind such a perfect set of cheeks and their gorgeously awaiting hole, Matthew couldn't resist. He reared back and slapped Cane's ass as hard as he could.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Leaning — J.W. Swartz; tertile=end; p=0.51**
>
> Jude almost managed a laugh. [TARGET] A startled Caribbean face came around the curtain. " Check your vitals?"

**Manual checklist** (fill in)

- Interpretable romance content: yes / no / mixed
- Noise / boilerplate / discourse residue: yes / no
- Suggested label (if unlabeled or wrong): ________
- Keep in landscape narrative: KEEP / DROP / FLAG
- Notes: ________

---
