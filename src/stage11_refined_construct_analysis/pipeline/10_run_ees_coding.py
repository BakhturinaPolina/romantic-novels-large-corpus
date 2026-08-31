#!/usr/bin/env python3
"""Single-pass LLM coding for EES candidates (rating-blind evidence).

Requires candidates from 09_build_ees_candidates.py.
Use --dry-run to write placeholder codes without an API key.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.analysis.ees_coding import (  # noqa: E402
    run_ees_coding,
    write_semantic_codes,
)
from src.stage11_refined_construct_analysis.analysis.ees_discovery import (  # noqa: E402
    DEFAULT_EES_CONFIG,
    ees_output_dir,
    load_ees_config,
    load_stage11_from_ees,
)

LOGGER = logging.getLogger("stage11.ees_coding")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ees-config", default=str(DEFAULT_EES_CONFIG))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--families",
        nargs="*",
        default=None,
        help="Optional subset: emotion embodiment social cognition work",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ees_cfg = load_ees_config(Path(args.ees_config))
    cfg = load_stage11_from_ees(ees_cfg)
    cfg.ensure_output_tree()

    frame = run_ees_coding(
        cfg,
        ees_cfg,
        dry_run=args.dry_run,
        limit=args.limit,
        families=args.families,
    )
    out_dir = ees_output_dir(cfg, ees_cfg)
    paths = write_semantic_codes(frame, out_dir)
    LOGGER.info("Wrote %d semantic codes → %s", len(frame), paths["csv"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
