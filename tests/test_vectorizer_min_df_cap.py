"""Tests for BERTopic c-TF-IDF vectorizer min_df capping."""

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from src.legacy.stage03_modeling.bertopic_octis_model import _cap_vectorizer_min_df


def _doc_counts(vectorizer: CountVectorizer, n_docs: int) -> tuple[float, float]:
    min_df = _cap_vectorizer_min_df(vectorizer, n_docs)
    max_df = vectorizer.max_df if vectorizer.max_df is not None else 1.0
    max_count = max_df if isinstance(max_df, int) else float(max_df) * n_docs
    min_count = min_df if isinstance(min_df, int) else float(min_df) * n_docs
    return max_count, min_count


def test_cap_absolute_min_df_when_few_topics():
    vectorizer = CountVectorizer(min_df=5, max_df=1.0)
    assert _cap_vectorizer_min_df(vectorizer, 3) == 1


def test_keep_absolute_min_df_when_enough_topics():
    vectorizer = CountVectorizer(min_df=5, max_df=1.0)
    assert _cap_vectorizer_min_df(vectorizer, 10) == 5


def test_safe_ctfidf_single_feature():
    import scipy.sparse as sp

    from src.legacy.stage03_modeling.bertopic_octis_model import SafeClassTfidfTransformer

    X = sp.csr_matrix([[10], [5], [3]], dtype=np.float64)
    model = SafeClassTfidfTransformer(bm25_weighting=True, reduce_frequent_words=True)
    model.fit(X)
    out = model.transform(X)
    assert out.shape == (3, 1)
