# Infographics Plugin — Design & Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a shareable Claude Code plugin that generates infographic images from text using Gemini (and later ChatGPT) web interfaces via Playwright MCP browser automation.

**Architecture:** Two skills within a single plugin. Each skill instructs Claude to use Playwright MCP tools to navigate to an AI chat interface (Gemini or ChatGPT), submit a prompt with the user's text, wait for an image to be generated, and save it locally. The Playwright MCP is configured with a persistent browser profile so the user only logs into Google once. No Python scripts — pure skill-driven browser automation.

**Tech Stack:** Claude Code plugin system, Playwright MCP (`@playwright/mcp`), Gemini web interface, ChatGPT web interface (phase 2).

---

## Scope

### Phase 1 (This Plan): Gemini Infographic Skill
- Plugin scaffold (plugin.json, .mcp.json)
- `infographic-gemini` skill with full Playwright MCP workflow
- Marketplace registration
- README updates

### Phase 2 (Future): ChatGPT Infographic Skill
- `infographic-chatgpt` skill (same pattern, different selectors/workflow)

### Out of Scope
- OpenAI API / Anthropic API calls
- Python browser automation scripts
- Shortform downloads
- ACSM handling, OCR
- Ebook format conversion (separate plugin later)

---

## Key Design Decisions

### Why Playwright MCP Instead of Python Scripts
The original ebook-processing pipeline used 400-500 line Python scripts with Playwright for browser automation. The Playwright MCP server (`@playwright/mcp@latest`) gives Claude Code native browser automation tools — navigate, click, fill, screenshot, wait. The skill just tells Claude *what to do* and Claude uses the MCP tools directly. This eliminates all Python code for browser automation.

### Why Persistent Browser Profile
Gemini requires Google login. The Playwright MCP `--user-data-dir` flag persists cookies between sessions. User logs in once on first use; all subsequent sessions are pre-authenticated. No need to launch Chrome with special flags or install browser extensions.

### Why Skills Not Agents
Skills run in the main conversation context where Playwright MCP tools are available. They allow user interaction mid-flow (e.g., "please log in now"). Agents would add subprocess overhead and complexity without benefit for this use case.

### Prompt Template
Ported from the proven `generate_infographic_gemini_web.py` prompt. Key elements:
- Dark theme (navy/blue background)
- No real people depiction (Gemini constraint)
- Abstract icons, symbols, conceptual imagery
- Style parameter (modern/minimal/abstract/illustrated/tech)
- Text truncated to 3000 characters

---

## Plugin File Structure

```
plugins/infographics/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── .mcp.json                    # Playwright MCP with persistent profile
└── skills/
    └── infographic-gemini/
        └── SKILL.md             # Gemini infographic generation skill
```

---

## Task 1: Create Plugin Scaffold

**Files:**
- Create: `plugins/infographics/.claude-plugin/plugin.json`
- Create: `plugins/infographics/.mcp.json`

**Step 1: Create the plugin manifest**

Create `plugins/infographics/.claude-plugin/plugin.json`:
```json
{
  "name": "infographics",
  "version": "1.0.0",
  "description": "Generate infographic images from text using AI chat interfaces via browser automation",
  "author": {
    "name": "kennyrnwilson"
  },
  "repository": "https://github.com/kennyrnwilson/kennys-ai-integrations",
  "license": "MIT",
  "keywords": ["infographic", "image-generation", "gemini", "browser-automation"]
}
```

**Step 2: Create the Playwright MCP configuration**

Create `plugins/infographics/.mcp.json`:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--user-data-dir", "~/Library/Caches/ms-playwright/mcp-infographics-profile"
      ]
    }
  }
}
```

**Step 3: Commit**

```bash
git add plugins/infographics/.claude-plugin/plugin.json plugins/infographics/.mcp.json
git commit -m "feat: scaffold infographics plugin with Playwright MCP config"
```

---

## Task 2: Create the Gemini Infographic Skill

**Files:**
- Create: `plugins/infographics/skills/infographic-gemini/SKILL.md`

**Step 1: Write the SKILL.md**

The skill must contain:
1. Frontmatter with name, description, trigger conditions
2. The prompt template
3. Step-by-step Playwright MCP workflow instructions
4. DOM selector fallback lists (ported from the Python script)
5. Image download strategy
6. Error handling guidance
7. Output naming conventions

Key workflow steps for the skill to instruct Claude:

```
1. Read the source text (user provides file path or text in conversation)
2. Truncate to first 3000 characters
3. Construct the prompt using the template
4. Use browser_navigate to go to https://gemini.google.com/
5. Use browser_snapshot to check if logged in (look for chat input)
6. If not logged in → tell user to log in manually in the browser window
7. Use browser_snapshot to get the ref for the text input area
8. Use browser_fill_form to enter the prompt, then browser_press_key Enter or browser_click send
9. Wait ~10 seconds, then start polling with browser_snapshot for image elements
10. When an image appears in the response, use browser_take_screenshot with element ref to save it
11. Use browser_click to start a new chat (cleanup)
12. Report the saved file path to the user
```

DOM selectors to try (from existing script):
- Chat input: `textarea[placeholder*="Enter"]`, `textarea[aria-label*="chat"]`, `div[contenteditable="true"]`, `textarea`
- Send button: `button[aria-label*="Send"]`, `button[aria-label*="submit"]`, `button:has-text("Send")`
- New chat: `button:has-text("New chat")`, `a:has-text("New chat")`

Image detection strategy (from existing script):
- Find all `img` elements on page
- Filter for images > 200x200 pixels (excludes UI icons)
- Take the last matching candidate (most recently generated)
- Use element screenshot to save (most reliable method)

**Step 2: Commit**

```bash
git add plugins/infographics/skills/infographic-gemini/SKILL.md
git commit -m "feat: add Gemini infographic generation skill with Playwright MCP workflow"
```

---

## Task 3: Register Plugin in Marketplace

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md`

