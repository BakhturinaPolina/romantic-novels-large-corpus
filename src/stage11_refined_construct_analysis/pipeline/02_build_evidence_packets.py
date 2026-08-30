#!/usr/bin/env python3
"""Build shared blinded evidence packets (+ human-review export + sealed cell key)."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.evidence.human_review import (  # noqa: E402
    write_human_review_packets,
)
from src.stage11_refined_construct_analysis.evidence.packets import (  # noqa: E402
    build_evidence_packets,
    write_evidence_packets,
)
from src.stage11_refined_construct_analysis.lookup import (  # noqa: E402
    build_all_manifests,
    write_manifests,
)

LOGGER = logging.getLogger("stage11.evidence")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--topic-ids",
        default="",
        help="Comma-separated topic IDs (default: all audited topics from manifests)",
    )
    parser.add_argument(
        "--lexical-only",
        action="store_true",
        help="Skip contextual sentence fetch (fast scaffold / CI)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional cap on number of topics (0 = all)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    manifests = build_all_manifests(cfg)
    write_manifests(cfg, manifests)

    if args.topic_ids.strip():
        topic_ids = [int(x) for x in args.topic_ids.split(",") if x.strip()]
    else:
        topic_ids = list(manifests["audited_topic_ids"])
        # Full builds always include exhaustive thin-leaf topics.
        for tid in manifests["exhaustive_topic_ids"]:
            if tid not in topic_ids:
                topic_ids.append(tid)

    topic_ids = sorted(set(topic_ids))
    if args.limit and args.limit > 0:
        topic_ids = topic_ids[: args.limit]

    packets = build_evidence_packets(
        cfg,
        topic_ids,
        include_contextual=not args.lexical_only,
    )
    index_path = write_evidence_packets(cfg, packets)
    review_path = write_human_review_packets(cfg, packets)
    LOGGER.info("Evidence index: %s", index_path)
    LOGGER.info("Human-review index: %s", review_path)
    LOGGER.info("Cell key: %s", cfg.output_path("cell_key"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
