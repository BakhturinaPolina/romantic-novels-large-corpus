"""Orchestrate metadata build, figure generation, validation, and docs."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import List

import pandas as pd

from .evidence_metadata import build_all_metadata
from .figures_appendix import build_appendix_figures
from .figures_main import build_main_figures
from .paths import PresentationPaths, default_paths
from .slide_manifest import build_slide_manifest, write_figure_manifest
from .slide_plots import build_all_slide_figures
from .validate_presentation_data import run_all_validations, run_v2_validations


def _seed_annotation_templates(paths: PresentationPaths) -> None:
    """Copy committed annotation templates into deck if missing."""
    template_dir = Path(__file__).resolve().parent / "annotation_templates"
    paths.deck_annotations.mkdir(parents=True, exist_ok=True)
    for name in (
        "slide_feature_selection.csv",
        "plot_annotations.csv",
        "animation_sequence.csv",
        "label_positions.csv",
    ):
        dest = paths.deck_annotations / name
        src = template_dir / name
        if src.exists() and not dest.exists():
            shutil.copy2(src, dest)


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


def build_v2(*, paths: PresentationPaths | None = None, skip_validate: bool = False) -> PresentationPaths:
    """Build storyboard-aligned v2 deck under results/presentation/final_v1/."""
    paths = paths or default_paths()
    paths.ensure_deck_dirs()
    _seed_annotation_templates(paths)

    from .catalogs import build_all_catalogs
    from .slide_data import (
        prepare_representative_passages,
        prepare_topic_card,
    )

    build_all_metadata(paths, write=True)
    build_all_catalogs(paths, write=True)
    from .catalogs import build_corpus_stats

    build_corpus_stats(paths).to_csv(paths.deck_data / "corpus_stats.csv", index=False)
    prepare_topic_card(paths)
    prepare_representative_passages(paths)

    figure_rows = build_all_slide_figures(paths)
    build_slide_manifest(paths)
    write_figure_manifest(figure_rows, paths)

    if not skip_validate:
        frames = {
            "presentation_agreement": pd.read_csv(paths.out_dir / "presentation_agreement.csv"),
            "presentation_primary_results": pd.read_csv(paths.out_dir / "presentation_primary_results.csv"),
            "presentation_component_results": pd.read_csv(paths.out_dir / "presentation_component_results.csv"),
        }
        run_v2_validations(frames, paths, raise_on_error=True)

    return paths


def build_all_decks(*, paths: PresentationPaths | None = None, skip_validate: bool = False) -> PresentationPaths:
    paths = build_all(paths=paths, skip_validate=skip_validate)
    build_v2(paths=paths, skip_validate=skip_validate)
    return paths


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build Stage 11 presentation figures from saved tables.")
    parser.add_argument("--run-id", default=None, help="Stage 11 run id (default from config / v4_l12…)")
    parser.add_argument("--skip-validate", action="store_true")
    parser.add_argument(
        "--deck",
        choices=("v1", "v2", "all"),
        default="all",
        help="v1=legacy fig01-*; v2=slide deck; all=both",
    )
    args = parser.parse_args(argv)
    paths = default_paths(run_id=args.run_id)
    if args.deck == "v1":
        build_all(paths=paths, skip_validate=args.skip_validate)
        print(f"Wrote v1 figures to {paths.out_dir}")
    elif args.deck == "v2":
        build_v2(paths=paths, skip_validate=args.skip_validate)
        print(f"Wrote v2 deck to {paths.deck_root}")
    else:
        build_all_decks(paths=paths, skip_validate=args.skip_validate)
        print(f"Wrote v1 figures to {paths.out_dir}")
        print(f"Wrote v2 deck to {paths.deck_root}")


if __name__ == "__main__":
    main()
