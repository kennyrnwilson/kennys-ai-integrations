# Kenny's AI Integrations

Claude Code plugin marketplace with professional skills for everyday development workflows.

## Installation

```bash
# Add the marketplace
/plugin marketplace add kennyrnwilson/kennys-ai-integrations

# Install a plugin
/plugin install image-gen@kennys-ai-integrations
```

## Plugins

### `image-gen` — AI Image and Infographic Generator

Generate images and infographics through the Gemini image API. A direct API
call — no browser, no login, no rate-limit pacing.

| Skill | Purpose |
|---|---|
| `generate-image` | Any image, from inline text or a source file |
| `infographic` | Dark-themed infographic from text or a file |

```bash
/image-gen:generate-image "a dancing dog in a park" --aspect-ratio 16:9
/image-gen:infographic path/to/summary.md --style modern
```

### `documentation-conventions` — Documentation Authoring Conventions

Kenny's conventions for authoring documentation: markdown file structure and
Mermaid diagram theming.

| Skill | Purpose |
|---|---|
| `markdown-conventions` | File structure, bidirectional parent/child links, backlinks, relative paths, kebab-case names, and the Related/Tags/dates footer |
| `mermaid-conventions` | When to theme a diagram at all, the semantic colour palette, and the dark-theme init blocks |

```bash
/documentation-conventions:markdown-conventions
```

### `ebook-processing` — AI-Enriched Book Library Builder

Process ebooks into organised, AI-enriched library folders with summaries,
chapter breakdowns, infographics, critical reviews, and index pages. Entirely
prompt-driven — no Python code required.

Set `EBOOK_LIBRARY_PATH` to your book library root to use short book names
instead of full paths:

```bash
export EBOOK_LIBRARY_PATH=/Users/kenne/code/book-library
```

With this set, all skills accept bare book names — `designing-data-intensive-applications`
resolves to `/Users/kenne/code/book-library/designing-data-intensive-applications/`. Full
paths always override.

| Skill | Purpose |
|---|---|
| `process-book` | Run the full pipeline end-to-end |
| `download-acsm` | Download and unlock ACSM files using Adobe Digital Editions |
| `convert-book` | Convert ebook files (EPUB, PDF) into multiple formats using Calibre |
| `summarize-book` | Generate a comprehensive structured summary using Claude |
| `chapter-summaries` | Extract and summarise individual chapters |
| `critical-review` | Evidence-based critical review of key claims using web research |
| `book-infographics` | Book-level infographics via the `image-gen` plugin |
| `chapter-infographics` | Per-chapter infographics via the `image-gen` plugin |
| `book-index` | Generate README index page, action items, and metadata |

```bash
/ebook-processing:process-book ~/Downloads/my-book.epub
/ebook-processing:process-book designing-data-intensive-applications --skip infographics,critical-review
```

### `operating-context` — Standing Context in Every Session

One `SessionStart` hook that prints a bundled markdown file, which Claude Code
folds into the session as context. No skills, no commands to run, and nothing to
paste: install it and every session — terminal, cloud, or desktop — starts already
knowing what it needs to.

| Part | Purpose |
|---|---|
| `operating-manual.md` | The document that loads. Replace it with your own |
| `hooks/hooks.json` | Registers the `SessionStart` hook |
| `scripts/print-manual.sh` | Prints the manual. Exits cleanly if the file is missing, so a session is never blocked |

```bash
/plugin install operating-context@kennys-ai-integrations
```

## Requirements

- `uv` on PATH.
- `GEMINI_API_KEY` set on a funded Gemini API billing account, for `image-gen`
  (directly, and indirectly for `ebook-processing`'s infographic stages).
- Calibre CLI (`ebook-convert`) and WeasyPrint, for `ebook-processing`'s
  conversion and PDF-rendering stages.
- `pandoc` is not installed on this machine and is not required. Several
  `ebook-processing` skills reference it as a preferred PDF-conversion route
  but fall back to WeasyPrint, or skip PDF generation entirely, when it is
  absent — no new `pandoc` dependency should be introduced.

No MCP servers and no external plugins are required — every plugin here is
self-contained, calling an API or a local CLI directly.

## History

Earlier versions of this marketplace included a `mermaid-diagrams` plugin, a
`notebooklm` plugin, a `dev-conventions` plugin, and browser-automation-based
image skills (`gemini-image`, `chatgpt-image`, `infographic-gemini`,
`infographic-chatgpt`). All were retired as part of a July 2026 remediation —
Mermaid conventions merged into `documentation-conventions`, and image
generation moved entirely to the Gemini API. See
[`docs/plans/2026-07-29-marketplace-remediation.md`](docs/plans/2026-07-29-marketplace-remediation.md)
for the full rationale, and [`docs/plans/archive/`](docs/plans/archive/) for
the superseded pre-implementation designs.

## Marketplace Structure

```
kennys-ai-integrations/
├── .claude-plugin/
│   └── marketplace.json
├── docs/
│   ├── README.md
│   └── plans/
│       ├── archive/
│       │   ├── 2026-03-08-infographics-plugin-design.md
│       │   ├── 2026-03-08-notebooklm-plugin-design.md
│       │   ├── 2026-03-09-ebook-processing-plugin-design.md
│       │   ├── 2026-03-09-ebook-processing-plugin-plan.md
│       │   └── README.md
│       ├── 2026-07-29-execution-handoff.md
│       └── 2026-07-29-marketplace-remediation.md
├── plugins/
│   ├── documentation-conventions/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── markdown-conventions/
│   │   │   │   └── SKILL.md
│   │   │   └── mermaid-conventions/
│   │   │       └── SKILL.md
│   │   └── README.md
│   ├── ebook-processing/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── scripts/
│   │   │   └── convert_book.sh
│   │   └── skills/
│   │       ├── book-index/
│   │       │   └── SKILL.md
│   │       ├── book-infographics/
│   │       │   └── SKILL.md
│   │       ├── chapter-infographics/
│   │       │   └── SKILL.md
│   │       ├── chapter-summaries/
│   │       │   └── SKILL.md
│   │       ├── convert-book/
│   │       │   └── SKILL.md
│   │       ├── critical-review/
│   │       │   └── SKILL.md
│   │       ├── download-acsm/
│   │       │   └── SKILL.md
│   │       ├── process-book/
│   │       │   └── SKILL.md
│   │       └── summarize-book/
│   │           └── SKILL.md
│   ├── operating-context/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── hooks/
│   │   │   └── hooks.json
│   │   ├── scripts/
│   │   │   ├── print-manual.sh
│   │   │   └── test_print_manual.py
│   │   └── operating-manual.md
│   └── image-gen/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── scripts/
│       │   ├── generate_image.py
│       │   └── test_generate_image.py
│       ├── skills/
│       │   ├── generate-image/
│       │   │   └── SKILL.md
│       │   └── infographic/
│       │       └── SKILL.md
│       └── README.md
├── tools/
│   ├── src/
│   │   └── marketplace_validator/
│   │       ├── __init__.py
│   │       ├── cli.py
│   │       ├── manifest.py
│   │       ├── mcp.py
│   │       ├── models.py
│   │       └── skills.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_manifest.py
│   │   ├── test_mcp.py
│   │   └── test_skills.py
│   ├── .gitignore
│   ├── pyproject.toml
│   └── uv.lock
└── README.md                 # This file
```

## License

MIT License
