#!/usr/bin/env python3
"""Run H5 (focused) then H6 (arc + inherit H5-flagged 3.2) Pass A/B/C."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.audits.llm import load_dotenv_key  # noqa: E402
from src.stage11_refined_construct_analysis.audits.runner import (  # noqa: E402
    resolve_audit_topic_ids,
    run_hypothesis_audit,
)
from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import (  # noqa: E402
    build_all_manifests,
    write_manifests,
)

LOGGER = logging.getLogger("stage11.h5h6")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--hypotheses", default="H5,H6")
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
    write_manifests(cfg, build_all_manifests(cfg))

    order = [h.strip().upper() for h in args.hypotheses.split(",") if h.strip()]
    for hyp in order:
        ids = resolve_audit_topic_ids(cfg, hyp)
        LOGGER.info("==== %s (%d topics) ====", hyp, len(ids))
        summary = run_hypothesis_audit(
            cfg,
            hyp,
            topic_ids=ids,
            dry_run=args.dry_run,
            resume=not args.no_resume,
            limit=args.limit,
            model=(args.model.strip() or None),
        )
        LOGGER.info(
            "%s done newly=%d total=%d dry_run=%s",
            hyp,
            summary["n_newly_audited"],
            summary["n_adjudicated_total"],
            summary["dry_run"],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
