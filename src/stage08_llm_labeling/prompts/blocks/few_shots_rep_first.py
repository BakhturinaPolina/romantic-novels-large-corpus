REP_FIRST_FEW_SHOTS = """
REP-FIRST FEW-SHOT EXAMPLES (keyword thread defines label; snippets ground it):

Example L — snippet trap; keywords win:
ALL KEYWORDS: confessed, resigned, session, weapons, pathetic, realization, explanation, invite, suggest
KeyBERT/MMR: resigned, confessed, session, inevitable, weapons
Snippets: "I'll see you tomorrow at the barn", "I just hope you'll come", "I'll come back later tonight"
Main: leave, stay, come, go, ll, you
→ WRONG label: "Plans to Meet Tomorrow" (literal snippet only)
→ RIGHT label: "Resigned Promise To Return" or "Confession Before Leaving"
→ rationale cites confessed/resigned/session/weapons first; barn snippet used only in scene_summary

Example M — keywords + snippets agree (snippets still ground):
ALL KEYWORDS: kissed, lips, tongue, mouth, whimpered, bodies
Snippets: soft lip press, temple brush kiss
→ label: "Soft Kiss Turning Urgent" (keywords and snippets align — no conflict)

Example N — narrow snippet, broader keyword thread:
ALL KEYWORDS: stalked, darted, peered, muffled, voices, doorway, hovering, entrance
Snippets: "I'll give you a ride home", "grab a taxi back to the hotel", "driving straight through"
Main: door, car, open, room, truck
→ WRONG label: "Offering A Ride Home" (scheduling snippet only)
→ RIGHT label: "Tense Approach Through Doorway" or "Hovering At The Entrance"
→ rationale cites stalked/muffled/voices/doorway first

Example O — keywords sparse; snippets define (discourse/noise path unchanged):
ALL KEYWORDS: chapter, copyright, published, author, book
Snippets: copyright page text, ISBN line
→ is_noise: true, label: "Publisher Copyright Page" (keywords and snippets agree)
""".strip()
