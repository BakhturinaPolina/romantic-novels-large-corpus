"""Load versioned Stage 08 labeling prompts and JSON schema."""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_PROMPT_VERSION = "v2"

_PROMPTS_DIR = Path(__file__).resolve().parent


def load_prompts(version: str | None = None) -> tuple[str, str]:
    """Return (system_prompt, user_prompt_template) for the given version."""
    ver = (version or DEFAULT_PROMPT_VERSION).lower()
    if ver in ("v1", "v1_scene_only"):
        from src.stage08_llm_labeling.prompts.v1_scene_only import (
            SYSTEM_PROMPT,
            USER_PROMPT_TEMPLATE,
        )
        return SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    if ver in ("v2", "v2_multi_genre"):
        from src.stage08_llm_labeling.prompts.v2_multi_genre import (
            SYSTEM_PROMPT,
            USER_PROMPT_TEMPLATE,
        )
        return SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    raise ValueError(f"Unknown prompt version: {version!r} (use v1 or v2)")


def load_schema(version: str | None = None) -> dict:
    """Load JSON Schema for LLM output validation."""
    ver = (version or DEFAULT_PROMPT_VERSION).lower()
    if ver.startswith("v1"):
        path = _PROMPTS_DIR / "schema_v1.json"
    else:
        path = _PROMPTS_DIR / "schema_v2.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)
