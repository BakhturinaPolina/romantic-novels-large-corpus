"""
Fast character-name extraction with spaCy PERSON entities.

Resumable, incrementally saved alternative to BookNLP:
- processes sentences_train.csv in CSV chunks
- checkpoints chunk index + aggregate token state
- optional per-session chunk limit for overnight runs
- merges token-level names into custom_stoplist.txt when complete
"""

from __future__ import annotations

import csv
import json
import logging
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import click
import pandas as pd
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from src.common.config import get_path, load_config, resolve_path
from src.common.logging import setup_logging

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

TS_FMT = "%Y%m%d_%H%M%S"
STATE_FILE = "spacy_state.json"
CHUNK_CKPT_FILE = "spacy_chunk.ckpt"
NAMES_PER_BOOK_CSV = "names_per_book.csv"
ALL_NAMES_FILE = "all_names_so_far.txt"
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
LOGGER: Optional[logging.Logger] = None

NOISE_TOKENS = {
    "mr",
    "mrs",
    "miss",
    "ms",
    "dr",
    "lady",
    "lord",
    "sir",
    "madam",
    "mister",
}


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def log(message: str) -> None:
    if LOGGER is None:
        print(f"[{_ts()}] {message}", flush=True)
        return
    LOGGER.info(message)


def configure_stage_logger(logs_dir: Path, log_file: str) -> Path:
    global LOGGER
    logger = setup_logging(logs_dir=logs_dir, log_file=log_file)
    logger.name = "stage02_spacy_fast"
    logger.propagate = False
    LOGGER = logger
    return logs_dir / log_file


def _book_id(work_id: int) -> str:
    return f"w{work_id}"


def parse_work_ids_csv(work_ids_csv: str) -> set[int]:
    return {int(x.strip()) for x in work_ids_csv.split(",") if x.strip()}


def parse_work_ids_file(work_ids_file: Path) -> set[int]:
    ids: set[int] = set()
    with open(work_ids_file, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            ids.add(int(s))
    return ids


def normalize_entity_to_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    for m in TOKEN_RE.finditer(text):
        tok = m.group(0).strip("'-").lower()
        if tok:
            tokens.append(tok)
    return tokens


def merge_stoplist(stoplist_path: Path, new_tokens: set[str], run_dir: Path) -> tuple[int, int]:
    existing_lines: list[str] = []
    seen: set[str] = set()
    if stoplist_path.is_file():
        with open(stoplist_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                existing_lines.append(line.rstrip("\n"))
                s = line.strip()
                if s and not s.startswith("#"):
                    seen.add(s)

    append_lines: list[str] = []
    for token in sorted(new_tokens):
        if token and token not in seen and not token.startswith("#"):
            seen.add(token)
            append_lines.append(token)

    stamp = datetime.now(timezone.utc).strftime(TS_FMT)
    if stoplist_path.is_file():
        backup = stoplist_path.parent / f"{stoplist_path.name}.bak_{stamp}"
        shutil.copy2(stoplist_path, backup)
        log(f"Backed up stoplist to {backup}")

    stoplist_path.parent.mkdir(parents=True, exist_ok=True)
    merged = existing_lines + append_lines
    with open(stoplist_path, "w", encoding="utf-8") as f:
        f.write("\n".join(merged))
        if merged:
            f.write("\n")
    log(f"Wrote stoplist {stoplist_path} ({len(append_lines)} new line(s))")

    audit = run_dir / f"custom_stoplist_merged_{stamp}.txt"
    shutil.copy2(stoplist_path, audit)
    log(f"Audit copy: {audit}")
    existing_noncomment = len([x for x in existing_lines if x.strip() and not x.strip().startswith("#")])
    return existing_noncomment, len(append_lines)


def _read_chunk_ckpt(ckpt_path: Path) -> tuple[int, int]:
    """Return (last_completed_chunk_index, rows_scanned). -1 if no checkpoint."""
    if not ckpt_path.is_file():
        return -1, 0
    text = ckpt_path.read_text(encoding="utf-8").strip()
    if not text:
        return -1, 0
    parts = text.split()
    if len(parts) == 1:
        return int(parts[0]), 0
    return int(parts[0]), int(parts[1])


def _write_chunk_ckpt(ckpt_path: Path, chunk_idx: int, rows_scanned: int) -> None:
    ckpt_path.write_text(f"{chunk_idx}\t{rows_scanned}\n", encoding="utf-8")


def _load_state(state_path: Path) -> dict[str, Any]:
    if not state_path.is_file():
        return {
            "global_counts": {},
            "book_presence": {},
            "per_book_person_mentions": {},
            "per_book_token_counts": {},
            "ordered_work_ids": [],
            "rows_scanned": 0,
        }
    data = json.loads(state_path.read_text(encoding="utf-8"))
    data.setdefault("global_counts", {})
    data.setdefault("book_presence", {})
    data.setdefault("per_book_person_mentions", {})
    data.setdefault("per_book_token_counts", {})
    data.setdefault("ordered_work_ids", [])
    data.setdefault("rows_scanned", 0)
    return data


def _save_state(
    state_path: Path,
    global_counts: Counter[str],
    book_presence: dict[str, set[int]],
    per_book_person_mentions: Counter[int],
    per_book_counts: dict[int, Counter[str]],
    ordered_work_ids: list[int],
    rows_scanned: int,
) -> None:
    payload = {
        "updated_utc": _ts(),
        "rows_scanned": rows_scanned,
        "n_books_seen": len(ordered_work_ids),
        "n_unique_tokens_raw": len(global_counts),
        "global_counts": dict(global_counts),
        "book_presence": {k: sorted(v) for k, v in book_presence.items()},
        "per_book_person_mentions": {str(k): v for k, v in per_book_person_mentions.items()},
        "per_book_token_counts": {
            str(wid): dict(cnt) for wid, cnt in per_book_counts.items()
        },
        "ordered_work_ids": ordered_work_ids,
    }
    tmp = state_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload), encoding="utf-8")
    tmp.replace(state_path)


