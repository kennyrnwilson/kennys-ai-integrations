# Keep notes

← [Back to communicate-clearly](../SKILL.md)

How to capture, file and write notes in knowledge-library, and in book-library for
books that have been through the book pipeline. The house style applies to every
note except fleeting notes, which are raw capture.

The reasons behind these rules are in the
[note-taking note](https://github.com/kennyrnwilson/knowledge-library/blob/main/03-permanent-notes/productivity/knowledge-and-communication/note-taking-and-pkm.md).
The terms (fleeting note, inbox, life area, guidance goal) are defined in the
[glossary](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/glossary.md#notes-and-guidance).

## Where a note goes

| Kind | Where | When |
|---|---|---|
| Fleeting note | knowledge-library `01-fleeting-notes/` | Immediately. Raw, unstructured |
| Literature note | knowledge-library `02-literature-notes/` (`books/`, `articles/`, `courses/` and others) | After reading a source that has not been through the book pipeline |
| A pipeline book's notes | book-library `<book>/personal-notes/README.md` | After reading a book that has its own folder in book-library |
| Permanent note | knowledge-library `03-permanent-notes/<life area>/` | When an idea is worth keeping in your own words |
| Guidance | knowledge-library `04-guidance/<goal>/` | When knowledge turns into a repeatable action |
| Learning record | a `/teach` workspace, `05-projects/<project>/teach/` | While learning a subject. The [Learning plan](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/learning-plan.md) owns these |

A book "has been through the pipeline" when book-library has a folder for it. Check
with the book-library MCP's `list_books`, or look for the folder.

## Who writes the note

Decide first whether the goal is learning or output.
[`write-with-ai.md`](write-with-ai.md) has the three modes.

- **Permanent notes are written in coach mode.** Kenny writes every sentence. The AI
  asks questions, critiques and plays the confused reader. A note an AI drafts
  exists on disk, but the understanding it was meant to build does not.
- **Literature notes and a pipeline book's notes** are Kenny's words too: the
  pipeline's summaries already hold the book's words.
- **Guidance** may be co-written: Kenny owns which actions it lists, and the AI may
  draft the wording.

## Capture

1. Write the thought down at once, in `01-fleeting-notes/`. From a chat, use the
   knowledge-library MCP's `append_fleeting`.
2. Do not structure it. Capture is fast or it does not happen.
3. Process the inbox within a day or two, while the context is still fresh.

## Process the inbox

The `/process-inbox` skill follows these steps: it proposes, and Kenny decides and
writes. For each fleeting note:

1. Decide its fate: develop it, merge it into an existing note, or archive it to
   `07-archive/`.
2. To develop it, ask which existing note it belongs with. Search before you create.
3. Ask: "in which context will I want to find this again?" File and link the note
   for that context, not for where it came from.
4. Write the developed note in your own words. Never paste the fleeting note in.

Topics are not planned in advance. A cluster of related permanent notes becomes a
folder, and then a hub with a `README.md`, when there are enough of them.

## Write a literature note

Use [`.templates/literature-summary.md`](https://github.com/kennyrnwilson/knowledge-library/blob/main/.templates/literature-summary.md).

1. Record the source: author, type, link, status, rating and dates read.
2. Write the overview and the takeaways in your own words. A copied passage is a
   quote and follows the quote rules below.
3. Link each takeaway that matters to the permanent note it informs, and link back.
4. List the actions the source suggests.

For a pipeline book, write the same sections in the book's
`personal-notes/README.md` instead. Do not repeat what the book's summaries and
chapter summaries already say: link to them, and write only what is yours.
book-library may not link to knowledge-library, so name related permanent notes in
plain text. The permanent notes link to the book.

## Write a permanent note

Use [`.templates/note.md`](https://github.com/kennyrnwilson/knowledge-library/blob/main/.templates/note.md).

1. Find the parent folder in the right life area. Create its `README.md` first if
   the folder is new.
2. Check that no note anywhere in the library has the same base filename. A
   duplicate breaks the portal build as soon as a wikilink points at it.
3. Write the summary first: one paragraph that says the idea.
4. State the evidence strength: Strong, Moderate or Limited. For a health claim,
   use the claim-verification structure in knowledge-library `AGENTS.md`.
5. Write "How I Use This": what you do differently, with one specific example.
6. Cite the sources. Link a book with the `book-library/` prefix form, for example
   `[Outlive](book-library/outlive/README.md)`. The portal rewrites it to the
   book's page.
7. Link generously to related notes, with relative links.
8. Add the backlink under the title, and link down from the parent `README.md`.
9. For every note you link to, add a link back from its `**Related:**` section.
10. Finish with the footer: Related, Tags, Created and Last Updated.

A note does not have to hold one idea. It can hold a whole subject that reads
better in one piece. Do not split a note only to make it smaller.

A permanent note never ranks levers against each other. Ranking lives only in the
guidance hubs.

## Write guidance

1. Name the outcome the guidance serves, and file it under that goal in
   `04-guidance/`.
2. Write from the outcome: "To lead well, I…".
3. Say what to do, as steps. [`write-a-procedure.md`](write-a-procedure.md) applies.
4. Rate each action for impact and evidence.
5. Link to the permanent note that explains why. If the guidance starts to explain
   a mechanism, move that prose into the permanent note.
6. If the action is a ranked lever, add or update its row in the goal's hub
   (`maximise-healthspan/README.md` or `master-your-mind/README.md`). The hub is the
   only place that holds the tiers `T0` to `T4`.

## Quotes

A quote is worth keeping only if it can be cited later and you can say why it
mattered.

### Where a quote lives

- **In its source's notes,** under "Quotes & Highlights": the literature note, or a
  pipeline book's `personal-notes/README.md`.
- **A quote with no source note yet** (a talk, a conversation, a post) goes into
  the day's fleeting note. Processing the inbox moves it to a literature note, and
  creates one if needed.
- **A quote that becomes your own idea** is quoted in a permanent note that links
  back to the source's notes.
- A quote never gets a file of its own.

### The shape

Every quote has four parts:

```markdown
> "Exercise is the most potent longevity drug we have."
> — Peter Attia, *Outlive*, ch. 11, p. 213

- **Why:** one line, in your own words, on why it mattered
- **Links:** [Zone 2 Cardio](../../03-permanent-notes/wellbeing/fitness/zone-2-cardio.md) · #quote/exercise
```

- The **source line** makes the quote citable: author, title, and a chapter, page,
  timestamp or URL precise enough to find it again.
- The **Why** line is what makes it a note and not a copied highlight. It is the
  seed of a permanent note.
- The **`#quote/<theme>` tag** gives a view across sources. A search for
  `#quote/exercise` finds every quote on exercise.

### From a chat

- knowledge-library MCP: `add_quote` appends a quote in this shape to a literature
  note, and creates the note from the template if it does not exist.
- book-library MCP: `add_book_quote` appends a quote to a pipeline book's personal
  notes.

Both stage the change on disk. Nothing is committed until Kenny approves and the
matching save tool runs.

## Promote a learning record

A `/teach` learning record belongs to its workspace. When it holds an insight you
would want without the workspace:

1. Write that insight as a permanent note, in coach mode.
2. Link the permanent note to the lesson or record it came from.
3. Leave the learning record where it is.

## End a session

Before you stop, write one line at the end of the note you were working on, or in
the day's fleeting note, saying where to start next time.

## Worked examples

- **Folding a book into notes and guidance:** the dose-effect, worry-cure and
  longevity specs in knowledge-library
  [`docs/superpowers/specs/`](https://github.com/kennyrnwilson/knowledge-library/tree/main/docs/superpowers/specs).
  They predate the move of pipeline-book notes to book-library, so read their
  literature-note steps as "the book's personal notes".
- **A playbook for one type of note:**
  [`docs/swimming-stroke-note-playbook.md`](https://github.com/kennyrnwilson/knowledge-library/blob/main/docs/swimming-stroke-note-playbook.md).
  Its book links use tailnet URLs. New notes use the `book-library/` prefix form.

## Sources

- Ahrens, *How to Take Smart Notes*: process fleeting notes within a day or two;
  write in your own words; link for the context of retrieval; let topics emerge;
  separate drafting from editing. Ahrens also wants one idea per note.
  knowledge-library deliberately does not require that.
- Forte, *Building a Second Brain*: PARA, which the folders blend in; distil a note
  only when a project needs it; end each session with where to start next.
