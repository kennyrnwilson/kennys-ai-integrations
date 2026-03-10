---
name: chapter-infographics
description: Generate infographic images for each chapter summary. Use when the user wants visual infographics for individual chapters. Delegates to the image-gen plugin.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Chapter Infographics Generator

Generate infographic images for each chapter summary by delegating to the `image-gen` plugin's infographic skill. Embeds the infographic reference into each chapter markdown and re-converts to PDF.

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

For each chapter markdown file, in order:

1. **Resume check**: Check if `chapter-summaries/chapter-{NN}-{slug}_infographic.png` already exists. If it does and `--force` was NOT specified, skip and report: "Skipping chapter {N} infographic (already exists)."

2. **Generate infographic**: Invoke `/image-gen:infographic-chatgpt` with:
   - Source: the chapter markdown file path
   - Output: `chapter-summaries/chapter-{NN}-{slug}_infographic.png`

3. **Embed in chapter markdown**: Edit the chapter markdown file to add an infographic reference before the "Connections" section (the `## 🔗 Connections` heading). Insert:
   ```markdown
   ## 📊 Infographic

   ![Chapter Infographic](chapter-{NN}-{slug}_infographic.png)

   ---
   ```
   If the Connections section is not found, append the infographic section at the end of the file before the final `---`.

4. **Re-convert to PDF**: Run `pandoc "chapter-summaries/{filename}.md" -o "chapter-summaries/{filename}.pdf" --pdf-engine=weasyprint` via Bash. Skip if pandoc is not available.

5. **Report progress**: "Generated infographic for chapter {N} of {total}: {title}"

### Step 3: Report

Tell the user:
- Total infographics generated
- Any chapters skipped (already had infographics)
- File paths for the generated infographics

## Error Handling

- **No chapter summaries found**: Tell the user to run `chapter-summaries` first.
- **image-gen plugin not available**: Tell the user the `image-gen` plugin is required.
- **Single chapter infographic fails**: Log the error, skip that chapter, continue with remaining chapters. Report failures at the end.
- **Browser not available**: Report the error and suggest the user ensure the Playwright MCP server is configured.
- **PDF re-conversion fails**: Skip PDF for that chapter, continue.
