"""Regression models for the two outcome channels.

Three constraints shape every model here.

* **Authors confound everything.** 8,264 authors write the 16,000 books, and 5,353 of them
  appear exactly once. Author fixed effects are therefore infeasible (they would absorb a
  third of the sample entirely), so we use author-cluster-robust standard errors plus a
  cluster bootstrap, and check headline results with leave-one-author-out.
* **Predictors are compositional.** Raw shares are linearly dependent, so regressions run
  on CLR-transformed shares or on explicit log-ratios, never on raw shares side by side.
* **Ratings are unequally reliable.** A book with 12 ratings and one with 40,000 ratings
  carry very different information about quality, so the quality channel is fit weighted by
  reliability v/(v+m), with unweighted and n>=30 fits as sensitivity checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


@dataclass
class ModelFit:
    name: str
    outcome: str
    n_obs: int
    n_clusters: Optional[int]
    r_squared: Optional[float]
    coefficients: pd.DataFrame
    summary_text: str
    extra: Dict[str, Any]


def _design(
    frame: pd.DataFrame,
    predictors: Sequence[str],
    categorical: Sequence[str] = (),
) -> pd.DataFrame:
    """Numeric predictors plus one-hot categoricals, first level dropped."""
    parts: List[pd.DataFrame] = []
    numeric = [p for p in predictors if p not in categorical]
    if numeric:
        parts.append(frame[numeric].astype(float))
    for col in categorical:
        if col not in frame.columns:
            continue
        dummies = pd.get_dummies(frame[col].astype("string"), prefix=col, drop_first=True, dtype=float)
        parts.append(dummies)
    if not parts:
        raise ValueError("No predictors resolved for the design matrix")
    return pd.concat(parts, axis=1)


def _prepare(
    frame: pd.DataFrame,
    outcome: str,
    predictors: Sequence[str],
    categorical: Sequence[str],
    cluster: Optional[str],
    weights: Optional[str],
) -> Tuple[pd.Series, pd.DataFrame, Optional[pd.Series], Optional[pd.Series]]:
    needed = [outcome, *predictors, *categorical]
    if cluster:
        needed.append(cluster)
    if weights:
        needed.append(weights)
    needed = [c for c in dict.fromkeys(needed) if c in frame.columns]

    subset = frame[needed].replace([np.inf, -np.inf], np.nan).dropna()
    y = subset[outcome].astype(float)
    X = _design(subset, predictors, categorical)
    groups = subset[cluster].astype("string") if cluster and cluster in subset else None
    w = subset[weights].astype(float) if weights and weights in subset else None
    return y, X, groups, w


def fit_ols(
    frame: pd.DataFrame,
    outcome: str,
    predictors: Sequence[str],
    *,
    categorical: Sequence[str] = (),
    cluster: Optional[str] = None,
    weights: Optional[str] = None,
    name: str = "ols",
) -> ModelFit:
    """OLS (or WLS when `weights` is given) with cluster-robust standard errors.

    Clustering by author is what keeps the standard errors honest: a prolific author's
    books share unmeasured style, so treating them as independent observations would
    understate uncertainty, sometimes badly.
    """
    import statsmodels.api as sm

    y, X, groups, w = _prepare(frame, outcome, predictors, categorical, cluster, weights)
    X_const = sm.add_constant(X, has_constant="add")

    model = sm.WLS(y, X_const, weights=w) if w is not None else sm.OLS(y, X_const)
    if groups is not None:
        codes = pd.factorize(groups)[0]
        result = model.fit(cov_type="cluster", cov_kwds={"groups": codes})
        n_clusters = int(pd.Series(codes).nunique())
    else:
        result = model.fit(cov_type="HC3")
        n_clusters = None

    coefficients = pd.DataFrame({
        "term": result.params.index,
        "coefficient": result.params.to_numpy(),
        "std_error": result.bse.to_numpy(),
        "t_statistic": result.tvalues.to_numpy(),
        "p_value": result.pvalues.to_numpy(),
        "ci_low": result.conf_int()[0].to_numpy(),
        "ci_high": result.conf_int()[1].to_numpy(),
    })

    return ModelFit(
        name=name,
        outcome=outcome,
        n_obs=int(result.nobs),
        n_clusters=n_clusters,
        r_squared=float(result.rsquared),
        coefficients=coefficients,
        summary_text=str(result.summary()),
        extra={
            "adj_r_squared": float(result.rsquared_adj),
            "weighted": w is not None,
            "cov_type": result.cov_type,
        },
    )


def fit_logistic(
    frame: pd.DataFrame,
    outcome: str,
    predictors: Sequence[str],
    *,
    categorical: Sequence[str] = (),
    cluster: Optional[str] = None,
    name: str = "logit",
) -> ModelFit:
    """Logistic regression, reported as odds ratios.

    Used for the high-versus-low tier contrast, which sidesteps the mid tier's ambiguity
    and gives a directly interpretable "odds of being highly rated" statement.
    """
    import statsmodels.api as sm

    y, X, groups, _ = _prepare(frame, outcome, predictors, categorical, cluster, None)
    X_const = sm.add_constant(X, has_constant="add")

    model = sm.Logit(y, X_const)
    if groups is not None:
        codes = pd.factorize(groups)[0]
        result = model.fit(disp=False, cov_type="cluster", cov_kwds={"groups": codes})
        n_clusters = int(pd.Series(codes).nunique())
    else:
        result = model.fit(disp=False)
        n_clusters = None

    conf = result.conf_int()
    coefficients = pd.DataFrame({
        "term": result.params.index,
        "coefficient": result.params.to_numpy(),
        "odds_ratio": np.exp(result.params.to_numpy()),
        "std_error": result.bse.to_numpy(),
        "z_statistic": result.tvalues.to_numpy(),
        "p_value": result.pvalues.to_numpy(),
        "or_ci_low": np.exp(conf[0].to_numpy()),
        "or_ci_high": np.exp(conf[1].to_numpy()),
    })

    return ModelFit(
        name=name,
        outcome=outcome,
        n_obs=int(result.nobs),
        n_clusters=n_clusters,
        r_squared=float(result.prsquared),
        coefficients=coefficients,
        summary_text=str(result.summary()),
        extra={"pseudo_r_squared": float(result.prsquared), "cov_type": result.cov_type},
    )


def add_quadratic(frame: pd.DataFrame, column: str, suffix: str = "_sq") -> Tuple[pd.DataFrame, str]:
    """Add a squared term on the centred predictor, for the H5 inverted-U test.

    Centring first means the linear coefficient stays interpretable at the corpus mean
    instead of at the meaningless value zero, and it removes most of the collinearity
    between a variable and its square.
    """
    out = frame.copy()
    new_col = f"{column}{suffix}"
    centred = out[column] - out[column].mean()
    out[new_col] = centred ** 2
    return out, new_col


def add_interaction(
    frame: pd.DataFrame,
    left: str,
    right: str,
) -> Tuple[pd.DataFrame, str]:
    """Product of two mean-centred predictors, so the main effects stay interpretable."""
    out = frame.copy()
    name = f"{left}_x_{right}"
    out[name] = (out[left] - out[left].mean()) * (out[right] - out[right].mean())
    return out, name


def turning_point(linear_coef: float, quadratic_coef: float) -> Optional[float]:
    """Vertex of a fitted quadratic, in centred units. None when there is no interior optimum."""
    if quadratic_coef == 0:
        return None
    return float(-linear_coef / (2.0 * quadratic_coef))


def variance_inflation(frame: pd.DataFrame, predictors: Sequence[str]) -> pd.DataFrame:
    """VIF per predictor. Above ~10 the coefficient is not separately identified.

    Matters here because several axes share taxonomy leaves by construction — 4.6 sits in
    both the payoff axis and H4's protective leg, for instance.
    """
    subset = frame[list(predictors)].replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    rows: List[Dict[str, object]] = []
    for col in subset.columns:
        others = subset.drop(columns=[col])
        if others.empty:
            rows.append({"predictor": col, "vif": 1.0, "r_squared": 0.0})
            continue
        design = np.column_stack([np.ones(len(others)), others.to_numpy()])
        target = subset[col].to_numpy()
        coef, *_ = np.linalg.lstsq(design, target, rcond=None)
        resid = target - design @ coef
        ss_tot = float(((target - target.mean()) ** 2).sum())
        r2 = 1.0 - float((resid ** 2).sum()) / ss_tot if ss_tot > 0 else 0.0
        vif = 1.0 / max(1e-12, 1.0 - r2)
        rows.append({"predictor": col, "vif": float(vif), "r_squared": float(r2)})
    return pd.DataFrame(rows).sort_values("vif", ascending=False).reset_index(drop=True)


def predictive_check(
    frame: pd.DataFrame,
    outcome: str,
    theme_predictors: Sequence[str],
    control_predictors: Sequence[str],
    *,
    categorical: Sequence[str] = (),
    group_column: str = "author_id",
    n_splits: int = 5,
    n_repeats: int = 20,
    seed: int = 42,
) -> pd.DataFrame:
    """Does adding themes improve out-of-sample prediction beyond controls alone?

    Grouped by author so the same author never appears in both train and test — otherwise
    the model can memorise an author's typical rating and the theme gain is illusory.
    Repeated to average over the arbitrariness of a single fold assignment.

    This is the honest headline for "do themes explain ratings at all". In-sample R-squared
    on 16,000 books will always look non-zero; held-out R-squared will not.
    """
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import GroupKFold
    from sklearn.metrics import mean_absolute_error, r2_score

    needed = [outcome, group_column, *theme_predictors, *control_predictors, *categorical]
    needed = [c for c in dict.fromkeys(needed) if c in frame.columns]
    subset = frame[needed].replace([np.inf, -np.inf], np.nan).dropna()

    y = subset[outcome].to_numpy(dtype=float)
    groups = pd.factorize(subset[group_column].astype("string"))[0]
    designs = {
        "controls_only": _design(subset, control_predictors, categorical),
        "controls_plus_themes": _design(
            subset, [*control_predictors, *theme_predictors], categorical
        ),
    }

    rng = np.random.default_rng(seed)
    rows: List[Dict[str, object]] = []
    for repeat in range(n_repeats):
        # GroupKFold is deterministic, so shuffle group labels to vary the partition.
        permutation = rng.permutation(groups.max() + 1)
        shuffled_groups = permutation[groups]
        splitter = GroupKFold(n_splits=n_splits)
        for fold, (train_idx, test_idx) in enumerate(
            splitter.split(np.zeros(len(y)), y, shuffled_groups)
        ):
            for label, X in designs.items():
                X_arr = X.to_numpy(dtype=float)
                mean = X_arr[train_idx].mean(axis=0)
                std = X_arr[train_idx].std(axis=0)
                std[std == 0] = 1.0
                model = Ridge(alpha=1.0)
                model.fit((X_arr[train_idx] - mean) / std, y[train_idx])
                prediction = model.predict((X_arr[test_idx] - mean) / std)
                rows.append({
                    "repeat": repeat,
                    "fold": fold,
                    "model": label,
                    "r2": float(r2_score(y[test_idx], prediction)),
                    "mae": float(mean_absolute_error(y[test_idx], prediction)),
                    "n_test": int(len(test_idx)),
                })
    return pd.DataFrame(rows)


def summarize_predictive_check(fold_results: pd.DataFrame) -> pd.DataFrame:
    """Mean held-out performance per model, plus the paired gain from adding themes."""
    summary = fold_results.groupby("model").agg(
        mean_r2=("r2", "mean"),
        sd_r2=("r2", "std"),
        mean_mae=("mae", "mean"),
        n_folds=("r2", "size"),
    ).reset_index()

    pivot = fold_results.pivot_table(
        index=["repeat", "fold"], columns="model", values="r2"
    ).dropna()
    if {"controls_only", "controls_plus_themes"} <= set(pivot.columns):
        gain = pivot["controls_plus_themes"] - pivot["controls_only"]
        summary.attrs["mean_r2_gain"] = float(gain.mean())
        summary.attrs["gain_positive_fraction"] = float((gain > 0).mean())
        summary.attrs["gain_ci"] = tuple(np.quantile(gain, [0.025, 0.975]))
    return summary


def tidy_fits(fits: Sequence[ModelFit], drop_const: bool = True) -> pd.DataFrame:
    """Stack several model fits into one comparable coefficient table."""
    frames: List[pd.DataFrame] = []
    for fit in fits:
        table = fit.coefficients.copy()
        table.insert(0, "model", fit.name)
        table.insert(1, "outcome", fit.outcome)
        table["n_obs"] = fit.n_obs
        table["n_clusters"] = fit.n_clusters
        table["r_squared"] = fit.r_squared
        if drop_const:
            table = table[table["term"] != "const"]
        frames.append(table)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
