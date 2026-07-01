SEXUAL_LABELING_RULES = """
SEXUAL AND INTIMACY CLASSIFICATION (v3 — JSON fields first, natural label second)

Step 1 — set sexual_explicitness and sexual_function from snippets + all keyword representations.
Step 2 — set consent_status when boundary or coercion signals appear.
Step 3 — write label in NATURAL LABEL VOICE (2–6 words, scene-visible beat only).

sexual_explicitness:
- none: no sexual or romantic bodily content (work, transit, abstract dialogue)
- affection_only: kissing, hugging, cuddling, hand-holding, gentle touch without explicit arousal
- suggestive: desire, tension, undressing, private lodging, bodily heat, pre-sex escalation
- explicit: genital terms, orgasm, penetration, oral sex, condom/lube preparation, described sex acts

sexual_function — choose the DOMINANT narrative function (never leave none for romantic physical topics):
- nonsexual_affection: gentle kisses, hugs, goodnight kisses, cautious step closer, flirtatious wink/smile, reassuring hug
- sexual_tension: desire, visual admiration, compliments on appearance, stolen glances, sweat/heat/flushed skin in charged scenes, overheard pleasure sounds, taste during kissing, hotel room leads to bed
- presex_escalation: undressing, bed positioning, buttons/zippers, towel after shower, crawling onto bed
- contraception_preparation: condoms, lube, bedside drawer
- sexual_negotiation: agreeing to stop when asked, negotiating when sex should happen (without coercion signals)
- explicit_contact: intercourse, forceful sex positioning, straining erection through clothing
- orgasm_climax: approaching orgasm, eyes closed near climax
- postsex_aftercare / postsex_arousal: tenderness or continued arousal after sex
- sex_without_commitment: sex vs emotional commitment debate
- consent_boundary: unwanted touch, coercion, threats

Common mistakes to avoid:
- Do NOT use sexual_function none for romantic approach, hugs, or kisses — use nonsexual_affection
- Do NOT use sexual_tension for straining erection / explicit arousal through clothing — use explicit_contact
- Do NOT use consent_boundary for consensual "stop when asked" negotiation — use sexual_negotiation
- NEVER use label "Character Name Artifact" or route to noise for name-heavy Main alone

LABEL vs JSON: analytic function in sexual_* JSON fields; label stays fluent index-style (picture test).

Consent: do not infer non-consent from intensity alone. coercion_watchlist only when snippets
show refusal, fear, pressure, threat, captivity, or inability to stop.
""".strip()

SEXUAL_FEW_SHOTS = """
FEW-SHOT EXAMPLES FOR SEXUAL TOPICS (natural scene-visible labels + v3 JSON fields):

Example G — contraception preparation:
Keywords: condom, condoms, lube, drawer, nightstand
→ label: "Condom And Lube Preparation"
→ sexual_explicitness: explicit, sexual_function: contraception_preparation

Example H — suggestive undressing:
Keywords: fumbled, buttons, zipper, shirt, thigh
→ label: "Fumbling With Buttons And Zippers"
→ sexual_explicitness: suggestive, sexual_function: presex_escalation

Example I — forceful sex, unclear consent:
Keywords: backs, mattress, bed, pinned, throw
→ label: "Pounding Into The Mattress"
→ sexual_explicitness: explicit, sexual_function: explicit_contact,
  consent_status: unclear_from_topic

Example J — sex without commitment:
Keywords: sex, commitment, relationship, casual, agreement
→ label: "Choosing Sex Without Commitment"
→ sexual_function: sex_without_commitment

Example K — cautious approach:
Keywords: step, closer, hesitant, distance
→ sexual_function: nonsexual_affection
→ label: "Cautious Step Closer"

Example L — stolen glances:
Keywords: appearance, struck, stranger, beautiful, glances
→ sexual_function: sexual_tension
→ label: "Stolen Glances And Admiration"

Example M — agreeing to stop:
Keywords: stop, asked, agree, wait
→ sexual_function: sexual_negotiation
→ label: "Agreeing To Stop When Asked"

Example N — tender kiss with rising desire:
Keywords: kiss, kissed, lips, gentle, cupped, gripped, bodies
→ sexual_function: nonsexual_affection
→ label: "Tender Kiss With Rising Desire"

Example O — hair touching:
Keywords: hair, fingers, touch, flirt
→ sexual_function: nonsexual_affection
→ label: "Fingers Threading Through Hair"

Example P — possessive kissing desire:
Keywords: mouth, kiss, longing, claim
→ sexual_function: sexual_tension
→ label: "Longing To Claim Her Mouth"

Example Q — sweat-soaked bodies in charged scene:
Keywords: sweat, heat, soaked, exertion, flushed
→ sexual_function: sexual_tension
→ label: "Sweat-Soaked Bodies"

Example R — hotel room leads to bed:
Keywords: hotel, room, bed, privacy, suitcase
→ sexual_function: sexual_tension
→ label: "Hotel Room Leads To Bed"

Example S — coercion threats over touch:
Keywords: touch, break, hands, kill, family, suffer
→ sexual_function: consent_boundary, consent_status: coercion_watchlist
→ label: "Break Your Hands If You Touch Her"

Example T — still hard after sex:
Keywords: worn, cock, pulling, hips, rock hard
→ sexual_function: postsex_arousal, sexual_explicitness: explicit
→ label: "Worn Out But Still Hard"
""".strip()
