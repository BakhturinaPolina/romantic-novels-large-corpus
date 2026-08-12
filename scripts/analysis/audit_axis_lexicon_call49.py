#!/usr/bin/env python3
"""Pre-registered lexicon audit of call-49 topics.

Falsifiability guard: the same probe runs for target axes (luxury, security),
positive controls (axes we already know exist) and a negative control (an axis
that should be absent). "Not found" is only meaningful relative to how the
negative control scores.

Usage:
  .venv/bin/python scripts/analysis/audit_axis_lexicon_call49.py
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

# Word-stem probes; matched with word boundaries against topic words / labels.
LEXICONS: dict[str, dict[str, list[str]]] = {
    "luxury_H3": {
        "role": "target",
        "terms": [
            "luxury", "luxurious", "wealth", "wealthy", "rich", "fortune", "millionaire",
            "billionaire", "mansion", "estate", "penthouse", "villa", "chateau", "manor",
            "limousine", "limo", "yacht", "jet", "chauffeur", "butler", "maid", "servant",
            "diamond", "diamonds", "jewel", "jewels", "jewelry", "emerald", "sapphire",
            "pearls", "gown", "designer", "couture", "silk", "satin", "velvet", "cashmere",
            "champagne", "caviar", "vintage", "crystal", "chandelier", "marble", "gold",
            "golden", "expensive", "priceless", "extravagant", "opulent", "lavish",
            "elegant", "exquisite", "boutique", "gala", "ballroom", "ball", "tuxedo",
            "cufflinks", "rolex", "ferrari", "porsche", "bentley", "cartier", "gucci",
        ],
    },
    "security_H4": {
        "role": "target",
        "terms": [
            "safe", "safely", "safety", "secure", "security", "protect", "protected",
            "protecting", "protection", "protective", "protector", "guard", "guarded",
            "shield", "shielded", "defend", "defended", "shelter", "sheltered", "refuge",
            "sanctuary", "haven", "harm", "danger", "dangerous", "threat", "threatened",
            "rescue", "rescued", "saved", "save", "trust", "trusted", "reassure",
            "reassured", "comfort", "comforted", "soothe", "soothed", "calm", "steady",
            "stability", "reliable", "dependable", "provider", "provide", "care",
            "watch", "watching", "vigilant", "wary", "risk", "protectively",
        ],
    },
    # High-precision variants: polysemous words dropped ("rich", "gold", "silk",
    # "ball", "care", "watch") so prevalence is not inflated by incidental usage.
    "luxury_strict": {
        "role": "target_strict",
        "terms": [
            "luxury", "luxurious", "millionaire", "billionaire", "mansion",
            "penthouse", "chateau", "limousine", "chauffeur", "butler",
            "yacht", "caviar", "champagne", "chandelier", "couture",
            "opulent", "lavish", "extravagant", "tuxedo", "cufflinks",
            "rolex", "ferrari", "porsche", "bentley", "cartier",
            "diamond necklace", "designer dress", "private jet",
        ],
    },
    "security_strict": {
        "role": "target_strict",
        "terms": [
            "protect", "protected", "protecting", "protection", "protective",
            "protectively", "protector", "keep you safe", "keep her safe",
            "keep him safe", "safe with me", "shield", "shielded", "safeguard",
            "guard", "guarding", "sanctuary", "refuge", "haven",
        ],
    },
    "kissing_control": {
        "role": "positive_control",
        "terms": [
            "kiss", "kissed", "kisses", "kissing", "lips", "mouth", "tongue",
            "brushed", "nibbled", "lingered", "breathless",
        ],
    },
    "wedding_hea_control": {
        "role": "positive_control",
        "terms": [
            "wedding", "married", "marry", "marriage", "bride", "groom", "vows",
            "engaged", "engagement", "husband", "wife", "honeymoon", "aisle",
            "forever", "always", "future",
        ],
    },
    "possessive_control": {
        "role": "positive_control",
        "terms": [
            "mine", "belong", "belongs", "belonged", "possess", "possessive",
            "jealous", "jealousy", "claim", "claimed", "own", "owned", "rival",
        ],
    },
    "spaceflight_negcontrol": {
        "role": "negative_control",
        "terms": [
            "spacecraft", "spaceship", "orbit", "orbital", "astronaut", "galaxy",
            "nebula", "asteroid", "cockpit", "warp", "hyperspace", "telescope",
            "satellite", "lunar", "interstellar",
        ],
    },
    "accounting_negcontrol": {
        "role": "negative_control",
        "terms": [
            "invoice", "ledger", "audit", "spreadsheet", "depreciation", "payroll",
            "receivable", "taxable", "amortization", "quarterly", "balance sheet",
        ],
    },
}


def compile_probes(terms: list[str]) -> re.Pattern:
    escaped = [re.escape(t) for t in sorted(terms, key=len, reverse=True)]
    return re.compile(r"\b(" + "|".join(escaped) + r")\b", re.IGNORECASE)


def load_topic_words(path: Path) -> dict[str, dict[str, list[str]]]:
    """topic_id -> representation -> list of words."""
    raw = json.load(open(path))
    out: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for rep_name, per_topic in raw.items():
        for tid, entries in per_topic.items():
            words = []
            for e in entries:
                if isinstance(e, dict):
                    w = e.get("word")
                elif isinstance(e, (list, tuple)):
                    w = e[0]
                else:
                    w = e
                if w:
                    words.append(str(w))
            out[tid][rep_name] = words
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--topics",
        type=Path,
        default=Path(
            "results/stage06_name_cleaning/placeholder_v4_call49/"
            "cleaned_topics_all_representations.json"
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
    ap.add_argument("--top-n", type=int, default=10, help="Top words per representation to probe")
    ap.add_argument("--out-dir", type=Path, default=Path("results/reports/call49/axis_audit"))
    args = ap.parse_args()

    topic_words = load_topic_words(args.topics)
    labels = json.load(open(args.labels)) if args.labels.exists() else {}
    args.out_dir.mkdir(parents=True, exist_ok=True)

    probes = {name: compile_probes(spec["terms"]) for name, spec in LEXICONS.items()}

    rows = []
    per_axis_hits: dict[str, list[dict]] = defaultdict(list)

    for tid, reps in topic_words.items():
        if tid == "-1":
            continue
        word_blob = " ".join(
            w for rep in reps.values() for w in rep[: args.top_n]
        )
        lab = labels.get(tid, {})
        label_blob = " ".join(
            str(lab.get(k, ""))
            for k in ("label", "scene_summary", "rationale")
        )
        label_kw = " ".join(str(x) for x in lab.get("keywords", []))
        combined = f"{word_blob} {label_blob} {label_kw}"

        for axis, rx in probes.items():
            w_hits = sorted(set(m.lower() for m in rx.findall(word_blob)))
            l_hits = sorted(set(m.lower() for m in rx.findall(f"{label_blob} {label_kw}")))
            if not w_hits and not l_hits:
                continue
            entry = {
                "topic_id": int(tid),
                "axis": axis,
                "role": LEXICONS[axis]["role"],
                "n_word_hits": len(w_hits),
                "n_label_hits": len(l_hits),
                "word_hits": ";".join(w_hits),
                "label_hits": ";".join(l_hits),
                "label": lab.get("label", ""),
                "content_type": lab.get("content_type", ""),
                "exclude_from_axes": lab.get("exclude_from_axes", ""),
                "is_noise": lab.get("is_noise", ""),
                "top_main_words": ",".join(reps.get("Main", [])[: args.top_n]),
            }
            rows.append(entry)
            per_axis_hits[axis].append(entry)

    import csv

    detail_path = args.out_dir / "axis_lexicon_topic_hits.csv"
    fields = list(rows[0].keys()) if rows else []
    with open(detail_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["axis"], -r["n_word_hits"])))

    n_topics = len([t for t in topic_words if t != "-1"])
    print(f"topics probed: {n_topics} | top_n words/rep: {args.top_n}\n")
    print(f"{'axis':<26} {'role':<18} {'topics_hit':>10} {'strong(>=2w)':>13} {'in_topic_words':>15}")
    print("-" * 88)
    summary = []
    for axis, spec in LEXICONS.items():
        hits = per_axis_hits.get(axis, [])
        strong = [h for h in hits if h["n_word_hits"] >= 2]
        in_words = [h for h in hits if h["n_word_hits"] >= 1]
        print(
            f"{axis:<26} {spec['role']:<18} {len(hits):>10} {len(strong):>13} {len(in_words):>15}"
        )
        summary.append(
            {
                "axis": axis,
                "role": spec["role"],
                "topics_hit": len(hits),
                "topics_strong": len(strong),
                "topics_in_words": len(in_words),
                "pct_topics_hit": round(100 * len(hits) / max(n_topics, 1), 2),
            }
        )

    with open(args.out_dir / "axis_lexicon_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)

    for axis in LEXICONS:
        hits = sorted(per_axis_hits.get(axis, []), key=lambda r: -r["n_word_hits"])[:12]
        if not hits:
            continue
        print(f"\n### {axis} — top {len(hits)} topics")
        for h in hits:
            print(
                f"  t{h['topic_id']:<4} w={h['n_word_hits']} l={h['n_label_hits']} "
                f"| {h['label'][:52]:<52} | {h['word_hits'][:60]}"
            )

    print(f"\nwrote {detail_path}")
    print(f"wrote {args.out_dir / 'axis_lexicon_summary.csv'}")


if __name__ == "__main__":
    main()
