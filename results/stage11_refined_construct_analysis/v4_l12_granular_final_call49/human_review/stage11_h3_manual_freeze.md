# H3 manual freeze — emotional vs material (42 topics)

Run: `v4_l12_granular_final_call49` — 42 topics.

No LLM adjudication on this pack. Fill KEEP/REMOVE after reading evidence.
Focus: does each topic belong on the emotional side, the material side, or appearance/status (kept separate)?

```
Decision rules (manual freeze — emotional vs material dichotomy)

1. Classify FUNCTION, not object. A house/gown/paycheck may be emotional
   belonging, material provision, appearance/status, or off-target.
2. Emotional (S1–S4): reassurance, belonging, trust, commitment-as-safety.
   KEEP on emotional side only if the topic primarily soothes / affirms /
   binds the relationship emotionally — not money or housing transfer.
3. Material (S8/S9): relationship-directed transfer of money/housing/
   necessities as security for a partner. REJECT merely being rich,
   luxury display, occupational status, workplace talk, or objects
   without a provision function.
4. Appearance / status (S12–S15): display, grooming, prestige, gifts-as-
   tokens, workplace rank — keep SEPARATE from material provision.
5. Contradiction trap: do not KEEP a topic on the material side if
   sentences show only appearance, status, or job-seeking without
   provision-to-partner.
6. KEEP = retain under final_code. REMOVE = drop from H3 atoms (S0).
```

### Codes in scope

| Code | Category | Definition |
| --- | --- | --- |
| `S0` | **off target** | Not doing security / provision / status-display work. Generic plot, logistics, or intimacy-only content without a security function. |
| `S1` | **emotional security reassurance** | Comforting, soothing, affirming safety/worth/the bond. |
| `S2` | **emotional security belonging** | Belonging, acceptance, "you're one of us", home-as-attachment. |
| `S3` | **emotional security trust** | Trust, reliability, keeping confidence, earned faith in the partner. |
| `S4` | **commitment security** | Commitment-as-security (promises of permanence, fidelity as safety). |
| `S8` | **material provision money** | Money, gifts-as-provision, paying bills, financial support. |
| `S9` | **material provision housing** | Housing, shelter, providing a place to stay. |
| `S10` | **economic dependency** | Dependency / control via money or resources (not mutual provision). |
| `S12` | **status display** | Status / wealth / prestige signalling as display (not provision-to-partner). |
| `S13` | **appearance grooming** | Appearance, grooming, dress as presentation (function = display/craft). |
| `S14` | **gift romance token** | Romantic gift / token (function = affection signal, not material security). |
| `S15` | **workplace status** | Workplace rank, career prestige, professional standing. |
| `S16` | **mixed or unclear function** | Multiple security functions compete with no clear dominant. |

## 1. Emotional security (S1–S4)

_28 topics_

### Topic 29 — Confessing Long-Held Love

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** love, loved, you, loves, too, falling, fall, always, me, know
- **KeyBERT:** happiness, genuinely, hated, forgive, dreamed, uttered, instantly, deserve, crushed, secretly
- **POS:** spite, slightest, reflection, issue, delicate, actions
- **MMR:** responding, uttered, spite, blinking, slightest, crushed, reflection, fired, apologize, delicate

**BERTopic representative docs**

> 1. he loves you even more than i do.”

> 2. you said if i tried--" "he loves me." "

> 3. i don’t think anyone will ever love me like mr. fielding loves ms. greenberg,” she said. “

**Stage-08 labeling snippets**

> 1. i love you with everything i am, everything i’ve been, and everything i hope to be .” “

> 2. tell her i’ve always loved her.

> 3. i’ve always been in love with you.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Packet representative sentences** (fallback when CELL sample empty)

> 1. I love you, too, sweetheart.”

> 2. I love you both.”

> 3. I love you.”

> 4. Oh, child, I love you, too.”

> 5. You just say ‘I love you.’”

> 6. I love you, Mom.”

> 7. I love you, too.”

> 8. I love you.” “

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 38 — Admitting Shared Pain

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** feel, feels, good, felt, feeling, better, make, how, so, like
- **KeyBERT:** hurts, experienced, worst, recently, um, honestly, accustomed, incredibly, magical
- **POS:** accustomed, magical, insides, problems, opportunity, worst, loose
- **MMR:** hurts, ticked, accustomed, magical, insides, apologize, recently, admitted, experienced, loose

**BERTopic representative docs**

> 1. that feels like a hard-on.” “

> 2. or it feels like it.

> 3. do you know what that feels like?

**Stage-08 labeling snippets**

> 1. i’ve seen your pain.

> 2. i've never felt that way before."

> 3. will it make you feel better to know that i’ve got one, too?”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Suzanne's Diary for Nicholas — James Patterson; tertile=middle; p=0.66**
>
> I was incredibly lucky, and it gave me a chill as I stood there with Matt on our wedding night. [TARGET] That’s what it felt like—that was the exact feeling—and I’m so happy that now you were there. Nicholas, Matt and I went on a whirlwind, three-week honeymoon that started on New Year’s Day.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Wolf Tales VIII — Kate Douglas; tertile=end; p=0.71**
>
> It’s very strange, like another entity inside me. [TARGET] I hadn’t noticed that feeling before.” “ Good.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Hit the Spot — J.  Daniels; tertile=middle; p=0.73**
>
> Same as gettin’ mad at me for shit we both let happen. [TARGET] I’ll feel that, babe, but you’re feelin’ it, too.” “ Jamie—” I slammed my mouth down on hers and kissed her then, hard and hurried, shoving my tongue inside and expecting protests, her hands pushing away or her head turning, body twisting out of my arms, but getting none of that.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Third Chances — Ivy Smoak; tertile=middle; p=0.72**
>
> She seemed to be torn. [TARGET] It was the same thing I was feeling. I wanted her.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Ugly Beautiful — Sean-Paul Thomas; tertile=middle; p=0.73**
>
> I don't know. [TARGET] But it doesn't feel great this feeling I'm getting, you know. It doesn't feel good at all Jason.'

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Her Twin Brother — Yamila Abraham; tertile=middle; p=0.74**
>
> If you feel beautiful, then I’m happy. [TARGET] That’s how I wanted you to feel.” I sat at the side of the table and he sat at the end beside me.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Neighbors — Ashleigh Royce; tertile=begin; p=0.70**
>
> He’s embarrassed. [TARGET] But I’d felt the same way. “ I know I only met you two days ago, but I want to be with you.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · A Nightmare Come True — Sage Marlowe; tertile=middle; p=0.63**
>
> A peculiar calm settled over me and chased away the chill that had held me in its grip. [TARGET] The sensation was unlike what I’d felt seconds before and even as I surrendered to the feeling that spread inside me now, I wondered how such a swift and complete change of emotions was possible. Investigating the source of the sentiment, I realised that it seemed to come from Colin or, rather, it radiated off the hand he still rested on mine, that cold iron clasp of his fingers. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · One Bite To Passion — MaryLynn Bast; tertile=end; p=0.59**
>
> It had been so long since she had had a donut, it tasted like heaven. " [TARGET] Okay, so you know, I'm not afraid to tell you how I feel." He leaned back and pulled her to him in a light hug. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Family Love — Liz Crowe; tertile=middle; p=0.51**
>
> What had occurred Friday night and well into Saturday with Joffe was what she imagined occurred to Susie all the time, and Susie undoubtedly handled it with a lot more savoir faire. “ [TARGET] The thing is, I don’t know how I feel about the whole thing. I guess that’s where I need advice.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Grandma Must Die — Maureen L. Bonatch; tertile=begin; p=0.52**
>
> Carman closed her eyes, absorbing the power from the book. [TARGET] The delicious feeling evoked a sensation like melting chocolate, sweet and satisfying. “ I remember hearing about her, Esmeralda Wrath.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · The Shark — Mary Burton; tertile=end; p=0.67**
>
> What’re you doing here?” “ [TARGET] Thought I’d come by and see how you’re feeling.” “ I’ll live.” “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · The Sabbides secret baby — Jacqueline Baird; tertile=end; p=0.59**
>
> I know you care for him, so instead of damning him you should tell him you love him. [TARGET] Trust me—it will make you feel a whole lot better.’ ‘ Ah, Phoebe!’

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Galaxy's Heart — Shawn Lane; tertile=begin; p=0.50**
>
> Honestly, I've never taken anyone's virginity so I need to wrap my mind around this. [TARGET] Up to this point all I could think of was fucking you senseless." " You-you can still do that." "

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Kicking The Habit — Kari Lee Townsend; tertile=begin; p=0.57**
>
> Let’s just say I’ve always been different from the other nuns. [TARGET] I felt like something was missing, like maybe I wasn’t doing something right. I just thought I could help more people from outside the church, that’s all.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Below the Belt — Jeanette Murray; tertile=middle; p=0.46**
>
> And I’d also like to have about ten minutes this evening before practice begins so I can give the guys the warning signs of heatstroke. [TARGET] Just things to look out for so they can come tell me if they’re feeling any of it.” “ That I can do.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 45 — Reassured Everything Will Be Fine

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** fine, okay, everything, right, be, all, honey, ok, will, alright
- **KeyBERT:** ok, assured, assure, smoothly, uh, incredibly
- **POS:** problems, sir, lord
- **MMR:** smoothly, assure, acknowledged, injured, ms, appreciate, assured, problems, repeated, urge

**BERTopic representative docs**

> 1. i’m fine right where i am.”

> 2. actually, i'm not—' 'it's ok, honey.

> 3. oh… umm… okay, fine.

**Stage-08 labeling snippets**

> 1. we’ll be ok.” “

> 2. nadines : you’ll be ok?

> 3. ok, maybe a zero-tolerance one, but there’s no doubt about it, you’ll be great.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 12 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_003 · The Pagan Stone — Nora Roberts; tertile=middle; p=0.76**
>
> The last thing she said to me was, ‘Don’t worry, baby, don’t be scared. [TARGET] It’s going to be all right.’ It wasn’t, but I hope she believed it.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · One Night with a Santini — Melissa Schroeder; tertile=begin; p=0.64**
>
> Please call when you get in. [TARGET] I need to know you made it okay.” She smiled and nodded. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Loving the Country Boy — Mia Ross; tertile=begin; p=0.80**
>
> We’re not. [TARGET] Everything’s going fine.” Technically, she was telling the truth.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Jingle all the Mitchell way — Jennifer Foor; tertile=begin; p=0.69**
>
> Either way, I accepted his support. “ [TARGET] It’s all going to be fine, bro,” he tried to reassure me. “ Don’t listen to those assholes.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Good Luck, Fatty?! — Maggie Bloom; tertile=begin; p=0.75**
>
> Maybe,” I say, picturing racks of baby clothes that have been rescued from a flood and, consequently, look like they’ve already been spit up on. “ [TARGET] Are you sure you’re okay?” Denise asks again, studying me as I wobble to the cast iron sink and lean against the faux marble counter.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Me & My Invisible Guy — Sarah Jeffrey; tertile=middle; p=0.76**
>
> I slowed my walk. [TARGET] Everything is going to be fine. No one knows for sure.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Outback Thunder — Ann B. Harrison; tertile=middle; p=0.77**
>
> Just keep calm Zoe. [TARGET] You're going to be okay." *** The blood running down her face scared him more than he would have imagined and he knew he was being snappy with the sheer fright of seeing her like this. "

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Outback Thunder — Ann B. Harrison; tertile=end; p=0.78**
>
> I will have to sit forward to give you room to put that sling on." " [TARGET] Are you going to be okay?" " No, it hurts enough now but at least when you put the sling on at it will be more secure than me holding it.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · By Break of Day — M.L. Buchman; tertile=middle; p=0.66**
>
> He tried to say her name, but it wouldn’t come out. “ [TARGET] It will be okay,” he finally managed. “ I just need some time.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · By Break of Day — M.L. Buchman; tertile=end; p=0.64**
>
> What in the wide world are you doing here?” “ [TARGET] I wanted to make sure you were okay.” “ Okay?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Stepbrother With Benefits 7 — Mia Clark; tertile=middle; p=0.49**
>
> If that's true, why is my mom staring at us with a look of abject horror, then? [TARGET] Um... I don't think this is fine. Ethan's dad glances between the two of us, one eyebrow raised. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Ivar the Red — Victoria Vane; tertile=middle; p=0.61**
>
> She was so exhausted in both mind and body that her legs almost gave way as her feet hit the ground. “ [TARGET] Are you all right, my lady?” Budic rushed to her side. “’

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Mona Lisa Awakening — Sunny; tertile=middle; p=0.65**
>
> I tapped his arm and gestured to his bare chest. " [TARGET] I'm fine," Amber replied quietly. " Doesn't hurt?"

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · A King Undone — Cooper Davis; tertile=begin; p=0.60**
>
> I was secure until I reached your premises,” Arend replied. “ [TARGET] And, unbelievably enough, am in fine health even now, despite my near-endless wait outside your gates.” “ My king, I am—” Arend lifted a kidskin-gloved hand, silencing the fellow without another glance, for he already knew that actually staring into the other man’s moody, sensual eyes produced a downright leveling effect on Arend’s own composure.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · A King Undone — Cooper Davis; tertile=end; p=0.59**
>
> He glanced away, shuttering himself. “ [TARGET] Yes, well, just don’t expect that I shall call you ‘my darling’ and I’m sure we will be fine henceforth.” Jules bowed and low. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · A King Undone — Cooper Davis; tertile=begin; p=0.61**
>
> Here, Julian. [TARGET] I am so very, very sorry, but all shall be well. I will see that it is so, by my own hands, my own care.”

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 46 — Asking Someone to Trust You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S3 — emotional security trust**

**Four keyword representations** (BERTopic / labeling)

- **Main:** trust, trusted, betrayed, betray, trusting, me, betrayal, you, can, don
- **KeyBERT:** instincts, willingly, worries, sentence, expect, admit, insisted, deserve, warned, appreciate
- **POS:** instincts, possibilities, worries, percent, creatures, concrete, treatment, result, twisting, options
- **MMR:** instincts, worries, percent, described, concrete, twisting, options, hesitation, sleeve, heal

**BERTopic representative docs**

> 1. i do trust you.

> 2. otherwise wouldn’t your trust be misplaced?”

> 3. do you trust me, jackson?” “

**Stage-08 labeling snippets**

> 1. you’ll just have to trust me.”

> 2. he’ll trust you if you promise to keep me in sight.” “

> 3. my trust that he’ll bring me to safety.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Amberly — Mary E.  Hall; tertile=begin; p=0.45**
>
> http://www.munseys.com MY name is Mrs. Elizabeth Jennings. [TARGET] I am a highly respectable woman. I may style myself a gentlewoman, for in my youth I enjoyed advantages.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Saved by a Dangerous Man — Cleo Peitsche; tertile=middle; p=0.68**
>
> He’d respected my wishes when I decided to go rather than act like a meathead on steroids, getting all crazy territorial and telling me what I could and couldn’t do. [TARGET] Which helped me trust him… and trust our relationship. That I’d ignored his request and he’d been there to help me when things got bad only made him that much more awesome.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Sarai's Fortune — Abigail Owen; tertile=middle; p=0.75**
>
> Then he leaned in closer and took her face between both his hands. “ [TARGET] You’re going to learn to trust me someday, sweetheart.” Then he shocked the hell out of her when he lay his lips over hers in a kiss so achingly gentle she felt tears mist her eyes.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Untainted — Shanora Williams; tertile=begin; p=0.75**
>
> His features softened a touch, and his lips parted. “ [TARGET] Look, I know it’s been a while, but can you trust me?” He grabbed my hand and hauled me closer.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Sapphire Universe — Devon Herrera; tertile=end; p=0.79**
>
> I don’t have time to argue with you. [TARGET] You’re just going to have trust me!” I hang up the phone, knowing that my best friend will come through for me.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · The Dogcatcher — Bruce Luchsinger; tertile=middle; p=0.81**
>
> I can tell. [TARGET] And I can tell you don’t trust him.” I started to protest and Charlie pressed on. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Love Taps — Shannon West; tertile=middle; p=0.68**
>
> No, Paul. [TARGET] You have to trust me to do what’s best for you, and if you can’t, then I can’t play with you any longer. You’ll have to find another Dom better suited to you, but you need to be careful to find one who has limits of his own, or else you’ll wind up seriously injured.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · From Lambton to Longbourn — Abigail Reynolds; tertile=end; p=0.58**
>
> Elizabeth, I believe you know full well that nothing would make me happier than to marry you as soon as possible”— preferably before this uncertainty drives me out of my mind , he added to himself—“but will you allow me to ask why you suggest the change? [TARGET] Is it for my sake, or your own, or perhaps because you cannot trust our ability not to stray?” She colored becomingly. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Family Ties — Krista Kedrick; tertile=begin; p=0.62**
>
> Jimmy had dropped off a fresh delivery this morning as scheduled. [TARGET] At least he was trustworthy. Of course he’d probably try to screw her over on the bill now that he knew she was in charge instead of her mother, who opted to pay him with a different kind of screwing.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Forever You — Sandi Lynn; tertile=middle; p=0.55**
>
> Everyone’s been hurt at least once in their life, some more than others, but you have to make a choice what to do with that pain,” she said. “ [TARGET] It’s not that simple, Ellery; trust me,” I said as I continuously stared at the road ahead of me. “ So, you don’t ever want to get married or have children and do the whole perfect family thing?”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Finding Harmony — JoMarie DeGioia; tertile=end; p=0.77**
>
> I’ve changed. [TARGET] I’m ready to trust again. In you.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · First Bite is the Deepst — Nora Snowdon; tertile=begin; p=0.42**
>
> Cold wings and warm beer. [TARGET] He should stop trusting the stupid food critic who’d recommended the bloody pub. Best hot wings, my ass .

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Life Changes Everything — T.C. Blue; tertile=begin; p=0.27**
>
> The intended implication was that I had put numbers and statistical analysis ahead of God. [TARGET] The critics wanted to prove that setting goals, drawing graphs, measuring results and evaluating the performance of individuals was nothing less than taking the place of trusting the Holy Spirit to give increase. I could only reply that I guess I was, in fact, playing the numbers game—if the numbers represent lost people being saved and coming into the kingdom of God.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · FUBAR — Stephani Hecht; tertile=begin; p=0.61**
>
> My place is close enough.” “ [TARGET] Trust us, all we need to do to you can be done here,” one of the other guys said. The other gave a nasty laugh. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Olivia — Donna Sturgeon; tertile=middle; p=0.65**
>
> Her heart broke for him, and she squeezed him in comfort. “ [TARGET] Wasn’t there anyone you trusted to share your joy with?” “ Yeah, there was someone… Two someones actually.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_011 · Covert Interview — Missy Marciassa; tertile=begin; p=0.50**
>
> Oooh, Navy guys!” [TARGET] Trust Marni to focus on the important stuff. “ Seen any hot sailors yet?”

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S3`)
- Decision: KEEP / REMOVE

---

### Topic 56 — Promising Never to Hurt You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** hurt, hurting, harm, mean, never, won, you, want, don, hurts
- **KeyBERT:** hurts, painful, distress, tightly, threatened, protect, cried, assured, insisted, causing
- **POS:** hurts, distress, painful, possibility, purpose, ye, process
- **MMR:** hurts, distress, tries, intend, deserve, threatened, causing, insisted, tightly, protect

**BERTopic representative docs**

> 1. i know, but you seem sweet and i don’t like the thought of anyone hurting you.” “

> 2. hurting that town would mean hurting you, which would mean i'd hurt katherine and my son.

> 3. by hurting others, you hurt yourself.

**Stage-08 labeling snippets**

> 1. you'll get hurt," he managed to say. "

> 2. you know i’ll never hurt you .”

> 3. i’ll make sure you aren’t hurt.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

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

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Summer On Blossom Street — Debbie Macomber; tertile=end; p=0.79**
>
> This new man you’re seeing. [TARGET] You’re only doing it to hurt me, aren’t you?” “ Who I’m seeing is none of your business.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Love Unfeigned — Nadine C. Keels; tertile=end; p=0.70**
>
> First of all, for the record, let me tell you that I wasn’t keeping quiet this time because I didn’t think you deserved to be told or that I didn’t need your forgiveness. [TARGET] I haven’t meant to hurt you, I just wanted to be careful not to…not to trigger anything that I shouldn’t, at the wrong time.” Lorraine’s flinch was so near imperceptible that Isaiah wasn’t sure if she’d actually shaken or not, but he forged on. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Amber Light — Virginia McCullough; tertile=end; p=0.50**
>
> Olivia put more distance between them. “ [TARGET] Do you really think I’d do anything to hurt Carson? You told Matt you weren’t sure how I feel about this.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Bittersweet — Sarina Bowen; tertile=end; p=0.63**
>
> Twice, I think.” [TARGET] It had honestly never occurred to me that I would have had the power to hurt him. “ Let’s see.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Bookends — Jane Green; tertile=middle; p=0.51**
>
> You can’t grow as a person,’ she said sadly, ignoring my joke, ‘when you close yourself off emotionally. [TARGET] It’s all well and good saying you avoid pain by avoiding relationships, but what about the wonderful things you’re avoiding as well? What about the joy and the intimacy and the trust that come with finding someone you love?’ ‘

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · H.R.H. — Danielle Steel; tertile=middle; p=0.48**
>
> She sounded bitter as she said it, but even more than that, wounded and sad. “ [TARGET] Don’t give him the satisfaction of letting it destroy you. He doesn’t deserve that, and neither does your socalled best friend who ran off with him.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Car Wash — Shawn Lane; tertile=middle; p=0.53**
>
> Are you sure? [TARGET] You’re not too sensitive for this?” Kevin gave him what he hoped was an exasperated look. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Stars Collide — Janice  Thompson; tertile=middle; p=0.42**
>
> Surely not. [TARGET] Lenora Worth was not the type to hurt people. That much I knew to be true.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 96 — Confessing Long-Standing Worry

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** worry, worried, about, bother, concern, worrying, concerned, don, does, nothing
- **KeyBERT:** concerned, worrying, worries, fears, bothering, bothered, problems, assure
- **POS:** annoying, slightest, fears, concerned, amusement, possibility, purpose, problems, reaction, worried
- **MMR:** worrying, worries, bothered, assure, crashing, fears, concerned, amusement, sounding, repeated

**BERTopic representative docs**

> 1. don’t worry about us.

> 2. no need worrying when we don’t know if there’s anything to worry about.

> 3. don't be so worried."

**Stage-08 labeling snippets**

> 1. i’ve been worried about you, [person].

> 2. i’ve worried about you since i was twelve.

> 3. i’ve been worried about you.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Amber Light — Virginia McCullough; tertile=end; p=0.60**
>
> But they were babies when their parents got them.” “ [TARGET] This is an entirely different situation, which is why I don’t want you to worry about what you call me.” “ Uh, did you tell Heather or Olivia or anybody else about adopting me?” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Still Life — A.M. Johnson; tertile=end; p=0.72**
>
> I need to be there for you, don’t push me away,” her voice pleaded. “ [TARGET] Don’t you think I’m just as worried about you as you are of me? I can’t lose you either.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Jax — Lane Hart; tertile=end; p=0.81**
>
> I'm going to be fine. [TARGET] The only thing I'm worried about is you." " Let's go," the officer says more forcefully.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Novelista Girl — Meredith Schorr; tertile=begin; p=0.63**
>
> And it doesn’t excuse her treatment of me.” “ [TARGET] I don’t know what her deal is, but she’s not my concern—you are.” He patted my back in a circular motion. “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Ten Things We Did — Sarah Mlynowski; tertile=begin; p=0.74**
>
> Another look with Penny. “ [TARGET] We didn’t want to worry you.” Yeah, why would I want some time to get used to the idea?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · The Ex-Factor — Laura Greaves; tertile=end; p=0.60**
>
> A flicker of uncertainty clouds Vida’s expression. [TARGET] I can tell she’s worried that I’m losing it. ‘ So Debi thought that Mitchell should find another girlfriend, one who was’ – she looks me up and down –’ ordinary, and make her the most talked-about woman in the world.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_014 · Don't Kiss the Vicar — Charlie Cochrane; tertile=middle; p=0.64**
>
> I think we all worry about her,” Dan said, noncommittally. “ [TARGET] I worry about all of you,” he added, with a smile. “ Don’t you go wasting any time fretting about me.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · The Country Omega — Penelope Peters; tertile=end; p=0.66**
>
> Ethan touched Antonio’s arm, and even through the odd possessive fog, Antonio could see the realization dawn on his face. “ [TARGET] This isn’t just you worrying about me coming home from the station, is it?” “ It’s not safe,” said Antonio through gritted teeth. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Duke of Midnight — Elizabeth Hoyt; tertile=begin; p=0.60**
>
> There wasn’t much left: the mantel and her bedside table, both without anything to hide something in. “ [TARGET] Why are you so concerned with my actions in any case?” Even in his whispered voice he sounded irritable, and she supposed he had a right. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Nate — Delores Fossen; tertile=end; p=0.61**
>
> Good. [TARGET] One less thing to worry about right now. Later, he would deal with his hatred for this SOB who’d nearly cost Nate everything.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Barefoot with a Bad Boy — Roxanne St. Claire; tertile=begin; p=0.59**
>
> She inhaled as if gathering her thoughts, then lifted his drink to her lips, staring at him over the rim. “ [TARGET] If it makes you feel any better, I’m more nervous about this than you are.” She punctuated that with a healthy gulp, and no girlie cringe as it went down.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Barefoot with a Bad Boy — Roxanne St. Claire; tertile=middle; p=0.59**
>
> You already mentioned it to him last night,” he said. “ [TARGET] He’s got enough on his mind and can’t worry about me, too.” Nino lifted his brows. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Bound by Honor — Donna Clayton; tertile=middle; p=0.50**
>
> I think that's a normal reaction, Jenna. [TARGET] You grew up worrying about having your basic needs met. It's quite natural to want to see to it that you have enough income to survive."

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Edge Play X — M. Jarrett Wilson; tertile=middle; p=0.70**
>
> His desire was rupturing out of him. “ [TARGET] You don’t know how worried I was about you,” he confessed, exaggerating his concern. “ I didn’t know where you were.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Edge Play X — M. Jarrett Wilson; tertile=begin; p=0.66**
>
> Promise me that you’ll stay away from the drugs.” “ [TARGET] You don’t have to worry about that,” he answered. “ That part of my life is over.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Lily — Xavier Axelson; tertile=begin; p=0.60**
>
> I mean, she'd really like it. [TARGET] I've been a little off lately, and she's worrying." His voice dropped off.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 128 — Confessing How Much You've Missed

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Current code (LLM):** **S4 — commitment security**

**Four keyword representations** (BERTopic / labeling)

- **Main:** miss, missed, missing, much, ve, you, too, misses, wouldn, ll
- **KeyBERT:** hi, sir, escaped, honestly, repeated, solemnly
- **POS:** handful, precious, voices, elevator, opportunity, pieces
- **MMR:** solemnly, breathlessly, thoughtfully, handful, voices, sounding, elevator, repeated, considering, pressing

**BERTopic representative docs**

> 1. i’ve missed being adored. ‘

> 2. i've missed you all so much.” “

> 3. i’ve missed you around here.”

**Stage-08 labeling snippets**

> 1. i’ve missed most of his life already.

> 2. and, god, how i’ve missed this.”

> 3. i’ve come to realize that you are the one thing in my life i don’t want to miss.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_thin cells CELL_D; 16 examples from 11 books; ±1 context on 16_

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

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Fatty Patty — Kathleen Irene Paterka; tertile=middle; p=0.75**
>
> We’ve talked every day since he’s been gone, more than we ever do when he’s home. [TARGET] I didn’t count on missing him so much. “ Where are you?

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · The End of Our Story — Meg Haston; tertile=middle; p=0.68**
>
> I want to stroke his hair, its sunset colors, the way I did when we were kids and he couldn’t sleep. [TARGET] I miss him being this close. “ Quit being psycho,” he tells the television. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Deadly Desire — Keri Arthur; tertile=begin; p=0.61**
>
> He paused. " [TARGET] I sometimes miss the peace of you and me, though." " Because it's only been a few weeks.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Deadly Desire — Keri Arthur; tertile=end; p=0.44**
>
> I waited until the last possible moment, then shifted my arms so that my top rode up my breasts, and leaned over the table, giving him an eyeful. [TARGET] He missed the ball even worse than I did. He swore under his breath, then said, "So you think this hidden doorway could lead to one or both of our sorceresses?" "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Deadly Desire — Keri Arthur; tertile=end; p=0.45**
>
> I went for the shot, but a second before the cue tip hit the ball, his hand snaked down my back and butt, a caress so light and yet so heated that it practically singed. [TARGET] Needless to say, I missed the ball. He moved around to the other side of the table and began to line up the same ball I had. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Red & Her Big Bad Dom — Sydney St. Claire; tertile=end; p=0.59**
>
> Staring at herself in the mirror, she frowned. [TARGET] Something was missing. Shoes!

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Tales of the Djinn: The Guardian — Emma Holly; tertile=end; p=0.52**
>
> Do not faint,” he warned. “ [TARGET] If you do, you’ll miss your orgasm.” The implication that he would still take his both outraged and titillated her. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Tales of the Djinn: The Guardian — Emma Holly; tertile=end; p=0.54**
>
> She nudged his foot playfully with her toe, which made both of them grin like kids. “ [TARGET] Do you miss your own stars?” he asked. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Tales of the Djinn: The Guardian — Emma Holly; tertile=middle; p=0.60**
>
> His second hand joined his first on the grip, and he pulled the trigger. [TARGET] He didn’t miss. Arcadius grunted as a bullet hit him high in the chest, beneath his left shoulder.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Monster Prick — Kendall Ryan; tertile=end; p=0.59**
>
> Poof. [TARGET] Vanished. “ What are you doing here?”

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S4`)
- Decision: KEEP / REMOVE

