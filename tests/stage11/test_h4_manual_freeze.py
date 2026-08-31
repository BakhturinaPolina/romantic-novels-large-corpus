"""Tests for H4 manual freeze worksheet + master overrides."""

from __future__ import annotations

import json

import pandas as pd

from src.stage11_refined_construct_analysis.analysis.constructs import rax_for_code
from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
    EXPECTED_TOPIC_IDS,
    apply_h4_manual_freeze_to_master,
    freeze_overrides,
    seed_decisions_worksheet,
    validate_h4_manual_freeze,
)
from src.stage11_refined_construct_analysis.analysis.master import build_W_tk
from src.stage11_refined_construct_analysis.config import DEFAULT_CONFIG_PATH, load_stage11_config

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def _filled_freeze(*, remove_ids=(68,), keep_code="H4_5") -> dict:
    decisions = []
    for tid in EXPECTED_TOPIC_IDS:
        if tid in remove_ids:
            decisions.append(
                {
                    "topic_id": tid,
                    "decision": "REMOVE",
                    "final_code": "H4_0",
                    "external_threat": "no",
                    "main_romantic_target": "yes",
                    "notes": "unit test remove",
                }
            )
        else:
            # Default keep under original bucket suggestion
            from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
                EXTERNAL_PROTECTION_IDS,
                POSSESSION_CONTROL_IDS,
                PROTECTIVE_COMMITMENT_IDS,
            )

            if tid in EXTERNAL_PROTECTION_IDS:
                code = "H4_5"
            elif tid in PROTECTIVE_COMMITMENT_IDS:
                code = "H4_5a"
            else:
                code = "H4_7"
            decisions.append(
                {
                    "topic_id": tid,
                    "decision": "KEEP",
                    "final_code": code if tid not in remove_ids else keep_code,
                    "external_threat": "yes" if code in ("H4_5", "H4_6") else "no",
                    "main_romantic_target": "yes",
                    "notes": "",
                }
            )
    return {"hypothesis": "H4", "frozen": True, "decisions": decisions}


def test_validate_blank_worksheet_fails():
    df = pd.DataFrame(
        {
            "topic_id": list(EXPECTED_TOPIC_IDS),
            "current_topic_label": ["x"] * len(EXPECTED_TOPIC_IDS),
            "care_protection_code": ["H4_5"] * len(EXPECTED_TOPIC_IDS),
        }
    )
    blank = seed_decisions_worksheet(df)
    errs = validate_h4_manual_freeze(blank, require_frozen=True)
    assert errs
    assert any("frozen" in e for e in errs)


def test_validate_filled_ok():
    data = _filled_freeze()
    assert validate_h4_manual_freeze(data) == []


def test_freeze_overrides_remove_to_h4_0():
    data = _filled_freeze(remove_ids=(68, 78))
    ov = freeze_overrides(data)
    assert ov[68]["final_code"] == "H4_0"
    assert ov[68]["action_tag"] == "H4:HUMAN_REMOVE"
    assert ov[87]["decision"] == "KEEP"
    assert rax_for_code("H4_0") == []


def test_select_diversified_prefers_all_cells_and_books():
    from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
        select_diversified_sentences,
    )

    raw = []
    # 4 cells × 3 books × short+long
    for cell_i, cell in enumerate(["CELL_A", "CELL_B", "CELL_C", "CELL_D"]):
        for b in range(3):
            raw.append(
                {
                    "cell": cell,
                    "book_id_anon": f"BOOK_{cell_i * 10 + b:03d}",
                    "sentence": "x" * 10,
                    "chapter_index": 1,
                    "sentence_index": b,
                    "sid": f"{cell}_{b}_short",
                    "max_topic_prob": 0.5,
                }
            )
            raw.append(
                {
                    "cell": cell,
                    "book_id_anon": f"BOOK_{cell_i * 10 + b:03d}",
                    "sentence": ("Longer narrative sentence about protection. " * 3).strip(),
                    "chapter_index": 1,
                    "sentence_index": b + 10,
                    "sid": f"{cell}_{b}_long",
                    "max_topic_prob": 0.9,
                }
            )
    # Extra low-rated pile (like topic 68 CELL_B flood)
    for i in range(20):
        raw.append(
            {
                "cell": "CELL_B",
                "book_id_anon": "BOOK_001",
                "sentence": f"Flood short {i}.",
                "chapter_index": 2,
                "sentence_index": i,
                "sid": f"flood_{i}",
                "max_topic_prob": 0.99,
            }
        )

    selected, meta = select_diversified_sentences(raw, per_cell=2, max_total=12)
    cells = {s["cell"] for s in selected}
    books = {s["book_id_anon"] for s in selected}
    assert cells == {"CELL_A", "CELL_B", "CELL_C", "CELL_D"}
    assert len(books) >= 6
    assert 8 <= meta["n_selected"] <= 12
    # Prefer longer: most selected should be the long variants
    longish = sum(1 for s in selected if len(s["sentence"]) >= 55)
    assert longish >= 6
    # CELL_B flood from one book must not dominate
    assert sum(1 for s in selected if s["book_id_anon"] == "BOOK_001") <= 2


def test_apply_remove_drops_from_strict_w_tk():
    """REMOVE → H4_0 excludes topic from RAX_external_protection under strict W_tk."""
    master = pd.DataFrame(
        [
            {
                "topic_id": 68,
                "care_protection_code": "H4_5",
                "intimacy_code": None,
                "hea_code": None,
                "security_code": None,
                "darkness_code": None,
                "arc_role": None,
                "family_proportions_json": json.dumps({"H4": {"H4_5": 1.0}}),
                "adjudication_actions": [],
                "proposed_constructs": [],
                "current_taxonomy_id": "4.7",
            },
            {
                "topic_id": 87,
                "care_protection_code": "H4_5",
                "intimacy_code": None,
                "hea_code": None,
                "security_code": None,
                "darkness_code": None,
                "arc_role": None,
                "family_proportions_json": json.dumps({"H4": {"H4_5": 1.0}}),
                "adjudication_actions": [],
                "proposed_constructs": [],
                "current_taxonomy_id": "4.7",
            },
        ]
    )
    freeze = _filled_freeze(remove_ids=(68,))
    out = apply_h4_manual_freeze_to_master(master, CFG, freeze_data=freeze)
    assert out.loc[out.topic_id == 68, "care_protection_code"].iloc[0] == "H4_0"
    assert out.loc[out.topic_id == 87, "care_protection_code"].iloc[0] == "H4_5"
    actions68 = out.loc[out.topic_id == 68, "adjudication_actions"].iloc[0]
    assert "H4:HUMAN_REMOVE" in actions68

    w = build_W_tk(out, mode="strict", dominance=0.70)
    h4 = w[w["construct_family"] == "care_protection"]
    assert 68 not in set(h4["topic_id"].tolist())
    assert 87 in set(h4["topic_id"].tolist())
    assert set(h4["construct_code"]) == {"H4_5"}
