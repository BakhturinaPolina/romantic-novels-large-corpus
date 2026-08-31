"""Tests for H3 material-provision spillover discovery."""

from __future__ import annotations

import pytest

from src.stage11_refined_construct_analysis.audits.spillover import (
    _h3_material_should_promote,
    _load_already_material_topic_ids,
    build_h3_spillover_candidates,
)
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import (
    build_all_manifests,
    load_topic_lookup,
)


CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def test_h3_material_promote_rule():
    assert _h3_material_should_promote(
        {
            "relationship_directed_transfer": "yes",
            "provision_function": "money_provision",
            "promote_to_full_H3_audit": False,
        }
    )
    assert _h3_material_should_promote(
        {
            "relationship_directed_transfer": "unclear",
            "provision_function": "housing_provision",
            "promote_to_full_H3_audit": False,
        }
    )
    assert _h3_material_should_promote(
        {
            "relationship_directed_transfer": "no",
            "provision_function": "off_target",
            "promote_to_full_H3_audit": True,
        }
    )
    assert not _h3_material_should_promote(
        {
            "relationship_directed_transfer": "yes",
            "provision_function": "status_luxury_display",
            "promote_to_full_H3_audit": False,
        }
    )
    assert not _h3_material_should_promote(
        {
            "relationship_directed_transfer": "yes",
            "provision_function": "workplace_status",
            "promote_to_full_H3_audit": False,
        }
    )
    assert not _h3_material_should_promote(
        {
            "relationship_directed_transfer": "yes",
            "provision_function": "gift_token",
            "promote_to_full_H3_audit": False,
        }
    )
    assert not _h3_material_should_promote(
        {
            "relationship_directed_transfer": "yes",
            "provision_function": "economic_dependency",
            "promote_to_full_H3_audit": False,
        }
    )


def test_build_h3_spillover_candidates_seeds():
    if not CFG.input_path("topic_lookup") or not CFG.input_path("topic_lookup").exists():
        pytest.skip("lookup missing")
    manifests = build_all_manifests(CFG)
    lookup = load_topic_lookup(CFG)
    man = manifests["hypotheses"]["H3"]
    cands = build_h3_spillover_candidates(CFG, lookup, man)
    ids = {c["topic_id"] for c in cands}

    # Already-strict material (topic 17) must be excluded from triage bill.
    already = _load_already_material_topic_ids(CFG)
    assert 17 in already or not already  # coverage may be absent in bare CI
    assert 17 not in ids

    # Known material / economic seeds outside pure appearance.
    assert 22 in ids, "expected seed 22 (payment/debts) in H3 material spillover candidates"
    # 191 may already be in construct coverage (excluded from triage bill) after audits.
    if 191 not in already:
        assert 191 in ids, "expected seed 191 in H3 material spillover candidates"

    # Job topic may appear via leaf/tag but is not auto-promoted by the rule.
    # Cap and source.
    assert len(cands) <= 40
    assert all(c.get("source") == "h3_full_corpus_material_discovery" for c in cands)

    # Appearance leaf 1.6 must not be a discovery signal by itself:
    # topics whose only signal would be primary_leaf=1.6 should not appear.
    for c in cands:
        notes = str(c.get("heuristic_notes") or "")
        if "primary_leaf=1.6" in notes and "secondary_leaf=" not in notes:
            # Must have mechanic or proto beyond the forbidden leaf (1.6 not in discovery).
            assert "primary_leaf=1.6" not in notes


def test_h3_spillover_prompt_frozen():
    from src.stage11_refined_construct_analysis.audits.spillover import load_spillover_prompt

    prompt = load_spillover_prompt(CFG, "H3")
    assert prompt.get("frozen") is True
    assert prompt.get("hypothesis") == "H3"
    assert "h3_spillover_triage" in str(prompt.get("name", ""))