---

### Topic 137 — Pitching A Career Change

- **Taxonomy:** 6.2 — Work & Professional Identity
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** nick, nathan, shook, head, nik
- **KeyBERT:** stalked, giggled, gotta, snorted, mumbled, willing, digging, urged, blurted, approached
- **POS:** unhappy, remark, possibilities, annoyance, enthusiasm, notion, fears, recent, warmth
- **MMR:** snorted, playfully, sweep, annoyance, enthusiasm, stalked, shout, fears, recent, sharply

**BERTopic representative docs**

> 1. adam glanced sideways at matt who gave a barely imperceptible shake of his head that said, don’t get involved.

> 2. i nod, glancing up to find danny already glaring at me from the far side of the lawn, where the three cooney boys are kicking a soccer ball while emmie scoots through the middle of their game on a plastic train. “

> 3. leaning forward i glance around nod and give ryan the evil eye, which he just shakes his head at. “

**Stage-08 labeling snippets**

> 1. [person], i’ve been giving this a lot of thought, and i think it’s time i moved onto hard news.

> 2. ryan smiled in a way that told her he wasn't that dense, and said, "i'll keep digging here, but maybe not with as much enthusiasm, but if marc gets to be a bore, let me know." "

> 3. i'll come too—" [person] makes to get up from the bed. "

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Lover's Leap — Emily March; tertile=begin; p=0.55**
>
> Michael got gingerly to his feet. [TARGET] He half thought of just flipping them the finger and carrying on down the hall to Rufus’s room, but somehow he wasn’t feeling in the mood anymore. Rufus would probably just tell him to piss off anyhow.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Locked — Ella Frank; tertile=middle; p=0.65**
>
> I guess that’s about right. [TARGET] I was ready to give the new guy a piece of my mind once I found out we were working together but then I realized…” When Ace trailed off, Derek looked to me then back to Ace. “ You realized…?” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Finding Chris Evans: The 9-1-1 Edition — Erin Nicholas; tertile=begin; p=0.64**
>
> And maybe you could go to my mom’s party with me.” [TARGET] Chris seemed surprised for a second. “ Well, yeah.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · The Naughty Step — Nikky Kaye; tertile=middle; p=0.62**
>
> She let go of my arm in order to get the door. [TARGET] Nathan still wore a frown, which only eased a little bit when I put my arms around his neck. “ I promise, I’ll be fine.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Stripped — Marcia Colette; tertile=begin; p=0.65**
>
> I’ll buy you one, Chris,” her customer said to the man next to him as he handed Abby another bill. [TARGET] Abby moved toward him in anticipation, but he shook his head and smiled. “ That’s okay,” he said.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Porpoiseful Intent — Tymber Dalton; tertile=middle; p=0.58**
>
> Not to mention he was exhausted and worried about Emery and the rest of the shifters. [TARGET] A nasty, niggling feeling in his gut told him maybe Erik was behind the missing shifters. When the call came in, Sean conferred with Emery and his dad on where to send the three shifters.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Undercover — Olivia Ruin; tertile=begin; p=0.50**
>
> My plan went for naught when Frank caught me out of the corner of his eye and cut off his sentence mid-word. [TARGET] I had just gotten close enough to start to be able to make out individual words, but all I heard was “... those stupid bean...” Jed looked over when Frank stopped talking, and sprang out of his seat to come and take the beers from my hands. “ Thanks, Leslie, but don’t come over here again, got it?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Wrong Side of the Law — Edward Kendrick; tertile=begin; p=0.53**
>
> But you are far from over it.” [TARGET] The corners of Dirk’s mouth turned up in a partial sneer when he replied, “I have a feeling my lieutenant wouldn’t be in the least surprised, considering he believed that bastard’s accusations. So score one for him.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Required Surrender — Riley  Murphy; tertile=begin; p=0.51**
>
> Yeah.” [TARGET] Ted eyed him, gauging how much he should say, if anything at all. “ What’s with the look?” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Waiting For Wren — Cate Beauman; tertile=end; p=0.60**
>
> Hmm.” [TARGET] What the hell else was he supposed to say as he looked from Wren’s pleading, terrified eyes into JT’s calculated stare? “ Owens put two and two together and they rushed to JT’s apartment.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · The Highest Bid — Joey W. Hill; tertile=end; p=0.50**
>
> There’s someone worth your attention at your two o’clock.” [TARGET] When Tyler Winterman, part-owner of The Zone, put his hand on Peter’s shoulder, bent, and murmured that statement into his ear, Peter blinked. There’d been plenty of available women hovering since they arrived, and of course Ben had hinted they had someone special lined up for him.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Where She Is — Loriana Cappello; tertile=end; p=0.52**
>
> You do know he exaggerates that accent? [TARGET] If you heard Simon and Esther talk, you’d know what I mean.” Her lips purse and her eyes narrow, so I clarify. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · The Care and Feeding of Unmarried Men — Christie Ridgway; tertile=end; p=0.46**
>
> Now you and I have a few things to discuss,” she said to him. [TARGET] Nash ghosted a grin at the lethal sound of the words and wondered if he’d left the other man with the most dangerous of them all. But the smile died as he settled Eve into the passenger seat of her car.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · The Care and Feeding of Unmarried Men — Christie Ridgway; tertile=middle; p=0.52**
>
> What did you say?” [TARGET] He was annoyed at having to repeat himself—that was obvious. “ Did you think about what I said at Doug’s party?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · The Breakup — Brenda Grate; tertile=begin; p=0.51**
>
> I got here in record time, man.” [TARGET] Then not giving Stephen time to counter his comment, he said, “Now, why don’t you start by telling me exactly what happened.” Stephen settled back with a low moan, making full use of his pain now that he had an audience. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · The Breakup — Brenda Grate; tertile=begin; p=0.62**
>
> The man’s eyes widened. [TARGET] He looked at Stephen’s lap and shuddered. “ Are you okay?

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 141 — Warned to Use His Title

- **Taxonomy:** 6.3 — Shared Workplaces & Professional Interaction
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** bo, lewis, si, vasco, derek, tickles, stage, maxum, maxim
- **KeyBERT:** gotta, responded, smirk, hi, hesitation, sir, prodded, chuckle, asks, warmth
- **POS:** visits, unlikely, president, tracks, urgency, unhappy, spite, hesitation, process, members
- **MMR:** bo, prodded, visits, president, worries, hovering, hopped, twitched, wiping, hesitation

**BERTopic representative docs**

> 1. bo looked up at him and realised that wasn’t the reason for max’s shakes after all.

> 2. and just like that, bo felt lower than dirt for sharing something that would absolutely mortify max. “

> 3. breathing in the sharp smell of sweat from the mosh pit of chefs, judges, and audience members on the stage, max deliberately blanked his mind and his face, and hopped down off the stage to head for his next good-bye.

**Stage-08 labeling snippets**

> 1. i’ll have it my own way,” branch said to [person]’s back. “

> 2. [person] can handle himself but he looks like a tiny wee thing in comparison to us so they’ll see him as easy pickings.”

> 3. you'll call me director and you'll like it," lincoln warned [person], a wide grin covering his face.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_D; thin cells CELL_C; 10 examples from 8 books; ±1 context on 10_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Full Package — Lauren Blakely; tertile=end; p=0.74**
>
> That riles up Spencer, who grabs a paddle from Nick. [TARGET] As they play, Max wanders back in, his jaw set, his eyes blazing. “ Everything good?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Full Package — Lauren Blakely; tertile=end; p=0.74**
>
> Keeping busy watching monster truck rallies and avoiding all food that requires utensils?” [TARGET] I look around for Max, but he’s disappeared. “ Yeah, it’s one big fiesta of masculine stereotypes.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Full Package — Lauren Blakely; tertile=end; p=0.73**
>
> She said we need to stop.” [TARGET] Max holds up his hands in a T . “ Whoa.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · With This Ring — Debra Clopton; tertile=begin; p=0.78**
>
> Levi shook his head and met his brother’s laughing eyes. [TARGET] Max cocked his head to one side. “ Betty Lou, I tend to be with you on this one.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · The Importance of Being Married — Gemma Townley; tertile=middle; p=0.81**
>
> Why?” [TARGET] Max looked thoroughly confused. “ You have a nice…self.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Blood From a Stone — Cynthia Lucas; tertile=middle; p=0.52**
>
> Yo u ’ l l fi nd out soon enou g h.” T he w o r ds w e r e not sa i d a l oud but i n st ead see m ed t o m a t e ri a li z e i ns i de S a m son ’ s head. [TARGET] Max i m us l oo k ed at t he coun t er t o m a k e su r e no one e l se w as t he r e be f o r e he be g an t o de m a t e ri a li z e. H e r a i sed t he paper back up t o co v er h i s f ea t u r es. “ Y ou ’l l k now w hen t he ti m e co m es.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Click Date Repeat — K.J. Farnham; tertile=end; p=0.62**
>
> Some of them bombarded me with questions about my ex on the first date and some made reference to meeting Max right away. [TARGET] On the flipside, there’ve been quite a few who didn’t seem interested in knowing anything about Max. You make it so easy for me to share organically, and I really appreciate that.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Driven Snow — Tara Lain; tertile=begin; p=0.44**
>
> The domino effect began. [TARGET] Junior the giant leaned over to Cyclops number two and asked who they were. Cyclops passed it on until heads started turning, forming a phalanx of frowns.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Hakan/Severin — Alexandra Ivy; tertile=middle; p=0.41**
>
> Busted. “ [TARGET] Who is the best?” he prodded.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · A Season of Change — Lynette Sowell; tertile=middle; p=0.35**
>
> Steven was the professional among them, and she imagined Henry did his fair share of angling, judging by the way he cast his line where he stood, a few feet away. [TARGET] Zeke said something about having prize ribbons for whoever caught the first fish, the biggest fish, and the most fish. Of course, he kept insisting he’d reel in a shark. “

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 193 — Nurse Arranged After Hospital Release

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** caleb, gage, jeremiah, conrad, mica, said, texting, ignore, went, fooled
- **KeyBERT:** dr, willing, hi, uh, arrange, stares, embarrassment, nearby, speaking, admitted
- **POS:** snaps, hopeful, stares, embarrassment, explanation, evidence, screen, bodies, huge
- **MMR:** prodded, acknowledge, snaps, arrange, collected, hopeful, hovered, stares, embarrassment, climb

**BERTopic representative docs**

> 1. that’s not fair, i’ve never thought of you like that, ty, and gage—” tyler’s eyes narrowed and darkened at the mention of his cousin. “

> 2. gage was cute, but despite the fact that i didn’t acknowledge ruger’s right to give orders, i also didn’t want to get into a huge fight with him. “

> 3. i want caleb goode to treat me like his own personal fuck toy, his dirty secret, his guilty pleasure.

**Stage-08 labeling snippets**

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

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 240 — Unsure How to Offer Comfort

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** sean, jaime, brogue, answered, looked, said, bryan, yseult, morrissey, repressive
- **KeyBERT:** mumbled, solemnly, absently, winced, patted, willing, shivered, assume, anxious, ed
- **POS:** equal, anxious, stares, conscious, latest, unsure, curiosity, task, distracted, thigh
- **MMR:** absently, solemnly, anxious, stares, ducked, conscious, studying, distracted, mumbled, shivered

**BERTopic representative docs**

> 1. sean would never admit it if asked —his stock answer being that he developed the five r’s after years of watching other men make mistakes, his personal track record with women being flawless—but a few points are actually derived from personal experience.

> 2. asbjorn chose to ignore the hated nickname, focusing on sean instead, running his hand underneath the shorts and down sean’s slender hip.

> 3. sean took nell’s hand and began walking toward the club, noticing that the other three were quick to retreat, and not anxious to fight once the odds weren’t in their favor. “

**Stage-08 labeling snippets**

> 1. oh my god, sean!

> 2. sean pursed his lips, unsure he was equal to the task of comforting [person].

> 3. sean held out his hand and added; “now if you’ll excuse me i have a beautiful woman waiting to have breakfast with me.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_D; thin cells CELL_C; 10 examples from 9 books; ±1 context on 10_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · A Little Harmless Fantasy — Melissa Schroeder; tertile=end; p=0.55**
>
> That’s not the really bad news.” “ [TARGET] Dammit, Conner just tell me.” “ The name of the company, your name in particular, came up in some documents.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Letting Evil In — Ellie Eden; tertile=middle; p=0.79**
>
> Why? [TARGET] What’s going on between you and Sean?” Emma and Sean had a tumultuous relationship.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Crossing Hudson — Mandy M. Roth; tertile=begin; p=0.44**
>
> I was used to it. “ [TARGET] This blows, Ryan,” Shona, a close friend and fellow demon-butt kicker, said as she turned to head back to the group of teen girls who were currently giggling in the other room of the establishment. She did not share my enthusiasm for the celebration.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Crossing Hudson — Mandy M. Roth; tertile=end; p=0.49**
>
> His breathing increased and he clenched his fists, the cords in his neck popping. “ [TARGET] Geesh, cut the guy some slack, Ryan,” said Shona. “ He did just go on a killing spree for you.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Pants on Fire — Meg Cabot; tertile=begin; p=0.50**
>
> Sidney wanted to know. “ [TARGET] Oh,” I said, thinking fast, watching as Seth started to show Liam how to use another nearby machine, while the Tiffanys and Brittanys gathered round, looking more worshipful than ever. Because, hello, Jake Turner’s little brother.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · In Service — Mima; tertile=end; p=0.48**
>
> Kor calls it, ‘getting his crazy on.’ [TARGET] You need to stop nipping at him and face the fact that when Shon goes under, he’s off limits, one breath away from being a hostile at our backs.” “ He wouldn’t do that!” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · The Day You Saved My Life — Louise Candlish; tertile=middle; p=0.75**
>
> If you’re not there at the beginning of a child’s life, maybe there’s just not the same pull later.’ [TARGET] James gave this only a moment’s consideration before asking, ‘What’s Sean’s excuse?’ But to this Joanna had no reply.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Make it Rain — Terri  Marie; tertile=end; p=0.77**
>
> Uh, our grandmother died if anyone asks." " [TARGET] Let me guess," said Sean. " You had court appointments?" "

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · The Finale — KaSonndra Leigh; tertile=middle; p=0.36**
>
> I despised not being able to move, to talk, to shout, to help. “ [TARGET] Nwoooo!” Nila.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Rebellion — Sabine Priestley; tertile=begin; p=0.23**
>
> Kensington and the K logo Reg. [TARGET] U.S. Pat. & TM Off.

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 242 — Trading Forgiveness For Old Wrongs

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** forgive, forgiveness, forgiven, forgiving, me, please, can, hope, ll, never
- **KeyBERT:** forgive, apology, harshly, fault, spite, terribly, hurts, surely, assume, willing
- **POS:** spite, treatment, apology, permission, hurts, actions, bigger, purpose, process, emotions
- **MMR:** forgive, spite, harshly, treatment, apology, permission, process, thousand, emotions, fault

**BERTopic representative docs**

> 1. can you forgive me ?”

> 2. he forgives us so we have to forgive others.

> 3. would you forgive me anything?’ ‘

**Stage-08 labeling snippets**

> 1. not if you’ll forgive him.” “

> 2. he’ll never forgive you.

