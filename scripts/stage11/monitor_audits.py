#!/usr/bin/env python3
"""Live Stage 11 audit progress + ETA (reads logs/artifacts; does not call the API)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

HTTP_RE = re.compile(r"HTTP/1\.1 200")
TOPIC_RE = re.compile(r"\[(\d+)/(\d+)\] (H\d) topic (\d+)")
SPILL_RE = re.compile(r"(H\d) spillover candidates: (\d+)")
SPILL_DONE_RE = re.compile(r"(H\d) spillover: promoted (\d+)/(\d+)")
AUDIT_START_RE = re.compile(
    r"(H\d) audit: (\d+) topics \((\d+) already adjudicated, (\d+) pending\)"
)


def _count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _process_start_epoch() -> float | None:
    """Earliest start time of run_audits / spillover / hypothesis audit processes."""
    try:
        out = subprocess.check_output(
            ["ps", "-eo", "pid,lstart,cmd"],
            text=True,
        )
    except Exception:
        return None
    starts = []
    for line in out.splitlines():
        if not any(
            s in line
            for s in (
                "run_audits.sh",
                "04_run_spillover",
                "05_run_hypothesis",
            )
        ):
            continue
        if "grep" in line or "monitor_audits" in line:
            continue
        # ps lstart: "Day Mon DD HH:MM:SS YYYY" after pid
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        rest = parts[1]
        # cmd starts at known script names; lstart is 5 tokens
        toks = rest.split(None, 5)
        if len(toks) < 6:
            continue
        stamp = " ".join(toks[:5])
        try:
            starts.append(datetime.strptime(stamp, "%a %b %d %H:%M:%S %Y").timestamp())
        except ValueError:
            continue
    return min(starts) if starts else None


def estimate_total_calls(base: Path, log_text: str) -> tuple[int, str, dict]:
    spill = {"H1": 28, "H3": 20}
    for m in SPILL_RE.finditer(log_text):
        spill[m.group(1)] = int(m.group(2))
    spill_calls = spill.get("H1", 28) + spill.get("H3", 20)

    audits = {"H1": 118, "H3": 90, "H4": 32, "H2": 10}
    for hyp in ("H1", "H3", "H4", "H2"):
        summary = _load_json(base / "audits" / hyp.lower() / "audit_summary.json")
        if summary and "n_topics" in summary:
            audits[hyp] = int(summary["n_topics"])
    for m in AUDIT_START_RE.finditer(log_text):
        audits[m.group(1)] = int(m.group(2))
    # After spillover files exist, refine H1/H3 before audit starts
    for hyp in ("H1", "H3"):
        sp = _load_json(base / "candidates" / f"{hyp.lower()}_spillover.json")
        man = _load_json(base / "candidates" / f"{hyp.lower()}_candidates.json")
        if sp and man and hyp not in {m.group(1) for m in AUDIT_START_RE.finditer(log_text)}:
            # mandatory (+ comparator for H3) approx: exclude spillover_discovery role from n
            roles = {}
            for e in man.get("entries", []):
                if e.get("topic_id") is None:
                    continue
                roles.setdefault(e.get("role"), set()).add(int(e["topic_id"]))
            core = set(roles.get("mandatory", set())) | set(roles.get("comparator", set()))
            promoted = set(int(t) for t in sp.get("promoted_topic_ids", []))
            audits[hyp] = len(core | promoted)

    audit_calls = 3 * sum(audits.values())
    total = spill_calls + audit_calls
    detail = (
        f"spill≈{spill_calls} + "
        f"H1={audits['H1']} H3={audits['H3']} H4={audits['H4']} H2={audits['H2']}×3 "
        f"= {audit_calls} → ≈{total} calls"
    )
    return total, detail, audits


def phase_from_log(log_text: str) -> str:
    if "H2 done:" in log_text:
        return "done"
    if "==== H2 Pass" in log_text:
        return "H2 audits"
    if "==== H4 Pass" in log_text:
        return "H4 audits"
    if "==== H3 Pass" in log_text:
        return "H3 audits"
    if "==== H1 Pass" in log_text:
        return "H1 audits"
    if "H3 spillover candidates" in log_text and "H3 spillover: promoted" not in log_text:
        return "H3 spillover"
    if "H1 spillover candidates" in log_text and "H1 spillover: promoted" not in log_text:
        return "H1 spillover"
    if "Spillover triage" in log_text:
        return "spillover"
    return "starting"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default="results/stage11_refined_construct_analysis/v4_l12_granular_final_call49",
    )
    parser.add_argument("--interval", type=float, default=20.0)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    base = Path(args.base)
    log_path = base / "logs" / "audits_live.log"
    start_ts = _process_start_epoch()
    if start_ts is None and log_path.exists():
        # Birth time if available, else mtime of first write approximation
        st = log_path.stat()
        start_ts = getattr(st, "st_birthtime", None) or st.st_mtime
    if start_ts is None:
        start_ts = time.time()

    prev_http = None
    prev_t = None

    while True:
        log_text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
        http_ok = len(HTTP_RE.findall(log_text))
        warns = log_text.count("WARNING OpenRouter")
        phase = phase_from_log(log_text)
        total, detail, _audits = estimate_total_calls(base, log_text)

        arts = {}
        for hyp in ("h1", "h2", "h3", "h4"):
            arts[hyp] = {
                "A": _count_lines(base / "audits" / hyp / "lexical.jsonl"),
                "B": _count_lines(base / "audits" / hyp / "contextual.jsonl"),
                "C": _count_lines(base / "audits" / hyp / "adjudication.jsonl"),
            }
        spill_h1 = _load_json(base / "candidates" / "h1_spillover.json")
        spill_h3 = _load_json(base / "candidates" / "h3_spillover.json")

        now_t = time.time()
        elapsed = max(1.0, now_t - start_ts)
        # Prefer instantaneous rate from last poll; fall back to cumulative
        if prev_http is not None and prev_t is not None and now_t > prev_t:
            d_http = max(0, http_ok - prev_http)
            d_t = now_t - prev_t
            inst_rate = d_http / d_t if d_t > 0 else 0.0
        else:
            inst_rate = 0.0
        cum_rate = http_ok / elapsed
        rate = inst_rate if inst_rate > 0 else cum_rate
        remaining = max(0, total - http_ok)
        eta_s = remaining / rate if rate > 0 else float("inf")
        eta = str(timedelta(seconds=int(eta_s))) if eta_s != float("inf") else "unknown"
        finish = (
            (datetime.now() + timedelta(seconds=int(eta_s))).strftime("%H:%M")
            if eta_s != float("inf")
            else "?"
        )
        pct = min(100.0, 100.0 * http_ok / total) if total else 0.0
        now = datetime.now().strftime("%H:%M:%S")
        topics = list(TOPIC_RE.finditer(log_text))
        latest = topics[-1].group(0) if topics else "(spillover / no Pass A/B/C lines yet)"

        print(
            f"\n[{now}] {phase}  {http_ok}/{total} calls ({pct:.1f}%)  "
            f"elapsed {timedelta(seconds=int(elapsed))}  "
            f"{rate * 60:.1f}/min  ETA {eta} (~{finish})  warns={warns}",
            flush=True,
        )
        print(f"  budget: {detail}", flush=True)
        print(f"  latest: {latest}", flush=True)
        if spill_h1:
            print(
                f"  spillover H1: {spill_h1.get('n_promoted')}/{spill_h1.get('n_candidates')} promoted",
                flush=True,
            )
        if spill_h3:
            print(
                f"  spillover H3: {spill_h3.get('n_promoted')}/{spill_h3.get('n_candidates')} promoted",
                flush=True,
            )
        for hyp, counts in arts.items():
            if any(counts.values()):
                print(
                    f"  {hyp.upper()} A/B/C rows: {counts['A']}/{counts['B']}/{counts['C']}",
                    flush=True,
                )
        print(f"  log: {log_path}", flush=True)

        prev_http, prev_t = http_ok, now_t

        if phase == "done" or (http_ok >= total and arts["h2"]["C"] >= 10):
            print("\nDONE.", flush=True)
            return 0
        if args.once:
            return 0
        time.sleep(float(args.interval))


if __name__ == "__main__":
    raise SystemExit(main())
