#!/usr/bin/env python3
"""Build refined book-level analysis frames (strict / weighted / inclusive)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.analysis.frame import (  # noqa: E402
    write_refined_frame,
)
from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)

LOGGER = logging.getLogger("stage11.frame")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()
    paths = write_refined_frame(cfg)
    for name, path in paths.items():
        LOGGER.info("%s → %s", name, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
