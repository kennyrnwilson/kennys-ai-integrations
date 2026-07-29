---
name: convert-book
description: Convert ebook files (EPUB, PDF) into multiple formats using Calibre. Use when the user wants to convert a book file, remove DRM, or create book-formats folder. Requires Calibre with DeDRM plugin. For ACSM files, use download-acsm first.
argument-hint: <book-file> [--output-dir <directory>] [--force]
user-invocable: true
---

# Book Converter

Convert ebook files (EPUB, PDF) into multiple formats (EPUB, PDF, Markdown, AZW3) using Calibre's command-line tools. Organizes converted files into a `book-formats/` directory ready for AI processing.

For ACSM files, use the `download-acsm` skill first to obtain a DRM-free EPUB/PDF, then pass the result to this skill.

## Prerequisites

- **Calibre** must be installed with `ebook-convert` on PATH
- **DeDRM plugin** should be installed in Calibre so `ebook-convert` can read
  DRM-protected input directly — this skill converts the file in place via
  `ebook-convert` and never adds it to a Calibre library

## Arguments

- `$0` — The input ebook file path (e.g., `~/Downloads/my-book.epub`). Supported formats: `.epub`, `.pdf`.
- `--output-dir` — Output directory path. If not specified, resolved in this order:
  1. If `$EBOOK_LIBRARY_PATH` is set, use `$EBOOK_LIBRARY_PATH/{book-name}/`
  2. Otherwise, create `{book-name}/` under the current working directory
- `--force` — Bypass resume check and reconvert even if outputs already exist.

If no arguments are provided, ask the user for the book file path.

## Workflow

Resolve the output directory, then run the script. It handles validation,
slug derivation, resume, and all four format conversions.

1. Resolve the output directory:
   - If `--output-dir` was given, use it.
   - Otherwise read `EBOOK_LIBRARY_PATH` (`echo $EBOOK_LIBRARY_PATH`) and use
     `$EBOOK_LIBRARY_PATH/{slug}/`.
   - If that variable is unset, use `./{slug}/` and tell the user.

2. Run:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/convert_book.sh" "$INPUT_FILE" "$OUTPUT_DIR" $FORCE_FLAG
```

3. Report the script's output verbatim, including the slug it derived —
   downstream skills key off that slug.

The script exits non-zero on failure with the reason on stderr. Surface it and
stop; do not attempt to convert by other means.

## Error Handling

- **File not found**: Report the exact path that was tried.
- **Calibre not installed**: Tell the user to install Calibre and ensure `ebook-convert` is on PATH.
- **DRM removal fails**: The DeDRM plugin may need configuration. Tell the user to check their Calibre DeDRM plugin setup.
- **ACSM file provided**: Redirect the user to the `download-acsm` skill.
- **Single format conversion fails**: Report the error, continue with remaining formats.
- **Markdown conversion fails**: This is critical — warn that AI processing skills require the markdown file.
