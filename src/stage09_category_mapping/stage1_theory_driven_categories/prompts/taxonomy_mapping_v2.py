"""Stage09 taxonomy mapping prompts v2 — XML-structured, few-shot, expanded schema."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    MECHANIC_TAG_ENUM,
    load_taxonomy_config,
    taxonomy_block_for_prompt,
)

_RWA_PURPOSE = """
ROMANCE GENRE PURPOSE (Stage09)
Stage09 is not to classify every topic into a romance-relevant axis. Many coherent topics are context-only.
Use macro-axis categories only when snippets show direct evidence for project hypotheses: love/commitment/tenderness,
HEA/repair, sexual explicitness, protection/care, possessiveness/control, conflict/darkness, luxury/status as romantic
appeal, or narrative repair. Object, setting, transit, speech style, facial gesture, subgenre furniture, or ordinary
business logistics → context category + use_in_macro_axes=false.
""".strip()

_BOUNDARY_RULES = """
AXIS vs CONTEXT (v2.4)
- axis_bearing_ids: narrow set for Stage10 hypotheses (2.x, 3.1/3.2, 4.2–4.7, 5.3a, 6.1a/6.4/6.6/6.7, 7.x, 8.3a).
- Context-only labels (1.x, 5.1/5.2, 6.1b/6.2/6.3/6.5, 7.1, 8.x except 8.3a, 9.x, 10.x, uncertain_interpretable): mappable but use_in_macro_axes=false.
- 3.3 ambivalence is exploratory-only (H5/H6) — use_in_macro_axes=false even when main.
- Stage08 axis_hint and sexual_function are WEAK hints only. Do NOT promote wink/gesture to 2.2 without kiss/hug/embrace evidence.
- Never assign macro-axis category only because axis_hint says everyday_intimacy_emotional_safety or no_hypothesis_signal.

HYPOTHESIS-RELEVANCE GATE (apply before choosing main)
1. Is this narrative story content, discourse mechanics, subgenre furniture, paratext, or noise?
2. Does visible evidence support a project hypothesis?
   H1: love/tenderness/care vs explicit sex | H2: HEA/commitment/wedding/recognition
   H3: luxury/status paired with love | H4: protective care vs possessiveness
   H5: darkness/conflict/threat vs tenderness | H6: conflict/miscommunication vs repair
3. If no hypothesis-relevant evidence, assign context-only category and use_in_macro_axes=false.
   Prefer uncertain_interpretable over forcing 4.2 when bonding function is not visible.

NEGATIVE EXAMPLES — DO NOT COUNT AS EVERYDAY INTIMACY
- Taxi, car, doorway, arrival, stairs, hotel transit → 8.5 or 8.2 context; macro false unless snippets show care/courtship.
- Coffee mug, cup, kitchen object → 8.3b or 8.1 context only unless meaningful gift/care act.
- Smile, wink, eyes opening, gaze without desire → 1.7 context only — NOT 2.2 unless kiss/hug/embrace in snippets.
- Love confession / admitting love after denial → 4.5 main — NOT 2.2 (verbal commitment is not physical affection).
- Shared chuckles/laughter without courtship function → 9.3 or 1.7 context only.
- Generic "I'll call / I'll come back" → 9.2 or 8.3b unless it repairs, commits, reassures, or threatens the relationship.
- Paranormal creature vocabulary alone → 10.1 context; map to 2.x/4.x/7.x only when desire, care, conflict, or danger is visible.

POSITIVE AXIS EXAMPLES
- "Soft Kiss Turning Urgent" → 2.2 main, 2.1 secondary if tender kisses but escalation keywords.
- "Hot Breath Against Her Neck" → 2.1 main. Do NOT route to 1.6/1.7 because hair, neck, breath, forehead, or gaze appears.
- "Reluctant Agreement to Marry" → 4.5 main.
- "Vowing to Keep Her Safe" → 4.6 main.
- "Crawling Onto The King-Sized Bed" → 7.4 only if refusal, fear, restraint, or unclear consent; else 2.1/2.3 + forceful_intensity if consensual.

PRIMARY vs SECONDARY
- Primary axis labels: what the topic is thematically doing — attraction, sex, bonding, conflict, danger, care.
- Secondary/context: where, when, objects, discourse style, subgenre — use as main ONLY when that context truly dominates.
- When couple bonding dominates a restaurant outing → 4.2 main, 8.2 secondary (not 8.2 or 4.2 from object/setting alone).

