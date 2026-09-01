"""Load presentation annotation / selection CSVs from deck annotations dir."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from .paths import PresentationPaths, default_paths


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_slide_selection(slide_id: str, paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    df = _read_csv(paths.deck_annotations / "slide_feature_selection.csv")
    if df.empty:
        return df
    return df.loc[df["slide_id"] == slide_id].sort_values("display_order")


def load_annotations(slide_id: str, paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    df = _read_csv(paths.deck_annotations / "plot_annotations.csv")
    if df.empty:
        return df
    mask = df["slide_id"] == slide_id if "slide_id" in df.columns else df["figure"] == slide_id
    return df.loc[mask]


def load_animation_sequence(slide_id: str, paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    df = _read_csv(paths.deck_annotations / "animation_sequence.csv")
    if df.empty:
        return df
    return df.loc[df["slide_id"] == slide_id].sort_values("step")


def load_label_positions(figure_id: str, paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    df = _read_csv(paths.deck_annotations / "label_positions.csv")
    if df.empty:
        return df
    return df.loc[df["figure_id"] == figure_id]


def write_csv(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
