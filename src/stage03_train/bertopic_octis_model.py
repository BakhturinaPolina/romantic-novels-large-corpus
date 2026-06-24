"""Compatibility shim for moved Stage 03 BERTopic OCTIS wrapper."""

from src.legacy.stage03_modeling.bertopic_octis_model import (  # noqa: F401
    BERTopicOctisModelWithEmbeddings,
    BERTopicWithSafeVectorizer,
    create_representation_models,
    get_embedding_model_cache_dir,
    load_embedding_model,
)

