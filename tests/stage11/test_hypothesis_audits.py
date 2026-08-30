"""Spillover triage + Pass A/B/C audit runner tests (dry-run, no API)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.stage11_refined_construct_analysis.audits.prompts import (
    format_pass_messages,
    load_hypothesis_prompt,
)
from src.stage11_refined_construct_analysis.audits.runner import (
    ensure_packet,
    resolve_audit_topic_ids,
    run_hypothesis_audit,
    run_pass,
)
from src.stage11_refined_construct_analysis.audits.spillover import (
    build_h1_spillover_candidates,
    build_h3_spillover_candidates,
    load_spillover_prompt,
    run_spillover_triage,
    write_spillover_result,
)
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import (
    build_all_manifests,
    load_topic_lookup,
    write_manifests,
)

CFG = load_stage11_config(DEFAULT_CONFIG_PATH)


@pytest.fixture(scope="module")
def manifests():
    if not CFG.input_path("topic_lookup") or not CFG.input_path("topic_lookup").exists():
        pytest.skip("lookup missing")
    payload = build_all_manifests(CFG)
    write_manifests(CFG, payload)
    return payload


def test_spillover_prompt_frozen():
    prompt = load_spillover_prompt(CFG)
    assert prompt["frozen"] is True
    assert "primary" in prompt["phrasing"]


def test_h2_pass_b_shows_position(manifests):
    prompt = load_hypothesis_prompt(CFG, "H2")
    assert prompt.get("pass_b_shows_position") is True
    packet = {
        "topic_id": 29,
        "lexical": {
            "representations": {
                "Main": ["love"],
                "KeyBERT": ["forever"],
                "POS": ["said"],
                "MMR": ["promise"],
            }
        },
        "contextual": {
            "sentences": [
                {
                    "sid": "s1",
                    "cell": "CELL_A",
                    "tertile": "end",
                    "normalized_position": 0.92,
                    "max_topic_prob": 0.9,
                    "sentence": "I will marry you.",
                }
            ]
        },
        "pass_c_reveal": {},
    }
    msg = format_pass_messages(prompt, packet, phrasing="primary", pass_name="B")
    assert "tertile=end" in msg["user"]
    assert "CELL_A" in msg["user"]


def test_spillover_and_h1_h3_audits_dry_run(manifests):
    lookup = load_topic_lookup(CFG)
    h1_man = manifests["hypotheses"]["H1"]
    h3_man = manifests["hypotheses"]["H3"]

    h1_cands = build_h1_spillover_candidates(CFG, lookup, h1_man)
    assert h1_cands, "expected H1 spillover candidates from secondary/sexual flags"
    h1_result = run_spillover_triage(CFG, "H1", h1_cands[:8], dry_run=True)
    write_spillover_result(CFG, h1_result)
    assert h1_result["n_candidates"] == 8
    assert "promoted_topic_ids" in h1_result

    h3_cands = build_h3_spillover_candidates(CFG, lookup, h3_man)
    assert h3_cands, "expected H3 discovery-leaf candidates"
    h3_result = run_spillover_triage(CFG, "H3", h3_cands[:6], dry_run=True)
    write_spillover_result(CFG, h3_result)

    # Smoke: limited Pass A/B/C for H1 and H3
    s1 = run_hypothesis_audit(CFG, "H1", dry_run=True, resume=False, limit=3)
    assert s1["n_newly_audited"] == 3
    assert (CFG.output_path("audits_dir") / "h1" / "lexical.jsonl").exists()
    assert (CFG.output_path("audits_dir") / "h1" / "contextual.jsonl").exists()
    assert (CFG.output_path("audits_dir") / "h1" / "adjudication.jsonl").exists()

    s3 = run_hypothesis_audit(CFG, "H3", dry_run=True, resume=False, limit=3)
    assert s3["n_newly_audited"] == 3


def test_h4_reuses_h3_and_h2_position_audit(manifests):
    # Seed tiny H3 adjudication so H4 can load priors
    lookup = load_topic_lookup(CFG)
    leaf46 = lookup.loc[lookup["taxonomy_main_id"].astype(str) == "4.6", "topic_id"]
    if leaf46.empty:
        pytest.skip("no 4.6 topics")
    tid46 = int(leaf46.iloc[0])
    h3_dir = CFG.output_path("audits_dir", create=True) / "h3"
    h3_dir.mkdir(parents=True, exist_ok=True)
    (h3_dir / "adjudication.jsonl").write_text(
        json.dumps(
            {
                "topic_id": tid46,
                "code": "S5",
                "response": {"security_code": "S5", "action": "KEEP"},
            }
        )
        + "\n",
        encoding="utf-8",
    )

    # Exhaustive 4.7 topics must be in H4 pool
    h4_ids = resolve_audit_topic_ids(CFG, "H4", include_spillover=False)
    leaf47 = set(
        int(t)
        for t in lookup.loc[lookup["taxonomy_main_id"].astype(str) == "4.7", "topic_id"]
    )
    assert leaf47.issubset(set(h4_ids))
    assert len(leaf47) == 2

    s4 = run_hypothesis_audit(
        CFG,
        "H4",
        topic_ids=[tid46] + sorted(leaf47),
        dry_run=True,
        resume=False,
    )
    assert s4["n_newly_audited"] == 3
    assert s4["n_h3_priors_reused"] >= 1
    # Pass C for 4.6 should carry prior
    rows = [
        json.loads(line)
        for line in (CFG.output_path("audits_dir") / "h4" / "adjudication.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    prior_rows = [r for r in rows if int(r["topic_id"]) == tid46]
    assert prior_rows and prior_rows[0].get("prior_h3")

    # H2 pool size from live lookup (10, not hard-coded 11)
    h2 = run_hypothesis_audit(CFG, "H2", dry_run=True, resume=False)
    assert h2["n_topics"] == 10
    assert h2["n_newly_audited"] == 10
    assert len(manifests["integrity"]["h2_topic_ids"]) == 10


def test_ensure_packet_synthesizes_when_missing(manifests):
    packet = ensure_packet(CFG, topic_id=1, lookup=load_topic_lookup(CFG))
    assert packet["topic_id"] == 1
    assert "representations" in packet["lexical"]
    msg = run_pass(CFG, hypothesis="H1", packet=packet, pass_name="A", dry_run=True)
    assert msg["code"] == "I3"  # known kissing/explicit trap topic
