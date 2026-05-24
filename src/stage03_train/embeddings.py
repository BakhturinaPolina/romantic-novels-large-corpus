"""Embedding caching utilities for Stage 03."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import torch

from src.stage03_train.bertopic_octis_model import load_embedding_model
from src.stage03_train.data_io import iter_split_csv_chunks
from src.stage03_train.embeddings_resume import (
    assert_resume_stream_aligned,
    should_skip_embedding_chunk,
)


def safe_embedding_name(model_name: str) -> str:
    return model_name.replace("/", "__").replace("\\", "__")


def get_cache_file(cache_dir: Path, split: str, model_name: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{split}_{safe_embedding_name(model_name)}.npy"


def _resolve_device(device: str) -> str:
    if device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device


def _progress_path(cache_file: Path) -> Path:
    return cache_file.with_suffix(cache_file.suffix + ".progress.json")


def load_or_compute_embeddings(
    docs: list[str],
    model_name: str,
    cache_dir: Path,
    split: str,
    device: str = "auto",
    batch_size: int = 256,
    logger: logging.Logger | None = None,
) -> np.ndarray:
    """Load embedding cache or compute and persist it (in-memory doc list)."""
    cache_file = get_cache_file(cache_dir, split, model_name)
    if cache_file.exists():
        if logger:
            logger.info("Loading cached embeddings: %s", cache_file)
        return np.load(cache_file, mmap_mode="r")

    resolved_device = _resolve_device(device)
    if logger:
        logger.info(
            "Computing embeddings model=%s split=%s device=%s batch_size=%d",
            model_name,
            split,
            resolved_device,
            batch_size,
        )
    model = load_embedding_model(model_name, device=resolved_device)
    embeddings = model.encode(
        docs,
        batch_size=batch_size,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=False,
        device=resolved_device,
    )
    np.save(cache_file, embeddings)
    if logger:
        logger.info("Saved embeddings cache: %s", cache_file)
    return embeddings


def compute_embeddings_from_csvs(
    train_csv: Path,
    eval_csv: Path,
    model_name: str,
    cache_file: Path,
    *,
    sentence_column: str = "sentence",
    chunk_size: int = 50_000,
    device: str = "auto",
    batch_size: int = 256,
    logger: logging.Logger | None = None,
    hub_cfg: dict | None = None,
    run_id: str | None = None,
) -> np.ndarray:
    """Encode train+eval CSV rows in chunks and persist as a memory-mappable array."""
    if hub_cfg and run_id:
        from src.stage03_train.embeddings_hub import hub_config_enabled, sync_embeddings_with_hub

        if hub_config_enabled(hub_cfg) and not cache_file.exists():
            sync_embeddings_with_hub(
                hub_cfg=hub_cfg,
                run_id=run_id,
                model_name=model_name,
                cache_file=cache_file,
                computed=False,
                logger=logger,
            )

    if cache_file.exists() and not _progress_path(cache_file).exists():
        if logger:
            logger.info("Loading cached embeddings (mmap): %s", cache_file)
        return np.load(cache_file, mmap_mode="r")

    resolved_device = _resolve_device(device)
    progress_path = _progress_path(cache_file)
    rows_done = 0
    if progress_path.exists():
        with open(progress_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        rows_done = int(payload.get("rows_done", 0))
        if logger:
            logger.info("Resuming embedding cache from row %d (%s)", rows_done, progress_path)

    model = load_embedding_model(model_name, device=resolved_device)

    probe_docs: list[str] = []
    for docs, _labels in iter_split_csv_chunks(
        train_csv, sentence_column=sentence_column, chunk_size=min(chunk_size, 1024)
    ):
        probe_docs = docs[: min(32, len(docs))]
        if probe_docs:
            break
    if not probe_docs:
        raise ValueError(f"No documents found in {train_csv}")
    probe_emb = model.encode(
        probe_docs,
        batch_size=min(batch_size, len(probe_docs)),
        convert_to_numpy=True,
        show_progress_bar=False,
        device=resolved_device,
    )
    dim = int(probe_emb.shape[1])

    from src.stage03_train.data_io import count_split_rows

    n_total = count_split_rows(train_csv, sentence_column) + count_split_rows(
        eval_csv, sentence_column
    )
    if logger:
        logger.info(
            "Embedding %d documents (dim=%d) in chunks of %d -> %s",
            n_total,
            dim,
            chunk_size,
            cache_file,
        )

    if rows_done > 0 and cache_file.exists():
        mmap = np.lib.format.open_memmap(cache_file, mode="r+", dtype=np.float32)
        if mmap.shape != (n_total, dim):
            raise RuntimeError(
                f"Partial cache shape {mmap.shape} != expected {(n_total, dim)}; delete cache and retry."
            )
    else:
        mmap = np.lib.format.open_memmap(
            cache_file, mode="w+", dtype=np.float32, shape=(n_total, dim)
        )
    # Linear index in train+eval CSV order; must start at 0 so resume can fast-forward
    # already-written rows via rows_done without re-encoding or misaligned mmap writes.
    write_idx = 0
    chunks_skipped = 0
    resume_guard_checked = rows_done == 0

    def _encode_split(csv_path: Path) -> None:
        nonlocal write_idx, chunks_skipped, resume_guard_checked
        for docs, _labels in iter_split_csv_chunks(
            csv_path, sentence_column=sentence_column, chunk_size=chunk_size
        ):
            chunk_len = len(docs)
            if should_skip_embedding_chunk(write_idx, chunk_len, rows_done):
                write_idx += chunk_len
                chunks_skipped += 1
                continue
            if write_idx >= n_total:
                break

            if not resume_guard_checked:
                assert_resume_stream_aligned(
                    rows_done=rows_done,
                    write_idx=write_idx,
                    chunks_skipped=chunks_skipped,
                )
                resume_guard_checked = True

            emb = model.encode(
                docs,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=True,
                normalize_embeddings=False,
                device=resolved_device,
            )
            end_idx = write_idx + len(docs)
            mmap[write_idx:end_idx] = emb.astype(np.float32, copy=False)
            write_idx = end_idx
            mmap.flush()
            with open(progress_path, "w", encoding="utf-8") as f:
                json.dump({"rows_done": write_idx, "n_total": n_total}, f)
            if logger:
                logger.info("Embeddings progress: %d / %d", write_idx, n_total)

    _encode_split(train_csv)
    _encode_split(eval_csv)

    if write_idx != n_total:
        raise RuntimeError(
            f"Embedding row count mismatch: wrote {write_idx}, expected {n_total}"
        )

    del mmap
    if progress_path.exists():
        progress_path.unlink()
    if logger:
        logger.info("Saved embeddings cache: %s", cache_file)

    if hub_cfg and run_id:
        from src.stage03_train.embeddings_hub import hub_config_enabled, sync_embeddings_with_hub

        if hub_config_enabled(hub_cfg):
            sync_embeddings_with_hub(
                hub_cfg=hub_cfg,
                run_id=run_id,
                model_name=model_name,
                cache_file=cache_file,
                computed=True,
                n_docs=n_total,
                dim=dim,
                logger=logger,
            )

    return np.load(cache_file, mmap_mode="r")
