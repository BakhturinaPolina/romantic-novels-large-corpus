#!/usr/bin/env python3
"""On-the-fly QA for live Stage 11 Nemo audits.

Runs against partial jsonl/log artifacts so model failures surface early
(before the full ~2h batch finishes).

Exit codes:
  0 = OK / only info
  1 = warnings (continue, but inspect)
  2 = critical failures (consider pausing / fixing)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.stage11_refined_construct_analysis.audits.prompts import (  # noqa: E402
    list_code_ids,
    load_hypothesis_prompt,
)
from src.stage11_refined_construct_analysis.config import load_stage11_config  # noqa: E402

HTTP_RE = re.compile(r"HTTP/1\.1 200")
WARN_RE = re.compile(r"WARNING OpenRouter")

# Measurement traps from the Stage 11 plan / stability pilot
TRAP_EXPECTATIONS = {
    # topic_id -> (hypothesis, preferred codes, note)
    1: ("H1", {"I3", "I5", "MIXED"}, "2.3 kissing/undressing must NOT be I6-only"),
    7: ("H1", {"I3", "I5", "MIXED"}, "2.3 kissing contamination"),
    18: ("H3", {"S12", "S13", "S14", "S8", "S16", "MIXED"}, "1.6 appearance vs provision"),
    29: ("H2", {"H2_1", "H2_2", "H2_7", "MIXED"}, "4.5 confession ≠ HEA"),
    62: ("H2", {"H2_1", "H2_2", "H2_7", "MIXED"}, "4.5 confession/repair"),
    167: ("H2", {"H2_4", "H2_5", "H2_3", "MIXED"}, "5.3a thin HEA leaf"),
    293: ("H4", {"H4_7", "H4_8", "H4_9", "H4_13", "MIXED"}, "4.7 possessiveness"),
    315: ("H4", {"H4_7", "H4_8", "H4_9", "H4_13", "MIXED"}, "4.7 possessiveness"),
}

CODE_FIELD = {
    "H1": "intimacy_code",
    "H2": "hea_code",
    "H3": "security_code",
    "H4": "care_protection_code",
}


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"_raw_parse_error": True, "raw": line[:200]})
    return rows


def _code_of(row: Mapping[str, Any], hyp: str) -> str:
    if row.get("code"):
        return str(row["code"])
    resp = row.get("response") or {}
    for key in (
        "consensus_code",
        "dominant_code",
        CODE_FIELD.get(hyp, ""),
        "intimacy_code",
        "hea_code",
        "security_code",
        "care_protection_code",
    ):
        if key and resp.get(key):
            return str(resp[key])
    return "UNKNOWN"


def check_hypothesis(
    base: Path,
    hyp: str,
    valid_codes: Sequence[str],
    *,
    min_rows_for_rates: int = 8,
) -> Tuple[List[str], List[str], List[str], Dict[str, Any]]:
    """Return (critical, warnings, info, stats)."""
    crit: List[str] = []
    warn: List[str] = []
    info: List[str] = []
    hdir = base / "audits" / hyp.lower()
    lexical = _load_jsonl(hdir / "lexical.jsonl")
    contextual = _load_jsonl(hdir / "contextual.jsonl")
    adjud = _load_jsonl(hdir / "adjudication.jsonl")
    spill = _load_jsonl(hdir / "spillover_triage.jsonl")

    valid = set(valid_codes) | {"MIXED", "UNKNOWN"}
    stats: Dict[str, Any] = {
        "n_A": len(lexical),
        "n_B": len(contextual),
        "n_C": len(adjud),
        "n_spillover": len(spill),
    }

    # --- structural ---
    for label, rows in (("A", lexical), ("B", contextual), ("C", adjud)):
        dry = sum(1 for r in rows if r.get("dry_run"))
        if dry:
            crit.append(f"{hyp} Pass {label}: {dry} dry_run rows in LIVE artifacts")
        bad_json = sum(
            1
            for r in rows
            if r.get("_raw_parse_error")
            or (r.get("response") or {}).get("parse_error")
        )
        if bad_json:
            crit.append(f"{hyp} Pass {label}: {bad_json} JSON parse errors")
        unknown = sum(1 for r in rows if _code_of(r, hyp) == "UNKNOWN")
        if unknown:
            crit.append(f"{hyp} Pass {label}: {unknown} UNKNOWN codes")
        invalid = [
            (r.get("topic_id"), _code_of(r, hyp))
            for r in rows
            if _code_of(r, hyp) not in valid
        ]
        if invalid:
            crit.append(
                f"{hyp} Pass {label}: invalid codes {invalid[:5]}"
                + ("…" if len(invalid) > 5 else "")
            )

    # duplicates
    for label, rows in (("A", lexical), ("B", contextual), ("C", adjud)):
        ids = [int(r["topic_id"]) for r in rows if "topic_id" in r]
        dup = [tid for tid, c in Counter(ids).items() if c > 1]
        if dup:
            warn.append(f"{hyp} Pass {label}: duplicate topic_ids {dup[:8]}")

    # Pass B empty-sentence / vacuous MIXED
    empty_b = 0
    mixed_b = 0
    for r in contextual:
        resp = r.get("response") or {}
        rationale = str(resp.get("rationale") or "").lower()
        n_sent = int(r.get("n_sentences") or 0)
        scodes = resp.get("sentence_codes") or []
        if _code_of(r, hyp) == "MIXED":
            mixed_b += 1
        # Vacuous only when the packet truly had no sentences to code.
        if n_sent == 0 or "no contextual sentence" in rationale or "no sentences" in rationale:
            empty_b += 1
        elif n_sent > 0 and not scodes and _code_of(r, hyp) == "MIXED":
            # Soft signal: MIXED without per-sentence codes despite evidence present
            pass
    stats["pass_b_empty"] = empty_b
    stats["pass_b_mixed"] = mixed_b
    if contextual and empty_b == len(contextual) and empty_b > 0:
        crit.append(
            f"{hyp} Pass B: ALL {empty_b} rows lack contextual sentences "
            "(vacuous MIXED) — evidence packets need sentences or Pass B is non-informative"
        )
    elif contextual and len(contextual) >= 3 and empty_b / len(contextual) >= 0.5:
        warn.append(
            f"{hyp} Pass B: {empty_b}/{len(contextual)} empty-sentence / vacuous MIXED"
        )

    # A vs B / A vs C agreement (when B not vacuous)
    by_a = {int(r["topic_id"]): _code_of(r, hyp) for r in lexical if "topic_id" in r}
    by_b = {int(r["topic_id"]): _code_of(r, hyp) for r in contextual if "topic_id" in r}
    by_c = {int(r["topic_id"]): _code_of(r, hyp) for r in adjud if "topic_id" in r}
    ab_pairs = [
        (tid, by_a[tid], by_b[tid])
        for tid in by_a
        if tid in by_b and by_b[tid] != "MIXED"
    ]
    ac_pairs = [(tid, by_a[tid], by_c[tid]) for tid in by_a if tid in by_c]
    if len(ab_pairs) >= min_rows_for_rates:
        agree = sum(1 for _, a, b in ab_pairs if a == b) / len(ab_pairs)
        stats["a_b_agree"] = agree
        if agree < 0.40:
            warn.append(f"{hyp} Pass A↔B agreement {agree:.0%} on {len(ab_pairs)} topics")
        else:
            info.append(f"{hyp} Pass A↔B agreement {agree:.0%} (n={len(ab_pairs)})")
    if len(ac_pairs) >= min_rows_for_rates:
        agree = sum(1 for _, a, c in ac_pairs if a == c) / len(ac_pairs)
        stats["a_c_agree"] = agree
        if agree < 0.50:
            warn.append(f"{hyp} Pass A↔C agreement {agree:.0%} on {len(ac_pairs)} topics")
        else:
            info.append(f"{hyp} Pass A↔C agreement {agree:.0%} (n={len(ac_pairs)})")

    # Code distribution collapse (all same code)
    if len(lexical) >= min_rows_for_rates:
        dist = Counter(_code_of(r, hyp) for r in lexical)
        top, n = dist.most_common(1)[0]
        frac = n / len(lexical)
        stats["pass_a_top"] = (top, frac)
        if frac >= 0.90:
            warn.append(
                f"{hyp} Pass A: {frac:.0%} of codes are {top} — possible mode collapse"
            )
        else:
            info.append(f"{hyp} Pass A top code {top} ({frac:.0%}); n={len(lexical)}")

    # Trap topics
    for tid, (thyp, allowed, note) in TRAP_EXPECTATIONS.items():
        if thyp != hyp:
            continue
        # Prefer Pass C, else A
        code = by_c.get(tid) or by_a.get(tid)
        if code is None:
            continue
        if code == "I6" and tid in (1, 7):
            crit.append(
                f"{hyp} TRAP topic {tid}: coded {code} but expected non-I6 ({note})"
            )
        elif code not in allowed and code != "UNKNOWN":
            warn.append(
                f"{hyp} TRAP topic {tid}: got {code}; preferred {sorted(allowed)} ({note})"
            )
        else:
            info.append(f"{hyp} TRAP topic {tid}: {code} OK ({note})")

    # Spillover sanity
    if spill:
        includes = [bool(r.get("include")) for r in spill]
        rate = sum(includes) / len(includes)
        stats["spillover_include_rate"] = rate
        if rate >= 0.95:
            warn.append(
                f"{hyp} spillover include rate {rate:.0%} ({sum(includes)}/{len(includes)}) — too permissive?"
            )
        elif rate <= 0.05 and len(spill) >= 10:
            warn.append(
                f"{hyp} spillover include rate {rate:.0%} — almost nothing promoted"
            )
        else:
            info.append(
                f"{hyp} spillover include {sum(includes)}/{len(includes)} ({rate:.0%})"
            )
        # parse / dry_run on spillover
        if any(r.get("dry_run") for r in spill):
            crit.append(f"{hyp} spillover contains dry_run=True rows")

    # H2 position awareness: Pass B should mention tertile patterns when sentences exist
    if hyp == "H2" and contextual:
        missing_fields = 0
        for r in contextual:
            resp = r.get("response") or {}
            if r.get("n_sentences", 0) > 0 and resp.get("finality") is None and resp.get("main_couple") is None:
                missing_fields += 1
        if missing_fields and missing_fields == len(contextual):
            warn.append("H2 Pass B: missing finality/main_couple fields on all rows")

    # H4 prior reuse when C exists for 4.6
    if hyp == "H4" and adjud:
        with_prior = sum(1 for r in adjud if r.get("prior_h3"))
        stats["h4_with_prior"] = with_prior
        if len(adjud) >= 5 and with_prior == 0:
            warn.append("H4: no prior_h3 attached yet (expected for 4.6 topics)")

    return crit, warn, info, stats


def check_log(log_path: Path) -> Tuple[List[str], List[str], Dict[str, Any]]:
    crit: List[str] = []
    warn: List[str] = []
    stats: Dict[str, Any] = {}
    if not log_path.exists():
        warn.append(f"missing live log: {log_path}")
        return crit, warn, stats
    text = log_path.read_text(encoding="utf-8")
    http = len(HTTP_RE.findall(text))
    warnings = len(WARN_RE.findall(text))
    fatal = text.count("Traceback")
    stats.update({"http_ok": http, "openrouter_warnings": warnings, "tracebacks": fatal})
    if fatal:
        crit.append(f"live log has {fatal} Traceback(s)")
    if http >= 20 and warnings / max(http, 1) >= 0.25:
        warn.append(
            f"high OpenRouter retry rate: {warnings} warnings / {http} HTTP 200 "
            f"({warnings / http:.0%})"
        )
    elif warnings:
        warn.append(f"OpenRouter warnings so far: {warnings} (retries OK if recovering)")
    return crit, warn, stats


def run_once(base: Path, cfg) -> int:
    now = datetime.now().strftime("%H:%M:%S")
    all_crit: List[str] = []
    all_warn: List[str] = []
    all_info: List[str] = []
    summary: Dict[str, Any] = {"ts": now, "hypotheses": {}}

    log_crit, log_warn, log_stats = check_log(base / "logs" / "audits_live.log")
    all_crit.extend(log_crit)
    all_warn.extend(log_warn)
    summary["log"] = log_stats

    for hyp in ("H1", "H2", "H3", "H4"):
        prompt = load_hypothesis_prompt(cfg, hyp)
        valid = list(list_code_ids(prompt))
        crit, warn, info, stats = check_hypothesis(base, hyp, valid)
        all_crit.extend(crit)
        all_warn.extend(warn)
        all_info.extend(info)
        summary["hypotheses"][hyp] = stats

    print(f"\n[{now}] Stage11 live QA", flush=True)
    if all_crit:
        print("  CRITICAL:", flush=True)
        for m in all_crit:
            print(f"    ✗ {m}", flush=True)
    if all_warn:
        print("  WARNINGS:", flush=True)
        for m in all_warn:
            print(f"    ! {m}", flush=True)
    if all_info:
        print("  OK / info:", flush=True)
        for m in all_info[:12]:
            print(f"    · {m}", flush=True)
        if len(all_info) > 12:
            print(f"    · … +{len(all_info) - 12} more", flush=True)
    if not (all_crit or all_warn or all_info):
        print("  (no audit rows yet)", flush=True)

    out = base / "logs" / "qa_live.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    # Also append a one-line status for tail -f
    status_line = {
        "ts": now,
        "critical": len(all_crit),
        "warnings": len(all_warn),
        "messages_critical": all_crit,
        "messages_warnings": all_warn[:20],
    }
    with (base / "logs" / "qa_live.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(status_line, ensure_ascii=False) + "\n")

    if all_crit:
        return 2
    if all_warn:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default="results/stage11_refined_construct_analysis/v4_l12_granular_final_call49",
    )
    parser.add_argument("--config", default="configs/stage11/refined_constructs.yaml")
    parser.add_argument("--interval", type=float, default=60.0)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    cfg = load_stage11_config(args.config)
    base = Path(args.base)
    base.mkdir(parents=True, exist_ok=True)
    (base / "logs").mkdir(parents=True, exist_ok=True)

    rc = 0
    while True:
        rc = run_once(base, cfg)
        if args.once:
            return rc
        time.sleep(float(args.interval))


if __name__ == "__main__":
    raise SystemExit(main())
