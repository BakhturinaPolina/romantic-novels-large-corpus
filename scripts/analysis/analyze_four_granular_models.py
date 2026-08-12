"""Compare the four high-granularity shortlist models.

MPNet-38 (444), L12-11 (387), L12-49 (373), L12-73 (329).
Uses phase2 compare-fit artifacts (same 432,145-doc sample, same posthoc rules).
"""

from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/reports/stage04/granularity_four_models"

MODELS = {
    "MPNet-38": ROOT / "results/experiments/v4_mpnet_granular_phase2_pareto/final_compare/call_38",
    "L12-11": ROOT / "results/experiments/v4_l12_granular_phase2_pareto/final_compare/call_11",
    "L12-49": ROOT / "results/experiments/v4_l12_granular_phase2_pareto/final_compare/call_49",
    "L12-73": ROOT / "results/experiments/v4_l12_granular_phase2_pareto/final_compare/call_73",
}

STOP = set(
    "the to of she was and in her that had you i he it don do me my his we they "
    "what is are not for on with be this so at as but if or all just know like "
    "re ll ve can want say said get go got one two thing things right okay well "
    "now then there here who how why when yes no that s t m d didn couldn wouldn "
    "about from him them their our your been have has were being been would could "
    "should will ll ve re".split()
)

AXIS = {
    "H1_explicit_sex": r"cock|pussy|clit|orgasm|thrust|fucked|fucking|climax|nipple|penetration|erection|moaned|panting",
    "H1_kiss_attraction": r"kiss|kissed|kissing|lips|mouth|tongue|nibble|caress",
    "H1_H5_tenderness": r"cuddle|snuggled|tender|gentle|soothing|forehead|cradled|embrace|hugged|comforted",
    "H2_hea_commitment": r"married|marriage|wedding|vows|engaged|proposal|forever|husband|wife",
    "H3_luxury_status": r"mansion|limousine|champagne|diamond|penthouse|yacht|millionaire|billionaire|duke|duchess|silk|jewels|butler",
    "H4_protective_care": r"protect|protective|safety|shield|rescue|reassured|nursed|caretaking",
    "H4_possessive_jealous": r"possessive|jealous|jealousy|territorial|mine|belongs",
    "H5_dark_threat": r"gun|knife|blood|killed|kidnapped|attacked|hostage|weapon|scream|terror",
    "H6_conflict_repair": r"apologize|apology|forgive|forgiveness|argument|yelled|sorry|reconcile",
    "consent_negotiation": r"consent|permission|condom|stop if|say no|said no",
}
AXIS = {k: re.compile(rf"\b(?:{v})\b", re.I) for k, v in AXIS.items()}

GENERIC_NAME_RE = re.compile(
    r"^(michael|mike|sam|sarah|sara|samantha|kate|maggie|charlotte|lily|"
    r"adam|eve|jack|jake|logan|zach|james|john|mary|anna|emma|alex|"
    r"nick|david|mark|tom|ben|chris|ryan|luke|max|zoe|rachel)$",
    re.I,
)


def words_of(ti_row, k=10) -> list[str]:
    try:
        rep = ast.literal_eval(ti_row["Representation"])
        return [w for w in rep if isinstance(w, str) and w][:k]
    except Exception:
        return []


def load(name: str, path: Path) -> dict:
    m = json.loads((path / "metrics.json").read_text())
    st = json.loads((path / "stability.json").read_text())
    ph = json.loads((path / "posthoc_summary.json").read_text())
    ti = pd.read_csv(
        path / "topic_info.csv",
        usecols=["Topic", "Count", "Name", "Representation"],
    )
    flags = pd.read_csv(path / "posthoc_flags.csv")
    rd = pd.read_csv(path / "representative_docs.csv")
    ti = ti[ti["Topic"] >= 0].copy()
    flags = flags[flags["Topic"] >= 0].copy()
    flags["posthoc_reason"] = flags["posthoc_reason"].fillna("")
    flags["tiny"] = flags["posthoc_reason"].str.contains("tiny_topic")
    flags["boilerplate"] = flags["posthoc_reason"].str.contains("publisher_boilerplate")
    flags["multilingual"] = flags["posthoc_reason"].str.contains("multilingual")
    merged = ti.merge(flags[["Topic", "tiny", "boilerplate", "multilingual", "posthoc_reason"]], on="Topic", how="left")
    merged["tiny"] = merged["tiny"].fillna(False)
    merged["boilerplate"] = merged["boilerplate"].fillna(False)
    merged["multilingual"] = merged["multilingual"].fillna(False)
    docs = {int(t): " ".join(str(s) for s in g["sentence"]) for t, g in rd.groupby("topic")}
    return {
        "name": name,
        "metrics": m,
        "stability": st,
        "posthoc": ph,
        "ti": merged,
        "docs": docs,
        "hp": m.get("hyperparameters", {}),
    }


