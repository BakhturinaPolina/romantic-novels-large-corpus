"""Stage 09: Zero-shot taxonomy mapping of BERTopic topics using OpenRouter (Mistral-Nemo).

This module assumes you already ran Stage 08 LLM labeling and have a JSON file
with enriched topic metadata of the form:

{
  "33": {
    "label": "Business Discussion",
    "keywords": ["business", "company", "dollars", ...],
    "primary_categories": ["domestic_life", "work_or_school"],
    "secondary_categories": ["setting:dinner_table", "activity:discussion"],
    "scene_summary": "The couple discusses business matters at the dinner table.",
    "is_noise": false,
    "rationale": "...",
    ...
  },
  ...
}

We now map each topic to a fixed Romance Corpus Topic Taxonomy using zero-shot
classification with mistralai/Mistral-Nemo-Instruct-2407 via OpenRouter.

The output is a JSON mapping:

{
  "33": {
    "topic_id": 33,
    "main_category_id": "6.1",
    "secondary_category_id": "5.1",
    "other_plausible_ids": ["4.2"],
    "is_noise": false,
    "rationale": "..."
  },
  ...
}
"""

from __future__ import annotations

import json
import logging
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from openai import OpenAI
from bertopic import BERTopic

# Reuse existing OpenRouter client + helpers from Stage 08
from src.stage08_llm_labeling.openrouter_experiments.core.generate_labels_openrouter import (
    DEFAULT_OPENROUTER_API_KEY,
    DEFAULT_OPENROUTER_BASE_URL,
    DEFAULT_OPENROUTER_MODEL,
    load_openrouter_client,
    rerank_snippets_centrality,
    format_snippets,
    extract_representative_docs_per_topic,
)

# Reuse model loading helpers from Stage 1
from src.stage06_topic_exploration.explore_retrained_model import (
    DEFAULT_BASE_DIR,
    DEFAULT_EMBEDDING_MODEL,
    load_native_bertopic_model,
)
from src.stage09_category_mapping.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    apply_domain_heuristics,
    enrich_with_category_names,
    fallback_main_category,
    load_taxonomy_nodes,
    taxonomy_block_for_prompt,
    taxonomy_by_id,
    try_pre_route_taxonomy,
    valid_taxonomy_ids,
)

LOGGER = logging.getLogger("stage09_zeroshot_taxonomy")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)


# ---------------------------------------------------------------------------
# 1. Romance Corpus Topic Taxonomy v2 (configs/romance_corpus_taxonomy_v2.yaml)
# ---------------------------------------------------------------------------

TAXONOMY_CONFIG_PATH = DEFAULT_TAXONOMY_PATH
TAXONOMY_NODES: List[Dict[str, str]] = load_taxonomy_nodes(str(TAXONOMY_CONFIG_PATH))
TAXONOMY_BY_ID: Dict[str, Dict[str, str]] = taxonomy_by_id(str(TAXONOMY_CONFIG_PATH))
VALID_TAXONOMY_IDS = valid_taxonomy_ids(str(TAXONOMY_CONFIG_PATH))
TAXONOMY_TEXT_BLOCK = taxonomy_block_for_prompt(str(TAXONOMY_CONFIG_PATH))


def reload_taxonomy(config_path: Optional[Path] = None) -> None:
    """Reload taxonomy globals from YAML (for CLI --taxonomy-config)."""
    global TAXONOMY_CONFIG_PATH, TAXONOMY_NODES, TAXONOMY_BY_ID, VALID_TAXONOMY_IDS, TAXONOMY_TEXT_BLOCK
    path = config_path or DEFAULT_TAXONOMY_PATH
    TAXONOMY_CONFIG_PATH = path
    TAXONOMY_NODES = load_taxonomy_nodes(str(path))
    TAXONOMY_BY_ID = taxonomy_by_id(str(path))
    VALID_TAXONOMY_IDS = valid_taxonomy_ids(str(path))
    TAXONOMY_TEXT_BLOCK = taxonomy_block_for_prompt(str(path))


# ---------------------------------------------------------------------------
# 3. System + user prompts for zero-shot taxonomy mapping
#    Optimized for Mistral-Nemo, JSON-only output, similar style to Stage 08.
# ---------------------------------------------------------------------------

