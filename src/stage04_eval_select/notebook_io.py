"""Shared helpers for notebooks/04_selection/ (single- and multi-run BO analysis)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from src.common.config import resolve_path

_DEPRECATED_TRIALS_COLS = frozenset({"coherence_c_npmi", "outlier_rate"})

STRATEGY_FILES: dict[str, str] = {
    "equal_weights": "top_10_equal_weights.csv",
    "coherence_priority": "top_10_coherence_priority.csv",
    "eval_select": "top_10_eval_select.csv",
}

LEGACY_RENAME: dict[str, str] = {
    "embedding_model": "Embeddings_Model",
    "coherence_c_v": "Coherence",
    "topic_diversity": "Topic_Diversity",
}

OUTPUT_DIR_KEYS = ("figures_dir", "tables_dir", "top_models_dir")


def normalize_trials_partial_df(df: pd.DataFrame) -> pd.DataFrame:
    """Drop deprecated columns only when entirely null.

    v4 granular runs populate ``outlier_rate`` during BO; it must be kept
    for the ``max_outlier_rate`` gate and the weighted-score outlier penalty.
    """
    drop = [c for c in _DEPRECATED_TRIALS_COLS if c in df.columns and df[c].isna().all()]
    if drop:
        df = df.drop(columns=drop)
    return df


def resolve_runs(nb_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Return configured runs; fall back to top-level single-run keys."""
    if "runs" in nb_cfg:
        return list(nb_cfg["runs"])
    return [
        {
            "run_id": nb_cfg["run_id"],
            "label": nb_cfg.get("label", nb_cfg["run_id"]),
            "inputs": nb_cfg["inputs"],
            "outputs": nb_cfg["outputs"],
        }
    ]


def resolve_run_dirs(run: dict[str, Any], project_root: Path) -> dict[str, Path]:
    return {
        key: resolve_path(Path(run["outputs"][key]), project_root)
        for key in OUTPUT_DIR_KEYS
        if key in run.get("outputs", {})
    }


def ensure_run_dirs(run_dirs: dict[str, Path]) -> None:
    for path in run_dirs.values():
        path.mkdir(parents=True, exist_ok=True)


def resolve_comparison_dirs(
    nb_cfg: dict[str, Any], project_root: Path
) -> dict[str, Path] | None:
    cmp = nb_cfg.get("comparison")
    if not cmp:
        return None
    base = resolve_path(Path(cmp["base_dir"]), project_root)
    figures_dir = base / "figures"
    tables_dir = base / "tables"
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    return {"base_dir": base, "figures_dir": figures_dir, "tables_dir": tables_dir}


