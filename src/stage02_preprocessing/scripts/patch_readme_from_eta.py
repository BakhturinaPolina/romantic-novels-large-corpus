#!/usr/bin/env python3
"""Replace README ETA-RUNTIME section from eta_estimate.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ETA = ROOT / "data/interim/booknlp_character_runs/train_stage02_eta50/eta_estimate.json"
README = ROOT / "src/stage02_preprocessing/README.md"


def main() -> None:
    if not ETA.is_file():
        raise SystemExit(f"Missing {ETA}")
    r = json.loads(ETA.read_text(encoding="utf-8"))
    mean_s = r.get("runtime_mean_s")
    med_s = r.get("runtime_median_s")
    p90_s = r.get("runtime_p90_s")
    full_h = r.get("projected_full_corpus_hours")
    lo = r.get("projected_full_corpus_ci95_low_hours")
    hi = r.get("projected_full_corpus_ci95_high_hours")
    n = r.get("sample_size")
    corpus = r.get("books_total_corpus")

    if med_s and med_s <= 60:
        decision = "Median ≤60 s/book → full corpus may be feasible in roughly 4–8 days on one GPU; still prefer checkpointed shards."
    elif mean_s and mean_s >= 180:
        decision = "Mean ≥180 s/book → use `--stoplist-sample-books` (e.g. 1500) or external/multi-GPU; avoid full 11k-book run on one GPU."
    else:
        decision = "Mixed distribution → use stratified `--stoplist-sample-books` for stoplist; re-evaluate if topic metrics require full corpus."

    block = f"""<!-- ETA-RUNTIME-START -->

Measured on **RTX 2070 Max-Q**, `entity` + `small`, `sentences_train.csv` (~{corpus:,} `work_id`s; `train_stage02_eta50`).

**Source:** `{ETA.relative_to(ROOT)}` (n={n} timed books).

| Metric | Value | Notes |
|--------|-------|-------|
| Mean | {mean_s} s/book | Pulled up by very long books |
| Median | {med_s} s/book | Better typical-book estimate |
| P90 | {p90_s} s/book | Heavy tail |
| Full corpus (point) | {full_h} h | 11,429 books × mean |
| Full corpus (95% CI) | {lo}–{hi} h | Normal approx. on sample mean |

**Decision:** {decision}

<!-- ETA-RUNTIME-END -->
"""
    text = README.read_text(encoding="utf-8")
    new_text, nsub = re.subn(
        r"<!-- ETA-RUNTIME-START -->.*?<!-- ETA-RUNTIME-END -->",
        block.strip(),
        text,
        count=1,
        flags=re.DOTALL,
    )
    if nsub != 1:
        raise SystemExit("ETA-RUNTIME markers not found in README")
    README.write_text(new_text, encoding="utf-8")
    print(f"Updated {README}")


if __name__ == "__main__":
    main()
