#!/usr/bin/env python3
"""Select Phase 2 stability-rerun candidates from v4 granular Phase 1 BO trials."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from src.common.config import resolve_path

BANDS: list[tuple[str, int, int]] = [
    ("A", 50, 120),
    ("B", 120, 250),
    ("C", 250, 500),
    ("D", 500, 800),
]

HYPER_COL_PREFIXES = (
    "umap__",
    "hdbscan__",
    "vectorizer__",
    "bertopic__",
)


def _hyper_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if any(c.startswith(p) for p in HYPER_COL_PREFIXES)]


def _hyper_signature(row: pd.Series, cols: list[str]) -> str:
    payload = {c: row.get(c) for c in cols}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def _score_column(df: pd.DataFrame) -> str:
    if "bo_objective" in df.columns and df["bo_objective"].notna().any():
        return "bo_objective"
    return "coherence_c_v"


def filter_candidates(
    df: pd.DataFrame,
    *,
    per_band: int = 12,
    min_n_topics: int = 50,
    max_outlier_rate: float = 0.85,
    max_largest_topic_share: float = 0.20,
    min_median_topic_size: float = 25.0,
) -> pd.DataFrame:
    work = df.copy()
    score_col = _score_column(work)

    if "n_topics" in work.columns:
        work = work[work["n_topics"].fillna(0) >= min_n_topics]
    if "outlier_rate" in work.columns:
        work = work[work["outlier_rate"].fillna(1.0) <= max_outlier_rate]
    if "largest_topic_share" in work.columns:
        work = work[work["largest_topic_share"].fillna(1.0) <= max_largest_topic_share]
    if "median_topic_size" in work.columns:
        work = work[work["median_topic_size"].fillna(0) >= min_median_topic_size]

    hyper_cols = _hyper_cols(work)
    seen: set[str] = set()
    selected: list[pd.Series] = []

    for band, lo, hi in BANDS:
        band_df = work[(work["n_topics"] >= lo) & (work["n_topics"] < hi)].copy()
        if band_df.empty:
            continue
        band_df = band_df.sort_values(score_col, ascending=False)
        for _, row in band_df.iterrows():
            sig = _hyper_signature(row, hyper_cols)
            if sig in seen:
                continue
            seen.add(sig)
            out = row.copy()
            out["granularity_band"] = band
            selected.append(out)
            if sum(1 for s in selected if s["granularity_band"] == band) >= per_band:
                break

    if not selected:
        return pd.DataFrame()
    return pd.DataFrame(selected).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=Path, required=True, help="Phase 1 trials_partial.csv")
    parser.add_argument("--run-id", type=str, required=True)
    parser.add_argument("--per-band", type=int, default=12)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV (default: results/selection/{run_id}/phase2_candidates.csv)",
    )
    args = parser.parse_args()

    trials_path = resolve_path(args.trials)
    df = pd.read_csv(trials_path)
    candidates = filter_candidates(df, per_band=args.per_band)

    out_path = args.output
    if out_path is None:
        out_path = resolve_path(Path("results/selection")) / args.run_id / "phase2_candidates.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    candidates.to_csv(out_path, index=False)

    print(f"Wrote {len(candidates)} candidates to {out_path}")
    if not candidates.empty and "bo_call" in candidates.columns:
        calls = ",".join(str(int(c)) for c in candidates["bo_call"].tolist())
        print(f"bo_calls for compare-fit: {calls}")


if __name__ == "__main__":
    main()
