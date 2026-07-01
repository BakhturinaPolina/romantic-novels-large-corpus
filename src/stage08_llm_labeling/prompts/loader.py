"""Load versioned Stage 08 labeling prompts and JSON schema."""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_PROMPT_VERSION = "v3_topic_labeling"

_PROMPTS_DIR = Path(__file__).resolve().parent
_LEGACY_DIR = _PROMPTS_DIR / "legacy"


def load_prompts(version: str | None = None) -> tuple[str, str]:
    """Return (system_prompt, user_prompt_template) for the given version."""
    ver = (version or DEFAULT_PROMPT_VERSION).lower()
    if ver in ("v3", "v3_topic_labeling", "v3_sexual_precision"):
        from src.stage08_llm_labeling.prompts.v3_topic_labeling import (
            SYSTEM_PROMPT,
            USER_PROMPT_TEMPLATE,
        )
        return SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    if ver in ("v3_rep_first", "v3_keywords_first"):
        from src.stage08_llm_labeling.prompts.v3_rep_first import (
            SYSTEM_PROMPT,
            USER_PROMPT_TEMPLATE,
        )
        return SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    if ver in ("v1", "v1_scene_only"):
        from src.stage08_llm_labeling.prompts.legacy.v1_scene_only import (
            SYSTEM_PROMPT,
            USER_PROMPT_TEMPLATE,
        )
        return SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    if ver in ("v2", "v2_multi_genre"):
        from src.stage08_llm_labeling.prompts.legacy.v2_multi_genre_full import (
            SYSTEM_PROMPT,
            USER_PROMPT_TEMPLATE,
        )
        return SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    if ver.startswith("v2_"):
        from src.stage08_llm_labeling.prompts.legacy.v2_variants_sweeps import load_variant

        return load_variant(ver)
    if ver == "v3_sexual_precision_legacy":
        from src.stage08_llm_labeling.prompts.legacy.v3_sexual_precision import (
            SYSTEM_PROMPT,
            USER_PROMPT_TEMPLATE,
        )
        return SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    raise ValueError(
        f"Unknown prompt version: {version!r} "
        "(use v3_topic_labeling, v3_rep_first, v1, v2, v2_*, or v3_sexual_precision_legacy)"
    )


def load_schema(version: str | None = None) -> dict:
    """Load JSON Schema for LLM output validation."""
    ver = (version or DEFAULT_PROMPT_VERSION).lower()
    if ver.startswith("v1"):
        path = _LEGACY_DIR / "schema_v1.json"
    elif ver.startswith("v3"):
        path = _PROMPTS_DIR / "schema_v3.json"
    elif ver.startswith("v2"):
        path = _LEGACY_DIR / "schema_v2_full.json"
    else:
        path = _PROMPTS_DIR / "schema_v3.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)
