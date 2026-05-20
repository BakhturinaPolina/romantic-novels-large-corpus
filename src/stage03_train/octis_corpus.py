"""OCTIS corpus writer with split-aware partitions."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

import numpy as np

from src.stage03_train.data_io import iter_split_csv_chunks


def write_octis_corpus(
    docs_train: list[str],
    labels_train: list[str],
    docs_eval: list[str],
    labels_eval: list[str],
    output_dir: Path,
) -> Path:
    """Write OCTIS corpus.tsv with explicit train/val partitions."""
    output_dir.mkdir(parents=True, exist_ok=True)
    corpus_path = output_dir / "corpus.tsv"

    with open(corpus_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        for doc, label in zip(docs_train, labels_train):
            writer.writerow([doc, "train", label])
        for doc, label in zip(docs_eval, labels_eval):
            writer.writerow([doc, "val", label])

    return corpus_path


def write_octis_corpus_from_csvs(
    train_csv: Path,
    eval_csv: Path,
    output_dir: Path,
    *,
    sentence_column: str = "sentence",
    chunk_size: int = 50_000,
    logger: logging.Logger | None = None,
) -> tuple[Path, Path, int, int]:
    """
    Stream train/eval CSVs into corpus.tsv and build byte-offset index.

    Returns:
        (corpus_path, offsets_path, n_train, n_eval)
    """
    from src.stage03_train.corpus_store import corpus_offsets_path, write_corpus_metadata

    output_dir.mkdir(parents=True, exist_ok=True)
    corpus_path = output_dir / "corpus.tsv"
    offsets_path = corpus_offsets_path(output_dir)

    offsets: list[int] = [0]
    n_train = 0
    n_eval = 0

    with open(corpus_path, "wb") as f:
        def _write_rows(docs: list[str], labels: list[str], partition: str) -> int:
            nonlocal offsets
            count = 0
            for doc, label in zip(docs, labels):
                line = f"{doc}\t{partition}\t{label}\n".encode("utf-8")
                f.write(line)
                offsets.append(offsets[-1] + len(line))
                count += 1
            return count

        for docs, labels in iter_split_csv_chunks(
            train_csv, sentence_column=sentence_column, chunk_size=chunk_size
        ):
            n_train += _write_rows(docs, labels, "train")
            if logger:
                logger.info("corpus.tsv train rows written: %d", n_train)

        for docs, labels in iter_split_csv_chunks(
            eval_csv, sentence_column=sentence_column, chunk_size=chunk_size
        ):
            n_eval += _write_rows(docs, labels, "val")
            if logger:
                logger.info("corpus.tsv val rows written: %d", n_eval)

    np.save(offsets_path, np.asarray(offsets, dtype=np.uint64))
    write_corpus_metadata(output_dir, n_train=n_train, n_val=n_eval)
    if logger:
        logger.info(
            "Wrote corpus.tsv (%d train + %d val rows), offsets: %s",
            n_train,
            n_eval,
            offsets_path,
        )
    return corpus_path, offsets_path, n_train, n_eval
