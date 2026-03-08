---
name: notebooklm-generate
description: Generate outputs from a Google NotebookLM notebook — slide decks, reports, mind maps, quizzes, and more. Use when the user wants to generate content from an existing NotebookLM notebook.
argument-hint: <notebook-url> [--type slide-deck|reports|mind-map|flashcards|quiz|infographic|data-table|audio|video] [--prompt "custom instructions"] [--output file.md] [--format pdf|pptx]
user-invocable: true
---

# NotebookLM Output Generator

Generate outputs from an existing Google NotebookLM notebook via Playwright browser automation. The Studio panel offers multiple output types including slide decks, reports, mind maps, quizzes, and more.

## Arguments

- `$0` — Notebook URL (from `notebooklm-create` output, e.g., `https://notebooklm.google.com/notebook/abc123`)
- `--type` — Output type (default: `reports`). See Output Type Mapping below.
- `--prompt` — Custom instructions for the generation (e.g., `"Focus on economic arguments. 10 slides max. Executive audience."`)
- `--output` — Output file path (default: auto-generated based on type and format)
- `--format` — Download format for slide decks: `pdf` or `pptx` (default: `pdf`). Only applies to `slide-deck` type.

If no arguments are provided, ask the user for a notebook URL.

## First-Run Setup

On the very first use, a browser window will open and you will need to log into your Google account. After that first login, credentials are persisted automatically in the Playwright browser profile and subsequent runs will not require login.

## Output Type Mapping

NotebookLM's Studio panel has these output types. Map the `--type` argument to the UI button labels:

| `--type` value | UI Button Label | Icon | Notes |
|----------------|----------------|------|-------|
| `audio` | "Audio Overview" | `audio_magic_eraser` | Generates a podcast-style audio overview |
| `slide-deck` | "Slide Deck" | `tablet` | Generates a presentation / slides |
| `video` | "Video Overview" | `subscriptions` | Generates a video overview |
| `mind-map` | "Mind Map" | `flowchart` | Generates a visual mind map |
| `reports` | "Reports" | `auto_tab_group` | Generates text reports (briefings, study guides, FAQs) |
| `flashcards` | "Flashcards" | `cards_star` | Generates study flashcards |
| `quiz` | "Quiz" | `quiz` | Generates a quiz |
| `infographic` | "Infographic" | `stacked_bar_chart` | Generates a visual infographic |
| `data-table` | "Data Table" | `table_view` | Generates a structured data table |

Use exact button label matching from the accessibility tree. Each button in the Studio panel has the label as its accessible name.

## Customization

Some output types have a "Customize" button (pencil/edit icon) next to them. When `--prompt` is provided:

1. First click the **"Customize {Type}"** button (e.g., "Customize Slide Deck") to open a customization dialog.
2. The dialog contains options specific to each type. For slide decks, this includes:
   - **Format**: "Detailed Deck" (comprehensive, standalone) or "Presenter Slides" (clean, with talking points)
   - **Language**: Dropdown to choose output language
   - **Length**: Short / Default
   - **Description textbox**: "Describe the slide deck you want to create" — enter `--prompt` text here
3. After filling in options, click the **"Generate"** button inside the dialog.

Output types with customization support (have an edit button): Audio Overview, Slide Deck, Flashcards, Quiz, Infographic, Data Table.

## Workflow

Follow these steps exactly, in order.

### Step 1: Navigate to Notebook

1. Use `browser_navigate` to go to the notebook URL provided in `$0`.
2. Wait 2-3 seconds for the page to load.

### Step 2: Check Login Status

1. Use `browser_snapshot` to get the accessibility tree of the page.
2. Look for elements indicating the notebook is loaded — Sources panel, Chat panel, and Studio panel should all be visible.
3. If the notebook is loaded, proceed to Step 3.
4. If not logged in (you see a "Sign in" button or login page):
   - Tell the user: "Please log in to your Google account in the browser window that just opened. I'll wait for you to complete login."
   - Poll with `browser_snapshot` every 10 seconds, up to 60 seconds total (6 attempts).
   - If login succeeds, the page should redirect to the notebook. Proceed to Step 3.
   - If login does not succeed after 60 seconds, tell the user: "Login timed out after 60 seconds. Please try again." and stop.

### Step 3: Locate the Studio Panel

1. Use `browser_snapshot` to find the **Studio** panel — look for a heading with text "Studio" on the right side of the page.
2. The Studio panel contains all output type buttons. Verify you can see the output type buttons (Audio Overview, Slide Deck, etc.).
3. If the Studio panel is collapsed, look for a button to expand it (may have a `dock_to_left` icon) and click it.

### Step 4: Enter Custom Instructions and Generate

**If `--prompt` was specified** and the target output type supports customization:

1. Look for a **"Customize {Type}"** button next to the output type button (it has an edit/pencil icon).
2. Click it to open a customization **dialog** overlay.
3. Use `browser_snapshot` to examine the dialog. It will contain type-specific options and a description textbox.
4. Find the description textbox (look for a textbox with placeholder text about describing the output).
5. Use `browser_fill_form` to enter the `--prompt` text into the description textbox.
6. Click the **"Generate"** button inside the dialog.
7. Tell the user: "Generating {type}..."

**If `--prompt` was NOT specified** or the output type does not support customization:

