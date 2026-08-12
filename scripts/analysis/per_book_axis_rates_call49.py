#!/usr/bin/env python3
"""Per-book axis-lexicon rates across the full call-49 corpus.

Question this answers: does luxury (H3) concentrate in a subgenre? If a minority
of books carry most luxury language, H3 stays testable on between-book variation
even though no single topic owns the axis.

Controls run alongside the targets so "concentrated" is judged against axes whose
behaviour we already know (kissing = ubiquitous, spaceflight = absent).

Outputs under <out-dir>/:
  per_book_axis_rates.parquet   one row per book, counts + per-1k rates
  axis_concentration_summary.csv distribution stats per axis
  luxury_top_books.csv           highest-luxury books joined to metadata

Usage:
  .venv/bin/python scripts/analysis/per_book_axis_rates_call49.py
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from pathlib import Path

import duckdb
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_axis_lexicon_call49 import LEXICONS  # noqa: E402

# Axes kept for the corpus-wide scan; each adds a regex pass over ~115M rows.
SCAN_AXES = [
    "luxury_strict",
    "luxury_H3",
    "security_strict",
    "security_H4",
    "kissing_control",
    "wedding_hea_control",
    "possessive_control",
    "spaceflight_negcontrol",
]


def re2_pattern(terms: list[str]) -> str:
    escaped = [re.escape(t) for t in sorted(terms, key=len, reverse=True)]
    return r"(?i)\b(" + "|".join(escaped) + r")\b"


def gini(x: np.ndarray) -> float:
    if x.size == 0 or x.sum() == 0:
        return float("nan")
    xs = np.sort(x.astype(float))
    n = xs.size
    idx = np.arange(1, n + 1)
    return float((2 * (idx * xs).sum()) / (n * xs.sum()) - (n + 1) / n)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--infer-dir",
        type=Path,
        default=Path("results/experiments/v4_l12_granular_final_call49/full_corpus_infer"),
    )
    ap.add_argument("--splits", type=str, default="train,val,test")
    ap.add_argument(
        "--metadata",
        type=Path,
        default=Path(
            "data/raw/romance_subdataset_filtered_v3/subsampling_metadata/"
            "romance_subdataset_filtered_v3_full.csv"
        ),
    )
    ap.add_argument("--out-dir", type=Path, default=Path("results/reports/call49/axis_audit"))
    ap.add_argument("--threads", type=int, default=6)
    ap.add_argument("--min-sentences", type=int, default=1000, help="Book filter for rate stats")
    args = ap.parse_args()

    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    paths = []
    for s in splits:
        p = args.infer_dir / f"sentence_topics_{s}.parquet"
        if not p.exists():
            raise FileNotFoundError(p)
        paths.append(str(p.resolve()))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = args.out_dir / "_tmp"
    tmp_dir.mkdir(exist_ok=True)

    con = duckdb.connect()
    con.execute(f"SET threads TO {args.threads}")
    con.execute("SET preserve_insertion_order=false")
    con.execute(f"SET temp_directory='{tmp_dir.resolve()}'")

    axes = [a for a in SCAN_AXES if a in LEXICONS]
    count_exprs = ",\n          ".join(
        f"SUM(CASE WHEN regexp_matches(sentence, '{re2_pattern(LEXICONS[a]['terms'])}') "
        f"THEN 1 ELSE 0 END)::BIGINT AS n_{a}"
        for a in axes
    )

    print(f"axes: {len(axes)} | splits: {splits}", flush=True)
    per_split_tables = []
    for split, path in zip(splits, paths):
        t0 = time.time()
        tbl = f"book_counts_{split}"
        print(f"[{split}] scanning {Path(path).name} ...", flush=True)
        con.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE {tbl} AS
            SELECT
              work_id::BIGINT AS work_id,
              '{split}' AS split,
              COUNT(*)::BIGINT AS n_sentences,
              {count_exprs}
            FROM read_parquet('{path}')
            GROUP BY work_id
            """
        )
        n = con.execute(f"SELECT COUNT(*), SUM(n_sentences) FROM {tbl}").fetchone()
        print(
            f"[{split}] done in {time.time() - t0:,.0f}s | books={n[0]:,} sentences={n[1]:,}",
            flush=True,
        )
        per_split_tables.append(tbl)

    union_sql = "\nUNION ALL\n".join(f"SELECT * FROM {t}" for t in per_split_tables)
    rate_exprs = ",\n          ".join(
        f"(n_{a} * 1000.0 / n_sentences) AS rate_{a}" for a in axes
    )
    per_book_path = str((args.out_dir / "per_book_axis_rates.parquet").resolve())
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE per_book AS
        SELECT *, {rate_exprs}
        FROM ({union_sql})
        """
    )
    con.execute(f"COPY per_book TO '{per_book_path}' (FORMAT PARQUET)")
    print(f"wrote {per_book_path}", flush=True)

    df = con.execute(
        f"SELECT * FROM per_book WHERE n_sentences >= {int(args.min_sentences)}"
    ).fetchdf()
    print(f"\nbooks with >= {args.min_sentences} sentences: {len(df):,}\n")

    header = (
        f"{'axis':<24} {'role':<18} {'mean/1k':>8} {'med':>7} {'p90':>7} "
        f"{'p99':>8} {'max':>9} {'CV':>6} {'gini':>6} {'top5%share':>11} {'books=0%':>9}"
    )
    print(header)
    print("-" * len(header))
    rows = []
    for a in axes:
        r = df[f"rate_{a}"].to_numpy()
        counts = df[f"n_{a}"].to_numpy()
        total = counts.sum()
        k = max(int(round(0.05 * len(r))), 1)
        top5_share = 100 * np.sort(counts)[-k:].sum() / total if total else float("nan")
        cv = float(r.std() / r.mean()) if r.mean() else float("nan")
        zero_pct = 100 * float((counts == 0).mean())
        stat = {
            "axis": a,
            "role": LEXICONS[a]["role"],
            "mean_per_1k": round(float(r.mean()), 4),
            "median_per_1k": round(float(np.median(r)), 4),
            "p90_per_1k": round(float(np.percentile(r, 90)), 4),
            "p99_per_1k": round(float(np.percentile(r, 99)), 4),
            "max_per_1k": round(float(r.max()), 4),
            "cv": round(cv, 3),
            "gini": round(gini(counts.astype(float)), 3),
            "top5pct_books_share_of_matches": round(float(top5_share), 2),
            "pct_books_zero": round(zero_pct, 2),
        }
        rows.append(stat)
        print(
            f"{a:<24} {LEXICONS[a]['role']:<18} {stat['mean_per_1k']:>8.3f} "
            f"{stat['median_per_1k']:>7.3f} {stat['p90_per_1k']:>7.3f} "
            f"{stat['p99_per_1k']:>8.3f} {stat['max_per_1k']:>9.3f} "
            f"{stat['cv']:>6.2f} {stat['gini']:>6.3f} "
            f"{stat['top5pct_books_share_of_matches']:>10.1f}% {stat['pct_books_zero']:>8.1f}%"
        )

    with open(args.out_dir / "axis_concentration_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Top luxury books joined to metadata → is the tail a recognisable subgenre?
    if args.metadata.exists():
        meta_path = str(args.metadata.resolve())
        top = con.execute(
            f"""
            SELECT
              p.work_id, p.split, p.n_sentences,
              ROUND(p.rate_luxury_strict, 3) AS rate_luxury_strict,
              ROUND(p.rate_luxury_H3, 3) AS rate_luxury_loose,
              ROUND(p.rate_kissing_control, 3) AS rate_kissing,
              m.title, m.author_name, m.publication_year, m.genres_str
            FROM per_book p
            LEFT JOIN read_csv_auto('{meta_path}') m
              ON p.work_id = m.work_id
            WHERE p.n_sentences >= {int(args.min_sentences)}
            ORDER BY p.rate_luxury_strict DESC
            LIMIT 40
            """
        ).fetchdf()
        top.to_csv(args.out_dir / "luxury_top_books.csv", index=False)
        print("\n### highest luxury_strict books")
        for _, r in top.head(20).iterrows():
            title = str(r.get("title", ""))[:42]
            auth = str(r.get("author_name", ""))[:22]
            print(
                f"  {r['rate_luxury_strict']:>6.2f}/1k  {title:<42} {auth:<22} "
                f"{str(r.get('publication_year', '')):<6}"
            )

        # Genre-group contrast: where does luxury sit by subgenre tag?
        genre = con.execute(
            f"""
            SELECT
              COALESCE(m.genre_group, 'unknown') AS genre_group,
              COUNT(*) AS n_books,
              ROUND(AVG(p.rate_luxury_strict), 3) AS mean_luxury_strict,
              ROUND(MEDIAN(p.rate_luxury_strict), 3) AS med_luxury_strict,
              ROUND(AVG(p.rate_kissing_control), 3) AS mean_kissing,
              ROUND(AVG(p.rate_security_strict), 3) AS mean_security_strict
            FROM per_book p
            LEFT JOIN read_csv_auto('{meta_path}') m ON p.work_id = m.work_id
            WHERE p.n_sentences >= {int(args.min_sentences)}
            GROUP BY 1
            ORDER BY mean_luxury_strict DESC
            """
        ).fetchdf()
        genre.to_csv(args.out_dir / "luxury_by_genre_group.csv", index=False)
        print("\n### luxury by genre group")
        print(genre.to_string(index=False))

    print("\ndone")


if __name__ == "__main__":
    main()
