#!/usr/bin/env bash
# Corne v4 (RP2040, crkbd/rev4_1/standard) Vial firmware build helper
# Usage:
#   ./build.sh           # build → produces .uf2 in ./build/
#   ./build.sh flash     # build + print flashing instructions
#   ./build.sh clean     # clean build artifacts
#
# To build the mini variant, set:
#   KEYBOARD=crkbd/rev4_1/mini ./build.sh
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

VIAL_QMK="${VIAL_QMK:-$HOME/vial-qmk}"
KEYBOARD="${KEYBOARD:-crkbd/rev4_1/standard}"
KEYMAP="takow"
OUT_DIR="$(cd "$(dirname "$0")" && pwd)/build"

if [[ ! -d "$VIAL_QMK" ]]; then
  echo "vial-qmk not found at $VIAL_QMK" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# Convert keyboard path to artifact filename (crkbd/rev4_1/standard -> crkbd_rev4_1_standard)
ARTIFACT_BASE="$(echo "${KEYBOARD}_${KEYMAP}" | tr '/' '_')"

case "${1:-build}" in
  clean)
    cd "$VIAL_QMK"
    make clean
    rm -f "$OUT_DIR"/*.uf2 "$OUT_DIR"/*.hex "$OUT_DIR"/*.bin
    ;;
  build|flash)
    cd "$VIAL_QMK"
    make "${KEYBOARD}:${KEYMAP}"
    for ext in uf2 hex bin; do
      if [[ -f "${ARTIFACT_BASE}.${ext}" ]]; then
        cp "${ARTIFACT_BASE}.${ext}" "$OUT_DIR/"
        echo
        echo "Built: $OUT_DIR/${ARTIFACT_BASE}.${ext}"
      fi
    done
    if [[ "${1:-}" == "flash" ]]; then
      cat <<EOF

=== Flashing Corne v4 (RP2040) ===
For EACH half (left and right), repeat the following:

1. Disconnect USB from PC
2. Hold the BOOT button on the keyboard
3. While holding BOOT, plug USB into PC
4. Release BOOT
5. A USB drive named "RPI-RP2" should appear on your PC
6. Open Explorer at:
     \\\\wsl.localhost\\Ubuntu${OUT_DIR#/mnt/c}\\${ARTIFACT_BASE}.uf2
   OR copy from Windows path:
     ${OUT_DIR//\//\\}\\${ARTIFACT_BASE}.uf2
7. Drag-and-drop the .uf2 file onto the RPI-RP2 drive
8. The drive disappears automatically when flashing completes

After both halves are flashed:
- Connect halves with TRRS cable
- Connect LEFT half to PC via USB (left = master)
- Open Vial — it should now detect "Corne v4"

EOF
    fi
    ;;
  *)
    echo "Unknown command: $1" >&2
    echo "Usage: $0 [build|flash|clean]" >&2
    exit 1
    ;;
esac
