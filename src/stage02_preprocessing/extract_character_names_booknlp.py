"""
Build per-book UTF-8 .txt files from sentences_train.csv, run BookNLP (GPU via
PyTorch), extract person-name strings from .entities (and .book when available),
and merge into custom_stoplist.txt with a timestamped backup.

Default pipeline is entity (fast mode). Use entity,quote,coref for full outputs.

Usage (from repo root):
  python -m src.stage02_preprocessing.extract_character_names_booknlp --config configs/paths.yaml
  python -m src.stage02_preprocessing.extract_character_names_booknlp --plan-shards --num-shards 4
  python -m src.stage02_preprocessing.extract_character_names_booknlp --estimate-eta --eta-sample-books 50
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import csv
import gzip
import json
import logging
import math
import os
import random
import shlex
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import click
import pandas as pd
from src.common.logging import setup_logging

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover
    tqdm = None


def _load_config_module(project_root: Path):
    """Load ``src.common.config`` without importing ``src.common`` (avoids torch via package __init__)."""
    path = project_root / "src" / "common" / "config.py"
    spec = importlib.util.spec_from_file_location("stage02_config_loader", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load config module from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

TS_FMT = "%Y%m%d_%H%M%S"
LOGGER: Optional[logging.Logger] = None


class _TqdmLoggingHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        if tqdm is None:
            return
        try:
            msg = self.format(record)
            tqdm.write(msg)
        except Exception:
            self.handleError(record)


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def log(msg: str) -> None:
    if LOGGER is None:
        print(f"[{_ts()}] {msg}", flush=True)
        return
    level = logging.INFO
    if msg.startswith("WARN:"):
        level = logging.WARNING
    elif msg.startswith("ERROR:"):
        level = logging.ERROR
    LOGGER.log(level, msg)


def configure_stage_logger(logs_dir: Path, log_file: str, use_tqdm_progress: bool) -> Path:
    global LOGGER
    logger = setup_logging(logs_dir=logs_dir, log_file=log_file)
    logger.name = "stage02_preprocessing"
    logger.propagate = False
    for handler in list(logger.handlers):
        if isinstance(handler, logging.StreamHandler) and not isinstance(
            handler, logging.FileHandler
        ):
            logger.removeHandler(handler)
    if use_tqdm_progress and tqdm is not None:
        console_handler = _TqdmLoggingHandler()
    else:
        console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s"))
    logger.addHandler(console_handler)
    LOGGER = logger
    return logs_dir / log_file


def _init_booknlp_with_compat(BookNLP: Any, model_params: Dict[str, Any], torch_mod: Any) -> Any:
    """Initialize BookNLP with a compatibility retry for legacy checkpoint keys."""
    try:
        return BookNLP("en", model_params)
    except RuntimeError as e:
        msg = str(e)
        if "position_ids" not in msg:
            raise
        log(
            "WARN: BookNLP model compatibility mismatch detected "
            "(unexpected position_ids). Retrying with non-strict state loading."
        )
        original_load_state_dict = torch_mod.nn.Module.load_state_dict

        def _compat_load_state_dict(self: Any, state_dict: Dict[str, Any], *args: Any, **kwargs: Any):
            if "strict" not in kwargs:
                kwargs["strict"] = False
            return original_load_state_dict(self, state_dict, *args, **kwargs)

        torch_mod.nn.Module.load_state_dict = _compat_load_state_dict
        try:
            return BookNLP("en", model_params)
        finally:
            torch_mod.nn.Module.load_state_dict = original_load_state_dict


def _package_version(name: str) -> Optional[str]:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _git_head(project_root: Path) -> Optional[str]:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(project_root),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


def _read_completed_ckpt(ckpt: Path) -> Set[int]:
    if not ckpt.is_file():
        return set()
    done: Set[int] = set()
    with open(ckpt, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                done.add(int(line))
            except ValueError:
                log(f"WARN: skip bad ckpt line: {line!r}")
    return done


def _append_ckpt(ckpt: Path, work_id: int) -> None:
    with open(ckpt, "a", encoding="utf-8") as f:
        f.write(f"{work_id}\n")
        f.flush()
        os.fsync(f.fileno())


def _book_id(work_id: int) -> str:
    return f"w{work_id}"


def _pipeline_needs_book_json(pipeline: str) -> bool:
    parts = {x.strip() for x in pipeline.split(",") if x.strip()}
    return "quote" in parts or "coref" in parts


def _artifacts_ok(out_dir: Path, book_id: str, need_book_json: bool) -> bool:
    book_p = out_dir / f"{book_id}.book"
    ent_p = out_dir / f"{book_id}.entities"
    if not ent_p.is_file():
        return False
    if need_book_json and not book_p.is_file():
        return False
    if ent_p.stat().st_size < 20:
        return False
    if need_book_json and book_p.stat().st_size < 3:
        return False
    return True


def parse_work_ids_csv(work_ids_csv: str) -> Set[int]:
    return {int(x.strip()) for x in work_ids_csv.split(",") if x.strip()}


def parse_work_ids_file(work_ids_file: Path) -> Set[int]:
    ids: Set[int] = set()
    with open(work_ids_file, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            ids.add(int(s))
    return ids


def collect_ordered_work_ids(
    sentences_csv: Path,
    max_rows: Optional[int],
    chunk_size: int,
    work_ids_filter: Optional[Set[int]],
    limit_books: Optional[int],
) -> Tuple[List[int], int]:
    if not sentences_csv.is_file():
        raise FileNotFoundError(f"Missing sentences CSV: {sentences_csv}")
    ordered_wids: List[int] = []
    seen: Set[int] = set()
    total_rows = 0
    reader = pd.read_csv(
        sentences_csv,
        usecols=["work_id"],
        chunksize=max(chunk_size, 250_000),
        dtype={"work_id": "int64"},
    )
    for chunk in reader:
        if max_rows is not None and total_rows >= max_rows:
            break
        if max_rows is not None and total_rows + len(chunk) > max_rows:
            chunk = chunk.iloc[: max_rows - total_rows].copy()
        if chunk.empty:
            continue
        total_rows += len(chunk)
        for wid in chunk["work_id"].tolist():
            wid_i = int(wid)
            if wid_i in seen:
                continue
            if work_ids_filter is not None and wid_i not in work_ids_filter:
                continue
            ordered_wids.append(wid_i)
            seen.add(wid_i)
            if limit_books is not None and len(ordered_wids) >= limit_books:
                return ordered_wids, total_rows
    return ordered_wids, total_rows


def split_work_ids_into_shards(work_ids: List[int], num_shards: int) -> List[List[int]]:
    shards: List[List[int]] = [[] for _ in range(num_shards)]
    for idx, wid in enumerate(work_ids):
        shards[idx % num_shards].append(wid)
    return shards


def work_ids_from_txt_input_dir(txt_dir: Path) -> List[int]:
    wids: List[int] = []
    for path in sorted(txt_dir.glob("w*.txt")):
        stem = path.stem
        if stem.startswith("w") and stem[1:].isdigit():
            wids.append(int(stem[1:]))
    return wids


def txt_byte_sizes_for_work_ids(txt_dir: Path, work_ids: Iterable[int]) -> Dict[int, int]:
    sizes: Dict[int, int] = {}
    for wid in work_ids:
        path = txt_dir / f"{_book_id(wid)}.txt"
        if path.is_file() and path.stat().st_size > 0:
            sizes[wid] = int(path.stat().st_size)
    return sizes


def stratified_sample_work_ids_by_length(
    txt_dir: Path,
    candidate_wids: List[int],
    n: int,
    seed: int,
    n_bins: int = 10,
) -> Tuple[List[int], Dict[str, Any]]:
    """Pick N work_ids with approximate length stratification (txt byte size proxy)."""
    if n <= 0:
        raise ValueError("n must be positive")
    pool = [w for w in candidate_wids if (txt_dir / f"{_book_id(w)}.txt").is_file()]
    if not pool:
        raise ValueError("No candidate work_ids with txt files for stratified sampling")
    if n >= len(pool):
        return sorted(pool), {
            "n_requested": n,
            "n_selected": len(pool),
            "n_pool": len(pool),
            "truncated_to_all": True,
            "seed": seed,
            "n_bins": 0,
        }

    sizes = txt_byte_sizes_for_work_ids(txt_dir, pool)
    pool = [w for w in pool if w in sizes]
    df = pd.DataFrame({"work_id": pool, "txt_bytes": [sizes[w] for w in pool]})
    n_bins_eff = max(2, min(n_bins, n, len(df) // 5))
    df["length_bin"] = pd.qcut(df["txt_bytes"], q=n_bins_eff, duplicates="drop")
    rng = random.Random(seed)
    selected: List[int] = []
    bin_counts: Dict[str, int] = {}
    groups = list(df.groupby("length_bin", observed=True))
    per_bin = max(1, n // len(groups))
    remainder = n
    for _bin, sub in groups:
        take = min(per_bin, len(sub), remainder)
        if take <= 0:
            continue
        bin_ids = [int(x) for x in sub["work_id"].tolist()]
        picks = rng.sample(bin_ids, take)
        selected.extend(picks)
        bin_counts[str(_bin)] = take
        remainder -= take
    if remainder > 0:
        remaining = df[~df["work_id"].isin(selected)]
        if not remaining.empty:
            extra = remaining.sample(n=min(remainder, len(remaining)), random_state=seed + 1)
            selected.extend(int(x) for x in extra["work_id"].tolist())
    selected = sorted(set(selected))[:n]
    meta = {
        "n_requested": n,
        "n_selected": len(selected),
        "n_pool": len(pool),
        "seed": seed,
        "n_bins": n_bins_eff,
        "per_bin_target": per_bin,
        "bin_counts": bin_counts,
        "txt_bytes_min": int(df["txt_bytes"].min()),
        "txt_bytes_median": int(df["txt_bytes"].median()),
        "txt_bytes_max": int(df["txt_bytes"].max()),
    }
    return selected, meta


def build_txts_per_work_id_incremental(
    sentences_csv: Path,
    max_rows: Optional[int],
    streaming: bool,
    chunk_size: int,
    txt_dir: Path,
    work_ids_filter: Optional[Set[int]],
    limit_books: Optional[int],
    reuse_existing: bool,
) -> Tuple[List[int], int]:
    usecols = ["work_id", "chapter_index", "sentence_index", "sentence"]
    if not sentences_csv.is_file():
        raise FileNotFoundError(f"Missing sentences CSV: {sentences_csv}")
    txt_dir.mkdir(parents=True, exist_ok=True)
    ordered_wids: List[int] = []
    seen_wids: Set[int] = set()
    excluded_by_limit: Set[int] = set()
    total_rows = 0
    per_work_state: Dict[int, Dict[str, Any]] = defaultdict(
        lambda: {"last_chapter": None, "wrote_any": False}
    )
    forced_rewrite: Set[int] = set()
    reused_wids: Set[int] = set()
    effective_chunk_size = chunk_size if streaming else max(chunk_size, 250_000)
    progress_every = max(50_000, effective_chunk_size)
    log(f"Streaming sentences CSV: {sentences_csv}")
    log(f"Materializing txt_input incrementally to: {txt_dir}")
    mode_label = "streaming" if streaming else "incremental-default"
    log(f"CSV ingestion mode={mode_label}, chunk_size={effective_chunk_size:,}")

    reader = pd.read_csv(
        sentences_csv,
        usecols=usecols,
        chunksize=effective_chunk_size,
        dtype={"work_id": "int64", "chapter_index": "int64", "sentence_index": "int64"},
    )

    for chunk_idx, chunk in enumerate(reader, start=1):
        if max_rows is not None and total_rows >= max_rows:
            break
        if max_rows is not None and total_rows + len(chunk) > max_rows:
            chunk = chunk.iloc[: max_rows - total_rows].copy()
        if chunk.empty:
            continue

        chunk = chunk.sort_values(
            ["work_id", "chapter_index", "sentence_index"],
            kind="mergesort",
        )
        total_rows += len(chunk)

        for wid, sub in chunk.groupby("work_id", sort=False):
            wid_i = int(wid)
            if work_ids_filter is not None and wid_i not in work_ids_filter:
                continue

            if wid_i not in seen_wids:
                if limit_books is not None and len(ordered_wids) >= limit_books:
                    excluded_by_limit.add(wid_i)
                    continue
                ordered_wids.append(wid_i)
                seen_wids.add(wid_i)
            if wid_i in excluded_by_limit:
                continue

            bid = _book_id(wid_i)
            out_path = txt_dir / f"{bid}.txt"
            state = per_work_state[wid_i]
            if (
                reuse_existing
                and not state["wrote_any"]
                and out_path.is_file()
                and out_path.stat().st_size > 0
            ):
                if wid_i not in reused_wids:
                    log(
                        f"Reusing existing txt_input/{out_path.name} ({out_path.stat().st_size} bytes)"
                    )
                    reused_wids.add(wid_i)
                continue

            if wid_i not in forced_rewrite:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                if out_path.exists():
                    out_path.unlink()
                forced_rewrite.add(wid_i)

            pieces: List[str] = []
            last_chapter = state["last_chapter"]
            wrote_any = state["wrote_any"]
            for row in sub.itertuples(index=False):
                ch = int(row.chapter_index)
                sent = str(row.sentence).replace("\r\n", "\n").replace("\r", "\n").strip()
                if wrote_any:
                    pieces.append("\n\n" if ch != last_chapter else "\n")
                pieces.append(sent)
                wrote_any = True
                last_chapter = ch

            if pieces:
                text = "".join(pieces)
                if not text.endswith("\n"):
                    text += "\n"
                with open(out_path, "a", encoding="utf-8") as f:
                    f.write(text)
                state["wrote_any"] = wrote_any
                state["last_chapter"] = last_chapter

        if total_rows % progress_every < len(chunk):
            log(
                f"CSV scan progress: {total_rows:,} rows, {len(ordered_wids):,} work_id(s) selected, chunk={chunk_idx}"
            )

    if total_rows == 0:
        return [], 0
    log(f"Loaded {total_rows:,} sentence rows and built {len(ordered_wids):,} txt_input file(s)")
    return ordered_wids, total_rows


def names_from_book_json(data: Dict[str, Any], also_nom_per: bool) -> Set[str]:
    names: Set[str] = set()
    for ch in data.get("characters", []) or []:
        mentions = ch.get("mentions") or {}
        for item in mentions.get("proper", []) or []:
            n = (item.get("n") or "").strip()
            if n:
                names.add(n)
        if also_nom_per:
            for item in mentions.get("common", []) or []:
                n = (item.get("n") or "").strip()
                if n:
                    names.add(n)
    return names


def names_from_entities_file(entities_path: Path, also_nom_per: bool) -> Set[str]:
    names: Set[str] = set()
    with open(entities_path, "r", encoding="utf-8", errors="replace") as f:
        header = f.readline()
        if not header:
            return names
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 6:
                continue
            prop, cat, text = parts[3], parts[4], parts[5]
            if cat != "PER":
                continue
            if prop == "PROP" or (also_nom_per and prop == "NOM"):
                t = text.strip()
                if t:
                    names.add(t)
    return names


def write_character_summary_json(book_path: Path, summary_path: Path) -> None:
    with open(book_path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    slim: Dict[str, Any] = {"characters": []}
    for ch in data.get("characters", []) or []:
        slim["characters"].append(
            {
                "id": ch.get("id"),
                "count": ch.get("count"),
                "mentions": ch.get("mentions"),
            }
        )
    summary_path.write_text(json.dumps(slim, ensure_ascii=False, indent=2), encoding="utf-8")


def export_per_free_tokens_gz(tokens_path: Path, gzip_path: Path) -> int:
    """Write gzipped CSV: token_ID_within_document,lemma for non-PER, non-PUNCT."""
    n = 0
    with open(tokens_path, "r", encoding="utf-8", errors="replace") as inp, gzip.open(
        gzip_path, "wt", encoding="utf-8", newline=""
    ) as out:
        w = csv.writer(out)
        w.writerow(["token_ID_within_document", "lemma", "POS_tag", "fine_POS_tag"])
        header = inp.readline()
        if not header:
            return 0
        cols = header.strip().split("\t")
        try:
            i_tid = cols.index("token_ID_within_document")
            i_lem = cols.index("lemma")
            i_pos = cols.index("POS_tag")
            i_fine = cols.index("fine_POS_tag")
        except ValueError:
            log("WARN: unexpected .tokens header; skipping PER-free export")
            return 0
        for line in inp:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= max(i_tid, i_lem, i_pos, i_fine):
                continue
            pos = parts[i_pos]
            fine = parts[i_fine]
            if fine == "PER" or pos == "PUNCT":
                continue
            w.writerow([parts[i_tid], parts[i_lem], pos, fine])
            n += 1
    return n


def merge_stoplist(
    stoplist_path: Path,
    new_phrases: Iterable[str],
    run_dir: Path,
) -> Tuple[int, int]:
    """Backup stoplist, append unique new lines. Returns (existing_noncomment_lines, appended)."""
    new_unique: List[str] = []
    seen: Set[str] = set()
    existing_lines: List[str] = []
    if stoplist_path.is_file():
        with open(stoplist_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                existing_lines.append(line.rstrip("\n"))
                s = line.strip()
                if s and not s.startswith("#"):
                    seen.add(s)
    for phrase in new_phrases:
        p = phrase.strip()
        if not p or p.startswith("#"):
            continue
        if p not in seen:
            seen.add(p)
            new_unique.append(p)
    stamp = datetime.now(timezone.utc).strftime(TS_FMT)
    if stoplist_path.is_file():
        bak = stoplist_path.parent / f"{stoplist_path.name}.bak_{stamp}"
        shutil.copy2(stoplist_path, bak)
        log(f"Backed up stoplist to {bak}")
    to_write = existing_lines + new_unique
    stoplist_path.parent.mkdir(parents=True, exist_ok=True)
    with open(stoplist_path, "w", encoding="utf-8") as f:
        f.write("\n".join(to_write))
        if to_write:
            f.write("\n")
    log(f"Wrote stoplist {stoplist_path} ({len(new_unique)} new line(s))")
    audit = run_dir / f"custom_stoplist_merged_{stamp}.txt"
    shutil.copy2(stoplist_path, audit)
    log(f"Audit copy: {audit}")
    return len([x for x in existing_lines if x.strip() and not x.strip().startswith("#")]), len(new_unique)


def flush_names_aggregate(path: Path, names: Set[str]) -> None:
    sorted_names = sorted(names)
    path.write_text("\n".join(sorted_names) + ("\n" if sorted_names else ""), encoding="utf-8")


@click.command(context_settings={"show_default": True})
@click.option("--config", type=click.Path(exists=True, path_type=Path), default="configs/paths.yaml")
@click.option("--sentences-csv", type=click.Path(path_type=Path), default=None, help="Override sentences_train.csv path")
@click.option("--run-id", "run_id", type=str, default=None, help="Fixed subdirectory name under booknlp_character_runs_parent")
@click.option("--overwrite-run", is_flag=True, help="Delete run directory if it already exists")
@click.option("--limit-books", type=int, default=None, help="Process only the first N work_ids (after sort)")
@click.option("--work-ids", type=str, default=None, help="Comma-separated work_id list to include")
@click.option("--work-ids-file", type=click.Path(exists=True, path_type=Path), default=None, help="File containing one work_id per line")
@click.option("--max-rows", type=int, default=None, help="Read at most this many rows from CSV (debug)")
@click.option(
    "--streaming",
    is_flag=True,
    help="Use configured chunk size for CSV ingestion (default mode is already incremental)",
)
@click.option("--chunk-size", type=int, default=100_000)
@click.option("--model", type=click.Choice(["big", "small"]), default="small")
@click.option("--pipeline", type=str, default="entity", help="BookNLP pipeline string")
@click.option("--require-gpu", is_flag=True, help="Exit if CUDA is not available")
@click.option("--dry-run", is_flag=True, help="Only build txt_input + manifest; skip BookNLP and stoplist merge")
@click.option("--no-merge-stoplist", is_flag=True, help="Skip updating data/processed/custom_stoplist.txt")
@click.option("--no-reuse-inputs", is_flag=True, help="Always rewrite txt_input even if present")
@click.option("--also-nom-per", is_flag=True, help="Include NOM mentions for PER (noisier)")
@click.option("--export-character-summary", is_flag=True, help="Write character_summary.json per book after BookNLP")
@click.option("--export-per-free-tokens", is_flag=True, help="Write w<id>.tokens_non_per.csv.gz per book")
@click.option("--flush-names-every", type=int, default=0, help="If >0, rewrite all_names_so_far.txt every K books")
@click.option("--log-file", type=str, default=None, help="Optional log file name under outputs.logs")
@click.option("--no-progress", is_flag=True, help="Disable tqdm progress bar output")
@click.option("--plan-shards", is_flag=True, help="Write balanced shard work_id files and print per-shard run commands")
@click.option("--num-shards", type=int, default=0, help="Number of shards for --plan-shards")
@click.option("--start-shard", type=int, default=0, help="First shard index to print command for")
@click.option("--end-shard", type=int, default=None, help="Last shard index to print command for")
@click.option("--print-only", is_flag=True, help="For --plan-shards, print commands without writing shard files")
@click.option("--shard-output-dir", type=click.Path(path_type=Path), default=None, help="Directory for generated shard files")
@click.option("--estimate-eta", is_flag=True, help="Sample books and print projected full runtime")
@click.option("--eta-sample-books", type=int, default=50, help="Number of books to sample when --estimate-eta is used")
@click.option("--eta-seed", type=int, default=42, help="Random seed for ETA sampling")
@click.option("--eta-resume", is_flag=True, help="Skip ETA books that already have valid sample artifacts")
@click.option(
    "--txt-input-dir",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Reuse prebuilt txt_input directory (skip CSV->txt materialization)",
)
@click.option("--shard-index", type=int, default=None, help="Optional shard index metadata for this run")
@click.option("--shard-count", type=int, default=None, help="Optional total shard count metadata for this run")
@click.option(
    "--stoplist-sample-books",
    type=int,
    default=None,
    help="Process only N books stratified by txt length (stoplist-oriented subset)",
)
@click.option("--stoplist-sample-seed", type=int, default=42, help="RNG seed for --stoplist-sample-books")
@click.option(
    "--stoplist-sample-bins",
    type=int,
    default=10,
    help="Number of length quantile bins for --stoplist-sample-books",
)
def main(
    config: Path,
    sentences_csv: Optional[Path],
    run_id: Optional[str],
    overwrite_run: bool,
    limit_books: Optional[int],
    work_ids: Optional[str],
    work_ids_file: Optional[Path],
    max_rows: Optional[int],
    streaming: bool,
    chunk_size: int,
    model: str,
    pipeline: str,
    require_gpu: bool,
    dry_run: bool,
    no_merge_stoplist: bool,
    no_reuse_inputs: bool,
    also_nom_per: bool,
    export_character_summary: bool,
    export_per_free_tokens: bool,
    flush_names_every: int,
    log_file: Optional[str],
    no_progress: bool,
    plan_shards: bool,
    num_shards: int,
    start_shard: int,
    end_shard: Optional[int],
    print_only: bool,
    shard_output_dir: Optional[Path],
    estimate_eta: bool,
    eta_sample_books: int,
    eta_seed: int,
    eta_resume: bool,
    txt_input_dir: Optional[Path],
    shard_index: Optional[int],
    shard_count: Optional[int],
    stoplist_sample_books: Optional[int],
    stoplist_sample_seed: int,
    stoplist_sample_bins: int,
) -> None:
    project_root = Path(__file__).resolve().parents[2]
    cfg_mod = _load_config_module(project_root)
    cfg = cfg_mod.load_config(config)
    get_path = cfg_mod.get_path
    resolve_path = cfg_mod.resolve_path

    sentences_path = sentences_csv
    if sentences_path is None:
        p = cfg.get("inputs", {}).get("sentences_train_csv")
        if p:
            sentences_path = resolve_path(Path(p), project_root)
        else:
            base = get_path(cfg, "inputs", "romance_v2_sentences_dir")
            sentences_path = resolve_path(base, project_root) / "sentences_train.csv"

    runs_parent = resolve_path(
        get_path(cfg, "inputs", "booknlp_character_runs_parent"), project_root
    )
    model_path_cfg = cfg.get("inputs", {}).get("booknlp_model_path")
    model_path = resolve_path(Path(model_path_cfg), project_root) if model_path_cfg else None

    stoplist_path = resolve_path(get_path(cfg, "inputs", "custom_stoplist"), project_root)
    logs_dir = resolve_path(
        Path(cfg.get("outputs", {}).get("logs", "logs")),
        project_root,
    )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    run_name = run_id if run_id else f"run_{stamp}"
    run_dir = runs_parent / run_name
    logfile_name = log_file if log_file else f"stage02_booknlp_{run_name}.log"
    use_progress = not no_progress and tqdm is not None
    log_path = configure_stage_logger(logs_dir=logs_dir, log_file=logfile_name, use_tqdm_progress=use_progress)
    if tqdm is None and not no_progress:
        log("WARN: tqdm is not installed; progress bar is disabled.")
    log(f"Project root: {project_root}")
    log(f"Run directory: {run_dir}")
    log(f"Logs directory: {logs_dir}")
    log(f"Log file: {log_path}")

    if run_dir.exists() and overwrite_run:
        log(f"--overwrite-run: removing {run_dir}")
        shutil.rmtree(run_dir)
    if run_dir.exists() and not run_id and not overwrite_run:
        raise click.ClickException(
            f"Run directory exists: {run_dir}. Pass --overwrite-run or use a new timestamp."
        )
    run_dir.mkdir(parents=True, exist_ok=True)

    work_ids_filter: Optional[Set[int]] = None
    if work_ids and work_ids_file:
        raise click.ClickException("Use only one of --work-ids or --work-ids-file.")
    if work_ids:
        work_ids_filter = parse_work_ids_csv(work_ids)
    if work_ids_file:
        work_ids_filter = parse_work_ids_file(work_ids_file)

    if plan_shards:
        if num_shards <= 0:
            raise click.ClickException("--plan-shards requires --num-shards > 0.")
        if txt_input_dir is not None:
            sample_txt_dir = resolve_path(txt_input_dir, project_root)
            ordered_all_wids = work_ids_from_txt_input_dir(sample_txt_dir)
            if work_ids_filter is not None:
                ordered_all_wids = [w for w in ordered_all_wids if w in work_ids_filter]
            if limit_books is not None:
                ordered_all_wids = ordered_all_wids[:limit_books]
            scanned_rows = 0
            log(f"Shard planning from txt_input: {len(ordered_all_wids):,} work_id(s)")
        else:
            ordered_all_wids, scanned_rows = collect_ordered_work_ids(
                Path(sentences_path),
                max_rows,
                chunk_size,
                work_ids_filter,
                limit_books,
            )
        if not ordered_all_wids:
            raise click.ClickException("No work_ids available for shard planning.")
        if stoplist_sample_books is not None and stoplist_sample_books > 0:
            if txt_input_dir is None:
                raise click.ClickException(
                    "--stoplist-sample-books with --plan-shards requires --txt-input-dir "
                    "(length stratification uses prebuilt txt file sizes)."
                )
            sample_txt_dir = resolve_path(txt_input_dir, project_root)
            n_corpus = len(ordered_all_wids)
            ordered_all_wids, sample_meta = stratified_sample_work_ids_by_length(
                sample_txt_dir,
                ordered_all_wids,
                stoplist_sample_books,
                stoplist_sample_seed,
                n_bins=stoplist_sample_bins,
            )
            log(
                f"Stoplist stratified sample: {sample_meta['n_selected']:,} / {n_corpus:,} work_ids "
                f"(bins={sample_meta['n_bins']}, seed={stoplist_sample_seed})"
            )
            (run_dir / "stoplist_sample_manifest.json").write_text(
                json.dumps(
                    {
                        "corpus_work_ids_before_sample": n_corpus,
                        **sample_meta,
                        "work_ids": ordered_all_wids,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        shards = split_work_ids_into_shards(ordered_all_wids, num_shards)
        shard_dir = (
            resolve_path(shard_output_dir, project_root)
            if shard_output_dir is not None
            else run_dir / "shards"
        )
        if not print_only:
            shard_dir.mkdir(parents=True, exist_ok=True)
        start_i = max(0, start_shard)
        end_i = num_shards - 1 if end_shard is None else min(end_shard, num_shards - 1)
        log(
            f"Shard planning: rows_scanned={scanned_rows:,}, total_work_ids={len(ordered_all_wids):,}, num_shards={num_shards}"
        )
        for i, shard_wids in enumerate(shards):
            shard_file = shard_dir / f"work_ids_shard_{i:03d}.txt"
            if not print_only:
                shard_file.write_text("\n".join(str(w) for w in shard_wids) + ("\n" if shard_wids else ""), encoding="utf-8")
            if start_i <= i <= end_i:
                shard_file_ref = shard_file if not print_only else Path(f"<SHARD_DIR>/work_ids_shard_{i:03d}.txt")
                txt_flag = ""
                if txt_input_dir is not None:
                    txt_flag = f" --txt-input-dir {shlex.quote(str(resolve_path(txt_input_dir, project_root)))}"
                cmd = (
                    "python -m src.stage02_preprocessing.extract_character_names_booknlp "
                    f"--config {shlex.quote(str(config))} "
                    f"--run-id {shlex.quote(f'{run_name}_shard_{i:03d}')} "
                    f"--work-ids-file {shlex.quote(str(shard_file_ref))} "
                    f"--pipeline {shlex.quote(pipeline)} --model {shlex.quote(model)} "
                    f"--shard-index {i} --shard-count {num_shards}"
                    f"{txt_flag}"
                )
                click.echo(cmd)
        return

    rows_loaded_t0 = time.perf_counter()
    if txt_input_dir is not None:
        txt_dir = resolve_path(txt_input_dir, project_root)
        if work_ids_file:
            ordered_wids = []
            seen: Set[int] = set()
            for w in parse_work_ids_file(work_ids_file):
                if w in seen:
                    continue
                txt_p = txt_dir / f"{_book_id(w)}.txt"
                if not txt_p.is_file() or txt_p.stat().st_size == 0:
                    log(f"WARN: missing txt for work_id {w} in {txt_dir}")
                    continue
                ordered_wids.append(w)
                seen.add(w)
        elif work_ids_filter is not None:
            ordered_wids = [w for w in work_ids_from_txt_input_dir(txt_dir) if w in work_ids_filter]
        else:
            ordered_wids = work_ids_from_txt_input_dir(txt_dir)
        if limit_books is not None:
            ordered_wids = ordered_wids[:limit_books]
        n_sentence_rows = 0
        log(f"Reusing txt_input from {txt_dir} ({len(ordered_wids):,} work_id(s)) in {time.perf_counter() - rows_loaded_t0:.2f}s")
    else:
        ordered_wids, n_sentence_rows = build_txts_per_work_id_incremental(
            Path(sentences_path),
            max_rows,
            streaming,
            chunk_size,
            run_dir / "txt_input",
            work_ids_filter,
            limit_books,
            reuse_existing=not no_reuse_inputs,
        )
        txt_dir = run_dir / "txt_input"
        log(f"txt_input ready in {time.perf_counter() - rows_loaded_t0:.2f}s")
    if not ordered_wids:
        raise click.ClickException("No rows loaded from sentences CSV.")

    corpus_n_work_ids = len(ordered_wids)
    stoplist_sample_meta: Optional[Dict[str, Any]] = None
    if stoplist_sample_books is not None and stoplist_sample_books > 0:
        ordered_wids, stoplist_sample_meta = stratified_sample_work_ids_by_length(
            txt_dir,
            ordered_wids,
            stoplist_sample_books,
            stoplist_sample_seed,
            n_bins=stoplist_sample_bins,
        )
        log(
            f"Stoplist stratified sample: {stoplist_sample_meta['n_selected']:,} / "
            f"{corpus_n_work_ids:,} work_ids (bins={stoplist_sample_meta['n_bins']})"
        )
        (run_dir / "stoplist_sample_manifest.json").write_text(
            json.dumps(
                {
                    "corpus_work_ids_before_sample": corpus_n_work_ids,
                    **stoplist_sample_meta,
                    "work_ids": ordered_wids,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    manifest = {
        "created_utc": _ts(),
        "sentences_csv": str(sentences_path),
        "work_ids": ordered_wids,
        "n_work_ids": len(ordered_wids),
        "corpus_n_work_ids_before_stoplist_sample": corpus_n_work_ids,
        "stoplist_sample_books": stoplist_sample_books,
        "n_sentence_rows_loaded": n_sentence_rows,
        "model": model,
        "pipeline": pipeline,
        "need_book_json": _pipeline_needs_book_json(pipeline),
        "dry_run": dry_run,
        "estimate_eta": estimate_eta,
        "txt_input_dir": str(txt_dir) if txt_input_dir is not None else None,
        "shard_index": shard_index,
        "shard_count": shard_count,
        "git_head": _git_head(project_root),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log(f"Wrote manifest.json ({len(ordered_wids)} work_ids)")

    if dry_run:
        log("Dry run: stopping before BookNLP (no PyTorch import).")
        return

    try:
        import torch
    except ImportError as e:
        raise click.ClickException(f"PyTorch required for BookNLP: {e}") from e

    cuda_ok = torch.cuda.is_available()
    log(f"torch.cuda.is_available() = {cuda_ok}")
    if cuda_ok:
        log(f"CUDA device 0: {torch.cuda.get_device_name(0)}")
    if require_gpu and not cuda_ok:
        raise click.ClickException("--require-gpu set but CUDA is not available.")

    try:
        from booknlp.booknlp import BookNLP
    except ImportError as e:
        raise click.ClickException(
            f"booknlp import failed ({e}). Install dependencies: pip install booknlp"
        ) from e

    model_params: Dict[str, Any] = {"pipeline": pipeline, "model": model}
    need_book_json = _pipeline_needs_book_json(pipeline)
    if not need_book_json:
        log("Fast mode active: entity-only pipeline; names are extracted primarily from .entities.")
    if model_path:
        model_path.mkdir(parents=True, exist_ok=True)
        model_params["model_path"] = str(model_path)
        log(f"BookNLP model_path: {model_path}")

    log("Initializing BookNLP (downloads models on first use) …")
    t0 = time.perf_counter()
    booknlp = _init_booknlp_with_compat(BookNLP, model_params, torch)
    log(f"BookNLP ready in {time.perf_counter() - t0:.2f}s")

    if estimate_eta:
        if eta_sample_books <= 0:
            raise click.ClickException("--eta-sample-books must be > 0.")
        sample_n = min(eta_sample_books, len(ordered_wids))
        rng = random.Random(eta_seed)
        sample_wids = rng.sample(ordered_wids, sample_n)
        sample_dir = run_dir / "eta_sample"
        sample_dir.mkdir(parents=True, exist_ok=True)
        sample_timings: Dict[int, float] = {}
        failed_eta: List[int] = []
        resumed_wids: Set[int] = set()
        if eta_resume:
            for child in sample_dir.glob("w*"):
                if not child.is_dir():
                    continue
                wid_s = child.name[1:] if child.name.startswith("w") else ""
                if not wid_s.isdigit():
                    continue
                wid_i = int(wid_s)
                if _artifacts_ok(child, child.name, need_book_json=need_book_json):
                    resumed_wids.add(wid_i)
            if resumed_wids:
                log(f"ETA resume: {len(resumed_wids)} book(s) already have sample artifacts")
        log(f"ETA sampling {sample_n} book(s) from {len(ordered_wids)} total selected work_ids")
        for idx, wid in enumerate(sample_wids, start=1):
            bid = _book_id(wid)
            txt_path = txt_dir / f"{bid}.txt"
            out_dir = sample_dir / bid
            if not txt_path.is_file() or txt_path.stat().st_size == 0:
                failed_eta.append(wid)
                log(f"WARN: ETA skip missing txt for work_id={wid}")
                continue
            if eta_resume and wid in resumed_wids:
                log(f"ETA sample [{idx}/{sample_n}] work_id={wid} resume-skip (artifacts OK)")
                continue
            out_dir.mkdir(parents=True, exist_ok=True)
            t_eta = time.perf_counter()
            booknlp.process(str(txt_path), str(out_dir), bid)
            elapsed_eta = time.perf_counter() - t_eta
            if _artifacts_ok(out_dir, bid, need_book_json=need_book_json):
                sample_timings[wid] = elapsed_eta
                log(f"ETA sample [{idx}/{sample_n}] work_id={wid} runtime={elapsed_eta:.2f}s")
            else:
                failed_eta.append(wid)
                log(f"WARN: ETA sample missing artifacts for work_id={wid}")
        if not sample_timings and not resumed_wids:
            raise click.ClickException("ETA sampling failed: no successful sample books.")
        if not sample_timings and resumed_wids:
            raise click.ClickException(
                "ETA resume found artifacts but no new timings; delete eta_sample or rerun without --eta-resume."
            )
        sample_values = list(sample_timings.values())
        avg_s = mean(sample_values)
        med_s = median(sample_values)
        std_s = float(pd.Series(sample_values).std(ddof=1)) if len(sample_values) > 1 else 0.0
        if txt_input_dir is not None and work_ids_file is None and work_ids_filter is None:
            total_books_eta = corpus_n_work_ids
        else:
            total_books_eta = corpus_n_work_ids
        n_books_this_run = len(ordered_wids)
        projected_full_corpus_s = avg_s * total_books_eta
        projected_this_run_s = avg_s * n_books_this_run
        ci_half_full_s = (
            1.96 * (std_s / math.sqrt(len(sample_values))) * total_books_eta
            if len(sample_values) > 1
            else 0.0
        )
        ci_half_run_s = (
            1.96 * (std_s / math.sqrt(len(sample_values))) * n_books_this_run
            if len(sample_values) > 1
            else 0.0
        )
        eta_report = {
            "created_utc": _ts(),
            "sentences_csv": str(sentences_path),
            "pipeline": pipeline,
            "model": model,
            "sample_size": len(sample_values),
            "sample_target": sample_n,
            "sample_failed_count": len(failed_eta),
            "runtime_mean_s": round(avg_s, 3),
            "runtime_median_s": round(med_s, 3),
            "runtime_std_s": round(std_s, 3),
            "runtime_p90_s": round(float(pd.Series(sample_values).quantile(0.9)), 3),
            "books_total_corpus": total_books_eta,
            "books_this_run": n_books_this_run,
            "stoplist_sample_books": stoplist_sample_books,
            "books_per_hour": round(3600.0 / avg_s, 3),
            "projected_full_corpus_hours": round(projected_full_corpus_s / 3600.0, 3),
            "projected_full_corpus_ci95_low_hours": round(
                max((projected_full_corpus_s - ci_half_full_s) / 3600.0, 0.0), 3
            ),
            "projected_full_corpus_ci95_high_hours": round(
                (projected_full_corpus_s + ci_half_full_s) / 3600.0, 3
            ),
            "projected_this_run_hours": round(projected_this_run_s / 3600.0, 3),
            "projected_this_run_ci95_low_hours": round(
                max((projected_this_run_s - ci_half_run_s) / 3600.0, 0.0), 3
            ),
            "projected_this_run_ci95_high_hours": round(
                (projected_this_run_s + ci_half_run_s) / 3600.0, 3
            ),
            "sample_work_ids": list(sample_timings.keys()),
        }
        (run_dir / "eta_estimate.json").write_text(json.dumps(eta_report, indent=2), encoding="utf-8")
        log(
            "ETA projection (full corpus): "
            f"books={total_books_eta}, mean_s={eta_report['runtime_mean_s']}, "
            f"median_s={eta_report['runtime_median_s']}, "
            f"projected_hours={eta_report['projected_full_corpus_hours']} "
            f"(95%: {eta_report['projected_full_corpus_ci95_low_hours']}.."
            f"{eta_report['projected_full_corpus_ci95_high_hours']})"
        )
        if n_books_this_run != total_books_eta:
            log(
                "ETA projection (this run): "
                f"books={n_books_this_run}, projected_hours={eta_report['projected_this_run_hours']}"
            )
        return

    ckpt_path = run_dir / "booknlp_work.ckpt"
    done = _read_completed_ckpt(ckpt_path)
    log(f"Resume ckpt has {len(done)} completed work_id(s)")

    names_per_book_csv = run_dir / "names_per_book.csv"
    wids_logged_csv: Set[int] = set()
    if names_per_book_csv.is_file() and names_per_book_csv.stat().st_size > 0:
        with open(names_per_book_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    wids_logged_csv.add(int(row["work_id"]))
                except (KeyError, ValueError):
                    pass
    csv_header_written = names_per_book_csv.is_file() and names_per_book_csv.stat().st_size > 0

    aggregated_names: Set[str] = set()
    books_since_flush = 0

    total_books = len(ordered_wids)
    iterator = tqdm(
        ordered_wids,
        desc="BookNLP books",
        unit="book",
        disable=not use_progress,
    ) if total_books else ordered_wids
    skipped_books = 0
    processed_books = 0
    failed_books: List[Dict[str, Any]] = []
    per_book_runtime_s: Dict[int, float] = {}

    names_file_handle = open(names_per_book_csv, "a", newline="", encoding="utf-8")
    names_writer = csv.writer(names_file_handle)
    if not csv_header_written:
        names_writer.writerow(
            [
                "work_id",
                "book_id",
                "n_names",
                "book_json",
                "entities_tsv",
                "ts_utc",
            ]
        )
        names_file_handle.flush()
        csv_header_written = True

    try:
        for idx, wid in enumerate(iterator):
            bid = _book_id(wid)
            txt_path = txt_dir / f"{bid}.txt"
            out_dir = run_dir / "booknlp" / bid
            if use_progress and tqdm is not None:
                iterator.set_postfix_str(f"work_id={wid}")
            log(f"--- [{idx+1}/{total_books}] work_id={wid} book_id={bid} ---")

            artifacts = _artifacts_ok(out_dir, bid, need_book_json=need_book_json)
            in_ckpt = wid in done

            if artifacts and in_ckpt:
                log(f"Skipping BookNLP (checkpoint + artifacts OK): {out_dir}")
                skipped_books += 1
            elif artifacts and not in_ckpt:
                log(f"Healing checkpoint for work_id {wid} (artifacts present)")
                _append_ckpt(ckpt_path, wid)
                done.add(wid)
                skipped_books += 1
            else:
                if not txt_path.is_file() or txt_path.stat().st_size == 0:
                    log(f"ERROR: missing or empty txt for work_id {wid}: {txt_path}")
                    failed_books.append({"work_id": wid, "reason": "missing_or_empty_txt"})
                    continue
                out_dir.mkdir(parents=True, exist_ok=True)
                log(f"Starting BookNLP.process({txt_path.name}, …)")
                t1 = time.perf_counter()
                booknlp.process(str(txt_path), str(out_dir), bid)
                elapsed_s = time.perf_counter() - t1
                per_book_runtime_s[wid] = elapsed_s
                log(f"BookNLP finished in {elapsed_s:.2f}s for work_id={wid}")
                if not _artifacts_ok(out_dir, bid, need_book_json=need_book_json):
                    log(f"ERROR: BookNLP did not produce expected outputs in {out_dir}")
                    failed_books.append({"work_id": wid, "reason": "missing_artifacts"})
                    continue
                _append_ckpt(ckpt_path, wid)
                done.add(wid)
                processed_books += 1

            book_p = out_dir / f"{bid}.book"
            ent_p = out_dir / f"{bid}.entities"
            names: Set[str] = set()
            if _artifacts_ok(out_dir, bid, need_book_json=need_book_json):
                try:
                    if need_book_json and book_p.is_file():
                        with open(book_p, "r", encoding="utf-8") as fp:
                            book_data = json.load(fp)
                        names |= names_from_book_json(book_data, also_nom_per)
                except (json.JSONDecodeError, OSError) as e:
                    log(f"WARN: could not parse .book for {wid}: {e}")

                try:
                    names |= names_from_entities_file(ent_p, also_nom_per)
                except OSError as e:
                    log(f"WARN: could not read .entities for {wid}: {e}")

                aggregated_names |= names
                books_since_flush += 1

                if export_character_summary and book_p.is_file():
                    write_character_summary_json(book_p, out_dir / "character_summary.json")

                if export_per_free_tokens:
                    tok = out_dir / f"{bid}.tokens"
                    if tok.is_file():
                        gz_out = out_dir / f"{bid}.tokens_non_per.csv.gz"
                        nrows = export_per_free_tokens_gz(tok, gz_out)
                        log(f"Wrote {gz_out.name} ({nrows} token row(s))")

                if flush_names_every > 0 and books_since_flush >= flush_names_every:
                    flush_names_aggregate(run_dir / "all_names_so_far.txt", aggregated_names)
                    log(f"Flushed all_names_so_far.txt ({len(aggregated_names)} unique name(s))")
                    books_since_flush = 0

                if wid not in wids_logged_csv:
                    names_writer.writerow(
                        [
                            wid,
                            bid,
                            len(names),
                            str(book_p.relative_to(run_dir)) if book_p.is_file() else "",
                            str(ent_p.relative_to(run_dir)) if ent_p.is_file() else "",
                            _ts(),
                        ]
                    )
                    names_file_handle.flush()
                    wids_logged_csv.add(wid)
                log(f"Extracted {len(names)} unique surface phrase(s) for work_id={wid}")
            else:
                log(f"WARN: no valid BookNLP artifacts yet for work_id={wid}")
                failed_books.append({"work_id": wid, "reason": "no_valid_artifacts"})
    finally:
        names_file_handle.close()

    flush_names_aggregate(run_dir / "all_names_so_far.txt", aggregated_names)
    log(f"Final aggregate: {len(aggregated_names)} unique name phrase(s) in all_names_so_far.txt")

    durations = list(per_book_runtime_s.values())
    slowest = sorted(per_book_runtime_s.items(), key=lambda kv: kv[1], reverse=True)[:10]
    run_summary = {
        "finished_utc": _ts(),
        "shard_index": shard_index,
        "shard_count": shard_count,
        "n_books_total": total_books,
        "n_books_processed": processed_books,
        "n_books_skipped": skipped_books,
        "n_books_failed": len(failed_books),
        "n_unique_name_phrases": len(aggregated_names),
        "booknlp_runtime_avg_s": round(mean(durations), 3) if durations else None,
        "booknlp_runtime_median_s": round(median(durations), 3) if durations else None,
        "booknlp_runtime_slowest_top10": [
            {"work_id": wid, "runtime_s": round(runtime_s, 3)}
            for wid, runtime_s in slowest
        ],
        "failed_work_ids": failed_books,
    }
    (run_dir / "run_summary.json").write_text(
        json.dumps(run_summary, indent=2),
        encoding="utf-8",
    )
    if failed_books:
        with open(run_dir / "failed_work_ids.csv", "w", newline="", encoding="utf-8") as ff:
            wr = csv.DictWriter(ff, fieldnames=["work_id", "reason"])
            wr.writeheader()
            wr.writerows(failed_books)
    log(
        "Run summary: "
        f"processed={processed_books}, skipped={skipped_books}, failed={len(failed_books)}, "
        f"avg_s={run_summary['booknlp_runtime_avg_s']}, median_s={run_summary['booknlp_runtime_median_s']}"
    )

    merged_manifest = {
        "finished_utc": _ts(),
        "n_work_ids": len(ordered_wids),
        "n_unique_name_phrases": len(aggregated_names),
        "torch_cuda": cuda_ok,
        "cuda_device": torch.cuda.get_device_name(0) if cuda_ok else None,
        "booknlp_pipeline": pipeline,
        "need_book_json": need_book_json,
        "booknlp_model": model,
        "booknlp_version": _package_version("booknlp"),
        "sentences_csv": str(sentences_path),
        "stoplist_path": str(stoplist_path),
        "shard_index": shard_index,
        "shard_count": shard_count,
        "git_head": _git_head(project_root),
    }
    (run_dir / "merged_manifest.json").write_text(
        json.dumps(merged_manifest, indent=2), encoding="utf-8"
    )

    if no_merge_stoplist:
        log("--no-merge-stoplist: not updating custom_stoplist.txt")
        return

    prev_n, appended = merge_stoplist(stoplist_path, aggregated_names, run_dir)
    merged_manifest["stoplist_existing_nonempty_lines"] = prev_n
    merged_manifest["stoplist_appended_lines"] = appended
    (run_dir / "merged_manifest.json").write_text(
        json.dumps(merged_manifest, indent=2), encoding="utf-8"
    )
    log("Done.")


if __name__ == "__main__":
    main()
