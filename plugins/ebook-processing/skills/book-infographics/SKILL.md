---
name: book-infographics
description: Generate book-level infographic images using ChatGPT and Gemini. Use when the user wants visual infographics for a book overview. Delegates to the image-gen plugin.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Book Infographics Generator

Generate book-level infographic images by delegating to the `image-gen` plugin's infographic skills. Produces both a ChatGPT and Gemini infographic from the book's best available summary.

## Arguments

- `$0` — The book directory path (e.g., `~/electronic-books/designing-data-intensive-applications/`). Must contain a `summaries/` subdirectory with at least one summary file.
- `--force` — Bypass resume check and regenerate infographics even if they already exist.

If no arguments are provided, ask the user for the book directory path.

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
2. Check for existing infographic files in the book root directory:
   - `{book-name}_book_infographic_chatgpt.png`
   - `{book-name}_book_infographic_gemini.png`
3. Note which ones already exist. If both exist and `--force` was NOT specified, tell the user: "Both infographics already exist. Use `--force` to regenerate." and stop.

### Step 3: Generate ChatGPT Infographic

If `{book-name}_book_infographic_chatgpt.png` does not exist (or `--force` was specified):

1. Invoke the `/image-gen:infographic-chatgpt` skill with:
   - Source: the summary file path found in Step 1
   - Output: `{book-directory}/{book-name}_book_infographic_chatgpt.png`
2. Report: "Generated ChatGPT infographic."

If the infographic already exists and `--force` was not specified, skip and report: "ChatGPT infographic already exists, skipping."

### Step 4: Generate Gemini Infographic

If `{book-name}_book_infographic_gemini.png` does not exist (or `--force` was specified):

1. Invoke the `/image-gen:infographic-gemini` skill with:
   - Source: the summary file path found in Step 1
   - Output: `{book-directory}/{book-name}_book_infographic_gemini.png`
2. Report: "Generated Gemini infographic."

If the infographic already exists and `--force` was not specified, skip and report: "Gemini infographic already exists, skipping."

### Step 5: Report

Tell the user:
- Which infographics were generated (ChatGPT, Gemini, or both)
- Which were skipped (already existed)
- File paths for the generated infographics

## Error Handling

- **No summary found**: Tell the user to run `summarize-book` first.
- **image-gen plugin not available**: Tell the user: "The `image-gen` plugin is required for infographic generation. Please install it first."
- **Infographic generation fails**: Report the error for that provider, continue with the other provider if applicable.
- **Browser not available**: The image-gen skills require Playwright browser automation. If the browser is not available, report the error and suggest the user ensure the Playwright MCP server is configured.
