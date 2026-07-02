"""Tests for Stage09 taxonomy mapping v2 schema and normalization."""

from __future__ import annotations

import pandas as pd

from src.stage09_category_mapping.stage1_theory_driven_categories.prompts.taxonomy_mapping_schema import (
    build_taxonomy_mapping_schema,
    normalize_taxonomy_mapping_result,
    taxonomy_id_enum,
)
from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    apply_domain_heuristics,
    axis_bearing_ids,
    build_composite_series,
    composite_index_spec,
    exploratory_only_ids,
    fallback_main_category,
    load_taxonomy_config,
    taxonomy_block_for_prompt,
    try_pre_route_taxonomy,
    valid_taxonomy_ids,
)


def test_v24_version():
    cfg = load_taxonomy_config(str(DEFAULT_TAXONOMY_PATH))
    assert cfg["version"] == "2.4"


def test_schema_includes_split_ids():
    schema = build_taxonomy_mapping_schema(str(DEFAULT_TAXONOMY_PATH))
    main_enum = schema["properties"]["main_category_id"]["enum"]
    for required in ("8.3a", "8.3b", "5.3a", "5.3b", "6.1a", "6.1b", "uncertain_interpretable"):
        assert required in main_enum
    assert "6.1" not in main_enum


def test_schema_includes_extended_yaml_ids():
    schema = build_taxonomy_mapping_schema(str(DEFAULT_TAXONOMY_PATH))
    main_enum = schema["properties"]["main_category_id"]["enum"]
    for required in ("2.5", "4.6", "7.4", "9.1", "10.1", "1.6", "noise"):
        assert required in main_enum


def test_schema_id_count_matches_yaml():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    enum_ids = set(taxonomy_id_enum(str(DEFAULT_TAXONOMY_PATH), include_noise=True))
    assert enum_ids == valid_ids


def test_taxonomy_block_includes_primary_or_secondary():
    block = taxonomy_block_for_prompt(str(DEFAULT_TAXONOMY_PATH))
    assert "primary" in block
    assert "secondary" in block
    assert "Boundary:" in block


def test_secondary_context_macro_off():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    raw = {
        "topic_id": 99,
        "content_type": "scene",
        "main_category_id": "8.2",
        "secondary_category_id": None,
        "other_plausible_ids": [],
        "mechanic_tags": [],
        "is_noise": False,
        "use_in_macro_axes": True,
        "use_in_theory_watchlist": True,
        "noise_reason": None,
        "confidence": 0.7,
        "evidence_quality": "medium",
        "uncertainty_reason": None,
        "rationale": "Restaurant setting topic.",
    }
    result = normalize_taxonomy_mapping_result(
        raw, topic_id=99, topic_metadata={}, valid_ids=valid_ids,
    )
    assert result["use_in_macro_axes"] is False
    assert result["exclude_from_axes"] is True


def test_discourse_normalization_macro_off_watchlist_on():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    raw = {
        "topic_id": 5,
        "content_type": "discourse",
        "main_category_id": "9.1",
        "secondary_category_id": None,
        "other_plausible_ids": [],
        "mechanic_tags": [],
        "is_noise": False,
        "use_in_macro_axes": True,
        "use_in_theory_watchlist": False,
        "noise_reason": None,
        "confidence": 0.8,
        "evidence_quality": "medium",
        "uncertainty_reason": None,
        "rationale": "Discourse topic.",
        "mapping_reasoning": "Evidence: speech-tag keywords dominate; no scene beat. Main 9.1 over 4.3 because content is delivery mechanics. macro_axes=false for discourse.",
    }
    meta = {"content_type": "discourse", "primary_categories": ["narrative_style"]}
    result = normalize_taxonomy_mapping_result(
        raw, topic_id=5, topic_metadata=meta, valid_ids=valid_ids,
    )
    assert result["use_in_macro_axes"] is False
    assert result["use_in_theory_watchlist"] is True
    assert result["exclude_from_axes"] is True


