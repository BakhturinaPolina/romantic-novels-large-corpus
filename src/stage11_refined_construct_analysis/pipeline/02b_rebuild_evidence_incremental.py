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


def _refresh_index(cfg, topic_ids: list[int]) -> Path:
    out_dir = cfg.output_path("evidence_packets_dir", create=True)
    index = []
    for tid in sorted(topic_ids):
        path = out_dir / f"topic_{int(tid):04d}.json"
        if not path.exists():
            continue
        packet = json.loads(path.read_text(encoding="utf-8"))
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--topic-ids-file",
        default="results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/candidates/audit_topic_ids.txt",
    )
    parser.add_argument("--skip-existing-with-sentences", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()

    ids = [
        int(x)
        for x in Path(args.topic_ids_file).read_text(encoding="utf-8").split()
        if x.strip()
    ]
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

    t0 = time.time()
    done = 0
    with_sents = 0
    for i, tid in enumerate(ids, start=1):
        path = out_dir / f"topic_{int(tid):04d}.json"
        if args.skip_existing_with_sentences and path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
            n = len(existing.get("contextual", {}).get("sentences", []) or [])
            if n > 0:
                LOGGER.info("[%d/%d] skip topic %s (already %d sentences)", i, len(ids), tid, n)
                done += 1
                with_sents += 1
                continue

        LOGGER.info("[%d/%d] building topic %s", i, len(ids), tid)
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
            "  → n_sentences=%d n_books=%d elapsed=%.0fs ETA≈%.0fs (%.1f/min)",
            n,
            len(packet.get("contextual", {}).get("books_sampled", [])),
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
        "elapsed_s": time.time() - t0,
    }
    out_path = cfg.output_path("evidence_packets_dir") / "rebuild_summary.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    LOGGER.info("Done: %s", summary)
    return 0 if with_sents > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
