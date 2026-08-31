"""Tests for Stage 11 presentation suite metadata and outputs."""

from __future__ import annotations

import pytest

from src.stage11_refined_construct_analysis.analysis.presentation_suite.evidence_metadata import (
    COMPONENT_FOCUS,
    build_all_metadata,
)
from src.stage11_refined_construct_analysis.analysis.presentation_suite.paths import default_paths
from src.stage11_refined_construct_analysis.analysis.presentation_suite.validate_presentation_data import (
    EXPECTED_FIGURES,
    assert_provenance_vs_sources,
    validate_frames,
    validate_outputs,
)


@pytest.fixture(scope="module")
def paths():
    p = default_paths()
    if not (p.analysis / "13_final_statistical_tests" / "tables").exists():
        pytest.skip("Stage 11 results not present")
    return p


@pytest.fixture(scope="module")
def frames(paths):
    return build_all_metadata(paths, write=False)


def test_all_hypotheses_present(frames):
    primary = frames["presentation_primary_results"]
    assert list(primary["hypothesis"]) == ["H1", "H2", "H3", "H4", "H5", "H6"]


def test_h2_h3_unmeasurable_not_zero(frames):
    primary = frames["presentation_primary_results"].set_index("hypothesis")
    for h in ("H2", "H3"):
        assert primary.loc[h, "measurement_status"] == "unmeasurable"
        assert primary.loc[h, "effect_size"] != primary.loc[h, "effect_size"]  # NaN


def test_h4_thin_not_unmeasurable(frames):
    primary = frames["presentation_primary_results"].set_index("hypothesis")
    assert primary.loc["H4", "measurement_status"] == "thin"
    assert primary.loc["H4", "effect_size"] == primary.loc["H4", "effect_size"]  # not NaN
    assert "primary ratio unmeasurable" not in str(primary.loc["H4", "one_sentence"]).lower()


def test_agreement_percentages(frames):
    ag = frames["presentation_agreement"]
    for _, r in ag.iterrows():
        assert abs(r["agreement_pct"] - 100.0 * r["n_agree"] / r["n_total"]) < 1e-6


def test_validate_frames_clean(frames):
    errors = validate_frames(frames)
    assert errors == []


def test_provenance_vs_sources(paths, frames):
    errors = assert_provenance_vs_sources(paths, frames)
    assert errors == [], errors


def test_external_protection_thin(frames):
    comp = frames["presentation_component_results"].set_index("feature")
    assert comp.loc["RAX_external_protection", "measurement_status"] == "thin"
    assert int(comp.loc["RAX_external_protection", "n_topics"]) == 1


def test_h1_adjusted_disagreement_flagged(frames):
    primary = frames["presentation_primary_results"].set_index("hypothesis")
    assert primary.loc["H1", "effect_size"] > 0
    assert primary.loc["H1", "adjusted_coefficient"] < 0
    assert primary.loc["H1", "adjusted_sign_aligned"] is False or primary.loc["H1", "adjusted_sign_aligned"] == False


def test_focal_components_present(frames):
    comp = set(frames["presentation_component_results"]["feature"])
    for feat in COMPONENT_FOCUS:
        assert feat in comp, feat


def test_figures_exist_if_built(paths):
    # Soft check: if suite has been built, all expected stems exist
    built = list(paths.out_dir.glob("fig01_contextual_agreement.png"))
    if not built:
        pytest.skip("Presentation figures not built yet")
    errors = validate_outputs(paths)
    assert errors == [], errors
    for stem in EXPECTED_FIGURES:
        assert (paths.out_dir / f"{stem}.png").exists()
        assert (paths.out_dir / f"{stem}.pdf").exists()
