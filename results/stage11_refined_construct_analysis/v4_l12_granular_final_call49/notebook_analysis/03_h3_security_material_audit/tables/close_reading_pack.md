# H3 security / material — close-reading pack

## Topic 18 — Ordering A Gown For Her

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S13 (norm: S13)

> he’ll make sure you have a dress worthy of you.”

> i’ll order a gown for you and have it sent to the house.” “

> we’ll have to borrow their clothes.” “

> *(CELL_D, tertile=middle)* I did not mean to hurt your feelings about your attention to the womanly details of dress and appearance and wished to compensate you for the loss of the gown you’ve been wearing to work with Wilfrid.”

> *(CELL_D, tertile=end)* Mayhap if you were clothed when you attempted it, Edmee might have accepted it?” “’

> *(CELL_D, tertile=middle)* Her gown should be clean and her hair always groomed and under a veil. “

> *(CELL_C, tertile=middle)* So she’d have to go out in a damn sports bra and bike pants.

> *(CELL_C, tertile=begin)* Then put your pants on so I don’t have to wonder what that is hanging between your legs.”

> *(CELL_C, tertile=begin)* Add the crooked smile, the long, lean body in jeans and flannel, and a woman might be tempted to hang a SOLD!

> *(CELL_C, tertile=end)* She wore fuzzy purple socks, black flannel pants, and a hot pink sweatshirt that announced: T.G.I.F. THANK GOD I’M FEMALE.

### Pass A/B/C

- **A lexical:** `S13`
  - All four keyword lists centre on clothing and dress: Main lists garment types (dress, gown, jeans, shirt, suit); KeyBERT adds fitting/matching/appropriate/revealing — all descriptors of how clothing looks or fits on the body; POS adds graceful/stunning/fitting/appropriate — aesthetic evaluations of appearance; MMR adds flowing/flared/graceful/topped — visual/tactile garment descriptors. The cluster is entirely about how characters are clothed and presented, which maps to S13 (appearance_grooming) rather than S12 (status_display), because the emphasis is on the physical presentation of the body through clothing rather than social rank signalling.
- **B contextual:** `S13`
  - All sentences in this topic revolve around clothing, dress, grooming, and appearance — what characters wear, how they are dressed, providing or replacing garments, and commentary on attire. This is squarely the appearance/grooming security function (S13). There is no meaningful material provision, emotional reassurance, or status-display function dominating; the focus is consistently on the physical presentation of clothing and grooming as a social/relational concern.
- **C adjudicate:** `S13`
  - Both lexical consensus and contextual dominant converge on S13 (appearance_grooming), consistent with Taxonomy 1.6 Character Appearance & Self-Presentation. The secondary taxonomy tag (6.6 Material Glamour & Consumption) could suggest S12 or S14, but the primary function here is self-presentation and grooming rather than status display or gift-giving. S13 is the most specific and appropriate code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 77 — Haircut and Grooming Offered

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S13 (norm: S13)

> i’ll send [person] in to help you finish dressing and repair your hair.

> it’ll be good for the librarian to take down her hair and have some fun for a change.

> iffen you want a haircut and shave, megan’ll do that for an extra two bits.

> *(CELL_C, tertile=begin)* Nic was simply one of those guys who had to shave in the evening before going out on a date.

> *(CELL_C, tertile=begin)* The way he brushed his hair back and the single lock that flopped forward.

> *(CELL_C, tertile=begin)* Her eyes were light brown, and while her hair was darker than Katie’s, it wasn’t as dark as Brenna’s, even without the blond streaks she painted in every couple of months.

> *(CELL_C, tertile=begin)* Katie was mostly Irish with pale skin and reddish-brown hair.

> *(CELL_C, tertile=begin)* Francesca had the thick, dark hair from the Marcelli side of the family, but had also inherited hazel eyes and a tall, thin body from the O’Sheas.

> *(CELL_B, tertile=middle)* Tiny blonde hair still covered one hand while the other was smooth.

> *(CELL_B, tertile=end)* The rumor is they liked to drag their mates about by the hair.”

### Pass A/B/C

- **A lexical:** `S13`
  - Main keywords (hair, blonde, blond, shave, shaved, brown, black, dark, haircut, short) are overwhelmingly hair-color and hair-styling descriptors — canonical grooming/appearance vocabulary. KeyBERT reinforces with 'curled', 'attractive', 'delicate', 'patted' — physical appearance cues. MMR adds 'neatly', 'shaped', 'dried', 'blowing' — all hair-grooming process words. POS keywords (extent, contrast, inevitable, annoying, desperation) are abstract/evaluative and do not anchor a security function, yielding S0 for that rep alone, but the three-to-one majority and the coherent grooming theme across Main, KeyBERT, and MMR firmly establish S13.
- **B contextual:** `S13`
  - The overwhelming majority of sentences describe hair style, hair color, hair length, and shaving/grooming practices of characters. These are all appearance and grooming descriptors, fitting S13 (appearance_grooming). One sentence (BOOK_002_6) references dragging mates by the hair as a rumored behavior, which is more of a narrative/plot detail without a clear security function, coded S0. All other sentences are straightforwardly about physical appearance and grooming, making S13 the dominant code at well above 70%.
- **C adjudicate:** `S13`
  - Lexical consensus and contextual dominant both converge on S13 (appearance_grooming), consistent with Taxonomy 1.6 Character Appearance & Self-Presentation. No conflict between passes; the topic addresses how characters present themselves physically, which maps cleanly to S13. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 127 — Photographer Reviewing Pictures

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> my first ever but i’ll need another photographer at this rate.

> i’ll bring the pictures down.’

> let me look over the file and i’ll get back to you.”

> *(CELL_C, tertile=end)* Other images followed, a tormenting and teasing kaleidoscope—Hart and Daisy, Hart in his office, Hart on his knees, cradling her face in his hands.

> *(CELL_C, tertile=begin)* She walked over to the mantel where he kept a dozen family photographs.

> *(CELL_B, tertile=end)* I am amazed at the number of photos inside – there must be literally hundreds – some of them posed, most snapshots of me I wasn’t even aware he was taking.

> *(CELL_B, tertile=begin)* He takes photographs himself, all the time, of the docks, the city, people, things, but mostly of me.

### Pass A/B/C

- **A lexical:** `S0`
  - All keyword lists centre on photography equipment and imagery (camera, photos, pictures, photographer, files, snaps, framed, capture, stunning). While 'stunning' and 'framed' could gesture toward appearance or display, the dominant semantic cluster is photographic practice/documentation with no discernible security function — emotional, material, or status-based — being performed. No cues indicate reassurance, provision, protection, commitment, or status signalling in a romance-security sense.
- **B contextual:** `S0`
  - Topic 127 centers on photographs, portraits, and images — characters taking, collecting, or viewing pictures of each other or in galleries. None of these sentences perform a recognizable security function (emotional reassurance, material provision, protection, status display, etc.). The photographs are narrative objects or plot devices (obsession, surveillance, identity), not security-provision acts. All sentences are off-target for the security taxonomy.
- **C adjudicate:** `S0`
  - Both lexical consensus and contextual dominant agree on S0 (off_target). The taxonomy confirms this topic belongs to Character Appearance & Self-Presentation (1.6), which describes how characters look or present themselves. This is descriptive/aesthetic content, not a security function. No security work is being performed — no emotional reassurance, no material provision, no status signaling in a security-relevant sense. S13 (appearance_grooming) was considered but applies when grooming/appearance serves a protective or dependency-related security function; here the topic is purely presentational. S0 is correct and should be kept.
- **Action:** KEEP

---

## Topic 170 — Staying Close Despite Long Separation

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S2 (norm: S2)

> despite going months without talking to each other—their daily lives hectic enough that even living in the same city had never ensured regular visits—they were close.

> my guess is they’ve been seeing each other the whole time.

> they might've solved his problems together.

> *(CELL_B, tertile=end)* It was strange how they’d met, almost as if it was fated to happen sooner or later. “

### Pass A/B/C

- **A lexical:** `S2`
  - Main keywords (together, relationship, couple, between, both, them) and KeyBERT/MMR cues (closely, separated, shared, spending, separated) all point to the security function of belonging — the togetherness or separateness of a pair and their relational bond. POS keywords (separate, session, visits, scenario, stunning, exciting) are more procedural/descriptive and lean S0, but the dominant signal across three reps is relational belonging (S2). The 'separated/closely/shared' cluster confirms the security concern is about maintaining or losing a coupled bond.
- **B contextual:** `S2`
  - The majority of sentences describe the relational state between two people — friendship, mutual connection, shared space, being together, having things in common — all functioning as belonging/togetherness (S2). A few sentences are purely descriptive or narrative with no security function (S0). One sentence references commitment via mating (S4) and one references emotional support through love even in conflict (S1). S2 accounts for roughly 50% of sentences; combined with the low-probability tail sentences that dilute the signal, S2 is still the dominant code at ≥50%, and no other code approaches it, making S2 the dominant code.
- **C adjudicate:** `S13`
  - Lexical and contextual consensus both point to S2 (belonging), but the taxonomy metadata reveals the primary classification is 1.6 Character Appearance & Self-Presentation. Appearance and grooming behaviors map most precisely to S13 (appearance_grooming) rather than S2 (belonging). The secondary taxonomy (4.2 Ongoing Courtship & Everyday Relational Bonding) could suggest a belonging or bonding function, but the primary taxonomy governs here. S13 is the most specific applicable code for appearance/self-presentation content, and the courtship framing is a context rather than the security function being performed. No free-form labels were carried forward; S2 from Pass A/B is superseded by S13 upon taxonomy disclosure.
- **Action:** RETAXONOMIZE

---

## Topic 171 — Staring at Her Own Reflection

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S13 (norm: S13)

> she stood and checked her reflection in the mirror over her parents’ dresser.

> esme stared at their reflection in the glass. "

> but then she stared at her surface-repaired reflection.

> *(CELL_D, tertile=end)* She checked the mirror again, fluffed her hair, tried out a smile.

> *(CELL_D, tertile=end)* Lifting her head, she caught a look at her dripping face in the mirror.

> *(CELL_D, tertile=end)* Stepping before the mirror that hung on the bathroom door, she held the hangers under her chin.

> *(CELL_B, tertile=middle)* A mirror stood in the corner of the bedroom, and she went to check how she looked.

> *(CELL_B, tertile=middle)* She glanced in the mirror and wondered what Richard saw in her.

> *(CELL_B, tertile=begin)* The door clicked shut, and he looked in the mirror and stared at his reflection. “

> *(CELL_B, tertile=middle)* When the other women left, giving her a disparaging look, she splashed water on her face and stared at her reflection.

> *(CELL_B, tertile=end)* On the mirror pictures of his friends and Opal were placed at odd angles.

### Pass A/B/C

- **A lexical:** `S13`
  - All four keyword lists centre on self-inspection via reflective surfaces: 'mirror, reflection, rearview, checked, stared' (Main); 'gazing, peered, glimpse, studied, polished' (KeyBERT); 'stares, glimpse, stunning, unhappy, fitting' (POS); 'stares, glimpse, stunning, gazing, blinking' (MMR). The consistent pattern is a character scrutinising their own appearance — checking, evaluating, or reacting to how they look. 'Stunning' and 'unhappy' in POS/MMR confirm an evaluative appearance function. No emotional reassurance, material provision, or status-display cues dominate; the function is grooming/appearance self-monitoring, coded S13.
- **B contextual:** `S13`
  - The overwhelming majority of sentences involve characters checking their appearance in mirrors — inspecting hair, face, clothing, and overall look — which is the core function of S13 (appearance/grooming). A small number of sentences (BOOK_002_1 with a rhetorical idiom, BOOK_004_6 describing photos on a mirror, and BOOK_006_1 using 'reflection' figuratively) do not perform any security function and are coded S0. No other security functions are present.
- **C adjudicate:** `S13`
  - Lexical consensus and contextual dominant both resolve to S13 (appearance_grooming), consistent with Taxonomy 1.6 Character Appearance & Self-Presentation. No conflict between passes; the topic centers on grooming, physical self-presentation, and appearance-related content. S13 is the most specific applicable code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 192 — Peeking Through The Window

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> i stayed hidden beside the window and peeked out as grandmother and [person] arrived. “

> a sense of déjàvous washed over him as he approached the rear window of the building and peeked in through that small slant.

> he wandered over to the window on the other side of the door and peeked out the corner of the still closed drapes before letting them fall back. “

> *(CELL_B, tertile=middle)* Jenna shook her head, and then leaned forward to peer out the window. “

> *(CELL_B, tertile=begin)* She stared out her window, and fought to bring herself back under control. “

> *(CELL_B, tertile=end)* After he’d been gone about ten minutes, Jenna ventured closer and peered in the window.

> *(CELL_B, tertile=begin)* She swiveled her chair around so she could prop her legs up on the windowsill, stare at the rain, and really, truly brood.

> *(CELL_B, tertile=end)* He walked over to the window, and looked out at a very different Times Square than the one they’d just raced through the night before.

> *(CELL_B, tertile=middle)* Jenna sat next to him, her jaw tight and her lips pursed as she stared out the tinted windows while dusk fell across the city.

> *(CELL_B, tertile=end)* Ignoring the ache in his arse, Phil walked to the window and looked out. “

> *(CELL_B, tertile=begin)* Mark got up from the couch and moved to one of the windows, pulling back the curtains.

### Pass A/B/C

- **A lexical:** `S0`
  - All four keyword lists describe visual/perceptual actions (gazing, peeking, glancing, looking through windows, curtains, reflections) and spatial/sensory vocabulary. There is no security-provision function — emotional, material, or status — being performed. The topic captures a scene-setting or observational motif, not a resource transfer or reassurance act.
- **B contextual:** `S0`
  - All sentences in this topic describe characters looking out of, peering through, or standing near windows. This is purely a physical/spatial action or setting description with no security function — emotional, material, or status/appearance. No sentence conveys reassurance, protection, provision, belonging, commitment, or any other security-relevant function. The topic is entirely off-target for security coding.
- **C adjudicate:** `S0`
  - Both lexical consensus and contextual dominant converge on S0 (off_target). The taxonomy confirms this topic is about Character Appearance & Self-Presentation (1.6), with a secondary tag of Public/Travel/Leisure Spaces (8.2). Neither category performs a security function — appearance description and leisure-space setting are narrative/descriptive elements, not emotional reassurance, material provision, or status-display security acts. S13 (appearance_grooming) was considered but rejected because the topic describes appearance as characterisation, not as a security-function signal directed at a partner or audience. S0 is correct; the topic should be excluded from the security hypothesis analysis.
- **Action:** EXCLUDE_FROM_HYPOTHESIS

---

## Topic 209 — Flowers Held With Guilty Glance

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> then i look at the flowers i’m holding guiltily, as if i’ve already accepted his offer to go to new york.

> i’ll bet there are a thousand flowers then.”

> i’m sure i’ll find some more – and with owen’s research the flowers are now coming in under budget so there’s still a bit of cash to play with.’

> *(CELL_C, tertile=middle)* Four huge plants grew in wild profusion, one in each corner.

> *(CELL_B, tertile=begin)* A faint imprint of thoughts drifts toward me—color and brightness, a swirling burst of rose petals.

### Pass A/B/C

- **A lexical:** `S14`
  - Main keywords (flowers, roses, bouquet, daisies, vase, red/yellow rose) are canonical romantic gift objects. KeyBERT adds 'dozen' (dozen roses = classic romantic gift), 'bedside' (placement of flowers as token), 'porch' (delivery site). POS and MMR reinforce with 'exquisite', 'delicate', 'feminine', 'bedside', 'dozen' — all consistent with flowers as a romantic/affective token rather than practical provision, status display, or emotional reassurance per se. The security function is the gift itself as a relational token.
- **B contextual:** `S0`
  - The overwhelming majority of sentences in this topic describe flowers, plants, and decorative elements in purely descriptive or environmental terms — interior décor, garden imagery, metaphorical comparisons — with no security function. A small subset (yellow roses sent/given, rose petals as romantic gesture, sending flowers as a social courtesy) function as romantic tokens or gifts (S14), but these are a minority. No single security function reaches 70% on its own, but S0 (off-target, no security work) clearly dominates at ~75%, so S0 is the dominant code.
- **C adjudicate:** `S0`
  - Lexical consensus S14 (gift/romance token) was driven by surface co-occurrence with gift-like or token-exchange language, but the taxonomy placement in 1.6 Character Appearance & Self-Presentation (secondary: 4.2 Ongoing Courtship & Everyday Relational Bonding) indicates the topic's primary function is describing how characters look and present themselves, not the transfer of a security-providing object or gesture. Appearance and grooming (S13) could be considered, but the contextual dominant from Pass B is S0 (off-target), meaning the topic does not perform a security function for the recipient — it describes aesthetic self-presentation as part of courtship atmosphere. S0 is therefore the correct resolution. No security hypothesis is served by this topic.
- **Action:** REINTERPRET

---

## Topic 218 — Resenting Someone More Attractive

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S13 (norm: S13)

> the human in charge of maintaining his harem was moderately dishevelled from the panic, but he was, as always, poised and visually attractive.

> i think he’s still trying to prove that he is mister attractive and can make anyone fall in love with him.’ ‘

> how could i even begin to like someone who was:  a) gorgeous, thereby making me, someone who until now was considered pretty decent looking, seem, at best, perfectly average, and, at worst, like the sibling who got beaten with the ugly stick;  b) paid huge bucks to roll around in the sand making out with equally gorgeous girls while i donned a hideous fluorescent orange apron, an equally hideous lime green baseball cap with an assortment of stuffed fruit dangling from the center in a makeshift pom-pom, and honed my smoothie- making skills for six bucks an hour;  c) a veteran of rehab, probably attended more 12-step programs than all the boy bands from the nineties combined, thought nothing of totaling a hundred-thousand-dollar sports car, and even managed to expose his pearly whites in his [person] shots so that he looked like someone making a dentyne commercial instead of a criminal about to begin two hundred hours of community service, while i followed the rules or never caused my parents a day of worry, and yet they wouldn‘t even let me spend one lousy summer in europe, for god‘s sake.

> *(CELL_C, tertile=middle)* He was so handsome, so kind, so sweet and funny with his little boy.

> *(CELL_C, tertile=end)* He was, in her opinion, too handsome for his own good, too smooth for anyone else’s.

> *(CELL_C, tertile=middle)* And looked gorgeous doing it, he realized—and just a little fierce.

### Pass A/B/C

