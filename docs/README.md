# Documentation

← [Back to Project Root](../README.md)

## Plugins

- **[mermaid-diagrams](../plugins/mermaid-diagrams/)** — Professional dark-mode Mermaid diagram generator
  - [mermaid](../plugins/mermaid-diagrams/skills/mermaid/SKILL.md) — Generate Mermaid diagrams

- **[image-gen](../plugins/image-gen/)** — AI-powered image generation via browser automation
  - [gemini-image](../plugins/image-gen/skills/gemini-image/SKILL.md) — Base Gemini image generation
  - [infographic-gemini](../plugins/image-gen/skills/infographic-gemini/SKILL.md) — Gemini infographic styling
  - [chatgpt-image](../plugins/image-gen/skills/chatgpt-image/SKILL.md) — Base ChatGPT image generation
  - [infographic-chatgpt](../plugins/image-gen/skills/infographic-chatgpt/SKILL.md) — ChatGPT infographic styling

- **[notebooklm](../plugins/notebooklm/)** — Google NotebookLM automation
  - [notebooklm-create](../plugins/notebooklm/skills/notebooklm-create/SKILL.md) — Create notebook + upload sources
  - [notebooklm-generate](../plugins/notebooklm/skills/notebooklm-generate/SKILL.md) — Generate outputs (reports, slides, etc.)

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

## Design Documents

- [Ebook Processing Plugin Design](plans/2026-03-09-ebook-processing-plugin-design.md)
- [Ebook Processing Plugin Plan](plans/2026-03-09-ebook-processing-plugin-plan.md)
- [NotebookLM Plugin Design](plans/2026-03-08-notebooklm-plugin-design.md)

## Adding New Plugins

1. Create a directory under `plugins/` with the plugin name
2. Add `.claude-plugin/plugin.json` with name, description, version
3. Add skills under `plugins/<name>/skills/<skill-name>/SKILL.md`
4. Register the plugin in `.claude-plugin/marketplace.json`
5. Update this index

---

*Last Updated: 2026-03-14*
