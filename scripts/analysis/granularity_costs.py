"""What the granular fit (call 73) loses relative to the coarse fit (call 55).

Two costs: coarse topics whose documents the granular model pushes back into the
outlier pool, and coarse content that the granular model shatters into topics
below the 200-doc usability floor.
"""

from __future__ import annotations

import json
from collections import Counter
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


def main() -> None:
    a55 = np.asarray(json.loads((COMPARE / "call_55/model_compare_enriched/topics.json").read_text())["topics"])
    a73 = np.asarray(json.loads((COMPARE / "call_73/model_compare_enriched/topics.json").read_text())["topics"])
    labels = {int(k): v for k, v in json.loads(LABELS.read_text()).items()}

    q73 = pd.read_csv(QUALITY / "placeholder_v4_call73/topic_quality_placeholder_v4_call73.csv")
    q73["posthoc_reason"] = q73["posthoc_reason"].fillna("")
    unusable73 = set(
        q73.loc[
            q73["posthoc_reason"].str.contains("tiny_topic|name_contaminated|character_name|publisher"),
            "Topic",
        ]
    )
    q55 = pd.read_csv(QUALITY / "placeholder_v4_call55/topic_quality_placeholder_v4_call55.csv")
    name55 = dict(zip(q55["Topic"], q55["Name"]))

    rows = []
    for t in sorted(set(a55[a55 >= 0])):
        mask = a55 == t
        tot = int(mask.sum())
        kids = Counter(a73[mask].tolist())
        to_outlier = kids.get(-1, 0)
        to_unusable = sum(c for k, c in kids.items() if k in unusable73 and k >= 0)
        to_usable = tot - to_outlier - to_unusable
        rows.append(
            {
                "c55_topic": t,
                "c55_name": name55.get(t, ""),
                "c55_size": tot,
                "pct_to_c73_outlier": round(to_outlier / tot, 3),
                "pct_to_c73_tiny_or_flagged": round(to_unusable / tot, 3),
                "pct_still_usable_in_c73": round(to_usable / tot, 3),
                "n_c73_topics_touched": len([k for k in kids if k >= 0]),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "call55_retention_in_call73.csv", index=False)

    print("== coarse topics whose content the granular fit mostly stops modelling ==")
    lost = df[df["pct_still_usable_in_c73"] < 0.35].sort_values("c55_size", ascending=False)
    print(f"{len(lost)} of {len(df)} coarse topics keep <35% of their docs in a usable granular topic")
    print(lost.head(20).to_string(index=False, max_colwidth=40))
    print()

    print("== best-retained coarse topics ==")
    print(
        df.nlargest(10, "pct_still_usable_in_c73").to_string(index=False, max_colwidth=40)
    )
    print()
    print(f"mean retention into usable granular topics: {df['pct_still_usable_in_c73'].mean():.1%}")
    print(f"docs in usable c55 topics that land in a usable c73 topic: "
          f"{(df['pct_still_usable_in_c73'] * df['c55_size']).sum() / df['c55_size'].sum():.1%}")
    print()

    # Where does the granular model's tiny tail come from?
    tiny_sizes = q73[q73["posthoc_reason"].str.contains("tiny_topic")]["Count"]
    print(f"call73 tiny topics: n={len(tiny_sizes)} docs={int(tiny_sizes.sum()):,} "
          f"(median size {int(tiny_sizes.median())})")
    hyp_tiny = [
        (t, labels.get(t, {}).get("label", ""), labels.get(t, {}).get("sexual_explicitness", ""))
        for t in q73[q73["posthoc_reason"].str.contains("tiny_topic")]["Topic"]
        if labels.get(t, {}).get("sexual_explicitness") in {"explicit", "suggestive"}
    ]
    print(f"of which sexually explicit/suggestive (H1-relevant but below the floor): {len(hyp_tiny)}")
    for t, lab, ex in hyp_tiny[:15]:
        print(f"  T{t:<4d} {ex:<11s} {lab}")

    print(f"\nwrote: {OUT / 'call55_retention_in_call73.csv'}")


if __name__ == "__main__":
    main()
