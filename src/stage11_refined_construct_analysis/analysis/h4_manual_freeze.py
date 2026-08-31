"""H4 manual freeze: topic lists, worksheet seeding, override application."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import pandas as pd

from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code
from src.stage11_refined_construct_analysis.config import Stage11Config

LOGGER = logging.getLogger("stage11.h4_manual_freeze")

# Plan defaults (used when construct_coverage is missing keys)
EXTERNAL_PROTECTION_IDS: Tuple[int, ...] = (68, 78, 87, 107, 113, 114, 122, 307, 363)
PROTECTIVE_COMMITMENT_IDS: Tuple[int, ...] = (
    20,
    24,
    73,
    100,
    102,
    119,
    148,
    239,
    240,
    329,
    335,
    338,
)
POSSESSION_CONTROL_IDS: Tuple[int, ...] = (181, 223, 293, 294, 315)

EXPECTED_TOPIC_IDS: Tuple[int, ...] = (
    EXTERNAL_PROTECTION_IDS + PROTECTIVE_COMMITMENT_IDS + POSSESSION_CONTROL_IDS
)

BUCKET_ORDER: Tuple[str, ...] = (
    "external_protection",
    "protective_commitment",
    "possession_control",
)

H4_MANUAL_FREEZE_CODES: Set[str] = {
    "H4_5",
    "H4_5a",
    "H4_6",
    "H4_7",
    "H4_8",
    "H4_9",
    "H4_10",
    "H4_11",
}

VALID_DECISIONS = {"KEEP", "REMOVE"}
VALID_YN = {"yes", "no", ""}

# Manual-freeze sentence display (diversified; not the LLM Pass-B pack)
FREEZE_CELLS: Tuple[str, ...] = ("CELL_A", "CELL_B", "CELL_C", "CELL_D")
FREEZE_PER_CELL = 3
FREEZE_MAX_TOTAL = 16
FREEZE_MIN_CHARS = 25
FREEZE_PREFER_CHARS = 55


def bucket_for_code(code: Any) -> Optional[str]:
    canon = normalize_code(code) if code is not None else None
    if canon in ("H4_5", "H4_6"):
        return "external_protection"
    if canon == "H4_5a":
        return "protective_commitment"
    if canon in ("H4_7", "H4_8", "H4_9", "H4_10", "H4_11"):
        return "possession_control"
    return None


def default_freeze_path(cfg: Stage11Config) -> Path:
    """Canonical freeze file applied by master rebuild."""
    custom = cfg.section("h4_manual_freeze_path", default=None)
    if custom:
        p = Path(custom)
        return p if p.is_absolute() else cfg.root / p
    return cfg.output_path("human_review_dir") / "h4_manual_freeze.json"


def decisions_worksheet_path(cfg: Stage11Config) -> Path:
    return cfg.output_path("human_review_dir") / "h4_manual_freeze_decisions.json"


def load_construct_coverage_ids(cfg: Stage11Config) -> Dict[str, List[int]]:
    """Load the three H4 buckets from construct_coverage.json (preferred)."""
    path = cfg.output_path("constructs_dir") / "construct_coverage.json"
    out: Dict[str, List[int]] = {
        "external_protection": list(EXTERNAL_PROTECTION_IDS),
        "protective_commitment": list(PROTECTIVE_COMMITMENT_IDS),
        "possession_control": list(POSSESSION_CONTROL_IDS),
    }
    if not path.exists():
        return out
    data = json.loads(path.read_text(encoding="utf-8"))
    atoms = data.get("atoms") or {}
    composites = data.get("composites") or {}

    ext = (atoms.get("RAX_external_protection") or {}).get("topic_ids")
    if ext:
        out["external_protection"] = [int(x) for x in ext]

    commit = (atoms.get("RAX_protective_commitment") or {}).get("topic_ids")
    if commit:
        out["protective_commitment"] = [int(x) for x in commit]

    poss = (composites.get("RAX_h4_possession_side") or {}).get("topic_ids")
    if not poss:
        claiming = (atoms.get("RAX_possessive_claiming") or {}).get("topic_ids") or []
        control = (atoms.get("RAX_coercive_control") or {}).get("topic_ids") or []
        poss = sorted(set(int(x) for x in claiming) | set(int(x) for x in control))
    if poss:
        out["possession_control"] = [int(x) for x in poss]
    return out


def seed_decisions_worksheet(df: pd.DataFrame) -> Dict[str, Any]:
    """Blank worksheet for human fill-in (frozen=false until complete)."""
    decisions = []
    for _, row in df.iterrows():
        tid = int(row["topic_id"])
        code = normalize_code(row.get("care_protection_code")) or str(
            row.get("care_protection_code") or ""
        )
        decisions.append(
            {
                "topic_id": tid,
                "topic_label": row.get("current_topic_label"),
                "suggested_code": code,
                "decision": "",  # KEEP | REMOVE
                "final_code": code,  # pre-filled suggestion; edit on KEEP / ignore on REMOVE
                "external_threat": "",  # yes | no
                "main_romantic_target": "",  # yes | no
                "notes": "",
            }
        )
    return {
        "hypothesis": "H4",
        "frozen": False,
        "n_topics": len(decisions),
        "decisions": decisions,
        "instructions": (
            "Fill decision (KEEP|REMOVE), external_threat (yes|no), "
            "main_romantic_target (yes|no), and final_code for KEEP rows. "
            "Set frozen=true and save as h4_manual_freeze.json to apply."
        ),
    }


def load_h4_manual_freeze(cfg: Stage11Config) -> Optional[Dict[str, Any]]:
    path = default_freeze_path(cfg)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"H4 freeze file must be a JSON object: {path}")
    return data


def validate_h4_manual_freeze(
    data: Mapping[str, Any],
    *,
    expected_ids: Optional[Sequence[int]] = None,
    require_frozen: bool = True,
) -> List[str]:
    """Return list of validation errors (empty = OK)."""
    errors: List[str] = []
    if require_frozen and not data.get("frozen"):
        errors.append("frozen must be true before applying")
    decisions = data.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        errors.append("decisions must be a non-empty list")
        return errors

    expected = set(int(x) for x in (expected_ids or EXPECTED_TOPIC_IDS))
    seen: Set[int] = set()
    for i, d in enumerate(decisions):
        if not isinstance(d, dict):
            errors.append(f"decisions[{i}] is not an object")
            continue
        try:
            tid = int(d["topic_id"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"decisions[{i}] missing topic_id")
            continue
        seen.add(tid)
        decision = str(d.get("decision") or "").strip().upper()
        if decision not in VALID_DECISIONS:
            errors.append(f"topic {tid}: decision must be KEEP or REMOVE (got {decision!r})")
            continue
        threat = str(d.get("external_threat") or "").strip().lower()
        target = str(d.get("main_romantic_target") or "").strip().lower()
        if threat not in VALID_YN or threat == "":
            errors.append(f"topic {tid}: external_threat must be yes or no")
        if target not in VALID_YN or target == "":
            errors.append(f"topic {tid}: main_romantic_target must be yes or no")
        if decision == "KEEP":
            final = normalize_code(d.get("final_code")) or str(d.get("final_code") or "").strip()
            if not final:
                errors.append(f"topic {tid}: KEEP requires final_code")
            elif final == "H4_0":
                errors.append(f"topic {tid}: use REMOVE instead of KEEP with H4_0")
            elif final not in H4_MANUAL_FREEZE_CODES and not str(final).startswith("H4_"):
                errors.append(f"topic {tid}: invalid final_code {final!r}")
            # Soft codes (H4_1–H4_4, H4_12) allowed if human reclassifies out of the 26
            # but still KEEP under a non-atom care code — rare; accept any H4_* except H4_0.
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    if missing:
        errors.append(f"missing topic_ids: {missing}")
    if extra:
        errors.append(f"unexpected topic_ids: {extra}")
    return errors


def freeze_overrides(data: Mapping[str, Any]) -> Dict[int, Dict[str, str]]:
    """Map topic_id → {decision, final_code, action_tag} for master application."""
    out: Dict[int, Dict[str, str]] = {}
    for d in data.get("decisions") or []:
        tid = int(d["topic_id"])
        decision = str(d.get("decision") or "").strip().upper()
        if decision == "REMOVE":
            out[tid] = {
                "decision": "REMOVE",
                "final_code": "H4_0",
                "action_tag": "H4:HUMAN_REMOVE",
            }
        elif decision == "KEEP":
            final = normalize_code(d.get("final_code")) or str(d.get("final_code") or "").strip()
            out[tid] = {
                "decision": "KEEP",
                "final_code": final,
                "action_tag": "H4:HUMAN_KEEP",
            }
    return out


def _patch_h4_family_props(row: Mapping[str, Any], final_code: str) -> str:
    """Rewrite H4 Pass-B proportions so W_tk admits the human final_code."""
    raw = row.get("family_proportions_json")
    if isinstance(raw, dict):
        blob = dict(raw)
    elif isinstance(raw, str) and raw.strip():
        try:
            blob = json.loads(raw)
        except json.JSONDecodeError:
            blob = {}
    else:
        blob = {}
    if final_code == "H4_0":
        blob["H4"] = {}
    else:
        blob["H4"] = {final_code: 1.0}
    return json.dumps(blob)


def apply_h4_manual_freeze_to_master(
    master: pd.DataFrame,
    cfg: Stage11Config,
    *,
    freeze_data: Optional[Mapping[str, Any]] = None,
) -> pd.DataFrame:
    """Override care_protection_code from a frozen human decision file.

    No-op if the freeze file is missing or frozen=false.
    """
    data = freeze_data if freeze_data is not None else load_h4_manual_freeze(cfg)
    if not data or not data.get("frozen"):
        return master

    errors = validate_h4_manual_freeze(data, require_frozen=True)
    if errors:
        raise ValueError("Invalid H4 manual freeze:\n  - " + "\n  - ".join(errors))

    overrides = freeze_overrides(data)
    if not overrides:
        return master

    df = master.copy()
    if "adjudication_actions" not in df.columns:
        df["adjudication_actions"] = [[] for _ in range(len(df))]

    n_keep = n_remove = 0
    for idx, row in df.iterrows():
        tid = int(row["topic_id"])
        ov = overrides.get(tid)
        if not ov:
            continue
        final = ov["final_code"]
        df.at[idx, "care_protection_code"] = final
        df.at[idx, "family_proportions_json"] = _patch_h4_family_props(row, final)
        actions = row.get("adjudication_actions")
        if isinstance(actions, list):
            new_actions = list(actions) + [ov["action_tag"]]
        elif isinstance(actions, str) and actions:
            new_actions = [actions, ov["action_tag"]]
        else:
            new_actions = [ov["action_tag"]]
        df.at[idx, "adjudication_actions"] = new_actions
        if ov["decision"] == "REMOVE":
            n_remove += 1
        else:
            n_keep += 1

    LOGGER.info(
        "Applied H4 manual freeze: KEEP=%d REMOVE=%d (of %d overrides)",
        n_keep,
        n_remove,
        len(overrides),
    )
    return df


def _norm_text(text: Any) -> str:
    return " ".join(str(text or "").split())


def _sent_len(s: Mapping[str, Any]) -> int:
    return len(_norm_text(s.get("sentence")))


def load_packet_sentences(cfg: Stage11Config, topic_id: int) -> List[Dict[str, Any]]:
    """Full contextual sentence list from the evidence packet (not the 12-cap review)."""
    from src.stage11_refined_construct_analysis.audits.runner import load_evidence_packet

    packet = load_evidence_packet(cfg, int(topic_id)) or {}
    raw = (packet.get("contextual") or {}).get("sentences") or []
    out: List[Dict[str, Any]] = []
    for s in raw:
        item = dict(s)
        item["sentence"] = _norm_text(item.get("sentence"))
        out.append(item)
    return out


def select_diversified_sentences(
    sentences: Sequence[Mapping[str, Any]],
    *,
    per_cell: int = FREEZE_PER_CELL,
    max_total: int = FREEZE_MAX_TOTAL,
    min_chars: int = FREEZE_MIN_CHARS,
    prefer_chars: int = FREEZE_PREFER_CHARS,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Stratify by CELL_A–D, prefer different books and longer sentences.

    Returns (selected, coverage_meta) where coverage_meta notes empty cells.
    """
    by_cell: Dict[str, List[Dict[str, Any]]] = {c: [] for c in FREEZE_CELLS}
    other: List[Dict[str, Any]] = []
    for s in sentences:
        item = dict(s)
        item["sentence"] = _norm_text(item.get("sentence"))
        cell = str(item.get("cell") or "").strip() or "UNKNOWN"
        if cell in by_cell:
            by_cell[cell].append(item)
        else:
            other.append(item)

    for cell in FREEZE_CELLS:
        by_cell[cell].sort(
            key=lambda s: (
                0 if _sent_len(s) >= prefer_chars else 1,
                -_sent_len(s),
                -float(s.get("max_topic_prob") or 0.0),
            )
        )

    selected: List[Dict[str, Any]] = []
    used_books: Set[str] = set()
    used_keys: Set[Tuple[Any, ...]] = set()

    def _key(s: Mapping[str, Any]) -> Tuple[Any, ...]:
        return (
            s.get("book_id_anon"),
            s.get("chapter_index"),
            s.get("sentence_index"),
            s.get("sid"),
        )

    def _cell_count(cell: str) -> int:
        return sum(1 for s in selected if str(s.get("cell")) == cell)

    def _take_from_pool(
        pool: List[Dict[str, Any]],
        n: int,
        *,
        require_new_book: bool,
        cell_cap: Optional[int] = None,
    ) -> int:
        taken = 0
        for pass_new_book in (True, False) if not require_new_book else (True,):
            use_new = require_new_book or pass_new_book
            for s in pool:
                if taken >= n or len(selected) >= max_total:
                    break
                cell = str(s.get("cell") or "")
                if cell_cap is not None and cell in FREEZE_CELLS and _cell_count(cell) >= cell_cap:
                    continue
                book = str(s.get("book_id_anon") or "")
                if use_new and book and book in used_books:
                    continue
                if _sent_len(s) < min_chars and any(_sent_len(x) >= min_chars for x in pool):
                    continue
                k = _key(s)
                if k in used_keys:
                    continue
                selected.append(s)
                used_keys.add(k)
                if book:
                    used_books.add(book)
                taken += 1
            if require_new_book:
                # second pass: allow book reuse within cell if still thin
                for s in pool:
                    if taken >= n or len(selected) >= max_total:
                        break
                    cell = str(s.get("cell") or "")
                    if cell_cap is not None and cell in FREEZE_CELLS and _cell_count(cell) >= cell_cap:
                        continue
                    k = _key(s)
                    if k in used_keys:
                        continue
                    if _sent_len(s) < min_chars and any(
                        _sent_len(x) >= min_chars for x in pool
                    ):
                        continue
                    selected.append(s)
                    used_keys.add(k)
                    book = str(s.get("book_id_anon") or "")
                    if book:
                        used_books.add(book)
                    taken += 1
                break
        return taken

    empty_cells: List[str] = []
    thin_cells: List[str] = []
    cell_hard_cap = per_cell + 1
    for cell in FREEZE_CELLS:
        pool = by_cell[cell]
        if not pool:
            empty_cells.append(cell)
            continue
        n = _take_from_pool(pool, per_cell, require_new_book=True, cell_cap=cell_hard_cap)
        if n < per_cell:
            thin_cells.append(cell)

    # Fill remaining slots: first finish thin cells, then round-robin with new books
    if len(selected) < max_total:
        leftover_by_cell: Dict[str, List[Dict[str, Any]]] = {
            c: [s for s in by_cell[c] if _key(s) not in used_keys] for c in FREEZE_CELLS
        }
        for cell in FREEZE_CELLS:
            have = _cell_count(cell)
            if have >= per_cell:
                continue
            _take_from_pool(
                leftover_by_cell[cell],
                per_cell - have,
                require_new_book=True,
                cell_cap=cell_hard_cap,
            )
        while len(selected) < max_total:
            progressed = False
            for cell in FREEZE_CELLS:
                if len(selected) >= max_total:
                    break
                if _cell_count(cell) >= cell_hard_cap:
                    continue
                pool = [s for s in leftover_by_cell[cell] if _key(s) not in used_keys]
                n = _take_from_pool(pool, 1, require_new_book=True, cell_cap=cell_hard_cap)
                if n:
                    progressed = True
            if not progressed:
                break
        if len(selected) < max_total:
            leftover: List[Dict[str, Any]] = []
            for cell in FREEZE_CELLS:
                leftover.extend(by_cell[cell])
            leftover.extend(other)
            leftover = [s for s in leftover if _key(s) not in used_keys]
            leftover.sort(key=lambda s: -_sent_len(s))
            _take_from_pool(
                leftover, max_total - len(selected), require_new_book=True, cell_cap=cell_hard_cap
            )

    # Stable display order: by cell then book
    cell_rank = {c: i for i, c in enumerate(FREEZE_CELLS)}
    selected.sort(
        key=lambda s: (
            cell_rank.get(str(s.get("cell") or ""), 99),
            str(s.get("book_id_anon") or ""),
            -_sent_len(s),
        )
    )
    meta = {
        "empty_cells": empty_cells,
        "thin_cells": thin_cells,
        "n_selected": len(selected),
        "n_books": len(used_books),
        "cells_present": sorted(
            {str(s.get("cell")) for s in selected if s.get("cell")}
        ),
    }
    return selected, meta