def test_noise_flags():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    raw = {
        "topic_id": 0,
        "content_type": "noise",
        "main_category_id": "noise",
        "secondary_category_id": None,
        "other_plausible_ids": [],
        "mechanic_tags": [],
        "is_noise": True,
        "use_in_macro_axes": True,
        "use_in_theory_watchlist": True,
        "noise_reason": "boilerplate",
        "confidence": 0.95,
        "evidence_quality": "high",
        "uncertainty_reason": None,
        "rationale": "Publisher boilerplate.",
        "mapping_reasoning": "Evidence: incoherent paratext fragments. Classified as noise; excluded from macro axes.",
    }
    result = normalize_taxonomy_mapping_result(
        raw, topic_id=0, topic_metadata={}, valid_ids=valid_ids,
    )
    assert result["main_category_id"] == "noise"
    assert result["use_in_macro_axes"] is False
    assert result["use_in_theory_watchlist"] is False
    assert result["exclude_from_axes"] is True


def test_schema_includes_mapping_reasoning():
    schema = build_taxonomy_mapping_schema(str(DEFAULT_TAXONOMY_PATH))
    assert "mapping_reasoning" in schema["properties"]
    assert "mapping_reasoning" in schema["required"]


def test_mapping_reasoning_defaults_from_rationale():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    raw = {
        "topic_id": 1,
        "content_type": "scene",
        "main_category_id": "4.2",
        "secondary_category_id": None,
        "other_plausible_ids": [],
        "mechanic_tags": [],
        "is_noise": False,
        "use_in_macro_axes": True,
        "use_in_theory_watchlist": True,
        "noise_reason": None,
        "confidence": 0.8,
        "evidence_quality": "high",
        "uncertainty_reason": None,
        "rationale": "Courtship bonding dominates.",
    }
    result = normalize_taxonomy_mapping_result(
        raw, topic_id=1, topic_metadata={}, valid_ids=valid_ids,
    )
    assert result["mapping_reasoning"] == "Courtship bonding dominates."


def test_mapping_debug_block_from_classifier():
    from src.stage09_category_mapping.stage1_theory_driven_categories.scripts.zeroshot_taxonomy_openrouter import (
        _attach_mapping_debug,
        _finalize_taxonomy_result,
        _snapshot_mapping_fields,
    )

    raw = {
        "topic_id": 118,
        "content_type": "scene",
        "main_category_id": "2.3",
        "secondary_category_id": "8.1",
        "other_plausible_ids": [],
        "mechanic_tags": [],
        "is_noise": False,
        "use_in_macro_axes": True,
        "use_in_theory_watchlist": True,
        "noise_reason": None,
        "confidence": 0.9,
        "evidence_quality": "high",
        "uncertainty_reason": None,
        "rationale": "Explicit sex is central.",
        "mapping_reasoning": "Snippets show explicit intercourse; main 2.3 over 8.1 setting.",
    }
    meta = {"rationale": "Stage08 says explicit bedroom scene."}
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    result = normalize_taxonomy_mapping_result(
        raw, topic_id=118, topic_metadata=meta, valid_ids=valid_ids,
    )
    snapshot = _snapshot_mapping_fields(result)
    result = _finalize_taxonomy_result(result, meta)
    result = _attach_mapping_debug(
        result,
        topic_metadata=meta,
        model_name="test-model",
        prompt_version="v2",
        classification_source="llm",
        llm_snapshot=snapshot,
    )
    assert "mapping_debug" in result
    assert result["mapping_debug"]["classification_source"] == "llm"
    assert result["mapping_debug"]["stage08_label_rationale"] == "Stage08 says explicit bedroom scene."
    assert result["mapping_reasoning"]


def test_mechanic_tags_capped():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    raw = {
        "topic_id": 9,
        "content_type": "scene",
        "main_category_id": "6.4",
        "secondary_category_id": None,
        "other_plausible_ids": [],
        "mechanic_tags": [
            "economic_power",
            "professional_hierarchy",
            "economic_power",
            "invalid_tag",
            "secret_misunderstanding",
            "trust_repair",
            "domestic_care",
        ],
        "is_noise": False,
        "use_in_macro_axes": True,
        "use_in_theory_watchlist": True,
        "noise_reason": None,
        "confidence": 0.7,
        "evidence_quality": "medium",
        "uncertainty_reason": None,
        "rationale": "Business deal topic.",
    }
    result = normalize_taxonomy_mapping_result(
        raw, topic_id=9, topic_metadata={}, valid_ids=valid_ids,
    )
    assert len(result["mechanic_tags"]) <= 5
    assert "invalid_tag" not in result["mechanic_tags"]
    assert "economic_power" in result["mechanic_tags"]