**Step 1: Add plugin to marketplace catalog**

Add to the `plugins` array in `.claude-plugin/marketplace.json`:
```json
{
  "name": "infographics",
  "source": "./plugins/infographics",
  "description": "Generate infographic images from text using AI chat interfaces via browser automation"
}
```

**Step 2: Add plugin section to README.md**

Add after the mermaid-diagrams section:
```markdown
### `infographics` — AI-Powered Infographic Generator

Generate beautiful infographic images from text summaries using AI chat interfaces.

```bash
/infographics:infographic-gemini path/to/summary.md
/infographics:infographic-gemini path/to/summary.md --output infographic.png --style minimal
```

Features:
- Browser automation via Playwright MCP (no Python scripts needed)
- Persistent browser profile (log in to Google once, stays authenticated)
- Dark-theme infographics with vibrant colors
- Multiple style options (modern, minimal, abstract, illustrated, tech)
- Gemini web interface for free image generation

**First-run setup:** On first use, a browser window opens. Log into your Google account once — credentials persist for all future sessions.
```

**Step 3: Commit**

```bash
git add .claude-plugin/marketplace.json README.md
git commit -m "feat: register infographics plugin in marketplace and update README"
```

---

## Task 4: Test the Skill End-to-End

**Step 1: Install the plugin locally**

```bash
/plugin install infographics@kennys-ai-integrations
```

Or for local development, enable the plugin from the local path.

**Step 2: Create a test summary file**

Create a short test markdown file with a book summary or any substantial text (~500 words).

**Step 3: Invoke the skill**

```
Generate a Gemini infographic from test-summary.md
```

**Step 4: Verify**
- Browser opens (or reuses existing session)
- If first run: user is prompted to log into Google
- Prompt is submitted to Gemini
- Image is generated and saved
- File path is reported back

**Step 5: Iterate on selectors if needed**

Gemini's DOM changes over time. If selectors fail:
- Use `browser_snapshot` to inspect current page structure
- Update SKILL.md with new selectors
- The skill should instruct Claude to use `browser_snapshot` as a diagnostic tool when selectors fail

---

## Important Notes for the Implementing Engineer

### Playwright MCP Tool Usage Pattern

The skill does NOT call Playwright directly. It instructs Claude to use MCP tools like:
- `mcp__plugin_playwright_playwright__browser_navigate` — go to URL
- `mcp__plugin_playwright_playwright__browser_snapshot` — get page accessibility tree (preferred for finding elements)
- `mcp__plugin_playwright_playwright__browser_fill_form` — fill text inputs
- `mcp__plugin_playwright_playwright__browser_click` — click buttons/links
- `mcp__plugin_playwright_playwright__browser_press_key` — press Enter, etc.
- `mcp__plugin_playwright_playwright__browser_take_screenshot` — save images
- `mcp__plugin_playwright_playwright__browser_wait_for` — wait for elements

The SKILL.md tells Claude which tools to use and in what order. Claude then makes the actual MCP tool calls.

### Snapshot vs Screenshot

- `browser_snapshot` returns an **accessibility tree** (text-based DOM representation) — use this for finding elements and their `ref` attributes
- `browser_take_screenshot` captures a **visual image** — use this for saving the generated infographic

### The Skill Must Handle

1. **First-run authentication** — detect not-logged-in state, ask user to log in
2. **Prompt construction** — read source file, truncate, apply template
3. **Waiting for generation** — Gemini takes 30-120 seconds to generate images
4. **Image detection** — identify the generated infographic vs UI chrome
5. **Image saving** — screenshot the element to a file
6. **Cleanup** — start a new chat to avoid context pollution
7. **Error recovery** — take diagnostic snapshot if things go wrong

### Output Naming Convention

Default: `{source_filename}_infographic_gemini.png`
Example: `outlive_summary.md` → `outlive_summary_infographic_gemini.png`

User can override with explicit output path.

---

*Created: 2026-03-08*
*Last Updated: 2026-03-08*
