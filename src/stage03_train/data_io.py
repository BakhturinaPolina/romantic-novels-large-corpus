"""Split-aware data loading for Stage 03 train/eval."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pandas as pd


def clean_sentence(text: Any) -> str:
    """Normalize sentence text for BERTopic input."""
    if text is None:
        return ""
    s = str(text).replace("\n", " ")
    s = " ".join(s.split())
    return s.strip().lower()


def count_split_rows(csv_path: Path, sentence_column: str = "sentence") -> int:
    """Count non-empty rows in a split CSV without loading it into memory."""
    total = 0
    for chunk in iter_split_csv_chunks(csv_path, sentence_column=sentence_column):
        total += len(chunk[0])
    return total


def iter_split_csv_chunks(
    csv_path: Path,
    sentence_column: str = "sentence",
    work_id_column: str = "work_id",
    chunk_size: int = 50_000,
) -> Iterator[tuple[list[str], list[str]]]:
    """Yield (docs, labels) batches from a sentence split CSV."""
    usecols = [work_id_column, sentence_column]
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size, usecols=usecols):
        if sentence_column not in chunk.columns:
            raise ValueError(
                f"Expected column '{sentence_column}' in {csv_path}, got {list(chunk.columns)}"
            )
        docs: list[str] = []
        labels: list[str] = []
        for work_id, sentence in zip(
            chunk[work_id_column].tolist(), chunk[sentence_column].tolist(), strict=False
        ):
            doc = clean_sentence(sentence)
            if not doc:
                continue
            docs.append(doc)
            labels.append(f"work_{work_id}")
        if docs:
            yield docs, labels


def load_eval_tokens_chunked(
    eval_csv: Path,
    sentence_column: str = "sentence",
    chunk_size: int = 50_000,
    max_docs: int | None = None,
    logger: logging.Logger | None = None,
) -> list[list[str]]:
    """Load eval tokens in chunks; optional cap limits coherence metric memory."""
    tokens_eval: list[list[str]] = []
    for docs, _labels in iter_split_csv_chunks(
        eval_csv, sentence_column=sentence_column, chunk_size=chunk_size
    ):
        for doc in docs:
            tokens_eval.append(doc.split())
            if max_docs is not None and len(tokens_eval) >= max_docs:
                if logger:
                    logger.info(
                        "Eval token cap reached (%d docs); coherence metric uses subset.",
                        max_docs,
                    )
                return tokens_eval
    return tokens_eval


def read_split_csv(csv_path: Path, sentence_column: str = "sentence") -> pd.DataFrame:
    """Read a Stage 01 sentence split and apply cleaning (loads full file)."""
    df = pd.read_csv(csv_path)
    if sentence_column not in df.columns:
        raise ValueError(
            f"Expected column '{sentence_column}' in {csv_path}, got {list(df.columns)}"
        )
    df = df.copy()
    df[sentence_column] = df[sentence_column].map(clean_sentence)
    df = df[df[sentence_column].astype(bool)].reset_index(drop=True)
    return df


def dataframe_to_docs(
    df: pd.DataFrame, sentence_column: str = "sentence"
) -> tuple[list[str], list[list[str]], list[str]]:
    """Convert split dataframe to docs/tokens/labels."""
    docs = df[sentence_column].tolist()
    tokens = [d.split() for d in docs]
    labels = [f"work_{wid}" for wid in df.get("work_id", pd.Series(["unknown"] * len(df))).tolist()]
    return docs, tokens, labels


def load_train_eval(
    train_csv: Path,
    eval_csv: Path,
    sentence_column: str = "sentence",
    chunk_size: int = 50_000,
    coherence_eval_max_docs: int | None = None,
    logger: logging.Logger | None = None,
) -> dict[str, Any]:
    """Load train/eval metadata and eval tokens without materializing full train split."""
    n_train = count_split_rows(train_csv, sentence_column=sentence_column)
    n_eval = count_split_rows(eval_csv, sentence_column=sentence_column)
    if logger:
        logger.info("Counted rows (chunked): train=%d eval=%d", n_train, n_eval)

    tokens_eval = load_eval_tokens_chunked(
        eval_csv,
        sentence_column=sentence_column,
        chunk_size=chunk_size,
        max_docs=coherence_eval_max_docs,
        logger=logger,
    )

    return {
        "n_train_docs": n_train,
        "n_eval_docs": n_eval,
        "tokens_eval": tokens_eval,
        "train_csv": train_csv,
        "eval_csv": eval_csv,
    }


def load_train_eval_in_memory(
    train_csv: Path,
    eval_csv: Path,
    sentence_column: str = "sentence",
) -> dict[str, Any]:
    """Legacy in-memory loader for small tests and smoke runs."""
    train_df = read_split_csv(train_csv, sentence_column=sentence_column)
    eval_df = read_split_csv(eval_csv, sentence_column=sentence_column)

    docs_train, tokens_train, labels_train = dataframe_to_docs(train_df, sentence_column)
    docs_eval, tokens_eval, labels_eval = dataframe_to_docs(eval_df, sentence_column)

    return {
        "train_df": train_df,
        "eval_df": eval_df,
        "docs_train": docs_train,
        "tokens_train": tokens_train,
        "labels_train": labels_train,
        "docs_eval": docs_eval,
        "tokens_eval": tokens_eval,
        "labels_eval": labels_eval,
    }
