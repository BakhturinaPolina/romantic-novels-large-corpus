"""Does the granular fit (call 73) separate hypothesis axes the coarse fit (call 55) merges?

For every usable call 73 topic carrying a hypothesis-relevant Stage08 label, find
which call 55 topic its documents came from, and flag coarse topics that host
topics from opposing axes (e.g. protective care and possessiveness).
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
COMPARE = ROOT / "results/experiments/placeholder_v4_models/final_compare"
QUALITY = ROOT / "results/stage07_topic_quality"
LABELS = ROOT / (
    "results/stage08_llm_labeling/placeholder_v4_call73/production/"
    "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_"
    "paraphrase-MiniLM-L6-v2_v3_topic_labeling.json"
)
OUT = ROOT / "results/reports/stage04/granularity_call55_vs_call73"

# Hypothesis buckets keyed on Stage08 label / scene_summary wording.
# Patterns are matched with word boundaries to avoid substring false positives
# ("care" in "scared", "own" in "town").
BUCKETS = {
    "H1_explicit_sex": r"fuck\w*|cock|thrust\w*|orgasm\w*|pounded|nipple\w*|penetrat\w*|climax\w*|erection",
    "H1_presex_escalation": r"undress\w*|zipper\w*|condom\w*|foreplay|grinding|straddl\w*|arousal|aroused",
    "H1_kiss_affection": r"kiss\w*|hug\w*|embrace\w*|cuddl\w*|nuzzl\w*|caress\w*|snuggl\w*|tender\w*",
    "H2_hea_commitment": r"marry|marriage|married|wedding|vows?|propos\w*|engagement|engaged|forever|commitment",
    "H4_protective_care": r"protect\w*|safe|safety|reassur\w*|comfort\w*|shield\w*|defend\w*|nurs\w*|care|caring|caretak\w*",
    "H4_possessive_jealous": r"mine|possessive\w*|jealous\w*|territorial|claiming|claims?|belongs?",
    "H5_dark_threat": r"threat\w*|gun|rifle|knife|blade|blood|kill\w*|attack\w*|kidnap\w*|danger\w*|revenge|captive|hostage",
    "H6_conflict_repair": r"apolog\w*|sorry|forgive\w*|forgiveness|argument|arguing|blame\w*|confess\w*|reconcil\w*",
    "consent_negotiation": r"consent\w*|permission|stop when asked|says? no|said no|slow down|asking if",
}
BUCKETS = {k: re.compile(rf"\b(?:{v})\b") for k, v in BUCKETS.items()}
OPPOSED = [
    ("H4_protective_care", "H4_possessive_jealous"),
    ("H1_explicit_sex", "H1_kiss_affection"),
    ("H1_explicit_sex", "H2_hea_commitment"),
    ("H5_dark_threat", "H1_kiss_affection"),
]


def bucket_of(lab: dict) -> list[str]:
    text = " ".join(
        str(lab.get(f, "")) for f in ("label", "scene_summary", "sexual_function", "consent_status")
    ).lower()
    hits = [b for b, pat in BUCKETS.items() if pat.search(text)]
    if lab.get("sexual_explicitness") == "explicit" and "H1_explicit_sex" not in hits:
        hits.append("H1_explicit_sex")
    return hits


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    a55 = np.asarray(json.loads((COMPARE / "call_55/model_compare_enriched/topics.json").read_text())["topics"])
    a73 = np.asarray(json.loads((COMPARE / "call_73/model_compare_enriched/topics.json").read_text())["topics"])
    labels = {int(k): v for k, v in json.loads(LABELS.read_text()).items()}

    q73 = pd.read_csv(QUALITY / "placeholder_v4_call73/topic_quality_placeholder_v4_call73.csv")
    q73["posthoc_reason"] = q73["posthoc_reason"].fillna("")
    usable = set(
        q73.loc[
            ~q73["posthoc_reason"].str.contains("tiny_topic|name_contaminated|character_name|publisher"),
            "Topic",
        ]
    )
    q55 = pd.read_csv(QUALITY / "placeholder_v4_call55/topic_quality_placeholder_v4_call55.csv")
    name55 = dict(zip(q55["Topic"], q55["Name"]))

    rows = []
    for t in sorted(usable):
        if t < 0:
            continue
        lab = labels.get(t, {})
        bks = bucket_of(lab)
        if not bks:
            continue
        mask = a73 == t
        parents = Counter(a55[mask].tolist())
        tot = int(mask.sum())
        top_p, top_c = parents.most_common(1)[0]
        rows.append(
            {
                "c73_topic": t,
                "size": tot,
                "label": lab.get("label", ""),
                "buckets": "|".join(bks),
                "explicitness": lab.get("sexual_explicitness", ""),
                "consent": lab.get("consent_status", ""),
                "top_parent_c55": top_p,
                "top_parent_name": "OUTLIER" if top_p < 0 else name55.get(top_p, ""),
                "top_parent_share": round(top_c / tot, 2),
            }
        )
    df = pd.DataFrame(rows).sort_values("size", ascending=False)
    df.to_csv(OUT / "hypothesis_topic_provenance.csv", index=False)

    print(f"usable call73 topics with a hypothesis-relevant label: {len(df)} / {len(usable)}")
    print(f"  of these, carved out of the call55 outlier pool: {(df['top_parent_c55'] < 0).sum()}")
    print()
    for b in BUCKETS:
        sub = df[df["buckets"].str.contains(b)]
        if len(sub):
            from_out = int((sub["top_parent_c55"] < 0).sum())
            print(f"{b:24s} n={len(sub):2d}  docs={int(sub['size'].sum()):6,}  new-from-c55-outliers={from_out}")
    print()

    print("== hypothesis-relevant granular topics and where their text sat in the coarse model ==")
    print(df.head(40).to_string(index=False, max_colwidth=42))
    print()

    # Coarse topics hosting opposing axes.
    host = defaultdict(set)
    for _, r in df.iterrows():
        if r["top_parent_c55"] >= 0:
            for b in r["buckets"].split("|"):
                host[r["top_parent_c55"]].add(b)
    print("== coarse topics that conflate opposing hypothesis axes ==")
    found = False
    for p, bs in sorted(host.items()):
        for x, y in OPPOSED:
            if x in bs and y in bs:
                found = True
                kids = df[df["top_parent_c55"] == p]
                print(f"\nc55 topic {p} ({name55.get(p,'')}) hosts {x} + {y}:")
                print(kids[["c73_topic", "size", "label", "buckets"]].to_string(index=False, max_colwidth=45))
                break
    if not found:
        print("(none at the dominant-parent level)")

    print(f"\nwrote: {OUT / 'hypothesis_topic_provenance.csv'}")


if __name__ == "__main__":
    main()
