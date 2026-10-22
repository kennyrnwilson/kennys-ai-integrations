# Review a draft

← [Back to communicate-clearly](../SKILL.md)

How to review a draft against the standard, whether Kenny wrote it or an AI did.
The `/review` and `/new-joiner` skills follow this guide.

## How to review

1. **Read the draft once as its reader.** Name that reader and what they need from
   the draft before you look for faults.
2. **Run the new-joiner test** (below), and note every point where you got lost.
3. **Run the checklist,** section by section.
4. **Report each finding** with:
   - the passage, quoted;
   - the rule it breaks;
   - a suggested fix.
5. **Order the findings by harm to the reader.** A wrong fact comes before a vague
   sentence, and a vague sentence before a style slip.
6. **Stop at what matters.** Report the pattern once, with two examples, rather than
   every instance.

In coach mode, point at the problem and ask a question. Do not rewrite Kenny's
sentences for him: the rewriting is where he learns. In co-write and draft mode,
give the rewritten sentence.

## The new-joiner test

Read the draft as a capable newcomer: someone with the skills, but none of the
history, and none of the conversation that produced the draft. Mark every point
where that reader would stop:

- a term used before it is defined;
- an abbreviation not spelled out on first use;
- a step that assumes something the page never said;
- a reference to "the issue", "the change" or "this" with nothing to point at;
- a jump the writer made because they knew the answer.

Each mark needs a definition, a link or a sentence. This is the curse of
knowledge: the writer cannot see these gaps, so someone else has to.

## Checklist

### Purpose and structure

- [ ] The first sentence says what the page is for.
- [ ] Each section leads with its point.
- [ ] The page is one kind: explanation, how-to, reference or tutorial. See
  [`write-a-system-explanation.md`](write-a-system-explanation.md).
- [ ] Nothing in it is duplicated from the page that owns that fact. It links
  instead.

### House style

- [ ] UK spelling in prose; code keeps its own spelling.
- [ ] Plain words: no "utilise", "leverage", "facilitate".
- [ ] Each sentence names its actor: no "it was decided", "is performed".
- [ ] Each thing has one name, and the name matches the
  [glossary](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/glossary.md).
- [ ] Headings, captions and summaries are plain statements, not slogans.
- [ ] Numbers, commands, paths and code are exact.

### Concision

- [ ] No sentence opens with "There is" or "There are" when it could name the
  subject.
- [ ] No "the fact that", "in order to", "it is important to note that".
- [ ] No empty intensifiers: "very", "really", "extremely", "clearly".
- [ ] No padding nouns: "in the case of", "of a … nature", "a key factor".
- [ ] No metadiscourse: "In this section we will look at…". Say the thing.
- [ ] No needless hedging. A real uncertainty is stated once, where it applies.

The active voice is the default. The passive is right when it keeps the reader's
attention on the right thing: "The key is stored in the VM" when the key is the
subject.

### Claims

- [ ] Every fact a sentence relies on is stated, or linked, before it.
- [ ] A judgement is marked as a judgement.
- [ ] Anything not checked says so. A useful scheme labels each claim as one of:
  - **Product:** established by official documentation;
  - **Here:** the current state of this machine or account;
  - **Inferred:** concluded from evidence, but documented nowhere;
  - **Unverified:** an open question.
- [ ] A dated claim says when it was checked, and against what.
- [ ] A health claim follows the claim-verification structure in knowledge-library
  `AGENTS.md`.

### Procedures

- [ ] Every step follows the eight rules in
  [`write-a-procedure.md`](write-a-procedure.md): among them one action per step,
  the imperative, the condition before the action, and what the reader should see
  after a step.

### Form

- [ ] The backlink, filename and footer follow `markdown-conventions`.
- [ ] Every link resolves. In-repo links are relative and file-relative.
- [ ] Every Mermaid diagram follows `mermaid-conventions` and has an `accTitle` and
  an `accDescr`.

## Read it aloud

Read the draft aloud, or have it read to you. A sentence you stumble over will
mislead a reader too: the stress falls on the wrong word, or a phrase attaches to
the wrong noun.

## Sources

- Pinker, *The Sense of Style*: the curse of knowledge, metadiscourse, hedging,
  reading aloud, and when the passive is right.
- Strunk, *The Elements of Style*: the concision checks. Pinker's rule on the
  passive overrides Strunk's "always use the active voice".
- Reilly, *The Staff Engineer's Path*: no bare "this" or "that".
- The sourcing labels come from mac-homedir's diagram and voice conventions
  ([`docs/diagram-and-voice-conventions.md`](https://github.com/kennyrnwilson/mac-homedir/blob/main/docs/diagram-and-voice-conventions.md)).
