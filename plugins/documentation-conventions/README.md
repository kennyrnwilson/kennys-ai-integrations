# documentation-conventions

← [Back to Marketplace](../../README.md)

Kenny's conventions for authoring documentation.

## Skills

| Skill | Covers |
|---|---|
| `markdown-conventions` | File structure, bidirectional parent/child links, backlinks, relative paths, kebab-case names, the Related/Tags/dates footer, and the Astro variant used by the portal hub |
| `mermaid-conventions` | When to theme a diagram at all, the semantic colour palette, and the dark-theme init blocks |

## Scope

These are authoring conventions for documents. Python project scaffolding is
**not** here and is not in this marketplace at all — use `uv init --lib`, or
[scientific-python/cookie](https://github.com/scientific-python/cookie) for a
full package template.

## History

`mermaid-conventions` replaces the retired `mermaid-diagrams` plugin. Beyond
the move, it fixes a defect: the original mandated a hardcoded dark theme on
every diagram, which makes diagrams unreadable in GitHub's light view. Theming
is now opt-in with guidance on when it applies.
