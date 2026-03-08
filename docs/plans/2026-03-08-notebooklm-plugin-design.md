# NotebookLM Plugin Design

## Goal

Create a Claude Code plugin that automates Google NotebookLM via browser automation (Playwright MCP), enabling users to create notebooks, upload sources, and generate outputs (briefing docs, study guides, FAQs, presentations) from the command line.

## Decisions

- **Separate plugin** (`notebooklm`) — not part of `image-gen`, different category (research/content synthesis)
- **Two skills**: `notebooklm-create` (create + upload) and `notebooklm-generate` (produce outputs)
- **Separate browser profile** (`mcp-notebooklm-profile`) to avoid session conflicts with image-gen
- **One generate skill with `--type` flag** rather than separate skills per output type
- **Custom instructions via `--prompt`** for controlling output focus/style
- **Both local files and URLs** supported as sources

## Plugin Structure

```
plugins/notebooklm/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json                    # Playwright MCP with persistent profile
└── skills/
    ├── notebooklm-create/
    │   └── SKILL.md
    └── notebooklm-generate/
        └── SKILL.md
```

## Skill 1: `notebooklm-create`

**Purpose:** Create a new NotebookLM notebook and upload source materials.

**Arguments:**
- `$0` — Notebook name (e.g., `"My Research"`)
- `--sources` — One or more local file paths and/or URLs

**Usage:**
```bash
/notebooklm:notebooklm-create "My Research" --sources file1.pdf file2.md https://example.com/article
```

**Workflow:**
1. Navigate to `https://notebooklm.google.com/`
2. Check Google login (same pattern as Gemini — poll for UI elements indicating logged-in state)
3. Click "New notebook" or equivalent button
4. Set the notebook title
5. Upload sources one by one:
   - **Files**: Use `browser_file_upload` for each local file (PDF, text, markdown)
   - **URLs**: Use the "Add source" > "Website" flow, paste URL into the input
6. Wait for each source to process (NotebookLM shows processing status per source)
7. Capture the notebook URL from the browser address bar
8. Report to user: notebook created, sources uploaded, notebook URL

**Output:** The notebook URL — user passes this to `notebooklm-generate`.

## Skill 2: `notebooklm-generate`

**Purpose:** Generate an output from an existing NotebookLM notebook.

**Arguments:**
- `$0` — Notebook URL (from `notebooklm-create` output)
- `--type` — Output type: `briefing` (default), `study-guide`, `faq`, `presentation`
- `--prompt` — Custom instructions for generation (e.g., `"Focus on economic arguments. 10 slides max."`)
- `--output` — Optional output file path

**Usage:**
```bash
/notebooklm:notebooklm-generate https://notebooklm.google.com/notebook/abc123 --type briefing
/notebooklm:notebooklm-generate https://notebooklm.google.com/notebook/abc123 --type presentation --prompt "Focus on key findings. Executive audience."
```

**Workflow:**
1. Navigate to the notebook URL
2. Check Google login
3. Locate the "Notebook guide" or output generation panel in the accessibility tree
4. Select the output type (briefing, study guide, FAQ, or presentation)
5. If `--prompt` is provided, find the customize/instructions input and enter the custom text
6. Trigger generation
7. Wait for generation to complete (poll accessibility tree for output content)
8. Save the output:
   - **Text outputs** (briefing, study-guide, faq): Copy generated content, save as markdown file
   - **Presentation**: Download the generated file if available, or screenshot as fallback
9. Report to user: output saved, file path

## MCP Configuration

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--user-data-dir", "~/Library/Caches/ms-playwright/mcp-notebooklm-profile"
      ]
    }
  }
}
```

Separate profile from image-gen to avoid session conflicts.

## Error Handling

Same patterns as image-gen skills:
- **Login timeout**: Poll 60 seconds, instruct user to log in
- **Source upload failure**: Report which source failed, continue with others
- **Generation timeout**: Poll up to 5 minutes, capture debug screenshot on failure
- **UI element not found**: Capture snapshot for debugging, report to user
- **Browser not available**: Instruct user to check Playwright MCP config

## Uncertainty

NotebookLM's accessibility tree structure is untested. The skills will use generic element discovery (look for buttons by accessible name, text inputs by role) rather than hardcoded selectors. First test run may require refinement of element identification logic.

## First-Run Setup

Same as image-gen: on first use, browser window opens for Google login. Credentials persist in the browser profile for all future sessions.
