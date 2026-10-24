---
name: process-inbox
description: Go through knowledge-library's fleeting notes and propose a fate for each — develop, merge into an existing note, or archive — with where it would be filed and linked. The AI proposes; Kenny decides and writes. Follows "Process the inbox" in communicate-clearly's keep-notes guide. Use when the user says /process-inbox, asks to process, triage, clear or review their inbox or fleeting notes.
argument-hint: "[note path, optional]"
---

# Process the inbox

Propose what to do with each fleeting note. This skill has no rules of its own:
the steps are "Process the inbox" in `references/keep-notes.md` in the
`communicate-clearly` skill. The AI proposes and Kenny writes. A developed
permanent note is written in coach mode, never drafted by the AI.

## Steps

1. Load the `communicate-clearly` skill.
2. Load `references/keep-notes.md` from it, and read "Process the inbox" and
   "Where a note goes".
3. List the inbox. Use the knowledge-library MCP's `list_fleeting`. With a local
   clone and no MCP, list `01-fleeting-notes/` instead. If the user named one
   note, take only that note.
4. Read each note with `get_note`, or from the clone.
5. For each note, search for the notes it belongs with: `search_notes` on its key
   terms, and `list_permanent_notes` for the likely life area. A book named in
   the note is checked with the book-library MCP's `list_books`.
6. Propose a fate for each note, as "Process the inbox" defines them:
   - **Develop:** the kind of note it becomes, and where it is filed by "Where a
     note goes". Ask "in which context will I want to find this again?", and name
     that context.
   - **Merge:** the existing note it adds to, and the section.
   - **Archive:** to `07-archive/`, with the reason.
   For a quote in a fleeting note, propose the source's notes it moves to.
7. Name the links each developed note would need, and the notes that would link
   back.
8. Ask Kenny to accept, change or skip each proposal.
9. For each accepted proposal:
   - **Develop** a permanent note: switch to coach mode with `/draft coach`.
     Kenny writes it.
   - **Develop** a literature note or a quote: Kenny writes it. `add_quote` and
     `add_book_quote` may stage a quote he dictates.
   - **Merge:** Kenny writes the addition. Stage it with `update_note` only after
     he gives the words.
   - **Archive:** move the file with the clone, or list it for Kenny to move.
     The MCP has no move tool.
10. Run `save_changes` only when Kenny says to save.

## Output

A table in the conversation, one row per note: the note, the proposed fate, where
it goes, the links, and one line on why. Then the questions for step 8.

Do not write a developed note's prose. Do not paste a fleeting note into another
note.
