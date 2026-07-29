---
name: book-infographics
description: Generate a book-level infographic image using Gemini. Use when the user wants a visual infographic for a book overview. Delegates to the image-gen plugin.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Book Infographics Generator

Generate a book-level infographic image by delegating to the `image-gen` plugin's infographic skill. Produces a Gemini infographic from the book's best available summary.

## Requires

The `image-gen` plugin (v2.0.0 or later) from this marketplace, enabled, plus
`GEMINI_API_KEY` on a funded billing account. If `generate_image.py` is not
found at the expected path, tell the user to enable `image-gen` and stop.
A `429 RESOURCE_EXHAUSTED` means the prepaid balance is spent — stop and
report; do not retry.

`image-gen` is a sibling plugin: the `${CLAUDE_PLUGIN_ROOT}/../image-gen/`
path only resolves when both plugins are installed from the same
marketplace and `image-gen` is enabled.

## Arguments

- `$0` — The book directory path or book name. Can be:
  - A full/relative path (e.g., `~/electronic-books/designing-data-intensive-applications/`)
  - A bare book name (e.g., `designing-data-intensive-applications`) — resolved against `$EBOOK_LIBRARY_PATH`
  Must contain a `summaries/` subdirectory with at least one summary file.
- `--force` — Bypass resume check and regenerate infographics even if they already exist.

If no arguments are provided, ask the user for the book directory path.

**One image per book.** OpenAI is removed from `image-gen` v2, so this skill
now generates only `{book-name}_book_infographic_gemini.png`. Existing
`*_infographic_chatgpt.png` files in the library are left alone — this skill
neither renames nor deletes them.

## Path Resolution

Resolve `$0` to a book directory path:
1. If `$0` is an absolute path or starts with `~`, `./`, or `../` — use it directly
2. If `$0` is a bare name (no path separators): check the `EBOOK_LIBRARY_PATH` environment variable (via Bash: `echo $EBOOK_LIBRARY_PATH`). If set, resolve to `$EBOOK_LIBRARY_PATH/{name}/`. If not set, resolve to `./{name}/`

## Workflow

### Step 1: Locate Best Summary

1. Use Glob to search `summaries/` in the book directory for available summary files.
2. Select the best summary using this priority order:
   - `*_summary_claude_*` (Claude-generated, highest quality)
   - `*_summary_anthropic_*` (Anthropic API)
   - `*_summary_openai_*` (OpenAI API)
   - `*_summary_gemini_*` (Gemini)
   - Any other `*_summary_*` file
3. If no summary is found, tell the user: "No summary found in `{directory}/summaries/`. Please run `summarize-book` first." and stop.

### Step 2: Resume Check

1. Extract the book name from the directory (kebab-case).
2. Check whether `{book-name}_book_infographic_gemini.png` already exists in the book root directory.
3. If it exists and `--force` was NOT specified, tell the user: "Infographic already exists. Use `--force` to regenerate." and stop.

### Step 3: Generate the Book Infographic

If `{book-name}_book_infographic_gemini.png` does not exist (or `--force` was given):

```bash
uv run "${CLAUDE_PLUGIN_ROOT}/../image-gen/scripts/generate_image.py" \
  "{summary-file-path}" --kind infographic \
  --output "{book-directory}/{book-name}_book_infographic_gemini.png"
```

There is no second provider and no pacing requirement.

Report: "Generated book infographic."

If the infographic already exists and `--force` was not specified, skip and report: "Book infographic already exists, skipping."

### Step 4: Report

Tell the user:
- Whether the infographic was generated or skipped (already existed)
- The file path for the generated infographic

## Error Handling

- **No summary found**: Tell the user to run `summarize-book` first.
- **image-gen plugin not available**: Tell the user: "The `image-gen` plugin is required for infographic generation. Please install it first."
- **Infographic generation fails**: Report the error; do not retry.
- **Image generation unavailable**: `generate_image.py` needs `GEMINI_API_KEY`
  on a funded billing account. A `429 RESOURCE_EXHAUSTED` means the prepaid
  balance is spent. Report it and skip the infographic stages; do not retry and
  do not fall back to any browser-based route — none exists.
