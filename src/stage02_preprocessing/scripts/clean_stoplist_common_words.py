#!/usr/bin/env python3
"""Remove common English words wrongly swept into the character-name stoplist.

Why: the spaCy name extraction added ordinary vocabulary (love, kiss, wedding,
money, kill, said, ...) to ``data/processed/custom_stoplist.txt``. Those tokens
are then hidden from every BERTopic c-TF-IDF representation, crippling topic
keywords and coherence scoring on the romance corpus.

Decision rule per stoplist token:
1. zipf(en) >= ``--hyper-common-zipf``  -> remove (just/time/know tier; no
   character name justifies hiding these).
2. zipf(en) >= ``--zipf-threshold`` AND corpus lowercase-usage share >=
   ``--lowercase-share`` -> remove. Case statistics come from a sample of the
   raw ``sentences_train.csv`` (case-preserving, unlike the OCTIS corpus):
   names occur capitalized ("Betty"), common words occur lowercase ("kiss").
3. Otherwise keep (rare tokens and capitalized-usage tokens are treated as
   plausible character names).

Only single-token alphabetic lines are considered; multi-word or hyphenated
entries never match the topic vectorizer's token pattern anyway.

Dry-run by default; ``--apply`` writes a timestamped backup then rewrites the
stoplist in place. A per-token report CSV is always written.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from wordfreq import zipf_frequency

PROJECT_ROOT = Path(__file__).resolve().parents[3]

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z']+")
ALPHA_LINE_RE = re.compile(r"^[a-z][a-z']*$")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stoplist",
        type=Path,
        default=PROJECT_ROOT / "data" / "processed" / "custom_stoplist.txt",
    )
    parser.add_argument(
        "--train-csv",
        type=Path,
        default=PROJECT_ROOT
        / "data"
        / "raw"
        / "romance_subdataset_filtered_v3"
        / "sentences_train.csv",
        help="Case-preserving sentence CSV used for lowercase-share statistics.",
    )
    parser.add_argument("--zipf-threshold", type=float, default=3.5)
    parser.add_argument("--hyper-common-zipf", type=float, default=5.0)
    parser.add_argument("--lowercase-share", type=float, default=0.5)
    parser.add_argument("--sample-rows", type=int, default=3_000_000)
    parser.add_argument("--chunk-size", type=int, default=250_000)
    parser.add_argument("--apply", action="store_true", help="Rewrite the stoplist (default: dry run).")
    parser.add_argument(
        "--report-csv",
        type=Path,
        default=PROJECT_ROOT
        / "data"
        / "processed"
        / f"stoplist_cleaning_report_{_utc_stamp()}.csv",
    )
    return parser.parse_args()


def _case_stats(train_csv: Path, targets: set[str], *, sample_rows: int, chunk_size: int) -> dict[str, tuple[int, int]]:
    """Return {token_lower: (lowercase_count, other_case_count)} from a corpus sample."""
    lower_counts: Counter[str] = Counter()
    total_counts: Counter[str] = Counter()
    rows_seen = 0
    reader = pd.read_csv(train_csv, usecols=["sentence"], chunksize=chunk_size)
    for chunk in reader:
        for sent in chunk["sentence"].dropna():
            for match in TOKEN_RE.finditer(sent):
                # Skip sentence-initial tokens (incl. after an opening quote):
                # their capitalization is orthographic, not evidence of a name.
                if match.start() <= 1:
                    continue
                tok = match.group(0)
                low = tok.lower()
                if low not in targets:
                    continue
                total_counts[low] += 1
                if tok == low:
                    lower_counts[low] += 1
        rows_seen += len(chunk)
        print(
            f"[case-scan] rows={rows_seen:,} tracked_tokens={len(total_counts):,}",
            flush=True,
        )
        if rows_seen >= sample_rows:
            break
    return {t: (lower_counts.get(t, 0), total_counts[t] - lower_counts.get(t, 0)) for t in total_counts}


def main() -> None:
    args = _parse_args()

    raw_lines = args.stoplist.read_text(encoding="utf-8", errors="replace").splitlines()
    print(f"Stoplist lines: {len(raw_lines):,}")

    candidates: dict[str, float] = {}
    for line in raw_lines:
        tok = line.strip().lower()
        if not ALPHA_LINE_RE.match(tok):
            continue
        z = float(zipf_frequency(tok, "en"))
        if z >= args.zipf_threshold:
            candidates[tok] = z
    print(f"Common-word candidates (zipf >= {args.zipf_threshold}): {len(candidates):,}")

    hyper = {t for t, z in candidates.items() if z >= args.hyper_common_zipf}
    needs_case = {t for t in candidates if t not in hyper}
    print(
        f"Hyper-common (zipf >= {args.hyper_common_zipf}, removed unconditionally): {len(hyper):,}; "
        f"case-checked candidates: {len(needs_case):,}"
    )

    stats = _case_stats(
        args.train_csv, needs_case, sample_rows=args.sample_rows, chunk_size=args.chunk_size
    )

    remove: set[str] = set(hyper)
    rows: list[dict[str, object]] = []
    for tok, z in sorted(candidates.items(), key=lambda kv: -kv[1]):
        low, other = stats.get(tok, (0, 0))
        total = low + other
        share = (low / total) if total else None
        if tok in hyper:
            decision, reason = "remove", "hyper_common"
        elif total == 0:
            decision, reason = "keep", "not_in_sample"
        elif share is not None and share >= args.lowercase_share:
            decision, reason = "remove", "lowercase_usage"
            remove.add(tok)
        else:
            decision, reason = "keep", "capitalized_usage"
        rows.append(
            {
                "token": tok,
                "zipf_en": z,
                "lowercase_count": low,
                "other_case_count": other,
                "lowercase_share": round(share, 4) if share is not None else "",
                "decision": decision,
                "reason": reason,
            }
        )

    args.report_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(args.report_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    kept_names = [r["token"] for r in rows if r["decision"] == "keep" and r["reason"] == "capitalized_usage"]
    removed = [r["token"] for r in rows if r["decision"] == "remove"]
    print(f"\nDecision: remove {len(removed):,} tokens, keep {len(rows) - len(removed):,} candidates")
    print(f"Report: {args.report_csv}")
    print(f"Sample removed: {removed[:25]}")
    print(f"Sample kept as names (capitalized usage): {kept_names[:25]}")

    if not args.apply:
        print("\nDry run only (pass --apply to rewrite the stoplist).")
        return

    backup = args.stoplist.with_name(args.stoplist.name + f".bak_{_utc_stamp()}")
    backup.write_text("\n".join(raw_lines) + "\n", encoding="utf-8")
    cleaned = [line for line in raw_lines if line.strip().lower() not in remove]
    args.stoplist.write_text("\n".join(cleaned) + "\n", encoding="utf-8")
    print(f"\nBackup: {backup}")
    print(f"Rewrote {args.stoplist}: {len(raw_lines):,} -> {len(cleaned):,} lines")


if __name__ == "__main__":
    sys.exit(main())