SEXUALITY BOUNDARIES
- 2.1: desire, anticipation, arousal, longing, sexual tension without clear physical act.
- 2.2: kissing, hugging, stroking, cuddling, non-explicit affection.
- 2.3: explicit sexual acts. 2.4: post-sex aftercare. 2.5: condom/lube/boundary negotiation.
- Forceful consensual sex → 2.3 + forceful_intensity, NOT 7.4.
- Unwanted touch, coercion, unclear consent → 7.4 (overrides 2.1/2.3).

WORK / STATUS BOUNDARIES
- 6.4: economic precarity ONLY with rent, debt, can't afford, dependence — NOT generic deal/contract/payment.
- 6.1a: billionaire/CEO/aristocratic authority tied to romantic hero appeal or status display — axis-bearing for H3.
- 6.1b: generic business deal/contract/payment/percent — context-only, use_in_macro_axes=false.
- Generic business negotiation → 6.1b, 8.3b, or uncertain_interpretable — NOT 6.4 or 6.1a.
- 8.3a: rings, wedding bands, love letters, meaningful gifts (HEA low-weight).
- 8.3b: phones, cars, coffee mugs, ordinary props.

SOCIAL / HEA
- 5.3a: weddings, proposals, formal couple recognition (HEA axis).
- 5.3b: parties, gossip, community judgment (context only).
- 3.1: resolution/relief/payoff only — NOT generic amusement or laughter (use 9.3/1.7).

SUBGENRE, DISCOURSE & MACRO AXES
- Context mains (8.x, 9.x, 10.x, 1.x, uncertain_interpretable) → use_in_macro_axes=false.
- 9.x discourse → use_in_theory_watchlist=true.

