"""Compositional-data helpers.

Topic shares are a composition: they sum to 1 within each book, so they live on a simplex
rather than in ordinary Euclidean space. Two consequences drive everything here.

1. An increase in one topic is necessarily a decrease elsewhere. Every effect we report is
   a *reallocation* of narrative attention, never an absolute amount.
2. Raw shares are not suitable for regression — the sum constraint induces spurious
   negative correlation. We use the centred log-ratio (CLR) transform for models, ranks
   for tier tests, and raw shares only for description.
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

import numpy as np
import pandas as pd


def half_min_observable_epsilon(median_sentences_per_book: float) -> float:
    """Smallest meaningful non-zero share: half a sentence.

    A book with N sentences can only observe shares in steps of 1/N, so a zero really
    means "below 1/N". Using eps = 1/(2N) places the zero replacement half a step below
    the smallest observable value, which is the standard multiplicative-replacement idea
    without needing an iterative imputation.
    """
    if median_sentences_per_book <= 0:
        raise ValueError("median_sentences_per_book must be positive")
    return 1.0 / (2.0 * float(median_sentences_per_book))


def resolve_epsilon(
    mode: str,
    *,
    median_sentences_per_book: Optional[float] = None,
    fallback: float = 1e-5,
) -> float:
    if mode == "half_min_observable":
        if median_sentences_per_book is None:
            return fallback
        return half_min_observable_epsilon(median_sentences_per_book)
    if mode == "fixed":
        return fallback
    raise ValueError(f"Unknown epsilon mode: {mode}")


def epsilon_from_counts(
    sentences_per_book: pd.Series,
    *,
    mode: str = "half_min_observable",
    fallback: float = 1e-5,
) -> float:
    """Derive epsilon from the actual corpus, rather than picking a round number."""
    return resolve_epsilon(
        mode,
        median_sentences_per_book=float(pd.Series(sentences_per_book).median()),
        fallback=fallback,
    )


def check_share_sums(frame: pd.DataFrame, *, name: str = "shares", tolerance: float = 1e-6) -> float:
    """Assert the composition is intact and return the worst deviation seen."""
    worst = float(share_sum_check(frame, tolerance).max())
    if worst > tolerance:
        raise AssertionError(f"{name} do not sum to 1 per row; worst deviation {worst:.2e}")
    return worst


def clr(frame: pd.DataFrame, epsilon: float) -> pd.DataFrame:
    """Centred log-ratio: log(s + eps) minus the row mean of log(s + eps).

    CLR removes the sum constraint while keeping every part interpretable relative to the
    book's own geometric mean, so a positive CLR value means "more of this theme than this
    book's typical theme".
    """
    if frame.empty:
        return frame.copy()
    values = frame.to_numpy(dtype=float)
    if np.any(values < 0):
        raise ValueError("CLR expects non-negative shares")
    logged = np.log(values + epsilon)
    centred = logged - logged.mean(axis=1, keepdims=True)
    return pd.DataFrame(centred, index=frame.index, columns=frame.columns)


def alr(frame: pd.DataFrame, reference: str, epsilon: float) -> pd.DataFrame:
    """Additive log-ratio against one reference part. Useful when a natural baseline exists."""
    if reference not in frame.columns:
        raise KeyError(f"Reference column {reference!r} not in frame")
    logged = np.log(frame.to_numpy(dtype=float) + epsilon)
    ref = np.log(frame[reference].to_numpy(dtype=float) + epsilon)
    out = pd.DataFrame(logged - ref[:, None], index=frame.index, columns=frame.columns)
    return out.drop(columns=[reference])


def log_ratio(
    frame: pd.DataFrame,
    numerator: Sequence[str],
    denominator: Sequence[str],
    epsilon: float,
    *,
    strict: bool = True,
) -> pd.Series:
    """log( sum(numerator parts) / sum(denominator parts) ) — the balance form.

    This is the natural way to state a "A over B" hypothesis on compositional data: it is
    scale-free, symmetric (reversing the legs flips the sign), and unaffected by the other
    parts of the composition.
    """
    num_cols = _present(frame, numerator, "numerator", strict)
    den_cols = _present(frame, denominator, "denominator", strict)
    num = frame[num_cols].sum(axis=1) + epsilon
    den = frame[den_cols].sum(axis=1) + epsilon
    return np.log(num / den)


def _present(frame: pd.DataFrame, cols: Sequence[str], role: str, strict: bool) -> List[str]:
    found = [c for c in cols if c in frame.columns]
    missing = [c for c in cols if c not in frame.columns]
    if missing and strict:
        raise KeyError(f"{role} columns absent from frame: {missing}")
    if not found:
        raise KeyError(f"No {role} columns present; requested {list(cols)}")
    return found


def zscore(series: pd.Series) -> pd.Series:
    """Standardise, tolerating a constant column instead of returning NaN."""
    std = series.std(ddof=0)
    if not np.isfinite(std) or std == 0:
        return pd.Series(0.0, index=series.index, name=series.name)
    return (series - series.mean()) / std


def zscore_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.apply(zscore)


def share_sum_check(frame: pd.DataFrame, tolerance: float = 1e-6) -> pd.Series:
    """Absolute deviation of each row's share sum from 1."""
    return (frame.sum(axis=1) - 1.0).abs()


