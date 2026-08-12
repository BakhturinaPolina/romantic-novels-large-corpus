#!/usr/bin/env python3
"""Corpus-level probe: where do axis-lexicon sentences actually land in call-49?

Complements the topic-word audit. For each pre-registered axis it measures:
  1. prevalence  - share of sentences containing the lexicon (is the theme in the text?)
  2. dispersion  - how matched sentences spread over the 373 topics
  3. capture     - top topics that absorb them, with Stage08 labels

Reads a spread sample of parquet row groups with column pruning, so it stays
cheap even while the Stage10 aggregator is running.

Usage:
  .venv/bin/python scripts/analysis/probe_axis_sentences_call49.py --row-groups 60
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import sys

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_axis_lexicon_call49 import LEXICONS, compile_probes  # noqa: E402


def load_labels(path: Path) -> dict[int, str]:
    if not path.exists():
        return {}
    raw = json.load(open(path))
    return {int(k): v.get("label", "") for k, v in raw.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--parquet",
        type=Path,
        default=Path(
            "results/experiments/v4_l12_granular_final_call49/full_corpus_infer/"
            "sentence_topics_test.parquet"
        ),
    )
    ap.add_argument(
        "--labels",
        type=Path,
        default=Path(
            "results/stage08_llm_labeling/placeholder_v4_call49/production/"
            "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_"
            "paraphrase-MiniLM-L6-v2_v3_topic_labeling.json"
        ),
    )
    ap.add_argument("--row-groups", type=int, default=60, help="Row groups sampled, spread evenly")
    ap.add_argument("--out-dir", type=Path, default=Path("results/reports/call49/axis_audit"))
    ap.add_argument(
        "--cache",
        type=Path,
        default=Path("results/reports/call49/axis_audit/_sample_cache.parquet"),
        help="Reuse/write the sampled columns so re-probing skips the big scan",
    )
    args = ap.parse_args()

    labels = load_labels(args.labels)

    if args.cache and args.cache.exists():
        print(f"reusing cached sample: {args.cache}")
        tbl = pq.read_table(args.cache)
    else:
        pf = pq.ParquetFile(args.parquet)
        total_rg = pf.num_row_groups
        k = min(args.row_groups, total_rg)
        idx = sorted(set(np.linspace(0, total_rg - 1, k).astype(int).tolist()))
        print(f"parquet: {args.parquet.name}")
        print(f"sampling {len(idx)}/{total_rg} row groups (spread)\n")
        tbl = pf.read_row_groups(
            idx, columns=["work_id", "sentence", "topic", "max_topic_prob"]
        )
        if args.cache:
            args.cache.parent.mkdir(parents=True, exist_ok=True)
            pq.write_table(tbl, args.cache, compression="zstd")
            print(f"cached sample → {args.cache}")
    sentences = tbl.column("sentence").to_pylist()
    topics = np.asarray(tbl.column("topic").to_pylist())
    maxp = np.asarray(tbl.column("max_topic_prob").to_pylist(), dtype=float)
    works = np.asarray(tbl.column("work_id").to_pylist())
    n = len(sentences)
    n_books = len(set(works.tolist()))
    print(f"sampled sentences: {n:,} across {n_books:,} books")
    print(f"baseline outlier share: {float((topics == -1).mean()) * 100:.2f}%")
    print(f"baseline mean max_topic_prob: {maxp.mean():.4f}\n")

    probes = {name: compile_probes(spec["terms"]) for name, spec in LEXICONS.items()}

    summary_rows = []
    capture_rows = []

    header = (
        f"{'axis':<26} {'role':<18} {'match%':>8} {'n_match':>9} "
        f"{'topics':>7} {'top1%':>7} {'top5%':>7} {'out%':>6} {'meanP':>7}"
    )
    print(header)
    print("-" * len(header))

    for axis, rx in probes.items():
        hits = [i for i, s in enumerate(sentences) if s and rx.search(s)]
        n_hit = len(hits)
        if n_hit == 0:
            print(f"{axis:<26} {LEXICONS[axis]['role']:<18} {0.0:>8.4f} {0:>9} "
                  f"{0:>7} {'-':>7} {'-':>7} {'-':>6} {'-':>7}")
            summary_rows.append(
                {
                    "axis": axis,
                    "role": LEXICONS[axis]["role"],
                    "match_pct": 0.0,
                    "n_match": 0,
                    "n_topics_touched": 0,
                    "top1_share_pct": None,
                    "top5_share_pct": None,
                    "outlier_pct": None,
                    "mean_max_prob": None,
                }
            )
            continue

        h_topics = topics[hits]
        h_maxp = maxp[hits]
        non_out = h_topics[h_topics != -1]
        cnt = Counter(non_out.tolist())
        ranked = cnt.most_common()
        tot = max(len(non_out), 1)
        top1 = 100 * ranked[0][1] / tot if ranked else 0.0
        top5 = 100 * sum(c for _, c in ranked[:5]) / tot if ranked else 0.0
        out_pct = 100 * float((h_topics == -1).mean())
        match_pct = 100 * n_hit / n

        print(
            f"{axis:<26} {LEXICONS[axis]['role']:<18} {match_pct:>8.4f} {n_hit:>9,} "
            f"{len(cnt):>7} {top1:>7.1f} {top5:>7.1f} {out_pct:>6.2f} {h_maxp.mean():>7.4f}"
        )

        summary_rows.append(
            {
                "axis": axis,
                "role": LEXICONS[axis]["role"],
                "match_pct": round(match_pct, 4),
                "n_match": n_hit,
                "n_topics_touched": len(cnt),
                "top1_share_pct": round(top1, 2),
                "top5_share_pct": round(top5, 2),
                "outlier_pct": round(out_pct, 2),
                "mean_max_prob": round(float(h_maxp.mean()), 4),
            }
        )

        for tid, c in ranked[:10]:
            capture_rows.append(
                {
                    "axis": axis,
                    "role": LEXICONS[axis]["role"],
                    "topic_id": int(tid),
                    "n_matched_sentences": c,
                    "share_of_axis_pct": round(100 * c / tot, 2),
                    "label": labels.get(int(tid), ""),
                }
            )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with open(args.out_dir / "axis_sentence_prevalence.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)
    if capture_rows:
        with open(args.out_dir / "axis_sentence_capture_topics.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(capture_rows[0].keys()))
            w.writeheader()
            w.writerows(capture_rows)

    for axis in LEXICONS:
        rows = [r for r in capture_rows if r["axis"] == axis][:8]
        if not rows:
            continue
        print(f"\n### {axis} — topics absorbing matched sentences")
        for r in rows:
            print(
                f"  t{r['topic_id']:<4} {r['share_of_axis_pct']:>5.1f}%  "
                f"n={r['n_matched_sentences']:<6} {r['label'][:56]}"
            )

    print(f"\nwrote {args.out_dir / 'axis_sentence_prevalence.csv'}")
    print(f"wrote {args.out_dir / 'axis_sentence_capture_topics.csv'}")


if __name__ == "__main__":
    main()
