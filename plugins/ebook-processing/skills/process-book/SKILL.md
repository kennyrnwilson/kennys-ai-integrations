---
name: process-book
description: Run the full ebook processing pipeline — convert, summarize, generate chapters, infographics, critical review, and index. Use when the user wants to process a book end-to-end or run the ebook pipeline.
argument-hint: <book-file-or-directory> [--force] [--skip <stages>]
user-invocable: true
---

# Book Processing Pipeline

Run the full ebook processing pipeline end-to-end. Orchestrates all stage skills in sequence: ACSM download (if needed), convert, summarize, chapter summaries, chapter infographics, book infographics, critical review, and index generation.

## Arguments

- `$0` — A book file, book directory path, or bare book name:
  - **Book file** (`.epub`, `.pdf`) — full pipeline starting with conversion
  - **ACSM file** (`.acsm`) — full pipeline starting with ACSM download
  - **Directory path** (e.g., `~/electronic-books/my-book/`) — enrichment only
  - **Bare book name** (e.g., `designing-data-intensive-applications`) — resolved against `$EBOOK_LIBRARY_PATH`, enrichment only
- `--force` — Pass through to all stage skills to regenerate everything, bypassing resume checks.
- `--skip <stages>` — Comma-separated list of stage names to skip. Valid values: `download-acsm`, `convert`, `summarize`, `chapters`, `chapter-infographics`, `infographics`, `critical-review`, `index`.

If no arguments are provided, ask the user for the book file or directory path.

## Workflow

### Step 1: Determine Input Type

1. Examine `$0` to determine what it is:
   - **ACSM file** (ends with `.acsm`): Set mode to **full pipeline with ACSM download**.
   - **EPUB/PDF file** (ends with `.epub` or `.pdf`): Set mode to **full pipeline**.
   - **Existing directory** (path exists as a directory): Set mode to **enrichment only**.
   - **Bare name** (no path separators, no file extension): Resolve against `$EBOOK_LIBRARY_PATH` (check via Bash: `echo $EBOOK_LIBRARY_PATH`). If set, resolve to `$EBOOK_LIBRARY_PATH/{name}/`. If not set, resolve to `./{name}/`. Set mode to **enrichment only**.
2. If the resolved path doesn't exist, tell the user and stop.
3. Report the mode: "Running in {full pipeline / full pipeline with ACSM download / enrichment only} mode."

### Step 2: Parse Flags

1. Check for `--force` flag. If present, it will be passed through to every stage skill.
2. Check for `--skip` flag. Parse the comma-separated list of stage names to skip.
3. Valid skip values: `download-acsm`, `convert`, `summarize`, `chapters`, `chapter-infographics`, `infographics`, `critical-review`, `index`.
4. If invalid skip values are provided, warn the user and ignore the invalid ones.

### Step 3: Determine Book Directory

1. **For files**: Derive the book name from the filename (kebab-case, remove extension). Check `$EBOOK_LIBRARY_PATH` — if set, create directory under `$EBOOK_LIBRARY_PATH/{book-name}/`. Otherwise, create under the current working directory.
2. **For directories / bare names**: Use the resolved directory from Step 1.
3. Report: "Book directory: `{directory}`"

### Step 4: Run Pipeline

Execute stages in order. For each stage, invoke the corresponding skill with the book directory (or file for convert-book) and the `--force` flag if applicable. Report the result of each stage before moving to the next.

**If a stage fails, log the error and continue with the next stage.** Do not abort the entire pipeline for a single stage failure.

#### Stage 1: Download ACSM
- **Skip if**: Input is NOT an ACSM file OR `download-acsm` is in skip list
- **Invoke**: `/ebook-processing:download-acsm {acsm-file} --output-dir {book-directory}`
- **On success**: Use the downloaded EPUB/PDF as the input for Stage 2
- **Report**: "Stage 1/8: Download ACSM — {result}"

#### Stage 2: Convert Book
- **Skip if**: Input is a directory (enrichment mode) OR `convert` is in skip list
- **Invoke**: `/ebook-processing:convert-book {book-file} --output-dir {book-directory}` (add `--force` if applicable)
- **Report**: "Stage 2/8: Convert Book — {result}"

#### Stage 3: Summarize Book
- **Skip if**: `summarize` is in skip list
- **Invoke**: `/ebook-processing:summarize-book {book-directory}` (add `--force` if applicable)
- **Report**: "Stage 3/8: Summarize Book — {result}"

#### Stage 4: Chapter Summaries
- **Skip if**: `chapters` is in skip list
- **Invoke**: `/ebook-processing:chapter-summaries {book-directory}` (add `--force` if applicable)
- **Report**: "Stage 4/8: Chapter Summaries — {result}"

#### Stage 5: Chapter Infographics
- **Skip if**: `chapter-infographics` is in skip list
- **Invoke**: `/ebook-processing:chapter-infographics {book-directory}` (add `--force` if applicable)
- **Report**: "Stage 5/8: Chapter Infographics — {result}"

#### Stage 6: Book Infographics
- **Skip if**: `infographics` is in skip list
- **Invoke**: `/ebook-processing:book-infographics {book-directory}` (add `--force` if applicable)
- **Report**: "Stage 6/8: Book Infographics — {result}"

#### Stage 7: Critical Review
- **Skip if**: `critical-review` is in skip list
- **Invoke**: `/ebook-processing:critical-review {book-directory}` (add `--force` if applicable)
- **Report**: "Stage 7/8: Critical Review — {result}"

#### Stage 8: Book Index
- **Skip if**: `index` is in skip list (but this should rarely be skipped)
- **Invoke**: `/ebook-processing:book-index {book-directory}` (add `--force` if applicable)
- **Report**: "Stage 8/8: Book Index — {result}"

### Step 5: Final Report

Provide a summary of the entire pipeline run:

```
Pipeline Complete: {book-name}
─────────────────────────────

Stage                Status
─────                ──────
Download ACSM        ✅ Completed / ⏭️ Skipped / ❌ Failed
Convert Book         ✅ Completed / ⏭️ Skipped / ❌ Failed
Summarize Book       ✅ Completed / ⏭️ Skipped / ❌ Failed
Chapter Summaries    ✅ Completed / ⏭️ Skipped / ❌ Failed
Chapter Infographics ✅ Completed / ⏭️ Skipped / ❌ Failed
Book Infographics    ✅ Completed / ⏭️ Skipped / ❌ Failed
Critical Review      ✅ Completed / ⏭️ Skipped / ❌ Failed
Book Index           ✅ Completed / ⏭️ Skipped / ❌ Failed

Book directory: {directory}
```

Include any error details for failed stages.

## Important Notes

- Each stage is a separate skill invocation — the orchestrator delegates entirely to stage skills
- The orchestrator does NOT embed templates — all templates live in the stage skills
- Stages have built-in resume logic, so re-running the pipeline on the same directory will skip already-completed stages (unless `--force` is used)
- The pipeline is designed to be interruptible and resumable

## Error Handling

- **Input not found**: Tell the user the path is invalid.
- **Single stage failure**: Log the error, report it, continue with the next stage.
- **Multiple stage failures**: Report all failures in the final summary. Suggest the user fix the issues and re-run with `--skip` for already-completed stages.
- **Calibre not available (convert stage)**: Skip conversion, tell the user to install Calibre or provide a pre-converted directory.
- **Playwright not available (infographic stages)**: Skip infographic generation, note it in the report.
