---
name: convert-book
description: Convert ebook files (EPUB, PDF, ACSM) into multiple formats using Calibre. Use when the user wants to convert a book file, remove DRM, or create book-formats folder. Requires Calibre with DeDRM plugin.
argument-hint: <book-file> [--output-dir <directory>] [--force]
user-invocable: true
---

# Book Converter

Convert ebook files (EPUB, PDF, ACSM) into multiple formats (EPUB, PDF, Markdown, AZW3) using Calibre's command-line tools. Organizes converted files into a `book-formats/` directory ready for AI processing.

## Prerequisites

- **Calibre** must be installed with command-line tools available (`calibredb`, `ebook-convert`)
- **DeDRM plugin** should be installed in Calibre for DRM-protected books
- **Adobe Digital Editions** required for ACSM files

## Arguments

- `$0` — The input ebook file path (e.g., `~/Downloads/my-book.epub`). Supported formats: `.epub`, `.pdf`, `.acsm`.
- `--output-dir` — Output directory path. If not specified, a directory is created from the book filename in kebab-case under the current working directory.
- `--force` — Bypass resume check and reconvert even if outputs already exist.

If no arguments are provided, ask the user for the book file path.

## Workflow

### Step 1: Validate Input

1. Check that the input file (`$0`) exists using Bash `ls`.
2. Determine the file format from the extension (`.epub`, `.pdf`, `.acsm`).
3. If the file doesn't exist, tell the user: "File not found: `{path}`" and stop.
4. If the format is unsupported, tell the user: "Unsupported format. Supported formats: .epub, .pdf, .acsm" and stop.

### Step 2: Determine Output Directory

1. If `--output-dir` was specified, use that directory.
2. Otherwise, derive the book name from the filename:
   - Remove the file extension
   - Convert to kebab-case (lowercase, hyphens for spaces/special characters)
   - Create a directory with that name under the current working directory
3. Create the output directory if it doesn't exist.

### Step 3: Resume Check

1. Check if `book-formats/` exists in the output directory.
2. Check if it contains `*_book.epub`, `*_book.pdf`, and `*_book.md`.
3. If all three exist and `--force` was NOT specified, tell the user: "Book formats already exist in `{directory}/book-formats/`. Use `--force` to reconvert." and stop.

### Step 4: Process ACSM (if applicable)

If the input file is `.acsm`:

1. Open with Adobe Digital Editions via Bash: `open -a "Adobe Digital Editions" "{file}"`
2. Tell the user: "Opening ACSM file in Adobe Digital Editions. Please wait for the download to complete, then tell me when it's ready."
3. Wait for user confirmation.
4. The resulting epub/pdf will be in `~/Documents/Digital Editions/`. Ask the user to confirm the downloaded file path, or search for the most recently modified file in that directory.
5. Use the downloaded file as the new input for subsequent steps.

### Step 5: Add to Calibre

1. Run via Bash: `calibredb add "{file}" --with-library ~/calibre-library`
2. This adds the book to the Calibre library. The DeDRM plugin removes DRM automatically during import.
3. If the command fails, try without `--with-library`: `calibredb add "{file}"`
4. If Calibre is not available, tell the user: "Calibre command-line tools not found. Please install Calibre first." and stop.

### Step 6: Export Formats

Extract the book name (kebab-case) for output filenames. Use `ebook-convert` to generate each format:

1. **EPUB** (DRM-free):
   ```bash
   ebook-convert "{input}" "book-formats/{book-name}_book.epub"
   ```

2. **PDF**:
   ```bash
   ebook-convert "{input}" "book-formats/{book-name}_book.pdf"
   ```

3. **Markdown** (for AI processing):
   ```bash
   ebook-convert "{input}" "book-formats/{book-name}_book.md"
   ```

4. **AZW3** (Kindle format):
   ```bash
   ebook-convert "{input}" "book-formats/{book-name}_book.azw3"
   ```

If a conversion fails, report the error and continue with remaining formats. The markdown conversion is the most important — if it fails, warn the user that AI processing skills will not work without it.

### Step 7: Organize

1. Create `book-formats/` directory in the output directory if it doesn't exist.
2. Move all converted files there (they should already be output there from Step 6).
3. Verify all expected files exist.

### Step 8: Report

Tell the user:
- Output directory path
- Files created with sizes (use `ls -lh` via Bash)
- Any formats that failed conversion
- Remind them they can now run `summarize-book`, `chapter-summaries`, etc. on this directory

## Error Handling

- **File not found**: Report the exact path that was tried.
- **Calibre not installed**: Tell the user to install Calibre and ensure `calibredb` and `ebook-convert` are on PATH.
- **DRM removal fails**: The DeDRM plugin may need configuration. Tell the user to check their Calibre DeDRM plugin setup.
- **ACSM processing**: This requires manual steps with Adobe Digital Editions. Guide the user through the process.
- **Single format conversion fails**: Report the error, continue with remaining formats.
- **Markdown conversion fails**: This is critical — warn that AI processing skills require the markdown file.
