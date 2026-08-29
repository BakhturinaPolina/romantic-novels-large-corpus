"""Narrative arc analysis on within-book tertiles.

H6 asks a question no book-level average can answer: does repair *rise* and conflict *fall*
as a romance progresses, and do better-rated books show a stronger movement?

Splitting each book into three equal-length parts and taking within-book differences
(end minus begin) is the key design choice. Because every difference is computed inside a
single book, every book-level confound — author voice, subgenre, length, era, publisher —
cancels exactly. What survives is the shape of the arc, which is what the hypothesis is
about.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

TERTILE_ORDER = ("begin", "middle", "end")


def pivot_tertiles(
    tertile_long: pd.DataFrame,
    *,
    id_column: str = "book_id",
    tertile_column: str = "tertile",
    feature_column: str = "feature",
    value_column: str = "share",
) -> pd.DataFrame:
    """Long tertile table to a book x (feature, tertile) wide frame."""
    wide = tertile_long.pivot_table(
        index=id_column,
        columns=[feature_column, tertile_column],
        values=value_column,
        aggfunc="sum",
        fill_value=0.0,
    )
    wide.columns = [f"{feat}__{tert}" for feat, tert in wide.columns]
    return wide.sort_index()


def tertile_deltas(
    tertile_wide: pd.DataFrame,
    features: Sequence[str],
    contrasts: Sequence[Sequence[str]] = (("end", "begin"), ("middle", "begin")),
) -> pd.DataFrame:
    """Within-book differences between tertiles, one column per feature and contrast.

    Also emits a `__slope` column: the least-squares slope across begin/middle/end, which
    uses all three points instead of just the endpoints and is less sensitive to a single
    noisy tertile.
    """
    out = pd.DataFrame(index=tertile_wide.index)
    positions = np.array([0.0, 1.0, 2.0])

    for feature in features:
        columns = {t: f"{feature}__{t}" for t in TERTILE_ORDER}
        if not all(c in tertile_wide.columns for c in columns.values()):
            continue
        for later, earlier in contrasts:
            out[f"{feature}__{later}_minus_{earlier}"] = (
                tertile_wide[columns[later]] - tertile_wide[columns[earlier]]
            )
        values = tertile_wide[[columns[t] for t in TERTILE_ORDER]].to_numpy(dtype=float)
        centred = positions - positions.mean()
        out[f"{feature}__slope"] = (values * centred).sum(axis=1) / (centred ** 2).sum()
    return out


def arc_direction_summary(
    deltas: pd.DataFrame,
    rising_features: Sequence[str],
    falling_features: Sequence[str],
    *,
    contrast: str = "end_minus_begin",
) -> pd.DataFrame:
    """Does each feature move in the direction the hypothesis predicts?

    Reports the fraction of books moving as predicted alongside the mean shift, because a
    small mean can hide a strong majority direction and vice versa.
    """
    rows: List[Dict[str, object]] = []
    for features, expected in ((rising_features, "rise"), (falling_features, "fall")):
        for feature in features:
            column = f"{feature}__{contrast}"
            if column not in deltas.columns:
                rows.append({
                    "feature": feature, "expected": expected, "n_books": 0,
                    "note": "feature absent from tertile table",
                })
                continue
            values = deltas[column].dropna()
            share_up = float((values > 0).mean())
            observed = "rise" if values.mean() > 0 else "fall"
            rows.append({
                "feature": feature,
                "expected": expected,
                "mean_shift": float(values.mean()),
                "median_shift": float(values.median()),
                "share_books_rising": share_up,
                "observed": observed,
                "matches_prediction": observed == expected,
                "n_books": int(values.size),
                "note": "",
            })
    return pd.DataFrame(rows)


def arc_index(
    deltas: pd.DataFrame,
    rising_features: Sequence[str],
    falling_features: Sequence[str],
    *,
    contrast: str = "end_minus_begin",
) -> pd.Series:
    """One number per book: how strongly it follows the predicted arc.

    Sum of the rising features' shifts minus the falling features' shifts. Positive means
    the book resolves toward repair and away from conflict, which is the H6 prediction.
    """
    rising_cols = [f"{f}__{contrast}" for f in rising_features if f"{f}__{contrast}" in deltas.columns]
    falling_cols = [f"{f}__{contrast}" for f in falling_features if f"{f}__{contrast}" in deltas.columns]
    if not rising_cols and not falling_cols:
        raise KeyError("Neither rising nor falling features present in the delta frame")

    rise = deltas[rising_cols].sum(axis=1) if rising_cols else 0.0
    fall = deltas[falling_cols].sum(axis=1) if falling_cols else 0.0
    return pd.Series(rise - fall, index=deltas.index, name=f"arc_index__{contrast}")


def tertile_profile_by_group(
    tertile_long: pd.DataFrame,
    group_map: pd.Series,
    features: Sequence[str],
    *,
    id_column: str = "book_id",
    tertile_column: str = "tertile",
    feature_column: str = "feature",
    value_column: str = "share",
) -> pd.DataFrame:
    """Mean share per tertile per tier — the data behind the arc plots."""
    subset = tertile_long[tertile_long[feature_column].isin(features)].copy()
    subset["group"] = subset[id_column].map(group_map)
    subset = subset.dropna(subset=["group"])

    profile = subset.groupby(
        [feature_column, "group", tertile_column], observed=True
    )[value_column].agg(mean="mean", median="median", sd="std", n="size").reset_index()
    profile[tertile_column] = pd.Categorical(
        profile[tertile_column], categories=list(TERTILE_ORDER), ordered=True
    )
    return profile.sort_values([feature_column, "group", tertile_column]).reset_index(drop=True)


def within_book_wilcoxon(
    deltas: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Wilcoxon signed-rank test that each within-book shift differs from zero.

    The paired form is the right test here: each book supplies its own baseline, so the
    null is "this book's end looks like its own beginning", not "books differ from each
    other".
    """
    from scipy import stats as sps

    rows: List[Dict[str, object]] = []
    for col in columns:
        if col not in deltas.columns:
            continue
        values = deltas[col].dropna().to_numpy(dtype=float)
        nonzero = values[values != 0]
        if nonzero.size < 10:
            continue
        statistic, p_value = sps.wilcoxon(nonzero)
        # Matched-pairs rank-biserial correlation: the paired effect size.
        n = nonzero.size
        total_rank = n * (n + 1) / 2
        positive_rank = sps.rankdata(np.abs(nonzero))[nonzero > 0].sum()
        rows.append({
            "feature": col,
            "wilcoxon_statistic": float(statistic),
            "p_value": float(p_value),
            "mean_shift": float(values.mean()),
            "median_shift": float(np.median(values)),
            "rank_biserial": float(2 * positive_rank / total_rank - 1),
            "share_rising": float((values > 0).mean()),
            "n_books": int(values.size),
            "n_nonzero": int(n),
        })
    return pd.DataFrame(rows)


