#!/usr/bin/env bash
# Copy project files for large-corpus replication (N=6k–12k books).
# Run from project root: ./scripts/copy_for_large_corpus.sh [TARGET_DIR]
# Example: ./scripts/copy_for_large_corpus.sh ../billionaire_large_corpus

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="${1:-${PROJECT_ROOT}/../billionaire_large_corpus}"

echo "Source (project root): $PROJECT_ROOT"
echo "Target:                $TARGET"
echo ""

if [[ -e "$TARGET" && ! -d "$TARGET" ]]; then
  echo "Error: Target exists and is not a directory: $TARGET"
  exit 1
fi

mkdir -p "$TARGET"
cd "$PROJECT_ROOT"

# --- Directories (full tree) ---
for dir in src configs scripts; do
  if [[ -d "$dir" ]]; then
    echo "Copying $dir/ ..."
    mkdir -p "$TARGET/$dir"
    rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.pytest_cache' "$dir/" "$TARGET/$dir/"
  else
    echo "Skip (missing): $dir/"
  fi
done

# --- Single files at project root ---
for f in Makefile requirements.txt .gitignore .env.example SCIENTIFIC_README.md README.md LICENSE; do
  if [[ -f "$f" ]]; then
    echo "Copying $f"
    cp -a "$f" "$TARGET/"
  else
    echo "Skip (missing): $f"
  fi
done

# --- Optional: analysis structure template ---
mkdir -p "$TARGET/notebooks/07_analysis"
if [[ -f "notebooks/07_analysis/topic_analysis_all_STRUCTURE.md" ]]; then
  echo "Copying notebooks/07_analysis/topic_analysis_all_STRUCTURE.md"
  cp -a "notebooks/07_analysis/topic_analysis_all_STRUCTURE.md" "$TARGET/notebooks/07_analysis/"
fi

# --- Empty data/results dirs so paths.yaml works ---
echo "Creating empty data and output dirs..."
mkdir -p "$TARGET/data/raw" "$TARGET/data/interim" "$TARGET/data/processed"
mkdir -p "$TARGET/results/experiments" "$TARGET/results/stage04_selection" "$TARGET/results/topics" "$TARGET/results/figures"
mkdir -p "$TARGET/models" "$TARGET/logs"

echo ""
echo "Done. Next steps:"
echo "  cd $TARGET"
echo "  git init"
echo "  python -m venv .venv && source .venv/bin/activate   # or use your env manager"
echo "  pip install -r requirements.txt"
echo "  Add your large corpus under data/raw/ and run the pipeline (e.g. make stage01 stage02 ...)."
