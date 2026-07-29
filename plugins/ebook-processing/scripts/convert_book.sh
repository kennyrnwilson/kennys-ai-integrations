#!/usr/bin/env bash
# Convert an EPUB or PDF into the book-formats/ layout used by book-library.
#
# Usage: convert_book.sh <input-file> <output-dir> [--force]
#
# Produces <output-dir>/book-formats/<slug>_book.{epub,pdf,md,azw3}
# Requires Calibre CLI (ebook-convert) on PATH.

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <input-file> <output-dir> [--force]" >&2
    exit 2
fi

INPUT="$1"
OUTPUT_DIR="$2"
FORCE="${3:-}"

if [[ ! -f "$INPUT" ]]; then
    echo "Input file not found: $INPUT" >&2
    exit 1
fi

INPUT_LOWER="$(echo "$INPUT" | tr '[:upper:]' '[:lower:]')"

case "$INPUT_LOWER" in
    *.epub|*.pdf) ;;
    *.acsm)
        echo "ACSM files are DRM tokens, not books. Run the download-acsm skill first." >&2
        exit 1
        ;;
    *)
        echo "Unsupported format. Supported: .epub, .pdf" >&2
        exit 1
        ;;
esac

if ! command -v ebook-convert >/dev/null 2>&1; then
    echo "Calibre CLI not found. Install Calibre and ensure ebook-convert is on PATH." >&2
    exit 1
fi

# Derive a kebab-case slug from the filename.
BASENAME="$(basename "$INPUT")"
SLUG="$(echo "${BASENAME%.*}" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"

FORMATS_DIR="$OUTPUT_DIR/book-formats"
mkdir -p "$FORMATS_DIR"

if [[ "$FORCE" != "--force" ]] && [[ -f "$FORMATS_DIR/${SLUG}_book.md" ]]; then
    echo "Already converted: $FORMATS_DIR/${SLUG}_book.md (pass --force to redo)"
    exit 0
fi

echo "Converting '$BASENAME' -> $FORMATS_DIR/${SLUG}_book.*"

# Keep the source in its native format, then derive the rest.
SRC_EXT="${BASENAME##*.}"
SRC_EXT_LOWER="$(echo "$SRC_EXT" | tr '[:upper:]' '[:lower:]')"
cp "$INPUT" "$FORMATS_DIR/${SLUG}_book.${SRC_EXT_LOWER}"

failed=()
for target in epub pdf md azw3; do
    if [[ "$target" == "$SRC_EXT_LOWER" ]]; then
        continue
    fi
    printf '  -> %s ... ' "$target"
    if ebook-convert "$INPUT" "$FORMATS_DIR/${SLUG}_book.${target}" >/dev/null 2>&1; then
        echo "ok"
    else
        echo "FAILED"
        failed+=("$target")
    fi
done

if [[ ${#failed[@]} -gt 0 ]]; then
    echo "Warning: could not produce: ${failed[*]}" >&2
fi

if [[ ! -f "$FORMATS_DIR/${SLUG}_book.md" ]]; then
    echo "Markdown conversion failed; downstream summarisation needs it." >&2
    exit 1
fi

echo "Done. Slug: $SLUG"
