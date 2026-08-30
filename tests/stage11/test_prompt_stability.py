"""Prompt freeze + stability pilot scaffolding tests."""

from __future__ import annotations

import importlib
import json

import pytest

from src.stage11_refined_construct_analysis.audits.prompts import (
    format_pass_messages,
    list_code_ids,
    load_hypothesis_prompt,
)
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


def test_all_prompts_frozen_with_two_phrasings():
    for hyp in ("H1", "H2", "H3", "H4", "H5", "H6"):
        prompt = load_hypothesis_prompt(CFG, hyp)
        assert prompt["frozen"] is True
        assert "primary" in prompt["phrasing"]
        assert "alternate" in prompt["phrasing"]
        assert list_code_ids(prompt)


def test_format_pass_a_uses_four_reps_without_taxonomy_leak():
    prompt = load_hypothesis_prompt(CFG, "H1")
    packet = {
        "topic_id": 1,
        "lexical": {
            "representations": {
                "Main": ["kiss"],
                "KeyBERT": ["stroking"],
                "POS": ["moves"],
                "MMR": ["panting"],
            }
        },
        "contextual": {"sentences": []},
        "pass_c_reveal": {},
    }
    msg = format_pass_messages(prompt, packet, phrasing="primary", pass_name="A")
    assert "kiss" in msg["user"]
    assert "stroking" in msg["user"]
    assert "2.3" not in msg["user"]


def test_stability_pilot_dry_run_writes_summary():
    """End-to-end dry-run of the stability pilot with lexical-only packets."""
    if not CFG.input_path("topic_lookup") or not CFG.input_path("topic_lookup").exists():
        pytest.skip("lookup missing")

    mod = importlib.import_module(
        "src.stage11_refined_construct_analysis.pipeline.03_run_stability_pilot"
    )
    rc = mod.main(["--dry-run", "--lexical-only", "--hypotheses", "H1,H2,H3,H4"])
    assert rc == 0
    summary_path = CFG.output_path("stability_pilot_dir") / "pilot_summary.json"
    assert summary_path.exists()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["dry_run"] is True
    assert summary["n_topics"] >= 10
    assert "phrasing_agreement" in summary
    refine = CFG.output_path("stability_pilot_dir") / "refine_notes.md"
    assert refine.exists()
