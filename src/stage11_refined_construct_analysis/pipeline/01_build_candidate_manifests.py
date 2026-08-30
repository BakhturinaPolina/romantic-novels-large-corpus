#!/usr/bin/env python3
"""Build lookup-derived hypothesis candidate manifests + frozen_inputs.json."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import (  # noqa: E402
    build_all_manifests,
    write_manifests,
)

LOGGER = logging.getLogger("stage11.manifests")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    payload = build_all_manifests(cfg)
    path = write_manifests(cfg, payload)
    LOGGER.info(
        "Wrote manifests: %s topics across H1–H6 → %s",
        payload["n_audited_topics"],
        path,
    )
    LOGGER.info(
        "H2 pool n=%d ids=%s",
        len(payload["integrity"]["h2_topic_ids"]),
        payload["integrity"]["h2_topic_ids"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
