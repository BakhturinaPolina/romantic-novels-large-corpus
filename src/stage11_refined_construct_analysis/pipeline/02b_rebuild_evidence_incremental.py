#!/usr/bin/env python3
"""Incrementally rebuild contextual evidence packets (write each topic as it finishes)."""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage11_refined_construct_analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.evidence.blinding import (  # noqa: E402
    load_or_create_cell_key,
    seal_cell_key,
)
from src.stage11_refined_construct_analysis.evidence.human_review import (  # noqa: E402
    write_human_review_packets,
)
from src.stage11_refined_construct_analysis.evidence.packets import (  # noqa: E402
    build_evidence_packet,
    load_representative_docs,
    load_topic_metadata,
)
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup  # noqa: E402

import pandas as pd  # noqa: E402

LOGGER = logging.getLogger("stage11.evidence_incremental")


def _write_one_packet(cfg, tid: int, packet: dict) -> Path:
    """Write a single packet + sealed book map without clobbering the full index."""
    out_dir = cfg.output_path("evidence_packets_dir", create=True)
    path = out_dir / f"topic_{int(tid):04d}.json"
    public = json.loads(json.dumps(packet, default=str))
    book_map = public.get("contextual", {}).pop("_book_id_map", None)
    path.write_text(json.dumps(public, indent=2, ensure_ascii=False), encoding="utf-8")
    if book_map:
        sealed = out_dir / "sealed" / f"topic_{int(tid):04d}_book_map.json"
        sealed.parent.mkdir(parents=True, exist_ok=True)
        sealed.write_text(json.dumps(book_map, indent=2), encoding="utf-8")
    return path


def _refresh_index(cfg, topic_ids: list[int] | None = None) -> Path:
    """Refresh index for all on-disk packets (optionally ensure topic_ids are included)."""
    out_dir = cfg.output_path("evidence_packets_dir", create=True)
    paths = sorted(out_dir.glob("topic_*.json"))
    if topic_ids is not None:
        wanted = {int(t) for t in topic_ids}
        present = {
            int(p.stem.split("_")[1]) for p in paths if p.stem.startswith("topic_")
        }
        missing = sorted(wanted - present)
        if missing:
            LOGGER.warning("Index refresh: packets still missing for %s", missing)
    index = []
    for path in paths:
        try:
            tid = int(path.stem.split("_")[1])
        except (IndexError, ValueError):
            continue
        packet = json.loads(path.read_text(encoding="utf-8"))
        index.append(
            {
                "topic_id": tid,
                "path": str(path.relative_to(cfg.root)),
                "exhaustive": bool(packet.get("exhaustive")),
                "n_sentences": len(packet.get("contextual", {}).get("sentences", [])),
                "n_books": len(packet.get("contextual", {}).get("books_sampled", [])),
                "design": (packet.get("contextual", {}) or {})
                .get("sampling", {})
                .get("design"),
            }
        )
    index.sort(key=lambda r: r["topic_id"])
    index_path = out_dir / "index.json"
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index_path


