"""Validity checks for the composite axes.

A composite index is only worth interpreting if its components actually belong together.
Four independent questions, four checks:

* **Do the components covary?** Cronbach's alpha and McDonald's omega. Alpha assumes equal
  loadings; omega does not, which matters because our axes use deliberately unequal weights
  (AX_hea_index is 1.0 x 4.5 + 0.8 x 5.3a + 0.5 x 8.3a).
* **Is it one dimension or several?** PCA on the components. If PC1 explains little more
  than PC2, the axis is measuring two things and should not be summed.
* **Is it stable?** Split-half correlation, and leave-one-component-out sign stability.
* **Does it depend on a single component?** Leave-one-out correlation with the full index.
  An axis that collapses when one leaf is removed is that leaf under another name.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd


def _clean(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.replace([np.inf, -np.inf], np.nan).dropna()
    constant = [c for c in out.columns if out[c].std(ddof=0) == 0]
    return out.drop(columns=constant)


def cronbach_alpha(frame: pd.DataFrame) -> float:
    """Standard internal-consistency coefficient. Undefined for fewer than 2 components."""
    data = _clean(frame)
    k = data.shape[1]
    if k < 2:
        return float("nan")
    item_var = data.var(axis=0, ddof=1).sum()
    total_var = data.sum(axis=1).var(ddof=1)
    if total_var <= 0:
        return float("nan")
    return float(k / (k - 1) * (1 - item_var / total_var))


def mcdonald_omega(frame: pd.DataFrame) -> float:
    """Omega from a one-factor solution, allowing unequal loadings.

    Estimated from the first principal component of the correlation matrix, rescaled to the
    covariance scale. Preferred over alpha whenever components are weighted unequally, which
    is true of most axes here.
    """
    data = _clean(frame)
    if data.shape[1] < 2:
        return float("nan")

    corr = np.corrcoef(data.to_numpy(), rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(corr)
    idx = int(np.argmax(eigenvalues))
    loadings = eigenvectors[:, idx] * np.sqrt(max(eigenvalues[idx], 0.0))
    # Sign is arbitrary; orient so most loadings are positive.
    if np.sum(loadings) < 0:
        loadings = -loadings

    sds = data.std(axis=0, ddof=1).to_numpy()
    scaled = loadings * sds
    common = float(scaled.sum() ** 2)
    unique = float(np.sum(sds ** 2 * (1 - np.clip(loadings ** 2, 0, 1))))
    denom = common + unique
    return float(common / denom) if denom > 0 else float("nan")


def pca_structure(frame: pd.DataFrame, n_components: int = 3) -> pd.DataFrame:
    """Explained-variance table plus PC1 loadings — the dimensionality check."""
    data = _clean(frame)
    if data.shape[1] < 2:
        return pd.DataFrame()

    standardised = (data - data.mean()) / data.std(ddof=0)
    matrix = standardised.to_numpy()
    _, singular, right = np.linalg.svd(matrix, full_matrices=False)
    variance = singular ** 2 / (matrix.shape[0] - 1)
    total = variance.sum()

    k = min(n_components, len(variance))
    rows: List[Dict[str, object]] = []
    for i in range(k):
        loadings = right[i]
        if np.sum(loadings) < 0:
            loadings = -loadings
        rows.append({
            "component": f"PC{i + 1}",
            "explained_variance_ratio": float(variance[i] / total) if total else np.nan,
            "cumulative_ratio": float(variance[: i + 1].sum() / total) if total else np.nan,
            "loadings": dict(zip(data.columns, np.round(loadings, 3))),
            "min_loading": float(loadings.min()),
            "all_loadings_same_sign": bool(np.all(loadings > 0) or np.all(loadings < 0)),
        })
    return pd.DataFrame(rows)


def split_half(frame: pd.DataFrame, seed: int = 42) -> Dict[str, float]:
    """Correlation between two halves of the components, with Spearman-Brown correction.

    Averaged over random splits so the answer does not hinge on one arbitrary partition.
    """
    data = _clean(frame)
    if data.shape[1] < 4:
        return {"split_half_r": float("nan"), "spearman_brown": float("nan"), "n_splits": 0}

    rng = np.random.default_rng(seed)
    columns = list(data.columns)
    correlations: List[float] = []
    for _ in range(50):
        shuffled = rng.permutation(columns)
        mid = len(shuffled) // 2
        left = data[list(shuffled[:mid])].sum(axis=1)
        right = data[list(shuffled[mid:])].sum(axis=1)
        if left.std() == 0 or right.std() == 0:
            continue
        correlations.append(float(np.corrcoef(left, right)[0, 1]))

    if not correlations:
        return {"split_half_r": float("nan"), "spearman_brown": float("nan"), "n_splits": 0}
    r = float(np.mean(correlations))
    return {
        "split_half_r": r,
        "spearman_brown": float(2 * r / (1 + r)) if r > -1 else float("nan"),
        "n_splits": len(correlations),
    }


def leave_one_out_stability(
    frame: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None,
) -> pd.DataFrame:
    """Drop each component and measure how much the index changes.

    Two numbers per component: correlation of the reduced index with the full index (near 1
    means the component is redundant, low means the index depends on it), and the share of
    books whose index sign flips.
    """
    data = _clean(frame)
    if data.shape[1] < 2:
        return pd.DataFrame()

    w = {c: float((weights or {}).get(c, 1.0)) for c in data.columns}
    full = sum(data[c] * w[c] for c in data.columns)

    rows: List[Dict[str, object]] = []
    for col in data.columns:
        remaining = [c for c in data.columns if c != col]
        reduced = sum(data[c] * w[c] for c in remaining)
        if reduced.std() == 0 or full.std() == 0:
            correlation = float("nan")
        else:
            correlation = float(np.corrcoef(full, reduced)[0, 1])
        sign_flip = float(np.mean(np.sign(full) != np.sign(reduced)))
        rows.append({
            "dropped_component": col,
            "weight": w[col],
            "corr_with_full": correlation,
            "sign_flip_rate": sign_flip,
            "sign_stable": sign_flip <= 0.10,
            "component_mean": float(data[col].mean()),
            "component_share_of_index": float(
                (data[col] * w[col]).sum() / full.sum()
            ) if full.sum() != 0 else np.nan,
        })
    return pd.DataFrame(rows).sort_values("corr_with_full").reset_index(drop=True)


def axis_validity_report(
    component_frame: pd.DataFrame,
    axis_name: str,
    *,
    weights: Optional[Dict[str, float]] = None,
    alpha_threshold: float = 0.60,
    omega_threshold: float = 0.65,
    sign_stability_threshold: float = 0.90,
) -> Dict[str, object]:
    """One-row verdict for an axis, combining all four checks.

    Thresholds come from `global.reliability_thresholds` in the axis schema.
    """
    data = _clean(component_frame)
    alpha = cronbach_alpha(data)
    omega = mcdonald_omega(data)
    pca = pca_structure(data)
    halves = split_half(data)
    loo = leave_one_out_stability(data, weights)

    pc1_ratio = float(pca.loc[0, "explained_variance_ratio"]) if len(pca) else np.nan
    same_sign = bool(pca.loc[0, "all_loadings_same_sign"]) if len(pca) else False
    min_stability = float(1.0 - loo["sign_flip_rate"].max()) if len(loo) else np.nan

    checks = {
        "alpha_ok": bool(np.isnan(alpha) or alpha >= alpha_threshold),
        "omega_ok": bool(np.isnan(omega) or omega >= omega_threshold),
        "unidimensional": same_sign and (np.isnan(pc1_ratio) or pc1_ratio >= 0.40),
        "sign_stable": bool(np.isnan(min_stability) or min_stability >= sign_stability_threshold),
    }
    if data.shape[1] < 2:
        verdict = "atomic"   # single component: reliability is undefined, not failed
    elif all(checks.values()):
        verdict = "valid"
    elif checks["unidimensional"] and checks["sign_stable"]:
        verdict = "usable_low_reliability"
    else:
        verdict = "questionable"

    return {
        "axis": axis_name,
        "n_components": int(data.shape[1]),
        "components": ", ".join(data.columns),
        "cronbach_alpha": alpha,
        "mcdonald_omega": omega,
        "pc1_explained": pc1_ratio,
        "pc1_all_same_sign": same_sign,
        "split_half_r": halves["split_half_r"],
        "spearman_brown": halves["spearman_brown"],
        "min_sign_stability": min_stability,
        "most_load_bearing_component": (
            loo.loc[0, "dropped_component"] if len(loo) else None
        ),
        "verdict": verdict,
        **checks,
    }


def axis_correlation_matrix(axis_frame: pd.DataFrame, method: str = "spearman") -> pd.DataFrame:
    """Correlations among axes. High values flag axes that are not separate constructs."""
    return axis_frame.corr(method=method)


def redundancy_flags(correlation: pd.DataFrame, threshold: float = 0.85) -> pd.DataFrame:
    """Axis pairs correlated above `threshold` — candidates for merging or dropping."""
    rows: List[Dict[str, object]] = []
    columns = list(correlation.columns)
    for i, left in enumerate(columns):
        for right in columns[i + 1:]:
            r = float(correlation.loc[left, right])
            if abs(r) >= threshold:
                rows.append({"axis_a": left, "axis_b": right, "correlation": r})
    return pd.DataFrame(rows).sort_values(
        "correlation", key=lambda s: s.abs(), ascending=False
    ).reset_index(drop=True) if rows else pd.DataFrame(columns=["axis_a", "axis_b", "correlation"])
