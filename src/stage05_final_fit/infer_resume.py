"""Pure helpers for full-corpus infer checkpoint resume (no ML imports)."""


def should_skip_infer_chunk(stream_idx: int, chunk_len: int, rows_done: int) -> bool:
    """Return True if this CSV chunk is already written to chunk shards."""
    return stream_idx + chunk_len <= rows_done


def assert_infer_stream_aligned(
    *,
    rows_done: int,
    stream_idx: int,
    chunks_skipped: int,
) -> None:
    """Fail fast if resume would transform the wrong CSV rows."""
    if rows_done <= 0:
        return
    if stream_idx != rows_done:
        raise RuntimeError(
            f"Infer resume misaligned: stream index {stream_idx} != checkpoint {rows_done}"
        )
    if chunks_skipped == 0:
        raise RuntimeError(
            "Infer resume refused: CSV stream was not advanced from row 0 before "
            f"transform at checkpoint {rows_done}."
        )
