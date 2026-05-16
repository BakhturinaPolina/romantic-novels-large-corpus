"""OCTIS corpus writer with split-aware partitions."""

from __future__ import annotations

import csv
from pathlib import Path


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

