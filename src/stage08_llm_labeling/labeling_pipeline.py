"""Shared Stage 08 labeling pipeline helpers (prompts, validation, snippets, resume)."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import numpy as np

from src.stage08_llm_labeling.lexicon import (
    explicit_sexual_terms,
    family_relation_terms,
    forbidden_neutral_words,
)
from src.stage08_llm_labeling.prompts.loader import DEFAULT_PROMPT_VERSION, load_prompts, load_schema
from src.stage08_llm_labeling.topic_quality_hints import TopicHints

LOGGER = logging.getLogger("stage08_llm_labeling.pipeline")

V2_RESULT_DEFAULTS: dict[str, Any] = {
    "content_type": "scene",
    "register": "neutral",
    "exclude_from_axes": False,
    "subgenre_hints": [],
    "merge_group_hint": None,
    "primary_categories": [],
    "secondary_categories": [],
    "is_noise": False,
    "rationale": "",
    "scene_summary": "",
}


def validate_label_json(result: dict[str, Any], prompt_version: str) -> list[str]:
    """Return list of validation errors (empty if ok)."""
    schema = load_schema(prompt_version)
    if not schema:
        return []
    try:
        import jsonschema

        jsonschema.validate(instance=result, schema=schema)
        return []
    except Exception as exc:
        return [str(exc)]


def parse_llm_json_content(content: str) -> dict[str, Any]:
    """Extract JSON object from model response."""
    json_content = content.strip()
    if "```json" in json_content:
        json_content = json_content.split("```json")[1].split("```")[0].strip()
    elif "```" in json_content:
        json_content = json_content.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        label_match = re.search(r'"label"\s*:\s*"([^"]+)"', json_content)
        scene_match = re.search(r'"scene_summary"\s*:\s*"([^"]+)"', json_content)
        if label_match:
            out: dict[str, Any] = {"label": label_match.group(1)}
            if scene_match:
                out["scene_summary"] = scene_match.group(1)
            return out
        raise


def normalize_parsed_result(
    raw: dict[str, Any],
    keywords: list[str],
    *,
    prompt_version: str,
) -> dict[str, Any]:
    """Merge defaults, normalize label, apply post-hoc safety nets."""
    result = {**V2_RESULT_DEFAULTS, **raw}
    label_text = str(result.get("label", "")).strip()
    result["label"] = normalize_label_text(label_text, keywords=keywords)

    scene = str(result.get("scene_summary", "") or "")
    if scene:
        result["scene_summary"] = clean_scene_summary_text(scene, keywords)

    if prompt_version.startswith("v1"):
        for key in ("content_type", "register", "exclude_from_axes", "subgenre_hints", "merge_group_hint"):
            result.pop(key, None)

    for key in ("primary_categories", "secondary_categories", "subgenre_hints"):
        val = result.get(key)
        if val is None:
            result[key] = []
        elif not isinstance(val, list):
            result[key] = [str(val)]

    if prompt_version.startswith("v2"):
        ct = result.get("content_type", "scene")
        if result.get("is_noise") or ct in ("noise", "paratext"):
            result["exclude_from_axes"] = True
        elif ct == "discourse":
            result["exclude_from_axes"] = False

    return result


def normalize_label_text(raw: str, keywords: list[str] | None = None) -> str:
    label = raw.strip().strip('"').strip("'")
    label = re.sub(r"<s>|</s>|\[.*?\]", "", label)
    label = re.sub(r"<[^>]+>", "", label)
    label = re.sub(r"\s+", " ", label).strip().rstrip(".,;:!-")

    words = label.split()
    if len(words) > 6:
        label = " ".join(words[:6])

    def smart_tc(w: str) -> str:
        if w.lower() in {"and", "or", "in", "on", "of", "at", "to"}:
            return w.lower()
        if "-" in w:
            return "-".join(smart_tc(part) for part in w.split("-"))
        return w.capitalize()

    label = " ".join(smart_tc(w) for w in label.split())

    low = label.lower()
    if low in {"time units passing", "time passing units"} or ("units" in low and "time" in low):
        label = "Waiting And Watching Clock"

    if keywords:
        kw_lower = [k.lower() for k in keywords]
        sexual = explicit_sexual_terms()
        forbidden = forbidden_neutral_words()
        family = family_relation_terms()

        if not sexual.intersection(kw_lower):
            label_lower = label.lower()
            for word in forbidden:
                if word in label_lower:
                    label = re.sub(rf"\b{re.escape(word)}\b", "", label, flags=re.IGNORECASE)
                    label = re.sub(r"\s+", " ", label).strip()

        if not family.intersection(kw_lower):
            for pat, repl in [
                (r"\bwith\s+son\b", ""),
                (r"\bson\b", "player"),
                (r"\bwith\s+(?:father|dad)\b", ""),
                (r"\b(?:father|dad)\b", "goalie"),
            ]:
                if re.search(pat, label, re.IGNORECASE):
                    snippets_text = " ".join(kw_lower)
                    if not re.search(pat.replace(r"\b", ""), snippets_text):
                        label = re.sub(pat, repl, label, flags=re.IGNORECASE)
                        label = re.sub(r"\s+", " ", label).strip()

    return label or (keywords[0] if keywords else "Topic")


def clean_scene_summary_text(summary: str, keywords: list[str]) -> str:
    if not summary:
        return summary
    keywords_lower = [kw.lower() for kw in keywords]
    repair_kw = {"repair", "fix", "mechanic", "garage", "engine", "broken"}
    family_kw = family_relation_terms()

    if not repair_kw.intersection(keywords_lower):
        summary = re.sub(
            r"discuss(?:ing)?\s+car\s+repairs?\s+(?:and\s+)?(?:other\s+)?topics?",
            "discuss various topics",
            summary,
            flags=re.IGNORECASE,
        )
        summary = re.sub(r"car\s+repairs?", "their cars", summary, flags=re.IGNORECASE)

    if not family_kw.intersection(keywords_lower):
        for pat, repl in [
            (r"\bhis\s+son\b", "the player"),
            (r"\bher\s+son\b", "the player"),
            (r"\bthe\s+son\b", "the player"),
        ]:
            summary = re.sub(pat, repl, summary, flags=re.IGNORECASE)

    return summary.strip()


def format_stage07_hints_block(hints: TopicHints | None) -> str:
    if hints is None:
        return "(no Stage07 quality hints for this topic)"
    flags = ", ".join(hints.posthoc_flags) if hints.posthoc_flags else "(none)"
    return (
        f"doc_count={hints.doc_count}, tier={hints.tier}, "
        f"stage07_content_type={hints.content_type}, posthoc_flags=[{flags}], "
        f"stage07_exclude_from_axes={hints.exclude_from_axes} (advisory flag only — "
        f"label all topics; you may agree or override with rationale), "
        f"posthoc_reason={hints.posthoc_reason or '(none)'}"
    )


_NO_SNIPPETS_BLOCK = """
(NO REPRESENTATIVE SNIPPETS AVAILABLE for this topic — keywords and POS cues only.)

