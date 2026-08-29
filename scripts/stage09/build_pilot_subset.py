#!/usr/bin/env python
"""Build a stratified pilot subset of Stage09 topic metadata.

The pilot deliberately over-samples the cases the v2.5 prompt hardening targets, so a
30-topic run is informative about whether the hardening worked:

  - topics currently mapped to ``uncertain_interpretable``
  - topics whose current ``evidence_quality`` is ``low``
  - plausible ``3.1`` (relief / payoff) candidates that v2 routed elsewhere
  - high-confidence control topics, to catch regressions on cases v2 already got right

Writes a subset of ``topic_metadata_v3.json`` that can be passed straight to
``zeroshot_taxonomy_openrouter.py --labels-json``.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Any, Dict, List

# Relief / resolution / felt-safety vocabulary used to spot plausible 3.1 candidates.
PAYOFF_PATTERN = re.compile(
    r"\b(relief|reliev\w*|relax\w*|loosen\w*|eased?|easing|calm\w*|settled|safe|safety|"
    r"reassur\w*|content\w*|peace\w*|grateful|gratitude|finally|at last|no longer|"
    r"breath\w* (?:out|easy)|tension (?:left|drained))\b",
    re.IGNORECASE,
)

# Categories that v2 tends to absorb 3.1 into.
PAYOFF_HOST_IDS = {"4.5", "4.6", "3.2", "3.3", "9.3", "1.7", "uncertain_interpretable"}


def topic_blob(meta: Dict[str, Any]) -> str:
    parts: List[str] = [
        str(meta.get("label", "")),
        str(meta.get("scene_summary", "")),
        " ".join(meta.get("keywords") or []),
        " ".join(meta.get("snippets") or []),
    ]
    return " ".join(parts)


def select_pilot_ids(
    metadata: Dict[str, Dict[str, Any]],
    mappings: Dict[str, Dict[str, Any]],
    *,
    n_uncertain: int,
    n_low_evidence: int,
    n_payoff: int,
    n_control: int,
    seed: int,
) -> Dict[str, List[str]]:
    rng = random.Random(seed)
    chosen: set[str] = set()
    strata: Dict[str, List[str]] = {}

    def take(pool: List[str], k: int, name: str) -> None:
        available = [tid for tid in pool if tid not in chosen]
        rng.shuffle(available)
        picked = sorted(available[:k], key=int)
        strata[name] = picked
        chosen.update(picked)

    uncertain = [
        tid for tid, m in mappings.items()
        if m.get("main_category_id") == "uncertain_interpretable"
    ]
    take(uncertain, n_uncertain, "uncertain_interpretable")

    low_evidence = [
        tid for tid, m in mappings.items()
        if str(m.get("evidence_quality", "")).lower() == "low"
    ]
    take(low_evidence, n_low_evidence, "low_evidence_quality")

    payoff = [
        tid for tid, m in mappings.items()
        if m.get("main_category_id") in PAYOFF_HOST_IDS
        and tid in metadata
        and PAYOFF_PATTERN.search(topic_blob(metadata[tid]))
    ]
    take(payoff, n_payoff, "payoff_3_1_candidates")

    control = [
        tid for tid, m in mappings.items()
        if str(m.get("evidence_quality", "")).lower() == "high"
        and float(m.get("confidence") or 0) >= 0.8
        and m.get("main_category_id") != "uncertain_interpretable"
    ]
    take(control, n_control, "high_confidence_control")

    return strata


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--metadata-json", type=Path, required=True, help="Stage09 input topic_metadata_v3.json")
    ap.add_argument("--current-mappings", type=Path, required=True, help="Existing taxonomy_mappings.json to stratify on")
    ap.add_argument("--output-json", type=Path, required=True, help="Where to write the pilot metadata subset")
    ap.add_argument("--n-uncertain", type=int, default=10)
    ap.add_argument("--n-low-evidence", type=int, default=10)
    ap.add_argument("--n-payoff", type=int, default=5)
    ap.add_argument("--n-control", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    metadata = json.loads(args.metadata_json.read_text(encoding="utf-8"))
    mappings = json.loads(args.current_mappings.read_text(encoding="utf-8"))

    strata = select_pilot_ids(
        metadata,
        mappings,
        n_uncertain=args.n_uncertain,
        n_low_evidence=args.n_low_evidence,
        n_payoff=args.n_payoff,
        n_control=args.n_control,
        seed=args.seed,
    )

    pilot_ids = sorted({tid for ids in strata.values() for tid in ids}, key=int)
    missing = [tid for tid in pilot_ids if tid not in metadata]
    if missing:
        raise SystemExit(f"Pilot ids absent from metadata: {missing}")

    subset = {tid: metadata[tid] for tid in pilot_ids}
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(subset, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest = {
        "n_topics": len(pilot_ids),
        "seed": args.seed,
        "source_metadata": str(args.metadata_json),
        "source_mappings": str(args.current_mappings),
        "strata": strata,
        "topic_ids": pilot_ids,
    }
    manifest_path = args.output_json.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Wrote {len(pilot_ids)} pilot topics -> {args.output_json}")
    for name, ids in strata.items():
        print(f"  {name:26s} n={len(ids):2d}  {ids}")
    print(f"Manifest -> {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