def test_pre_router_subgenre_macro_off():
    meta = {
        "is_noise": False,
        "content_type": "subgenre_marker",
        "primary_categories": ["subgenre_paranormal"],
        "exclude_from_axes": False,
        "keywords": ["growl", "instincts"],
    }
    result = try_pre_route_taxonomy(31, meta, str(DEFAULT_TAXONOMY_PATH))
    assert result is not None
    assert result["main_category_id"] == "10.1"
    assert result["content_type"] == "subgenre_marker"
    assert result["use_in_macro_axes"] is False
    assert result["use_in_theory_watchlist"] is True
    assert result["exclude_from_axes"] is True
    assert "confidence_band" in result


def test_composite_spec_shapes():
    wide = pd.DataFrame(
        {"4.2": [0.5], "4.6": [0.3], "2.2": [0.2], "8.1": [0.4], "8.2": [0.2]},
        index=[1],
    )
    ei_spec = composite_index_spec("everyday_intimacy_emotional_safety", str(DEFAULT_TAXONOMY_PATH))
    series = build_composite_series(wide, ei_spec)
    expected = 0.5 * 1.0 + 0.3 * 1.0 + 0.2 * 1.0
    assert abs(float(series.iloc[0]) - expected) < 1e-9
    assert "optional_low_weight_context" not in ei_spec or not ei_spec.get("optional_low_weight_context")


def test_coercion_watchlist_spec():
    spec = composite_index_spec("coercion_risk_watchlist", str(DEFAULT_TAXONOMY_PATH))
    assert spec is not None
    core_ids = set(spec.get("taxonomy_ids", []))
    assert core_ids == {"7.4", "7.2"}
    assert "4.7" in (spec.get("optional_low_weight_context") or [])


def test_status_power_excludes_precarity():
    spec = composite_index_spec("status_power", str(DEFAULT_TAXONOMY_PATH))
    ids = set(spec.get("taxonomy_ids", []))
    assert ids == {"6.1a", "6.6", "6.7"}
    assert "6.4" in (spec.get("exclude_taxonomy_ids") or [])


def test_sexual_lock_blocks_appearance_override():
    result = {
        "main_category_id": "2.1",
        "secondary_category_id": "1.1",
        "use_in_macro_axes": True,
        "mechanic_tags": [],
        "rationale": "Sexual tension from charged proximity.",
        "mapping_reasoning": "Primary is 2.1.",
    }
    meta = {
        "sexual_function": "sexual_tension",
        "consent_status": "consensual_implied",
        "keywords": ["forehead", "hair", "grasp", "flush"],
        "label": "Hot Breath Against Her Neck",
        "scene_summary": "His fingers move under her hair around her throat as hot breath grazes her neck.",
    }
    out = apply_domain_heuristics(result, meta, str(DEFAULT_TAXONOMY_PATH))
    assert out["main_category_id"] == "2.1"
    assert out["use_in_macro_axes"] is True


def test_axis_bearing_enforcement():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    for main_id in ("1.7", "8.5", "9.2", "uncertain_interpretable"):
        raw = {
            "topic_id": 1,
            "content_type": "scene",
            "main_category_id": main_id,
            "secondary_category_id": None,
            "other_plausible_ids": [],
            "mechanic_tags": [],
            "is_noise": False,
            "use_in_macro_axes": True,
            "use_in_theory_watchlist": True,
            "noise_reason": None,
            "confidence": 0.7,
            "evidence_quality": "medium",
            "uncertainty_reason": None,
            "rationale": "Context topic.",
        }
        result = normalize_taxonomy_mapping_result(
            raw, topic_id=1, topic_metadata={}, valid_ids=valid_ids,
        )
        assert result["use_in_macro_axes"] is False
        assert main_id not in axis_bearing_ids(str(DEFAULT_TAXONOMY_PATH))


def test_precarity_6_4_gate():
    result = {
        "main_category_id": "6.4",
        "secondary_category_id": None,
        "use_in_macro_axes": True,
        "mechanic_tags": [],
    }
    meta = {
        "keywords": ["terms", "percent", "deal", "contract", "partners"],
        "label": "Negotiating Terms and Deals",
        "scene_summary": "Characters discuss contract terms and payment percentages.",
    }
    out = apply_domain_heuristics(result, meta, str(DEFAULT_TAXONOMY_PATH))
    assert out["main_category_id"] in {"6.1b", "8.3b", "uncertain_interpretable"}


