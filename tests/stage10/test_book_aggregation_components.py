"""Tests for ID-based component sums in book aggregation."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd

_AGG_PATH = (
    Path(__file__).resolve().parents[2]
    / "src/stage10_correlation_analysis/data_preparation/02_book_aggregation.py"
)
_spec = importlib.util.spec_from_file_location("book_aggregation", _AGG_PATH)
assert _spec and _spec.loader
agg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agg)


def test_component_ids_cover_schema_anchors():
    """Every COMPONENT_TAXONOMY_IDS entry should use valid v2.2 leaf ids."""
    from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
        valid_taxonomy_ids,
    )

    valid = valid_taxonomy_ids()
    for comp, ids in agg.COMPONENT_TAXONOMY_IDS.items():
        assert ids, f"empty id list for {comp}"
        for cid in ids:
            assert cid in valid, f"{comp} references unknown id {cid}"


def test_sum_taxonomy_id_columns_weighted():
    wide = pd.DataFrame({"4.5": [0.4], "3.1": [0.6]}, index=[1])
    payoff = agg.sum_taxonomy_id_columns(wide, ["4.5", "3.1"])
    assert float(payoff.iloc[0]) == 1.0

    weighted = agg.sum_taxonomy_id_columns(
        wide, ["4.5", "3.1"], {"4.5": 1.0, "3.1": 0.5, "default": 1.0}
    )
    assert float(weighted.iloc[0]) == 0.7


if __name__ == "__main__":
    test_component_ids_cover_schema_anchors()
    test_sum_taxonomy_id_columns_weighted()
    print("book aggregation component tests passed.")
