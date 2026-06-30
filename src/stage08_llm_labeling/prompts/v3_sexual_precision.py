"""Stage 08 v3 prompts — v2/c8 base + sexual-function JSON fields, natural label voice."""

from src.stage08_llm_labeling.prompts.v1_scene_only import SYSTEM_PROMPT as _V1_SYSTEM
from src.stage08_llm_labeling.prompts.v2_multi_genre import (
    _CORPUS_CONTEXT,
    _FEW_SHOTS,
    _TAXONOMY_ALIGNMENT,
    _V2_SCHEMA_EXTENSION,
)
from src.stage08_llm_labeling.prompts.v2_variants import (
    _C8_CHARACTER_NAMES,
    _C8_FEW_SHOT_APPEND,
    _STAGE07_EMPHASIZE,
    _USER_SNIPPETS_FIRST,
)

_V3_SCHEMA_EXTENSION = """
JSON SCHEMA (MANDATORY) — v3 sexual-precision fields (extends v2)

Classify sexual_explicitness and sexual_function internally BEFORE writing label.
The label itself must stay fluent and natural (see NATURAL LABEL VOICE) — put analytic
function in the JSON fields below, not clinical jargon in the label string.

{
  "content_type": "scene",
  "register": "neutral",
  "exclude_from_axes": false,
  "subgenre_hints": [],
  "merge_group_hint": null,
  "sexual_explicitness": "none",
  "sexual_function": "none",
  "consent_status": "not_applicable",
  "axis_hint": "everyday_intimacy_emotional_safety",
  "label": "Short Noun Phrase Here",
  "scene_summary": "One complete sentence (12–25 words).",
  "primary_categories": ["romance_core"],
  "secondary_categories": ["activity:kissing"],
  "is_noise": false,
  "rationale": "1–3 short sentences."
}

sexual_explicitness: none | affection_only | suggestive | explicit
sexual_function: none | nonsexual_affection | sexual_tension | presex_escalation |
  contraception_preparation | sexual_negotiation | explicit_contact | orgasm_climax |
  postsex_aftercare | postsex_arousal | sex_without_commitment | consent_boundary
consent_status: not_applicable | consensual_implied | unclear_from_topic |
  coercion_watchlist | nonconsent_explicit
axis_hint: everyday_intimacy_emotional_safety | sexual_tension_explicit_intimacy |
  consent_control_risk | exclude_from_axes

Secondary tags for sexual topics: sexual:contraception, sexual:negotiation,
risk:coercive_control, intimacy:consent_negotiation
""".strip()

_SEXUAL_LABELING_RULES = """
SEXUAL AND INTIMACY CLASSIFICATION (v3 — JSON fields first, natural label second)

Step 1 — set sexual_explicitness and sexual_function from keywords + snippets.
Step 2 — set consent_status and axis_hint.
Step 3 — write label in NATURAL LABEL VOICE (2–5 words, romance index style).

LABEL vs JSON SPLIT (CRITICAL):
- sexual_function / axis_hint carry the analytic category for Stage09 axes.
- label must read like a romance theme index entry — fluent English, not a taxonomy code.
- NEVER put words like "coercion", "male member", "towel-clad", or keyword dumps in labels.
- Paraphrase body-part keywords into readable beats ("Deep Kissing", "Flirtatious Hair Touching").

Good label + JSON pairings:
- function=contraception_preparation → label "Condom And Lube Preparation" (not "Condom Availability Discussion")
- function=presex_escalation → label "Undressing During Tension" (not "Fumbling With Zippers")
- function=explicit_contact, unclear consent → label "Forceful Sex In Bed" (not "Forceful Pounding Into Mattress")
- function=sex_without_commitment → label "Sex Without Commitment" (not "Weighing Sex Without Emotional Commitment")
- function=nonsexual_affection → label "Tender Goodnight Kiss" (not "Goodnight Farewell At Door")
- function=consent_boundary → label "Unwanted Touch Confrontation" (not "Threatening Touch With Coercion")

Avoid vague clichés: "Intimate Moment", "Heated Encounter", "Claiming Her Mouth", "Bedroom Encounter".

Consent: do not infer non-consent from intensity alone. coercion_watchlist only when snippets
show refusal, fear, pressure, threat, captivity, or inability to stop.
""".strip()

_V3_FEW_SHOTS = """
FEW-SHOT EXAMPLES FOR SEXUAL TOPICS (natural labels + v3 JSON fields):

Example G — contraception preparation:
Keywords: condom, condoms, lube, drawer, nightstand
→ label: "Condom And Lube Preparation"
→ sexual_function: contraception_preparation, axis_hint: sexual_tension_explicit_intimacy

Example H — suggestive undressing:
Keywords: fumbled, buttons, zipper, shirt, thigh
→ label: "Undressing In Tension"
→ sexual_function: presex_escalation, register: suggestive

Example I — forceful sex, unclear consent:
Keywords: backs, mattress, bed, pinned, throw
→ label: "Forceful Sex In Bed"
→ sexual_function: explicit_contact, consent_status: unclear_from_topic,
  axis_hint: consent_control_risk

Example J — sex without commitment:
Keywords: sex, commitment, relationship, casual, agreement
→ label: "Sex Without Commitment"
→ sexual_function: sex_without_commitment
""".strip()

_V3_SYSTEM_BASE = _V1_SYSTEM.replace(
    "You are RomanceTopicLabeler, an expert assistant for automatic topic labelling in modern heterosexual romantic and erotic fiction.",
    "You are RomanceTopicLabeler, an expert assistant for automatic topic labelling in modern English romance fiction across multiple subgenres.",
)

SYSTEM_PROMPT = "\n\n".join([
    _V3_SYSTEM_BASE,
    _CORPUS_CONTEXT,
    _V2_SCHEMA_EXTENSION,
    _TAXONOMY_ALIGNMENT,
    _STAGE07_EMPHASIZE,
    _C8_CHARACTER_NAMES,
    _FEW_SHOTS,
    _C8_FEW_SHOT_APPEND,
    _V3_SCHEMA_EXTENSION,
    _SEXUAL_LABELING_RULES,
    _V3_FEW_SHOTS,
])

USER_PROMPT_TEMPLATE = _USER_SNIPPETS_FIRST + """

Classify sexual_explicitness and sexual_function before the label (v3 JSON fields).
Keep the label fluent and natural — analytic function belongs in JSON, not stiff label wording.
"""

ROMANCE_AWARE_SYSTEM_PROMPT = SYSTEM_PROMPT
ROMANCE_AWARE_USER_PROMPT = USER_PROMPT_TEMPLATE
