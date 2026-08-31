"""Shared evidence packets (lexical + contextual + tertile) for all Stage 11 audits.

One packet per topic — built once, reused by H1–H6 notebooks and the stability pilot.
Taxonomy / rating effects stay sealed until Pass C / notebook 10.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set

import numpy as np
import pandas as pd

from src.stage11_refined_construct_analysis.config import Stage11Config
from src.stage11_refined_construct_analysis.evidence.blinding import (
    CellKey,
    apply_cell_blind,
    load_or_create_cell_key,
    seal_cell_key,
)
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup, topics_for_leaves

LOGGER = logging.getLogger("stage11.evidence")

REP_NAMES = ("Main", "KeyBERT", "POS", "MMR")
TERTILE_MAP = {1: "begin", 2: "middle", 3: "end"}


def load_topic_metadata(cfg: Stage11Config) -> Dict[int, Dict[str, Any]]:
    path = cfg.input_path("topic_metadata", required=True)
    assert path is not None
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: Dict[int, Dict[str, Any]] = {}
    for key, value in raw.items():
        try:
            tid = int(key)
        except (TypeError, ValueError):
            continue
        if isinstance(value, dict):
            out[tid] = value
    return out


def load_representative_docs(cfg: Stage11Config) -> Dict[int, List[str]]:
    path = cfg.input_path("representative_docs", required=False)
    if path is None or not path.exists():
        return {}
    df = pd.read_csv(path)
    topic_col = "topic" if "topic" in df.columns else "topic_id"
    sent_col = "sentence" if "sentence" in df.columns else "Document"
    out: Dict[int, List[str]] = {}
    for topic_id, group in df.groupby(topic_col):
        try:
            tid = int(topic_id)
        except (TypeError, ValueError):
            continue
        if tid < 0:
            continue
        texts = [str(s).strip() for s in group[sent_col].tolist() if str(s).strip()]
        out[tid] = texts
    return out


def lexical_block(
    topic_id: int,
    metadata: Mapping[int, Mapping[str, Any]],
    *,
    representation_names: Sequence[str] = REP_NAMES,
) -> Dict[str, Any]:
    meta = dict(metadata.get(int(topic_id), {}))
    reps = meta.get("representations") or {}
    lexical = {
        name: list(reps.get(name, []) or [])
        for name in representation_names
    }
    # Fallback: POS-style keywords field if Main empty
    if not lexical.get("Main") and meta.get("keywords"):
        lexical["Main"] = list(meta.get("keywords") or [])
    return {
        "topic_id": int(topic_id),
        "label_public": meta.get("label"),  # descriptive only; taxonomy ids stay sealed
        "representations": lexical,
        "stage08_snippets": list(meta.get("snippets") or []),
    }


def _prevalence_frame(
    book_topic_counts: pd.DataFrame,
    topic_id: int,
    analysis_frame: pd.DataFrame,
    *,
    tier_column: str,
) -> pd.DataFrame:
    counts = book_topic_counts[book_topic_counts["topic_id"] == int(topic_id)][
        ["book_id", "share", "n_sentences"]
    ].copy()
    # Books with zero mass for this topic still matter for the low-prevalence cell.
    frame = analysis_frame[["book_id", tier_column]].copy()
    merged = frame.merge(counts, on="book_id", how="left")
    merged["share"] = merged["share"].fillna(0.0)
    merged["n_sentences"] = merged["n_sentences"].fillna(0).astype(int)
    return merged


def sample_prevalence_rating_books(
    prevalence: pd.DataFrame,
    *,
    tier_column: str,
    tier_high: str,
    tier_low: str,
    quantiles: Sequence[float],
    books_per_cell: int,
    seed: int,
    max_books: Optional[int] = None,
) -> pd.DataFrame:
    """2×2: topic prevalence extreme × rating tier (meanings later blinded to CELL_*).

    Low cells use **positive-share only** (share > 0 and n_sentences > 0) so
    DuckDB hard-assignment fetches can return sentences. Empty cells are
    backfilled from the same rating tier by extreme share rank.
    """
    valid = prevalence.dropna(subset=[tier_column]).copy()
    low_q, high_q = list(quantiles)
    # Review packets need fetchable sentences; exclude true zeros from all cells.
    present = valid[(valid["share"] > 0) & (valid["n_sentences"] > 0)].copy()
    if present.empty:
        return pd.DataFrame(
            columns=["book_id", "share", "n_sentences", tier_column, "cell_meaning"]
        )

    low_cut = float(present["share"].quantile(low_q))
    high_cut = float(present["share"].quantile(high_q))
    # If the topic is ultra-sparse, treat any positive share as "high".
    if high_cut <= low_cut:
        high_cut = float(present["share"].min())
        low_cut = float(present["share"].max())

    cells = {
        "high_prevalence_high_tier": (present["share"] >= high_cut)
        & (present[tier_column] == tier_high),
        "high_prevalence_low_tier": (present["share"] >= high_cut)
        & (present[tier_column] == tier_low),
        "low_prevalence_high_tier": (present["share"] <= low_cut)
        & (present[tier_column] == tier_high),
        "low_prevalence_low_tier": (present["share"] <= low_cut)
        & (present[tier_column] == tier_low),
    }
    low_meanings = {"low_prevalence_high_tier", "low_prevalence_low_tier"}
    tier_for_meaning = {
        "high_prevalence_high_tier": tier_high,
        "high_prevalence_low_tier": tier_low,
        "low_prevalence_high_tier": tier_high,
        "low_prevalence_low_tier": tier_low,
    }

    rng = np.random.default_rng(seed)
    picks: List[pd.DataFrame] = []
    used_ids: Set[int] = set()
    for meaning, mask in cells.items():
        candidates = present.loc[mask]
        if candidates.empty:
            chosen = present.iloc[0:0].copy()
        else:
            take = min(int(books_per_cell), len(candidates))
            chosen_idx = rng.choice(len(candidates), size=take, replace=False)
            chosen = candidates.iloc[chosen_idx].copy()
        chosen["cell_meaning"] = meaning

        # Backfill thin cells from same rating tier by extreme share.
        if len(chosen) < int(books_per_cell):
            tier = tier_for_meaning[meaning]
            pool = present[
                (present[tier_column] == tier)
                & (~present["book_id"].isin(set(chosen["book_id"]).union(used_ids)))
            ].copy()
            if meaning in low_meanings:
                pool = pool.sort_values(["share", "n_sentences"], ascending=[True, False])
            else:
                pool = pool.sort_values(["share", "n_sentences"], ascending=[False, False])
            need = int(books_per_cell) - len(chosen)
            extra = pool.head(need).copy()
            if not extra.empty:
                extra["cell_meaning"] = meaning
                chosen = pd.concat([chosen, extra], ignore_index=True)

        if not chosen.empty:
            used_ids.update(int(b) for b in chosen["book_id"].tolist())
            picks.append(chosen)

    if not picks:
        return pd.DataFrame(
            columns=["book_id", "share", "n_sentences", tier_column, "cell_meaning"]
        )

    out = pd.concat(picks, ignore_index=True)
    if max_books is not None and len(out) > max_books:
        out = out.sample(n=max_books, random_state=seed).reset_index(drop=True)
    out.attrs["low_cut"] = low_cut
    out.attrs["high_cut"] = high_cut
    return out


def fetch_topic_sentences(
    sentence_files: Sequence[Path],
    topic_id: int,
    book_ids: Sequence[int],
    *,
    per_book: int,
    threads: int = 4,
    exhaustive: bool = False,
    max_sentences: Optional[int] = None,
    per_tertile: Optional[int] = None,
) -> pd.DataFrame:
    """Pull hard-assigned sentences with normalized position and tertile.

    If ``per_tertile`` is set, rank within (book, tertile) and keep that many
    high-confidence sentences per position (H6 position_x_books design).
    """
    import duckdb

    if not book_ids:
        return pd.DataFrame()

    con = duckdb.connect()
    con.execute(f"pragma threads={threads}")
    files = ", ".join(f"'{f}'" for f in sentence_files)
    book_list = ", ".join(str(int(b)) for b in book_ids)
    tid = int(topic_id)

    if per_tertile is not None:
        rank_sql = f"""
                row_number() over (
                    partition by b.book_id, p.tertile_num
                    order by b.max_topic_prob desc, b.chapter_index, b.sentence_index
                ) as rank_in_slot
        """
        where_rank = f"rank_in_slot <= {int(per_tertile)}"
    else:
        rank_sql = f"""
                row_number() over (
                    partition by b.book_id
                    order by b.max_topic_prob desc, b.chapter_index, b.sentence_index
                ) as rank_in_book
        """
        where_rank = f"rank_in_book <= {int(per_book)}"

    query = f"""
        with base as (
            select
                work_id::bigint as book_id,
                chapter_index::int as chapter_index,
                sentence_index::int as sentence_index,
                sentence,
                topic::int as topic_id,
                max_topic_prob::double as max_topic_prob
            from read_parquet([{files}])
            where work_id in ({book_list})
              and topic = {tid}
        ),
        book_pos as (
            select
                work_id::bigint as book_id,
                chapter_index::int as chapter_index,
                sentence_index::int as sentence_index,
                ntile(3) over (
                    partition by work_id
                    order by chapter_index, sentence_index
                )::tinyint as tertile_num,
                percent_rank() over (
                    partition by work_id
                    order by chapter_index, sentence_index
                )::double as normalized_position
            from read_parquet([{files}])
            where work_id in ({book_list})
        ),
        joined as (
            select
                b.*,
                p.tertile_num,
                p.normalized_position,
                {rank_sql}
            from base b
            left join book_pos p
              on b.book_id = p.book_id
             and b.chapter_index = p.chapter_index
             and b.sentence_index = p.sentence_index
        )
        select *
        from joined
        where {where_rank}
        order by book_id, tertile_num, max_topic_prob desc
    """
    result = con.execute(query).df()
    con.close()

    if result.empty:
        return result

    result["tertile"] = result["tertile_num"].map(TERTILE_MAP)
    if "rank_in_book" not in result.columns and "rank_in_slot" in result.columns:
        result["rank_in_book"] = result["rank_in_slot"]
    if max_sentences is not None and len(result) > max_sentences:
        result = result.head(int(max_sentences)).copy()
    return result


def sample_position_books(
    book_topic_counts: pd.DataFrame,
    topic_id: int,
    *,
    n_books: int = 4,
    seed: int = 42,
    min_sentences: int = 6,
) -> pd.DataFrame:
    """Pick books with enough hard-assigned mass for position-stratified sampling."""
    counts = book_topic_counts[book_topic_counts["topic_id"] == int(topic_id)].copy()
    if counts.empty:
        return pd.DataFrame(columns=["book_id", "share", "n_sentences", "cell_meaning"])
    eligible = counts[counts["n_sentences"] >= int(min_sentences)].copy()
    if eligible.empty:
        eligible = counts[counts["n_sentences"] > 0].copy()
    if eligible.empty:
        return pd.DataFrame(columns=["book_id", "share", "n_sentences", "cell_meaning"])
    take = min(int(n_books), len(eligible))
    chosen = eligible.nlargest(take, "n_sentences").copy()
    # Stable shuffle among top for diversity when many books tie
    chosen = chosen.sample(n=len(chosen), random_state=seed + int(topic_id)).reset_index(drop=True)
    chosen["cell_meaning"] = "position_sample"
    return chosen[["book_id", "share", "n_sentences", "cell_meaning"]]


def _anonymous_book_map(book_ids: Iterable[int]) -> Dict[int, str]:
    unique = sorted({int(b) for b in book_ids})
    return {bid: f"BOOK_{i:03d}" for i, bid in enumerate(unique, start=1)}


def build_evidence_packet(
    cfg: Stage11Config,
    topic_id: int,
    *,
    lookup: pd.DataFrame,
    metadata: Mapping[int, Mapping[str, Any]],
    representative_docs: Mapping[int, Sequence[str]],
    book_topic_counts: pd.DataFrame,
    analysis_frame: pd.DataFrame,
    cell_key: CellKey,
    sentence_files: Optional[Sequence[Path]] = None,
    include_contextual: bool = True,
    sampling_design: Optional[str] = None,
    stage11_codes: Optional[Sequence[str]] = None,
    radway_other_plausible: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """Build one blinded evidence packet for a topic.

    ``sampling_design='position_x_books'`` samples 3–4 books × begin/middle/end
    sentences (H6 Radway day). Ratings stay sealed; Radway/taxonomy reveal in Pass C.
    """
    tid = int(topic_id)
    row = lookup.loc[lookup["topic_id"] == tid]
    if row.empty:
        # Stage07-excluded / unlabeled survivors still need CELL samples for review.
        LOGGER.warning(
            "topic_id %s not in topic_lookup; building unlabeled stub packet", tid
        )
        meta_row = pd.Series(
            {
                "taxonomy_main_id": "unlabeled",
                "taxonomy_main_name": None,
                "taxonomy_secondary_id": None,
                "taxonomy_secondary_name": None,
                "taxonomy_confidence": None,
                "label_rationale": None,
                "radway_main_id": None,
                "radway_main_name": None,
                "radway_secondary_id": None,
                "radway_phase": None,
                "radway_confidence": None,
            }
        )
    else:
        meta_row = row.iloc[0]

    exhaustive_leaves = {str(x) for x in cfg.section("evidence", "exhaustive_leaves")}
    leaf = str(meta_row["taxonomy_main_id"])
    exhaustive = leaf in exhaustive_leaves

    sampling_cfg = cfg.section("evidence", "sampling")
    design = str(sampling_design or sampling_cfg.get("design") or "prevalence_x_rating")
    position_mode = design == "position_x_books"
    # Position mode never uses exhaustive rating×prevalence cells
    if position_mode:
        exhaustive = False

    exh_cfg = cfg.section("evidence", "exhaustive")
    books_per_cell = int(exh_cfg["books_per_cell"] if exhaustive else sampling_cfg["books_per_cell"])
    per_book = int(
        exh_cfg["sentences_per_book_topic"] if exhaustive else sampling_cfg["sentences_per_book_topic"]
    )
    max_books = int(exh_cfg["max_books_per_topic"]) if exhaustive else None
    max_sentences = int(exh_cfg["max_sentences_per_topic"]) if exhaustive else None

    if position_mode:
        n_books = int(sampling_cfg.get("position_n_books", 4))
        per_tertile = int(sampling_cfg.get("position_sentences_per_tertile", 4))
        books_per_cell = n_books
        per_book = per_tertile * 3
        max_books = n_books
        max_sentences = n_books * per_tertile * 3
    else:
        per_tertile = None

    lexical = lexical_block(tid, metadata, representation_names=cfg.section("evidence", "representation_names"))
    stage08_snips = list(lexical.get("stage08_snippets") or [])
    rep_docs = list(representative_docs.get(tid, []))
    if exhaustive:
        seen: Set[str] = set()
        all_snips: List[str] = []
        for text in stage08_snips + rep_docs:
            key = text.strip().lower()
            if key and key not in seen:
                seen.add(key)
                all_snips.append(text.strip())
        stage08_snips = all_snips

    others = list(radway_other_plausible or [])
    sealed_taxonomy = {
        "taxonomy_main_id": leaf,
        "taxonomy_main_name": meta_row.get("taxonomy_main_name"),
        "taxonomy_secondary_id": meta_row.get("taxonomy_secondary_id"),
        "taxonomy_secondary_name": meta_row.get("taxonomy_secondary_name"),
        "taxonomy_confidence": meta_row.get("taxonomy_confidence"),
        "label_rationale": meta_row.get("label_rationale"),
        "radway_main_id": meta_row.get("radway_main_id"),
        "radway_main_name": meta_row.get("radway_main_name"),
        "radway_secondary_id": meta_row.get("radway_secondary_id"),
        "radway_other_plausible_ids": others,
        "radway_phase": meta_row.get("radway_phase"),
        "radway_confidence": meta_row.get("radway_confidence"),
        "stage11_codes": list(stage11_codes or []),
    }

    packet: Dict[str, Any] = {
        "topic_id": tid,
        "exhaustive": exhaustive,
        "taxonomy_leaf_sealed": leaf,
        "lexical": {
            "representations": lexical["representations"],
            "stage08_snippets": stage08_snips,
            "label_public": lexical.get("label_public"),
        },
        "contextual": {
            "sentences": [],
            "books_sampled": [],
            "sampling": {
                "design": design,
                "exhaustive": exhaustive,
                "books_per_cell": books_per_cell,
                "sentences_per_book_topic": per_book,
                "position_sentences_per_tertile": per_tertile,
            },
        },
        "pass_c_reveal": sealed_taxonomy,
        "blinding": {
            "rating_cells": "CELL_A..CELL_D",
            "position_visible": True,
            "taxonomy_hidden_until_pass_c": True,
            "radway_hidden_until_pass_c": True,
        },
    }

    if not include_contextual:
        return packet

    tier_column = str(sampling_cfg["tier_column"])
    if position_mode:
        sampled = sample_position_books(
            book_topic_counts,
            tid,
            n_books=int(sampling_cfg.get("position_n_books", 4)),
            seed=int(sampling_cfg["seed"]) + tid,
            min_sentences=int(sampling_cfg.get("position_min_sentences", 6)),
        )
    else:
        prevalence = _prevalence_frame(
            book_topic_counts, tid, analysis_frame, tier_column=tier_column
        )
        sampled = sample_prevalence_rating_books(
            prevalence,
            tier_column=tier_column,
            tier_high=str(sampling_cfg["tier_high"]),
            tier_low=str(sampling_cfg["tier_low"]),
            quantiles=list(sampling_cfg["prevalence_quantiles"]),
            books_per_cell=books_per_cell,
            seed=int(sampling_cfg["seed"]) + tid,
            max_books=max_books,
        )

    if sampled.empty:
        return packet

    anon = _anonymous_book_map(sampled["book_id"].tolist())
    books_out: List[Dict[str, Any]] = []
    for _, brow in sampled.iterrows():
        record = {
            "book_id_anon": anon[int(brow["book_id"])],
            "book_id_real": int(brow["book_id"]),
            "share": float(brow.get("share", 0.0) or 0.0),
            "n_sentences": int(brow["n_sentences"]),
            "cell_meaning": str(brow.get("cell_meaning") or "position_sample"),
            "rating_class": str(brow[tier_column]) if tier_column in brow.index else "hidden",
        }
        if position_mode:
            # Position packets: no rating cell; use POS_* placeholders
            record["cell"] = f"POS_{record['book_id_anon'].split('_')[-1]}"
        else:
            apply_cell_blind(record, cell_key)
        books_out.append(
            {
                "book_id_anon": record["book_id_anon"],
                "cell": record["cell"],
                "share": record["share"],
                "n_sentences": record["n_sentences"],
                "_book_id_real": record["book_id_real"],
            }
        )

    files = list(sentence_files) if sentence_files is not None else cfg.sentence_topic_files()
    real_ids = [b["_book_id_real"] for b in books_out]
    try:
        sentences = fetch_topic_sentences(
            files,
            tid,
            real_ids,
            per_book=per_book,
            exhaustive=exhaustive,
            max_sentences=max_sentences,
            per_tertile=per_tertile,
        )
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("Sentence fetch failed for topic %s: %s", tid, exc)
        sentences = pd.DataFrame()

    cell_by_real = {b["_book_id_real"]: b["cell"] for b in books_out}
    sent_out: List[Dict[str, Any]] = []
    if not sentences.empty:
        for _, srow in sentences.iterrows():
            bid = int(srow["book_id"])
            tert = srow.get("tertile") or "na"
            rank = int(srow.get("rank_in_book", srow.get("rank_in_slot", 0)) or 0)
            sent_out.append(
                {
                    "sid": f"{anon[bid]}_{tert}_{rank}",
                    "book_id_anon": anon[bid],
                    "cell": cell_by_real.get(bid),
                    "sentence": str(srow["sentence"]),
                    "max_topic_prob": float(srow["max_topic_prob"]),
                    "normalized_position": (
                        float(srow["normalized_position"])
                        if pd.notna(srow.get("normalized_position"))
                        else None
                    ),
                    "tertile": srow.get("tertile"),
                    "chapter_index": int(srow["chapter_index"]) if pd.notna(srow.get("chapter_index")) else None,
                    "sentence_index": int(srow["sentence_index"]) if pd.notna(srow.get("sentence_index")) else None,
                }
            )

    packet["contextual"]["sentences"] = sent_out
    packet["contextual"]["books_sampled"] = [
        {k: v for k, v in b.items() if not k.startswith("_")} for b in books_out
    ]
    packet["contextual"]["sampling"]["n_books"] = len(books_out)
    packet["contextual"]["sampling"]["n_sentences"] = len(sent_out)
    packet["contextual"]["_book_id_map"] = {
        b["book_id_anon"]: b["_book_id_real"] for b in books_out
    }
    return packet


def llm_view(packet: Mapping[str, Any], *, pass_name: str = "B") -> Dict[str, Any]:
    """Strip sealed fields before sending a packet slice to an LLM."""
    view = {
        "topic_id": packet["topic_id"],
        "lexical": {
            "representations": packet["lexical"]["representations"],
            "stage08_snippets": packet["lexical"].get("stage08_snippets", []),
        },
        "contextual": {
            "sentences": packet.get("contextual", {}).get("sentences", []),
            "books_sampled": packet.get("contextual", {}).get("books_sampled", []),
        },
    }
    if pass_name.upper() == "C":
        view["pass_c_reveal"] = packet.get("pass_c_reveal", {})
        view["label_public"] = packet["lexical"].get("label_public")
    return view


def build_evidence_packets(
    cfg: Stage11Config,
    topic_ids: Sequence[int],
    *,
    include_contextual: bool = True,
    progress: bool = True,
) -> Dict[int, Dict[str, Any]]:
    lookup = load_topic_lookup(cfg)
    metadata = load_topic_metadata(cfg)
    rep_docs = load_representative_docs(cfg)
    cell_key = load_or_create_cell_key(cfg)
    seal_cell_key(cfg, cell_key)

    counts_path = cfg.input_path("book_topic_counts", required=True)
    frame_path = cfg.input_path("analysis_frame", required=True)
    assert counts_path is not None and frame_path is not None
    book_topic_counts = pd.read_parquet(counts_path)
    analysis_frame = pd.read_parquet(frame_path, columns=["book_id", "rating_class"])

    sentence_files: Optional[List[Path]] = None
    if include_contextual:
        sentence_files = cfg.sentence_topic_files()

    packets: Dict[int, Dict[str, Any]] = {}
    for i, tid in enumerate(topic_ids, start=1):
        if progress:
            LOGGER.info("[%d/%d] evidence packet topic %s", i, len(topic_ids), tid)
        packets[int(tid)] = build_evidence_packet(
            cfg,
            int(tid),
            lookup=lookup,
            metadata=metadata,
            representative_docs=rep_docs,
            book_topic_counts=book_topic_counts,
            analysis_frame=analysis_frame,
            cell_key=cell_key,
            sentence_files=sentence_files,
            include_contextual=include_contextual,
        )
    return packets


def write_evidence_packets(
    cfg: Stage11Config,
    packets: Mapping[int, Mapping[str, Any]],
) -> Path:
    out_dir = cfg.output_path("evidence_packets_dir", create=True)
    index: List[Dict[str, Any]] = []
    for tid, packet in sorted(packets.items(), key=lambda x: int(x[0])):
        path = out_dir / f"topic_{int(tid):04d}.json"
        # Persist without real book ids in the main blob; keep map in sidecar sealed file.
        public = json.loads(json.dumps(packet, default=str))
        book_map = public.get("contextual", {}).pop("_book_id_map", None)
        path.write_text(json.dumps(public, indent=2, ensure_ascii=False), encoding="utf-8")
        if book_map:
            sealed = out_dir / "sealed" / f"topic_{int(tid):04d}_book_map.json"
            sealed.parent.mkdir(parents=True, exist_ok=True)
            sealed.write_text(json.dumps(book_map, indent=2), encoding="utf-8")
        index.append(
            {
                "topic_id": int(tid),
                "path": str(path.relative_to(cfg.root)),
                "exhaustive": bool(packet.get("exhaustive")),
                "n_sentences": len(packet.get("contextual", {}).get("sentences", [])),
                "n_books": len(packet.get("contextual", {}).get("books_sampled", [])),
            }
        )
    index_path = out_dir / "index.json"
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index_path