> 3. okay, how’s this — i’ll forgive you for summer if you forgive me for kabir.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_15 examples from 14 books; ±1 context on 15_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · Mending Places — Denise Hunter; tertile=end; p=0.79**
>
> It helps me to forgive.” “ [TARGET] I don’t deserve your forgiveness.” “ Your mom didn’t deserve forgiveness, either, but you gave it to her.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Buck's Landing — Cameron D. Garriepy; tertile=end; p=0.51**
>
> I spent so much time and energy running from my father’s ghost that I was blinded to the fact that I was repeating his mistakes. [TARGET] I let someone I love slip away, and I was too proud to fight to get him back.” She saw a tiny flicker, a muscle working in his jaw.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Revenge — Shelly Bell; tertile=begin; p=0.60**
>
> He unlocked the door and switched on the lights as she stepped inside. “ [TARGET] But forgiveness doesn’t require you to invite her back into your life, and it certainly doesn’t obligate you to take the blame for the attack. She chose her actions, and she has to accept the consequences for them.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · The Widow Vanishes — Grace Callaway; tertile=begin; p=0.54**
>
> Laura would never be his, and thinking of her—of the life he'd left behind years ago—only made bitterness well up again. [TARGET] By nature, he was quick to anger and equally quick to forgive ... except when it came to betrayal. The Scotsman in him—the man in him—could not abide disloyalty.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Ruined by Rumor — Alyssa Everett; tertile=begin; p=0.55**
>
> I know this must come as an unwelcome surprise, but it will be best for both of us.” [TARGET] Any man delivering such a speech to the lady he had planned to marry—a lady who had waited faithfully for him—should have had the grace to appear remorseful, or at least apologetic. George just looked determined.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Pride, Prejudice and the Perfect Match — Marilyn Brant; tertile=end; p=0.73**
>
> Yes, Beth. [TARGET] What I’m asking, though, here and now, is if you’ve forgiven me . I lied to you, too.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Not Quite Broken — Diana DeRicci; tertile=end; p=0.68**
>
> We’re still here, where you grew up. [TARGET] If you can forgive us enough to take that step, I will swear on any promise you want that we still love you. Because we do.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · The Bride Behind the Curtain — Darcie Wilde; tertile=begin; p=0.49**
>
> This is our dance, and I am offensively late to come to you. [TARGET] Do say you will forgive your clumsy chevalier and grant me the very great favor of your company for this waltz.” He bowed and held out his arm.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Hanging by a Thread — Jenna Sutton; tertile=begin; p=0.44**
>
> So, Bebe’s a virgin, and you’ve taken it upon yourself to get rid of her pesky hymen,” Quinn noted dryly. “ [TARGET] You’re such a martyr to sacrifice yourself like that. Maybe you’ll be canonized as Callum, the Patron Saint of Cherry Popping.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Surrender Forever — Raven J. Spencer; tertile=end; p=0.83**
>
> I wanted to tell you, but he asked for more time, and I honestly thought he was going to clean this mess up, not make more of it. [TARGET] Do you think you can ever forgive me?” “ I already have.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Sugar Pine Trail — RaeAnne Thayne; tertile=middle; p=0.59**
>
> I’m a nice guy. [TARGET] Besides, Pop would never forgive me if he found out I let you suffer down here on your own without lending a hand.” She did adore his father.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Sugar Pine Trail — RaeAnne Thayne; tertile=middle; p=0.51**
>
> Don’t worry. [TARGET] I won’t accost you again.” “ You didn’t accost me.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Marrying for King's Millions — Maureen Child; tertile=middle; p=0.59**
>
> Why?” “ [TARGET] You must forgive him,” Rico said with a laugh. “ A freshly wed man has many things on his mind.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Hope for Christmas — Jennifer  Hayden; tertile=end; p=0.79**
>
> You didn’t have to do this. [TARGET] I would have forgiven you eventually.” “ That’s not what you said,” Holly pointed out, smiling halfway.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Never Just Friends — Mina V. Esguerra; tertile=end; p=0.62**
>
> I’m sorry,” Lindsay said, but not about the show. [TARGET] And she wasn’t just sorry, she was repentant. She was an idiot.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 247 — Promising You Will Not Be Alone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** alone, solitude, want, be, being, don, live, here, rather, prefer
- **KeyBERT:** upset, praying
- **POS:** options, terms, circumstances, attempt, fault
- **MMR:** praying, preferred, options, circumstances, chose, appreciate, attempt, insisted, planned, fault

**BERTopic representative docs**

> 1. shopping for one person doesn’t depress me as it does some of my other single friends; i am happy to be alone and everybody needs to eat, but it has come to this.

> 2. i didn't want anyone to know just how alone i felt. "

> 3. there was a part of me that wondered if being alone permanently was a good solution to my issues .

**Stage-08 labeling snippets**

> 1. if we make it through this alone, we’ll just be better at being alone.”

> 2. you’ll never be alone.

> 3. before you say no, i want you to know i’ll be alone mostly.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Lovely Shadows — Kendra Kilbourn; tertile=end; p=0.64**
>
> Everything that had happened in the last six weeks went with him. [TARGET] Despite being surrounded by my family I felt utterly alone. For the last six weeks I had something to live for, something that mattered, a purpose.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · The Arrangement 10: The Ferro Family — H.M. Ward; tertile=middle; p=0.49**
>
> When does pretending become a mental illness? [TARGET] I’ve had to pretend day in and day out that I’m fine, that I’m not falling apart. How is this any different?

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · A Peculiar Connection — Jan Hahn; tertile=middle; p=0.67**
>
> I sometimes thought daylight stretched into twenty-four hours before evening fell. [TARGET] I longed to be alone with my thoughts, to avoid my family’s questions as to why I suffered such discomposure and what had become of my former lively self. While spending the required hours in their company following supper, I counted the minutes until I could flee to my chamber.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Chasing Eva — Camellia Hart; tertile=end; p=0.53**
>
> I should stop dilly-dallying and simply ask Dusty to be my husband. [TARGET] There was no one else I wanted to spend the rest of my life with but him. We were made for each other. “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Shattered Glass — A.C. Katt; tertile=begin; p=0.64**
>
> I’m so afraid that this is all a dream. [TARGET] I’ve pictured this so many times in my mind, I don’t want to wake up and find I’m alone again.” “ I promise you, you will never be alone again so long as I live.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · A.J.'s Angel — L.A. Witt; tertile=end; p=0.52**
>
> Once we’d started on the tattoo, you were pretty much stuck with me until it was done, so…” “I know. [TARGET] I was going to get it anyway, and I honestly couldn’t imagine anyone but you doing it, so I figured that would also get us in the same room.” “ Captive audience?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Come Dancing — Leslie   Wells; tertile=middle; p=0.70**
>
> All this time I’ve been worried about you. [TARGET] It’s hard enough being alone in a small town where you know everybody; I can’t imagine being single in a place like this.” “ I wanted to tell you in person.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · Love's Betrayal — Stormy Glenn; tertile=middle; p=0.76**
>
> You might be right. [TARGET] I guess I wanted to be alone or I wouldn’t have ended up like I have. But I don’t want that for you.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · So Into You — Sandra Hill; tertile=end; p=0.44**
>
> Apparently, he had already filed guardianship papers for Lena this morning, now that the house is complete, and that’s what prompted this SWAT-type swoop down on them. [TARGET] Luc says Lena is a basket case and is alone at the house. Can you go over there, Grace?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Born of Ashes — Caris Roane; tertile=end; p=0.56**
>
> So we watch and we wait. [TARGET] When the time comes, please believe that you will not be alone, that Madame Endelle, for all her eccentricity, is not alone. There are movements in every Territory on the planet, usually led by Militia Warriors, even in those Territories aligned with Greaves, that work to keep the average ascender informed.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · What Were You Expecting? — Katy Regnery; tertile=begin; p=0.43**
>
> He didn’t need much, and if he had longings deep in his heart for more than his life offered, he was able to ignore them. [TARGET] He lived quiet and alone, loving his family and avoiding anything more than an occasional short-lived fling. He’d had his chance for love long ago and destroyed it.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · What Were You Expecting? — Katy Regnery; tertile=middle; p=0.47**
>
> Before Maggie could process the jolt of confused pleasure she got from his words, Mrs. Skinner stepped forward, offering her hand to Maggie. “ [TARGET] How nice not to be the only girl with all of these boys.” Maggie chuckled softly, shaking hands. “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Knockout — Leora Stark; tertile=begin; p=0.41**
>
> You need to deal with this. [TARGET] You need to get used to people seeing you. Figure out a way to deal with their questions.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · The Dungeon of Depraved Beasts — Bree Bellucci; tertile=begin; p=0.60**
>
> Olivia wasn’t in the mood for pleasantries, especially now. “ [TARGET] I don’t really want to go into it, and forgive me for being rude, but I would really prefer to be by myself right now.” Olivia chose her words carefully.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Frosh: First Blush — Monica B. Wagner; tertile=middle; p=0.55**
>
> Ellie had seen her at the party— “The competition at the Nexus is always fierce,” Tanner interrupted her thoughts. “ [TARGET] Unless, you reckon there’s someone else out to get you?” Ellie couldn’t meet his eyes.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Frosh: First Blush — Monica B. Wagner; tertile=middle; p=0.41**
>
> He stepped in front of her. “ [TARGET] I know you’re not like ‘all the other girls around.’ It’s why I like you.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 293 — Admitting Jealousy Out Loud

- **Taxonomy:** 4.7 — Jealousy & Possessive Romance Conflict
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** jealous, jealousy, jealously, sliver, irrational, twinge, pang, emotion, be, being
- **KeyBERT:** attracted, upset, emotional, concerned, warned, assured
- **POS:** concept, foreign, current, emotional, advantage, ex, wound, upset, reaction
- **MMR:** inched, playfully, wiping, stirred, emotional, tipped, warned, approached, wound, upset

**BERTopic representative docs**

> 1. should i be jealous of this cayden?”

> 2. they would be so jealous. “

> 3. i am never jealous.” “

**Stage-08 labeling snippets**

> 1. the concept of jealousy is foreign to them.

> 2. but this jealousy of yours is gonna ruin what you’ve got with j.d.” “i know.” “

> 3. we’ve been around the markets and —’ as she enthused away, i couldn’t help but feel jealous.

> 4. should i be jealous of this cayden?”

> 5. they would be so jealous. “

> 6. i am never jealous.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Packet representative sentences** (fallback when CELL sample empty)

> 1. You're jealous." "

> 2. I've always maintained that a little bit of jealousy looks good on a man. "

> 3. Well, of course I'm jealous," I frowned, poking him in the chest. "

> 4. She was also extremely irate over the fact that her boyfriend was using me to make her jealous—without my permission, as I've told you a couple of times.

> 5. I'm flattered that you're jealous, but you should know by now that no other woman could begin to compare with you.

> 6. And he was insanely jealous of the man I loved.

> 7. This is not arrogance talking, this is not jealousy, it is simply a matter of facts."

> 8. I debated staying where I was, standing firm for ethical reasons, but the thought that she'd be in the closed, womb-like confines of the trailer alone with Raphael was enough to spike my jealousy count off the chart.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 299 — Pledging to Have Your Back

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** dane, eoin, dan, would, alicia, seen, handle, time
- **KeyBERT:** promises, tries, willingly, exquisite, embarrassing
- **POS:** remark, threats, hundreds, remote, exquisite, distraction, embarrassing, promises, spending, terms
- **MMR:** remark, solemnly, instructed, discussing, distraction, promises, rapidly, terms, threat, forgive

**BERTopic representative docs**

> 1. it means there’s probably only one person who knew the real charlie blacksworth and unless you go back there, talk to her and try to understand, you’ll end up just like me, tormented and miserable for the rest of your damn life.”

> 2. charlie day, you are quite possibly the most exquisite creature on this planet, and if anyone tries to tell you different, i’ll cut a bitch.”

> 3. i realise charlie’s creating a distraction to save candi getting herself in too much trouble with the guys and to try to put an end to the rapidly escalating fight.

**Stage-08 labeling snippets**

> 1. before she’s completely out i ask, “[person], you know i’ve always got your back, right?”

> 2. but i’ve seen you, seen who you are, watched you handle uncle charlie.

> 3. i’ve got a little time before charlie finishes my bike.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_C, CELL_D; 8 examples from 7 books; ±1 context on 8_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Revenge — Debra Webb; tertile=middle; p=0.49**
>
> Yes. [TARGET] Kevin was worried that Scott’s death was somehow related to Todd’s return to Birmingham.’ Juliette Coleman was scared to death and still she was keeping some aspect of the reason to herself; otherwise she’d have no trouble with direct eye contact.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · When Fully Fused — Shari J. Ryan; tertile=middle; p=0.69**
>
> It's locked, like always. [TARGET] Charlie keeps us locked in here so Alex can’t get out and hurt himself like he used to at the institution. If the door is locked, then where is he?

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Life Before Damaged, Volume 1: The Ferro Family — H.M. Ward; tertile=end; p=0.41**
>
> It makes me want to say yes. [TARGET] Pete makes me reconsider everything. Heat pools in my forbidden areas against my will.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · The Biker's Brother — Victoria Danann; tertile=end; p=0.37**
>
> So he bought a copy of the magazine, found out who Brandon was and went to New York looking for him. [TARGET] When Brash turned up at Brand’s office, the first thing Brash noticed - after Brandon’s shocked look, was a big bowl of peanuts on his desk.” Brigid stopped to chuckle like she could imagine being there. “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Summers at Blue Lake: A Novel — Jill Althouse-Wood; tertile=end; p=0.77**
>
> I’ve been meaning to come visit with you and express my condolences for your loss.” “ [TARGET] I understand you were the last one to see Charlie alive.” “ Yes.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Set: A Love Story — Karen Dodson; tertile=middle; p=0.69**
>
> Isn’t it possible that you can stay at someone’s house a lot without sleeping with her? [TARGET] Charlie again, reading my mind: “A lot of people more or less understood that they were together. He allowed that to be understood.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Bad Impressions — Franca Storm; tertile=middle; p=0.50**
>
> I never had been. [TARGET] But Brad was such a consuming force that he was always there on my mind. I had to force myself to put him out of my mind when I was at work, or I’d lose my concentration.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_012 · Bad Impressions — Franca Storm; tertile=begin; p=0.51**
>
> God, do the men in my life not understand the concept of privacy? [TARGET] It was then that I realized Brad wasn’t in my room. He’d gone?

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 305 — Confessing A Lifelong Regret

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** regret, regretted, regrets, regretting, regrettable, won, will, decision, promise, don
- **KeyBERT:** embarrassing, fears, remark, admit, surely, instantly, decision
- **POS:** fears, remark, decision, loose, upset, unable
- **MMR:** handled, fears, remark, fumbled, drift, assure, acted, decision, upset, ended

**BERTopic representative docs**

> 1. why would i regret this?” “

> 2. you will regret it.

> 3. both of you will regret this.”

**Stage-08 labeling snippets**

> 1. i know that now, and i’ll go to my grave regretting what i did to you.” “

> 2. come on in, you’ll no doubt regret it.

> 3. you’ll regret that.’ ‘

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 12 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Rogue — Katy Evans; tertile=middle; p=0.71**
>
> and the morning after. [TARGET] The memory brought with it a pang of regret. Regret that he was not there.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Negotiation Tactics — Lori Ryan; tertile=middle; p=0.59**
>
> She knew he’d probably gone for a run on the beach and she was glad to have the time to herself. [TARGET] She didn’t regret last night, but she did hope it didn’t destroy the friendship they had. She wanted Chad in her life.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · The Remedy Files: Illusion — Lauren Eckhardt; tertile=end; p=0.45**
>
> I finish my trek around the final three houses and swing up to go behind the back row and to the route back home. [TARGET] I replay the conversation in my head with Jacqueline, wishing that the outcomes I had practiced were the final result instead of how reality turned out to be. Jacqueline did always firmly believe in the ways of Impetus.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Salvation — Ahren Sanders; tertile=end; p=0.72**
>
> If she’d have come back here, I’m not sure what would have happened. [TARGET] I couldn’t trust myself to not say something we’d regret.” “ You mean, you’d regret.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · A Marriageable Miss — Dorothy Elbury; tertile=middle; p=0.66**
>
> I’m not sure that I entirely understand you,’ queried Richard. ‘ [TARGET] You are surely not intending to imply that you are beginning to regret this marriage already?’ ‘ I doubt that it would bother you greatly were I to do so, my lord,’ returned Helena, with a careless shrug. ‘

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Having Patience — Debra Glass; tertile=middle; p=0.61**
>
> He’d told her he loved her. [TARGET] Cringing, he regretted the admission. His heart twisted.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Too Dangerous For a Lady — Jo Beverley; tertile=begin; p=0.64**
>
> I will be willing to give any information I can, though I know no more than you do. [TARGET] Convey my regrets that my obligations mean I cannot linger hereabouts.” He offered some coins. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_014 · Bad Impressions — Franca Storm; tertile=begin; p=0.59**
>
> So, I’d done what I’d had to: I’d blown her off. [TARGET] Better a short period of hurt than a lifetime of regret for her. She’d called me a coward the other day, but she had no idea how hard it’d been for me to walk away like that.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Child of War - A God is Born — Lisa Beth Darling; tertile=begin; p=0.47**
>
> I will not share my bed or my life with someone like that. [TARGET] I would rather this belt cut into me forever; never know the love of a man, than to take that risk." Ares was stunned into silence by her words but he soon recovered and leaned forward. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Child of War - A God is Born — Lisa Beth Darling; tertile=begin; p=0.58**
>
> My trip to the Underworld has left me even more so than before. [TARGET] I have been unkind to you, which I deeply regret. It has…left a scar upon my heart."

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Falling for the Hometown Girl — Shelli Stevens; tertile=middle; p=0.61**
>
> He hadn’t even hesitated, just made the decision to book with them. [TARGET] And, so far, he couldn’t bring himself to regret, despite his initial reluctance. No matter what happened with Katie.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Falling for the Hometown Girl — Shelli Stevens; tertile=middle; p=0.43**
>
> Sounds about right.” “ [TARGET] I wish they would’ve let me know ahead of time. I would’ve adjusted the amount of food I cooked.” “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · In Her Eyes — T.R. Jones; tertile=begin; p=0.45**
>
> Mary drove you to the hospital, and you were trying to feed squi r r e ls the very next day. [TARGET] At least you did it from the ground the second time. ” “ Hey Sam, could you go into the kitchen and make s ure Bell doesn’t burn it down.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · In Her Eyes — T.R. Jones; tertile=middle; p=0.68**
>
> He had done what he knew was best for her. [TARGET] He had no regrets. “ Sit down Charles you’re making a fool of yourself.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · The Morning After Memoirs — Kate  Michaels; tertile=begin; p=0.38**
>
> If the national form of commemoration comes as a silence, and the general feeling is that ‘nothing can be said that is sufficient to the subject’, then any objection or testimony put forward by the ex-servicemen can be deemed as unpatriotic and insensitive. [TARGET] 40 The ‘regrettable scene’ in Liverpool on Armistice Day 1921 was reported in just these tones. 41 About 200 ex-servicemen, ‘purporting to represent the unemployed of the city’, forced their way through the crowd that was gathered for the Two Minutes’ Silence at 11 o’clock and proceeded to ‘demonstrat[e] their grievances’.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · The Morning After Memoirs — Kate  Michaels; tertile=middle; p=0.27**
>
> As with the previous League-themed competition, the editors remarked, ‘this competition has proved rather more difficult than usual, and the results are rather disappointing’; they did single out ‘for honourable mention’ a number of other contributors, though only six. [TARGET] 28 Both competitions proved disappointing – a symbol perhaps of attitudes towards the League. Yet some found cause to celebrate the negotiations at Versailles, if for no other reason than to exploit the momentous events to sell their wares.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 307 — Hauling Someone Up The Stairs

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** ash, fee, roy, ashe, darren, amaranth, after, vasai
- **KeyBERT:** heaved, winced, struggled, digging, emerged, merely, items, fought, urge, precisely
- **POS:** threats, la, items, conscious, affection, anxiety, member, panting, movements, permission
- **MMR:** threats, emerged, heaved, discussing, urged, anxiety, panting, movements, winked, merely

**BERTopic representative docs**

> 1. his thoughts threatened to return to those awful times once again, but thankfully, ash and dan emerged from the thicket.

> 2. given how introverted fee was, ash doubted he'd lure fee out with the late-night after party crowd he usually hung out with. "

> 3. trouble was, ash was starting to really like how he fit at her hips, how his weight shifted between her thighs, how the falls of his dreads tickled her bare arms whenever she struggled to stop his movements and she had to readjust her hold to keep him from wriggling free or to keep the ... please don’t let that be a gun ... in his pocket from digging into her flesh.

**Stage-08 labeling snippets**

> 1. [person] would hate it if she took a rake like [person] to her bed, and she would so love to rub it in joshua’s face and prove his threats could not restrain her. “

> 2. his thoughts threatened to return to those awful times once again, but thankfully, ash and [person] emerged from the thicket.

> 3. getting ash up the stairs and into the bedroom was a lot harder than it had been last night, mostly because ash was pissed off and conscious instead of in la-la land.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_C, CELL_D; 8 examples from 7 books; ±1 context on 8_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Origin — Jennifer L. Armentrout; tertile=end; p=0.76**
>
> They threatened to take you all in.” [TARGET] He spun toward Ash and Andrew. “ Even you.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · A Touch of Midnight — Lara Adrian; tertile=middle; p=0.43**
>
> Gideon dropped the big corpse as the titanium began to feed on the Rogue, dissolving it from the inside out. [TARGET] In mere minutes, the lump of dying flesh and bone would be nothing more than ash, then all evidence of its existence gone altogether. Gideon turned to face Savannah. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Cinder & Ella — Kelly Oram; tertile=end; p=0.55**
>
> I was the last person that should ever be in the spotlight. [TARGET] Cinder started to look excited, but I couldn’t share his optimism. “ I don’t think so, Cinder—er, Brian.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Forget Me Not — Allison Whitmore; tertile=begin; p=0.70**
>
> She knew they caused trouble sometimes, but Ashleigh was way more exciting and popular than Lizzie’s old friends. [TARGET] Her parents didn’t like Ash, she could tell. They were always asking when Georgia was coming over.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · A Change of Tune — J.M. Cartwright; tertile=end; p=0.51**
>
> They chatted a bit, his mother asking about the dogs and Johnny asking about the hospital where she worked. [TARGET] But as he was approaching Clarksburg, Ashlynn chose that moment to be cranky. Her little voice rose as she began crying.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Moon Chilled — Caitlin Ricci; tertile=end; p=0.48**
>
> Gasps broke the silence of the gathered crowd, but no one moved forward to help on either side. [TARGET] I was glad that none of the men jumped in to help the alpha, but I wished someone would help Shae. I started to understand why not, though, why no one would or could.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Moon Chilled — Caitlin Ricci; tertile=end; p=0.45**
>
> Is there really no one else?" [TARGET] I looked around at the others, searching for anyone with Shae's strength, her will. Finally, I shook my head and shifted Gavin to my hip. "

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · The Tide of War — Lori A. Witt; tertile=end; p=0.65**
>
> He was afraid to even think of which cities they might have been. [TARGET] Which places on his own home planet he’d turned to ash. “ We’ve all lost people,” he heard himself telling Kyle.

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 356 — Admitting Exhaustion After A Long Day

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** tired, exhausted, exhaustion, am, must, tiredness, kind, fatigue, getting, too
- **KeyBERT:** rested, drained, worn, sir, remarked, session
- **POS:** session, sir
- **MMR:** remarked, drained, session, emotionally, studying, ok, washed, worn, rested, sir

**BERTopic representative docs**

> 1. you must be exhausted.”

> 2. and you must be even more exhausted.” “

> 3. you must be exhausted.”

**Stage-08 labeling snippets**

> 1. i am kind of tired, but you’ve done enough.

> 2. i’ve been riding most of the day, i’m tired.” “