- **A lexical:** `S13`
  - All four keyword lists are dominated by physical appearance descriptors: 'handsome, gorgeous, cute, beautiful, adorable, attractive, good-looking' in Main; 'attractive, poised, described' in KeyBERT; 'attractive, features, decent' in POS; 'attractive, built, poised' in MMR. The consistent focus is on evaluating a person's physical appearance rather than emotional reassurance, material provision, or social status display. S13 (appearance_grooming) is the most specific match for lexical content centered on physical attractiveness assessment.
- **B contextual:** `S13`
  - The overwhelming majority of sentences in this topic describe characters' physical attractiveness — handsomeness, beauty, cuteness — which maps to S13 (appearance_grooming/physical appearance evaluation). A small subset of lower-probability sentences (finding a scene, assessing innocence/skill, looking the other way, receiving a look) do not perform any security function and are coded S0. S13 accounts for ~75% of sentences, well above the 70% threshold for a dominant code.
- **C adjudicate:** `S13`
  - Both lexical consensus and contextual dominant converge on S13 (appearance_grooming), consistent with Taxonomy 1.6 Character Appearance & Self-Presentation. The secondary taxonomy flag (3.2 Negative Emotions & Distress) may reflect anxiety around appearance but does not displace the primary security function, which remains grooming/appearance-related self-presentation. No split or reinterpretation is warranted; S13 is the most specific applicable code.
- **Action:** KEEP

---

## Topic 241 — Calling Someone A Stubborn Idiot

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> it’s the first time i’ve known it,” [person] said. “

> i ’ ve asked [person] to keep watch over julie and [person].

> i’ve already told this to jason, the stubborn idiot!” “

> *(CELL_B, tertile=end)* He and Kay were never meant to be and, the sooner he put the whole thing behind him, the better.

### Pass A/B/C

- **A lexical:** `S1`
  - Across all four keyword sets the dominant signals are interpersonal friction and emotional regulation: 'insulted', 'disappointed', 'pout', 'growl', 'emotionally', 'behavior', 'dealing'. 'charge', 'uncle', 'parent', 'finding' in Main suggest a guardian/authority figure dynamic, but the operative function is managing hurt feelings and reassuring after conflict, not material provision or status display. 'meal' and 'wound' in MMR are incidental; the cluster's weight sits firmly on emotional repair/reassurance (S1).
- **B contextual:** `S0`
  - The vast majority of sentences are narrative references to named characters (Jason, Kay, Chaz, Trevor) in plot-driven contexts — investigations, relationship endings, dialogue tags — with no security function being performed. Three sentences (BOOK_005_2, _4, _6) involve physical confrontation (Chaz/Judd fight) which touches on physical protection (S7), but even these are incidental plot description rather than a sustained security provision. Overall the topic is off-target for security coding.
- **C adjudicate:** `S0`
  - Pass A/B produced a lexical consensus of S1 (emotional_reassurance), likely driven by distress-adjacent vocabulary in the topic tokens. However, the taxonomy metadata places this topic squarely in 1.6 Character Appearance & Self-Presentation with a secondary signal of 3.2 Negative Emotions & Distress. The topic's primary function is descriptive/presentational — how a character looks or presents themselves — not the provision of security or reassurance to another party. The distress secondary signal reflects emotional coloring of appearance-related content (e.g., anxious self-presentation, appearance shame), not a security-provision act. Neither appearance display nor grooming-as-security (S13) is the operative function here; S13 applies when grooming/appearance serves as a security-provision mechanism between characters, which is not evidenced. The contextual dominant S0 (off_target) is therefore correct: this topic does not perform security work and should be excluded from the security hypothesis. No split is warranted because both taxonomy axes converge on non-security content.
- **Action:** REINTERPRET

---

## Topic 253 — Hair Pinned Up in Style

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S13 (norm: S13)

> she had pinned her wispy blonde hair back in a loose chignon.

> when she messed up, she’d pout and toss her golden hair over her shoulder.

> her glossy hair is piled up in loose ringlets on her head and pinned with a coral comb.

> *(CELL_D, tertile=begin)* She was thirtyish, with dark blonde hair scraped back in a ponytail, and she was attractive in a non-glossy way. ‘

> *(CELL_D, tertile=begin)* If she’d been smooth-haired you would have noticed it, but her long fur covers it up.

> *(CELL_D, tertile=end)* I suddenly noticed the short white hairs on her jumper again.

> *(CELL_D, tertile=begin)* She adjusted the diamanté barrette in Jennifer’s floor-length blonde hair. ‘

> *(CELL_A, tertile=begin)* Her sunny hair was twisted at the back of her head into a messy knot that somehow suited the angular triangle of her face.

> *(CELL_A, tertile=begin)* Her curling black hair bounced over the shoulders of her sweatshirt. “

> *(CELL_A, tertile=begin)* He turned as she came back and had the errant thought that her hair was like that—an intense spot of color. “

> *(CELL_A, tertile=end)* She’d done something to her hair, something sleek, and darkened her lips and eyes to exotic.

### Pass A/B/C

- **A lexical:** `S13`
  - All four keyword lists are dominated by hair-styling vocabulary: specific styles (ponytail, bun, braid, curls), hair attributes (blonde, blond, brown, long, loose), and grooming-state descriptors (neatly, straightened, dangling, wound, fashioned, tumbled, spilling, flowed). Words like 'feminine' and 'admire' confirm the function is appearance display/grooming rather than emotional reassurance, material provision, or social status. No cues point to any other S-code.
- **B contextual:** `S13`
  - Every sentence in this topic describes hair appearance, styling, or grooming details (hairstyles, hair color, hair accessories, makeup). This is uniformly appearance/grooming description (S13). No sentence performs emotional, material, or other security functions — all are descriptive observations of physical appearance and grooming, making S13 the clear and dominant code at 100%.
- **C adjudicate:** `S13`
  - Lexical consensus and contextual dominant both resolve to S13 (appearance_grooming), consistent with Taxonomy 1.6 Character Appearance & Self-Presentation. No conflict between passes; the topic centers on grooming, physical self-presentation, and appearance-related content. S13 is the most specific applicable code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 268 — Vivid Colors Remarked Upon

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> the colours are brighter than i’ve ever seen them.

> they’ve been preserved under piles of peat that has tanned their bodies to a dark brown, but you can see their expressions, absolutely what they looked like.

> that’s the most amazing green i’ve ever seen.”

> *(CELL_B, tertile=middle)* When I got them in there, I realized it looked kind of dumb having so much blue, so I took them back and got some gray ones.” “

> *(CELL_A, tertile=end)* She was unsure of their color, but she thought they looked to be a deep blue.

### Pass A/B/C

- **A lexical:** `S0`
  - All keyword lists center on color terms (blue, green, purple, red, black, pink, white), descriptors of appearance in a naturalistic/descriptive sense (colored, attractive, unusual, creatures, swimming, edges, bodies), and emotional/sensory words (sadness, happiness, reminds). There is no security-provision function being performed — no reassurance, protection, provision, commitment, or status signaling in a romance-security sense. The topic appears to describe physical/visual descriptions of settings or creatures, not a security resource.
- **B contextual:** `S0`
  - The overwhelming majority of sentences in this topic are references to colors (blue, red, navy, burgundy) in descriptive or conversational contexts with no security function — coded S0. A small subset (BOOK_002_1, BOOK_002_2, BOOK_002_3, BOOK_003_4, BOOK_003_5) explicitly discuss how colors or clothing suit or flatter a person's appearance, which maps to S13 (appearance/grooming). S0 dominates at ~80%, well above the 70% threshold.
- **C adjudicate:** `S0`
  - Both lexical consensus and contextual dominant agree on S0 (off_target). The taxonomy places this in Character Appearance & Self-Presentation, which maps to S13 (appearance_grooming) only if the content is performing a security function for a character. Without evidence that the appearance/grooming content is functioning as emotional reassurance, status display, or any other security mechanism, it remains descriptive/presentational rather than security-functional. S0 is the correct and most specific code here.
- **Action:** KEEP

---

## Topic 323 — Polite Address Under Distress

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> i am not [person], no matter what you’ve told the director.

> lady [person],” he said politely, “lady [person], lady [person].”

> i’ll keep praying for [person].

> *(CELL_B, tertile=begin)* Right behind them in walked Elizabeth, and I understood what had caused their reaction.

> *(CELL_B, tertile=begin)* She has to be the centre of attention, and she couldn’t stand the threat that Elizabeth posed. ‘

> *(CELL_A, tertile=end)* She had her heart set on being a viscountess and I would have made sure she did not have to wait too long to be a duchess.” “

> *(CELL_A, tertile=begin)* She probably thinks it enhances her status—that of a future viscountess.” “

> *(CELL_A, tertile=begin)* She would be an excellent hostess, which was also important now that he was a viscount.

> *(CELL_A, tertile=begin)* Penelope suddenly wondered if the madam was really married, and if so, where was her husband?

### Pass A/B/C

- **A lexical:** `S1`
  - KeyBERT, POS, and MMR converge on distress/anxious/worries/praying/assure/softened — a cluster of emotional agitation and soothing. 'Assure', 'softened', 'politely', and 'insides' point to characters managing or relieving anxiety, which is the core function of emotional reassurance (S1). Main keywords are aristocratic proper nouns and place names (georgiana, lady, matlock, netherfield, redmayne) with no clear security function, coded S0. The majority (3/4) signal S1, overriding the S0 Main rep.
- **B contextual:** `S0`
  - The vast majority of sentences are narrative references to characters named Elizabeth or brief dialogue fragments with no discernible security function, coded S0. Three sentences from BOOK_002 reference viscountess/duchess titles and status enhancement (S12), one references the social utility of a hostess role tied to a viscount's position (S15), and one sentence notes familial doting (S2). S0 dominates at 75%.
- **C adjudicate:** `S0`
  - Pass A/B produced a lexical consensus of S1 (emotional_reassurance), likely driven by distress-adjacent vocabulary in the topic tokens. However, the taxonomy metadata places this topic squarely in 1.6 Character Appearance & Self-Presentation with a secondary signal of 3.2 Negative Emotions & Distress. Appearance and self-presentation content does not perform a security function in the S1–S16 sense — it describes how characters look or present themselves, not how they provide or receive reassurance, belonging, or any other security dimension. The distress secondary tag further suggests the topic captures emotional reactions to appearance (e.g., insecurity about looks) rather than a provider-recipient security dynamic. S13 (appearance_grooming) could be considered, but S13 is reserved for grooming/appearance acts that function as care or status signals directed at another person; self-presentation distress does not meet that threshold. S0 (off_target) is therefore the correct resolution. The contextual dominant from Pass B (S0) is upheld over the lexical consensus (S1).
- **Action:** REINTERPRET

---

## Topic 347 — Saying Goodnight Before Bed

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> no, i think i’ll get to bed,” i told him, smiling weakly. “

> i’ll probably only sleep for an hour or so,” leigh said with a smile as she turned back into the room, then paused to add, “bastien asked me to have you call him when you woke up.” “

> i’ll just say good night now,” [person] says. “

> *(CELL_A, tertile=begin)* Good morning, Delaney,” he whispered huskily, close to her ear when he finally released her mouth.

> *(CELL_A, tertile=middle)* Breaking into their conversation he said, “Good morning, Shelly.

> *(CELL_A, tertile=end)* AJ and I are going to have to say good-night to everyone,” Shelly said smiling. “

> *(CELL_B, tertile=middle)* Wrapping his arms around her middle, he said, “Plan on keeping you in bed this evening, too.” “

### Pass A/B/C

- **A lexical:** `S0`
  - Main keywords (goodnight, good morning, sleep, whispered, night, evening, afternoon) suggest routine social greetings and time-of-day exchanges. KeyBERT adds politely, greeted, mumbled, assured, demanded — generic speech-act descriptors with no clear security function. POS and MMR introduce stunning, purse, entrance, sir, lady, shock — appearance/social-register cues that could hint at S12/S13, but the dominant pattern across all four reps is mundane greeting ritual rather than any sustained security provision. No single security function is consistently evidenced; the topic appears to capture conversational pleasantries and scene-setting rather than emotional reassurance, material provision, or status display as a security mechanism. S0 is the most defensible consensus.
- **B contextual:** `S1`
  - The majority of sentences are intimate greetings and farewells (good morning/night whispered to a named partner) that function as emotional reassurance — affirming presence, warmth, and affection in a romantic dyad (S1). A smaller cluster involves invitations to stay or physical closeness that signal belonging/togetherness (S2). Two sentences involve bringing refreshment or steering someone to bed as practical everyday care (S5). The remaining sentences are plain social greetings or scene-closing lines with no clear security function (S0). S1 accounts for roughly 45% of sentences, well above any single alternative, making it the dominant code.
- **C adjudicate:** `S0`
  - Lexical consensus (S0) and taxonomy placement (1.6 Character Appearance & Self-Presentation) both point away from security function. The contextual dominant S1 (emotional_reassurance) was a Pass B inference, but appearance/grooming content in romance novels primarily serves self-presentation or attractiveness signaling rather than delivering emotional reassurance as a security function. S13 (appearance_grooming) could apply if the content depicts grooming acts as care gestures, but without evidence of that caregiving dynamic the taxonomy label 'Character Appearance & Self-Presentation' indicates the topic is about how characters look or present themselves — descriptive rather than security-functional. S0 is the correct resolution; the topic does not perform a security function in the attachment/provision sense the taxonomy measures.
- **Action:** REINTERPRET

---

## Topic 354 — Threatening to Bite Someone's Nose

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S0 (norm: S0)

> i’ll send the dentist’s bill to the incredible hulk .

> i’ll try not to rot your teeth.”

> i’ll bite that fucking bloody nose you’ve got right off.

> *(CELL_B, tertile=end)* Oh, please, don't bite me," I said, doing my best not to giggle as I feigned fear.

> *(CELL_B, tertile=end)* I finished chewing the bite I'd just taken and looked up at Christopher. "

> *(CELL_B, tertile=middle)* Fangs nicked at my lip, stinging, and it only heightened the sensations.

> *(CELL_B, tertile=middle)* Lucien's hand came up around my throat, his thumb caressing the bite mark he'd just put there. "

> *(CELL_B, tertile=end)* It was almost orgasmic and each bite caused a small shiver of pleasure to work over her limbs.

### Pass A/B/C

- **A lexical:** `S0`
  - All four keyword lists centre on dental/biting vocabulary (bite, teeth, dental, dentist, gnashing, gum, chew, biting, wound, appointment). This is literal oral/dental content with no discernible security function — emotional, material, or status-related. Supporting terms (annoying, attractive, spite, memories) are generic modifiers that do not shift the cluster toward any S1–S16 security category. Coded S0.
- **B contextual:** `S0`
  - Topic 354 centers on the literal act of biting — vampire fangs, food consumption, physical sensations, and idiomatic expressions ('bit my tongue', 'bite in my words'). None of these sentences perform a security function (emotional, material, or status/appearance). They describe physical actions, sensory experiences, or figurative speech. All sentences are off-target for security coding.
- **C adjudicate:** `S0`
  - Both lexical consensus and contextual dominant converge on S0 (off_target). The taxonomy places this topic under Character Appearance & Self-Presentation (1.6) with a secondary tag of Interpersonal Non-Romantic Conflict (7.1). Neither dimension performs a security function: appearance/self-presentation here is descriptive characterisation rather than status display (S12) or grooming-as-care (S13), and the conflict framing is non-romantic and non-protective. No security provision — emotional, material, or status-based — is being enacted. S0 is confirmed; the topic should be excluded from the security-function hypothesis.
- **Action:** EXCLUDE_FROM_HYPOTHESIS

---

## Topic 364 — Noticing What He Wears

- **Taxonomy:** 1.6 — Character Appearance & Self-Presentation
- **Code:** S13 (norm: S13)

> if i had any nerve i’d go throw them open and see what he’s wearing, not that i’ve seen him in anything except shorts, t-shirts and a stupid beanie.

> he was dressed as he was at the court: [person] t‐shirt, black [person] hoodie hanging open, loose‐fitting jeans and biker boots.

> he wore a loose-fitting, blue jacket and white shirt, and the lack of a cravat exposed too much of his throat and even his chest.

> *(CELL_D, tertile=middle)* He donned his shirt and folded the kilt and girdle around his waist.

> *(CELL_D, tertile=middle)* The black gelding had three white stockings and a blaze down his forehead.

> *(CELL_D, tertile=middle)* Slender arms slid around his neck and a supple body clothed in a deep green surcoat molded to his tall frame.

> *(CELL_D, tertile=end)* Alexander’s large frame was covered from neck to calf in fur; his hands protected by leather gloves and his feet by knee high boots.

> *(CELL_D, tertile=end)* Duncan accepted from Mai, the bundled wool secured by a scrap of fabric.

> *(CELL_B, tertile=middle)* I picture him, dressed in his expensively modest suit and that waistcoat. ‘

> *(CELL_B, tertile=end)* Jeremy has removed his beige corduroy jacket too, and his cream turtle-neck sweater.

### Pass A/B/C

- **A lexical:** `S13`
  - All four keyword lists are dominated by clothing and grooming descriptors: garment types (shirt, jeans, boots, pants, sweater), colour/style markers (black, white), wearing/dressing verbs (wore, wearing, dressed, draped), and fit/condition adjectives (wrinkled, loose, neatly, polished, fitted, smoothed). POS and MMR add texture words (pattern, contrast, reveal) that still describe physical appearance rather than any emotional, practical-care, or economic function. No cues point to protection, provision, or emotional reassurance; the entire cluster describes how characters look through their clothing and grooming.
- **B contextual:** `S13`
  - The overwhelming majority of sentences describe clothing worn on the body — garments, grooming, and personal appearance — functioning as appearance/grooming signals (S13). A small subset (BOOK_001_2, BOOK_001_6) involves tending to or providing clothing as practical everyday care (S5). Three sentences (BOOK_002_3, BOOK_004_1, BOOK_004_2) emphasise expensive or status-signalling attire, coding as S12 (status display). One sentence (BOOK_001_3) describes a horse with no security function (S0). S13 accounts for ~70% of sentences, making it the dominant code.
- **C adjudicate:** `S13`
  - Lexical consensus and contextual dominant both converge on S13 (appearance_grooming), consistent with Taxonomy 1.6 Character Appearance & Self-Presentation. No conflict between passes; the topic addresses how characters present themselves physically, which maps cleanly to S13. No splitting or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 27 — Racing The Approaching Storm

- **Taxonomy:** 7.3 — Risk, Danger & External Crises
- **Code:** S7 (norm: S7)

> it’ll be dark before we know it.’’

> i don’t know if i’ll be able to get back here before the storm hits.

> it’s going to rain and we’ll be caught out in the storm.

> *(CELL_D, tertile=end)* Their lips met, and an explosion of passion took them along on a tide, the darkness that surrounded them like a blanket against the rest of the world.

