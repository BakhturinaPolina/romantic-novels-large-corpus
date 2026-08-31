#!/usr/bin/env python3
"""Build EES exploratory candidate manifests (leaf ∪ prototype; no embeddings)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.analysis.ees_discovery import (  # noqa: E402
    DEFAULT_EES_CONFIG,
    build_all_ees_candidates,
    load_ees_config,
    load_stage11_from_ees,
    write_ees_candidates,
)

LOGGER = logging.getLogger("stage11.ees_candidates")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ees-config", default=str(DEFAULT_EES_CONFIG))
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ees_cfg = load_ees_config(Path(args.ees_config))
    cfg = load_stage11_from_ees(ees_cfg)
    cfg.ensure_output_tree()

    payload = build_all_ees_candidates(cfg, ees_cfg)
    paths = write_ees_candidates(cfg, ees_cfg, payload)
    LOGGER.info(
        "EES candidates: %d unique topics across families %s → %s",
        payload["n_unique_candidates"],
        payload["families"],
        paths["csv"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
