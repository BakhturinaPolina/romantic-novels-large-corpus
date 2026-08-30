"""Lookup-driven integrity asserts for Stage 11 (H2 pool, 7.2 count, empty leaves)."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import (
    build_all_manifests,
    build_hypothesis_manifest,
    leaf_pool,
    load_topic_lookup,
    run_lookup_integrity,
    topics_for_leaves,
)

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def require_lookup():
    path = CFG.input_path("topic_lookup")
    if path is None or not path.exists():
        pytest.skip(f"topic_lookup not available: {path}")
    return load_topic_lookup(CFG)


def test_config_loads_and_prompt_files_exist():
    assert CFG.run_id
    prompts_dir = CFG.root / "configs" / "stage11" / "prompts"
    for name in (
        "h1_intimacy.yaml",
        "h2_hea.yaml",
        "h3_security.yaml",
        "h4_protection.yaml",
        "h5_darkness.yaml",
        "h6_arc.yaml",
    ):
        assert (prompts_dir / name).exists()


def test_h2_pool_is_ten_not_eleven():
    lookup = require_lookup()
    report = run_lookup_integrity(CFG, lookup)
    assert report.ok, [c for c in report.checks if not c["ok"]]
    assert len(report.h2_topic_ids) == 10
    by_leaf = {c["name"]: c for c in report.checks}
    assert by_leaf["h2_leaf_4.5"]["n_topics"] == 8
    assert by_leaf["h2_leaf_5.3a"]["n_topics"] == 1
    assert by_leaf["h2_leaf_8.3a"]["n_topics"] == 1


def test_leaf_7_2_has_twelve_topics():
    lookup = require_lookup()
    pool = leaf_pool(lookup, "7.2")
    assert pool.n_topics == 12
    assert 91 not in pool.topic_ids


def test_topic_91_is_7_1_not_7_2():
    lookup = require_lookup()
    row = lookup.loc[lookup["topic_id"] == 91].iloc[0]
    assert str(row["taxonomy_main_id"]) == "7.1"


def test_empty_leaves_remain_unmeasurable():
    lookup = require_lookup()
    for leaf in ("2.4", "6.1a", "6.7"):
        assert leaf_pool(lookup, leaf).empty


def test_h2_manifest_derives_ids_from_lookup():
    lookup = require_lookup()
    man = build_hypothesis_manifest(CFG, lookup, "H2")
    assert man["n_topics"] == 10
    expected = topics_for_leaves(lookup, ["4.5", "5.3a", "8.3a"])
    assert man["topic_ids"] == expected


def test_exhaustive_leaves_flagged():
    lookup = require_lookup()
    payload = build_all_manifests(CFG, lookup)
    exhaustive = set(payload["exhaustive_topic_ids"])
    # 5.3a, 8.3a, both 4.7
    assert exhaustive == {61, 167, 293, 315}


def test_output_tree_scaffold():
    dirs = CFG.ensure_output_tree()
    assert dirs["candidates"].is_dir()
    assert dirs["evidence_packets"].is_dir()
    assert dirs["stability_pilot"].is_dir()
    assert (dirs["audits"] / "h1").is_dir()
