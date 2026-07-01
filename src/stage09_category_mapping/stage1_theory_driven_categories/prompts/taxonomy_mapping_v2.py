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

_BOUNDARY_RULES = """
PRIMARY vs SECONDARY (v2.2)
- Primary labels (1–7.x): what the topic is thematically doing — attraction, sex, bonding, conflict, family, work, danger, care.
- Secondary/context (8.x, 9.x, 10.x): where, when, objects, discourse style, or subgenre machinery — use as main ONLY when that context truly dominates.
- When a restaurant outing is mainly couple bonding → 4.2 main, 8.2 secondary (not 8.2 main).

SEXUALITY BOUNDARIES
- 2.1: desire, anticipation, arousal, longing, sexual tension without clear physical act.
- 2.2: kissing, hugging, stroking, cuddling, non-explicit affection.
- 2.3: explicit sexual acts, penetration, genital terms, orgasm, undressing in explicitly sexual context.
- 2.4: post-sex, aftercare, reflection after intimacy, emotional processing after sex.
- 2.5: condom/lube preparation, sexual boundary talk, sex-without-commitment negotiation.
- Forceful consensual sex without coercion evidence → 2.3 + forceful_intensity tag, NOT 7.4.
- Unwanted touch, coercion, unclear consent → 7.4 (overrides 2.1/2.3).

WORK / STATUS BOUNDARIES
- 6.1: elite roles, authority, high-power work (CEO, surgeon, royalty as power).
- 6.2: any character's job, career, professional identity.
- 6.3: main couple interacting through shared workplace.
- 6.4: economic precarity, debt, housing insecurity — NOT status/luxury (6.6/6.7).
- 6.5: courts, hospitals, schools, formal institutions and procedures.
- 6.6: material glamour and luxury consumption. 6.7: aristocracy and period status.

CONFLICT / RISK BOUNDARIES
- 4.7: jealousy/possessive main-couple conflict — distinct from 7.4 coercion watchlist.
- 7.1: non-romantic interpersonal conflict without violence.
- 7.2: violence, threats, non-sexual coercion.
- 7.3: accidents, illness crises, external danger, disasters.
- 7.4: unwanted/coercive sexual contact — watchlist; manual review recommended.

RELATIONSHIP vs INNER LIFE vs SOCIAL WORLD
- 4.x: main couple bond trajectory (setup, bonding, secrets, conflict, reconciliation, care, jealousy).
- 3.x: internal affect when no clearer scene function dominates.
- 5.1: family, kinship, pregnancy, parenthood.

DOMINANT SEMANTIC CENTER (not setting alone)
- Pregnancy/baby future → 5.1 or 4.5, not 8.1 alone.
- Bedroom explicit sex → 2.x main, 8.1 secondary at most.
- Phone/message secrets → 4.3 main, 8.3 secondary.

SUBGENRE, DISCOURSE & MACRO AXES
- 8.x / 9.x / 10.x as main → use_in_macro_axes=false (context tags for watchlist/analysis).
- 10.x main only when genre furniture dominates AND no stronger primary theme applies.
- 9.x discourse → use_in_macro_axes=false, use_in_theory_watchlist=true.

NOISE
- is_noise=true only for boilerplate, paratext, encoding garbage, character-name clusters without coherent scene.
""".strip()

_FEW_SHOT_EXAMPLES = """
EXAMPLE 1 — Topic 50 (Pregnancy Worries and Baby Talk)
Input: keywords pregnant, worries, conversations; label "Pregnancy Worries and Baby Talk"; scene about baby/family future.
Output:
{"topic_id":50,"content_type":"scene","main_category_id":"5.1","secondary_category_id":"4.5","other_plausible_ids":["3.2"],"mechanic_tags":["pregnancy_future"],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.88,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Pregnancy and baby talk center family/kinship and future commitment, not domestic routine alone."}

EXAMPLE 2 — Topic 118 (Forceful Bedroom Encounter)
Input: explicit sexual_content; forceful intercourse on mattress; register explicit.
Output:
{"topic_id":118,"content_type":"scene","main_category_id":"2.3","secondary_category_id":"8.1","other_plausible_ids":[],"mechanic_tags":["forceful_intensity"],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.9,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Explicit forceful sexual act is central; bedroom is secondary setting. Not coercion without consent evidence."}

EXAMPLE 3 — Topic 9 (Negotiating Terms and Deals)
Input: keywords terms, partners, percent, scenario; business deal negotiation.
Output:
{"topic_id":9,"content_type":"scene","main_category_id":"6.4","secondary_category_id":"6.1","other_plausible_ids":["4.3"],"mechanic_tags":["economic_power","professional_hierarchy"],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.82,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Money, contracts, and deal terms dominate; elite business power may be secondary."}

EXAMPLE 4 — Topic 31 (Werewolf Identity and Instincts)
Input: content_type subgenre_marker; growl, instincts, paranormal; werewolf identity.
Output:
{"topic_id":31,"content_type":"subgenre_marker","main_category_id":"10.1","secondary_category_id":null,"other_plausible_ids":["3.3"],"mechanic_tags":["paranormal_instinct"],"is_noise":false,"use_in_macro_axes":false,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.86,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Paranormal shifter identity as subgenre context flag; excluded from macro axes per v2.2 policy."}

EXAMPLE 5 — Topic 5 (Discourse: Explaining Unlikely Behavior)
Input: content_type discourse; keywords explanation, unlikely, behavior; narrative_style.
Output:
{"topic_id":5,"content_type":"discourse","main_category_id":"9.1","secondary_category_id":null,"other_plausible_ids":["4.3"],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":false,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.8,"evidence_quality":"medium","uncertainty_reason":null,"rationale":"Abstract explanation/justification speech pattern; meaningful for qualitative analysis but weak macro axis."}

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
Map one BERTopic topic from a romance-fiction corpus to a fixed analytic taxonomy (v2.2).
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
use_in_macro_axes: true only for primary thematic labels (not 8.x/9.x/10.x as main) that are coherent and stable for aggregation.
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
