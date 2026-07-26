#!/usr/bin/env bash
# Detailed Stage03 v4 Phase 1 BO progress + ETA (from trials_partial + pipeline log).
#
# Usage:
#   ./scripts/stage03/bo_v4_eta.sh mpnet
#   ./scripts/stage03/bo_v4_eta.sh mpnet --watch
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WATCH=0
MODEL="${1:-mpnet}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --watch) WATCH=1; shift ;;
    l12|l6|mpnet) MODEL="$1"; shift ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

case "$MODEL" in
  l12)
    RUN_ID="v4_l12_granular_phase1"
    MODEL_NAME="sentence-transformers/all-MiniLM-L12-v2"
    ;;
  l6)
    RUN_ID="v4_l6_granular_phase1"
    MODEL_NAME="sentence-transformers/paraphrase-MiniLM-L6-v2"
    ;;
  mpnet)
    RUN_ID="v4_mpnet_granular_phase1"
    MODEL_NAME="sentence-transformers/paraphrase-mpnet-base-v2"
    ;;
  *)
    echo "Unknown model '$MODEL'. Use: l12 | l6 | mpnet" >&2
    exit 1
    ;;
esac

EXP="$ROOT/results/experiments/${RUN_ID}"
OPT_DIR="$EXP/opt_1_${MODEL_NAME//\//__}"
PARTIAL="$OPT_DIR/trials_partial.csv"
RESULT="$OPT_DIR/result.json"
PIPE_LOG="$ROOT/logs/stage03_${RUN_ID}.log"
CONSOLE_LOG="$ROOT/logs/${RUN_ID}_console.log"
PID_FILE="$ROOT/logs/${RUN_ID}.pid"
TOTAL=160
STATE="$ROOT/logs/.bo_eta_${MODEL}.state"

format_duration() {
  python3 - <<PY
sec = int(float("$1"))
if sec < 0:
    print("?")
elif sec < 60:
    print(f"{sec}s")
elif sec < 3600:
    print(f"{sec // 60}m {sec % 60}s")
elif sec < 86400:
    h, rem = divmod(sec, 3600)
    print(f"{h}h {rem // 60}m")
else:
    d, rem = divmod(sec, 86400)
    h, rem = divmod(rem, 3600)
    print(f"{d}d {h}h {rem // 60}m")
PY
}

print_status() {
  local now done pid_line last_call last_obj last_topics last_coh last_div
  now=$(date +%s)
  done=0

  if [[ -f "$PARTIAL" ]]; then
    done=$(python3 - <<PY
from pathlib import Path
p = Path("$PARTIAL")
lines = p.read_text(errors="replace").strip().splitlines()
print(max(0, len(lines) - 1) if lines else 0)
PY
)
  fi

  pid_line="not running"
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      pid_line="running (pid $pid)"
    else
      pid_line="stale pid $pid"
    fi
  fi

  last_call="—"
  last_obj="—"
  last_topics="—"
  last_coh="—"
  last_div="—"
  if [[ -f "$PARTIAL" ]] && [[ "$done" -gt 0 ]]; then
    read -r last_call last_coh last_obj last_div last_topics < <(
      python3 - <<PY
import csv
from pathlib import Path
rows = list(csv.DictReader(Path("$PARTIAL").open()))
r = rows[-1]
print(
    r.get("bo_call", "?"),
    f"{float(r.get('coherence_c_v') or 0):.4f}",
    f"{float(r.get('bo_objective') or 0):.4f}",
    f"{float(r.get('topic_diversity') or 0):.3f}",
    f"{float(r.get('n_topics') or 0):.0f}",
)
PY
    )
  fi

  local pct remain eta rate_note
  pct=$(python3 - <<PY
print(f"{100.0 * $done / $TOTAL:.1f}")
PY
)
  remain=$((TOTAL - done))
  eta="?"
  rate_note="warming up (need ≥2 completed calls for ETA)"

  if [[ -f "$STATE" ]]; then
    read -r prev_done prev_ts < "$STATE" || true
    if [[ -n "${prev_done:-}" ]] && [[ -n "${prev_ts:-}" ]] && [[ "$done" -gt "$prev_done" ]]; then
      local delta_calls delta_sec
      delta_calls=$((done - prev_done))
      delta_sec=$((now - prev_ts))
      if [[ "$delta_calls" -gt 0 ]] && [[ "$delta_sec" -gt 0 ]]; then
        local sec_per_call
        sec_per_call=$(python3 - <<PY
print($delta_sec / $delta_calls)
PY
)
        eta=$(format_duration "$(python3 - <<PY
print(int($remain * $sec_per_call))
PY
)")
        rate_note=$(printf "~%.1f min/call | remain %s" \
          "$(python3 -c "print($delta_sec / $delta_calls / 60)")" \
          "$eta")
      fi
    fi
  fi
  echo "$done $now" > "$STATE"

  # Fallback ETA from first→latest BO call timestamps in pipeline log
  if [[ "$eta" == "?" ]] && [[ "$done" -ge 2 ]] && [[ -f "$PIPE_LOG" ]]; then
    read -r eta rate_note < <(
      python3 - <<PY
import re
from pathlib import Path
from datetime import datetime
log = Path("$PIPE_LOG").read_text(errors="replace").splitlines()
pat = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*BO call (\d+)/${TOTAL} complete")
times = {}
for line in log:
    m = pat.search(line)
    if m:
        times[int(m.group(2))] = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
if len(times) >= 2:
    keys = sorted(times)
    span = (times[keys[-1]] - times[keys[0]]).total_seconds()
    n = keys[-1] - keys[0]
    if n > 0 and span > 0:
        spc = span / n
        remain = $TOTAL - $done
        eta_s = int(remain * spc)
        def fmt(sec):
            if sec < 3600: return f"{sec//60}m"
            if sec < 86400: return f"{sec//3600}h {(sec%3600)//60}m"
            return f"{sec//86400}d {(sec%86400)//3600}h"
        print(fmt(eta_s), f"~{spc/60:.1f} min/call (log) | remain {fmt(eta_s)}")
    else:
        print("?", "insufficient log span")
else:
    print("?", "warming up (need ≥2 completed calls for ETA)")
PY
    )
  fi

  local last_log=""
  if [[ -f "$PIPE_LOG" ]]; then
    last_log=$(grep -aE 'BO call |Stage03 run |Embedding cache |Starting model |Completed sentence' "$PIPE_LOG" 2>/dev/null | tail -1 | cut -c1-120 || true)
  fi

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ${MODEL} BO ${RUN_ID}"
  echo "  status:   $pid_line"
  echo "  progress: $done / $TOTAL ($pct%)"
  echo "  last:     call=$last_call  c_v=$last_coh  obj=$last_obj  div=$last_div  n_topics=$last_topics"
  echo "  ETA:      $eta  |  $rate_note"
  if [[ -n "$last_log" ]]; then
    echo "  log:      $last_log"
  fi
  echo "  artifacts: $PARTIAL"
  echo "  logs:      $PIPE_LOG | $CONSOLE_LOG"

  if [[ "$done" -ge "$TOTAL" ]] && [[ -f "$EXP/trials.csv" ]]; then
    echo "  DONE: trials.csv present"
    return 0
  fi
  return 1
}

if [[ "$WATCH" == "1" ]]; then
  while true; do
    if print_status; then
      break
    fi
    sleep "${BO_ETA_INTERVAL:-60}"
  done
else
  print_status || true
fi
