"""Invariants on the prepared Stage10 tables.

These run against the real outputs and are skipped when they have not been built yet, so a
fresh clone still gets a green test run. They are the last line of defence against a data
problem reaching the notebooks: shares that do not sum to 1, a book losing its metadata, or
an axis coming out constant.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.stage10_correlation_analysis.analysis import compositional as comp
from src.stage10_correlation_analysis.analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_analysis_config,
)

CFG = load_analysis_config(DEFAULT_CONFIG_PATH)


def require(path: Path) -> Path:
    if path is None or not path.exists():
        pytest.skip(f"{path} not built yet; run the data_preparation scripts first")
    return path


@pytest.fixture(scope="module")
def book_topic_counts():
    path = require(CFG.output_path("hard_counts_dir") / "book_topic_counts.parquet")
    return pd.read_parquet(path)


@pytest.fixture(scope="module")
def frame():
    return pd.read_parquet(require(CFG.output_path("analysis_frame"))).set_index("book_id")


def test_hard_book_shares_sum_to_one(book_topic_counts):
    sums = book_topic_counts.groupby("book_id")["share"].sum()
    assert float((sums - 1.0).abs().max()) < 1e-9


def test_outlier_topic_is_excluded_from_shares(book_topic_counts):
    outlier = int(CFG.section("measurement", "outlier_topic_id"))
    if CFG.section("measurement", "drop_outlier_from_shares"):
        assert outlier not in set(book_topic_counts["topic_id"].unique())


def test_tertile_shares_sum_to_one_within_each_tertile():
    path = require(CFG.output_path("hard_counts_dir") / "tertile_topic_counts.parquet")
    tertiles = pd.read_parquet(path, columns=["book_id", "tertile", "share"])
    sums = tertiles.groupby(["book_id", "tertile"])["share"].sum()
    assert float((sums - 1.0).abs().max()) < 1e-9
    assert set(tertiles["tertile"].unique()) == {"begin", "middle", "end"}


def test_hard_assignments_carry_more_between_book_signal_than_soft():
    """The measurement decision, re-checked: hard counts must vary far more across books."""
    path = require(CFG.output_path("hard_counts_dir") / "hard_vs_soft_variance.parquet")
    table = pd.read_parquet(path).set_index("measure")
    if "soft_probability" not in table.index:
        pytest.skip("soft probability tables absent")
    assert table.loc["hard_assignment", "median_cv"] > 5 * table.loc["soft_probability", "median_cv"]


def test_analysis_frame_has_one_row_per_book(frame):
    assert frame.index.is_unique
    assert len(frame) > 15_000


def test_topic_shares_in_the_frame_are_a_composition(frame):
    topic_cols = [c for c in frame.columns if c.startswith("topic_")]
    assert len(topic_cols) > 300
    comp.check_share_sums(frame[topic_cols], name="frame topic shares", tolerance=1e-6)


def test_leaf_shares_are_a_composition_for_analysable_books(frame):
    """Leaf shares are conditional on interpretable mass, so they only apply where some exists."""
    leaf_cols = [c for c in frame.columns if c.startswith("leaf_")]
    usable = frame[frame["analysable"]]
    comp.check_share_sums(usable[leaf_cols], name="frame leaf shares", tolerance=1e-6)


def test_almost_every_book_is_analysable(frame):
    """A book with no interpretable sentence is expected to be a rarity, not a pattern."""
    assert float(frame["analysable"].mean()) > 0.999


def test_no_axis_is_constant(frame):
    axis_cols = [c for c in frame.columns
                 if c.startswith("AX_") and not c.endswith(("_z", "_clr"))]
    assert axis_cols
    constant = [c for c in axis_cols if frame[c].std(ddof=0) < 1e-12]
    assert not constant, f"constant axes reached the frame: {constant}"


def test_shrunk_rating_lies_between_the_raw_rating_and_the_prior(frame):
    """Shrinkage must pull toward the corpus mean, never past it or away from it."""
    prior = float(CFG.section("outcomes", "quality", "shrinkage", "c_prior_mean"))
    shrunk = frame["rating_shrunk"]
    raw = frame["avg_rating"]
    lower = pd.concat([raw, pd.Series(prior, index=raw.index)], axis=1).min(axis=1)
    upper = pd.concat([raw, pd.Series(prior, index=raw.index)], axis=1).max(axis=1)
    assert (shrunk >= lower - 1e-9).all()
    assert (shrunk <= upper + 1e-9).all()


def test_shrinkage_moves_thin_books_more_than_well_rated_ones(frame):
    move = (frame["rating_shrunk"] - frame["avg_rating"]).abs()
    thin = frame["n_ratings"] < 30
    assert move[thin].mean() > move[~thin].mean()


def test_reliability_weight_is_a_proportion(frame):
    assert frame["reliability"].between(0, 1).all()


def test_quality_and_reach_are_distinct_channels(frame):
    """If these correlated strongly there would be no reason to keep two channels."""
    r = float(frame["avg_rating"].corr(frame["log_n_ratings"]))
    assert abs(r) < 0.4


def test_tier_column_uses_the_configured_levels(frame):
    tier_col = CFG.tier_column
    assert set(frame[tier_col].dropna().unique()) <= set(CFG.tier_order)
    counts = frame[tier_col].value_counts()
    assert counts.min() > int(CFG.section("screening", "min_books_per_tier"))


def test_controls_are_present_and_usable(frame):
    for col in ["log_pages", "publication_year", "genre_group", "author_id", "series_id",
                "n_sentences"]:
        assert col in frame.columns, f"missing control {col}"
        assert frame[col].notna().mean() > 0.95


def test_mapping_coverage_is_much_better_than_the_legacy_pipeline(frame):
    """The old soft-probability pipeline mapped 20% of topic mass; this must beat it."""
    assert float(frame["mapped_mass"].mean()) > 0.5


def test_axis_coverage_audit_exists_and_flags_the_known_gaps():
    path = require(CFG.output_path("book_features_dir") / "axis_coverage.parquet")
    coverage = pd.read_parquet(path)
    empty = set(coverage.loc[coverage["verdict"] == "empty", "leaf_id"])
    # These are documented limitations of this model, not surprises.
    assert {"6.1a", "6.7"} <= empty


def test_strict_and_generous_mappings_broadly_agree():
    path = require(CFG.output_path("book_features_dir") / "axis_mapping_stability.parquet")
    stability = pd.read_parquet(path)
    assert float(stability["spearman_r"].median()) > 0.7
