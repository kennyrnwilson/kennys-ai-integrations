# Write a system explanation

← [Back to communicate-clearly](../SKILL.md)

How to write documentation that explains a software system: an architecture page,
a design document, an app profile, a repo README or a plan. The house style
applies, and the prose follows the explanation rules in `SKILL.md`. Steps inside
the page, such as a setup sequence, follow [`write-a-procedure.md`](write-a-procedure.md).

The reasons behind these rules are in the
[documentation-systems note](https://github.com/kennyrnwilson/knowledge-library/blob/main/03-permanent-notes/productivity/knowledge-and-communication/documentation-systems.md).

## Before you write

1. **Name the reader and their goal.** "Kenny, a year from now, debugging the
   deploy" is a reader. "Anyone" is not.
2. **Name the kind of page.** Diátaxis separates four kinds, and a page that mixes
   them serves no reader well:

   | Kind | The reader wants to | Example here |
   |---|---|---|
   | Explanation | understand why it is built this way | `mcp-topology.md` |
   | How-to | do a task they already understand | `ingress-vm-setup-guide.md` |
   | Reference | look up a fact | `glossary.md`, `fleet.tsv` |
   | Tutorial | learn by doing, from nothing | a `/teach` lesson |

3. **Decide where the page goes.** Apply the three-way test in the
   [documentation standard](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/documentation-standard.md):
   a fact about the whole fleet goes in the personal-portal hub; a fact about one
   repo goes in that repo; a fact about how a machine is set up goes in
   mac-homedir. A concept, true for anyone, goes in knowledge-library.
4. **Search for an existing page.** Extend it, or link to it, before you create
   another.

## The shape of the page

### An architecture page or app profile

1. **What it is and why it exists,** in the first paragraph.
2. **How it fits the system:** what calls it, what it calls, and where it runs.
3. **One diagram** for the structure. Choose the C4 level the reader needs: the
   system in its context, its containers (processes and stores), or the
   components inside one container. Do not mix levels in one diagram.
4. **The parts,** each with what it does and where its code or config lives.
5. **What goes wrong,** and where to look when it does.

### A design document or plan

Use at least these headings, after Reilly:

1. **Context:** the problem, and what is true today.
2. **Goals and non-goals.**
3. **The design.**
4. **Security and risks.**
5. **Alternatives considered,** each with why it lost.
6. **Phases,** for a plan, and **open questions.**

A plan is deleted when its work lands. Before that, move every fact that will
outlast it into the page it belongs on.

## Rules

- **Lead with the point** of each section, then the detail.
- **Wrong is better than vague.** A precise statement that turns out wrong gets
  corrected. A vague one survives, and misleads for longer.
- **Spend words to avoid ambiguity.** Never leave a bare "this" or "that": say this
  what.
- **Use the glossary's names.** "The Mac Mini", never "the server"; "the MCP
  portal" in full. See the
  [glossary](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/glossary.md).
- **Link, do not duplicate.** Each fact has one home. Every other page links to it.
  A copied fact goes stale in one of its places.
- **Say what you checked, and when.** Distinguish what a specification permits from
  what the implementation does, and name which one you checked: "Checked
  2026-10-21 against Codex CLI 0.157.1."
- **Give the reasoning,** not only the conclusion: what would go wrong if it were
  done the other way.

## Diagrams

- Follow the `mermaid-conventions` skill for theme and palette.
- Give every diagram an `accTitle` and an `accDescr`. The description says in
  prose what the diagram shows, for a reader who cannot see it and for an AI.
- One diagram answers one question. Two questions get two diagrams.
- Write the caption as a plain statement of what the diagram shows.
- A diagram is a summary of the prose, never the only place a fact appears.

## Keep it true

- Change the documentation in the same commit as the code it describes.
- When you find a page out of date, fix it, or mark the wrong statement and say
  what is true.
- Read the page as a newcomer would: a reader with the skills but none of the
  history. Every point where that reader gets lost needs a definition, a link or a
  sentence. `review-a-draft.md` has the check.

## Worked examples

- The personal-portal
  [documentation standard](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/documentation-standard.md):
  the four surfaces, the three-way test, and the templates for a repo README, a
  repo agent guide and an app profile.
- [`mcp-topology.md`](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/mcp-topology.md):
  an explanation with a context diagram and a sequence diagram.

## Sources

- [Diátaxis](https://diataxis.fr): the four kinds of documentation.
- [The C4 model](https://c4model.com): levels of architecture diagram.
- Reilly, *The Staff Engineer's Path*: the minimum headings of a design document;
  wrong is better than vague; no bare "this".
- Fournier, *The Manager's Path*: onboarding documents that each new joiner
  corrects, which keeps a system explanation true.
