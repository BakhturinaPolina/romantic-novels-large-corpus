"""Compositional transforms: CLR, log-ratio, epsilon, share invariants."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.stage10_correlation_analysis.analysis import compositional as comp


def make_shares() -> pd.DataFrame:
    frame = pd.DataFrame({
        "leaf_a": [0.5, 0.1, 0.34],
        "leaf_b": [0.3, 0.2, 0.33],
        "leaf_c": [0.2, 0.7, 0.33],
    })
    return frame.div(frame.sum(axis=1), axis=0)


def test_clr_rows_sum_to_zero():
    """CLR subtracts the row mean of the logs, so each row must sum to zero."""
    result = comp.clr(make_shares(), epsilon=1e-6)
    assert np.allclose(result.sum(axis=1), 0.0, atol=1e-10)


def test_clr_is_scale_invariant():
    """Doubling every part is the same composition, so CLR must not change."""
    shares = make_shares()
    a = comp.clr(shares, epsilon=0.0)
    b = comp.clr(shares * 2.0, epsilon=0.0)
    assert np.allclose(a.to_numpy(), b.to_numpy(), atol=1e-10)


def test_clr_rejects_negative_input():
    with pytest.raises(ValueError):
        comp.clr(pd.DataFrame({"x": [-0.1], "y": [1.1]}), epsilon=1e-6)


def test_log_ratio_is_antisymmetric():
    """Swapping numerator and denominator must flip the sign exactly."""
    shares = make_shares()
    forward = comp.log_ratio(shares, ["leaf_a"], ["leaf_c"], epsilon=1e-9)
    reverse = comp.log_ratio(shares, ["leaf_c"], ["leaf_a"], epsilon=1e-9)
    assert np.allclose(forward.to_numpy(), -reverse.to_numpy(), atol=1e-6)


def test_log_ratio_known_value():
    shares = pd.DataFrame({"leaf_a": [0.6], "leaf_b": [0.2], "leaf_c": [0.2]})
    value = float(comp.log_ratio(shares, ["leaf_a"], ["leaf_b", "leaf_c"], epsilon=0.0).iloc[0])
    assert value == pytest.approx(np.log(0.6 / 0.4))


def test_log_ratio_missing_column_raises_when_strict():
    with pytest.raises(KeyError):
        comp.log_ratio(make_shares(), ["leaf_a"], ["leaf_missing"], epsilon=1e-6)


def test_epsilon_is_half_a_sentence():
    """eps = 1/(2N): half of the smallest share a book of N sentences can express."""
    eps = comp.epsilon_from_counts(pd.Series([1000, 2000, 3000]))
    assert eps == pytest.approx(1.0 / (2 * 2000))


def test_epsilon_falls_back_when_mode_is_fixed():
    assert comp.epsilon_from_counts(pd.Series([100]), mode="fixed", fallback=1e-4) == 1e-4


def test_check_share_sums_accepts_valid_composition():
    assert comp.check_share_sums(make_shares(), name="test") < 1e-9


def test_check_share_sums_rejects_broken_composition():
    broken = pd.DataFrame({"a": [0.5], "b": [0.2]})
    with pytest.raises(AssertionError):
        comp.check_share_sums(broken, name="broken")


def test_zscore_handles_constant_column():
    """A constant column must become zeros, not NaN, or it silently poisons a model."""
    result = comp.zscore(pd.Series([2.0, 2.0, 2.0]))
    assert (result == 0.0).all()


def test_residualise_removes_the_shared_component():
    """H4 residualises 4.6 on 4.5; the residual must be orthogonal to the covariate."""
    rng = np.random.default_rng(0)
    shared = pd.Series(rng.normal(size=200))
    target = 2.0 * shared + pd.Series(rng.normal(scale=0.1, size=200))
    resid = comp.residualise(target, pd.DataFrame({"shared": shared}))
    assert abs(float(np.corrcoef(resid, shared)[0, 1])) < 1e-8


def test_screen_columns_marks_rare_and_tiny_parts():
    frame = pd.DataFrame({
        "common": [0.2] * 100,
        "rare": [0.0] * 98 + [0.5, 0.5],
        "tiny": [1e-6] * 100,
    })
    table = comp.screen_columns(frame, min_prevalence=0.05, min_mean_share=1e-3)
    assert bool(table.loc["common", "passes_screen"])
    assert not bool(table.loc["rare", "passes_prevalence"])
    assert not bool(table.loc["tiny", "passes_mean_share"])


def test_add_missing_columns_makes_absent_leaves_explicit():
    frame = pd.DataFrame({"leaf_a": [1.0]})
    out = comp.add_missing_columns(frame, ["leaf_a", "leaf_b"])
    assert list(out.columns) == ["leaf_a", "leaf_b"]
    assert float(out["leaf_b"].iloc[0]) == 0.0