def load_trials_for_runs(runs: list[dict[str, Any]], project_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for run in runs:
        path = resolve_path(Path(run["inputs"]["trials_partial_csv"]), project_root)
        df = normalize_trials_partial_df(pd.read_csv(path))
        df["run_id"] = run["run_id"]
        df["model_label"] = run.get("label", run["run_id"])
        # Note: no Embeddings_Model alias here — LEGACY_RENAME creates it later,
        # and pre-creating it produces duplicate columns after the rename.
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def apply_selection_filters(
    df: pd.DataFrame, sel: dict[str, Any]
) -> tuple[pd.DataFrame, list[tuple[str, int, int]]]:
    """Same row filters, in the same order, as ``src.stage04_eval_select.cli select``."""
    out = df.copy()
    steps: list[tuple[str, int, int]] = [("loaded", 0, len(out))]

    min_n_topics = int(sel.get("min_n_topics", 0))
    if min_n_topics > 0 and "n_topics" in out.columns:
        before = len(out)
        out = out[out["n_topics"].fillna(0) >= min_n_topics].copy()
        steps.append((f"n_topics >= {min_n_topics}", before - len(out), len(out)))

    max_n_topics = int(sel.get("max_n_topics", 0))
    if max_n_topics > 0 and "n_topics" in out.columns:
        before = len(out)
        out = out[out["n_topics"].fillna(0) <= max_n_topics].copy()
        steps.append((f"n_topics <= {max_n_topics}", before - len(out), len(out)))

    max_outlier_rate = float(sel.get("max_outlier_rate", 0))
    if max_outlier_rate > 0 and "outlier_rate" in out.columns:
        before = len(out)
        out = out[out["outlier_rate"].fillna(1.0) <= max_outlier_rate].copy()
        steps.append((f"outlier_rate <= {max_outlier_rate}", before - len(out), len(out)))

    max_largest_share = float(sel.get("max_largest_topic_share", 0))
    if max_largest_share > 0 and "largest_topic_share" in out.columns:
        before = len(out)
        out = out[out["largest_topic_share"].fillna(1.0) <= max_largest_share].copy()
        steps.append(
            (f"largest_topic_share <= {max_largest_share}", before - len(out), len(out))
        )

    if bool(sel.get("require_topic_stability", False)) and "topic_stability_pass" in out.columns:
        before = len(out)
        out = out[out["topic_stability_pass"].fillna(True).astype(bool)].copy()
        steps.append(("topic_stability_pass", before - len(out), len(out)))

    max_n_topics_std = float(sel.get("max_n_topics_std", 0))
    if max_n_topics_std > 0 and "n_topics_std" in out.columns:
        before = len(out)
        std_ok = out["n_topics_std"].isna() | (out["n_topics_std"] <= max_n_topics_std)
        out = out[std_ok].copy()
        steps.append((f"n_topics_std <= {max_n_topics_std}", before - len(out), len(out)))

    return out.reset_index(drop=True), steps


def filter_trials_by_run(
    df_raw: pd.DataFrame,
    runs: list[dict[str, Any]],
    sel: dict[str, Any],
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    """Apply selection filters per run; return map, concatenated trials, funnel table."""
    filtered_by_run: dict[str, pd.DataFrame] = {}
    funnel_rows: list[dict[str, Any]] = []
    for run in runs:
        run_id = run["run_id"]
        subset = df_raw[df_raw["run_id"] == run_id]
        filtered, steps = apply_selection_filters(subset, sel)
        filtered_by_run[run_id] = filtered
        label = run.get("label", run_id)
        for step, removed, remaining in steps:
            funnel_rows.append(
                {
                    "run_id": run_id,
                    "model_label": label,
                    "step": step,
                    "removed": removed,
                    "remaining": remaining,
                }
            )
    funnel_df = pd.DataFrame(funnel_rows)
    if filtered_by_run:
        df_trials = pd.concat(filtered_by_run.values(), ignore_index=True)
    else:
        df_trials = pd.DataFrame()
    return filtered_by_run, df_trials, funnel_df


def identify_pareto(df: pd.DataFrame, metrics: list[str]) -> np.ndarray:
    pareto_efficient = np.ones(df.shape[0], dtype=bool)
    values = df[metrics].values
    for pos_idx, row_vals in enumerate(values):
        other_rows_better = np.all(values >= row_vals, axis=1) & np.any(values > row_vals, axis=1)
        pareto_efficient[pos_idx] = not np.any(other_rows_better)
    return pareto_efficient


def analyze_pareto_efficiency(
    df: pd.DataFrame, metrics: list[str], *, per_model: bool = True
) -> pd.DataFrame:
    out = df.copy()
    out["Pareto_Efficient_All"] = identify_pareto(out, metrics)
    if per_model and "Embeddings_Model" in out.columns:
        out["Pareto_Efficient_PerModel"] = False
        for _, group in out.groupby("Embeddings_Model"):
            out.loc[group.index, "Pareto_Efficient_PerModel"] = identify_pareto(group, metrics)
    return out


def normalize_metrics(df: pd.DataFrame, *, method: str = "zscore") -> pd.DataFrame:
    out = df.copy()
    cols = ["Coherence", "Topic_Diversity"]
    if method == "zscore":
        out[["Coherence_norm", "Topic_Diversity_norm"]] = StandardScaler().fit_transform(out[cols])
    elif method == "minmax":
        out[["Coherence_norm", "Topic_Diversity_norm"]] = MinMaxScaler().fit_transform(out[cols])
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    return out


def calculate_combined_score(
    df: pd.DataFrame, weight_coherence: float, weight_topic_diversity: float
) -> pd.DataFrame:
    out = df.copy()
    out["Combined_Score"] = (
        weight_coherence * out["Coherence_norm"]
        + weight_topic_diversity * out["Topic_Diversity_norm"]
    )
    return out


def normalize_for_pareto(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ("coherence_c_v", "topic_diversity"):
        lo, hi = float(out[col].min()), float(out[col].max())
        out[f"{col}_norm"] = (out[col] - lo) / (hi - lo) if hi > lo else 0.0
    return out


def normalize_for_pareto_pooled(df: pd.DataFrame) -> pd.DataFrame:
    """Min-max normalize coherence/diversity over the pooled (multi-run) trial set.

    Same math as :func:`normalize_for_pareto`; the separate name makes explicit
    that the normalization range spans all embeddings, so Pareto fronts computed
    on the ``*_norm`` columns are comparable across runs.
    """
    return normalize_for_pareto(df)


def load_phase2_results(
    runs: list[dict[str, Any]], project_root: Path
) -> pd.DataFrame:
    """Load Phase 2 Pareto refit results (compare-fit + stability) for each run.

    Reads ``comparison_summary.csv`` and ``stability_summary.csv`` from each
    run's ``inputs.phase2_compare_dir`` and merges them on ``bo_call``.
    Runs without a configured/existing directory are skipped, so the notebook
    degrades gracefully when Phase 2 has not been run yet.
    """
    frames: list[pd.DataFrame] = []
    for run in runs:
        compare_dir = run.get("inputs", {}).get("phase2_compare_dir")
        if not compare_dir:
            continue
        base = resolve_path(Path(compare_dir), project_root)
        comparison_path = base / "comparison_summary.csv"
        stability_path = base / "stability_summary.csv"
        if not comparison_path.exists() or not stability_path.exists():
            continue
        comparison = pd.read_csv(comparison_path)
        stability = pd.read_csv(stability_path)
        stability_cols = [
            c
            for c in ("bo_call", "n_topics_median", "n_topics_std", "stability_pass", "refit_collapse")
            if c in stability.columns
        ]
        merged = comparison.merge(stability[stability_cols], on="bo_call", how="outer")
        merged = merged.rename(
            columns={
                "coherence_c_v": "refit_coherence_c_v",
                "n_topics": "refit_n_topics",
                "topic_diversity": "refit_topic_diversity",
                "outlier_rate": "refit_outlier_rate",
                "n_topics_std": "refit_n_topics_std",
                "n_topics_median": "refit_n_topics_median",
            }
        )
        merged["run_id"] = run["run_id"]
        merged["model_label"] = run.get("label", run["run_id"])
        frames.append(merged)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def load_top_k_sets(
    runs: list[dict[str, Any]], project_root: Path
) -> dict[tuple[str, str], pd.DataFrame]:
    """Load strategy top-k CSVs keyed by (run_id, strategy_name)."""
    top_sets: dict[tuple[str, str], pd.DataFrame] = {}
    for run in runs:
        run_id = run["run_id"]
        top_models_dir = resolve_path(Path(run["outputs"]["top_models_dir"]), project_root)
        for strategy, filename in STRATEGY_FILES.items():
            path = top_models_dir / filename
            if not path.exists():
                raise FileNotFoundError(
                    f"Missing {path}. Run 04_pareto_efficiency_analysis_v3.ipynb first."
                )
            df = pd.read_csv(path)
            df["run_id"] = run_id
            df["model_label"] = run.get("label", run_id)
            top_sets[(run_id, strategy)] = df
    return top_sets


def metric_snapshot(
    df: pd.DataFrame,
    cols: tuple[str, ...] = ("Coherence", "Topic_Diversity", "n_topics"),
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for col in cols:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        rows.append(
            {
                "metric": col,
                "n": len(series),
                "median": round(float(series.median()), 4) if len(series) else np.nan,
                "q25": round(float(series.quantile(0.25)), 4) if len(series) else np.nan,
                "q75": round(float(series.quantile(0.75)), 4) if len(series) else np.nan,
                "min": round(float(series.min()), 4) if len(series) else np.nan,
                "max": round(float(series.max()), 4) if len(series) else np.nan,
            }
        )
    return pd.DataFrame(rows).set_index("metric")


def compare_metric_snapshot_by_run(
    df_raw: pd.DataFrame,
    filtered_by_run: dict[str, pd.DataFrame],
    runs: list[dict[str, Any]],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for run in runs:
        run_id = run["run_id"]
        label = run.get("label", run_id)
        for stage, frame in (
            ("raw", df_raw[df_raw["run_id"] == run_id]),
            ("filtered", filtered_by_run.get(run_id, pd.DataFrame())),
        ):
            renamed = frame.rename(columns=LEGACY_RENAME)
            snap = metric_snapshot(renamed)
            for metric, row in snap.iterrows():
                rows.append(
                    {
                        "run_id": run_id,
                        "model_label": label,
                        "stage": stage,
                        "metric": metric,
                        **row.to_dict(),
                    }
                )
    return pd.DataFrame(rows)
