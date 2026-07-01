"""Export slim Stage08 topic metadata for Stage09 taxonomy mapping.

Strips deprecated / review-only fields and writes to a dedicated subfolder.

Usage:
    python3 -m src.stage08_llm_labeling.openrouter_experiments.tools.export_stage09_topic_metadata \
        --input-json results/stage08_llm_labeling/placeholder_v4_call73/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_topic_labeling_review_enriched.json
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Fields removed from Stage08 v3 slim schema (derived in Stage09 at read time).
DEPRECATED_STAGE08_FIELDS = frozenset({"register", "subgenre_hints", "axis_hint"})

# Stage07 audit passthrough — not used by Stage09 prompts.
STAGE07_AUDIT_FIELDS = frozenset(
    {"stage07_exclude_from_axes", "stage07_posthoc_reason", "stage07_content_type"}
)

# Human review / labeling artifacts — not required for taxonomy mapping.
REVIEW_ONLY_FIELDS = frozenset({"rationale", "representations", "all_keywords"})

DEFAULT_OUTPUT_SUBDIR = "stage09_input"
DEFAULT_OUTPUT_NAME = "topic_metadata_v3.json"


def slim_topic_entry(entry: dict[str, Any]) -> dict[str, Any]:
    drop = DEPRECATED_STAGE08_FIELDS | STAGE07_AUDIT_FIELDS | REVIEW_ONLY_FIELDS
    return {k: v for k, v in entry.items() if k not in drop}


def export_stage09_metadata(
    labels: dict[str, Any],
    *,
    drop_noise: bool = False,
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for topic_id_str, entry in labels.items():
        if drop_noise and entry.get("is_noise"):
            continue
        out[topic_id_str] = slim_topic_entry(entry)
    return out


def default_output_dir(input_path: Path) -> Path:
    return input_path.parent / DEFAULT_OUTPUT_SUBDIR


def write_readme(output_dir: Path) -> None:
    readme = output_dir / "README.md"
    readme.write_text(
        """# Stage09 topic metadata input (call 73)

Slim export from Stage08 v3 labels — ready for `--labels-json` in Stage09 taxonomy mapping.

## Included per topic

- `label`, `scene_summary`, `keywords`
- `content_type`, `is_noise`, `exclude_from_axes`
- `sexual_explicitness`, `sexual_function`, `consent_status`
- `snippets` (when present in source enriched export)

## Excluded (derived or review-only)

- `register`, `subgenre_hints`, `axis_hint` — derived in Stage09 via `v3_derived_fields.py`
- `stage07_*`, `rationale`, `representations`, `all_keywords`

## Run Stage09

```bash
python3 -m src.stage09_category_mapping.stage2_theory_driven_categories.scripts.zeroshot_taxonomy_openrouter \\
  --labels-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \\
  --output-json results/stage09_category_mapping/stage2_theory_driven_categories/placeholder_v4_call73/taxonomy_mappings.json \\
  --prompt-version v2 \\
  --no-snippets
```

Use `--no-snippets` when snippets are already embedded in this JSON (recommended for this bundle).
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Export slim Stage09 topic metadata JSON")
    parser.add_argument("--input-json", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--output-name", default=DEFAULT_OUTPUT_NAME)
    parser.add_argument(
        "--move",
        action="store_true",
        help="Delete input file after successful export (when input was the enriched review JSON).",
    )
    parser.add_argument(
        "--drop-noise",
        action="store_true",
        help="Omit is_noise topics from export.",
    )
    args = parser.parse_args()

    input_path = args.input_json.resolve()
    output_dir = (args.output_dir or default_output_dir(input_path)).resolve()
    output_path = output_dir / args.output_name

    with input_path.open(encoding="utf-8") as f:
        labels = json.load(f)

    slim = export_stage09_metadata(labels, drop_noise=args.drop_noise)
    output_dir.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(slim, f, indent=2, ensure_ascii=False)
        f.write("\n")
    write_readme(output_dir)

    LOGGER.info(
        "Wrote %d topics to %s (dropped fields: %s)",
        len(slim),
        output_path,
        ", ".join(sorted(DEPRECATED_STAGE08_FIELDS | STAGE07_AUDIT_FIELDS | REVIEW_ONLY_FIELDS)),
    )

    if args.move and input_path != output_path:
        input_path.unlink()
        LOGGER.info("Removed source file: %s", input_path)


if __name__ == "__main__":
    main()
