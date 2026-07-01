"""JSON schema and normalization for Stage09 taxonomy mapping v2."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Set

from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    MECHANIC_TAG_ENUM,
    valid_taxonomy_ids,
)

CONTENT_TYPE_ENUM = [
    "scene",
    "discourse",
    "subgenre_marker",
    "paratext_or_boilerplate",
    "character_name_cluster",
    "noise",
]

EVIDENCE_QUALITY_ENUM = ["high", "medium", "low"]

MACRO_EXCLUDED_CONTENT_TYPES = frozenset({
    "noise",
    "paratext_or_boilerplate",
    "character_name_cluster",
})

WATCHLIST_CONTENT_TYPES = frozenset({
    "discourse",
    "subgenre_marker",
})

TAXONOMY_MAPPING_DEFAULTS: Dict[str, Any] = {
    "content_type": "scene",
    "mechanic_tags": [],
    "use_in_macro_axes": True,
    "use_in_theory_watchlist": True,
    "noise_reason": None,
    "evidence_quality": "medium",
    "uncertainty_reason": None,
    "other_plausible_ids": [],
    "mapping_reasoning": None,
}


def taxonomy_id_enum(path: Optional[str] = None, *, include_noise: bool = True) -> List[str]:
    ids = sorted(valid_taxonomy_ids(path))
    if include_noise and "noise" not in ids:
        ids.append("noise")
    return ids


def secondary_id_enum(path: Optional[str] = None) -> List[str]:
    return [cid for cid in taxonomy_id_enum(path, include_noise=False) if cid != "noise"]


def build_taxonomy_mapping_schema(taxonomy_path: Optional[str] = None) -> Dict[str, Any]:
    """Build OpenRouter/Anthropic JSON schema from romance_corpus_taxonomy_v2.yaml."""
    path = taxonomy_path or str(DEFAULT_TAXONOMY_PATH)
    main_enum = taxonomy_id_enum(path, include_noise=True)
    sec_enum = secondary_id_enum(path)

    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "topic_id",
            "content_type",
            "main_category_id",
            "secondary_category_id",
            "other_plausible_ids",
            "mechanic_tags",
            "is_noise",
            "use_in_macro_axes",
            "use_in_theory_watchlist",
            "confidence",
            "evidence_quality",
            "uncertainty_reason",
            "rationale",
            "mapping_reasoning",
            "noise_reason",
        ],
        "properties": {
            "topic_id": {"type": "integer"},
            "content_type": {"type": "string", "enum": CONTENT_TYPE_ENUM},
            "main_category_id": {"type": "string", "enum": main_enum},
            "secondary_category_id": {
                "anyOf": [
                    {"type": "string", "enum": sec_enum},
                    {"type": "null"},
                ],
            },
            "other_plausible_ids": {
                "type": "array",
                "items": {"type": "string", "enum": sec_enum},
                "maxItems": 4,
            },
            "mechanic_tags": {
                "type": "array",
                "items": {"type": "string", "enum": MECHANIC_TAG_ENUM},
                "maxItems": 5,
            },
            "is_noise": {"type": "boolean"},
            "use_in_macro_axes": {"type": "boolean"},
            "use_in_theory_watchlist": {"type": "boolean"},
            "noise_reason": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
            },
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "evidence_quality": {"type": "string", "enum": EVIDENCE_QUALITY_ENUM},
            "uncertainty_reason": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
            },
            "rationale": {"type": "string", "maxLength": 600},
            "mapping_reasoning": {
                "type": "string",
                "maxLength": 1200,
                "description": (
                    "Structured debug reasoning: cite strongest evidence (snippets first), "
                    "explain main vs rejected alternatives, secondary choice, and macro_axes decision."
                ),
            },
        },
    }


def confidence_to_band(value: Any) -> str:
    """Map numeric or legacy string confidence to low|medium|high."""
    if isinstance(value, str):
        band = value.lower().strip()
        if band in {"low", "medium", "high"}:
            return band
    try:
        num = float(value)
    except (TypeError, ValueError):
        return "low"
    if num >= 0.75:
        return "high"
    if num >= 0.45:
        return "medium"
    return "low"


def band_to_confidence(band: str) -> float:
    return {"high": 0.85, "medium": 0.6, "low": 0.3}.get(band, 0.5)


def _coerce_confidence(value: Any, *, fallback_band: str = "medium") -> float:
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    if isinstance(value, str):
        lower = value.lower().strip()
        if lower in {"low", "medium", "high"}:
            return band_to_confidence(lower)
        try:
            return max(0.0, min(1.0, float(value)))
        except ValueError:
            pass
    return band_to_confidence(fallback_band)


def _normalize_mechanic_tags(tags: Any) -> List[str]:
    if not isinstance(tags, list):
        return []
    valid = set(MECHANIC_TAG_ENUM)
    out: List[str] = []
    for tag in tags:
        if isinstance(tag, str) and tag in valid and tag not in out:
            out.append(tag)
        if len(out) >= 5:
            break
    return out


def _apply_quality_flag_consistency(result: Dict[str, Any]) -> None:
    content_type = result.get("content_type", "scene")
    is_noise = bool(result.get("is_noise", False))

    if is_noise:
        result["main_category_id"] = "noise"
        result["secondary_category_id"] = None
        result["use_in_macro_axes"] = False
        result["use_in_theory_watchlist"] = False
        result["exclude_from_axes"] = True
        if not result.get("noise_reason"):
            result["noise_reason"] = result.get("noise_reason") or "incoherent_or_artifact_topic"
        return

    if content_type in MACRO_EXCLUDED_CONTENT_TYPES:
        result["use_in_macro_axes"] = False
    elif content_type == "discourse":
        result["use_in_macro_axes"] = False
        result["use_in_theory_watchlist"] = True
    elif content_type == "subgenre_marker":
        result["use_in_macro_axes"] = False
        result["use_in_theory_watchlist"] = True

    if content_type in WATCHLIST_CONTENT_TYPES and not is_noise:
        result["use_in_theory_watchlist"] = True

    main_id = result.get("main_category_id")
    if main_id:
        from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
            exclude_from_axes_ids,
            secondary_context_ids,
        )

        if main_id in exclude_from_axes_ids() or main_id in secondary_context_ids():
            result["use_in_macro_axes"] = False

    result["exclude_from_axes"] = not bool(result.get("use_in_macro_axes", True))


def normalize_taxonomy_mapping_result(
    raw: Dict[str, Any],
    *,
    topic_id: int,
    topic_metadata: Dict[str, Any],
    valid_ids: Set[str],
    prompt_version: str = "v2",
) -> Dict[str, Any]:
    """Normalize LLM or pre-routed taxonomy mapping to v2 contract."""
    result = copy.deepcopy(raw)
    result["topic_id"] = topic_id

    for key, default in TAXONOMY_MAPPING_DEFAULTS.items():
        if key not in result or result[key] is None:
            if key == "content_type" and topic_metadata.get("content_type"):
                stage08_ct = topic_metadata["content_type"]
                mapping = {
                    "paratext": "paratext_or_boilerplate",
                    "procedural_transition": "scene",
                }
                result[key] = mapping.get(stage08_ct, stage08_ct)
            else:
                result[key] = copy.deepcopy(default)

    result["mechanic_tags"] = _normalize_mechanic_tags(result.get("mechanic_tags"))
    result["confidence"] = _coerce_confidence(result.get("confidence"))
    result["confidence_band"] = confidence_to_band(result["confidence"])

    eq = result.get("evidence_quality")
    if not isinstance(eq, str) or eq not in EVIDENCE_QUALITY_ENUM:
        result["evidence_quality"] = result["confidence_band"]

    other_ids = result.get("other_plausible_ids", [])
    if not isinstance(other_ids, list):
        other_ids = []
    filtered_other: List[str] = []
    for cid in other_ids[:4]:
        if (
            isinstance(cid, str)
            and cid in valid_ids
            and cid != "noise"
            and cid not in {result.get("main_category_id"), result.get("secondary_category_id")}
        ):
            filtered_other.append(cid)
    result["other_plausible_ids"] = filtered_other

    is_noise = bool(result.get("is_noise", False))
    main_id = result.get("main_category_id")
    sec_id = result.get("secondary_category_id")

    if is_noise:
        result["main_category_id"] = "noise"
        result["secondary_category_id"] = None
    else:
        if not main_id or main_id not in valid_ids or main_id == "noise":
            if topic_metadata.get("is_noise"):
                result["main_category_id"] = "noise"
                result["secondary_category_id"] = None
                result["is_noise"] = True
            else:
                from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import fallback_main_category

                primary = topic_metadata.get("primary_categories", []) or []
                result["main_category_id"] = fallback_main_category(primary)
                result["is_noise"] = False
        if sec_id is not None and sec_id not in valid_ids:
            result["secondary_category_id"] = None
        elif sec_id == result.get("main_category_id"):
            result["secondary_category_id"] = None

    _apply_quality_flag_consistency(result)

    rationale = result.get("rationale")
    if not result.get("mapping_reasoning") and isinstance(rationale, str) and rationale.strip():
        result["mapping_reasoning"] = rationale.strip()

    if prompt_version.startswith("v1") and "confidence_band" not in result:
        result["confidence"] = result.get("confidence_band", confidence_to_band(result["confidence"]))

    return result


def validate_taxonomy_mapping_json(
    result: Dict[str, Any],
    schema: Dict[str, Any],
) -> List[str]:
    """Return list of validation error messages (empty if valid)."""
    try:
        import jsonschema

        jsonschema.validate(instance=result, schema=schema)
        return []
    except ImportError:
        return []
    except Exception as exc:
        return [str(exc)]