Because snippets are missing:
- Do NOT invent specific settings, body parts, or actions beyond what top keywords support.
- Prefer broad but natural scene names over literal keyword chains.
- Keep scene_summary generic but grammatical; avoid stuffing multiple keywords into one sentence.
""".strip()


def build_user_prompt(
    *,
    user_template: str,
    keywords: list[str],
    hints_str: str,
    pos_str: str,
    snippets_block: str,
    existing_labels_str: str,
    topic_hints: TopicHints | None,
) -> str:
    stage07 = format_stage07_hints_block(topic_hints)
    snippet_text = snippets_block.strip()
    if not snippet_text:
        snippet_text = _NO_SNIPPETS_BLOCK
    format_kwargs = {
        "kw": ", ".join(keywords),
        "hints": hints_str,
        "pos": pos_str,
        "snippets": snippet_text,
        "existing_labels": existing_labels_str,
    }
    if "{stage07_hints}" in user_template:
        format_kwargs["stage07_hints"] = stage07
    return user_template.format(**format_kwargs)


def rerank_snippets_mmr(
    docs: list[str],
    top_k: int,
    embedding_model,
    diversity: float = 0.5,
) -> list[str]:
    """Centrality-first seed, then MMR for diverse snippets."""
    if not docs or top_k <= 0:
        return []
    if len(docs) <= top_k:
        return docs

    embeddings = embedding_model.encode(docs, normalize_embeddings=True)
    centroid = embeddings.mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm > 0:
        centroid = centroid / norm
    sims = embeddings @ centroid
    seed_idx = int(np.argmax(sims))

    selected = [seed_idx]
    remaining = [i for i in range(len(docs)) if i != seed_idx]

    while len(selected) < top_k and remaining:
        best_score = -float("inf")
        best_idx = None
        for idx in remaining:
            rel = float(embeddings[idx] @ centroid)
            if selected:
                div = 1.0 - max(float(embeddings[idx] @ embeddings[j]) for j in selected)
            else:
                div = 1.0
            score = (1 - diversity) * rel + diversity * div
            if score > best_score:
                best_score = score
                best_idx = idx
        if best_idx is None:
            break
        selected.append(best_idx)
        remaining.remove(best_idx)

    return [docs[i] for i in selected]


def load_existing_labels_json(json_path: Path) -> dict[int, dict[str, Any]]:
    if not json_path.is_file():
        return {}
    with json_path.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}


def merge_topic_entry(keywords: list[str], result: dict[str, Any]) -> dict[str, Any]:
    label = result.get("label", "")
    entry = {"label": label, "keywords": keywords, **{k: v for k, v in result.items() if k != "label"}}
    return entry