def arc_vs_outcome(
    deltas: pd.DataFrame,
    outcome: pd.Series,
    columns: Sequence[str],
    method: str = "spearman",
) -> pd.DataFrame:
    """Correlate each within-book arc shift with a rating outcome.

    This is the second half of H6: not just "do arcs move" but "does the movement relate to
    how the book is received".
    """
    from scipy import stats as sps

    rows: List[Dict[str, object]] = []
    aligned_outcome = outcome.reindex(deltas.index)
    for col in columns:
        if col not in deltas.columns:
            continue
        valid = pd.concat([deltas[col], aligned_outcome], axis=1).dropna()
        if len(valid) < 30:
            continue
        x, y = valid.iloc[:, 0], valid.iloc[:, 1]
        if method == "spearman":
            result = sps.spearmanr(x, y)
            coefficient, p_value = float(result.statistic), float(result.pvalue)
        else:
            coefficient, p_value = sps.pearsonr(x, y)
        rows.append({
            "feature": col,
            "outcome": outcome.name,
            f"{method}_r": coefficient,
            "p_value": float(p_value),
            "n": int(len(valid)),
        })
    out = pd.DataFrame(rows)
    return out.sort_values(f"{method}_r", key=lambda s: s.abs(), ascending=False).reset_index(drop=True) if len(out) else out


def aggregate_tertile_leaves(
    tertile_counts: pd.DataFrame,
    topic_to_leaf: pd.Series,
    *,
    id_column: str = "book_id",
    tertile_column: str = "tertile",
    topic_column: str = "topic_id",
    count_column: str = "n_sentences",
) -> pd.DataFrame:
    """Roll tertile topic counts up to taxonomy leaves, renormalising within each tertile."""
    frame = tertile_counts.copy()
    frame["leaf"] = frame[topic_column].map(topic_to_leaf)
    frame = frame.dropna(subset=["leaf"])

    grouped = frame.groupby([id_column, tertile_column, "leaf"], as_index=False)[count_column].sum()
    totals = grouped.groupby([id_column, tertile_column], as_index=False)[count_column].sum()
    totals = totals.rename(columns={count_column: "tertile_total"})
    grouped = grouped.merge(totals, on=[id_column, tertile_column], how="left")
    grouped["share"] = grouped[count_column] / grouped["tertile_total"].replace(0, np.nan)
    return grouped.rename(columns={"leaf": "feature"})
