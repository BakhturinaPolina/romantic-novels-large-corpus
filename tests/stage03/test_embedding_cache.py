"""Unit tests for embedding cache resolution."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.stage05_final_fit import embedding_cache


class EmbeddingCacheTests(unittest.TestCase):
    def test_resolve_test_override(self) -> None:
        cfg = {
            "embedding_models": ["sentence-transformers/all-MiniLM-L12-v2"],
            "embeddings_cache": {
                "overrides": {
                    "sentence-transformers/all-MiniLM-L12-v2": "data/interim/octis/v3/cache/train_eval.npy"
                },
                "test_overrides": {
                    "sentence-transformers/all-MiniLM-L12-v2": "data/interim/octis/v3/cache/test.npy"
                },
            },
        }
        path = embedding_cache.resolve_embeddings_cache_path(
            cfg, "sentence-transformers/all-MiniLM-L12-v2", split="test"
        )
        self.assertIsNotNone(path)
        assert path is not None
        self.assertTrue(str(path).endswith("test.npy"))

    def test_test_cache_complete_requires_no_progress_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp) / "test_model.npy"
            cache.write_bytes(b"")
            self.assertTrue(embedding_cache.test_cache_complete(cache))
            progress = cache.with_suffix(cache.suffix + ".progress.json")
            progress.write_text("{}", encoding="utf-8")
            self.assertFalse(embedding_cache.test_cache_complete(cache))

    def test_load_embeddings_mmap_missing_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.npy"
            self.assertIsNone(embedding_cache.load_embeddings_mmap(missing, split="test"))

    def test_load_embeddings_mmap_existing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp) / "emb.npy"
            np.save(cache, np.zeros((3, 4), dtype=np.float32))
            mmap = embedding_cache.load_embeddings_mmap(cache, split="test")
            self.assertIsNotNone(mmap)
            assert mmap is not None
            self.assertEqual(mmap.shape, (3, 4))


if __name__ == "__main__":
    unittest.main()
