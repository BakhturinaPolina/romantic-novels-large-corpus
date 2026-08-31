"""Tests for H4 spillover discovery, H4_5a codes, and hypothesis-aware verdicts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.stage11_refined_construct_analysis.analysis.constructs import (
    COMPOSITE_DEFS,
    H5_TENDERNESS_H4_CODES,
    normalize_code,
    rax_for_code,
)
from src.stage11_refined_construct_analysis.analysis.notebook_helpers import (
    gated_verdict,
    verdict,
)
from src.stage11_refined_construct_analysis.audits.spillover import (
    _h4_should_promote,
    build_h4_spillover_candidates,
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


def test_normalize_h4_5a():
    assert normalize_code("H4_5a") == "H4_5a"
    assert normalize_code("H4_5A") == "H4_5a"
    assert normalize_code("PROTECTIVE_COMMITMENT") == "H4_5a"
    assert rax_for_code("H4_5a") == ["RAX_protective_commitment"]
    assert rax_for_code("H4_5") == ["RAX_external_protection"]
    assert "RAX_protective_commitment" in COMPOSITE_DEFS["RAX_protective_care_broad"]
    assert COMPOSITE_DEFS["RAX_h4_protection_side"] == ["RAX_external_protection"]
    assert "H4_2" not in H5_TENDERNESS_H4_CODES
    assert "H4_5a" not in H5_TENDERNESS_H4_CODES


def test_gated_verdict_expected_sign():
    assert (
        gated_verdict(-0.15, -0.20, -0.10, expected_sign=+1, measurement_gate="viable")
        == "contradicted"
    )
    assert (
        gated_verdict(0.15, 0.10, 0.20, expected_sign=+1, measurement_gate="viable")
        == "supported"
    )
    assert (
        gated_verdict(0.05, 0.01, 0.09, expected_sign=+1, measurement_gate="viable")
        == "directionally consistent, effect below threshold"
    )
    assert (
        gated_verdict(0.15, 0.10, 0.20, expected_sign=+1, measurement_gate="thin")
        == "thin:supported"
    )
    assert verdict(0.15, 0.10, 0.20) == "clears_gate"  # unsigned fallback


def test_h4_promote_rule():
    assert _h4_should_promote(
        {
            "external_threat": "yes",
            "protective_action": "unclear",
            "function": "off_target",
            "promote_to_full_H4_audit": False,
        }
    )
    assert _h4_should_promote(
        {
            "external_threat": "no",
            "protective_action": "no",
            "function": "protective_commitment",
            "promote_to_full_H4_audit": False,
        }
    )
    assert not _h4_should_promote(
        {
            "external_threat": "no",
            "protective_action": "no",
            "function": "emotional_reassurance",
            "promote_to_full_H4_audit": False,
        }
    )


def test_build_h4_spillover_candidates_seeds():
    if not CFG.input_path("topic_lookup") or not CFG.input_path("topic_lookup").exists():
        pytest.skip("lookup missing")
    manifests = build_all_manifests(CFG)
    lookup = load_topic_lookup(CFG)
    man = manifests["hypotheses"]["H4"]
    cands = build_h4_spillover_candidates(CFG, lookup, man)
    ids = {c["topic_id"] for c in cands}
    # Mandatory 4.6/4.7 must not appear
    mandatory = {
        int(e["topic_id"])
        for e in man["entries"]
        if e.get("role") == "mandatory"
    }
    assert ids.isdisjoint(mandatory)
    # Known external-danger / protection seeds outside 4.6/4.7
    for seed in (223, 324, 335, 327, 184, 284, 100):
        assert seed in ids, f"expected seed {seed} in H4 spillover candidates"
    assert len(cands) <= 80
