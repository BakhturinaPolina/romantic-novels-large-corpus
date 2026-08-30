#!/usr/bin/env python3
"""Nemo Pass A/B/C for Stage 11 hypothesis audits (H1–H4 primary batch).

Order honoring the reuse graph: H1 → H3 → H4 (reuses H3 4.6) → H2 (position-aware).
Spillover-promoted IDs are merged from candidates/*_spillover.json when present.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.audits.runner import (  # noqa: E402
    run_hypothesis_audit,
)
from src.stage11_refined_construct_analysis.audits.llm import load_dotenv_key  # noqa: E402
from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import (  # noqa: E402
    build_all_manifests,
    write_manifests,
)

LOGGER = logging.getLogger("stage11.audits")

# Plan order: H1 → H3 → H4 (reuse) → H2
DEFAULT_ORDER = ("H1", "H3", "H4", "H2")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--hypotheses",
        default=",".join(DEFAULT_ORDER),
        help=f"Comma-separated subset (default: {','.join(DEFAULT_ORDER)})",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Cap topics per hypothesis (0 = all); useful for smoke tests",
    )
    parser.add_argument(
        "--topic-ids",
        default="",
        help="Optional comma-separated topic IDs (applies to each selected hypothesis)",
    )
    parser.add_argument(
        "--model",
        default="",
        help="OpenRouter model id override (default: configs/stage11 llm.primary_model)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    load_dotenv_key()
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    # Refresh manifests so leaf pools stay lookup-derived
    write_manifests(cfg, build_all_manifests(cfg))

    requested = [h.strip().upper() for h in args.hypotheses.split(",") if h.strip()]
    # Preserve scientific order when user passes a subset out of order
    order = [h for h in DEFAULT_ORDER if h in requested]
    for h in requested:
        if h not in order:
            order.append(h)

    topic_ids = None
    if args.topic_ids.strip():
        topic_ids = [int(x) for x in args.topic_ids.split(",") if x.strip()]

    for hyp in order:
        LOGGER.info("==== %s Pass A/B/C ====", hyp)
        summary = run_hypothesis_audit(
            cfg,
            hyp,
            topic_ids=topic_ids,
            dry_run=args.dry_run,
            resume=not args.no_resume,
            limit=args.limit,
            model=(args.model.strip() or None),
        )
        LOGGER.info(
            "%s done: newly=%d total_adjudicated=%d dry_run=%s exhaustive=%d",
            hyp,
            summary["n_newly_audited"],
            summary["n_adjudicated_total"],
            summary["dry_run"],
            summary["n_exhaustive"],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
