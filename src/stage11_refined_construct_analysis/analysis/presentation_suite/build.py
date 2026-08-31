"""Orchestrate metadata build, figure generation, validation, and docs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import pandas as pd

from .evidence_metadata import build_all_metadata
from .figures_appendix import build_appendix_figures
from .figures_main import build_main_figures
from .paths import PresentationPaths, default_paths
from .validate_presentation_data import run_all_validations


def write_manifest(rows: List[dict], paths: PresentationPaths) -> Path:
    df = pd.DataFrame(rows)
    paths.out_dir.mkdir(parents=True, exist_ok=True)
    paths.docs_dir.mkdir(parents=True, exist_ok=True)
    out1 = paths.out_dir / "figure_source_manifest.csv"
    out2 = paths.docs_dir / "figure_source_manifest.csv"
    df.to_csv(out1, index=False)
    df.to_csv(out2, index=False)
    return out1


def build_all(*, paths: PresentationPaths | None = None, skip_validate: bool = False) -> PresentationPaths:
    paths = paths or default_paths()
    paths.out_dir.mkdir(parents=True, exist_ok=True)
    main_manifest, frames = build_main_figures(paths)
    appendix_manifest = build_appendix_figures(paths)
    write_manifest(main_manifest + appendix_manifest, paths)
    if not skip_validate:
        run_all_validations(frames, paths, raise_on_error=True)
    return paths


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build Stage 11 presentation figures from saved tables.")
    parser.add_argument("--run-id", default=None, help="Stage 11 run id (default from config / v4_l12…)")
    parser.add_argument("--skip-validate", action="store_true")
    args = parser.parse_args(argv)
    paths = default_paths(run_id=args.run_id)
    build_all(paths=paths, skip_validate=args.skip_validate)
    print(f"Wrote figures to {paths.out_dir}")


if __name__ == "__main__":
    main()