def test_wink_nonsexual_affection_stays_1_7():
    result = {
        "main_category_id": "1.7",
        "secondary_category_id": None,
        "use_in_macro_axes": False,
        "mechanic_tags": [],
        "evidence_quality": "medium",
        "rationale": "Wink is nonverbal cue.",
        "mapping_reasoning": "MAIN CATEGORY: 1.7",
    }
    meta = {
        "sexual_function": "nonsexual_affection",
        "consent_status": "not_applicable",
        "keywords": ["wink", "winked", "playful"],
        "label": "Playful Wink Across The Room",
        "scene_summary": "She gave him a playful wink across the room.",
    }
    out = apply_domain_heuristics(result, meta, str(DEFAULT_TAXONOMY_PATH))
    assert out["main_category_id"] == "1.7"


def test_love_confession_stays_4_5():
    result = {
        "main_category_id": "4.5",
        "secondary_category_id": "3.3",
        "use_in_macro_axes": True,
        "mechanic_tags": [],
        "evidence_quality": "high",
        "rationale": "Love confession after denial.",
        "mapping_reasoning": "MAIN CATEGORY: 4.5",
    }
    meta = {
        "sexual_function": "nonsexual_affection",
        "consent_status": "not_applicable",
        "keywords": ["love", "loved", "denial", "confession"],
        "label": "Admitting Love After Denial",
        "scene_summary": "I loved you the whole damn time, walling it up inside me.",
    }
    out = apply_domain_heuristics(result, meta, str(DEFAULT_TAXONOMY_PATH))
    assert out["main_category_id"] == "4.5"
    assert out["use_in_macro_axes"] is True


def test_generic_deal_routes_6_1b():
    result = {
        "main_category_id": "6.1a",
        "secondary_category_id": "8.3b",
        "use_in_macro_axes": True,
        "mechanic_tags": [],
        "evidence_quality": "medium",
    }
    meta = {
        "keywords": ["terms", "percent", "deal", "contract", "payment", "partners"],
        "label": "Negotiating A Deal With Payment",
        "scene_summary": "They discussed contract terms and payment percentages.",
    }
    out = apply_domain_heuristics(result, meta, str(DEFAULT_TAXONOMY_PATH))
    assert out["main_category_id"] == "6.1b"
    assert out["use_in_macro_axes"] is False


def test_elite_hero_routes_6_1a():
    result = {
        "main_category_id": "6.1b",
        "secondary_category_id": None,
        "use_in_macro_axes": False,
        "mechanic_tags": [],
        "evidence_quality": "high",
    }
    meta = {
        "keywords": ["billionaire", "ceo", "executive", "power"],
        "label": "Billionaire CEO Authority",
        "scene_summary": "The billionaire CEO commanded the boardroom with elite authority.",
    }
    out = apply_domain_heuristics(result, meta, str(DEFAULT_TAXONOMY_PATH))
    assert out["main_category_id"] == "6.1a"
    assert out["use_in_macro_axes"] is True


def test_3_3_not_axis_bearing():
    assert "3.3" in exploratory_only_ids(str(DEFAULT_TAXONOMY_PATH))
    assert "3.3" not in axis_bearing_ids(str(DEFAULT_TAXONOMY_PATH))


def test_fallback_uncertain():
    assert fallback_main_category([]) == "uncertain_interpretable"
    assert fallback_main_category(["domestic_life"]) == "8.1"


if __name__ == "__main__":
    test_v24_version()
    test_schema_includes_split_ids()
    test_schema_includes_extended_yaml_ids()
    test_schema_id_count_matches_yaml()
    test_taxonomy_block_includes_primary_or_secondary()
    test_secondary_context_macro_off()
    test_schema_includes_mapping_reasoning()
    test_mapping_reasoning_defaults_from_rationale()
    test_mapping_debug_block_from_classifier()
    test_noise_flags()
    test_mechanic_tags_capped()
    test_pre_router_subgenre_macro_off()
    test_composite_spec_shapes()
    test_coercion_watchlist_spec()
    test_status_power_excludes_precarity()
    test_sexual_lock_blocks_appearance_override()
    test_axis_bearing_enforcement()
    test_precarity_6_4_gate()
    test_wink_nonsexual_affection_stays_1_7()
    test_love_confession_stays_4_5()
    test_generic_deal_routes_6_1b()
    test_elite_hero_routes_6_1a()
    test_3_3_not_axis_bearing()
    test_fallback_uncertain()
    print("All taxonomy_mapping_v2_schema tests passed.")
