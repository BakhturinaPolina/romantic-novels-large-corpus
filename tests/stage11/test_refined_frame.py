"""Tests for refined analysis frame builder."""

from __future__ import annotations

import pytest

from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code, rax_for_code
from src.stage11_refined_construct_analysis.analysis.frame import build_refined_frame, write_refined_frame
from src.stage11_refined_construct_analysis.config import DEFAULT_CONFIG_PATH, load_stage11_config

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def test_normalize_code_aliases():
    assert normalize_code("I3") == "I3"
    assert normalize_code("HEA") == "H2_5"
    assert normalize_code("PROTECT") == "H4_5"
    assert normalize_code("Conflict") == "ARC_2"
    assert normalize_code("UNKNOWN") is None
    assert normalize_code("MIXED") is None


def test_rax_for_code():
    assert "RAX_explicit_sex" in rax_for_code("I6")
    assert "RAX_final_relational_payoff" in rax_for_code("HEA")
    assert "RAX_arc_falling" in rax_for_code("Conflict")


def test_build_refined_frame_smoke():
    w = CFG.output_path("constructs_dir") / "W_tk_strict.parquet"
    frame_path = CFG.input_path("analysis_frame")
    if not w.exists() or frame_path is None or not frame_path.exists():
        pytest.skip("weights or stage10 frame missing")
    frame = build_refined_frame(CFG, mode="strict")
    assert len(frame) > 1000
    assert "rating_shrunk" in frame.columns
    # At least some RAX columns present
    rax = [c for c in frame.columns if c.startswith("RAX_")]
    assert len(rax) >= 5


def test_write_refined_frame():
    w = CFG.output_path("constructs_dir") / "W_tk_strict.parquet"
    if not w.exists():
        pytest.skip("weights missing")
    paths = write_refined_frame(CFG)
    assert paths["primary"].exists()
    assert paths["weighted"].exists()
    assert paths["manifest"].exists()
