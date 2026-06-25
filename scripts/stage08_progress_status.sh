#!/usr/bin/env bash
# Quick Stage08 status: pilot JSONs, topic counts, latest log.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${ROOT}/results/stage08_llm_labeling/placeholder_v4_call73"
LOG_DIR="${ROOT}/logs"

echo "=== Stage08 call_73 labeling status ==="
echo "Output: ${OUT}/"
echo ""

if [[ -d "$OUT" ]]; then
  shopt -s nullglob
  files=("$OUT"/*.json)
  if ((${#files[@]} == 0)); then
    echo "(no label JSON files yet)"
  else
    printf "%-8s  %s\n" "TOPICS" "FILE"
    for f in "${files[@]}"; do
      n=$(python3 -c "import json; print(len(json.load(open('$f'))))")
      printf "%-8s  %s\n" "$n" "$(basename "$f")"
    done | sort -t_ -k1 -n
  fi
fi

echo ""
latest_log=$(ls -t "$LOG_DIR"/stage08_llm_labeling_*.log 2>/dev/null | head -1 || true)
if [[ -n "${latest_log:-}" ]]; then
  echo "Latest log: $latest_log"
  echo "Last 5 topic lines:"
  grep -E 'topic [0-9]+ \| label=' "$latest_log" 2>/dev/null | tail -5 || true
fi

echo ""
echo "Progress doc: results/reports/stage08_progress.md"
