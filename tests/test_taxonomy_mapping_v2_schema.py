"""Tests for Stage09 taxonomy mapping v2 schema and normalization."""

from __future__ import annotations

from src.stage09_category_mapping.stage2_theory_driven_categories.prompts.taxonomy_mapping_schema import (
    build_taxonomy_mapping_schema,
    normalize_taxonomy_mapping_result,
    taxonomy_id_enum,
)
from src.stage09_category_mapping.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    try_pre_route_taxonomy,
    valid_taxonomy_ids,
)


def test_schema_includes_extended_yaml_ids():
    schema = build_taxonomy_mapping_schema(str(DEFAULT_TAXONOMY_PATH))
    main_enum = schema["properties"]["main_category_id"]["enum"]
    for required in ("2.5", "4.6", "7.4", "9.1", "10.1", "1.6", "noise"):
        assert required in main_enum


def test_schema_id_count_matches_yaml():
    valid_ids = valid_taxonomy_ids(str(DEFAULT_TAXONOMY_PATH))
    enum_ids = set(taxonomy_id_enum(str(DEFAULT_TAXONOMY_PATH), include_noise=True))
    assert enum_ids == valid_ids


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
    }
    result = normalize_taxonomy_mapping_result(
        raw, topic_id=0, topic_metadata={}, valid_ids=valid_ids,
    )
    assert result["main_category_id"] == "noise"
    assert result["use_in_macro_axes"] is False
    assert result["use_in_theory_watchlist"] is False
    assert result["exclude_from_axes"] is True


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


def test_pre_router_populates_v2_fields():
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
    assert result["use_in_theory_watchlist"] is True
    assert "confidence_band" in result


if __name__ == "__main__":
    test_schema_includes_extended_yaml_ids()
    test_schema_id_count_matches_yaml()
    test_discourse_normalization_macro_off_watchlist_on()
    test_noise_flags()
    test_mechanic_tags_capped()
    test_pre_router_populates_v2_fields()
    print("All taxonomy_mapping_v2_schema tests passed.")
