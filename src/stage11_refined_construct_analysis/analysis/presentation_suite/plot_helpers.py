"""Shared plotting helpers for categorical y-axes and label alignment."""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes


def categorical_y_positions(n: int) -> np.ndarray:
    """Return 0..n-1 y positions; row 0 is plotted at top after invert_yaxis."""
    return np.arange(n)


def apply_categorical_y_axis(ax: Axes, y: np.ndarray, labels: Sequence[str]) -> None:
    """Set y ticks/labels with row 0 at the top."""
    ax.set_yticks(y)
    ax.set_yticklabels(list(labels))
    ax.invert_yaxis()


def categorical_ylim(n: int, *, pad: float = 0.5) -> Tuple[float, float]:
    """Fixed y limits for animation frames with n categorical rows."""
    return (-pad, n - 1 + pad)


def extract_barh_label_values(ax: Axes) -> List[Tuple[str, float]]:
    """Return (tick_label, bar_width) pairs; row 0 at top after invert_yaxis."""
    tick_labels = [t.get_text() for t in ax.get_yticklabels()]
    tick_locs = list(ax.get_yticks())
    loc_to_label = dict(zip(tick_locs, tick_labels))
    loc_to_width: dict[float, float] = {}
    for patch in ax.patches:
        if patch.get_height() <= 0:
            continue
        yi = patch.get_y() + patch.get_height() / 2
        nearest = min(tick_locs, key=lambda t: abs(t - yi)) if tick_locs else yi
        loc_to_width[nearest] = float(patch.get_width())
    pairs: List[Tuple[str, float]] = []
    for loc in sorted(tick_locs):
        label = loc_to_label.get(loc, "")
        if label and loc in loc_to_width:
            pairs.append((label, loc_to_width[loc]))
    return pairs


def extract_scatter_x_at_y(ax: Axes) -> List[Tuple[str, float]]:
    """Return (tick_label, scatter_x) for horizontal categorical scatter/errorbar plots."""
    tick_labels = [t.get_text() for t in ax.get_yticklabels()]
    tick_locs = list(ax.get_yticks())
    loc_to_label = dict(zip(tick_locs, tick_labels))
    results: List[Tuple[str, float]] = []
    for coll in ax.collections:
        offsets = coll.get_offsets()
        if len(offsets) == 0:
            continue
        for x, y in offsets:
            yi = float(y)
            if tick_locs:
                nearest = min(tick_locs, key=lambda t: abs(t - yi))
                label = loc_to_label.get(nearest, "")
            else:
                label = ""
            results.append((label, float(x)))
    # Deduplicate by label (keep first scatter x)
    seen: dict[str, float] = {}
    for label, x in results:
        if label and label not in seen:
            seen[label] = x
    tick_order = [loc_to_label[t] for t in sorted(tick_locs)]
    return [(lb, seen[lb]) for lb in tick_order if lb in seen]


def assert_label_value_alignment(
    labels: Sequence[str],
    values: Sequence[float],
    expected_labels: Sequence[str],
    expected_values: Sequence[float],
    *,
    tol: float = 1e-6,
) -> None:
    """Assert displayed labels match expected row order and values."""
    assert list(labels) == list(expected_labels), f"Label mismatch: {labels} vs {expected_labels}"
    assert len(values) == len(expected_values), f"Value count mismatch: {len(values)} vs {len(expected_values)}"
    for got, exp in zip(values, expected_values):
        if pd.isna(exp):
            continue
        assert abs(got - exp) < tol, f"Value mismatch: {got} vs {exp}"
