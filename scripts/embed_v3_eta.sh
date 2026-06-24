#!/usr/bin/env bash
# Print embedding progress and ETA from .progress.json (or the encode log).
#
# Usage:
#   ./scripts/embed_v3_eta.sh minilm6
#   ./scripts/embed_v3_eta.sh minilm6 --watch
#   ./scripts/embed_v3_eta.sh --watch minilm6
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WATCH="${WATCH:-0}"
MODEL="${1:-minilm6}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --watch) WATCH=1; shift ;;
    minilm6|mpnet) MODEL="$1"; shift ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

case "$MODEL" in
  minilm6)
    CACHE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-MiniLM-L6-v2.npy"
    LOG="$ROOT/logs/v3_embeddings_minilm6.log"
    ;;
  mpnet)
    CACHE="data/interim/octis/v3_english_only/embeddings_cache/train_eval_sentence-transformers__paraphrase-mpnet-base-v2.npy"
    LOG="$ROOT/logs/v3_embeddings_mpnet.log"
    ;;
  *)
    echo "Unknown model '$MODEL'. Use: minilm6 | mpnet" >&2
    exit 1
    ;;
esac

PROGRESS="$ROOT/${CACHE}.progress.json"
STATE="$ROOT/logs/.embed_eta_${MODEL}.state"
TOTAL="${EMBED_TOTAL_ROWS:-97428306}"

read_progress() {
  local done=0 total="$TOTAL"
  if [[ -f "$PROGRESS" ]]; then
    read -r done total < <(
      python3 - <<PY
import json
from pathlib import Path
p = Path("$PROGRESS")
if p.exists():
    d = json.loads(p.read_text())
    print(int(d.get("rows_done", 0)), int(d.get("n_total", $TOTAL)))
else:
    print(0, $TOTAL)
PY
    )
  elif [[ -f "$LOG" ]]; then
    read -r done total < <(
      python3 - <<PY
import re
from pathlib import Path
log = Path("$LOG").read_text(errors="replace").splitlines()
pat = re.compile(r"Embeddings progress: (\d+) / (\d+)")
done = total = 0
for line in log:
    m = pat.search(line)
    if m:
        done, total = int(m.group(1)), int(m.group(2))
if done == 0 and Path("${ROOT}/${CACHE}").exists() and not Path("$PROGRESS").exists():
    done = total = $TOTAL
print(done, total or $TOTAL)
PY
    )
  elif [[ -f "${ROOT}/${CACHE}" ]] && [[ ! -f "$PROGRESS" ]]; then
    done=$TOTAL
  fi
  echo "$done $total"
}

format_duration() {
  python3 - <<PY
sec = int("$1")
if sec < 0:
    print("?")
elif sec < 60:
    print(f"{sec}s")
elif sec < 3600:
    print(f"{sec//60}m {sec%60}s")
elif sec < 86400:
    h, rem = divmod(sec, 3600)
    print(f"{h}h {rem//60}m")
else:
    d, rem = divmod(sec, 86400)
    print(f"{d}d {rem//3600}h")
PY
}

print_eta() {
  local now done total pct remain rate eta
  read -r done total <<< "$(read_progress)"
  now=$(date +%s)

  if [[ "$done" -ge "$total" ]] && [[ "$total" -gt 0 ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $MODEL: complete ($done / $total rows)"
    return 0
  fi

  pct=$(python3 - <<PY
print(f"{100.0 * $done / $total:.2f}" if $total else "0.00")
PY
)

  rate=""
  eta="?"
  remain=$((total - done))
  if [[ -f "$STATE" ]]; then
    read -r prev_done prev_ts < "$STATE" || true
    if [[ -n "${prev_done:-}" ]] && [[ -n "${prev_ts:-}" ]]; then
      delta_rows=$((done - prev_done))
      delta_sec=$((now - prev_ts))
      if [[ "$delta_rows" -gt 0 ]] && [[ "$delta_sec" -gt 0 ]]; then
        rate=$(python3 - <<PY
print(f"{($delta_rows / $delta_sec):.0f}")
PY
)
        eta=$(format_duration "$(python3 - <<PY
print(int($remain / ($delta_rows / $delta_sec)))
PY
)")
      fi
    fi
  fi
  echo "$done $now" > "$STATE"

  if [[ -n "$rate" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $MODEL: $done / $total ($pct%) | ~${rate} rows/s | ETA ${eta} | remain $(format_duration "$(python3 - <<PY
print(int($remain / float("$rate")))
PY
)")"
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $MODEL: $done / $total ($pct%) | warming up (need second sample for ETA)"
  fi
}

if [[ "$WATCH" == "1" ]]; then
  while true; do
    print_eta
    read -r done total <<< "$(read_progress)"
    if [[ "$done" -ge "$total" ]] && [[ "$total" -gt 0 ]]; then
      break
    fi
    sleep "${EMBED_ETA_INTERVAL:-60}"
  done
else
  print_eta
fi
