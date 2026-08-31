#!/usr/bin/env python3
"""Audit only H6 Radway-day new topics with h6_arc_v2 + position packets.

Merges into audits/h6 without archiving the restored Sonnet-29 baseline.
Also writes h6_radway_day/h6_position_audit.jsonl (Pass B rows for new topics).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import yaml

from src.stage11_refined_construct_analysis.audits.llm import load_dotenv_key
from src.stage11_refined_construct_analysis.audits.runner import (
    PASS_FILES,
    audit_dir,
    load_jsonl,
    run_hypothesis_audit,
)
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    find_project_root,
    load_stage11_config,
)

LOGGER = logging.getLogger("stage11.h6_radway_audit")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--crosswalk", default="configs/stage11/h6_radway_crosswalk.yaml")
    parser.add_argument(
        "--prompt",
        default="configs/stage11/prompts/h6_arc_v2.yaml",
    )
    parser.add_argument(
        "--model",
        default="anthropic/claude-sonnet-4.6",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    load_dotenv_key()
    root = find_project_root()
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()
    cw = yaml.safe_load((root / args.crosswalk).read_text(encoding="utf-8"))
    day = root / cw["paths"]["day_dir"]
    ids = [
        int(x)
        for x in (day / "h6_new_topic_ids.txt").read_text(encoding="utf-8").split()
        if x.strip()
    ]
    if args.limit and args.limit > 0:
        ids = ids[: args.limit]

    # Protect restored 29: never pass --no-resume with archive; selective drop only
    summary = run_hypothesis_audit(
        cfg,
        "H6",
        topic_ids=ids,
        dry_run=args.dry_run,
        resume=not args.no_resume,
        limit=0,
        model=args.model,
        prompt_override=root / args.prompt,
        archive_on_no_resume=False,
    )
    LOGGER.info("Audit summary: %s", json.dumps(summary, indent=2))

    # Extract Pass B rows for new topics into day deliverable
    ctx_path = audit_dir(cfg, "H6") / PASS_FILES["B"]
    new_set = set(ids)
    rows = [r for r in load_jsonl(ctx_path) if int(r["topic_id"]) in new_set]
    out_jsonl = day / "h6_position_audit.jsonl"
    out_jsonl.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in rows)
        + ("\n" if rows else ""),
        encoding="utf-8",
    )
    meta = {
        "n_new_audited": len(rows),
        "topic_ids": sorted(new_set),
        "prompt": args.prompt,
        "model": args.model,
        "dry_run": args.dry_run,
        "audit_summary": summary,
    }
    (day / "h6_position_audit_meta.json").write_text(
        json.dumps(meta, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps(meta, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
