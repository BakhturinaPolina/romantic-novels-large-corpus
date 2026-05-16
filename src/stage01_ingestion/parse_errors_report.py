"""Summarize and dedupe ``parse_errors.csv`` from Stage 01 ingestion.

Reads with ``csv.DictReader`` (quoted errors with commas). For each ``work_id``,
keeps the **last** row in file order (most recent append). Writes a deduped CSV
beside the input by default; never overwrites ``parse_errors.csv`` unless
``--overwrite-output`` is set explicitly to that path.

Also prints deduped **recovery hints** (Calibre repair, ``--use-zip-fallback``,
re-download, etc.). Optional ``--recovery-hints-csv`` writes those per row.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

FIELDNAMES = ["work_id", "md5", "epub_path", "error"]
SPLIT_NAMES = frozenset({"train", "val", "test"})


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_errors_csv(project_root: Path) -> Path:
    return project_root / "data/processed/romance_subdataset_downloaded_v2_sentences/parse_errors.csv"


def resolve_path(p: Path, project_root: Path) -> Path:
    if p.is_absolute():
        return p
    return (project_root / p).resolve()


def split_from_epub_path(epub_path: str) -> str:
    p = Path(epub_path)
    if p.parent.name in SPLIT_NAMES:
        return p.parent.name
    for part in p.parts:
        if part in SPLIT_NAMES:
            return part
    return "unknown"


def recovery_hint(error: str) -> str:
    """Short suggested next step for triage (dedupe / repair / re-ingest)."""
    coarse, fine = error_bucket(error)
    if coarse == "epub_missing_on_disk":
        return "restore_epub_at_path_or_fix_metadata_path"
    if coarse == "no_sentences_extracted":
        return "reingest_with_parse_epub_use_zip_fallback_or_inspect_epub_html"
    if fine == "missing_archive_member":
        return "calibre_ebook_convert_epub_to_epub_then_reingest_or_use_zip_fallback"
    if fine in ("bad_zip_file", "bad_magic_header", "zip_decompress_error"):
        return "replace_epub_redownload_or_skip"
    if fine == "list_index_out_of_range":
        return "try_calibre_repair_then_reingest_or_zip_fallback"
    if fine in ("none_type_attribute", "container_related"):
        return "try_calibre_repair_then_reingest_or_zip_fallback"
    if coarse == "get_body_content_failed":
        return "calibre_repair_or_zip_fallback_if_readable_zip"
    if coarse == "read_epub_failed" and fine == "other":
        return "try_calibre_repair_then_reingest_or_manual_inspect"
    if coarse == "other":
        return "inspect_parse_errors_row_manually"
    return "see_parse_errors_repair_failed_epubs_modes"


def error_bucket(error: str) -> Tuple[str, str]:
    """Return (coarse_bucket, fine_bucket) for display and JSON."""
    e = (error or "").strip()
    if e == "epub_missing_on_disk":
        return ("epub_missing_on_disk", "epub_missing_on_disk")
    if e == "no_sentences_extracted":
        return ("no_sentences_extracted", "no_sentences_extracted")
    if e.startswith("get_body_content_failed:"):
        if "There is no item named" in e:
            return ("get_body_content_failed", "missing_archive_member")
        return ("get_body_content_failed", "other")
    if e.startswith("read_epub_failed:"):
        if "Bad Zip file" in e:
            return ("read_epub_failed", "bad_zip_file")
        if "Bad magic number" in e:
            return ("read_epub_failed", "bad_magic_header")
        if "There is no item named" in e:
            return ("read_epub_failed", "missing_archive_member")
        if "decompressing" in e:
            return ("read_epub_failed", "zip_decompress_error")
        if "list index out of range" in e:
            return ("read_epub_failed", "list_index_out_of_range")
        if "container" in e.lower() or "container.xml" in e:
            return ("read_epub_failed", "container_related")
        if "NoneType" in e:
            return ("read_epub_failed", "none_type_attribute")
        return ("read_epub_failed", "other")
    return ("other", "other")


def read_error_rows(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        missing = set(FIELDNAMES) - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{path}: missing columns {sorted(missing)}; got {reader.fieldnames!r}")
        for row in reader:
            rows.append({k: (row.get(k) or "").strip() for k in FIELDNAMES})
    return rows


def dedupe_last_per_work_id(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    """Last occurrence of each ``work_id`` in file order wins; output sorted by ``work_id``."""
    last: Dict[int, Dict[str, str]] = {}
    for row in rows:
        try:
            wid = int(row["work_id"])
        except ValueError:
            continue
        last[wid] = {k: row[k] for k in FIELDNAMES}
    return [last[wid] for wid in sorted(last.keys())]


def resolve_output_csv_path(output_csv: Optional[Path], input_csv: Path, project_root: Path) -> Path:
    if output_csv is None:
        return input_csv.parent / "parse_errors_deduped.csv"
    if output_csv.is_absolute():
        return output_csv
    if output_csv.parent in (Path("."), Path("")):
        return input_csv.parent / output_csv.name
    return (project_root / output_csv).resolve()


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    root = _project_root()
    default_err = default_errors_csv(root)
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--errors-csv",
        type=Path,
        default=default_err,
        help="Path to parse_errors.csv (relative paths resolved from project root)",
    )
    p.add_argument(
        "--output-csv",
        type=Path,
        default=None,
        help="Deduped output path (default: <input_dir>/parse_errors_deduped.csv)",
    )
    p.add_argument(
        "--no-write",
        action="store_true",
        help="Only print summary; do not write deduped CSV",
    )
    p.add_argument(
        "--overwrite-output",
        action="store_true",
        help="Allow replacing an existing output file",
    )
    p.add_argument(
        "--print-json",
        action="store_true",
        help="Print a JSON summary to stdout after the text report",
    )
    p.add_argument(
        "--recovery-hints-csv",
        type=Path,
        default=None,
        help="Write work_id, md5, epub_path, error, recovery_hint (deduped rows)",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(list(argv) if argv is not None else None)
    root = _project_root()
    err_path = resolve_path(args.errors_csv, root)
    if not err_path.is_file():
        print(f"Error: file not found: {err_path}", file=sys.stderr)
        return 1

    rows = read_error_rows(err_path)
    raw_n = len(rows)
    raw_work_ids = set()
    for row in rows:
        try:
            raw_work_ids.add(int(row["work_id"]))
        except ValueError:
            pass

    raw_rows_by_split: Counter[str] = Counter()
    for row in rows:
        raw_rows_by_split[split_from_epub_path(row["epub_path"])] += 1

    deduped = dedupe_last_per_work_id(rows)
    dedup_n = len(deduped)
    dedup_work_ids = {int(r["work_id"]) for r in deduped}

    split_unique: Counter[str] = Counter()
    coarse: Counter[str] = Counter()
    fine: Counter[str] = Counter()
    for row in deduped:
        wid = int(row["work_id"])
        split_unique[split_from_epub_path(row["epub_path"])] += 1
        c, f = error_bucket(row["error"])
        coarse[c] += 1
        fine[f"{c}::{f}"] += 1

    print(f"Input: {err_path}")
    print(f"Raw rows: {raw_n}  unique work_id (raw): {len(raw_work_ids)}")
    print(f"Deduped rows: {dedup_n}  unique work_id (deduped): {len(dedup_work_ids)}")
    print()
    print("Raw rows by split (includes duplicates):")
    for s in sorted(raw_rows_by_split.keys(), key=lambda x: (x == "unknown", x)):
        print(f"  {s}: {raw_rows_by_split[s]}")
    print()
    print("Deduped unique work_id by split:")
    for s in sorted(split_unique.keys(), key=lambda x: (x == "unknown", x)):
        print(f"  {s}: {split_unique[s]}")
    print()
    print("Deduped rows by error bucket (coarse):")
    for k, v in coarse.most_common():
        print(f"  {k}: {v}")
    print()
    print("Deduped rows by error bucket (fine):")
    for k, v in fine.most_common():
        print(f"  {k}: {v}")

    hint_counts: Counter[str] = Counter()
    for row in deduped:
        hint_counts[recovery_hint(row["error"])] += 1
    print()
    print("Deduped rows by recovery hint (see repair_failed_epubs + parse_epub --use-zip-fallback):")
    for h, v in hint_counts.most_common():
        print(f"  {v}\t{h}")

    if args.print_json:
        payload: Dict[str, Any] = {
            "input": str(err_path),
            "raw_rows": raw_n,
            "unique_work_id_raw": len(raw_work_ids),
            "deduped_rows": dedup_n,
            "unique_work_id_deduped": len(dedup_work_ids),
            "raw_rows_by_split": dict(raw_rows_by_split),
            "deduped_unique_work_id_by_split": dict(split_unique),
            "deduped_by_coarse_bucket": dict(coarse),
            "deduped_by_fine_bucket": dict(fine),
            "deduped_by_recovery_hint": dict(hint_counts),
        }
        print()
        print(json.dumps(payload, indent=2))

    if not args.no_write:
        out_path = resolve_output_csv_path(args.output_csv, err_path, root)

        if out_path.resolve() == err_path.resolve() and not args.overwrite_output:
            print(
                f"\nRefusing to write to input file {out_path} without --overwrite-output.",
                file=sys.stderr,
            )
            return 1

        if out_path.exists() and not args.overwrite_output:
            print(f"\nRefusing to overwrite existing {out_path} without --overwrite-output.", file=sys.stderr)
            return 1

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", newline="", encoding="utf-8") as fp:
            w = csv.DictWriter(fp, fieldnames=FIELDNAMES)
            w.writeheader()
            for row in deduped:
                w.writerow(row)
        print(f"\nWrote deduped CSV: {out_path}")

    if args.recovery_hints_csv is not None:
        hint_path = resolve_path(args.recovery_hints_csv, root)
        if hint_path.exists() and not args.overwrite_output:
            print(f"\nRefusing to overwrite {hint_path} without --overwrite-output.", file=sys.stderr)
            return 1
        hint_path.parent.mkdir(parents=True, exist_ok=True)
        hf = ["work_id", "md5", "epub_path", "error", "recovery_hint"]
        with open(hint_path, "w", newline="", encoding="utf-8") as fp:
            hw = csv.DictWriter(fp, fieldnames=hf)
            hw.writeheader()
            for row in deduped:
                hw.writerow(
                    {
                        "work_id": row["work_id"],
                        "md5": row["md5"],
                        "epub_path": row["epub_path"],
                        "error": row["error"],
                        "recovery_hint": recovery_hint(row["error"]),
                    }
                )
        print(f"\nWrote recovery hints CSV: {hint_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
