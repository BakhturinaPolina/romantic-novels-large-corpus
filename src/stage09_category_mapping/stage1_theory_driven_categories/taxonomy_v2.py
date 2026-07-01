"""Shared Romance Corpus Taxonomy v2 loader, pre-router, and domain heuristics."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

DEFAULT_TAXONOMY_PATH = (
    Path(__file__).resolve().parents[3] / "configs" / "stage09" / "romance_corpus_taxonomy_v2.yaml"
)

EXPLICIT_EROGENOUS_TERMS = {
    "breast", "breasts", "boob", "boobs",
    "nipple", "nipples",
    "clit", "clitoris",
    "pussy", "cunt",
    "cock", "dick", "penis",
}

VIOLENCE_TERMS = {
    "punch", "punches", "hit", "hits", "kick", "kicks",
    "gun", "guns", "knife", "stab", "stabbed",
    "blood", "bleeding", "fight", "fighting",
    "attack", "attacked", "assault",
}

FAMILY_TERMS = {
    "mother", "mom", "mum", "father", "dad", "parents",
    "sister", "brother", "daughter", "son",
    "niece", "nephew", "in-law", "stepmother", "stepfather",
    "sibling", "siblings", "parent", "child", "children",
}

LUXURY_FASHION_TERMS = {
    "gown", "silk", "jewelry", "jewellery", "designer", "fashion",
    "model", "modeling", "modelling", "fitting", "glamour", "stunning dress",
    "champagne", "luxury",
}

ARISTOCRACY_TERMS = {
    "court", "duke", "lord", "lady", "titled", "noble", "aristocrat",
    "regency", "aristocratic",
}

ELITE_WORK_TERMS = {
    "ceo", "executive", "boardroom", "corporate", "company", "business",
    "hospital", "surgeon", "lawyer",
}

APPEARANCE_TERMS = {
    "hair", "braid", "ponytail", "mirror", "groom", "shave", "outfit",
    "dress", "physique", "attractive", "stunning", "appearance", "beauty",
    "clothes", "clothing", "shoe", "shoes", "makeup",
}

GAZE_TERMS = {
    "gaze", "eyes", "stare", "smirk", "wink", "eyebrow", "forehead",
}

NON_OVERRIDABLE_CATEGORIES = {
    "2.1", "2.2", "2.3", "2.4", "2.5",
    "3.1", "3.2", "3.3", "3.4",
    "4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7",
    "7.1", "7.2", "7.3", "7.4",
    "1.6", "1.7",
    "9.1", "9.2", "9.3", "9.4",
    "10.1", "10.2", "10.3", "10.4",
}

CONTRACEPTION_TERMS = {
    "condom", "condoms", "lube", "lubricant", "nightstand", "drawer", "bedside",
}

BOUNDARY_RISK_TERMS = {
    "pinned", "forceful", "coercion", "coercive", "blackmail", "threat", "captivity",
    "refusal", "refuse", "cannot move", "unwanted", "nonconsent",
}

SEXUAL_FUNCTION_TO_TAXONOMY = {
    "nonsexual_affection": "2.2",
    "sexual_tension": "2.1",
    "presex_escalation": "2.1",
    "contraception_preparation": "2.5",
    "sexual_negotiation": "2.5",
    "sex_without_commitment": "2.5",
    "explicit_contact": "2.3",
    "orgasm_climax": "2.3",
    "postsex_aftercare": "2.4",
    "postsex_arousal": "2.3",
    "consent_boundary": "7.4",
}

PROTECTIVE_CARE_TERMS = {
    "protect", "protection", "protective", "reassure", "reassurance",
    "caretaking", "safe", "safety", "comfort", "shield", "guard",
}

JEALOUSY_POSSESSIVE_TERMS = {
    "jealous", "jealousy", "possessive", "possessiveness", "mine",
    "territorial", "rival", "ex-boyfriend", "ex-girlfriend",
}

SUBGENRE_PRIMARY_TO_TAXONOMY = {
    "subgenre_paranormal": "10.1",
    "subgenre_historical": "10.2",
    "subgenre_suspense": "10.3",
}

CONTENT_TYPE_TO_TAXONOMY = {
    "noise": "noise",
    "paratext": "noise",
    "paratext_or_boilerplate": "noise",
    "character_name_cluster": "noise",
    "discourse": "9.1",
}

MECHANIC_TAG_ENUM = [
    "protective_care",
    "possessive_control",
    "external_threat",
    "sex_without_commitment",
    "post_sex_bonding",
    "pregnancy_future",
    "paternity_secret",
    "trust_repair",
    "secret_misunderstanding",
    "economic_power",
    "professional_hierarchy",
    "domestic_care",
    "paranormal_instinct",
    "forceful_intensity",
    "ambiguous_consent_watchlist",
    "reputation_risk",
    "series_world",
]

FORCEFUL_INTENSITY_TERMS = {
    "forceful", "pounded", "pinned", "thrust", "grip", "gripped",
}


@lru_cache(maxsize=4)
def load_taxonomy_config(path: Optional[str] = None) -> Dict[str, Any]:
    cfg_path = Path(path) if path else DEFAULT_TAXONOMY_PATH
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_taxonomy_nodes(path: Optional[str] = None) -> List[Dict[str, str]]:
    cfg = load_taxonomy_config(path)
    return list(cfg.get("nodes", []))


def taxonomy_by_id(path: Optional[str] = None) -> Dict[str, Dict[str, str]]:
    return {node["id"]: node for node in load_taxonomy_nodes(path)}


def valid_taxonomy_ids(path: Optional[str] = None) -> Set[str]:
    return set(taxonomy_by_id(path).keys())


def taxonomy_block_for_prompt(path: Optional[str] = None) -> str:
    lines = []
    for node in load_taxonomy_nodes(path):
        lines.append(
            f"- {node['id']} — {node['name']} "
            f"({node['group']}): {node['description']}"
        )
    return "\n".join(lines)


def composite_index_spec(name: str, path: Optional[str] = None) -> Dict[str, Any]:
    cfg = load_taxonomy_config(path)
    composites = cfg.get("composite_indices", {})
    if name not in composites:
        raise KeyError(f"Unknown composite index: {name}")
    return composites[name]


def category_names_for_ids(ids: List[str], path: Optional[str] = None) -> List[str]:
    by_id = taxonomy_by_id(path)
    return [by_id[cid]["name"] for cid in ids if cid in by_id]


def _token_set(keywords: List[str]) -> Set[str]:
    joined = " ".join(str(k) for k in keywords).lower()
    return set(re.findall(r"\b\w+\b", joined))


def _text_blob(topic_metadata: Dict[str, Any]) -> str:
    parts = [
        topic_metadata.get("label", ""),
        topic_metadata.get("scene_summary", ""),
        topic_metadata.get("rationale", ""),
    ]
    parts.extend(topic_metadata.get("keywords", []) or [])
    return " ".join(str(p) for p in parts).lower()


def try_pre_route_taxonomy(
    topic_id: int,
    topic_metadata: Dict[str, Any],
    path: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Deterministic routing for clear Stage 08 v2 cases.
    Returns a full mapping dict when LLM call can be skipped; otherwise None.
    """
    valid_ids = valid_taxonomy_ids(path)
    by_id = taxonomy_by_id(path)

    if topic_metadata.get("is_noise"):
        return _make_result(
            topic_id, "noise", None, True, 0.9,
            "Stage 08 marked topic as noise (is_noise=true).",
            by_id,
            exclude_from_axes=True,
            pre_routed=True,
            content_type="noise",
            use_in_macro_axes=False,
            use_in_theory_watchlist=False,
            noise_reason="stage08_is_noise",
        )

    if topic_metadata.get("exclude_from_axes"):
        content_type = topic_metadata.get("content_type", "")
        primary = topic_metadata.get("primary_categories", []) or []

        if content_type in {"discourse", "subgenre_marker", "scene"}:
            # Stage09 policy: only is_noise / paratext / publisher artifacts are excluded.
            pass
        elif content_type in CONTENT_TYPE_TO_TAXONOMY:
            main_id = CONTENT_TYPE_TO_TAXONOMY[content_type]
            is_noise = main_id == "noise"
            ct_out = content_type
            if content_type == "paratext":
                ct_out = "paratext_or_boilerplate"
            return _make_result(
                topic_id, main_id, None, is_noise, 0.9,
                f"exclude_from_axes with content_type={content_type}.",
                by_id,
                exclude_from_axes=True,
                pre_routed=True,
                content_type=ct_out,
                use_in_macro_axes=False,
                use_in_theory_watchlist=not is_noise,
                noise_reason=f"stage08_{content_type}" if is_noise else None,
            )
        elif "narrative_style" in primary:
            return _make_result(
                topic_id, "9.1", None, False, 0.85,
                "Stage 08 primary narrative_style → dialogue delivery discourse.",
                by_id,
                exclude_from_axes=False,
                pre_routed=True,
                content_type="discourse",
                use_in_macro_axes=False,
                use_in_theory_watchlist=True,
            )
        elif "nonfiction_or_technical" in primary:
            return _make_result(
                topic_id, "noise", None, True, 0.9,
                "Nonfiction/technical primary category.",
                by_id,
                exclude_from_axes=True,
                pre_routed=True,
                content_type="paratext_or_boilerplate",
                use_in_macro_axes=False,
                use_in_theory_watchlist=False,
                noise_reason="nonfiction_or_technical",
            )

    content_type = topic_metadata.get("content_type", "")
    primary = topic_metadata.get("primary_categories", []) or []
    secondary = topic_metadata.get("secondary_categories", []) or []

    if content_type == "subgenre_marker":
        for tag, tid in SUBGENRE_PRIMARY_TO_TAXONOMY.items():
            if tag in primary:
                return _make_result(
                    topic_id, tid, None, False, 0.85,
                    f"Subgenre marker ({tag}).",
                    by_id,
                    exclude_from_axes=False,
                    pre_routed=True,
                    content_type="subgenre_marker",
                    use_in_macro_axes=True,
                    use_in_theory_watchlist=True,
                    mechanic_tags=["paranormal_instinct"] if tid == "10.1" else [],
                )

    for tag, tid in SUBGENRE_PRIMARY_TO_TAXONOMY.items():
        if tag in primary and content_type != "scene":
            return _make_result(
                topic_id, tid, None, False, 0.6,
                f"Primary {tag} without clear scene beat.",
                by_id,
                exclude_from_axes=False,
                pre_routed=True,
                content_type="subgenre_marker",
                use_in_macro_axes=True,
                use_in_theory_watchlist=True,
            )

    if "appearance_presentation" in primary or "activity:dressing" in secondary:
        sec_id = "8.3" if any(t in _text_blob(topic_metadata) for t in ("dress", "outfit", "gown", "clothes")) else None
        return _make_result(
            topic_id, "1.6", sec_id, False, 0.85,
            "Appearance/grooming or activity:dressing from Stage 08.",
            by_id,
            exclude_from_axes=False,
            pre_routed=True,
            content_type="scene",
            use_in_macro_axes=True,
            use_in_theory_watchlist=True,
        )

    return None


