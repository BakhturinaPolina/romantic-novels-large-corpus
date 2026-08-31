#!/usr/bin/env python3
"""Cheap Nemo spillover triage for H1, H3 (material discovery), and H4."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.audits.spillover import (  # noqa: E402
    build_h1_spillover_candidates,
    build_h3_spillover_candidates,
    build_h4_spillover_candidates,
    run_spillover_triage,
    write_spillover_result,
)
from src.stage11_refined_construct_analysis.audits.llm import load_dotenv_key  # noqa: E402
from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.lookup import (  # noqa: E402
    build_all_manifests,
    load_topic_lookup,
    write_manifests,
)

LOGGER = logging.getLogger("stage11.spillover")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--hypotheses",
        default="H1,H3,H4",
        help="Comma-separated (default: H1,H3,H4)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    load_dotenv_key()
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    manifests = build_all_manifests(cfg)
    write_manifests(cfg, manifests)
    lookup = load_topic_lookup(cfg)

    builders = {
        "H1": build_h1_spillover_candidates,
        "H3": build_h3_spillover_candidates,
        "H4": build_h4_spillover_candidates,
    }
    hyps = [h.strip().upper() for h in args.hypotheses.split(",") if h.strip()]
    for hyp in hyps:
        if hyp not in builders:
            LOGGER.warning("No spillover builder for %s; skipping", hyp)
            continue
        man = manifests["hypotheses"][hyp]
        candidates = builders[hyp](cfg, lookup, man)
        LOGGER.info("%s spillover candidates: %d", hyp, len(candidates))
        result = run_spillover_triage(
            cfg,
            hyp,
            candidates,
            dry_run=args.dry_run,
        )
        path = write_spillover_result(cfg, result)
        LOGGER.info(
            "%s spillover: promoted %d/%d → %s",
            hyp,
            result["n_promoted"],
            result["n_candidates"],
            path,
        )
        # Write a small index for notebooks
        index_path = cfg.output_path("candidates_dir") / "spillover_index.json"
        index = {}
        if index_path.exists():
            index = json.loads(index_path.read_text(encoding="utf-8"))
        index[hyp] = {
            "n_candidates": result["n_candidates"],
            "n_promoted": result["n_promoted"],
            "promoted_topic_ids": result["promoted_topic_ids"],
            "dry_run": result["dry_run"],
            "path": str(path.relative_to(cfg.root)),
        }
        index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
