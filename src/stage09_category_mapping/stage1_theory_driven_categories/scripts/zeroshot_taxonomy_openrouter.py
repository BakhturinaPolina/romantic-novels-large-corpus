"""Stage 09: Zero-shot taxonomy mapping of BERTopic topics using OpenRouter (Mistral-Nemo).

This module assumes you already ran Stage 08 LLM labeling and have a JSON file
with enriched topic metadata of the form:

{
  "33": {
    "label": "Business Discussion",
    "keywords": ["business", "company", "dollars", ...],
    "primary_categories": ["domestic_life", "work_or_school"],
    "secondary_categories": ["setting:dinner_table", "activity:discussion"],
    "scene_summary": "The couple discusses business matters at the dinner table.",
    "is_noise": false,
    "rationale": "...",
    ...
  },
  ...
}

We now map each topic to a fixed Romance Corpus Topic Taxonomy using zero-shot
classification with mistralai/Mistral-Nemo-Instruct-2407 via OpenRouter.

The output is a JSON mapping:

{
  "33": {
    "topic_id": 33,
    "main_category_id": "6.1",
    "secondary_category_id": "5.1",
    "other_plausible_ids": ["4.2"],
    "is_noise": false,
    "rationale": "..."
  },
  ...
}
"""

from __future__ import annotations

import json
import logging
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from openai import OpenAI
from bertopic import BERTopic

# Reuse existing OpenRouter client + helpers from Stage 08
from src.stage08_llm_labeling.openrouter_experiments.core.generate_labels_openrouter import (
    DEFAULT_OPENROUTER_API_KEY,
    DEFAULT_OPENROUTER_BASE_URL,
    DEFAULT_OPENROUTER_MODEL,
    load_openrouter_client,
    rerank_snippets_centrality,
    format_snippets,
    extract_representative_docs_per_topic,
)

# Reuse model loading helpers from Stage 1
from src.stage06_topic_exploration.explore_retrained_model import (
    DEFAULT_BASE_DIR,
    DEFAULT_EMBEDDING_MODEL,
    load_native_bertopic_model,
)
from src.stage08_llm_labeling.openrouter_experiments.core.structured_json_call import (
    chat_completions_json_schema,
    parse_json_object_content,
)
from src.stage09_category_mapping.stage1_theory_driven_categories.prompts import (
    DEFAULT_PROMPT_VERSION,
    load_taxonomy_prompts,
)
from src.stage09_category_mapping.stage1_theory_driven_categories.prompts.taxonomy_mapping_schema import (
    build_taxonomy_mapping_schema,
    normalize_taxonomy_mapping_result,
    validate_taxonomy_mapping_json,
)

from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
    DEFAULT_TAXONOMY_PATH,
    apply_domain_heuristics,
    enrich_with_category_names,
    fallback_main_category,
    load_taxonomy_nodes,
    taxonomy_block_for_prompt,
    taxonomy_by_id,
    try_pre_route_taxonomy,
    valid_taxonomy_ids,
)

LOGGER = logging.getLogger("stage09_zeroshot_taxonomy")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

# Production default for taxonomy mapping (Stage08 labels use the same model family).
STAGE09_DEFAULT_MODEL = "anthropic/claude-sonnet-4.6"


# ---------------------------------------------------------------------------
# 1. Romance Corpus Topic Taxonomy v2 (configs/stage09/romance_corpus_taxonomy_v2.yaml)
# ---------------------------------------------------------------------------

TAXONOMY_CONFIG_PATH = DEFAULT_TAXONOMY_PATH
TAXONOMY_NODES: List[Dict[str, str]] = load_taxonomy_nodes(str(TAXONOMY_CONFIG_PATH))
TAXONOMY_BY_ID: Dict[str, Dict[str, str]] = taxonomy_by_id(str(TAXONOMY_CONFIG_PATH))
VALID_TAXONOMY_IDS = valid_taxonomy_ids(str(TAXONOMY_CONFIG_PATH))
TAXONOMY_TEXT_BLOCK = taxonomy_block_for_prompt(str(TAXONOMY_CONFIG_PATH))


def reload_taxonomy(config_path: Optional[Path] = None) -> None:
    """Reload taxonomy globals from YAML (for CLI --taxonomy-config)."""
    global TAXONOMY_CONFIG_PATH, TAXONOMY_NODES, TAXONOMY_BY_ID, VALID_TAXONOMY_IDS, TAXONOMY_TEXT_BLOCK
    path = config_path or DEFAULT_TAXONOMY_PATH
    TAXONOMY_CONFIG_PATH = path
    TAXONOMY_NODES = load_taxonomy_nodes(str(path))
    TAXONOMY_BY_ID = taxonomy_by_id(str(path))
    VALID_TAXONOMY_IDS = valid_taxonomy_ids(str(path))
    TAXONOMY_TEXT_BLOCK = taxonomy_block_for_prompt(str(path))