def _restore_counters(state: dict[str, Any]) -> tuple[
    Counter[str],
    dict[str, set[int]],
    Counter[int],
    dict[int, Counter[str]],
    list[int],
    int,
]:
    global_counts = Counter(state.get("global_counts", {}))
    book_presence = {k: set(v) for k, v in state.get("book_presence", {}).items()}
    per_book_person_mentions = Counter(
        {int(k): v for k, v in state.get("per_book_person_mentions", {}).items()}
    )
    per_book_counts: dict[int, Counter[str]] = {}
    for wid_s, tok_map in state.get("per_book_token_counts", {}).items():
        per_book_counts[int(wid_s)] = Counter(tok_map)
    ordered_work_ids = [int(x) for x in state.get("ordered_work_ids", [])]
    rows_scanned = int(state.get("rows_scanned", 0))
    return (
        global_counts,
        book_presence,
        per_book_person_mentions,
        per_book_counts,
        ordered_work_ids,
        rows_scanned,
    )


def _selected_tokens(
    global_counts: Counter[str],
    book_presence: dict[str, set[int]],
    min_global_freq: int,
    min_book_freq: int,
) -> set[str]:
    return {
        token
        for token, count in global_counts.items()
        if count >= min_global_freq and len(book_presence.get(token, set())) >= min_book_freq
    }


def _write_all_names(path: Path, selected: set[str]) -> None:
    sorted_tokens = sorted(selected)
    path.write_text(
        "\n".join(sorted_tokens) + ("\n" if sorted_tokens else ""),
        encoding="utf-8",
    )


