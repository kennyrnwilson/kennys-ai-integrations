# Documentation

← [Back to Project Root](../README.md)

## Plugins

- [Mermaid Diagram Skill](../plugins/mermaid-diagrams/skills/mermaid/SKILL.md) — Professional dark-mode Mermaid diagram generator

## Adding New Plugins

1. Create a directory under `plugins/` with the plugin name
2. Add `.claude-plugin/plugin.json` with name, description, version
3. Add skills under `plugins/<name>/skills/<skill-name>/SKILL.md`
4. Register the plugin in `.claude-plugin/marketplace.json`
5. Update this index

---

*Last Updated: 2026-03-08*