> 3. i’ve rested more than i ever expected to rest in the whole of my lifetime during the past six weeks,” he said, “and i’m feeling perfectly fresh.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Exposed — Raven St. Pierre; tertile=end; p=0.70**
>
> Alright, I think I’ve had enou gh of you two ladies’ brutality for one night,” he announced, rubbing his hand down his face. “ [TARGET] And I’m sure you’re pretty tired by now, too,” he said to me, making this assumption because, lately, I was always tired. On cue, our son kicked me hard enough that I had to place a hand on my stomach, attempting to rub the tender spot that he’d been pummeling all day. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Hidden Trust — Nicole Colville; tertile=middle; p=0.79**
>
> When I've run out of oxygen, I pull off his lips and smile down at him. “ [TARGET] I'm not as tired as I thought.” Davide shakes his head softly. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Her Darkest Road — Nicole  Hart; tertile=begin; p=0.58**
>
> I jerked my head up as I glared my eyes at her, willing her to look at me. “ [TARGET] My husband has to run some errands and I could use a nap, I’m a little tired,” she said, and started to yawn. She was lying.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Volatile — Avylinn Winter; tertile=begin; p=0.57**
>
> I held the card in a tight grip, afraid that I would drop it—that was how much I was struggling to stay awake. [TARGET] Perhaps it was the fact that I was so close to a bed that made me feel exhausted beyond what I should feel at one-thirty a.m. When I opened my door, I realized that my bags were already inside. For a moment, I just stood there, wondering how the hell that happened.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Air Kisses — Zoe Foster; tertile=end; p=0.60**
>
> As we drove home, my conversation gradually slowed until I was entirely mute. [TARGET] I was tired from a big week, my nervous energy had transformed into lethargy, and I was still drunkish. I tried to digest what had occurred that evening, as well as forecast what I would do when he pulled up at my place.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Kept — Shawntelle Madison; tertile=middle; p=0.72**
>
> It could very well be exhaustion.” “ [TARGET] But I’ve been exhausted before and it’s never been like this .” “ Could you be pregnant?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Become You — Michelle Grubb; tertile=end; p=0.68**
>
> Olivia sulked and focused on the road. “ [TARGET] You look tired,” she said finally. “ Are you okay?” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Sand & Clay — Sarah  Robinson; tertile=middle; p=0.70**
>
> It’s going to be six months long around the globe and it is going to be jam packed, international and east coast to west coast finally ending in Las Vegas. [TARGET] Then I will be back home and sleeping because I will be exhausted.” Logan was saying to the host, jokingly. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Out of Control — Suzanne Brockmann; tertile=middle; p=0.55**
>
> I thought we were over the pouting phase. [TARGET] Aren’t you getting just a little tired of—” “I wasn’t kidding about the way it gets dark out here. I don’t know when moonrise will be.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Out of Control — Suzanne Brockmann; tertile=begin; p=0.70**
>
> But I didn’t want to go anywhere lovely with Prince Anyone and have to sit at a table covered with white linen while waiters and wine stewards danced nervously around, and looked down their noses at me for using the wrong fork. [TARGET] I was tired and cold and done with feeling under siege for the day. “ It’s not very fancy,” he told me as if he could read my mind. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Timeless — S.J. West; tertile=end; p=0.58**
>
> Finally, he has no choice but to meet my gaze when he hands me the blanket back. “ [TARGET] You should get some rest,” he tells me, his voice completely devoid of emotion. “ I’ll see you tomorrow at Jess’ place.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · The Light — Kate  Thomas; tertile=middle; p=0.53**
>
> He blew out a long breath. [TARGET] Caden was so fucking exhausted. And it was an exhaustion that had absolutely nothing to do with last night’s lack of sleep.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · The Firefighter's Secret Baby — Anna DeStefano; tertile=middle; p=0.67**
>
> About trusting her father to help you—” “Don’t tell me you actually think Randy should stay with me!” “ [TARGET] You’re exhausted and emotionally drained. If having Montgomery around is what’s best for you, if he’s willing to risk—” “Like Peter was willing to risk his life to stay with me?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Overbite — Meg Cabot; tertile=end; p=0.62**
>
> I can hear it in your voice. [TARGET] You’re tired, and I’m certain you’re feeling weak because of the smoke in your lungs. Imagine a life where you’d never have to feel weakness or pain again.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Letting Go — Kelli Roberts; tertile=middle; p=0.35**
>
> Nothing with wheels is allowed on this trail, making it popular with both walkers and runners who don’t want to hassle with mountain bikers whizzing by. [TARGET] This time of the evening, with people having just gotten off work, there are a fair number of exercisers here. I wouldn’t call it crowded, by any means, though.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Letting Go — Kelli Roberts; tertile=middle; p=0.59**
>
> It feels good, even though my wrists are still bound together. [TARGET] I hadn’t realized how tired my shoulders had become until I was able to bring my arms down. But why has Sir untied me?

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 61 — Planning to Exchange Rings

- **Taxonomy:** 8.3a — Commitment Symbols & Love Tokens
- **Current code (LLM):** **S4 — commitment security**

**Four keyword representations** (BERTopic / labeling)

- **Main:** ring, necklace, finger, diamond, stone, jewelry, gold, engagement, rings, diamonds
- **KeyBERT:** rings, promises, precious, engaged, glint, twisting, magical, gesturing, polished, dangling
- **POS:** rings, sized, precious, scenario, threats, glint, matching, polished, commander, value
- **MMR:** rings, collect, precious, claims, glint, presented, polished, commander, worn, stunning

**BERTopic representative docs**

> 1. anna was admiring his ring.

> 2. no wedding ring, but he did have a gold ring on his pinky finger.

> 3. her ring finger was adorned with a sizeable diamond. “

**Stage-08 labeling snippets**

> 1. in a few days, i’ll go to the stone.

> 2. next time we’ll put a ring on him.”

> 3. we’ll take care of the rings tomorrow.”

> 4. anna was admiring his ring.

> 5. no wedding ring, but he did have a gold ring on his pinky finger.

> 6. her ring finger was adorned with a sizeable diamond. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Packet representative sentences** (fallback when CELL sample empty)

> 1. Just have to close it up again, until it looks like a ring, and we'll be fine.

> 2. Once they're gone, Shanley pricks Marie's finger with a lancet. "

> 3. It's not quite a perfect C-shape any longer, but more like one of those spoon bracelets that come in and out of fashion--the ends are drawing together, tightening, and that's a good thing, right?

> 4. He took the ring out of the box and, with Damon’s help, they placed it on her finger.

> 5. I just need to put on my jewellery.”

> 6. I might even be persuaded to wear my jewellery for you.”

> 7. Jewellery?

> 8. Damon and I agreed that you own our hearts so we thought this ring would be perfect for our union.”

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S4`)
- Decision: KEEP / REMOVE

---

### Topic 65 — Declaring A True Partnership

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Current code (LLM):** **S4 — commitment security**

**Four keyword representations** (BERTopic / labeling)

- **Main:** date, dating, together, each, we, other, dated, dates, ve, two
- **KeyBERT:** engaged, partners, nods, fashioned, uh, honestly, longest, fitting, playfully, admit
- **POS:** longest, failure, partners, typical, session, fashioned, fitting, potential, handful, nods
- **MMR:** longest, officially, failure, partners, playfully, forming, forgetting, session, leads, intend

**BERTopic representative docs**

> 1. were you on a date?

> 2. we are on our date.

> 3. it’s not a date.

**Stage-08 labeling snippets**

> 1. what we’ve been though together, the way we’ve been there for each other ... we have a true partnership, a true love, and if that sounds stupid and romantic, then i don’t care.”

> 2. we’ve been together forever, and what if it takes us years?”

> 3. i’ll do that,” he said softly, “we’ve got a date.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Ciao — Bethany Lopez; tertile=middle; p=0.70**
>
> I talked to her before she went to dinner. [TARGET] We had a great date just a couple of days before… I don’t understand why this happened.” He started to break down again, and I reached over to grab his hand.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · To Know Me — Marcy Blesy; tertile=begin; p=0.72**
>
> It doesn’t make sense. [TARGET] We’ve only known each other a few weeks.” “ So what’s the magic time requirement for you, Mae?” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · The House At The End Of The Street — Jennie  Jones; tertile=middle; p=0.67**
>
> Thank you all for participating in our speed-dating night. [TARGET] There’ll be lots of fun, lots of opportunities to get to know each other—wink wink—and the hoped-for outcome, of course: a date.’ Gem winced.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Wish You Were Mine — Tara Sivec; tertile=end; p=0.65**
>
> Leaving my brother to deal with his own mess, I quickly move through the crowd of people until I catch up with Amelia standing by the opening of the tent opposite the main door I just came through. “ [TARGET] You are so lucky right now that woman was not really your date,” Amelia tells me as soon as I get to her. “ You’re going to have to do a lot of groveling with Cameron, but I’ve got your back.”

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · A Day at the Office — Matt Dunn; tertile=middle; p=0.67**
>
> Well, it isn’t really. [TARGET] We’re going out tonight, and…’ ‘On a first date?’ The man raised one eyebrow, and Sophie blushed. ‘

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Love Him or Leave Him — Sara  Daniel; tertile=middle; p=0.62**
>
> I can show you how to Skype,” Veronica said, “and you can rack up frequent flyer miles. [TARGET] If you’re really meant to be together, a long distance relationship will be worth it.” “ We’re definitely not meant to be together,” Becca said, walking down the steps, retracing her way along the driveway as Connor deftly separated Ron and Larry.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Holding On To Love — A.E. Neal; tertile=end; p=0.64**
>
> I’d like that,” I giggled and my cheeks flushed a little. “ [TARGET] Good, its a date then,” he said and pulled me into his chest. I buried my face in his neck and he still smelled amazing.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · The Houseguest: Complete Series — Nora Blackstock; tertile=middle; p=0.59**
>
> I was very happy for him. [TARGET] As I put some leftover food away I thought about our relationship. I had known hims since he was a baby, and we had now become quite close again.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · Sinful Magic — Jennifer Lyon; tertile=begin; p=0.49**
>
> We don’t make love, I just screw you until your magic is full! [TARGET] And if we do go out, then I have to deal with all the men swarming around wanting a taste of your sex magic! ” She shook her head and dizziness made the room sway. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Adam — Jacquelyn Frank; tertile=end; p=0.51**
>
> This is not like the mental rape Ruth put you through, and I will not have you equate the two. [TARGET] This is something with pure intentions, open emotions, and a reciprocation that will never cause harm to either of us.” “ How can you say that?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · My Hellion, My Heart — Amalie Howard; tertile=begin; p=0.44**
>
> But there was only one thing that helped to silence the noise: the base act of sexual release. [TARGET] No emotion attached, no conversation, no pleasant company. Just sex.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Brazos Bend Bride — Eugenia Riley; tertile=end; p=0.47**
>
> Then Margaret giggled. “ [TARGET] Pardon me, Emilie, I’m a wicked girl for thinking this—but the entire situation has a ring of romance to it, does it not? I don’t doubt Mr. Houston might have considered such shenanigans, had I refused his suit.”

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · The Fire Lord's Lover — Kathryne Kennedy; tertile=end; p=0.58**
>
> I am determined to enjoy my first public appearance with my husband." " [TARGET] We have often been together in public." " Ah, but not as a true couple.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Tuareg — Sarah Black; tertile=begin; p=0.47**
>
> You do not have to investigate unless it is something you feel strongly about, because I am doing that. [TARGET] But if you do wish to ask questions, you might start with the two of us. We wil tel you what you need to know."

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · The Legacy of Buchanan's Crossing — Rhea Rhodan; tertile=begin; p=0.67**
>
> Oh yeah, this was more like it. “ [TARGET] You can’t know how much I’ve been looking forward to meeting you.” Cumberland beamed enthusiasm and sincerity. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · The Legacy of Buchanan's Crossing — Rhea Rhodan; tertile=middle; p=0.64**
>
> Then I took a gander at my truck. [TARGET] It got me thinking maybe dating you wasn’t such a great idea.” Now it was her turn to be confused. “

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S4`)
- Decision: KEEP / REMOVE

---

### Topic 93 — Meal Plans Casually Arranged

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Current code (LLM):** **S2 — emotional security belonging**

**Four keyword representations** (BERTopic / labeling)

- **Main:** dinner, lunch, supper, tonight, tomorrow, we, ll, eat, having, lunches
- **KeyBERT:** meal, eaten, sentence, appointment, sir, shortly
- **POS:** appointment, exciting, regular, meal, sentence, movement, lady
- **MMR:** discussing, appointment, exciting, arranged, meal, sentence, ex, appreciate, planning, sending

**BERTopic representative docs**

> 1. then have dinner with me.

> 2. get on to dinner.

> 3. i could always cook dinner for you.

**Stage-08 labeling snippets**

> 1. that’ll wait ’til after supper, though.” “

> 2. i’ll go get started on lunch,” clark offered.

> 3. i’ll show you over dinner.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Damaged 2 — H.M. Ward; tertile=middle; p=0.67**
>
> Peter seems tense, like he has liquid anxiety flowing through his veins instead of blood. " [TARGET] We're going to have dinner with my brother tonight, if that's all right. I need his help with something."

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · The Art of My Life — Ann Lee Miller; tertile=middle; p=0.67**
>
> Yup. [TARGET] You’re invited for dinner at seven sharp, as per my Mom’s instructions.” The gleam fizzles out of his eyes and I stifle a chuckle at the nervousness that washes over his face. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Abstract Love — Samantha Christy; tertile=begin; p=0.64**
>
> I’m pretty sure there was some sexual abuse going on in his home, but he won’t talk about it and Social Services hasn’t come to that conclusion. [TARGET] We cook meatloaf and mashed potatoes, a house favorite and since my appetite is back I decide to stay for dinner. Unfortunately, Tyler and another teenage boy, Anthony, don’t get along very well and tension is high at the dinner table.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Mince Pies and Mistletoe at the Christmas Market — Heidi Swain; tertile=begin; p=0.63**
>
> No,’ she said, waving over at Marie. ‘ [TARGET] Don’t worry about that, I’ll bring you a sandwich and a hot drink on my way home, if you like.’ ‘ Ready?’

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Only You — A.J. Llewellyn; tertile=middle; p=0.72**
>
> Back home late in the afternoon, I chatted briefly on the phone with Angus, who was in meetings hell. [TARGET] We agreed to have dinner the following night. “ Bring the dogs,” he said. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Hooking Up — Jessica L. Degarmo; tertile=middle; p=0.72**
>
> I also knew that I was currently in no condition to give my heart to Ryan. [TARGET] We had made plans to meet for dinner tonight. I didn’t feel like going anywhere or doing anything.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Leftovers — Stella Newman; tertile=end; p=0.74**
>
> At least two pairs,’ he says. ‘ [TARGET] I’m back in a fortnight, I’d like to take you for dinner.’ ‘ Great.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · Because You're Mine — Avery Kaye; tertile=middle; p=0.71**
>
> I dump the bags of food on the counter and motion to the bedroom. “ [TARGET] I’m going to clean up and then I’ll cook dinner.” “ All right.”

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Midnight Awakening — Lara Adrian; tertile=end; p=0.52**
>
> What kind of host would I be to let you go all day without a proper meal? [TARGET] It seemed only fitting that I treat you to one of the city‘s finest dinners. They were seated together in a top-floor restaurant in one of Berlin‘s most exclusive hotels.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Seduce Me — Ryan Michele; tertile=middle; p=0.47**
>
> I try not reading more into this than it is, but he is making it difficult. [TARGET] After we are done, I clear the plates setting them on the desk after G.T. refuses to let me leave to take them back to the kitchen. I give G.T. his meds and he takes them without complaint. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Targeted — Becky Avella; tertile=middle; p=0.64**
>
> Do you want to wait around for Hale to deliver another present for you? [TARGET] Maybe I’ll call down and order breakfast and see what he has next on the menu.” “ All right, I get it.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Love at First Note — Jenny Proctor; tertile=middle; p=0.49**
>
> No, it wasn’t someone local. [TARGET] Ty promised to look into it and now they were off for their afternoon of unplanned shopping and eventually dinner. Of course, shopping meant a lot of shuttling back and forth between the stores and home.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · So I Married A Vampire — Elisa Adams; tertile=begin; p=0.51**
>
> He’d been right there with her as she scoured bridal magazines, getting ideas for bridesmaids’ dresses and flowers. [TARGET] He’d sat with her for hours going over the catering menu for the reception, listening to her gripe and moan about what they would serve their guests. He’d even been the one to choose the cream-colored frosting on the cake 7 Elisa Adams when she hadn’t been able to make up her mind.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Awakening — A.C. Warneke; tertile=begin; p=0.56**
>
> Her heart flopped in her chest at the heat of his mouth, the heat in his gaze. “ [TARGET] Perhaps we could skip dinner and get to know each other better now,” she said, her voice low and throaty. She couldn’t believe her words, or her sexy voice, yet she couldn’t take them back – she didn’t want to.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Awakening — A.C. Warneke; tertile=begin; p=0.63**
>
> Even stranger was how they brightened slightly the longer he stood in Adam’s presence. “ [TARGET] Celeste and I w ould enjoy our meal in the dining room immediately.” “ Will Master Auberon be join….”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_005 · Awakening — A.C. Warneke; tertile=end; p=0.40**
>
> He forced his lips upwards in a smile as he tilted his head back to look at her. “ [TARGET] I’m just wondering how many Calices I’m going to have tonight.” She smiled down at him as she began to massage the stress from his body.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S2`)
- Decision: KEEP / REMOVE

---

### Topic 143 — Complaining About Family Pressure

- **Taxonomy:** 5.1 — Family, Kinship & Parenthood
- **Current code (LLM):** **S2 — emotional security belonging**

**Four keyword representations** (BERTopic / labeling)

- **Main:** family, parents, your, families, my, are, our, we, know, part
- **KeyBERT:** admit, experience, folks, dealing
- **POS:** failure, slightest, folks, distress, typical, options, strained, disappointed, member, extended
- **MMR:** failure, distress, compared, survived, options, dealing, provided, strained, members, pressure

**BERTopic representative docs**

> 1. would you like to see your parents again?"

> 2. what do you know about your parents?” “

> 3. do you know either of my parents?

**Stage-08 labeling snippets**

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

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S2`)
- Decision: KEEP / REMOVE

---

### Topic 167 — Planning A Wedding Reception

- **Taxonomy:** 5.3a — Romantic Social Rituals & Public Couple Recognition
- **Current code (LLM):** **S4 — commitment security**

**Four keyword representations** (BERTopic / labeling)

- **Main:** wedding, bride, weddings, groom, bridal, our, ceremony, attend, jitters, bridesmaids
- **KeyBERT:** planned, invitation, reception, arrange, include, announced, destination, preparing, planning, official
- **POS:** reception, century, longest, invitation, extent, destination, official, tv, member, circumstances
- **MMR:** reception, include, century, invitation, destination, observed, planning, circumstances, announced, spending

**BERTopic representative docs**

> 1. on the eve of your wedding.”

> 2. so when will the wedding be?” “

> 3. i attended a wedding.’

**Stage-08 labeling snippets**

> 1. it’s my dream job, but instead of shooting brides, i’ll be shooting naked women.

> 2. we'll get married next summer in the church in maine that my mother would take me to every sunday.

> 3. the ‘ceremony’ in boorowa might just be signing a few papers, but carley’s planned a wedding reception they’ll never forget.” “

> 4. on the eve of your wedding.”

> 5. so when will the wedding be?” “

> 6. i attended a wedding.’

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Packet representative sentences** (fallback when CELL sample empty)

> 1. There’ll be plenty to talk about, anyway, after the wedding today .” “

> 2. Or my wedding .

> 3. It was their wedding day.

> 4. We can’t have a bride without flowers.”

> 5. Most of you seem to have caught wind of the DeWitt wedding.

> 6. Brice, you may kiss your bride .”

> 7. Madison and I are getting married after church services.

