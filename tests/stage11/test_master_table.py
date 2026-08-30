"""Master annotation table and family-specific W_tk tests."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from src.stage11_refined_construct_analysis.analysis.constructs import (
    normalize_code,
    rax_for_code,
)
from src.stage11_refined_construct_analysis.analysis.master import (
    build_W_tk,
    build_master_annotations,
    write_master_artifacts,
)
from src.stage11_refined_construct_analysis.audits.runner import audit_dir
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def _seed_minimal_audits():
    """Write tiny dry-run style adjudication so master builder has input."""
    for hyp, code, field in (
        ("H1", "I3", "intimacy_code"),
        ("H2", "H2_1", "hea_code"),
        ("H3", "S5", "security_code"),
        ("H4", "H4_1", "care_protection_code"),
        ("H5", "D1", "darkness_code"),
        ("H6", "ARC_2", "arc_role"),
    ):
        d = audit_dir(CFG, hyp)
        d.mkdir(parents=True, exist_ok=True)
        for pass_name, fname in (
            ("A", "lexical.jsonl"),
            ("B", "contextual.jsonl"),
            ("C", "adjudication.jsonl"),
        ):
            row = {
                "topic_id": 1,
                "hypothesis": hyp,
                "pass": pass_name,
                "code": code,
                "dry_run": True,
                "response": {
                    "consensus_code": code,
                    "dominant_code": code,
                    field: code,
                    "action": "KEEP",
                    "proportions": {code: 0.8},
                    "main_couple": True,
                    "proposed_constructs": [code],
                },
            }
            path = d / fname
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            if '"topic_id": 1' in existing or '"topic_id":1' in existing:
                continue
            with path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row) + "\n")


def test_master_builder_smoke():
    if not CFG.input_path("topic_lookup") or not CFG.input_path("topic_lookup").exists():
        pytest.skip("lookup missing")
    _seed_minimal_audits()
    master = build_master_annotations(CFG)
    assert len(master) >= 1
    assert "intimacy_code" in master.columns
    assert "arc_role" in master.columns
    assert "family_proportions_json" in master.columns
    w = build_W_tk(master, mode="strict")
    assert not w.empty
    paths = write_master_artifacts(CFG)
    assert paths["master"].exists()
    assert paths["freeze"].exists()
    freeze = json.loads(paths["freeze"].read_text(encoding="utf-8"))
    assert freeze["frozen"] is True
    assert freeze.get("weight_design") == "family_specific_v2"


def test_h6_arc_mapping():
    assert "RAX_arc_falling" in rax_for_code("ARC_4")
    assert "RAX_arc_rising" in rax_for_code("ARC_8")
    assert "RAX_external_plot_conflict" in rax_for_code("ARC_9")
    assert normalize_code("DISCLOSURE") == "ARC_5"
    assert normalize_code("EXTERNAL_PLOT_CONFLICT") == "ARC_9"


def test_h3_h4_mapping():
    assert rax_for_code("S13") == ["RAX_appearance_grooming"]
    assert rax_for_code("S12") == ["RAX_status_display"]
    assert rax_for_code("S15") == ["RAX_workplace_status"]
    assert rax_for_code("S10") == ["RAX_economic_dependency"]
    assert rax_for_code("S11") == ["RAX_practical_care"]
    assert rax_for_code("S14") == ["RAX_gift_romance_token"]
    assert rax_for_code("H4_4") == ["RAX_emotional_reassurance"]
    assert rax_for_code("H4_5") == ["RAX_external_protection"]
    assert normalize_code("CLAIMING") == "H4_7"
    assert normalize_code("JEALOUSY") == "H4_8"


def _synthetic_master() -> pd.DataFrame:
    """Two topics: one with cross-family share asymmetry; one mixed H1."""
    # Topic 61-like: H2 strong, H3 mixed/weak
    row_a = {
        "topic_id": 61,
        "intimacy_code": "MIXED",
        "hea_code": "H2_6",
        "security_code": "S4",
        "care_protection_code": None,
        "darkness_code": None,
        "arc_role": None,
        "current_taxonomy_id": "8.3a",
        "proposed_constructs": [],
        "family_proportions_json": json.dumps(
            {
                "H1": {"I0": 0.55, "I3": 0.45},  # I0 off-target filtered
                "H2": {"H2_6": 0.95},
                "H3": {"S1": 0.40, "S4": 0.35},  # no dominant ≥0.70
            }
        ),
        "review_status": "audited",
    }
    # Topic with multi-code H1 weighted
    row_b = {
        "topic_id": 7,
        "intimacy_code": "I3",
        "hea_code": None,
        "security_code": None,
        "care_protection_code": None,
        "darkness_code": None,
        "arc_role": None,
        "current_taxonomy_id": "2.3",
        "proposed_constructs": [],
        "family_proportions_json": json.dumps(
            {"H1": {"I3": 0.65, "I6": 0.35}}
        ),
        "review_status": "audited",
    }
    # Darkness anchor leaf
    row_c = {
        "topic_id": 99,
        "intimacy_code": None,
        "hea_code": None,
        "security_code": None,
        "care_protection_code": None,
        "darkness_code": None,
        "arc_role": None,
        "current_taxonomy_id": "7.2",
        "proposed_constructs": [],
        "family_proportions_json": json.dumps({}),
        "review_status": "unaudited",
    }
    # H1 tenderness bridge candidate
    row_d = {
        "topic_id": 50,
        "intimacy_code": "I2",
        "hea_code": None,
        "security_code": None,
        "care_protection_code": None,
        "darkness_code": None,
        "arc_role": None,
        "current_taxonomy_id": "4.6",
        "proposed_constructs": [],
        "family_proportions_json": json.dumps({"H1": {"I2": 0.80}}),
        "review_status": "audited",
    }
    return pd.DataFrame([row_a, row_b, row_c, row_d])


def test_strict_no_cross_family_leakage():
    master = _synthetic_master()
    w = build_W_tk(master, mode="strict", dominance=0.70)
    # Topic 61: H2_6 should be in; S4 should NOT (share 0.35 < 0.70)
    t61 = w[w["topic_id"] == 61]
    assert (t61["construct_code"] == "H2_6").any()
    assert not (t61["construct_code"] == "S4").any()
    # Topic 7: primary I3 at 0.65 < 0.70 → excluded in strict
    t7 = w[w["topic_id"] == 7]
    assert t7[t7["construct_family"] == "intimacy"].empty


def test_weighted_retains_full_proportions():
    master = _synthetic_master()
    w = build_W_tk(master, mode="weighted")
    t7 = w[(w["topic_id"] == 7) & (w["construct_family"] == "intimacy")]
    codes = dict(zip(t7["construct_code"], t7["weight"]))
    assert abs(codes.get("I3", 0) - 0.65) < 1e-9
    assert abs(codes.get("I6", 0) - 0.35) < 1e-9


def test_inclusive_adds_secondary():
    master = _synthetic_master()
    w = build_W_tk(master, mode="inclusive")
    t7 = w[(w["topic_id"] == 7) & (w["construct_family"] == "intimacy")]
    codes = dict(zip(t7["construct_code"], t7["weight"]))
    assert codes.get("I3") == 1.0
    assert codes.get("I6") == 0.5  # secondary at inclusive weight


def test_h5_darkness_and_tenderness_bridge():
    master = _synthetic_master()
    w = build_W_tk(master, mode="strict", dominance=0.70)
    # Leaf 7.2 → D1 darkness bridge
    t99 = w[w["topic_id"] == 99]
    assert (t99["construct_code"] == "D1").any()
    # I2 with share 0.80 → D5 tenderness bridge
    t50 = w[w["topic_id"] == 50]
    assert (t50["construct_code"] == "D5").any()
    assert (t50["construct_code"] == "I2").any()


def test_strict_excludes_below_threshold_no_audited_fallback():
    master = pd.DataFrame(
        [
            {
                "topic_id": 25,
                "intimacy_code": "I0",
                "hea_code": None,
                "security_code": None,
                "care_protection_code": None,
                "darkness_code": None,
                "arc_role": None,
                "current_taxonomy_id": "1.1",
                "proposed_constructs": [],
                "family_proportions_json": json.dumps({"H1": {"I0": 0.60}}),
                "review_status": "audited",
            }
        ]
    )
    w = build_W_tk(master, mode="strict", dominance=0.70)
    # I0 is off-target; audited fallback must NOT force weight 1
    assert w[w["topic_id"] == 25].empty or not (
        w[(w["topic_id"] == 25) & (w["construct_family"] == "intimacy")].shape[0] > 0
        and (w[(w["topic_id"] == 25)]["weight"] == 1.0).all()
        and (w[(w["topic_id"] == 25)]["construct_code"] == "I0").any()
    )
    assert not (w["construct_code"] == "I0").any()
