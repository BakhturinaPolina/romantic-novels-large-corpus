"""Tests for H3 manual freeze worksheet + master overrides."""

from __future__ import annotations

import json

import pandas as pd

from src.stage11_refined_construct_analysis.analysis.constructs import rax_for_code
from src.stage11_refined_construct_analysis.analysis.h3_manual_freeze import (
    apply_h3_manual_freeze_to_master,
    freeze_overrides,
    seed_decisions_worksheet,
    validate_h3_manual_freeze,
)
from src.stage11_refined_construct_analysis.analysis.master import build_W_tk
from src.stage11_refined_construct_analysis.config import DEFAULT_CONFIG_PATH, load_stage11_config

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)

H3_TOPIC_IDS = [
    29, 38, 45, 46, 56, 96, 128, 137, 141, 193, 240, 242, 247, 293, 299, 305, 307, 356,
    17, 112, 191, 18, 77, 171, 218, 253, 364, 22, 61, 65, 93, 140, 143, 167, 170, 174,
    190, 277, 315, 345, 351, 358,
]


def _filled_freeze(*, remove_ids=(38,), keep_overrides=None) -> dict:
    keep_overrides = keep_overrides or {}
    decisions = []
    for tid in H3_TOPIC_IDS:
        if tid in remove_ids:
            decisions.append(
                {
                    "topic_id": tid,
                    "decision": "REMOVE",
                    "final_code": "S0",
                    "relationship_directed": "no",
                    "function": "other",
                    "notes": "unit test remove",
                }
            )
        else:
            code = keep_overrides.get(tid, "S1")
            func = "emotional" if code.startswith("S") and code not in ("S8", "S9", "S13", "S10") else "other"
            if code == "S13":
                func = "appearance_status"
            decisions.append(
                {
                    "topic_id": tid,
                    "decision": "KEEP",
                    "final_code": code,
                    "relationship_directed": "yes",
                    "function": func,
                    "notes": "",
                }
            )
    return {"hypothesis": "H3", "frozen": True, "decisions": decisions}


def test_validate_blank_worksheet_fails():
    df = pd.DataFrame(
        {
            "topic_id": H3_TOPIC_IDS[:5],
            "current_topic_label": ["x"] * 5,
            "security_code": ["S1"] * 5,
        }
    )
    blank = seed_decisions_worksheet(df)
    errs = validate_h3_manual_freeze(blank, require_frozen=True)
    assert errs
    assert any("frozen" in e for e in errs)


def test_validate_filled_ok():
    data = _filled_freeze()
    assert validate_h3_manual_freeze(data, expected_ids=H3_TOPIC_IDS) == []


def test_freeze_overrides_remove_to_s0():
    data = _filled_freeze(remove_ids=(38, 45))
    ov = freeze_overrides(data)
    assert ov[38]["final_code"] == "S0"
    assert ov[38]["action_tag"] == "H3:HUMAN_REMOVE"
    assert ov[46]["decision"] == "KEEP"
    assert rax_for_code("S0") == []


def test_apply_remove_drops_from_strict_w_tk():
    """REMOVE → S0 excludes topic from RAX_emotional_security under strict W_tk."""
    master = pd.DataFrame(
        [
            {
                "topic_id": 38,
                "security_code": "S1",
                "intimacy_code": None,
                "hea_code": None,
                "care_protection_code": None,
                "darkness_code": None,
                "arc_role": None,
                "family_proportions_json": json.dumps({"H3": {"S1": 1.0}}),
                "adjudication_actions": [],
                "proposed_constructs": [],
                "current_taxonomy_id": "4.6",
            },
            {
                "topic_id": 46,
                "security_code": "S3",
                "intimacy_code": None,
                "hea_code": None,
                "care_protection_code": None,
                "darkness_code": None,
                "arc_role": None,
                "family_proportions_json": json.dumps({"H3": {"S3": 1.0}}),
                "adjudication_actions": [],
                "proposed_constructs": [],
                "current_taxonomy_id": "4.6",
            },
        ]
    )
    freeze = _filled_freeze(remove_ids=(38,), keep_overrides={46: "S3"})
    out = apply_h3_manual_freeze_to_master(master, CFG, freeze_data=freeze)
    assert out.loc[out.topic_id == 38, "security_code"].iloc[0] == "S0"
    assert out.loc[out.topic_id == 46, "security_code"].iloc[0] == "S3"
    actions38 = out.loc[out.topic_id == 38, "adjudication_actions"].iloc[0]
    assert "H3:HUMAN_REMOVE" in actions38

    w = build_W_tk(out, mode="strict", dominance=0.70)
    h3 = w[w["construct_family"] == "security"]
    assert 38 not in set(h3["topic_id"].tolist())
    assert 46 in set(h3["topic_id"].tolist())
    assert set(h3["construct_code"]) == {"S3"}


def test_apply_reassign_s2():
    master = pd.DataFrame(
        [
            {
                "topic_id": 170,
                "security_code": "S13",
                "intimacy_code": None,
                "hea_code": None,
                "care_protection_code": None,
                "darkness_code": None,
                "arc_role": None,
                "family_proportions_json": json.dumps({"H3": {"S13": 1.0}}),
                "adjudication_actions": [],
                "proposed_constructs": [],
                "current_taxonomy_id": "1.6",
            },
        ]
    )
    freeze = _filled_freeze(keep_overrides={170: "S2"})
    out = apply_h3_manual_freeze_to_master(master, CFG, freeze_data=freeze)
    assert out.loc[out.topic_id == 170, "security_code"].iloc[0] == "S2"
