#!/usr/bin/env python3
"""
Audit likely non-name tokens in custom stoplist merges.

Default scope:
- target tokens newly added since latest backup:
  current_stoplist - backup_new

Outputs:
- CSV with per-token heuristics
- stdout summary of top likely non-name suspects

This script is read-only with respect to stoplist inputs.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from wordfreq import zipf_frequency as _zipf_frequency
except ImportError:  # pragma: no cover
    _zipf_frequency = None


@dataclass(frozen=True)
class AuditConfig:
    current_path: Path
    backup_old_path: Path
    backup_new_path: Path
    target_delta: str
    zipf_threshold: float
    top_n: int
    output_csv: Path
    enable_spacy_probe: bool
    spacy_model: str


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _read_stoplist_tokens(path: Path) -> set[str]:
    tokens: set[str] = set()
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip().lower()
            if not s or s.startswith("#"):
                continue
            tokens.add(s)
    return tokens


def _resolve_default_paths(project_root: Path) -> tuple[Path, Path, Path]:
    base = project_root / "data" / "processed"
    return (
        base / "custom_stoplist.txt",
        base / "custom_stoplist.txt.bak_20260519_221137",
        base / "custom_stoplist.txt.bak_20260520_080905",
    )


def _zipf_en(token: str) -> Optional[float]:
    if _zipf_frequency is None:
        return None
    return float(_zipf_frequency(token, "en"))


def _maybe_load_spacy(model: str):
    try:
        import spacy
    except ImportError:  # pragma: no cover
        return None
    try:
        return spacy.load(model, disable=["parser", "tagger", "lemmatizer"])
    except Exception:  # pragma: no cover
        return None


def _person_probe(token: str, nlp) -> Optional[bool]:
    if nlp is None:
        return None
    doc = nlp(f"I met {token} yesterday.")
    return any(ent.label_ == "PERSON" and token in ent.text.lower() for ent in doc.ents)


def _parse_args() -> AuditConfig:
    project_root = Path(__file__).resolve().parents[3]
    current_default, old_default, new_default = _resolve_default_paths(project_root)
    output_default = (
        project_root
        / "data"
        / "processed"
        / f"stoplist_non_name_audit_{_utc_stamp()}.csv"
    )

    parser = argparse.ArgumentParser(description="Audit likely non-name stoplist tokens.")
    parser.add_argument("--current", type=Path, default=current_default)
    parser.add_argument("--backup-old", type=Path, default=old_default)
    parser.add_argument("--backup-new", type=Path, default=new_default)
    parser.add_argument(
        "--target-delta",
        choices=["new", "old", "union"],
        default="new",
        help="new=current-backup_new, old=current-backup_old, union=union of both deltas",
    )
    parser.add_argument("--zipf-threshold", type=float, default=4.0)
    parser.add_argument("--top-n", type=int, default=50)
    parser.add_argument("--output-csv", type=Path, default=output_default)
    parser.add_argument("--enable-spacy-probe", action="store_true")
    parser.add_argument("--spacy-model", type=str, default="en_core_web_sm")

    args = parser.parse_args()
    return AuditConfig(
        current_path=args.current,
        backup_old_path=args.backup_old,
        backup_new_path=args.backup_new,
        target_delta=args.target_delta,
        zipf_threshold=args.zipf_threshold,
        top_n=max(1, int(args.top_n)),
        output_csv=args.output_csv,
        enable_spacy_probe=bool(args.enable_spacy_probe),
        spacy_model=args.spacy_model,
    )


def main() -> None:
    cfg = _parse_args()

    current = _read_stoplist_tokens(cfg.current_path)
    backup_old = _read_stoplist_tokens(cfg.backup_old_path)
    backup_new = _read_stoplist_tokens(cfg.backup_new_path)

    delta_old = current - backup_old
    delta_new = current - backup_new
    if cfg.target_delta == "old":
        target = delta_old
    elif cfg.target_delta == "union":
        target = delta_old | delta_new
    else:
        target = delta_new

    nlp = None
    if cfg.enable_spacy_probe:
        nlp = _maybe_load_spacy(cfg.spacy_model)
        if nlp is None:
            print(
                "Warning: spaCy probe requested but model/import unavailable; continuing without probe.",
                flush=True,
            )

    rows: list[dict[str, object]] = []
    for token in sorted(target):
        has_non_ascii = any(ord(ch) > 127 for ch in token)
        contains_hyphen_or_apostrophe = ("-" in token) or ("'" in token)
        is_alpha_only = token.isalpha()
        len_lt_3 = len(token) < 3
        zipf = _zipf_en(token)
        looks_like_common_word = zipf is not None and zipf >= cfg.zipf_threshold
        spacy_person_in_context = _person_probe(token, nlp) if nlp is not None else None

        likely_non_name = bool(
            looks_like_common_word
            and (spacy_person_in_context is False or spacy_person_in_context is None)
        )

        rows.append(
            {
                "token": token,
                "len": len(token),
                "has_non_ascii": has_non_ascii,
                "contains_hyphen_or_apostrophe": contains_hyphen_or_apostrophe,
                "is_alpha_only": is_alpha_only,
                "len_lt_3": len_lt_3,
                "zipf_en": zipf,
                "looks_like_common_word": looks_like_common_word,
                "spacy_person_in_context": spacy_person_in_context,
                "likely_non_name": likely_non_name,
            }
        )

    cfg.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "token",
        "len",
        "has_non_ascii",
        "contains_hyphen_or_apostrophe",
        "is_alpha_only",
        "len_lt_3",
        "zipf_en",
        "looks_like_common_word",
        "spacy_person_in_context",
        "likely_non_name",
    ]
    with open(cfg.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    suspects = [r for r in rows if r["likely_non_name"]]
    suspects.sort(key=lambda r: (r["zipf_en"] if r["zipf_en"] is not None else -1.0), reverse=True)

    print(f"Current tokens: {len(current):,}")
    print(f"Delta vs old backup: {len(delta_old):,}")
    print(f"Delta vs new backup: {len(delta_new):,}")
    print(f"Audit target ({cfg.target_delta}): {len(target):,}")
    print(f"Likely non-name suspects: {len(suspects):,}")
    print(f"CSV: {cfg.output_csv}")
    print("")
    print(f"Top {min(cfg.top_n, len(suspects))} suspects:")
    for row in suspects[: cfg.top_n]:
        zipf = row["zipf_en"]
        zipf_str = "NA" if zipf is None else f"{float(zipf):.2f}"
        print(f"- {row['token']} (zipf={zipf_str}, person_probe={row['spacy_person_in_context']})")


if __name__ == "__main__":
    main()
