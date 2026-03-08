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

### `infographics` — AI-Powered Infographic Generator

Generate infographic images from text summaries using AI chat interfaces via browser automation.

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
│   └── infographics/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── .mcp.json             # Playwright MCP config
│       └── skills/
│           └── infographic-gemini/
│               └── SKILL.md      # Gemini infographic skill
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
