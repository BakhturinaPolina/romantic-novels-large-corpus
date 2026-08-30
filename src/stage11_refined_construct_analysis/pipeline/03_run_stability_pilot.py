#!/usr/bin/env python3
"""Pre-batch prompt stability pilot (two phrasings and/or two models).

Runs 10–15 difficult topics through meaning-equivalent prompt variants before the
full H1–H6 batch. If agreement falls below the configured threshold, definitions
must be refined before examining ratings.

Supports --dry-run (no API) for CI / scaffolding. Real calls need OPENROUTER_API_KEY.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.audits.prompts import (  # noqa: E402
    format_pass_messages,
    list_code_ids,
    load_hypothesis_prompt,
)
from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.evidence.packets import (  # noqa: E402
    build_evidence_packet,
    load_representative_docs,
    load_topic_metadata,
    llm_view,
    write_evidence_packets,
)
from src.stage11_refined_construct_analysis.evidence.blinding import (  # noqa: E402
    load_or_create_cell_key,
    seal_cell_key,
)
from src.stage11_refined_construct_analysis.lookup import (  # noqa: E402
    load_topic_lookup,
    run_lookup_integrity,
)

LOGGER = logging.getLogger("stage11.stability")

CODE_RE = re.compile(r"\b(I\d+|H2_\d+|S\d+|H4_\d+|D\d+|ARC_\d+|MIXED)\b")


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return {"raw": text, "parse_error": True}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"raw": text, "parse_error": True}


def _consensus_code(payload: Mapping[str, Any], valid_codes: Sequence[str]) -> str:
    for key in ("consensus_code", "dominant_code", "intimacy_code", "hea_code",
                "security_code", "care_protection_code", "darkness_code", "arc_role"):
        val = payload.get(key)
        if isinstance(val, str) and val:
            return val
    blob = json.dumps(payload)
    hits = [m for m in CODE_RE.findall(blob) if m in set(valid_codes) or m == "MIXED"]
    return hits[0] if hits else "UNKNOWN"


def _dry_run_response(topic_id: int, hypothesis: str, phrasing: str, model: str) -> Dict[str, Any]:
    """Deterministic pseudo-label for CI after codebook refinement (I3≠I6 boundary)."""
    code = {
        ("H1", 1, "primary"): "I3",
        ("H1", 1, "alternate"): "I3",
        ("H1", 7, "primary"): "I3",
        ("H1", 7, "alternate"): "I3",
        ("H2", 29, "primary"): "H2_1",
        ("H2", 29, "alternate"): "H2_1",
        ("H2", 167, "primary"): "H2_4",
        ("H2", 167, "alternate"): "H2_4",
        ("H3", 18, "primary"): "S13",
        ("H3", 18, "alternate"): "S13",
        ("H4", 293, "primary"): "H4_7",
        ("H4", 293, "alternate"): "H4_7",
    }.get((hypothesis, int(topic_id), phrasing), "I0")
    return {
        "topic_id": int(topic_id),
        "consensus_code": code,
        "disagreement": False,
        "rationale": f"dry-run {hypothesis} {phrasing} {model}",
        "dry_run": True,
    }


def call_openrouter(
    *,
    model: str,
    system: str,
    user: str,
    temperature: float,
    max_tokens: int,
    api_key: str,
    base_url: str = "https://openrouter.ai/api/v1",
) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content or ""


def resolve_hard_topics(cfg, lookup) -> List[int]:
    configured = [int(t) for t in cfg.section("stability_pilot", "hard_topic_ids")]
    present = set(int(t) for t in lookup["topic_id"].tolist())
    resolved = [t for t in configured if t in present]
    n = int(cfg.section("stability_pilot", "n_topics"))
    if len(resolved) < n:
        LOGGER.warning(
            "Only %d/%d configured hard topics present in lookup", len(resolved), n
        )
    return resolved[:n]


def run_condition(
    *,
    cfg,
    hypothesis: str,
    packet: Mapping[str, Any],
    phrasing: str,
    model: str,
    dry_run: bool,
    api_key: str,
) -> Dict[str, Any]:
    prompt = load_hypothesis_prompt(cfg, hypothesis)
    valid = list(list_code_ids(prompt)) + ["MIXED"]
    view = llm_view(packet, pass_name="A")
    messages = format_pass_messages(prompt, view, phrasing=phrasing, pass_name="A")

    if dry_run or not api_key:
        parsed = _dry_run_response(packet["topic_id"], hypothesis, phrasing, model)
        raw = json.dumps(parsed)
    else:
        raw = call_openrouter(
            model=model,
            system=messages["system"],
            user=messages["user"],
            temperature=float(cfg.section("llm", "temperature")),
            max_tokens=int(cfg.section("llm", "max_tokens")),
            api_key=api_key,
        )
        parsed = _extract_json(raw)
        time.sleep(float(cfg.section("llm", "rate_limit_delay_s")))

    code = _consensus_code(parsed, valid)
    return {
        "hypothesis": hypothesis,
        "topic_id": int(packet["topic_id"]),
        "phrasing": phrasing,
        "model": model,
        "consensus_code": code,
        "response": parsed,
        "raw": raw if not dry_run else None,
        "prompt_version": messages["prompt_version"],
    }


def pairwise_agreement(
    rows: Sequence[Mapping[str, Any]],
    *,
    primary_model: str,
    alternate_model: str,
) -> Dict[str, Any]:
    """Compare primary vs alternate phrasing and primary vs alternate model."""
    by_key: Dict[Tuple[str, int], Dict[str, str]] = {}
    for row in rows:
        key = (str(row["hypothesis"]), int(row["topic_id"]))
        by_key.setdefault(key, {})
        tag = f"{row['phrasing']}::{row['model']}"
        by_key[key][tag] = str(row["consensus_code"])

    phrasing_pairs = []
    model_pairs = []

    for (hyp, tid), codes in sorted(by_key.items()):
        p_primary = codes.get(f"primary::{primary_model}")
        p_alt = codes.get(f"alternate::{primary_model}")
        if p_primary and p_alt:
            phrasing_pairs.append(
                {
                    "hypothesis": hyp,
                    "topic_id": tid,
                    "primary": p_primary,
                    "alternate": p_alt,
                    "agree": p_primary == p_alt,
                }
            )
        m_primary = codes.get(f"primary::{primary_model}")
        m_alt = codes.get(f"primary::{alternate_model}")
        if m_primary and m_alt and primary_model != alternate_model:
            model_pairs.append(
                {
                    "hypothesis": hyp,
                    "topic_id": tid,
                    "primary_model": m_primary,
                    "alternate_model": m_alt,
                    "agree": m_primary == m_alt,
                }
            )

    def rate(pairs: List[Dict[str, Any]]) -> Optional[float]:
        if not pairs:
            return None
        return sum(1 for p in pairs if p["agree"]) / len(pairs)

    return {
        "phrasing_pairs": phrasing_pairs,
        "model_pairs": model_pairs,
        "phrasing_agreement": rate(phrasing_pairs),
        "model_agreement": rate(model_pairs),
    }


def refine_recommendations(
    agreement: Mapping[str, Any],
    *,
    threshold: float,
) -> List[str]:
    notes: List[str] = []
    for pair in agreement.get("phrasing_pairs", []):
        if not pair["agree"]:
            notes.append(
                f"{pair['hypothesis']} topic {pair['topic_id']}: "
                f"primary={pair['primary']} vs alternate={pair['alternate']} — "
                "tighten codebook definitions before full batch."
            )
    for pair in agreement.get("model_pairs", []):
        if not pair["agree"]:
            notes.append(
                f"{pair['hypothesis']} topic {pair['topic_id']}: "
                f"models disagree ({pair['primary_model']} vs {pair['alternate_model']})."
            )
    phr = agreement.get("phrasing_agreement")
    if phr is not None and phr < threshold:
        notes.append(
            f"Overall phrasing agreement {phr:.2f} < threshold {threshold:.2f}; "
            "refine frozen prompt definitions and re-run the pilot."
        )
    return notes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="No OpenRouter calls; write deterministic pilot artifacts",
    )
    parser.add_argument(
        "--lexical-only",
        action="store_true",
        help="Build lexical packets only (skip sentence parquet scan)",
    )
    parser.add_argument(
        "--hypotheses",
        default="",
        help="Comma-separated subset (default: config stability_pilot.hypotheses_to_pilot)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    lookup = load_topic_lookup(cfg)
    integrity = run_lookup_integrity(cfg, lookup)
    integrity.raise_if_failed()

    hard_topics = resolve_hard_topics(cfg, lookup)
    LOGGER.info("Stability pilot topics (%d): %s", len(hard_topics), hard_topics)

    # Build evidence packets for the pilot set
    import pandas as pd

    metadata = load_topic_metadata(cfg)
    rep_docs = load_representative_docs(cfg)
    cell_key = load_or_create_cell_key(cfg)
    seal_cell_key(cfg, cell_key)
    counts = pd.read_parquet(cfg.input_path("book_topic_counts", required=True))
    frame = pd.read_parquet(
        cfg.input_path("analysis_frame", required=True),
        columns=["book_id", "rating_class"],
    )

    packets = {}
    for tid in hard_topics:
        packets[tid] = build_evidence_packet(
            cfg,
            tid,
            lookup=lookup,
            metadata=metadata,
            representative_docs=rep_docs,
            book_topic_counts=counts,
            analysis_frame=frame,
            cell_key=cell_key,
            include_contextual=not args.lexical_only,
        )
    write_evidence_packets(cfg, packets)

    hyps = (
        [h.strip().upper() for h in args.hypotheses.split(",") if h.strip()]
        if args.hypotheses.strip()
        else [str(h).upper() for h in cfg.section("stability_pilot", "hypotheses_to_pilot")]
    )

    # Map each hard topic to the first matching pilot hypothesis by leaf
    leaf_of = {
        int(r.topic_id): str(r.taxonomy_main_id)
        for r in lookup.itertuples()
    }
    hyp_leaves = {
        hyp: set(
            str(x)
            for key in ("mandatory_leaves", "focus_leaves", "comparator_leaves")
            for x in (cfg.section("hypotheses", hyp).get(key) or [])
        )
        for hyp in hyps
    }

    primary_model = str(cfg.section("llm", "primary_model"))
    alt_model = str(cfg.section("llm", "alternate_model"))
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    dry_run = bool(args.dry_run or not api_key)
    if dry_run:
        LOGGER.info("Running stability pilot in dry-run mode (no API calls)")

    results: List[Dict[str, Any]] = []
    compare_modes = cfg.section("stability_pilot", "compare")

    for tid in hard_topics:
        leaf = leaf_of.get(tid)
        matched = [h for h, leaves in hyp_leaves.items() if leaf in leaves]
        if not matched:
            # Fall back to H1 for intimacy-adjacent leftovers
            matched = [hyps[0]]
        for hyp in matched[:1]:
            packet = packets[tid]
            # Always run two phrasings on primary model
            for phrasing in ("primary", "alternate"):
                results.append(
                    run_condition(
                        cfg=cfg,
                        hypothesis=hyp,
                        packet=packet,
                        phrasing=phrasing,
                        model=primary_model,
                        dry_run=dry_run,
                        api_key=api_key,
                    )
                )
            # Optional second model on primary phrasing
            if any(m.get("mode") == "two_models" for m in compare_modes):
                results.append(
                    run_condition(
                        cfg=cfg,
                        hypothesis=hyp,
                        packet=packet,
                        phrasing="primary",
                        model=alt_model,
                        dry_run=dry_run,
                        api_key=api_key,
                    )
                )

    agreement = pairwise_agreement(
        results,
        primary_model=primary_model,
        alternate_model=alt_model,
    )
    threshold = float(cfg.section("stability_pilot", "agreement_threshold"))
    notes = refine_recommendations(agreement, threshold=threshold)
    phr_agree = agreement.get("phrasing_agreement")
    stable = phr_agree is not None and phr_agree >= threshold and not notes

    out_dir = cfg.output_path("stability_pilot_dir", create=True)
    (out_dir / "pilot_results.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n",
        encoding="utf-8",
    )
    summary = {
        "run_id": cfg.run_id,
        "dry_run": dry_run,
        "n_topics": len(hard_topics),
        "topic_ids": hard_topics,
        "hypotheses": hyps,
        "primary_model": primary_model,
        "alternate_model": alt_model,
        "agreement_threshold": threshold,
        "phrasing_agreement": phr_agree,
        "model_agreement": agreement.get("model_agreement"),
        "stable_enough_for_batch": bool(stable) and not notes,
        "refine_notes": notes,
        "agreement_detail": agreement,
        "integrity": {"ok": integrity.ok, "h2_n": len(integrity.h2_topic_ids)},
    }
    (out_dir / "pilot_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (out_dir / "refine_notes.md").write_text(
        "# Stability pilot refine notes\n\n"
        + ("\n".join(f"- {n}" for n in notes) if notes else "- No refine actions required.\n"),
        encoding="utf-8",
    )

    LOGGER.info(
        "Phrasing agreement=%.3f threshold=%.3f stable=%s",
        phr_agree if phr_agree is not None else -1.0,
        threshold,
        summary["stable_enough_for_batch"],
    )
    if notes:
        LOGGER.warning("Refine before full batch:\n  %s", "\n  ".join(notes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
