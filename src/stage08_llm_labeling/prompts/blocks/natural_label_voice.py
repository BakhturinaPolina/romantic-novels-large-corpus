NATURAL_LABEL_VOICE = """
NATURAL LABEL VOICE (CRITICAL)

Write labels the way a romance scholar would name a theme in a book index — fluent English, not a keyword bag.

PICTURE TEST: If you cannot imagine a 3-second film clip from the label alone, rewrite it.

LABEL STYLE: [Concrete action or line-echo] + [optional body part / setting]
Put analytic function in JSON fields (sexual_function, sexual_explicitness) — NEVER in the label.

GOOD labels (scene-visible):
- "Tender Kiss With Rising Desire", "Cautious Step Closer", "Complimenting Her Appearance"
- "Hotel Room Leads To Bed", "Break Your Hands If You Touch Her", "Goodnight Kiss At The Door"
- "Fumbling With Buttons", "Publisher Copyright Page", "Whispered Dialogue"

BAD labels (unnatural — NEVER do this):
- Analytic qualifiers: "With Sexual Subtext", "With Possible Escalation", "During Reunion", "Post-Sex Arousal"
- Keyword chains: "Plump Squeeze With Fingertips", "Damp Lungs And Rear"
- Slash compounds: "Verbal Physical Admiration / Attraction", "Post-Shower Body Display / Bathroom Intimacy"
- Double-function joins: "Explicit Sexual Contact And Post-Sex Arousal"
- Vague buckets: "Threat Of Unwanted Touch", "Visual Attraction To A Stranger" (name the visible beat instead)
- Academic jargon: "Statistical Possibility Speech", "Negotiating Private Lodging"
- Genre clichés: "Intimate Moment", "Heated Encounter", "Claiming Her Mouth", "Bedroom Encounter"
- Meta name labels: "Character Name Artifact", "Name Artifact", "Name References", "Name Cluster"
- Over-literal POS dumps: stacking 3+ bare keywords with "And"

scene_summary rules:
- One sentence, 12–25 words: who + does what + to whom (a mini-scene a human would write).
- Do NOT use analytic words: subtext, escalation, negotiation, arousal, tension, intimacy (as abstract nouns).
- Do not echo keyword lists; paraphrase snippets into readable prose.

Label rules:
- Use 2–6 words; Title Case; one central visible beat.
- Paraphrase keywords into readable prose ("rear" + "doorway" → "Doorway Hesitation", NOT "Rear And Doorway").
- If snippets are missing, stay conservative — do not invent body parts or settings absent from evidence.
- Vary wording across topics — do not reuse vague words ("charged", "intimate") without a concrete beat.
""".strip()
