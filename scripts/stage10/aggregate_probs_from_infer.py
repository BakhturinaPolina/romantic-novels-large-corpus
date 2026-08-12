#!/usr/bin/env python3
"""Aggregate Stage05 infer-corpus sentence_topics_*.parquet → Stage10 topic probs.

Writes under <output-dir>/topic_probabilities/:
  book_topic_probs.parquet      [book_id, topic_id, prob]
  chapter_topic_probs.parquet   [book_id, chapter_id, topic_id, prob]
  tertile_topic_probs.parquet   [book_id, tertile, topic_id, prob]

Uses DuckDB over existing soft-prob columns (no BERTopic re-transform).

Usage:
  .venv/bin/python scripts/stage10/aggregate_probs_from_infer.py \
    --infer-dir results/experiments/v4_l12_granular_final_call49/full_corpus_infer \
    --output-dir results/stage10_correlation_analysis/v4_l12_granular_final_call49
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

import duckdb
import pyarrow.parquet as pq


def setup_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    return logging.getLogger("agg_from_infer")


def prob_columns(schema_names: list[str]) -> list[str]:
    cols = [c for c in schema_names if re.fullmatch(r"prob_\d+", c)]
    cols.sort(key=lambda c: int(c.split("_", 1)[1]))
    return cols


def unpivot_sql(
    source: str,
    id_cols: list[str],
    prob_cols: list[str],
    topic_ids: list[int],
) -> str:
    """Long-form probs from a mean_norm-like table with mass column."""
    ids = ", ".join(id_cols)
    tid_list = ", ".join(str(t) for t in topic_ids)
    val_list = ", ".join(
        f"CASE WHEN mass > 0 THEN {c} / mass ELSE 0 END" for c in prob_cols
    )
    # Paired unnest() in the same SELECT keeps list positions aligned (DuckDB 1.5).
    return f"""
    SELECT
      {ids},
      unnest([{tid_list}]::INTEGER[]) AS topic_id,
      unnest([{val_list}]::DOUBLE[]) AS prob
    FROM {source}
    """


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--infer-dir", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--splits", type=str, default="train,val,test")
    ap.add_argument("--min-sentences", type=int, default=3, help="Min sentences per book for tertiles")
    ap.add_argument("--skip-chapter", action="store_true")
    ap.add_argument("--skip-tertile", action="store_true")
    ap.add_argument("--tmp-dir", type=Path, default=None, help="Spill dir for tertile labels")
    args = ap.parse_args()

    logger = setup_logger()
    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    paths = []
    for s in splits:
        p = args.infer_dir / f"sentence_topics_{s}.parquet"
        if not p.exists():
            raise FileNotFoundError(p)
        paths.append(str(p.resolve()))

    sample = Path(paths[0])
    prob_cols = prob_columns(pq.read_schema(sample).names)
    if not prob_cols:
        raise RuntimeError(f"No prob_* columns in {sample}")
    topic_ids = [int(c.split("_", 1)[1]) for c in prob_cols]
    n_topics = len(prob_cols)
    logger.info(f"splits={splits} n_topics={n_topics} files={len(paths)}")

    out_dir = args.output_dir / "topic_probabilities"
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = args.tmp_dir or (out_dir / "_tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    con.execute("SET threads TO 4")
    con.execute("SET preserve_insertion_order=false")
    # Prefer spill to disk over OOM on large window/aggs
    con.execute(f"SET temp_directory='{tmp_dir.resolve()}'")
    con.execute("SET max_temp_directory_size='80GiB'")

    file_list_sql = ", ".join(f"'{p}'" for p in paths)
    # COALESCE misses NaN; soft-prob caches can contain NaN/inf.
    prob_zero = ", ".join(
        f"(CASE WHEN {c} IS NULL OR isnan({c}) OR isinf({c}) THEN 0.0 "
        f"ELSE GREATEST({c}::DOUBLE, 0.0) END) AS {c}"
        for c in prob_cols
    )
    prob_sum_exprs = ", ".join(f"SUM({c}) AS {c}" for c in prob_cols)
    mean_cols = ", ".join(f"({c} / n_sent) AS {c}" for c in prob_cols)
    mass_expr = " + ".join(f"({c} / n_sent)" for c in prob_cols)

    con.execute(
        f"""
        CREATE OR REPLACE VIEW sentences AS
        SELECT
          work_id::BIGINT AS book_id,
          chapter_index::BIGINT AS chapter_id,
          sentence_index::BIGINT AS sentence_index,
          {prob_zero}
        FROM read_parquet([{file_list_sql}], union_by_name=true)
        """
    )
    logger.info("registered sentences view")

    # ---- BOOK ----
    book_out = str((out_dir / "book_topic_probs.parquet").resolve())
    logger.info(f"aggregating BOOK → {book_out}")
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE book_sums AS
        SELECT book_id, COUNT(*)::BIGINT AS n_sent, {prob_sum_exprs}
        FROM sentences
        GROUP BY book_id
        """
    )
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE book_mean_norm AS
        SELECT book_id, {mean_cols}, ({mass_expr}) AS mass
        FROM book_sums
        """
    )
    book_long = unpivot_sql("book_mean_norm", ["book_id"], prob_cols, topic_ids)
    con.execute(f"COPY ({book_long}) TO '{book_out}' (FORMAT PARQUET)")
    n_books = con.execute("SELECT COUNT(*) FROM book_sums").fetchone()[0]
    logger.info(f"book_topic_probs done | books={n_books:,}")

    # ---- CHAPTER ----
    if not args.skip_chapter:
        chap_out = str((out_dir / "chapter_topic_probs.parquet").resolve())
        logger.info(f"aggregating CHAPTER → {chap_out}")
        con.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE chap_sums AS
            SELECT book_id, chapter_id, COUNT(*)::BIGINT AS n_sent, {prob_sum_exprs}
            FROM sentences
            GROUP BY book_id, chapter_id
            """
        )
        con.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE chap_mean_norm AS
            SELECT book_id, chapter_id, {mean_cols}, ({mass_expr}) AS mass
            FROM chap_sums
            """
        )
        chap_long = unpivot_sql(
            "chap_mean_norm", ["book_id", "chapter_id"], prob_cols, topic_ids
        )
        con.execute(f"COPY ({chap_long}) TO '{chap_out}' (FORMAT PARQUET)")
        n_chap = con.execute("SELECT COUNT(*) FROM chap_sums").fetchone()[0]
        logger.info(f"chapter_topic_probs done | chapters={n_chap:,}")

    # ---- TERTILE ----
    # Two-pass to avoid holding 115M × n_topics in a windowed temp table:
    # 1) keys-only tertile labels  2) join + aggregate
    if not args.skip_tertile:
        tert_out = str((out_dir / "tertile_topic_probs.parquet").resolve())
        labels_path = str((tmp_dir / "tertile_labels.parquet").resolve())
        logger.info(f"writing tertile labels → {labels_path}")
        con.execute(
            f"""
            COPY (
              SELECT book_id, chapter_id, sentence_index, tertile
              FROM (
                SELECT
                  book_id,
                  chapter_id,
                  sentence_index,
                  CASE
                    WHEN n_sent < {int(args.min_sentences)} THEN NULL
                    WHEN rn < (n_sent // 3) THEN 'begin'
                    WHEN rn < ((2 * n_sent) // 3) THEN 'middle'
                    ELSE 'end'
                  END AS tertile
                FROM (
                  SELECT
                    work_id::BIGINT AS book_id,
                    chapter_index::BIGINT AS chapter_id,
                    sentence_index::BIGINT AS sentence_index,
                    ROW_NUMBER() OVER (
                      PARTITION BY work_id
                      ORDER BY chapter_index, sentence_index
                    ) - 1 AS rn,
                    COUNT(*) OVER (PARTITION BY work_id) AS n_sent
                  FROM read_parquet([{file_list_sql}], union_by_name=true)
                )
              )
              WHERE tertile IS NOT NULL
            ) TO '{labels_path}' (FORMAT PARQUET)
            """
        )
        logger.info(f"aggregating TERTILE → {tert_out}")
        con.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE tert_sums AS
            SELECT
              s.book_id,
              l.tertile,
              COUNT(*)::BIGINT AS n_sent,
              {prob_sum_exprs}
            FROM sentences s
            INNER JOIN read_parquet('{labels_path}') l
              ON s.book_id = l.book_id
             AND s.chapter_id = l.chapter_id
             AND s.sentence_index = l.sentence_index
            GROUP BY s.book_id, l.tertile
            """
        )
        con.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE tert_mean_norm AS
            SELECT book_id, tertile, {mean_cols}, ({mass_expr}) AS mass
            FROM tert_sums
            """
        )
        tert_long = unpivot_sql(
            "tert_mean_norm", ["book_id", "tertile"], prob_cols, topic_ids
        )
        con.execute(f"COPY ({tert_long}) TO '{tert_out}' (FORMAT PARQUET)")
        stats = con.execute(
            "SELECT COUNT(DISTINCT book_id), COUNT(*) FROM tert_sums"
        ).fetchone()
        logger.info(f"tertile_topic_probs done | books={stats[0]:,} groups={stats[1]:,}")
        try:
            Path(labels_path).unlink(missing_ok=True)
        except OSError:
            pass

    s = con.execute(
        f"""
        SELECT MIN(s), MEDIAN(s), MAX(s)
        FROM (
          SELECT book_id, SUM(prob) AS s
          FROM read_parquet('{book_out}')
          GROUP BY book_id
        )
        """
    ).fetchone()
    logger.info(f"book prob sums: min={s[0]:.6f} median={s[1]:.6f} max={s[2]:.6f}")
    logger.info("done")


if __name__ == "__main__":
    main()
