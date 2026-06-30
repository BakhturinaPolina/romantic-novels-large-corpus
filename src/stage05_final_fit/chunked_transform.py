"""Chunked BERTopic transform helpers for holdout and full-corpus inference."""

from __future__ import annotations

import logging
import time
from typing import Any

import numpy as np
from bertopic import BERTopic
from tqdm import tqdm

LOGGER = logging.getLogger(__name__)


def transform_docs_batched(
    topic_model: BERTopic,
    docs: list[str],
    *,
    embeddings: np.ndarray | None = None,
    batch_size: int = 8192,
    desc: str = "transform",
) -> tuple[np.ndarray, np.ndarray | None]:
    """Transform documents in batches; return (topics, probs) aligned to docs."""
    if not docs:
        return np.array([], dtype=np.int64), None

    if batch_size <= 0 or batch_size >= len(docs):
        if embeddings is not None:
            topics, probs = topic_model.transform(docs, embeddings=embeddings)
        else:
            topics, probs = topic_model.transform(docs)
        topics_arr = np.asarray(topics, dtype=np.int64)
        probs_arr = np.asarray(probs) if probs is not None else None
        return topics_arr, probs_arr

    all_topics: list[np.ndarray] = []
    all_probs: list[np.ndarray] = []
    n_batches = (len(docs) + batch_size - 1) // batch_size
    pbar = tqdm(
        total=len(docs),
        unit="doc",
        unit_scale=True,
        desc=desc,
        ncols=100,
        mininterval=1.0,
    )
    for batch_idx in range(n_batches):
        start = batch_idx * batch_size
        end = min(len(docs), start + batch_size)
        batch_docs = docs[start:end]
        batch_emb = embeddings[start:end] if embeddings is not None else None
        if batch_emb is not None:
            topics, probs = topic_model.transform(batch_docs, embeddings=batch_emb)
        else:
            topics, probs = topic_model.transform(batch_docs)
        all_topics.append(np.asarray(topics, dtype=np.int64))
        if probs is not None:
            all_probs.append(np.asarray(probs))
        pbar.update(len(batch_docs))
        pbar.set_postfix({"batch": f"{batch_idx + 1}/{n_batches}"})
    pbar.close()

    topics_full = np.concatenate(all_topics)
    probs_full: np.ndarray | None = None
    if all_probs:
        probs_full = np.vstack(all_probs)
    return topics_full, probs_full


def streaming_transform_metrics(
    topic_model: BERTopic,
    doc_batches: Any,
    *,
    batch_size: int = 8192,
    coherence_max_docs: int = 100_000,
    logger: logging.Logger | None = None,
) -> tuple[dict[str, float | int], list[list[str]]]:
    """
    Stream document batches through transform and accumulate holdout metrics.

    ``doc_batches`` yields ``(docs, embeddings_or_none)`` tuples.
    Returns (metrics_partial, coherence_tokens_sample).
    """
    log = logger or LOGGER
    n_docs = 0
    n_outliers = 0
    max_prob_sum = 0.0
    max_prob_count = 0
    coherence_tokens: list[list[str]] = []

    batch_num = 0
    stream_start = time.perf_counter()
    for docs, embeddings in doc_batches:
        if not docs:
            continue
        batch_num += 1
        topics, probs = transform_docs_batched(
            topic_model,
            docs,
            embeddings=embeddings,
            batch_size=batch_size,
            desc=f"holdout batch {batch_num}",
        )
        n_docs += len(topics)
        n_outliers += int(np.sum(topics == -1))
        if probs is not None and probs.size:
            batch_max = np.max(probs, axis=1)
            max_prob_sum += float(batch_max.sum())
            max_prob_count += len(batch_max)

        if len(coherence_tokens) < coherence_max_docs:
            remaining = coherence_max_docs - len(coherence_tokens)
            for doc in docs[:remaining]:
                coherence_tokens.append(doc.split())
            if len(coherence_tokens) >= coherence_max_docs:
                log.info(
                    "Coherence eval token cap reached (%d docs); using stratified stream sample.",
                    coherence_max_docs,
                )

    elapsed = time.perf_counter() - stream_start
    outlier_rate = float(n_outliers / n_docs) if n_docs else 0.0
    avg_max_prob = float(max_prob_sum / max_prob_count) if max_prob_count else 0.0
    log.info(
        "Streaming transform done: %d docs in %.1fs (outlier=%.4f avg_max_prob=%.4f)",
        n_docs,
        elapsed,
        outlier_rate,
        avg_max_prob,
    )
    partial = {
        "n_docs_test": n_docs,
        "outlier_rate": outlier_rate,
        "avg_max_topic_prob": avg_max_prob,
    }
    return partial, coherence_tokens
