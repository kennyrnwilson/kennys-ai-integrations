---
name: new-joiner
description: Read a draft as a capable newcomer with none of the history and mark every point where they would stop — an undefined term, an unexpanded abbreviation, an assumed step, a "this" with nothing to point at. Follows the new-joiner test in communicate-clearly's review-a-draft. Use when the user says /new-joiner, asks whether a newcomer could follow a page, or asks to test a doc for the curse of knowledge.
argument-hint: "[path or pasted draft] [reader, optional]"
---

# New-joiner test

Run only the new-joiner test on a draft. It is step 2 of `/review-draft`, on its
own, for when the question is "could someone new follow this?" and not "is this
well written?". This skill has no rules of its own: the test is in
`references/review-a-draft.md` in the `communicate-clearly` skill.

## Steps

1. Load the `communicate-clearly` skill.
2. Load `references/review-a-draft.md` from it, and read "The new-joiner test".
3. Get the draft. If the user gave a path, read the file. If they gave no draft,
   ask for one.
4. Name the newcomer: the reader the user gives, or else a capable engineer who
   has the skills but has never seen this system. Say who you are reading as.
5. Forget the conversation. Use only what the page says, and what it links to.
   Do not use what you know from the repo, the session or earlier pages.
6. Read the page once, top to bottom, in order. At each point where the newcomer
   would stop, record:
   - the passage, quoted, with its heading;
   - which of the test's five kinds of stop it is;
   - what the newcomer is missing.
7. For each mark, suggest the smallest fix: a definition, a link to the page that
   owns the fact, or one sentence. Prefer a link to the
   [glossary](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/glossary.md)
   for a term the system already names.
8. Do not edit the draft. Report only, unless the user asks you to apply the
   fixes.

## Output

1. One line: who you read as, and whether they could finish the page.
2. The marks, in page order. A term that is missing in many places goes in once,
   with its first place and a count.
3. The first place where the newcomer would give up, if there is one.

Do not report style or structure findings. Those belong to `/review-draft`.