TAXONOMY_ZEROSHOT_SYSTEM_PROMPT = f"""
You are RomanceTaxonomyMapper, an expert assistant for assigning topics from modern English romance fiction (2000–2017) to a fixed analytic taxonomy.

CORPUS CONTEXT (IMPORTANT)

The corpus is multi-genre: contemporary, paranormal, historical, young-adult, and mystery.
It is NOT a billionaire-only or CEO-romance subset. Do NOT default to 6.1 for generic negotiation,
social scenes, or fashion unless elite professional work is clearly central.

You will receive, for each topic:

- A topic_id

- TOPIC KEYWORDS from BERTopic

- An LLM-generated label and scene_summary from a previous stage

- Primary and secondary categories from the earlier labeler (e.g., "romance_core", "narrative_style", "appearance_presentation", "activity:dressing")

- Optional Stage 08 fields: content_type, exclude_from_axes, subgenre_hints, register,
  sexual_explicitness, sexual_function, consent_status, axis_hint (v3 sexual-precision labels)

- Optional representative snippets from the corpus

Your task is to map this topic to one or two nodes in a fixed Romance Corpus Topic Taxonomy.

IMPORTANT: This is ZERO-SHOT classification.

- The taxonomy is fixed and must NOT be modified.

- You must select IDs only from the taxonomy list shown below.

AVAILABLE TAXONOMY NODES

(Use these IDs exactly; do NOT invent new ones):

{TAXONOMY_TEXT_BLOCK}

OUTPUT CONSTRAINTS

- Think through the mapping internally.

- In your final answer, output only a valid JSON object.

- Do NOT include markdown, backticks, or any explanation outside the JSON.

- Never wrap JSON in ```json or any other formatting.

- Use only taxonomy IDs listed above, or "noise" for junk topics.

JSON SCHEMA (MANDATORY)

Return exactly these keys and types:

{{
  "topic_id": 0,
  "main_category_id": "4.2",
  "secondary_category_id": "5.1",
  "other_plausible_ids": ["3.2", "6.4"],
  "is_noise": false,
  "confidence": "medium",
  "rationale": "1–3 short sentences explaining why these IDs fit this topic."
}}

FIELD RULES

1) "topic_id"

- Echo the integer topic id from the input.

2) "main_category_id"

- REQUIRED.

- One taxonomy ID that best captures the central function of the topic.

- Use:

  - 4.x for dynamics BETWEEN the main romantic couple (interactions, dialogue,
    arguments, dates, bonding, conflicts, reconciliations). NOT for family
    members or friends - those go to 5.x.

  - 5.x for social world outside the main couple (family, friends, community).
    Use 5.1 for family/kinship scenes even if they affect the couple indirectly.

  - 6.x for work, money, institutional scenes, material glamour (6.6), aristocracy (6.7).
    Use 6.1 ONLY for elite professional/business power — NOT generic social bargaining.
    Use 6.2 for a character's job or professional identity (any lead or supporting character).
    Use 6.6 for fashion, jewelry, modeling, upscale consumption.
    Use 6.7 for titled nobility, court formality, period status markers.
    Use 6.4 for economic precarity (rent, debt) — NOT luxury glamour.

  - 1.6 for hair, grooming, clothes, mirror checks, body cataloguing, beauty evaluation
    (neutral register, not explicit sex).

  - 1.7 for gaze, eye color, smirk/wink, facial expression, self-conscious awareness.

  - 9.x for dialogue delivery and discourse patterns (included in Stage09 analysis).

  - 10.x for subgenre plot furniture ONLY when genre markers dominate the topic
    (see rule 8 below). Scene beats (kiss, argument, dinner, phone) → 2.x–8.x first.

  - 2.x for sexual attraction/acts/intimacy.

  - 1.5 for any non-violent sport or physical training, workouts, exercise.

  - 7.x for risk, harm, violence, coercion, and antagonistic non-couple conflict (7.1).
    Use 7.1 for bosses, rivals, antagonists outside the main couple (see rule 2b).
    Use 7.2 ONLY for actual violence/threats, NOT for verbal arguments or
    emotional conflict between the main couple (those belong in 4.4).

  - 8.x when the topic is primarily about spaces, time, or objects.

  - 3.x when the topic is mostly ONE character's inner feelings, beliefs,
    cognitive states, or internal monologue WITHOUT much interaction.
    Use 3.1 for standalone happiness/gratitude/relief (any character).
    Use 4.5 when commitment/HEA is central; 4.6 when reassurance/protection
    is central; 2.2 when affection is physical, not purely internal.
    Use 4.1 for early romantic approach (first dates, flirtation, invitations);
    4.2 for ongoing bonding and everyday intimacy; 4.6 for emotional safety
    and repair. Do NOT map courtship/affection/reassurance to 8.1 alone.

  - "noise" only if the topic is mostly boilerplate or paratext.

3) "secondary_category_id"

- OPTIONAL but recommended.

- A second taxonomy ID when the topic clearly blends two dimensions
  (e.g., argument in kitchen → 4.4 + 8.1; pregnancy conflict → 5.1 + 3.2).

- Use null if there is no meaningful second dimension.

4) "other_plausible_ids"

- OPTIONAL list (0–3 items) of other taxonomy IDs that are plausible,
  but clearly less central than main_category_id and secondary_category_id.

5) "is_noise"

- true only if the topic is mostly boilerplate, technical artefacts, or paratext.

- If true, main_category_id MUST be "noise" and secondary_category_id MUST be null.

- If false, main_category_id MUST NOT be "noise".

6) "confidence"

- REQUIRED.

- One of: "low", "medium", "high".

- "high" = strong, unambiguous match to one taxonomy node.

- "medium" = reasonably clear, a couple of plausible alternatives.

- "low" = noisy or ambiguous topic, mapping is uncertain.

7) "rationale"

- 1–3 short sentences.

- Refer to:

  - specific high-weight keywords,

  - the label and scene_summary,

  - and any primary/secondary categories in the input.

- Explain why these support the chosen taxonomy IDs.

- Do NOT quote long snippets verbatim; summarize them instead.

CRITICAL BOUNDARY RULES

1) 4.x (Relationship Trajectory) vs. 3.x (Inner Life) vs. 5.x (Social World)

- Use 4.x ONLY when the interaction is BETWEEN the main romantic couple
  (dialogue, arguments, dates, separations, reconciliations, bonding moments).

- Use 3.x when the focus is on ONE character's internal feelings, reflections,
  or monologue about the relationship, without much interaction in the scene.

- Use 3.1 (Positive Emotions & Contentment) for standalone happiness, gratitude,
  relief, or contentment (any character). Use 4.5 when commitment/HEA is central;
  4.6 when reassurance/protection is central; 2.2 when affection is physical,
  not purely internal.

- Use 5.1 (Family & Kinship) when the emotional core of the topic is about
  parents, children, or siblings, even if it indirectly affects the main couple.
  If a topic mentions "mother", "sister", "father" etc. and the scene is about
  family dynamics rather than the main couple's direct interaction, prefer 5.1
  over 4.x.

- Use 5.2 (Friends & Social Circles) for friend interactions, colleague social
  support, found family.

- Use 5.3 (Community, Norms & Social Events) for parties, weddings, holidays,
  community judgment, public rituals.

2) 7.2 (Violence, Threats & Coercion) - USE SPARINGLY

- Use 7.2 ONLY when there is clear physical violence, explicit threats,
  coercion, or danger (weapons, beating, assault, explicit harm).

- Teasing, snarky banter, or verbal arguments WITHOUT explicit threats belong
  in 4.4 (Conflict, Distance & Breakup Threats), NOT 7.2.

- Emotional conflict, relationship struggles, or heated discussions between
  the main couple should use 4.4, not 7.2.

- Only use 7.2 when violence or coercion is the PRIMARY function of the scene.

2b) 7.1 (Interpersonal Non-Romantic Conflict / Antagonistic Conflict, Non-Couple)

- Arguments, hostility, or power struggles with bosses, rivals, antagonists, or
  institutional gatekeepers — NOT main-couple conflict (→ 4.4), NOT family/kinship
  dynamics (→ 5.1), NOT friend support circles (→ 5.2), NOT violence/threats (→ 7.2),
  NOT accidents/disasters (→ 7.3).

- Shared-workplace spats between the main couple → 6.3 or 4.4, NOT 7.1.

3) 4.3 (Secrets, Misunderstandings) vs. 4.4 (Conflict, Distance)

- Use 4.3 when the topic is about concealed facts, misunderstandings, or
  withheld truths BETWEEN the main couple that create tension.

- Use 4.4 for arguments, distancing, threats of breakup, or serious relational
  strain - even if it involves emotional intensity.

- Do NOT use 4.3 for any emotionally tense talk; reserve it for topics where
  hidden information or misunderstandings are the core issue.

4) LUXURY & STATUS (COMPOSITE — NO SINGLE "BILLIONAIRE" NODE)

- Luxury appears indirectly: fashion/gowns (6.6), aristocratic formality (6.7),
  weddings/parties (5.3), hotels/restaurants (8.2), jewelry/clothes as objects (8.3).
- Do NOT collapse all wealth signals into 6.1. Prefer the most specific node.
- Generic "negotiating terms" without business context → 4.x or 5.x, NOT 6.1.

5) APPEARANCE vs ATTRACTION vs EXPLICIT vs NEGOTIATION vs COERCION

- Cataloguing hair, clothes, mirror, grooming → 1.6 (or 1.7 if gaze/expression dominates).
- Charged desire/longing with flirtation → 2.1.
- Explicit sexual body focus or intercourse → 2.3, NOT 1.6/1.7.
- Condom/lube preparation, negotiating when to stop, sex-without-commitment talk → 2.5, NOT 2.3.
- Aftercare and emotional processing after sex → 2.4.
- Unwanted touch, coercion signals, nonconsent, threatening sexual contact → 7.4 (watchlist).
  Forceful consensual intensity without boundary-risk evidence → 2.3 with unclear consent in
  Stage 08 metadata, NOT 7.4 automatically.
- Physical violence/threats outside sexual contact → 7.2.

5b) STAGE 08 v3 SEXUAL-FUNCTION HINTS (when present)

- sexual_function contraception_preparation | sexual_negotiation | sex_without_commitment → 2.5
- sexual_function explicit_contact | orgasm_climax | postsex_arousal → 2.3
- sexual_function postsex_aftercare → 2.4
- sexual_function sexual_tension | presex_escalation → 2.1
- sexual_function nonsexual_affection → 2.2 or 4.1/4.2/4.6 by relational beat
- consent_status coercion_watchlist | nonconsent_explicit → prefer 7.4 over 2.3
- axis_hint consent_control_risk → 7.4, 7.2, or 4.7 by dominant beat

6) STAGE 08 ROUTING HINTS

- If primary includes narrative_style → prefer 9.1–9.4 (discourse is included in analysis).
- Reserve exclude_from_axes for is_noise / paratext / publisher boilerplate only.
- If primary includes appearance_presentation or secondary includes activity:dressing → 1.6.

7) PROTECTIVE CARE vs JEALOUSY (H4)

- Use 4.6 for non-coercive protection, reassurance, vows to keep someone safe, caretaking.
- Use 4.7 for jealousy, possessive claiming, rivalry with exes — NOT generic 4.4 unless jealousy is absent.
- Do NOT use 7.2 for protective vows unless actual violence/coercion is central.

8) SUBGENRE & 10.x ROUTING

- Default rule: If the topic is a scene beat (kiss, argument, dinner, phone), map to the
  scene category (2.x–8.x). Subgenre is incidental.

- Use 10.x as main ONLY when genre furniture dominates:
  supernatural systems (10.1), period social furniture beyond generic conflict (10.2),
  investigation/clues (10.3), combat set-pieces (10.4).

- Subgenre hint routing:
  - subgenre_hints [contemporary] or [young_adult] → do NOT use 10.x unless keywords
    clearly show paranormal/historical/mystery/action.
  - subgenre_paranormal / hints [paranormal] → 10.1
  - subgenre_historical / hints [historical] → 10.2
  - subgenre_suspense / hints [mystery] → 10.3
  - Armed combat / gunfight keywords without couple-conflict center → 10.4

- Blended topics: werewolf kiss → main 2.1 or 2.2, secondary 10.1; Regency ball
  etiquette → main 5.3 or 6.7, secondary 10.2.

- Negative rule: Never assign 10.x solely because Stage08 listed a contemporary hint.
  If content_type is subgenre_marker → prefer 10.x matching subgenre_hints.

9) EVERYDAY INTIMACY & EMOTIONAL SAFETY (composite axis — H1 / Goodreads hypothesis)

Use taxonomy IDs 4.1, 4.2, 4.6, and 2.2 (plus 8.1 or 8.2 as secondary) for non-explicit
scenes that create romantic closeness, comfort, trust, or low-threat bonding. This axis
replaces the overly narrow "domestic care" framing — domestic routines are only one subpart.

Include when the topic's central function is:
- Courtship / romantic approach: first-date planning, dinner dates, flirtation, winks,
  invitations, dance-floor approach, goodnight farewells, negotiating relationship terms.
- Non-sexual affection: gentle kisses, hugs, reassuring touch, cautious physical approach,
  flirtatious but non-explicit touch, physical closeness with anticipation.
- Everyday companionship: shared meals, coffee/tea/kitchen moments, offers to drive home,
  practical help, seasonal outing plans, invitation to sit together.
- Emotional safety: reassurance, apologies, forgiveness, worry for wellbeing, trust-building,
  medical/recovery care, vows to protect, respecting limits and negotiating when to stop.

Do NOT restrict this axis to domestic settings. A restaurant, doorway, car, dance floor,
phone call, or public social event can count if the function is courtship, affection, care,
or emotional safety.

Routing preferences:
- Early approach / first-date / flirtation → 4.1 main (4.2 secondary if bonding dominates).
- Ongoing dates, meals, goodnight scenes, ordinary closeness → 4.2 main.
- Reassurance, apology, protection vow, medical care, limit negotiation → 4.6 main.
- Kiss/hug/touch as the central beat → 2.2 main (4.2 or 4.6 secondary if relational).
- Kitchen/chore routine with weak relational beat → 8.1 main; if care/bonding is clear → 4.2 or 4.6 main, 8.1 secondary.

Do NOT use this axis for:
- Explicit sex, coercive control, armed danger, jealousy/possessive claiming (4.7),
  forceful intensity with boundary-risk signals, or stalker threat — unless the topic clearly
  emphasizes aftercare or repair (→ 2.4 or 4.6) rather than threat or domination.
- Forceful explicit sexual contact with unclear consent → 7.4 watchlist or 2.3, NOT 4.2/4.6.
- Condom/boundary/sex-without-commitment negotiation → 2.5, NOT 4.2/4.6 alone.
- Pure setting description without a relational function → 8.x only.

Stage 08 hints: intimacy:courtship_ritual, intimacy:nonsexual_affection,
intimacy:everyday_companionship, intimacy:domestic_care, intimacy:emotional_safety,
intimacy:consent_negotiation, sexual:contraception, sexual:negotiation, risk:coercive_control
support routing but do not override explicit sex or violence keywords.

SPECIAL RULES ABOUT VIOLENCE VS EXERCISE

- Any physical activity that is NOT clearly harmful or coercive
  (e.g., workouts, sport, training, running, dance practice) should use 1.5.

- Only use 7.2 (Violence, Threats & Coercion) when the language or scenes clearly
  indicate harm, threat, assault, or coercion.

NO REASONING OUTSIDE JSON

- You may think step-by-step internally.

- The final answer must be only the JSON object described above.
""".strip()


