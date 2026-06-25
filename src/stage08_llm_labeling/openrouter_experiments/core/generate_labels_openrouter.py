"""Stage 08 utilities for generating topic labels using OpenRouter API (mistralai/mistral-nemo) from POS representation keywords."""

from __future__ import annotations

import csv
import json
import logging
import os
import re
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import numpy as np
from bertopic import BERTopic
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Import shared utilities from parent module
from src.stage08_llm_labeling.generate_labels import (
    detect_domains,
    extract_pos_topics,
    extract_pos_topics_from_json,
    integrate_labels_to_bertopic,
    load_bertopic_model,
    log_batch_progress,
    make_context_hints,
    rerank_keywords_mmr,
    stage_timer_local,
)

LOGGER = logging.getLogger("stage08_llm_labeling.openrouter")

from src.stage08_llm_labeling.labeling_pipeline import (
    clean_scene_summary_text,
    normalize_label_text,
)
from src.stage08_llm_labeling.prompts.v1_scene_only import (
    ROMANCE_AWARE_SYSTEM_PROMPT,
    ROMANCE_AWARE_USER_PROMPT,
)

DEFAULT_RATE_LIMIT_DELAY_S = 4.0



# OpenRouter API configuration
# Preferred: set OPENROUTER_API_KEY in your environment.
# You can still override with --api-key on the CLI.
DEFAULT_OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
# OpenRouter uses an OpenAI-compatible /v1 endpoint
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# Default model for production romance/erotica topic labelling.
# You can override this via --model-name on the CLI.
DEFAULT_OPENROUTER_MODEL = "mistralai/Mistral-Nemo-Instruct-2407"
# Curated set of literary / roleplay-oriented models you might want to try.
# These are all accessed via the same OpenRouter API key.
ROLEPLAY_LITERARY_MODELS: dict[str, str] = {
    # General-purpose Nemo Instruct (good reasoning + instruction following)
    "nemo_instruct_2407": "mistralai/Mistral-Nemo-Instruct-2407",
    # Story-writing / roleplay model based on Nemo (very "literary" prose)
    "nemo_celeste": "nothingiisreal/mn-celeste-12b",
    # Gutenberg-tuned Nemo trained on book-like data (strong for fiction)
    "nemo_gutenberg_v2": "nbeerbower/mistral-nemo-gutenberg-12B-v2",
    # Alias for clarity
    "nemo_instruct": "mistralai/Mistral-Nemo-Instruct-2407",
}

# Module-level cache for MMR embedding model (loaded once, reused for all topics)
_MMR_EMBEDDING_MODEL: SentenceTransformer | None = None

# Module-level cache for spaCy NLP model (loaded once, reused for all topics)
_SPACY_NLP = None

try:
    import spacy

    SPACY_AVAILABLE = True
except ImportError:
    spacy = None  # type: ignore[assignment]
    SPACY_AVAILABLE = False


def _get_embedding_model() -> SentenceTransformer:
    """Load (or reuse) a sentence embedding model for snippet centrality."""
    global _MMR_EMBEDDING_MODEL
    if _MMR_EMBEDDING_MODEL is None:
        LOGGER.info("Loading SentenceTransformer model for snippet centrality...")
        _MMR_EMBEDDING_MODEL = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    return _MMR_EMBEDDING_MODEL


def rerank_snippets_centrality(
    docs: list[str],
    top_k: int,
) -> list[str]:
    """
    Rerank representative docs by semantic centrality.

    - Embed each sentence.
    - Compute centroid (mean embedding).
    - Rank by cosine similarity to centroid.
    - Return top_k most central sentences.
    """
    if not docs:
        return []
    model = _get_embedding_model()
    embeddings = model.encode(docs, normalize_embeddings=True)
    if len(embeddings) == 0:
        return docs[:top_k]
    centroid = embeddings.mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm == 0.0:
        return docs[:top_k]
    centroid = centroid / norm
    sims = embeddings @ centroid  # cosine similarity (normalized)
    indices = np.argsort(-sims)[:top_k]
    return [docs[i] for i in indices]


