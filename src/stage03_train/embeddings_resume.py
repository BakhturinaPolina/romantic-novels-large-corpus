"""Pure helpers for Stage03 embedding-cache resume (no ML imports)."""


def should_skip_embedding_chunk(write_idx: int, chunk_len: int, rows_done: int) -> bool:
    """Return True if this CSV chunk is already persisted in the mmap cache."""
    return write_idx + chunk_len <= rows_done


def assert_resume_stream_aligned(
    *,
    rows_done: int,
    write_idx: int,
    chunks_skipped: int,
) -> None:
    """Fail fast if resume would encode the wrong CSV rows into mmap[write_idx]."""
    if rows_done <= 0:
        return
    if write_idx != rows_done:
        raise RuntimeError(
            f"Embedding resume misaligned: stream index {write_idx} != checkpoint {rows_done}"
        )
    if chunks_skipped == 0:
        raise RuntimeError(
            "Embedding resume refused: CSV stream was not advanced from row 0 before "
            f"encoding at checkpoint {rows_done}. "
            "This usually means write_idx was initialized to rows_done instead of 0."
        )
