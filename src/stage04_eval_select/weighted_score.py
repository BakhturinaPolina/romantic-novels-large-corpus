"""Weighted ranking utilities for Pareto-selected trial rows."""

from __future__ import annotations

import pandas as pd

from src.stage03_train.topic_size_metrics import topic_floor_score


def add_stability_penalty(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize stability into a penalty term (lower is better)."""
    out = df.copy()
    stab = out.get("stability_score")
    if stab is None:
        out["stability_penalty"] = 0.0
        return out
    max_abs = float(stab.abs().max()) if len(stab) else 0.0
    if max_abs == 0:
        out["stability_penalty"] = 0.0
    else:
        out["stability_penalty"] = (max_abs - stab.abs()) / max_abs
    return out


def apply_weighted_score(
    df: pd.DataFrame,
    w_coherence: float,
    w_diversity: float,
    w_outlier: float,
    w_stability: float,
    w_topic_count_floor: float = 0.0,
) -> pd.DataFrame:
    """Apply weighted objective score used after Pareto filtering."""
    out = add_stability_penalty(df)
    outlier = (
        out["outlier_rate"].fillna(0.0)
        if "outlier_rate" in out.columns
        else 0.0
    )
    if w_topic_count_floor > 0 and "n_topics" in out.columns:
        floor_term = out["n_topics"].apply(topic_floor_score)
    else:
        floor_term = 0.0
    out["weighted_score"] = (
        w_coherence * out["coherence_c_v"].fillna(0.0)
        + w_diversity * out["topic_diversity"].fillna(0.0)
        + w_topic_count_floor * floor_term
        - w_outlier * outlier
        - w_stability * out["stability_penalty"].fillna(0.0)
    )
    return out