def _load_spacy_model(enable_ner: bool = False):
    """Load spaCy model for POS tagging or NER (cached).
    
    Note: If model was previously loaded without NER and NER is now requested,
    the model will be reloaded with NER enabled. This means:
    - First call (e.g., from extract_pos_cues) loads model without NER (faster for POS)
    - Later call (e.g., from format_snippets with anonymize=True) reloads with NER
    This is a reasonable trade-off for simplicity, but not "free" - the model loads twice.
    
    Args:
        enable_ner: If True, enable NER component (needed for name anonymization)
    """
    global _SPACY_NLP
    if _SPACY_NLP is None and SPACY_AVAILABLE:
        try:
            if enable_ner:
                # Load with NER enabled for name anonymization
                _SPACY_NLP = spacy.load("en_core_web_sm", disable=["parser"])
            else:
                # Load with NER disabled for POS tagging (faster)
                _SPACY_NLP = spacy.load("en_core_web_sm", disable=["ner", "parser"])
            LOGGER.info("Loaded spaCy model for %s", "NER and POS tagging" if enable_ner else "POS tagging")
        except OSError:
            LOGGER.warning("spaCy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
            return None
    elif _SPACY_NLP is not None and enable_ner and "ner" not in _SPACY_NLP.pipe_names:
        # Reload model with NER enabled if it was previously loaded without NER
        try:
            _SPACY_NLP = spacy.load("en_core_web_sm", disable=["parser"])
            LOGGER.info("Reloaded spaCy model with NER enabled")
        except Exception as e:
            LOGGER.warning("Could not reload spaCy model with NER: %s", e)
    return _SPACY_NLP


def extract_pos_cues(keywords: list[str]) -> str:
    """
    Extract real POS cues from keywords using spaCy POS tagging for romance-aware labeling.
    
    Uses actual POS tagging from spaCy to categorize keywords into nouns, verbs, and adjectives.
    Falls back to simplified extraction if spaCy is not available.
    
    Args:
        keywords: List of keyword strings
        
    Returns:
        Formatted POS cues string (empty if no cues detected)
    """
    if not keywords:
        return ""
    
    nlp = _load_spacy_model()
    
    # Use real POS tagging if spaCy is available
    if nlp is not None:
        nouns = []
        verbs = []
        adjs = []
        
        # Process each keyword individually for better POS accuracy
        # (spaCy works better on individual words/phrases than joined text)
        for kw in keywords:
            if not kw or not kw.strip():
                continue
            
            # Process keyword with spaCy
            doc = nlp(kw)
            
            # Get POS tag from the first (and usually only) token
            # For multi-word keywords, use the head token or first significant token
            pos_tag = None
            for token in doc:
                # Skip punctuation and stop words for POS determination
                if not token.is_punct and not token.is_stop:
                    pos_tag = token.pos_
                    break
            
            # If no significant token found, use first token's POS
            if pos_tag is None and len(doc) > 0:
                pos_tag = doc[0].pos_
            
            # spaCy POS tags: NOUN, VERB, ADJ, etc.
            if pos_tag == "NOUN" or pos_tag == "PROPN":  # Noun or proper noun
                nouns.append(kw)
            elif pos_tag == "VERB":
                verbs.append(kw)
            elif pos_tag == "ADJ":  # Adjective
                adjs.append(kw)
        
        # Build POS cues string
        parts = []
        if nouns:
            parts.append(f"Nouns→{', '.join(nouns[:5])}")  # Limit to 5 for brevity
        if verbs:
            parts.append(f"Verbs→{', '.join(verbs[:5])}")
        if adjs:
            parts.append(f"Adjectives→{', '.join(adjs[:5])}")
        
        if parts:
            return "POS cues: " + "; ".join(parts) + "."
        return ""
    
    # Fallback: simplified extraction using domain knowledge
    # Common body part nouns (from domain lexicon)
    body_parts = {
        "lip", "lips", "mouth", "tongue", "teeth", "cheek", "cheeks", "nose", "chin",
        "brows", "eyebrow", "eyebrows", "eye", "eyes", "neck", "nape", "shoulder",
        "shoulders", "arm", "arms", "hand", "hands", "finger", "fingers", "fist",
        "fists", "breast", "breasts", "nipples", "waist", "belly", "stomach", "chest",
        "spine", "back", "hip", "hips", "thigh", "thighs", "legs", "leg", "knee",
        "knees", "feet", "foot", "heels", "clit", "clitoris", "pussy", "genitals",
    }
    
    # Common touch/intimacy verbs
    touch_verbs = {
        "kiss", "kissed", "kissing", "touch", "touched", "touching", "caress", "caressed",
        "cup", "cupped", "grab", "grabbed", "grasp", "grasped", "hold", "held", "hug",
        "hugged", "embrace", "embraced", "stroke", "stroked", "rub", "rubbed", "squeeze",
        "squeezed", "pinch", "pinched", "lick", "licked", "suck", "sucked", "bite",
        "bit", "nibble", "nibbled",
    }
    
    # Common emotional/adjective words
    adjectives = {
        "tender", "gentle", "soft", "hard", "rough", "smooth", "warm", "cold", "hot",
        "sweet", "bitter", "sour", "intense", "passionate", "romantic", "loving",
        "affectionate", "desperate", "urgent", "slow", "fast", "deep", "shallow",
    }
    
    nouns = []
    verbs = []
    adjs = []
    
    keywords_lower = [kw.lower() for kw in keywords]
    
    for kw in keywords_lower:
        if kw in body_parts:
            nouns.append(kw)
        elif kw in touch_verbs:
            verbs.append(kw)
        elif kw in adjectives:
            adjs.append(kw)
    
    # Build POS cues string
    parts = []
    if nouns:
        parts.append(f"Nouns→{', '.join(nouns[:5])}")  # Limit to 5 for brevity
    if verbs:
        parts.append(f"Verbs→{', '.join(verbs[:5])}")
    if adjs:
        parts.append(f"Adjectives→{', '.join(adjs[:5])}")
    
    if parts:
        return "POS cues: " + "; ".join(parts) + "."
    return ""


def anonymize_names(text: str, nlp) -> str:
    """
    Anonymize person and pet names in text by replacing them with generic role tokens.
    
    Uses spaCy NER to detect PERSON entities and replaces them with "[NAME]".
    This helps prevent the model from overfitting on specific character names in snippets.
    
    Args:
        text: Input text string
        nlp: spaCy language model (must have NER enabled)
        
    Returns:
        Text with person/pet names replaced by generic tokens
    """
    if not text or not nlp:
        return text
    
    try:
        # Check if NER is enabled
        if "ner" not in nlp.pipe_names:
            LOGGER.debug("NER not enabled in spaCy model, skipping anonymization")
            return text
        
        doc = nlp(text)
        if not doc.ents:
            return text
        
        result = text
        # Process entities in reverse order to preserve character indices
        # (process from end to start to avoid index shifting issues)
        entities = sorted(doc.ents, key=lambda e: e.start_char, reverse=True)
        
        for ent in entities:
            if ent.label_ in {"PERSON"}:
                # Replace with generic token
                # Could be fancier (e.g., detect role from context), but [NAME] is sufficient
                result = result[:ent.start_char] + "[NAME]" + result[ent.end_char:]
        
        return result
    except Exception as e:
        LOGGER.warning("Error anonymizing names in text: %s", e)
        return text  # Return original text on error


def format_snippets(
    docs: list[str],
    max_snippets: int = 15,
    max_chars: int = 1200,
    anonymize: bool = True,
) -> str:
    """
    Convert a list of documents into a bullet-style snippets block for LLM prompts.
    
    Formats representative document snippets as numbered quotes, with truncation
    for long sentences. Designed for sentence-level documents (each doc is a sentence).
    Optionally anonymizes person/pet names to prevent overfitting on specific characters.
    
    Args:
        docs: List of document strings (sentences in this corpus)
        max_snippets: Maximum number of snippets to include (default: 15)
        max_chars: Maximum characters per snippet before truncation (default: 1200)
        anonymize: If True, anonymize person/pet names using spaCy NER (default: True)
        
    Returns:
        Formatted string with numbered snippets, or empty string if no docs provided
    """
    if not docs:
        return ""
    
    # Load spaCy model for anonymization if requested
    nlp = None
    if anonymize and SPACY_AVAILABLE:
        nlp = _load_spacy_model(enable_ner=True)
    
    snippets = []
    for i, doc in enumerate(docs[:max_snippets], start=1):
        # Collapse whitespace
        s = " ".join(doc.split())
        
        # Anonymize names if requested and spaCy is available
        if anonymize and nlp is not None:
            s = anonymize_names(s, nlp)
        
        # Truncate at word boundary if too long
        if len(s) > max_chars:
            s = s[:max_chars].rsplit(" ", 1)[0] + "..."
        
        snippets.append(f'{i}) "{s}"')
    
    if not snippets:
        return ""
    
    return "Representative snippets (short excerpts for this topic):\n" + "\n".join(snippets)


def _topic_ids_from_model(topic_model: BERTopic) -> set[int]:
    """Collect non-outlier topic IDs from the best available model attribute."""
    aspects = getattr(topic_model, "topic_aspects_", None)
    if isinstance(aspects, dict) and aspects.get("POS"):
        ids = {int(k) for k in aspects["POS"].keys() if int(k) != -1}
        if ids:
            return ids

    representations = getattr(topic_model, "topic_representations_", None)
    if isinstance(representations, dict) and representations:
        return {int(k) for k in representations.keys() if int(k) != -1}

    topics = getattr(topic_model, "topics_", None)
    if topics is not None:
        return {int(t) for t in topics if int(t) != -1}

    return set()


def load_representative_docs_from_csv(
    csv_path: Path | str,
    max_docs_per_topic: int = 10,
) -> dict[int, list[str]]:
    """Load per-topic representative sentences exported by stage05 compare-fit."""
    path = Path(csv_path)
    if not path.is_file():
        LOGGER.warning("Representative docs CSV not found: %s", path)
        return {}

    topic_to_docs: dict[int, list[str]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                topic_id = int(row["topic"])
            except (KeyError, TypeError, ValueError):
                continue
            if topic_id == -1:
                continue
            sentence = (row.get("sentence") or "").strip()
            if not sentence:
                continue
            docs = topic_to_docs.setdefault(topic_id, [])
            if len(docs) < max_docs_per_topic:
                docs.append(sentence)

    LOGGER.info(
        "Loaded representative docs from CSV for %d topics (%s)",
        len(topic_to_docs),
        path,
    )
    return topic_to_docs


def extract_representative_docs_per_topic(
    topic_model: BERTopic,
    max_docs_per_topic: int = 10,
    fallback_csv: Path | str | None = None,
) -> dict[int, list[str]]:
    """
    Extract representative documents for each topic from BERTopic model.
    
    Tries get_representative_docs() method first, falls back to representative_docs_
    attribute. When the saved model has no rep docs (common for enriched exports),
    falls back to compare-fit ``representative_docs.csv``.
    
    Args:
        topic_model: BERTopic model instance
        max_docs_per_topic: Maximum number of representative docs to extract per topic
        fallback_csv: Optional CSV from stage05 compare-fit with topic/sentence columns
        
    Returns:
        Dictionary mapping topic_id to list of representative document strings
    """
    topic_ids = _topic_ids_from_model(topic_model)
    topic_to_docs: dict[int, list[str]] = {}
    if not topic_ids:
        LOGGER.warning("Cannot determine topic IDs from BERTopic model")
    else:
        LOGGER.info("Extracting representative documents for %d topics", len(topic_ids))
    
    # Try get_representative_docs() method first (newer BERTopic versions)
    if topic_ids and hasattr(topic_model, "get_representative_docs"):
        try:
            for topic_id in topic_ids:
                try:
                    rep_docs = topic_model.get_representative_docs(topic=topic_id)

                    if isinstance(rep_docs, dict):
                        if topic_id in rep_docs:
                            rep_docs = rep_docs[topic_id]
                        elif len(rep_docs) == 1:
                            rep_docs = list(rep_docs.values())[0]
                        else:
                            rep_docs = rep_docs.get(topic_id, [])
                    elif rep_docs is None:
                        rep_docs = []
                    elif not isinstance(rep_docs, list):
                        LOGGER.warning(
                            "Unexpected return type from get_representative_docs for topic %d: %s",
                            topic_id,
                            type(rep_docs),
                        )
                        rep_docs = []

                    if not isinstance(rep_docs, list):
                        rep_docs = [rep_docs] if rep_docs else []

                    if len(rep_docs) > max_docs_per_topic:
                        rep_docs = rep_docs[:max_docs_per_topic]

                    topic_to_docs[topic_id] = [str(doc) for doc in rep_docs if doc]
                except Exception as e:
                    LOGGER.warning(
                        "Error getting representative docs for topic %d via method: %s",
                        topic_id,
                        e,
                    )
                    topic_to_docs[topic_id] = []

            model_nonempty = len([tid for tid, docs in topic_to_docs.items() if docs])
            LOGGER.info(
                "Extracted representative docs via get_representative_docs() for %d topics",
                model_nonempty,
            )
            if model_nonempty:
                return topic_to_docs
        except Exception as e:
            LOGGER.warning(
                "get_representative_docs() method failed, falling back to attribute: %s",
                e,
            )

    # Fallback to representative_docs_ attribute
    if topic_ids and hasattr(topic_model, "representative_docs_"):
        try:
            rep_docs_attr = topic_model.representative_docs_

            if isinstance(rep_docs_attr, dict) and rep_docs_attr:
                for topic_id in topic_ids:
                    if topic_id in rep_docs_attr:
                        docs = rep_docs_attr[topic_id]
                        if isinstance(docs, list):
                            docs = [str(doc) for doc in docs[:max_docs_per_topic] if doc]
                        else:
                            docs = [str(docs)] if docs else []
                        topic_to_docs[topic_id] = docs
                    else:
                        topic_to_docs.setdefault(topic_id, [])

                model_nonempty = len([tid for tid, docs in topic_to_docs.items() if docs])
                LOGGER.info(
                    "Extracted representative docs via representative_docs_ for %d topics",
                    model_nonempty,
                )
                if model_nonempty:
                    return topic_to_docs
        except Exception as e:
            LOGGER.warning("Error accessing representative_docs_ attribute: %s", e)

    # Compare-fit CSV fallback (enriched models often omit representative_docs_)
    if fallback_csv:
        csv_docs = load_representative_docs_from_csv(
            fallback_csv,
            max_docs_per_topic=max_docs_per_topic,
        )
        if csv_docs:
            if not topic_to_docs:
                return csv_docs
            for topic_id, docs in csv_docs.items():
                if not topic_to_docs.get(topic_id):
                    topic_to_docs[topic_id] = docs
            LOGGER.info(
                "Filled %d topics from representative docs CSV fallback",
                len([tid for tid, docs in topic_to_docs.items() if docs]),
            )
            return topic_to_docs

    if not any(topic_to_docs.values()):
        LOGGER.warning(
            "Could not extract representative docs from BERTopic model. "
            "Labels will be generated from keywords only."
        )
    return topic_to_docs


def load_openrouter_client(
    api_key: str = DEFAULT_OPENROUTER_API_KEY,
    model_name: str = DEFAULT_OPENROUTER_MODEL,
    base_url: str = DEFAULT_OPENROUTER_BASE_URL,
    timeout: int = 60,
) -> tuple[OpenAI, str]:
    """
    Load OpenRouter API client for label generation.
    Uses the official OpenAI Python client pointed at OpenRouter's /v1 endpoint.
    We also set the recommended identification headers.
    """
    with stage_timer_local(f"Initializing OpenRouter client: {model_name}"):
        LOGGER.info("Initializing OpenRouter API client")
        LOGGER.info("Model: %s", model_name)
        LOGGER.info("Base URL: %s", base_url)
        # Log API key status (masked for security)
        if api_key:
            api_key_display = (
                f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "***"
            )
            LOGGER.info("API key: %s (length: %d)", api_key_display, len(api_key))
        else:
            LOGGER.warning("API key is empty or None! Authentication WILL fail.")
        # OpenRouter-specific headers (recommended but not strictly required)
        default_headers = {
            # Replace this with the URL of your project/repo if you want to appear on leaderboards
            "HTTP-Referer": "https://example.com/your-bertopic-project",
            "X-Title": "bertopic-romance-llm-labeling",
        }
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            default_headers=default_headers,
        )
        LOGGER.info("✓ OpenRouter client initialized successfully")
    return client, model_name


def test_openrouter_authentication(
    client: OpenAI,
    model_name: str,
) -> bool:
    """
    Test OpenRouter API authentication with a simple test call.
    
    Args:
        client: OpenRouter OpenAI client
        model_name: Model name to test
        
    Returns:
        True if authentication succeeds, False otherwise
    """
    try:
        LOGGER.info("Testing OpenRouter API authentication...")
        # Make a minimal test call (1 token request)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "test"}
            ],
            max_tokens=1,
        )
        if response.choices and len(response.choices) > 0:
            LOGGER.info("✓ API authentication test successful")
            return True
        else:
            LOGGER.warning("API authentication test returned empty response")
            return False
    except Exception as e:
        error_msg = str(e)
        LOGGER.error("✗ API authentication test FAILED: %s", error_msg)
        
        if "401" in error_msg or "Unauthorized" in error_msg or "User not found" in error_msg:
            LOGGER.error("AUTHENTICATION ERROR: API key is invalid, expired, or account doesn't exist")
            LOGGER.error("Please verify:")
            LOGGER.error("  1. API key is correct and active (check at https://openrouter.ai/keys)")
            LOGGER.error("  2. Account has sufficient credits/billing enabled")
            LOGGER.error("  3. Model '%s' is accessible with your account tier", model_name)
        elif "403" in error_msg or "Forbidden" in error_msg:
            LOGGER.error("ACCESS DENIED: Account may not have access to model '%s'", model_name)
            LOGGER.error("Please check if your account tier allows access to this model")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            LOGGER.warning("Rate limit hit during test - but authentication may be OK")
            return True  # Rate limit means auth worked
        else:
            LOGGER.error("Unexpected error during authentication test")
        
        return False


