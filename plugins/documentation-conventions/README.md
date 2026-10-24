# documentation-conventions

← [Back to Marketplace](../../README.md)

Kenny's conventions for authoring documentation.

## Skills

| Skill | Covers |
|---|---|
| `communicate-clearly` | The writing standard: the house style, which style applies (procedure rules or stand-alone prose), and a guide per kind of document in `references/` |
| `structure` | `/structure`: asks what kind of document it is, loads that kind's guide, interviews for the reader, goal and format, and proposes an outline |
| `review-draft` | `/review-draft`: reviews a draft against the `review-a-draft` checklist and new-joiner test, and reports findings by harm to the reader. Not `/review`, which is Claude Code's code review |
| `markdown-conventions` | File structure, bidirectional parent/child links, backlinks, relative paths, kebab-case names, the Related/Tags/dates footer, and the Astro variant used by the portal hub |
| `mermaid-conventions` | When to theme a diagram at all, the semantic colour palette, and the dark-theme init blocks |

## Scope

These are authoring conventions for documents. Python project scaffolding is
**not** here and is not in this marketplace at all — use `uv init --lib`, or
[scientific-python/cookie](https://github.com/scientific-python/cookie) for a
full package template.

## History

`communicate-clearly` (1.2.0) holds the writing standard that used to sit in
`markdown-conventions` ("Which prose style applies"), and replaces the personal
`ste-writing` skill and the `STE-100` output style. ASD-STE100 was dropped for eight
procedure rules that need no controlled dictionary. 1.3.0 adds four guides:
`keep-notes`, `write-a-system-explanation`, `review-a-draft` and `write-with-ai`.
1.4.0 adds the first two task skills, `structure` and `review-draft`. Each loads
`communicate-clearly` and follows one guide, and carries no rules of its own.

`mermaid-conventions` replaces the retired `mermaid-diagrams` plugin. Beyond
the move, it fixes a defect: the original mandated a hardcoded dark theme on
every diagram, which makes diagrams unreadable in GitHub's light view. Theming
is now opt-in with guidance on when it applies.
