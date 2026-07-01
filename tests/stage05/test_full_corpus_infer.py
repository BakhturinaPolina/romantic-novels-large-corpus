"""Unit tests for full-corpus inference helpers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from src.stage05_final_fit import full_corpus_infer


class FullCorpusInferHelperTests(unittest.TestCase):
    def test_prepare_chunk_frame_skips_empty_sentences(self) -> None:
        chunk = pd.DataFrame(
            {
                "work_id": [1, 2],
                "chapter_index": [0, 1],
                "sentence_index": [0, 0],
                "sentence": ["  Hello World  ", "   "],
            }
        )
        meta, docs, keep = full_corpus_infer._prepare_chunk_frame(chunk)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0], "hello world")
        self.assertEqual(len(meta), 1)
        self.assertEqual(int(meta.iloc[0]["work_id"]), 1)

    def test_infer_split_to_parquet_uses_embedding_offset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_path = tmp_path / "train.csv"
            pd.DataFrame(
                {
                    "work_id": [10],
                    "chapter_index": [0],
                    "sentence_index": [0],
                    "sentence": ["alpha beta gamma delta"],
                }
            ).to_csv(csv_path, index=False)
            out_parquet = tmp_path / "out.parquet"
            emb = np.random.randn(5, 4).astype(np.float32)

            mock_model = MagicMock()
            seen_embeddings: list[np.ndarray | None] = []

            def fake_transform(docs, embeddings=None):
                seen_embeddings.append(embeddings)
                return np.array([3], dtype=np.int64), np.array([[0.2, 0.8]], dtype=np.float32)

            mock_model.transform.side_effect = fake_transform

            stats = full_corpus_infer.infer_split_to_parquet(
                mock_model,
                csv_path,
                out_parquet,
                split="train",
                embeddings_mmap=emb,
                embedding_row_offset=2,
                batch_size=64,
                chunk_size=10,
            )

            self.assertIsNotNone(seen_embeddings[0])
            self.assertEqual(seen_embeddings[0].shape[0], 1)
            self.assertTrue(out_parquet.exists())
            self.assertEqual(stats["n_docs"], 1)
            self.assertEqual(stats["embedding_row_offset_start"], 2)
            self.assertEqual(stats["embedding_row_offset_end"], 3)
            df = pd.read_parquet(out_parquet)
            self.assertEqual(int(df.iloc[0]["topic"]), 3)
            self.assertAlmostEqual(float(df.iloc[0]["max_topic_prob"]), 0.8)


if __name__ == "__main__":
    unittest.main()
