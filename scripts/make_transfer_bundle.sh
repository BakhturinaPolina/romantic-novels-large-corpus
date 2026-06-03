#!/usr/bin/env bash
# Assemble a self-contained transfer bundle for shipping Stage03 to another GPU machine.
#
# The bundle is a single folder you can rsync to a flash drive and unpack on a
# second NVIDIA/CUDA box. It carries the full Docker build context (Dockerfile,
# compose file, requirements, app code, configs) so the image can be built there
# without cloning the repo. Data CSVs and the private .env are shipped separately
# (see docker/README.md), never baked into the image.
#
# Regenerate any time the code/config/Dockerfile changes:
#   bash scripts/make_transfer_bundle.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE="${1:-$ROOT/transfer_bundle}"
DOCKER_DIR="$ROOT/docker"

echo "Assembling transfer bundle at: $BUNDLE"
rm -rf "$BUNDLE"
mkdir -p "$BUNDLE"

# Docker build files from docker/ (build context root = bundle root).
cp "$DOCKER_DIR/Dockerfile" "$BUNDLE/"
cp "$DOCKER_DIR/docker-compose.yml" "$BUNDLE/"
cp "$ROOT/.dockerignore" "$BUNDLE/"
cp "$DOCKER_DIR/.env.example" "$BUNDLE/"

# The runbook becomes the bundle README and is also copied into the image
# (Dockerfile: `COPY README.md ./`).
cp "$DOCKER_DIR/README.md" "$BUNDLE/README.md"

# Python build context referenced by the Dockerfile.
cp "$ROOT/requirements.txt" "$BUNDLE/"
cp "$ROOT/requirements-venv.txt" "$BUNDLE/"
cp "$ROOT/Makefile" "$BUNDLE/"

# Application code + configs (exclude caches so the bundle stays small).
rsync -a --delete \
  --exclude '__pycache__' \
  --exclude '*.py[cod]' \
  "$ROOT/src/" "$BUNDLE/src/"
rsync -a --delete "$ROOT/configs/" "$BUNDLE/configs/"

echo "Done. Bundle contents:"
find "$BUNDLE" -maxdepth 1 -mindepth 1 -printf '  %f\n' | sort
echo
echo "Bundle size: $(du -sh "$BUNDLE" | cut -f1)"
echo
echo "Next: copy '$BUNDLE' to the target machine, plus the data CSVs and a"
echo "filled-in .env. Then follow README.md inside the bundle."
