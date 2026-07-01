#!/usr/bin/env python3
"""Score Stage08 prompt sweep JSONs against call73 gold panel."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD = ROOT / "data/stage08_benchmark/call73_panel_v1.json"
DEFAULT_GOLD_CHARACTER_NAME = ROOT / "data/stage08_benchmark/call73_panel_character_name_v1.json"

_NAME_LABEL_BAD = re.compile(
    r"\b("
    r"Scattered|Name Cluster|Name References|Name-Clustered|Character References"
    r"|Cole|Ryan|Jared|Shane|Aiden|Caleb|Noah|Rose|Josh|Travis|Callie|Miles|Dylan|Marcus"
    r")\b",
    re.IGNORECASE,
)


def _label_quality_ok(label: str) -> bool:
    if not label or not label.strip():
        return False
    words = label.split()
    if len(words) < 2 or len(words) > 6:
        return False
    if re.search(r"\b(and|with)\b", label.lower()) and len(words) >= 4:
        parts = re.split(r"\s+and\s+|\s+with\s+", label.lower())
        if len(parts) >= 3:
            return False
    return True


def _name_label_ok(label: str) -> bool:
    return not _NAME_LABEL_BAD.search(str(label or ""))


def score_labels(labels_path: Path, gold: dict, panel_ids: list[int]) -> dict:
    with labels_path.open(encoding="utf-8") as f:
        labels = json.load(f)

    routing_w = 0.30
    ground_w = 0.40
    label_w = 0.20
    schema_w = 0.10

    n = 0
    routing_pts = 0.0
    ground_pts = 0.0
    label_pts = 0.0
    schema_pts = 0.0
    name_label_pts = 0.0
    per_topic: dict[str, dict] = {}

    for tid in panel_ids:
        key = str(tid)
        if key not in gold["topics"]:
            continue
        g = gold["topics"][key]
        if key not in labels:
            per_topic[key] = {"missing": True}
            continue
        n += 1
        pred = labels[key]
        pred_label = str(pred.get("label", ""))
        ct_ok = pred.get("content_type") == g["expected_content_type"]
        ex_ok = bool(pred.get("exclude_from_axes")) == bool(g["expected_exclude_from_axes"])
        routing_ok = ct_ok and ex_ok
        if routing_ok:
            routing_pts += 1.0

        ground_ok = g.get("snippet_grounding_pass", True)
        label_low = pred_label.lower()
        bad_ground = ("bedroom", "incoherent keyword", "keyword cluster")
        if ground_ok:
            if not any(b in label_low for b in bad_ground):
                ground_pts += 1.0
        else:
            ground_pts += 1.0

        lq_ok = _label_quality_ok(pred_label)
        if lq_ok:
            label_pts += 1.0

        schema_ok = bool(pred.get("label")) and "content_type" in pred
        if schema_ok:
            schema_pts += 1.0

        nl_ok = _name_label_ok(pred_label)
        if nl_ok:
            name_label_pts += 1.0

        per_topic[key] = {
            "routing_ok": routing_ok,
            "content_type": pred.get("content_type"),
            "expected_content_type": g["expected_content_type"],
            "exclude_from_axes": pred.get("exclude_from_axes"),
            "expected_exclude_from_axes": g["expected_exclude_from_axes"],
            "label": pred.get("label"),
            "name_label_ok": nl_ok,
        }

    if n == 0:
        return {"score": 0.0, "n": 0, "per_topic": per_topic}

    total = (
        routing_w * (routing_pts / n)
        + ground_w * (ground_pts / n)
        + label_w * (label_pts / n)
        + schema_w * (schema_pts / n)
    )
    discourse_ids = [
        int(k)
        for k, g in gold["topics"].items()
        if g.get("expected_content_type") == "discourse" and int(k) in panel_ids
    ]
    discourse_hits = sum(
        1
        for tid in discourse_ids
        if per_topic.get(str(tid), {}).get("routing_ok")
    )
    name_artifact_ids = [
        tid
        for tid in panel_ids
        if gold["topics"].get(str(tid), {}).get("stratum") == "name_artifact"
    ]
    name_artifact_routing_hits = sum(
        1
        for tid in name_artifact_ids
        if per_topic.get(str(tid), {}).get("routing_ok")
    )
    return {
        "score": round(total, 4),
        "n": n,
        "routing_accuracy": round(routing_pts / n, 4),
        "discourse_stratum": f"{discourse_hits}/{len(discourse_ids)}",
        "name_label_ok": f"{int(name_label_pts)}/{n}",
        "name_artifact_routing": f"{name_artifact_routing_hits}/{len(name_artifact_ids)}",
        "per_topic": per_topic,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score Stage08 sweep labels vs gold panel")
    parser.add_argument("--gold", type=Path, default=None)
    parser.add_argument("--sweep-dir", type=Path, required=True)
    parser.add_argument(
        "--panel",
        choices=["pilot20", "full30", "character_name"],
        default="pilot20",
    )
    parser.add_argument("--labels", type=Path, default=None, help="Single JSON to score")
    args = parser.parse_args()

    if args.gold is not None:
        gold_path = args.gold
    elif args.panel == "character_name":
        gold_path = DEFAULT_GOLD_CHARACTER_NAME
    else:
        gold_path = DEFAULT_GOLD

    with gold_path.open(encoding="utf-8") as f:
        gold = json.load(f)

    if args.panel == "pilot20":
        panel_ids = list(range(20))
    else:
        panel_ids = [int(k) for k in gold["topics"]]

    if args.labels:
        paths = [args.labels]
    else:
        paths = sorted(
            p
            for p in args.sweep_dir.rglob("*.json")
            if p.name != "sweep_scores_summary.json"
            and "v3_rep_first" not in p.parts
            and p.parent.name != "scores"
        )

    rows = []
    for path in paths:
        if path.name.endswith(".partial.json"):
            continue
        result = score_labels(path, gold, panel_ids)
        rel = path.relative_to(args.sweep_dir)
        rows.append((result["score"], str(rel), result))

    rows.sort(key=lambda x: x[0], reverse=True)
    print(f"Panel: {args.panel} ({len(panel_ids)} topics)\n")
    header = f"{'Score':>8}  {'Routing':>8}  {'Discourse':>10}  {'Names':>8}  File"
    if args.panel == "character_name":
        header = f"{'Score':>8}  {'Routing':>8}  {'NameArt':>8}  {'Names':>8}  File"
    print(header)
    print("-" * 80)
    for score, name, result in rows:
        if args.panel == "character_name":
            print(
                f"{score:8.4f}  {result.get('routing_accuracy', 0):8.4f}  "
                f"{result.get('name_artifact_routing', '?'):>8}  "
                f"{result.get('name_label_ok', '?'):>8}  {name}"
            )
        else:
            print(
                f"{score:8.4f}  {result.get('routing_accuracy', 0):8.4f}  "
                f"{result.get('discourse_stratum', '?'):>10}  "
                f"{result.get('name_label_ok', '?'):>8}  {name}"
            )

    summary_dir = args.sweep_dir / "scores"
    summary_dir.mkdir(parents=True, exist_ok=True)
    summary_path = summary_dir / "sweep_scores_summary.json"
    summary_path.write_text(
        json.dumps(
            [
                {"file": name, "score": score, **{k: v for k, v in res.items() if k != "per_topic"}}
                for score, name, res in rows
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {summary_path}")


if __name__ == "__main__":
    main()