TAXONOMY_ZEROSHOT_USER_PROMPT = """
### TOPIC DATA

topic_id: {topic_id}

TOPIC KEYWORDS (most important first):

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

REPRESENTATIVE SNIPPETS (optional):

{snippets}

### TASK

Using ONLY the information above and the taxonomy defined in the system message:

- Decide whether this topic is noise or meaningful.

- If meaningful, choose:

  - one main_category_id (required),

  - an optional secondary_category_id,

  - optional other_plausible_ids (0–3).

- If noise, set main_category_id to "noise", secondary_category_id to null, and is_noise to true.

Return a SINGLE JSON object following the schema in the system message.

Do NOT include explanations outside the JSON.
""".strip()


# ---------------------------------------------------------------------------
# 4. Core function: classify a single topic into the taxonomy
# ---------------------------------------------------------------------------

def _finalize_taxonomy_result(
    result: Dict[str, Any],
    topic_metadata: Dict[str, Any],
) -> Dict[str, Any]:
    """Apply heuristics, enrich names, and propagate Stage 08 axis flags."""
    taxonomy_path = str(TAXONOMY_CONFIG_PATH)
    result = apply_domain_heuristics(result, topic_metadata, taxonomy_path)
    result = enrich_with_category_names(result, taxonomy_path)
    if "exclude_from_axes" not in result:
        result["exclude_from_axes"] = bool(topic_metadata.get("exclude_from_axes", False))
    return result