> 8. If the bride and groom would join hands and face each other, we’ll proceed in joining you together in holy matrimony .”

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S4`)
- Decision: KEEP / REMOVE

---

### Topic 190 — Offering to Get Someone Cleaned Up

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** clean, cleaning, cleaned, mess, up, cleaners, messes, freshen, ll, cleaner
- **KeyBERT:** cleaned, wipe, sweeping, dump, ok
- **POS:** sweeping, dump, session, parties, suitcase, ok, places, entire
- **MMR:** cleaned, sweeping, dump, provide, parties, suitcase, paying, including, assured, planned

**BERTopic representative docs**

> 1. i’m just … cleaning.” “

> 2. i hope you get all hot and sweaty cleaning out that mess,” betsy said. “

> 3. they’re cleaning up the mess.

**Stage-08 labeling snippets**

> 1. i’ll get cleaned up here as soon as i can.

> 2. i’ll pay to have it cleaned.” “

> 3. i'll get her cleaned up," said a handsome groom, taking her arm. "

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 14 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Witch Hunter — Shari Nichols; tertile=begin; p=0.62**
>
> She wrapped her arms around her body and sighed. “ [TARGET] But no matter how hard I scrubbed, I couldn’t seem to get the stench of death off me.” His gut tightened at her words.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Special Passage — M.L. Ryan; tertile=middle; p=0.51**
>
> After some discussion, we decided on a story that my sister Sarah was once again in a family way, but confined to bed due to complications. [TARGET] I was going to go to Ohio to help take care of my nieces while Sarah’s husband, Terry, continued to run their dry cleaning establishment. Rachel and Chelsea should find that believable, as Sarah had had some minor problems during her last pregnancy, and they knew enough about Terry from me to accept that he wouldn’t be able to supervise a business and three children under the age of four by himself.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · The Forgotten Recipe — Amy Clipston; tertile=begin; p=0.64**
>
> Mamm wiped her hands on a dish towel and then touched the short sleeve of Veronica’s blue dress. “ [TARGET] I know you’re doing all of this cleaning to distract yourself, but you need to slow down. You need to allow yourself time to grieve.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Noah — Cara Dee; tertile=begin; p=0.66**
>
> It was too soon to go through everything, and I wasn't hurting for money. [TARGET] I'd have the furniture covered and hire someone to clean until I was ready. " Let me know if you need help with your dad's will." "

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Khyber Run — Amber Green; tertile=begin; p=0.56**
>
> Here I pass for Tajik or Hazara, until I open my mouth." [TARGET] I scrubbed my tongue and teeth with a clean corner of the washcloth. Ugh.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Mergers & Acquisitions — Lillian  Grant; tertile=end; p=0.38**
>
> You should enquire with each to know their schedules. [TARGET] I suggest not going immediately, but a day or two after to allow them to sort through all the junk. Some caveats with buying from thrift stores and recycle facilities are that these keyboards usually aren’t modern.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · The Witch's Stone — Dawn  Brown; tertile=middle; p=0.71**
>
> He swallowed hard and continued. “ [TARGET] I’m going home to clean up, then I’ll get myself to the hospital.” Ms. Jenkins looked unconvinced.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · The Broken Triangle — Jane Davitt; tertile=middle; p=0.62**
>
> Some of them, like the mold by the kitchen sink, weren’t Patrick’s fault, but the mess and general grunginess were. [TARGET] He always seemed to have something better to do than clean. He could smell coffee.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Dark Peril — Christine Feehan; tertile=middle; p=0.49**
>
> We are preparing the body now.” “ [TARGET] I know you would prefer to burn it yourselves out of respect, but my way will be faster, cleaner and will ensure no parasites escape. It will also not provide a beacon for the undead.” “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Dark Peril — Christine Feehan; tertile=middle; p=0.55**
>
> Perhaps we made his choice easier. [TARGET] I will clean up the battlefield while you drink plenty of fluids. Then you must take me to the body and send everyone else away.”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Escaping Reality — Lisa Renee Jones; tertile=begin; p=0.51**
>
> Just let me grab a few things for the flight.” [TARGET] I quickly remove my file and my purse and hand over my carry-on, and in the process my hand brushes his. A jolt of electricity darts up my arm and I quickly turn away, buckling myself in.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · His Uncle's Favorite — Lory Lilian; tertile=end; p=0.56**
>
> It never crossed my mind to go to sleep without speaking to you. [TARGET] I just need to go and clean myself a little; then I will come to you shortly. Are you hungry?

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Midnight Marriage — Lucinda Brant; tertile=begin; p=0.41**
>
> Oh, but you do look well,” she sighed with satisfaction. [TARGET] A lackey came out from behind the butler with pan and brush and quickly set to sweeping up the shards of broken glass from Deb’s smashed wine glass. This broke the spell for Deb and she quickly pulled her hands free and crossed to the table, feeling the heat in her cheeks.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Midnight Marriage — Lucinda Brant; tertile=middle; p=0.45**
>
> You shouldn’t have called me a-a coward! [TARGET] Don’t you see that if you go ahead with this annulment, if you air the Roxtons’ dirty laundry in public, I will be utterly, utterly ruined. I will be struck off the register at White’s.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Mythic — Jae Lynne Davies; tertile=end; p=0.57**
>
> Oh and Nicholas? [TARGET] Do try your very best not to make a mess of things." At the moment, too many questions ran through his mind for him to retort.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Light on Shadow — Cassidy Ryan; tertile=end; p=0.46**
>
> It is always easier to kill a person than to enslave them. [TARGET] Better, many think, to simply wipe the world clean and focus on our next victory.” “ My father and the others will fight.” “

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 277 — Promising to Handle The Lawyer

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** lawyer, attorney, law, lawyers, legal, firm, defense, counsel, appointed, advice
- **KeyBERT:** involved, expect, impatiently, official, warned, begging, afford, stumbled, cost, worrying
- **POS:** official, worrying, member, current, cost, process, worst, experience
- **MMR:** impatiently, presented, worrying, afford, warned, begging, mumbled, process, expect, ended

**BERTopic representative docs**

> 1. take it from your lawyer.” “

> 2. alec was a lawyer.

> 3. he’s a lawyer now.” “

**Stage-08 labeling snippets**

> 1. i’ll talk to the lawyer tomorrow.

> 2. we’ll find a good lawyer to help.

> 3. you can count on me to deal with the legal trouble they’ll cause.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_thin cells CELL_C; 13 examples from 11 books; ±1 context on 13_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Fair Valley Refuge — Lynnette Bonner; tertile=middle; p=0.59**
>
> I don’t know exactly. [TARGET] Just…, when you’ve been a lawman for a bit you get to recognize the look of a con and this somehow feels like one to me.” “ I see.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · The Cougar's Bargain — Holley Trent; tertile=end; p=0.61**
>
> We thought, as I told you, that we were completely penniless and without a friend in the galaxy.” “ [TARGET] Well, except for your fiancé, the future Duke of Barrington,” the lawyer amended. “ Speaking of the future duke, I think I hear him coming now.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Trust — Sarah Ann Walker; tertile=begin; p=0.70**
>
> Is there a reason?" " [TARGET] Um, I watched someone close to me convicted of a minor offense because he couldn't afford a private lawyer. He was defended by a half-ass Public Defender who didn't give a shit about him.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Saving Sebastian — Luna David; tertile=end; p=0.62**
>
> He’d gotten home the next day and started to research. [TARGET] He knew he needed to avoid his parents and their pastor providing their own lawyer, so he found what sounded like a good lawyer online and made an appointment. As he walked out of the law office the next day, he’d retained his own lawyer.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · A Place Called Home — Jo Goodman; tertile=begin; p=0.74**
>
> His fallback position was wry humor. “ [TARGET] You’d think a sharp lawyer like you would know that. Finished.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Natural Evil — Thea Harrison; tertile=end; p=0.36**
>
> What’s relevant is, an area has got to be surveyed before a mine can go into production. [TARGET] It’s important to establish legal boundaries of ownership, especially when you’re talking about gems and precious metals. Those boundaries never include Other lands, so crossover passages have to be mapped and the entrances clearly defined.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · The Set Piece — Catherine Lane; tertile=begin; p=0.59**
>
> I do have a proposition for you. [TARGET] But you need to hear it at our lawyers’ office, and you need to sign a confidential non-disclosure agreement before we go any further.” “ This is getting too weird for me.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · The Two Lords of Wealdhant Manor — Katherine Marlowe; tertile=middle; p=0.47**
>
> Whether Algernon stayed or went, Jasper needed a permanent solution to the threat of the railway. [TARGET] If Algernon went, at least the legal and bureaucratic paperwork that entailed would buy him time. If Algernon stayed... Algernon could not stay.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Sacrifice of Love — Quinn Loftis; tertile=end; p=0.46**
>
> He’s sort of a computer nerd. [TARGET] Working primarily for private investigators, Uncle Jim handles mostly divorce cases, specifically, cheating spouses. He gains access to the alleged cheating spouse’s computer and clones the hard drive, always with the express permission of the suspicious spouse, since it’s usually considered joint property.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Sacrifice of Love — Quinn Loftis; tertile=middle; p=0.34**
>
> She surveyed the room around her and then looked at Decebel. “ [TARGET] If I were you, instead of life insurance, I would invest in counseling. Lots and lots of counseling.” “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Just One Taste — C.J. Ellisson; tertile=end; p=0.40**
>
> My head no longer pounds like it did before, but I prefer the softer light when I want to relax. [TARGET] Mediation has never come easily for me and I need all the help I can get. I walk across the vast room, passing free-weights and stand-alone equipment.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Making Marion: Where's Robin Hood When You Need Him? — Beth  Moran; tertile=begin; p=0.45**
>
> I shall be reporting you to your employer at the first opportunity. [TARGET] And if either my sister or I should suffer from any effects of dehydration, I shall be contacting my lawyer.” She pulled open the door. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Making Marion: Where's Robin Hood When You Need Him? — Beth  Moran; tertile=middle; p=0.77**
>
> And he stayed here in the holidays?” “ [TARGET] He was going to be a lawyer.” The tears were streaming again.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 315 — Claiming Her As His Own

- **Taxonomy:** 4.7 — Jealousy & Possessive Romance Conflict
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** tristan, adrienne, simon, colby, comfortable, damon, crispus, sey, presuaded
- **KeyBERT:** hesitation, sounding, screaming, sentence, lets, nudged, opportunity, ends, indication, practically
- **POS:** indication, utter, tracks, hesitation, ends, sentence, ribs, behavior, actions, practice
- **MMR:** belongs, paced, grumbled, hesitation, nudged, studying, ribs, bothered, behavior, sounding

**BERTopic representative docs**

> 1. besides, i suspect that even if i were cruel enough to hand tristan over, it would gain me little except a lifetime of slavery to george.

> 2. everything he was warmed in tristan’s presence, and short of sounding like one of those cards that sang when opened, wolf didn’t know where to begin telling sey how much tristan seemed to fit into him—and around him.

> 3. one hot afternoon, after a particularly grueling practice in a meadow away from the castle grounds, tristan refreshed himself with water from a nearby stream and returned to sit beside gerard in the shade of an old willow at the top of a rise.

**Stage-08 labeling snippets**

> 1. henri, should any ask, this woman belongs to my cousin tristan—and to me.”

> 2. everything he was warmed in tristan’s presence, and short of sounding like one of those cards that sang when opened, [person] didn’t know where to begin telling sey how much tristan seemed to fit into him—and around him.

> 3. i'll call tristan right after i get off the phone." "

> 4. besides, i suspect that even if i were cruel enough to hand tristan over, it would gain me little except a lifetime of slavery to george.

> 5. everything he was warmed in tristan’s presence, and short of sounding like one of those cards that sang when opened, wolf didn’t know where to begin telling sey how much tristan seemed to fit into him—and around him.

> 6. one hot afternoon, after a particularly grueling practice in a meadow away from the castle grounds, tristan refreshed himself with water from a nearby stream and returned to sit beside gerard in the shade of an old willow at the top of a rise.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Packet representative sentences** (fallback when CELL sample empty)

> 1. But Val walked out on me, remember?” “

> 2. Val’s words slapped at him, forced him to realize a few things he’d rather have ignored.

> 3. Val was your shot at actually having a real life and you let her waltz right out the door.”

> 4. Val looked at him as if he was out of his mind and that’s exactly how Dev felt. “

> 5. Just what Val had suspected.

> 6. Val wondered, just a little embarrassed to think that might be true.

> 7. I mean, Val’s not the enemy.

> 8. Val?”

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

### Topic 351 — Warm Greeting Upon Return

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Current code (LLM):** **S2 — emotional security belonging**

**Four keyword representations** (BERTopic / labeling)

- **Main:** see, nice, good, glad, again, pleasure, you, happy, great, awfully
- **KeyBERT:** greeted, mister, madam, replies, warmth, reminds, reaches
- **POS:** lack, warmth, crowd
- **MMR:** madam, reminds, replies, greeted, winced, reaches, ms, drifted, warmth, crowd

**BERTopic representative docs**

> 1. nice to see you again,” seth said coolly. “

> 2. it was so nice to see you again, lucas, ” she said.

> 3. i am glad that you are back,’ she replies, beaming, and helps me with the luggage. ‘

**Stage-08 labeling snippets**

> 1. thank god you’ve come back—and will you look at me, just in time.”

> 2. it is a pleasure to see you again—so soon, madam. ”

> 3. so i’ll see you there,” he said, feeling upbeat for the first time in a long time. “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 12 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · A Cadence Creek Christmas — Donna Alward; tertile=middle; p=0.67**
>
> And merry Christmas, Taylor. [TARGET] To you and your family, if I don’t see you again.” “ You, too.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · A penny's worth of affection — rosesarered27; tertile=end; p=0.76**
>
> Your father informed me that you had gone for a walk. [TARGET] I am glad I waited though, it is such a pleasure to see you again."

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Dreamlike State — Macy Farmer; tertile=begin; p=0.64**
>
> It gets dark here really quick.” [TARGET] I gazed into his eyes, thanked him again for earlier and for walking me back to my cabin now. “ It’s my pleasure.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · True To You — Liwen Y. Ho; tertile=middle; p=0.63**
>
> Ben laughed. “ [TARGET] I was talking about seeing you here.” “ I know.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Gallant Officer, Forbidden Lady — Diane Gaston; tertile=middle; p=0.72**
>
> She smiled at Nancy. ‘ [TARGET] It is a pleasure to see you again, Miss Vernon.’ Nancy curtsied. ‘

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Courageous — Diana Palmer; tertile=end; p=0.69**
>
> Thanks,” one of the younger students said, with a flush. “ [TARGET] Nice to have you back, General,” she added. “ It’s been difficult since the coup.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Domestic Relations — K-lee Klein; tertile=end; p=0.62**
>
> Well, I'm gonna take off. [TARGET] I'm sure I'll see you again, Josh. Talk to you in a couple days, Riley?"

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · Just One Kiss — Amelia Whitmore; tertile=begin; p=0.62**
>
> The girl, who I’m now assuming is Brayden’s younger sister, steps forward to hug him. “ [TARGET] I knew you were going to be here, but it’s still a surprise to see you,” he says with a large smile. I’ve got a smile on my face, but I’m feeling a little put off by what she said just a few seconds before.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Cry No More — Linda Howard; tertile=begin; p=0.51**
>
> Since he probably already had her home phone and address, thanks to her slipup of using her real name instead of her business name, Milla couldn’t see how giving him her cell phone number could hurt. “ [TARGET] I’ll give it to him when I see him again.” “ See who?”

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · Cry No More — Linda Howard; tertile=end; p=0.60**
>
> Now get out of my house. [TARGET] I never want to see you again.” Because he was Diaz, he didn’t stand there arguing his side.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Sanctuary — Bethany Shaw; tertile=middle; p=0.50**
>
> Tess sighed wistfully, closing her eyes as she let the memories wash over her. [TARGET] It was nice to laugh again, to remember the good times. As long as she held onto those, her family would never truly be lost.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · Sanctuary — Bethany Shaw; tertile=begin; p=0.56**
>
> Eden beamed as she approached, placing a hand on Tess’ shoulder. “ [TARGET] I’m glad to see you’re okay. How do you feel?”

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Cathryn — Shannon Waverly; tertile=begin; p=0.52**
>
> Not from you. [TARGET] I’ll see you as often as I can,” he said, only making matters worse by reminding the children he wouldn’t be seeing them on a normal basis. “ But who’ll take me to Scouts?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Cathryn — Shannon Waverly; tertile=middle; p=0.37**
>
> One Labor Day when she was a young teenager, her fun-loving friend Amber had suggested walking out onto the harbor’s breakwater and mooning the last official ferry of summer. [TARGET] Amber had seen it as a splendid way to say goodbye to the hoards of tourists who crowded Harmony during that season. Her friends and classmates had agreed and all had participated in and thoroughly enjoyed the prank.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_015 · The Bit In Between — Claire Varley; tertile=end; p=0.50**
>
> For getting so caught up in me. [TARGET] Seeing you here made me think about things, about us. I mean, what are the chances of us turning up on the same Pacific island?’

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_015 · The Bit In Between — Claire Varley; tertile=end; p=0.66**
>
> Hi,’ she said and shifted the bag of groceries protectively in front of her. ‘ [TARGET] I’m glad I saw you,’ Ed said, panting slightly. ‘ I wanted to say something.’ ‘

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S2`)
- Decision: KEEP / REMOVE

---

### Topic 358 — Reassuring Squeeze of The Hand

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Current code (LLM):** **S1 — emotional security reassurance**

**Four keyword representations** (BERTopic / labeling)

- **Main:** squeezed, squeeze, hand, gave, squeezing, shoulder, gently, arm, fingers, reassuring
- **KeyBERT:** squeeze, squeezed, gripped, tightening, reassuring, trembling, calming, pouring, landed, notes
- **POS:** squeeze, reassuring, notes, trembling, loose, waist
- **MMR:** squeeze, calming, pouring, draped, tightening, lingering, notes, trembling, squeezed, gripped

**BERTopic representative docs**

> 1. she squeezed reese's hand. "

> 2. bennie—” she squeezed his hand. “

> 3. he squeezed her hand. “

**Stage-08 labeling snippets**

> 1. she took bronte's hand and gave it a reassuring squeeze. "

> 2. ted reached for caroline's hands and smiled at her reassuring squeeze. "

> 3. they'll ask,” he murmured, and gave her waist a reassuring squeeze.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 13 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · The Renovated Heart — Jean C. Joachim; tertile=middle; p=0.79**
>
> He reached behind her and snapped open her bra, then returned to massaging her flesh, stroking the peak gently with his thumb, his breath growing ragged. [TARGET] His other hand slid down her back, the fingers closed around her bottom and squeezed. Kit arched into him, wanting more, her desire spiraling quickly when she felt him get hard.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Ashes Ashes — Julie Coulter Bellon; tertile=middle; p=0.80**
>
> Ready.” [TARGET] Her voice sounded small and unsure, so he gave her hands a squeeze. “ Hang on.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Perfect Game — Collette West; tertile=end; p=0.82**
>
> I promise you I’ll never fuck up again.” [TARGET] I reached for her hands, squeezing them as I pleaded. “ I know my promises mean nothing to you right now, but I’ll make them mean something again.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Win, Love, or Draw — Crystal L. Barnes; tertile=middle; p=0.88**
>
> Oh, honey, I’m so glad to see you.” [TARGET] She squeezed him tight, then cupped his face in her hands. “ Let me look at you.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Lust & Vamp — Joyee Flynn; tertile=end; p=0.58**
>
> I asked, smirking at Sark. " [TARGET] Please, yes please," Reid begged, thrusting his fingers in himself harder as he added a third. I gave Sark a nod, and he went to my mate as well.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · I Dream of Genies — Judi Fennell; tertile=middle; p=0.79**
>
> Trust me.” [TARGET] She smiled when he squeezed her shoulder. Smiled even more when he whispered, “I do trust you, Eden.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Dangerous Alpha — Anitra Lynn McLeod; tertile=end; p=0.69**
>
> When Maxwell took his hand, Quinn practically burst into tears of joy. [TARGET] He couldn’t speak, but he squeezed Maxwell’s hand and was ecstatic when he squeezed back. “ By your leave?”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Dark Isle — Shannon Mayer; tertile=end; p=0.62**
>
> You’re better at this than I am.” [TARGET] Ashling gripped my hand, the flow of her Healing abilities washing through me. “ No, Quinn, you were always the strong one, you just didn’t see it.”

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · The World in Reverse — Latrivia S. Nelson; tertile=end; p=0.68**
>
> She could see him shooting back at the men who had come to their home to take their lives. [TARGET] Fingers trembling, she clasped them together and said another prayer. Thank you, Lord, for your deliverance , she mumbled.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Get Off — KouriArashi; tertile=middle; p=0.46**
>
> The ship had sent out its death knell, the last thing this type of spacecraft was programmed to do before all its systems failed. [TARGET] Shahanna reached with an enfeebled hand to her side pouch, fumbled for a stimulant and a pain depressor. Clumsily, she jabbed the drugs into her arm and then, gasping at the discomfort even that slight motion caused, lay back.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Get Off — KouriArashi; tertile=middle; p=0.81**
>
> She pointed, furious that she obeyed him so instantly, and that she couldn't control the chattering of her teeth or the trembling of her body. [TARGET] He reached for her hand, relaxing his grip a little at her involuntary gasp of pain. Replace "grubby paws" with "highgravity paws," she told herself in an effort to keep up her spirits as she stepped in front of him. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Get Off — KouriArashi; tertile=middle; p=0.82**
>
> There's no other company I'd rather keep, you know." [TARGET] She gently returned the pressure of his hand. " But I know you want children.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · You Sexy Thing! — Tori Carrington; tertile=end; p=0.55**
>
> Remember?" " [TARGET] But my parents—" "Are fine," he interrupted, groaning when she curved her fingers as far as she could around his hardening shaft. " Look."

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · You Sexy Thing! — Tori Carrington; tertile=middle; p=0.70**
>
> she asked herself, adopting her mother's tone. [TARGET] She wrapped her fingers around the door handle. " That you want to be his beck-and-call girl?"

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_002 · Rescuing Rose — Isabel Wolff; tertile=middle; p=0.70**
>
> Andrew knows so many people,’ she added reassuringly, ‘I’ll ask him to find someone nice.’ [TARGET] Bea groaned then lifted her right hand to her brow. ‘ Oh God,’ she said, ‘I’m miserable and I’m absolutely pissed —we’d better go.’

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Yours, Mine, and Ours — MaryJanice Davidson; tertile=middle; p=0.48**
>
> I never looked back. [TARGET] D’you want to squeeze off a few?” She extended the unloaded gun to me, butt first with the safety on.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S1`)
- Decision: KEEP / REMOVE

---

## 2. Material / economic provision (S8–S9)

_5 topics_

### Topic 17 — Discussing Rooms and Privacy

- **Taxonomy:** 8.1 — Domestic Spaces & Routines
- **Current code (LLM):** **S9 — material provision housing**

**Four keyword representations** (BERTopic / labeling)

- **Main:** house, hotel, room, apartment, bedroom, rent, upstairs, home, bedrooms, living
- **KeyBERT:** porch, lets, ceiling, address, assume, remarked, occupied, remark, folks, ok
- **POS:** secure, concept, privacy, separate, remark, address, contrast, smaller, sucks, areas
- **MMR:** belongs, visited, suggest, privacy, address, built, remarked, areas, guarantee, intend

**BERTopic representative docs**

> 1. we need to get to the hotel,” she said.

> 2. i have a nice apartment upstairs.

> 3. you can stay at my apartment if you like, or if you’d rather, i’ll put you up in a hotel.” “

**Stage-08 labeling snippets**

> 1. i’ll just go back to the dorms.”

> 2. i think we’ll go back upstairs and discuss that – don’t you?”

> 3. but upstairs—” “we’ll add two more bedrooms and another bath.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · Shaken — Alyne Roberts; tertile=end; p=0.60**
>
> It wasn't even dinnertime yet and the day had me exhausted. [TARGET] After leaving Logan's, I went into town to avoid going back to the apartment and answer for where I was the night before. Being that our town was closely knit, everyone heard of my dad's passing.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · A Problematic Love — Rebecca Rohman; tertile=begin; p=0.69**
>
> I can’t seem to stop thinking about the fact that he and I will be sleeping under the same roof. [TARGET] Thank God, the master bedroom is downstairs. “ Feel free to choose the room you want.” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · A Frost of Cares — Amy Rae Durreson; tertile=middle; p=0.65**
>
> Out in the foyer, I looked at the stairs. “ [TARGET] We should probably get what we left in my room.” “ Luke.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · The Sound of You — Annie Hughes; tertile=end; p=0.64**
>
> You better had be, or I'm coming to get you," she sniffs, leaning into Ryan as he comes back to join us. " [TARGET] I'll have a room ready for you when you come back because like hell I'm gonna let you live with anyone else." " You only want me for my cooking," I laugh. "

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Hide in Plain Sight — Marta Perry; tertile=begin; p=0.62**
>
> Come along in. [TARGET] We have the back stairway and the rooms on this side, so that’ll give us our privacy. You’ll be surprised at how well this is working out.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Fall Girl — Toni Jordan; tertile=end; p=0.71**
>
> The staircase is a grand one, carved banisters, ornate gold rods along each rise holding the carpet in place. [TARGET] First I must find the room. The first floor landing leads to a wide corridor lined with paintings in intricate gold frames.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Sold! — Etienne; tertile=end; p=0.69**
>
> Let’s go, Clancey, if you and the guys are through eating.” [TARGET] When we were back in the living room of our suite, I said, “Refresh my memory, Clancey, is there a decent hotel near your parents’ house?” “ Not really.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · Hers for the Holidays — Samantha Hunter; tertile=middle; p=0.61**
>
> Good girl,” he said, kissing her again as he slung an arm around her and headed toward the door. “ [TARGET] Um, Ely, the bedroom is that way,” she said, gesturing at the stairs. “ Not that a bed is necessary,” she added provocatively.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Steal Away — Amber Green; tertile=begin; p=0.55**
>
> I just felt so lonely. [TARGET] What was the point of a huge house with nobody to live in it? A huge bed with nobody to sleep in it?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · The Enchanted — Genevra Thorne; tertile=middle; p=0.56**
>
> She smiled at the thick chairs and heavy wooden furniture. [TARGET] This was his room, and she liked it even more than the first time she had sneaked into it. She passed the rowan tapestry on her way to the bed and waved at it, half expecting it to wave back.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Pansies — Alexis  Hall; tertile=begin; p=0.64**
>
> Take me somewhere .” “ [TARGET] I’ve got a room at the — ” “I don’t care, take me somewhere .” This was another terrible idea.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Ghost Wolf — Heather Long; tertile=begin; p=0.59**
>
> A reminder that the beautiful woman— girl, she’s still a teenager— was also a fit and capable wolf. “ [TARGET] Since I’m here, why don’t I go apartment hunting with you? Kill two birds with one stone.”

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Cupid's Pursuit — Patrick  Shanahan; tertile=end; p=0.57**
>
> It was a large house, several rooms leading off the main hall with a staircase situated to one side that led to the upper floor. [TARGET] I didn’t feel comfortable wandering around a stranger’s home by myself, and after a cursory glance around the lower floor, I returned to the sitting room. The most striking feature in the room was the enormous Christmas tree taking pride of place in one corner, its fallen pine needles forming a carpet-like circle at its base.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Vampire Betrayed — Rachel Carrington; tertile=end; p=0.47**
>
> Wealth whispered around every corner, hung from every chandelier, and beckoned with the glistening promise of perfection. [TARGET] With over 11,000 square feet of living space— in case they decided to stay a while as Joaquin explained—the suite boasted everything from a private spa to a cinema. Ariana walked from room to room, inspecting her surroundings.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Fiancé for Hire — S.K. Weathers; tertile=middle; p=0.58**
>
> He shrugged, which made her smile. “ [TARGET] Here’s you,” she said, pointing into a small bedroom. There was a double bed, a nightstand, small dresser, and a closet.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_015 · Live Fast, Die Young — Vanessa Barneveld; tertile=middle; p=0.61**
>
> I do my best to sound super enthusiastic about the super juice. [TARGET] As I follow her to the rear of the house, I peek left and right into the dining and living rooms. Alex and his mom recently moved, so now they’re only three blocks from my house instead of four.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S9`)
- Decision: KEEP / REMOVE

