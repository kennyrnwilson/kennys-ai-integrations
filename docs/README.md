# Documentation

← [Back to Project Root](../README.md)

## Plugins

- **[image-gen](../plugins/image-gen/)** — Generate images and infographics through the Gemini image API
  - [generate-image](../plugins/image-gen/skills/generate-image/SKILL.md) — Any image, from inline text or a source file
  - [infographic](../plugins/image-gen/skills/infographic/SKILL.md) — Dark-themed infographic from text or a file

- **[documentation-conventions](../plugins/documentation-conventions/)** — Markdown authoring conventions and Mermaid diagram theming
  - [markdown-conventions](../plugins/documentation-conventions/skills/markdown-conventions/SKILL.md) — File structure, bidirectional parent/child links, backlinks, relative paths, kebab-case names, and the Related/Tags/dates footer
  - [mermaid-conventions](../plugins/documentation-conventions/skills/mermaid-conventions/SKILL.md) — Semantic colour palette and dark-theme init blocks for Mermaid diagrams

- **[ebook-processing](../plugins/ebook-processing/)** — AI-enriched book library builder
  - [process-book](../plugins/ebook-processing/skills/process-book/SKILL.md) — Full pipeline orchestrator
  - [download-acsm](../plugins/ebook-processing/skills/download-acsm/SKILL.md) — ACSM download via Adobe Digital Editions
  - [convert-book](../plugins/ebook-processing/skills/convert-book/SKILL.md) — Calibre format conversion
  - [summarize-book](../plugins/ebook-processing/skills/summarize-book/SKILL.md) — Comprehensive book summary
  - [chapter-summaries](../plugins/ebook-processing/skills/chapter-summaries/SKILL.md) — Per-chapter summaries
  - [critical-review](../plugins/ebook-processing/skills/critical-review/SKILL.md) — Evidence-based claim review
  - [book-infographics](../plugins/ebook-processing/skills/book-infographics/SKILL.md) — Book-level infographics
  - [chapter-infographics](../plugins/ebook-processing/skills/chapter-infographics/SKILL.md) — Per-chapter infographics
  - [book-index](../plugins/ebook-processing/skills/book-index/SKILL.md) — README index + metadata

- **[operating-context](../plugins/operating-context/)** — Standing context in every session, via a `SessionStart` hook
  - No skills. `standing-instructions.md` (the global rules) and `operating-manual.md` load, in that order; `scripts/print-manual.sh` prints them

## Plans

- [Marketplace Remediation Plan](plans/2026-07-29-marketplace-remediation.md) — the current plan governing this repo's structure
- [Execution Handoff](plans/2026-07-29-execution-handoff.md)
- [Archived Design Documents](plans/archive/) — superseded pre-implementation designs, kept for history only

## Adding New Plugins

1. Create a directory under `plugins/` with the plugin name
2. Add `.claude-plugin/plugin.json` with name, description, version
3. Add skills under `plugins/<name>/skills/<skill-name>/SKILL.md`
4. Register the plugin in `.claude-plugin/marketplace.json`
5. Update this index

---

*Last Updated: 2026-09-13*
