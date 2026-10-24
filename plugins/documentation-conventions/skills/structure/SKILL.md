---
name: structure
description: Plan a document before writing it — ask what kind it is, load that kind's guide from communicate-clearly, interview for the reader, their goal and the format, then propose an outline. Use when the user says /structure, asks to outline or plan a doc, note, procedure or talk, or wants help deciding how to organise something before drafting.
argument-hint: "[topic or path to notes]"
---

# Structure

Turn a topic into an outline that a draft can follow. This skill has no rules of its
own: the standard and the guides are in the `communicate-clearly` skill. It does not
write the draft; that is `/draft`, or the user.

## Steps

1. Load the `communicate-clearly` skill.
2. Read what the user gave you: the topic, and any notes, files or sources it names.
   If it names a book in book-library, get its summary or action items through the
   book MCP tools, where available, so the outline can cite chapters.
3. Ask what kind of document it is. Offer these kinds, with your recommendation:

   | Kind | Guide to load from `communicate-clearly/references/` |
   |---|---|
   | Software documentation: an architecture page, design doc, app profile, README or plan | `write-a-system-explanation.md` |
   | A procedure: a runbook, setup guide, protocol or skill | `write-a-procedure.md` |
   | A note: a permanent note, literature note or guidance | `keep-notes.md` |
   | A talk | `build-a-talk.md` |

4. Load the guide for that kind.
5. If no guide exists for the kind, tell the user so. Name the kind as a candidate
   for a new guide. Continue with the house style and the explanation or procedure
   rules in `SKILL.md`.
6. Interview the user. Use the round format of the `grilling` skill, where it is
   installed: number each question and give your recommended answer. Settle these
   decisions, in this order:
   1. The reader: a named person or role, and what they already know.
   2. The reader's goal: what they can do or understand after reading.
   3. For software documentation, the Diátaxis kind: explanation, how-to, reference
      or tutorial. One page is one kind.
   4. Where the page goes, by the three-way test in `write-a-system-explanation.md`.
      Search for an existing page first, and recommend extending it if it fits.
   5. The format: a page, a section of a page, a note or a talk, and its length.
   6. Any question the guide adds for this kind.
7. Find facts yourself. Do not ask the user for anything you can read in the repo,
   the notes or the MCP tools.
8. Stop asking when every decision above is settled.
9. Propose the outline:
   - the title, as a plain statement;
   - the reader and their goal, in one line each;
   - each heading, with one sentence that states its point;
   - where each diagram goes, and the one question it answers;
   - the facts each section relies on, with their source, or "to check";
   - the existing pages it links to instead of repeating them.
10. Use the shape the guide gives for the kind, such as Reilly's headings for a
    design document.
11. Ask the user to accept or change the outline.

## Mode

Ask whether the piece is for learning or for output, if it is not clear. The
capstone and permanent notes are learning: in coach mode the user writes the
outline's sentences, and you ask questions and point at gaps. See
`write-with-ai.md` in `communicate-clearly`.

## Output

The outline in the conversation. Write it to a file only when the user asks, and
then beside the draft it serves.
