#!/usr/bin/env python3
"""Rebuild W_tkr H6-v2 + H6-only effect tests; write comparison vs baseline."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import yaml

from src.stage10_correlation_analysis.analysis.effects import two_group_effects
from src.stage11_refined_construct_analysis.analysis.master import write_master_artifacts
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    find_project_root,
    load_stage11_config,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--crosswalk", default="configs/stage11/h6_radway_crosswalk.yaml")
    args = parser.parse_args(argv)

    root = find_project_root()
    cfg = load_stage11_config(args.config)
    cw = yaml.safe_load((root / args.crosswalk).read_text(encoding="utf-8"))
    day = root / cw["paths"]["day_dir"]
    membership = json.loads((day / "h6_v2_membership.json").read_text(encoding="utf-8"))
    baseline = json.loads((day / "baseline_freeze.json").read_text(encoding="utf-8"))

    # Rebuild master + W_tkr from merged audits/h6
    paths = write_master_artifacts(cfg)
    wtkr_src = cfg.output_path("constructs_dir") / "W_tkr.parquet"
    wtkr_dst = day / "W_tkr_h6_v2.parquet"
    shutil.copy2(wtkr_src, wtkr_dst)

    from src.stage11_refined_construct_analysis.analysis.frame import write_refined_frame

    write_refined_frame(cfg)

    # H6-only effects from strict frame
    frame_path = cfg.output_path("book_features_dir") / "book_refined_analysis_frame_strict.parquet"
    frame = pd.read_parquet(frame_path)
    h6_cols = [c for c in ("RARC", "DELTA_rising", "DELTA_falling") if c in frame.columns]
    if not h6_cols:
        raise SystemExit(f"H6 columns missing from {frame_path}; columns={list(frame.columns)[:30]}")

    effects = two_group_effects(
        frame,
        h6_cols,
        "rating_class",
        "high_rate",
        "low_rate",
        n_replicates=1000,
        seed=42,
    )
    effects_path = day / "h6_v2_hypothesis_effects.csv"
    effects.to_csv(effects_path, index=False)

    # Coverage from membership
    cov = {
        "RAX_arc_rising": {
            "n_topics": membership["n_strict_rising"],
            "topic_ids": membership["strict_rising_topic_ids"],
            "gate": (
                "viable"
                if membership["n_strict_rising"] >= 5
                else ("thin" if membership["n_strict_rising"] >= 1 else "unmeasurable")
            ),
        },
        "RAX_arc_falling": {
            "n_topics": membership["n_strict_falling"],
            "topic_ids": membership["strict_falling_topic_ids"],
        },
    }

    def _row(feature: str) -> dict:
        sub = effects[effects["feature"] == feature]
        if sub.empty:
            return {}
        r = sub.iloc[0]
        return {
            "cliffs_delta": float(r["cliffs_delta"]),
            "ci_low": float(r["ci_low"]),
            "ci_high": float(r["ci_high"]),
            "magnitude": str(r.get("magnitude", "")),
        }

    comparison = {
        "baseline": {
            "RARC": baseline.get("RARC"),
            "DELTA_rising": baseline.get("DELTA_rising"),
            "DELTA_falling": baseline.get("DELTA_falling"),
            "strict_rising": baseline.get("strict_RAX_arc_rising"),
        },
        "h6_v2": {
            "effects": {f: _row(f) for f in h6_cols},
            "coverage": cov,
        },
        "artifacts": {
            "W_tkr_h6_v2": str(wtkr_dst.relative_to(root)),
            "effects_csv": str(effects_path.relative_to(root)),
            "master_paths": {k: str(v) for k, v in paths.items()},
        },
    }
    (day / "h6_v2_vs_baseline.json").write_text(
        json.dumps(comparison, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps(comparison, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
