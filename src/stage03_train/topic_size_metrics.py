"""Topic-size distribution helpers for granular BERTopic BO diagnostics."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def topic_size_stats_from_counts(sizes: np.ndarray, n_fit_docs: int) -> dict[str, float]:
    """Compute topic-size distribution metrics from non-outlier topic counts."""
    nan = {
        "largest_topic_share": float("nan"),
        "median_topic_size": float("nan"),
        "p10_topic_size": float("nan"),
        "p90_topic_size": float("nan"),
        "n_tiny_topics_lt25": float("nan"),
        "n_tiny_topics_lt50": float("nan"),
    }
    if n_fit_docs <= 0 or sizes.size == 0:
        return nan
    return {
        "largest_topic_share": float(sizes.max() / n_fit_docs),
        "median_topic_size": float(np.median(sizes)),
        "p10_topic_size": float(np.percentile(sizes, 10)),
        "p90_topic_size": float(np.percentile(sizes, 90)),
        "n_tiny_topics_lt25": float(int((sizes < 25).sum())),
        "n_tiny_topics_lt50": float(int((sizes < 50).sum())),
    }


def topic_size_stats_from_topic_info(topic_info: Any, n_fit_docs: int) -> dict[str, float]:
    """Build stats dict from a BERTopic ``get_topic_info()`` frame."""
    if topic_info is None or len(topic_info) == 0:
        return topic_size_stats_from_counts(np.array([]), n_fit_docs)
    non_outlier = topic_info.loc[topic_info["Topic"] != -1, "Count"]
    sizes = non_outlier.to_numpy(dtype=float)
    return topic_size_stats_from_counts(sizes, n_fit_docs)


def topic_floor_score(n_topics: float) -> float:
    """Soft reward for useful granularity (floor 50, plateau to 500, decay above)."""
    if math.isnan(n_topics):
        return 0.0
    n = int(n_topics)
    if n < 50:
        return n / 50.0
    if n <= 500:
        return 1.0
    if n <= 800:
        return 0.85
    return 0.50
