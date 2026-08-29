"""Nonparametric tests and multiplicity control.

Design decisions worth stating once:

* **Nonparametric throughout.** Topic shares are bounded, zero-inflated and right-skewed;
  rating distributions are truncated. Rank-based tests need none of the assumptions that
  a t-test or ANOVA would violate here.
* **Two-level correction.** Holm *within* a family of pairwise contrasts (strong control of
  the familywise error rate on a small set), Benjamini-Hochberg *across* the family of
  features (false discovery rate on 374 topics, where familywise control would be
  hopelessly conservative).
* **Families are corrected separately.** 374 topics, ~45 taxonomy leaves, ~11 main groups,
  ~22 axes and 6 hypotheses are five independent families. Pooling them would let the
  large topic family swallow the alpha budget of the small hypothesis family.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats as sps

from src.stage10_correlation_analysis.analysis import effects as eff


def kruskal_wallis(
    frame: pd.DataFrame,
    value_columns: Sequence[str],
    group_column: str,
    group_order: Sequence[str],
) -> pd.DataFrame:
    """Omnibus test of "do the tiers differ at all", with epsilon-squared alongside."""
    rows: List[Dict[str, object]] = []
    for col in value_columns:
        groups = [
            frame.loc[frame[group_column] == g, col].dropna().to_numpy(dtype=float)
            for g in group_order
        ]
        groups = [g for g in groups if g.size > 1]
        if len(groups) < 2:
            continue
        if all(np.allclose(g, groups[0][0]) for g in groups):
            stat, p_value = 0.0, 1.0
        else:
            stat, p_value = sps.kruskal(*groups)
        rows.append({
            "feature": col,
            "kw_statistic": float(stat),
            "p_value": float(p_value),
            "epsilon_squared": eff.epsilon_squared(groups),
            "n_groups": len(groups),
            "n_total": int(sum(g.size for g in groups)),
        })
    out = pd.DataFrame(rows)
    return out.sort_values("epsilon_squared", ascending=False).reset_index(drop=True) if len(out) else out


def mann_whitney(
    a: Iterable[float],
    b: Iterable[float],
    alternative: str = "two-sided",
) -> Tuple[float, float]:
    a_arr = np.asarray(list(a), dtype=float)
    b_arr = np.asarray(list(b), dtype=float)
    a_arr, b_arr = a_arr[np.isfinite(a_arr)], b_arr[np.isfinite(b_arr)]
    if a_arr.size < 1 or b_arr.size < 1:
        return float("nan"), float("nan")
    stat, p_value = sps.mannwhitneyu(a_arr, b_arr, alternative=alternative)
    return float(stat), float(p_value)


def pairwise_mann_whitney(
    frame: pd.DataFrame,
    value_columns: Sequence[str],
    group_column: str,
    contrasts: Sequence[Tuple[str, str]],
    *,
    holm_within_feature: bool = True,
) -> pd.DataFrame:
    """All requested tier contrasts, with Holm applied within each feature's contrast set."""
    rows: List[Dict[str, object]] = []
    for col in value_columns:
        for group_a, group_b in contrasts:
            a_vals = frame.loc[frame[group_column] == group_a, col].dropna().to_numpy(dtype=float)
            b_vals = frame.loc[frame[group_column] == group_b, col].dropna().to_numpy(dtype=float)
            if a_vals.size < 2 or b_vals.size < 2:
                continue
            stat, p_value = mann_whitney(a_vals, b_vals)
            delta = eff.cliffs_delta(a_vals, b_vals)
            rows.append({
                "feature": col,
                "group_a": group_a,
                "group_b": group_b,
                "mw_statistic": stat,
                "p_value": p_value,
                "cliffs_delta": delta,
                "magnitude": eff.magnitude(delta),
                "median_a": float(np.median(a_vals)),
                "median_b": float(np.median(b_vals)),
                "n_a": int(a_vals.size),
                "n_b": int(b_vals.size),
            })

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    if holm_within_feature:
        out["p_holm_within_feature"] = (
            out.groupby("feature")["p_value"].transform(lambda s: holm(s.to_numpy()))
        )
    return out.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Multiplicity
# ---------------------------------------------------------------------------

def holm(p_values: np.ndarray) -> np.ndarray:
    """Holm-Bonferroni adjusted p-values. Controls the familywise error rate."""
    p = np.asarray(p_values, dtype=float)
    finite = np.isfinite(p)
    out = np.full(p.shape, np.nan)
    if not finite.any():
        return out

    vals = p[finite]
    n = vals.size
    order = np.argsort(vals)
    adjusted = np.empty(n)
    running = 0.0
    for rank, idx in enumerate(order):
        candidate = (n - rank) * vals[idx]
        running = max(running, candidate)
        adjusted[idx] = min(1.0, running)
    out[finite] = adjusted
    return out