def classify_topic_to_taxonomy_openrouter(
    *,
    topic_id: int,
    topic_metadata: Dict[str, Any],
    client: OpenAI,
    model_name: str,
    temperature: float = 0.25,
    max_new_tokens: int = 220,
    representative_docs: Optional[List[str]] = None,
    max_snippets: int = 8,
    max_chars_per_snippet: int = 400,
) -> Dict[str, Any]:
    """
    Classify a single BERTopic topic into the Romance Corpus Topic Taxonomy
    using Mistral-Nemo via OpenRouter.

    Parameters
    ----------
    topic_id:
        Integer topic id.
    topic_metadata:
        Dict with at least:
        - "keywords": List[str]
        - "label": str (from Stage 08)
        - "scene_summary": str (optional but recommended)
        - "primary_categories": List[str] (optional)
        - "secondary_categories": List[str] (optional)
        - "is_noise": bool (optional hint)
    client:
        OpenRouter OpenAI-compatible client.
    model_name:
        Model name (e.g., "mistralai/Mistral-Nemo-Instruct-2407").
    temperature:
        Sampling temperature (low-ish for stable classification).
    max_new_tokens:
        Max tokens for JSON output.
    representative_docs:
        Optional list of representative doc snippets for this topic.
    max_snippets:
        Max snippets to include.
    max_chars_per_snippet:
        Max characters per snippet.

    Returns
    -------
    Dict with keys:
        "topic_id",
        "main_category_id",
        "secondary_category_id",
        "other_plausible_ids",
        "is_noise",
        "confidence",
        "rationale",
        "main_category_name",
        "main_category_group",
        "secondary_category_name",
        "secondary_category_group",
        "other_plausible_categories" (list of {id, name, group})
    """
    keywords = topic_metadata.get("keywords", [])
    label = topic_metadata.get("label", "")
    scene_summary = topic_metadata.get("scene_summary", "")
    primary_categories = topic_metadata.get("primary_categories", [])
    secondary_categories = topic_metadata.get("secondary_categories", [])
    prev_is_noise = topic_metadata.get("is_noise", False)
    content_type = topic_metadata.get("content_type", "(unknown)")
    exclude_from_axes = topic_metadata.get("exclude_from_axes", False)
    subgenre_hints = topic_metadata.get("subgenre_hints", []) or []
    register = topic_metadata.get("register", "neutral")
    sexual_explicitness = topic_metadata.get("sexual_explicitness", "(none)")
    sexual_function = topic_metadata.get("sexual_function", "(none)")
    consent_status = topic_metadata.get("consent_status", "(not_applicable)")
    axis_hint = topic_metadata.get("axis_hint", "(none)")

    pre_routed = try_pre_route_taxonomy(
        topic_id,
        topic_metadata,
        str(TAXONOMY_CONFIG_PATH),
    )
    if pre_routed is not None:
        result = _finalize_taxonomy_result(pre_routed, topic_metadata)
        LOGGER.info(
            "Topic %d pre-routed → main=%s (%s), secondary=%s, noise=%s",
            topic_id,
            result.get("main_category_id"),
            result.get("main_category_name"),
            result.get("secondary_category_id"),
            result.get("is_noise"),
        )
        return result

    kw_str = ", ".join(keywords) if keywords else "(no keywords)"
    primary_str = ", ".join(primary_categories) if primary_categories else "(none)"
    secondary_str = ", ".join(secondary_categories) if secondary_categories else "(none)"

    # Format representative snippets using same helper as Stage 08
    snippets_block = "(none)"
    if representative_docs:
        central_docs = rerank_snippets_centrality(
            representative_docs,
            top_k=max_snippets,
        )
        formatted = format_snippets(
            central_docs,
            max_snippets=max_snippets,
            max_chars=max_chars_per_snippet,
            anonymize=True,
        )
        snippets_block = formatted if formatted else "(none)"

    user_prompt = TAXONOMY_ZEROSHOT_USER_PROMPT.format(
        topic_id=topic_id,
        keywords=kw_str,
        label=label or "(no label)",
        scene_summary=scene_summary or "(no scene summary)",
        primary_categories=primary_str,
        secondary_categories=secondary_str,
        content_type=content_type,
        exclude_from_axes=exclude_from_axes,
        subgenre_hints=", ".join(subgenre_hints) if subgenre_hints else "(none)",
        register=register,
        sexual_explicitness=sexual_explicitness,
        sexual_function=sexual_function,
        consent_status=consent_status,
        axis_hint=axis_hint,
        snippets=snippets_block,
    )

    messages = [
        {"role": "system", "content": TAXONOMY_ZEROSHOT_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    LOGGER.info("Classifying topic %d into taxonomy (Mistral-Nemo)...", topic_id)

    # Retry logic with exponential backoff for rate limits
    max_retries = 6
    base_delay = 15.0  # Start with 15 seconds (Mistral-Nemo has strict rate limits)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_new_tokens,
                temperature=temperature,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.0,
            )
            break  # Success, exit retry loop
        except Exception as e:
            error_str = str(e).lower()
            is_rate_limit = "429" in error_str or "rate limit" in error_str or "rate-limited" in error_str
            
            if is_rate_limit and attempt < max_retries - 1:
                # Calculate delay with exponential backoff
                if attempt == max_retries - 2:
                    # Second-to-last attempt: wait 5 minutes for rate limit window to reset
                    delay = 300.0
                    LOGGER.warning(
                        "Rate limit hit for topic %d (attempt %d/%d). Waiting %.1f seconds (5 minutes) for rate limit window to reset...",
                        topic_id, attempt + 1, max_retries, delay
                    )
                else:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff: 15s, 30s, 60s, 120s, 240s
                    LOGGER.warning(
                        "Rate limit hit for topic %d (attempt %d/%d). Waiting %.1f seconds before retry...",
                        topic_id, attempt + 1, max_retries, delay
                    )
                time.sleep(delay)
            else:
                # Not a rate limit, or we've exhausted retries
                raise

    if not response.choices:
        raise ValueError("Empty API response for taxonomy classification")

    content = response.choices[0].message.content.strip()
    LOGGER.debug("Raw taxonomy response for topic %d: %s", topic_id, content[:300])

    # Extract JSON (strip optional code fences defensively)
    json_content = content
    if "```json" in json_content:
        json_content = json_content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in json_content:
        # Any fenced code block
        json_content = json_content.split("```", 1)[1].split("```", 1)[0].strip()

    # Fallback: try to grab the first {...} span
    if not json_content.strip().startswith("{"):
        first_brace = json_content.find("{")
        last_brace = json_content.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_content = json_content[first_brace : last_brace + 1]

    try:
        result = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse taxonomy JSON for topic {topic_id}: {e}\nContent:\n{content}"
        ) from e

    # Minimal sanity checks + gentle corrections
    result_topic_id = result.get("topic_id", topic_id)
    if result_topic_id != topic_id:
        LOGGER.warning(
            "Model echoed different topic_id (%s) than input (%s); overriding with input.",
            result_topic_id,
            topic_id,
        )
        result["topic_id"] = topic_id

    main_id = result.get("main_category_id")
    sec_id = result.get("secondary_category_id", None)
    is_noise = bool(result.get("is_noise", False))

    # If model says noise, enforce noise semantics
    if is_noise:
        result["main_category_id"] = "noise"
        result["secondary_category_id"] = None
    else:
        # Fix missing or invalid main_category_id
        if not main_id or main_id not in VALID_TAXONOMY_IDS or main_id == "noise":
            # If previous stage already marked this topic as noise, keep it noise
            if prev_is_noise:
                result["main_category_id"] = "noise"
                result["secondary_category_id"] = None
                result["is_noise"] = True
            else:
                result["main_category_id"] = fallback_main_category(primary_categories)
                result["is_noise"] = False

        # Validate secondary ID
        if sec_id is not None and sec_id not in VALID_TAXONOMY_IDS:
            result["secondary_category_id"] = None

    # Normalize other_plausible_ids
    other_ids = result.get("other_plausible_ids", [])
    if not isinstance(other_ids, list):
        other_ids = []
    filtered_other = []
    for cid in other_ids:
        if (
            isinstance(cid, str)
            and cid in VALID_TAXONOMY_IDS
            and cid not in {result["main_category_id"], result.get("secondary_category_id")}
        ):
            filtered_other.append(cid)
    result["other_plausible_ids"] = filtered_other

    # Normalize confidence
    confidence = result.get("confidence", None)
    valid_conf = {"low", "medium", "high"}
    if not isinstance(confidence, str) or confidence.lower() not in valid_conf:
        # Simple heuristic: if we had to fall back or fix IDs, treat as low confidence
        if is_noise:
            confidence = "medium"
        else:
            confidence = "low"
    else:
        confidence = confidence.lower()
    result["confidence"] = confidence

    result = _finalize_taxonomy_result(result, topic_metadata)

    LOGGER.info(
        "Topic %d → main=%s (%s), secondary=%s (%s), noise=%s, confidence=%s",
        topic_id,
        result.get("main_category_id"),
        result.get("main_category_name"),
        result.get("secondary_category_id"),
        result.get("secondary_category_name"),
        result.get("is_noise"),
        result.get("confidence"),
    )

    return result


