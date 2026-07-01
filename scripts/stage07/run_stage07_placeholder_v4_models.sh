#!/usr/bin/env bash
# Stage07 topic quality for v4 placeholder compare-fit models.
#
# Frozen analysis default: call 73 only (override with CALLS= env).
# Uses stratified 100k eval tokens once for dictionary + coherence (v3-aligned).
# Outputs: results/stage07_topic_quality/placeholder_v4_call{73,...}/
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

exec "$PY" - <<'PY'
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import numpy as np
from bertopic import BERTopic
from gensim.corpora import Dictionary

from src.common.config import load_config, resolve_path
from src.stage03_train.corpus_store import (
    CorpusDocStore,
    corpus_metadata_path,
    corpus_offsets_path,
)
from src.stage07_topic_quality.topic_quality_analysis import build_topic_quality_table
from src.stage07_topic_quality.export_audit import write_stage07_audit_artifacts
from src.common.topic_posthoc.topic_info_sync import sync_topic_info_csv

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("stage07_placeholder_v4")

ROOT = Path(".")
COMPARE_ROOT = ROOT / "results/experiments/placeholder_v4_models/final_compare"
_default_calls = [73]
_env_calls = __import__("os").environ.get("CALLS", "")
CALLS = [int(c.strip()) for c in _env_calls.split(",") if c.strip()] if _env_calls else _default_calls
RULES_CONFIG = ROOT / "configs/call73/topic_posthoc_rules.yaml"
STAGE07_CONFIG = ROOT / "configs/stage07/stage07_topic_quality.yaml"
OUT_ROOT = ROOT / "results/stage07_topic_quality"
NAME_CLEANING_ROOT = ROOT / "results/stage06_name_cleaning"

paths_cfg = load_config(ROOT / "configs/stage03/paths_stage03_fit_v3.yaml")
inputs = paths_cfg["inputs"]
octis_dir = resolve_path(Path(inputs["octis_corpus_dir"]))
corpus_tsv = octis_dir / "corpus.tsv"
doc_store = CorpusDocStore(corpus_tsv, corpus_offsets_path(octis_dir))

with open(corpus_metadata_path(octis_dir), encoding="utf-8") as f:
    n_train = int(json.load(f)["last-training-doc"])

eval_idx = np.asarray(
    np.load(resolve_path(Path(inputs["eval_indices_file"]))), dtype=np.int64
)
in_val = eval_idx[(eval_idx >= n_train) & (eval_idx < len(doc_store))]
eval_idx = np.unique(in_val)
logger.info("Loading %d stratified eval docs for dictionary/coherence", len(eval_idx))
t0 = time.perf_counter()
docs = doc_store.fetch_documents(eval_idx)
tokens = [d.split() for d in docs if d]
dictionary = Dictionary(tokens)
dictionary.compactify()
logger.info(
    "Dictionary ready: %d tokens from %d docs (%.1fs)",
    len(dictionary),
    len(tokens),
    time.perf_counter() - t0,
)

summary_rows = []
for call in CALLS:
    call_dir = COMPARE_ROOT / f"call_{call}"
    enriched = call_dir / "model_compare_enriched"
    model_dir = enriched if enriched.is_dir() else call_dir / "model_compare"
    topic_info_path = call_dir / "topic_info.csv"
    out_dir = OUT_ROOT / f"placeholder_v4_call{call}"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not model_dir.is_dir():
        raise FileNotFoundError(f"Missing model: {model_dir}")

    logger.info("=== Stage07 call_%d ===", call)
    t_call = time.perf_counter()
    topic_model = BERTopic.load(str(model_dir))
    sync_topic_info_csv(topic_model, topic_info_path)
    name_cleaning_dir = NAME_CLEANING_ROOT / f"placeholder_v4_call{call}"
    name_cleaning_csv = name_cleaning_dir / "character_name_ratio_by_topic.csv"
    rep_docs_csv = name_cleaning_dir / "cleaned_representative_docs.csv"

    quality_df = build_topic_quality_table(
        topic_model,
        docs_tokens=tokens,
        dictionary=dictionary,
        stage07_config_path=STAGE07_CONFIG,
        top_k=10,
        topic_info_path=topic_info_path,
        rules_config=RULES_CONFIG,
        name_cleaning_csv=name_cleaning_csv if name_cleaning_csv.is_file() else None,
        representative_docs_csv=rep_docs_csv if rep_docs_csv.is_file() else None,
    )

    model_tag = f"placeholder_v4_call{call}"
    artifact_paths = write_stage07_audit_artifacts(
        quality_df, out_dir, model_tag=model_tag
    )

    elapsed = time.perf_counter() - t_call
    n_hard = int(quality_df["hard_exclude_candidate"].sum())
    n_soft = int(quality_df["soft_review_candidate"].sum())
    summary_rows.append(
        {
            "call": call,
            "n_topics": len(quality_df),
            "hard_exclude_candidates": n_hard,
            "soft_review_candidates": n_soft,
            "noise_candidates": int(quality_df["noise_candidate"].sum()),
            "elapsed_s": round(elapsed, 1),
            "audit_csv": str(artifact_paths["audit_csv"]),
            "quality_csv": str(artifact_paths["legacy_quality_csv"]),
            "manual_review_packet": str(artifact_paths["manual_review_packet"]),
        }
    )
    logger.info(
        "call_%d done: %d topics, hard=%d soft=%d (%.1fs)",
        call,
        len(quality_df),
        n_hard,
        n_soft,
        elapsed,
    )

summary_path = OUT_ROOT / "placeholder_v4_summary.json"
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary_rows, f, indent=2)
print(json.dumps(summary_rows, indent=2))
print(f"Summary: {summary_path}")
PY
