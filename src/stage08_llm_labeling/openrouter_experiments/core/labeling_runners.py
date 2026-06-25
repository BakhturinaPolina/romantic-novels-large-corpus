"""OpenRouter labeling runners — all topics LLM-labeled; Stage07 flags are hints only."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Iterator

from bertopic import BERTopic
from openai import OpenAI

from src.stage08_llm_labeling.generate_labels import (
    detect_domains,
    log_batch_progress,
    make_context_hints,
    rerank_keywords_mmr,
    stage_timer_local,
)
from src.stage08_llm_labeling.labeling_pipeline import (
    build_user_prompt,
    load_existing_labels_json,
    merge_topic_entry,
    normalize_parsed_result,
    parse_llm_json_content,
    rerank_snippets_mmr,
    validate_label_json,
)
from src.stage08_llm_labeling.prompts.loader import DEFAULT_PROMPT_VERSION, load_prompts
from src.stage08_llm_labeling.topic_quality_hints import TopicHints

LOGGER = logging.getLogger("stage08_llm_labeling.openrouter")

DEFAULT_RATE_LIMIT_DELAY_S = 4.0


def _openrouter_helpers():
    from src.stage08_llm_labeling.openrouter_experiments.core import generate_labels_openrouter as gl

    return gl


def _select_snippets(
    representative_docs: list[str] | None,
    *,
    max_snippets: int,
    max_chars_per_snippet: int,
    use_snippet_mmr: bool = True,
) -> str:
    if not representative_docs:
        return ""
    if use_snippet_mmr and len(representative_docs) > 1:
        gl = _openrouter_helpers()
        model = gl._get_embedding_model()
        ranked = rerank_snippets_mmr(
            representative_docs,
            top_k=max_snippets,
            embedding_model=model,
        )
    else:
        gl = _openrouter_helpers()
        ranked = gl.rerank_snippets_centrality(representative_docs, top_k=max_snippets)
    gl = _openrouter_helpers()
    block = gl.format_snippets(
        ranked,
        max_snippets=max_snippets,
        max_chars=max_chars_per_snippet,
    )
    return "\n\n" + block if block else ""


# Cumulative token usage for the current labeling run (reset in main_openrouter).
_run_token_usage: dict[str, int] = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "requests": 0,
}

# OpenRouter list prices per 1M tokens (input, output) — Jun 2026.
OPENROUTER_PRICE_PER_1M: dict[str, tuple[float, float]] = {
    "anthropic/claude-opus-4.6": (5.0, 25.0),
    "anthropic/claude-sonnet-4.6": (3.0, 15.0),
    "mistralai/mistral-nemo": (0.02, 0.03),
}


def reset_token_usage() -> None:
    _run_token_usage["prompt_tokens"] = 0
    _run_token_usage["completion_tokens"] = 0
    _run_token_usage["requests"] = 0


def get_token_usage() -> dict[str, int]:
    return dict(_run_token_usage)


def estimate_openrouter_cost(model_name: str, usage: dict[str, int]) -> float:
    """Estimate USD cost from OpenRouter list prices (no prompt-cache discount)."""
    in_per_m, out_per_m = OPENROUTER_PRICE_PER_1M.get(model_name, (0.0, 0.0))
    prompt = usage.get("prompt_tokens", 0)
    completion = usage.get("completion_tokens", 0)
    return (prompt / 1_000_000) * in_per_m + (completion / 1_000_000) * out_per_m


def _record_token_usage(response: Any) -> None:
    usage = getattr(response, "usage", None)
    if not usage:
        return
    _run_token_usage["prompt_tokens"] += int(getattr(usage, "prompt_tokens", 0) or 0)
    _run_token_usage["completion_tokens"] += int(getattr(usage, "completion_tokens", 0) or 0)
    _run_token_usage["requests"] += 1


def generate_label_from_keywords_openrouter(
    keywords: list[str],
    client: OpenAI,
    model_name: str,
    max_new_tokens: int = 256,
    use_mmr_reranking: bool = False,
    mmr_diversity: float = 0.5,
    mmr_top_k: int | None = None,
    temperature: float = 0.35,
    use_improved_prompts: bool = True,
    representative_docs: list[str] | None = None,
    max_snippets: int = 6,
    max_chars_per_snippet: int = 1200,
    existing_labels: set[str] | None = None,
    reasoning_effort: str | None = None,
    prompt_version: str | None = None,
    topic_hints: TopicHints | None = None,
    rate_limit_delay_s: float = DEFAULT_RATE_LIMIT_DELAY_S,
) -> dict[str, Any]:
    """Label one topic via OpenRouter (all topics; Stage07 flags are advisory hints)."""
    if use_mmr_reranking and len(keywords) > 1:
        keywords = rerank_keywords_mmr(
            keywords,
            embedding_model=None,
            top_k=mmr_top_k,
            diversity=mmr_diversity,
        )

    version = prompt_version or DEFAULT_PROMPT_VERSION
    if not use_improved_prompts:
        version = "v1"

    system_prompt, user_template = load_prompts(version)

    domains = detect_domains(keywords)
    hints_str = make_context_hints(domains) or ""
    gl = _openrouter_helpers()
    pos_str = gl.extract_pos_cues(keywords) or ""
    snippets_block = _select_snippets(
        representative_docs,
        max_snippets=max_snippets,
        max_chars_per_snippet=max_chars_per_snippet,
    )
    existing_labels_str = ""
    if existing_labels:
        existing_labels_str = (
            "\n\nExisting labels in this dataset (avoid reusing them exactly):\n"
            + ", ".join(sorted(existing_labels))
        )

    user_prompt = build_user_prompt(
        user_template=user_template,
        keywords=keywords,
        hints_str=hints_str,
        pos_str=pos_str,
        snippets_block=snippets_block,
        existing_labels_str=existing_labels_str,
        topic_hints=topic_hints,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    max_new_tokens = max(max_new_tokens, 220)

    extra_body: dict[str, Any] | None = None
    if reasoning_effort and reasoning_effort.lower() not in ("none", "off"):
        extra_body = {"reasoning": {"effort": reasoning_effort.lower(), "exclude": True}}

    def _api_call(temp: float) -> str:
        kwargs: dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_new_tokens,
            "temperature": temp,
            "top_p": 0.9,
            "frequency_penalty": 0.3,
        }
        if extra_body:
            kwargs["extra_body"] = extra_body
        try:
            kwargs["response_format"] = {"type": "json_object"}
            response = client.chat.completions.create(**kwargs)
        except Exception:
            kwargs.pop("response_format", None)
            response = client.chat.completions.create(**kwargs)
        if not response.choices:
            raise ValueError("Empty API response")
        _record_token_usage(response)
        return response.choices[0].message.content.strip()

    try:
        content = _api_call(temperature)
        raw = parse_llm_json_content(content)
        result = normalize_parsed_result(raw, keywords, prompt_version=version)
        errors = validate_label_json(result, version)
        if errors:
            LOGGER.warning("JSON schema validation failed, retrying: %s", errors[0][:120])
            content = _api_call(0.1)
            raw = parse_llm_json_content(content)
            result = normalize_parsed_result(raw, keywords, prompt_version=version)

        if topic_hints is not None:
            result["stage07_exclude_from_axes"] = topic_hints.exclude_from_axes
            result["stage07_posthoc_reason"] = topic_hints.posthoc_reason
            result["stage07_content_type"] = topic_hints.content_type

        LOGGER.info(
            "Generated label: %s | content_type=%s",
            result.get("label"),
            result.get("content_type", "n/a"),
        )
        return result
    except Exception as exc:
        LOGGER.warning("Error generating label for keywords %s: %s", keywords[:3], exc)
        fallback = keywords[0] if keywords else "Topic"
        return {"label": fallback, "scene_summary": ""}


def _write_json_entry(f, first_item: bool, topic_id: int, entry: dict[str, Any]) -> bool:
    if not first_item:
        f.write(",\n")
    f.write(f'  "{topic_id}": {json.dumps(entry, ensure_ascii=False)}')
    f.flush()
    return False


def _write_labels_json(json_path: Path, topic_data: dict[int, dict[str, Any]]) -> None:
    serializable = {str(k): v for k, v in sorted(topic_data.items(), key=lambda x: x[0])}
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
        f.flush()


def generate_labels_streaming(
    pos_topics_iter: Iterator[tuple[int, list[str]]],
    client: OpenAI,
    model_name: str,
    output_path: Path,
    max_new_tokens: int = 256,
    batch_size: int = 50,
    temperature: float = 0.35,
    limit: int | None = None,
    use_improved_prompts: bool = True,
    topic_model: BERTopic | None = None,
    topic_to_snippets: dict[int, list[str]] | None = None,
    max_snippets: int = 6,
    max_chars_per_snippet: int = 1200,
    reasoning_effort: str | None = None,
    prompt_version: str | None = None,
    quality_hints: dict[int, TopicHints] | None = None,
    resume: bool = True,
    rate_limit_delay_s: float = DEFAULT_RATE_LIMIT_DELAY_S,
) -> dict[int, dict[str, Any]]:
    """Stream labels for all topics; writes full metadata per topic."""
    json_path = Path(str(output_path.parent) + "/" + output_path.name + ".json")
    json_path.parent.mkdir(parents=True, exist_ok=True)

    if topic_to_snippets is None and topic_model is not None:
        gl = _openrouter_helpers()
        topic_to_snippets = gl.extract_representative_docs_per_topic(topic_model)
    topic_to_snippets = topic_to_snippets or {}

    existing_on_disk = load_existing_labels_json(json_path) if resume else {}
    topic_data: dict[int, dict[str, Any]] = dict(existing_on_disk)
    existing_labels: set[str] = {
        str(v.get("label", "")) for v in topic_data.values() if v.get("label")
    }

    processed_count = 0
    batch_idx = 0

    with stage_timer_local("Generating labels (streaming)"):
        for topic_id, keywords in pos_topics_iter:
            if limit is not None and processed_count >= limit:
                break

            if resume and topic_id in topic_data:
                LOGGER.info("topic %d | resume skip (already labeled)", topic_id)
                continue

            processed_count += 1
            hints = quality_hints.get(topic_id) if quality_hints else None
            rep_docs = topic_to_snippets.get(topic_id, [])

            LOGGER.info(
                "topic %d | tier=%s | exclude_flag=%s | snippets=%d",
                topic_id,
                hints.tier if hints else "?",
                hints.exclude_from_axes if hints else False,
                len(rep_docs),
            )

            t0 = time.perf_counter()
            result = generate_label_from_keywords_openrouter(
                keywords=keywords,
                client=client,
                model_name=model_name,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                use_improved_prompts=use_improved_prompts,
                representative_docs=rep_docs,
                max_snippets=max_snippets,
                max_chars_per_snippet=max_chars_per_snippet,
                existing_labels=existing_labels or None,
                reasoning_effort=reasoning_effort,
                prompt_version=prompt_version,
                topic_hints=hints,
                rate_limit_delay_s=rate_limit_delay_s,
            )
            elapsed = time.perf_counter() - t0

            entry = merge_topic_entry(keywords, result)
            topic_data[topic_id] = entry
            label = entry.get("label", "")
            if label:
                existing_labels.add(label)

            _write_labels_json(json_path, topic_data)
            LOGGER.info("topic %d | label='%s' | %.2fs", topic_id, label, elapsed)

            if processed_count % batch_size == 0:
                batch_idx += 1
                log_batch_progress(
                    "Label generation (streaming)",
                    batch_idx,
                    processed_count - batch_size + 1,
                    processed_count,
                    -1,
                )

            time.sleep(rate_limit_delay_s)

    LOGGER.info("Saved %d topic entries to %s", len(topic_data), json_path)
    return topic_data


def generate_all_labels(
    pos_topics: dict[int, list[str]],
    client: OpenAI,
    model_name: str,
    max_new_tokens: int = 256,
    batch_size: int = 50,
    temperature: float = 0.35,
    use_improved_prompts: bool = True,
    topic_model: BERTopic | None = None,
    topic_to_snippets: dict[int, list[str]] | None = None,
    max_snippets: int = 6,
    max_chars_per_snippet: int = 1200,
    reasoning_effort: str | None = None,
    prompt_version: str | None = None,
    quality_hints: dict[int, TopicHints] | None = None,
    rate_limit_delay_s: float = DEFAULT_RATE_LIMIT_DELAY_S,
) -> dict[int, dict[str, Any]]:
    """Generate labels for all topics (batch mode, keeps all in memory)."""
    if topic_to_snippets is None and topic_model is not None:
        gl = _openrouter_helpers()
        topic_to_snippets = gl.extract_representative_docs_per_topic(topic_model)
    topic_to_snippets = topic_to_snippets or {}

    topic_data: dict[int, dict[str, Any]] = {}
    existing_labels: set[str] = set()
    items = list(pos_topics.items())
    total = len(items)

    with stage_timer_local("Generating labels for all topics"):
        for idx, (topic_id, keywords) in enumerate(items, start=1):
            hints = quality_hints.get(topic_id) if quality_hints else None
            rep_docs = topic_to_snippets.get(topic_id, [])
            result = generate_label_from_keywords_openrouter(
                keywords=keywords,
                client=client,
                model_name=model_name,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                use_improved_prompts=use_improved_prompts,
                representative_docs=rep_docs,
                max_snippets=max_snippets,
                max_chars_per_snippet=max_chars_per_snippet,
                existing_labels=existing_labels or None,
                reasoning_effort=reasoning_effort,
                prompt_version=prompt_version,
                topic_hints=hints,
                rate_limit_delay_s=rate_limit_delay_s,
            )
            entry = merge_topic_entry(keywords, result)
            topic_data[topic_id] = entry
            if entry.get("label"):
                existing_labels.add(entry["label"])

            if idx % batch_size == 0 or idx == total:
                log_batch_progress(
                    "Label generation",
                    idx // batch_size + (1 if idx % batch_size else 0),
                    max(1, idx - batch_size + 1),
                    idx,
                    total,
                )
            time.sleep(rate_limit_delay_s)

    return topic_data
