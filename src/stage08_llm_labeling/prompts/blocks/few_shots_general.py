GENERAL_FEW_SHOTS = """
FEW-SHOT EXAMPLES (follow these patterns — no category taxonomy):

Example A — generic dialogue:
Keywords: wanted, need, tell, know, don
→ content_type: discourse
→ label: "Promises About the Future", exclude_from_axes: false

Example B — whispered delivery:
Keywords: whispered, murmured, breathlessly, softly
→ content_type: discourse
→ label: "Whispered Dialogue", exclude_from_axes: false

Example C — intimacy / kissing:
Keywords: kissed, lips, mouth, tongue (no explicit genital terms)
→ content_type: scene, sexual_explicitness: affection_only
→ label: "Deep Kissing", sexual_function: nonsexual_affection or sexual_tension

Example D — subgenre:
Keywords: werewolf, pack, shifted, alpha
→ content_type: subgenre_marker
→ label: "Shifter Pack Scene"

Example E — publisher noise:
Keywords: chapter, copyright, published, author, book
→ is_noise: true, content_type: noise, exclude_from_axes: true
→ label: "Publisher Copyright Page"

Example F — phone medium:
Keywords: texted, phone, buzzed, message, screen
→ content_type: scene
→ label: "Text Message Notifications"

Example H — courtship / goodnight:
Keywords: date, dinner, tomorrow, call, door, kiss
→ content_type: scene, sexual_function: nonsexual_affection
→ label: "Goodnight Kiss At The Door"
""".strip()