---

### Topic 112 — Desperate Need For A Job

- **Taxonomy:** 6.4 — Economic Precarity, Security & Dependency
- **Current code (LLM):** **S8 — material provision money**

**Four keyword representations** (BERTopic / labeling)

- **Main:** job, business, company, jobs, work, do, working, boss, living, hire
- **KeyBERT:** opportunity, reassuring, dealing
- **POS:** addition, testing, regular, pathetic, impressive, related, decent, larger, actual, anxiety
- **MMR:** addition, reassuring, testing, pretending, anxiety, task, distracted, spending, ability, ms

**BERTopic representative docs**

> 1. give me a job." "

> 2. there are not many good jobs around in my business.”

> 3. i'll tell everyone in the business that you were unprofessional, incompetent, that you weren't up to the job.

**Stage-08 labeling snippets**

> 1. i’ve never worked in such a beautiful place and i want this job so badly.”

> 2. i've lost my job, and i'm not going to find another one in elliot or prestonsburg or probably even in auburn.

> 3. you’ve got a hell of a career ahead of you.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Secret Agent Secretary — Melissa Cutler; tertile=begin; p=0.62**
>
> The realization scared her to her core. “ [TARGET] Maybe I should stick to being a secretary.” Against her forehead, she felt the rumble of his chuckle.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Let Me Love You Again — Anna DeStefano; tertile=middle; p=0.61**
>
> My mother’s got a houseful of kids and me— me —as her best fallback plan to keep Family Services satisfied until we know how things are going to shake out for the toddler my parents just signed on to foster. [TARGET] I have no experience with kids, a full-time job demanding my attention all over the globe— if I don’t lose every potential client I have lined up because I can’t schedule a damn thing with every minute of my day up in the air the way it is right now. And on top of it all, I’m dealing with maybe having a child of my own to be responsible for.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Of Love and Distance — Divya Jyoti Randev; tertile=middle; p=0.44**
>
> Then I’ll thank you twice for helping. [TARGET] Not many people can handle this kind of work, and even fewer would sacrifice their health for it. Will I—will we, that is—see you next time?” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · White Christmas — Cathy Bramley; tertile=middle; p=0.58**
>
> Well,’ he said, patting his red jacket, ‘gives me time to settle in, you know, get into character. [TARGET] Besides, if no one knows where I am, they can’t give me any jobs to do, can they?’ He chuckled. ‘

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Breathing — Cheryl Renee Herbsman; tertile=middle; p=0.67**
>
> I have spent the entire day puking my guts out after being poisoned by the hospital, in case you forgot. “ [TARGET] He offered me a job in the office, you know, filing, typing, secretarial work.” “ You ain’t qualified for that.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Black Ties and Lullabies — Jane Graves; tertile=middle; p=0.68**
>
> Isn’t that what a manager is supposed to do?” “ [TARGET] If I wanted to actually work, I’d go get a real job.” She picked up the remote. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · Below the Belt — Jeanette Murray; tertile=end; p=0.67**
>
> He’s in pain, hurting, potentially injured, and won’t tell me about it. [TARGET] Won’t let me do my job.” “ Oh.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · Becoming Daddy's Girl — Normandie Alleman; tertile=middle; p=0.62**
>
> Yep. [TARGET] I guess that’s a blessing, though it’s tough because since I’m not working I’m not getting paid.” That sucked.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Werewolf Descent — Elizabeth J. Kolodziej; tertile=begin; p=0.41**
>
> Then he just stood there for a moment, feeling the restless, rising urge of his blood and wondering what to do with himself. [TARGET] He worked as a handyman, doing odd jobs and chores for people in the town below and in the other cabins, but he always took care not to take on any assignment that would require him to work on days like these. He could go hunting…but it might stir up his blood lust to a feverish height, and he didn’t want to come home with a torn-apart deer he didn’t even remember killing.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_004 · Werewolf Descent — Elizabeth J. Kolodziej; tertile=middle; p=0.54**
>
> I don’t want a safe, steady job,” Leo told him, trying hard to keep his voice level. “ [TARGET] I don’t want to work at the same lab for forty years until they retire me. I want to paint, and I want to make a living as a painter.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Heart of a Highland Warrior — Anita Clenney; tertile=begin; p=0.55**
>
> Odd question. “ [TARGET] Everyone has to work unless they’re already rich.” Her job just wasn’t typical.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · The Billionaire's Voice — J.S. Scott; tertile=begin; p=0.65**
>
> Honey, you don’t have to serve coffee. [TARGET] You aren’t an employee anymore.” Helen shot her a grin, one so similar to Simon’s that Kara was momentarily distracted.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · The Lily and the Sword — Sara Bennett; tertile=begin; p=0.40**
>
> He is a great warrior, ’tis true, but he is also a wise and just lord. [TARGET] I cannot speak for others, but I know that my Olaf is well paid for his work, and has a dry, comfortable place to live and sleep, and that our table groans with food. At Crevitch, the people do not talk of his lack of heart.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Callum of Drakkar Coven — Leigh Jarrett; tertile=begin; p=0.45**
>
> There are plenty of men working in the castle that have been here for decades. [TARGET] I've been here for nine years already myself, and I spent five years before that working for Drakkar." " Do they feed on you?"

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Changes — Pamela Nowak; tertile=begin; p=0.44**
>
> They can sense something’s different.” “ [TARGET] You really should become a shrink.” He ignored her. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_016 · Flawless Danger — Rachel Woods; tertile=begin; p=0.52**
>
> As if liquor could erase the terror and trauma of waking up to a knife in her face that could have ended up in her back instead of the doorframe. “ [TARGET] How did you get into this business of drugging men and stealing from them?” Ben asked.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S8`)
- Decision: KEEP / REMOVE

---

### Topic 191 — Working to Pay The Bills

- **Taxonomy:** 6.2 — Work & Professional Identity
- **Current code (LLM):** **S8 — material provision money**

**Four keyword representations** (BERTopic / labeling)

- **Main:** job, money, pay, bills, business, paid, fund, she, career, work
- **KeyBERT:** paying, paid, afford, circumstances, provide, assistant, dr, earned, claims, television
- **POS:** value, activities, areas, partners, exchange, television, decent, assistant, previous
- **MMR:** value, claims, earned, activities, partners, exchange, afford, fishing, bounced, assistant

**BERTopic representative docs**

> 1. annabelle had been perfect for the new job, not just because of her background with her father's company and her business degree, but because she actually liked roughnecks.

> 2. for her own convenience, petra had opened a household account in both their names, and paid in sufficient money to cover her bills, so that dixie could easily pay them for her.

> 3. she’d been looking for a week, but each time she checked the job board at the student employment center, there were either no jobs she was qualified for, or all the little fringe thingies with the contact phone number were all torn off and by the time she called, the job had been filled.

**Stage-08 labeling snippets**

> 1. but in all honesty, she needed every penny of the income she earned, so even if she had known, she probably wouldn’t have paid the premiums.

> 2. her job as an accountant for h & h lumber wasn't exactly exhilarating, but it paid the bills, and they treated her kindly there.

> 3. once the television shows pay her major loot, she'll retire from her day job and write from home.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · At Home In Stone Creek — Linda Lael Miller; tertile=end; p=0.57**
>
> Initially, flushed with the success of helping Ashley steer the bed-and- breakfast through the Valentine’s Day rush, Melissa had seemed to be wavering a little on the subject of moving away. [TARGET] After all, she liked her job at the small, local firm where she’d worked since graduating from law school, but then Dan Guthrie had suddenly eloped with Holly the Waitress. Now nothing would move Melissa to stay.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Love Finds You in Golden New Mexico — Lena Nelson Dooley; tertile=end; p=0.70**
>
> All of this meant she had to make some important decisions. [TARGET] Having a lot of money at her disposal would allow her to do good for other people. People had needs in Boston, and many in and near Golden could use a helping hand.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Lessons From A Younger Lover — Zuri Day; tertile=begin; p=0.63**
>
> She’d done her homework, and knew that aside from three Hispanics and one Asian, there were no other minorities besides Adam on the staff at Sienna Elementary. [TARGET] That, along with her credentials, would have to heavily favor her getting the job. The only potential obstacle, at this point, seemed to be sitting in front of her. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Asking for Trouble — Anna J. Stewart; tertile=begin; p=0.67**
>
> Instead, she focused on donning the mask of her professional self: the woman who didn’t care that men skimmed their uninterested eyes over her size fourteen figure before moving on to whatever svelte, posh, polished socialite stood nearby. [TARGET] She was Morgan Tremayne and she needed to raise a truckload of cash or risk a financial scandal that could destroy her family. When she noticed Gage had shortened his stride to match her unsteady one, Morgan wished she could have pulled off tennis shoes under the gown.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Baby Bonanza — Maureen Child; tertile=middle; p=0.64**
>
> Maxie was a medical transcriber. [TARGET] She worked out of her home, which was a big bonus for those times when Jenna needed a babysitter fast. Like now. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Sex By The Numbers — Marie Donovan; tertile=end; p=0.65**
>
> Bob from accounting is clean, and so is Glenn. [TARGET] She’s been here long enough to learn everything, she has an accounting background, and she has the motive.” “ We’ll see.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Deeper — Megan Hart; tertile=begin; p=0.65**
>
> Regret and a touch of jealousy surfaced when she considered the memories she had missed out on and that Noah had obviously shared with her family. [TARGET] When she started with the CIA, she hadn’t anticipated having to sacrifice so much of her private life in order to do her job well. But of course, it was more than just a job.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · The Kings of Charleston — Kat H. Clayton; tertile=end; p=0.69**
>
> From himself, it seemed. [TARGET] She couldn’t let him throw away everything he’d worked for, just for her. The tension in the room felt like a rubber band about to snap.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · End of the Innocence — John  Goode; tertile=begin; p=0.46**
>
> At home, my mom was still in her “I can be sober” phase, because she thought of herself as my own little civil rights activist since the school board meeting, and activist parents don’t drink. [TARGET] She was doing exactly what she had done every other time—like after she had found Jesus or Buddha and, once, Tony Robbins after watching too many late night infomercials. Trying to love my mom was like trying to have a lasting relationship with Charlie from Flowers for Algernon .

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · Compromising — C.C.   Brown; tertile=begin; p=0.55**
>
> I was ambushed by Castillo as I was about to enter the Admin office. [TARGET] Not only was pushing papers not up my alley, but working in close proximity to her was just another reason to hate life at the moment. I couldn ’ t be sure that she wasn ’ t the loose lips who’d spilled the beans to O ’ Hara. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · The Vampire's Pet — V.R. Cumming; tertile=begin; p=0.61**
>
> I pinched the bridge of my nose and squeezed my eyes shut, trying to push that memory away so I could concentrate on studying. [TARGET] I hadn’t cashed the checks she’d given me yet, mostly because I was still thinking the whole thing over, which meant I still had to fit school in around two jobs. It all boiled down to whether or not I was willing to commit my life to Elizabet and become her blood slave.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · In the Distance — Nikka Michaels; tertile=middle; p=0.56**
>
> My mom, Margaret Windsor Pratt, was the daughter of a prominent investment broker. [TARGET] She had grown up in New York’s elite society, but had always worked hard not to let her family’s money and status make her one of the obnoxious socialites she’d grown up with. They’d met at a social gala, talked all night and into the morning, both freely admitting to this day it had been love at first sight.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · Stay With Me — Evelyn Shepherd; tertile=end; p=0.53**
>
> She spends her time writing, but when she isn’t working on her next novel she’s either reading or spoiling her nieces and nephew. [TARGET] She is currently working hard at her next novel. Links to reach the author: Web site: http://www.evelynshepherd.com Blog: http://singleauthorseeks.blogspot.com Table of Contents Dedication Chapter One Chapter Two Chapter Three Chapter Four Chapter Five Chapter Six Epilogue Loose Id Titles by Evelyn Shepherd Evelyn Shepherd

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · Broken — J.K.  Lewis; tertile=begin; p=0.45**
>
> After the tour we had lunch and she told me a little about Drake from when he was a kid, she said that when they were younger he was very overprotective of his family, he still is, but now it's gotten worst. [TARGET] Apparently when he became CEO of the company he bought a house for his parents in Rome, claiming that he wanted them to have a nice retirement life but she thinks it's either because he wants them closer to her to save himself from all the stress about worrying about his parents or that he doesn't want any of his family living in America for some strange reason. After Sky left I walked back up stairs to the bedroom to shower, so I could ask one of the drivers to take me to the mall to get a phone before Drake comes home, hopefully Drake won't have me here like a complete prisoner without a phone.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_013 · Broken — J.K.  Lewis; tertile=begin; p=0.58**
>
> Ava and I both worked at two different night clubs, I always refused to work in the same club as Ava because she does more drinking and partying on her shift than when we go out to have fun. [TARGET] The only reason she still has her job is because she has sex with the club owner, and the only reason she's still there is because apparently he's a good lay, I'm sorry but I rather work in a club without Ava, so she wouldn’t try to get me to party with her every night and then sleep with the boss to keep from getting fired. " You know why I quit, you just don't agree with me, just because Brian is, and I quote, 'Sex on legs & Drop your panties kind of guy' doesn't mean that if he calls me to an important "meeting" an when I get there he wants me to bend over the table so he can fuck me in my ass, in exchange for a promotion doesn't mean that I'll be ok with that.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_015 · Sharing a Pond — Alex Whitehall; tertile=end; p=0.42**
>
> Search. [TARGET] That eventually led him to some websites, some places not far from work, some that he could actually afford. Maybe.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S8`)
- Decision: KEEP / REMOVE

---

### Topic 22 — Negotiating Payment and Debts

- **Taxonomy:** 6.1b — Generic Business / Institutional Negotiation
- **Current code (LLM):** **S8 — material provision money**

**Four keyword representations** (BERTopic / labeling)

- **Main:** money, pay, owe, contract, cash, dollars, bank, debt, afford, paid
- **KeyBERT:** paying, provide, afford, paid, cost, buying, begging, spending, earned, behalf
- **POS:** insulted, potential, century, percent, value, dislike, unlikely, increase, behalf, decent
- **MMR:** afford, insulted, earned, potential, paid, century, percent, dislike, dramatically, increase

**BERTopic representative docs**

> 1. and it only cost two thousand dollars.

> 2. the money has been withdrawn from your bank account.”

> 3. and you owe me seventy dollars.”

**Stage-08 labeling snippets**

> 1. but you'll be paying us less than you'd be paying at the mercantile, and we'll deliver them right to your door each morning." "

> 2. you’ll get that after i’ve paid a bill or two at tattersall’s,” [person] said. “

> 3. and as soon as i finish that computer program for ted and get paid, i’ll redeem it.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Hidden Deceit — Nicole Colville; tertile=begin; p=0.67**
>
> He's doing this for Scot, isn’t he? [TARGET] Me and you being here together…My God, if he doesn’t want the money, then…..No.” “ Jamie, Scot won't believe you’ve run away with me , and even if he does, he’ll hunt us down.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Vanished — Carter Quinn; tertile=begin; p=0.45**
>
> Each on its own would fetch in the mid to high nine figures. [TARGET] But once those sales were realized, the money would go right into an ever-quickening whirlpool of loss and debt. Trevor leaned back in his chair, the disbelief written across his face like a bold marker, and considered that for a moment. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Broken A M/M Modern Retelling of Beauty & the Beast — X. Aratare; tertile=begin; p=0.63**
>
> He’ll even get paid , which is so very rare these days. [TARGET] His payment will, of course, be the chance for your family to be rich and powerful again.” “ I don’t understand.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · In at the Deep End — Penelope Janu; tertile=middle; p=0.57**
>
> You’re going back to sea in a few weeks, and it’ll be mid-September by the time you get back. [TARGET] And I won’t be able to go to the pool for a few days after that because a mining magnate has paid $10 000 for me.’ ‘ What?’ ‘

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_001 · Wanted: One Scoundrel — Jenny Schwartz; tertile=end; p=0.57**
>
> Cut your losses. [TARGET] I’ll give you a thousand pounds to do just that.” It took Jed a moment to realize he was being paid off.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Transplanting Holly Oakwood — Di Jones; tertile=begin; p=0.64**
>
> In the meantime Warren spoils me. [TARGET] I couldn’t afford half of what I have on my salary.” “ Sounds like you don’t really love him.” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Burn It Up — Cara McKenna; tertile=end; p=0.69**
>
> One night’s work, thirty thousand bucks. [TARGET] There’s a lot of good I can do with that kind of money.” “ But the money itself is bad ,” she spat, catching how hysterical she now sounded, and not caring. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · Becoming Daddy's Girl — Normandie Alleman; tertile=end; p=0.61**
>
> He opened the box to show her the small diamond ring. “ [TARGET] It’s not big, but you know I’ve got some financial issues.” He smiled. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · Honored Vow — Mary Calmes; tertile=middle; p=0.44**
>
> I want my freedom.” “ [TARGET] And so because you want to be free of the semel-aten, the price is to help him here at the sepat and try and tempt any of the mates of the yareahs you see here beside me, is that it?” Her eyes were hard as her chin snapped up. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Checked Again — Jennifer Jamelli; tertile=begin; p=0.59**
>
> The Beatles are back, now with “Here Comes the Sun . ” } [TARGET] He waves over the waitress, asks for our bill, and promptly gives her some cash to cover it. Then he motions for me to go first, for me to start to walk upstairs and out of the restaurant.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Stepbrother With Benefits 7 — Mia Clark; tertile=end; p=0.42**
>
> I wanted to let you know, so you can put a stop to it, but also to tell you that I'll gladly erase the evidence I have for a small fee. [TARGET] Please don't think of this as bribery, but as a gesture of good will. Maybe $10,000 sounds good?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · The Baller — Vi Keeland; tertile=end; p=0.49**
>
> I tossed a few in my basket, along with a handful of trading card packages. [TARGET] By the time the cashier got to me, my stall had cost me thirty-three dollars. The empty elevator made up for lost time.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Destined to Play — Indigo Bloome; tertile=end; p=0.60**
>
> I need to know you are getting the right fluids and we only have one more test to complete, then it’s precautionary. [TARGET] I can’t afford to risk anything when it comes to you.’ My head spins with his words. ‘

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_004 · Ripples Along the Shore — Mona Hodgson; tertile=middle; p=0.50**
>
> You should come to the meeting here tonight at 6:30. [TARGET] I’ll have the contracts for signing up and a supply list for every family.” Garrett raked his hair. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Secret for a Song — S.K. Falls; tertile=begin; p=0.52**
>
> They’ve paid for family members’ hotel rooms in the past, when people had to be hospitalized in a different city. [TARGET] They pick up the bill for stuff like that all the time. And they’re totally against this plan.”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · Ely Jesse and Robin's Guide to Asexuality — R.J. Seeley; tertile=middle; p=0.46**
>
> He said and I looked up, frowning at the statement. “ [TARGET] That equals five thousand, six hundred, fifty two pounds and sixteen pence.” He said so I looked at Mum who was looking probably as shocked as I was. “

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S8`)
- Decision: KEEP / REMOVE

---

### Topic 174 — Ranch Life and Falling in Love

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Current code (LLM):** **S9 — material provision housing**

**Four keyword representations** (BERTopic / labeling)

- **Main:** ranch, farm, cattle, cows, cow, farmer, rancher, ranches, land, pa
- **KeyBERT:** feeding, experience, porch, bo, folks, popped, owned, areas, surrounded, nearest
- **POS:** areas, regular, suggestion, foreign, repeat, nearest, equipment, folks, sinking, larger
- **MMR:** belongs, guarded, areas, guarantee, owned, described, nearest, equipment, sinking, provide

**BERTopic representative docs**

> 1. at the ranch?” “

> 2. i can rebuild this ranch.

> 3. it meant i'd be on a farm and i already knew i liked being on a ranch.

**Stage-08 labeling snippets**

> 1. i’ve seen your willy on numerous occasions on the ranch.

> 2. the ranch is doing good, and i’ve fallen in love.

> 3. i’d take you there, but i imagine you’ve already seen enough cattle to last you a lifetime.”

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_thin cells CELL_C, CELL_D; 12 examples from 12 books; ±1 context on 12_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Gracie's Touch — S.E. Smith; tertile=end; p=0.64**
>
> While Indy’s brothers left as soon as they were old enough to live elsewhere, Indy never planned on leaving. [TARGET] She loved every aspect of ranch life from the cattle, to the horses, to the old cowpunchers that came and went each year. “ Indy, accept it.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_014 · Protector for Hire — Tawna Fenske; tertile=begin; p=0.49**
>
> I wasn’t suggesting⁠—” “There’s a town about an hour from here. [TARGET] Lotsa lonely female ski instructors and raft guides and ranch hands end up there to grab a drink or meet people.” “ And you’re one of the people they meet?” “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Blood and Sorcery — Ann Gimpel; tertile=middle; p=0.66**
>
> The only reason to remain prone would be if he was asleep. [TARGET] Since that wasn’t happening, he was better off working at the myriad tasks that kept the ranch running smoothly. Ranching and farming were nothing if not hard work.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Lone Star Joy — Kathleen Ball; tertile=end; p=0.73**
>
> You're here now, that's all that matters. [TARGET] The ranch is yours now, and I just know you can turn it around." Stetson frowned. "

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · The Surrogate — Ann Somerville; tertile=middle; p=0.47**
>
> Their home had been a dower house on the edge of one of the larger farms, a couple of miles from the city. [TARGET] When the resident died, the farmer, needing the money, had been glad to sell it off with some land to a couple of wealthy Gidinians in need of solitude and a place away from the bustle of the town. Seve had loved it from the moment he’d seen it, and for him, it was all he needed, though Jaime of course had work which took him into the city itself.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Blue Line — Kim Henkel; tertile=begin; p=0.47**
>
> He hated it, it always made the room smell of cabbage. [TARGET] Even that was preferable to the dried dung of the animals that most people in the castle burned if they were lucky enough to gather it before their neighbors. " Why not?"

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Swift Runs the Heart — Mary Brock Jones; tertile=begin; p=0.41**
>
> Aunt Shonagh would have been horrified at her behaviour, but Geraldine had grown up with the whalers and their children. [TARGET] Her parents had begun life in the colony working for Johnny Jones, the earliest farmer in this part of the colony, and their only other neighbours had been from the nearby whaling settlement. The whaling families, the rough men and their self-proclaimed wives and children, made up the world of her childhood and were still the only people apart from her parents she had ever trusted.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · The Farmer Takes a Wife — Genevieve Turner; tertile=middle; p=0.61**
>
> Farming’s a hard life.” “ [TARGET] It is, but I come from a long line of farmers, and I’ve got big plans for my place.” If they were worried about him being a farmer—well, he’d show them that if there was anything he knew, it was farming. “

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Darkness Deserved — Jessica Spoon; tertile=begin; p=0.47**
>
> Finally Avery has enough of his silence. “ [TARGET] So Breccan, how’s that restaurant of yours down on Hickory doing?” “ It’s doing quite well actually.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_012 · Ink Slapped — A.M.  Jones; tertile=begin; p=0.43**
>
> That’s why I want it to be him and not me. [TARGET] Grass and weeds grow thick in the dense junkyard since I can’t afford anyone to take care of it. “ For one, you don’t have to crawl underneath it this time.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · Micah — Joyee Flynn; tertile=end; p=0.50**
>
> Currently Joyee lives with her dog, Marius, named after a vampire from Ann Rice’s Interview with the Vampire series. [TARGET] She dreams of one day living out in Montana, enough land to have a few horses, and find a couple of cowboys of her own. A lover of men, Joyee’s all about them in any form in her books.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Biggest Flirts — Jennifer Echols; tertile=begin; p=0.48**
>
> Great food. [TARGET] I will find you some vegan.” I really did want to see him.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S9`)
- Decision: KEEP / REMOVE