def assert_composition(frame: pd.DataFrame, tolerance: float = 1e-6, label: str = "shares") -> None:
    worst = share_sum_check(frame).max()
    if worst > tolerance:
        raise AssertionError(f"{label} do not sum to 1 per row; worst deviation {worst:.2e}")


def prevalence(frame: pd.DataFrame, threshold: float = 0.0) -> pd.Series:
    """Fraction of rows where each column exceeds `threshold`."""
    return (frame > threshold).mean()


def screen_columns(
    frame: pd.DataFrame,
    *,
    min_prevalence: float,
    min_mean_share: float,
) -> pd.DataFrame:
    """Screening table for the topic-level funnel: which parts are worth testing at all.

    A topic present in 1% of books, or averaging 0.001% of sentences, cannot support a
    tier comparison however large the corpus is.
    """
    table = pd.DataFrame({
        "prevalence": prevalence(frame),
        "mean_share": frame.mean(),
        "median_share": frame.median(),
        "max_share": frame.max(),
    })
    table["passes_prevalence"] = table["prevalence"] >= min_prevalence
    table["passes_mean_share"] = table["mean_share"] >= min_mean_share
    table["passes_screen"] = table["passes_prevalence"] & table["passes_mean_share"]
    return table.sort_values("mean_share", ascending=False)


def residualise(target: pd.Series, covariates: pd.DataFrame) -> pd.Series:
    """Regress `target` on `covariates` and return the residual.

    Used where two axes share a taxonomy leaf — H4's protective-care leg (4.6) also feeds
    the payoff axis, so the shared component is removed rather than silently counted twice.
    """
    design = np.column_stack([np.ones(len(target)), covariates.to_numpy(dtype=float)])
    y = target.to_numpy(dtype=float)
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    return pd.Series(y - design @ coef, index=target.index, name=f"{target.name}_resid")


def aitchison_distance(frame: pd.DataFrame, epsilon: float) -> np.ndarray:
    """Pairwise Aitchison distance — Euclidean distance in CLR space."""
    clr_frame = clr(frame, epsilon)
    values = clr_frame.to_numpy()
    sq = (values ** 2).sum(axis=1)
    dist_sq = sq[:, None] + sq[None, :] - 2 * values @ values.T
    return np.sqrt(np.maximum(dist_sq, 0.0))


def wide_from_long(
    long_df: pd.DataFrame,
    *,
    index: str,
    columns: str,
    values: str,
    fill_value: float = 0.0,
    prefix: str = "",
) -> pd.DataFrame:
    """Pivot a long counts table to a wide share matrix, filling absent parts with 0."""
    wide = long_df.pivot_table(
        index=index, columns=columns, values=values, aggfunc="sum", fill_value=fill_value
    )
    wide.columns = [f"{prefix}{c}" for c in wide.columns]
    return wide.sort_index()


def add_missing_columns(frame: pd.DataFrame, expected: Iterable[str], fill: float = 0.0) -> pd.DataFrame:
    """Ensure every expected part exists, so a leaf with zero topics is an explicit zero.

    The earlier pipeline dropped absent categories entirely, which made an empty axis look
    like a legitimate 0.0 rather than a coverage failure.
    """
    out = frame.copy()
    for col in expected:
        if col not in out.columns:
            out[col] = fill
    return out
