"""Shared Stage 08 labeling pipeline helpers (prompts, validation, snippets, resume)."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import numpy as np

from src.stage08_llm_labeling.lexicon import forbidden_genre_cliche_phrases
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

V3_RESULT_DEFAULTS: dict[str, Any] = {
    "content_type": "scene",
    "exclude_from_axes": False,
    "sexual_explicitness": "none",
    "sexual_function": "none",
    "consent_status": "not_applicable",
    "is_noise": False,
    "rationale": "",
    "scene_summary": "",
}


def validate_v3_consistency(result: dict[str, Any]) -> list[str]:
    """Soft checks for v3 sexual-field coherence (logged as warnings, not schema errors)."""
    warnings: list[str] = []
    sexual_fn = str(result.get("sexual_function", "none"))
    consent = str(result.get("consent_status", "not_applicable"))

    if sexual_fn == "consent_boundary" and consent == "not_applicable":
        warnings.append("sexual_function=consent_boundary but consent_status=not_applicable")
    return warnings


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
    defaults = V3_RESULT_DEFAULTS if prompt_version.startswith("v3") else V2_RESULT_DEFAULTS
    result = {**defaults, **raw}
    label_text = str(result.get("label", "")).strip()
    result["label"] = normalize_label_text(label_text)

    scene = str(result.get("scene_summary", "") or "")
    if scene:
        result["scene_summary"] = clean_scene_summary_text(scene)

    if prompt_version.startswith("v1"):
        for key in ("content_type", "register", "exclude_from_axes", "subgenre_hints", "merge_group_hint"):
            result.pop(key, None)

    if prompt_version.startswith("v2"):
        for key in ("primary_categories", "secondary_categories", "subgenre_hints"):
            val = result.get(key)
            if val is None:
                result[key] = []
            elif not isinstance(val, list):
                result[key] = [str(val)]
        ct = result.get("content_type", "scene")
        if result.get("is_noise") or ct in ("noise", "paratext"):
            result["exclude_from_axes"] = True
        elif ct == "discourse":
            result["exclude_from_axes"] = False

    if prompt_version.startswith("v3"):
        ct = result.get("content_type", "scene")
        if result.get("is_noise") or ct in ("noise", "paratext"):
            result["exclude_from_axes"] = True
        elif ct == "discourse":
            result["exclude_from_axes"] = False
        for key in ("register", "subgenre_hints", "axis_hint"):
            result.pop(key, None)
        for warn in validate_v3_consistency(result):
            LOGGER.warning("v3 consistency: %s", warn)
        label_lower = str(result.get("label", "")).lower()
        for phrase in forbidden_genre_cliche_phrases():
            if phrase in label_lower:
                LOGGER.warning("v3 label contains genre cliché phrase: %r in %r", phrase, result.get("label"))

    return result


def normalize_label_text(raw: str) -> str:
    """Format label text (Title Case, length cap) without keyword-based rewriting."""
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
    return label or "Topic"


def clean_scene_summary_text(summary: str) -> str:
    """Light whitespace cleanup for scene summaries."""
    return re.sub(r"\s+", " ", summary).strip()


def format_stage07_hints_block(hints: TopicHints | None) -> str:
    if hints is None:
        return "(no Stage07 quality hints for this topic)"
    return hints.format_for_prompt()


def format_keyword_list(words: list[str]) -> str:
    return ", ".join(words) if words else "(none)"


def format_all_keywords_union(reps: dict[str, list[str]]) -> str:
    """Union KeyBERT, MMR, POS (Main excluded), preserving first-seen order."""
    seen: set[str] = set()
    ordered: list[str] = []
    for rep in ("KeyBERT", "MMR", "POS"):
        for word in reps.get(rep, []):
            key = word.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(word)
    return format_keyword_list(ordered)


_NO_SNIPPETS_BLOCK = """
(NO REPRESENTATIVE SNIPPETS AVAILABLE for this topic.)

Because snippets are missing:
- Do NOT invent specific settings, body parts, or actions beyond what keyword evidence supports.
- Prefer broad but natural scene names over literal keyword chains.
- Keep scene_summary generic but grammatical.
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
    representations: dict[str, list[str]] | None = None,
) -> str:
    stage07 = format_stage07_hints_block(topic_hints)
    snippet_text = snippets_block.strip()
    if not snippet_text:
        snippet_text = _NO_SNIPPETS_BLOCK

    reps = representations or {"POS": keywords}
    format_kwargs: dict[str, str] = {
        "kw": format_keyword_list(keywords),
        "hints": hints_str,
        "pos": format_keyword_list(reps.get("POS", keywords)),
        "pos_cues": pos_str or "(none)",
        "snippets": snippet_text,
        "existing_labels": existing_labels_str or "(none)",
        "stage07_hints": stage07,
        "keybert": format_keyword_list(reps.get("KeyBERT", [])),
        "mmr": format_keyword_list(reps.get("MMR", [])),
        "main": format_keyword_list(reps.get("Main", [])),
        "all_keywords": format_all_keywords_union(reps),
    }

    # Legacy v1/v2 templates use {kw}{hints} inline — hints_str kept empty for v3
    if "{kw}" in user_template and "keybert" not in user_template:
        format_kwargs["kw"] = ", ".join(keywords) + (hints_str or "")

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