# ---------------------------------------------------------------------------
# 5. Batch mapping utility: map all topics from a labels JSON file
# ---------------------------------------------------------------------------

def load_topic_metadata(labels_json_path: Path) -> Dict[int, Dict[str, Any]]:
    """
    Load Stage 08 topic metadata JSON (labels + keywords + categories etc.)
    and convert keys to int.
    """
    with open(labels_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta: Dict[int, Dict[str, Any]] = {}
    for k, v in data.items():
        try:
            tid = int(k)
        except ValueError:
            continue
        meta[tid] = v
    return meta


def load_bertopic_model_for_snippets(
    *,
    base_dir: Path = DEFAULT_BASE_DIR,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    model_suffix: str = "_with_llm_labels",
    stage_subfolder: Optional[str] = "stage08_llm_labeling",
    max_docs_per_topic: int = 10,
) -> Optional[Dict[int, List[str]]]:
    """
    Load BERTopic model and extract representative documents for snippets.
    
    Parameters
    ----------
    base_dir:
        Base directory for models (default: models/retrained).
    embedding_model:
        Embedding model name (default: paraphrase-MiniLM-L6-v2).
    model_suffix:
        Model suffix (default: "_with_llm_labels").
    stage_subfolder:
        Optional stage subfolder (default: "stage08_llm_labeling").
    max_docs_per_topic:
        Maximum number of representative docs to extract per topic.
        
    Returns
    -------
    Dict mapping topic_id to list of representative document strings, or None if loading fails.
    """
    try:
        LOGGER.info("Loading BERTopic model for representative document extraction...")
        LOGGER.info("  Base dir: %s", base_dir)
        LOGGER.info("  Embedding model: %s", embedding_model)
        LOGGER.info("  Model suffix: %s", model_suffix)
        LOGGER.info("  Stage subfolder: %s", stage_subfolder)
        
        topic_model = load_native_bertopic_model(
            base_dir=base_dir,
            embedding_model=embedding_model,
            pareto_rank=1,
            model_suffix=model_suffix,
            stage_subfolder=stage_subfolder,
        )
        
        LOGGER.info("✓ BERTopic model loaded successfully")
        
        # Extract representative documents
        LOGGER.info("Extracting representative documents from model...")
        topic_to_snippets = extract_representative_docs_per_topic(
            topic_model,
            max_docs_per_topic=max_docs_per_topic,
        )
        
        snippets_count = len([tid for tid, docs in topic_to_snippets.items() if docs])
        avg_snippets = (
            sum(len(docs) for docs in topic_to_snippets.values()) / max(snippets_count, 1)
        )
        LOGGER.info(
            "✓ Extracted representative docs for %d topics (avg %.1f docs per topic)",
            snippets_count,
            avg_snippets,
        )
        
        return topic_to_snippets
        
    except Exception as e:
        LOGGER.warning(
            "Failed to load BERTopic model or extract snippets: %s. "
            "Taxonomy classification will proceed without representative snippets.",
            e,
        )
        return None


def map_all_topics_to_taxonomy(
    *,
    labels_json_path: Path,
    output_path: Path,
    client: Optional[OpenAI] = None,
    model_name: str = DEFAULT_OPENROUTER_MODEL,
    api_key: Optional[str] = None,
    temperature: float = 0.25,
    max_new_tokens: int = 220,
    topic_to_snippets: Optional[Dict[int, List[str]]] = None,
    # Model loading parameters for snippet extraction
    load_model_for_snippets: bool = True,
    base_dir: Path = DEFAULT_BASE_DIR,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    model_suffix: str = "_with_llm_labels",
    stage_subfolder: Optional[str] = "stage08_llm_labeling",
    max_docs_per_topic: int = 10,
    limit_topics: Optional[int] = None,
    include_source_metadata: bool = False,
) -> Dict[int, Dict[str, Any]]:
    """
    Run zero-shot taxonomy mapping for all topics that have LLM labels.

    Parameters
    ----------
    labels_json_path:
        Path to Stage 08 labels JSON (as produced by generate_labels_openrouter.save_labels_openrouter).
    output_path:
        Path to write taxonomy mapping JSON (topic_id → mapping dict).
    client:
        Optional existing OpenRouter client. If None, a new one is created via load_openrouter_client.
    model_name:
        Model name for classification.
    api_key:
        Optional API key (if client is None). If None, environment variable is used.
    temperature, max_new_tokens:
        Generation params.
    topic_to_snippets:
        Optional dict[topic_id → list[str]] of representative docs.
        If None and load_model_for_snippets=True, will attempt to load from BERTopic model.
    load_model_for_snippets:
        If True and topic_to_snippets is None, load BERTopic model and extract snippets.
    base_dir, embedding_model, model_suffix, stage_subfolder:
        Parameters for loading BERTopic model (used if load_model_for_snippets=True).
    max_docs_per_topic:
        Maximum number of representative docs to extract per topic.
    include_source_metadata:
        If True, include original metadata from labels JSON (keywords, label, primary_categories,
        secondary_categories, scene_summary, label_rationale) in the output for manual evaluation.

    Returns
    -------
    Dict[int, Dict[str, Any]] mapping topic_id → taxonomy mapping.
    """
    # Initialize client if needed
    if client is None:
        client, _ = load_openrouter_client(
            api_key=api_key or "",
            model_name=model_name,
        )

    # Load topic metadata
    topic_meta = load_topic_metadata(labels_json_path)
    topic_ids = sorted(topic_meta.keys())
    total = len(topic_ids)
    LOGGER.info("Loaded metadata for %d topics from %s", total, labels_json_path)
    
    # Apply limit if specified (for testing)
    if limit_topics is not None and limit_topics > 0:
        topic_ids = topic_ids[:limit_topics]
        total = len(topic_ids)
        LOGGER.info("Limited to first %d topics for testing", limit_topics)

    # Load snippets from BERTopic model if requested and not provided
    if topic_to_snippets is None and load_model_for_snippets:
        LOGGER.info("Loading BERTopic model to extract representative documents...")
        topic_to_snippets = load_bertopic_model_for_snippets(
            base_dir=base_dir,
            embedding_model=embedding_model,
            model_suffix=model_suffix,
            stage_subfolder=stage_subfolder,
            max_docs_per_topic=max_docs_per_topic,
        )
        if topic_to_snippets:
            LOGGER.info(
                "Using representative snippets from BERTopic model for taxonomy classification"
            )
        else:
            LOGGER.info("Proceeding without representative snippets")
    elif topic_to_snippets is None:
        LOGGER.info("No representative snippets provided, using keywords and labels only")

    # Try to load existing checkpoint if output file exists
    taxonomy_map: Dict[int, Dict[str, Any]] = {}
    if output_path.exists():
        LOGGER.info("Found existing output file. Loading checkpoint to resume...")
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            for k, v in existing_data.items():
                try:
                    tid = int(k)
                    taxonomy_map[tid] = v
                except ValueError:
                    continue
            LOGGER.info("Loaded %d topics from checkpoint", len(taxonomy_map))
        except Exception as e:
            LOGGER.warning("Failed to load checkpoint: %s. Starting fresh.", e)
            taxonomy_map = {}

    # Filter out already processed topics
    remaining_topics = [tid for tid in topic_ids if tid not in taxonomy_map]
    if len(remaining_topics) < len(topic_ids):
        LOGGER.info(
            "Resuming: %d topics already processed, %d remaining",
            len(taxonomy_map),
            len(remaining_topics),
        )
    else:
        LOGGER.info("Starting fresh: processing all %d topics", len(topic_ids))

    for idx, tid in enumerate(remaining_topics, start=1):
        tm = topic_meta[tid]
        snippets = topic_to_snippets.get(tid, []) if topic_to_snippets else None
        
        try:
            result = classify_topic_to_taxonomy_openrouter(
                topic_id=tid,
                topic_metadata=tm,
                client=client,
                model_name=model_name,
                temperature=temperature,
                max_new_tokens=max_new_tokens,
                representative_docs=snippets,
            )
        except Exception as e:
            LOGGER.error(
                "Failed to classify topic %d after retries: %s. Saving checkpoint and exiting.",
                tid, e
            )
            # Save checkpoint before exiting
            output_path.parent.mkdir(parents=True, exist_ok=True)
            serializable = {str(k): v for k, v in taxonomy_map.items()}
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2, ensure_ascii=False)
            LOGGER.info("Checkpoint saved. Resume by running the same command again.")
            raise
        
        # Optionally include source metadata from labels JSON for manual evaluation
        if include_source_metadata:
            result["source_metadata"] = {
                "label": tm.get("label", ""),
                "keywords": tm.get("keywords", []),
                "primary_categories": tm.get("primary_categories", []),
                "secondary_categories": tm.get("secondary_categories", []),
                "scene_summary": tm.get("scene_summary", ""),
                "label_rationale": tm.get("rationale", ""),  # Original rationale from labeling stage
            }
        
        taxonomy_map[tid] = result

        # Delay to avoid rate limits (10 seconds between requests for Mistral-Nemo)
        # Mistral-Nemo has very strict rate limits, so we need longer delays
        if idx < len(remaining_topics):
            time.sleep(10.0)

        # Save checkpoint every 10 topics
        if idx % 10 == 0 or idx == len(remaining_topics):
            output_path.parent.mkdir(parents=True, exist_ok=True)
            serializable = {str(k): v for k, v in taxonomy_map.items()}
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2, ensure_ascii=False)
            LOGGER.info(
                "Processed %d/%d remaining topics (%.1f%%). Checkpoint saved.",
                idx, len(remaining_topics), idx / len(remaining_topics) * 100.0
            )

    # Final save (already saved during checkpointing, but ensure it's up to date)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {str(k): v for k, v in taxonomy_map.items()}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)

    LOGGER.info(
        "✓ Completed! Saved taxonomy mappings for %d topics to %s", len(serializable), output_path
    )
    return taxonomy_map


