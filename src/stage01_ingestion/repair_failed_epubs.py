"""Audit and optionally repair EPUBs listed in Stage 01 ``parse_errors*.csv``.

This is **not** a second ingestion pipeline. It helps triage corrupt or odd EPUBs
before re-running ``parse_epub_corpus_to_sentence_csvs``.

Modes
-----

- ``audit`` (default): ``exists``, file size, ``zipfile.ZipFile.testzip()``.
- ``try-read-epub``: ``ebooklib.epub.read_epub`` (same entry point as ingestion).
- ``calibre-repair``: run Calibre's ``ebook-convert`` EPUB→EPUB (rewrite). Requires
  Calibre on ``PATH``; see https://manual.calibre-ebook.com/generated/en/ebook-convert.html

Out of scope: automatic OPF/package surgery inside ZIPs. Use ``calibre-repair``
or replace files from your download pipeline for ``bad_zip`` / ``missing``.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import zlib
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

FIELDNAMES = ("work_id", "md5", "epub_path", "error")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_errors_csv(project_root: Path) -> Path:
    out_dir = project_root / "data/processed/romance_subdataset_downloaded_v2_sentences"
    deduped = out_dir / "parse_errors_deduped.csv"
    raw = out_dir / "parse_errors.csv"
    if deduped.is_file():
        return deduped
    return raw


def resolve_path(p: Path, project_root: Path) -> Path:
    if p.is_absolute():
        return p
    return (project_root / p).resolve()


def read_error_rows(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            rows.append({k: (row.get(k) or "").strip() for k in FIELDNAMES})
    return rows


def audit_epub(epub_path: Path) -> Tuple[str, str]:
    if not epub_path.is_file():
        return "missing", ""
    size = epub_path.stat().st_size
    if size == 0:
        return "zero_size", ""
    try:
        with zipfile.ZipFile(epub_path, "r") as zf:
            bad = zf.testzip()
            if bad is not None:
                return "bad_zip", f"testzip_bad_member={bad}"
    except (zipfile.BadZipFile, OSError, zlib.error, RuntimeError) as e:
        return "bad_zip", f"{type(e).__name__}: {e}"
    return "readable_zip", f"size_bytes={size}"


def try_read_epub(epub_path: Path) -> Tuple[str, str]:
    try:
        from ebooklib import epub as epub_reader
    except ImportError as e:
        return "read_failed", f"ImportError: {e}"
    try:
        epub_reader.read_epub(str(epub_path))
        return "read_ok", ""
    except Exception as e:
        return "read_failed", f"{type(e).__name__}: {e}"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    root = _project_root()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--errors-csv",
        type=Path,
        default=None,
        help="parse_errors CSV (default: parse_errors_deduped.csv if present, else parse_errors.csv)",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most this many rows",
    )
    p.add_argument(
        "--mode",
        choices=("audit", "try-read-epub", "calibre-repair"),
        default="audit",
        help="audit: zip/exists; try-read-epub: ebooklib; calibre-repair: ebook-convert EPUB→EPUB",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="For calibre-repair: print commands only, do not run or write outputs",
    )
    p.add_argument(
        "--repair-dir",
        type=Path,
        default=None,
        help="Output directory for repaired EPUBs (default: same directory as source EPUB)",
    )
    p.add_argument(
        "--audit-output-csv",
        type=Path,
        default=None,
        help="Write per-row audit / read results to this CSV path",
    )
    return p.parse_args(argv)


def _calibre_bin() -> Optional[str]:
    return shutil.which("ebook-convert")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(list(argv) if argv is not None else None)
    root = _project_root()
    err_path = resolve_path(args.errors_csv, root) if args.errors_csv else default_errors_csv(root)
    if not err_path.is_file():
        print(f"Error: file not found: {err_path}", file=sys.stderr)
        return 1

    rows = read_error_rows(err_path)
    if args.limit is not None:
        rows = rows[: args.limit]

    if args.mode == "try-read-epub":
        try:
            import ebooklib  # noqa: F401
        except ImportError:
            print(
                "Error: try-read-epub requires ebooklib (same venv as ingestion).",
                file=sys.stderr,
            )
            return 1

    calibre = _calibre_bin()
    if args.mode == "calibre-repair" and not args.dry_run and calibre is None:
        print("Error: ebook-convert not found on PATH (install Calibre CLI).", file=sys.stderr)
        return 1
    calibre_cmd = calibre or "ebook-convert"

    out_rows: List[Dict[str, str]] = []
    summary: Dict[str, int] = {}

    for row in rows:
        epub_path = Path(row["epub_path"])
        pipeline_error = row["error"]
        rec: Dict[str, str] = {
            "work_id": row["work_id"],
            "md5": row["md5"],
            "epub_path": str(epub_path),
            "pipeline_error": pipeline_error,
        }

        if args.mode == "audit":
            status, detail = audit_epub(epub_path)
            rec["audit_status"] = status
            rec["audit_detail"] = detail
            key = status
        elif args.mode == "try-read-epub":
            a_status, a_detail = audit_epub(epub_path)
            rec["audit_status"] = a_status
            rec["audit_detail"] = a_detail
            if a_status != "readable_zip":
                rec["read_status"] = "skipped_not_readable_zip"
                rec["read_detail"] = ""
                key = f"{a_status}_skip"
            else:
                r_status, r_detail = try_read_epub(epub_path)
                rec["read_status"] = r_status
                rec["read_detail"] = r_detail
                key = f"{r_status}"
        else:
            a_status, a_detail = audit_epub(epub_path)
            rec["audit_status"] = a_status
            rec["audit_detail"] = a_detail
            if a_status != "readable_zip":
                rec["calibre_status"] = "skipped_not_readable_zip"
                rec["calibre_detail"] = ""
                key = f"{a_status}_skip"
                out_rows.append(rec)
                summary[key] = summary.get(key, 0) + 1
                continue

            out_epub = epub_path.with_name(f"{epub_path.stem}.repaired.epub")
            if args.repair_dir is not None:
                rd = resolve_path(args.repair_dir, root) if not args.repair_dir.is_absolute() else args.repair_dir
                rd.mkdir(parents=True, exist_ok=True)
                out_epub = rd / out_epub.name

            cmd = [calibre_cmd, str(epub_path), str(out_epub)]
            if args.dry_run:
                rec["calibre_status"] = "dry_run"
                rec["calibre_detail"] = " ".join(cmd)
                print(f"[dry-run] {' '.join(cmd)}")
                key = "dry_run"
            else:
                try:
                    subprocess.run(cmd, check=True, capture_output=True, text=True)
                    rec["calibre_status"] = "ok"
                    rec["calibre_detail"] = str(out_epub)
                    key = "calibre_ok"
                except subprocess.CalledProcessError as e:
                    rec["calibre_status"] = "failed"
                    rec["calibre_detail"] = (e.stderr or e.stdout or str(e))[:2000]
                    key = "calibre_failed"

        out_rows.append(rec)
        summary[key] = summary.get(key, 0) + 1

    print(f"Input: {err_path}")
    print(f"Mode: {args.mode}  rows: {len(rows)}")
    print("Summary:")
    for k in sorted(summary.keys()):
        print(f"  {k}: {summary[k]}")

    if args.audit_output_csv is not None:
        outp = resolve_path(args.audit_output_csv, root) if not args.audit_output_csv.is_absolute() else args.audit_output_csv
        outp.parent.mkdir(parents=True, exist_ok=True)
        if not out_rows:
            print("No rows written (--limit 0 or empty errors CSV).", file=sys.stderr)
        else:
            fieldnames = list(out_rows[0].keys())
            with open(outp, "w", newline="", encoding="utf-8") as fp:
                w = csv.DictWriter(fp, fieldnames=fieldnames)
                w.writeheader()
                for r in out_rows:
                    w.writerow(r)
            print(f"Wrote: {outp}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