def enrich_sentences_with_neighbors(
    cfg: Stage11Config,
    topic_id: int,
    sentences: Sequence[Mapping[str, Any]],
    book_map: Mapping[str, int],
    *,
    neighbor_cache: Optional[Dict[Tuple[int, int, int], Dict[str, str]]] = None,
    always: bool = True,
    short_chars: int = FREEZE_PREFER_CHARS,
) -> List[Dict[str, Any]]:
    """Attach ±1 sentence context from corpus parquet.

    Sets ``sentence_before``, ``sentence_after``, and ``display_sentence``.
    Pass ``neighbor_cache`` from :func:`fetch_neighbor_context_batch` to avoid
    rescanning sentence parquets per topic.
    """
    if not sentences:
        return []

    out = [dict(s) for s in sentences]
    need_keys: List[Tuple[int, int, int]] = []
    need_idx: List[Tuple[int, Tuple[int, int, int]]] = []
    for i, s in enumerate(out):
        text = _norm_text(s.get("sentence"))
        s["sentence"] = text
        s["display_sentence"] = text
        anon = str(s.get("book_id_anon") or "")
        real = book_map.get(anon)
        ch = s.get("chapter_index")
        si = s.get("sentence_index")
        if real is None or ch is None or si is None:
            continue
        if always or len(text) < short_chars:
            key = (int(real), int(ch), int(si))
            need_keys.append(key)
            need_idx.append((i, key))

    if not need_keys:
        return out

    cache = neighbor_cache
    if cache is None:
        cache = fetch_neighbor_context_batch(cfg, need_keys)

    for i, key in need_idx:
        neigh = cache.get(key) or {}
        before = neigh.get("before", "")
        after = neigh.get("after", "")
        target = out[i].get("sentence") or neigh.get("target") or ""
        out[i]["sentence_before"] = before
        out[i]["sentence_after"] = after
        if before or after:
            parts = []
            if before:
                parts.append(before)
            parts.append(f"[TARGET] {target}")
            if after:
                parts.append(after)
            out[i]["display_sentence"] = " ".join(parts)
        else:
            out[i]["display_sentence"] = target
    return out


