#!/usr/bin/env python3
"""Compare compare-fit candidates on honest (cleaned-stoplist) representations.

Reads ``final_compare/call_N/repr_stoplist_v2/`` outputs produced by
``recompute_topic_representations.py`` and reports, per candidate:

- honest vs original coherence / diversity / topic count
- how many topics carry each hypothesis-relevant vocabulary bucket
  (>= ``--min-hits`` bucket words within the topic's top-``--top-n`` keywords)
- example topics per bucket, for manual reading

Buckets are keyword proxies for the taxonomy axes used by H1-H6 in
SCIENTIFIC_README.md; they are a coverage screen, not a classifier.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# label -> (run_id, bo_call)
CANDIDATES: dict[str, tuple[str, int]] = {
    "L6_16": ("v4_l6_granular_phase2_pareto", 16),
    "MPNet_131": ("v4_mpnet_granular_phase2_pareto", 131),
    "MPNet_133": ("v4_mpnet_granular_phase2_pareto", 133),
    "MPNet_80": ("v4_mpnet_granular_phase2_pareto", 80),
    "L12_73": ("v4_l12_granular_phase2_pareto", 73),
    "L12_49": ("v4_l12_granular_phase2_pareto", 49),
    "L12_11": ("v4_l12_granular_phase2_pareto", 11),
    "MPNet_38": ("v4_mpnet_granular_phase2_pareto", 38),
}

BUCKETS: dict[str, set[str]] = {
    "explicit_sex_2.3": {
        "cock", "pussy", "clit", "nipples", "nipple", "thrust", "thrusts", "orgasm",
        "moan", "moaned", "cum", "suck", "sucked", "licked", "lick", "breasts",
        "breast", "naked", "thighs", "erection", "arousal", "groaned", "shaft",
        "climax", "panties", "condom",
    },
    "commit_hea_4.5": {
        "wedding", "marry", "married", "marriage", "bride", "groom", "proposal",
        "propose", "engaged", "engagement", "ring", "vows", "forever", "husband",
        "wife", "honeymoon", "aisle",
    },
    "protective_care_4.6": {
        "protect", "protecting", "protective", "protection", "safe", "safety",
        "careful", "gentle", "comfort", "comforted", "care", "soothe", "reassure",
        "shield", "guard",
    },
    "possessive_jealousy_4.7": {
        "jealous", "jealousy", "possessive", "possession", "claimed", "claiming",
        "territorial", "belong", "belongs", "belonged", "mine", "envy",
    },
    "wealth_luxury_6.x": {
        "money", "rich", "wealthy", "wealth", "billionaire", "millionaire",
        "mansion", "penthouse", "yacht", "luxury", "luxurious", "expensive",
        "fortune", "estate", "limo", "designer", "jet", "champagne", "diamond",
        "diamonds", "inheritance",
    },
    "econ_dependency_6.4": {
        "job", "pay", "paid", "salary", "rent", "debt", "loan", "bank", "account",
        "contract", "afford", "bills", "broke", "poor", "working", "employer",
    },
    "danger_dark_7.x": {
        "gun", "knife", "blood", "kill", "killed", "killer", "murder", "dead",
        "danger", "dangerous", "threat", "threatened", "attack", "attacked",
        "escape", "kidnapped", "stalker", "shoot", "shot", "weapon", "hostage",
    },
    "conflict_negemo_3.x": {
        "angry", "anger", "furious", "yelled", "argument", "argue", "arguing",
        "fight", "fought", "tears", "crying", "cried", "hurt", "betrayed",
        "lied", "liar", "sorry", "apologize", "apology", "guilt", "regret",
    },
    "family_children": {
        "baby", "babies", "pregnant", "pregnancy", "kids", "children", "child",
        "son", "daughter", "mom", "mother", "father", "dad", "parents", "family",
        "brother", "sister", "birth",
    },
    "paranormal": {
        "vampire", "werewolf", "wolf", "shifter", "shifting", "witch", "magic",
        "demon", "dragon", "fae", "pack", "mate", "immortal", "spell", "fangs",
    },
    "profession_setting": {
        "doctor", "hospital", "nurse", "patient", "office", "boss", "lawyer",
        "cop", "detective", "ranch", "cowboy", "chef", "firefighter", "soldier",
        "military", "teacher", "professor", "medical",
    },
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidates",
        nargs="*",
        default=None,
        help=f"Subset of {sorted(CANDIDATES)} (default: all available on disk).",
    )
    parser.add_argument("--subdir", type=str, default="repr_stoplist_v2")
    parser.add_argument("--top-n", type=int, default=10, help="Keyword depth per topic.")
    parser.add_argument("--min-hits", type=int, default=2, help="Bucket words needed to count a topic.")
    parser.add_argument("--examples", type=int, default=1, help="Example topics printed per bucket.")
    parser.add_argument("--out-csv", type=Path, default=None)
    return parser.parse_args()


def _candidate_dir(run_id: str, call: int, subdir: str) -> Path:
    return PROJECT_ROOT / "results" / "experiments" / run_id / "final_compare" / f"call_{call}" / subdir


def main() -> None:
    args = _parse_args()
    labels = args.candidates or list(CANDIDATES)

    metric_rows: list[dict[str, object]] = []
    coverage: dict[str, dict[str, int]] = {}
    examples: dict[str, dict[str, list[str]]] = {}

    for label in labels:
        run_id, call = CANDIDATES[label]
        d = _candidate_dir(run_id, call, args.subdir)
        if not (d / "top_words.csv").exists():
            print(f"[skip] {label}: no {args.subdir} output at {d}")
            continue

        m = json.loads((d / "metrics.json").read_text(encoding="utf-8"))
        orig = m.get("original", {})
        metric_rows.append(
            {
                "model": label,
                "n_topics": int(m["n_topics"]),
                "n_orig": orig.get("n_topics"),
                "c_v_honest": round(float(m["coherence_c_v"]), 3),
                "c_v_orig": round(float(orig.get("coherence_c_v") or 0.0), 3),
                "div_honest": round(float(m["topic_diversity"]), 3),
                "div_orig": round(float(orig.get("topic_diversity") or 0.0), 3),
                "outlier_rate": round(float(m["outlier_rate"]), 3),
            }
        )

        tw = pd.read_csv(d / "top_words.csv")
        tw = tw[(tw["topic"] != -1) & (tw["rank"] <= args.top_n)]
        per_topic = tw.sort_values("rank").groupby("topic")["word"].apply(list)

        counts: dict[str, int] = {}
        for bucket, words in BUCKETS.items():
            hits = [t for t, ws in per_topic.items() if len(words.intersection(ws)) >= args.min_hits]
            counts[bucket] = len(hits)
            if hits:
                examples.setdefault(label, {})[bucket] = [
                    f"T{t}: " + ", ".join(per_topic[t][:8]) for t in hits[: args.examples]
                ]
        counts["n_topics"] = int(per_topic.shape[0])
        coverage[label] = counts

    if not metric_rows:
        print("No candidates found.")
        return

    metrics_df = pd.DataFrame(metric_rows).sort_values("n_topics", ascending=False)
    print("=== Honest vs original metrics (same clustering) ===")
    print(metrics_df.to_string(index=False))

    cov_df = pd.DataFrame(coverage)
    cov_df = cov_df[metrics_df["model"].tolist()]
    print(
        f"\n=== Topics carrying each bucket (>= {args.min_hits} bucket words in top-{args.top_n}) ==="
    )
    print(cov_df.to_string())

    bucket_rows = cov_df.drop(index="n_topics")
    print("\n=== Buckets with zero coverage ===")
    for label in cov_df.columns:
        missing = bucket_rows.index[bucket_rows[label] == 0].tolist()
        print(f"  {label:10s} {'none' if not missing else ', '.join(missing)}")

    print("\n=== Example topics ===")
    for label in cov_df.columns:
        print(f"--- {label} ---")
        for bucket, lines in examples.get(label, {}).items():
            for line in lines:
                print(f"  {bucket:24s} {line}")

    if args.out_csv:
        args.out_csv.parent.mkdir(parents=True, exist_ok=True)
        merged = metrics_df.set_index("model").join(cov_df.T)
        merged.to_csv(args.out_csv)
        print(f"\nWrote {args.out_csv}")


if __name__ == "__main__":
    main()