def update_model_with_taxonomy_mappings(
    *,
    taxonomy_json_path: Path,
    base_dir: Path = DEFAULT_BASE_DIR,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    model_suffix: str = "_with_llm_labels",
    source_stage_subfolder: str = "stage08_llm_labeling",
    target_stage_subfolder: str = "stage09_category_mapping",
    target_model_suffix: str = "_with_taxonomy_mappings",
) -> Path:
    """
    Load BERTopic model, attach taxonomy mappings, and save to new location.
    
    Parameters
    ----------
    taxonomy_json_path:
        Path to taxonomy mappings JSON file.
    base_dir:
        Base directory for models.
    embedding_model:
        Embedding model name.
    model_suffix:
        Suffix of source model to load.
    source_stage_subfolder:
        Stage subfolder where source model is located.
    target_stage_subfolder:
        Stage subfolder where updated model will be saved.
    target_model_suffix:
        Suffix for the updated model.
        
    Returns
    -------
    Path to the saved model directory.
    """
    LOGGER.info("Loading taxonomy mappings from %s", taxonomy_json_path)
    with open(taxonomy_json_path, "r", encoding="utf-8") as f:
        taxonomy_data = json.load(f)
    
    # Convert string keys to int
    taxonomy_map: Dict[int, Dict[str, Any]] = {}
    for k, v in taxonomy_data.items():
        try:
            tid = int(k)
            taxonomy_map[tid] = v
        except ValueError:
            continue
    
    LOGGER.info("Loaded taxonomy mappings for %d topics", len(taxonomy_map))
    
    # Load source model
    LOGGER.info("Loading source BERTopic model...")
    LOGGER.info("  Base dir: %s", base_dir)
    LOGGER.info("  Embedding model: %s", embedding_model)
    LOGGER.info("  Model suffix: %s", model_suffix)
    LOGGER.info("  Stage subfolder: %s", source_stage_subfolder)
    
    # Construct path with stage subfolder
    source_base_dir = base_dir / embedding_model / source_stage_subfolder
    
    topic_model = load_native_bertopic_model(
        base_dir=source_base_dir,
        embedding_model=".",  # Use "." to avoid path duplication
        pareto_rank=1,
        model_suffix=model_suffix,
    )
    
    LOGGER.info("✓ Source model loaded successfully")
    
    # Attach taxonomy mappings to model
    LOGGER.info("Attaching taxonomy mappings to model...")
    topic_model.topic_taxonomy_ = taxonomy_map
    LOGGER.info("✓ Taxonomy mappings attached to model.topic_taxonomy_")
    
    # Verify attachment
    if hasattr(topic_model, "topic_taxonomy_") and topic_model.topic_taxonomy_:
        LOGGER.info(
            "✓ Verified: taxonomy mappings attached for %d topics",
            len(topic_model.topic_taxonomy_)
        )
        # Log sample
        sample_topic = list(taxonomy_map.keys())[0]
        sample_data = taxonomy_map[sample_topic]
        LOGGER.info(
            "  Sample taxonomy keys for topic %d: %s",
            sample_topic,
            list(sample_data.keys())[:10],  # First 10 keys
        )
    else:
        LOGGER.warning("⚠ Taxonomy mappings may not have been attached correctly")
    
    # Save model to target location
    target_dir = base_dir / embedding_model / target_stage_subfolder
    target_dir.mkdir(parents=True, exist_ok=True)
    
    model_dir = target_dir / f"model_1{target_model_suffix}"
    
    # Remove existing directory if it exists
    if model_dir.exists() and model_dir.is_dir():
        LOGGER.info("Removing existing model directory: %s", model_dir)
        shutil.rmtree(model_dir)
    
    LOGGER.info("Saving updated model to %s", model_dir)
    topic_model.save(str(model_dir))
    LOGGER.info("✓ Model saved successfully to %s", model_dir)
    
    return model_dir


