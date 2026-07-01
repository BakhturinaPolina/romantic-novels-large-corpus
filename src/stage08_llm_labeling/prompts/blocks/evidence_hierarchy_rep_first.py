EVIDENCE_HIERARCHY_REP_FIRST = """
EVIDENCE HIERARCHY (highest → lowest weight)

STEP 1 — Infer the topic thread (do this BEFORE using snippets for the label):
1. ALL KEYWORDS union (KeyBERT + MMR + POS; Main excluded) — primary semantic field
2. KeyBERT + MMR together — salient and diverse terms that define scene vs discourse
3. POS keywords — content-word anchors (nouns, verbs, adjectives)

STEP 2 — Ground and polish (do NOT let these override the keyword thread):
4. Representative snippets — concretize the keyword thread into a visible beat; pick ONE typical micro-scene
5. Main representation — lowest weight; often dialogue glue ("I'll", "come", "tell"), character names, or high-frequency verbs

KEYWORD-THREAD RULE (CRITICAL):
- The label must reflect the shared semantic field across KeyBERT + MMR + POS + ALL KEYWORDS.
- Snippets confirm or sharpen that thread — they do NOT replace it when they show only one narrow variant.
- Main never defines the label when KeyBERT/MMR/POS cohere on a different theme.

SNIPPET TRAP (avoid):
Topics clustered on future-tense promises ("I'll…", "we'll…") often have bland scheduling snippets
("see you tomorrow", "I'll call you back") while MMR/POS show heavier beats (confessed, resigned,
weapons, session, threats, horrified). Label the KEYWORD thread, not the blandest snippet.
Use snippets in scene_summary for a concrete example, not to shrink the label.

CONFLICT RESOLUTION:
- Keywords cohere + snippets are narrow literal glue → trust keywords for label; use snippets for scene_summary detail
- Keywords sparse/incoherent + snippets share a clear thread → trust snippets (discourse/noise cases)
- Keywords and snippets disagree on content_type → re-read ALL KEYWORDS; prefer discourse when keywords are abstract/speech-tag heavy with no setting nouns
- Main conflicts with everything else → ignore Main unless snippets and keywords are both empty

When Stage07 flags conflict with the keyword thread, override only if snippets AND keywords both support the flag.
""".strip()

STAGE07_EMPHASIZE_REP_FIRST = """
STAGE07 HINTS (IMPORTANT): Post-hoc flags are often correct for publisher_boilerplate topics,
but may false-positive on real scenes. Override when the keyword thread (KeyBERT/MMR/POS) OR
snippets clearly contradict the flag; cite which evidence layer supports the override.
""".strip()

CHARACTER_NAMES_REP_FIRST_ADDENDUM = """
REP-FIRST SNIPPET vs KEYWORD BALANCE:
- When one snippet is clearly dominant AND KeyBERT/MMR/POS support the same beat, anchor the label there.
- If snippets show a narrow literal line but keywords show a broader shared field, label the keyword field.
- Examples: reunion longing → "Frantic Longing After Separation"; romantic rival talk → "Discussing A Romantic Rival";
  resigned confession cluster → "Resigned Promise To Return" (NOT "Plans to Meet Tomorrow" from one scheduling snippet).
""".strip()
