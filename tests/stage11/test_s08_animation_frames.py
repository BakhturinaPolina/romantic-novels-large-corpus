"""Tests for S08 animation frame SVG viewport stability."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from src.stage11_refined_construct_analysis.analysis.presentation_suite.paths import default_paths
from src.stage11_refined_construct_analysis.analysis.presentation_suite.slide_data import prepare_component_effects
from src.stage11_refined_construct_analysis.analysis.presentation_suite.slide_plots import export_component_animation_steps


@pytest.fixture(scope="module")
def paths():
    p = default_paths()
    if not (p.analysis / "13_final_statistical_tests" / "tables").exists():
        pytest.skip("Stage 11 results not present")
    p.ensure_deck_dirs()
    return p


def _svg_viewbox(svg_path: Path) -> tuple[str, str] | None:
    text = svg_path.read_text(encoding="utf-8")
    m = re.search(r'viewBox="([^"]+)"', text)
    if m:
        parts = m.group(1).split()
        if len(parts) == 4:
            return parts[2], parts[3]
    try:
        root = ET.fromstring(text)
        vb = root.get("viewBox")
        if vb:
            parts = vb.split()
            return parts[2], parts[3]
    except ET.ParseError:
        pass
    return None


def test_s08_animation_frames_share_viewbox(paths):
    df = prepare_component_effects(paths)
    export_component_animation_steps(df, paths, mode="chart_only")
    svgs = sorted(paths.deck_figures.glob("slide08_step*.svg"))
    if len(svgs) < 2:
        pytest.skip("No S08 animation frames generated (check animation_sequence.csv)")
    viewboxes = [_svg_viewbox(p) for p in svgs]
    assert all(vb is not None for vb in viewboxes), "Missing viewBox on animation SVG"
    first = viewboxes[0]
    for vb in viewboxes[1:]:
        assert abs(float(vb[0]) - float(first[0])) < 0.01, f"ViewBox width mismatch: {first} vs {vb}"
        assert abs(float(vb[1]) - float(first[1])) < 0.01, f"ViewBox height mismatch: {first} vs {vb}"
