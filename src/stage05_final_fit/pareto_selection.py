"""Load top-k BO calls from Stage04 pareto notebook outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.common.config import load_config, resolve_path

_STRATEGY_FILES = {
    "equal_weights": "top_10_equal_weights.csv",
    "coherence_priority": "top_10_coherence_priority.csv",
    "eval_select": "top_10_eval_select.csv",
}


def collect_bo_calls_from_pareto(
    top_models_dir: Path,
    *,
    strategies: tuple[str, ...] = ("equal_weights", "coherence_priority", "eval_select"),
) -> list[int]:
    """Return sorted unique ``bo_call`` values from pareto top-k CSVs."""
    calls: set[int] = set()
    for name in strategies:
        filename = _STRATEGY_FILES.get(name)
        if filename is None:
            raise ValueError(f"Unknown strategy {name!r}; expected one of {sorted(_STRATEGY_FILES)}")
        path = top_models_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Pareto top-k file not found: {path}")
        df = pd.read_csv(path)
        if "bo_call" not in df.columns:
            raise ValueError(f"Expected bo_call column in {path}")
        calls.update(int(v) for v in df["bo_call"].dropna().astype(int).tolist())
    return sorted(calls)


def load_pareto_selection_config(config_path: Path) -> dict:
    """Load ``configs/stage04/selection_notebooks.yaml`` and resolve key paths."""
    cfg = load_config(config_path)
    run_id = cfg["run_id"]
    base = resolve_path(Path(cfg["outputs"]["base_dir"]))
    top_models_dir = resolve_path(Path(cfg["outputs"]["top_models_dir"]))
    trials_partial = resolve_path(Path(cfg["inputs"]["trials_partial_csv"]))
    return {
        "run_id": run_id,
        "top_models_dir": top_models_dir,
        "trials_partial_csv": trials_partial,
        "notebook_analysis_dir": base,
    }
