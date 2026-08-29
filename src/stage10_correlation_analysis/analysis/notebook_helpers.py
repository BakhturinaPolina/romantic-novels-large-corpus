"""Setup, saving and formatting helpers so the notebooks stay readable.

Every notebook in `notebooks/07_analysis/` opens with `setup(notebook_name)`, which finds
the project root, loads the config, applies the plot style and creates the output folders.
All heavy logic lives in the sibling modules; the notebooks are meant to read as a
walkthrough, not as a codebase.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from src.stage10_correlation_analysis.analysis.config import (
    AnalysisConfig,
    DEFAULT_CONFIG_PATH,
    find_project_root,
    load_analysis_config,
)


@dataclass
class NotebookContext:
    cfg: AnalysisConfig
    notebook: str
    root: Path
    figures_dir: Path
    tables_dir: Path

    # The save_* methods deliberately return None. They are usually the last statement in a
    # notebook cell, and returning a Path would make Jupyter echo it as a result, cluttering
    # the walkthrough with filesystem noise.

    def save_table(self, frame: pd.DataFrame, name: str, *, index: bool = False) -> None:
        """Write a table as both CSV (readable) and Parquet (round-trips dtypes)."""
        csv_path = self.tables_dir / f"{name}.csv"
        frame.to_csv(csv_path, index=index)
        try:
            frame.to_parquet(self.tables_dir / f"{name}.parquet", index=index)
        except Exception:
            # Object columns holding dicts (PCA loadings) cannot go to parquet; CSV is enough.
            pass
        print(f"  saved table: {csv_path.relative_to(self.root)}  ({len(frame):,} rows)")

    def save_figure(self, fig, name: str, *, dpi: Optional[int] = None) -> None:
        path = self.figures_dir / f"{name}.png"
        fig.savefig(path, dpi=dpi or self.cfg.section("plotting", "figure_dpi"), bbox_inches="tight")
        print(f"  saved figure: {path.relative_to(self.root)}")

    def save_markdown(self, text: str, name: str) -> None:
        path = self.tables_dir / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        print(f"  saved markdown: {path.relative_to(self.root)}")


def setup(
    notebook: str,
    *,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    quiet: bool = False,
) -> NotebookContext:
    """Resolve the project root, load the config, set the plot style, create output dirs."""
    root = find_project_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    cfg = load_analysis_config(config_path, root=root)
    dirs = cfg.notebook_output_dirs(notebook)
    apply_plot_style(cfg)

    pd.set_option("display.max_columns", 80)
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda v: f"{v:,.4f}")

    if not quiet:
        print(f"Project root : {root}")
        print(f"Config       : {cfg.config_path.relative_to(root)}")
        print(f"Run          : {cfg.run_id}")
        print(f"Model        : {cfg.get('model_label')}")
        print(f"Outputs      : {dirs['base'].relative_to(root)}")

    return NotebookContext(
        cfg=cfg, notebook=notebook, root=root,
        figures_dir=dirs["figures"], tables_dir=dirs["tables"],
    )


def apply_plot_style(cfg: AnalysisConfig) -> None:
    import matplotlib.pyplot as plt
    import seaborn as sns

    plotting = cfg.get("plotting", {})
    sns.set_theme(
        style=plotting.get("style", "whitegrid"),
        context=plotting.get("context", "notebook"),
    )
    plt.rcParams["figure.dpi"] = plotting.get("figure_dpi", 120)
    plt.rcParams["savefig.dpi"] = plotting.get("figure_dpi", 120)
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.titleweight"] = "semibold"
    plt.rcParams["figure.autolayout"] = False


def tier_palette(cfg: AnalysisConfig) -> Dict[str, str]:
    return dict(cfg.section("plotting", "palette_tiers"))


# ---------------------------------------------------------------------------
# Loading the prepared data
# ---------------------------------------------------------------------------

def load_analysis_frame(cfg: AnalysisConfig) -> pd.DataFrame:
    """Load the book-level analysis frame, with a clear message if it has not been built."""
    path = cfg.output_path("analysis_frame")
    if not path.exists():
        raise FileNotFoundError(
            f"Analysis frame not found at {path}.\n"
            "Build it first:\n"
            "  .venv/bin/python src/stage10_correlation_analysis/data_preparation/05_aggregate_hard_assignments.py\n"
            "  .venv/bin/python src/stage10_correlation_analysis/data_preparation/02_book_aggregation.py\n"
            "  .venv/bin/python src/stage10_correlation_analysis/data_preparation/06_build_analysis_frame.py"
        )
    frame = pd.read_parquet(path)
    tier_col = cfg.tier_column
    if tier_col in frame.columns:
        frame[tier_col] = pd.Categorical(frame[tier_col], categories=cfg.tier_order, ordered=True)
    return frame.set_index("book_id") if "book_id" in frame.columns else frame


def load_hard_counts(cfg: AnalysisConfig, name: str) -> pd.DataFrame:
    path = cfg.output_path("hard_counts_dir") / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"{path} missing — run 05_aggregate_hard_assignments.py first")
    return pd.read_parquet(path)


def load_book_features(cfg: AnalysisConfig, name: str) -> pd.DataFrame:
    path = cfg.output_path("book_features_dir") / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"{path} missing — run 02_book_aggregation.py first")
    return pd.read_parquet(path)


def load_topic_lookup(cfg: AnalysisConfig) -> pd.DataFrame:
    path = cfg.input_path("topic_lookup", required=True)
    assert path is not None
    return pd.read_parquet(path)


def columns_with_prefix(frame: pd.DataFrame, prefix: str) -> List[str]:
    return [c for c in frame.columns if c.startswith(prefix)]


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

def describe_step(title: str, body: str) -> None:
    """Print a labelled explanation, so a printed notebook still reads as prose."""
    print(f"\n{title}\n{'-' * len(title)}\n{body.strip()}\n")


def format_effect_table(
    frame: pd.DataFrame,
    *,
    label_map: Optional[Dict[Any, str]] = None,
    top_n: Optional[int] = 25,
    delta_column: str = "cliffs_delta",
) -> pd.DataFrame:
    """Human-readable effect table: readable labels, rounded numbers, plain-language verdict."""
    out = frame.copy()
    if label_map is not None and "feature" in out.columns:
        out.insert(1, "description", out["feature"].map(label_map))

    if delta_column in out.columns:
        out = out.reindex(out[delta_column].abs().sort_values(ascending=False).index)
        out["direction"] = np.where(out[delta_column] > 0, "more in high-rated", "more in low-rated")
    if top_n:
        out = out.head(top_n)

    numeric = out.select_dtypes(include=[np.number]).columns
    return out.round({c: 4 for c in numeric}).reset_index(drop=True)


def share_as_percent(frame: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """Convert share columns to percentage points, which is how they are reported in text."""
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = out[col] * 100.0
    return out


def topic_label_map(topic_lookup: pd.DataFrame, prefix: str = "topic_") -> Dict[str, str]:
    """Map `topic_57` style column names to readable topic labels."""
    return {
        f"{prefix}{int(row.topic_id)}": str(row.label)
        for row in topic_lookup.itertuples()
        if pd.notna(getattr(row, "label", None))
    }


def leaf_label_map(topic_lookup: pd.DataFrame, prefix: str = "leaf_") -> Dict[str, str]:
    """Map `leaf_4.6` style column names to taxonomy category names."""
    pairs = (
        topic_lookup[["taxonomy_main_id", "taxonomy_main_name"]]
        .dropna().drop_duplicates()
    )
    return {f"{prefix}{row.taxonomy_main_id}": str(row.taxonomy_main_name) for row in pairs.itertuples()}


def summarise_counts(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    counts = frame[column].value_counts(dropna=False)
    return pd.DataFrame({
        column: counts.index.astype(str),
        "n": counts.to_numpy(),
        "percent": (counts / counts.sum() * 100).round(1).to_numpy(),
    })


def markdown_table(frame: pd.DataFrame, index: bool = False) -> str:
    return frame.to_markdown(index=index)


def significance_note(n_per_group: int) -> str:
    """Standing caveat about p-values at this sample size, printed where tests are reported."""
    return (
        f"With about {n_per_group:,} books per tier, a p-value below 0.05 is nearly automatic: "
        "differences far too small to matter still clear the threshold. Read the effect size "
        "and its confidence interval, and treat the p-value as a footnote."
    )


def compositional_note() -> str:
    return (
        "Topic shares sum to 1 within each book, so they are compositional. Every result is a "
        "relative reallocation of narrative attention, not an absolute amount: a theme rising "
        "in one book necessarily means other themes fall."
    )
