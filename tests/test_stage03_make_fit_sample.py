"""Tests for the Stage03 stratified fit/eval index selector."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from src.stage03_train.data_io import iter_split_csv_chunks
from src.stage03_train.make_fit_sample import load_metadata_map, select_stratified_indices


def _write_sentence_csv(path: Path, *, n_books: int, rows_per_book: int) -> None:
    rows = []
    for wid in range(n_books):
        for idx in range(rows_per_book):
            rows.append(
                {
                    "work_id": wid,
                    "chapter_index": idx // 10,
                    "chapter_title": "",
                    "sentence_index": idx,
                    "sentence": f"book {wid} narrative sentence number {idx} love",
                }
            )
    pd.DataFrame(rows).to_csv(path, index=False)


def _write_metadata_csv(path: Path, *, n_books: int, n_authors: int) -> None:
    rows = []
    for wid in range(n_books):
        rows.append(
            {
                "work_id": wid,
                "author_name": f"author_{wid % n_authors}",
                "publication_year": 2000 + (wid % 5),
                "genre_group": "contemporary",
            }
        )
    pd.DataFrame(rows).to_csv(path, index=False)


def _clean_stream_work_ids(csv_path: Path) -> list[str]:
    """Replicate iter_split_csv_chunks order -> per-row work labels (work_<id>)."""
    labels: list[str] = []
    for _docs, lbls in iter_split_csv_chunks(csv_path, chunk_size=137):
        labels.extend(lbls)
    return labels


class MakeFitSampleTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_indices_respect_caps_target_and_alignment(self) -> None:
        sent_csv = self.tmp / "sentences.csv"
        meta_csv = self.tmp / "meta.csv"
        _write_sentence_csv(sent_csv, n_books=40, rows_per_book=100)
        _write_metadata_csv(meta_csv, n_books=40, n_authors=4)

        meta = load_metadata_map(meta_csv)
        indices, manifest, n_clean = select_stratified_indices(
            sent_csv,
            target_rows=500,
            seed=42,
            metadata_map=meta,
            index_offset=0,
            chunk_size=137,
            min_rows_per_book=5,
            max_rows_per_book=20,
            max_rows_per_author=200,
            position_bins=5,
        )

        self.assertEqual(n_clean, 4000)
        self.assertEqual(manifest["actual_rows"], len(indices))
        self.assertEqual(manifest["n_books_input"], 40)
        # Indices are sorted, unique, in range.
        self.assertTrue(np.all(np.diff(indices) > 0))
        self.assertGreaterEqual(int(indices.min()), 0)
        self.assertLess(int(indices.max()), n_clean)

        # Alignment: gather work labels at selected indices from the clean stream,
        # confirm per-book cap holds (book == work label).
        stream_labels = _clean_stream_work_ids(sent_csv)
        self.assertEqual(len(stream_labels), n_clean)
        picked = [stream_labels[i] for i in indices]
        counts = pd.Series(picked).value_counts()
        self.assertLessEqual(int(counts.max()), 20)

        # Narrative position spread: selected rows are not only book openings.
        # sentence_index == position within book == idx % 100 here.
        positions = [i % 100 for i in indices]
        self.assertGreater(max(positions), 50)

    def test_offset_places_indices_in_val_partition(self) -> None:
        sent_csv = self.tmp / "val.csv"
        _write_sentence_csv(sent_csv, n_books=10, rows_per_book=50)
        n_train = 123456
        indices, manifest, n_clean = select_stratified_indices(
            sent_csv,
            target_rows=100,
            seed=7,
            metadata_map={},
            index_offset=n_train,
            chunk_size=64,
            min_rows_per_book=5,
            max_rows_per_book=20,
            max_rows_per_author=1000,
        )
        self.assertEqual(n_clean, 500)
        self.assertGreaterEqual(int(indices.min()), n_train)
        self.assertLess(int(indices.max()), n_train + n_clean)
        self.assertFalse(manifest["has_metadata"])

    def test_works_without_position_column(self) -> None:
        sent_csv = self.tmp / "minimal.csv"
        pd.DataFrame(
            {
                "work_id": [w for w in range(10) for _ in range(50)],
                "sentence": [f"sentence {i} love story" for i in range(500)],
            }
        ).to_csv(sent_csv, index=False)
        indices, manifest, n_clean = select_stratified_indices(
            sent_csv,
            target_rows=100,
            seed=3,
            metadata_map={},
            chunk_size=64,
            min_rows_per_book=5,
            max_rows_per_book=20,
            max_rows_per_author=1000,
        )
        self.assertEqual(n_clean, 500)
        self.assertLessEqual(len(indices), 100)
        self.assertIsNone(manifest["position_column"])


if __name__ == "__main__":
    unittest.main()
