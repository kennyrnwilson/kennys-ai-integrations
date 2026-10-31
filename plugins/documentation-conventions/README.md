# documentation-conventions

← [Back to Marketplace](../../README.md)

Kenny's conventions for authoring documentation.

## Skills

| Skill | Covers |
|---|---|
| `communicate-clearly` | The writing standard: the house style, which style applies (procedure rules or stand-alone prose), and a guide per kind of document in `references/` |
| `structure` | `/structure`: asks what kind of document it is, loads that kind's guide, interviews for the reader, goal and format, and proposes an outline |
| `draft` | `/draft`: writes a piece with Kenny in coach, co-write or draft mode, by `write-with-ai`. In coach mode it writes no prose of the piece |
| `review-draft` | `/review-draft`: reviews a draft against the `review-a-draft` checklist and new-joiner test, and reports findings by harm to the reader. Not `/review`, which is Claude Code's code review |
| `new-joiner` | `/new-joiner`: runs only the new-joiner test from `review-a-draft`, and marks every point where a capable newcomer would stop |
| `talk` | `/talk`: turns a document into a talk by `build-a-talk` — one message, an arc, slides as visuals, speaker notes — as a Marp deck beside the document |
| `process-inbox` | `/process-inbox`: proposes a fate for each fleeting note (develop, merge or archive) by `keep-notes`. The AI proposes; Kenny writes |
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
1.5.0 adds `draft`, `new-joiner` and `process-inbox`. `/draft` does not wrap Matt
Pocock's `writing-*` skills: on 2026-10-24 they were still in his `in-progress/`
folder.
1.6.0 adds the `build-a-talk` guide and the `talk` skill. Marp is the slide tool:
it exports one self-contained HTML file that the portal publishes as it is.
1.6.1 states the version in `communicate-clearly`'s `SKILL.md`, for the claude.ai
copy. 1.6.2 cites *Resonate*, which book-library now holds, in `build-a-talk`.
1.6.3 makes coach mode ask Kenny to confirm before it writes any of a learning
piece, such as a permanent note, when he asks it to. 1.6.4 has `/talk` list every
slide with its title, its visual and its speaker notes, even in an outline.
1.7.0 adds the `learn-a-subject` guide, from the personal-portal Learning plan: how
to route material, where a `/teach` workspace lives, review on a Todoist schedule,
promotion, graduation from `explore`, and what Kenny expects of the teacher. It is
a guide in `communicate-clearly`, not a skill of its own, so it reaches claude.ai in
the existing ZIP.
1.7.1 links the skills and the documentation standard named in `communicate-clearly`.
1.7.2 has `learn-a-subject` write Recall model answers as checkable key points
and load `recall.js`, so learning-app can mark a typed answer.
1.7.3 adds `communicate-clearly/scripts/lesson-diagrams/`: the engine that draws
lesson diagrams as inline SVG and records each one's boxes, nesting and arrows as
the answer for a Draw it exercise.

## claude.ai

claude.ai does not install plugins, so `communicate-clearly` is uploaded to the
account by hand. The task skills are not uploaded: the standard's router covers
the same jobs when they are asked for in plain words. On each push that changes
this plugin, the `communicate-clearly ZIP` workflow checks that `SKILL.md` states
the version in `plugin.json`, and builds `communicate-clearly-<version>.zip`. On a
new version it publishes the ZIP as the release `communicate-clearly-v<version>`.
The upload steps are in mac-homedir `docs/claude-ai-skills.md`.

`mermaid-conventions` replaces the retired `mermaid-diagrams` plugin. Beyond
the move, it fixes a defect: the original mandated a hardcoded dark theme on
every diagram, which makes diagrams unreadable in GitHub's light view. Theming
is now opt-in with guidance on when it applies.
