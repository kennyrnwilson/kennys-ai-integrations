---
name: draft
description: Write a document with Kenny in one of three modes — coach (Kenny writes, the AI asks and critiques), co-write (Kenny owns the outline and key sentences, the AI drafts the rest) or draft (the AI writes from a brief). Follows write-with-ai and the house style in communicate-clearly. Use when the user says /draft, asks to write, draft or flesh out a document, note, section or runbook, or asks for help writing from an outline.
argument-hint: "[coach|co-write|draft] [topic, outline or path]"
---

# Draft

Write a piece, or help Kenny write it, in the mode the piece needs. This skill has
no rules of its own: the modes are in `references/write-with-ai.md` and the
standard is in the `communicate-clearly` skill. Plan first with `/structure`;
check the result with `/review-draft`.

## Steps

1. Load the `communicate-clearly` skill.
2. Load `references/write-with-ai.md` from it.
3. Find the mode. If the user named one, use it. If not, ask whether the piece is
   for learning or for output, and recommend a mode:
   - learning, such as a permanent note or the capstone: coach;
   - a team document: co-write;
   - reference material or a slide scaffold: draft.
4. Get the outline. If none exists, run `/structure` first, or ask the user for
   one.
5. Load the guide for the kind of piece:
   - software documentation: `write-a-system-explanation.md`;
   - a procedure: `write-a-procedure.md`;
   - a note: `keep-notes.md`;
   - a talk: `build-a-talk.md`.
6. In draft mode, collect the brief. Check it against "Brief the AI" in
   `write-with-ai.md`, and ask for each missing item.
7. Do the mode's steps in `write-with-ai.md`:
   - **Coach:** ask Kenny to write first. Do not write a sentence of the piece.
     When he is stuck, offer a scaffold: a sentence stem, a paragraph frame or a
     list of points to cover. If he asks you to write it, follow "When Kenny
     asks the AI to write it" before switching mode.
   - **Co-write:** wait for Kenny's key sentences, then draft one section at a
     time from the outline. Stop after each section for his rewrite.
   - **Draft:** write the whole draft from the brief and its sources only.
8. Check each fact you write against its source. Mark a claim you could not check
   as **Unverified**.
9. When the draft or section is done, run `/review-draft` on it, unless the user
   says not to.

## Output

- **Coach:** questions, critiques and scaffolds in the conversation. No prose of
  the piece.
- **Co-write and draft:** the text, written to the file the outline names. If no
  file is named, show the text in the conversation and ask where it goes.

Never change a sentence Kenny marked as his.
