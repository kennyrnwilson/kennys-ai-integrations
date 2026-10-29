---
name: talk
description: Turn a document or a subject into a talk — one message, an arc that opens with a promise and repeats the message, slides as visuals, and speaker notes — as a Marp deck beside the document. Follows build-a-talk in communicate-clearly. Use when the user says /talk, asks to make a presentation, slides or a deck from a document, or to plan a talk.
argument-hint: "[path to source document, or topic]"
---

# Talk

Turn a document into a talk, not bullets pasted onto slides. This skill has no
rules of its own: the guide is `references/build-a-talk.md` in the
`communicate-clearly` skill.

## Steps

1. Load the `communicate-clearly` skill.
2. Load `references/build-a-talk.md` from it.
3. Read the source document, if the user gave one. If they gave a topic only, run
   `/structure` first, with the kind "a talk".
4. Settle the decisions in "Before you build", in this order. Number each
   question and give your recommended answer:
   1. the audience, and what they should do afterwards;
   2. the message, in one sentence;
   3. the length, in minutes;
   4. the mode, by `write-with-ai.md`: coach if Kenny is learning to present
      this subject, draft for a slide scaffold.
5. Propose the arc, by "The shape of the talk": one line per section, with its
   point, its slide count and its running time. Ask Kenny to accept or change it.
6. List the slides, by "Slides" in the guide: for each one, its title as a
   statement, its visual (an image, a diagram or one number), and one line of
   what the speaker says. If Kenny asked for an outline only, stop here.
7. Build the deck in the mode:
   - **Coach:** Kenny writes the slide titles and the speaker notes. Ask questions
     and point at gaps. Write only the Marp scaffolding.
   - **Draft:** write the slides and the speaker notes from the source document
     only. Mark a claim not in the source as **Unverified**.
8. Write the deck as `talk.md` next to the source document, in the format in
   "Format and where it lives". If the source is not in knowledge-library, ask
   where the deck goes.
9. For each image a slide needs, name it and its one point. Generate it with the
   `image-gen` plugin only after Kenny agrees, and say the cost first (about
   USD 0.04 an image).
10. Check the deck against "Slides" and "Rehearse" in the guide. Report each slide
    that is a page and not a visual, or that has no speaker notes.
11. Give Kenny the export command. Do not run it unless he asks.

## Output

- The arc, in the conversation, for step 5.
- The slide list, in the conversation, for step 6.
- The deck, `talk.md`, with speaker notes as comments under each slide.
- A list of the images to make, and the slides that failed the check.
