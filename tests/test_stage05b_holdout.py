"""Unit tests for chunked Stage05b holdout scoring."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from src.stage05b_test_holdout import test_runner


class Stage05bChunkedHoldoutTests(unittest.TestCase):
    def test_infer_on_test_chunked_accumulates_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_path = tmp_path / "test.csv"
            pd.DataFrame(
                {
                    "work_id": [1, 1],
                    "chapter_index": [0, 0],
                    "sentence_index": [0, 1],
                    "sentence": ["hello world again", "second sentence here"],
                }
            ).to_csv(csv_path, index=False)

            mock_model = MagicMock()
            mock_model.topic_representations_ = {0: [("hello", 1.0), ("world", 0.5)]}

            def fake_transform(docs, embeddings=None):
                n = len(docs)
                topics = np.array([0] * n, dtype=np.int64)
                probs = np.full((n, 2), 0.5, dtype=np.float32)
                return topics, probs

            mock_model.transform.side_effect = fake_transform

            with patch.object(test_runner, "_load_model", return_value=mock_model):
                metrics = test_runner.infer_on_test(
                    tmp_path / "model",
                    csv_path,
                    batch_size=1,
                    chunk_size=2,
                    coherence_max_docs=10,
                )

        self.assertEqual(metrics["n_docs_test"], 2)
        self.assertAlmostEqual(metrics["outlier_rate"], 0.0)
        self.assertAlmostEqual(metrics["avg_max_topic_prob"], 0.5)
        self.assertEqual(metrics["coherence_eval_docs"], 2)
        self.assertGreaterEqual(metrics["coherence_c_v"], 0.0)


if __name__ == "__main__":
    unittest.main()
