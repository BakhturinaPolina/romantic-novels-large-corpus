#!/usr/bin/env bash
# Relabel call73 snippet-trap panel only (v3_rep_first). Production v3_topic_labeling unchanged.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"

PANEL_JSON="data/stage08_benchmark/call73_snippet_trap_panel.json"
CONFIG="configs/stage08/stage08_labeling_rep_first.yaml"
OUTPUT_SUFFIX="snippet_trap_rep_first"
TS="$(date +%Y%m%d_%H%M%S)"
LOG="logs/stage08_snippet_trap_relabel_${TS}.log"
mkdir -p logs

TOPIC_IDS="$("$PY" -c "
import json
from pathlib import Path
p = json.loads(Path('${PANEL_JSON}').read_text())
print(','.join(str(t) for t in p['topic_ids']))
")"

echo "=== Stage08 snippet-trap relabel (v3_rep_first) ===" | tee "$LOG"
echo "Panel: ${PANEL_JSON} ($(echo "$TOPIC_IDS" | tr ',' '\n' | wc -l) topics)" | tee -a "$LOG"
echo "Log: $LOG" | tee -a "$LOG"

SNIPPET_TRAP_DIR="results/stage08_llm_labeling/placeholder_v4_call73/snippet_trap"
mkdir -p "$SNIPPET_TRAP_DIR"

"$PY" -m src.stage08_llm_labeling.openrouter_experiments.core.main_openrouter \
  --stage08-config "$CONFIG" \
  --topic-ids "$TOPIC_IDS" \
  --output-dir "$SNIPPET_TRAP_DIR" \
  --output-suffix "$OUTPUT_SUFFIX" \
  --label-all-topics \
  --no-integrate \
  --no-resume \
  2>&1 | tee -a "$LOG"

LABELS_JSON=$(ls -t "$SNIPPET_TRAP_DIR"/*"${OUTPUT_SUFFIX}"*.json 2>/dev/null | head -1)
echo "Labels: $LABELS_JSON" | tee -a "$LOG"

"$PY" - <<'PY' | tee -a "$LOG"
import csv
import json
from pathlib import Path

panel = json.loads(Path("data/stage08_benchmark/call73_snippet_trap_panel.json").read_text())
prod_path = Path("results/stage08_llm_labeling/placeholder_v4_call73/production/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_topic_labeling.json")
snippet_trap_dir = Path("results/stage08_llm_labeling/placeholder_v4_call73/snippet_trap")
rep_paths = sorted(snippet_trap_dir.glob("*snippet_trap_rep_first*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
if not rep_paths:
    raise SystemExit("No snippet_trap_rep_first labels JSON found")
rep_path = rep_paths[0]
prod = json.loads(prod_path.read_text())
rep = json.loads(rep_path.read_text())

out_csv = snippet_trap_dir / "comparison_call73.csv"
rows = []
changed = 0
for tid in panel["topic_ids"]:
    ps, rs = prod.get(str(tid), {}), rep.get(str(tid), {})
    pl, rl = ps.get("label", ""), rs.get("label", "")
    if pl != rl:
        changed += 1
    rows.append({
        "topic_id": tid,
        "production_label": pl,
        "rep_first_label": rl,
        "changed": pl != rl,
        "rep_first_rationale": (rs.get("rationale") or "")[:240],
    })

out_csv.parent.mkdir(parents=True, exist_ok=True)
with out_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print(f"Comparison CSV: {out_csv}")
print(f"Labels changed: {changed}/{len(rows)}")
PY

ARCHIVE_DIR="results/stage08_llm_labeling/prompt_sweeps/call73/v3_rep_first"
mkdir -p "$ARCHIVE_DIR"
cp "$LABELS_JSON" "$ARCHIVE_DIR/"
cp results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/snippet_trap_merge_log.json "$ARCHIVE_DIR/" 2>/dev/null || true

echo "Merging into stage09_input..." | tee -a "$LOG"
"$PY" -m src.stage08_llm_labeling.openrouter_experiments.tools.merge_snippet_trap_into_stage09 \
  --panel-json "$PANEL_JSON" \
  --overrides-json "$LABELS_JSON" \
  --slim-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3.json \
  --review-json results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/topic_metadata_v3_review_enriched.json \
  2>&1 | tee -a "$LOG"

cp results/stage08_llm_labeling/placeholder_v4_call73/stage09_input/snippet_trap_merge_log.json "$ARCHIVE_DIR/"
echo "Archived to $ARCHIVE_DIR" | tee -a "$LOG"
