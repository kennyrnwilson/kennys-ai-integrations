# Kenny's AI Integrations

Claude Code plugin marketplace with professional skills for everyday development workflows.

## Installation

```bash
# Add the marketplace
/plugin marketplace add kennyrnwilson/kennys-ai-integrations

# Install a plugin
/plugin install mermaid-diagrams@kennys-ai-integrations
```

## Plugins

### `mermaid-diagrams` — Professional Dark-Mode Diagrams

Generate beautiful Mermaid diagrams optimised for dark-mode editors (VS Code, Obsidian).

```bash
/mermaid-diagrams:mermaid flowchart data pipeline from API to database with caching layer
/mermaid-diagrams:mermaid sequence user authentication flow with OAuth
/mermaid-diagrams:mermaid class handler hierarchy with factory pattern
```

Features:
- Consistent dark theme across all diagram types (flowchart, sequence, class, state, ER, gantt, pie, mindmap, gitgraph)
- Semantic colour-coded nodes (input/teal, core/blue, AI/purple, browser/amber, output/emerald)
- Deep navy subgraph backgrounds with subtle borders
- Design rules for readable, professional layouts

### `image-gen` — AI-Powered Image Generator

Generate images from text descriptions or files via browser automation. Supports both Google Gemini and ChatGPT, each with a base skill and a professional infographic wrapper.

#### Gemini

**`gemini-image`** — Base image generation via Gemini.

```bash
/image-gen:gemini-image "a dancing dog in a park"
/image-gen:gemini-image path/to/prompt.txt --output result.png
```

**`infographic-gemini`** — Professional infographic styling on top of `gemini-image`.

```bash
/image-gen:infographic-gemini "benefits of remote work"
/image-gen:infographic-gemini path/to/summary.md --style minimal
```

#### ChatGPT

**`chatgpt-image`** — Base image generation via ChatGPT (DALL-E).

```bash
/image-gen:chatgpt-image "a dancing dog in a park"
/image-gen:chatgpt-image path/to/prompt.txt --output result.png
```

**`infographic-chatgpt`** — Professional infographic styling on top of `chatgpt-image`.

```bash
/image-gen:infographic-chatgpt "benefits of remote work"
/image-gen:infographic-chatgpt path/to/summary.md --style minimal
```

#### Features

- Browser automation via Playwright MCP (no Python scripts needed)
- Persistent browser profile (log in once per provider, stays authenticated)
- Works with file paths or inline text descriptions
- Infographic skills add dark navy background, vibrant colours, professional layout
- Multiple style options (modern, minimal, abstract, illustrated, tech)

**First-run setup:** On first use of each provider, a browser window opens. Log into your account once — credentials persist for all future sessions.

### `notebooklm` — Google NotebookLM Automation

Create notebooks, upload sources, and generate outputs from Google NotebookLM via browser automation.

**`notebooklm-create`** — Create a notebook and upload source files/URLs.

```bash
/notebooklm:notebooklm-create "My Research" --sources paper.pdf notes.md https://example.com/article
```

**`notebooklm-generate`** — Generate outputs from an existing notebook.

```bash
/notebooklm:notebooklm-generate https://notebooklm.google.com/notebook/abc123 --type reports
/notebooklm:notebooklm-generate https://notebooklm.google.com/notebook/abc123 --type slide-deck --prompt "10 slides, executive audience"
/notebooklm:notebooklm-generate https://notebooklm.google.com/notebook/abc123 --type mind-map --output mindmap.md
```

Output types: `audio`, `slide-deck`, `video`, `mind-map`, `reports`, `flashcards`, `quiz`, `infographic`, `data-table`

Features:
- Create notebooks and upload local files (PDF, text, markdown) or URLs
- Generate slide decks, reports, mind maps, quizzes, flashcards, and more
- Custom instructions via `--prompt` to control output focus and style
- Persistent browser profile (log in to Google once, stays authenticated)

**First-run setup:** On first use, a browser window opens. Log into your Google account once — credentials persist for all future sessions.

### `ebook-processing` — AI-Enriched Book Library Builder

Process ebooks into organized, AI-enriched library folders with summaries, chapter breakdowns, infographics, critical reviews, and index pages. Entirely prompt-driven — no Python code required.

**`process-book`** — Run the full pipeline end-to-end.

```bash
/ebook-processing:process-book ~/Downloads/my-book.epub
/ebook-processing:process-book ~/electronic-books/designing-data-intensive-applications/
/ebook-processing:process-book ~/Downloads/my-book.epub --skip infographics,critical-review
```