1. Use `browser_snapshot` to find the button matching the target output type in the Studio panel (see Output Type Mapping table).
2. Use `browser_click` with the matching button's `ref`.
3. Tell the user: "Generating {type}..."

### Step 5: Wait for Generation

1. Wait 10 seconds initially.
2. Poll with `browser_snapshot` every 30 seconds, for up to 10 minutes (approximately 20 attempts).
3. On each poll, look for:
   - **Generation complete indicators**: The generated output appears in the Studio output area as a clickable item with a title, source count, and timestamp (e.g., "Mastering Biological Time 1 source · 5m ago"). For slide decks, you will see slide thumbnail images.
   - **Still generating indicators**: A disabled button showing "Generating {Type}... based on N source(s)" with a sync icon — continue polling.
   - **Error indicators**: Error messages, "Failed", "Try again" — report to user and stop.
4. When generation appears complete, proceed to Step 6.
5. If generation does not complete after 10 minutes:
   - Use `browser_take_screenshot` to capture a debug screenshot. Save it as `notebooklm_debug.png` in the current working directory.
   - Tell the user: "Generation timed out after 10 minutes. A debug screenshot has been saved. Please check the browser window."
   - Stop.

### Step 6: Open the Generated Output

1. Use `browser_snapshot` to find the generated output item in the Studio panel — it will be a clickable button with the output title.
2. Click on it to open the full output view.
3. Use `browser_snapshot` to verify the output is displayed — you should see the content along with action buttons (Share, More options, etc.).

### Step 7: Save the Output

**For slide decks (`--type slide-deck`):**

Slide decks can be downloaded as PDF or PowerPoint:

1. Use `browser_snapshot` to find the **"More options"** button (three dots / `more_horiz` icon) in the output header.
2. Click it to open the context menu.
3. The menu contains:
   - **"Download PDF Document (.pdf)"** — for PDF format
   - **"Download PowerPoint (.pptx)"** — for PowerPoint format
   - **"Show prompt"** — to view the generation prompt
4. Based on the `--format` argument (default `pdf`):
   - For `pdf`: Click **"Download PDF Document (.pdf)"**
   - For `pptx`: Click **"Download PowerPoint (.pptx)"**
5. The file will download automatically to `.playwright-mcp/` in the current working directory.
6. Use Bash to find the downloaded file: `ls -t .playwright-mcp/*.pdf .playwright-mcp/*.pptx 2>/dev/null | head -1`
7. Move the downloaded file to the `--output` path, or to the current working directory if no output specified: `mv .playwright-mcp/Title-Name.pdf ./`
8. The downloaded filename uses the slide deck title with hyphens (e.g., `Mastering-Biological-Time.pdf`).

**For text-based outputs (reports, flashcards, quiz, data-table):**

1. Use `browser_snapshot` to examine the generated content in the output view.
2. Look for the generated text content directly in the accessibility tree — NotebookLM displays output as readable text.
3. Extract the text content from the accessibility tree elements.
4. If the text content is accessible, use the `Write` tool to save it to the output path.
5. If the text is not directly accessible, check the "More options" menu for download options, or fall back to `browser_take_screenshot`.

**For visual outputs (mind-map, infographic):**

1. Check the "More options" menu for download options (PDF, etc.).
2. If a download option is found, use it.
3. If no download option is available, use `browser_take_screenshot` to capture a screenshot of the output.
4. Save to the output path.

**For media outputs (audio, video):**

1. Use `browser_snapshot` to look for a "Download" or playback controls.
2. If download is available, click it.
3. Otherwise, tell the user the media was generated and is available in the browser.

**Determine output path:**
1. If `--output` was specified, use that path.
2. Otherwise, use the auto-downloaded filename in the current working directory. Default patterns:
   - Slide decks: `{title}.pdf` or `{title}.pptx`
   - Text outputs: `notebooklm_{type}.md`
   - Screenshots: `notebooklm_{type}.png`

### Step 8: Report to User

Tell the user:
- The output was generated and saved successfully.
- The full output file path.
- The output type and format that was generated.
- The title NotebookLM gave the output.
- Any relevant details (e.g., number of slides, whether text was extracted or a screenshot was captured as fallback).

## Error Handling

### Login Timeout
If the user does not log in within 60 seconds, tell them: "Login timed out. Please ensure you can access notebooklm.google.com in your browser and try again."

### Notebook Not Found
If navigating to the notebook URL shows an error page or "not found" message, tell the user: "Could not access the notebook. Please verify the URL is correct and that you have access to this notebook."

### Output Type Not Found
If the requested output type button cannot be found in the UI, list the available options visible in the accessibility tree and ask the user which one to use.

### Generation Timeout
If generation does not complete after 10 minutes, capture a debug screenshot, inform the user, and suggest checking the browser window.

### Download Failed
If the download menu item is not found or the download does not complete, fall back to `browser_take_screenshot` and inform the user: "Could not download the file. A screenshot of the output has been saved instead."

### Cannot Extract Text
If the generated text content cannot be extracted from the accessibility tree, fall back to taking a screenshot and inform the user: "Could not extract the text content. A screenshot of the output has been saved instead."

### Browser Not Available
If any Playwright MCP tool call fails with a connection or browser error, tell the user: "The Playwright browser does not appear to be available. Please ensure the Playwright MCP server is configured and the browser is installed. You may need to run the browser_install tool first."
