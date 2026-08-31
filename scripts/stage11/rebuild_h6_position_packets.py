#!/usr/bin/env python3
"""Rebuild position-aware evidence packets for H6 Radway-day new topic IDs."""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import yaml

from src.stage11_refined_construct_analysis.analysis.radway_phases import load_radway_lookup
from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    find_project_root,
    load_stage11_config,
)
from src.stage11_refined_construct_analysis.evidence.blinding import (
    load_or_create_cell_key,
    seal_cell_key,
)
from src.stage11_refined_construct_analysis.evidence.packets import (
    build_evidence_packet,
    load_representative_docs,
    load_topic_metadata,
)

LOGGER = logging.getLogger("stage11.h6_position_packets")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--crosswalk", default="configs/stage11/h6_radway_crosswalk.yaml")
    parser.add_argument(
        "--topic-ids-file",
        default="",
        help="Default: h6_radway_day/h6_new_topic_ids.txt",
    )
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    root = find_project_root()
    cfg = load_stage11_config(args.config)
    cfg.ensure_output_tree()
    cw = yaml.safe_load((root / args.crosswalk).read_text(encoding="utf-8"))
    day = root / cw["paths"]["day_dir"]
    ids_path = Path(args.topic_ids_file) if args.topic_ids_file else day / "h6_new_topic_ids.txt"
    if not ids_path.is_absolute():
        ids_path = root / ids_path
    ids = [int(x) for x in ids_path.read_text(encoding="utf-8").split() if x.strip()]

    lookup = load_radway_lookup(
        root / cw["paths"]["topic_lookup"],
        root / cw["paths"]["taxonomy_with_radway"],
    )
    # Prefer Stage11 config lookup if it has same columns; merge radway extras
    cfg_lookup = pd.read_parquet(cfg.input_path("topic_lookup", required=True))
    for col in (
        "radway_main_id",
        "radway_main_name",
        "radway_secondary_id",
        "radway_phase",
        "radway_confidence",
        "radway_other_plausible_ids",
    ):
        if col in lookup.columns and col not in cfg_lookup.columns:
            cfg_lookup = cfg_lookup.merge(
                lookup[["topic_id", col]], on="topic_id", how="left"
            )
        elif col in lookup.columns:
            cfg_lookup = cfg_lookup.drop(columns=[col], errors="ignore").merge(
                lookup[["topic_id", col]], on="topic_id", how="left"
            )

    cov = json.loads((root / cw["paths"]["construct_coverage"]).read_text(encoding="utf-8"))
    atoms = cov.get("atoms") or {}
    tid_to_codes: dict[int, list[str]] = {}
    for name, meta in atoms.items():
        for tid in meta.get("topic_ids") or []:
            tid_to_codes.setdefault(int(tid), []).append(name)

    other_map = {
        int(r["topic_id"]): list(r.get("radway_other_plausible_ids") or [])
        for _, r in lookup.iterrows()
    }

    metadata = load_topic_metadata(cfg)
    rep_docs = load_representative_docs(cfg)
    cell_key = load_or_create_cell_key(cfg)
    seal_cell_key(cfg, cell_key)
    counts = pd.read_parquet(cfg.input_path("book_topic_counts", required=True))
    frame = pd.read_parquet(
        cfg.input_path("analysis_frame", required=True),
        columns=["book_id", "rating_class"],
    )
    out_dir = cfg.output_path("evidence_packets_dir", create=True)
    day_packets = day / "position_packets"
    day_packets.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    index = []
    for i, tid in enumerate(ids, start=1):
        LOGGER.info("[%d/%d] position packet topic %s", i, len(ids), tid)
        packet = build_evidence_packet(
            cfg,
            tid,
            lookup=cfg_lookup,
            metadata=metadata,
            representative_docs=rep_docs,
            book_topic_counts=counts,
            analysis_frame=frame,
            cell_key=cell_key,
            sentence_files=cfg.sentence_topic_files(),
            include_contextual=True,
            sampling_design="position_x_books",
            stage11_codes=tid_to_codes.get(tid, []),
            radway_other_plausible=other_map.get(tid, []),
        )
        public = json.loads(json.dumps(packet, default=str))
        book_map = public.get("contextual", {}).pop("_book_id_map", None)
        path = out_dir / f"topic_{tid:04d}.json"
        path.write_text(json.dumps(public, indent=2, ensure_ascii=False), encoding="utf-8")
        # Day-local copy
        (day_packets / f"topic_{tid:04d}.json").write_text(
            json.dumps(public, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        if book_map:
            sealed = out_dir / "sealed" / f"topic_{tid:04d}_book_map.json"
            sealed.parent.mkdir(parents=True, exist_ok=True)
            sealed.write_text(json.dumps(book_map, indent=2), encoding="utf-8")
        index.append(
            {
                "topic_id": tid,
                "n_sentences": len(public.get("contextual", {}).get("sentences", [])),
                "n_books": len(public.get("contextual", {}).get("books_sampled", [])),
                "design": "position_x_books",
            }
        )
    (day_packets / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    LOGGER.info("Done %d packets in %.1fs", len(ids), time.time() - t0)
    print(json.dumps({"n_packets": len(ids), "index": index}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
