#!/usr/bin/env python3
"""Aggregate hard topic assignments to book, tertile and chapter level.

Why hard assignments rather than the soft probabilities used earlier in the pipeline:
averaging 374 topic probabilities over roughly 6,000 sentences per book produces almost
identical vectors for every book (median per-topic coefficient of variation 0.087, and
taxonomy 2.1 sits at 20.23% +/- 0.25pp for all 16,000 books). Counting each sentence's
argmax topic instead gives a median CV of 0.877, is directly readable as "3.3% of this
book's sentences", and costs only the 0.74% of sentences assigned to the outlier topic.

Reads only four of the 376 columns in the sentence parquet files, so a pass over ~250 GB
of input finishes in minutes.

Outputs (under `outputs.hard_counts_dir`):
  book_topic_counts.parquet     book_id, topic_id, n_sentences, share
  tertile_topic_counts.parquet  book_id, tertile, topic_id, n_sentences, share
  chapter_topic_counts.parquet  book_id, chapter_index, topic_id, n_sentences, share
  book_totals.parquet           book_id, split, n_sentences, n_chapters, n_topics_present,
                                outlier_share, n_sentences_assigned

Usage:
  .venv/bin/python src/stage10_correlation_analysis/data_preparation/05_aggregate_hard_assignments.py
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import List

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage10_correlation_analysis.analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_analysis_config,
)

LOGGER = logging.getLogger("stage10.hard_aggregation")


def setup_logging(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    for handler in (
        logging.FileHandler(output_dir / "05_aggregate_hard_assignments.log", mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ):
        handler.setFormatter(fmt)
        LOGGER.addHandler(handler)


def parquet_list_sql(files: List[Path]) -> str:
    quoted = ", ".join(f"'{f}'" for f in files)
    return f"read_parquet([{quoted}])"


def materialize_sentences(con: duckdb.DuckDBPyConnection, files: List[Path]) -> int:
    """Materialise the five columns we need into one narrow table, with a tertile label.

    This is deliberately a table rather than a view. As a view, each of the four
    downstream aggregations re-scans all 255 GB of parquet and recomputes the window
    function; materialising costs one scan and one sort, and the resulting table is only
    about 3 GB (five small integer columns over ~115M rows).

    Tertiles use `ntile(3)` over the book's sentences in reading order, so each tertile
    holds the same number of sentences regardless of chapter lengths. Outlier sentences
    stay in the ordering — they are part of the narrative — but are excluded from share
    denominators later, so tertile boundaries do not shift when outliers are dropped.
    """
    LOGGER.info("Materialising narrow sentence table (one pass over the parquet files) ...")
    t0 = time.perf_counter()
    con.execute(
        f"""
        create or replace table sentences as
        select
            work_id::int          as book_id,
            chapter_index::int    as chapter_index,
            topic::smallint       as topic_id,
            split,
            ntile(3) over (
                partition by work_id
                order by chapter_index, sentence_index
            )::tinyint            as tertile_num
        from {parquet_list_sql(files)}
        """
    )
    n_rows = con.execute("select count(*) from sentences").fetchone()[0]
    LOGGER.info(
        "  %s sentence rows materialised in %.1f min",
        f"{n_rows:,}", (time.perf_counter() - t0) / 60,
    )
    return int(n_rows)


def write(df: pd.DataFrame, path: Path, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    LOGGER.info("Wrote %s: %s rows -> %s", label, f"{len(df):,}", path)


def aggregate(
    con: duckdb.DuckDBPyConnection,
    out_dir: Path,
    *,
    outlier_topic_id: int,
    drop_outlier: bool,
) -> pd.DataFrame:
    # Shares are denominated in assigned (non-outlier) sentences when drop_outlier is on,
    # so per-book shares sum to exactly 1 over the 348 real topics.
    share_filter = f"and topic_id <> {outlier_topic_id}" if drop_outlier else ""

    LOGGER.info("Book totals and outlier share ...")
    t0 = time.perf_counter()
    book_totals = con.execute(
        f"""
        select
            book_id,
            any_value(split)                                          as split,
            count(*)                                                  as n_sentences,
            count(distinct chapter_index)                             as n_chapters,
            sum(case when topic_id = {outlier_topic_id} then 1 else 0 end) as n_outlier_sentences,
            sum(case when topic_id = {outlier_topic_id} then 1 else 0 end) * 1.0 / count(*) as outlier_share,
            count(*) - sum(case when topic_id = {outlier_topic_id} then 1 else 0 end) as n_sentences_assigned,
            count(distinct case when topic_id <> {outlier_topic_id} then topic_id end) as n_topics_present
        from sentences
        group by book_id
        order by book_id
        """
    ).df()
    LOGGER.info("  %s books in %.1fs", f"{len(book_totals):,}", time.perf_counter() - t0)
    write(book_totals, out_dir / "book_totals.parquet", "book_totals")

    LOGGER.info("Book x topic counts ...")
    t0 = time.perf_counter()
    book_topic = con.execute(
        f"""
        with counts as (
            select book_id, topic_id, count(*) as n_sentences
            from sentences
            where true {share_filter}
            group by book_id, topic_id
        )
        select
            book_id,
            topic_id,
            n_sentences,
            n_sentences * 1.0 / sum(n_sentences) over (partition by book_id) as share
        from counts
        order by book_id, topic_id
        """
    ).df()
    LOGGER.info("  %s rows in %.1fs", f"{len(book_topic):,}", time.perf_counter() - t0)
    write(book_topic, out_dir / "book_topic_counts.parquet", "book_topic_counts")

    LOGGER.info("Tertile x topic counts ...")
    t0 = time.perf_counter()
    tertile_topic = con.execute(
        f"""
        with counts as (
            select
                book_id,
                case tertile_num when 1 then 'begin' when 2 then 'middle' else 'end' end as tertile,
                topic_id,
                count(*) as n_sentences
            from sentences
            where true {share_filter}
            group by book_id, tertile_num, topic_id
        )
        select
            book_id,
            tertile,
            topic_id,
            n_sentences,
            n_sentences * 1.0 / sum(n_sentences) over (partition by book_id, tertile) as share
        from counts
        order by book_id, tertile, topic_id
        """
    ).df()
    LOGGER.info("  %s rows in %.1fs", f"{len(tertile_topic):,}", time.perf_counter() - t0)
    write(tertile_topic, out_dir / "tertile_topic_counts.parquet", "tertile_topic_counts")

    LOGGER.info("Chapter x topic counts ...")
    t0 = time.perf_counter()
    chapter_topic = con.execute(
        f"""
        with counts as (
            select book_id, chapter_index, topic_id, count(*) as n_sentences
            from sentences
            where true {share_filter}
            group by book_id, chapter_index, topic_id
        )
        select
            book_id,
            chapter_index,
            topic_id,
            n_sentences,
            n_sentences * 1.0 / sum(n_sentences) over (partition by book_id, chapter_index) as share
        from counts
        order by book_id, chapter_index, topic_id
        """
    ).df()
    LOGGER.info("  %s rows in %.1fs", f"{len(chapter_topic):,}", time.perf_counter() - t0)
    write(chapter_topic, out_dir / "chapter_topic_counts.parquet", "chapter_topic_counts")

    validate(book_topic, tertile_topic, book_totals)
    return book_totals


def validate(
    book_topic: pd.DataFrame,
    tertile_topic: pd.DataFrame,
    book_totals: pd.DataFrame,
) -> None:
    """Fail loudly if the shares are not a valid composition."""
    LOGGER.info("Validating share invariants ...")

    book_sums = book_topic.groupby("book_id")["share"].sum()
    worst = (book_sums - 1.0).abs().max()
    if worst > 1e-6:
        raise AssertionError(f"Book shares do not sum to 1; worst deviation {worst:.2e}")
    LOGGER.info("  book shares sum to 1 (max deviation %.2e)", worst)

    tertile_sums = tertile_topic.groupby(["book_id", "tertile"])["share"].sum()
    worst_t = (tertile_sums - 1.0).abs().max()
    if worst_t > 1e-6:
        raise AssertionError(f"Tertile shares do not sum to 1; worst deviation {worst_t:.2e}")
    LOGGER.info("  tertile shares sum to 1 (max deviation %.2e)", worst_t)

    n_books = book_totals["book_id"].nunique()
    if book_topic["book_id"].nunique() != n_books:
        raise AssertionError(
            f"Book coverage mismatch: {book_topic['book_id'].nunique()} in counts "
            f"vs {n_books} in totals"
        )
    missing_tertiles = (
        tertile_topic.groupby("book_id")["tertile"].nunique().pipe(lambda s: s[s < 3])
    )
    if len(missing_tertiles):
        LOGGER.warning(
            "  %d books have fewer than 3 non-empty tertiles (very short books)",
            len(missing_tertiles),
        )

    LOGGER.info(
        "  outlier share: mean %.4f, median %.4f, p99 %.4f",
        book_totals["outlier_share"].mean(),
        book_totals["outlier_share"].median(),
        book_totals["outlier_share"].quantile(0.99),
    )
    LOGGER.info(
        "  sentences per book: median %s, min %s, max %s",
        f"{int(book_totals['n_sentences'].median()):,}",
        f"{int(book_totals['n_sentences'].min()):,}",
        f"{int(book_totals['n_sentences'].max()):,}",
    )


def report_variance_gain(book_topic: pd.DataFrame, cfg, out_dir: Path) -> None:
    """Quantify the hard-vs-soft variance gap that motivated this script.

    Notebook 00 shows this comparison; writing it here means the claim is measured by the
    same code that produces the data rather than restated by hand.
    """
    soft_path = cfg.input_path("soft_book_topic_probs")
    if soft_path is None or not soft_path.exists():
        LOGGER.info("Soft probability table absent; skipping variance comparison")
        return

    LOGGER.info("Comparing between-book variance, hard vs soft ...")
    soft = pd.read_parquet(soft_path)

    def cv_by_topic(df: pd.DataFrame, value: str) -> pd.Series:
        stats = df.groupby("topic_id")[value].agg(["mean", "std"])
        return (stats["std"] / stats["mean"]).replace([float("inf")], pd.NA).dropna()

    hard_cv = cv_by_topic(book_topic, "share")
    soft_cv = cv_by_topic(soft, "prob")
    comparison = pd.DataFrame({
        "measure": ["hard_assignment", "soft_probability"],
        "n_topics": [len(hard_cv), len(soft_cv)],
        "median_cv": [hard_cv.median(), soft_cv.median()],
        "mean_cv": [hard_cv.mean(), soft_cv.mean()],
        "p90_cv": [hard_cv.quantile(0.9), soft_cv.quantile(0.9)],
    })
    write(comparison, out_dir / "hard_vs_soft_variance.parquet", "hard_vs_soft_variance")
    LOGGER.info(
        "  median per-topic CV: hard %.3f vs soft %.3f (%.1fx more between-book signal)",
        hard_cv.median(), soft_cv.median(), hard_cv.median() / max(soft_cv.median(), 1e-12),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=str, default=DEFAULT_CONFIG_PATH)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--memory-limit", type=str, default="16GB")
    ap.add_argument("--skip-variance-report", action="store_true")
    ap.add_argument("--keep-scratch", action="store_true", help="Keep the intermediate DuckDB file")
    ap.add_argument(
        "--only-file",
        type=str,
        default=None,
        help="Substring filter on input filenames, for a smoke test on one split.",
    )
    ap.add_argument(
        "--output-suffix",
        type=str,
        default="",
        help="Suffix appended to the output directory, so a smoke test cannot clobber the real run.",
    )
    args = ap.parse_args()

    cfg = load_analysis_config(args.config)
    out_dir = cfg.output_path("hard_counts_dir")
    if args.output_suffix:
        out_dir = out_dir.parent / f"{out_dir.name}{args.output_suffix}"
    out_dir.mkdir(parents=True, exist_ok=True)
    setup_logging(out_dir)

    LOGGER.info("=" * 78)
    LOGGER.info("Stage10 hard-assignment aggregation — run %s", cfg.run_id)
    LOGGER.info("=" * 78)

    files = cfg.sentence_topic_files()
    if args.only_file:
        files = [f for f in files if args.only_file in f.name]
        if not files:
            raise SystemExit(f"No input file name contains {args.only_file!r}")
        LOGGER.warning("SMOKE TEST: restricted to %s", [f.name for f in files])
    total_gb = sum(f.stat().st_size for f in files) / 1e9
    LOGGER.info("Input: %d parquet files, %.1f GB total", len(files), total_gb)
    for f in files:
        LOGGER.info("  %s (%.1f GB)", f.name, f.stat().st_size / 1e9)

    outlier_topic_id = int(cfg.section("measurement", "outlier_topic_id"))
    drop_outlier = bool(cfg.section("measurement", "drop_outlier_from_shares"))
    LOGGER.info(
        "Outlier topic %d is %s from share denominators",
        outlier_topic_id, "excluded" if drop_outlier else "included",
    )

    # File-backed so the materialised sentence table and the sort spill to the results
    # volume rather than into RAM or a possibly small /tmp.
    scratch_dir = out_dir / "_duckdb_tmp"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    db_path = scratch_dir / "hard_agg.duckdb"
    db_path.unlink(missing_ok=True)

    con = duckdb.connect(str(db_path))
    con.execute(f"pragma threads={args.threads}")
    con.execute(f"pragma memory_limit='{args.memory_limit}'")
    con.execute(f"pragma temp_directory='{scratch_dir}'")
    con.execute("pragma preserve_insertion_order=false")

    started = time.perf_counter()
    materialize_sentences(con, files)
    aggregate(con, out_dir, outlier_topic_id=outlier_topic_id, drop_outlier=drop_outlier)

    if not args.skip_variance_report:
        book_topic = pd.read_parquet(out_dir / "book_topic_counts.parquet")
        report_variance_gain(book_topic, cfg, out_dir)

    LOGGER.info("=" * 78)
    LOGGER.info("Done in %.1f min", (time.perf_counter() - started) / 60)
    LOGGER.info("=" * 78)

    con.close()
    if not args.keep_scratch:
        for leftover in scratch_dir.glob("hard_agg.duckdb*"):
            leftover.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