# ---------------------------------------------------------------------------
# Prompts (v1 legacy + v2 default via prompts package)
# ---------------------------------------------------------------------------

def get_taxonomy_prompts(prompt_version: str = DEFAULT_PROMPT_VERSION) -> tuple[str, str]:
    return load_taxonomy_prompts(prompt_version, taxonomy_path=TAXONOMY_CONFIG_PATH)


def _format_representations(representations: Any) -> str:
    if not isinstance(representations, dict):
        return "(none)"
    lines = []
    for name in ("KeyBERT", "MMR", "POS", "Main"):
        words = representations.get(name)
        if isinstance(words, list) and words:
            lines.append(f"{name}: {', '.join(str(w) for w in words)}")
    return "\n".join(lines) if lines else "(none)"


def build_user_prompt(
    *,
    topic_id: int,
    topic_metadata: Dict[str, Any],
    snippets_block: str,
    prompt_version: str = DEFAULT_PROMPT_VERSION,
) -> str:
    from src.stage08_llm_labeling.v3_derived_fields import enrich_v3_metadata_for_stage09

    _, user_template = get_taxonomy_prompts(prompt_version)
    topic_metadata = enrich_v3_metadata_for_stage09(topic_metadata)
    keywords = topic_metadata.get("keywords", [])
    all_keywords = topic_metadata.get("all_keywords", []) or keywords
    primary_categories = topic_metadata.get("primary_categories", [])
    secondary_categories = topic_metadata.get("secondary_categories", [])
    subgenre_hints = topic_metadata.get("subgenre_hints", []) or []

    format_kwargs = {
        "topic_id": topic_id,
        "keywords": ", ".join(keywords) if keywords else "(no keywords)",
        "label": topic_metadata.get("label") or "(no label)",
        "scene_summary": topic_metadata.get("scene_summary") or "(no scene summary)",
        "primary_categories": ", ".join(primary_categories) if primary_categories else "(none)",
        "secondary_categories": ", ".join(secondary_categories) if secondary_categories else "(none)",
        "content_type": topic_metadata.get("content_type", "(unknown)"),
        "exclude_from_axes": topic_metadata.get("exclude_from_axes", False),
        "subgenre_hints": ", ".join(subgenre_hints) if subgenre_hints else "(none)",
        "register": topic_metadata.get("register", "neutral"),
        "sexual_explicitness": topic_metadata.get("sexual_explicitness", "(none)"),
        "sexual_function": topic_metadata.get("sexual_function", "(none)"),
        "consent_status": topic_metadata.get("consent_status", "(not_applicable)"),
        "axis_hint": topic_metadata.get("axis_hint", "(none)"),
        "snippets": snippets_block,
    }
    if prompt_version.lower().startswith("v2"):
        format_kwargs.update({
            "all_keywords": ", ".join(all_keywords) if all_keywords else "(no keywords)",
            "representations": _format_representations(topic_metadata.get("representations")),
            "label_rationale": topic_metadata.get("rationale") or "(no Stage 08 rationale)",
            "stage07_exclude_from_axes": topic_metadata.get("stage07_exclude_from_axes", "(none)"),
            "stage07_posthoc_reason": topic_metadata.get("stage07_posthoc_reason", "(none)"),
            "stage07_content_type": topic_metadata.get("stage07_content_type", "(none)"),
        })
    return user_template.format(**format_kwargs)


# Backward-compatible names for dry-run / external imports
TAXONOMY_ZEROSHOT_SYSTEM_PROMPT, TAXONOMY_ZEROSHOT_USER_PROMPT = get_taxonomy_prompts("v1")


# ---------------------------------------------------------------------------
# Core function: classify a single topic into the taxonomy
# ---------------------------------------------------------------------------


def _finalize_taxonomy_result(
    result: Dict[str, Any],
    topic_metadata: Dict[str, Any],
) -> Dict[str, Any]:
    """Apply heuristics, enrich names, and propagate Stage 08 axis flags."""
    taxonomy_path = str(TAXONOMY_CONFIG_PATH)
    result = apply_domain_heuristics(result, topic_metadata, taxonomy_path)
    result = enrich_with_category_names(result, taxonomy_path)
    if "exclude_from_axes" not in result:
        result["exclude_from_axes"] = bool(topic_metadata.get("exclude_from_axes", False))
    return result


