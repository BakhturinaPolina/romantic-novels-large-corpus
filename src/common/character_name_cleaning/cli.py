"""CLI for pre-Stage07 character name cleaning."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.common.character_name_cleaning.pipeline import run_cleaning_pipeline

LOGGER = logging.getLogger("character_name_cleaning.cli")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean character names from Stage06 topics and representative snippets."
    )
    parser.add_argument(
        "call",
        type=int,
        nargs="?",
        default=73,
        help="BO call number (default: 73)",
    )
    parser.add_argument(
        "--topics-json",
        type=Path,
        default=None,
        help="Stage06 topics_all_representations JSON",
    )
    parser.add_argument(
        "--representative-docs-csv",
        type=Path,
        default=None,
        help="compare-fit representative_docs.csv",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory for cleaned artifacts",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/stage06/character_name_cleaning.yaml"),
        help="Lexicon YAML config",
    )
    parser.add_argument(
        "--no-ner",
        action="store_true",
        help="Skip spaCy NER second pass",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )
    args = parse_args(argv)
    root = Path(".")

    call = args.call
    topics_json = args.topics_json or (
        root
        / f"results/stage06_topic_exploration/placeholder_v4_call{call}"
        / "topics_all_representations_placeholder_v4_call.json"
    )
    rep_csv = args.representative_docs_csv or (
        root
        / f"results/experiments/placeholder_v4_models/final_compare/call_{call}"
        / "representative_docs.csv"
    )
    out_dir = args.out_dir or (
        root / f"results/stage06_name_cleaning/placeholder_v4_call{call}"
    )

    if not topics_json.is_file():
        LOGGER.error("Topics JSON not found: %s", topics_json)
        return 1
    if not rep_csv.is_file():
        LOGGER.error("Representative docs CSV not found: %s", rep_csv)
        return 1

    paths = run_cleaning_pipeline(
        topics_json=topics_json,
        representative_docs_csv=rep_csv,
        out_dir=out_dir,
        config_path=args.config,
        run_ner=not args.no_ner,
    )
    for name, path in paths.items():
        LOGGER.info("%s: %s", name, path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