> *(CELL_D, tertile=begin)* Just as they reached the spot a man strode angrily out of a neighbouring field, and even in the poor light his expression could be seen as thunderous.

> *(CELL_D, tertile=begin)* They were still driving, the high hedges making it impossible for them to see anything but the road in front of them.

### Pass A/B/C

- **A lexical:** `S7`
  - Keywords like 'rain', 'snow', 'storm', 'dark', 'dangerously' suggest protection from harsh weather conditions, which is a physical protection function.
- **B contextual:** `S0`
  - Most sentences describe weather conditions or lack of security-related actions, hence the dominant code is S0. The only other significant code is S1, which appears in two sentences describing emotional connection.
- **C adjudicate:** `S7`
  - The topic's lexical consensus of S7 (Physical Protection) aligns with the taxonomy's secondary category of 'Movement, Transit & Spatial Transition'. The dominant code S0 (off_target) is overridden as it's less specific. No manual review is required.
- **Action:** RENAME

---

## Topic 36 — Eagerly Offering to Help

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S11 (norm: S11)

> of course, i’ll help you.’

> then you’ll let me help,” frances said at once, her expression eager. “

> sure, of course, i’ll help.”

> *(CELL_B, tertile=end)* And you know I’m here to help you in any way I can.”

> *(CELL_D, tertile=middle)* Well make yourself useful,” he said. “

> *(CELL_B, tertile=end)* I’ve got to do something to help.”

### Pass A/B/C

- **A lexical:** `S11`
  - Main keywords (help, helping, assistance, helped, need) and KeyBERT/MMR cues (provided, willing, requested, task, promptly, eagerly) all point to the provision of practical assistance or task-completion help — not emotional reassurance, not money/housing, not status. POS keywords (unlikely, sadness, sentence, fault) are abstract/narrative and do not signal a security function, yielding S0 for that rep. The dominant signal across three of four reps is practical help rendered to another person (S11), so consensus is S11 despite the POS outlier.
- **B contextual:** `S11`
  - The overwhelming majority of sentences are generic offers or expressions of willingness to help ('Can I help you?', 'I'll help you.', 'I've got to do something to help.'). These function as practical assistance offers without specifying emotional reassurance, material provision, or status display — best captured by S11 (practical_help_other). A small subset ('Can I ask you a question?', 'Sure thing.') carry no discernible security function and are coded S0. S11 accounts for ~85% of sentences, well above the 70% threshold for a dominant code.
- **C adjudicate:** `S11`
  - Both lexical consensus and contextual dominant converge on S11 (practical_help_other), indicating the topic's security function is practical assistance rather than emotional reassurance. However, the taxonomy metadata assigns it to 4.6 Emotional Safety, Reassurance & Caretaking, which maps more naturally to S1 (emotional_reassurance). This mismatch between the Pass A/B codes (S11) and the taxonomy placement (S1 territory) requires retaxonomizing: the topic should be moved out of 4.6 and into the practical care/help cluster. Manual review is flagged to confirm whether the underlying tokens are genuinely practical-help content mislabeled in the taxonomy, or whether the Pass A/B coding underweighted an emotional-reassurance signal.
- **Action:** RETAXONOMIZE

---

## Topic 38 — Admitting Shared Pain

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> i’ve seen your pain.

> i've never felt that way before."

> will it make you feel better to know that i’ve got one, too?”

> *(CELL_A, tertile=middle)* That’s what it felt like—that was the exact feeling—and I’m so happy that now you were there.

### Pass A/B/C

- **A lexical:** `S1`
  - The dominant lexical cluster ('feel, feels, good, felt, feeling, better, make') centres on subjective emotional states and the act of improving them. KeyBERT adds 'hurts, experienced, worst, honestly, magical, incredibly', all of which describe felt emotional experience and its intensity. POS and MMR reinforce this with 'insides, apologize, admitted, accustomed, magical' — language of internal emotional processing, acknowledgement of hurt, and apology, which are canonical emotional-reassurance acts. No material provision, housing, money, status, or appearance cues are present. The function is soothing/validating felt distress, mapping squarely to S1.
- **B contextual:** `S1`
  - The overwhelming majority of sentences in this topic revolve around expressing, sharing, and validating internal emotional states — feelings of relief, mutual feeling, wanting to communicate feelings, and checking whether someone feels better. These all perform the security function of emotional reassurance (S1): characters are affirming, acknowledging, or seeking acknowledgment of emotional experience to provide or receive comfort and validation. A small number of sentences (BOOK_003_5 'Good sign or bad?', BOOK_004_2 sexual thought, BOOK_004_3 'Same here') are too vague or off-topic to carry a security function and are coded S0. S1 accounts for ~85% of sentences, well above the 70% threshold.
- **C adjudicate:** `S1`
  - Lexical consensus and contextual dominant both resolve to S1 (emotional_reassurance). The taxonomy placement under Ongoing Courtship & Everyday Relational Bonding with a secondary of Negative Emotions & Distress is consistent with S1 — the topic captures reassurance-seeking and comfort provision within an established or developing romantic relationship. No material or status/appearance security function is indicated. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 45 — Reassured Everything Will Be Fine

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> we’ll be ok.” “

> nadines : you’ll be ok?

> ok, maybe a zero-tolerance one, but there’s no doubt about it, you’ll be great.

> *(CELL_D, tertile=middle)* I'm fine," Amber replied quietly. "

> *(CELL_D, tertile=begin)* Your wound…'" "I'm fine."

> *(CELL_B, tertile=middle)* Is everything okay?” “

### Pass A/B/C

- **A lexical:** `S1`
  - Main keywords ('fine, okay, everything, right, honey, alright') are classic reassurance utterances. KeyBERT reinforces with 'assured, assure, smoothly, incredibly' — all signalling that a worried party is being calmed. POS 'problems, sir, lord' indicate a concern being addressed. MMR 'assure, assured, acknowledged, smoothly, problems' confirm the pattern of one party reassuring another that difficulties are under control. No material provision or status display is present; the entire cluster functions as verbal emotional reassurance.
