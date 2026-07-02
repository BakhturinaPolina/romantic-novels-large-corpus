"""Chunked full-corpus BERTopic inference (train + val + test)."""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from bertopic import BERTopic
from tqdm import tqdm

from src.common.config import load_config, resolve_path
from src.stage03_train.corpus_store import corpus_metadata_path
from src.stage03_train.data_io import clean_sentence
from src.stage05_final_fit.chunked_transform import transform_docs_batched
from src.stage05_final_fit.compare_fit import compare_model_dir
from src.stage05_final_fit.embedding_cache import load_test_embeddings_mmap, resolve_embeddings_cache_path
from src.stage05_final_fit.infer_resume import assert_infer_stream_aligned, should_skip_infer_chunk

LOGGER = logging.getLogger("stage05_full_corpus_infer")

SENTENCE_COLUMNS = ("work_id", "chapter_index", "sentence_index", "sentence")


def _load_model(model_root: Path) -> BERTopic:
    candidates = [
        compare_model_dir(model_root),
        model_root,
    ]
    for base in candidates:
        if not base.is_dir():
            continue
        subdirs = sorted([p for p in base.rglob("model_*") if p.is_dir()])
        if subdirs:
            return BERTopic.load(subdirs[0])
    raise FileNotFoundError(f"No BERTopic model directory found under {model_root}")


def _resolve_embeddings_cache(train_cfg: dict[str, Any], embedding_model_name: str) -> Path:
    cache_path = resolve_embeddings_cache_path(
        train_cfg, embedding_model_name, split="train_eval"
    )
    if cache_path is None:
        raise ValueError(
            f"No embeddings cache override for {embedding_model_name} in train config."
        )
    if not cache_path.exists():
        raise FileNotFoundError(f"Embeddings cache not found: {cache_path}")
    return cache_path


def _iter_sentence_rows(
    csv_path: Path,
    *,
    chunk_size: int = 50_000,
    sentence_column: str = "sentence",
) -> Iterator[pd.DataFrame]:
    header = pd.read_csv(csv_path, nrows=0)
    usecols = [c for c in SENTENCE_COLUMNS if c in header.columns]
    if sentence_column not in usecols:
        usecols.append(sentence_column)
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size, usecols=usecols):
        yield chunk


def _prepare_chunk_frame(
    chunk: pd.DataFrame,
    *,
    sentence_column: str = "sentence",
) -> tuple[pd.DataFrame, list[str], np.ndarray | None]:
    """Return metadata frame, cleaned docs, and keep mask aligned to chunk rows."""
    docs: list[str] = []
    keep_rows: list[int] = []
    for row_idx, sentence in enumerate(chunk[sentence_column].tolist()):
        doc = clean_sentence(sentence)
        if not doc:
            continue
        docs.append(doc)
        keep_rows.append(row_idx)
    if not keep_rows:
        return chunk.iloc[0:0], [], None
    meta = chunk.iloc[keep_rows].reset_index(drop=True)
    return meta, docs, np.asarray(keep_rows, dtype=np.int64)


def _infer_progress_path(output_parquet: Path) -> Path:
    return output_parquet.with_suffix(output_parquet.suffix + ".progress.json")


def _infer_stats_path(output_parquet: Path) -> Path:
    return output_parquet.with_suffix(output_parquet.suffix + ".stats.json")


def _infer_partial_dir(output_parquet: Path) -> Path:
    return output_parquet.parent / f"{output_parquet.stem}.partial"


def _count_parquet_rows(parquet_path: Path) -> int:
    return int(pq.ParquetFile(parquet_path).metadata.num_rows)


def _load_split_stats(output_parquet: Path) -> dict[str, Any] | None:
    stats_path = _infer_stats_path(output_parquet)
    if not stats_path.exists():
        return None
    with open(stats_path, encoding="utf-8") as f:
        return json.load(f)


def _merge_chunk_parquets(chunk_dir: Path, output_parquet: Path) -> None:
    chunk_files = sorted(chunk_dir.glob("chunk_*.parquet"))
    if not chunk_files:
        raise RuntimeError(f"No chunk shards to merge in {chunk_dir}")
    writer: pq.ParquetWriter | None = None
    for chunk_file in chunk_files:
        table = pq.read_table(chunk_file)
        if writer is None:
            writer = pq.ParquetWriter(output_parquet, table.schema, compression="snappy")
        writer.write_table(table)
    if writer is not None:
        writer.close()


def _write_chunk_shard(partial_dir: Path, chunk_idx: int, frame: pd.DataFrame) -> Path:
    partial_dir.mkdir(parents=True, exist_ok=True)
    shard = partial_dir / f"chunk_{chunk_idx:06d}.parquet"
    frame.to_parquet(shard, index=False, compression="snappy")
    return shard