def classify_contamination(row) -> str:
    words = words_of(row, 10)
    if not words:
        return "empty"
    n_stop = sum(w.lower() in STOP for w in words)
    n_name = sum(bool(GENERIC_NAME_RE.match(w)) for w in words)
    if n_name >= 3:
        return "character_names"
    if n_stop >= 6:
        return "function_words"
    return "ok"


def axis_hits(row, docs: dict[int, str]) -> list[str]:
    words = " ".join(words_of(row, 15))
    text = words + " " + docs.get(int(row["Topic"]), "")
    return [a for a, pat in AXIS.items() if pat.search(text)]


def summarize(model: dict) -> dict:
    ti = model["ti"]
    n = len(ti)
    sizes = ti["Count"].astype(int)
    tiny = ti["tiny"].astype(bool)
    flagged = tiny | ti["boilerplate"].astype(bool) | ti["multilingual"].astype(bool)
    usable = ti[~flagged]
    contam = ti.apply(classify_contamination, axis=1)
    usable_ok = usable[usable.apply(classify_contamination, axis=1) == "ok"]

    axis_map = {int(r["Topic"]): axis_hits(r, model["docs"]) for _, r in ti.iterrows()}
    usable_axis = Counter()
    usable_ok_axis = Counter()
    tiny_axis = Counter()
    for _, r in ti.iterrows():
        hits = axis_map[int(r["Topic"])]
        t = int(r["Topic"])
        is_tiny = bool(r["tiny"])
        is_flagged = bool(r["tiny"] or r["boilerplate"] or r["multilingual"])
        for h in hits:
            if is_tiny:
                tiny_axis[h] += 1
            if not is_flagged:
                usable_axis[h] += 1
            if not is_flagged and classify_contamination(r) == "ok":
                usable_ok_axis[h] += 1

    hp = model["hp"]
    st = model["stability"]["stats"]
    m = model["metrics"]
    return {
        "model": model["name"],
        "embedding": m["embedding_model"].split("/")[-1],
        "n_topics": n,
        "c_v": round(m["coherence_c_v"], 3),
        "diversity": round(m["topic_diversity"], 3),
        "outlier": round(m["outlier_rate"], 3),
        "n_topics_std": round(st["std"], 2),
        "n_topics_range": int(st["range"]),
        "min_cluster_size": hp.get("hdbscan__min_cluster_size"),
        "min_samples": hp.get("hdbscan__min_samples"),
        "min_df": hp.get("vectorizer__min_df"),
        "n_neighbors": hp.get("umap__n_neighbors"),
        "min_dist": round(float(hp.get("umap__min_dist", 0)), 3),
        "n_components": hp.get("umap__n_components"),
        "assigned_docs": int(sizes.sum()),
        "tiny_n": int(tiny.sum()),
        "tiny_docs": int(sizes[tiny].sum()),
        "usable_n": int((~flagged).sum()),
        "usable_docs": int(sizes[~flagged].sum()),
        "usable_median": int(usable["Count"].median()) if len(usable) else 0,
        "usable_p10": int(usable["Count"].quantile(0.1)) if len(usable) else 0,
        "usable_p90": int(usable["Count"].quantile(0.9)) if len(usable) else 0,
        "largest": int(sizes.max()),
        "n_ge_800": int((sizes >= 800).sum()),
        "n_200_799": int(((sizes >= 200) & (sizes < 800)).sum()),
        "n_lt_200": int((sizes < 200).sum()),
        "funcword_n": int((contam == "function_words").sum()),
        "name_n": int((contam == "character_names").sum()),
        "usable_ok_n": len(usable_ok),
        "usable_ok_docs": int(usable_ok["Count"].sum()) if len(usable_ok) else 0,
        "axis_usable": dict(usable_axis),
        "axis_usable_ok": dict(usable_ok_axis),
        "axis_tiny": dict(tiny_axis),
        "top15": [
            {
                "t": int(r["Topic"]),
                "n": int(r["Count"]),
                "name": r["Name"],
                "words": ", ".join(words_of(r, 8)),
                "tiny": bool(r["tiny"]),
                "contam": classify_contamination(r),
                "axes": axis_map[int(r["Topic"])],
            }
            for _, r in ti.nlargest(15, "Count").iterrows()
        ],
        "axis_examples": {
            a: [
                f"T{int(r['Topic'])} n={int(r['Count'])} {r['Name']}"
                for _, r in ti.iterrows()
                if a in axis_map[int(r["Topic"])] and not (r["tiny"] or r["boilerplate"] or r["multilingual"])
            ][:6]
            for a in AXIS
        },
        "tiny_sex": [
            f"T{int(r['Topic'])} n={int(r['Count'])} {r['Name']}"
            for _, r in ti.iterrows()
            if r["tiny"] and "H1_explicit_sex" in axis_map[int(r["Topic"])]
        ],
    }


