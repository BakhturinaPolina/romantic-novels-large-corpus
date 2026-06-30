"""Prompt loader for Stage09 taxonomy mapping."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

DEFAULT_PROMPT_VERSION = "v2"


def load_taxonomy_prompts(
    version: str = DEFAULT_PROMPT_VERSION,
    taxonomy_path: Path | str | None = None,
) -> Tuple[str, str]:
    """Return (system_prompt, user_prompt_template) for the given version."""
    ver = (version or DEFAULT_PROMPT_VERSION).lower()
    if ver in ("v1", "1"):
        from src.stage09_category_mapping.stage2_theory_driven_categories.prompts.taxonomy_mapping_v1 import (
            TAXONOMY_ZEROSHOT_USER_PROMPT,
            build_system_prompt_v1,
        )
        return build_system_prompt_v1(taxonomy_path), TAXONOMY_ZEROSHOT_USER_PROMPT
    if ver in ("v2", "2", DEFAULT_PROMPT_VERSION):
        from src.stage09_category_mapping.stage2_theory_driven_categories.prompts.taxonomy_mapping_v2 import (
            build_system_prompt,
            TAXONOMY_ZEROSHOT_USER_PROMPT_V2,
        )
        return build_system_prompt(taxonomy_path), TAXONOMY_ZEROSHOT_USER_PROMPT_V2
    raise ValueError(f"Unknown taxonomy prompt version: {version}")