def _append_names_per_book_rows(
    csv_path: Path,
    work_ids: list[int],
    per_book_person_mentions: Counter[int],
    per_book_counts: dict[int, Counter[str]],
    selected_tokens: set[str],
) -> None:
    write_header = not csv_path.is_file() or csv_path.stat().st_size == 0
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(
                [
                    "work_id",
                    "book_id",
                    "n_person_mentions",
                    "n_name_tokens_before_freq_filter",
                    "n_name_tokens_after_freq_filter",
                    "ts_utc",
                ]
            )
        for wid in work_ids:
            before = len(per_book_counts.get(wid, {}))
            after = len([t for t in per_book_counts.get(wid, {}) if t in selected_tokens])
            writer.writerow(
                [wid, _book_id(wid), per_book_person_mentions[wid], before, after, _ts()]
            )


def _finalize_outputs(
    run_dir: Path,
    global_counts: Counter[str],
    book_presence: dict[str, set[int]],
    per_book_person_mentions: Counter[int],
    per_book_counts: dict[int, Counter[str]],
    ordered_work_ids: list[int],
    rows_scanned: int,
    min_global_freq: int,
    min_book_freq: int,
    stoplist_path: Path,
    no_merge_stoplist: bool,
) -> dict[str, Any]:
    selected = _selected_tokens(global_counts, book_presence, min_global_freq, min_book_freq)
    _write_all_names(run_dir / ALL_NAMES_FILE, selected)

    names_csv = run_dir / NAMES_PER_BOOK_CSV
    if names_csv.is_file():
        names_csv.unlink()
    _append_names_per_book_rows(
        names_csv,
        ordered_work_ids,
        per_book_person_mentions,
        per_book_counts,
        selected,
    )

    summary = {
        "finished_utc": _ts(),
        "n_rows_scanned": rows_scanned,
        "n_books_selected": len(ordered_work_ids),
        "n_unique_name_tokens_raw": len(global_counts),
        "n_unique_name_tokens_filtered": len(selected),
        "top_tokens_raw": global_counts.most_common(30),
        "complete": True,
    }
    (run_dir / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    merged_manifest: dict[str, Any] = {"n_selected_tokens": len(selected)}
    if no_merge_stoplist:
        log("--no-merge-stoplist set: custom_stoplist.txt not modified.")
        return merged_manifest

    prev_n, appended = merge_stoplist(stoplist_path, selected, run_dir)
    merged_manifest.update(
        {
            "finished_utc": _ts(),
            "stoplist_path": str(stoplist_path),
            "stoplist_existing_nonempty_lines": prev_n,
            "stoplist_appended_lines": appended,
        }
    )
    (run_dir / "merged_manifest.json").write_text(
        json.dumps(merged_manifest, indent=2), encoding="utf-8"
    )
    log("Done.")
    return merged_manifest


@click.command(context_settings={"show_default": True})
@click.option("--config", type=click.Path(exists=True, path_type=Path), default="configs/paths.yaml")
@click.option("--sentences-csv", type=click.Path(path_type=Path), default=None, help="Override sentences_train.csv path")
@click.option(
    "--run-id",
    type=str,
    default=None,
    help="Fixed subdirectory under booknlp_character_runs_parent (reuse for resume)",
)
@click.option("--overwrite-run", is_flag=True, help="Delete run directory if it already exists")
@click.option("--resume", is_flag=True, help="Resume from chunk checkpoint in --run-id directory")
@click.option(
    "--merge-stoplist-only",
    is_flag=True,
    help="Skip extraction; rebuild outputs and merge stoplist from saved spacy_state.json",
)
@click.option("--limit-books", type=int, default=None, help="Process only the first N work_ids encountered")
@click.option("--work-ids", type=str, default=None, help="Comma-separated work_id list to include")
@click.option("--work-ids-file", type=click.Path(exists=True, path_type=Path), default=None)
@click.option("--max-rows", type=int, default=None, help="Read at most this many CSV rows (debug)")
@click.option(
    "--max-chunks-per-run",
    type=int,
    default=None,
    help="Process at most N CSV chunks this session, then exit (for overnight batches)",
)
@click.option("--chunk-size", type=int, default=100_000, help="CSV chunk size")
@click.option("--batch-size", type=int, default=512, help="spaCy nlp.pipe batch size")
@click.option("--n-process", type=int, default=0, help="spaCy n_process for nlp.pipe (0 => os.cpu_count())")
@click.option("--flush-every-chunks", type=int, default=5, help="Save state every N chunks")
@click.option(
    "--heartbeat-every-docs",
    type=int,
    default=0,
    help="Log in-chunk progress every N docs (0 disables heartbeat logs)",
)
@click.option("--min-token-len", type=int, default=3, help="Minimum token length")
@click.option("--min-global-freq", type=int, default=5, help="Minimum total mention count across corpus")
@click.option("--min-book-freq", type=int, default=2, help="Minimum distinct books containing token")
@click.option("--dry-run", is_flag=True, help="Only write run metadata; skip spaCy and stoplist merge")
@click.option("--no-merge-stoplist", is_flag=True, help="Skip updating data/processed/custom_stoplist.txt")
@click.option("--log-file", type=str, default=None, help="Optional log file name under outputs.logs")
@click.option("--no-progress", is_flag=True, help="Disable tqdm progress output")
def main(
    config: Path,
    sentences_csv: Optional[Path],
    run_id: Optional[str],
    overwrite_run: bool,
    resume: bool,
    merge_stoplist_only: bool,
    limit_books: Optional[int],
    work_ids: Optional[str],
    work_ids_file: Optional[Path],
    max_rows: Optional[int],
    max_chunks_per_run: Optional[int],
    chunk_size: int,
    batch_size: int,
    n_process: int,
    flush_every_chunks: int,
    heartbeat_every_docs: int,
    min_token_len: int,
    min_global_freq: int,
    min_book_freq: int,
    dry_run: bool,
    no_merge_stoplist: bool,
    log_file: Optional[str],
    no_progress: bool,
) -> None:
    project_root = Path(__file__).resolve().parents[2]
    cfg = load_config(config)

    sentences_path = sentences_csv
    if sentences_path is None:
        p = cfg.get("inputs", {}).get("sentences_train_csv")
        if p:
            sentences_path = resolve_path(Path(p), project_root)
        else:
            base = get_path(cfg, "inputs", "romance_v2_sentences_dir")
            sentences_path = resolve_path(base, project_root) / "sentences_train.csv"

    runs_parent = resolve_path(get_path(cfg, "inputs", "booknlp_character_runs_parent"), project_root)
    stoplist_path = resolve_path(get_path(cfg, "inputs", "custom_stoplist"), project_root)
    logs_dir = resolve_path(Path(cfg.get("outputs", {}).get("logs", "logs")), project_root)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    run_name = run_id if run_id else f"spacy_fast_{stamp}"
    run_dir = runs_parent / run_name
    logfile_name = log_file if log_file else f"stage02_spacy_fast_{run_name}.log"
    log_path = configure_stage_logger(logs_dir=logs_dir, log_file=logfile_name)

    if run_dir.exists() and overwrite_run:
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    state_path = run_dir / STATE_FILE
    ckpt_path = run_dir / CHUNK_CKPT_FILE

    if work_ids and work_ids_file:
        raise click.ClickException("Use only one of --work-ids or --work-ids-file.")
    work_ids_filter: Optional[set[int]] = None
    if work_ids:
        work_ids_filter = parse_work_ids_csv(work_ids)
    if work_ids_file:
        work_ids_filter = parse_work_ids_file(work_ids_file)

    n_proc = n_process if n_process > 0 else max(1, os.cpu_count() or 1)
    log(f"Project root: {project_root}")
    log(f"Sentences CSV: {sentences_path}")
    log(f"Run directory: {run_dir}")
    log(f"Log file: {log_path}")

    if merge_stoplist_only:
        if not state_path.is_file():
            raise click.ClickException(f"Missing {state_path}; run extraction first.")
        state = _load_state(state_path)
        (
            global_counts,
            book_presence,
            per_book_person_mentions,
            per_book_counts,
            ordered_work_ids,
            rows_scanned,
        ) = _restore_counters(state)
        log(
            f"merge-stoplist-only: rows_scanned={rows_scanned:,}, "
            f"books={len(ordered_work_ids):,}, raw_tokens={len(global_counts):,}"
        )
        _finalize_outputs(
            run_dir,
            global_counts,
            book_presence,
            per_book_person_mentions,
            per_book_counts,
            ordered_work_ids,
            rows_scanned,
            min_global_freq,
            min_book_freq,
            stoplist_path,
            no_merge_stoplist,
        )
        return

    auto_resume = resume or (state_path.is_file() and ckpt_path.is_file())
    start_chunk = -1
    if auto_resume and not overwrite_run:
        start_chunk, _ = _read_chunk_ckpt(ckpt_path)
        log(f"Resume: will skip chunks 0..{start_chunk} (inclusive)")

    manifest: dict[str, Any] = {
        "created_utc": _ts(),
        "sentences_csv": str(sentences_path),
        "run_name": run_name,
        "chunk_size": chunk_size,
        "batch_size": batch_size,
        "n_process": n_proc,
        "flush_every_chunks": flush_every_chunks,
        "heartbeat_every_docs": heartbeat_every_docs,
        "max_chunks_per_run": max_chunks_per_run,
        "min_token_len": min_token_len,
        "min_global_freq": min_global_freq,
        "min_book_freq": min_book_freq,
        "work_ids_filter_size": 0 if work_ids_filter is None else len(work_ids_filter),
        "limit_books": limit_books,
        "max_rows": max_rows,
        "dry_run": dry_run,
        "resume": auto_resume,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if dry_run:
        log("Dry run: stopping before spaCy extraction.")
        return

    (
        global_counts,
        book_presence,
        per_book_person_mentions,
        per_book_counts,
        ordered_work_ids,
        rows_scanned,
    ) = _restore_counters(_load_state(state_path)) if auto_resume else (
        Counter(),
        defaultdict(set),
        Counter(),
        defaultdict(Counter),
        [],
        0,
    )
    seen_wids: set[int] = set(ordered_work_ids)
    excluded_by_limit: set[int] = set()

    log("Loading spaCy model en_core_web_sm (parser/lemmatizer/tagger disabled)...")
    try:
        nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer", "tagger"])
    except OSError as e:
        raise click.ClickException(
            "spaCy model 'en_core_web_sm' is not installed. Run: python -m spacy download en_core_web_sm"
        ) from e

    reader = pd.read_csv(
        sentences_path,
        usecols=["work_id", "sentence"],
        chunksize=max(1, chunk_size),
        dtype={"work_id": "int64"},
    )
    iterator = reader
    if not no_progress and tqdm is not None:
        iterator = tqdm(reader, desc="spaCy chunks", unit="chunk")

    chunks_this_session = 0
    session_complete = False
    chunk_idx = start_chunk

    for chunk_idx, chunk in enumerate(iterator):
        if chunk_idx <= start_chunk:
            continue
        if max_chunks_per_run is not None and chunks_this_session >= max_chunks_per_run:
            log(
                f"Reached --max-chunks-per-run={max_chunks_per_run}; "
                "saving state and exiting (resume later with same --run-id)."
            )
            break
        if max_rows is not None and rows_scanned >= max_rows:
            session_complete = True
            break
        if max_rows is not None and rows_scanned + len(chunk) > max_rows:
            chunk = chunk.iloc[: max_rows - rows_scanned].copy()
        if chunk.empty:
            continue

        docs: list[str] = []
        doc_wids: list[int] = []
        for row in chunk.itertuples(index=False):
            wid = int(row.work_id)
            if work_ids_filter is not None and wid not in work_ids_filter:
                continue
            if wid not in seen_wids:
                if limit_books is not None and len(ordered_work_ids) >= limit_books:
                    excluded_by_limit.add(wid)
                    continue
                ordered_work_ids.append(wid)
                seen_wids.add(wid)
            if wid in excluded_by_limit:
                continue

            sentence = str(row.sentence).strip()
            if not sentence:
                continue
            docs.append(sentence)
            doc_wids.append(wid)

        if docs:
            total_docs = len(docs)
            log(f"Chunk {chunk_idx}: starting PERSON extraction for {total_docs:,} docs")
            for doc_idx, (wid, doc) in enumerate(
                zip(doc_wids, nlp.pipe(docs, batch_size=batch_size, n_process=n_proc)),
                start=1,
            ):
                for ent in doc.ents:
                    if ent.label_ != "PERSON":
                        continue
                    per_book_person_mentions[wid] += 1
                    for token in normalize_entity_to_tokens(ent.text):
                        if len(token) < min_token_len:
                            continue
                        if token in NOISE_TOKENS:
                            continue
                        if token in ENGLISH_STOP_WORDS:
                            continue
                        if not any(ch.isalpha() for ch in token):
                            continue
                        global_counts[token] += 1
                        book_presence[token].add(wid)
                        per_book_counts[wid][token] += 1
                if heartbeat_every_docs > 0 and (
                    doc_idx % heartbeat_every_docs == 0 or doc_idx == total_docs
                ):
                    pct = (doc_idx / total_docs) * 100
                    log(
                        f"Chunk {chunk_idx}: processed {doc_idx:,}/{total_docs:,} docs "
                        f"({pct:.1f}%)"
                    )

        rows_scanned += len(chunk)
        chunks_this_session += 1

        if flush_every_chunks > 0 and chunks_this_session % flush_every_chunks == 0:
            _save_state(
                state_path,
                global_counts,
                book_presence,
                per_book_person_mentions,
                per_book_counts,
                ordered_work_ids,
                rows_scanned,
            )
            _write_chunk_ckpt(ckpt_path, chunk_idx, rows_scanned)
            selected = _selected_tokens(
                global_counts, book_presence, min_global_freq, min_book_freq
            )
            _write_all_names(run_dir / ALL_NAMES_FILE, selected)
            log(
                f"Checkpoint chunk={chunk_idx} rows_scanned={rows_scanned:,} "
                f"raw_tokens={len(global_counts):,} filtered_tokens={len(selected):,}"
            )

        if max_rows is not None and rows_scanned >= max_rows:
            session_complete = True
            break
    else:
        session_complete = True

    if not ordered_work_ids and not global_counts:
        raise click.ClickException("No matching rows/books selected from input CSV.")

    _save_state(
        state_path,
        global_counts,
        book_presence,
        per_book_person_mentions,
        per_book_counts,
        ordered_work_ids,
        rows_scanned,
    )
    last_chunk = chunk_idx if chunks_this_session > 0 else start_chunk
    _write_chunk_ckpt(ckpt_path, last_chunk, rows_scanned)
    selected = _selected_tokens(global_counts, book_presence, min_global_freq, min_book_freq)
    _write_all_names(run_dir / ALL_NAMES_FILE, selected)

    partial_summary = {
        "updated_utc": _ts(),
        "n_rows_scanned": rows_scanned,
        "n_books_selected": len(ordered_work_ids),
        "n_unique_name_tokens_raw": len(global_counts),
        "n_unique_name_tokens_filtered": len(selected),
        "complete": session_complete,
        "last_chunk_index": last_chunk,
    }
    (run_dir / "run_summary.json").write_text(json.dumps(partial_summary, indent=2), encoding="utf-8")

    if session_complete:
        _finalize_outputs(
            run_dir,
            global_counts,
            book_presence,
            per_book_person_mentions,
            per_book_counts,
            ordered_work_ids,
            rows_scanned,
            min_global_freq,
            min_book_freq,
            stoplist_path,
            no_merge_stoplist,
        )
    else:
        log(
            f"Paused after {chunks_this_session} chunk(s) this session. "
            f"Resume with: --run-id {run_name} --resume"
        )


if __name__ == "__main__":
    main()
