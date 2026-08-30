#!/usr/bin/env python3
"""H1 v1.2 anti-I3-collapse pilot on a hard topic set (Sonnet by default).

Writes to audits/h1_pilot_<tag>/ without touching the main H1 jsonl files.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.audits.llm import load_dotenv_key  # noqa: E402
from src.stage11_refined_construct_analysis.audits.runner import (  # noqa: E402
    CODE_FIELD,
    append_jsonl,
    ensure_packet,
    load_topic_metadata,
    run_pass,
)
from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh  # noqa: E402
from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code  # noqa: E402
from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup  # noqa: E402

LOGGER = logging.getLogger("stage11.h1_pilot")

# Hard cases: previous freeze mostly said I3; expected codes are approximate targets.
HARD_TOPICS = [
    {"topic_id": 11, "expect": "I4/I10", "why": "gaze / charged look"},
    {"topic_id": 279, "expect": "I4", "why": "desire / invitation"},
    {"topic_id": 72, "expect": "I10", "why": "eroticized beauty appraisal"},
    {"topic_id": 6, "expect": "I2", "why": "reassurance"},
    {"topic_id": 56, "expect": "I2", "why": "care / safety promise"},
    {"topic_id": 88, "expect": "I2/I0", "why": "medical caretaking"},
    {"topic_id": 52, "expect": "I0", "why": "domestic / animals"},
    {"topic_id": 116, "expect": "I0", "why": "domestic meal"},
    {"topic_id": 160, "expect": "I0", "why": "domestic movies"},
    {"topic_id": 151, "expect": "I8", "why": "consent negotiation"},
    {"topic_id": 199, "expect": "I9", "why": "coercion-adjacent"},
    {"topic_id": 197, "expect": "I3", "why": "true affectionate contact (kiss)"},
    {"topic_id": 101, "expect": "I3", "why": "affectionate touch (hair)"},
    {"topic_id": 208, "expect": "I5/I6", "why": "explicit-leaning sex topic"},
    {"topic_id": 292, "expect": "I4/I6", "why": "genital arousal / explicit boundary"},
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--model",
        default="anthropic/claude-sonnet-4.6",
        help="OpenRouter model id",
    )
    parser.add_argument(
        "--tag",
        default="v12_sonnet",
        help="Output subdirectory suffix under audits/",
    )
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    load_dotenv_key()
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    out = cfg.output_path("audits_dir", create=True) / f"h1_pilot_{args.tag}"
    out.mkdir(parents=True, exist_ok=True)
    paths = {
        "A": out / "lexical.jsonl",
        "B": out / "contextual.jsonl",
        "C": out / "adjudication.jsonl",
    }
    for p in paths.values():
        if p.exists():
            p.unlink()

    master = nh.load_master(cfg)
    old_map = {
        int(r.topic_id): str(r.intimacy_code)
        for _, r in master[master.intimacy_code.notna()].iterrows()
    }
    lookup = load_topic_lookup(cfg)
    metadata = load_topic_metadata(cfg)

    topics = HARD_TOPICS[: args.limit] if args.limit else HARD_TOPICS
    rows_out = []
    t0 = time.time()
    for i, spec in enumerate(topics, start=1):
        tid = int(spec["topic_id"])
        lu = lookup.loc[lookup["topic_id"] == tid]
        label = lu.iloc[0]["label"] if not lu.empty else "?"
        LOGGER.info(
            "[%d/%d] topic %s — %s (expect %s; old=%s)",
            i,
            len(topics),
            tid,
            label,
            spec["expect"],
            old_map.get(tid),
        )
        packet = ensure_packet(cfg, tid, metadata=metadata, lookup=lookup)
        row_a = run_pass(
            cfg,
            hypothesis="H1",
            packet=packet,
            pass_name="A",
            dry_run=args.dry_run,
            model=args.model,
        )
        row_b = run_pass(
            cfg,
            hypothesis="H1",
            packet=packet,
            pass_name="B",
            lexical_consensus=str(row_a["code"]),
            dry_run=args.dry_run,
            model=args.model,
        )
        row_c = run_pass(
            cfg,
            hypothesis="H1",
            packet=packet,
            pass_name="C",
            lexical_consensus=str(row_a["code"]),
            contextual_dominant=str(row_b["code"]),
            dry_run=args.dry_run,
            model=args.model,
        )
        append_jsonl(paths["A"], row_a)
        append_jsonl(paths["B"], row_b)
        append_jsonl(paths["C"], row_c)
        rows_out.append(
            {
                "topic_id": tid,
                "label": label,
                "taxonomy": (
                    f"{lu.iloc[0]['taxonomy_main_id']} — {lu.iloc[0]['taxonomy_main_name']}"
                    if not lu.empty
                    else "?"
                ),
                "why_hard": spec["why"],
                "expect": spec["expect"],
                "old_code": old_map.get(tid),
                "code_a": row_a.get("code"),
                "code_b": row_b.get("code"),
                "code_c": row_c.get("code"),
                "code_c_norm": normalize_code(row_c.get("code")),
                "rationale_c": (row_c.get("response") or {}).get("rationale"),
                "i3_contact_evidence": (row_c.get("response") or {}).get(
                    "i3_contact_evidence"
                ),
                "action": (row_c.get("response") or {}).get("action"),
                "model": row_c.get("model"),
                "prompt_version": row_c.get("prompt_version"),
                "dry_run": row_c.get("dry_run"),
            }
        )

    summary = {
        "hypothesis": "H1",
        "tag": args.tag,
        "model": args.model,
        "n_topics": len(rows_out),
        "elapsed_s": round(time.time() - t0, 1),
        "code_c_counts": {},
        "i3_share": None,
        "rows": rows_out,
        "outputs": {k: str(v.relative_to(cfg.root)) for k, v in paths.items()},
    }
    from collections import Counter

    counts = Counter(r["code_c_norm"] or r["code_c"] for r in rows_out)
    summary["code_c_counts"] = dict(counts)
    summary["i3_share"] = counts.get("I3", 0) / max(1, len(rows_out))

    out_json = out / "pilot_summary.json"
    out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n=== H1 v1.2 Sonnet pilot ===")
    print(f"model={args.model}  n={len(rows_out)}  I3_share={summary['i3_share']:.0%}")
    print(f"Pass C counts: {dict(counts)}")
    print(
        f"{'tid':>4} {'old':>4} {'A':>4} {'B':>6} {'C':>6}  {'expect':7}  label"
    )
    for r in rows_out:
        print(
            f"{r['topic_id']:4d} {str(r['old_code']):>4} {str(r['code_a']):>4} "
            f"{str(r['code_b']):>6} {str(r['code_c']):>6}  {r['expect']:7}  {r['label']}"
        )
    print(f"\nWrote {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