def print_block(s: dict) -> None:
    print(f"\n{'='*78}\n{s['model']}  {s['embedding']}  n={s['n_topics']}  c_v={s['c_v']}  div={s['diversity']}")
    print(
        f"outlier={s['outlier']}  std={s['n_topics_std']} (range {s['n_topics_range']})  "
        f"min_cluster={s['min_cluster_size']} min_samples={s['min_samples']} min_df={s['min_df']} "
        f"n_neighbors={s['n_neighbors']} min_dist={s['min_dist']} n_comp={s['n_components']}"
    )
    print(
        f"assigned={s['assigned_docs']:,}  usable={s['usable_n']} topics / {s['usable_docs']:,} docs  "
        f"tiny={s['tiny_n']} / {s['tiny_docs']:,} docs"
    )
    print(
        f"size: median usable {s['usable_median']}  p10–p90 {s['usable_p10']}–{s['usable_p90']}  "
        f"largest {s['largest']}  ≥800={s['n_ge_800']}  200–799={s['n_200_799']}  <200={s['n_lt_200']}"
    )
    print(
        f"contamination in all topics: function_words={s['funcword_n']} names={s['name_n']}  "
        f"usable-and-clean={s['usable_ok_n']} / {s['usable_ok_docs']:,} docs"
    )
    print("top 15:")
    for t in s["top15"]:
        flag = []
        if t["tiny"]:
            flag.append("TINY")
        if t["contam"] != "ok":
            flag.append(t["contam"])
        if t["axes"]:
            flag.append("+".join(t["axes"]))
        print(f"  T{t['t']:<4d} n={t['n']:<5d} {t['words']:<55s} {' '.join(flag)}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summaries = [summarize(load(n, p)) for n, p in MODELS.items()]

    for s in summaries:
        print_block(s)

    print("\n" + "=" * 78)
    print("USABLE YIELD")
    rows = []
    for s in summaries:
        rows.append(
            {k: s[k] for k in (
                "model", "n_topics", "c_v", "diversity", "outlier", "n_topics_std",
                "min_df", "min_cluster_size", "usable_n", "usable_docs", "tiny_n",
                "tiny_docs", "usable_ok_n", "usable_ok_docs", "n_ge_800", "n_200_799",
            )}
        )
    yld = pd.DataFrame(rows)
    print(yld.to_string(index=False))
    yld.to_csv(OUT / "yield_comparison.csv", index=False)

    print("\nAXIS COVERAGE (usable topics / tiny leftover)")
    axes = list(AXIS)
    ax_rows = []
    header = f"{'axis':28s}" + "".join(f"{s['model']:>14s}" for s in summaries)
    print(header)
    for a in axes:
        cells = []
        rec = {"axis": a}
        for s in summaries:
            u = s["axis_usable"].get(a, 0)
            t = s["axis_tiny"].get(a, 0)
            cells.append(f"{u:3d}+{t:<2d}tiny")
            rec[f"{s['model']}_usable"] = u
            rec[f"{s['model']}_tiny"] = t
        print(f"{a:28s}" + "".join(f"{c:>14s}" for c in cells))
        ax_rows.append(rec)
    pd.DataFrame(ax_rows).to_csv(OUT / "axis_coverage.csv", index=False)

    print("\nAXIS EXAMPLES (usable)")
    for s in summaries:
        print(f"\n-- {s['model']} --")
        for a, ex in s["axis_examples"].items():
            if ex:
                print(f"  {a}: {'; '.join(ex[:4])}")
        if s["tiny_sex"]:
            print(f"  TINY explicit: {'; '.join(s['tiny_sex'][:8])}")

    # Persist top-topic tables
    all_top = []
    for s in summaries:
        for t in s["top15"]:
            all_top.append({"model": s["model"], **t, "axes": "|".join(t["axes"])})
    pd.DataFrame(all_top).to_csv(OUT / "top15_topics.csv", index=False)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
