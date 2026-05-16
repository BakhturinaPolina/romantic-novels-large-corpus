"""Compatibility shim for moved Stage 03 BERTopic OCTIS wrapper."""

from src.stage03_modeling.bertopic_octis_model import (  # noqa: F401
    BERTopicOctisModelWithEmbeddings,
    create_representation_models,
    get_embedding_model_cache_dir,
    load_embedding_model,
)

