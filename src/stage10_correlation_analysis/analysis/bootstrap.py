"""Cluster bootstrap and leave-one-cluster-out robustness.

The unit of independence in this corpus is not the book. An author's books share voice,
tropes, series continuity and often a fan base that rates them together, so resampling
individual books would treat correlated observations as independent and produce intervals
that are too narrow.

The cluster bootstrap resamples whole authors with replacement, which propagates that
correlation into the interval. It is the primary uncertainty statement for every headline
result, with series-level clustering as an alternative and leave-one-author-out as a check
that no single prolific author is driving a finding.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


def cluster_bootstrap(
    frame: pd.DataFrame,
    statistic: Callable[[pd.DataFrame], float],
    cluster_column: str,
    *,
    n_replicates: int = 2000,
    ci_level: float = 0.95,
    seed: int = 42,
    progress_every: Optional[int] = None,
) -> Dict[str, float]:
    """Percentile CI for any statistic, resampling whole clusters with replacement.

    `statistic` receives a resampled DataFrame and returns one number. Clusters are drawn
    with replacement to the original cluster count, so the resampled frame varies in row
    count — that is correct, and is exactly the variability a book-level bootstrap misses.
    """
    clusters = frame[cluster_column].astype("string").fillna("__missing__")
    groups = {key: idx.to_numpy() for key, idx in frame.groupby(clusters).groups.items()}
    keys = np.array(list(groups.keys()), dtype=object)
    n_clusters = len(keys)
    if n_clusters < 2:
        raise ValueError(f"Need at least 2 clusters in {cluster_column}, found {n_clusters}")

    point_estimate = float(statistic(frame))
    rng = np.random.default_rng(seed)
    replicates: List[float] = []

    for i in range(n_replicates):
        drawn = keys[rng.integers(0, n_clusters, n_clusters)]
        index = np.concatenate([groups[k] for k in drawn])
        try:
            replicates.append(float(statistic(frame.loc[index])))
        except Exception:
            # A resample can omit a tier or leave a predictor constant; skip rather than abort.
            continue
        if progress_every and (i + 1) % progress_every == 0:
            print(f"  cluster bootstrap {i + 1}/{n_replicates}")

    values = np.asarray(replicates, dtype=float)
    values = values[np.isfinite(values)]
    if values.size < 10:
        raise RuntimeError(f"Only {values.size} usable bootstrap replicates; statistic too fragile")

    alpha = 1.0 - ci_level
    low, high = np.quantile(values, [alpha / 2, 1 - alpha / 2])
    return {
        "estimate": point_estimate,
        "bootstrap_mean": float(values.mean()),
        "bias": float(values.mean() - point_estimate),
        "std_error": float(values.std(ddof=1)),
        "ci_low": float(low),
        "ci_high": float(high),
        "ci_excludes_zero": bool(low > 0 or high < 0),
        "n_replicates_used": int(values.size),
        "n_clusters": int(n_clusters),
    }


def cluster_bootstrap_many(
    frame: pd.DataFrame,
    statistics: Dict[str, Callable[[pd.DataFrame], float]],
    cluster_column: str,
    *,
    n_replicates: int = 2000,
    ci_level: float = 0.95,
    seed: int = 42,
) -> pd.DataFrame:
    """Bootstrap several statistics on the same resamples, so their CIs are comparable."""
    clusters = frame[cluster_column].astype("string").fillna("__missing__")
    groups = {key: idx.to_numpy() for key, idx in frame.groupby(clusters).groups.items()}
    keys = np.array(list(groups.keys()), dtype=object)
    n_clusters = len(keys)

    point = {name: float(fn(frame)) for name, fn in statistics.items()}
    collected: Dict[str, List[float]] = {name: [] for name in statistics}

    rng = np.random.default_rng(seed)
    for _ in range(n_replicates):
        drawn = keys[rng.integers(0, n_clusters, n_clusters)]
        index = np.concatenate([groups[k] for k in drawn])
        resampled = frame.loc[index]
        for name, fn in statistics.items():
            try:
                collected[name].append(float(fn(resampled)))
            except Exception:
                continue

    alpha = 1.0 - ci_level
    rows: List[Dict[str, object]] = []
    for name, values_list in collected.items():
        values = np.asarray(values_list, dtype=float)
        values = values[np.isfinite(values)]
        if values.size < 10:
            rows.append({
                "statistic": name, "estimate": point[name],
                "ci_low": np.nan, "ci_high": np.nan,
                "n_replicates_used": int(values.size), "note": "too few usable replicates",
            })
            continue
        low, high = np.quantile(values, [alpha / 2, 1 - alpha / 2])
        rows.append({
            "statistic": name,
            "estimate": point[name],
            "bootstrap_mean": float(values.mean()),
            "std_error": float(values.std(ddof=1)),
            "ci_low": float(low),
            "ci_high": float(high),
            "ci_excludes_zero": bool(low > 0 or high < 0),
            "n_replicates_used": int(values.size),
            "n_clusters": int(n_clusters),
            "note": "",
        })
    return pd.DataFrame(rows)


def leave_one_cluster_out(
    frame: pd.DataFrame,
    statistic: Callable[[pd.DataFrame], float],
    cluster_column: str,
    *,
    min_cluster_size: int = 5,
    top_n: Optional[int] = 50,
) -> pd.DataFrame:
    """Recompute the statistic with each large cluster removed.

    Only clusters big enough to matter are worth testing: dropping a one-book author cannot
    move a 16,000-book statistic. `top_n` limits this to the largest clusters, which are the
    only plausible single points of failure.
    """
    clusters = frame[cluster_column].astype("string").fillna("__missing__")
    sizes = clusters.value_counts()
    candidates = sizes[sizes >= min_cluster_size]
    if top_n:
        candidates = candidates.head(top_n)

    baseline = float(statistic(frame))
    rows: List[Dict[str, object]] = []
    for key, size in candidates.items():
        subset = frame.loc[clusters != key]
        try:
            value = float(statistic(subset))
        except Exception as exc:
            rows.append({
                "dropped_cluster": key, "cluster_size": int(size),
                "statistic": np.nan, "delta": np.nan, "note": str(exc)[:80],
            })
            continue
        rows.append({
            "dropped_cluster": key,
            "cluster_size": int(size),
            "statistic": value,
            "delta": value - baseline,
            "relative_change": (value - baseline) / abs(baseline) if baseline else np.nan,
            "sign_flipped": bool(np.sign(value) != np.sign(baseline)),
            "note": "",
        })
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out.attrs["baseline"] = baseline
    return out.sort_values("delta", key=lambda s: s.abs(), ascending=False).reset_index(drop=True)


def cluster_dominance(
    frame: pd.DataFrame,
    value_columns: Sequence[str],
    cluster_column: str,
) -> pd.DataFrame:
    """How concentrated is each feature's mass in a single cluster?

    A topic where one author holds 40% of the total mass is that author's stylistic tic,
    not a corpus-wide theme, and any tier difference on it is really an author difference.
    """
    clusters = frame[cluster_column].astype("string").fillna("__missing__")
    # One groupby for all features: 374 separate groupbys over 8,000 authors is minutes.
    totals = frame[list(value_columns)].groupby(clusters.to_numpy(), sort=False).sum()
    cluster_keys = totals.index.to_numpy()
    values = totals.to_numpy(dtype=float)
    grand = values.sum(axis=0)

    # Partial sort is enough: only the top three clusters per feature are reported.
    top_k = min(3, values.shape[0])
    top_idx = np.argpartition(-values, top_k - 1, axis=0)[:top_k]
    top_vals = np.take_along_axis(values, top_idx, axis=0)
    winner_pos = top_vals.argmax(axis=0)
    winner_idx = top_idx[winner_pos, np.arange(values.shape[1])]

    with np.errstate(invalid="ignore", divide="ignore"):
        top_share = top_vals.max(axis=0) / grand
        top3_share = top_vals.sum(axis=0) / grand

    empty = grand <= 0
    out = pd.DataFrame({
        "feature": list(totals.columns),
        "top_cluster": np.where(empty, None, cluster_keys[winner_idx]),
        "top_cluster_share": np.where(empty, np.nan, top_share),
        "top3_cluster_share": np.where(empty, np.nan, top3_share),
        "n_clusters_present": (values > 0).sum(axis=0),
    })
    return out.sort_values("top_cluster_share", ascending=False).reset_index(drop=True)


def flag_dominated_features(
    dominance: pd.DataFrame,
    max_share: float = 0.25,
) -> pd.DataFrame:
    out = dominance.copy()
    out["author_dominated"] = out["top_cluster_share"] > max_share
    return out


def make_delta_statistic(
    value_column: str,
    group_column: str,
    group_a: str,
    group_b: str,
) -> Callable[[pd.DataFrame], float]:
    """Cliff's delta between two groups, packaged for the bootstrap functions."""
    from src.stage10_correlation_analysis.analysis.effects import cliffs_delta

    def statistic(df: pd.DataFrame) -> float:
        a = df.loc[df[group_column] == group_a, value_column].dropna().to_numpy(dtype=float)
        b = df.loc[df[group_column] == group_b, value_column].dropna().to_numpy(dtype=float)
        if a.size < 2 or b.size < 2:
            raise ValueError("group too small in this resample")
        return cliffs_delta(a, b)

    return statistic


def make_coefficient_statistic(
    outcome: str,
    predictors: Sequence[str],
    term: str,
    *,
    categorical: Sequence[str] = (),
    weights: Optional[str] = None,
) -> Callable[[pd.DataFrame], float]:
    """One regression coefficient, packaged for the bootstrap functions."""
    from src.stage10_correlation_analysis.analysis.models import fit_ols

    def statistic(df: pd.DataFrame) -> float:
        fit = fit_ols(
            df, outcome, predictors,
            categorical=categorical, cluster=None, weights=weights, name="bootstrap",
        )
        match = fit.coefficients.loc[fit.coefficients["term"] == term, "coefficient"]
        if match.empty:
            raise ValueError(f"term {term} absent in this resample")
        return float(match.iloc[0])

    return statistic


def make_spearman_statistic(x_column: str, y_column: str) -> Callable[[pd.DataFrame], float]:
    from scipy import stats as sps

    def statistic(df: pd.DataFrame) -> float:
        valid = df[[x_column, y_column]].dropna()
        if len(valid) < 10:
            raise ValueError("too few rows in this resample")
        return float(sps.spearmanr(valid[x_column], valid[y_column]).statistic)

    return statistic
