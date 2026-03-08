# Kenny's AI Integrations

Claude Code plugin collection with professional skills for everyday development workflows.

## Installation

```bash
claude plugin install /path/to/kennys-ai-integrations
# or from GitHub:
claude plugin install kennyrnwilson/kennys-ai-integrations
```

## Skills

### `/mermaid` — Professional Dark-Mode Diagrams

Generate beautiful Mermaid diagrams optimised for dark-mode editors (VS Code, Obsidian).

```bash
/mermaid flowchart data pipeline from API to database with caching layer
/mermaid sequence user authentication flow with OAuth
/mermaid class handler hierarchy with factory pattern
```

Features:
- Consistent dark theme across all diagram types (flowchart, sequence, class, state, ER, gantt, pie, mindmap, gitgraph)
- Semantic colour-coded nodes (input/teal, core/blue, AI/purple, browser/amber, output/emerald)
- Deep navy subgraph backgrounds with subtle borders
- Design rules for readable, professional layouts

## Plugin Structure

```
kennys-ai-integrations/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/
│   └── mermaid/
│       └── SKILL.md          # Mermaid diagram skill
├── docs/
│   └── README.md             # Documentation index
└── README.md                 # This file
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
