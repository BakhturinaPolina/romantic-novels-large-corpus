"""Axis construction from the frozen schema.

The failure this file exists to prevent: an axis whose components have no topics being
emitted as a column of exactly 0.0, which then looks like a real variable in a regression
table. That happened in the previous run to four axes.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.stage10_correlation_analysis.analysis import axes as ax
from src.stage10_correlation_analysis.analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_analysis_config,
)


@pytest.fixture(scope="module")
def cfg():
    return load_analysis_config(DEFAULT_CONFIG_PATH)


@pytest.fixture(scope="module")
def specs(cfg):
    schema = ax.load_axis_schema(cfg.input_path("axis_schema", required=True))
    composites = ax.load_composites(cfg.input_path("taxonomy_config", required=True))
    additional = cfg.section("axes", "additional", default={})
    return ax.resolve_axes(schema, composites, additional=additional)


def test_every_confirmatory_axis_resolves(specs):
    confirmatory = [n for n, s in specs.items() if s.hypothesis_role == "confirmatory"]
    assert len(confirmatory) >= 8
    for name in confirmatory:
        spec = specs[name]
        assert spec.leaf_weights or spec.product_factors or spec.ratio_numerator, (
            f"{name} resolved to nothing"
        )


def test_deprecated_alias_is_not_resolved(specs):
    assert "AX_external_obstacle" not in specs


def test_segment_level_axis_is_excluded_from_book_level(specs):
    """The narrative-arc axis is tertile-level by construction; arc.py owns it."""
    assert "AX_narrative_arc_repair" not in specs


def test_h3_reframe_is_present_and_avoids_luxury_leaves(specs):
    """The reframed H3 axis must rest only on leaves that carry topics in this model."""
    spec = specs["AX_material_social_display"]
    assert set(spec.leaf_weights) == {"1.6", "8.2", "5.3a", "8.3a"}
    assert not {"6.1a", "6.6", "6.7"} & set(spec.leaf_weights)
    assert "H3" in spec.hypothesis


def test_difference_axis_has_signed_weights(specs):
    """AX_love_over_sex is payoff leaves minus explicit sex, so 2.3 must be negative."""
    weights = specs["AX_love_over_sex"].leaf_weights
    assert weights["2.3"] < 0
    assert weights["4.5"] > 0


def test_dark_vs_tender_signs_match_the_hypothesis(specs):
    weights = specs["AX_dark_vs_tender"].leaf_weights
    for dark in ("3.2", "4.4", "7.2", "7.3"):
        assert weights[dark] > 0, f"{dark} should load positively on darkness"
    for tender in ("2.2", "4.6", "3.1"):
        assert weights[tender] < 0, f"{tender} should load negatively on darkness"


def test_hea_index_uses_the_schema_weights(specs):
    weights = specs["AX_hea_index"].leaf_weights
    assert weights == pytest.approx({"4.5": 1.0, "5.3a": 0.8, "8.3a": 0.5})


def test_composite_backed_axis_picks_up_taxonomy_weights(specs):
    """AX_luxury_composite comes from the taxonomy composite block, weights included."""
    weights = specs["AX_luxury_composite"].leaf_weights
    assert weights["6.6"] == pytest.approx(1.0)
    assert weights["5.3a"] == pytest.approx(0.3)
    assert weights["8.2"] == pytest.approx(0.3)


def test_interaction_axis_names_its_factors(specs):
    spec = specs["AX_material_display_x_payoff"]
    assert spec.method == "product"
    assert spec.product_factors == ["AX_material_social_display", "AX_payoff_safety"]


def test_all_referenced_leaves_are_valid_taxonomy_ids(specs, cfg):
    """A typo in the schema must not silently create an unbuildable component."""
    from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
        valid_taxonomy_ids,
    )

    valid = set(valid_taxonomy_ids())
    for name, spec in specs.items():
        for leaf in spec.leaf_weights:
            assert leaf in valid, f"{name} references unknown taxonomy id {leaf!r}"


def test_coverage_audit_flags_empty_and_weak_components(specs):
    counts = {leaf: 5 for spec in specs.values() for leaf in spec.leaf_weights}
    counts["3.1"] = 0      # empty by design in this model
    counts["5.3a"] = 1     # a single topic
    mass = {leaf: 0.01 for leaf in counts}

    coverage = ax.audit_coverage(specs, counts, mass, viable_min_topics=3, weak_min_topics=1)
    by_leaf = dict(zip(zip(coverage["axis"], coverage["leaf_id"]), coverage["verdict"]))
    assert by_leaf[("AX_payoff_safety", "3.1")] == "empty"
    assert by_leaf[("AX_hea_index", "5.3a")] == "weak"
    assert by_leaf[("AX_hea_index", "4.5")] == "viable"

    summary = ax.summarise_coverage(coverage)
    assert summary.set_index("axis").loc["AX_hea_index", "axis_verdict"] == "weak"


def test_build_axis_values_raises_rather_than_emitting_zeros():
    """The whole point: no measurable component means no column, not a zero column."""
    spec = ax.AxisSpec(
        name="AX_test", method="weighted_sum", hypothesis=["H9"],
        hypothesis_role="confirmatory", axis_type="evaluative", description="",
        leaf_weights={"9.9": 1.0},
    )
    leaf_shares = pd.DataFrame({"leaf_4.5": [0.1, 0.2, 0.3]})
    with pytest.raises(ax.AxisConstructionError, match="no measurable component"):
        ax.build_axis_values(leaf_shares, {"AX_test": spec}, fail_on_empty_component=True)


def test_build_axis_values_can_skip_an_empty_axis_when_told_to():
    spec = ax.AxisSpec(
        name="AX_test", method="weighted_sum", hypothesis=[],
        hypothesis_role="exploratory", axis_type="evaluative", description="",
        leaf_weights={"9.9": 1.0},
    )
    other = ax.AxisSpec(
        name="AX_real", method="weighted_sum", hypothesis=[],
        hypothesis_role="exploratory", axis_type="evaluative", description="",
        leaf_weights={"4.5": 1.0},
    )
    leaf_shares = pd.DataFrame({"leaf_4.5": [0.1, 0.2, 0.3]})
    result = ax.build_axis_values(
        leaf_shares, {"AX_test": spec, "AX_real": other},
        fail_on_empty_component=True, allow_empty_axes=["AX_test"],
    )
    assert list(result.columns) == ["AX_real"]
    assert "AX_test" in result.attrs["skipped_axes"]


def test_build_axis_values_computes_the_signed_sum():
    spec = ax.AxisSpec(
        name="AX_diff", method="difference", hypothesis=[],
        hypothesis_role="confirmatory", axis_type="evaluative", description="",
        leaf_weights={"4.5": 1.0, "2.3": -1.0},
    )
    leaf_shares = pd.DataFrame({"leaf_4.5": [0.30, 0.10], "leaf_2.3": [0.05, 0.25]})
    result = ax.build_axis_values(leaf_shares, {"AX_diff": spec})
    assert result["AX_diff"].tolist() == pytest.approx([0.25, -0.15])


def test_interaction_is_centred_before_multiplying():
    """An uncentred product is mostly a proxy for the larger factor, not an interaction."""
    a = ax.AxisSpec("AX_a", "weighted_sum", [], "exploratory", "evaluative", "", {"4.5": 1.0})
    b = ax.AxisSpec("AX_b", "weighted_sum", [], "exploratory", "evaluative", "", {"2.3": 1.0})
    prod = ax.AxisSpec("AX_ab", "product", [], "confirmatory", "evaluative", "",
                       product_factors=["AX_a", "AX_b"])
    leaf_shares = pd.DataFrame({
        "leaf_4.5": [0.1, 0.2, 0.3, 0.4],
        "leaf_2.3": [0.4, 0.3, 0.2, 0.1],
    })
    result = ax.build_axis_values(leaf_shares, {"AX_a": a, "AX_b": b, "AX_ab": prod})
    assert result["AX_ab"].mean() == pytest.approx(
        float(((leaf_shares["leaf_4.5"] - 0.25) * (leaf_shares["leaf_2.3"] - 0.25)).mean())
    )


def test_constant_axis_is_rejected():
    spec = ax.AxisSpec("AX_const", "weighted_sum", [], "exploratory", "evaluative", "", {"4.5": 1.0})
    leaf_shares = pd.DataFrame({"leaf_4.5": [0.2, 0.2, 0.2]})
    with pytest.raises(ax.AxisConstructionError, match="constant"):
        ax.build_axis_values(leaf_shares, {"AX_const": spec})


def test_leaf_weight_table_is_readable(specs):
    table = ax.leaf_weight_table(specs)
    assert set(["axis", "method", "definition", "hypothesis", "role"]).issubset(table.columns)
    love = table.set_index("axis").loc["AX_love_over_sex", "definition"]
    assert "-1*2.3" in love