def infer_split_to_parquet(
    topic_model: BERTopic,
    csv_path: Path,
    output_parquet: Path,
    *,
    split: str,
    embeddings_mmap: np.ndarray | None = None,
    embedding_row_offset: int = 0,
    batch_size: int = 8192,
    chunk_size: int = 50_000,
    sentence_column: str = "sentence",
    resume: bool = True,
) -> dict[str, Any]:
    """Transform one split CSV to parquet with topic assignments (resumable)."""
    output_parquet.parent.mkdir(parents=True, exist_ok=True)
    stats_path = _infer_stats_path(output_parquet)
    progress_path = _infer_progress_path(output_parquet)
    partial_dir = _infer_partial_dir(output_parquet)

    if resume and output_parquet.exists() and not progress_path.exists():
        cached = _load_split_stats(output_parquet)
        if cached is not None:
            LOGGER.info("[%s] resume skip — output exists: %s (%d docs)", split, output_parquet, cached["n_docs"])
            return cached

    rows_done = 0
    chunks_done = 0
    if resume and progress_path.exists():
        with open(progress_path, encoding="utf-8") as f:
            payload = json.load(f)
        rows_done = int(payload.get("rows_done", 0))
        chunks_done = int(payload.get("chunks_done", 0))
        LOGGER.info(
            "[%s] resuming infer from row %d chunk %d (%s)",
            split,
            rows_done,
            chunks_done,
            progress_path,
        )
    elif (
        resume
        and output_parquet.exists()
        and not stats_path.exists()
        and not progress_path.exists()
    ):
        try:
            legacy_rows = _count_parquet_rows(output_parquet)
        except Exception as exc:
            LOGGER.warning(
                "[%s] corrupt partial parquet (%s); deleting and restarting split (%s)",
                split,
                output_parquet,
                exc,
            )
            output_parquet.unlink(missing_ok=True)
            legacy_rows = 0
        if legacy_rows > 0:
            import shutil

            partial_dir.mkdir(parents=True, exist_ok=True)
            legacy_shard = partial_dir / "chunk_000000_legacy.parquet"
            shutil.move(output_parquet, legacy_shard)
            rows_done = legacy_rows
            chunks_done = 1
            with open(progress_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "rows_done": rows_done,
                        "chunks_done": chunks_done,
                        "n_docs": rows_done,
                        "n_outliers": 0,
                        "legacy_parquet_import": True,
                    },
                    f,
                )
            LOGGER.info(
                "[%s] imported legacy partial parquet (%d rows) for resume -> %s",
                split,
                legacy_rows,
                legacy_shard,
            )
    elif output_parquet.exists():
        output_parquet.unlink()
    if partial_dir.exists() and not resume:
        import shutil

        shutil.rmtree(partial_dir)

    n_docs = rows_done
    n_outliers = 0
    if rows_done > 0 and stats_path.exists():
        with open(stats_path, encoding="utf-8") as f:
            partial_stats = json.load(f)
        n_outliers = int(partial_stats.get("n_outliers", 0))

    row_offset = embedding_row_offset + rows_done
    stream_idx = 0
    chunks_skipped = 0
    resume_guard_checked = rows_done == 0
    split_start = time.perf_counter()

    chunk_iter = _iter_sentence_rows(csv_path, chunk_size=chunk_size, sentence_column=sentence_column)
    pbar = tqdm(chunk_iter, desc=f"{split} csv chunks", unit="chunk", ncols=100)
    for chunk_idx, chunk in enumerate(pbar):
        meta, docs, _keep = _prepare_chunk_frame(chunk, sentence_column=sentence_column)
        chunk_len = len(docs)
        if chunk_len == 0:
            continue
        if resume and should_skip_infer_chunk(stream_idx, chunk_len, rows_done):
            stream_idx += chunk_len
            chunks_skipped += 1
            continue

        if not resume_guard_checked:
            assert_infer_stream_aligned(
                rows_done=rows_done,
                stream_idx=stream_idx,
                chunks_skipped=chunks_skipped,
            )
            resume_guard_checked = True

        emb = None
        if embeddings_mmap is not None:
            end = row_offset + chunk_len
            emb = np.asarray(embeddings_mmap[row_offset:end], dtype=np.float32)
            row_offset = end

        topics, probs = transform_docs_batched(
            topic_model,
            docs,
            embeddings=emb,
            batch_size=batch_size,
            desc=f"{split} transform",
        )
        n_docs += len(topics)
        n_outliers += int(np.sum(topics == -1))
        stream_idx += chunk_len

        out = meta.copy()
        out["split"] = split
        out["topic"] = topics.astype(np.int32)
        if probs is not None and probs.size:
            out["max_topic_prob"] = np.max(probs, axis=1).astype(np.float32)
            prob_cols = {
                f"prob_{i}": probs[:, i].astype(np.float32) for i in range(probs.shape[1])
            }
            out = pd.concat([out, pd.DataFrame(prob_cols)], axis=1)
        else:
            out["max_topic_prob"] = np.nan

        _write_chunk_shard(partial_dir, chunk_idx, out)
        chunks_done = chunk_idx + 1
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "rows_done": stream_idx,
                    "chunks_done": chunks_done,
                    "n_docs": n_docs,
                    "n_outliers": n_outliers,
                },
                f,
            )
        partial_stats = {
            "split": split,
            "n_docs": n_docs,
            "n_outliers": n_outliers,
            "outlier_rate": float(n_outliers / n_docs) if n_docs else 0.0,
            "output_parquet": str(output_parquet),
            "embedding_row_offset_start": embedding_row_offset,
            "embedding_row_offset_end": row_offset,
        }
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(partial_stats, f, indent=2)
        pbar.set_postfix({"docs": f"{n_docs:,}", "outlier": f"{100.0 * n_outliers / n_docs:.1f}%"})

    if n_docs == 0:
        raise RuntimeError(f"No documents scored for split {split!r} from {csv_path}")

    if partial_dir.exists():
        _merge_chunk_parquets(partial_dir, output_parquet)
        import shutil

        shutil.rmtree(partial_dir)
    if progress_path.exists():
        progress_path.unlink()

    elapsed = time.perf_counter() - split_start
    stats = {
        "split": split,
        "n_docs": n_docs,
        "outlier_rate": float(n_outliers / n_docs) if n_docs else 0.0,
        "elapsed_s": elapsed,
        "output_parquet": str(output_parquet),
        "embedding_row_offset_start": embedding_row_offset,
        "embedding_row_offset_end": row_offset,
        "resumed_from_rows": rows_done,
    }
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    LOGGER.info(
        "[%s] wrote %s (%d docs, outlier=%.4f) in %.1fs",
        split,
        output_parquet,
        n_docs,
        stats["outlier_rate"],
        elapsed,
    )
    return stats