def fetch_neighbor_context_batch(
    cfg: Stage11Config,
    keys: Sequence[Tuple[int, int, int]],
) -> Dict[Tuple[int, int, int], Dict[str, str]]:
    """One DuckDB scan: map (book_id, chapter, sentence_index) → before/target/after."""
    uniq = sorted({(int(b), int(c), int(s)) for b, c, s in keys})
    if not uniq:
        return {}
    try:
        import duckdb
    except ImportError:
        LOGGER.warning("duckdb unavailable; skipping neighbor enrichment")
        return {}

    files = cfg.sentence_topic_files()
    if not files:
        return {}
    files_sql = ", ".join(f"'{f}'" for f in files)
    values = ", ".join(f"({b}, {c}, {s})" for b, c, s in uniq)
    query = f"""
        with targets(book_id, chapter_index, sentence_index) as (
            values {values}
        )
        select
            t.book_id,
            t.chapter_index,
            t.sentence_index as target_si,
            s.sentence_index as neigh_si,
            s.sentence
        from targets t
        join read_parquet([{files_sql}]) s
          on s.work_id = t.book_id
         and s.chapter_index = t.chapter_index
         and s.sentence_index between t.sentence_index - 1 and t.sentence_index + 1
    """
    try:
        con = duckdb.connect()
        con.execute("pragma threads=4")
        df = con.execute(query).df()
        con.close()
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Neighbor batch fetch failed: %s", exc)
        return {}

    buckets: Dict[Tuple[int, int, int], Dict[int, str]] = {}
    for row in df.itertuples(index=False):
        key = (int(row.book_id), int(row.chapter_index), int(row.target_si))
        buckets.setdefault(key, {})[int(row.neigh_si)] = _norm_text(row.sentence)

    out: Dict[Tuple[int, int, int], Dict[str, str]] = {}
    for key in uniq:
        bid, ch, si = key
        neigh = buckets.get(key) or {}
        out[key] = {
            "before": neigh.get(si - 1, ""),
            "target": neigh.get(si, ""),
            "after": neigh.get(si + 1, ""),
        }
    return out


