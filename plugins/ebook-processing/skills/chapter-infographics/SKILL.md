---
name: chapter-infographics
description: Generate infographic images for each chapter summary. Use when the user wants visual infographics for individual chapters. Delegates to the image-gen plugin.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Chapter Infographics Generator

Generate infographic images for each chapter summary by delegating to the `image-gen` plugin's infographic skill. Embeds the infographic reference into each chapter markdown and re-converts to PDF.

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
  Must contain a `chapter-summaries/` subdirectory with chapter markdown files.
- `--force` — Bypass resume checks and regenerate all chapter infographics, even if they already exist.

If no arguments are provided, ask the user for the book directory path.

## Path Resolution

Resolve `$0` to a book directory path:
1. If `$0` is an absolute path or starts with `~`, `./`, or `../` — use it directly
2. If `$0` is a bare name (no path separators): check the `EBOOK_LIBRARY_PATH` environment variable (via Bash: `echo $EBOOK_LIBRARY_PATH`). If set, resolve to `$EBOOK_LIBRARY_PATH/{name}/`. If not set, resolve to `./{name}/`

## Workflow

### Step 1: Locate Chapter Summaries

1. Use Glob to find `chapter-summaries/chapter-*.md` files in the book directory.
2. If no chapter summary files are found, tell the user: "No chapter summaries found in `{directory}/chapter-summaries/`. Please run `chapter-summaries` first." and stop.
3. Sort the files by chapter number (based on the `chapter-{NN}` prefix).
4. Report: "Found {N} chapter summaries. Generating infographics..."

### Step 2: For Each Chapter

Generate every chapter's infographic. **There is no pacing requirement and no
per-session cap** — `image-gen` v2 calls the provider APIs directly. Run
straight through the chapter list without sleeping.

For each chapter markdown file, in order:

1. **Resume check** — if `chapter-summaries/chapter-{NN}-{slug}_infographic.png`
   exists and `--force` was not given, skip it and report the skip.

2. **Generate:**

```bash
uv run "${CLAUDE_PLUGIN_ROOT}/../image-gen/scripts/generate_image.py" \
  "chapter-summaries/chapter-{NN}-{slug}.md" \
  --kind infographic \
  --output "chapter-summaries/chapter-{NN}-{slug}_infographic.png"
```

   If the command exits non-zero, report the chapter and the error, then
   continue with the next chapter. Do not abort the whole run for one failure,
   and do not write a `.error.png` or `.debug.png` artefact — those polluted the
   library under the old browser path.

3. **Embed in the chapter markdown** — insert before the `## 🔗 Connections`
   heading (or before the final `---` if that heading is absent):

```markdown
## 📊 Infographic

![Chapter Infographic](chapter-{NN}-{slug}_infographic.png)

---
```

4. **Re-render the PDF** with WeasyPrint:

```bash
weasyprint "chapter-summaries/{filename}.html" "chapter-summaries/{filename}.pdf" 2>/dev/null \
  || echo "PDF regeneration skipped for {filename}"
```

   **Note:** `pandoc` is *not* installed on this machine — do not invoke it.
   If a markdown-to-HTML step is needed first and no converter is available,
   skip PDF regeneration and say so rather than failing the chapter.

5. **Report progress:** "Chapter {N}/{total}: {title} — infographic generated."

### Step 3: Report

Tell the user:
- Total infographics generated
- Any chapters skipped (already had infographics)
- File paths for the generated infographics

## Error Handling

- **No chapter summaries found**: Tell the user to run `chapter-summaries` first.
- **image-gen plugin not available**: Tell the user the `image-gen` plugin is required.
- **Single chapter infographic fails**: Log the error, skip that chapter, continue with remaining chapters. Report failures at the end.
- **Image generation unavailable**: `generate_image.py` needs `GEMINI_API_KEY`
  on a funded billing account. A `429 RESOURCE_EXHAUSTED` means the prepaid
  balance is spent. Report it and skip the infographic stages; do not retry and
  do not fall back to any browser-based route — none exists.
- **PDF re-conversion fails**: Skip PDF for that chapter, continue.
