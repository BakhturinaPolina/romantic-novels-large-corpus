"""Topic-count stability helpers for BO and compare-fit gating."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def topic_run_stats(counts: list[float] | list[int]) -> dict[str, float]:
    """Summarize topic counts across repeated fits."""
    if not counts:
        return {
            "min": float("nan"),
            "median": float("nan"),
            "max": float("nan"),
            "std": float("nan"),
            "range": float("nan"),
            "n_runs": 0.0,
        }
    arr = np.asarray(counts, dtype=float)
    return {
        "min": float(np.min(arr)),
        "median": float(np.median(arr)),
        "max": float(np.max(arr)),
        "std": float(np.std(arr)) if arr.size > 1 else 0.0,
        "range": float(np.max(arr) - np.min(arr)),
        "n_runs": float(arr.size),
    }


def stability_pass(
    counts: list[float] | list[int],
    *,
    max_std: float = 3.0,
    collapse_ratio: float = 0.5,
) -> bool:
    """Return True when topic counts are stable across runs.

    Legacy single-run iterations (len==1) always pass.
    """
    if len(counts) <= 1:
        return True
    stats = topic_run_stats(counts)
    if math.isnan(stats["median"]) or stats["median"] <= 0:
        return False
    if stats["std"] > max_std:
        return False
    if stats["min"] < collapse_ratio * stats["median"]:
        return False
    return True


def stability_violation(
    counts: list[float] | list[int],
    *,
    max_std: float = 3.0,
    collapse_ratio: float = 0.5,
) -> float:
    """Normalized violation in [0, inf); 0 means stable."""
    if len(counts) <= 1:
        return 0.0
    stats = topic_run_stats(counts)
    if math.isnan(stats["median"]) or stats["median"] <= 0:
        return 1.0
    std_violation = max(0.0, (stats["std"] - max_std) / max(max_std, 1.0))
    floor = collapse_ratio * stats["median"]
    collapse_violation = 0.0
    if stats["min"] < floor:
        collapse_violation = (floor - stats["min"]) / max(stats["median"], 1.0)
    return max(std_violation, collapse_violation)


def stability_penalty(
    median_score: float,
    counts: list[float] | list[int],
    *,
    max_std: float = 3.0,
    collapse_ratio: float = 0.5,
    weight: float = 0.2,
) -> float:
    """Subtract weighted stability violation from the BO objective."""
    violation = stability_violation(
        counts,
        max_std=max_std,
        collapse_ratio=collapse_ratio,
    )
    if violation <= 0.0:
        return float(median_score)
    return float(median_score) - weight * violation


def refit_collapse_flag(
    refit_median: float,
    reported_n_topics: float,
    *,
    collapse_ratio: float = 0.5,
) -> bool:
    """True when compare-fit median topics is far below BO-reported count."""
    if math.isnan(reported_n_topics) or reported_n_topics <= 0:
        return False
    if math.isnan(refit_median):
        return True
    return refit_median < collapse_ratio * reported_n_topics


def stability_config_from_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    """Parse ``optimization.topic_stability`` from train config."""
    opt = cfg.get("optimization", {})
    block = opt.get("topic_stability", {}) or {}
    return {
        "enabled": bool(block.get("enabled", False)),
        "max_n_topics_std": float(block.get("max_n_topics_std", 3.0)),
        "collapse_ratio": float(block.get("collapse_ratio", 0.5)),
        "penalty_weight": float(block.get("penalty_weight", 0.2)),
        "base_seed": int(opt.get("seed", 42)),
    }