def load_freeze_review_sentences(
    cfg: Stage11Config,
    topic_id: int,
    book_map: Mapping[str, int],
    *,
    neighbor_cache: Optional[Dict[Tuple[int, int, int], Dict[str, str]]] = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Diversified + context-enriched sentences for the H4 freeze PDF."""
    raw = load_packet_sentences(cfg, topic_id)
    selected, meta = select_diversified_sentences(raw)
    enriched = enrich_sentences_with_neighbors(
        cfg, topic_id, selected, book_map, neighbor_cache=neighbor_cache
    )
    meta["n_with_context"] = sum(
        1 for s in enriched if s.get("sentence_before") or s.get("sentence_after")
    )
    return enriched, meta


def preload_freeze_neighbor_cache(
    cfg: Stage11Config,
    topic_book_maps: Mapping[int, Mapping[str, int]],
) -> Dict[Tuple[int, int, int], Dict[str, str]]:
    """Select diversified sentences for all topics, then one corpus neighbor scan."""
    keys: List[Tuple[int, int, int]] = []
    for tid, book_map in topic_book_maps.items():
        raw = load_packet_sentences(cfg, tid)
        selected, _ = select_diversified_sentences(raw)
        for s in selected:
            anon = str(s.get("book_id_anon") or "")
            real = book_map.get(anon)
            ch = s.get("chapter_index")
            si = s.get("sentence_index")
            if real is None or ch is None or si is None:
                continue
            keys.append((int(real), int(ch), int(si)))
    LOGGER.info("H4 freeze neighbor preload: %d anchors", len(keys))
    return fetch_neighbor_context_batch(cfg, keys)