def _parse_topic_ids(args: argparse.Namespace) -> list[int]:
    ids: list[int] = []
    if args.topic_ids:
        for chunk in str(args.topic_ids).replace(",", " ").split():
            if chunk.strip():
                ids.append(int(chunk.strip()))
    elif args.topic_ids_file:
        ids = [
            int(x)
            for x in Path(args.topic_ids_file).read_text(encoding="utf-8").split()
            if x.strip()
        ]
    else:
        raise SystemExit("Provide --topic-ids or --topic-ids-file")
    # preserve order, drop dupes
    seen: set[int] = set()
    out: list[int] = []
    for tid in ids:
        if tid not in seen:
            seen.add(tid)
            out.append(tid)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--topic-ids",
        default="",
        help="Comma/space-separated topic IDs (preferred for small rebuilds)",
    )
    parser.add_argument(
        "--topic-ids-file",
        default="",
        help="Whitespace-separated topic ID file (used when --topic-ids is empty)",
    )
    parser.add_argument(
        "--sampling-design",
        default="prevalence_x_rating",
        choices=["prevalence_x_rating", "position_x_books"],
        help="Force packet sampling design (default: prevalence_x_rating)",
    )
    parser.add_argument("--skip-existing-with-sentences", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    if not args.topic_ids and not args.topic_ids_file:
        args.topic_ids_file = (
            "results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/"
            "candidates/audit_topic_ids.txt"
        )
    ids = _parse_topic_ids(args)
    lookup = load_topic_lookup(cfg)
    metadata = load_topic_metadata(cfg)
    rep_docs = load_representative_docs(cfg)
    cell_key = load_or_create_cell_key(cfg)
    seal_cell_key(cfg, cell_key)
    counts = pd.read_parquet(cfg.input_path("book_topic_counts", required=True))
    frame = pd.read_parquet(
        cfg.input_path("analysis_frame", required=True),
        columns=["book_id", "rating_class"],
    )
    sentence_files = cfg.sentence_topic_files()
    out_dir = cfg.output_path("evidence_packets_dir", create=True)
    # Preserve H6 position packets before overwriting with prevalence×rating.
    position_backup = (
        cfg.root
        / "results/stage11_refined_construct_analysis/v4_l12_granular_final_call49"
        / "h6_radway_day/position_packets"
    )

    t0 = time.time()
    done = 0
    with_sents = 0
    for i, tid in enumerate(ids, start=1):
        path = out_dir / f"topic_{int(tid):04d}.json"
        if args.skip_existing_with_sentences and path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
            n = len(existing.get("contextual", {}).get("sentences", []) or [])
            design = (
                (existing.get("contextual") or {}).get("sampling") or {}
            ).get("design")
            # Do not skip position packets when forcing prevalence×rating.
            if n > 0 and (
                args.sampling_design == "position_x_books"
                or design == args.sampling_design
            ):
                LOGGER.info("[%d/%d] skip topic %s (already %d sentences)", i, len(ids), tid, n)
                done += 1
                with_sents += 1
                continue

        if (
            path.exists()
            and args.sampling_design == "prevalence_x_rating"
        ):
            existing = json.loads(path.read_text(encoding="utf-8"))
            design = (
                (existing.get("contextual") or {}).get("sampling") or {}
            ).get("design")
            if design == "position_x_books":
                position_backup.mkdir(parents=True, exist_ok=True)
                bak = position_backup / path.name
                if not bak.exists():
                    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                    LOGGER.info("  preserved position packet → %s", bak)

        LOGGER.info(
            "[%d/%d] building topic %s (design=%s)",
            i,
            len(ids),
            tid,
            args.sampling_design,
        )
        packet = build_evidence_packet(
            cfg,
            int(tid),
            lookup=lookup,
            metadata=metadata,
            representative_docs=rep_docs,
            book_topic_counts=counts,
            analysis_frame=frame,
            cell_key=cell_key,
            sentence_files=sentence_files,
            include_contextual=True,
            sampling_design=args.sampling_design,
        )
        _write_one_packet(cfg, int(tid), packet)
        n = len(packet.get("contextual", {}).get("sentences", []) or [])
        done += 1
        if n > 0:
            with_sents += 1
        elapsed = time.time() - t0
        rate = done / elapsed
        eta = (len(ids) - i) / rate if rate > 0 else -1
        LOGGER.info(
            "  → n_sentences=%d n_books=%d design=%s elapsed=%.0fs ETA≈%.0fs (%.1f/min)",
            n,
            len(packet.get("contextual", {}).get("books_sampled", [])),
            (packet.get("contextual") or {}).get("sampling", {}).get("design"),
            elapsed,
            eta,
            rate * 60,
        )

    index_path = _refresh_index(cfg, ids)
    LOGGER.info("Index refreshed: %s", index_path)

    packets = {}
    for tid in ids:
        path = out_dir / f"topic_{int(tid):04d}.json"
        if path.exists():
            packets[int(tid)] = json.loads(path.read_text(encoding="utf-8"))
    write_human_review_packets(cfg, packets)

    summary = {
        "n_topics": len(ids),
        "n_written": done,
        "n_with_sentences": with_sents,
        "sampling_design": args.sampling_design,
        "elapsed_s": time.time() - t0,
    }
    out_path = cfg.output_path("evidence_packets_dir") / "rebuild_summary.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    LOGGER.info("Done: %s", summary)
    return 0 if with_sents > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
