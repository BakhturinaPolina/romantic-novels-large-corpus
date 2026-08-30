"""Lookup-driven candidate pools and integrity asserts for Stage 11.

Never hard-code topic counts in prompts or notebooks. All pools are derived from the
frozen Stage 10 `topic_lookup.parquet` and checked against known post-rerun traps.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set

import pandas as pd

from src.stage11_refined_construct_analysis.config import Stage11Config


@dataclass(frozen=True)
class LeafPool:
    leaf_id: str
    topic_ids: tuple[int, ...]
    n_topics: int
    empty: bool


@dataclass
class IntegrityReport:
    ok: bool
    checks: List[Dict[str, Any]] = field(default_factory=list)
    h2_topic_ids: List[int] = field(default_factory=list)
    leaf_pools: Dict[str, LeafPool] = field(default_factory=dict)
    empty_leaves: List[str] = field(default_factory=list)

    def raise_if_failed(self) -> None:
        if self.ok:
            return
        failed = [c for c in self.checks if not c.get("ok")]
        lines = [f"{c['name']}: {c.get('detail')}" for c in failed]
        raise AssertionError("Stage 11 lookup integrity failed:\n  " + "\n  ".join(lines))


def load_topic_lookup(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.input_path("topic_lookup", required=True)
    assert path is not None
    df = pd.read_parquet(path)
    required = {"topic_id", "taxonomy_main_id", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"topic_lookup missing columns: {sorted(missing)}")
    out = df.copy()
    out["topic_id"] = out["topic_id"].astype(int)
    out["taxonomy_main_id"] = out["taxonomy_main_id"].astype(str)
    return out


def topics_for_leaves(
    lookup: pd.DataFrame,
    leaves: Sequence[str],
    *,
    id_column: str = "taxonomy_main_id",
) -> List[int]:
    wanted = set(str(x) for x in leaves)
    mask = lookup[id_column].isin(wanted)
    return sorted(int(t) for t in lookup.loc[mask, "topic_id"].tolist())


def leaf_pool(lookup: pd.DataFrame, leaf_id: str) -> LeafPool:
    ids = topics_for_leaves(lookup, [leaf_id])
    return LeafPool(
        leaf_id=str(leaf_id),
        topic_ids=tuple(ids),
        n_topics=len(ids),
        empty=len(ids) == 0,
    )


def build_leaf_pools(
    lookup: pd.DataFrame,
    leaf_ids: Iterable[str],
) -> Dict[str, LeafPool]:
    return {str(leaf): leaf_pool(lookup, str(leaf)) for leaf in leaf_ids}


def all_hypothesis_leaves(cfg: Stage11Config) -> List[str]:
    leaves: Set[str] = set()
    for hyp_cfg in cfg.section("hypotheses").values():
        if not isinstance(hyp_cfg, dict):
            continue
        for key in (
            "mandatory_leaves",
            "comparator_leaves",
            "spillover_discovery_leaves",
            "focus_leaves",
            "skip_full_relabel_leaves",
        ):
            for leaf in hyp_cfg.get(key, []) or []:
                leaves.add(str(leaf))
    for leaf in cfg.section("integrity", "empty_leaves"):
        leaves.add(str(leaf))
    for leaf in cfg.section("integrity", "h2_pool_leaves"):
        leaves.add(str(leaf))
    for leaf in cfg.section("evidence", "exhaustive_leaves"):
        leaves.add(str(leaf))
    return sorted(leaves)


def run_lookup_integrity(
    cfg: Stage11Config,
    lookup: Optional[pd.DataFrame] = None,
) -> IntegrityReport:
    """Assert live lookup against post-rerun traps (H2 pool size, 7.2 count, empties)."""
    lookup = load_topic_lookup(cfg) if lookup is None else lookup
    integrity = cfg.section("integrity")
    report = IntegrityReport(ok=True)

    pools = build_leaf_pools(lookup, all_hypothesis_leaves(cfg))
    report.leaf_pools = pools

    # H2 pool: 4.5 ∪ 5.3a ∪ 8.3a
    h2_leaves = [str(x) for x in integrity["h2_pool_leaves"]]
    h2_ids = topics_for_leaves(lookup, h2_leaves)
    report.h2_topic_ids = h2_ids
    expected_h2 = int(integrity["h2_expected_n_topics"])
    h2_ok = len(h2_ids) == expected_h2
    report.checks.append(
        {
            "name": "h2_pool_size",
            "ok": h2_ok,
            "detail": (
                f"H2 pool leaves {h2_leaves} yield {len(h2_ids)} topics "
                f"(expected {expected_h2}); ids={h2_ids}"
            ),
            "topic_ids": h2_ids,
            "by_leaf": {leaf: list(pools[leaf].topic_ids) for leaf in h2_leaves},
        }
    )

    # Per-leaf H2 breakdown (informational + soft assert of non-empty critical leaves)
    for leaf in h2_leaves:
        pool = pools[leaf]
        report.checks.append(
            {
                "name": f"h2_leaf_{leaf}",
                "ok": pool.n_topics > 0,
                "detail": f"leaf {leaf}: n={pool.n_topics}, ids={list(pool.topic_ids)}",
                "n_topics": pool.n_topics,
                "topic_ids": list(pool.topic_ids),
            }
        )

    # 7.2 count (12, not the older prose “13”)
    leaf_72 = pools.get("7.2") or leaf_pool(lookup, "7.2")
    expected_72 = int(integrity["leaf_7_2_expected_n"])
    ok_72 = leaf_72.n_topics == expected_72
    report.checks.append(
        {
            "name": "leaf_7_2_count",
            "ok": ok_72,
            "detail": (
                f"leaf 7.2 has {leaf_72.n_topics} topics (expected {expected_72}); "
                f"ids={list(leaf_72.topic_ids)}"
            ),
            "n_topics": leaf_72.n_topics,
            "topic_ids": list(leaf_72.topic_ids),
        }
    )

    # Empty leaves stay empty — do not invent mass
    empty_leaves = [str(x) for x in integrity["empty_leaves"]]
    report.empty_leaves = []
    for leaf in empty_leaves:
        pool = pools.get(leaf) or leaf_pool(lookup, leaf)
        is_empty = pool.empty
        if is_empty:
            report.empty_leaves.append(leaf)
        report.checks.append(
            {
                "name": f"empty_leaf_{leaf}",
                "ok": is_empty,
                "detail": (
                    f"leaf {leaf} should be empty; found {pool.n_topics} topics "
                    f"{list(pool.topic_ids)}"
                ),
                "n_topics": pool.n_topics,
                "unmeasurable": is_empty,
            }
        )

    # Topic 91 → 7.1 (not 7.2)
    expected_91 = str(integrity["topic_91_expected_leaf"])
    row = lookup.loc[lookup["topic_id"] == 91]
    if row.empty:
        ok_91 = False
        detail_91 = "topic 91 missing from lookup"
    else:
        got = str(row.iloc[0]["taxonomy_main_id"])
        ok_91 = got == expected_91
        detail_91 = f"topic 91 taxonomy_main_id={got} (expected {expected_91})"
    report.checks.append({"name": "topic_91_leaf", "ok": ok_91, "detail": detail_91})

    report.ok = all(bool(c["ok"]) for c in report.checks)
    return report


def build_hypothesis_manifest(
    cfg: Stage11Config,
    lookup: pd.DataFrame,
    hypothesis: str,
) -> Dict[str, Any]:
    """Derive topic IDs for one hypothesis from the live lookup."""
    hyp = str(hypothesis).upper()
    hyp_cfg = cfg.section("hypotheses", hyp)
    exhaustive_leaves = set(str(x) for x in cfg.section("evidence", "exhaustive_leaves"))

    def pack(leaves: Sequence[str], role: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for leaf in leaves:
            pool = leaf_pool(lookup, str(leaf))
            for tid in pool.topic_ids:
                row = lookup.loc[lookup["topic_id"] == tid].iloc[0]
                rows.append(
                    {
                        "topic_id": int(tid),
                        "label": row.get("label"),
                        "taxonomy_main_id": str(leaf),
                        "taxonomy_main_name": row.get("taxonomy_main_name"),
                        "role": role,
                        "exhaustive": str(leaf) in exhaustive_leaves,
                        "unmeasurable_empty_leaf": False,
                    }
                )
            if pool.empty:
                rows.append(
                    {
                        "topic_id": None,
                        "label": None,
                        "taxonomy_main_id": str(leaf),
                        "taxonomy_main_name": None,
                        "role": role,
                        "exhaustive": str(leaf) in exhaustive_leaves,
                        "unmeasurable_empty_leaf": True,
                    }
                )
        return rows

    entries: List[Dict[str, Any]] = []
    entries.extend(pack(hyp_cfg.get("mandatory_leaves", []) or [], "mandatory"))
    entries.extend(pack(hyp_cfg.get("comparator_leaves", []) or [], "comparator"))
    entries.extend(pack(hyp_cfg.get("spillover_discovery_leaves", []) or [], "spillover_discovery"))
    entries.extend(pack(hyp_cfg.get("focus_leaves", []) or [], "focus"))

    measurable = [e for e in entries if e.get("topic_id") is not None]
    topic_ids = sorted({int(e["topic_id"]) for e in measurable})

    return {
        "hypothesis": hyp,
        "name": hyp_cfg.get("name"),
        "n_topics": len(topic_ids),
        "topic_ids": topic_ids,
        "entries": entries,
        "position_visible_in_pass_b": bool(hyp_cfg.get("position_visible_in_pass_b", False)),
        "skip_full_relabel_leaves": list(hyp_cfg.get("skip_full_relabel_leaves", []) or []),
    }


def build_all_manifests(cfg: Stage11Config, lookup: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    lookup = load_topic_lookup(cfg) if lookup is None else lookup
    integrity = run_lookup_integrity(cfg, lookup)
    integrity.raise_if_failed()

    manifests = {
        hyp: build_hypothesis_manifest(cfg, lookup, hyp)
        for hyp in cfg.section("hypotheses")
    }

    # Union of all audited topic IDs (for shared evidence packets)
    audited: Set[int] = set()
    for man in manifests.values():
        audited.update(int(t) for t in man["topic_ids"])

    exhaustive_ids = topics_for_leaves(
        lookup, cfg.section("evidence", "exhaustive_leaves")
    )

    return {
        "run_id": cfg.run_id,
        "integrity": {
            "ok": integrity.ok,
            "checks": integrity.checks,
            "h2_topic_ids": integrity.h2_topic_ids,
            "empty_leaves": integrity.empty_leaves,
        },
        "hypotheses": manifests,
        "audited_topic_ids": sorted(audited),
        "exhaustive_topic_ids": exhaustive_ids,
        "n_audited_topics": len(audited),
    }


def write_manifests(cfg: Stage11Config, payload: Mapping[str, Any]) -> Path:
    out_dir = cfg.output_path("candidates_dir", create=True)
    path = out_dir / "candidate_manifests.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    # Per-hypothesis CSV-friendly lists
    for hyp, man in payload["hypotheses"].items():
        hyp_path = out_dir / f"{hyp.lower()}_candidates.json"
        hyp_path.write_text(json.dumps(man, indent=2, default=str), encoding="utf-8")

    frozen = {
        "run_id": cfg.run_id,
        "topic_lookup": str(cfg.input_path("topic_lookup")),
        "n_audited_topics": payload["n_audited_topics"],
        "h2_topic_ids": payload["integrity"]["h2_topic_ids"],
        "h2_n": len(payload["integrity"]["h2_topic_ids"]),
        "empty_leaves": payload["integrity"]["empty_leaves"],
        "exhaustive_topic_ids": payload["exhaustive_topic_ids"],
        "integrity_ok": payload["integrity"]["ok"],
    }
    frozen_path = cfg.output_path("frozen_inputs", create=True)
    frozen_path.write_text(json.dumps(frozen, indent=2), encoding="utf-8")
    return path
