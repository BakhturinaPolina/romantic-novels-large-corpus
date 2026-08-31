"""Paths for Stage 11 presentation suite."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.stage11_refined_construct_analysis.config import Stage11Config, find_project_root, load_stage11_config

DEFAULT_RUN_ID = "v4_l12_granular_final_call49"


@dataclass(frozen=True)
class PresentationPaths:
    root: Path
    run_id: str
    analysis: Path
    out_dir: Path
    docs_dir: Path

    @property
    def constructs(self) -> Path:
        return self.analysis.parent / "constructs"

    def nb_tables(self, notebook: str) -> Path:
        return self.analysis / notebook / "tables"

    def table(self, notebook: str, name: str) -> Path:
        base = self.nb_tables(notebook)
        pq = base / f"{name}.parquet"
        if pq.exists():
            return pq
        return base / f"{name}.csv"


def default_paths(
    *,
    root: Path | None = None,
    run_id: str | None = None,
    config_path: str | Path | None = None,
) -> PresentationPaths:
    root = root or find_project_root()
    if run_id is None:
        try:
            cfg: Stage11Config = (
                load_stage11_config(config_path, root=root)
                if config_path
                else load_stage11_config(root=root)
            )
            run_id = cfg.run_id
        except Exception:
            run_id = DEFAULT_RUN_ID
    analysis = root / "results" / "stage11_refined_construct_analysis" / run_id / "notebook_analysis"
    out_dir = root / "results" / "stage11_refined_construct_analysis" / run_id / "presentation_figures"
    docs_dir = root / "notebooks" / "08_refined_construct_analysis" / "presentation_figures"
    return PresentationPaths(
        root=root,
        run_id=run_id,
        analysis=analysis,
        out_dir=out_dir,
        docs_dir=docs_dir,
    )
