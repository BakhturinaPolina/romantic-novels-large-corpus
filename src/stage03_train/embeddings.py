"""Embedding caching utilities for Stage 03."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from src.stage03_train.bertopic_octis_model import load_embedding_model


def safe_embedding_name(model_name: str) -> str:
    return model_name.replace("/", "__").replace("\\", "__")


def get_cache_file(cache_dir: Path, split: str, model_name: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{split}_{safe_embedding_name(model_name)}.npy"


def _resolve_device(device: str) -> str:
    if device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device


def load_or_compute_embeddings(
    docs: list[str],
    model_name: str,
    cache_dir: Path,
    split: str,
    device: str = "auto",
    batch_size: int = 256,
) -> np.ndarray:
    """Load embedding cache or compute and persist it."""
    cache_file = get_cache_file(cache_dir, split, model_name)
    if cache_file.exists():
        return np.load(cache_file, mmap_mode=None)

    resolved_device = _resolve_device(device)
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
    return embeddings