- **B contextual:** `S1`
  - The overwhelming majority of sentences are reassurances of wellbeing ('I'm fine', 'Are you okay?', 'It's going to be all right') — verbal exchanges that function to provide or seek emotional reassurance about safety and welfare, coding as S1 (emotional_reassurance). One sentence ('Your wound…I'm fine') has a slight illness/injury connotation (S6), but the response still functions as emotional reassurance rather than practical care. S1 accounts for ~95% of the topic, well above the 70% threshold.
- **C adjudicate:** `S1`
  - Lexical consensus and contextual dominant both resolve to S1 (emotional_reassurance). Taxonomy 4.6 Emotional Safety, Reassurance & Caretaking confirms this primary classification. The secondary taxonomy 9.2 Promise, Vow & Future-Tense Speech Acts is a delivery mechanism for emotional reassurance rather than a distinct security function, so no split is warranted. S1 is the most specific applicable code; no material or status/appearance function is present.
- **Action:** KEEP

---

## Topic 52 — Talking About Dogs and Animals

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> i’ll have you know that muffy is an intelligent dog and understands more than most people give her credit for.

> it’ll also notify the other campers that there’s a bear in the area.”

> i'll be taking the dogs out for their afternoon walk, so there'll be some peace and quiet for you." "

> *(CELL_A, tertile=middle)* I’m not too versed on dog-speak but I had a feeling that meant “Hey, food’s this way.

> *(CELL_A, tertile=begin)* While I tripped over a crack in the sidewalk, stepped in dog crap or spilled mustard across my white button-down, she dabbed the corner of her mouth with a lacy napkin, made friends with stray dogs and levitated down sidewalks like Mary Poppins.

> *(CELL_A, tertile=middle)* The fence beyond them held a spray-painted sign that read “Forget Dog, Beware of Owner.”

### Pass A/B/C

- **A lexical:** `S6`
  - Main keywords (dog, pet, puppy, bear, lion) are animal/object nouns with no inherent security function on their own — S0. However, KeyBERT, POS, and MMR converge on a care-under-distress frame: 'distress', 'suffering', 'treatment', 'appointment', 'feeding', 'affection', 'guarded', 'failure', 'behalf' all point to attending to a creature's welfare during a crisis or illness episode. This maps to S6 (care_illness_crisis) applied to an animal rather than a human, but the security function being performed is the same — providing material care and attention to a vulnerable being in distress. S6 is the most specific fit over S5 (everyday practical care) because the distress/suffering/treatment cluster signals a crisis rather than routine maintenance.
- **B contextual:** `S0`
  - The overwhelming majority of sentences in this topic are simply references to dogs as characters, observations, or incidental mentions with no security function. Three sentences carry minor security signals: BOOK_003_1 involves surprising someone with a pet to cheer them up (emotional reassurance, S1); BOOK_003_3 references animals being in good hands (practical everyday care, S5); BOOK_004_2 references a dog on guard at the foot of a bed (physical protection, S7). These are isolated and do not displace the dominant off-target classification.
- **C adjudicate:** `S0`
  - Pass A/B lexical consensus landed on S6 (care_illness_crisis), but the taxonomy placement in 4.2 Ongoing Courtship & Everyday Relational Bonding (secondary: 8.2 Public, Travel & Leisure Spaces) makes clear this topic captures routine courtship and leisure interaction rather than illness or crisis care. No security function is being performed — the content reflects everyday relational bonding and public/travel contexts that do not map to any S1–S16 security provision. Contextual dominant S0 (off_target) is correct. The S6 lexical signal was likely a surface co-occurrence artifact (e.g., words like 'comfort' or 'support' appearing in courtship dialogue) rather than genuine crisis-care security work. Resolving to S0.
- **Action:** REINTERPRET

---

## Topic 59 — Mother's Disapproval Looms

- **Taxonomy:** 5.1 — Family, Kinship & Parenthood
- **Code:** S0 (norm: S0)

> does mama know you’ve left the nursery?”

> didn’t your mom tell you i’ve been having problems?” “

> mum will berate me for leaving graham at “this time”, and i’ll be forced to defend myself, something i’m not used to doing.

> *(BOOK_001, CELL_D, tertile=begin)* Oh, and then there's my mother... maybe we should focus on your bad habits." "

### Pass A/B/C

- **A lexical:** `S1`
  - The keyword cluster centres on mother-child relational terms (mother, mom, mama, daughter, mum, momma, mamma) combined with affective and communicative cues (affection, tell, taught, instinctively, memories, disappointment, fault, judging). These signal the emotional-reassurance function of a maternal figure: providing or withholding validation, comfort, and guidance. No material provision, housing, status display, or physical protection cues are present. 'Suitcase' and 'ribs' are incidental nouns that do not shift the dominant function. The cluster consistently points to S1.
- **B contextual:** `S0`
  - The overwhelming majority of sentences in this topic are references to mothers and fathers as family figures, expletives, or neutral mentions with no security function — coded S0. A small subset (carrying a mother's picture, wishing a mother could see you, and mothers giving formative advice/statements) perform mild emotional reassurance or emotional bonding functions (S1), but these are a minority. No material or status security functions are present. S0 dominates at ~75%.
- **C adjudicate:** `S0`
  - Pass A/B lexical consensus landed on S1 (emotional_reassurance), but the taxonomy metadata places this topic firmly in Family, Kinship & Parenthood with a secondary axis of Negative Emotions & Distress. The content describes familial grief or parental-loss dynamics rather than a dyadic reassurance function between romantic partners. S1 requires an agent providing reassurance to a recipient within a security-seeking frame; here the emotional content is expressive/narrative (characters experiencing distress about family/kin) rather than functional security provision. Contextual dominant S0 (off_target) is therefore correct: the topic does not perform a security function in the romance-security taxonomy and should be excluded from hypothesis testing about security provision.
- **Action:** REINTERPRET

---

## Topic 61 — Planning to Exchange Rings

- **Taxonomy:** 8.3a — Commitment Symbols & Love Tokens
- **Code:** S4 (norm: S4)
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

- **A lexical:** `S14`
  - All four keyword lists centre on rings, necklaces, diamonds, gold, and engagement jewellery — physical objects exchanged as romantic or commitment tokens. KeyBERT adds 'promises' and 'engaged', confirming the token/pledge function. POS and MMR retain 'precious', 'glint', 'polished', 'worn', reinforcing the object-as-gift frame. The dominant security function is the romantic/commitment token (S14), not mere status display (S12) nor practical provision.
- **B contextual:** `MIXED`
  - Topic 61 centres on jewellery and body adornment in a romance context. The dominant split is between S14 (gift/romantic token — rings presented as symbols of union, ruby gifts, butt-plug described as exquisite craftsmanship with sentimental value) and S13 (appearance/grooming — wearing jewellery, nipple rings, how items look on the body). No single code reaches 70%, so MIXED is returned. One sentence (BOOK_001_2) involves a lancet prick suggesting a minor medical/ritual act (S6), and BOOK_002_14 is a bare name fragment with no security function (S0).
- **C adjudicate:** `S4`
  - Pass A/B yielded a lexical consensus of S14 (gift_romance_token) and a contextual dominant of MIXED. Taxonomy 8.3a (Commitment Symbols & Love Tokens) clarifies the functional role: the tokens in this topic cluster are not primarily about the gift-giving act itself but about what the token *signals* — a binding promise, a pledge of permanence, or a reconciliation seal (secondary taxonomy 4.5). The security function being performed is therefore commitment security (S4): the object (ring, token, keepsake) serves as a material anchor for the psychological assurance that the relationship is stable and enduring. S14 captures the vehicle; S4 captures the function. Because the task requires function over object, S4 is the dominant code. MIXED is not warranted because both the lexical and contextual signals converge on commitment-assurance once the taxonomy context is applied; the apparent tension between S14 and MIXED dissolves when the token is read as a commitment symbol rather than a standalone romantic gesture.
- **Action:** REINTERPRET

---

## Topic 65 — Declaring A True Partnership

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** S4 (norm: S4)

> what we’ve been though together, the way we’ve been there for each other ... we have a true partnership, a true love, and if that sounds stupid and romantic, then i don’t care.”

> we’ve been together forever, and what if it takes us years?”

> i’ll do that,” he said softly, “we’ve got a date.”

> *(CELL_C, tertile=begin)* And if we do go out, then I have to deal with all the men swarming around wanting a taste of your sex magic! ”

> *(CELL_C, tertile=begin)* Or was it just an accident that we dated and he found the schema?”

> *(CELL_C, tertile=end)* This is something with pure intentions, open emotions, and a reciprocation that will never cause harm to either of us.” “

> *(CELL_C, tertile=begin)* It’s just … I know I am nothing but a big disappointment to both of you.

### Pass A/B/C

- **A lexical:** `S4`
  - Main keywords (date, dating, together, dated, two, we) signal a romantic pairing in progress; KeyBERT adds 'engaged' and 'partners', pointing to formalising a relationship bond; POS reinforces with 'partners', 'potential', 'fitting'; MMR adds 'officially', 'intend', 'forming' — all cues about establishing or confirming relational commitment rather than practical provision, protection, or status display. The cluster consistently describes the security function of defining and securing a romantic partnership.
- **B contextual:** `S2`
  - The topic centers on romantic pairing and shared social presence — being seen together in public, going on dates, having a history of togetherness. The dominant security function is S2 (belonging): sentences repeatedly reference being together, shared history, and social coupling. S4 (commitment_security) appears in sentences about breaking up, whether a relationship can continue, or whether dating is real/stable. S3 appears once for mutual trust/intentions. S1 once for emotional reassurance about disappointment. Three sentences are off-target (commands or neutral questions with no security function). S2 is dominant at ~45%, well above any single alternative.
- **C adjudicate:** `S4`
  - Pass A/B produced a split between S4 (commitment_security) and S2 (belonging). Taxonomy placement in 4.5 Reconciliation, Commitments & HEA is decisive: the primary security function being performed is the establishment or restoration of durable relational commitment (HEA/HFN resolution), which maps squarely to S4. S2 (belonging) is a downstream emotional benefit of that commitment rather than the operative security function. The secondary taxonomy tag 4.2 Ongoing Courtship & Everyday Relational Bonding is consistent with S4 as the anchor — everyday bonding here serves to consolidate commitment rather than signal group membership. No free-form labels remain; S4 is retained as the single dominant code.
- **Action:** REINTERPRET

---

## Topic 75 — Talking About Being A Father

- **Taxonomy:** 5.1 — Family, Kinship & Parenthood
- **Code:** S0 (norm: S0)

> no matter how many disagreements you’ve had, he’s still your dad.”

> what kind of dad is this going to make me after i’ve missed so much in his life?”

> i’ve been waiting to join dads and daughters for ages, marni.

> *(CELL_B, tertile=middle)* A pity you did not tell your father so,’ he added silkily. ‘

> *(CELL_B, tertile=begin)* Plus it had also been made clear to me that your father had very different plans for you.

> *(CELL_C, tertile=end)* But if the leaders of the community find out my son brought you here, it will not go well for him.”

### Pass A/B/C

- **A lexical:** `S1`
  - All four keyword lists converge on father-child relational dynamics: Main has 'dad, father, daddy, son, fathers'; KeyBERT has 'emotionally, affection, memories, involved'; POS has 'affection, anxiety, determination, willing'; MMR has 'emotionally, affection, heal'. The dominant security function is emotional reassurance — a parent (or parental figure) providing or being asked to provide emotional validation, affection, and relational presence to a child or partner. 'Anxiety' and 'heal' reinforce an emotional-need context rather than material provision or status display.
- **B contextual:** `S0`
  - All sentences in this topic reference father/dad/son figures in narrative or conversational contexts — identifying family members, expressing concern about a parent's reaction, or relaying information about fathers. None of these sentences perform a security function (emotional reassurance, material provision, protection, status display, etc.). They are purely referential mentions of paternal/filial relationships without any security-provision dynamic being enacted. Topic 75 is off-target for security coding.
- **C adjudicate:** `S0`
  - Lexical consensus (S1) reflects surface-level emotional language, but the contextual dominant (S0) is more accurate given the taxonomy placement under Family, Kinship & Parenthood with secondary Ambivalence & Internal Conflict. The topic appears to center on family/kinship dynamics and internal conflict rather than a discrete security-provision function. No clear security behavior (emotional reassurance, material provision, status display, etc.) is being enacted between characters; instead, the content describes relational ambivalence within family structures. S0 (off_target) is therefore the correct resolution. Manual review is flagged because the S1 lexical signal is non-trivial and an analyst should confirm that no embedded security function (e.g., S2 belonging or S4 commitment_security) is being obscured by the ambivalence framing.
- **Action:** REINTERPRET

---

## Topic 81 — Mentioning A Brother

- **Taxonomy:** 5.1 — Family, Kinship & Parenthood
- **Code:** S0 (norm: S0)

> i have a brother, in case you’ve forgotten.

> i’m sure you’ve deduced by now that i’m not like my brothers.

> i’ve brought my brother with me.

> *(BOOK_002, CELL_A, tertile=middle)* He’s closer to me than a brother and he loves you as much as I do.” “

### Pass A/B/C

- **A lexical:** `S2`
  - Main keywords (brother, brothers, siblings, sibling, older) anchor the topic firmly in family-kinship identity. KeyBERT cues (related, introduce, reminds, follows) reinforce recognition and acknowledgment of family ties. POS and MMR cues (affection, appropriate, treatment, annoying) describe the relational texture of sibling bonds — being accepted, recognized, and emotionally placed within a family unit. The dominant security function is belonging (S2): the sense of being part of a defined family group, not practical care, protection, or status display.
- **B contextual:** `S0`
  - The overwhelming majority of sentences in this topic are simple references to sibling identity ('He's my brother,' 'Which brother?', 'Are you brothers?') with no security function being performed. They are identification or clarification statements about family relationships. One sentence (BOOK_002_4) expresses closeness and love comparable to brotherhood, which touches on belonging (S2), but this is a single outlier. The topic as a whole is off-target for security coding, dominated by S0 at ~95%.
- **C adjudicate:** `S0`
  - Lexical consensus S2 (belonging) reflects surface-level family/kinship language, but the contextual dominant S0 (off_target) is correct: the taxonomy places this firmly in Family, Kinship & Parenthood as a relational/structural category rather than a security-function cluster. Family membership and parenthood roles are not themselves performing a security function in the romance-novel sense — they are the relational context, not the mechanism of reassurance, protection, provision, or commitment. No specific S1–S16 security function is being enacted. S0 is the appropriate resolution.
- **Action:** REINTERPRET

---

## Topic 83 — Reassured About Eating Regularly

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S5 (norm: S5)

> i've eaten every few hours.

> of course, i’ve never eaten one.”

> and then you'll return late again… you won't need to do that—be late—because you've eaten."

> *(CELL_D, tertile=begin)* Then I’ll go hungry because I’m not eating with you.’ ‘

> *(CELL_B, tertile=end)* Wow, you really must have been hungry.”

> *(CELL_B, tertile=end)* Oh, I really was starving. “

### Pass A/B/C

- **A lexical:** `S5`
  - All four keyword lists centre on eating, hunger, food, meals, feeding, and appetite — the everyday act of ensuring someone is fed. 'Hungry', 'starving', 'skipped', 'eagerly', 'meal', 'feeding', 'eaten' all point to routine nutritional care rather than crisis illness (S6), money provision (S8), or emotional reassurance (S1). 'Regular' and 'previous' in POS reinforce habitual/daily feeding patterns. This is squarely practical everyday care (S5).
- **B contextual:** `S0`
  - The overwhelming majority of sentences are simple statements or questions about personal hunger states (hungry, starving, not hungry), with no security function being performed — they are descriptive dialogue about appetite, not acts of care or provision. A small subset (BOOK_003_1, BOOK_003_2, BOOK_004_1) involve one character directing or providing food to another, which qualifies as everyday practical care (S5). The topic as a whole is dominated by off-target hunger-state utterances with no meaningful security function, yielding S0 as dominant at ~85%.
- **C adjudicate:** `S5`
  - Pass A/B lexical consensus landed on S5 (practical_care_everyday), while contextual dominant from Pass B was S0 (off_target). The taxonomy placement in 4.6 Emotional Safety, Reassurance & Caretaking suggests the topic may carry emotional-safety content (S1), but without topic terms or documents to inspect, the lexical signal of everyday practical care (S5) is the strongest concrete anchor. S0 is overridden because the taxonomy explicitly places this in a caretaking category, indicating it is doing security work of some kind. S5 is retained over S1 because the lexical consensus reflects tangible caretaking acts rather than purely reassurance language. Manual review is flagged to confirm whether the dominant signal is routine practical care (S5) or emotional reassurance (S1), given the tension between the two passes.
- **Action:** REINTERPRET

---

## Topic 86 — First Name Used at Last

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> i’ve known you for two whole years, and that is the first time you’ve ever called me by my first name.”

> you’ve outgrown that nickname.” “

> just between you and me, i’ve been working on a catchy superhero name.

> *(CELL_B, tertile=middle)* Doesn't it bother you in the least that you don't really know him?" "

### Pass A/B/C

- **A lexical:** `S1`
  - Main keywords (name, nickname, real, knew) point to identity/naming exchange with no clear security function on their own (S0). However, KeyBERT, POS, and MMR converge on affective cues — embarrassment, flushed, painful, shout, admit — surrounding a naming/introduction scene. The emotional distress signals (embarrassment, painful, flushed) indicate the scene is doing emotional reassurance work: managing vulnerability around identity disclosure. No material or status-display function is evident. Consensus tips to S1 on the weight of three representers showing emotional regulation around a name reveal.
- **B contextual:** `S0`
  - The overwhelming majority of sentences are simple name exchanges or introductions (asking or stating names), which perform no security function and are coded S0. A small cluster (BOOK_001_2, _4, _5, _6) involves assertions about knowing or not knowing a person, which touches on trust/reliability (S3), but even these are borderline. The topic as a whole is dominated by off-target name-identification dialogue with no clear security function, making S0 the dominant code.
- **C adjudicate:** `S0`
  - Pass A/B lexical consensus landed on S1 (emotional_reassurance), but the taxonomy placement in 4.2 Ongoing Courtship & Everyday Relational Bonding with a secondary axis of 9.1 Dialogue Delivery & Speech Tags indicates the topic captures narrative craft mechanics (how characters speak, speech attribution) rather than a security-provision function. Courtship banter and speech tags do not constitute a character providing emotional reassurance as a security resource; they are stylistic/structural features of romantic interaction. Contextual dominant S0 (off_target) is correct. The S1 signal in Pass A/B was a surface-level lexical association with warm or affectionate language, not a genuine security function. No security construct is operative here.
- **Action:** REINTERPRET

---

## Topic 93 — Meal Plans Casually Arranged

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> that’ll wait ’til after supper, though.” “

> i’ll go get started on lunch,” clark offered.

> i’ll show you over dinner.” “

> *(CELL_C, tertile=end)* What kind of host would I be to let you go all day without a proper meal?

> *(CELL_C, tertile=middle)* What happened to Reichen finding you some dinner downstairs?

> *(CELL_C, tertile=end)* It seemed only fitting that I treat you to one of the city‘s finest dinners.

> *(CELL_D, tertile=begin)* He’d sat with her for hours going over the catering menu for the reception, listening to her gripe and moan about what they would serve their guests.

### Pass A/B/C

- **A lexical:** `S5`
  - All four keyword lists converge on shared meals and meal planning (dinner, lunch, supper, eat, having, meal, eaten) combined with scheduling cues (tonight, tomorrow, appointment, arranged, planning). This is routine domestic provisioning — everyday practical care through food — not crisis care, not gifting, not status display. S5 is the most specific fit.
- **B contextual:** `S2`
  - The topic centres on shared meals — invitations to dinner/lunch and arranging to eat together. The majority of sentences (BOOK_003, BOOK_004, BOOK_005_1) are invitations or arrangements to share a meal, functioning as belonging/togetherness signals (S2: social bonding through shared time). A substantial minority (BOOK_001, BOOK_002_1, BOOK_005_2) involve a host or partner ensuring someone is fed or catered for, which is practical everyday care (S5). S2 reaches ~60% and is the dominant function, reflecting the topic's core pattern of meal-sharing as relational belonging rather than mere sustenance provision.
- **C adjudicate:** `S2`
  - Pass A/B lexical consensus landed on S5 (practical_care_everyday), but the taxonomy placement in 4.2 Ongoing Courtship & Everyday Relational Bonding signals that the primary security function is fostering a sense of belonging and relational inclusion rather than instrumental caregiving. S2 (belonging) is the more specific fit: the everyday props and communication media (taxonomy 8.3b) serve as vehicles for maintaining relational closeness and mutual recognition, not for meeting practical needs. S5 would require evidence of task-oriented provision; absent that, S2 is dominant. No free-form labels remain; all prior codes are mapped to valid S-codes.
- **Action:** REINTERPRET

---

## Topic 96 — Confessing Long-Standing Worry

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S1 (norm: S1)

> i’ve been worried about you, [person].

> i’ve worried about you since i was twelve.

> i’ve been worried about you.” “

> *(CELL_D, tertile=middle)* You grew up worrying about having your basic needs met.

> *(CELL_D, tertile=middle)* Don't beat yourself up about it.

> *(CELL_B, tertile=begin)* We didn’t want to worry you.”

### Pass A/B/C

- **A lexical:** `S1`
  - All four keyword lists centre on anxiety/worry vocabulary (worry, worried, concern, worrying, concerned, fears, bothering, bothered) paired with reassurance cues (assure, 'nothing', 'don't'). The dominant security function is one partner soothing or addressing the other's emotional distress — classic emotional reassurance (S1). No material, housing, or status cues are present.
- **B contextual:** `S1`
  - All sentences revolve around the expression, management, or dismissal of worry and concern between characters — reassuring others not to worry, confessing worry about someone, or deflecting concern. This is uniformly emotional reassurance (S1): the security function is soothing anxiety and providing emotional comfort, with no material, practical, or status dimensions present.
- **C adjudicate:** `S1`
  - Lexical consensus and contextual dominant both resolve to S1 (emotional_reassurance), consistent with Taxonomy 4.6 Emotional Safety, Reassurance & Caretaking. The secondary taxonomy 3.2 Negative Emotions & Distress is compatible as the context in which reassurance is sought, not a competing security function. No ambiguity requiring MIXED or further splitting. S1 is the most specific applicable code.
- **Action:** KEEP

---

## Topic 112 — Desperate Need For A Job

- **Taxonomy:** 6.4 — Economic Precarity, Security & Dependency
- **Code:** S0 (norm: S0)

> i’ve never worked in such a beautiful place and i want this job so badly.”

> i've lost my job, and i'm not going to find another one in elliot or prestonsburg or probably even in auburn.

> you’ve got a hell of a career ahead of you.”

> *(CELL_D, tertile=begin)* I cannot speak for others, but I know that my Olaf is well paid for his work, and has a dry, comfortable place to live and sleep, and that our table groans with food.

> *(CELL_B, tertile=middle)* He offered me a job in the office, you know, filing, typing, secretarial work.” “

### Pass A/B/C

- **A lexical:** `S1`
  - Keywords like 'reassuring', 'anxiety', and 'ability' suggest emotional reassurance, outweighing the material aspect of 'job' and 'work'.
- **B contextual:** `S8`
  - The dominant code is S8 (money_provision) as most sentences discuss jobs, employment, and earning a living.
- **C adjudicate:** `S8`
  - The topic's dominant code is S8 (money_provision), which aligns with the taxonomy of Economic Precarity, Security & Dependency. No manual review is required.
- **Action:** KEEP

---

## Topic 116 — Sharing A Meal Together

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> [person] dipped his spoon into the ice cream dish once again, and my mouth opened in anticipation.

> i’ll finish the carrots up while you wash those,” he said, nodding to the potatoes she held as he reached for the bowl of veggies she had left unfinished.

> i’ll get that,” clarissa said, whisking mandy’s empty plate away and depositing it on the counter along with her own before mandy could say a word. “

> *(CELL_A, tertile=begin)* She reached across the table and pulled the pie plate away from him before he could sink his fork in.

> *(CELL_A, tertile=begin)* She dropped a generous scoop of it on Jake’s pie and set it in front of him. “

> *(CELL_D, tertile=end)* Bacchus chased it with his forked tongue, catching the droplets before they hit the sheets. “

> *(CELL_B, tertile=middle)* Finishing off his sandwich in a couple of bites, he reached for another and checked to see how she was doing. “

> *(CELL_B, tertile=middle)* Grabbing a couple of napkins, he moved on, snagging a bag of chips to round out the meal.

> *(CELL_B, tertile=end)* He gave her the ice cream and the napkin he‟d held at the ready.

### Pass A/B/C

- **A lexical:** `S5`
  - Main keywords (plate, fork, sandwich, bowl, bread, bacon, food) and KeyBERT terms (meal, eaten, feeding, tasted, preparing) all point to routine food preparation and consumption — a classic everyday practical-care function. MMR reinforces this with action verbs (dipped, stirred, preparing, eagerly) describing the act of eating/feeding. POS keywords (irritation, enthusiasm, anticipation, warmth) are affective descriptors of the scene rather than security-function signals, coding S0 in isolation, but the dominant signal across three reps is unambiguous everyday material care (S5).
- **B contextual:** `S0`
  - The topic clusters around eating utensils, plates, napkins, and mealtime actions. The vast majority of sentences describe physical gestures with cutlery or tableware (tapping a fork, dropping a spoon, swiping silverware) with no security function — these are S0 off-target. A small subset (BOOK_001_6, BOOK_003_1, BOOK_003_2, BOOK_003_4, BOOK_003_6) show one character preparing or delivering food/snacks to another, which qualifies as S5 practical everyday care. No emotional reassurance, protection, money, housing, or status functions are present. S0 dominates at ~75%.
- **C adjudicate:** `S0`
  - Lexical consensus S5 (practical_care_everyday) reflects surface-level domestic/routine vocabulary, but the contextual dominant S0 (off_target) is correct given the taxonomy placement in 4.2 Ongoing Courtship & Everyday Relational Bonding. The topic's primary function is relational bonding and courtship maintenance, not security provision of any kind. Everyday routines here serve narrative intimacy-building rather than meeting a security need (emotional, material, or status). S5 would require the acts to function as care directed at a vulnerability or dependency; courtship bonding does not meet that threshold. Resolving to S0.
- **Action:** REINTERPRET

---

## Topic 119 — Offering to Keep Her Safe

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S7 (norm: S7)

> come on, i’ll protect you.”

> you’ll protect me?” “

> i can protect you from crystal, but you’ll have to let me.

> *(CELL_D, tertile=begin)* I’m your man for getting you to the point of passing out, if you ever want to take that risk.”

> *(CELL_C, tertile=middle)* At least in LA you’d both have protection; you know my security guys are some of the best in the business.

> *(CELL_C, tertile=end)* I didn’t think security would leave you standing out here like this.’ ‘

### Pass A/B/C

- **A lexical:** `S7`
  - All four keyword lists converge on physical-protection semantics: Main has 'safe, protect, protection, dangerous, protecting, keep, defend, safety'; KeyBERT adds 'protect, guarded, secure, threat, dangerously'; POS reinforces with 'protect, secure, threat, precious' (something/someone worth defending); MMR echoes 'guarded, dangerously, threat, determination' (resolve to shield). The cluster consistently frames a protector-figure actively shielding someone from danger/threat, which is the core function of S7 physical_protection. No emotional-reassurance, housing, or status cues dominate.
- **B contextual:** `S7`
  - All sentences across all books centre on physical protection and safety — explicit promises to protect, assurances of being safe, references to security personnel, and missions to eliminate threats. This is uniformly S7 (physical_protection). No material-provision, emotional-reassurance, or status functions are present; the topic is entirely about keeping characters physically safe from danger.
- **C adjudicate:** `S7`
  - Both lexical consensus and contextual dominant from Pass A/B converge on S7 (physical_protection). The taxonomy metadata places this under 4.6 Emotional Safety, Reassurance & Caretaking, which would suggest S1 or S6, but the adjudication instruction requires resolving to the Pass A/B signal when it is consistent. S7 and S1 can co-occur in romance contexts (e.g., a hero physically shielding a heroine also provides emotional reassurance), creating genuine tension with the taxonomy label. However, because both prior passes independently coded S7 and the taxonomy assignment appears to reflect a broader categorical bucket rather than the specific security function evidenced in the topic tokens, S7 is retained as the dominant code. Manual review is flagged because the taxonomy mismatch (4.6 Emotional Safety vs. physical protection) warrants a human check to confirm the topic's lexical content is primarily about bodily safety rather than soothing/reassurance.
- **Action:** RETAXONOMIZE

---

## Topic 128 — Confessing How Much You've Missed

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** S2 (norm: S2)

> i’ve missed most of his life already.

> and, god, how i’ve missed this.”

> i’ve come to realize that you are the one thing in my life i don’t want to miss.

> *(CELL_C, tertile=middle)* The suckhead you brought back with you here tonight…I saw it all.”

> *(CELL_C, tertile=end)* While I was in there, I also brought you something I thought you might be missing.”

### Pass A/B/C

- **A lexical:** `S0`
  - Main keywords (miss, missed, missing, misses) strongly evoke longing/absence, which could gesture toward S1 emotional reassurance, but the remaining lists offer no reinforcing security function. KeyBERT terms (hi, sir, escaped, honestly, repeated, solemnly) are procedural/speech-act words with no security signal. POS terms (handful, precious, voices, elevator, opportunity, pieces) are generic nouns with no consistent security frame. MMR terms (solemnly, breathlessly, thoughtfully, elevator, repeated, considering, pressing) are adverbs and verbs of manner/action, not security provision. Without corroboration across lists, the topic does not reliably perform a security function and is best coded S0.
- **B contextual:** `S2`
  - The overwhelming majority of sentences express longing for and reunion with loved ones — partners, family members, close others — functioning as belonging/connection security (S2). Expressions like 'I missed you so much,' 'We've missed you,' and 'I missed my family' all signal the security function of felt belonging and relational presence. A minority of sentences (literal misses of a ball, a physical action, or an orgasm) are off-target (S0) with no security function. S2 reaches ~70%, making it the dominant code.
- **C adjudicate:** `S4`
  - Pass A/B produced a lexical consensus of S0 (off-target) and a contextual dominant of S2 (belonging). The taxonomy anchor — 4.5 Reconciliation, Commitments & HEA — resolves the ambiguity: the security function being performed is the establishment or restoration of a durable relational bond (HEA/HFN endpoint), which maps most precisely to S4 (commitment_security) rather than the more diffuse S2 (belonging). S2 captures a sense of being included or accepted, whereas S4 captures the forward-looking guarantee of the relationship's permanence that reconciliation and commitment scenes specifically enact. The secondary taxonomy tag (3.1 Positive Resolution, Relief & Emotional Payoff) is consistent with S4 — the emotional payoff here derives from the security of knowing the commitment is sealed, not merely from belonging per se. S0 is overridden because the topic is clearly doing security work within the romance narrative frame.
- **Action:** REINTERPRET

---

## Topic 137 — Pitching A Career Change

- **Taxonomy:** 6.2 — Work & Professional Identity
- **Code:** S0 (norm: S0)

> [person], i’ve been giving this a lot of thought, and i think it’s time i moved onto hard news.

> ryan smiled in a way that told her he wasn't that dense, and said, "i'll keep digging here, but maybe not with as much enthusiasm, but if marc gets to be a bore, let me know." "

> i'll come too—" [person] makes to get up from the bed. "

> *(CELL_D, tertile=middle)* He was annoyed at having to repeat himself—that was obvious. “

> *(CELL_D, tertile=end)* Nash ghosted a grin at the lethal sound of the words and wondered if he’d left the other man with the most dangerous of them all.

> *(CELL_B, tertile=begin)* Abby moved toward him in anticipation, but he shook his head and smiled. “

> *(CELL_A, tertile=begin)* Rufus was staring into Michael’s bag with a weird expression on his face. “

> *(CELL_A, tertile=begin)* Rufus’s expression didn’t magically change from annoyed to turned on, so he was fairly sure he’d missed and grabbed a knee or something. “

### Pass A/B/C

- **A lexical:** `S1`
  - The keywords 'giggled', 'willing', 'playfully', 'urged', 'blurted', 'approached', 'warmth', and 'enthusiasm' suggest emotional reassurance and connection.
- **B contextual:** `S0`
  - Most sentences do not explicitly show any security function, so they are coded as S0. A few sentences show belonging (S2) but do not reach the 70% threshold.
- **C adjudicate:** `S1`
  - The topic's lexical consensus of S1 (emotional_reassurance) aligns with the contextual dominant of S0 (off_target), indicating that the topic primarily focuses on emotional support and reassurance, which is the most specific security function in this context.
- **Action:** KEEP

---

## Topic 140 — Demanding Answers Before Departure

- **Taxonomy:** 6.6 — Material Glamour & Consumption
- **Code:** S0 (norm: S0)

> before [person] could growl—david at least knew him well enough to know he would—[person] touched [person] leg and said, “right now i’ll settle for some answers.”

> it’s kind of amazing that a few simple words from [person] can have this effect, and [person] doesn’t think he’ll tire of it, ever.

> who knows what you'll be walking into on benezet , much less how long you'll be gone."

> *(CELL_B, tertile=begin)* Ben’s doleful expression said that’s exactly what he feared.

> *(CELL_B, tertile=end)* She’d told Ben about her engagement, and he’d been apoplectic at first, wanting to come immediately and “rescue” her.

### Pass A/B/C

- **A lexical:** `S14`
  - The keywords 'benjamin', 'hutton', 'spencer', 'morrison', 'jim' suggest different characters, and 'had' implies a past action. 'Scenario', 'strolled', 'thinks', 'asks', 'anxious', 'possibilities', 'remarked', 'poised', 'growl', 'urge' suggest a social interaction or scenario. 'Extent', 'behalf', 'irritation', 'hopeful', 'enormous', 'session', 'fashioned', 'notion' suggest a discussion or negotiation. None of these directly relate to emotional, material, or status/appearance security functions, but 'gift_romance_token' (S14) is suggested by the use of 'had' with character names, implying a past gift or token of affection.
- **B contextual:** `S0`
  - Most sentences are either calling out or referring to 'Ben', which does not indicate any specific security function. A few sentences hint at emotional reassurance (S1), but they do not reach the 70% threshold.
- **C adjudicate:** `S14`
  - The topic revolves around romantic gestures and gifts, which aligns with the 'gift_romance_token' security function.
- **Action:** RENAME

---

## Topic 141 — Warned to Use His Title

- **Taxonomy:** 6.3 — Shared Workplaces & Professional Interaction
- **Code:** S0 (norm: S0)

> i’ll have it my own way,” branch said to [person]’s back. “

> [person] can handle himself but he looks like a tiny wee thing in comparison to us so they’ll see him as easy pickings.”

> you'll call me director and you'll like it," lincoln warned [person], a wide grin covering his face.

> *(CELL_B, tertile=middle)* Max i m us l oo k ed at t he coun t er t o m a k e su r e no one e l se w as t he r e be f o r e he be g an t o de m a t e ri a li z e. H e r a i sed t he paper back up t o co v er h i s f ea t u r es. “

### Pass A/B/C

- **A lexical:** `S1`
  - Keywords like 'tickles', 'smirk', 'chuckle', 'warmth' suggest emotional reassurance.
- **B contextual:** `S0`
  - Most sentences are neutral or off-target (S0), with a few discussing commitment and security (S4) related to Max's mother and health.
- **C adjudicate:** `S1`
  - The topic's lexical consensus of S1 (emotional reassurance) is more specific and appropriate than the contextual dominant of S0 (off-target). The topic focuses on emotional support and reassurance in a workplace setting, which aligns with the taxonomy of Shared Workplaces & Professional Interaction.
- **Action:** RENAME

---

## Topic 161 — Reassuring Squeeze on The Shoulder

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

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

- **A lexical:** `S1`
  - Main keywords are character names and a place name (noah, phan, cam, tobias, cameron, beaumont, ark) with no clear security signal, pointing to S0. However, KeyBERT, POS, and MMR all converge on affective-regulation vocabulary: 'reassuring' and 'calming' appear across all three lists, supported by 'praying', 'shivered', 'fiercely', 'clenched', 'emotions' (KeyBERT), 'squeeze', 'slightest' (POS), and 'snaps', 'bursting', 'blinking' (MMR). This cluster describes a character actively soothing or steadying another's emotional state — the core function of S1 emotional_reassurance. The Main list's S0 signal is overridden by the strong three-list consensus on emotional calming cues.
- **B contextual:** `S0`
  - All sentences in this topic are character name references, descriptions of stubbornness/animalistic tendencies, theological/biblical exposition, or brief action fragments. None perform any security function (emotional reassurance, material provision, status display, etc.). Every sentence is off-target for security coding.
- **C adjudicate:** `S0`
  - Lexical Pass A/B converged on S1 (emotional_reassurance), but contextual dominant from Pass B is S0 (off_target). The taxonomy metadata places this in 4.6 Emotional Safety & Reassurance with a secondary tag of 5.1 Family/Kinship/Parenthood. The family/kinship secondary tag is the deciding factor: if the reassurance function is operating within a parental or sibling relationship rather than a romantic dyad, it falls outside the romance-security hypothesis scope. S1 requires the security function to be delivered within a romantic attachment context; familial caretaking does not meet that criterion. Contextual S0 therefore overrides lexical S1. Manual review is flagged to confirm whether any tokens in this topic cluster are unambiguously romantic rather than familial before final exclusion.
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

- **A lexical:** `S7`
  - Main keywords (police, cop, officer, enforcement, authorities) point directly to law-enforcement agents whose narrative function is physical protection/safety. KeyBERT reinforces this with 'protect', 'weapons', 'secured', 'evidence' — all physical-safety cues. POS and MMR echo 'weapons', 'secured', 'task', 'dealing', 'stops', consistent with protective/enforcement action rather than emotional reassurance, material provision, or status display. No emotional-comfort or resource-provision signals dominate; the cluster is squarely about physical safety and protection.
- **B contextual:** `S7`
  - The topic clusters around law enforcement (police/cops) and workplace officer hierarchy. BOOK_001 and BOOK_005 sentences all reference calling or identifying police/cops in contexts of threat response or protection — coded S7 (physical protection). BOOK_004 sentences focus on officer rank, regulations, superior orders, and a female officer's standing among colleagues — coded S15 (workplace status). S7 accounts for ~70% of sentences, making it the dominant code.
- **C adjudicate:** `MIXED`
  - Lexical consensus (S7: physical_protection) and contextual dominant (S7) both point to external danger/risk scenarios, but the taxonomy metadata flags Emotional Safety & Reassurance (S1) as the primary category with Risk/Danger as secondary. This tension is meaningful: the topic likely captures moments where physical threat occasions emotional reassurance-seeking or provision, making neither S7 nor S1 alone sufficient. The functional security work is split between protection from external harm (S7) and the emotional comfort derived from or sought during that protection (S1). MIXED is therefore the most accurate resolution. Manual review is required to determine whether the dominant reader-experienced security function is the physical shield or the emotional soothing it enables, which would resolve the code to S7 or S1 respectively.
- **Action:** REINTERPRET

---

## Topic 175 — Gentleman Offers Steadying Support

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> the occurrences of the day were too full of interest to leave elizabeth much attention for any of these new friends; and she could do nothing but think, and think with wonder, of mr. [person]'s civility, and, above all, of his wishing her to be acquainted with his sister.

> mr. [person] placed his hand on [person]’s shoulder for support as mr. [person] barely walked out the front door.

> yes, but when i fell ill, it was apparent that i could not travel all the way to calais, so mr. [person] took me to the house of a friend of his: mr. [person].”

> *(CELL_B, tertile=end)* On his way to see Mistress Gwyllain to explain your…ah, unexplained arrival.”

> *(CELL_B, tertile=begin)* Shit," grunted Sheridan, apparently immune to Owen's considerable charms. "

### Pass A/B/C

- **A lexical:** `S1`
  - Main keywords (Bingley, Georgiana, Bennet, Pemberley) point to social belonging/group membership (S2), but KeyBERT, POS, and MMR are dominated by affective-state vocabulary — 'affection, longing, concerned, worrying, distress, passionate, warming, encouraged, thoughtfully' — all signalling emotional comfort and reassurance rather than material provision or status display. The emotional register overwhelms the social-network framing, driving consensus to S1. Disagreement flagged because Main alone suggested S2.
- **B contextual:** `S0`
  - All sentences in this topic are character name references, dialogue tags, brief reactions, or plot-movement fragments (orders, arrivals, departures). None perform a security function — emotional, material, or status/appearance. They are narrative scaffolding centered on named characters (Gwyllain, Sheridan, Pippen, Darcy) without conveying reassurance, provision, protection, belonging, commitment, or any other security-relevant content. All coded S0 off_target.
- **C adjudicate:** `S0`
  - Pass A/B lexical consensus landed on S1 (emotional_reassurance), but the contextual dominant is S0 (off_target). The taxonomy placement under 5.2 Friends, Allies & Social Circles as secondary is the decisive signal: the topic's primary function is peer/ally dynamics rather than dyadic emotional reassurance directed at the protagonist's security needs. Emotional warmth present in friend-group content does not constitute the security-provision function required for S1. The 4.6 primary taxonomy label describes the broader category but the actual topic content, per contextual dominant, does not perform emotional reassurance as a security function — it describes social circle interactions. S0 is therefore the correct resolution. No split warranted; no hypothesis inclusion.
- **Action:** REINTERPRET

---

## Topic 190 — Offering to Get Someone Cleaned Up

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> i’ll get cleaned up here as soon as i can.

> i’ll pay to have it cleaned.” “

> i'll get her cleaned up," said a handsome groom, taking her arm. "

> *(CELL_C, tertile=middle)* I will clean up the battlefield while you drink plenty of fluids.

> *(CELL_C, tertile=middle)* I know you would prefer to burn it yourselves out of respect, but my way will be faster, cleaner and will ensure no parasites escape.

> *(CELL_D, tertile=middle)* May I know why you gave Mr. Thesiger the brush off just now?”

> *(CELL_D, tertile=middle)* Don’t you see that if you go ahead with this annulment, if you air the Roxtons’ dirty laundry in public, I will be utterly, utterly ruined.

> *(CELL_D, tertile=begin)* A lackey came out from behind the butler with pan and brush and quickly set to sweeping up the shards of broken glass from Deb’s smashed wine glass.

### Pass A/B/C

- **A lexical:** `S5`
  - Main keywords (clean, cleaning, cleaned, mess, cleaner, freshen) and KeyBERT (cleaned, wipe, sweeping, dump) all point to routine domestic cleaning/tidying — a classic everyday practical-care function (S5). MMR adds 'paying' and 'planned' alongside 'cleaned/sweeping/dump', reinforcing the domestic-service/practical-care reading rather than crisis care. POS keywords (sweeping, dump, session, parties, suitcase, places) are more ambiguous and could be off-target (S0) without the cleaning anchor, hence minor disagreement. The dominant signal across three of four reps is routine household maintenance as a material security provision.
- **B contextual:** `S0`
  - The majority of sentences describe literal cleaning, tidying, or hygiene actions with no clear security function in the romance-novel sense, coding as S0 (off_target). A cluster from BOOK_004 and BOOK_006 depicts one character helping another with physical cleanup tasks in a caregiving/everyday-practical manner (S5). Three sentences from BOOK_001 involve tending to someone after a battle/crisis (S6). One sentence from BOOK_002 concerns social reputation/ruin (S12). S0 dominates at ~50%, making it the dominant code.
- **C adjudicate:** `S1`
  - Pass A/B lexical consensus landed on S5 (practical_care_everyday), but the taxonomy metadata places this topic squarely in 4.6 Emotional Safety, Reassurance & Caretaking. The contextual dominant S0 (off_target) is overridden by the taxonomy signal: the topic is doing security work, just emotional rather than practical. S1 (emotional_reassurance) is the most specific match for reassurance and caretaking functions within the emotional safety cluster. The secondary taxonomy note (8.3b Everyday Props & Communication Media) suggests the surface lexicon involves mundane objects or messages, which explains the S5 false positive in Pass A/B — the objects are vehicles for emotional reassurance, not practical provision. Function over object rule resolves this to S1.
- **Action:** REINTERPRET

---

## Topic 191 — Working to Pay The Bills

- **Taxonomy:** 6.2 — Work & Professional Identity
- **Code:** S0 (norm: S0)

> but in all honesty, she needed every penny of the income she earned, so even if she had known, she probably wouldn’t have paid the premiums.

> her job as an accountant for h & h lumber wasn't exactly exhilarating, but it paid the bills, and they treated her kindly there.

> once the television shows pay her major loot, she'll retire from her day job and write from home.

> *(CELL_B, tertile=middle)* She worked out of her home, which was a big bonus for those times when Jenna needed a babysitter fast.

> *(CELL_B, tertile=end)* And I hope for the maid’s sake that it was a good bribe, because it just cost her her job.” “

> *(CELL_B, tertile=begin)* When she’d enjoyed the adventure of a job that was never the same two days in a row.

> *(CELL_B, tertile=begin)* She’d loved the job, loved the idea of travel and stupidly, had fallen in love with the boss.

> *(CELL_B, tertile=middle)* Actually, she had earned a ton of money, even without any full-contact stuff.

> *(CELL_B, tertile=begin)* That might help tide her over while she built her client base.

> *(CELL_B, tertile=end)* She’s been here long enough to learn everything, she has an accounting background, and she has the motive.” “

### Pass A/B/C

- **A lexical:** `S8`
  - All keyword lists focus on financial aspects such as 'job', 'money', 'pay', 'bills', 'business', 'paid', 'fund', 'earned', 'afford', 'claims', indicating that the topic revolves around material security through money provision.
- **B contextual:** `S0`
  - The dominant code is S0 (off_target) as most sentences do not explicitly mention any security function. The next most frequent codes are S4 (commitment_security) and S8 (money_provision), but they do not reach the 70% threshold.
- **C adjudicate:** `S8`
  - The topic's dominant code is S0 (off_target), but the lexical consensus is S8 (money_provision). Given the taxonomy's focus on economic precarity and security, renaming the topic to better reflect its financial security aspect is appropriate.
- **Action:** RENAME

---

## Topic 193 — Nurse Arranged After Hospital Release

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

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

- **A lexical:** `S1`
  - The keywords 'ignore', 'fooled', 'embarrassment', 'admitted', 'hopeful', and 'stares' suggest emotional tension and reassurance-seeking behaviors.
- **B contextual:** `S0|MIXED`
  - Most sentences do not explicitly discuss security functions, so the dominant code is S0. The other codes are assigned based on specific mentions of status display (S12), commitment security (S4), housing (S9), and gift romance token (S14).
- **C adjudicate:** `S1`
  - The topic's dominant code is S0, but the taxonomy and lexical consensus suggest a focus on emotional safety and reassurance. Therefore, the topic should be renamed to better reflect its emotional security function.
- **Action:** RENAME

---

## Topic 204 — Promising to Care For Her Sister

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** S0 (norm: S0)

> i’ll need to finish dressing and leave a note for my sister.”

> yes, and soon you’ll be my sister.

> i’ll find a way to care for your mother and your sister.” “

> *(CELL_D, tertile=middle)* My sister’s still there with her husband, who’s a copper, and their three kids.

> *(CELL_A, tertile=begin)* You have not been paying close attention to your sister’s problems lately, have you?” “

> *(CELL_A, tertile=begin)* Your sister mentioned in passing that you are something of a recluse.” “

> *(CELL_A, tertile=end)* You mock your sister, but you will admit that she has great talents.” “

> *(CELL_A, tertile=end)* I realize that you are concerned for your sister’s happiness.

### Pass A/B/C

- **A lexical:** `S2`
  - Main keywords (sister, sisters, sis, sisterly, little) and POS/MMR cues (affection, introduce, treated) all point to sibling relational identity and belonging. 'Affection' and 'sisterly' signal emotional bonding within a family unit, which maps to S2 (belonging) rather than S1 (reassurance) because the emphasis is on group/relational membership. KeyBERT terms (asks, assume, willing, uh, hi, speaking) are conversational scaffolding with no clear security function, hence S0 for that rep. The majority (3/4) converge on S2.
- **B contextual:** `S0`
  - The vast majority of sentences are simple references to a sister character — naming, identifying, or describing family relationships — with no security function being performed. A small number perform security functions: concern for a sister's happiness (S1 emotional reassurance), feeling of gaining/having a sister-like bond (S2 belonging), and explicit protective/rescue directives (S7 physical protection). S0 dominates at ~75%.
- **C adjudicate:** `S0`
  - Pass A/B lexical consensus landed on S2 (belonging), but the contextual dominant is S0 (off_target). The taxonomy placement under 4.5 Reconciliation/Commitments/HEA and 5.1 Family/Kinship confirms this topic is primarily about narrative resolution and relational repair rather than a discrete security-provision function. Reconciliation and HEA arcs describe plot outcomes, not a character performing emotional reassurance (S1), belonging-conferral (S2), or commitment-security (S4) as a functional act. The S2 lexical signal likely arose from surface co-occurrence of family/togetherness vocabulary, but function-over-object adjudication finds no single security function being enacted. S0 is the correct resolution.
- **Action:** REINTERPRET

---

## Topic 232 — Conversation Cut Short By Arrival

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> dex had come in and gabe's conversation with her, the longest conversation that they'd had in the couple of weeks he'd been back, was over.

> gabe leaned down so he wouldn’t be overheard. “

> i'll tell you right now falan and gabe are the only people on my team that i'd stake my career— or my balls —on."

> *(CELL_C, tertile=end)* Have Remy or the boys been out to question you again or give you more information about Joshua’s attack?”

> *(CELL_A, tertile=end)* He almost told her to call him Gabe, but he knew his name would sound way too good coming from her full lips.

> *(CELL_A, tertile=end)* Her name fit her, Gabe had found himself thinking one too many times.

> *(CELL_A, tertile=begin)* Gabe pretended to tackle Zach as he pulled the microphone from his hand, but he instantly sobered as he turned to Chase and Chloe. “

> *(CELL_A, tertile=end)* Her face got red then and she said angrily, "So, Gabe knew and didn't clue me in?

### Pass A/B/C

- **A lexical:** `S1`
  - Across all four keyword sets the dominant signals are interpersonal emotional exchange: 'trembling', 'groaned', 'longing', 'pained', 'instincts', 'awareness', 'stroking', 'kindly', 'squeezed', 'gesture', 'impatiently'. These cues point to characters managing emotional distress and seeking or providing comfort through conversation and physical touch (hand, gesture, stroking). No material provision, housing, money, or status display cues are present. The function is soothing/reassuring emotional states, consistent with S1.
- **B contextual:** `S0`
  - The vast majority of sentences in this topic are character-name references, dialogue tags, and interpersonal exchanges that do not perform a security function — they are narrative scaffolding centered on a character named Gabe/Gabriel. A small subset carries light emotional-reassurance signals (not wanting Gabe mad, asking for Gabe, letting someone in emotionally) coded S1/S3, one sentence references a physical attack inquiry (S7), and one a health check (S6). None of these minority codes reaches 70%, but S0 (off-target) dominates at ~70%, making it the dominant code.
- **C adjudicate:** `S0`
  - Pass A/B produced a lexical consensus of S1 (emotional_reassurance), likely driven by surface affect-laden vocabulary. However, contextual dominant analysis correctly identifies S0 (off_target): the taxonomy placement in 4.2 Ongoing Courtship & Everyday Relational Bonding indicates this topic captures routine romantic interaction and bonding rituals rather than a discrete security-provision function. Courtship and everyday bonding are relational processes, not security behaviors — no specific emotional reassurance, belonging, trust, or commitment-security function is being performed as a distinct act. The S1 lexical signal is incidental to the courtship register, not evidence of a security function. S0 is the correct resolution. No split is warranted as there is no separable security-functional sub-cluster evident.
- **Action:** REINTERPRET

---

## Topic 240 — Unsure How to Offer Comfort

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> oh my god, sean!

> sean pursed his lips, unsure he was equal to the task of comforting [person].

> sean held out his hand and added; “now if you’ll excuse me i have a beautiful woman waiting to have breakfast with me.”

> *(CELL_B, tertile=begin)* Oh,” I said, thinking fast, watching as Seth started to show Liam how to use another nearby machine, while the Tiffanys and Brittanys gathered round, looking more worshipful than ever.

> *(CELL_B, tertile=end)* You need to stop nipping at him and face the fact that when Shon goes under, he’s off limits, one breath away from being a hostile at our backs.” “

### Pass A/B/C

- **A lexical:** `S1`
  - KeyBERT, POS, and MMR are dominated by affective-state words (anxious, shivered, winced, unsure, distracted, conscious, stares, solemnly, mumbled) pointing to characters managing or seeking emotional reassurance in tense interpersonal exchanges. Main keywords are proper names and dialogue tags (sean, jaime, brogue, answered, said) with no clear security function on their own, hence S0 for Main. The cross-rep majority signals S1 emotional reassurance. No material or status/appearance cues are present.
- **B contextual:** `S0`
  - All sentences in this topic consist of character name references, brief dialogue fragments, exclamations, and minimal conversational exchanges (e.g., 'Liam wanted to know', 'Shon!', 'I want Sean', 'Conner asked'). None of these sentences perform any identifiable security function — emotional reassurance, material provision, status display, or otherwise. They are narrative/dialogue scaffolding centered on character names and short utterances with no security-relevant content. All coded S0 (off_target).
- **C adjudicate:** `S1`
  - Pass A/B lexical consensus mapped to S1 (emotional_reassurance), while contextual dominant suggested S0 (off_target). Taxonomy 4.6 Emotional Safety, Reassurance & Caretaking directly anchors this topic to S1 functions — soothing, comforting, and affirming emotional safety. The S0 contextual read likely reflects surface-level ambiguity rather than a genuine absence of security function. Given the taxonomy label explicitly names reassurance and caretaking, S1 is the most specific and defensible code. Secondary taxonomy 4.2 (Ongoing Courtship & Everyday Relational Bonding) does not override the primary emotional safety signal. No split is warranted because the dominant function is coherently S1.
- **Action:** REINTERPRET

---

## Topic 247 — Promising You Will Not Be Alone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> if we make it through this alone, we’ll just be better at being alone.”

> you’ll never be alone.

> before you say no, i want you to know i’ll be alone mostly.

> *(CELL_B, tertile=end)* If I went out alone, it seemed I felt surrounded by people who couldn’t speak to me.

> *(CELL_B, tertile=begin)* I promise you, you will never be alone again so long as I live.”

> *(CELL_B, tertile=begin)* I’ve pictured this so many times in my mind, I don’t want to wake up and find I’m alone again.” “

### Pass A/B/C

- **A lexical:** `S0`
  - Main keywords (alone, solitude, want, prefer, rather, live) describe a state of chosen or imposed aloneness and personal preference — no security provision is being enacted. POS terms (options, terms, circumstances, attempt, fault) are generic situational/deliberative vocabulary with no security function. MMR terms (chose, preferred, planned, insisted, fault, circumstances) reinforce deliberation and agency framing, not provision of security. KeyBERT's 'upset, praying' hints at emotional distress, nudging toward S1, but two isolated affect words are insufficient to override the dominant theme of solitude/preference with no provider-recipient security dynamic. The topic as a whole depicts a character's stance on being alone rather than any security-providing act.
- **B contextual:** `S2`
  - The overwhelming theme of this topic is aloneness vs. togetherness — characters expressing loneliness, fear of being alone, promises never to be alone again, and the comfort of another's presence. This is the security function of belonging (S2): the felt sense of not being isolated, of being included and accompanied by a significant other. A small number of sentences are purely situational/logistical references to being alone (e.g., 'Alone, I hoped'; 'Alone with Luke Emerson'; 'May I speak with you … alone?') that carry no security function and are coded S0. No material or status/appearance security functions are present.
- **C adjudicate:** `S1`
  - Lexical consensus (S0) and contextual dominant (S2 belonging) diverge, but the taxonomy anchor — 4.6 Emotional Safety, Reassurance & Caretaking with secondary 9.2 Promise/Vow/Future-Tense Speech Acts — points clearly to S1 (emotional_reassurance). Reassurance and caretaking speech acts (promises, vows, future-tense comfort) are the defining function here, not belonging per se. S2 would require evidence of group/relational inclusion; S0 would require absence of security function altogether. The taxonomy metadata resolves the conflict: the topic is performing emotional safety work through reassuring language, mapping to S1. No split is warranted because the secondary taxonomy (promise/vow speech acts) is the vehicle for delivering emotional reassurance, not an independent security function.
- **Action:** REINTERPRET

---

## Topic 273 — Mentor Gives Firm Instructions

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

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

- **A lexical:** `S1`
  - Across all four keyword lists the dominant signals are interpersonal emotional repair: 'insensitivity', 'apology', 'upset', 'awareness', 'appreciate', 'treatment', 'explanation', 'choices'. These cues point to a scene in which one character must acknowledge hurt feelings and offer reassurance/apology to another — the classic emotional-reassurance security function (S1). No material, housing, money, or status/appearance cues are present.
- **B contextual:** `S0`
  - The overwhelming majority of sentences are character name-drops, dialogue fragments, and scene-setting utterances with no discernible security function — coded S0. Two sentences (BOOK_001_3, BOOK_001_5) signal commitment security (a rival being dismissed, acknowledging a rival complicates the relationship) → S4. Two sentences (BOOK_002_4, BOOK_006_1) reference belonging/social inclusion → S2. One sentence (BOOK_002_3) offers emotional distraction/reassurance → S1. S0 dominates at ~75%.
- **C adjudicate:** `S0`
  - Pass A/B lexical consensus landed on S1 (emotional_reassurance), but the contextual dominant is S0 (off_target). The taxonomy placement under 4.6 Emotional Safety with a secondary of 5.2 Friends, Allies & Social Circles suggests the topic's primary function is social/peer dynamics rather than dyadic emotional reassurance from a romantic partner. Emotional Safety (4.6) can overlap with S1, but the secondary taxonomy node (5.2) shifts the functional weight toward group belonging or ally networks, which is not cleanly S1 or S2 in a romantic-security sense. Because the content appears to be about social circles rather than partner-directed reassurance or belonging, S0 is the more defensible code — the topic is not performing a clear romantic-security function. Manual review is flagged because the 4.6 primary taxonomy does carry genuine S1 signal that should not be dismissed without human verification.
- **Action:** REINTERPRET

---

## Topic 277 — Promising to Handle The Lawyer

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> i’ll talk to the lawyer tomorrow.

> we’ll find a good lawyer to help.

> you can count on me to deal with the legal trouble they’ll cause.”

> *(CELL_D, tertile=end)* Mediation has never come easily for me and I need all the help I can get.

> *(CELL_B, tertile=end)* Such a lot of fuss over a piece of real estate that was destined by federal law to go unclaimed by anyone.

> *(CELL_B, tertile=end)* It’s important to establish legal boundaries of ownership, especially when you’re talking about gems and precious metals.

### Pass A/B/C

- **A lexical:** `S11`
  - Main keywords (lawyer, attorney, law, legal, firm, defense, counsel, appointed, advice) point squarely to legal representation and counsel — a practical, instrumental service. KeyBERT cues 'afford' and 'cost' confirm the material/service dimension (can one pay for legal help?), while 'begging' and 'worrying' suggest urgency around obtaining that help. POS 'cost' and 'process' reinforce the transactional/procedural nature. MMR 'afford', 'warned', 'begging', 'process' all support navigating a legal/official process. This is practical assistance (legal aid/counsel) rather than emotional reassurance, housing, money provision, or status display, so S11 (practical_help_other) is the most specific fit.
- **B contextual:** `MIXED`
  - Topic 277 clusters around legal/law enforcement roles and legal processes. 'Lawman' sentences function as physical protection (S7) — a lawman's role is protective/security-enforcing. Lawyer references where someone is being advised to get legal help function as practical help (S11). Property/real estate legal boundary sentences function as housing/property security (S9). Several sentences are purely descriptive or conversational with no security function (S0). No single code reaches 70%, so MIXED applies.
- **C adjudicate:** `S1`
  - Pass A/B lexical consensus landed on S11 (practical_help_other), but the taxonomy metadata clarifies the primary function is Emotional Safety & Reassurance (4.6), with a secondary of Promise/Vow speech acts (9.2). Neither of these is practical/material help. The contextual dominant 'MIXED' reflected uncertainty between S1 and the vow/commitment dimension (S4), but the primary taxonomy anchor is emotional reassurance. Promise and vow speech acts in romance contexts typically serve to deliver emotional safety rather than binding contractual commitment, so S1 is the most specific single code. S4 would apply if the vow were foregrounding future material or relational security obligations, but here the function is soothing/reassuring the partner emotionally. S11 is overridden as a misclassification from surface lexical features. Single code S1 is preferred over MIXED because the secondary taxonomy node (speech-act form) describes the vehicle, not a distinct security function.
- **Action:** REINTERPRET

---

## Topic 299 — Pledging to Have Your Back

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> before she’s completely out i ask, “[person], you know i’ve always got your back, right?”

> but i’ve seen you, seen who you are, watched you handle uncle charlie.

> i’ve got a little time before charlie finishes my bike.

> *(CELL_A, tertile=middle)* Kevin was worried that Scott’s death was somehow related to Todd’s return to Birmingham.’

> *(CELL_A, tertile=begin)* They all left for college with big dreams, except Scott and Kevin,’ she said sadly. ‘

### Pass A/B/C

- **A lexical:** `S3`
  - KeyBERT 'promises/tries/willingly', POS 'promises/threats/terms', and MMR 'promises/threat/forgive/solemnly/terms' all cluster around negotiating reliability and trustworthiness between characters — the classic lexical signature of S3 trust-building. Main keywords (character names + 'handle/seen/time') are too generic to code independently (S0), but the three richer rep sets converge on trust dynamics, yielding S3 consensus.
- **B contextual:** `S0`
  - The majority of sentences are narrative references to named characters (Charlie, Scott, Pete, Kevin) without performing any security function — they are plot/dialogue fragments with no discernible security work. A small cluster of Charlie-related sentences provide emotional reassurance (soothing, comfort, promise of return) coded S1. One sentence describes physical confinement to prevent self-harm, coded S7. One sentence references a welfare check on Charlie, coded S6. S0 dominates at ~70%, making it the dominant code.
- **C adjudicate:** `S1`
  - Pass A/B lexical consensus landed on S3 (trust), but the taxonomy metadata places this firmly in 4.6 Emotional Safety, Reassurance & Caretaking. The contextual dominant S0 (off_target) is overridden by the taxonomy signal: the topic is doing security work, specifically providing emotional reassurance and safety rather than trust-building per se. S1 (emotional_reassurance) is the most specific match for Emotional Safety & Caretaking. The secondary taxonomy note (5.2 Friends, Allies & Social Circles) does not shift the primary security function. S3 would require evidence of reliability/dependability framing; S1 better captures the soothing/reassurance function described. No split needed as the dominant function is singular.
- **Action:** REINTERPRET

---

## Topic 305 — Confessing A Lifelong Regret

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** S0 (norm: S0)

> i know that now, and i’ll go to my grave regretting what i did to you.” “

> come on in, you’ll no doubt regret it.

> you’ll regret that.’ ‘

> *(CELL_B, tertile=middle)* You are surely not intending to imply that you are beginning to regret this marriage already?’ ‘

> *(CELL_B, tertile=end)* I fear that my careless remarks must have been the cause of that outburst.

### Pass A/B/C

- **A lexical:** `S1`
  - All four keyword lists centre on internal emotional states (regret, fears, upset, embarrassing) and communicative acts aimed at managing those states (assure, admit, handled, fumbled). The cluster signals a character seeking or providing reassurance about a past decision or remark — classic emotional-reassurance security function. No material, housing, money, or status/appearance cues are present.
- **B contextual:** `S1`
  - The overwhelming majority of sentences express emotional states of regret, remorse, or reassurance about past actions and feelings — all functioning as emotional reassurance or processing of emotional distress (S1). A smaller subset references regret about commitment decisions such as marriage or a life choice, pointing to commitment security (S4). A few sentences are too vague or off-topic to carry a security function (S0). S1 exceeds 70% and is the dominant code.
- **C adjudicate:** `S1`
  - Lexical consensus and contextual dominant both converge on S1 (emotional_reassurance). The taxonomy placement under Reconciliation, Commitments & HEA with a secondary of Negative Emotions & Distress is fully consistent with S1: these narrative moments centre on soothing distress, reaffirming emotional bonds, and restoring felt security after conflict or rupture. No material or status/appearance function is implicated. S1 is the most specific applicable code; no split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 307 — Hauling Someone Up The Stairs

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> [person] would hate it if she took a rake like [person] to her bed, and she would so love to rub it in joshua’s face and prove his threats could not restrain her. “

> his thoughts threatened to return to those awful times once again, but thankfully, ash and [person] emerged from the thicket.

> getting ash up the stairs and into the bedroom was a lot harder than it had been last night, mostly because ash was pissed off and conscious instead of in la-la land.

> *(CELL_B, tertile=end)* You and Ashlynn are gonna have to keep him on the straight and narrow."

> *(CELL_B, tertile=end)* He stopped to pat Ashlynn and congratulate her on a large belch. "

> *(CELL_B, tertile=end)* But as he was approaching Clarksburg, Ashlynn chose that moment to be cranky.

> *(CELL_B, tertile=end)* Henry's crankiness had returned, and even sweet Ashlynn was wailing by now.

> *(CELL_B, tertile=end)* Sniffing in disdain, Johnny pushed Ashlynn's stroler over to Grissom. "

### Pass A/B/C

- **A lexical:** `S7`
  - Main keywords are proper nouns and place names with no clear security signal (S0). KeyBERT, POS, and MMR converge on physical threat and bodily-stress vocabulary: 'threats', 'heaved', 'winced', 'struggled', 'fought', 'panting', 'movements', 'anxiety', 'permission', 'urged' — collectively evoking a scene of physical danger, bodily exertion, and protective action. 'Threats' and 'permission' suggest a power/protection dynamic; 'panting', 'heaved', 'struggled', 'emerged' indicate physical effort under duress. This pattern maps most specifically to S7 (physical protection). Disagreement flagged because Main is S0 while the other three reps align on S7.
- **B contextual:** `S0`
  - The majority of sentences are either bare name references ('Ash.', 'Ash nodded', etc.) or descriptions of physical destruction (ash/bone/ooze), none of which perform a security function. A small subset (BOOK_002_1, _2, _3, _6) depicts practical everyday caregiving of an infant (changing, managing a stroller, monitoring behaviour), coded S5. The topic as a whole is dominated by off-target content, so S0 is dominant.
- **C adjudicate:** `S1`
  - Pass A/B lexical consensus landed on S7 (physical_protection), likely driven by surface-level protective language. However, the taxonomy metadata places this topic squarely in 4.6 Emotional Safety, Reassurance & Caretaking, with a secondary tag of 8.1 Domestic Spaces & Routines. The contextual dominant from Pass B is S0 (off_target), suggesting the physical-protection reading was an over-literal interpretation of the lexical signal. Reconciling all three signals: the primary taxonomy node (emotional safety/reassurance/caretaking) maps directly to S1 (emotional_reassurance), which is more specific than S0 and better captures the security function actually performed. The domestic-spaces secondary tag does not elevate this to S5 (practical_care_everyday) because the caretaking described is affective rather than task-based. S1 is therefore the most specific valid code consistent with the taxonomy evidence, and S7 is rejected as a surface-lexical artefact.
- **Action:** REINTERPRET

---

## Topic 315 — Claiming Her As His Own

- **Taxonomy:** 4.7 — Jealousy & Possessive Romance Conflict
- **Code:** S0 (norm: S0)
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

- **A lexical:** `S0`
  - All four keyword lists are dominated by character names (tristan, adrienne, simon, colby, damon, crispus), vague action/speech verbs (screaming, sounding, grumbled, nudged, paced), and generic narrative terms (sentence, indication, hesitation, ends, tracks, ribs, behavior, actions). None of these cues signal a security-provision function—emotional reassurance, material support, status display, or any other S1–S16 category. The cluster appears to capture a scene-level dialogue or action sequence without a discernible security theme.
- **B contextual:** `S1`
  - The topic centres on the emotional relationship between Dev and Val — arguments, hurt feelings, emotional walls, and the struggle to reconnect. The majority of sentences (S1) involve emotional reassurance or its absence: characters confronting each other about feelings, emotional reactions, and appeals to let things go. A meaningful minority (S4) addresses commitment security — whether the relationship will survive, Dev wanting Val back, and Val winning 'the first battle for his heart.' One sentence touches on trust (S3 — Dev upset Val didn't mention a confrontation). Several sentences are purely referential name-calls or fragments with no security function (S0). S1 exceeds 70% when S0 sentences are excluded from the functional count, and is clearly dominant overall.
- **C adjudicate:** `S1`
  - Lexical pass coded S0 (off-target), but contextual dominant correctly identifies S1 (emotional_reassurance). Taxonomy 4.7 Jealousy & Possessive Romance Conflict centers on emotional security threats — jealousy and possessiveness are fundamentally about reassurance-seeking and fear of emotional loss, not material or status functions. The secondary taxonomy (5.2 Friends, Allies & Social Circles) reinforces a social-emotional rather than material frame. S0 is overridden: the topic is doing security work, specifically emotional reassurance provision in the context of relational threat. S1 is the most specific applicable code.
- **Action:** REINTERPRET

---

## Topic 316 — Snapping Over Money and Control

- **Taxonomy:** 4.4 — Conflict, Distance & Breakup Threats
- **Code:** S0 (norm: S0)

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

- **A lexical:** `S1`
  - The Main and KeyBERT lists suggest a focus on appearance and status (S12, S14), but the POS and MMR lists indicate emotional reassurance (S1). The consensus is emotional reassurance due to the prevalence of emotional cues like 'thoughtful', 'annoyance', 'disappointment', and 'worries'.
- **B contextual:** `S0`
  - Most sentences do not contain any security function, hence S0. The sentence 'Lucas shouted in panic.' (BOOK_006_1) indicates physical protection (S7), and 'Perhaps you should show Eva to her room,” Lucas finally suggested to Michael.' (BOOK_002_4) shows practical help (S11).
- **C adjudicate:** `S0`
  - The topic primarily revolves around conflicts and threats, which do not directly relate to emotional, material, or status/appearance security functions.
- **Action:** RENAME

---

## Topic 340 — Patience Tested Through Small Trials

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> for two years he had observed the christmas elf, but he never imagined touching her.

> from the moment that she started working at her current job, she had never clicked with frank.

> her patience throughout the meal with the girls never wavered, not with spilled drinks, sloppy faces and an occasional cry for attention.

> *(CELL_A, tertile=middle)* Up until now, she'd never met anyone who made her ache for the things that were denied her.

> *(CELL_A, tertile=begin)* She'd never known anything like the power and hunger of his kiss.

### Pass A/B/C

- **A lexical:** `S1`
  - KeyBERT, POS, and MMR converge on emotional-state vocabulary: 'emotionally', 'feared', 'unhappy', 'disappointed', 'upset', 'cared' — all pointing to emotional experience and reassurance needs. 'Main' lacks clear security cues ('never', 'mentioned', 'regime', 'standards') and reads as narrative framing rather than a security function, warranting S0. The majority signal is emotional distress and the need for reassurance (S1), overriding the ambiguous Main rep.
- **B contextual:** `S0`
  - Half the sentences carry no security function — they describe emotional reactions, character traits, or narrative observations without performing a security role. Among those that do carry security function, physical protection (S7) and emotional reassurance (S1) are roughly equal minorities. No single security code reaches 70%, but S0 (off-target) is the plurality at 50%, making it the dominant code overall.
- **C adjudicate:** `S0`
  - Lexical consensus (S1) reflects surface-level emotional reassurance vocabulary, but contextual dominant (S0) correctly identifies that the topic's security function is off-target for the romance-security hypothesis. The taxonomy placement under 4.6 Emotional Safety with a secondary of 5.1 Family/Kinship/Parenthood confirms the emotional content is operating in a familial or parental register rather than a romantic-dyadic one. Because the security function here is not directed at a romantic partner relationship, S0 is the appropriate resolution. The S1 signal is real but misattributed to the wrong relational context for this study's scope. Manual review is flagged to confirm whether any tokens in this topic do carry romantic-dyadic reassurance that would warrant a SPLIT.
- **Action:** REINTERPRET

---

## Topic 345 — Older Man Trading Shelter For Sex

- **Taxonomy:** 7.4 — Unwanted or Coercive Sexual Contact
- **Code:** S10 (norm: S10)

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

- **A lexical:** `S14`
  - Words like 'revealing', 'winked', 'straightened' suggest subtle, romantic gestures, fitting S14.
- **B contextual:** `S3`
  - The dominant code is S3 (trust) as many sentences revolve around characters understanding, watching, and communicating with each other, indicating a level of trust and security in their relationships.
- **C adjudicate:** `S14`
  - The dominant code S3 (trust) is not the most specific representation of the topic. The topic revolves around the exchange of gifts and tokens, which is more accurately represented by S14 (gift_romance_token).
- **Action:** RENAME

---

## Topic 351 — Warm Greeting Upon Return

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> thank god you’ve come back—and will you look at me, just in time.”

> it is a pleasure to see you again—so soon, madam. ”

> so i’ll see you there,” he said, feeling upbeat for the first time in a long time. “

> *(CELL_D, tertile=begin)* I’ll see you as often as I can,” he said, only making matters worse by reminding the children he wouldn’t be seeing them on a normal basis. “

> *(CELL_D, tertile=middle)* Amber had seen it as a splendid way to say goodbye to the hoards of tourists who crowded Harmony during that season.

### Pass A/B/C

- **A lexical:** `S1`
  - All four keyword sets converge on the lexical field of warm social acknowledgment: Main keywords (glad, happy, pleasure, nice, great) signal positive affect exchange; KeyBERT adds 'greeted, warmth, mister, madam, replies' pointing to a formal but affectively warm greeting ritual; POS 'warmth' and 'lack' (absence of coldness) reinforce emotional tone; MMR 'greeted, warmth, reminds, replies' confirm the same. No material provision, housing, money, status display, or physical protection cues are present. The dominant security function is emotional reassurance delivered through pleasurable social re-encounter.
- **B contextual:** `S2`
  - The topic clusters around expressions of pleasure, gladness, and delight at seeing or reuniting with someone — social belonging and interpersonal connection ('good to see you', 'a pleasure to see you again', 'I am glad to see you'). These function as belonging/social-inclusion security (S2). Sentences that are mere farewells, neutral observations, or context-free fragments with no security function are coded S0. S2 accounts for ~60% of sentences, exceeding the 70% threshold when weighted by the higher-probability CELL_B sentences that anchor the topic.
- **C adjudicate:** `S2`
  - Pass A yielded S1 (emotional_reassurance) and Pass B yielded S2 (belonging). In the context of Taxonomy 4.2 — Ongoing Courtship & Everyday Relational Bonding — the dominant security function is the establishment and maintenance of felt belonging within a developing relationship, rather than discrete reassurance acts. S2 is the more specific and contextually accurate code: the topic captures the ongoing sense of being included, chosen, and bonded rather than soothing of acute distress (S1). Contextual dominant S2 is therefore adopted as the consensus security_code.
- **Action:** REINTERPRET

---

## Topic 355 — Blanket Draped Over Someone

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S5 (norm: S5)

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

- **A lexical:** `S5`
  - All four keyword lists centre on bedding and covering actions — blanket, comforter, sheet, tucked, wrapped, draped, curled, folded — describing the routine physical act of covering/tending to someone's body comfort. This is everyday practical care (tucking in, wrapping up) rather than crisis care, emotional reassurance, or status display. POS and MMR add movement/task words (edges, movements, task, straightened) and mild affect (terrified, embarrassed) but these are incidental to the dominant covering-care function. S5 (practical_care_everyday) is the most specific fit.
- **B contextual:** `S5`
  - The overwhelming majority of sentences depict blankets, coats, and coverings being arranged, tucked, spread, or carried to provide physical warmth and bodily comfort — classic everyday practical care (S5). A few sentences show care during vulnerability or illness (S6: frail neck under blanket, peeling blanket off prone body). One sentence shows anxiety-driven self-wrapping (S1). Several sentences are purely descriptive with no security function (S0: groggy waking, nibbled wire, naked man, empty seat bundle). S5 comfortably exceeds 70% of the security-coded sentences and represents the dominant function of this topic.
- **C adjudicate:** `S5`
  - Lexical consensus and contextual dominant both converge on S5 (practical_care_everyday). The taxonomy metadata (4.6 Emotional Safety, Reassurance & Caretaking with secondary 8.1 Domestic Spaces & Routines) is consistent with S5, which captures routine domestic caregiving acts. While the taxonomy label references 'emotional safety,' the functional security work being performed is grounded in everyday practical care rather than pure emotional reassurance (S1), so S5 remains the most specific and accurate code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 356 — Admitting Exhaustion After A Long Day

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> i am kind of tired, but you’ve done enough.

> i’ve been riding most of the day, i’m tired.” “

> i’ve rested more than i ever expected to rest in the whole of my lifetime during the past six weeks,” he said, “and i’m feeling perfectly fresh.

> *(CELL_C, tertile=begin)* I was tired and cold and done with feeling under siege for the day. “

> *(CELL_C, tertile=middle)* Aren’t you getting just a little tired of—” “I wasn’t kidding about the way it gets dark out here.

> *(CELL_B, tertile=middle)* You must be exhausted with all of your commitments at the moment?’ ‘

> *(CELL_B, tertile=end)* I was tired from a big week, my nervous energy had transformed into lethargy, and I was still drunkish.

### Pass A/B/C

- **A lexical:** `S1`
  - Dominant cues across Main (tired, exhausted, exhaustion, fatigue, tiredness) and MMR (drained, emotionally, worn, rested) point to a state of depletion being acknowledged or addressed — classic emotional reassurance territory where one character recognises and responds to another's distress/weariness. 'Emotionally' in MMR confirms the affective register. POS yields only 'session, sir' which are too sparse to code beyond S0, but the three other reps converge on S1. No material or status signals present.
- **B contextual:** `MIXED`
  - Topic 356 clusters around expressions of exhaustion and fatigue. Most sentences are simple self-reports or observations of tiredness with no clear security function (S0). A subset involves one character noticing or acknowledging another's exhaustion in a way that functions as emotional attunement or reassurance (S1). A smaller subset involves directing a fatigued/ill person to rest or noting physical symptoms like smoke inhalation or sickness, which functions as care during illness/crisis (S6). No single code reaches 70%, so MIXED is assigned.
- **C adjudicate:** `S1`
  - Lexical consensus from Pass A/B converges on S1 (emotional_reassurance), and the taxonomy placement in 4.6 Emotional Safety, Reassurance & Caretaking confirms this as the primary function. The contextual dominant flagged MIXED due to a secondary signal of 3.1 Positive Resolution/Relief, but that secondary taxonomy node describes an outcome (relief, payoff) rather than a distinct security function — it is downstream of the reassurance act itself, not a separate security type. No material or status/appearance function is present. Resolving to S1 as the single most specific code; MIXED is not warranted when the secondary signal is an emotional valence variant rather than a cross-domain security function.
- **Action:** REINTERPRET

---

## Topic 358 — Reassuring Squeeze of The Hand

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

> she took bronte's hand and gave it a reassuring squeeze. "

> ted reached for caroline's hands and smiled at her reassuring squeeze. "

> they'll ask,” he murmured, and gave her waist a reassuring squeeze.

> *(CELL_D, tertile=end)* But my parents—" "Are fine," he interrupted, groaning when she curved her fingers as far as she could around his hardening shaft. "

### Pass A/B/C

- **A lexical:** `S1`
  - All four keyword lists converge on physical gestures of comfort: 'squeeze/squeezed/squeezing', 'shoulder', 'hand', 'arm', 'fingers', 'gently', 'reassuring', 'calming', 'trembling', 'tightening', 'gripped', 'draped'. The dominant semantic cluster is soothing, steadying touch directed at an anxious or distressed person — the canonical form of emotional reassurance (S1). No material provision, housing, status, or gift cues are present.
- **B contextual:** `MIXED`
  - Topic 358 clusters around hand-gripping and finger-touching gestures. Where these gestures occur in contexts of comfort, reassurance, or emotional connection (squeezing a hand in support, holding tighter, rubbing a thumb over a hand), they function as S1 emotional_reassurance. Where the gestures are purely physical/mechanical actions with no discernible security function (gripping a door handle, tightening on a receiver, sexual acts, eating nuts, shooting), they are S0 off_target. The split is approximately even between S1 and S0, so no single code reaches 70%, yielding MIXED.
- **C adjudicate:** `S1`
  - Lexical consensus from Pass A/B converges on S1 (emotional_reassurance), consistent with Taxonomy 4.6 Emotional Safety, Reassurance & Caretaking. The contextual dominant flagged MIXED, likely due to the secondary taxonomy signal (2.2 Kissing & Non-Explicit Affection), but physical affection here functions as a vehicle for emotional reassurance rather than an independent security dimension. Function-over-object principle resolves the ambiguity: the dominant security function is S1. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 367 — Sorting Out Concert Tickets

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> i’m assuming since there are two tickets, you’ll go with me?” “

> we’ll have to figure out how to get you a ticket.

> [person]—” “sure, i’ll give her the five-cent tour.”

> *(CELL_B, tertile=begin)* Mrs. Schmidt told me this is the coach I should take, and I was simply trying to find out—” “How much is the ticket?”

> *(CELL_D, tertile=middle)* He took my hand and guided me through the crowd of tourists on the side walk.

> *(CELL_A, tertile=begin)* All I have to do is take the public track tour and get conveniently separated from the tourists.

> *(CELL_A, tertile=middle)* I hop back in the limo and rush to my second event of the night, a Q & A event with racing fans.

### Pass A/B/C

- **A lexical:** `S14`
  - Main and MMR are anchored by 'tour, ticket, tickets, concert, concerts, bought, paid, cost, cancel' — the cluster describes purchasing or gifting event tickets (concerts, tours) as a romantic or relational gesture, with 'cancel' and 'apology' suggesting disruption of that plan. This maps to S14 (gift/romance token) rather than pure practical care. KeyBERT and POS lack ticket/event cues and read as off-target (S0), creating mild disagreement, but the dominant signal across Main and MMR is clearly S14.
- **B contextual:** `S0`
  - The topic clusters around touring, tickets, and travel logistics. The majority of sentences describe tour activities, events, and movement with no security function — coded S0. A subset of sentences (BOOK_001_1, _2, _4, _6; BOOK_005_1) involve paying for or purchasing tickets, functioning as financial provision/payment (S8). One sentence (BOOK_002_3) involves physical guidance through a crowd, coded S7 (physical protection). One sentence (BOOK_003_6) references competitive professional standing, coded S15 (workplace status). S0 dominates at ~65%.
- **C adjudicate:** `S0`
  - Pass A/B lexical consensus landed on S14 (gift/romance token), but the taxonomy placement in 4.2 Ongoing Courtship & Everyday Relational Bonding with a secondary tag of 8.3b Everyday Props & Communication Media indicates the topic's functional work is routine relational maintenance rather than a discrete gift-giving security act. S14 requires a token or gift functioning as a security-provision signal; here the objects (props, media) serve as courtship scaffolding without performing a security function. Contextual dominant S0 (off_target) is correct: the topic does not operationalize any of S1–S16 security functions. No free-form labels remain to remap.
- **Action:** REINTERPRET

---

## Topic 372 — Told to Keep Up Strength

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S0 (norm: S0)

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

- **A lexical:** `S1`
  - The dominant lexical cluster (strength, stronger, strong, weak, weakling, limitations, weaker) frames a discourse about personal vulnerability and emotional adequacy — classic territory for emotional reassurance. Supporting cues 'emotions', 'reflection', 'admit', 'hated' confirm introspective emotional processing. 'Crushed', 'destroyed' signal emotional wounding requiring reassurance. 'Feeding' and 'gain' in context of emotional reflection suggest drawing strength from a relationship. No material provision, housing, money, or status-display cues are present. The security function is reassurance against feelings of weakness/inadequacy.
- **B contextual:** `S0`
  - The overwhelming majority of sentences in this topic describe physical or personal strength, resilience, and toughness as abstract qualities or character traits — not performing any security function for another person. They are off-target (S0). One sentence (BOOK_002_1) references background/credentials needed for advancement, coded S15 (workplace status). Two sentences (BOOK_004_3, BOOK_004_4) involve encouraging someone to be strong emotionally, coded S1 (emotional reassurance). One sentence (BOOK_004_6) involves managing weakness/dizziness in a crisis context, coded S6 (care in illness/crisis). S0 dominates at ~80%.
- **C adjudicate:** `S0`
  - Lexical consensus (S1) and contextual dominant (S0) conflict. The taxonomy placement in 4.6 Emotional Safety & Reassurance suggests surface-level emotional language, but the contextual dominant analysis determined the topic is not performing security work in the romance-novel sense. S0 (off_target) takes precedence because function over object: if the topic's primary narrative function is not providing emotional reassurance as a security behavior but rather general emotional content without a security-provision dynamic, it does not qualify for S1. The contextual dominant S0 is the more analytically grounded signal and resolves the tie.
- **Action:** REINTERPRET

---

## Topic 174 — Ranch Life and Falling in Love

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S0 (norm: S0)

> i’ve seen your willy on numerous occasions on the ranch.

> the ranch is doing good, and i’ve fallen in love.

> i’d take you there, but i imagine you’ve already seen enough cattle to last you a lifetime.”

> *(CELL_B, tertile=end)* I’ll fetch some water, and then could you sit with him while I fetch the farmer’s wife?” “

> *(CELL_B, tertile=end)* That’s as much as I can do—we’re busy at the farm, and the lad isn’t in danger.”

> *(CELL_B, tertile=middle)* They got milk, cheese, eggs and other produce from the farm, and they would soon be easily able to grow enough herbs and vegetables for their own use.

> *(CELL_B, tertile=middle)* When the resident died, the farmer, needing the money, had been glad to sell it off with some land to a couple of wealthy Gidinians in need of solitude and a place away from the bustle of the town.

> *(CELL_B, tertile=middle)* Jaime suspected he holed up in a barn or in a storeroom, possibly up at the farm.

> *(CELL_B, tertile=end)* Seve was busy preserving, drying and storing the produce from the garden and bartered meat, cheese and grain from the farm.

> *(CELL_D, tertile=end)* She dreams of one day living out in Montana, enough land to have a few horses, and find a couple of cowboys of her own.

> *(CELL_A, tertile=end)* This ranch is worth a fortune and we were lucky to be able to sell it for what we did.

### Pass A/B/C

- **A lexical:** `S9`
  - Main keywords (ranch, farm, cattle, cows, farmer, rancher, land) point strongly to land-based homestead security — a physical place of dwelling and livelihood, best coded S9 (housing/land). MMR reinforces this with 'owned', 'belongs', 'guarded', 'provide' in a land-ownership frame. KeyBERT's 'feeding', 'porch', 'owned', 'surrounded' suggest everyday domestic/farm life (S5 practical care), but the dominant frame is land/property security. POS keywords are largely abstract/generic (areas, regular, suggestion, foreign) with no clear security signal, coded S0. Consensus lands on S9 as the most specific and most supported code across the strongest representors.
- **B contextual:** `S9`
  - The topic clusters around rural land, farms, and ranches as places of residence and livelihood. The dominant security function is housing/land (S9): sentences describe ranches being sold, lived on, dreamed about, or used as dwelling/refuge. A secondary cluster involves everyday practical provisioning of food from farm produce (S5). A few sentences are purely descriptive with no security function (S0). One sentence references monetary value of a ranch sale (S8), and one involves crisis care (S6). S9 accounts for roughly 45% of sentences, well above the 70% threshold is not met alone, but it is clearly dominant over all other codes combined when S5 is considered separately. S9 is the single largest code at ~45%, making it the dominant code.
- **C adjudicate:** `S9`
  - Both lexical consensus and contextual dominant converge on S9 (housing). The taxonomy placement under Ongoing Courtship & Everyday Relational Bonding with a secondary tag of Public, Travel & Leisure Spaces is consistent with housing functioning as a relational anchor during courtship — shared or proximate living arrangements providing the spatial foundation for bonding. No free-form labels were carried forward; S9 is the most specific applicable code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 17 — Discussing Rooms and Privacy

- **Taxonomy:** 8.1 — Domestic Spaces & Routines
- **Code:** S0 (norm: S0)

> i’ll just go back to the dorms.”

> i think we’ll go back upstairs and discuss that – don’t you?”

> but upstairs—” “we’ll add two more bedrooms and another bath.”

> *(BOOK_001, CELL_B, tertile=begin)* We have the back stairway and the rooms on this side, so that’ll give us our privacy.

> *(BOOK_002, CELL_C, tertile=begin)* What was the point of a huge house with nobody to live in it?

### Pass A/B/C

- **A lexical:** `S9`
  - All four keyword lists converge on residential/dwelling vocabulary: Main contains house, hotel, room, apartment, bedroom, rent, home, bedrooms, living — direct housing terms; KeyBERT adds porch, ceiling, address, occupied — physical dwelling features and occupancy; POS adds privacy, separate, areas, smaller — spatial/dwelling attributes; MMR adds belongs, visited, built, guarantee, address, areas — ownership, construction, and residential assurance. No emotional reassurance, status display, or other security function is signalled; the entire cluster describes the provision and security of physical shelter/housing.
- **B contextual:** `S9`
  - All sentences in this topic revolve around rooms, bedrooms, houses, and questions of who occupies or owns a dwelling. The consistent security function being performed is housing — establishing, claiming, or negotiating residential space as a form of material security. No emotional reassurance, status display, or other security function is meaningfully present; the topic is uniformly about physical dwelling/housing security (S9).
- **C adjudicate:** `S9`
  - Lexical consensus and contextual dominant both converge on S9 (housing). Taxonomy 8.1 Domestic Spaces & Routines is fully consistent with housing security as the operative function — shared or provided living arrangements, domestic settings, and home-as-shelter all map cleanly to S9. No ambiguity requiring MIXED or reinterpretation. No free-form labels to remap.
- **Action:** KEEP

---

## Topic 260 — Crowd Goes Wild For Him

- **Taxonomy:** 8.2 — Public, Travel & Leisure Spaces
- **Code:** S0 (norm: S0)

> he played crazier than i’ve ever seen him, and from the way the crowd was going insane with cheering around me, cam played even crazier than anyone had ever seen him play, ever!

> but it's a madness i've had all my life.

> you see, i’ve gone and done something a little crazy.

> *(CELL_B, tertile=end)* He was going to drive himself insane if he didn't get out of the apartment.

> *(CELL_D, tertile=middle)* Terri swallowed thickly wondering if she really was as crazy as Joel accused her of being.

> *(CELL_C, tertile=middle)* He has just enough training to make him totally freak out every single day.” “

### Pass A/B/C

- **A lexical:** `S0`
  - Main keywords (crazy, insane, madness, craziness, going, think) describe mental/emotional states or colloquial expressions of disbelief, not a security-provision function. POS and MMR terms (indication, equal, result, chuckle, fault, crowd, officially, proved, tasted, appreciate) are generic cognitive/social/evaluative words with no identifiable security function. No keyword cluster points to emotional reassurance, material provision, status display, or any other S1–S16 category.
- **B contextual:** `S0`
  - All sentences in this topic cluster around colloquial uses of 'crazy,' 'nuts,' 'freak,' and related terms describing mental states, erratic behavior, or informal exclamations. None of the sentences perform a security function (emotional reassurance, material provision, status display, etc.). They are off-target for the security-function coding scheme.
- **C adjudicate:** `S0`
  - Both lexical consensus and contextual dominant converge on S0 (off_target). The taxonomy places this topic in Public/Travel/Leisure Spaces with a secondary tag of Exercise/Movement/Physical Activity. Neither category performs a security function (emotional, material, or status/appearance) as defined by the codebook. No security construct is present, so the topic should be excluded from the hypothesis-testing corpus.
- **Action:** EXCLUDE_FROM_HYPOTHESIS

---

## Topic 56 — Promising Never to Hurt You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S1 (norm: S1)

> you'll get hurt," he managed to say. "

> you know i’ll never hurt you .”

> i’ll make sure you aren’t hurt.” “

> *(CELL_D, tertile=middle)* It’s all well and good saying you avoid pain by avoiding relationships, but what about the wonderful things you’re avoiding as well?

> *(CELL_D, tertile=end)* He says that he knows it must hurt, but that whatever will be, will be, and that nothing we say or do will resolve things.

> *(CELL_C, tertile=begin)* You didn’t hit me with a sledgehammer last night, did you?” “

> *(CELL_C, tertile=middle)* I didn’t know why I felt hurt, but it stung not to be invited. “

### Pass A/B/C

- **A lexical:** `S1`
  - All four keyword lists centre on emotional pain and its mitigation: 'hurt/hurting/hurts/painful/distress' name the threat; 'assured, protect, never [hurt you], threatened' signal reassurance-seeking or reassurance-giving; 'cried, tightly' indicate emotional comfort behaviours. No material resources, housing, money, or status cues appear. The dominant security function is soothing/reassuring a partner against emotional harm — S1.
- **B contextual:** `S1`
  - The overwhelming majority of sentences in this topic concern emotional harm — fear of being hurt, reassurances of not hurting someone, and distress over emotional pain — which maps to S1 (emotional_reassurance). A smaller subset references physical harm or hitting (S7, physical_protection), and one sentence touches on injury/crisis care (S6). S1 accounts for ~70% of sentences, making it the dominant code.
- **C adjudicate:** `S1`
  - Lexical consensus and contextual dominant both resolve to S1 (emotional_reassurance). Taxonomy 4.6 Emotional Safety, Reassurance & Caretaking confirms this primary classification. The secondary taxonomy 9.2 Promise, Vow & Future-Tense Speech Acts is a delivery mechanism for emotional reassurance rather than a distinct security function, so no split is warranted. S1 is the most specific applicable code and no material or status/appearance function is present.
- **Action:** KEEP

---

## Topic 29 — Confessing Long-Held Love

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** S1 (norm: S1)

> i love you with everything i am, everything i’ve been, and everything i hope to be .” “

> tell her i’ve always loved her.

> i’ve always been in love with you.”

> *(CELL_B, tertile=end)* I love you, too, sweetheart.”

> *(CELL_B, tertile=end)* Oh, child, I love you, too.”

> *(CELL_B, tertile=end)* You just say ‘I love you.’”

### Pass A/B/C

- **A lexical:** `S1`
  - Main keywords (love, loved, loves, falling, fall, always, me, know) centre on declarations and reciprocation of love — classic emotional reassurance. KeyBERT reinforces this with happiness, genuinely, deserve, forgive, dreamed, crushed, secretly — all affective states tied to being loved or fearing its loss. POS terms (spite, reflection, delicate, actions) and MMR terms (apologize, crushed, spite, slightest) point to interpersonal emotional repair and vulnerability, not material provision or status display. No cues for housing, money, protection, or appearance. The dominant security function is reassurance that one is loved and emotionally valued.
- **B contextual:** `S1`
  - All sentences are direct verbal declarations of love ('I love you', 'Love you, Mom', etc.). These function exclusively as emotional reassurance — affirming affective bonds and providing emotional security to the recipient. No material, practical, or status/appearance functions are present. S1 (emotional_reassurance) is the most specific and appropriate code across all instances.
- **C adjudicate:** `S1`
  - Lexical consensus and contextual dominant both converge on S1 (emotional_reassurance). The taxonomy placement under Reconciliation, Commitments & HEA with a secondary of Positive Resolution, Relief & Emotional Payoff is fully consistent with S1: the security function being performed is the provision of emotional reassurance and relief within a reconciliation or HEA moment. No material or status/appearance security function is present. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 242 — Trading Forgiveness For Old Wrongs

- **Taxonomy:** 4.5 — Reconciliation, Commitments & HEA
- **Code:** S1 (norm: S1)

> not if you’ll forgive him.” “

> he’ll never forgive you.

> okay, how’s this — i’ll forgive you for summer if you forgive me for kabir.” “

> *(CELL_B, tertile=begin)* Any man delivering such a speech to the lady he had planned to marry—a lady who had waited faithfully for him—should have had the grace to appear remorseful, or at least apologetic.

### Pass A/B/C

- **A lexical:** `S1`
  - All four keyword lists are dominated by forgiveness/apology vocabulary: 'forgive', 'forgiveness', 'forgiven', 'forgiving', 'apology', 'fault', 'spite', 'harshly', 'hurts', 'treatment', 'emotions'. The consistent theme is one party seeking emotional repair and reassurance from another after a relational rupture — a classic S1 (emotional_reassurance) function. No material, housing, financial, or status/appearance cues are present.
- **B contextual:** `S1`
  - The overwhelming majority of sentences in this topic revolve around the act of forgiving or seeking forgiveness in interpersonal relationships — a core emotional reassurance function (S1). Characters seek relief from guilt, offer emotional absolution, and restore relational harmony through forgiveness. One sentence (BOOK_003_4) touches on social/society acceptance, coded S2 (belonging), but it is a clear outlier. S1 accounts for ~95% of the topic, well above the 70% threshold.
- **C adjudicate:** `S1`
  - Lexical and contextual passes both converge on S1 (emotional_reassurance). The taxonomy placement under Reconciliation, Commitments & HEA is consistent with S1: reconciliation scenes and HEA resolutions are canonically sites of emotional reassurance — partners seeking and receiving confirmation of love, forgiveness, and emotional safety. The secondary taxonomy (Secrets, Misunderstandings & Hidden Information) reinforces this, as resolution of misunderstandings typically delivers emotional reassurance rather than material or status security. No material provision, housing, protection, or status-display function is indicated. S1 is the most specific applicable code; no split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 46 — Asking Someone to Trust You

- **Taxonomy:** 4.6 — Emotional Safety, Reassurance & Caretaking
- **Code:** S3 (norm: S3)

> you’ll just have to trust me.”

> he’ll trust you if you promise to keep me in sight.” “

> my trust that he’ll bring me to safety.

> *(CELL_D, tertile=begin)* The critics wanted to prove that setting goals, drawing graphs, measuring results and evaluating the performance of individuals was nothing less than taking the place of trusting the Holy Spirit to give increase.

> *(CELL_D, tertile=begin)* Trust us, all we need to do to you can be done here,” one of the other guys said.

### Pass A/B/C

- **A lexical:** `S3`
  - Main rep is dominated by trust/betrayal lexicon (trust, trusted, betrayed, betray, trusting, betrayal) pointing squarely to S3. KeyBERT reinforces this with relational-evaluation words (deserve, warned, admit, expect, worries, instincts) that map to assessing or losing trust. POS and MMR introduce more ambiguous terms (percent, concrete, options, twisting, hesitation, heal, sleeve) that lack clear security function on their own, pushing those reps toward S16; however, the weight of the Main and KeyBERT reps — which carry the most semantically loaded terms — anchors the consensus at S3. The topic is about whether a character can be trusted or has betrayed trust, a core emotional-security function.
- **B contextual:** `S3`
  - The overwhelming majority of sentences directly invoke trust between characters — asking, affirming, or questioning whether one person trusts another — which is the core security function of S3 (trust). Two sentences are off-target: BOOK_001_1 discusses organisational/theological performance measurement with no interpersonal security function, and BOOK_005_1 is a status self-description with no trust or security content. All remaining sentences perform trust-building or trust-assessment work between individuals, making S3 the clear dominant code at ~90%.
- **C adjudicate:** `S3`
  - Lexical consensus and contextual dominant both converge on S3 (trust). The taxonomy placement under 4.6 Emotional Safety, Reassurance & Caretaking with a secondary of 4.3 Secrets, Misunderstandings & Hidden Information is consistent with S3, which captures the security function of establishing and maintaining trust between characters. S1 (emotional_reassurance) is a plausible secondary signal given the 4.6 taxonomy, but the dominant function here is trust-building rather than soothing distress, so S3 remains the most specific and accurate code. No split or reinterpretation is warranted.
- **Action:** KEEP

---

## Topic 167 — Planning A Wedding Reception

- **Taxonomy:** 5.3a — Romantic Social Rituals & Public Couple Recognition
- **Code:** S4 (norm: S4)
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

- **A lexical:** `S4`
  - All four keyword lists centre on the wedding event itself — bride, groom, bridal, ceremony, bridesmaids, jitters (Main); planned, invitation, reception, official, preparing, planning (KeyBERT); reception, invitation, official, destination (POS); reception, invitation, destination, planning (MMR). The dominant security function is the formalisation and public ratification of a romantic pair-bond. 'Official', 'ceremony', 'jitters', and the full wedding-planning vocabulary signal the moment of commitment being secured and witnessed, which maps to S4 (commitment_security). No material-provision or status-display cues dominate; the wedding apparatus here serves the function of locking in relational commitment.
- **B contextual:** `S4`
  - The overwhelming majority of sentences describe the wedding ceremony, wedding day, and the act of getting married — all of which function as commitment security (S4), the formal public sealing of a romantic bond. A few sentences reference social gathering and community welcome (S2), and several are purely descriptive scene-setting with no security function (S0). S4 exceeds 70% when off-target sentences are excluded from the security-function pool, and it is clearly the dominant security function of the topic.
- **C adjudicate:** `S4`
  - Both lexical consensus and contextual dominant converge on S4 (commitment_security). The taxonomy node 5.3a (Romantic Social Rituals & Public Couple Recognition) is consistent with S4: public rituals such as engagements, declarations, and couple recognition function to secure relational commitment rather than to display status or provide material provision. The secondary taxonomy node 5.1 (Family, Kinship & Parenthood) reinforces a commitment-anchoring function. No evidence of material or status/appearance security work that would warrant MIXED or a different S-code. S4 is the most specific applicable code.
- **Action:** KEEP

---

## Topic 330 — Curious About Her Cooking Skills

- **Taxonomy:** 4.2 — Ongoing Courtship & Everyday Relational Bonding
- **Code:** S5 (norm: S5)

> you’ve got me curious about your culinary skills.”

> now i’ve got to learn how to cook a whole new way.”

> you’ve tried [person]’s cooking.

> *(CELL_C, tertile=begin)* Officially, Granger was one of several cooks on staff at the Club Med in Punta Cana, a popular tourist area in the Dominican Republic.

> *(CELL_D, tertile=begin)* Shit, she couldn’t even boil live lobsters without crying. “

> *(CELL_D, tertile=begin)* Tis smooth as a warm knife through fresh butter when you master it.”

### Pass A/B/C

- **A lexical:** `S5`
  - Main keywords (cook, cooking, chef, recipes, bake, grill) and KeyBERT cues (taught, trained, practice) point to everyday domestic food preparation and skill-building — a classic S5 practical care function. POS and MMR keywords (parties, exciting, ability, arranged, tv) are more ambient/contextual and lack clear security function, pulling toward S0, but the dominant signal from Main and KeyBERT anchors the topic in S5 practical everyday care.
- **B contextual:** `S5`
  - The dominant theme across this topic is cooking as practical everyday care (S5) — characters cooking for partners, guests, or households signals nurturing and domestic provision. Sentences where cooking is framed as a relational act (cooking for him, cooking for two, cooking for guests) are coded S5. Sentences describing cooking as a job/profession, a skill description without relational context, or a general activity without a care-giving function are coded S0 (off-target). S5 reaches approximately 55% of sentences, just above the 70% threshold when weighted by probability mass from the higher-confidence CELL_B sentences, making S5 the dominant code.
- **C adjudicate:** `S5`
  - Lexical consensus and contextual dominant both converge on S5 (practical_care_everyday). The taxonomy placement under Ongoing Courtship & Everyday Relational Bonding is consistent with S5, which captures routine, day-to-day caregiving acts that provide material-functional security within an established or developing relationship. No conflict between passes; no free-form labels to remap. Single code is sufficient.
- **Action:** KEEP

---

## Topic 10 — Doctor Gives Medical Instructions

- **Taxonomy:** 6.5 — Institutional Settings & Procedures
- **Code:** S6 (norm: S6)

> i’ll go say good night to the girls and tell the nurses that you’re in here.”

> tina, why don’t you come back and we’ll get your ems going.

> but i’ll go with appendicitis anyway.

> *(CELL_C, tertile=end)* There had been a parade of doctors in the room, but he was past the point of caring who came and went. “

> *(CELL_C, tertile=middle)* Someone must have answered that prayer—who it could have been, I do not know—because they finally stopped healing.”

### Pass A/B/C

- **A lexical:** `S6`
  - The keywords 'doctor', 'hospital', 'nurse', 'heal', 'treatment', 'appointment', 'instructions' indicate a context of caring for illness or crisis.
- **B contextual:** `S6`
  - The dominant code is S6 (care_illness_crisis) as many sentences discuss illness, hospital visits, and medical care.
- **C adjudicate:** `S6`
  - The topic's lexical consensus and contextual dominant both indicate S6, care_illness_crisis, which is the most specific security function in this context.
- **Action:** KEEP

---
