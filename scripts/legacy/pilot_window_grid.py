#!/usr/bin/env python3
"""Grid search min_cluster_size on cached 5-sentence window pilot embeddings."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import time
from pathlib import Path
from typing import Any

import numpy as np

from pilot_five_sentence_windows import DEFAULT_FLAT_HP, fit_bertopic_on_windows

LOGGER = logging.getLogger("window_grid")

# call_3 ratios for coupled params
_MCS_REF = 731
_MTS_REF = 450
_MS_REF = 27


def _hp_for_min_cluster_size(base: dict[str, Any], min_cluster_size: int) -> dict[str, Any]:
    hp = dict(base)
    ratio = min_cluster_size / _MCS_REF
    hp["hdbscan__min_cluster_size"] = int(min_cluster_size)
    hp["bertopic__min_topic_size"] = max(10, int(round(_MTS_REF * ratio)))
    hp["hdbscan__min_samples"] = max(5, int(round(_MS_REF * ratio)))
    hp["bertopic__verbose"] = False
    return hp


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        default="results/experiments/window_pilot_minilm12_seed42",
        type=Path,
    )
    parser.add_argument(
        "--out-dir",
        default="results/experiments/window_pilot_minilm12_seed42/grid",
        type=Path,
    )
    parser.add_argument(
        "--min-cluster-sizes",
        default="50,75,100,125,150,175,200,250,300",
        help="Comma-separated grid values.",
    )
    parser.add_argument(
        "--embedding-model",
        default="sentence-transformers/all-MiniLM-L12-v2",
    )
    parser.add_argument(
        "--target-min-topics",
        default=20,
        type=int,
    )
    parser.add_argument(
        "--target-max-topics",
        default=50,
        type=int,
    )
    parser.add_argument(
        "--target-max-outlier-pct",
        default=30.0,
        type=float,
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    cache_dir = args.cache_dir
    windows_npz = cache_dir / "windows_w5.npz"
    embed_path = cache_dir / "window_embeddings.npy"
    if not windows_npz.exists() or not embed_path.exists():
        raise FileNotFoundError(f"Missing cache under {cache_dir}")

    cached = np.load(windows_npz, allow_pickle=True)
    window_docs = cached["docs"].tolist()
    embeddings = np.asarray(np.load(embed_path), dtype=np.float32)
    LOGGER.info("Loaded %d cached windows, embeddings %s", len(window_docs), embeddings.shape)

    grid_values = [int(x.strip()) for x in args.min_cluster_sizes.split(",") if x.strip()]
    base_hp = dict(DEFAULT_FLAT_HP)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    t_all = time.perf_counter()

    for mcs in grid_values:
        flat_hp = _hp_for_min_cluster_size(base_hp, mcs)
        LOGGER.info(
            "Grid fit mcs=%d mts=%d min_samples=%d ...",
            flat_hp["hdbscan__min_cluster_size"],
            flat_hp["bertopic__min_topic_size"],
            flat_hp["hdbscan__min_samples"],
        )
        _, metrics = fit_bertopic_on_windows(
            window_docs,
            embeddings,
            flat_hp,
            args.embedding_model,
            use_representation=False,
        )
        row = {
            "hdbscan__min_cluster_size": flat_hp["hdbscan__min_cluster_size"],
            "bertopic__min_topic_size": flat_hp["bertopic__min_topic_size"],
            "hdbscan__min_samples": flat_hp["hdbscan__min_samples"],
            "n_topics": metrics["n_topics"],
            "outlier_pct": metrics["outlier_pct"],
            "fit_seconds": metrics["fit_seconds"],
            "top_topic_words": "; ".join(
                " ".join(t["words"][:5]) for t in metrics["top5_topics"][:3]
            ),
        }
        rows.append(row)
        LOGGER.info(
            "  -> n_topics=%d outlier=%.1f%% (%.1fs)",
            row["n_topics"],
            row["outlier_pct"],
            row["fit_seconds"],
        )

    csv_path = args.out_dir / "grid_results.csv"
    fieldnames = list(rows[0].keys())
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    hits = [
        r
        for r in rows
        if args.target_min_topics <= r["n_topics"] <= args.target_max_topics
        and r["outlier_pct"] < args.target_max_outlier_pct
    ]
    best = None
    if hits:
        best = sorted(hits, key=lambda r: (-r["n_topics"], r["outlier_pct"]))[0]
    else:
        # fallback: closest to target topic band with lowest outliers
        best = sorted(
            rows,
            key=lambda r: (
                0
                if args.target_min_topics <= r["n_topics"] <= args.target_max_topics
                else min(
                    abs(r["n_topics"] - args.target_min_topics),
                    abs(r["n_topics"] - args.target_max_topics),
                ),
                r["outlier_pct"],
            ),
        )[0]

    summary = {
        "n_windows": len(window_docs),
        "grid_values": grid_values,
        "target": {
            "n_topics": [args.target_min_topics, args.target_max_topics],
            "max_outlier_pct": args.target_max_outlier_pct,
        },
        "hits_in_target": hits,
        "best_pick": best,
        "total_grid_seconds": round(time.perf_counter() - t_all, 2),
        "sentence_baseline_call_3": {
            "n_topics": 45,
            "outlier_pct": 72.56,
        },
    }
    summary_path = args.out_dir / "grid_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    LOGGER.info("Wrote %s", csv_path)
    LOGGER.info("Wrote %s", summary_path)
    LOGGER.info(
        "Best pick: mcs=%s -> %d topics, %.1f%% outliers (%.0fs total)",
        best["hdbscan__min_cluster_size"],
        best["n_topics"],
        best["outlier_pct"],
        summary["total_grid_seconds"],
    )
    if hits:
        LOGGER.info("%d configuration(s) hit target band.", len(hits))
    else:
        LOGGER.info("No configuration hit target band; reported closest fallback.")


if __name__ == "__main__":
    main()
