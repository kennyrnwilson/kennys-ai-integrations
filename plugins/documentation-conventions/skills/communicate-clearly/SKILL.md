---
name: communicate-clearly
description: Kenny's writing standard — the house style for anything finished that someone else reads, and the rules for procedures. Use when writing, rewriting or reviewing documentation, notes, explanations, runbooks, setup guides, skills or AGENTS.md; when learning a subject or starting a /teach workspace; and when asked for STE or Simplified Technical English.
---

# Communicate clearly

The one writing standard for Kenny's repos, notes and documents, for a person and an
AI alike. It applies to everything finished that someone else reads: a person, a
visitor to the portal, or an AI reading through the MCP. Fleeting notes are raw
capture and are exempt.

File form (backlinks, filenames, the footer) is the `markdown-conventions` skill;
Mermaid theming is `mermaid-conventions`. Which repo a page belongs in is the
personal-portal documentation standard.

The reasons behind these rules are permanent notes in knowledge-library, in the
[Knowledge and Communication hub](https://github.com/kennyrnwilson/knowledge-library/blob/main/03-permanent-notes/productivity/knowledge-and-communication/README.md).

This is version 1.7.0, from the documentation-conventions plugin in
kennys-ai-integrations. On claude.ai, the skill is an uploaded copy: when asked,
say which version this is.

## House style

The short form. [`references/write-in-house-style.md`](references/write-in-house-style.md)
gives each rule's reason and a good and a bad example.

1. **UK spelling** in prose; US spelling stays in code identifiers.
2. **Plain English.** Use the common word: "use", not "utilise"; "start", not
   "initiate".
3. **Lead with the point.** The first sentence of a page, section or paragraph says
   what it is for.
4. **Name the actor and the action.** "The deploy runner builds the site", not "the
   build of the site is performed".
5. **One thing, one name,** in the prose, the tables and the figures. Across the
   system, use the names in the
   [glossary](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/glossary.md).
6. **Earn every claim.** State a fact before a sentence relies on it. Mark a
   judgement, an uncertainty or something you did not check as such.
7. **Say it plainly.** Write captions, headings and summaries as plain statements
   that a reader seeing them cold can understand.
8. **Simplify the explanation, never the facts.** Numbers, commands, paths and code
   stay exact.

## Which style applies

Decide by what the document is for, not by which repo it sits in.

| | **Procedures** | **Explanations** |
|---|---|---|
| Examples | setup guides, runbooks, deploy steps, guidance protocols, skills | permanent notes, architecture and design docs, plans |
| Reader's job | follow it, possibly at a bad moment | understand something from cold |
| Style | the eight procedure rules | stand-alone prose |
| Sentences | one instruction each, short | as long as the idea needs |

**Procedures:** load
[`references/write-a-procedure.md`](references/write-a-procedure.md) and follow
its eight rules.

**Explanations:** write them to stand on their own.

- Assume a capable reader with no background in this particular thing, and no
  context carried over from the conversation that produced the text.
- Use the real term, and define it once, the first time.
- Say why it matters before how it works.
- Give the reasoning, not only the conclusion: show what goes wrong if it were done
  the other way.
- Say when something is contested, uncertain or a judgement. Distinguish what a
  specification permits from what an implementation does, and cite which one you
  checked.

A document can hold both: an explanation with a procedure inside it follows the
procedure rules for the steps and stand-alone prose for the rest.

## Guides

Load the guide that matches the job before writing.

| Job | Guide |
|---|---|
| Any finished prose, when a rule above needs its reason or an example | [`references/write-in-house-style.md`](references/write-in-house-style.md) |
| A procedure: a runbook, setup guide, protocol or skill | [`references/write-a-procedure.md`](references/write-a-procedure.md) |
| A note: capturing, filing, a literature or permanent note, guidance, a quote | [`references/keep-notes.md`](references/keep-notes.md) |
| Software documentation: an architecture page, design doc, app profile, README or plan | [`references/write-a-system-explanation.md`](references/write-a-system-explanation.md) |
| Reviewing a draft, yours or an AI's | [`references/review-a-draft.md`](references/review-a-draft.md) |
| Deciding who writes: coach, co-write or draft mode, and briefing an AI | [`references/write-with-ai.md`](references/write-with-ai.md) |
| A talk: the message, the arc, slides, speaker notes and the Marp deck | [`references/build-a-talk.md`](references/build-a-talk.md) |
| Learning a subject: routing the material, a `/teach` workspace, review, promotion | [`references/learn-a-subject.md`](references/learn-a-subject.md) |
| An `AGENTS.md`, a skill, or another document an agent reads | the `writing-for-agents` skill, where installed, plus the house style |
