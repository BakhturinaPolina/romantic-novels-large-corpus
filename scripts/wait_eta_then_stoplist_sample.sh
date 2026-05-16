#!/usr/bin/env bash
# Wait for train_stage02_eta50/eta_estimate.json, print analysis, plan+run stratified stoplist sample.
set -euo pipefail
cd "$(dirname "$0")/.."
PY=".venv/bin/python"
TXT="data/interim/booknlp_character_runs/train_stage02_eta50/txt_input"
ETA_DIR="data/interim/booknlp_character_runs/train_stage02_eta50"
ETA_FILE="$ETA_DIR/eta_estimate.json"
LOG="logs/wait_eta_then_stoplist_sample.log"
SAMPLE_N="${1:-1500}"
SHARDS="${2:-2}"

mkdir -p logs
exec > >(tee -a "$LOG") 2>&1

echo "[$(date -Is)] Waiting for $ETA_FILE ..."
while [[ ! -f "$ETA_FILE" ]]; do
  if pgrep -f "train_stage02_eta50.*--estimate-eta" >/dev/null 2>&1; then
    tail -1 logs/train_stage02_eta50_resume.log 2>/dev/null | grep -E "ETA sample|projection" || true
  else
    echo "[$(date -Is)] WARN: ETA process not running and file missing."
  fi
  sleep 120
done

echo "[$(date -Is)] ETA file found. Patching README ..."
"$PY" scripts/patch_readme_from_eta.py

echo "[$(date -Is)] Analysis:"
"$PY" - <<'PY'
import json
from pathlib import Path
p = Path("data/interim/booknlp_character_runs/train_stage02_eta50/eta_estimate.json")
r = json.loads(p.read_text())
mean_s = r.get("runtime_mean_s")
med_s = r.get("runtime_median_s")
full_h = r.get("projected_full_corpus_hours") or r.get("projected_total_hours")
lo = r.get("projected_full_corpus_ci95_low_hours") or r.get("projected_ci95_low_hours")
hi = r.get("projected_full_corpus_ci95_high_hours") or r.get("projected_ci95_high_hours")
print(f"  sample_size={r.get('sample_size')} mean_s={mean_s} median_s={med_s} p90_s={r.get('runtime_p90_s')}")
print(f"  full_corpus_hours={full_h} (95% {lo}..{hi})")
if med_s and med_s <= 90:
    print("  decision: median <= 90s -> full corpus may be feasible in ~1 week on 1 GPU")
elif mean_s and mean_s >= 180:
    print("  decision: mean >= 180s -> prefer --stoplist-sample-books or external GPU")
else:
    print("  decision: mixed -> use stratified stoplist sample (recommended)")
PY

echo "[$(date -Is)] Planning $SHARDS shards for stoplist sample N=$SAMPLE_N ..."
"$PY" -m src.stage02_preprocessing.extract_character_names_booknlp \
  --config configs/paths.yaml \
  --run-id "train_stoplist_sample_${SAMPLE_N}" \
  --plan-shards --num-shards "$SHARDS" \
  --stoplist-sample-books "$SAMPLE_N" \
  --txt-input-dir "$TXT"

SHARD_DIR="data/interim/booknlp_character_runs/train_stoplist_sample_${SAMPLE_N}/shards"
echo "[$(date -Is)] Starting sequential shard runs on single GPU ..."
for idx in $(seq 0 $((SHARDS - 1))); do
  i=$(printf '%03d' "$idx")
  echo "[$(date -Is)] Shard $idx ..."
  CUDA_VISIBLE_DEVICES=0 "$PY" -m src.stage02_preprocessing.extract_character_names_booknlp \
    --config configs/paths.yaml \
    --run-id "train_stoplist_sample_${SAMPLE_N}_shard_${i}" \
    --work-ids-file "${SHARD_DIR}/work_ids_shard_${i}.txt" \
    --txt-input-dir "$TXT" \
    --pipeline entity --model small \
    --shard-index "$idx" --shard-count "$SHARDS" \
    --no-merge-stoplist
done

echo "[$(date -Is)] Stoplist sample run complete."
