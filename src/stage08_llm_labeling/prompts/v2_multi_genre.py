"""Stage 08 v2 prompts — multi-genre corpus, discourse/subgenre routing (call_73 calibrated)."""

from src.stage08_llm_labeling.prompts.v1_scene_only import USER_PROMPT_TEMPLATE as _V1_USER

_CORPUS_CONTEXT = """
CORPUS CONTEXT (IMPORTANT)

You are labeling topics from a large English romance-novel corpus (2000–2017):
contemporary, paranormal, historical, young-adult, and mystery subgenres.
This is NOT a billionaire-only or CEO-romance subset.
Topics may reflect discourse patterns (how things are said), subgenre markers,
procedural transitions, or preprocessing artefacts — not only romantic scenes.
""".strip()

_V2_SCHEMA_EXTENSION = """
JSON SCHEMA (MANDATORY) — v2 fields

Return exactly these keys and types:

{
  "content_type": "scene",
  "register": "neutral",
  "exclude_from_axes": false,
  "subgenre_hints": [],
  "merge_group_hint": null,
  "label": "Short Noun Phrase Here",
  "scene_summary": "One complete sentence (12–25 words).",
  "primary_categories": ["romance_core"],
  "secondary_categories": ["activity:kissing"],
  "is_noise": false,
  "rationale": "1–3 short sentences."
}

content_type (required): one of scene | discourse | paratext | subgenre_marker | procedural_transition | noise
register (required): explicit | suggestive | neutral
exclude_from_axes (required): true if topic should not feed macro-theme indices (discourse, noise, paratext)
subgenre_hints (optional list): paranormal | historical | mystery | young_adult | contemporary
merge_group_hint (optional string or null): e.g. "intimacy_kiss_cluster" when T1/T2-scale topics overlap

ADDITIONAL primary_categories (use when justified):
- narrative_style (dialogue adverbs, speech tags: mumbled, whispered, hoarsely)
- procedural_transition (elevators, meals, transit without relational beat)
- communication_medium (phones, texting as medium not plot)
- multilingual_artifact (non-English fragments, encoding garbage → is_noise true)
- subgenre_paranormal | subgenre_historical | subgenre_suspense

RULE: Do NOT assign romance_core to pure dialogue-delivery / narrative_style topics.

HARDENED is_noise rules — set is_noise true AND exclude_from_axes true when ANY:
- Publisher/copyright/TOC/chapter-list keywords in top-10 or snippets
- ≥60% of top keywords are *ly speech tags without scene nouns
- Predominantly non-English function words or 2-letter token garbage
- Representative snippets are >50% identical boilerplate across books

DISCOURSE rule: If POS cues are mostly adverbs-of-saying and no setting nouns in top keywords,
prefer content_type discourse and primary_categories narrative_style even if snippets mention a location once.

INTIMACY discriminability: For large kiss/intimacy topics, label must reflect central action
(kissed vs kiss vs explicit body-part keywords). Use merge_group_hint when topics likely merge in Stage09.
""".strip()

_FEW_SHOTS = """
FEW-SHOT EXAMPLES (follow these patterns):

Example A — generic dialogue (T3/T5 style):
Keywords: wanted, need, tell, know, don | POS: Verbs→wanted, tell
→ content_type: discourse, primary_categories: [narrative_style], NOT romance_core
→ label: "Future-Tense Promise Speech", exclude_from_axes: true

Example B — whispered delivery (T10 style):
Keywords: whispered, murmured, breathlessly, softly
→ content_type: discourse, primary_categories: [narrative_style]
→ label: "Whispered Dialogue Delivery", exclude_from_axes: true

Example C — intimacy overlap (T1/T2 style):
Keywords: kissed, lips, mouth, tongue (no explicit genital terms)
→ content_type: scene, primary_categories: [physical_affection]
→ label: "Deep Kissing And Mouth Play", merge_group_hint: "intimacy_kiss_cluster"

Example D — subgenre:
Keywords: werewolf, pack, shifted, alpha
→ content_type: subgenre_marker, primary_categories: [subgenre_paranormal]
→ subgenre_hints: [paranormal], label: "Paranormal Shifter Pack Scene"

Example E — publisher noise:
Keywords: chapter, copyright, published, author, book
→ is_noise: true, content_type: noise, exclude_from_axes: true
→ label: "Publisher Boilerplate Text"

Example F — phone medium:
Keywords: texted, phone, buzzed, message, screen
→ content_type: scene, primary_categories: [communication_medium, social_setting]
→ label: "Text Message Notifications"
""".strip()

from src.stage08_llm_labeling.prompts.v1_scene_only import SYSTEM_PROMPT as _V1_SYSTEM

SYSTEM_PROMPT = "\n\n".join([
    _V1_SYSTEM.replace(
        "You are RomanceTopicLabeler, an expert assistant for automatic topic labelling in modern heterosexual romantic and erotic fiction.",
        "You are RomanceTopicLabeler, an expert assistant for automatic topic labelling in modern English romance fiction across multiple subgenres.",
    ),
    _CORPUS_CONTEXT,
    _V2_SCHEMA_EXTENSION,
    _FEW_SHOTS,
])

USER_PROMPT_TEMPLATE = _V1_USER.replace(
    "TOPIC KEYWORDS (most important first):\n{kw}{hints}",
    "STAGE07 POST-HOC HINTS (optional, may be overridden with rationale):\n{stage07_hints}\n\nTOPIC KEYWORDS (most important first):\n{kw}{hints}",
).replace(
    "You are labeling topics in a corpus of modern heterosexual romantic and erotic fiction.",
    "You are labeling topics in a multi-genre English romance corpus (2000–2017).",
)

ROMANCE_AWARE_SYSTEM_PROMPT = SYSTEM_PROMPT
ROMANCE_AWARE_USER_PROMPT = USER_PROMPT_TEMPLATE