def apply_domain_heuristics(
    result: Dict[str, Any],
    topic_metadata: Dict[str, Any],
    path: Optional[str] = None,
) -> Dict[str, Any]:
    """Post-hoc domain-specific fixes for borderline taxonomy mappings."""
    from src.stage08_llm_labeling.v3_derived_fields import enrich_v3_metadata_for_stage09

    topic_metadata = enrich_v3_metadata_for_stage09(topic_metadata)
    valid_ids = valid_taxonomy_ids(path)
    main_id = result.get("main_category_id")
    secondary_id = result.get("secondary_category_id")
    primary_cats = topic_metadata.get("primary_categories", []) or []
    secondary_cats = topic_metadata.get("secondary_categories", []) or []
    keywords = topic_metadata.get("keywords", []) or []
    tokens = _token_set(keywords)
    blob = _text_blob(topic_metadata)
    blob_tokens = _token_set(blob.split())
    appearance_hit = APPEARANCE_TERMS.intersection(tokens) or APPEARANCE_TERMS.intersection(blob_tokens)
    gaze_hit = GAZE_TERMS.intersection(tokens) or GAZE_TERMS.intersection(blob_tokens)

    register = str(topic_metadata.get("register", "neutral")).lower()
    consent_status = str(topic_metadata.get("consent_status", "not_applicable")).lower()
    sexual_function = str(topic_metadata.get("sexual_function", "none")).lower()
    axis_hint = str(topic_metadata.get("axis_hint", "")).lower()

    # Stage 08 v3 sexual-function routing (when present)
    if consent_status in {"coercion_watchlist", "nonconsent_explicit"}:
        if main_id in {"2.3", "2.2", "2.1", "4.4"}:
            result["secondary_category_id"] = main_id if main_id != "7.4" else secondary_id
        result["main_category_id"] = "7.4"
        main_id = "7.4"
    elif axis_hint == "consent_control_risk" and sexual_function == "consent_boundary":
        if main_id not in {"7.4", "7.2", "noise"}:
            result["secondary_category_id"] = main_id
        result["main_category_id"] = "7.4"
        main_id = "7.4"
    elif sexual_function in SEXUAL_FUNCTION_TO_TAXONOMY:
        target = SEXUAL_FUNCTION_TO_TAXONOMY[sexual_function]
        if main_id in {"8.1", "8.2", "8.3", "4.2", "4.1"} and target in valid_ids:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = target
            main_id = target
        elif main_id not in {"7.4", "noise"} and target != main_id:
            if target in {"2.3", "2.5", "2.4", "2.1", "2.2"} and main_id in {"8.1", "8.2", "1.6", "1.7"}:
                result["secondary_category_id"] = main_id
                result["main_category_id"] = target
                main_id = target

    if (
        "sexual:contraception" in secondary_cats
        or CONTRACEPTION_TERMS.intersection(tokens)
    ) and main_id in {"2.3", "8.1", "8.2", "4.2"}:
        result["secondary_category_id"] = main_id if main_id != "2.5" else secondary_id
        result["main_category_id"] = "2.5"
        main_id = "2.5"

    if (
        "sexual:negotiation" in secondary_cats
        or "intimacy:consent_negotiation" in secondary_cats
        or sexual_function in {"sexual_negotiation", "sex_without_commitment"}
    ) and main_id in {"2.3", "4.4", "4.6", "8.1"}:
        result["secondary_category_id"] = main_id if main_id != "2.5" else secondary_id
        result["main_category_id"] = "2.5"
        main_id = "2.5"

    if topic_metadata.get("exclude_from_axes") and "narrative_style" in primary_cats:
        if main_id not in {"noise", "9.1", "9.2", "9.3", "9.4"}:
            result["main_category_id"] = "9.1"
            result["secondary_category_id"] = None
            main_id = "9.1"
        result["exclude_from_axes"] = True

    if (
        "sexual_content" in primary_cats
        and main_id == "2.2"
        and EXPLICIT_EROGENOUS_TERMS.intersection(tokens)
    ):
        if secondary_id == "2.3":
            secondary_id = None
        result["secondary_category_id"] = secondary_id
        result["main_category_id"] = "2.3"
        main_id = "2.3"

    if main_id == "7.2":
        has_real_violence = bool(VIOLENCE_TERMS.intersection(tokens))
        if (
            not has_real_violence
            and ("relationship_conflict" in primary_cats or "romance_core" in primary_cats)
        ):
            result["secondary_category_id"] = "7.2"
            result["main_category_id"] = "4.4"
            main_id = "4.4"

    if (
        "sexual_content" not in primary_cats
        and VIOLENCE_TERMS.intersection(tokens)
        and main_id not in {"10.4", "7.2", "7.3"}
    ):
        if main_id not in {"noise", "7.1", "7.3"}:
            result["secondary_category_id"] = main_id
        result["main_category_id"] = "7.2"
        main_id = "7.2"

    if main_id in {"4.2", "4.3", "4.4"}:
        if FAMILY_TERMS.intersection(tokens) and "romance_core" not in primary_cats:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "5.1"
            main_id = "5.1"

    # Appearance routing
    if (
        main_id in {"2.1", "4.1", "4.2", "8.3"}
        and ("appearance_presentation" in primary_cats or "activity:dressing" in secondary_cats)
        and register != "explicit"
        and "sexual_content" not in primary_cats
    ):
        result["secondary_category_id"] = main_id if main_id != "1.6" else secondary_id
        result["main_category_id"] = "1.6"
        main_id = "1.6"

    if (
        main_id not in {"1.6", "1.7", "2.1", "2.3", "10.1"}
        and gaze_hit
        and "sexual_content" not in primary_cats
        and register != "explicit"
        and any(w in blob for w in ("gaze", "stare", "smirk", "wink", "eye color", "eyes"))
    ):
        if appearance_hit:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "1.7"
            main_id = "1.7"
        elif main_id not in NON_OVERRIDABLE_CATEGORIES:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "1.7"
            main_id = "1.7"

    if (
        appearance_hit
        and main_id not in {"1.6", "1.7", "2.3", "10.1"}
        and "sexual_content" not in primary_cats
        and register != "explicit"
    ):
        if main_id in {"8.3", "4.2", "4.1", "2.1"}:
            result["secondary_category_id"] = main_id
        result["main_category_id"] = "1.6"
        main_id = "1.6"

    # Luxury / status de-bias: do not leave generic negotiation on 6.1
    if main_id == "6.1":
        has_elite_work = bool(ELITE_WORK_TERMS.intersection(tokens)) or any(
            w in blob for w in ("ceo", "executive", "business terms", "professional")
        )
        if not has_elite_work:
            if LUXURY_FASHION_TERMS.intersection(tokens) or "fashion" in blob:
                result["main_category_id"] = "6.6"
                main_id = "6.6"
            elif ARISTOCRACY_TERMS.intersection(tokens) or "historical" in topic_metadata.get("subgenre_hints", []):
                result["main_category_id"] = "6.7"
                main_id = "6.7"
            elif any(w in blob for w in ("hotel", "restaurant", "wedding", "party")):
                result["secondary_category_id"] = "6.1" if has_elite_work else secondary_id
                result["main_category_id"] = "8.2" if "hotel" in blob or "restaurant" in blob else "5.3"
                main_id = result["main_category_id"]

    if LUXURY_FASHION_TERMS.intersection(tokens) and main_id in {"8.3", "5.3", "4.2", "8.2"}:
        result["secondary_category_id"] = main_id if main_id != "6.6" else secondary_id
        result["main_category_id"] = "6.6"
        main_id = "6.6"

    if main_id in {"4.1", "4.2", "8.1", "8.3"}:
        if "wedding" in blob or "ceremony" in blob:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "5.3"
            main_id = "5.3"
        elif "hotel" in blob or "restaurant" in blob:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "8.2"
            main_id = "8.2"
        elif "fashion" in blob or "gown" in blob or "model" in blob:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "6.6"
            main_id = "6.6"

    if ARISTOCRACY_TERMS.intersection(tokens) and main_id in {"5.3", "4.4", "7.1"}:
        result["secondary_category_id"] = main_id
        result["main_category_id"] = "6.7"
        main_id = "6.7"

    # Stage 08 intimacy subtags → everyday intimacy & emotional safety routing
    intimacy_subtag_map = {
        "intimacy:courtship_ritual": "4.1",
        "intimacy:nonsexual_affection": "2.2",
        "intimacy:everyday_companionship": "4.2",
        "intimacy:domestic_care": "4.2",
        "intimacy:emotional_safety": "4.6",
    }
    for subtag, preferred_id in intimacy_subtag_map.items():
        if subtag not in secondary_cats:
            continue
        if main_id in {"2.3", "2.5", "4.7", "7.2", "7.4", "noise"}:
            break
        if main_id in {"8.1", "8.2", "8.3", "8.5"} and preferred_id in valid_ids:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = preferred_id
            main_id = preferred_id
            break
        if main_id == "4.2" and preferred_id == "4.6" and "intimacy:emotional_safety" in secondary_cats:
            result["secondary_category_id"] = "4.2"
            result["main_category_id"] = "4.6"
            main_id = "4.6"
            break

    # Work/social setting nudges (replaces obsolete work_or_school → 6.1 default)
    if (
        main_id not in NON_OVERRIDABLE_CATEGORIES
        and main_id not in {"6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "noise"}
    ):
        if "social_setting" in primary_cats and ELITE_WORK_TERMS.intersection(tokens):
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "6.1"
        elif "communication_medium" in primary_cats:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "8.3"
        elif "procedural_transition" in primary_cats:
            result["secondary_category_id"] = main_id
            result["main_category_id"] = "8.5"

    # H4: protective care vs jealousy/possessiveness
    has_violence = bool(VIOLENCE_TERMS.intersection(tokens)) or bool(VIOLENCE_TERMS.intersection(blob_tokens))
    jealousy_hit = (
        JEALOUSY_POSSESSIVE_TERMS.intersection(tokens)
        or JEALOUSY_POSSESSIVE_TERMS.intersection(blob_tokens)
        or any(w in blob for w in ("jealous", "possessive", "you're mine", "you are mine"))
    )
    protective_hit = (
        PROTECTIVE_CARE_TERMS.intersection(tokens)
        or PROTECTIVE_CARE_TERMS.intersection(blob_tokens)
        or any(w in blob for w in ("protect", "keep you safe", "vow to protect", "reassur"))
    )

    if jealousy_hit and main_id in {"4.4", "4.2", "3.2", "3.3", "2.1"} and not has_violence:
        result["secondary_category_id"] = main_id if main_id != "4.7" else secondary_id
        result["main_category_id"] = "4.7"
        main_id = "4.7"
    elif protective_hit and not jealousy_hit and main_id in {"4.5", "7.2", "7.3", "4.4"} and not has_violence:
        if main_id == "7.2" and "relationship_conflict" in primary_cats:
            result["secondary_category_id"] = "7.2"
            result["main_category_id"] = "4.6"
        elif main_id in {"7.3", "4.5", "4.4"}:
            result["secondary_category_id"] = main_id if main_id != "4.6" else secondary_id
            result["main_category_id"] = "4.6"
        main_id = result["main_category_id"]
        _append_mechanic_tag(result, "protective_care")

  # Forceful explicit sex without coercion evidence → mechanic tag, not 7.2/7.4
    if main_id == "2.3" and consent_status not in {"coercion_watchlist", "nonconsent_explicit"}:
        if FORCEFUL_INTENSITY_TERMS.intersection(tokens) or FORCEFUL_INTENSITY_TERMS.intersection(blob_tokens):
            _append_mechanic_tag(result, "forceful_intensity")
    if main_id in {"7.3", "7.2"} and protective_hit and not has_violence and not jealousy_hit:
        _append_mechanic_tag(result, "external_threat")

    if "pregnant" in blob or "pregnancy" in blob or "baby" in blob:
        if main_id == "5.1":
            _append_mechanic_tag(result, "pregnancy_future")

    if ELITE_WORK_TERMS.intersection(tokens) and main_id in {"6.1", "6.4"}:
        _append_mechanic_tag(result, "economic_power")

    if result.get("main_category_id") not in valid_ids:
        result["main_category_id"] = "4.2"
    if result.get("secondary_category_id") not in valid_ids:
        result["secondary_category_id"] = None

    cfg = load_taxonomy_config(path)
    exclude_ids = set(cfg.get("exclude_from_axes_ids", []))
    if result.get("use_in_macro_axes") is not None:
        result["exclude_from_axes"] = not bool(result.get("use_in_macro_axes"))
    elif result.get("main_category_id") in exclude_ids or topic_metadata.get("exclude_from_axes"):
        result["exclude_from_axes"] = True
    else:
        result.setdefault("exclude_from_axes", False)

    return result


def _append_mechanic_tag(result: Dict[str, Any], tag: str) -> None:
    if tag not in MECHANIC_TAG_ENUM:
        return
    tags = result.get("mechanic_tags")
    if not isinstance(tags, list):
        tags = []
    if tag not in tags and len(tags) < 5:
        tags.append(tag)
    result["mechanic_tags"] = tags


def enrich_with_category_names(
    result: Dict[str, Any],
    path: Optional[str] = None,
) -> Dict[str, Any]:
    by_id = taxonomy_by_id(path)

    def _info(cid: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        if cid is None:
            return None, None
        node = by_id.get(cid)
        if not node:
            return None, None
        return node.get("name"), node.get("group")

    main_id = result.get("main_category_id")
    sec_id = result.get("secondary_category_id")
    main_name, main_group = _info(main_id)
    sec_name, sec_group = _info(sec_id)

    result["main_category_name"] = main_name
    result["main_category_group"] = main_group
    result["secondary_category_name"] = sec_name
    result["secondary_category_group"] = sec_group

    other_ids = result.get("other_plausible_ids", [])
    if not isinstance(other_ids, list):
        other_ids = []

    result["other_plausible_categories"] = [
        {"id": cid, "name": by_id[cid].get("name"), "group": by_id[cid].get("group")}
        for cid in other_ids
        if isinstance(cid, str) and cid in by_id
    ]
    return result


def fallback_main_category(primary_categories: List[str]) -> str:
    if "sexual_content" in primary_categories:
        return "2.3"
    if "sexual_tension" in primary_categories:
        return "2.1"
    if "physical_affection" in primary_categories:
        return "2.2"
    if "appearance_presentation" in primary_categories:
        return "1.6"
    if "subgenre_paranormal" in primary_categories:
        return "10.1"
    if "subgenre_historical" in primary_categories:
        return "10.2"
    if "subgenre_suspense" in primary_categories:
        return "10.3"
    if "narrative_style" in primary_categories:
        return "9.1"
    if "social_setting" in primary_categories:
        return "8.2"
    if "domestic_life" in primary_categories:
        return "4.2"
    if "relationship_conflict" in primary_categories:
        return "4.4"
    if any(w in " ".join(primary_categories).lower() for w in ("jealous", "possess")):
        return "4.7"
    if any(w in " ".join(primary_categories).lower() for w in ("protect", "caretak")):
        return "4.6"
    if "procedural_transition" in primary_categories:
        return "8.5"
    if "communication_medium" in primary_categories:
        return "8.3"
    return "4.2"


def _make_result(
    topic_id: int,
    main_id: str,
    secondary_id: Optional[str],
    is_noise: bool,
    confidence: Any,
    rationale: str,
    by_id: Dict[str, Dict[str, str]],
    *,
    exclude_from_axes: bool,
    pre_routed: bool,
    content_type: str = "scene",
    use_in_macro_axes: Optional[bool] = None,
    use_in_theory_watchlist: Optional[bool] = None,
    noise_reason: Optional[str] = None,
    mechanic_tags: Optional[List[str]] = None,
    evidence_quality: str = "medium",
) -> Dict[str, Any]:
    from src.stage09_category_mapping.stage1_theory_driven_categories.prompts.taxonomy_mapping_schema import (
        band_to_confidence,
        confidence_to_band,
    )

    if isinstance(confidence, str):
        conf_num = band_to_confidence(confidence.lower())
        conf_band = confidence.lower() if confidence.lower() in {"low", "medium", "high"} else confidence_to_band(conf_num)
    else:
        try:
            conf_num = max(0.0, min(1.0, float(confidence)))
        except (TypeError, ValueError):
            conf_num = 0.6
        conf_band = confidence_to_band(conf_num)

    macro = use_in_macro_axes if use_in_macro_axes is not None else (not exclude_from_axes and not is_noise)
    watchlist = use_in_theory_watchlist if use_in_theory_watchlist is not None else (not is_noise)

    result: Dict[str, Any] = {
        "topic_id": topic_id,
        "content_type": content_type,
        "main_category_id": main_id,
        "secondary_category_id": secondary_id,
        "other_plausible_ids": [],
        "mechanic_tags": list(mechanic_tags or []),
        "is_noise": is_noise,
        "use_in_macro_axes": macro,
        "use_in_theory_watchlist": watchlist,
        "noise_reason": noise_reason,
        "confidence": conf_num,
        "confidence_band": conf_band,
        "evidence_quality": evidence_quality,
        "uncertainty_reason": None,
        "rationale": rationale,
        "exclude_from_axes": not macro,
        "pre_routed": pre_routed,
    }
    main_node = by_id.get(main_id, {})
    result["main_category_name"] = main_node.get("name")
    result["main_category_group"] = main_node.get("group")
    if secondary_id and secondary_id in by_id:
        result["secondary_category_name"] = by_id[secondary_id].get("name")
        result["secondary_category_group"] = by_id[secondary_id].get("group")
    else:
        result["secondary_category_name"] = None
        result["secondary_category_group"] = None
    result["other_plausible_categories"] = []
    return result