def run_full_corpus_infer(
    *,
    model_dir: Path,
    run_id: str,
    paths_config: Path = Path("configs/stage03/paths_stage03_fit_v3.yaml"),
    train_config: Path = Path("configs/stage03/train_v4_l12_final_call73.yaml"),
    splits: tuple[str, ...] = ("train", "val", "test"),
    batch_size: int = 16_384,
    chunk_size: int = 50_000,
    output_dir: Path | None = None,
    resume: bool = True,
) -> Path:
    """Transform train/val/test sentence CSVs and write per-split parquet files."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )
    paths_cfg = load_config(paths_config)
    train_cfg = load_config(train_config)
    inputs = paths_cfg.get("inputs", {})

    model_dir = resolve_path(model_dir)
    out_root = resolve_path(output_dir) if output_dir else (
        resolve_path(Path(paths_cfg["outputs"]["experiments"])) / run_id / "full_corpus_infer"
    )
    out_root.mkdir(parents=True, exist_ok=True)

    topic_model = _load_model(model_dir)
    embedding_model_name = train_cfg.get("embedding_models", ["sentence-transformers/all-MiniLM-L12-v2"])[0]

    embeddings_mmap = None
    test_embeddings_mmap = None
    n_train_docs = 0
    if any(s in splits for s in ("train", "val")):
        cache_file = _resolve_embeddings_cache(train_cfg, embedding_model_name)
        embeddings_mmap = np.load(cache_file, mmap_mode="r")
        corpus_dir = resolve_path(Path(inputs["octis_corpus_dir"]))
        meta_path = corpus_metadata_path(corpus_dir)
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                corpus_meta = json.load(f)
            n_train_docs = int(corpus_meta["last-training-doc"])
        LOGGER.info(
            "Embeddings mmap: %s shape=%s; train row offset=0 val offset=%d",
            cache_file,
            embeddings_mmap.shape,
            n_train_docs,
        )
    if "test" in splits:
        test_embeddings_mmap = load_test_embeddings_mmap(train_config, embedding_model_name, logger=LOGGER)

    split_csv = {
        "train": resolve_path(Path(inputs["sentences_train_csv"])),
        "val": resolve_path(Path(inputs["sentences_val_csv"])),
        "test": resolve_path(Path(inputs["sentences_test_csv"])),
    }
    split_offsets = {"train": 0, "val": n_train_docs, "test": 0}

    summary_rows: list[dict[str, Any]] = []
    pipeline_start = time.perf_counter()
    for split in splits:
        if split not in split_csv:
            raise ValueError(f"Unknown split {split!r}; expected train|val|test")
        if split == "test":
            mmap = test_embeddings_mmap
        else:
            mmap = embeddings_mmap
        stats = infer_split_to_parquet(
            topic_model,
            split_csv[split],
            out_root / f"sentence_topics_{split}.parquet",
            split=split,
            embeddings_mmap=mmap,
            embedding_row_offset=split_offsets[split],
            batch_size=batch_size,
            chunk_size=chunk_size,
            resume=resume,
        )
        summary_rows.append(stats)

    summary = {
        "run_id": run_id,
        "model_dir": str(model_dir),
        "splits": list(splits),
        "batch_size": batch_size,
        "chunk_size": chunk_size,
        "split_stats": summary_rows,
        "total_docs": sum(int(r["n_docs"]) for r in summary_rows),
        "elapsed_s": time.perf_counter() - pipeline_start,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    summary_path = out_root / "infer_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    LOGGER.info(
        "Full-corpus infer complete: %d docs across %d splits in %.1fs -> %s",
        summary["total_docs"],
        len(splits),
        summary["elapsed_s"],
        out_root,
    )
    return out_root
