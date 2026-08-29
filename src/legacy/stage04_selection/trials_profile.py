"""Type-aware summaries for Stage03 ``trials_partial.csv`` rows."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

# Columns emitted by ``project_result_to_trials`` (partial BO rows only).
TRIALS_PARTIAL_COLUMNS: tuple[str, ...] = (
    "run_id",
    "trial_id",
    "bo_call",
    "seed",
    "embedding_model",
    "coherence_c_v",
    "bo_objective",
    "topic_diversity",
    "n_topics",
    "stability_score",
    "train_csv",
    "eval_csv",
    "test_csv",
    "outlier_rate",
    "largest_topic_share",
    "median_topic_size",
    "p10_topic_size",
    "p90_topic_size",
    "n_tiny_topics_lt25",
    "n_tiny_topics_lt50",
    "n_topics_min",
    "n_topics_max",
    "n_topics_std",
    "n_topics_runs",
    "topic_stability_pass",
    "bertopic__min_topic_size",
    "bertopic__top_n_words",
    "hdbscan__min_cluster_size",
    "hdbscan__min_samples",
    "hdbscan__cluster_selection_method",
    "umap__min_dist",
    "umap__n_components",
    "umap__n_neighbors",
    "vectorizer__min_df",
)

# Columns from older pipeline versions that were never populated during BO.
# They are only dropped when entirely null: v4 granular runs populate
# ``outlier_rate`` during BO, in which case it is kept as a metric.
DEPRECATED_TRIALS_PARTIAL_COLUMNS: frozenset[str] = frozenset(
    {"coherence_c_npmi", "outlier_rate"}
)

# Semantic roles — statistics depend on role, not pandas dtype alone.
TRIALS_COLUMN_ROLES: dict[str, str] = {
    "run_id": "identifier",
    "trial_id": "identifier",
    "bo_call": "bo_index",
    "seed": "run_constant",
    "embedding_model": "categorical",
    "coherence_c_v": "metric_continuous",
    "bo_objective": "metric_continuous",
    "topic_diversity": "metric_continuous",
    "n_topics": "metric_continuous",
    "outlier_rate": "metric_continuous",
    "largest_topic_share": "metric_continuous",
    "median_topic_size": "metric_continuous",
    "p10_topic_size": "metric_continuous",
    "p90_topic_size": "metric_continuous",
    "n_tiny_topics_lt25": "metric_continuous",
    "n_tiny_topics_lt50": "metric_continuous",
    "stability_score": "run_constant",
    "train_csv": "path",
    "eval_csv": "path",
    "test_csv": "path",
    "n_topics_min": "metric_continuous",
    "n_topics_max": "metric_continuous",
    "n_topics_std": "stability_std",
    "n_topics_runs": "bo_run_count",
    "topic_stability_pass": "boolean",
    "bertopic__min_topic_size": "hyperparameter",
    "bertopic__top_n_words": "hyperparameter",
    "hdbscan__min_cluster_size": "hyperparameter",
    "hdbscan__min_samples": "hyperparameter",
    "hdbscan__cluster_selection_method": "categorical",
    "umap__min_dist": "hyperparameter",
    "umap__n_components": "hyperparameter",
    "umap__n_neighbors": "hyperparameter",
    "vectorizer__min_df": "hyperparameter",
}

ROLE_PRESENTATION: dict[str, str] = {
    "identifier": "Unique count and example value (no mean/std).",
    "bo_index": "BO iteration index: range and sequential check (not a random variable).",
    "run_constant": "Single value shared by all trials in a run.",
    "categorical": "Value counts for each level.",
    "path": "Unique path count and one example (paths are metadata, not metrics).",
    "boolean": "True/False counts and percentages.",
    "metric_continuous": "Missingness plus distribution (min, quartiles, max, mean, std).",
    "stability_std": "Topic-count std across BO model_runs; meaningful only when n_topics_runs > 1.",
    "bo_run_count": "Configured repeat fits per BO call (value counts, not a distribution).",
    "hyperparameter": "Sampled BO search-space parameters: distribution summary.",
}

ROLE_ORDER = [
    "identifier",
    "bo_index",
    "run_constant",
    "categorical",
    "path",
    "boolean",
    "bo_run_count",
    "metric_continuous",
    "stability_std",
    "hyperparameter",
]


def normalize_trials_partial_df(df: pd.DataFrame) -> pd.DataFrame:
    """Drop deprecated columns only when they are entirely null (older CSVs)."""
    drop = [
        c
        for c in DEPRECATED_TRIALS_PARTIAL_COLUMNS
        if c in df.columns and df[c].isna().all()
    ]
    if drop:
        df = df.drop(columns=drop)
    unknown = [c for c in df.columns if c not in TRIALS_COLUMN_ROLES]
    if unknown:
        raise KeyError(f"Unclassified trials columns: {unknown}")
    return df


def _pct(n: int, total: int) -> float:
    return round(100.0 * n / total, 1) if total else 0.0


def _example(value: Any) -> str:
    text = str(value)
    return text if len(text) <= 80 else text[:77] + "..."


def trials_schema_overview(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: role, dtype, missingness, and cardinality."""
    rows: list[dict[str, Any]] = []
    for col in df.columns:
        role = TRIALS_COLUMN_ROLES.get(col, "unknown")
        series = df[col]
        rows.append(
            {
                "column": col,
                "role": role,
                "presentation": ROLE_PRESENTATION.get(role, "Unclassified column."),
                "dtype": str(series.dtype),
                "non_null": int(series.notna().sum()),
                "missing_pct": _pct(int(series.isna().sum()), len(df)),
                "n_unique": int(series.nunique(dropna=True)),
            }
        )
    overview = pd.DataFrame(rows)
    role_rank = {role: i for i, role in enumerate(ROLE_ORDER)}
    overview["_role_rank"] = overview["role"].map(lambda r: role_rank.get(r, 99))
    return overview.sort_values(["_role_rank", "column"]).drop(columns="_role_rank")


