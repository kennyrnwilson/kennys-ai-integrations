---
name: download-acsm
description: Download and unlock ACSM ebook files using Adobe Digital Editions. Use when the user has an ACSM file and needs to obtain a DRM-free EPUB or PDF for further processing.
argument-hint: <acsm-file> [--output-dir <directory>]
user-invocable: true
---

# ACSM Downloader

Download and unlock ACSM ebook files using Adobe Digital Editions. ACSM files are DRM license tokens — this skill opens them in Adobe Digital Editions to download the actual book, then locates the resulting EPUB/PDF for use with `convert-book`.

## Prerequisites

- **Adobe Digital Editions** must be installed and authorized with an Adobe ID
- The Adobe ID must be authorized for the ACSM file's DRM

## Arguments

- `$0` — The ACSM file path (e.g., `~/Downloads/URLLink.acsm`).
- `--output-dir` — Directory to copy the downloaded file to. If not specified, resolved in this order:
  1. If `$EBOOK_LIBRARY_PATH` is set, use `$EBOOK_LIBRARY_PATH/{book-name}/`
  2. Otherwise, the file remains in Adobe Digital Editions' default location (`~/Documents/Digital Editions/`)

If no arguments are provided, ask the user for the ACSM file path.

## Workflow

### Step 1: Validate Input

1. Check that the input file (`$0`) exists using Bash `ls`.
2. Verify the file has an `.acsm` extension.
3. If the file doesn't exist, tell the user: "File not found: `{path}`" and stop.
4. If the file is not `.acsm`, tell the user: "This skill is for ACSM files only. For EPUB/PDF files, use `convert-book` directly." and stop.

### Step 2: Open in Adobe Digital Editions

1. Run via Bash: `open -a "Adobe Digital Editions" "{file}"`
2. Tell the user: "Opening ACSM file in Adobe Digital Editions. The book will download automatically. Please tell me when the download is complete."
3. Wait for user confirmation.

### Step 3: Locate Downloaded File

1. Search `~/Documents/Digital Editions/` for the most recently modified `.epub` or `.pdf` file using Bash:
   ```bash
   ls -t ~/Documents/Digital\ Editions/*.epub ~/Documents/Digital\ Editions/*.pdf 2>/dev/null | head -5
   ```
2. Present the candidate files to the user and ask them to confirm which one is the downloaded book.
3. If no files are found, tell the user: "Could not find downloaded files in `~/Documents/Digital Editions/`. Please check Adobe Digital Editions and provide the file path manually." and stop.

### Step 4: Copy to Output (if requested)

If `--output-dir` was specified:

1. Create the output directory if it doesn't exist.
2. Copy the downloaded file to the output directory via Bash: `cp "{downloaded-file}" "{output-dir}/"`
3. Report the copied file path.

### Step 5: Report

Tell the user:
- The downloaded file path
- The file format (EPUB or PDF)
- Next step: "You can now convert this file with: `/ebook-processing:convert-book {file-path}`"

## Error Handling

- **ACSM file not found**: Report the exact path that was tried.
- **Adobe Digital Editions not installed**: Tell the user: "Adobe Digital Editions is required for ACSM files. Please install it from Adobe's website and authorize it with your Adobe ID."
- **Download fails or hangs**: Tell the user to check Adobe Digital Editions directly. The ACSM token may be expired or the Adobe ID may not be authorized.
- **File not found after download**: Ask the user to manually locate the file and provide the path.