# Generic bad labels to avoid
GENERIC_BAD_LABELS = {
    "Erotic Intimacy",
    "Erotic Encounter",
    "Romantic Moment",
    "Intense Love",
}


def clean_scene_summary(summary: str, keywords: list[str]) -> str:
    return clean_scene_summary_text(summary, keywords)



def normalize_label(raw: str, keywords: list[str] | None = None) -> str:
    return normalize_label_text(raw, keywords)



from src.stage08_llm_labeling.openrouter_experiments.core.labeling_runners import (
    generate_all_labels,
    generate_label_from_keywords_openrouter,
    generate_labels_streaming,
)




def save_labels_openrouter(
    topic_data: dict[int, dict[str, Any]],
    output_path: Path,
) -> None:
    """
    Save topic labels and keywords to JSON file with new structure.
    
    Args:
        topic_data: Dictionary mapping topic_id to dict with 'label' and 'keywords' keys
        output_path: Path to save JSON file (without extension)
    """
    # Use manual string construction to avoid pathlib truncation issues with long filenames
    # pathlib's with_suffix() and path joining can truncate in some cases
    json_path_str = str(output_path.parent) + "/" + output_path.name + ".json"
    json_path = Path(json_path_str)
    
    with stage_timer_local(f"Saving labels to JSON: {json_path.name}"):
        # Convert topic IDs to strings for JSON serialization
        data_serializable: dict[str, dict[str, Any]] = {
            str(topic_id): data for topic_id, data in topic_data.items()
        }
        
        # Create parent directory if it doesn't exist
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_serializable, f, indent=2, ensure_ascii=False)
        
        LOGGER.info(
            "Saved %d topic entries to %s",
            len(data_serializable),
            json_path,
        )

