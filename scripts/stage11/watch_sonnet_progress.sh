#!/usr/bin/env bash
# Print live Stage 11 Sonnet re-run progress to the terminal.
# Usage: bash scripts/stage11/watch_sonnet_progress.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
BASE=results/stage11_refined_construct_analysis/v4_l12_granular_final_call49/audits
PROGRESS=logs/sonnet_orchestrator_progress.txt

while true; do
  clear 2>/dev/null || true
  echo "======== Stage 11 Sonnet re-run — $(date '+%H:%M:%S') ========"
  if [[ -f "$PROGRESS" ]]; then
    echo "--- orchestrator ---"
    tail -8 "$PROGRESS"
    echo
  fi
  printf "%-4s %8s %8s %8s  status\n" "Hyp" "lex" "ctx" "adj"
  for hyp in h1 h2 h3 h4 h5 h6; do
    H=${hyp^^}
    d="$BASE/$hyp"
    a=0; b=0; c=0
    [[ -f "$d/lexical.jsonl" ]] && a=$(grep -c . "$d/lexical.jsonl" || true)
    [[ -f "$d/contextual.jsonl" ]] && b=$(grep -c . "$d/contextual.jsonl" || true)
    [[ -f "$d/adjudication.jsonl" ]] && c=$(grep -c . "$d/adjudication.jsonl" || true)
    # expected sizes (approx)
    case $hyp in
      h1) exp=98 ;; h2) exp=10 ;; h3) exp=82 ;; h4) exp=32 ;; h5) exp=22 ;; h6) exp=42 ;;
    esac
    st="pending"
    if pgrep -f "05_run_hypothesis_audits.py --hypotheses ${H}" >/dev/null 2>&1 \
       || pgrep -f "06_run_h5_h6_audits.py.*${H}" >/dev/null 2>&1; then
      st="RUNNING ${c}/${exp}"
    elif [[ "$c" -ge "$exp" ]]; then
      st="done"
    elif [[ "$c" -gt 0 ]]; then
      st="partial ${c}/${exp}"
    fi
    printf "%-4s %8d %8d %8d  %s\n" "$H" "$a" "$b" "$c" "$st"
  done
  echo
  echo "--- latest audit log lines ---"
  # Prefer the newest *sonnet* log
  latest=$(ls -t logs/*_sonnet_rerun.log logs/h1_sonnet_full_rerun.log 2>/dev/null | head -1 || true)
  if [[ -n "${latest:-}" ]]; then
    echo "log: $latest"
    # strip NULs from crashed logs
    tr -d '\000' < "$latest" | rg 'INFO \[[0-9]+/[0-9]+\]|DONE|ERROR|Archived|START|HTTP/1.1 [45]|Traceback' | tail -12
  else
    echo "(no sonnet logs yet)"
  fi
  echo
  if ! pgrep -f 'orchestrate_sonnet_rerun|05_run_hypothesis_audits|06_run_h5_h6' >/dev/null 2>&1; then
    if [[ -f "$PROGRESS" ]] && rg -q 'Orchestrator ALL DONE' "$PROGRESS"; then
      echo "ALL DONE"
      break
    fi
  fi
  sleep 20
done
