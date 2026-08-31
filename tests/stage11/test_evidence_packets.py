"""Unit tests for Stage 11 evidence blinding and lexical packet assembly."""

from __future__ import annotations

import json

import pandas as pd
import pytest

from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.evidence.blinding import (
    apply_cell_blind,
    load_or_create_cell_key,
    seal_cell_key,
    unblind_cell,
)
from src.stage11_refined_construct_analysis.evidence.human_review import (
    build_human_review_packet,
)
from src.stage11_refined_construct_analysis.evidence.packets import (
    build_evidence_packet,
    lexical_block,
    llm_view,
    load_topic_metadata,
    sample_prevalence_rating_books,
)
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def require_lookup():
    path = CFG.input_path("topic_lookup")
    if path is None or not path.exists():
        pytest.skip(f"topic_lookup not available: {path}")
    return load_topic_lookup(CFG)


def test_cell_key_seal_and_unblind():
    key = load_or_create_cell_key(CFG)
    path = seal_cell_key(CFG, key)
    assert path.exists()
    sealed = json.loads(path.read_text(encoding="utf-8"))
    assert set(sealed["labels"]) == {"CELL_A", "CELL_B", "CELL_C", "CELL_D"}
    assert unblind_cell("CELL_A", key) == "high_prevalence_high_tier"


def test_apply_cell_blind_drops_rating_tier():
    key = load_or_create_cell_key(CFG)
    row = {
        "cell_meaning": "high_prevalence_low_tier",
        "rating_class": "low_rate",
        "rating_tier": "low_rate",
    }
    apply_cell_blind(row, key)
    assert row["cell"] == "CELL_B"
    assert "rating_class" not in row
    assert "rating_tier" not in row
    assert "cell_meaning" not in row


def test_prevalence_rating_sampler_returns_blindable_cells():
    frame = pd.DataFrame(
        {
            "book_id": list(range(20)),
            "share": [0.2] * 5 + [0.01] * 5 + [0.2] * 5 + [0.0] * 5,
            "n_sentences": [10] * 15 + [0] * 5,
            "rating_class": (
                ["high_rate"] * 5
                + ["high_rate"] * 5
                + ["low_rate"] * 5
                + ["low_rate"] * 5
            ),
        }
    )
    sampled = sample_prevalence_rating_books(
        frame,
        tier_column="rating_class",
        tier_high="high_rate",
        tier_low="low_rate",
        quantiles=(0.25, 0.75),
        books_per_cell=2,
        seed=42,
    )
    assert not sampled.empty
    assert set(sampled["cell_meaning"]).issubset(
        {
            "high_prevalence_high_tier",
            "high_prevalence_low_tier",
            "low_prevalence_high_tier",
            "low_prevalence_low_tier",
        }
    )
    # Positive-share only: zero-mass books must not enter review cells.
    assert (sampled["share"] > 0).all()
    assert (sampled["n_sentences"] > 0).all()


def test_prevalence_rating_sampler_backfills_thin_low_cells():
    # Only one book at the low quantile per tier; backfill should still fill quota.
    rows = []
    bid = 0
    for tier in ("high_rate", "low_rate"):
        rows.append({"book_id": bid, "share": 0.01, "n_sentences": 3, "rating_class": tier})
        bid += 1
        for _ in range(6):
            rows.append({"book_id": bid, "share": 0.2, "n_sentences": 8, "rating_class": tier})
            bid += 1
    frame = pd.DataFrame(rows)
    sampled = sample_prevalence_rating_books(
        frame,
        tier_column="rating_class",
        tier_high="high_rate",
        tier_low="low_rate",
        quantiles=(0.25, 0.75),
        books_per_cell=3,
        seed=7,
    )
    counts = sampled.groupby("cell_meaning").size()
    assert counts.get("low_prevalence_high_tier", 0) == 3
    assert counts.get("low_prevalence_low_tier", 0) == 3
    assert (sampled["share"] > 0).all()


def test_lexical_packet_has_four_representations():
    meta_path = CFG.input_path("topic_metadata")
    if meta_path is None or not meta_path.exists():
        pytest.skip("topic metadata missing")
    metadata = load_topic_metadata(CFG)
    block = lexical_block(1, metadata)
    reps = block["representations"]
    for name in ("Main", "KeyBERT", "POS", "MMR"):
        assert name in reps
        assert isinstance(reps[name], list)


def test_llm_view_hides_taxonomy_until_pass_c():
    lookup = require_lookup()
    meta_path = CFG.input_path("topic_metadata")
    if meta_path is None or not meta_path.exists():
        pytest.skip("topic metadata missing")
    metadata = load_topic_metadata(CFG)
    counts_path = CFG.input_path("book_topic_counts")
    frame_path = CFG.input_path("analysis_frame")
    if not counts_path or not counts_path.exists() or not frame_path or not frame_path.exists():
        pytest.skip("book counts / frame missing")

    counts = pd.read_parquet(counts_path)
    frame = pd.read_parquet(frame_path, columns=["book_id", "rating_class"])
    key = load_or_create_cell_key(CFG)
    packet = build_evidence_packet(
        CFG,
        167,  # 5.3a exhaustive thin leaf
        lookup=lookup,
        metadata=metadata,
        representative_docs={},
        book_topic_counts=counts,
        analysis_frame=frame,
        cell_key=key,
        include_contextual=False,
    )
    assert packet["exhaustive"] is True
    view_a = llm_view(packet, pass_name="A")
    assert "pass_c_reveal" not in view_a
    view_c = llm_view(packet, pass_name="C")
    assert view_c["pass_c_reveal"]["taxonomy_main_id"] == "5.3a"

    review = build_human_review_packet(packet)
    assert review["taxonomy_main_id"] == "5.3a"
    assert "representations" in review
