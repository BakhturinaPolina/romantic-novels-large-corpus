"""Master annotation table scaffolding tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.stage11_refined_construct_analysis.analysis.master import (
    build_W_tk,
    build_master_annotations,
    write_master_artifacts,
)
from src.stage11_refined_construct_analysis.audits.runner import audit_dir
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def _seed_minimal_audits():
    """Write tiny dry-run style adjudication so master builder has input."""
    for hyp, code, field in (
        ("H1", "I3", "intimacy_code"),
        ("H2", "H2_1", "hea_code"),
        ("H3", "S5", "security_code"),
        ("H4", "H4_1", "care_protection_code"),
        ("H5", "D1", "darkness_code"),
        ("H6", "ARC_2", "arc_role"),
    ):
        d = audit_dir(CFG, hyp)
        d.mkdir(parents=True, exist_ok=True)
        for pass_name, fname in (
            ("A", "lexical.jsonl"),
            ("B", "contextual.jsonl"),
            ("C", "adjudication.jsonl"),
        ):
            row = {
                "topic_id": 1,
                "hypothesis": hyp,
                "pass": pass_name,
                "code": code,
                "dry_run": True,
                "response": {
                    "consensus_code": code,
                    "dominant_code": code,
                    field: code,
                    "action": "KEEP",
                    "proportions": {code: 0.8},
                    "main_couple": True,
                    "proposed_constructs": [code],
                },
            }
            path = d / fname
            # append seed without wiping live runs if present
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            if '"topic_id": 1' in existing or '"topic_id":1' in existing:
                continue
            with path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row) + "\n")


def test_master_builder_smoke():
    if not CFG.input_path("topic_lookup") or not CFG.input_path("topic_lookup").exists():
        pytest.skip("lookup missing")
    _seed_minimal_audits()
    master = build_master_annotations(CFG)
    assert len(master) >= 1
    assert "intimacy_code" in master.columns
    assert "arc_role" in master.columns
    w = build_W_tk(master, mode="strict")
    assert not w.empty
    paths = write_master_artifacts(CFG)
    assert paths["master"].exists()
    assert paths["freeze"].exists()
    freeze = json.loads(paths["freeze"].read_text(encoding="utf-8"))
    assert freeze["frozen"] is True
