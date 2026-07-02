"""Unit tests for full-corpus infer resume helpers."""

from __future__ import annotations

import unittest

from src.stage05_final_fit.infer_resume import (
    assert_infer_stream_aligned,
    should_skip_infer_chunk,
)


class InferResumeTests(unittest.TestCase):
    def test_should_skip_infer_chunk(self) -> None:
        self.assertTrue(should_skip_infer_chunk(0, 50_000, 100_000))
        self.assertTrue(should_skip_infer_chunk(50_000, 50_000, 100_000))
        self.assertFalse(should_skip_infer_chunk(75_000, 50_000, 100_000))
        self.assertFalse(should_skip_infer_chunk(0, 50_000, 0))

    def test_assert_infer_stream_aligned_ok(self) -> None:
        assert_infer_stream_aligned(rows_done=0, stream_idx=0, chunks_skipped=0)
        assert_infer_stream_aligned(rows_done=100_000, stream_idx=100_000, chunks_skipped=2)

    def test_assert_infer_stream_aligned_rejects_misaligned(self) -> None:
        with self.assertRaises(RuntimeError):
            assert_infer_stream_aligned(rows_done=100_000, stream_idx=0, chunks_skipped=0)


if __name__ == "__main__":
    unittest.main()