**`download-acsm`** — Download and unlock ACSM files using Adobe Digital Editions.

```bash
/ebook-processing:download-acsm ~/Downloads/URLLink.acsm --output-dir ~/electronic-books/my-book/
```

**`convert-book`** — Convert ebook files (EPUB, PDF) into multiple formats using Calibre.

```bash
/ebook-processing:convert-book ~/Downloads/my-book.epub --output-dir ~/electronic-books/my-book/
```

**`summarize-book`** — Generate a comprehensive structured summary using Claude.

```bash
/ebook-processing:summarize-book ~/electronic-books/my-book/
```

**`chapter-summaries`** — Extract and summarize individual chapters.

```bash
/ebook-processing:chapter-summaries ~/electronic-books/my-book/
```

**`critical-review`** — Evidence-based critical review of key claims using web research.

```bash
/ebook-processing:critical-review ~/electronic-books/my-book/
```

**`book-infographics`** — Generate book-level infographics via ChatGPT and Gemini.

```bash
/ebook-processing:book-infographics ~/electronic-books/my-book/
```

**`chapter-infographics`** — Generate infographics for each chapter summary.

```bash
/ebook-processing:chapter-infographics ~/electronic-books/my-book/
```

**`book-index`** — Generate README index page, action items, and metadata.

```bash
/ebook-processing:book-index ~/electronic-books/my-book/
```

Features:
- Full pipeline or individual stage execution
- Built-in resume logic — re-run safely without duplicating work
- Rich summary templates with executive summaries, frameworks, and action items
- Cross-plugin integration with `image-gen` for infographics
- PDF generation via pandoc/weasyprint
- `--force` flag to regenerate, `--skip` to skip stages

**Prerequisites:** Calibre (for book conversion), pandoc/weasyprint (for PDF output), `image-gen` plugin (for infographics).

## Marketplace Structure

```
kennys-ai-integrations/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog
├── plugins/
│   ├── mermaid-diagrams/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # Plugin manifest
│   │   └── skills/
│   │       └── mermaid/
│   │           └── SKILL.md      # Mermaid diagram skill
│   └── image-gen/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── .mcp.json             # Playwright MCP config
│       └── skills/
│           ├── gemini-image/
│           │   └── SKILL.md      # Base Gemini image generation
│           ├── infographic-gemini/
│           │   └── SKILL.md      # Gemini infographic styling
│           ├── chatgpt-image/
│           │   └── SKILL.md      # Base ChatGPT image generation
│           └── infographic-chatgpt/
│               └── SKILL.md      # ChatGPT infographic styling
│   ├── notebooklm/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # Plugin manifest
│   │   ├── .mcp.json             # Playwright MCP config
│   │   └── skills/
│   │       ├── notebooklm-create/
│   │       │   └── SKILL.md      # Create notebook + upload sources
│   │       └── notebooklm-generate/
│   │           └── SKILL.md      # Generate outputs (briefing, FAQ, etc.)
│   └── ebook-processing/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       └── skills/
│           ├── process-book/
│           │   └── SKILL.md      # Full pipeline orchestrator
│           ├── download-acsm/
│           │   └── SKILL.md      # ACSM download via Adobe Digital Editions
│           ├── convert-book/
│           │   └── SKILL.md      # Calibre format conversion
│           ├── summarize-book/
│           │   └── SKILL.md      # Comprehensive book summary
│           ├── chapter-summaries/
│           │   └── SKILL.md      # Per-chapter summaries
│           ├── critical-review/
│           │   └── SKILL.md      # Evidence-based claim review
│           ├── book-infographics/
│           │   └── SKILL.md      # Book-level infographics
│           ├── chapter-infographics/
│           │   └── SKILL.md      # Per-chapter infographics
│           └── book-index/
│               └── SKILL.md      # README index + metadata
├── docs/
│   └── README.md                 # Documentation index
└── README.md                     # This file
```

## Colour Palette Reference

| Class | Fill | Stroke | Use |
|-------|------|--------|-----|
| `input` | `#1a4a4a` | `#4ead8a` | Input data, sources |
| `primary` | `#1a3a5c` | `#4a90d9` | Core processing |
| `ai` | `#2d1f4e` | `#9d6dd9` | AI/ML, API calls |
| `browser` | `#3d2d1a` | `#d4944a` | Browser automation |
| `output` | `#1a3d2a` | `#4ead8a` | Results, metadata |
| `danger` | `#4a1a1a` | `#d94a4a` | Errors, destructive |
| `neutral` | `#2a2a3a` | `#6b7280` | Utility, secondary |

## License

MIT License