---

## 3. Appearance / status confounders (S12–S15)

_9 topics_

### Topic 18 — Ordering A Gown For Her

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Current code (LLM):** **S13 — appearance grooming**

**Four keyword representations** (BERTopic / labeling)

- **Main:** dress, wear, clothes, wearing, dressed, gown, jeans, shirt, dresses, suit
- **KeyBERT:** worn, fitting, matching, appropriate, fits, ensure, generous, arrange, madam, revealing
- **POS:** fits, graceful, fitting, stunning, benefit, extent, unlikely, appropriate, preferred, decades
- **MMR:** worn, arrange, matching, graceful, fitting, madam, topped, flowing, flared, exact

**BERTopic representative docs**

> 1. once the dress dries out i can wear it home…” “yeah.

> 2. incre dibly, there sat my mother, in the very vera wang dress both apolo and i had expressly told her not to wear.

> 3. i wear this dress all the time.

**Stage-08 labeling snippets**

> 1. he’ll make sure you have a dress worthy of you.”

> 2. i’ll order a gown for you and have it sent to the house.” “

> 3. we’ll have to borrow their clothes.” “

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_A, CELL_B, CELL_C, CELL_D; 0 examples from 0 books_

> **CELL_A** — high_prevalence_high_tier — _no usable sentences in packet_

> **CELL_B** — high_prevalence_low_tier — _no usable sentences in packet_

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Packet representative sentences** (fallback when CELL sample empty)

> 1. I am not some maid who needs these kinds of clothes.” “

> 2. I did not mean to hurt your feelings about your attention to the womanly details of dress and appearance and wished to compensate you for the loss of the gown you’ve been wearing to work with Wilfrid.”

> 3. Here, who you are matters more than what you wear.”

> 4. My thanks for it…and the gowns.”

> 5. Mayhap if you were clothed when you attempted it, Edmee might have accepted it?” “’

> 6. Her gown should be clean and her hair always groomed and under a veil. “

> 7. So get dressed.

> 8. You have the best clothes.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S13`)
- Decision: KEEP / REMOVE

---

### Topic 77 — Haircut and Grooming Offered

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Current code (LLM):** **S13 — appearance grooming**

**Four keyword representations** (BERTopic / labeling)

- **Main:** hair, blonde, blond, shave, shaved, brown, black, dark, haircut, short
- **KeyBERT:** curled, patted, wrinkled, blowing, delicate, attractive, willing, insisted, bothering, lined
- **POS:** extent, ends, contrast, overheard, inevitable, typical, annoying, slightest, desperation, treatment
- **MMR:** neatly, wrinkled, ends, contrast, blowing, described, bothering, slightest, shaped, dried

**BERTopic representative docs**

> 1. a tall, willowy blonde with not too much on.

> 2. for some reason, she couldn’t remember the right shade of brown, and it just looked strawberry-blonde.

> 3. her hair was light brown, not dark like her father’s but nowhere near as blonde as her sister’s. “

**Stage-08 labeling snippets**

> 1. i’ll send [person] in to help you finish dressing and repair your hair.

> 2. it’ll be good for the librarian to take down her hair and have some fun for a change.

> 3. iffen you want a haircut and shave, megan’ll do that for an extra two bits.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · One Way Or Another — Eve Rabi; tertile=begin; p=0.66**
>
> He walks toward me, no wheelchair, no assistance from anyone. [TARGET] Full head of hair, with just the slightest grey around the temples. When he sees me, he stops walking and smiles.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Sinful Desires: Vol. III — M.S. Parker; tertile=middle; p=0.50**
>
> Hello.” [TARGET] I'd seen this guy with his hands all over one of Britni's bridesmaids, some tiny little brunette with fake nails and awful pink lipstick. “ I'm Peter.”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · The Hating Game — Sally   Thorne; tertile=begin; p=0.65**
>
> Leave this to the expert.” [TARGET] When I return he’s a little less dark looking, but his hair is messed up. He takes the document, which I have stamped COPY.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_016 · Waking Lucy — Lorin Grace; tertile=end; p=0.65**
>
> Samuel is a big person. [TARGET] He can do his own hair and back,” Lucy explained not daring to look at his sandy hair or broad shoulders. “ But Mama used to help Papa.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Alcandians: Alcandian Soul — Mary Wine; tertile=middle; p=0.66**
>
> Lifting her arm, she compared one hand to the other. [TARGET] Tiny blonde hair still covered one hand while the other was smooth. Apparently the pool wasn’t malfunctioning.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Embrace — Megan Derr; tertile=begin; p=0.61**
>
> The Pet was beautiful, there was no denying that. [TARGET] His hair was the color of beeswax, cropped extremely short and seemingly fine, delicate wisps of it clinging to his cheeks and forehead. His skin was smooth and flawless, and ever so faintly sun-kissed, lending a further impression of warmth.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Bittersweet — Sarah Ockler; tertile=middle; p=0.58**
>
> The moment she hears my groan, her lips descend over my dick. [TARGET] My hands grab her hair, and all I can picture is Kennedy’s sunshine blonde hair, and her blue eyes pleading with me to pump into her mouth faster. My eyes pop open immediately as I try and get the visions of Kennedy’s pink lips wrapped around my throbbing dick out of my mind.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_010 · Dixon's Duty — Jenna Byrnes; tertile=middle; p=0.62**
>
> He motioned to the tall, slender woman standing next to the bar. [TARGET] Her hair was light brown, not dark like her father’s but nowhere near as blonde as her sister’s. “ Kay, this is Dix.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_001 · The Seductive One — Susan Mallery; tertile=begin; p=0.53**
>
> Like Francesca, Mia was a blend of the two sides of their family. [TARGET] Her eyes were light brown, and while her hair was darker than Katie’s, it wasn’t as dark as Brenna’s, even without the blond streaks she painted in every couple of months. Mia was the shortest of the sisters, as curved as Brenna, but without her tendency to gain in the hips. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · DRIFT — Elle Beauregard; tertile=end; p=0.63**
>
> Her hazel eyes were bright now that her coffee cup was empty. [TARGET] And her bed head hair above that T-shirt of his was almost more than he could handle. Jesus, he wanted a cigarette. "

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Into the Light — Tami Lund; tertile=middle; p=0.58**
>
> Having run on pure adrenaline for the past hour, exhaustion was finally beginning to set in. [TARGET] My body felt like heavy, like it had leaden weights attached, and though he didn't show it, I knew Braeden couldn’t be fairing much better He smiled, brushing a wet lock of hair from my forehead. “ Probably not a good idea.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · No Time for Secrets — Liz Borino; tertile=end; p=0.58**
>
> Kaden reached down and stroked Rhett’s shaved head. [TARGET] Rhett could tell Kaden missed his hair as much as he did. Rhett grounded Kaden’s hips to the bed so he didn’t thrust too hard into the back of his throat.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · The Forced Bride — Sara Craven; tertile=middle; p=0.57**
>
> Never. [TARGET] It also seemed, from the smoothness of his skin against hers, that he’d had the promised shave—presumably while she’d been preparing dinner. Advance planning, she thought, digging her nails into the palms of her hands.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_003 · The Forced Bride — Sara Craven; tertile=end; p=0.44**
>
> She kissed him on the mouth, her lips warm and lingering as they smiled against his. ‘ [TARGET] And, whatever your doctor friend may say,mio caro ,’ she whispered huskily, ‘tonight you will most definitely need to shave. And that’s a promise.’

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · Fair Play — Janna Shay; tertile=end; p=0.54**
>
> In your stupidity, you think she wanted you, but the truth is she hates you. [TARGET] One thing I know, if you touch one hair on her body, there will be no place on earth for you to hide. My husband, Dani’s real father, and Dani’s new husband will hunt you down for the filth that you are.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Save the Date — Susan Hatler; tertile=begin; p=0.54**
>
> She leaned forward, hands on her bare knees. “ [TARGET] Do you think I knew Jeremy had been getting it on with my hairdresser those weeks before he dumped me? No.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S13`)
- Decision: KEEP / REMOVE

---

### Topic 171 — Staring at Her Own Reflection

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Current code (LLM):** **S13 — appearance grooming**

**Four keyword representations** (BERTopic / labeling)

- **Main:** mirror, reflection, rearview, glanced, herself, checked, mirrors, stared, looked, in
- **KeyBERT:** reflection, reflected, gazing, peered, glimpse, observed, studied, flipped, blinking, polished
- **POS:** reflection, stares, glimpse, surroundings, unhappy, fitting, stunning, result, tracks, sidewalk
- **MMR:** reflection, stares, glimpse, surroundings, stunning, blinking, gazing, shaped, twitched, sidewalk

**BERTopic representative docs**

> 1. chapter 3 elle checked her reflection one last time in the mirror.

> 2. her reflection grinned at me in the mirror. “

> 3. she walked over to the mirror and stared at her reflection.

**Stage-08 labeling snippets**

> 1. she stood and checked her reflection in the mirror over her parents’ dresser.

> 2. esme stared at their reflection in the glass. "

> 3. but then she stared at her surface-repaired reflection.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Slow Dance in Purgatory: a novel — Amy Harmon; tertile=end; p=0.71**
>
> They stared soberly at the image reflected back at them – a beautiful girl held in the invisible arms of her soul mate. [TARGET] He moved around her then, stepping in front of the mirror, replacing the haunting image with something more tangible. “ Maggie.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_009 · His To Keep — Lydia Goodfellow; tertile=end; p=0.64**
>
> That night, I shut myself inside the bathroom to have a hot shower. [TARGET] As I undress, I catch a glimpse of myself in the mirror, cringing by how visible my bones are. No longer able to stand the sight, I get into the shower.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Caught in the Devil's Sheets — Jesse Johnson; tertile=end; p=0.72**
>
> I make my way into the bathroom and squint as I flick the lights on. [TARGET] After my eyes adjust, I hesitantly examine my back in the full length mirror on the back of the bathroom door. Fuck Me!

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Sawman Werebear — T.S. Joyce; tertile=end; p=0.56**
>
> The top was fitted with delicate straps that made her collar bones look quite lovely. [TARGET] The cream-colored cardigan matched the flats she slipped onto her feet, and when she looked in the mirror again, she felt like a princess. He’d imagined her in this dress and had picked out exactly the dress she would have adored on a manikin while window shopping. “

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Contract of Shame — Sam Crescent; tertile=middle; p=0.58**
>
> She’d been getting by like always. [TARGET] When the other women left, giving her a disparaging look, she splashed water on her face and stared at her reflection. Many revelations were happening all at once.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Losing and Gaining — Heidi Champa; tertile=end; p=0.48**
>
> It was the fresh start I never thought I'd get. [TARGET] The first day I walked into the gym, I put the old Doug Smith in my rearview mirror. I never thought I'd have to deal with any of that baggage ever again." "

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · Billionaire: Complete Set — Juliette Jones; tertile=begin; p=0.60**
>
> Time would tell if Eva’s estimations were at all accurate. [TARGET] I tried to let her enthusiasm rub off on me as I studied my own reflection. My long, honey-blond hair fell in sleek, waving skeins; highlights of platinum caught the light.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · Sweet Little Thing — Abbi Glines; tertile=end; p=0.61**
>
> I went to work with new musicians in the studio, and Mia went back to her obsession with being pregnant. “ [TARGET] I’m as big as a house,” she said one night into the mirror above our dresser as she examined her naked body from every angle. I watched her from the bed where I was propped against the headboard.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_002 · One Grave at a Time — Jeaniene Frost; tertile=middle; p=0.43**
>
> But, since I was supposed to be looking on the bright side, last night meant we didn’t have to start looking for Italian chefs and drug dealers in order to layer up this place with a bunch of garlic and weed. [TARGET] How was that for a Glass-Half-Full perspective? The first thing I did even before letting my kitty out was start lighting sage and putting it on some of the many incense burners and glass jars we’d acquired on our trip from St. Louis to Sioux City.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · Blue Roses — Sharon C. Cooper; tertile=end; p=0.55**
>
> You gon’ miss out.” [TARGET] Tuning his unwanted guest out, Mark faced forward looking at the mirror behind the bar, surprised at how quickly the bar and grill had filled up. He enjoyed the exhilaration that always surrounded him whenever he was there.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · A Knight to Call My Own — Sherry Ewing; tertile=middle; p=0.73**
>
> He tossed her a smug look, as if he had already read her thoughts. [TARGET] They were mirrored clearly on her face. “ Your hands are free. ’

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Bearfoot and Pregnant — Milly Taiden; tertile=middle; p=0.79**
>
> Having ordered her food, she slid out of bed and groaned at how tired she still felt. [TARGET] She went into the bathroom and stared at herself in the mirror. Instead of looking sick, she looked great.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Almost Perfect — Julie Ortolon; tertile=end; p=0.68**
>
> They were both simple, jersey knit, a flattering, forgiving fabric that could be dressed up or down. [TARGET] Stepping before the mirror that hung on the bathroom door, she held the hangers under her chin. The short red?

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Almost Perfect — Julie Ortolon; tertile=end; p=0.79**
>
> Once the boot camp was up and running, she’d get back to it. [TARGET] Lifting her head, she caught a look at her dripping face in the mirror. Good grief, she looked like hell.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_010 · A Baby On Her Christmas List — Louisa George; tertile=middle; p=0.67**
>
> He told himself that he didn’t want to make her jump. [TARGET] She was standing in front of her closet, holding a black lace dress up against her body and looking in the mirror, turning from side to side, stretching the fabric across her belly. The work dungarees had gone, and now she was wearing flannel shorts and a baggy blue T-shirt.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_015 · Jagger — Jane Perky; tertile=middle; p=0.63**
>
> Why would you think that?” “ [TARGET] It’s just…have you looked at yourself in the mirror? You’re like walking man-candy.”

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S13`)
- Decision: KEEP / REMOVE

---

### Topic 218 — Resenting Someone More Attractive

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Current code (LLM):** **S13 — appearance grooming**

**Four keyword representations** (BERTopic / labeling)

- **Main:** handsome, gorgeous, cute, beautiful, adorable, attractive, looked, man, good, looking
- **KeyBERT:** attractive, mister, highly, merely, intended, considered, poised, described, strangely, excited
- **POS:** attractive, mister, makeshift, potential, decent, features, intended, worst, comfortable, huge
- **MMR:** attractive, mister, makeshift, poised, dangerously, dangling, described, earned, snatched, built

**BERTopic representative docs**

> 1. he was a handsome and honorable man.

> 2. he really was a handsome man.

> 3. how could i even begin to like someone who was:  a) gorgeous, thereby making me, someone who until now was considered pretty decent looking, seem, at best, perfectly average, and, at worst, like the sibling who got beaten with the ugly stick;  b) paid huge bucks to roll around in the sand making out with equally gorgeous girls while i donned a hideous fluorescent orange apron, an equally hideous lime green baseball cap with an assortment of stuffed fruit dangling from the center in a makeshift pom-pom, and honed my smoothie- making skills for six bucks an hour;  c) a veteran of rehab, probably attended more 12-step programs than all the boy bands from the nineties combined, thought nothing of totaling a hundred-thousand-dollar sports car, and even managed to expose his pearly whites in his mug shots so that he looked like someone making a dentyne commercial instead of a criminal about to begin two hundred hours of community service, while i followed the rules or never caused my parents a day of worry, and yet they wouldn‘t even let me spend one lousy summer in europe, for god‘s sake.

**Stage-08 labeling snippets**

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

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S13`)
- Decision: KEEP / REMOVE

---

### Topic 253 — Hair Pinned Up in Style

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Current code (LLM):** **S13 — appearance grooming**

**Four keyword representations** (BERTopic / labeling)

- **Main:** hair, ponytail, loose, bun, braid, blonde, curls, blond, long, brown
- **KeyBERT:** dangling, curtain, straightened, neatly, feminine, worn, dipped, wound, delicate, loose
- **POS:** loose, feminine, admire, ends, unhappy, curtain, unable, waist
- **MMR:** fashioned, neatly, bursting, dangling, feminine, described, tumbled, curtain, flowed, spilling

**BERTopic representative docs**

> 1. she had pinned her wispy blonde hair back in a loose chignon.

> 2. her long blonde hair fell loose around her hips, wild tresses glowing nearly white.

> 3. her long, pale blonde hair was pulled back in a messy bun and a few wild loose strands stuck to the sweat soaked skin of her neck.

**Stage-08 labeling snippets**

> 1. she had pinned her wispy blonde hair back in a loose chignon.

> 2. when she messed up, she’d pout and toss her golden hair over her shoulder.

