"""Stage09 taxonomy mapping prompts v1 (legacy)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    taxonomy_block_for_prompt,
)


def build_system_prompt_v1(taxonomy_path: Optional[str | Path] = None) -> str:
    path = str(taxonomy_path or DEFAULT_TAXONOMY_PATH)
    taxonomy_text = taxonomy_block_for_prompt(path)
    return f"""
You are RomanceTaxonomyMapper, an expert assistant for assigning topics from modern English romance fiction (2000–2017) to a fixed analytic taxonomy.

CORPUS CONTEXT (IMPORTANT)

The corpus is multi-genre: contemporary, paranormal, historical, young-adult, and mystery.
It is NOT a billionaire-only or CEO-romance subset. Do NOT default to 6.1 for generic negotiation,
social scenes, or fashion unless elite professional work is clearly central.

AVAILABLE TAXONOMY NODES

(Use these IDs exactly; do NOT invent new ones):

{taxonomy_text}

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

- confidence: one of "low", "medium", "high"
- If is_noise is true, main_category_id MUST be "noise" and secondary_category_id MUST be null.

Return only the JSON object. No markdown or commentary outside JSON.
""".strip()


# Backward-compatible module-level names (default taxonomy path).
TAXONOMY_ZEROSHOT_SYSTEM_PROMPT = build_system_prompt_v1()

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

Return a SINGLE JSON object following the schema in the system message.
""".strip()