def benjamini_hochberg(p_values: np.ndarray) -> np.ndarray:
    """BH adjusted p-values (q-values). Controls the false discovery rate."""
    p = np.asarray(p_values, dtype=float)
    finite = np.isfinite(p)
    out = np.full(p.shape, np.nan)
    if not finite.any():
        return out

    vals = p[finite]
    n = vals.size
    order = np.argsort(vals)
    ranked = vals[order]
    scaled = ranked * n / np.arange(1, n + 1)
    # Enforce monotonicity from the largest p downward.
    adjusted_sorted = np.minimum.accumulate(scaled[::-1])[::-1]
    adjusted = np.empty(n)
    adjusted[order] = np.minimum(adjusted_sorted, 1.0)
    out[finite] = adjusted
    return out


def adjust_within_family(
    frame: pd.DataFrame,
    p_column: str = "p_value",
    family_column: Optional[str] = None,
    *,
    method: str = "fdr_bh",
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Add adjusted p-values, computed independently within each family."""
    func = {"fdr_bh": benjamini_hochberg, "holm": holm}[method]
    out = frame.copy()
    suffix = "q_value" if method == "fdr_bh" else "p_holm"

    if family_column is None:
        out[suffix] = func(out[p_column].to_numpy())
    else:
        out[suffix] = (
            out.groupby(family_column)[p_column]
            .transform(lambda s: func(s.to_numpy()))
        )
    out[f"{suffix}_significant"] = out[suffix] < alpha
    return out


# ---------------------------------------------------------------------------
# Screening funnel
# ---------------------------------------------------------------------------

def screening_funnel(
    screen_table: pd.DataFrame,
    effect_table: pd.DataFrame,
    *,
    min_abs_delta: float,
    require_ci_excludes_zero: bool = True,
    alpha: float = 0.05,
    q_column: str = "q_value",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Combine prevalence screening, effect size and FDR into a reportable funnel.

    Returns (funnel_counts, annotated_effects). At this sample size the funnel is the
    honest summary: how many features survive each requirement, and which survive all of
    them. Reporting only the final count would hide that the statistical gate is nearly
    free and the effect-size gate does all the work.
    """
    merged = effect_table.merge(
        screen_table.reset_index().rename(columns={"index": "feature"}),
        on="feature", how="left",
    )
    merged["passes_effect"] = merged["cliffs_delta"].abs() >= min_abs_delta
    merged["passes_ci"] = merged.get("ci_excludes_zero", True)
    if q_column in merged.columns:
        merged["passes_fdr"] = merged[q_column] < alpha
    else:
        merged["passes_fdr"] = True

    conditions = ["passes_screen", "passes_fdr", "passes_effect"]
    if require_ci_excludes_zero:
        conditions.append("passes_ci")
    merged["passes_all"] = merged[conditions].fillna(False).all(axis=1)

    stages: List[Dict[str, object]] = [
        {"stage": "all features tested", "n": int(len(merged))},
    ]
    cumulative = pd.Series(True, index=merged.index)
    labels = {
        "passes_screen": "present in enough books and carries enough mass",
        "passes_fdr": f"survives BH-FDR at alpha={alpha}",
        "passes_effect": f"|Cliff's delta| >= {min_abs_delta}",
        "passes_ci": "bootstrap CI excludes zero",
    }
    for cond in conditions:
        cumulative = cumulative & merged[cond].fillna(False)
        stages.append({"stage": labels[cond], "n": int(cumulative.sum())})

    return pd.DataFrame(stages), merged


def compare_tier_trend(
    frame: pd.DataFrame,
    value_columns: Sequence[str],
    group_column: str,
    group_order: Sequence[str],
) -> pd.DataFrame:
    """Monotone trend across ordered tiers, via Spearman on the tier index.

    Distinguishes "high differs from low" from "the feature increases steadily with
    rating", which is a stronger and more interpretable claim.
    """
    tier_index = {g: i for i, g in enumerate(group_order)}
    subset = frame[frame[group_column].isin(tier_index)].copy()
    subset["_tier_num"] = subset[group_column].map(tier_index)

    rows: List[Dict[str, object]] = []
    for col in value_columns:
        valid = subset[[col, "_tier_num"]].dropna()
        if len(valid) < 10 or valid[col].nunique() < 2:
            continue
        rho, p_value = sps.spearmanr(valid["_tier_num"], valid[col])
        rows.append({
            "feature": col,
            "spearman_rho": float(rho),
            "p_value": float(p_value),
            "direction": "rises with rating" if rho > 0 else "falls with rating",
            "n": int(len(valid)),
        })
    out = pd.DataFrame(rows)
    return out.sort_values("spearman_rho", key=lambda s: s.abs(), ascending=False).reset_index(drop=True) if len(out) else out