if __name__ == "__main__":
    import argparse
    import os

    from src.stage03_train.embeddings_hub import load_project_dotenv

    load_project_dotenv()

    parser = argparse.ArgumentParser(
        description="Stage 09: Zero-shot taxonomy mapping of BERTopic topics using Mistral via OpenRouter.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--labels-json",
        type=Path,
        required=True,
        help="Path to Stage 08 labels JSON (labels_pos_openrouter_..._romance_aware_*.json).",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        required=True,
        help="Where to save taxonomy mappings JSON.",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=DEFAULT_OPENROUTER_MODEL,
        help="OpenRouter model name to use.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="",
        help="OpenRouter API key (optional; otherwise environment variable is used).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.25,
        help="Sampling temperature (low for stable classification).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=220,
        help="Maximum new tokens for JSON output.",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=DEFAULT_BASE_DIR,
        help="Base directory for BERTopic models (default: models/retrained).",
    )
    parser.add_argument(
        "--embedding-model",
        type=str,
        default=DEFAULT_EMBEDDING_MODEL,
        help="Embedding model name (default: paraphrase-MiniLM-L6-v2).",
    )
    parser.add_argument(
        "--model-suffix",
        type=str,
        default="_with_llm_labels",
        help="Model suffix (default: _with_llm_labels).",
    )
    parser.add_argument(
        "--model-stage",
        type=str,
        default="stage08_llm_labeling",
        help="Stage subfolder for model (default: stage08_llm_labeling).",
    )
    parser.add_argument(
        "--max-docs-per-topic",
        type=int,
        default=10,
        help="Maximum number of representative docs to extract per topic (default: 10).",
    )
    parser.add_argument(
        "--no-snippets",
        action="store_true",
        help="Skip loading BERTopic model and extracting representative snippets.",
    )
    parser.add_argument(
        "--limit-topics",
        type=int,
        default=None,
        help="Limit processing to first N topics (for testing, default: process all).",
    )
    parser.add_argument(
        "--taxonomy-config",
        type=Path,
        default=DEFAULT_TAXONOMY_PATH,
        help="Path to romance_corpus_taxonomy_v2.yaml.",
    )
    parser.add_argument(
        "--include-source-metadata",
        action="store_true",
        help="Include original metadata from labels JSON (keywords, label, categories, scene_summary, label_rationale) in output. Useful for manual evaluation of first N topics.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call the API, just print the first user prompt and exit.",
    )
    parser.add_argument(
        "--save-model",
        action="store_true",
        help="After taxonomy mapping, update and save the BERTopic model with taxonomy mappings.",
    )
    parser.add_argument(
        "--target-model-suffix",
        type=str,
        default="_with_taxonomy_mappings",
        help="Suffix for the saved model (default: _with_taxonomy_mappings).",
    )

    args = parser.parse_args()

    # Set log level
    logging.getLogger().setLevel(args.log_level)
    reload_taxonomy(args.taxonomy_config)

    # Handle dry-run mode
    if args.dry_run:
        meta = load_topic_metadata(args.labels_json)
        first_tid = sorted(meta.keys())[0]
        tm = meta[first_tid]
        user_prompt = TAXONOMY_ZEROSHOT_USER_PROMPT.format(
            topic_id=first_tid,
            keywords=", ".join(tm.get("keywords", [])),
            label=tm.get("label", "(no label)"),
            scene_summary=tm.get("scene_summary", "(no scene summary)"),
            primary_categories=", ".join(tm.get("primary_categories", [])),
            secondary_categories=", ".join(tm.get("secondary_categories", [])),
            content_type=tm.get("content_type", "(unknown)"),
            exclude_from_axes=tm.get("exclude_from_axes", False),
            subgenre_hints=", ".join(tm.get("subgenre_hints", [])) or "(none)",
            register=tm.get("register", "neutral"),
            sexual_explicitness=tm.get("sexual_explicitness", "(none)"),
            sexual_function=tm.get("sexual_function", "(none)"),
            consent_status=tm.get("consent_status", "(not_applicable)"),
            axis_hint=tm.get("axis_hint", "(none)"),
            snippets="(none)",
        )
        print("=== SYSTEM PROMPT ===")
        print(TAXONOMY_ZEROSHOT_SYSTEM_PROMPT)
        print("\n=== USER PROMPT (topic", first_tid, ") ===")
        print(user_prompt)
        raise SystemExit(0)

    client, _ = load_openrouter_client(
        api_key=args.api_key or os.environ.get("OPENROUTER_API_KEY", ""),
        model_name=args.model_name,
    )

    map_all_topics_to_taxonomy(
        labels_json_path=args.labels_json,
        output_path=args.output_json,
        client=client,
        model_name=args.model_name,
        temperature=args.temperature,
        max_new_tokens=args.max_tokens,
        load_model_for_snippets=not args.no_snippets,
        base_dir=args.base_dir,
        embedding_model=args.embedding_model,
        model_suffix=args.model_suffix,
        stage_subfolder=args.model_stage,
        max_docs_per_topic=args.max_docs_per_topic,
        limit_topics=args.limit_topics,
        include_source_metadata=args.include_source_metadata,
    )
    
    # Update and save model if requested
    if args.save_model:
        LOGGER.info("\n" + "=" * 80)
        LOGGER.info("Updating BERTopic model with taxonomy mappings")
        LOGGER.info("=" * 80)
        model_path = update_model_with_taxonomy_mappings(
            taxonomy_json_path=args.output_json,
            base_dir=args.base_dir,
            embedding_model=args.embedding_model,
            model_suffix=args.model_suffix,
            source_stage_subfolder=args.model_stage,
            target_stage_subfolder="stage09_category_mapping",
            target_model_suffix=args.target_model_suffix,
        )
        LOGGER.info("✓ Model update complete. Saved to: %s", model_path)

