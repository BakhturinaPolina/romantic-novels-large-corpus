"""Rating-cell blinding for Stage 11 evidence packets.

Sampling cells stay as CELL_A…CELL_D until notebook 10 unblinds via sealed cell_key.json.
Narrative position/tertile is NOT blinded (needed for H2/H6 Pass B).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, MutableMapping, Optional

from src.stage11_refined_construct_analysis.config import Stage11Config

# Fixed semantic mapping declared in config; sealed file records the freeze.
DEFAULT_CELL_MEANINGS = {
    "CELL_A": "high_prevalence_high_tier",
    "CELL_B": "high_prevalence_low_tier",
    "CELL_C": "low_prevalence_high_tier",
    "CELL_D": "low_prevalence_low_tier",
}


@dataclass(frozen=True)
class CellKey:
    labels: tuple[str, ...]
    meanings: Dict[str, str]
    sealed: bool = True

    def to_dict(self) -> Dict[str, object]:
        return {
            "labels": list(self.labels),
            "meanings": dict(self.meanings),
            "sealed": self.sealed,
            "note": (
                "Do not open until notebook 10 contextual validation. "
                "Pass A/B must only see CELL_* labels; position/tertile may be visible."
            ),
        }

    def label_for_meaning(self, meaning: str) -> str:
        for label, mapped in self.meanings.items():
            if mapped == meaning:
                return label
        raise KeyError(f"No CELL_* label for meaning {meaning!r}")


def load_or_create_cell_key(cfg: Stage11Config) -> CellKey:
    meanings = dict(cfg.section("evidence", "cell_meanings", default=DEFAULT_CELL_MEANINGS))
    labels = tuple(cfg.section("evidence", "cell_labels", default=list(DEFAULT_CELL_MEANINGS)))
    return CellKey(labels=labels, meanings=meanings, sealed=True)


def seal_cell_key(cfg: Stage11Config, cell_key: Optional[CellKey] = None) -> Path:
    key = cell_key or load_or_create_cell_key(cfg)
    path = cfg.output_path("cell_key", create=True)
    path.write_text(json.dumps(key.to_dict(), indent=2), encoding="utf-8")
    return path


def apply_cell_blind(
    row: MutableMapping[str, object],
    cell_key: CellKey,
    *,
    meaning_field: str = "cell_meaning",
    blind_field: str = "cell",
) -> MutableMapping[str, object]:
    """Replace human-readable cell meaning with CELL_* and drop rating tier."""
    meaning = str(row.get(meaning_field, ""))
    if meaning:
        row[blind_field] = cell_key.label_for_meaning(meaning)
    row.pop("rating_tier", None)
    row.pop("rating_class", None)
    row.pop(meaning_field, None)
    return row


def unblind_cell(label: str, cell_key: CellKey | Mapping[str, str]) -> str:
    if isinstance(cell_key, CellKey):
        return cell_key.meanings[label]
    return dict(cell_key)[label]
