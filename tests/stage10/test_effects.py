"""Effect sizes checked against values computable by hand or by brute force."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.stage10_correlation_analysis.analysis import effects


def brute_force_cliffs_delta(a, b) -> float:
    """The textbook double loop. Slow, obviously correct, and the reference here."""
    a_arr, b_arr = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    greater = sum(1 for x in a_arr for y in b_arr if x > y)
    less = sum(1 for x in a_arr for y in b_arr if x < y)
    return (greater - less) / (a_arr.size * b_arr.size)


def test_cliffs_delta_complete_separation():
    """Every A above every B is delta = +1 by definition."""
    assert effects.cliffs_delta([4, 5, 6], [1, 2, 3]) == pytest.approx(1.0)
    assert effects.cliffs_delta([1, 2, 3], [4, 5, 6]) == pytest.approx(-1.0)


def test_cliffs_delta_identical_groups_is_zero():
    assert effects.cliffs_delta([1, 2, 3], [1, 2, 3]) == pytest.approx(0.0)


def test_cliffs_delta_known_fixture():
    """Hand-checked: of the 9 pairs, 3 favour A, 5 favour B and one ties, so delta = -2/9."""
    a, b = [1, 3, 5], [2, 4, 5]
    assert effects.cliffs_delta(a, b) == pytest.approx(-2.0 / 9.0)


def test_cliffs_delta_matches_brute_force_with_ties():
    """The rank-sum shortcut must agree with the double loop, ties included."""
    rng = np.random.default_rng(7)
    for _ in range(20):
        a = rng.integers(0, 6, size=25).astype(float)
        b = rng.integers(0, 6, size=18).astype(float)
        assert effects.cliffs_delta(a, b) == pytest.approx(brute_force_cliffs_delta(a, b))


def test_cliffs_delta_matches_mann_whitney_u():
    """Cliff's delta is a linear function of U; check the identity directly."""
    from scipy.stats import mannwhitneyu

    rng = np.random.default_rng(11)
    a = rng.normal(0.5, 1, 200)
    b = rng.normal(0.0, 1, 180)
    u = mannwhitneyu(a, b, alternative="two-sided").statistic
    expected = 2.0 * u / (a.size * b.size) - 1.0
    assert effects.cliffs_delta(a, b) == pytest.approx(expected)


def test_magnitude_bands_match_romano_thresholds():
    assert effects.magnitude(0.05) == "negligible"
    assert effects.magnitude(0.20) == "small"
    assert effects.magnitude(0.35) == "medium"
    assert effects.magnitude(0.60) == "large"


def test_cliffs_delta_rejects_empty_group():
    with pytest.raises(ValueError):
        effects.cliffs_delta([], [1, 2, 3])


def test_epsilon_squared_zero_when_groups_identical():
    groups = [[1, 2, 3, 4]] * 3
    assert effects.epsilon_squared(groups) == pytest.approx(0.0, abs=1e-9)


def test_epsilon_squared_reaches_its_ceiling_when_groups_separate():
    """Three fully separated equal groups top out near 8/9, not 1 — the k=3 ceiling."""
    groups = [list(range(0, 20)), list(range(100, 120)), list(range(200, 220))]
    assert effects.epsilon_squared(groups) == pytest.approx(8 / 9, abs=0.02)


def test_epsilon_squared_ceiling_rises_with_more_groups():
    """The ceiling is (k-1)/k-ish, so values are only comparable at a fixed group count."""
    three = effects.epsilon_squared([list(range(i * 100, i * 100 + 20)) for i in range(3)])
    six = effects.epsilon_squared([list(range(i * 100, i * 100 + 20)) for i in range(6)])
    assert six > three


def test_hodges_lehmann_recovers_a_known_shift():
    rng = np.random.default_rng(3)
    base = rng.normal(0, 1, 400)
    shifted = base + 2.5
    assert effects.hodges_lehmann(shifted, base) == pytest.approx(2.5, abs=0.2)


def test_fast_bootstrap_ci_agrees_with_the_point_estimate():
    rng = np.random.default_rng(5)
    a, b = rng.normal(0.4, 1, 300), rng.normal(0, 1, 300)
    estimate, low, high = effects.fast_bootstrap_ci(a, b, n_replicates=400, seed=1)
    assert estimate == pytest.approx(effects.cliffs_delta(a, b))
    assert low < estimate < high


def test_fast_bootstrap_ci_brackets_a_real_difference():
    """A genuine shift must produce an interval that excludes zero."""
    rng = np.random.default_rng(9)
    a, b = rng.normal(1.0, 1, 400), rng.normal(0.0, 1, 400)
    _, low, high = effects.fast_bootstrap_ci(a, b, n_replicates=400, seed=2)
    assert low > 0 and high > 0


def test_fast_bootstrap_ci_includes_zero_for_a_null_difference():
    rng = np.random.default_rng(13)
    a, b = rng.normal(0, 1, 400), rng.normal(0, 1, 400)
    _, low, high = effects.fast_bootstrap_ci(a, b, n_replicates=600, seed=3)
    assert low < 0 < high


def test_bca_and_percentile_intervals_are_close_for_symmetric_data():
    rng = np.random.default_rng(17)
    a, b = rng.normal(0.3, 1, 60), rng.normal(0, 1, 60)
    _, bca_low, bca_high = effects.bootstrap_ci(a, b, n_replicates=300, seed=4, bca=True)
    _, pct_low, pct_high = effects.bootstrap_ci(a, b, n_replicates=300, seed=4, bca=False)
    assert abs(bca_low - pct_low) < 0.25
    assert abs(bca_high - pct_high) < 0.25


def test_two_group_effects_sign_convention():
    """Positive delta must mean group_a is the higher group."""
    frame = pd.DataFrame({
        "tier": ["high"] * 50 + ["low"] * 50,
        "share": list(np.linspace(0.5, 1.0, 50)) + list(np.linspace(0.0, 0.5, 50)),
    })
    result = effects.two_group_effects(
        frame, ["share"], "tier", "high", "low", n_replicates=200,
    )
    assert float(result.loc[0, "cliffs_delta"]) > 0.9
    assert bool(result.loc[0, "ci_excludes_zero"])


def test_multi_group_effects_orders_by_separation():
    rng = np.random.default_rng(21)
    frame = pd.DataFrame({
        "tier": np.repeat(["a", "b", "c"], 100),
        "separated": np.concatenate([rng.normal(i, 0.3, 100) for i in range(3)]),
        "flat": rng.normal(0, 1, 300),
    })
    result = effects.multi_group_effects(frame, ["separated", "flat"], "tier", ["a", "b", "c"])
    assert result.iloc[0]["feature"] == "separated"
    assert result.iloc[0]["epsilon_squared"] > result.iloc[1]["epsilon_squared"]