def _summarize_identifiers(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        series = df[col]
        rows.append(
            {
                "column": col,
                "non_null": int(series.notna().sum()),
                "n_unique": int(series.nunique(dropna=True)),
                "example": _example(series.dropna().iloc[0]) if series.notna().any() else "",
            }
        )
    return pd.DataFrame(rows)


def _summarize_bo_index(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce").dropna().astype(int)
        values = series.sort_values().tolist()
        sequential = values == list(range(len(values)))
        rows.append(
            {
                "column": col,
                "non_null": int(df[col].notna().sum()),
                "n_unique": int(series.nunique()),
                "min": int(series.min()) if len(series) else np.nan,
                "max": int(series.max()) if len(series) else np.nan,
                "sequential_0_to_n_minus_1": bool(sequential),
            }
        )
    return pd.DataFrame(rows)


def _summarize_constants(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        non_null = df[col].dropna()
        rows.append(
            {
                "column": col,
                "non_null": int(non_null.shape[0]),
                "n_unique": int(non_null.nunique()),
                "value": _example(non_null.iloc[0]) if len(non_null) else "",
            }
        )
    return pd.DataFrame(rows)


def _summarize_categorical(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        counts = df[col].value_counts(dropna=False)
        for level, count in counts.items():
            rows.append(
                {
                    "column": col,
                    "level": _example(level),
                    "count": int(count),
                    "pct": _pct(int(count), len(df)),
                }
            )
    return pd.DataFrame(rows)


def _summarize_boolean(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        counts = df[col].value_counts(dropna=False)
        for level, count in counts.items():
            rows.append(
                {
                    "column": col,
                    "value": level,
                    "count": int(count),
                    "pct": _pct(int(count), len(df)),
                }
            )
    return pd.DataFrame(rows)


def _summarize_paths(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        non_null = df[col].dropna()
        rows.append(
            {
                "column": col,
                "non_null": int(non_null.shape[0]),
                "n_unique_paths": int(non_null.nunique()),
                "example": _example(non_null.iloc[0]) if len(non_null) else "",
            }
        )
    return pd.DataFrame(rows)


def _summarize_bo_run_count(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        counts = df[col].value_counts(dropna=False).sort_index()
        for level, count in counts.items():
            rows.append(
                {
                    "column": col,
                    "model_runs_per_bo_call": int(level),
                    "trial_count": int(count),
                    "pct": _pct(int(count), len(df)),
                }
            )
    return pd.DataFrame(rows)


def _summarize_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        non_null = series.dropna()
        if non_null.empty:
            rows.append(
                {
                    "column": col,
                    "non_null": 0,
                    "missing_pct": 100.0,
                    "mean": np.nan,
                    "std": np.nan,
                    "min": np.nan,
                    "p25": np.nan,
                    "median": np.nan,
                    "p75": np.nan,
                    "max": np.nan,
                }
            )
            continue
        rows.append(
            {
                "column": col,
                "non_null": int(non_null.shape[0]),
                "missing_pct": _pct(int(series.isna().sum()), len(df)),
                "mean": round(float(non_null.mean()), 6),
                "std": round(float(non_null.std()), 6),
                "min": round(float(non_null.min()), 6),
                "p25": round(float(non_null.quantile(0.25)), 6),
                "median": round(float(non_null.median()), 6),
                "p75": round(float(non_null.quantile(0.75)), 6),
                "max": round(float(non_null.max()), 6),
            }
        )
    return pd.DataFrame(rows)


def _summarize_stability_std(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if "n_topics_runs" not in df.columns:
        return _summarize_numeric(df, columns)

    max_runs = int(pd.to_numeric(df["n_topics_runs"], errors="coerce").max())
    if max_runs <= 1:
        return pd.DataFrame(
            [
                {
                    "column": columns[0] if columns else "n_topics_std",
                    "note": (
                        "All trials used 1 model_run per BO call (see result.json model_runs). "
                        "n_topics_std is 0 by definition; distribution stats are not shown."
                    ),
                    "max_model_runs_observed": max_runs,
                }
            ]
        )
    return _summarize_numeric(df, columns)


def summarize_trials_by_role(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return role-specific summary tables for all columns in ``df``."""
    df = normalize_trials_partial_df(df)

    by_role: dict[str, list[str]] = {role: [] for role in ROLE_ORDER}
    for col, role in TRIALS_COLUMN_ROLES.items():
        if col in df.columns:
            by_role.setdefault(role, []).append(col)

    summaries: dict[str, pd.DataFrame] = {"schema": trials_schema_overview(df)}
    if by_role["identifier"]:
        summaries["identifiers"] = _summarize_identifiers(df, by_role["identifier"])
    if by_role["bo_index"]:
        summaries["bo_index"] = _summarize_bo_index(df, by_role["bo_index"])
    if by_role["run_constant"]:
        summaries["run_constants"] = _summarize_constants(df, by_role["run_constant"])
    if by_role["categorical"]:
        summaries["categorical"] = _summarize_categorical(df, by_role["categorical"])
    if by_role["path"]:
        summaries["paths"] = _summarize_paths(df, by_role["path"])
    if by_role["boolean"]:
        summaries["boolean"] = _summarize_boolean(df, by_role["boolean"])
    if by_role["bo_run_count"]:
        summaries["bo_run_count"] = _summarize_bo_run_count(df, by_role["bo_run_count"])
    if by_role["metric_continuous"]:
        summaries["metrics"] = _summarize_numeric(df, by_role["metric_continuous"])
    if by_role["stability_std"]:
        summaries["stability_std"] = _summarize_stability_std(df, by_role["stability_std"])
    if by_role["hyperparameter"]:
        summaries["hyperparameters"] = _summarize_numeric(df, by_role["hyperparameter"])
    return summaries


SUMMARY_SECTIONS: tuple[tuple[str, str], ...] = (
    ("schema", "Column schema (all variables)"),
    ("identifiers", "Identifiers"),
    ("bo_index", "BO iteration index (not a metric)"),
    ("run_constants", "Run-level constants"),
    ("categorical", "Categorical levels"),
    ("paths", "Input paths (metadata)"),
    ("boolean", "Boolean flags"),
    ("bo_run_count", "BO model_runs per call (metadata)"),
    ("metrics", "Evaluation metrics"),
    ("stability_std", "Topic-count stability (n_topics_std)"),
    ("hyperparameters", "BO hyperparameters"),
)
