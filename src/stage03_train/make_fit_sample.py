"""Select a stratified BERTopic fit/eval sample as row indices into the full corpus.

Stage 03 fits BERTopic on a bounded subsample of the full corpus (the full train
split is ~82M sentence rows). The legacy path drew that subsample uniformly at
random, which over-represents long books, prolific authors, and common years.

This module produces a *book-balanced, year-aware, author-capped* sample that
also spreads rows across narrative position (book opening -> ending). Crucially,
it emits **row indices into the full train->eval corpus** rather than new CSVs,
so Stage 03 can reuse the already-computed full-corpus embedding ``.npy`` caches
(one per embedding model) by gathering ``embeddings[fit_indices]`` instead of
re-encoding anything.

Index space and alignment
-------------------------
The full embedding cache and ``corpus.tsv`` are both built by
``iter_split_csv_chunks`` in **train-then-eval** order, applying ``clean_sentence``
and dropping empty rows. This sampler iterates the same CSVs with the same cleaning
and the same order, assigning each surviving row a 0-based global index. Therefore:

* ``fit_indices``  index into the **train partition** ``[0, n_train)``.
* ``eval_indices`` index into the **val partition** ``[n_train, n_train + n_val)``.

Both are valid positions in the per-model full ``train_eval_*.npy`` and in the
disk-backed ``CorpusDocStore``. Fitting uses the train partition only.
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.stage03_train.data_io import clean_sentence

logger = logging.getLogger(__name__)

UNKNOWN_AUTHOR = "unknown_author"
UNKNOWN_YEAR = "unknown_year"
DEFAULT_PROGRESS_EVERY = 5_000_000


def _flush_log_handlers() -> None:
    """Ensure progress lines appear immediately under ``tail -f``."""
    for handler in logger.handlers:
        handler.flush()
    root = logging.getLogger()
    for handler in root.handlers:
        handler.flush()


def _log_row_progress(
    phase: str,
    csv_name: str,
    rows_done: int,
    *,
    progress_every: int,
    extra: str = "",
) -> None:
    """Log every ``progress_every`` clean rows (and at phase start when rows_done is 0)."""
    if rows_done == 0:
        logger.info("%s %s: starting stream", phase, csv_name)
        _flush_log_handlers()
        return
    if progress_every > 0 and rows_done % progress_every == 0:
        suffix = f" {extra}" if extra else ""
        logger.info("%s %s: %d clean rows processed%s", phase, csv_name, rows_done, suffix)
        _flush_log_handlers()


def _checkpoint_pass1_path(checkpoint_dir: Path, seed: int, split: str) -> Path:
    return checkpoint_dir / f"checkpoint_seed{seed}_{split}_pass1.json"


def _save_pass1_checkpoint(
    path: Path,
    *,
    input_csv: str,
    n_clean: int,
    stats: dict[str, dict[str, int]],
    index_offset: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "input_csv": input_csv,
                "n_clean": n_clean,
                "index_offset": index_offset,
                "stats": stats,
            },
            f,
            indent=2,
        )
    logger.info("Wrote pass-1 checkpoint (resume skips stats scan): %s", path)
    _flush_log_handlers()


def _load_pass1_checkpoint(path: Path, *, input_csv: str, index_offset: int) -> tuple[dict, int] | None:
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if payload.get("input_csv") != str(input_csv) or int(payload.get("index_offset", -1)) != index_offset:
        logger.warning(
            "Ignoring stale pass-1 checkpoint %s (csv or offset mismatch)", path
        )
        return None
    stats = payload["stats"]
    n_clean = int(payload["n_clean"])
    logger.info(
        "Resuming from pass-1 checkpoint: %s (%d clean rows, %d books)",
        path.name,
        n_clean,
        len(stats),
    )
    _flush_log_handlers()
    return stats, n_clean


def _read_header_columns(csv_path: Path) -> list[str]:
    """Return the column names of a CSV without loading the body."""
    head = pd.read_csv(csv_path, nrows=0)
    return list(head.columns)


def load_metadata_map(metadata_csv: Path | None) -> dict[str, dict[str, Any]]:
    """Build ``work_id -> {author, year, genre_group}`` from a cohort CSV.

    Column names are normalized to the sampler's internal vocabulary. Missing
    files or columns degrade gracefully to ``unknown_*`` defaults so the sampler
    still works on fixtures that lack metadata.
    """
    if metadata_csv is None:
        return {}
    if not metadata_csv.exists():
        logger.warning("Metadata CSV not found, sampling without it: %s", metadata_csv)
        return {}

    df = pd.read_csv(metadata_csv)
    rename = {"author_name": "author", "publication_year": "year"}
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    if "work_id" not in df.columns:
        logger.warning("Metadata CSV missing work_id, ignoring: %s", metadata_csv)
        return {}

    meta: dict[str, dict[str, Any]] = {}
    has_author = "author" in df.columns
    has_year = "year" in df.columns
    has_genre = "genre_group" in df.columns
    for row in df.itertuples(index=False):
        wid = str(getattr(row, "work_id"))
        meta[wid] = {
            "author": str(getattr(row, "author")) if has_author else UNKNOWN_AUTHOR,
            "year": str(getattr(row, "year")) if has_year else UNKNOWN_YEAR,
            "genre_group": str(getattr(row, "genre_group")) if has_genre else "unknown_genre",
        }
    return meta


def _book_stats_pass(
    csv_path: Path,
    *,
    sentence_column: str,
    work_id_column: str,
    position_column: str | None,
    chunk_size: int,
    progress_every: int = DEFAULT_PROGRESS_EVERY,
) -> tuple[dict[str, dict[str, int]], int]:
    """First pass: per-book non-empty row count and max narrative position.

    Returns ``(stats, n_clean_rows)`` where ``n_clean_rows`` is the number of
    surviving rows (the partition size in the global index space).
    """
    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"count": 0, "max_pos": 0})
    usecols = [work_id_column, sentence_column]
    if position_column is not None:
        usecols.append(position_column)

    n_clean = 0
    _log_row_progress("pass1-stats", csv_path.name, 0, progress_every=progress_every)
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size, usecols=usecols):
        mask = chunk[sentence_column].map(clean_sentence).astype(bool)
        chunk = chunk[mask]
        if chunk.empty:
            continue
        n_clean += len(chunk)
        _log_row_progress(
            "pass1-stats",
            csv_path.name,
            n_clean,
            progress_every=progress_every,
            extra=f"({len(stats)} books so far)",
        )
        for wid, grp in chunk.groupby(work_id_column, sort=False):
            key = str(wid)
            stats[key]["count"] += len(grp)
            if position_column is not None:
                grp_max = int(pd.to_numeric(grp[position_column], errors="coerce").max())
                if grp_max > stats[key]["max_pos"]:
                    stats[key]["max_pos"] = grp_max
    logger.info(
        "pass1-stats %s: finished (%d clean rows, %d books)",
        csv_path.name,
        n_clean,
        len(stats),
    )
    _flush_log_handlers()
    return dict(stats), n_clean


def _position_bin(rel: float, n_bins: int) -> int:
    """Map a relative position in [0, 1] to a bin index in [0, n_bins - 1]."""
    idx = int(rel * n_bins)
    if idx >= n_bins:
        idx = n_bins - 1
    if idx < 0:
        idx = 0
    return idx


def select_stratified_indices(
    csv_path: Path,
    *,
    target_rows: int,
    seed: int,
    metadata_map: dict[str, dict[str, Any]],
    index_offset: int = 0,
    sentence_column: str = "sentence",
    work_id_column: str = "work_id",
    position_column: str | None = "sentence_index",
    chunk_size: int = 50_000,
    min_rows_per_book: int = 10,
    max_rows_per_book: int = 80,
    max_rows_per_author: int = 500,
    position_bins: int = 5,
    progress_every: int = DEFAULT_PROGRESS_EVERY,
    checkpoint_dir: Path | None = None,
    checkpoint_split: str = "train",
    resume: bool = False,
) -> tuple[np.ndarray, dict[str, Any], int]:
    """Select stratified global row indices for one split.

    Returns ``(sorted_indices, manifest, n_clean_rows)``. Indices are offset by
    ``index_offset`` so callers can place a split into the combined train->eval
    index space (train: offset 0; val: offset n_train).
    """
    rng = np.random.default_rng(seed)

    columns = _read_header_columns(csv_path)
    if sentence_column not in columns or work_id_column not in columns:
        raise ValueError(
            f"{csv_path} must contain '{work_id_column}' and '{sentence_column}'; got {columns}"
        )
    pos_col = position_column if position_column in columns else None

    pass1_ckpt = (
        _checkpoint_pass1_path(checkpoint_dir, seed, checkpoint_split)
        if checkpoint_dir is not None
        else None
    )
    loaded = None
    if resume and pass1_ckpt is not None:
        loaded = _load_pass1_checkpoint(
            pass1_ckpt, input_csv=str(csv_path), index_offset=index_offset
        )
    if loaded is not None:
        stats, n_clean = loaded
    else:
        stats, n_clean = _book_stats_pass(
            csv_path,
            sentence_column=sentence_column,
            work_id_column=work_id_column,
            position_column=pos_col,
            chunk_size=chunk_size,
            progress_every=progress_every,
        )
        if pass1_ckpt is not None:
            _save_pass1_checkpoint(
                pass1_ckpt,
                input_csv=str(csv_path),
                n_clean=n_clean,
                stats=stats,
                index_offset=index_offset,
            )
    n_books = len(stats)
    if n_books == 0:
        raise ValueError(f"No non-empty rows found in {csv_path}")

    base_per_book = int(np.floor(target_rows / n_books))
    per_book_quota = int(np.clip(base_per_book, min_rows_per_book, max_rows_per_book))
    per_bin_cap = max(1, int(np.ceil(per_book_quota / position_bins)))
    logger.info(
        "%s: %d clean rows, %d books, per-book quota=%d (per-bin cap=%d), offset=%d",
        csv_path.name,
        n_clean,
        n_books,
        per_book_quota,
        per_bin_cap,
        index_offset,
    )

    # Per-stratum reservoirs: (work_id, bin) -> list of records {idx, work_id, author, year, pos}.
    reservoirs: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    stratum_seen: dict[tuple[str, int], int] = defaultdict(int)
    # Global reservoir for top-up (uniform over all clean rows).
    global_reservoir: list[dict[str, Any]] = []
    global_seen = 0
    book_counter: dict[str, int] = defaultdict(int)

    local_idx = 0  # position within this split's clean stream
    read_cols = [work_id_column, sentence_column]
    if pos_col is not None:
        read_cols.append(pos_col)
    _log_row_progress("pass2-sample", csv_path.name, 0, progress_every=progress_every)
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size, usecols=read_cols, dtype=str):
        wid_vals = chunk[work_id_column].tolist()
        sent_vals = chunk[sentence_column].tolist()
        pos_vals = chunk[pos_col].tolist() if pos_col is not None else [None] * len(wid_vals)
        for wid_raw, sent_raw, pos_raw in zip(wid_vals, sent_vals, pos_vals, strict=False):
            if not clean_sentence(sent_raw):
                continue
            gidx = index_offset + local_idx
            local_idx += 1
            _log_row_progress(
                "pass2-sample",
                csv_path.name,
                local_idx,
                progress_every=progress_every,
            )

            wid = str(wid_raw)
            book = stats.get(wid, {"count": 1, "max_pos": 0})
            if pos_col is not None:
                raw_pos = pd.to_numeric(pos_raw, errors="coerce")
                pos = 0 if pd.isna(raw_pos) else int(raw_pos)
                denom = max(book["max_pos"], 1)
            else:
                pos = book_counter[wid]
                book_counter[wid] += 1
                denom = max(book["count"] - 1, 1)
            bin_idx = _position_bin(pos / denom, position_bins)

            meta = metadata_map.get(wid, {})
            rec = {
                "idx": gidx,
                "work_id": wid,
                "author": meta.get("author", UNKNOWN_AUTHOR),
                "year": meta.get("year", UNKNOWN_YEAR),
                "pos": pos,
            }

            key = (wid, bin_idx)
            stratum_seen[key] += 1
            res = reservoirs[key]
            if len(res) < per_bin_cap:
                res.append(rec)
            else:
                j = int(rng.integers(0, stratum_seen[key]))
                if j < per_bin_cap:
                    res[j] = rec

            global_seen += 1
            if len(global_reservoir) < target_rows:
                global_reservoir.append(rec)
            else:
                j = int(rng.integers(0, global_seen))
                if j < target_rows:
                    global_reservoir[j] = rec

    # Flatten reservoirs and trim per book to the quota.
    by_book: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for (wid, _bin), recs in reservoirs.items():
        by_book[wid].extend(recs)

    sampled: list[dict[str, Any]] = []
    for wid, recs in by_book.items():
        if len(recs) > per_book_quota:
            keep = rng.choice(len(recs), size=per_book_quota, replace=False)
            recs = [recs[i] for i in keep]
        sampled.extend(recs)

    # Enforce per-author cap.
    by_author: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in sampled:
        by_author[rec["author"]].append(rec)
    capped: list[dict[str, Any]] = []
    for _author, recs in by_author.items():
        if len(recs) > max_rows_per_author:
            keep = rng.choice(len(recs), size=max_rows_per_author, replace=False)
            recs = [recs[i] for i in keep]
        capped.extend(recs)
    sampled = capped

    # Top up from the global reservoir if author caps left us short.
    if len(sampled) < target_rows:
        selected = {rec["idx"] for rec in sampled}
        candidates = [rec for rec in global_reservoir if rec["idx"] not in selected]
        need = min(target_rows - len(sampled), len(candidates))
        if need > 0:
            pick = rng.choice(len(candidates), size=need, replace=False)
            sampled.extend(candidates[i] for i in pick)

    # Final downsample to the exact target.
    if len(sampled) > target_rows:
        keep = rng.choice(len(sampled), size=target_rows, replace=False)
        sampled = [sampled[i] for i in keep]

    indices = np.array(sorted(rec["idx"] for rec in sampled), dtype=np.int64)

    sampled_years = pd.Series([rec["year"] for rec in sampled])
    n_authors_input = len({m.get("author", UNKNOWN_AUTHOR) for m in metadata_map.values()}) or None
    manifest = {
        "input_csv": str(csv_path),
        "index_offset": int(index_offset),
        "n_clean_rows": int(n_clean),
        "target_rows": int(target_rows),
        "actual_rows": int(len(indices)),
        "seed": int(seed),
        "n_books_input": int(n_books),
        "n_books_sampled": int(len({rec["work_id"] for rec in sampled})),
        "n_authors_input": n_authors_input,
        "n_authors_sampled": int(len({rec["author"] for rec in sampled})),
        "year_counts": {str(k): int(v) for k, v in sampled_years.value_counts().sort_index().items()},
        "min_rows_per_book": min_rows_per_book,
        "max_rows_per_book": max_rows_per_book,
        "max_rows_per_author": max_rows_per_author,
        "per_book_quota": per_book_quota,
        "position_bins": position_bins,
        "position_column": pos_col,
        "has_metadata": bool(metadata_map),
    }
    logger.info(
        "pass2-sample %s: finished stream (%d clean rows scanned)",
        csv_path.name,
        local_idx,
    )
    logger.info("Selected %d / %d indices from %s", len(indices), target_rows, csv_path.name)
    _flush_log_handlers()
    return indices, manifest, n_clean


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(
        description="Select stratified Stage 03 fit/eval row indices into the full corpus."
    )
    parser.add_argument("--train-csv", required=True, type=Path)
    parser.add_argument("--val-csv", required=True, type=Path)
    parser.add_argument("--metadata-train", default=None, type=Path)
    parser.add_argument("--metadata-val", default=None, type=Path)
    parser.add_argument("--out-dir", default=Path("data/stage03_samples"), type=Path)
    parser.add_argument("--seed", default=42, type=int)
    parser.add_argument("--train-target", default=500_000, type=int)
    parser.add_argument("--val-target", default=100_000, type=int)
    parser.add_argument("--sentence-column", default="sentence")
    parser.add_argument("--work-id-column", default="work_id")
    parser.add_argument("--position-column", default="sentence_index")
    parser.add_argument("--chunk-size", default=50_000, type=int)
    parser.add_argument(
        "--progress-every",
        default=DEFAULT_PROGRESS_EVERY,
        type=int,
        help="Log progress every N clean rows (0 disables periodic logs).",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse pass-1 checkpoints in --out-dir when CSV/offset match (skips stats scan).",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    progress_every = max(0, int(args.progress_every))

    # Train partition: global indices start at 0; fit uses these only.
    fit_indices, train_manifest, n_train = select_stratified_indices(
        args.train_csv,
        target_rows=args.train_target,
        seed=args.seed,
        metadata_map=load_metadata_map(args.metadata_train),
        index_offset=0,
        sentence_column=args.sentence_column,
        work_id_column=args.work_id_column,
        position_column=args.position_column,
        chunk_size=args.chunk_size,
        progress_every=progress_every,
        checkpoint_dir=args.out_dir,
        checkpoint_split="train",
        resume=args.resume,
    )

    # Val partition: offset by n_train so indices land in the combined corpus space.
    eval_indices, val_manifest, n_val = select_stratified_indices(
        args.val_csv,
        target_rows=args.val_target,
        seed=args.seed + 1,
        metadata_map=load_metadata_map(args.metadata_val),
        index_offset=n_train,
        sentence_column=args.sentence_column,
        work_id_column=args.work_id_column,
        position_column=args.position_column,
        chunk_size=args.chunk_size,
        min_rows_per_book=5,
        max_rows_per_book=40,
        max_rows_per_author=300,
        progress_every=progress_every,
        checkpoint_dir=args.out_dir,
        checkpoint_split="val",
        resume=args.resume,
    )

    fit_path = args.out_dir / f"fit_indices_seed{args.seed}.npy"
    eval_path = args.out_dir / f"eval_indices_seed{args.seed}.npy"
    np.save(fit_path, fit_indices)
    np.save(eval_path, eval_indices)

    manifest = {
        "seed": int(args.seed),
        "progress_every": progress_every,
        "n_train_clean": int(n_train),
        "n_val_clean": int(n_val),
        "n_total_clean": int(n_train + n_val),
        "fit_indices_file": str(fit_path),
        "eval_indices_file": str(eval_path),
        "fit_partition": "train",
        "eval_partition": "val",
        "pass1_checkpoints": {
            "train": str(_checkpoint_pass1_path(args.out_dir, args.seed, "train")),
            "val": str(_checkpoint_pass1_path(args.out_dir, args.seed, "val")),
        },
        "train": train_manifest,
        "validation": val_manifest,
    }
    manifest_path = args.out_dir / f"sample_manifest_seed{args.seed}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Wrote fit indices ({len(fit_indices)}): {fit_path}")
    print(f"Wrote eval indices ({len(eval_indices)}): {eval_path}")
    print(f"Wrote manifest: {manifest_path}")


if __name__ == "__main__":
    main()