def _snapshot_mapping_fields(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "main_category_id": result.get("main_category_id"),
        "secondary_category_id": result.get("secondary_category_id"),
        "rationale": result.get("rationale"),
        "mapping_reasoning": result.get("mapping_reasoning"),
        "use_in_macro_axes": result.get("use_in_macro_axes"),
        "mechanic_tags": list(result.get("mechanic_tags") or []),
    }


def _attach_mapping_debug(
    result: Dict[str, Any],
    *,
    topic_metadata: Dict[str, Any],
    model_name: str,
    prompt_version: str,
    classification_source: str,
    llm_snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Attach structured debug trace for taxonomy mapping review."""
    from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
        load_taxonomy_config,
    )

    adjustments = result.pop("heuristic_adjustments", [])
    debug: Dict[str, Any] = {
        "classification_source": classification_source,
        "model_name": model_name,
        "prompt_version": prompt_version,
        "taxonomy_version": load_taxonomy_config(str(TAXONOMY_CONFIG_PATH)).get("version"),
        "stage08_label_rationale": topic_metadata.get("rationale"),
        "llm_rationale": (llm_snapshot or {}).get("rationale", result.get("rationale")),
        "llm_mapping_reasoning": (llm_snapshot or {}).get(
            "mapping_reasoning", result.get("mapping_reasoning")
        ),
        "heuristic_adjustments": adjustments,
    }
    if llm_snapshot and (
        llm_snapshot.get("main_category_id") != result.get("main_category_id")
        or llm_snapshot.get("secondary_category_id") != result.get("secondary_category_id")
        or llm_snapshot.get("use_in_macro_axes") != result.get("use_in_macro_axes")
    ):
        debug["before_heuristics"] = llm_snapshot
    result["mapping_debug"] = debug
    return result


def classify_topic_to_taxonomy_openrouter(
    *,
    topic_id: int,
    topic_metadata: Dict[str, Any],
    client: OpenAI,
    model_name: str,
    temperature: float = 0.0,
    max_new_tokens: int = 700,
    representative_docs: Optional[List[str]] = None,
    max_snippets: int = 8,
    max_chars_per_snippet: int = 400,
    prompt_version: str = DEFAULT_PROMPT_VERSION,
) -> Dict[str, Any]:
    """Classify a single BERTopic topic into the Romance Corpus Topic Taxonomy."""
    taxonomy_path = str(TAXONOMY_CONFIG_PATH)
    valid_ids = VALID_TAXONOMY_IDS
    use_v2 = prompt_version.lower().startswith("v2")

    pre_routed = try_pre_route_taxonomy(topic_id, topic_metadata, taxonomy_path)
    if pre_routed is not None:
        if use_v2:
            pre_routed = normalize_taxonomy_mapping_result(
                pre_routed,
                topic_id=topic_id,
                topic_metadata=topic_metadata,
                valid_ids=valid_ids,
                prompt_version=prompt_version,
            )
        result = _finalize_taxonomy_result(pre_routed, topic_metadata)
        result = _attach_mapping_debug(
            result,
            topic_metadata=topic_metadata,
            model_name=model_name,
            prompt_version=prompt_version,
            classification_source="pre_router",
        )
        LOGGER.info(
            "Topic %d pre-routed → main=%s (%s), secondary=%s, noise=%s",
            topic_id,
            result.get("main_category_id"),
            result.get("main_category_name"),
            result.get("secondary_category_id"),
            result.get("is_noise"),
        )
        return result

    snippets_block = "(none)"
    if representative_docs:
        central_docs = rerank_snippets_centrality(representative_docs, top_k=max_snippets)
        formatted = format_snippets(
            central_docs,
            max_snippets=max_snippets,
            max_chars=max_chars_per_snippet,
            anonymize=True,
        )
        snippets_block = formatted if formatted else "(none)"

    system_prompt, _ = get_taxonomy_prompts(prompt_version)
    user_prompt = build_user_prompt(
        topic_id=topic_id,
        topic_metadata=topic_metadata,
        snippets_block=snippets_block,
        prompt_version=prompt_version,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    LOGGER.info("Classifying topic %d into taxonomy (%s)...", topic_id, model_name)

    schema = None
    if use_v2:
        schema = build_taxonomy_mapping_schema(taxonomy_path)

    def _call_api() -> Dict[str, Any]:
        if use_v2 and schema is not None:
            return chat_completions_json_schema(
                client,
                model=model_name,
                messages=messages,
                schema=schema,
                schema_name="romance_taxonomy_mapping",
                max_tokens=max_new_tokens,
                temperature=temperature,
                validate_fn=lambda parsed: validate_taxonomy_mapping_json(parsed, schema),
            )
        max_retries = 6
        base_delay = 15.0
        response = None
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    max_tokens=max_new_tokens,
                    temperature=temperature,
                    response_format={"type": "json_object"},
                )
                break
            except Exception as e:
                error_str = str(e).lower()
                is_rate_limit = "429" in error_str or "rate limit" in error_str
                if is_rate_limit and attempt < max_retries - 1:
                    delay = 300.0 if attempt == max_retries - 2 else base_delay * (2 ** attempt)
                    LOGGER.warning("Rate limit for topic %d; waiting %.1fs", topic_id, delay)
                    time.sleep(delay)
                else:
                    raise
        if not response or not response.choices:
            raise ValueError("Empty API response for taxonomy classification")
        return parse_json_object_content(response.choices[0].message.content.strip())

    max_retries = 6
    base_delay = 15.0
    for attempt in range(max_retries):
        try:
            raw = _call_api()
            break
        except Exception as e:
            error_str = str(e).lower()
            is_rate_limit = "429" in error_str or "rate limit" in error_str
            if is_rate_limit and attempt < max_retries - 1:
                delay = 300.0 if attempt == max_retries - 2 else base_delay * (2 ** attempt)
                LOGGER.warning("Rate limit for topic %d; waiting %.1fs", topic_id, delay)
                time.sleep(delay)
            else:
                raise

    if use_v2:
        result = normalize_taxonomy_mapping_result(
            raw,
            topic_id=topic_id,
            topic_metadata=topic_metadata,
            valid_ids=valid_ids,
            prompt_version=prompt_version,
        )
    else:
        result = _normalize_v1_result(raw, topic_id, topic_metadata, valid_ids)

    llm_snapshot = _snapshot_mapping_fields(result) if use_v2 else None
    result = _finalize_taxonomy_result(result, topic_metadata)
    result = _attach_mapping_debug(
        result,
        topic_metadata=topic_metadata,
        model_name=model_name,
        prompt_version=prompt_version,
        classification_source="llm",
        llm_snapshot=llm_snapshot,
    )

    conf_display = result.get("confidence_band", result.get("confidence"))
    LOGGER.info(
        "Topic %d → main=%s (%s), secondary=%s (%s), noise=%s, confidence=%s",
        topic_id,
        result.get("main_category_id"),
        result.get("main_category_name"),
        result.get("secondary_category_id"),
        result.get("secondary_category_name"),
        result.get("is_noise"),
        conf_display,
    )
    return result


def _normalize_v1_result(
    raw: Dict[str, Any],
    topic_id: int,
    topic_metadata: Dict[str, Any],
    valid_ids: Set[str],
) -> Dict[str, Any]:
    """Legacy v1 post-parse normalization (string confidence)."""
    result = dict(raw)
    result["topic_id"] = topic_id
    primary_categories = topic_metadata.get("primary_categories", []) or []
    prev_is_noise = topic_metadata.get("is_noise", False)

    is_noise = bool(result.get("is_noise", False))
    if is_noise:
        result["main_category_id"] = "noise"
        result["secondary_category_id"] = None
    else:
        main_id = result.get("main_category_id")
        if not main_id or main_id not in valid_ids or main_id == "noise":
            if prev_is_noise:
                result["main_category_id"] = "noise"
                result["secondary_category_id"] = None
                result["is_noise"] = True
            else:
                result["main_category_id"] = fallback_main_category(primary_categories)
                result["is_noise"] = False
        sec_id = result.get("secondary_category_id")
        if sec_id is not None and sec_id not in valid_ids:
            result["secondary_category_id"] = None

    confidence = result.get("confidence", "medium")
    if not isinstance(confidence, str) or confidence.lower() not in {"low", "medium", "high"}:
        confidence = "medium" if is_noise else "low"
    result["confidence"] = confidence.lower()
    return result


# ---------------------------------------------------------------------------
# 5. Batch mapping utility: map all topics from a labels JSON file
# ---------------------------------------------------------------------------

def load_topic_metadata(labels_json_path: Path) -> Dict[int, Dict[str, Any]]:
    """
    Load Stage 08 topic metadata JSON (labels + keywords + categories etc.)
    and convert keys to int.
    """
    with open(labels_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta: Dict[int, Dict[str, Any]] = {}
    for k, v in data.items():
        try:
            tid = int(k)
        except ValueError:
            continue
        meta[tid] = v
    return meta


def load_bertopic_model_for_snippets(
    *,
    base_dir: Path = DEFAULT_BASE_DIR,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    model_suffix: str = "_with_llm_labels",
    stage_subfolder: Optional[str] = "stage08_llm_labeling",
    max_docs_per_topic: int = 10,
) -> Optional[Dict[int, List[str]]]:
    """
    Load BERTopic model and extract representative documents for snippets.
    
    Parameters
    ----------
    base_dir:
        Base directory for models (default: models/retrained).
    embedding_model:
        Embedding model name (default: paraphrase-MiniLM-L6-v2).
    model_suffix:
        Model suffix (default: "_with_llm_labels").
    stage_subfolder:
        Optional stage subfolder (default: "stage08_llm_labeling").
    max_docs_per_topic:
        Maximum number of representative docs to extract per topic.
        
    Returns
    -------
    Dict mapping topic_id to list of representative document strings, or None if loading fails.
    """
    try:
        LOGGER.info("Loading BERTopic model for representative document extraction...")
        LOGGER.info("  Base dir: %s", base_dir)
        LOGGER.info("  Embedding model: %s", embedding_model)
        LOGGER.info("  Model suffix: %s", model_suffix)
        LOGGER.info("  Stage subfolder: %s", stage_subfolder)
        
        topic_model = load_native_bertopic_model(
            base_dir=base_dir,
            embedding_model=embedding_model,
            pareto_rank=1,
            model_suffix=model_suffix,
            stage_subfolder=stage_subfolder,
        )
        
        LOGGER.info("✓ BERTopic model loaded successfully")
        
        # Extract representative documents
        LOGGER.info("Extracting representative documents from model...")
        topic_to_snippets = extract_representative_docs_per_topic(
            topic_model,
            max_docs_per_topic=max_docs_per_topic,
        )
        
        snippets_count = len([tid for tid, docs in topic_to_snippets.items() if docs])
        avg_snippets = (
            sum(len(docs) for docs in topic_to_snippets.values()) / max(snippets_count, 1)
        )
        LOGGER.info(
            "✓ Extracted representative docs for %d topics (avg %.1f docs per topic)",
            snippets_count,
            avg_snippets,
        )
        
        return topic_to_snippets
        
    except Exception as e:
        LOGGER.warning(
            "Failed to load BERTopic model or extract snippets: %s. "
            "Taxonomy classification will proceed without representative snippets.",
            e,
        )
        return None


def map_all_topics_to_taxonomy(
    *,
    labels_json_path: Path,
    output_path: Path,
    client: Optional[OpenAI] = None,
    model_name: str = STAGE09_DEFAULT_MODEL,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    max_new_tokens: int = 700,
    prompt_version: str = DEFAULT_PROMPT_VERSION,
    topic_to_snippets: Optional[Dict[int, List[str]]] = None,
    # Model loading parameters for snippet extraction
    load_model_for_snippets: bool = True,
    base_dir: Path = DEFAULT_BASE_DIR,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    model_suffix: str = "_with_llm_labels",
    stage_subfolder: Optional[str] = "stage08_llm_labeling",
    max_docs_per_topic: int = 10,
    limit_topics: Optional[int] = None,
    include_source_metadata: bool = False,
) -> Dict[int, Dict[str, Any]]:
    """
    Run zero-shot taxonomy mapping for all topics that have LLM labels.

    Parameters
    ----------
    labels_json_path:
        Path to Stage 08 labels JSON (as produced by generate_labels_openrouter.save_labels_openrouter).
    output_path:
        Path to write taxonomy mapping JSON (topic_id → mapping dict).
    client:
        Optional existing OpenRouter client. If None, a new one is created via load_openrouter_client.
    model_name:
        Model name for classification.
    api_key:
        Optional API key (if client is None). If None, environment variable is used.
    temperature, max_new_tokens:
        Generation params.
    topic_to_snippets:
        Optional dict[topic_id → list[str]] of representative docs.
        If None and load_model_for_snippets=True, will attempt to load from BERTopic model.
    load_model_for_snippets:
        If True and topic_to_snippets is None, load BERTopic model and extract snippets.
    base_dir, embedding_model, model_suffix, stage_subfolder:
        Parameters for loading BERTopic model (used if load_model_for_snippets=True).
    max_docs_per_topic:
        Maximum number of representative docs to extract per topic.
    include_source_metadata:
        If True, include original metadata from labels JSON (keywords, label, primary_categories,
        secondary_categories, scene_summary, label_rationale) in the output for manual evaluation.

    Returns
    -------
    Dict[int, Dict[str, Any]] mapping topic_id → taxonomy mapping.
    """
    # Initialize client if needed
    if client is None:
        client, _ = load_openrouter_client(
            api_key=api_key or "",
            model_name=model_name,
        )

    # Load topic metadata
    topic_meta = load_topic_metadata(labels_json_path)
    topic_ids = sorted(topic_meta.keys())
    total = len(topic_ids)
    LOGGER.info("Loaded metadata for %d topics from %s", total, labels_json_path)
    
    # Apply limit if specified (for testing)
    if limit_topics is not None and limit_topics > 0:
        topic_ids = topic_ids[:limit_topics]
        total = len(topic_ids)
        LOGGER.info("Limited to first %d topics for testing", limit_topics)

    # Load snippets from BERTopic model if requested and not provided
    if topic_to_snippets is None and load_model_for_snippets:
        LOGGER.info("Loading BERTopic model to extract representative documents...")
        topic_to_snippets = load_bertopic_model_for_snippets(
            base_dir=base_dir,
            embedding_model=embedding_model,
            model_suffix=model_suffix,
            stage_subfolder=stage_subfolder,
            max_docs_per_topic=max_docs_per_topic,
        )
        if topic_to_snippets:
            LOGGER.info(
                "Using representative snippets from BERTopic model for taxonomy classification"
            )
        else:
            LOGGER.info("Proceeding without representative snippets")
    elif topic_to_snippets is None:
        LOGGER.info("No representative snippets provided, using keywords and labels only")

    # Try to load existing checkpoint if output file exists
    taxonomy_map: Dict[int, Dict[str, Any]] = {}
    if output_path.exists():
        LOGGER.info("Found existing output file. Loading checkpoint to resume...")
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            for k, v in existing_data.items():
                try:
                    tid = int(k)
                    taxonomy_map[tid] = v
                except ValueError:
                    continue
            LOGGER.info("Loaded %d topics from checkpoint", len(taxonomy_map))
        except Exception as e:
            LOGGER.warning("Failed to load checkpoint: %s. Starting fresh.", e)
            taxonomy_map = {}

    # Filter out already processed topics
    remaining_topics = [tid for tid in topic_ids if tid not in taxonomy_map]
    if len(remaining_topics) < len(topic_ids):
        LOGGER.info(
            "Resuming: %d topics already processed, %d remaining",
            len(taxonomy_map),
            len(remaining_topics),
        )
    else:
        LOGGER.info("Starting fresh: processing all %d topics", len(topic_ids))

    for idx, tid in enumerate(remaining_topics, start=1):
        tm = topic_meta[tid]
        snippets = topic_to_snippets.get(tid, []) if topic_to_snippets else None
        if not snippets:
            embedded = tm.get("snippets")
            if isinstance(embedded, list) and embedded:
                snippets = embedded
        
        try:
            result = classify_topic_to_taxonomy_openrouter(
                topic_id=tid,
                topic_metadata=tm,
                client=client,
                model_name=model_name,
                temperature=temperature,
                max_new_tokens=max_new_tokens,
                representative_docs=snippets,
                prompt_version=prompt_version,
            )
        except Exception as e:
            LOGGER.error(
                "Failed to classify topic %d after retries: %s. Saving checkpoint and exiting.",
                tid, e
            )
            # Save checkpoint before exiting
            output_path.parent.mkdir(parents=True, exist_ok=True)
            serializable = {str(k): v for k, v in taxonomy_map.items()}
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2, ensure_ascii=False)
            LOGGER.info("Checkpoint saved. Resume by running the same command again.")
            raise
        
        # Optionally include source metadata from labels JSON for manual evaluation
        if include_source_metadata:
            result["source_metadata"] = {
                "label": tm.get("label", ""),
                "keywords": tm.get("keywords", []),
                "all_keywords": tm.get("all_keywords", []),
                "representations": tm.get("representations", {}),
                "snippets": tm.get("snippets", []),
                "primary_categories": tm.get("primary_categories", []),
                "secondary_categories": tm.get("secondary_categories", []),
                "scene_summary": tm.get("scene_summary", ""),
                "label_rationale": tm.get("rationale", ""),
            }
        
        taxonomy_map[tid] = result

        # Delay to avoid rate limits (10 seconds between requests for Mistral-Nemo)
        # Mistral-Nemo has very strict rate limits, so we need longer delays
        if idx < len(remaining_topics):
            time.sleep(10.0)

        # Save checkpoint every 10 topics
        if idx % 10 == 0 or idx == len(remaining_topics):
            output_path.parent.mkdir(parents=True, exist_ok=True)
            serializable = {str(k): v for k, v in taxonomy_map.items()}
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2, ensure_ascii=False)
            LOGGER.info(
                "Processed %d/%d remaining topics (%.1f%%). Checkpoint saved.",
                idx, len(remaining_topics), idx / len(remaining_topics) * 100.0
            )

    # Final save (already saved during checkpointing, but ensure it's up to date)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {str(k): v for k, v in taxonomy_map.items()}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)

    LOGGER.info(
        "✓ Completed! Saved taxonomy mappings for %d topics to %s", len(serializable), output_path
    )
    return taxonomy_map


def update_model_with_taxonomy_mappings(
    *,
    taxonomy_json_path: Path,
    base_dir: Path = DEFAULT_BASE_DIR,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    model_suffix: str = "_with_llm_labels",
    source_stage_subfolder: str = "stage08_llm_labeling",
    target_stage_subfolder: str = "stage09_category_mapping",
    target_model_suffix: str = "_with_taxonomy_mappings",
) -> Path:
    """
    Load BERTopic model, attach taxonomy mappings, and save to new location.
    
    Parameters
    ----------
    taxonomy_json_path:
        Path to taxonomy mappings JSON file.
    base_dir:
        Base directory for models.
    embedding_model:
        Embedding model name.
    model_suffix:
        Suffix of source model to load.
    source_stage_subfolder:
        Stage subfolder where source model is located.
    target_stage_subfolder:
        Stage subfolder where updated model will be saved.
    target_model_suffix:
        Suffix for the updated model.
        
    Returns
    -------
    Path to the saved model directory.
    """
    LOGGER.info("Loading taxonomy mappings from %s", taxonomy_json_path)
    with open(taxonomy_json_path, "r", encoding="utf-8") as f:
        taxonomy_data = json.load(f)
    
    # Convert string keys to int
    taxonomy_map: Dict[int, Dict[str, Any]] = {}
    for k, v in taxonomy_data.items():
        try:
            tid = int(k)
            taxonomy_map[tid] = v
        except ValueError:
            continue
    
    LOGGER.info("Loaded taxonomy mappings for %d topics", len(taxonomy_map))
    
    # Load source model
    LOGGER.info("Loading source BERTopic model...")
    LOGGER.info("  Base dir: %s", base_dir)
    LOGGER.info("  Embedding model: %s", embedding_model)
    LOGGER.info("  Model suffix: %s", model_suffix)
    LOGGER.info("  Stage subfolder: %s", source_stage_subfolder)
    
    # Construct path with stage subfolder
    source_base_dir = base_dir / embedding_model / source_stage_subfolder
    
    topic_model = load_native_bertopic_model(
        base_dir=source_base_dir,
        embedding_model=".",  # Use "." to avoid path duplication
        pareto_rank=1,
        model_suffix=model_suffix,
    )
    
    LOGGER.info("✓ Source model loaded successfully")
    
    # Attach taxonomy mappings to model
    LOGGER.info("Attaching taxonomy mappings to model...")
    topic_model.topic_taxonomy_ = taxonomy_map
    LOGGER.info("✓ Taxonomy mappings attached to model.topic_taxonomy_")
    
    # Verify attachment
    if hasattr(topic_model, "topic_taxonomy_") and topic_model.topic_taxonomy_:
        LOGGER.info(
            "✓ Verified: taxonomy mappings attached for %d topics",
            len(topic_model.topic_taxonomy_)
        )
        # Log sample
        sample_topic = list(taxonomy_map.keys())[0]
        sample_data = taxonomy_map[sample_topic]
        LOGGER.info(
            "  Sample taxonomy keys for topic %d: %s",
            sample_topic,
            list(sample_data.keys())[:10],  # First 10 keys
        )
    else:
        LOGGER.warning("⚠ Taxonomy mappings may not have been attached correctly")
    
    # Save model to target location
    target_dir = base_dir / embedding_model / target_stage_subfolder
    target_dir.mkdir(parents=True, exist_ok=True)
    
    model_dir = target_dir / f"model_1{target_model_suffix}"
    
    # Remove existing directory if it exists
    if model_dir.exists() and model_dir.is_dir():
        LOGGER.info("Removing existing model directory: %s", model_dir)
        shutil.rmtree(model_dir)
    
    LOGGER.info("Saving updated model to %s", model_dir)
    topic_model.save(str(model_dir))
    LOGGER.info("✓ Model saved successfully to %s", model_dir)
    
    return model_dir


if __name__ == "__main__":
    import argparse
    import os

    from src.stage03_train.embeddings_hub import load_project_dotenv

    load_project_dotenv()

    parser = argparse.ArgumentParser(
        description="Stage 09: Zero-shot taxonomy mapping of BERTopic topics using Mistral via OpenRouter.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--labels-json",
        type=Path,
        required=True,
        help="Path to Stage 08 labels JSON (labels_pos_openrouter_..._romance_aware_*.json).",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        required=True,
        help="Where to save taxonomy mappings JSON.",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=STAGE09_DEFAULT_MODEL,
        help="OpenRouter model name to use.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="",
        help="OpenRouter API key (optional; otherwise environment variable is used).",
    )
    parser.add_argument(
        "--prompt-version",
        type=str,
        default=DEFAULT_PROMPT_VERSION,
        help="Taxonomy prompt version (v2 default; v1 for legacy).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature (0.0 recommended for classification).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=900,
        help="Maximum new tokens for JSON output.",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=DEFAULT_BASE_DIR,
        help="Base directory for BERTopic models (default: models/retrained).",
    )
    parser.add_argument(
        "--embedding-model",
        type=str,
        default=DEFAULT_EMBEDDING_MODEL,
        help="Embedding model name (default: paraphrase-MiniLM-L6-v2).",
    )
    parser.add_argument(
        "--model-suffix",
        type=str,
        default="_with_llm_labels",
        help="Model suffix (default: _with_llm_labels).",
    )
    parser.add_argument(
        "--model-stage",
        type=str,
        default="stage08_llm_labeling",
        help="Stage subfolder for model (default: stage08_llm_labeling).",
    )
    parser.add_argument(
        "--max-docs-per-topic",
        type=int,
        default=10,
        help="Maximum number of representative docs to extract per topic (default: 10).",
    )
    parser.add_argument(
        "--no-snippets",
        action="store_true",
        help="Skip loading BERTopic model and extracting representative snippets.",
    )
    parser.add_argument(
        "--limit-topics",
        type=int,
        default=None,
        help="Limit processing to first N topics (for testing, default: process all).",
    )
    parser.add_argument(
        "--taxonomy-config",
        type=Path,
        default=DEFAULT_TAXONOMY_PATH,
        help="Path to romance_corpus_taxonomy_v2.yaml.",
    )
    parser.add_argument(
        "--include-source-metadata",
        action="store_true",
        help="Include original metadata from labels JSON (keywords, label, categories, scene_summary, label_rationale) in output. Useful for manual evaluation of first N topics.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call the API, just print the first user prompt and exit.",
    )
    parser.add_argument(
        "--save-model",
        action="store_true",
        help="After taxonomy mapping, update and save the BERTopic model with taxonomy mappings.",
    )
    parser.add_argument(
        "--target-model-suffix",
        type=str,
        default="_with_taxonomy_mappings",
        help="Suffix for the saved model (default: _with_taxonomy_mappings).",
    )

    args = parser.parse_args()

    # Set log level
    logging.getLogger().setLevel(args.log_level)
    reload_taxonomy(args.taxonomy_config)

    # Handle dry-run mode
    if args.dry_run:
        meta = load_topic_metadata(args.labels_json)
        first_tid = sorted(meta.keys())[0]
        tm = meta[first_tid]
        system_prompt, _ = get_taxonomy_prompts(args.prompt_version)
        user_prompt = build_user_prompt(
            topic_id=first_tid,
            topic_metadata=tm,
            snippets_block="(none)",
            prompt_version=args.prompt_version,
        )
        print("=== SYSTEM PROMPT ===")
        print(system_prompt)
        print("\n=== USER PROMPT (topic", first_tid, ") ===")
        print(user_prompt)
        raise SystemExit(0)

    client, _ = load_openrouter_client(
        api_key=args.api_key or os.environ.get("OPENROUTER_API_KEY", ""),
        model_name=args.model_name,
    )

    map_all_topics_to_taxonomy(
        labels_json_path=args.labels_json,
        output_path=args.output_json,
        client=client,
        model_name=args.model_name,
        temperature=args.temperature,
        max_new_tokens=args.max_tokens,
        prompt_version=args.prompt_version,
        load_model_for_snippets=not args.no_snippets,
        base_dir=args.base_dir,
        embedding_model=args.embedding_model,
        model_suffix=args.model_suffix,
        stage_subfolder=args.model_stage,
        max_docs_per_topic=args.max_docs_per_topic,
        limit_topics=args.limit_topics,
        include_source_metadata=args.include_source_metadata,
    )
    
    # Update and save model if requested
    if args.save_model:
        LOGGER.info("\n" + "=" * 80)
        LOGGER.info("Updating BERTopic model with taxonomy mappings")
        LOGGER.info("=" * 80)
        model_path = update_model_with_taxonomy_mappings(
            taxonomy_json_path=args.output_json,
            base_dir=args.base_dir,
            embedding_model=args.embedding_model,
            model_suffix=args.model_suffix,
            source_stage_subfolder=args.model_stage,
            target_stage_subfolder="stage09_category_mapping",
            target_model_suffix=args.target_model_suffix,
        )
        LOGGER.info("✓ Model update complete. Saved to: %s", model_path)

