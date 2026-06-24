"""Run Stage05 compare-fit + Stage05b holdout for pareto notebook selections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.stage05_final_fit.compare_fit import compare_model_dir, run_compare_fit
from src.stage05_final_fit.pareto_selection import (
    collect_bo_calls_from_pareto,
    load_pareto_selection_config,
)
from src.stage05b_test_holdout.test_runner import run_holdout_score


def run_pareto_stage05(
    selection_config: Path = Path("configs/selection_notebooks.yaml"),
    *,
    paths_config: Path = Path("configs/paths_stage03_fit_v3.yaml"),
    train_config: Path = Path("configs/train_v3.yaml"),
    strategies: tuple[str, ...] = ("equal_weights", "coherence_priority", "eval_select"),
    stability_runs: int = 0,
    stability_tolerance: float = 3.0,
    reduce_outliers: bool = False,
    force_refit: bool = False,
    run_holdout: bool = True,
    allow_rerun: bool = False,
) -> dict[str, Any]:
    """Compare-fit pareto top-k trials, save models, and score test holdout."""
    sel = load_pareto_selection_config(selection_config)
    run_id = sel["run_id"]
    bo_calls = collect_bo_calls_from_pareto(sel["top_models_dir"], strategies=strategies)

    compare_root = run_compare_fit(
        trials_csv=sel["trials_partial_csv"],
        bo_calls=bo_calls,
        run_id=run_id,
        paths_config=paths_config,
        config_path=train_config,
        stability_runs=stability_runs,
        stability_tolerance=stability_tolerance,
        reduce_outliers=reduce_outliers,
        save_model=True,
        force_refit=force_refit,
    )

    holdout_results: list[dict[str, Any]] = []
    if run_holdout:
        for call in bo_calls:
            call_dir = compare_root / f"call_{call}"
            if not compare_model_dir(call_dir).is_dir():
                raise FileNotFoundError(
                    f"Compare-fit model missing for call_{call}: {compare_model_dir(call_dir)}"
                )
            metrics_path = run_holdout_score(
                final_model_dir=call_dir,
                policy="compare_fit",
                run_id=run_id,
                allow_rerun=allow_rerun,
                bo_call=call,
            )
            with open(metrics_path, "r", encoding="utf-8") as f:
                holdout_results.append(json.load(f))

    summary_rows = []
    for call in bo_calls:
        compare_metrics_path = compare_root / f"call_{call}" / "metrics.json"
        row: dict[str, Any] = {"bo_call": call}
        if compare_metrics_path.exists():
            with open(compare_metrics_path, "r", encoding="utf-8") as f:
                compare_metrics = json.load(f)
            row.update(
                {
                    "compare_n_topics": compare_metrics.get("n_topics"),
                    "compare_coherence_c_v": compare_metrics.get("coherence_c_v"),
                    "compare_topic_diversity": compare_metrics.get("topic_diversity"),
                    "compare_outlier_rate": compare_metrics.get("outlier_rate"),
                }
            )
        holdout = next((h for h in holdout_results if h.get("bo_call") == call), None)
        if holdout:
            row.update(
                {
                    "test_coherence_c_v": holdout.get("coherence_c_v"),
                    "test_topic_diversity": holdout.get("topic_diversity"),
                    "test_outlier_rate": holdout.get("outlier_rate"),
                    "test_n_topics": holdout.get("n_topics"),
                    "test_n_docs": holdout.get("n_docs_test"),
                }
            )
        summary_rows.append(row)

    summary_path = compare_root / "pareto_holdout_summary.csv"
    pd.DataFrame(summary_rows).to_csv(summary_path, index=False)

    return {
        "run_id": run_id,
        "bo_calls": bo_calls,
        "compare_root": compare_root,
        "holdout_summary_csv": summary_path,
        "holdout_results": holdout_results,
    }