> 3. her glossy hair is piled up in loose ringlets on her head and pinned with a coral comb.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_002 · Vision in White — Nora Roberts; tertile=begin; p=0.74**
>
> Laurel’s hand was steady as a surgeon’s as she added the next lily. [TARGET] Her sunny hair was twisted at the back of her head into a messy knot that somehow suited the angular triangle of her face. As she worked, her eyes, bright as bluebells, held narrowed concentration. “

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · Penmort Castle — Kristen Ashley; tertile=middle; p=0.72**
>
> Nicola was nearly sixty years old but she looked ten years younger. [TARGET] Tonight, as usual, her blonde hair was pulled back into an elegant bun at her nape, her clothing was understated yet stylish and her bearing was graceful but friendly. Honor was the only one of Nicola’s daughters that Cash could remotely endure.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_006 · Midnight's Lover — Donna Grant; tertile=begin; p=0.73**
>
> She was slowly descending the stairs with one hand always on the stone wall next to her. [TARGET] Her walnut-colored hair was pulled away from her face at her temples, but hung straight and glossy to her shoulderblades. Camdyn had been the one to carry her out of Declan’s dungeon.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Agnes and the Renegade — Elaine Levine; tertile=begin; p=0.73**
>
> She gave a cursory look at herself in the mirror above the dresser. [TARGET] Her light brown hair was too silky to stay neatly coiffed without an excess of pins. Her blue eyes were unexceptional.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Wicked Enchantment — Anya Bast; tertile=end; p=0.69**
>
> TWENTY-EIGHT AISLINN stood on the top of the Black Tower at dusk still wearing her wedding dress, a bloodred and cream affair, accompanied by dripping ruby jewelry that would rival any outfit of the Summer Queen’s. [TARGET] Her hair was gathered and twisted at the back of her head, the red tips fanning out in an arc at the top and secured by a silver and black crown. Her new husband stood beside her, now a king.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Edge Play X — M. Jarrett Wilson; tertile=begin; p=0.67**
>
> Judging by her appearance, it wouldn’t be such a leap to make that assumption. [TARGET] X had pulled her hair into a high ponytail that sat nearly at the top of her scalp, and around the lower couple inches of the ponytail she had placed a silver cylinder which made her hair extend straight up and jut out in wild strands. Her eyes were rimmed with kohl liner, her lids brushed with vibrant red and purple.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Only Everything — Kieran Scott; tertile=begin; p=0.75**
>
> She had, in fact, raised her hand to answer every question the teacher had posed. [TARGET] Her strawberry-blond hair was pulled back tightly from her head and tied into a French braid like Harmonia liked to weave into my hair when she was bored, adding a daisy or a sprig of lavender here and there. She had a smattering of freckles across her cute, upturned nose, and very pretty pink lips.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_013 · Relentless — Rachel  Ryan; tertile=end; p=0.76**
>
> My eyes drift to Jo as she leans forward and places the bowl of chips on the coffee table. [TARGET] Her shoulder length hair is pulled up into a tiny little pony tail on the top of her head, with a few loose strands framing her face. As I sit here staring at her I can tell she is trying not to look at me.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_007 · A Cowgirl's Pride — Lorraine Nelson; tertile=begin; p=0.66**
>
> The occasions when they’d stolen away for some time alone were imprinted on his memory, even after all the years that had passed. [TARGET] Her cascade of long, platinum hair had reached to her waist—thick, silken tresses that he’d loved to run his fingers through. When she was filled with desire, the depth of her eyes held a golden glow, almost like an inner halo.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_008 · Testing Fate — Belinda Boring; tertile=begin; p=0.51**
>
> Tell us how you remember it,” Atropos ordered. [TARGET] Resting on her elbow, her long legs were stretched out on the elegant chaise, the folds of her dress keeping the smooth whiteness of her skin hidden. It was hard to judge what she was thinking, her facial features void of emotion.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_009 · Finally...One Summer — Kristi Pelton; tertile=middle; p=0.58**
>
> Ryan smiled, Seth nodded and Austin waved. [TARGET] It wasn’t until we joined the circle that I saw the girl resting between his legs, her brown hair pulled up into a cute messy bun. My breath caught in my throat.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_015 · Blue Dream — Xavier Neal; tertile=begin; p=0.66**
>
> More like I go where I feel.” [TARGET] She tosses her blonde hair, which now has purple tips, over her shoulder. “ Free spirit.” “

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Behaving Badly — Isabel Wolff; tertile=begin; p=0.69**
>
> I’m normally circumspect when I meet someone new, but I immediately took to her. [TARGET] She was thirtyish, with dark blonde hair scraped back in a ponytail, and she was attractive in a non-glossy way. ‘ I’m so grateful to you,’ she repeated.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · The Walls of Troy — L.A. Witt; tertile=middle; p=0.67**
>
> Any particular reason?” [TARGET] Leaning forward, I pushed my hair back a little—damn, it was still weird to have it this long—to expose part of my forehead, right up by the hairline. “ See that scar?”

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Affairytale — C.J. English; tertile=begin; p=0.29**
>
> We were a spectacle. [TARGET] A pretty girl in a cowboy hat standing in the middle of a muddy field, while her berserk husband circled her and ranted furiously. I thought of Grant, wondered if he was there somewhere in the sea of bodies.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_016 · Keeping His Commandments — Elle Keating; tertile=begin; p=0.64**
>
> the waitress asked. [TARGET] She blew a stray lock of hair out of her line of vision while she retrieved a pen from the black apron at her waist. It was only nine o’clock but she already looked frazzled. “

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S13`)
- Decision: KEEP / REMOVE

---

### Topic 364 — Noticing What He Wears

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Current code (LLM):** **S13 — appearance grooming**

**Four keyword representations** (BERTopic / labeling)

- **Main:** shirt, jeans, black, wore, wearing, boots, dressed, white, pants, sweater
- **KeyBERT:** worn, draped, wrinkled, fitting, neatly, comfortable, loose, contrast, attached, smoothed
- **POS:** fitting, contrast, pattern, polished, worn, exchange, nods, issue, loose, lack
- **MMR:** wrinkled, contrast, pattern, polished, neatly, instincts, worn, draped, reveal, tied

**BERTopic representative docs**

> 1. chapter six g abe was dressed in a white shirt and jeans, but different boots than he’d worn outside today.

> 2. except now, he had changed from his tee shirt and running shorts into a pressed, collared shirt and dark navy blue jeans.

> 3. he wore a collared light blue dress shirt with a thin striped tie, a black blazer, and a pair of nicely fitted navy pants.

**Stage-08 labeling snippets**

> 1. if i had any nerve i’d go throw them open and see what he’s wearing, not that i’ve seen him in anything except shorts, t-shirts and a stupid beanie.

> 2. he was dressed as he was at the court: [person] t‐shirt, black [person] hoodie hanging open, loose‐fitting jeans and biker boots.

> 3. he wore a loose-fitting, blue jacket and white shirt, and the lack of a cravat exposed too much of his throat and even his chest.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 16 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · 32 Candles — Ernessa T. Carter; tertile=middle; p=0.68**
>
> And though I could tell from his few words that he had ditched his Southern accent, he was just as beautiful as ever. [TARGET] He wore his hair in one of those hip, urban Afros, and his skin shone out bright against the lightweight tan suit that he had on with a red T-shirt and very expensive-looking leather slip-ons. How could he still be so incredibly beautiful?

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_005 · A Lot Like Love — Julie James; tertile=begin; p=0.67**
>
> A sweater-vest. [TARGET] As in, Huxley wasn't wearing just a suit; he had this whole ensemble going: dark brown pants and jacket, crisp pinstriped shirt, V-neck vest, and tan silk tie. Nick, on the other hand, was dressed in his standard-issue, no-frills gray suit, white shirt, and navy tie.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · Unforgettable You — Heatherly Bell; tertile=middle; p=0.71**
>
> When she carried her bag outside, it nearly slipped out of her hands at the sight of Scott standing near his truck. [TARGET] He wore jeans falling tantalizingly low around his hips and that ever present t-shirt, cotton straining tight around his biceps and defining his broad shoulders. He was talking to a pretty blonde woman, who grabbed his shoulders, then threw back her head and laughed.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_013 · Russian Roulette — Sapphire Knight; tertile=begin; p=0.76**
>
> Tate steps inside and he looks absolutely gorgeous. [TARGET] He’s wearing a light grey button up shirt and some black slacks that mold to his physique perfectly. He looks professional and sexy but not over-dressed.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Things to Make and Mend — Ruth Thomas; tertile=end; p=0.67**
>
> She is one of those mousey women who is daring underneath. [TARGET] Jeremy has removed his beige corduroy jacket too, and his cream turtle-neck sweater. He is sitting there in a pale blue shirt, the top button undone to reveal a little chest-hair, far up, like a high Plimsoll line. (‘

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_003 · Bound by Love — T.A. Chase; tertile=begin; p=0.62**
>
> Jesus. [TARGET] You’d think he was meeting the president the way he couldn’t decide what to wear. It wasn’t like Ren hadn’t seen him a thousand times covered in horse shit, cow shit or mud.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_009 · The Cirque — Ryann Kerekes; tertile=begin; p=0.71**
>
> He had the whole sexy, brooding-and-misunderstood look down to a science. [TARGET] His dark hair was disheveled and though everyone else was in workout clothes, he wore jeans and a faded t-shirt with a logo for a band I’d never heard of. Tattoos crept from under his sleeves and decorated much of his arms.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_015 · Planet Sweshan — Olivia  Black; tertile=begin; p=0.64**
>
> But Ael had other plans. [TARGET] He wanted to see Grant wearing tailor-made clothes similar to the jumpsuit that clung tightly to his body. “ Grant,” Ael called out.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_010 · A Splash of Substance — Elizabeth Maddrey; tertile=end; p=0.62**
>
> “Are you sure this isn’t too casual?” [TARGET] Jackson brushed at the black slacks that he’d paired with a lime green polo. “ She’s going to be in catering clothes, right?

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_011 · Playing the Part — Jen Turano; tertile=begin; p=0.46**
>
> But there Mr. Kenton had been, holding the reins in hands that had clearly been shaking while Abigail beamed back at Bram from her seat beside her butler. [TARGET] Another time he’d come across her in the gentlemen’s suit section at Arnold Constable & Company, where she’d immediately sought his assistance in helping Mr. Kenton choose the perfect suit, even though, in Bram’s opinion, Mr. Kenton hadn’t been aware he was suit shopping until that very moment. The last time he’d encountered Mr. Kenton had been on the Hudson River, right beside Bram’s private dock.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_014 · Say You'll Stay — Corinne Michaels; tertile=begin; p=0.60**
>
> It’s like I’m fourteen all over again and he’s asking me to go on our first horseback ride. [TARGET] The assured grin he wore, the tight jeans that made his butt look great, and the way his eyes would convey everything he wouldn’t say. We were so young, so in love, and so idealistic. “

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_016 · Fallen from Grace — Nikki Landis; tertile=begin; p=0.74**
>
> The fitted black t-shirt he wore molded to his frame, moving with his muscles as if they were one. [TARGET] Only then did I realize he was dressed all in black, from that shirt to his jeans to the heavy tall boots laced up his calves. He reminded me of some dark god.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_001 · Highland Moonlight — Teresa J. Reasor; tertile=end; p=0.47**
>
> Her gaze focused on her husband as he spoke to Gabriel. [TARGET] Alexander’s large frame was covered from neck to calf in fur; his hands protected by leather gloves and his feet by knee high boots. He appeared well prepared for whatever the heavens decided to offer, but even the furs he wore would not keep the cold from penetrating should a blizzard strike.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_006 · Country Soul — Remmy Duchene; tertile=end; p=0.58**
>
> When he looked at his handy work, they were ready for a night in the woods alone. [TARGET] Drying his hands, he hurried into his bedroom and got dressed in a pair of track pants and a Toronto Blue Jays jersey top. He stuck his wallet into his back pocket and pulled a couple of clean towels from the linen closet.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_007 · If the Shoe Fits — Sandra D. Bricker; tertile=middle; p=0.43**
>
> He stopped in his tracks. [TARGET] Gone were the classic racks upon racks of clothes, the soft strains of elevator music, and stiff mannequins dressed in all-too-boring business attire. Even the lighting had been adjusted.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_008 · Pride, Prejudice and the Perfect Match — Marilyn Brant; tertile=end; p=0.40**
>
> In that case, count on me to show up.” [TARGET] Then he leaned forward, as if about to ask a personal question, when the electronic version of an old Prince tune, “Little Red Corvette,” blared from somewhere inside his clothing. Odd choice.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S13`)
- Decision: KEEP / REMOVE

---

### Topic 140 — Demanding Answers Before Departure

- **Taxonomy:** 6.6 — Material Glamour & Consumption
- **Current code (LLM):** **S14 — gift romance token**

**Four keyword representations** (BERTopic / labeling)

- **Main:** benjamin, himself, hutton, his, spencer, morrison, jim, had
- **KeyBERT:** scenario, strolled, thinks, asks, anxious, possibilities, remarked, poised, growl, urge
- **POS:** scenario, extent, behalf, possibilities, irritation, hopeful, enormous, session, fashioned, notion
- **MMR:** poised, insulted, scenario, extent, remarked, encouraged, heaved, fashioned, framed, strolled

**BERTopic representative docs**

> 1. holding his digits poised just inside david’s entrance, ben stopped thrusting and encouraged, “go on.

> 2. before ben could growl—david at least knew him well enough to know he would—david touched ben’s leg and said, “right now i’ll settle for some answers.”

> 3. every time ben gave his brief training report he couldn’t stop thinking that if the manager knew how he’d lost his grip and given in to his howling urges, how he’d shamelessly shoved his tongue in regan’s mouth and palmed her breast, that if spencer hadn’t come along ben almost certainly would’ve shoved that tight dress up over her hips, hauled down whatever silky scrap of cloth she wore beneath and— “that phrase sounds so funny when you say it.”

**Stage-08 labeling snippets**

> 1. before [person] could growl—david at least knew him well enough to know he would—[person] touched [person] leg and said, “right now i’ll settle for some answers.”

> 2. it’s kind of amazing that a few simple words from [person] can have this effect, and [person] doesn’t think he’ll tire of it, ever.

> 3. who knows what you'll be walking into on benezet , much less how long you'll be gone."

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_C, CELL_D; 8 examples from 6 books; ±1 context on 8_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Dragon and Crow 1 — Alex A. Akira; tertile=middle; p=0.69**
>
> He’d smirked nastily as he’d dictated his demands. [TARGET] It was only then that Ben had realized what a lowlife the guy was, how truly base the mind housed in that beautiful body was. Seeing no way out, he’d agreed to do the job.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Dragon and Crow 1 — Alex A. Akira; tertile=middle; p=0.68**
>
> No, I’m not up to it... Do me a favor, take the glasses and lemonade out to them and pour them a glass, I’ll be out with your money in a minute.” [TARGET] Ben stared at him, then spoke in a harsh whisper, “You’re sure? I, um, I really ...I mean, am I not your type?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Backfield in Motion — Jami Davenport; tertile=end; p=0.62**
>
> He should know that story better than anyone. [TARGET] Sonja and Ben were charged with first-degree murder, at which point Ben sang like a bird and pointed fingers at Sonja, swearing she was the mastermind, and he’d just been the cleanup guy. After all this time, Mac hadn’t expected it to hurt as much as it did, despite her relief to finally know the truth.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Backfield in Motion — Jami Davenport; tertile=end; p=0.72**
>
> Another wild goose chase that came to nothing. [TARGET] Ben’s former employee admitted he’d just been trying to cause trouble for Ben. Mac wasted a weekend on another dead-end lead.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_005 · Kiss of Pride — Sandra Hill; tertile=end; p=0.66**
>
> She also tried her best to hide her fears from Vikar, not wanting to spoil this short engagement period. [TARGET] She’d told Ben about her engagement, and he’d been apoplectic at first, wanting to come immediately and “rescue” her. But when she assured him how much she and Vikar loved each other and how happy she was, he gave his blessings, with reservations.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Vanity and Valor — R. Lynn; tertile=middle; p=0.45**
>
> Jefferson, however, did not think such a thing truly possible. “ [TARGET] Is it you, sir,” a Frenchman supposedly asked him, “who will replace Franklin?” “ No sir, I succeed him,” he replied.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Ruby — Juliet James; tertile=end; p=0.79**
>
> Now you told me last week … let me see if I remember … that the best reason for a man and a woman to marry is true love. [TARGET] That’s what you said wasn’t it Ben?’ Oh yes, he knew he’d said it — and remembered how he’d looked right at her eyes when he’d said it as well, and the way that he’d colored then too.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_014 · Steel Love — P.J. Rider; tertile=begin; p=0.65**
>
> According to Ben he’d left the club when he’d met the woman that would later become his wife. [TARGET] A combination of not liking where the club was heading, and wanting to settle down and get married and have kids led Ben to choose his current path. Ash respected the man making a decision and sticking with it, and he definitely left on good terms or else Ash wouldn’t even be speaking to him let alone paying him for his services, but that didn’t mean Ash was going to start discussing club business with him. “

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S14`)
- Decision: KEEP / REMOVE

---

### Topic 170 — Staying Close Despite Long Separation

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Current code (LLM):** **S13 — appearance grooming**

**Four keyword representations** (BERTopic / labeling)

- **Main:** together, each, they, other, relationship, their, them, both, couple, between
- **KeyBERT:** closely, separated, scenario, shared, separate, seemingly, theirs, visits, problems, opportunity
- **POS:** separate, session, visits, scenario, guarantee, creatures, stunning, exciting, exact, regular
- **MMR:** session, visits, scenario, constantly, warming, separated, television, emotional, spending, brief

**BERTopic representative docs**

> 1. never could tye have guessed they’d end up lovers after the misery of their parting ten years before.

> 2. lovers as post-graduates when they met at the kursi dig site on the sea of galilee, bridget had ended their liaison two years ago.

> 3. the little bit of history they shared was long gone and the new relationship they forged would be based on nothing permanent or emotional, and when it was safe, they’d walk away from each other to find their futures separately.

**Stage-08 labeling snippets**

> 1. despite going months without talking to each other—their daily lives hectic enough that even living in the same city had never ensured regular visits—they were close.

> 2. my guess is they’ve been seeing each other the whole time.

> 3. they might've solved his problems together.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_16 examples from 15 books; ±1 context on 16_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_001 · No Compromise — Rochelle Alers; tertile=begin; p=0.71**
>
> Jolene’s statement lingered with Michael as he reached for a metal canister, measuring a mixture of rose petals, linden flowers, and chamomile leaves into a small dish. [TARGET] They’d scaled the first hurdle: They liked each other. He poured boiling water into a pale green ceramic teapot covered with painted black Asian calligraphy.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_004 · Promise Me Texas — Jodi Thomas; tertile=end; p=0.69**
>
> Silence stretched between them. [TARGET] Since the shooting, they’d seen a great deal of each other, but somehow they’d become strangers. He missed her touch, her kiss.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_010 · Entwined — Bridgitte Lesley; tertile=middle; p=0.70**
>
> Malik was coming over tonight, and she wanted it to be perfect between her mum, him and her. [TARGET] It was bad enough they’d probably hated the idea of each other for several years beforehand. Sarah lined up her body wash liquids and decided on vanilla.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_015 · Dreaming With My Eyes Wide Open — Mary J. Williams; tertile=middle; p=0.69**
>
> His plan had been to spend the next few weeks making love with Paige again and again. [TARGET] It wasn’t easy knowing their first time together might have been their last. JAMES CRANSHAW WAS not a brave man.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_002 · Mastering Toby — Jan  Irving; tertile=end; p=0.67**
>
> He was here, nude, under a starlit sky, with the man he’d fantasized about. [TARGET] It was strange how they’d met, almost as if it was fated to happen sooner or later. “ Seth, like this.

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_007 · The Tempering — Adrianne James; tertile=middle; p=0.66**
>
> Teresa was next to her, arms wrapped around her waist with her head on Natalie’s shoulder. [TARGET] Seeing the two of them still together and close after such a tragedy made Mackenzie realize that the pack was still a family and they still loved each other. No amount of fuckups could take that away. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_008 · All's Fair in Love and Cupcakes — Betsy St. Amant; tertile=end; p=0.67**
>
> She was reaching now, desperate to fill the silence between them, same battle he’d been fighting. [TARGET] It was like, lately, if they weren’t bleeding their hearts out to each other, they couldn’t communicate at all. “ It was great—for California, anyway.”

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_011 · Breathless for You — Lexxie Couper; tertile=begin; p=0.55**
>
> That had been the beginning of their tradition. [TARGET] Friday afternoons in the Outback Skies, talking shit, giving each other shit, finding calm and peace in their friendship when their jobs flying high above the world left them raw and exhausted and drained. If it weren’t for Friday afternoons, Matt probably would have done something stupid by now.

**CELL_C** — low_prevalence_high_tier

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_003 · For Real — Staci Stallings; tertile=middle; p=0.43**
>
> Does he see what a great team he’s built? [TARGET] I can see how Coach, Diane, Pete and Riley love him even when they quarrel. I wanted to belong to this team, but now I just want to belong to this man.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_005 · Be with Me — J. Lynn; tertile=begin; p=0.65**
>
> Again. [TARGET] They must’ve made up, but they fought so much I wondered how they had any time for anything other than arguing and makeup sex. Erik appeared, his fingers flying over the screen of his cell.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_006 · Darkness Deserved — Jessica Spoon; tertile=end; p=0.43**
>
> Our friends have come over nearly every night and we have all grown close. [TARGET] Everyone gets along flawlessly and Rich has been brought into the fold without as much as a hiccup. I’m pretty sure Brynn and him have been getting it on, but as long as it doesn’t affect the group, I have no problem with it.

> **HIGH-rated (low topic share in this book; was CELL_C) · BOOK_013 · The Blue Room Vol. 5 — Kaiiln Gow; tertile=end; p=0.52**
>
> But now I see how wrong I was. [TARGET] Now I see that the intimacies we shared were no different from those I share with Xander or with Terrence: a role that two people play when one person wants something from the other, when money changes hands. My best friend was a prostitute, I knew that already.

**CELL_D** — low_prevalence_low_tier

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_009 · The Awakening Of Poppy Edwards — Marguerite Kaye; tertile=end; p=0.52**
>
> But you see, I thought that was work—that’s what I told myself. [TARGET] We wanted the same things, we were both ambitious, we complemented one another. It was a business relationship with sex thrown in.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_012 · Mercenary Instinct — Ruby Lionsdrake; tertile=end; p=0.48**
>
> He found her warm entrance and crashed into her, a wave surging up the beach. [TARGET] Their movements quickly became fast, frenzied, as if they had been apart for months instead of a couple of hours. They came together, the wave becoming a tsunami, a great blast that stole all of his strength and left him atop her, his face buried in her neck. “

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Here He Comes Again — Melissa Shirley; tertile=begin; p=0.61**
>
> He puckered his lips against Mom’s the way I wished Keaton’s lips would hop onto mine. [TARGET] From the duration of their kiss, I assumed this little development sprung forth from a rich and rather sleezy history. My next thought--Alex had been home the day before--flowed into another--my goody-two-shoes mother cheated on Alex.

> **LOW-rated (low topic share in this book; was CELL_D) · BOOK_014 · Here He Comes Again — Melissa Shirley; tertile=begin; p=0.61**
>
> Since I’d been home so many consecutive days over the last year, I noticed a change in their relationship. [TARGET] They no longer welcomed one another home with a kiss, and they barely spoke when Alex managed to be home for dinner. I sensed the end coming, and it saddened me because I didn’t want Alex to end up in the same loser pile as the others.

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S13`)
- Decision: KEEP / REMOVE

---

### Topic 345 — Older Man Trading Shelter For Sex

- **Taxonomy:** 7.4 — Unwanted or Coercive Sexual Contact
- **Current code (LLM):** **S14 — gift romance token**

**Four keyword representations** (BERTopic / labeling)

- **Main:** ilsa, dash, uncle, italian, informant, confidential, follow, asking
- **KeyBERT:** revealing, contrast, answering, flinched, winked, grumbled, handled, opposite, strangely, straightened
- **POS:** claims, contrast, stool, exchange, answers, meal, porch, opposite, decision
- **MMR:** claims, contrast, grumbled, stool, revealing, answering, pounded, straightened, meal, enjoying

**BERTopic representative docs**

> 1. tony, who talked about his mom’s italian cooking until they all wanted to chuck their mres in the dirt…tony who had a terrible voice but like to sing opera…tony who had been killed because nick decided to let the men take a wrong turn to make a point—and then…boom!

> 2. try telling that to my inner child,” i retorted grimly, going for my traditional tony nomination '“best dramatic performance over lunch”(. “

> 3. tony knew that nothing was something, but he had no claims on the boy; in fact, after hearing about jorge’s initiation into sex, it occurred to him that he might be just another older man trading off offers of shelter or a meal or booze in exchange for being fucked senseless.

**Stage-08 labeling snippets**

> 1. [person] says and then adds, “right.

> 2. mom didn’t talk to me about it, but i’m pretty sure uncle tony would’ve rather handled it a different way, if you know what i mean.” “

> 3. [person] knew that nothing was something, but he had no claims on the boy; in fact, after hearing about jorge’s initiation into sex, it occurred to him that he might be just another older man trading off offers of shelter or a meal or booze in exchange for being fucked senseless.

**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)

_no packet sentences for CELL_C, CELL_D; 8 examples from 8 books; ±1 context on 8_

**CELL_A** — high_prevalence_high_tier

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_007 · Blood Ties That Bind: The Beginning — April Ezell Wilson; tertile=begin; p=0.48**
>
> The lucky bastard landed in a deeply shaded spot on the road. [TARGET] Malcolm didn’t let his guard down and continued to watch him through the rear window waiting for Peter to attack again. He didn’t.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_008 · Never Doubt Me — S.R. Grey; tertile=end; p=0.73**
>
> he barks. “ [TARGET] I’m sorry, really, and I don’t mean to pry, but I just don’t understand why you’re here and Tony isn’t.” “ Tony?”

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_011 · Timeless — S.J. West; tertile=end; p=0.42**
>
> Yes, I’ve been told that,” Aiden says. “ [TARGET] Malcolm is supposed to take over the Watchers, so I should be making the transition just in time.” I realize Aiden’s plans are just like Mason’s.

> **HIGH-rated (high topic share in this book; was CELL_A) · BOOK_012 · The Poker Game — Enterprise1701-d; tertile=middle; p=0.43**
>
> In one instance the game is held up, with the robbery ending in a shootout and deaths. [TARGET] Another member of the crime family, Richie Aprile (David Proval), likewise hosts a regular game, as does Christopher Moltisanti (Michael Imperioli), Tony’s protégé. A subplot related to the Executive Game involves one of Tony’s friends joining and losing more than he can afford.

**CELL_B** — high_prevalence_low_tier

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_004 · Klutzy Love — Sharon Kleve; tertile=end; p=0.48**
>
> It better not be a criminal, because I wasn’t the least bit lethal yet. [TARGET] Instead of a malfeasant, it was Steve with a loaded pizza and a six-pack of beer—my dream man. When I opened the door he immediately noticed my partly naked body and went on instant sexual alert. “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_006 · Dusk — Lois H. Gresh; tertile=begin; p=0.35**
>
> If transistors were cool, how much cooler might microbial nanites be? ( [TARGET] Although I still want to know how Tony Stark fits those in-line roller skates inside his Iron Man boots, especially when the armor’s folded up and tucked away in his briefcase, which when you think about it is the source of yet another paradox, because even if you assume some ability to condense the volume of the armor into such a containment, how do you deal with the integral mass? I mean, how much does that puppy weigh and how the hell does anyone this side of the governor of California carry it?)

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_014 · Best Man for the Bridesmaid — Jennifer Faye; tertile=middle; p=0.55**
>
> How in the world were they supposed to have a wedding without a cake? [TARGET] Stefano gathered himself. “ So how are you at baking?” “

> **LOW-rated (high topic share in this book; was CELL_B) · BOOK_016 · At Your Service — Ariel Tachna; tertile=end; p=0.54**
>
> That includes you now.” [TARGET] Anthony was beginning to understand that. He’d have to make more of an effort to spend time at the restaurant with Paul’s family.

> **CELL_C** — low_prevalence_high_tier — _no usable sentences in packet_

> **CELL_D** — low_prevalence_low_tier — _no usable sentences in packet_

**Manual checklist** (fill in)

- Relationship-directed transfer / security act: yes / no
- Function: emotional / material_money / material_housing / appearance_status / other
- Security code: ________ (suggestion: `S14`)
- Decision: KEEP / REMOVE

---
