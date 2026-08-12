"""Compare coarse (call 55, 117 topics) vs granular (call 73, 329 topics) fits.

Both fits cover the same 432,145-sentence fit sample in the same order, so the
comparison is done on document-level assignments rather than keyword overlap.
Reports what the extra resolution buys for the Stage10 hypothesis axes.
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

# Lexicons for the Stage10 hypothesis axes (SCIENTIFIC_README H1-H6).
AXIS_LEXICON = {
    "H1 explicit sex (2.3/2.4/2.5)": (
        "cock thrust nipple orgasm clit pussy moan fucked fucking naked thrusting "
        "climax panting arousal erection stroked grinding writhing"
    ),
    "H1 kiss / attraction (2.1)": (
        "kiss kissed kissing lips mouth tongue nibbled brushed pressed caress"
    ),
    "H1/H5 tenderness, affection (4.2)": (
        "cuddle snuggled tender gentle soothing stroked hair forehead murmured cradled "
        "affection warmth comfort holding embrace hugged"
    ),
    "H2 HEA / commitment (4.5)": (
        "married marriage wedding vows engaged proposal forever promise commitment "
        "love husband wife future together always"
    ),
    "H3 luxury / status (6.1a/6.6/6.7)": (
        "mansion limousine champagne diamond designer gown estate penthouse butler "
        "yacht fortune wealthy millionaire duke duchess lord estate silk jewels"
    ),
    "H4 protective care (4.6)": (
        "protect protective safe safety shield guard defend rescue worried care "
        "looking after healed nursed comfort reassured"
    ),
    "H4 possessiveness / jealousy (4.7)": (
        "mine possessive jealous jealousy claim territorial growled snarled belongs "
        "envy rival glare"
    ),
    "H5 darkness / threat (7.x)": (
        "gun knife blood killed threat kidnapped attacked scream terror danger "
        "shot wound violence hostage weapon"
    ),
    "H6 conflict / repair (3.x/4.4)": (
        "apologize sorry forgive apology argument fight yelled misunderstood "
        "explain shouted tears cried regret reconcile"
    ),
}
AXIS_LEXICON = {k: set(v.split()) for k, v in AXIS_LEXICON.items()}


def load_assignments(call: str) -> np.ndarray:
    p = COMPARE / f"call_{call}/model_compare_enriched/topics.json"
    return np.asarray(json.loads(p.read_text())["topics"], dtype=np.int32)


def load_reprs(call: str) -> dict[int, list[str]]:
    """Union of the three representation aspects, for lexicon matching."""
    d = json.loads((COMPARE / f"call_{call}/model_compare_enriched/topics.json").read_text())
    out: dict[int, list[str]] = {}
    for tid, words in d["topic_representations"].items():
        bag = [w for w, _ in words]
        for aspect in ("KeyBERT", "MMR", "POS"):
            bag += [w for w, _ in d["topic_aspects"][aspect].get(tid, [])]
        out[int(tid)] = [w for w in bag if isinstance(w, str) and w]
    return out


def load_quality(call: str) -> pd.DataFrame:
    q = pd.read_csv(QUALITY / f"placeholder_v4_call{call}/topic_quality_placeholder_v4_call{call}.csv")
    q["posthoc_reason"] = q["posthoc_reason"].fillna("")
    q["tiny"] = q["posthoc_reason"].str.contains("tiny_topic")
    q["name_contaminated"] = q["posthoc_reason"].str.contains("name_contaminated|character_name")
    q["boilerplate"] = q["posthoc_reason"].str.contains("publisher_boilerplate")
    q["usable"] = ~(q["tiny"] | q["name_contaminated"] | q["boilerplate"])
    return q


def repr_docs(call: str) -> dict[int, str]:
    rd = pd.read_csv(COMPARE / f"call_{call}/representative_docs.csv")
    return {int(t): " ".join(str(s) for s in g["sentence"]) for t, g in rd.groupby("topic")}


def axis_hits(reprs: dict[int, list[str]], docs: dict[int, str], usable_ids: set[int]):
    """Topics per hypothesis axis, keyword-matched on representation + repr docs."""
    res: dict[str, list[int]] = defaultdict(list)
    for tid in sorted(usable_ids):
        bag = set(w.lower() for w in reprs.get(tid, []))
        bag |= set(re.findall(r"[a-z]+", docs.get(tid, "").lower()))
        for axis, lex in AXIS_LEXICON.items():
            if len(bag & lex) >= 2:
                res[axis].append(tid)
    return res


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    a55, a73 = load_assignments("55"), load_assignments("73")
    assert a55.shape == a73.shape
    q55, q73 = load_quality("55"), load_quality("73")
    r55, r73 = load_reprs("55"), load_reprs("73")
    d55, d73 = repr_docs("55"), repr_docs("73")
    labels = {int(k): v for k, v in json.loads(LABELS.read_text()).items()}

    n = len(a55)
    print(f"fit docs: {n:,}")
    for name, a, q in (("call55 (117)", a55, q55), ("call73 (329)", a73, q73)):
        assigned = int((a >= 0).sum())
        usable_ids = set(q.loc[q["usable"], "Topic"])
        in_usable = int(np.isin(a, list(usable_ids)).sum())
        print(
            f"{name}: topics={q.shape[0]:3d} usable={len(usable_ids):3d} "
            f"assigned={assigned:,} ({assigned/n:.1%}) "
            f"in-usable-topics={in_usable:,} ({in_usable/n:.1%}) "
            f"tiny={int(q['tiny'].sum())} name_contam={int(q['name_contaminated'].sum())}"
        )
    print()

    # Outlier cross-tab: who recovers what.
    both_out = int(((a55 < 0) & (a73 < 0)).sum())
    only55_out = int(((a55 < 0) & (a73 >= 0)).sum())
    only73_out = int(((a55 >= 0) & (a73 < 0)).sum())
    both_in = int(((a55 >= 0) & (a73 >= 0)).sum())
    print("== outlier cross-tab (docs) ==")
    print(f"outlier in both:                {both_out:>8,} ({both_out/n:.1%})")
    print(f"outlier in c55 only (c73 recovers): {only55_out:>8,} ({only55_out/n:.1%})")
    print(f"outlier in c73 only (c55 recovers): {only73_out:>8,} ({only73_out/n:.1%})")
    print(f"assigned in both:               {both_in:>8,} ({both_in/n:.1%})")
    print()

    # Document-level split structure.
    usable73 = set(q73.loc[q73["usable"], "Topic"])
    size73 = dict(zip(q73["Topic"], q73["Count"]))
    size55 = dict(zip(q55["Topic"], q55["Count"]))

    rows = []
    for t in sorted(set(a73[a73 >= 0])):
        mask = a73 == t
        parents = Counter(a55[mask].tolist())
        tot = int(mask.sum())
        top_p, top_c = parents.most_common(1)[0]
        from_out = parents.get(-1, 0)
        lab = labels.get(t, {})
        rows.append(
            {
                "c73_topic": t,
                "c73_size": tot,
                "c73_label": lab.get("label", ""),
                "usable": t in usable73,
                "explicitness": lab.get("sexual_explicitness", ""),
                "top_parent_c55": top_p,
                "top_parent_share": round(top_c / tot, 3),
                "share_from_c55_outlier": round(from_out / tot, 3),
                "n_parents": len(parents),
                "c73_words": ", ".join(r73.get(t, [])[:8]),
            }
        )
    align = pd.DataFrame(rows)
    align.to_csv(OUT / "call73_to_call55_doc_alignment.csv", index=False)

    novel = align[(align["share_from_c55_outlier"] >= 0.5) & align["usable"]]
    print("== granular topics carved mainly out of the coarse model's outlier pool ==")
    print(f"{len(novel)} of {int(align['usable'].sum())} usable call73 topics (>=50% of docs were c55 outliers)")
    print(novel.nlargest(20, "c73_size")[
        ["c73_topic", "c73_size", "c73_label", "share_from_c55_outlier", "explicitness"]
    ].to_string(index=False, max_colwidth=45))
    print()

    # How coarse topics fan out.
    frows = []
    for t in sorted(set(a55[a55 >= 0])):
        mask = a55 == t
        kids = Counter(a73[mask].tolist())
        tot = int(mask.sum())
        kids_named = [(k, c) for k, c in kids.most_common() if k >= 0 and c / tot >= 0.05]
        frows.append(
            {
                "c55_topic": t,
                "c55_size": tot,
                "c55_words": ", ".join(r55.get(t, [])[:8]),
                "n_c73_children_5pct": len(kids_named),
                "kept_as_outlier_by_c73": round(kids.get(-1, 0) / tot, 3),
                "children": "; ".join(
                    f"{k}:{labels.get(k, {}).get('label', '?')}({c/tot:.0%})" for k, c in kids_named[:6]
                ),
            }
        )
    fan = pd.DataFrame(frows).sort_values("n_c73_children_5pct", ascending=False)
    fan.to_csv(OUT / "call55_fanout.csv", index=False)
    print("== coarse topics that split into the most granular topics (>=5% of docs each) ==")
    print(fan.head(12).to_string(index=False, max_colwidth=70))
    print()

    # Hypothesis-axis coverage.
    u55 = set(q55.loc[q55["usable"], "Topic"])
    h55 = axis_hits(r55, d55, u55)
    h73 = axis_hits(r73, d73, usable73)
    print("== usable topics matching each hypothesis-axis lexicon ==")
    print(f"{'axis':38s} {'call55':>7s} {'call73':>7s}")
    arows = []
    for axis in AXIS_LEXICON:
        a, b = len(h55.get(axis, [])), len(h73.get(axis, []))
        print(f"{axis:38s} {a:7d} {b:7d}")
        arows.append({"axis": axis, "call55_topics": a, "call73_topics": b,
                      "call55_ids": h55.get(axis, []), "call73_ids": h73.get(axis, [])})
    pd.DataFrame(arows).to_csv(OUT / "axis_coverage.csv", index=False)
    print(f"\nwrote: {OUT}")


if __name__ == "__main__":
    main()
