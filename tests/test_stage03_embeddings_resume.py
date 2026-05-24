"""Regression tests for Stage03 embedding-cache resume indexing."""

from __future__ import annotations

import unittest

from src.stage03_train.embeddings_resume import (
    assert_resume_stream_aligned,
    should_skip_embedding_chunk,
)


def _simulate_stream(
    *,
    chunk_size: int,
    rows_done: int,
    start_write_idx: int = 0,
    max_chunks: int = 2_000_000,
) -> tuple[int, int, int | None]:
    """Return (write_idx, chunks_skipped, encode_at) for a uniform chunk stream."""
    write_idx = start_write_idx
    chunks_skipped = 0
    encode_at: int | None = None
    for _ in range(max_chunks):
        if should_skip_embedding_chunk(write_idx, chunk_size, rows_done):
            write_idx += chunk_size
            chunks_skipped += 1
            continue
        encode_at = write_idx
        break
    return write_idx, chunks_skipped, encode_at


class EmbeddingResumeTests(unittest.TestCase):
    def test_fresh_run_encodes_from_zero(self) -> None:
        write_idx, chunks_skipped, encode_at = _simulate_stream(chunk_size=50_000, rows_done=0)
        self.assertEqual(chunks_skipped, 0)
        self.assertEqual(encode_at, 0)
        self.assertEqual(write_idx, 0)

    def test_resume_fast_forwards_from_zero(self) -> None:
        rows_done = 69_700_000
        chunk_size = 50_000
        write_idx, chunks_skipped, encode_at = _simulate_stream(
            chunk_size=chunk_size, rows_done=rows_done, start_write_idx=0
        )
        self.assertEqual(chunks_skipped, rows_done // chunk_size)
        self.assertEqual(encode_at, rows_done)
        self.assertEqual(write_idx, rows_done)
        assert_resume_stream_aligned(
            rows_done=rows_done, write_idx=write_idx, chunks_skipped=chunks_skipped
        )

    def test_resume_rejects_buggy_start_at_checkpoint(self) -> None:
        rows_done = 69_700_000
        write_idx, chunks_skipped, encode_at = _simulate_stream(
            chunk_size=50_000, rows_done=rows_done, start_write_idx=rows_done
        )
        self.assertEqual(chunks_skipped, 0)
        self.assertEqual(encode_at, rows_done)
        with self.assertRaisesRegex(RuntimeError, "CSV stream was not advanced"):
            assert_resume_stream_aligned(
                rows_done=rows_done, write_idx=write_idx, chunks_skipped=chunks_skipped
            )

    def test_resume_at_chunk_aligned_checkpoint(self) -> None:
        rows_done = 3_200_000
        chunk_size = 50_000
        write_idx, chunks_skipped, encode_at = _simulate_stream(
            chunk_size=chunk_size, rows_done=rows_done
        )
        self.assertEqual(chunks_skipped, rows_done // chunk_size)
        self.assertEqual(encode_at, rows_done)
        assert_resume_stream_aligned(
            rows_done=rows_done, write_idx=write_idx, chunks_skipped=chunks_skipped
        )


if __name__ == "__main__":
    unittest.main()
