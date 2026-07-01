"""Merge v3_rep_first snippet-trap relabels into Stage09 topic metadata bundles.

Usage:
    python3 -m src.stage08_llm_labeling.openrouter_experiments.tools.merge_snippet_trap_into_stage09 \
        --panel-json data/stage08_benchmark/call73_snippet_trap_panel.json \
        --overrides-json results/stage08_llm_labeling/placeholder_v4_call73/production/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_rep_first_snippet_trap_rep_first_topics.json \
        --slim-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
        --review-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3_review_enriched.json
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

from src.stage08_llm_labeling.openrouter_experiments.tools.export_stage09_topic_metadata import (
    slim_topic_entry,
)

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

MERGE_FIELDS = (
    "label",
    "scene_summary",
    "keywords",
    "content_type",
    "is_noise",
    "exclude_from_axes",
    "sexual_explicitness",
    "sexual_function",
    "consent_status",
    "rationale",
)


def apply_override(entry: dict[str, Any], override: dict[str, Any], *, provenance: bool) -> dict[str, Any]:
    out = dict(entry)
    for key in MERGE_FIELDS:
        if key in override:
            out[key] = override[key]
    if provenance:
        out["label_source"] = "v3_rep_first_snippet_trap"
    return out


def merge_topics(
    bundle: dict[str, Any],
    *,
    topic_ids: list[int],
    overrides: dict[str, Any],
    provenance: bool,
) -> list[dict[str, Any]]:
    log: list[dict[str, Any]] = []
    for topic_id in topic_ids:
        tid = str(topic_id)
        if tid not in overrides:
            LOGGER.warning("Override missing for topic %s — skipped", tid)
            continue
        if tid not in bundle:
            LOGGER.warning("Topic %s not in target bundle — skipped", tid)
            continue
        before_label = bundle[tid].get("label")
        bundle[tid] = apply_override(bundle[tid], overrides[tid], provenance=provenance)
        log.append({
            "topic_id": topic_id,
            "before_label": before_label,
            "after_label": bundle[tid].get("label"),
        })
    return log


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge snippet-trap rep-first labels into Stage09 JSON")
    parser.add_argument("--panel-json", required=True, type=Path)
    parser.add_argument("--overrides-json", required=True, type=Path)
    parser.add_argument("--slim-json", required=True, type=Path)
    parser.add_argument("--review-json", type=Path, default=None)
    parser.add_argument("--log-json", type=Path, default=None)
    args = parser.parse_args()

    panel = json.loads(args.panel_json.read_text(encoding="utf-8"))
    overrides = json.loads(args.overrides_json.read_text(encoding="utf-8"))
    topic_ids = [int(t) for t in panel["topic_ids"]]

    slim = json.loads(args.slim_json.read_text(encoding="utf-8"))
    slim_work = {tid: dict(entry) for tid, entry in slim.items()}
    log = merge_topics(slim_work, topic_ids=topic_ids, overrides=overrides, provenance=False)
    for topic_id in topic_ids:
        tid = str(topic_id)
        if tid in slim_work:
            slim[tid] = slim_topic_entry(slim_work[tid])

    args.slim_json.write_text(
        json.dumps(slim, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    LOGGER.info("Updated slim bundle: %s (%d panel topics)", args.slim_json, len(log))

    if args.review_json:
        review = json.loads(args.review_json.read_text(encoding="utf-8"))
        merge_topics(review, topic_ids=topic_ids, overrides=overrides, provenance=True)
        args.review_json.write_text(
            json.dumps(review, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        LOGGER.info("Updated review bundle: %s", args.review_json)

    log_path = args.log_json or args.slim_json.parent / "snippet_trap_merge_log.json"
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    LOGGER.info("Wrote merge log (%d topics): %s", len(log), log_path)


if __name__ == "__main__":
    main()
