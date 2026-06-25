"""Sync compare-fit topic_info.csv from a loaded BERTopic model (e.g. after Stage06)."""

from __future__ import annotations

import logging
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd
from bertopic import BERTopic

LOGGER = logging.getLogger("topic_posthoc")


def backup_topic_info(path: Path) -> Path | None:
    """Copy topic_info.csv to topic_info_backup_<timestamp>.csv if it exists."""
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(f"{path.stem}_backup_{stamp}{path.suffix}")
    shutil.copy2(path, backup)
    LOGGER.info("Backed up topic_info: %s -> %s", path.name, backup.name)
    return backup


def sync_topic_info_csv(
    topic_model: BERTopic,
    topic_info_path: Path,
    *,
    backup: bool = True,
) -> pd.DataFrame:
    """
    Overwrite topic_info.csv with the model's current get_topic_info() export.

    Use after Stage06 enrichment so post-hoc rules see Main c-TF-IDF labels
    (not stale compare-fit verb-heavy words).
    """
    topic_info_path = Path(topic_info_path)
    topic_info_path.parent.mkdir(parents=True, exist_ok=True)
    if backup:
        backup_topic_info(topic_info_path)
    info = topic_model.get_topic_info()
    info.to_csv(topic_info_path, index=False)
    LOGGER.info(
        "Synced topic_info.csv (%d rows) -> %s",
        len(info),
        topic_info_path,
    )
    return info
