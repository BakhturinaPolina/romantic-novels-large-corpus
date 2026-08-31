"""Emotion / embodiment / social-world (EES) candidate discovery.

Leaf ∪ secondary ∪ lexical-prototype retrieval over the full mapped topic set.
No embedding index. Survivors are not required for membership — they only seed
the discovery leaf/prototype lists in the exploratory YAML.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

import pandas as pd
import yaml

from src.stage11_refined_construct_analysis.audits.spillover import (
    _lexical_hits,
    _lookup_text_blob,
)
from src.stage11_refined_construct_analysis.config import Stage11Config, load_stage11_config
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup, topics_for_leaves

DEFAULT_EES_CONFIG = Path("configs/stage11/exploratory_emotion_embodiment_social_world.yaml")

FAMILY_KEYS = ("emotion_embodiment", "family_social", "cognition_screen", "work_screen")


def load_ees_config(path: Optional[Path] = None) -> Dict[str, Any]:
    p = path or DEFAULT_EES_CONFIG
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_stage11_from_ees(ees_cfg: Mapping[str, Any]) -> Stage11Config:
    rel = ees_cfg.get("inputs", {}).get("stage11_config", "configs/stage11/refined_constructs.yaml")
    return load_stage11_config(rel)


def ees_output_dir(cfg: Stage11Config, ees_cfg: Mapping[str, Any]) -> Path:
    out = ees_cfg.get("outputs", {}) or {}
    if out.get("ees_dir"):
        path = Path(out["ees_dir"])
        if not path.is_absolute():
            path = cfg.root / path
    else:
        path = cfg.output_path("ees_exploration_dir", create=True)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _secondary_leaf(row: Any) -> Optional[str]:
    secondary = getattr(row, "taxonomy_secondary_id", None)
    if secondary is None or str(secondary) in ("", "None", "nan"):
        return None
    return str(secondary)


def _row_blob(row: Any) -> str:
    return _lookup_text_blob(
        {
            "label": getattr(row, "label", None),
            "scene_summary": getattr(row, "scene_summary", None),
            "all_keywords": getattr(row, "all_keywords", None),
            "keywords": getattr(row, "keywords", None),
            "label_rationale": getattr(row, "label_rationale", None),
        }
    )


def build_family_candidates(
    lookup: pd.DataFrame,
    *,
    primary_leaves: Sequence[str],
    selected_leaves: Optional[Sequence[str]] = None,
    lexical_prototypes: Optional[Sequence[str]] = None,
    max_candidates: int = 100,
    family: str = "",
) -> List[Dict[str, Any]]:
    """Multi-signal candidate rows for one EES discovery family."""
    leaves: Set[str] = {str(x) for x in primary_leaves}
    leaves |= {str(x) for x in (selected_leaves or [])}
    protos = [str(x).lower() for x in (lexical_prototypes or []) if str(x).strip()]

    rows: List[Dict[str, Any]] = []
    for r in lookup.itertuples():
        tid = int(r.topic_id)
        if tid < 0:
            continue
        main = str(getattr(r, "taxonomy_main_id", "") or "")
        secondary_s = _secondary_leaf(r)
        reasons: List[str] = []
        types: Set[str] = set()

        if main in leaves:
            reasons.append(f"primary_leaf={main}")
            types.add("leaf")
        if secondary_s and secondary_s in leaves:
            reasons.append(f"secondary_leaf={secondary_s}")
            types.add("leaf")

        blob = _row_blob(r)
        hits = _lexical_hits(blob, protos) if protos else []
        if hits:
            reasons.append("proto:" + ",".join(hits[:8]))
            types.add("proto")

        if not types:
            continue

        rows.append(
            {
                "family": family,
                "topic_id": tid,
                "label": str(getattr(r, "label", "") or ""),
                "taxonomy_main_id": main,
                "taxonomy_secondary_id": secondary_s,
                "heuristic_notes": "; ".join(reasons),
                "n_signals": len(types),
                "source": f"ees_{family}_discovery",
            }
        )

    rows.sort(key=lambda x: (-int(x.get("n_signals") or 0), int(x["topic_id"])))
    return rows[: int(max_candidates)]


def build_all_ees_candidates(
    cfg: Stage11Config,
    ees_cfg: Mapping[str, Any],
) -> Dict[str, Any]:
    lookup = load_topic_lookup(cfg)
    discovery = ees_cfg.get("discovery") or {}
    families: Dict[str, List[Dict[str, Any]]] = {}
    all_ids: Set[int] = set()

    for key in FAMILY_KEYS:
        block = discovery.get(key) or {}
        if not block:
            families[key] = []
            continue
        cands = build_family_candidates(
            lookup,
            primary_leaves=block.get("primary_leaves") or [],
            selected_leaves=block.get("selected_leaves") or [],
            lexical_prototypes=block.get("lexical_prototypes") or [],
            max_candidates=int(block.get("max_candidates") or 100),
            family=key,
        )
        families[key] = cands
        all_ids.update(int(r["topic_id"]) for r in cands)

    return {
        "run_id": ees_cfg.get("run_id") or cfg.run_id,
        "n_mapped_topics": int((lookup["topic_id"] >= 0).sum()),
        "n_unique_candidates": len(all_ids),
        "families": {k: len(v) for k, v in families.items()},
        "candidates": families,
        "note": (
            "Candidates retrieved from full mapped topic set via leaf ∪ secondary ∪ "
            "lexical prototypes. Survivors are seeds for questions only."
        ),
    }


def candidates_to_frame(payload: Mapping[str, Any]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for family, entries in (payload.get("candidates") or {}).items():
        for e in entries:
            row = dict(e)
            row["family"] = family
            rows.append(row)
    return pd.DataFrame(rows)


def write_ees_candidates(
    cfg: Stage11Config,
    ees_cfg: Mapping[str, Any],
    payload: Mapping[str, Any],
) -> Dict[str, Path]:
    out_dir = ees_output_dir(cfg, ees_cfg)
    json_path = out_dir / "candidate_topics.json"
    csv_path = out_dir / "candidate_topics.csv"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    frame = candidates_to_frame(payload)
    frame.to_csv(csv_path, index=False)
    return {"json": json_path, "csv": csv_path, "dir": out_dir}


def leaf_topic_ids(cfg: Stage11Config, leaves: Sequence[str]) -> List[int]:
    lookup = load_topic_lookup(cfg)
    return topics_for_leaves(lookup, leaves)
