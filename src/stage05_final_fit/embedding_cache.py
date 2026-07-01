"""Resolve precomputed sentence-embedding caches for inference splits."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal

import numpy as np

from src.common.config import load_config, resolve_path
from src.stage03_train.embeddings import get_cache_file, safe_embedding_name

LOGGER = logging.getLogger(__name__)

SplitCacheKey = Literal["train_eval", "test"]


def resolve_embeddings_cache_path(
    train_cfg: dict[str, Any],
    embedding_model_name: str,
    *,
    split: SplitCacheKey = "train_eval",
) -> Path | None:
    """Return configured cache path for train_eval or test, or None if unset."""
    cache_cfg = train_cfg.get("embeddings_cache", {}) or {}
    if split == "test":
        overrides = cache_cfg.get("test_overrides", {}) or {}
    else:
        overrides = cache_cfg.get("overrides", {}) or {}
    override_path = overrides.get(embedding_model_name)
    if not override_path:
        return None
    return resolve_path(Path(override_path))


def default_test_cache_path(train_cfg: dict[str, Any], embedding_model_name: str) -> Path:
    """Default test cache location alongside train_eval override directory."""
    train_path = resolve_embeddings_cache_path(train_cfg, embedding_model_name, split="train_eval")
    if train_path is not None:
        cache_dir = train_path.parent
    else:
        cache_dir = resolve_path(Path("data/interim/octis/v3_english_only/embeddings_cache"))
    return get_cache_file(cache_dir, "test", embedding_model_name)


def load_embeddings_mmap(
    cache_path: Path,
    *,
    split: str,
    logger: logging.Logger | None = None,
) -> np.ndarray | None:
    """Memory-map embeddings if the cache file exists."""
    log = logger or LOGGER
    if not cache_path.exists():
        log.warning("[%s] embedding cache not found: %s (will encode on the fly)", split, cache_path)
        return None
    mmap = np.load(cache_path, mmap_mode="r")
    log.info("[%s] using precomputed embeddings mmap: %s shape=%s", split, cache_path, mmap.shape)
    return mmap


def load_test_embeddings_mmap(
    train_config: Path | str,
    embedding_model_name: str | None = None,
    *,
    logger: logging.Logger | None = None,
) -> np.ndarray | None:
    """Load test-split embedding cache from train YAML config."""
    cfg = load_config(Path(train_config))
    model_name = embedding_model_name or cfg.get("embedding_models", [""])[0]
    cache_path = resolve_embeddings_cache_path(cfg, model_name, split="test")
    if cache_path is None:
        cache_path = default_test_cache_path(cfg, model_name)
    return load_embeddings_mmap(cache_path, split="test", logger=logger)


def test_cache_complete(cache_path: Path) -> bool:
    """True when cache exists and no in-progress marker remains."""
    from src.stage03_train.embeddings import _progress_path

    return cache_path.is_file() and not _progress_path(cache_path).exists()
