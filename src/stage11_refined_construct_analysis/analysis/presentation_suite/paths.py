"""Paths for Stage 11 presentation suite."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.stage11_refined_construct_analysis.config import Stage11Config, find_project_root, load_stage11_config

DEFAULT_RUN_ID = "v4_l12_granular_final_call49"
DEFAULT_DECK_ID = "final_v1"
PARETO_EXPERIMENT_ID = "v4_l12_granular_phase1"
PARETO_SELECTED_CALL = 49


@dataclass(frozen=True)
class PresentationPaths:
    root: Path
    run_id: str
    analysis: Path
    out_dir: Path
    docs_dir: Path
    deck_id: str = DEFAULT_DECK_ID

    @property
    def constructs(self) -> Path:
        return self.analysis.parent / "constructs"

    @property
    def deck_root(self) -> Path:
        return self.root / "results" / "presentation" / self.deck_id

    @property
    def deck_figures(self) -> Path:
        return self.deck_root / "figures"

    @property
    def deck_data(self) -> Path:
        return self.deck_root / "data"

    @property
    def deck_annotations(self) -> Path:
        return self.deck_root / "annotations"

    @property
    def deck_manifests(self) -> Path:
        return self.deck_root / "manifests"

    @property
    def deck_tables(self) -> Path:
        return self.deck_root / "tables"

    @property
    def deck_review(self) -> Path:
        return self.deck_root / "review"

    @property
    def stage10_analysis(self) -> Path:
        return (
            self.root
            / "results"
            / "stage10_correlation_analysis"
            / self.run_id
            / "notebook_analysis"
        )

    @property
    def pareto_trials(self) -> Path:
        partial = (
            self.root
            / "results"
            / "experiments"
            / PARETO_EXPERIMENT_ID
            / "opt_1_sentence-transformers__all-MiniLM-L12-v2"
            / "trials_partial.csv"
        )
        if partial.exists():
            return partial
        return self.root / "results" / "experiments" / PARETO_EXPERIMENT_ID / "trials.csv"

    def nb_tables(self, notebook: str) -> Path:
        return self.analysis / notebook / "tables"

    def stage10_table(self, notebook: str, name: str) -> Path:
        base = self.stage10_analysis / notebook / "tables"
        pq = base / f"{name}.parquet"
        if pq.exists():
            return pq
        return base / f"{name}.csv"

    def table(self, notebook: str, name: str) -> Path:
        base = self.nb_tables(notebook)
        pq = base / f"{name}.parquet"
        if pq.exists():
            return pq
        return base / f"{name}.csv"

    def ensure_deck_dirs(self) -> None:
        for d in (
            self.deck_figures,
            self.deck_data,
            self.deck_annotations,
            self.deck_manifests,
            self.deck_tables,
            self.deck_review,
        ):
            d.mkdir(parents=True, exist_ok=True)


def default_paths(
    *,
    root: Path | None = None,
    run_id: str | None = None,
    deck_id: str | None = None,
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
        deck_id=deck_id or DEFAULT_DECK_ID,
    )
