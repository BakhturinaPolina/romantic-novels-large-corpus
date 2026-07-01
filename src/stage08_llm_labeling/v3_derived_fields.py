"""Derive Stage09 routing fields from slim Stage08 v3 output (no LLM axis/register/subgenre)."""

from __future__ import annotations

from typing import Any

SEXUAL_FUNCTION_TO_AXIS: dict[str, str] = {
    "none": "everyday_intimacy_emotional_safety",
    "nonsexual_affection": "everyday_intimacy_emotional_safety",
    "sexual_tension": "sexual_tension_explicit_intimacy",
    "presex_escalation": "sexual_tension_explicit_intimacy",
    "contraception_preparation": "sexual_tension_explicit_intimacy",
    "sexual_negotiation": "sexual_tension_explicit_intimacy",
    "explicit_contact": "sexual_tension_explicit_intimacy",
    "orgasm_climax": "sexual_tension_explicit_intimacy",
    "postsex_aftercare": "sexual_tension_explicit_intimacy",
    "postsex_arousal": "sexual_tension_explicit_intimacy",
    "sex_without_commitment": "sexual_tension_explicit_intimacy",
    "consent_boundary": "consent_control_risk",
}

SUBGENRE_KEYWORD_HINTS: dict[str, frozenset[str]] = {
    "paranormal": frozenset(
        {
            "werewolf", "vampire", "shift", "shifted", "pack", "alpha", "wolf",
            "demon", "witch", "spell", "dragon", "angel", "growl", "fangs",
            "supernatural", "shifter", "lycan", "mate", "bespelled",
        }
    ),
    "historical": frozenset(
        {
            "regency", "duke", "duchess", "lord", "lady", "carriage", "ballroom",
            "ton", "gown", "corset", "parlor", "aristocrat", "viscount",
        }
    ),
    "mystery": frozenset(
        {
            "detective", "investigation", "clue", "suspect", "murder", "crime",
            "interrogate", "evidence", "alibi",
        }
    ),
    "young_adult": frozenset(
        {"dorm", "campus", "college", "homework", "prom", "teen", "teenager"},
    ),
}


def infer_register_v3(sexual_explicitness: str) -> str:
    mapping = {
        "none": "neutral",
        "affection_only": "neutral",
        "suggestive": "suggestive",
        "explicit": "explicit",
    }
    return mapping.get(str(sexual_explicitness).lower(), "neutral")


def infer_axis_hint_v3(
    *,
    sexual_function: str,
    consent_status: str = "not_applicable",
    exclude_from_axes: bool = False,
    is_noise: bool = False,
) -> str:
    if is_noise or exclude_from_axes:
        return "exclude_from_axes"
    consent = str(consent_status).lower()
    if consent in {"coercion_watchlist", "nonconsent_explicit"}:
        return "consent_control_risk"
    fn = str(sexual_function).lower()
    if fn == "consent_boundary":
        return "consent_control_risk"
    return SEXUAL_FUNCTION_TO_AXIS.get(fn, "everyday_intimacy_emotional_safety")


def infer_subgenre_hints_v3(
    *,
    content_type: str,
    label: str = "",
    keywords: list[str] | None = None,
) -> list[str]:
    """Infer subgenre tags only when evidence is strong; never default to contemporary."""
    if str(content_type).lower() != "subgenre_marker":
        return []

    blob = " ".join([label] + list(keywords or [])).lower()
    tokens = set(blob.split())
    hints: list[str] = []
    for hint, terms in SUBGENRE_KEYWORD_HINTS.items():
        if terms.intersection(tokens) or any(term in blob for term in terms):
            hints.append(hint)
    return hints


def enrich_v3_metadata_for_stage09(metadata: dict[str, Any]) -> dict[str, Any]:
    """Fill register, axis_hint, subgenre_hints when absent (Stage09 consumers)."""
    out = dict(metadata)
    if not out.get("register"):
        out["register"] = infer_register_v3(str(out.get("sexual_explicitness", "none")))
    if not out.get("axis_hint"):
        out["axis_hint"] = infer_axis_hint_v3(
            sexual_function=str(out.get("sexual_function", "none")),
            consent_status=str(out.get("consent_status", "not_applicable")),
            exclude_from_axes=bool(out.get("exclude_from_axes", False)),
            is_noise=bool(out.get("is_noise", False)),
        )
    if not out.get("subgenre_hints"):
        out["subgenre_hints"] = infer_subgenre_hints_v3(
            content_type=str(out.get("content_type", "scene")),
            label=str(out.get("label", "")),
            keywords=out.get("keywords") or out.get("all_keywords"),
        )
    return out
