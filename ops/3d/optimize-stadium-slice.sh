#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 path/to/stadium_slice_raw.glb" >&2
  exit 1
fi

IN="$1"
DIR="$(cd "$(dirname "$IN")" && pwd)"
BASE="$(basename "$IN" .glb)"
OPT="$DIR/${BASE}_opt.glb"
LOW="$DIR/${BASE}_low.glb"
LOW2="$DIR/${BASE}_low2.glb"
KTX2="$DIR/${BASE}_ktx2.glb"

NPX="npx --yes @gltf-transform/cli"

echo "[1/6] Inspect raw"
$NPX inspect "$IN" || true

echo "[2/6] Optimize + meshopt"
$NPX optimize "$IN" "$OPT" --meshopt

echo "[3/6] Simplify 0.5"
$NPX simplify "$OPT" "$LOW" --ratio 0.5

echo "[4/6] Simplify 0.35"
$NPX simplify "$LOW" "$LOW2" --ratio 0.35

echo "[5/6] Convert textures to KTX2 (etc1s)"
$NPX etc1s "$LOW2" "$KTX2"

echo "[6/6] Inspect final"
$NPX inspect "$KTX2" || true

echo "Done. Final: $KTX2"
