#!/usr/bin/env python3
"""Run direct Radway Phase I/II/III trajectories into h6_radway_day/radway_phases/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import yaml

from src.stage11_refined_construct_analysis.analysis.radway_phases import (
    load_radway_lookup,
    run_radway_phase_analysis,
)
from src.stage11_refined_construct_analysis.config import find_project_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--crosswalk",
        default="configs/stage11/h6_radway_crosswalk.yaml",
    )
    args = parser.parse_args(argv)
    root = find_project_root()
    cw = yaml.safe_load((root / args.crosswalk).read_text(encoding="utf-8"))
    paths = cw["paths"]
    day = root / paths["day_dir"]
    out = day / "radway_phases"

    lookup = load_radway_lookup(
        root / paths["topic_lookup"],
        root / paths["taxonomy_with_radway"],
    )
    tertile = pd.read_parquet(
        root
        / "results/stage10_correlation_analysis/v4_l12_granular_final_call49"
        / "topic_counts_hard/tertile_topic_counts.parquet"
    )
    frame = pd.read_parquet(
        root
        / "results/stage10_correlation_analysis/v4_l12_granular_final_call49"
        / "book_features_hard/book_analysis_frame.parquet"
    )
    written = run_radway_phase_analysis(
        tertile_counts=tertile,
        lookup=lookup,
        analysis_frame=frame,
        out_dir=out,
    )
    print(f"Wrote {len(written)} artifacts under {out}")
    for k, v in written.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
