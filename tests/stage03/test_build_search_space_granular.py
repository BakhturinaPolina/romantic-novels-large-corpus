"""Tests for granular v4 BO search space construction."""

from __future__ import annotations

import unittest

from skopt.space.space import Categorical, Integer, Real

from src.stage03_train.tune import build_search_space


class BuildSearchSpaceGranularTests(unittest.TestCase):
    def test_granular_v4_space(self) -> None:
        cfg = {
            "search_space": {
                "umap__n_neighbors": [5, 45],
                "umap__n_components": [5, 20],
                "umap__min_dist": [0.0, 0.12],
                "hdbscan__min_cluster_size": [25, 350],
                "hdbscan__min_samples": [5, 45],
                "hdbscan__cluster_selection_method": ["eom", "leaf"],
                "vectorizer__min_df": [3, 25],
                "bertopic__top_n_words": [20, 50],
            }
        }
        space = build_search_space(cfg)
        self.assertNotIn("bertopic__min_topic_size", space)
        self.assertIsInstance(space["vectorizer__min_df"], Integer)
        self.assertIsInstance(space["hdbscan__cluster_selection_method"], Categorical)
        self.assertEqual(list(space["hdbscan__cluster_selection_method"].categories), ["eom", "leaf"])

    def test_legacy_proportional_min_df(self) -> None:
        cfg = {
            "search_space": {
                "umap__n_neighbors": [10, 75],
                "umap__n_components": [5, 15],
                "umap__min_dist": [0.02, 0.15],
                "hdbscan__min_cluster_size": [50, 800],
                "hdbscan__min_samples": [5, 50],
                "vectorizer__min_df": [0.002, 0.015],
                "bertopic__top_n_words": [20, 50],
            }
        }
        space = build_search_space(cfg)
        self.assertIsInstance(space["vectorizer__min_df"], Real)
        self.assertNotIn("bertopic__min_topic_size", space)


if __name__ == "__main__":
    unittest.main()
