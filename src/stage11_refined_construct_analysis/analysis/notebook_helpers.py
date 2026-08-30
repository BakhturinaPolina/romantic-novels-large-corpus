"""Notebook helpers for Stage 11 (mirrors Stage 10 setup pattern)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    Stage11Config,
    find_project_root,
    load_stage11_config,
)


@dataclass
class NotebookContext:
    cfg: Stage11Config
    notebook: str
    root: Path
    figures_dir: Path
    tables_dir: Path

    def save_table(self, frame: pd.DataFrame, name: str, *, index: bool = False) -> None:
        csv_path = self.tables_dir / f"{name}.csv"
        frame.to_csv(csv_path, index=index)
        try:
            frame.to_parquet(self.tables_dir / f"{name}.parquet", index=index)
        except Exception:
            pass
        print(f"  saved table: {csv_path.relative_to(self.root)}  ({len(frame):,} rows)")

    def save_figure(self, fig, name: str, *, dpi: int = 120) -> None:
        path = self.figures_dir / f"{name}.png"
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
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
    root = find_project_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    cfg = load_stage11_config(config_path, root=root)
    base = cfg.output_path("notebook_dir", create=True) / notebook
    figures = base / "figures"
    tables = base / "tables"
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)

    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.dpi"] = 120
    pd.set_option("display.max_columns", 80)
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda v: f"{v:,.4f}")

    if not quiet:
        print(f"Project root : {root}")
        print(f"Config       : {cfg.config_path.relative_to(root)}")
        print(f"Run          : {cfg.run_id}")
        print(f"Outputs      : {base.relative_to(root)}")

    return NotebookContext(
        cfg=cfg,
        notebook=notebook,
        root=root,
        figures_dir=figures,
        tables_dir=tables,
    )


def load_master(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.output_path("constructs_dir") / "master_annotations.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Master annotations missing: {path}")
    return pd.read_parquet(path)


def load_weights(cfg: Stage11Config, mode: str = "strict") -> pd.DataFrame:
    path = cfg.output_path("constructs_dir") / f"W_tk_{mode}.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def load_w_tkr(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.output_path("constructs_dir") / "W_tkr.parquet"
    return pd.read_parquet(path) if path.exists() else pd.DataFrame()


def load_refined_frame(cfg: Stage11Config, mode: str = "strict") -> pd.DataFrame:
    out = cfg.output_path("book_features_dir")
    path = out / (
        "book_refined_analysis_frame.parquet"
        if mode == "strict"
        else f"book_refined_analysis_frame_{mode}.parquet"
    )
    if not path.exists():
        raise FileNotFoundError(
            f"Refined frame missing at {path}. Run "
            "pipeline/08_build_refined_analysis_frame.py first."
        )
    frame = pd.read_parquet(path)
    return frame


def load_freeze(cfg: Stage11Config) -> Dict[str, Any]:
    path = cfg.output_path("constructs_dir") / "dictionary_freeze.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_frozen_inputs(cfg: Stage11Config) -> Dict[str, Any]:
    path = cfg.output_path("frozen_inputs")
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_candidates(cfg: Stage11Config, hyp: str) -> Dict[str, Any]:
    path = cfg.output_path("candidates_dir") / f"{hyp.lower()}_candidates.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_audit_jsonl(cfg: Stage11Config, hyp: str, pass_name: str) -> pd.DataFrame:
    from src.stage11_refined_construct_analysis.audits.runner import PASS_FILES, audit_dir

    path = audit_dir(cfg, hyp) / PASS_FILES[pass_name]
    if not path.exists():
        return pd.DataFrame()
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return pd.DataFrame(rows)


def load_cell_key(cfg: Stage11Config) -> Dict[str, Any]:
    path = cfg.output_path("cell_key")
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def effect_gate(cfg: Stage11Config) -> float:
    # Prefer Stage 10 gate if available via inputs; else 0.11
    return 0.11


def cliffs_delta_table(
    frame: pd.DataFrame,
    columns: Sequence[str],
    *,
    tier_col: str = "rating_class",
    high: str = "high_rate",
    low: str = "low_rate",
    n_boot: int = 500,
    seed: int = 42,
) -> pd.DataFrame:
    """Cliff's δ high vs low for each column, with bootstrap CI (reuse Stage 10 effects)."""
    from src.stage10_correlation_analysis.analysis import effects as eff

    rows = []
    rng = np.random.default_rng(seed)
    usable = frame
    if "analysable" in frame.columns:
        usable = frame[frame["analysable"].fillna(True)]
    for col in columns:
        if col not in usable.columns:
            continue
        a = usable.loc[usable[tier_col] == high, col].dropna().to_numpy(dtype=float)
        b = usable.loc[usable[tier_col] == low, col].dropna().to_numpy(dtype=float)
        if a.size < 10 or b.size < 10:
            continue
        delta = eff.cliffs_delta(a, b)
        # percentile bootstrap
        boots = []
        for _ in range(n_boot):
            aa = rng.choice(a, size=a.size, replace=True)
            bb = rng.choice(b, size=b.size, replace=True)
            try:
                boots.append(eff.cliffs_delta(aa, bb))
            except ValueError:
                continue
        if boots:
            lo, hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
        else:
            lo = hi = float("nan")
        rows.append(
            {
                "feature": col,
                "cliffs_delta": float(delta),
                "ci_low": lo,
                "ci_high": hi,
                "magnitude": eff.magnitude(delta),
                "n_high": int(a.size),
                "n_low": int(b.size),
                "mean_high": float(np.mean(a)),
                "mean_low": float(np.mean(b)),
            }
        )
    return pd.DataFrame(rows)


def verdict(delta: float, lo: float, hi: float, gate: float = 0.11) -> str:
    clears = abs(delta) >= gate and not (lo <= 0 <= hi)
    if clears:
        return "clears_gate"
    if not (lo <= 0 <= hi):
        return "directional_only"
    return "null"
