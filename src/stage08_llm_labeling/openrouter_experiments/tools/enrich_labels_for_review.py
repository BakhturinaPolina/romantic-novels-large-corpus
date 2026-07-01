"""Enrich Stage 08 labels JSON with topic representations and representative snippets.

Adds per-topic:
- representations: KeyBERT, MMR, POS, Main keyword lists
- all_keywords: union of KeyBERT + MMR + POS (Main excluded)
- snippets: representative sentences from cleaned_representative_docs.csv

Usage:
    python -m src.stage08_llm_labeling.openrouter_experiments.tools.enrich_labels_for_review \
        --labels-json results/stage08_llm_labeling/placeholder_v4_call73/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_topic_labeling.json
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Any

REPRESENTATION_NAMES = ("KeyBERT", "MMR", "POS", "Main")


def _words_from_topic_content(topic_content: list, top_k: int) -> list[str]:
    keywords: list[str] = []
    for item in topic_content[:top_k]:
        word = None
        if isinstance(item, dict) and "word" in item:
            word = str(item["word"]).strip()
        elif isinstance(item, str):
            word = item.strip()
        if word:
            keywords.append(word)
    return keywords


def load_all_representations_from_json(
    json_path: Path,
    top_k: int = 15,
) -> dict[int, dict[str, list[str]]]:
    if not json_path.exists():
        raise FileNotFoundError(f"Topics JSON file not found: {json_path}")

    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)

    topic_to_reps: dict[int, dict[str, list[str]]] = {}
    for rep_name in REPRESENTATION_NAMES:
        rep_data = data.get(rep_name)
        if not isinstance(rep_data, dict):
            continue
        for topic_id_str, topic_content in rep_data.items():
            try:
                topic_id = int(topic_id_str)
            except ValueError:
                continue
            if topic_id == -1:
                continue
            if not isinstance(topic_content, list):
                continue
            words = _words_from_topic_content(topic_content, top_k)
            if words:
                topic_to_reps.setdefault(topic_id, {})[rep_name] = words

    LOGGER.info(
        "Loaded all representations for %d topics from %s",
        len(topic_to_reps),
        json_path.name,
    )
    return topic_to_reps


def union_keywords_excluding_main(reps: dict[str, list[str]]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for rep in ("KeyBERT", "MMR", "POS"):
        for word in reps.get(rep, []):
            key = word.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(word)
    return ordered

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

DEFAULT_TOPICS_JSON = (
    "results/stage06_name_cleaning/placeholder_v4_call73/"
    "cleaned_topics_all_representations.json"
)
DEFAULT_SNIPPETS_CSV = (
    "results/stage06_name_cleaning/placeholder_v4_call73/"
    "cleaned_representative_docs.csv"
)


def load_snippets_from_csv(csv_path: Path, max_snippets: int = 6) -> dict[int, list[str]]:
    """Load representative sentences per topic from Stage06 CSV."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Representative docs CSV not found: {csv_path}")

    by_topic: dict[int, list[tuple[int, str]]] = {}
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                topic_id = int(row["topic"])
            except (KeyError, TypeError, ValueError):
                continue
            if topic_id < 0:
                continue
            rank = int(row.get("doc_rank") or 0)
            sentence = (row.get("sentence") or "").strip()
            if sentence:
                by_topic.setdefault(topic_id, []).append((rank, sentence))

    topic_to_snippets: dict[int, list[str]] = {}
    for topic_id, ranked in by_topic.items():
        ranked.sort(key=lambda x: x[0])
        topic_to_snippets[topic_id] = [s for _, s in ranked[:max_snippets]]

    LOGGER.info("Loaded snippets for %d topics from %s", len(topic_to_snippets), csv_path.name)
    return topic_to_snippets


def enrich_labels(
    labels: dict[str, Any],
    *,
    topic_to_reps: dict[int, dict[str, list[str]]],
    topic_to_snippets: dict[int, list[str]],
    top_k: int = 15,
) -> dict[str, Any]:
    """Return a copy of labels with review fields added per topic."""
    enriched: dict[str, Any] = {}
    missing_reps = 0
    missing_snippets = 0

    for topic_id_str, entry in labels.items():
        try:
            topic_id = int(topic_id_str)
        except ValueError:
            enriched[topic_id_str] = dict(entry)
            continue

        out = dict(entry)
        reps = topic_to_reps.get(topic_id, {})
        if reps:
            trimmed = {k: v[:top_k] for k, v in reps.items()}
            out["representations"] = trimmed
            out["all_keywords"] = union_keywords_excluding_main(trimmed)
        else:
            missing_reps += 1
            out["representations"] = {}
            out["all_keywords"] = list(entry.get("keywords") or [])

        snippets = topic_to_snippets.get(topic_id, [])
        if snippets:
            out["snippets"] = snippets
        else:
            missing_snippets += 1
            out["snippets"] = []

        enriched[topic_id_str] = out

    LOGGER.info(
        "Enriched %d topics (%d missing reps, %d missing snippets)",
        len(enriched),
        missing_reps,
        missing_snippets,
    )
    return enriched


def default_output_path(labels_path: Path) -> Path:
    """Write review enriched JSON under sibling stage09_input/ for Stage08 result dirs."""
    if "stage08_llm_labeling" in labels_path.parts:
        stage09_dir = labels_path.parent / "stage09_input"
        stage09_dir.mkdir(parents=True, exist_ok=True)
        return stage09_dir / "topic_metadata_v3_review_enriched.json"

    stem = labels_path.stem
    if stem.endswith("_review"):
        return labels_path.with_name(f"{stem}_enriched.json")
    return labels_path.with_name(f"{stem}_review_enriched.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich Stage 08 labels JSON for human review")
    parser.add_argument("--labels-json", required=True, type=Path)
    parser.add_argument("--topics-json", type=Path, default=Path(DEFAULT_TOPICS_JSON))
    parser.add_argument("--snippets-csv", type=Path, default=Path(DEFAULT_SNIPPETS_CSV))
    parser.add_argument("--output-json", type=Path, default=None)
    parser.add_argument("--top-k", type=int, default=15, help="Keywords per representation")
    parser.add_argument("--max-snippets", type=int, default=6)
    args = parser.parse_args()

    labels_path = args.labels_json.resolve()
    output_path = (args.output_json or default_output_path(labels_path)).resolve()

    with labels_path.open(encoding="utf-8") as f:
        labels = json.load(f)

    topic_to_reps = load_all_representations_from_json(args.topics_json.resolve(), top_k=args.top_k)
    topic_to_snippets = load_snippets_from_csv(args.snippets_csv.resolve(), max_snippets=args.max_snippets)

    enriched = enrich_labels(
        labels,
        topic_to_reps=topic_to_reps,
        topic_to_snippets=topic_to_snippets,
        top_k=args.top_k,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)
        f.write("\n")

    LOGGER.info("Wrote %s", output_path)


if __name__ == "__main__":
    main()
