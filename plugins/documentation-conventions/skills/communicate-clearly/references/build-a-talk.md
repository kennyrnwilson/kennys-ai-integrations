# Build a talk

← [Back to communicate-clearly](../SKILL.md)

How to turn a document, or a subject, into a talk. A talk is not a document read
aloud: the audience cannot reread a sentence, skip ahead or look a term up. The
house style applies to the slides and the speaker notes. The `/talk` skill follows
this guide.

The reasons behind these rules will be in the
[presenting note](https://github.com/kennyrnwilson/knowledge-library/blob/main/03-permanent-notes/productivity/knowledge-and-communication/presenting.md),
which Kenny writes in coach mode. Until it is written, the sources below carry the
reasons.

## Before you build

1. **Name the audience and what they should do afterwards.** "The platform team,
   who should approve the migration" is an audience. "Engineers" is not. The
   audience is the hero of the talk, and the speaker is the mentor who gives them
   what they need. Cut what is about the speaker and not about them.
2. **Write the message in one sentence.** It is the sentence the audience should
   be able to repeat the next day. If it takes two sentences, the talk is two
   talks, or the message is not settled yet.
3. **Fix the length,** and the time kept for questions. Every later cut follows
   from it.
4. **Find the source document.** A talk built from an existing page links to it,
   and the page holds the detail. The talk does not have to carry everything.

## The shape of the talk

1. **Open with the promise:** what the audience will know or be able to do by the
   end. Do not open with a joke or an apology.
2. **Show the gap:** the problem as it is now, then what it could be. Return to
   this contrast as the talk moves on: it is what makes the audience want the
   change.
3. **Give the outline** in one slide, and show where you are in it at each new
   section. This signposting stands in for the headings a reader can see.
4. **Make each section one point,** with one example or piece of evidence.
5. **Repeat the message:** in the opening, at a turn in the middle, and at the
   end. Winston calls this cycling. A listener who drifted for a minute gets the
   message back; a reader would have reread it.
6. **Close with what the audience should do,** and the message once more. Show
   what is better once they have done it. End on your contributions or the call to
   action, not on "Thank you" or "Questions?".

## Slides

- A slide supports the speaker. It is not the document on a screen. If the slide
  can be read without the speaker, it is a page, and belongs in the handout.
- One idea per slide, with its point as the title, written as a statement.
- Few words: a short phrase, not sentences. The speaker says the sentences.
- Prefer an image, a diagram or one number to a list. Generate images with the
  `image-gen` plugin; never use screenshots of HTML as a substitute.
- A diagram on a slide is simpler than the same diagram in a document: fewer
  boxes, larger labels. Follow the `mermaid-conventions` skill for its theme.
- Show code only when the talk is about that code, and only the lines that
  matter.

## Speaker notes

- Put the notes under each slide: what to say, in full sentences, in the house
  style. The notes are where the prose lives.
- Mark where to repeat the message and where to signpost.
- Give each section a running time, so a long talk can be cut on the day.

## Format and where it lives

The deck is a [Marp](https://marp.app) markdown file, `talk.md`, next to the
document it came from. Talks live in `05-projects/<project>/` in knowledge-library.

- Start the file with `marp: true` in its front matter. Separate slides with `---`.
- Write the speaker notes as an HTML comment under each slide. Marp shows them in
  presenter view.
- Put images next to the deck, and link them relatively (`./diagram.png`).
- Export one self-contained HTML file: `npx @marp-team/marp-cli talk.md -o
  talk.html`. The portal build copies `talk.html` and its images, and publishes
  them under `/knowledge/projects/<project>/`. It also renders `talk.md` as an
  ordinary page, which reads as the talk's outline.

Use Claude Slides instead when the talk has to be edited outside git, or by
someone without the repo.

## Rehearse

1. Say the talk aloud once, with a timer. Cut to the length; do not speed up.
2. Run `/new-joiner` on the speaker notes. A term the audience has not heard needs
   a sentence in the talk, not a footnote.
3. Check that the message can be found on the first slide, a middle slide and the
   last slide.

## Sources

- Patrick Winston, [*How to Speak*](https://ocw.mit.edu/courses/res-tll-005-how-to-speak-january-iap-2018/)
  (MIT, 2018): open with an empowerment promise, not a joke; cycle back to the
  message; build a fence around the idea; signpost; too many words on slides; end
  on contributions, not "Thank you".
- Nancy Duarte, [*Resonate*](https://github.com/kennyrnwilson/book-library/tree/main/resonate),
  in book-library: the audience as hero and the speaker as mentor (chapter 1); the
  contrast between what is and what could be, the call to action, and the "new
  bliss" that ends the talk (chapter 2).
- Garr Reynolds, *Presentation Zen*: slides are not documents; restraint and
  simplicity; a separate handout for the detail.
- Winston and Reynolds are not in book-library. Their claims here are stated at
  the level of each source's main argument, not cited to a page.
