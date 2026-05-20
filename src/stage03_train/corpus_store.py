"""Disk-backed document access for large OCTIS corpora."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


class CorpusDocStore:
    """Random-access document texts via byte offsets into corpus.tsv."""

    def __init__(self, corpus_path: Path, offsets_path: Path) -> None:
        self.corpus_path = Path(corpus_path)
        self.offsets_path = Path(offsets_path)
        if not self.corpus_path.exists():
            raise FileNotFoundError(f"Missing corpus file: {self.corpus_path}")
        if not self.offsets_path.exists():
            raise FileNotFoundError(f"Missing corpus offsets: {self.offsets_path}")
        self._offsets = np.load(self.offsets_path, mmap_mode="r")
        self._n_docs = int(len(self._offsets) - 1)

    def __len__(self) -> int:
        return self._n_docs

    def __getitem__(self, index: int) -> str:
        if index < 0:
            index += self._n_docs
        if index < 0 or index >= self._n_docs:
            raise IndexError(f"Document index out of range: {index}")
        start = int(self._offsets[index])
        end = int(self._offsets[index + 1])
        with open(self.corpus_path, "rb") as f:
            f.seek(start)
            line = f.read(end - start)
        return line.decode("utf-8").split("\t", 1)[0]

    def __iter__(self):
        with open(self.corpus_path, "rb") as f:
            for i in range(self._n_docs):
                start = int(self._offsets[i])
                end = int(self._offsets[i + 1])
                f.seek(start)
                line = f.read(end - start)
                yield line.decode("utf-8").split("\t", 1)[0]


def corpus_offsets_path(octis_dir: Path) -> Path:
    return Path(octis_dir) / "corpus.offsets.npy"


def corpus_metadata_path(octis_dir: Path) -> Path:
    return Path(octis_dir) / "metadata.json"


def write_corpus_metadata(octis_dir: Path, n_train: int, n_val: int) -> Path:
    """Write OCTIS-compatible metadata without loading the full corpus."""
    meta = {
        "last-training-doc": int(n_train),
        "last-validation-doc": int(n_train + n_val),
    }
    path = corpus_metadata_path(octis_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    return path


def load_octis_dataset_metadata_only(octis_dir: Path):
    """Attach OCTIS metadata from disk without pandas-loading corpus.tsv."""
    from octis.dataset.dataset import Dataset

    octis_dir = Path(octis_dir)
    ds = Dataset()
    ds.dataset_path = str(octis_dir)
    meta_path = corpus_metadata_path(octis_dir)
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            ds._Dataset__metadata = json.load(f)
    else:
        ds._Dataset__metadata = {}
    ds._Dataset__corpus = []
    ds._Dataset__labels = []
    return ds
