#!/usr/bin/env bash
# Stage06 representation refresh for a v4 placeholder compare-fit model.
#
# Loads model_compare, runs KeyBERT/POS/MMR update_topics on the 500k stratified
# fit sample (same docs as compare-fit), saves enriched model + topics JSON.
#
# Usage:
#   bash scripts/stage06/run_stage06_placeholder_v4_call.sh 55
#
# Outputs:
#   results/experiments/placeholder_v4_models/final_compare/call_<N>/model_compare_enriched/
#   results/stage06_topic_exploration/placeholder_v4_call<N>/
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

CALL="${1:?usage: $0 <bo_call>}"
PY="${ROOT}/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

exec "$PY" - "$CALL" <<'PY'
from __future__ import annotations

import json
import logging
import sys
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
from src.stage03_train.tune import _load_fit_indices
from src.stage06_topic_exploration.explore_retrained_model import (
    apply_representations_and_update,
    build_representation_models,
    evaluate_representations,
    extract_all_topics,
    save_metrics,
    save_topics,
    stage_timer,
)
from src.common.topic_posthoc.topic_info_sync import sync_topic_info_csv

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("stage06_placeholder_v4")

call = int(sys.argv[1])
ROOT = Path(".")
COMPARE_ROOT = ROOT / "results/experiments/placeholder_v4_models/final_compare"
call_dir = COMPARE_ROOT / f"call_{call}"
model_in = call_dir / "model_compare"
model_out = call_dir / "model_compare_enriched"
out_dir = ROOT / "results/stage06_topic_exploration" / f"placeholder_v4_call{call}"
out_dir.mkdir(parents=True, exist_ok=True)

if not model_in.is_dir():
    raise FileNotFoundError(f"Missing compare-fit model: {model_in}")

paths_cfg = load_config(ROOT / "configs/stage03/paths_stage03_fit_v3.yaml")
inputs = paths_cfg["inputs"]
train_cfg = load_config(ROOT / "configs/stage03/train_v4_l12_granular_phase1.yaml")
octis_dir = resolve_path(Path(inputs["octis_corpus_dir"]))
corpus_tsv = octis_dir / "corpus.tsv"
doc_store = CorpusDocStore(corpus_tsv, corpus_offsets_path(octis_dir))

with open(corpus_metadata_path(octis_dir), encoding="utf-8") as f:
    n_train = int(json.load(f)["last-training-doc"])

fit_indices = resolve_path(Path(inputs["fit_indices_file"]))
fit_max_docs = int(train_cfg.get("text", {}).get("bertopic_fit_max_docs", 500_000))
seed = int(train_cfg.get("optimization", {}).get("seed", 42))

logger.info("=== Stage06 placeholder_v4 call_%d ===", call)
t0 = time.perf_counter()

with stage_timer("load stratified fit docs"):
    fit_idx = _load_fit_indices(fit_indices, n_train=n_train, logger=logger)
    if fit_idx is None:
        raise RuntimeError(f"Missing fit indices: {fit_indices}")
    if fit_max_docs is not None and fit_idx.size > fit_max_docs:
        rng = np.random.default_rng(seed)
        keep = rng.choice(fit_idx.size, size=fit_max_docs, replace=False)
        fit_idx = np.sort(fit_idx[keep])
    fit_docs = doc_store.fetch_documents(fit_idx)

MIN_WORDS_FIT = 4
orig_len = len(fit_docs)
fit_docs = [d for d in fit_docs if len(d.split()) >= MIN_WORDS_FIT]
logger.info(
    "Short-doc filter (>=%d words): %d -> %d",
    MIN_WORDS_FIT,
    orig_len,
    len(fit_docs),
)

with stage_timer("build fit-corpus dictionary"):
    dictionary = Dictionary(doc.split() for doc in fit_docs)
    dictionary.compactify()
    logger.info("Dictionary: %d tokens from %d docs", len(dictionary), len(fit_docs))

with stage_timer(f"load model_compare call_{call}"):
    topic_model = BERTopic.load(str(model_in))

representations = build_representation_models()
apply_representations_and_update(topic_model, fit_docs, representations)

metrics = evaluate_representations(topic_model, [d.split() for d in fit_docs], dictionary=dictionary)
metrics_path = out_dir / "metrics_placeholder_v4_call.json"
save_metrics(metrics, metrics_path, format="json")

all_topics = extract_all_topics(topic_model, top_k=10)
topics_path = out_dir / "topics_all_representations_placeholder_v4_call"
save_topics(all_topics, topics_path)

if model_out.exists():
    import shutil

    shutil.rmtree(model_out)
with stage_timer("save model_compare_enriched"):
    topic_model.save(str(model_out), serialization="safetensors")

topic_info_path = call_dir / "topic_info.csv"
with stage_timer("sync topic_info.csv from enriched model"):
    sync_topic_info_csv(topic_model, topic_info_path)

elapsed = time.perf_counter() - t0
logger.info("Stage06 call_%d done in %.1fs", call, elapsed)
logger.info("Enriched model: %s", model_out)
logger.info("Topics JSON: %s", topics_path.with_suffix(".json"))
print(json.dumps({"call": call, "elapsed_s": round(elapsed, 1), "model_out": str(model_out)}, indent=2))
PY
