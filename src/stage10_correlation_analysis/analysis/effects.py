"""Effect sizes.

With roughly 5,000 books per rating tier, a p-value tells us almost nothing: differences
far too small to matter are "significant". So every comparison in this analysis is
interpreted through an effect size with a bootstrap confidence interval, and the p-value is
reported only as a secondary column.

Cliff's delta is the workhorse. It is the probability that a randomly drawn book from group
A scores higher than one from group B, minus the reverse: fully nonparametric, unaffected by
the heavy right skew of topic shares, and readable as "how often does A exceed B".
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

# Romano et al. (2006) thresholds, the convention for Cliff's delta.
CLIFF_THRESHOLDS = {"negligible": 0.11, "small": 0.28, "medium": 0.43}


@dataclass
class EffectResult:
    metric: str
    estimate: float
    ci_low: float
    ci_high: float
    n_a: int
    n_b: int
    magnitude: str

    def as_dict(self) -> Dict[str, object]:
        return asdict(self)


def _clean_pair(a: Iterable[float], b: Iterable[float]) -> Tuple[np.ndarray, np.ndarray]:
    a_arr = np.asarray(list(a), dtype=float)
    b_arr = np.asarray(list(b), dtype=float)
    a_arr = a_arr[np.isfinite(a_arr)]
    b_arr = b_arr[np.isfinite(b_arr)]
    if a_arr.size == 0 or b_arr.size == 0:
        raise ValueError("Both groups must contain at least one finite value")
    return a_arr, b_arr


def cliffs_delta(a: Iterable[float], b: Iterable[float]) -> float:
    """P(A > B) - P(A < B), computed in O(n log n) via the rank-sum identity.

    The naive definition is a double loop over all pairs. Because Cliff's delta is a linear
    function of the Mann-Whitney U statistic, ranking the pooled sample gives the same
    answer at 5,000 x 5,000 scale in milliseconds, with correct handling of ties.
    """
    a_arr, b_arr = _clean_pair(a, b)
    n_a, n_b = a_arr.size, b_arr.size
    pooled = np.concatenate([a_arr, b_arr])
    ranks = pd.Series(pooled).rank(method="average").to_numpy()
    rank_sum_a = ranks[:n_a].sum()
    u_a = rank_sum_a - n_a * (n_a + 1) / 2.0
    return float(2.0 * u_a / (n_a * n_b) - 1.0)


def magnitude(delta: float) -> str:
    d = abs(delta)
    if d < CLIFF_THRESHOLDS["negligible"]:
        return "negligible"
    if d < CLIFF_THRESHOLDS["small"]:
        return "small"
    if d < CLIFF_THRESHOLDS["medium"]:
        return "medium"
    return "large"


def rank_biserial(a: Iterable[float], b: Iterable[float]) -> float:
    """Rank-biserial correlation. Identical in value to Cliff's delta for two groups.

    Kept as a separate name because the Mann-Whitney literature reports it under this label.
    """
    return cliffs_delta(a, b)


def epsilon_squared(groups: Sequence[Iterable[float]]) -> float:
    """Epsilon-squared for Kruskal-Wallis: the share of rank variance explained by group.

    Zero means no separation. The upper end depends on how many groups there are: with three
    equal-sized tiers, even perfect separation only reaches about 8/9, because within-tier
    rank variance remains. So compare these values across features at a fixed number of
    tiers, and do not read 0.4 as "40% of the way to perfect".
    """
    cleaned = [np.asarray(list(g), dtype=float) for g in groups]
    cleaned = [g[np.isfinite(g)] for g in cleaned]
    cleaned = [g for g in cleaned if g.size]
    if len(cleaned) < 2:
        raise ValueError("epsilon_squared needs at least two non-empty groups")

    n = sum(g.size for g in cleaned)
    pooled = np.concatenate(cleaned)
    ranks = pd.Series(pooled).rank(method="average").to_numpy()

    offset = 0
    h_numerator = 0.0
    for g in cleaned:
        group_ranks = ranks[offset:offset + g.size]
        offset += g.size
        h_numerator += g.size * (group_ranks.mean() - (n + 1) / 2.0) ** 2
    h = 12.0 / (n * (n + 1)) * h_numerator
    return float(h / (n - 1)) if n > 1 else 0.0


def hodges_lehmann(a: Iterable[float], b: Iterable[float], max_pairs: int = 4_000_000,
                   seed: int = 42) -> float:
    """Median of all pairwise differences a_i - b_j: a robust location shift.

    Unlike a difference of means it is not dragged by the long right tail of topic shares,
    and unlike a difference of medians it uses the whole distribution. Subsamples pairs
    when the exact grid would be too large.
    """
    a_arr, b_arr = _clean_pair(a, b)
    n_pairs = a_arr.size * b_arr.size
    if n_pairs <= max_pairs:
        diffs = (a_arr[:, None] - b_arr[None, :]).ravel()
    else:
        rng = np.random.default_rng(seed)
        idx_a = rng.integers(0, a_arr.size, max_pairs)
        idx_b = rng.integers(0, b_arr.size, max_pairs)
        diffs = a_arr[idx_a] - b_arr[idx_b]
    return float(np.median(diffs))


def bootstrap_ci(
    a: Iterable[float],
    b: Iterable[float],
    statistic=cliffs_delta,
    *,
    n_replicates: int = 2000,
    ci_level: float = 0.95,
    seed: int = 42,
    bca: bool = True,
) -> Tuple[float, float, float]:
    """Bootstrap CI for a two-group statistic. Returns (estimate, low, high).

    BCa corrects for the bias and skewness that a percentile interval ignores. Cliff's
    delta is bounded on [-1, 1], so its sampling distribution is skewed whenever the
    estimate is far from zero, which is exactly when we care about the interval.
    """
    a_arr, b_arr = _clean_pair(a, b)
    rng = np.random.default_rng(seed)
    estimate = statistic(a_arr, b_arr)

    replicates = np.empty(n_replicates, dtype=float)
    for i in range(n_replicates):
        sample_a = a_arr[rng.integers(0, a_arr.size, a_arr.size)]
        sample_b = b_arr[rng.integers(0, b_arr.size, b_arr.size)]
        replicates[i] = statistic(sample_a, sample_b)

    alpha = 1.0 - ci_level
    if not bca:
        low, high = np.quantile(replicates, [alpha / 2, 1 - alpha / 2])
        return float(estimate), float(low), float(high)

    low, high = _bca_interval(estimate, replicates, a_arr, b_arr, statistic, alpha)
    return float(estimate), float(low), float(high)


def _bca_interval(estimate, replicates, a_arr, b_arr, statistic, alpha):
    from scipy import stats as sps

    prop_less = float(np.mean(replicates < estimate))
    if prop_less in (0.0, 1.0):
        return tuple(np.quantile(replicates, [alpha / 2, 1 - alpha / 2]))
    z0 = sps.norm.ppf(prop_less)

    # Jackknife acceleration on the pooled sample, leaving out one observation at a time.
    jack: List[float] = []
    for i in range(a_arr.size):
        if a_arr.size > 1:
            jack.append(statistic(np.delete(a_arr, i), b_arr))
    for j in range(b_arr.size):
        if b_arr.size > 1:
            jack.append(statistic(a_arr, np.delete(b_arr, j)))
    jack_arr = np.asarray(jack, dtype=float)
    centred = jack_arr.mean() - jack_arr
    denom = 6.0 * (np.sum(centred ** 2) ** 1.5)
    acc = float(np.sum(centred ** 3) / denom) if denom > 0 else 0.0

    z_lo, z_hi = sps.norm.ppf(alpha / 2), sps.norm.ppf(1 - alpha / 2)

    def adjust(z: float) -> float:
        return float(sps.norm.cdf(z0 + (z0 + z) / max(1e-12, 1 - acc * (z0 + z))))

    return tuple(np.quantile(replicates, [adjust(z_lo), adjust(z_hi)]))


def fast_bootstrap_ci(
    a: Iterable[float],
    b: Iterable[float],
    *,
    n_replicates: int = 2000,
    ci_level: float = 0.95,
    seed: int = 42,
    chunk: int = 400,
) -> Tuple[float, float, float]:
    """Percentile bootstrap CI for Cliff's delta, without ever forming a resample.

    The BCa path jackknifes every observation, so it costs O(n) statistic evaluations —
    fine for a headline number, hopeless when screening 374 topics at 5,000 books a tier.

    The trick here is that a bootstrap resample only enters Cliff's delta through *how many
    times each distinct value was drawn*. Index the `K` distinct pooled values, count how
    often each was drawn, and writing `L_k` for the number of drawn B values strictly below
    the k-th distinct value,

        delta = sum_k  ca_k * (2*L_k + cb_k - n_b) / (n_a * n_b)

    which is a few array operations over a `(replicates, K)` count matrix. The counts are
    built with one offset `bincount` per chunk of replicates, so nothing is sorted and no
    resampled sample is ever materialised as values.
    """
    a_arr, b_arr = _clean_pair(a, b)
    n_a, n_b = a_arr.size, b_arr.size

    pooled = np.concatenate([a_arr, b_arr])
    _, inverse = np.unique(pooled, return_inverse=True)
    n_distinct = int(inverse.max()) + 1
    codes_a, codes_b = inverse[:n_a], inverse[n_a:]

    rng = np.random.default_rng(seed)
    deltas = np.empty(n_replicates, dtype=float)
    done = 0
    while done < n_replicates:
        size = min(chunk, n_replicates - done)
        offsets = (np.arange(size) * n_distinct)[:, None]
        counts_a = _draw_counts(rng, codes_a, n_a, size, n_distinct, offsets)
        counts_b = _draw_counts(rng, codes_b, n_b, size, n_distinct, offsets)
        below = np.cumsum(counts_b, axis=1) - counts_b
        deltas[done:done + size] = (
            (counts_a * (2.0 * below + counts_b - n_b)).sum(axis=1) / (n_a * n_b)
        )
        done += size

    alpha = 1.0 - ci_level
    low, high = np.quantile(deltas, [alpha / 2, 1 - alpha / 2])
    return float(cliffs_delta(a_arr, b_arr)), float(low), float(high)


def _draw_counts(rng, codes, n, n_replicates, n_distinct, offsets) -> np.ndarray:
    """Per-replicate counts of each distinct value under resampling with replacement."""
    drawn = codes[rng.integers(0, n, (n_replicates, n))] + offsets
    flat = np.bincount(drawn.ravel(), minlength=n_replicates * n_distinct)
    return flat.reshape(n_replicates, n_distinct).astype(np.float64)


def two_group_effects(
    frame: pd.DataFrame,
    value_columns: Sequence[str],
    group_column: str,
    group_a: str,
    group_b: str,
    *,
    n_replicates: int = 2000,
    ci_level: float = 0.95,
    seed: int = 42,
    exact_ci: bool = False,
    hl_max_pairs: int = 500_000,
) -> pd.DataFrame:
    """Cliff's delta with CI for many columns at once — the screening workhorse.

    Positive delta means group_a has higher values than group_b. `hl_max_pairs` caps the
    Hodges-Lehmann pair grid; at 5,000 books a tier the exact grid is 27 million pairs per
    column, and half a million sampled pairs pin the shift down to three significant figures.
    """
    mask_a = frame[group_column] == group_a
    mask_b = frame[group_column] == group_b
    ci_fn = bootstrap_ci if exact_ci else fast_bootstrap_ci

    rows: List[Dict[str, object]] = []
    for col in value_columns:
        a_vals = frame.loc[mask_a, col].to_numpy(dtype=float)
        b_vals = frame.loc[mask_b, col].to_numpy(dtype=float)
        a_vals = a_vals[np.isfinite(a_vals)]
        b_vals = b_vals[np.isfinite(b_vals)]
        if a_vals.size < 2 or b_vals.size < 2:
            continue
        if exact_ci:
            estimate, low, high = ci_fn(
                a_vals, b_vals, cliffs_delta,
                n_replicates=n_replicates, ci_level=ci_level, seed=seed,
            )
        else:
            estimate, low, high = ci_fn(
                a_vals, b_vals, n_replicates=n_replicates, ci_level=ci_level, seed=seed,
            )
        rows.append({
            "feature": col,
            "cliffs_delta": estimate,
            "ci_low": low,
            "ci_high": high,
            "ci_excludes_zero": (low > 0) or (high < 0),
            "magnitude": magnitude(estimate),
            "mean_a": float(a_vals.mean()),
            "mean_b": float(b_vals.mean()),
            "median_a": float(np.median(a_vals)),
            "median_b": float(np.median(b_vals)),
            "hodges_lehmann_shift": hodges_lehmann(a_vals, b_vals, max_pairs=hl_max_pairs, seed=seed),
            "n_a": int(a_vals.size),
            "n_b": int(b_vals.size),
        })
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values("cliffs_delta", key=lambda s: s.abs(), ascending=False).reset_index(drop=True)


def multi_group_effects(
    frame: pd.DataFrame,
    value_columns: Sequence[str],
    group_column: str,
    group_order: Sequence[str],
) -> pd.DataFrame:
    """Epsilon-squared across all tiers plus per-tier means, for the omnibus view."""
    rows: List[Dict[str, object]] = []
    for col in value_columns:
        groups = [
            frame.loc[frame[group_column] == g, col].to_numpy(dtype=float)
            for g in group_order
        ]
        groups = [g[np.isfinite(g)] for g in groups]
        if sum(g.size > 0 for g in groups) < 2:
            continue
        row: Dict[str, object] = {
            "feature": col,
            "epsilon_squared": epsilon_squared(groups),
        }
        for name, g in zip(group_order, groups):
            row[f"mean_{name}"] = float(g.mean()) if g.size else np.nan
            row[f"median_{name}"] = float(np.median(g)) if g.size else np.nan
        rows.append(row)
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values("epsilon_squared", ascending=False).reset_index(drop=True)
