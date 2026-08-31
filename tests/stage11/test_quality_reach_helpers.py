"""Unit tests for Stage 11 quality-vs-reach helpers (Notebook 16)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.stage11_refined_construct_analysis.analysis import presentation as pres


def _toy_frame(n: int = 120, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    authors = [f"a{i % 20}" for i in range(n)]
    genres = np.where(rng.random(n) > 0.5, "contemporary", "historical")
    feat = rng.normal(size=n)
    noise = rng.normal(scale=0.4, size=n)
    reliability = rng.uniform(0.2, 0.95, size=n)
    return pd.DataFrame(
        {
            "book_id": [f"b{i}" for i in range(n)],
            "author_id": authors,
            "genre_group": genres,
            "log_pages": rng.normal(5.0, 0.3, size=n),
            "n_sentences": rng.integers(2000, 8000, size=n).astype(float),
            "publication_year": rng.integers(2000, 2018, size=n).astype(float),
            "feat_good": feat,
            "feat_const": np.zeros(n),
            "feat_nan": np.full(n, np.nan),
            "rating_shrunk": 0.5 * feat + noise,
            "avg_rating": 0.4 * feat + noise + 0.05,
            "log_n_ratings": -0.2 * feat + rng.normal(scale=0.5, size=n) + 6.0,
            "reliability": reliability,
        }
    )


def test_standardized_two_channel_weights_quality_only(monkeypatch):
    """Quality path receives reliability weights; reach path does not."""
    calls = []

    class FakeFit:
        def __init__(self, name: str):
            self.name = name
            self.n_obs = 100
            self.n_clusters = 10
            self.coefficients = pd.DataFrame(
                [
                    {
                        "term": "feat_good__z",
                        "coefficient": 0.1,
                        "std_error": 0.02,
                        "p_value": 0.001,
                        "ci_low": 0.06,
                        "ci_high": 0.14,
                    }
                ]
            )

    def fake_fit_ols(frame, outcome, predictors, *, categorical=(), cluster=None, weights=None, name="ols"):
        calls.append({"outcome": outcome, "weights": weights, "cluster": cluster, "name": name})
        return FakeFit(name)

    import src.stage10_correlation_analysis.analysis.models as mdl

    monkeypatch.setattr(mdl, "fit_ols", fake_fit_ols)
    frame = _toy_frame()
    out = pres.standardized_two_channel_betas(frame, ["feat_good"])
    assert not out.empty
    assert set(out["channel"]) == {"quality", "reach"}
    q_calls = [c for c in calls if c["name"].endswith("->quality")]
    r_calls = [c for c in calls if c["name"].endswith("->reach")]
    assert len(q_calls) == 1 and q_calls[0]["weights"] == "reliability"
    assert len(r_calls) == 1 and r_calls[0]["weights"] is None
    assert all(c["cluster"] == "author_id" for c in calls)
    for col in ("beta_std", "se", "p", "ci_low", "ci_high", "n_obs", "n_clusters"):
        assert col in out.columns


def test_standardized_skips_constant_and_missing_features():
    frame = _toy_frame()
    out = pres.standardized_two_channel_betas(frame, ["feat_const", "feat_nan", "missing_col"])
    assert out.empty


def test_pivot_and_gap():
    long = pd.DataFrame(
        [
            {
                "feature": "f1",
                "channel": "quality",
                "beta_std": 0.2,
                "se": 0.05,
                "p": 0.01,
                "ci_low": 0.1,
                "ci_high": 0.3,
                "n_obs": 100,
                "n_clusters": 20,
            },
            {
                "feature": "f1",
                "channel": "reach",
                "beta_std": -0.05,
                "se": 0.04,
                "p": 0.2,
                "ci_low": -0.13,
                "ci_high": 0.03,
                "n_obs": 100,
                "n_clusters": 20,
            },
        ]
    )
    wide = pres.pivot_two_channel_betas(long)
    assert len(wide) == 1
    assert pytest.approx(wide.iloc[0]["beta_gap"], rel=1e-9) == 0.25
    assert pytest.approx(wide.iloc[0]["abs_beta_gap"], rel=1e-9) == 0.25


def test_flag_and_classify_patterns():
    wide = pd.DataFrame(
        [
            {
                "feature": "both",
                "quality_beta": 0.2,
                "quality_p": 0.001,
                "quality_ci_low": 0.1,
                "quality_ci_high": 0.3,
                "reach_beta": 0.15,
                "reach_p": 0.002,
                "reach_ci_low": 0.05,
                "reach_ci_high": 0.25,
            },
            {
                "feature": "q_only",
                "quality_beta": 0.2,
                "quality_p": 0.001,
                "quality_ci_low": 0.1,
                "quality_ci_high": 0.3,
                "reach_beta": 0.01,
                "reach_p": 0.8,
                "reach_ci_low": -0.05,
                "reach_ci_high": 0.07,
            },
            {
                "feature": "r_only",
                "quality_beta": 0.01,
                "quality_p": 0.7,
                "quality_ci_low": -0.04,
                "quality_ci_high": 0.06,
                "reach_beta": 0.2,
                "reach_p": 0.001,
                "reach_ci_low": 0.1,
                "reach_ci_high": 0.3,
            },
            {
                "feature": "opp",
                "quality_beta": 0.2,
                "quality_p": 0.001,
                "quality_ci_low": 0.1,
                "quality_ci_high": 0.3,
                "reach_beta": -0.2,
                "reach_p": 0.001,
                "reach_ci_low": -0.3,
                "reach_ci_high": -0.1,
            },
            {
                "feature": "none",
                "quality_beta": 0.01,
                "quality_p": 0.6,
                "quality_ci_low": -0.05,
                "quality_ci_high": 0.07,
                "reach_beta": -0.01,
                "reach_p": 0.5,
                "reach_ci_low": -0.06,
                "reach_ci_high": 0.04,
            },
        ]
    )
    flagged = pres.flag_channel_reliability(wide, alpha=0.05)
    patterns = flagged.apply(pres.classify_channel_pattern, axis=1).tolist()
    assert patterns == [
        "both_same_sign",
        "quality_only",
        "reach_only",
        "opposite_signs",
        "neither",
    ]


def test_unmeasurable_not_zero_placeholder():
    """Constant / absent features must be omitted, not returned as beta=0."""
    frame = _toy_frame()
    out = pres.standardized_two_channel_betas(frame, ["feat_const"])
    assert out.empty
    assert not ((out.get("beta_std") == 0).any() if not out.empty else False)
