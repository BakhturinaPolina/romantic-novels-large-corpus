#!/usr/bin/env python3
"""Estimate live ETA for stage02 spaCy-fast character extraction runs."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

TS_FMT = "%Y-%m-%d %H:%M:%S,%f"

CHECKPOINT_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}).*?Checkpoint chunk=(?P<chunk>\d+)\s+rows_scanned=(?P<rows>[\d,]+)"
)
PROGRESS_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}).*?Chunk (?P<chunk>\d+): processed (?P<done>[\d,]+)/(?P<total>[\d,]+) docs"
)


@dataclass(frozen=True)
class Checkpoint:
    ts: datetime
    chunk_idx: int
    rows_scanned: int


@dataclass(frozen=True)
class Progress:
    ts: datetime
    chunk_idx: int
    docs_done: int
    docs_total: int


def parse_ts(s: str) -> datetime:
    return datetime.strptime(s, TS_FMT)


def parse_checkpoints(lines: Iterable[str]) -> list[Checkpoint]:
    out: list[Checkpoint] = []
    for line in lines:
        m = CHECKPOINT_RE.search(line)
        if not m:
            continue
        out.append(
            Checkpoint(
                ts=parse_ts(m.group("ts")),
                chunk_idx=int(m.group("chunk")),
                rows_scanned=int(m.group("rows").replace(",", "")),
            )
        )
    return out


def parse_latest_progress(lines: Iterable[str]) -> Progress | None:
    latest: Progress | None = None
    for line in lines:
        m = PROGRESS_RE.search(line)
        if not m:
            continue
        latest = Progress(
            ts=parse_ts(m.group("ts")),
            chunk_idx=int(m.group("chunk")),
            docs_done=int(m.group("done").replace(",", "")),
            docs_total=int(m.group("total").replace(",", "")),
        )
    return latest


def count_rows(csv_path: Path, has_header: bool) -> int:
    line_count = 0
    with csv_path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            line_count += block.count(b"\n")
    if has_header and line_count > 0:
        return line_count - 1
    return line_count


def estimate_current_rows(
    ckpt_rows: int,
    ckpt_chunk: int,
    latest_progress: Progress | None,
) -> int:
    if latest_progress is None:
        return ckpt_rows
    if latest_progress.chunk_idx == ckpt_chunk + 1:
        return ckpt_rows + latest_progress.docs_done
    if latest_progress.chunk_idx <= ckpt_chunk:
        return ckpt_rows
    return ckpt_rows


def rate_from_checkpoints(checkpoints: list[Checkpoint], window: int) -> float | None:
    if len(checkpoints) < 2:
        return None
    use_count = min(len(checkpoints), max(2, window + 1))
    selected = checkpoints[-use_count:]
    delta_rows = selected[-1].rows_scanned - selected[0].rows_scanned
    delta_s = (selected[-1].ts - selected[0].ts).total_seconds()
    if delta_rows <= 0 or delta_s <= 0:
        return None
    return delta_rows / delta_s


def human_duration(seconds: float) -> str:
    seconds = int(max(0, round(seconds)))
    d, rem = divmod(seconds, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    if d > 0:
        return f"{d}d {h}h {m}m"
    if h > 0:
        return f"{h}h {m}m"
    if m > 0:
        return f"{m}m {s}s"
    return f"{s}s"


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="spacy_fast_full")
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Default: logs/stage02_spacy_fast_<run-id>.log",
    )
    parser.add_argument(
        "--ckpt-file",
        type=Path,
        default=None,
        help="Default: data/interim/booknlp_character_runs/<run-id>/spacy_chunk.ckpt",
    )
    parser.add_argument(
        "--sentences-csv",
        type=Path,
        default=root / "data/processed/romance_subdataset_downloaded_v2_sentences/sentences_train.csv",
    )
    parser.add_argument(
        "--checkpoint-window",
        type=int,
        default=3,
        help="Number of most recent checkpoint intervals for rolling throughput.",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Treat CSV as headerless when counting total rows.",
    )
    args = parser.parse_args()

    log_path = args.log_file or (root / f"logs/stage02_spacy_fast_{args.run_id}.log")
    ckpt_path = args.ckpt_file or (
        root / f"data/interim/booknlp_character_runs/{args.run_id}/spacy_chunk.ckpt"
    )
    csv_path = args.sentences_csv

    if not log_path.is_file():
        raise SystemExit(f"Missing log file: {log_path}")
    if not ckpt_path.is_file():
        raise SystemExit(f"Missing checkpoint file: {ckpt_path}")
    if not csv_path.is_file():
        raise SystemExit(f"Missing sentences CSV: {csv_path}")

    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    checkpoints = parse_checkpoints(lines)
    if not checkpoints:
        raise SystemExit(f"No checkpoint entries found in log: {log_path}")

    ckpt_text = ckpt_path.read_text(encoding="utf-8").strip().split()
    if not ckpt_text:
        raise SystemExit(f"Checkpoint file is empty: {ckpt_path}")
    ckpt_chunk = int(ckpt_text[0])
    ckpt_rows = int(ckpt_text[1]) if len(ckpt_text) > 1 else 0

    latest_progress = parse_latest_progress(lines)
    current_rows = estimate_current_rows(ckpt_rows, ckpt_chunk, latest_progress)
    total_rows = count_rows(csv_path, has_header=not args.no_header)
    remaining_rows = max(0, total_rows - current_rows)
    pct = (current_rows / total_rows * 100.0) if total_rows else 0.0

    rate_rows_per_s = rate_from_checkpoints(checkpoints, args.checkpoint_window)
    now = datetime.now()

    print(f"run_id: {args.run_id}")
    print(f"log_file: {log_path}")
    print(f"ckpt_file: {ckpt_path}")
    print(f"sentences_csv: {csv_path}")
    print()
    print(f"progress_rows: {current_rows:,}/{total_rows:,} ({pct:.2f}%)")
    print(f"remaining_rows: {remaining_rows:,}")
    print(
        f"latest_checkpoint: chunk={ckpt_chunk}, rows_scanned={ckpt_rows:,}, ts={checkpoints[-1].ts.isoformat(sep=' ')}"
    )
    if latest_progress is not None:
        print(
            "latest_in_chunk: "
            f"chunk={latest_progress.chunk_idx}, docs={latest_progress.docs_done:,}/{latest_progress.docs_total:,}, "
            f"ts={latest_progress.ts.isoformat(sep=' ')}"
        )
    if rate_rows_per_s is None:
        print("throughput_rows_per_s: unavailable (need >=2 checkpoints)")
        return

    eta_seconds = remaining_rows / rate_rows_per_s if rate_rows_per_s > 0 else float("inf")
    finish_at = now + timedelta(seconds=eta_seconds)
    print(f"throughput_rows_per_s: {rate_rows_per_s:.2f}")
    print(f"eta_remaining: {human_duration(eta_seconds)}")
    print(f"eta_finish_local: {finish_at.isoformat(sep=' ', timespec='seconds')}")


if __name__ == "__main__":
    main()
