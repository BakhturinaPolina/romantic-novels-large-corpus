"""Tests and multiplicity corrections, checked against statsmodels where possible."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.stage10_correlation_analysis.analysis import tests as st


def test_benjamini_hochberg_matches_statsmodels():
    from statsmodels.stats.multitest import multipletests

    rng = np.random.default_rng(1)
    p = np.concatenate([rng.uniform(0, 0.01, 20), rng.uniform(0, 1, 80)])
    expected = multipletests(p, method="fdr_bh")[1]
    assert np.allclose(st.benjamini_hochberg(p), expected)


def test_holm_matches_statsmodels():
    from statsmodels.stats.multitest import multipletests

    rng = np.random.default_rng(2)
    p = rng.uniform(0, 1, 50)
    expected = multipletests(p, method="holm")[1]
    assert np.allclose(st.holm(p), expected)


def test_adjusted_p_values_are_never_smaller_than_raw():
    rng = np.random.default_rng(3)
    p = rng.uniform(0, 1, 200)
    assert (st.benjamini_hochberg(p) >= p - 1e-12).all()
    assert (st.holm(p) >= p - 1e-12).all()


def test_holm_is_at_least_as_conservative_as_bh():
    """Familywise control cannot be looser than false-discovery-rate control."""
    rng = np.random.default_rng(4)
    p = rng.uniform(0, 0.2, 100)
    assert (st.holm(p) >= st.benjamini_hochberg(p) - 1e-12).all()


def test_corrections_preserve_nan_positions():
    p = np.array([0.01, np.nan, 0.5])
    for fn in (st.holm, st.benjamini_hochberg):
        out = fn(p)
        assert np.isnan(out[1])
        assert np.isfinite(out[0]) and np.isfinite(out[2])


def test_kruskal_wallis_finds_a_real_tier_difference():
    rng = np.random.default_rng(5)
    frame = pd.DataFrame({
        "tier": np.repeat(["low", "mid", "high"], 200),
        "separated": np.concatenate([rng.normal(i, 0.5, 200) for i in range(3)]),
        "flat": rng.normal(0, 1, 600),
    })
    result = st.kruskal_wallis(frame, ["separated", "flat"], "tier", ["low", "mid", "high"])
    separated = result.set_index("feature").loc["separated"]
    flat = result.set_index("feature").loc["flat"]
    assert separated["p_value"] < 1e-10
    assert separated["epsilon_squared"] > flat["epsilon_squared"]


def test_kruskal_wallis_handles_a_constant_feature():
    """A constant column must not blow up; scipy raises on identical inputs."""
    frame = pd.DataFrame({"tier": ["a"] * 10 + ["b"] * 10, "const": [1.0] * 20})
    result = st.kruskal_wallis(frame, ["const"], "tier", ["a", "b"])
    assert float(result.loc[0, "p_value"]) == 1.0


def test_pairwise_mann_whitney_applies_holm_within_feature():
    rng = np.random.default_rng(6)
    frame = pd.DataFrame({
        "tier": np.repeat(["low", "mid", "high"], 150),
        "value": np.concatenate([rng.normal(i * 0.5, 1, 150) for i in range(3)]),
    })
    result = st.pairwise_mann_whitney(
        frame, ["value"], "tier",
        [("high", "low"), ("high", "mid"), ("mid", "low")],
    )
    assert len(result) == 3
    assert (result["p_holm_within_feature"] >= result["p_value"] - 1e-12).all()


def test_adjust_within_family_corrects_families_separately():
    """A large family must not consume the alpha budget of a small one."""
    frame = pd.DataFrame({
        "family": ["topic"] * 300 + ["hypothesis"] * 6,
        "p_value": list(np.linspace(0.001, 0.9, 300)) + [0.04] * 6,
    })
    pooled = st.adjust_within_family(frame, family_column=None)
    split = st.adjust_within_family(frame, family_column="family")

    hypothesis_pooled = pooled[pooled["family"] == "hypothesis"]["q_value"].max()
    hypothesis_split = split[split["family"] == "hypothesis"]["q_value"].max()
    assert hypothesis_split < hypothesis_pooled


def test_screening_funnel_counts_decrease_monotonically():
    screen = pd.DataFrame(
        {"passes_screen": [True, True, False, True]},
        index=["topic_1", "topic_2", "topic_3", "topic_4"],
    )
    effects_table = pd.DataFrame({
        "feature": ["topic_1", "topic_2", "topic_3", "topic_4"],
        "cliffs_delta": [0.45, 0.02, 0.60, 0.15],
        "ci_excludes_zero": [True, False, True, True],
        "q_value": [0.001, 0.9, 0.001, 0.2],
    })
    funnel, annotated = st.screening_funnel(
        screen, effects_table, min_abs_delta=0.11, alpha=0.05,
    )
    counts = funnel["n"].to_numpy()
    assert (np.diff(counts) <= 0).all()
    # topic_1 alone clears prevalence, FDR, effect size and the CI.
    assert annotated.set_index("feature").loc["topic_1", "passes_all"]
    assert not annotated.set_index("feature").loc["topic_3", "passes_all"]  # fails prevalence


def test_compare_tier_trend_detects_monotone_rise():
    rng = np.random.default_rng(8)
    frame = pd.DataFrame({
        "tier": np.repeat(["low", "mid", "high"], 200),
        "rising": np.concatenate([rng.normal(i, 0.4, 200) for i in range(3)]),
    })
    result = st.compare_tier_trend(frame, ["rising"], "tier", ["low", "mid", "high"])
    assert float(result.loc[0, "spearman_rho"]) > 0.5
    assert result.loc[0, "direction"] == "rises with rating"
