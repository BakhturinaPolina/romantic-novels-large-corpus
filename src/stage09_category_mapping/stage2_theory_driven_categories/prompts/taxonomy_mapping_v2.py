"""Stage09 taxonomy mapping prompts v2 — XML-structured, few-shot, expanded schema."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.stage09_category_mapping.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    MECHANIC_TAG_ENUM,
    taxonomy_block_for_prompt,
)

_BOUNDARY_RULES = """
SEXUALITY BOUNDARIES
- 2.1: desire, anticipation, arousal, longing, sexual tension without clear physical act.
- 2.2: kissing, hugging, stroking, cuddling, non-explicit affection.
- 2.3: explicit sexual acts, penetration, genital terms, orgasm, undressing in explicitly sexual context.
- 2.4: post-sex, aftercare, reflection after intimacy, emotional processing after sex.
- 2.5: condom/lube preparation, sexual boundary talk, sex-without-commitment negotiation.
- Forceful sex without refusal/fear/pressure/blackmail/captivity → 2.3 + mechanic tag forceful_intensity or ambiguous_consent_watchlist, NOT 7.2 automatically.
- Unwanted touch, coercion, nonconsent → 7.4.

WORK / STATUS BOUNDARIES
- 6.1: elite hero work, wealth, business authority, CEO/tycoon/security power, male-coded professional dominance.
- 6.2: heroine's or any character's job, career, competence, professional identity.
- 6.3: workplace interaction between protagonists.
- 6.4: money, debt, housing, economic security, contracts, pay, property.
- 6.5: law, police, medicine, education, custody, court, formal institutions.
- 6.6: fashion, jewelry, glamour consumption. 6.7: aristocracy, period status.

CONFLICT / RISK BOUNDARIES
- 7.1: non-romantic interpersonal conflict without violence or external danger.
- 7.2: direct threats, physical violence, coercion, captivity, stalking, blackmail, non-consensual pressure.
- 7.3: accidents, illness crises, war, supernatural danger, external enemies, rescue danger, environmental risk.
- Protective rather than harmful → relationship or work/status as main + mechanic tag protective_care or external_threat.

RELATIONSHIP vs INNER LIFE vs SOCIAL WORLD
- 4.x: main couple bond trajectory (meeting, bonding, secrets, conflict, reconciliation, commitment, HEA).
- 3.x: internal affective/cognitive state when relationship action is not the main focus.
- 5.1: pregnancy, children, parents, siblings, kinship, paternity, family secrets.
- Do not map every emotional scene to 3.x; reconciliation/confession → 4.x main, 3.x secondary.

DOMINANT SEMANTIC CENTER (not setting alone)
- Pregnancy/baby future → 5.1 or 4.5 (commitment), not 8.1 domestic alone.
- Bedroom explicit sex → 2.x, not 8.1.
- Security/protection logistics → 6.5 or 6.1 + protective_care, not 7.3 unless danger is central.
- Phone/message carrying secrets → 4.3 main, 8.3 secondary.

SUBGENRE & DISCOURSE
- 10.x main only when genre furniture dominates (werewolf identity → 10.1; investigation → 10.3).
- Discourse (explanation, reassurance, apology patterns) → 9.x; use_in_macro_axes=false, use_in_theory_watchlist=true.
- narrative_style primary → 9.1–9.4.

NOISE
- is_noise=true only for boilerplate, author notes, web fragments, character-name clusters with no coherent scene, incoherent topics.
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
{"topic_id":31,"content_type":"subgenre_marker","main_category_id":"10.1","secondary_category_id":null,"other_plausible_ids":["3.3"],"mechanic_tags":["paranormal_instinct"],"is_noise":false,"use_in_macro_axes":true,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.86,"evidence_quality":"high","uncertainty_reason":null,"rationale":"Paranormal shifter identity dominates; useful as subgenre control even if small."}

EXAMPLE 5 — Topic 5 (Discourse: Explaining Unlikely Behavior)
Input: content_type discourse; keywords explanation, unlikely, behavior; narrative_style.
Output:
{"topic_id":5,"content_type":"discourse","main_category_id":"9.1","secondary_category_id":null,"other_plausible_ids":["4.3"],"mechanic_tags":[],"is_noise":false,"use_in_macro_axes":false,"use_in_theory_watchlist":true,"noise_reason":null,"confidence":0.8,"evidence_quality":"medium","uncertainty_reason":null,"rationale":"Abstract explanation/justification speech pattern; meaningful for qualitative analysis but weak macro axis."}
""".strip()


def build_system_prompt(taxonomy_path: Optional[str | Path] = None) -> str:
    path = str(taxonomy_path or DEFAULT_TAXONOMY_PATH)
    taxonomy_text = taxonomy_block_for_prompt(path)
    mechanic_list = ", ".join(MECHANIC_TAG_ENUM)

    return f"""
<task>
Map one BERTopic topic from a romance-fiction corpus to a fixed analytic taxonomy.
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
3. Decide use_in_macro_axes (coherent + stable enough for quantitative aggregation).
4. Decide use_in_theory_watchlist (meaningful for interpretation even if discourse-like or small).
5. Choose main_category_id from the fixed taxonomy (dominant semantic center, not setting alone).
6. Choose secondary_category_id only if a second category is genuinely important.
7. Add romance mechanic_tags if applicable; report confidence (0–1), evidence_quality, uncertainty_reason.
</decision_steps>

<category_principles>
A taxonomy category describes the topic's dominant observable evidence.
A mechanic tag describes what that evidence does in romance structure.
Choose main by semantic center; use secondary for non-dominant functions.
Do not use 8.x just because a scene happens in a room. Do not use 3.x for every emotional beat.
</category_principles>

<mechanic_tags>
Optional overlay tags (max 5): {mechanic_list}
Apply when romance mechanics are clear: protective_care, possessive_control, economic_power, pregnancy_future, forceful_intensity, etc.
</mechanic_tags>

<quality_flags>
is_noise: true only for boilerplate, paratext, web fragments, character-name clusters without coherent scene, incoherent topics.
use_in_macro_axes: true only if coherent and stable enough for book-level quantitative aggregation.
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
Return only JSON matching the enforced schema: topic_id, content_type, main_category_id, secondary_category_id, other_plausible_ids, mechanic_tags, is_noise, use_in_macro_axes, use_in_theory_watchlist, noise_reason, confidence (0–1), evidence_quality (high|medium|low), uncertainty_reason, rationale (max 600 chars).
No markdown or text outside JSON.
</output_schema>
""".strip()


TAXONOMY_ZEROSHOT_USER_PROMPT_V2 = """
### TOPIC DATA

REPRESENTATIVE SNIPPETS (read first — primary evidence; keywords are secondary when they conflict):

{snippets}

topic_id: {topic_id}

TOPIC KEYWORDS:

{keywords}

PREVIOUS LLM LABEL:

{label}

PREVIOUS SCENE SUMMARY:

{scene_summary}

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
