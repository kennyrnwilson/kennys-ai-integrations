---
name: notebooklm-create
description: Create a Google NotebookLM notebook and upload source materials. Use when the user wants to create a new notebook, upload documents or URLs to NotebookLM, or set up research sources.
argument-hint: <notebook-name> --sources <file1> [file2] [url1] ...
user-invocable: true
allowed-tools: Read, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_fill_form, mcp__plugin_playwright_playwright__browser_file_upload, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_wait_for, mcp__plugin_playwright_playwright__browser_tabs
---

# NotebookLM Notebook Creator

Create a new Google NotebookLM notebook and upload source materials (local files and/or URLs) via Playwright browser automation.

## Arguments

- `$0` — Notebook name (e.g., `"My Research Project"`)
- `--sources` — One or more source paths: local file paths (PDF, text, markdown) and/or URLs (https://...)

If no arguments are provided, ask the user for a notebook name and sources.

## First-Run Setup

On the very first use, a browser window will open and you will need to log into your Google account. After that first login, credentials are persisted automatically in the Playwright browser profile and subsequent runs will not require login.

## Workflow

Follow these steps exactly, in order.

### Step 1: Validate Sources

1. Examine each item in `--sources`.
2. For each item, determine if it is a **local file** or a **URL**:
   - **URL**: Starts with `http://` or `https://`
   - **Local file**: Everything else — verify the file exists using the `Read` tool (just check existence, don't read the full content). If a file does not exist, warn the user and skip it.
3. Tell the user: "Preparing to create notebook '{name}' with {n} sources ({x} files, {y} URLs)."

### Step 2: Navigate to NotebookLM

1. Use `browser_navigate` to go to `https://notebooklm.google.com/`.
2. Wait a moment for the page to load.

### Step 3: Check Login Status

1. Use `browser_snapshot` to get the accessibility tree of the page.
2. Look for elements indicating the user is logged in — a "New notebook" or "Create" button, or the main NotebookLM dashboard with existing notebooks.
3. If logged in, proceed to Step 4.
4. If not logged in (you see a "Sign in" button or login page):
   - Tell the user: "Please log in to your Google account in the browser window that just opened. I'll wait for you to complete login."
   - Poll with `browser_snapshot` every 10 seconds, up to 60 seconds total (6 attempts).
   - If login succeeds (dashboard elements appear), proceed to Step 4.
   - If login does not succeed after 60 seconds, tell the user: "Login timed out after 60 seconds. Please try again." and stop.

### Step 4: Create New Notebook

1. Use `browser_snapshot` to find a "New notebook", "Create", or "+" button in the accessibility tree. Note its `ref` attribute.
2. Use `browser_click` with that ref to create a new notebook.
3. Wait 2-3 seconds for the new notebook to load.
4. Use `browser_snapshot` to verify the notebook has been created (you should see a notebook view with options to add sources).

### Step 5: Set Notebook Title

1. Use `browser_snapshot` to look for a title/name field — it may be an editable heading, a textbox, or the default "Untitled notebook" text.
2. If found, use `browser_click` on the title element to select it, then use `browser_fill_form` or `browser_press_key` to clear the existing text and type the notebook name from `$0`.
3. If no editable title field is found, skip this step — the notebook can be renamed later.

### Step 6: Upload Sources

Process each source one at a time:

#### For Local Files:

1. Use `browser_snapshot` to find an "Add source", "Upload", or "+" button for adding sources. Note its `ref`.
2. Use `browser_click` to open the source upload dialog.
3. Use `browser_snapshot` to look for a file upload option — it may say "Upload files", "Upload", or show a file input area.
4. Use `browser_file_upload` with the local file path to upload the file.
5. Wait for the upload to complete — poll with `browser_snapshot` every 5 seconds, looking for the source to appear in the sources list or a success indicator.
6. Tell the user: "Uploaded: {filename}"

#### For URLs:

1. Use `browser_snapshot` to find an "Add source" button. Note its `ref`.
2. Use `browser_click` to open the source addition dialog.
3. Use `browser_snapshot` to look for a "Website" or "URL" or "Link" option. Click it.
4. Use `browser_snapshot` to find the URL input field. Note its `ref`.
5. Use `browser_fill_form` to paste the URL.
6. Use `browser_snapshot` to find a "Submit", "Add", "Insert", or confirmation button. Click it.
7. Wait for the URL to be processed — poll with `browser_snapshot` every 5 seconds, looking for the source to appear in the sources list.
8. Tell the user: "Added URL: {url}"

**Important**: After each source, wait for NotebookLM to finish processing before adding the next one. Look for processing indicators (spinners, "Processing..." text) to disappear.

### Step 7: Verify Sources

1. Use `browser_snapshot` to examine the sources panel.
2. Count the number of sources shown and compare to expected count.
3. If any sources failed, report which ones.

### Step 8: Capture Notebook URL

1. Use `browser_snapshot` or examine the current page URL.
2. The notebook URL will be in the browser's address bar — it should look like `https://notebooklm.google.com/notebook/...`.
3. Record this URL.

### Step 9: Report to User

Tell the user:
- The notebook was created successfully.
- How many sources were uploaded (and any that failed).
- The notebook URL — they can use this with `notebooklm-generate` to produce outputs.
- Example: "Notebook URL: https://notebooklm.google.com/notebook/abc123 — use this with `/notebooklm:notebooklm-generate` to generate briefings, study guides, or presentations."

## Error Handling

### Login Timeout
If the user does not log in within 60 seconds, tell them: "Login timed out. Please ensure you can access notebooklm.google.com in your browser and try again."

### File Upload Failure
If a file upload fails, report it to the user, skip it, and continue with remaining sources. Do not stop the entire process for one failed source.

### URL Add Failure
If adding a URL fails, report it and continue with remaining sources.

### Cannot Find UI Elements
If `browser_snapshot` does not reveal expected buttons or inputs, take a debug screenshot, tell the user: "Could not find the expected UI element. NotebookLM's interface may have changed. Please check the browser window." and stop.

### Browser Not Available
If any Playwright MCP tool call fails with a connection or browser error, tell the user: "The Playwright browser does not appear to be available. Please ensure the Playwright MCP server is configured and the browser is installed. You may need to run the browser_install tool first."
