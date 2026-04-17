"""
Build per-book UTF-8 .txt files from sentences_train.csv, run BookNLP (GPU via
PyTorch), extract person-name strings from .book + .entities, and merge into
custom_stoplist.txt with a timestamped backup.

Default pipeline is entity,quote,coref (coref requires quote + entity upstream).

Usage (from repo root):
  python -m src.stage02_preprocessing.extract_character_names_booknlp --config configs/paths.yaml
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import csv
import gzip
import json
import os
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

import click
import pandas as pd


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


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def log(msg: str) -> None:
    print(f"[{_ts()}] {msg}", flush=True)


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


def _artifacts_ok(out_dir: Path, book_id: str) -> bool:
    book_p = out_dir / f"{book_id}.book"
    ent_p = out_dir / f"{book_id}.entities"
    if not book_p.is_file() or not ent_p.is_file():
        return False
    if book_p.stat().st_size < 3 or ent_p.stat().st_size < 20:
        return False
    return True


def load_sentences_table(
    sentences_csv: Path,
    max_rows: Optional[int],
    streaming: bool,
    chunk_size: int,
) -> pd.DataFrame:
    usecols = ["work_id", "chapter_index", "sentence_index", "sentence"]
    log(f"Reading sentences CSV: {sentences_csv}")
    if not sentences_csv.is_file():
        raise FileNotFoundError(f"Missing sentences CSV: {sentences_csv}")

    if streaming:
        chunks: List[pd.DataFrame] = []
        n = 0
        for chunk in pd.read_csv(
            sentences_csv,
            usecols=usecols,
            chunksize=chunk_size,
            dtype={"work_id": "int64", "chapter_index": "int64", "sentence_index": "int64"},
        ):
            chunks.append(chunk)
            n += len(chunk)
            if max_rows is not None and n >= max_rows:
                break
        if not chunks:
            return pd.DataFrame(columns=usecols)
        df = pd.concat(chunks, ignore_index=True)
    else:
        df = pd.read_csv(
            sentences_csv,
            usecols=usecols,
            dtype={"work_id": "int64", "chapter_index": "int64", "sentence_index": "int64"},
            nrows=max_rows,
        )

    if max_rows is not None and len(df) > max_rows:
        df = df.iloc[:max_rows].copy()
    log(f"Loaded {len(df):,} sentence rows")
    return df


def write_txts_per_work_id(
    df: pd.DataFrame,
    txt_dir: Path,
    work_ids_filter: Optional[Set[int]],
    limit_books: Optional[int],
    reuse_existing: bool,
) -> List[int]:
    txt_dir.mkdir(parents=True, exist_ok=True)
    log("Sorting by work_id, chapter_index, sentence_index …")
    df = df.sort_values(["work_id", "chapter_index", "sentence_index"], kind="mergesort")

    ordered_wids: List[int] = []
    for wid, _ in df.groupby("work_id", sort=False):
        if work_ids_filter is not None and int(wid) not in work_ids_filter:
            continue
        ordered_wids.append(int(wid))
    if limit_books is not None:
        ordered_wids = ordered_wids[:limit_books]

    log(f"Will materialize {len(ordered_wids)} work_id text file(s) under {txt_dir}")

    for i, wid in enumerate(ordered_wids):
        bid = _book_id(wid)
        out_path = txt_dir / f"{bid}.txt"
        if reuse_existing and out_path.is_file() and out_path.stat().st_size > 0:
            log(f"[{i+1}/{len(ordered_wids)}] reuse txt_input/{out_path.name} ({out_path.stat().st_size} bytes)")
            continue
        sub = df.loc[df["work_id"] == wid]
        parts: List[str] = []
        prev_ch: Optional[int] = None
        for _, row in sub.iterrows():
            ch = int(row["chapter_index"])
            sent = str(row["sentence"]).replace("\r\n", "\n").replace("\r", "\n").strip()
            if prev_ch is not None and ch != prev_ch:
                parts.append("")
            parts.append(sent)
            prev_ch = ch
        body = "\n".join(parts)
        if not body.endswith("\n"):
            body += "\n"
        out_path.write_text(body, encoding="utf-8")
        log(f"[{i+1}/{len(ordered_wids)}] wrote txt_input/{out_path.name} ({len(body)} chars)")
    return ordered_wids


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
@click.option("--max-rows", type=int, default=None, help="Read at most this many rows from CSV (debug)")
@click.option("--streaming", is_flag=True, help="Read CSV in chunks (lower peak read memory; still holds grouped data)")
@click.option("--chunk-size", type=int, default=100_000)
@click.option("--model", type=click.Choice(["big", "small"]), default="big")
@click.option("--pipeline", type=str, default="entity,quote,coref", help="BookNLP pipeline string")
@click.option("--require-gpu", is_flag=True, help="Exit if CUDA is not available")
@click.option("--dry-run", is_flag=True, help="Only build txt_input + manifest; skip BookNLP and stoplist merge")
@click.option("--no-merge-stoplist", is_flag=True, help="Skip updating data/processed/custom_stoplist.txt")
@click.option("--no-reuse-inputs", is_flag=True, help="Always rewrite txt_input even if present")
@click.option("--also-nom-per", is_flag=True, help="Include NOM mentions for PER (noisier)")
@click.option("--export-character-summary", is_flag=True, help="Write character_summary.json per book after BookNLP")
@click.option("--export-per-free-tokens", is_flag=True, help="Write w<id>.tokens_non_per.csv.gz per book")
@click.option("--flush-names-every", type=int, default=0, help="If >0, rewrite all_names_so_far.txt every K books")
def main(
    config: Path,
    sentences_csv: Optional[Path],
    run_id: Optional[str],
    overwrite_run: bool,
    limit_books: Optional[int],
    work_ids: Optional[str],
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

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    run_name = run_id if run_id else f"run_{stamp}"
    run_dir = runs_parent / run_name
    log(f"Project root: {project_root}")
    log(f"Run directory: {run_dir}")

    if run_dir.exists() and overwrite_run:
        log(f"--overwrite-run: removing {run_dir}")
        shutil.rmtree(run_dir)
    if run_dir.exists() and not run_id and not overwrite_run:
        raise click.ClickException(
            f"Run directory exists: {run_dir}. Pass --overwrite-run or use a new timestamp."
        )
    run_dir.mkdir(parents=True, exist_ok=True)

    work_ids_filter: Optional[Set[int]] = None
    if work_ids:
        work_ids_filter = {int(x.strip()) for x in work_ids.split(",") if x.strip()}

    df = load_sentences_table(Path(sentences_path), max_rows, streaming, chunk_size)
    if df.empty:
        raise click.ClickException("No rows loaded from sentences CSV.")

    txt_dir = run_dir / "txt_input"
    reuse = not no_reuse_inputs
    ordered_wids = write_txts_per_work_id(
        df, txt_dir, work_ids_filter, limit_books, reuse_existing=reuse
    )
    del df

    manifest = {
        "created_utc": _ts(),
        "sentences_csv": str(sentences_path),
        "work_ids": ordered_wids,
        "n_work_ids": len(ordered_wids),
        "model": model,
        "pipeline": pipeline,
        "dry_run": dry_run,
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
    if model_path:
        model_path.mkdir(parents=True, exist_ok=True)
        model_params["model_path"] = str(model_path)
        log(f"BookNLP model_path: {model_path}")

    log("Initializing BookNLP (downloads models on first use) …")
    t0 = time.perf_counter()
    booknlp = BookNLP("en", model_params)
    log(f"BookNLP ready in {time.perf_counter() - t0:.2f}s")

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

    for idx, wid in enumerate(ordered_wids):
        bid = _book_id(wid)
        txt_path = txt_dir / f"{bid}.txt"
        out_dir = run_dir / "booknlp" / bid
        log(f"--- [{idx+1}/{len(ordered_wids)}] work_id={wid} book_id={bid} ---")

        artifacts = _artifacts_ok(out_dir, bid)
        in_ckpt = wid in done

        if artifacts and in_ckpt:
            log(f"Skipping BookNLP (checkpoint + artifacts OK): {out_dir}")
        elif artifacts and not in_ckpt:
            log(f"Healing checkpoint for work_id {wid} (artifacts present)")
            _append_ckpt(ckpt_path, wid)
            done.add(wid)
        else:
            if not txt_path.is_file() or txt_path.stat().st_size == 0:
                log(f"ERROR: missing or empty txt for work_id {wid}: {txt_path}")
                continue
            out_dir.mkdir(parents=True, exist_ok=True)
            log(f"Starting BookNLP.process({txt_path.name}, …)")
            t1 = time.perf_counter()
            booknlp.process(str(txt_path), str(out_dir), bid)
            log(f"BookNLP finished in {time.perf_counter() - t1:.2f}s for work_id={wid}")
            if not _artifacts_ok(out_dir, bid):
                log(f"ERROR: BookNLP did not produce expected outputs in {out_dir}")
                continue
            _append_ckpt(ckpt_path, wid)
            done.add(wid)

        book_p = out_dir / f"{bid}.book"
        ent_p = out_dir / f"{bid}.entities"
        names: Set[str] = set()
        if _artifacts_ok(out_dir, bid):
            try:
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
                with open(names_per_book_csv, "a", newline="", encoding="utf-8") as nf:
                    wr = csv.writer(nf)
                    if not csv_header_written:
                        wr.writerow(
                            [
                                "work_id",
                                "book_id",
                                "n_names",
                                "book_json",
                                "entities_tsv",
                                "ts_utc",
                            ]
                        )
                        csv_header_written = True
                    wr.writerow(
                        [
                            wid,
                            bid,
                            len(names),
                            str(book_p.relative_to(run_dir)) if book_p.is_file() else "",
                            str(ent_p.relative_to(run_dir)) if ent_p.is_file() else "",
                            _ts(),
                        ]
                    )
                wids_logged_csv.add(wid)
            log(f"Extracted {len(names)} unique surface phrase(s) for work_id={wid}")
        else:
            log(f"WARN: no valid BookNLP artifacts yet for work_id={wid}")

    flush_names_aggregate(run_dir / "all_names_so_far.txt", aggregated_names)
    log(f"Final aggregate: {len(aggregated_names)} unique name phrase(s) in all_names_so_far.txt")

    merged_manifest = {
        "finished_utc": _ts(),
        "n_work_ids": len(ordered_wids),
        "n_unique_name_phrases": len(aggregated_names),
        "torch_cuda": cuda_ok,
        "cuda_device": torch.cuda.get_device_name(0) if cuda_ok else None,
        "booknlp_pipeline": pipeline,
        "booknlp_model": model,
        "booknlp_version": _package_version("booknlp"),
        "sentences_csv": str(sentences_path),
        "stoplist_path": str(stoplist_path),
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