NOISE
- is_noise=true only for boilerplate, paratext, encoding garbage, character-name clusters without coherent scene.
""".strip()

_FEW_SHOT_EXAMPLES = """
EXAMPLE 1 — Topic 50 (Pregnancy Worries and Baby Talk)
Input: keywords pregnant, worries, conversations; label "Pregnancy Worries and Baby Talk"; scene about baby/family future.
Output:
{"topic_id":50,"content_type":"scene","main_category_id":"5.1","secondary_category_id":"4.5","other_plausible_ids":["3.2"],"mechanic_tags":["pregnancy_future"],"is_noise":false,"use_in_macro_axes":false,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.88,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Pregnancy and baby talk center family/kinship context; future commitment is secondary. 5.1 is context-only per v2.3."}

EXAMPLE 2 — Topic 118 (Forceful Bedroom Encounter)
Input: explicit sexual_content; forceful intercourse on mattress; register explicit; consent consensual_implied.
Output:
{"topic_id":118,"content_type":"scene","main_category_id":"2.3","secondary_category_id":"8.1","other_plausible_ids":[],"mechanic_tags":["forceful_intensity"],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.9,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Explicit forceful sexual act is central; bedroom is secondary setting. Not coercion without consent evidence."}

EXAMPLE 3 — Topic 9 (Generic Business Deal Negotiation)
Input: keywords terms, partners, percent, deal, contract; business negotiation without precarity vocabulary.
Output:
{"topic_id":9,"content_type":"scene","main_category_id":"6.1b","secondary_category_id":"8.3b","other_plausible_ids":["uncertain_interpretable"],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":false,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.78,"evidence_quality":"medium","uncertainty_reason":null,"rationale":"Generic deal/contract/payment terms — business logistics (6.1b), not elite romantic status (6.1a) or precarity (6.4)."}

EXAMPLE 3b — Topic 88 (Rent Due and Can't Afford It)
Input: snippets about rent, debt, eviction fear, can't afford groceries.
Output:
{"topic_id":88,"content_type":"scene","main_category_id":"6.4","secondary_category_id":null,"other_plausible_ids":["3.2"],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.85,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Rent, debt, and can't-afford vocabulary dominate — true economic precarity, not generic business deal."}

EXAMPLE 4 — Topic 0 (Hesitant Arrival at Entrance)
Input: snippets taxi, ride home, driving through; keywords doorway, hesitation.
Output:
{"topic_id":0,"content_type":"scene","main_category_id":"8.5","secondary_category_id":null,"other_plausible_ids":["8.2"],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":false,"use_in_theory_watchlist":false,"noise_reason":null,"confidence":0.72,"evidence_quality":"medium","uncertainty_reason":null,"rationale":"Transit/threshold vocabulary dominates; no courtship or care function visible."}

EXAMPLE 5 — Topic 2 (Hot Breath Against Her Neck)
Input: sexual_function sexual_tension; snippets charged proximity, hot breath on neck, fingers at throat.
Output:
{"topic_id":2,"content_type":"scene","main_category_id":"2.1","secondary_category_id":"1.1","other_plausible_ids":[],"mechanic_tags":["forceful_intensity"],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.88,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Charged erotic proximity and sexual tension dominate; hair/neck/forehead vocabulary does not make this appearance (1.6)."}

EXAMPLE 7 — Topic 7 (Playful Wink Across The Room)
Input: snippets show single wink gesture; sexual_function nonsexual_affection; no kiss/hug/embrace.
Output:
{"topic_id":7,"content_type":"scene","main_category_id":"1.7","secondary_category_id":null,"other_plausible_ids":[],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":false,"use_in_theory_watchlist":false,"noise_reason":null,"confidence":0.82,"evidence_quality":"medium","uncertainty_reason":null,"rationale":"Wink is nonverbal facial cue (1.7). sexual_function alone does not make this 2.2 without physical affection in snippets."}

EXAMPLE 8 — Topic 23 (Admitting Love After Denial)
Input: snippets 'loved you the whole damn time'; love confession resolving prior denial.
Output:
{"topic_id":23,"content_type":"scene","main_category_id":"4.5","secondary_category_id":"3.3","other_plausible_ids":["4.4"],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.88,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Verbal love confession after denial is relationship turning point (4.5), not physical affection (2.2)."}

EXAMPLE 6 — Topic 72 (Restaurant Date and Conversation)
Input: dinner date at restaurant, couple talking, shared meal, deepening connection.
Output:
{"topic_id":72,"content_type":"scene","main_category_id":"4.2","secondary_category_id":"8.2","other_plausible_ids":["2.1"],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.87,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Relational courtship and bonding dominate; restaurant is secondary setting context."}
""".strip()


def _priority_rules_block(taxonomy_path: str) -> str:
    cfg = load_taxonomy_config(taxonomy_path)
    rules = cfg.get("priority_rules", {})
    ordered = rules.get("ordered_priority", [])
    desc = str(rules.get("description", "")).strip().replace("\n", " ")
    lines = [desc] if desc else []
    lines.append("Priority order (higher wins when multiple labels fit):")
    for item in ordered:
        lines.append(f"  - {item}")
    notes = cfg.get("labeling_notes", {})
    primary_note = str(notes.get("primary_vs_secondary", "")).strip().replace("\n", " ")
    if primary_note:
        lines.append(f"Primary vs secondary: {primary_note}")
    return "\n".join(lines)


def build_system_prompt(taxonomy_path: Optional[str | Path] = None) -> str:
    path = str(taxonomy_path or DEFAULT_TAXONOMY_PATH)
    taxonomy_text = taxonomy_block_for_prompt(path)
    mechanic_list = ", ".join(MECHANIC_TAG_ENUM)
    priority_text = _priority_rules_block(path)

    return f"""
<task>
Map one BERTopic topic from a romance-fiction corpus to a fixed analytic taxonomy (v2.4).
</task>

<role>
You are RomanceTaxonomyMapper, an expert in mapping BERTopic-style topic clusters from contemporary romance, erotic romance, paranormal romance, romantic suspense, and related popular-romance subgenres to a fixed analytic taxonomy.

The corpus spans contemporary, paranormal, historical, YA, and mystery — not billionaire-only fiction.
</role>

<evidence_priority>
1. Representative snippets, if present, are strongest evidence.
2. The previous label and scene summary (may be wrong — verify against snippets).
3. Keywords are useful lexical anchors but may be generic.
4. Previous categories and Stage07 exclusion/noise flags are quality hints, not final truth.
</evidence_priority>

<decision_steps>
1. Decide whether the topic is coherent.
2. Decide content_type: scene | discourse | subgenre_marker | paratext_or_boilerplate | character_name_cluster | noise.
3. Decide use_in_macro_axes (primary thematic label, coherent, stable for book-level aggregation).
4. Decide use_in_theory_watchlist (meaningful for interpretation even if discourse-like or small).
5. Choose main_category_id from the fixed taxonomy (dominant semantic center, not setting alone).
6. Choose secondary_category_id only if a second category is genuinely important.
7. Add romance mechanic_tags if applicable; report confidence (0–1), evidence_quality, uncertainty_reason.
8. Write mapping_reasoning: structured debug text citing snippet evidence, rejected alternatives, and macro_axes rationale.
</decision_steps>

<priority_rules>
{priority_text}
</priority_rules>

<category_principles>
{_RWA_PURPOSE}

A taxonomy category describes the topic's dominant observable evidence.
A mechanic tag describes what that evidence does in romance structure.
Choose main by semantic center; use secondary for non-dominant functions.
Do not use 8.x just because a scene happens in a room. Do not use 3.x for every emotional beat.
Secondary/context labels (8.x, 9.x, 10.x) should not override stronger primary themes.
</category_principles>

<mechanic_tags>
Optional overlay tags (max 5): {mechanic_list}
Apply when romance mechanics are clear: protective_care, possessive_control, economic_power, pregnancy_future, forceful_intensity, etc.
</mechanic_tags>

<quality_flags>
is_noise: true only for boilerplate, paratext, web fragments, character-name clusters without coherent scene, incoherent topics.
use_in_macro_axes: true only when main_category_id is axis-bearing (see boundary_rules) AND hypothesis-relevant evidence is visible in snippets.
use_in_theory_watchlist: true if meaningful for interpretation (discourse, subgenre markers, small but theory-relevant topics).
noise_reason: short string when is_noise=true, else null.
</quality_flags>

<boundary_rules>
{_BOUNDARY_RULES}
</boundary_rules>

<taxonomy>
{taxonomy_text}
</taxonomy>

<few_shot_examples>
{_FEW_SHOT_EXAMPLES}
</few_shot_examples>

<output_schema>
Return only JSON matching the enforced schema: topic_id, content_type, main_category_id, secondary_category_id, other_plausible_ids, mechanic_tags, is_noise, use_in_macro_axes, use_in_theory_watchlist, noise_reason, confidence (0–1), evidence_quality (high|medium|low), uncertainty_reason, rationale (max 600 chars), mapping_reasoning (max 1200 chars — structured debug: evidence used, why main over alternatives, secondary/macro_axes decision).
No markdown or text outside JSON.
</output_schema>
""".strip()


TAXONOMY_ZEROSHOT_USER_PROMPT_V2 = """
### TOPIC DATA

REPRESENTATIVE SNIPPETS (read first — primary evidence; keywords are secondary when they conflict):

{snippets}

topic_id: {topic_id}

TOPIC LABEL (Stage 08):

{label}

SCENE SUMMARY (Stage 08):

{scene_summary}

STAGE 08 LABELING RATIONALE:

{label_rationale}

TOPIC KEYWORDS (c-TF-IDF / merged):

{keywords}

ALL KEYWORDS (union across representations):

{all_keywords}

REPRESENTATION KEYWORDS (KeyBERT / MMR / POS / Main):

{representations}

PREVIOUS PRIMARY CATEGORIES:

{primary_categories}

PREVIOUS SECONDARY CATEGORIES:

{secondary_categories}

STAGE 08 CONTENT TYPE: {content_type}
STAGE 08 EXCLUDE FROM AXES: {exclude_from_axes}
STAGE 08 SUBGENRE HINTS: {subgenre_hints}
STAGE 08 REGISTER: {register}
STAGE 08 SEXUAL EXPLICITNESS: {sexual_explicitness}
STAGE 08 SEXUAL FUNCTION: {sexual_function}
STAGE 08 CONSENT STATUS: {consent_status}
STAGE 08 AXIS HINT: {axis_hint}

STAGE 07 HINTS (weak — do not override snippets):
exclude_from_axes: {stage07_exclude_from_axes}
posthoc_reason: {stage07_posthoc_reason}
content_type: {stage07_content_type}

### TASK

Follow the decision_steps in the system message. Return a SINGLE JSON object only.
""".strip()
