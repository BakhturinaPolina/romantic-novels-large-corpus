"""Post-hoc topic classification rules (metadata only, no model mutation)."""

from src.common.topic_posthoc.rules import (
    PosthocRulesConfig,
    classify_topics_from_info,
    load_rules_config,
    write_posthoc_artifacts,
)

__all__ = [
    "PosthocRulesConfig",
    "classify_topics_from_info",
    "load_rules_config",
    "write_posthoc_artifacts",
]
