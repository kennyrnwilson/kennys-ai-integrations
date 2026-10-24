---
name: review-draft
description: Review a draft against Kenny's writing standard — the review-a-draft checklist and new-joiner test in communicate-clearly. Use when the user says /review-draft, asks to review, critique or check a document, note, runbook or explanation, or asks "is this clear?" about their writing. Not for code review.
argument-hint: "[path or pasted draft]"
---

# Review a draft

Named `review-draft` because Claude Code's built-in `/review` reviews code.

Check a draft against the standard and report what to fix. This skill has no rules
of its own: the checklist is `references/review-a-draft.md` in the
`communicate-clearly` skill.

## Steps

1. Load the `communicate-clearly` skill.
2. Load `references/review-a-draft.md` from it.
3. Get the draft. If the user gave a path, read the file. If they gave no draft, ask
   for one.
4. Find the mode. If the user wrote the draft to learn, such as a permanent note or
   the capstone, the mode is coach. If an AI drafted it, or it is a team doc, the
   mode is co-write or draft. If it is not clear, ask.
5. Load the guide for the kind of draft:
   - a procedure: `write-a-procedure.md`;
   - software documentation: `write-a-system-explanation.md`;
   - a note: `keep-notes.md`.
6. Follow "How to review" in `review-a-draft.md`, all six steps.
7. Check each claim that names a file, command, path, tool or count against the
   repo or the system. Mark a claim you could not check as **Unverified**.
8. In a procedure document in personal-portal, count the words in each sentence of
   each step. Report every sentence of more than 25 words; the sentence-length test
   fails on them.
9. Do not edit the draft. Report only, unless the user asks you to apply the fixes.

## Output

1. One line: the reader, and whether the draft serves them now.
2. The new-joiner marks: each quoted passage, and what the newcomer is missing.
3. The findings, ordered by harm to the reader. For each one give:
   - the passage, quoted, with its heading or line;
   - the rule it breaks, by the checklist item's name;
   - the fix: in coach mode, a question that points at the problem; in co-write or
     draft mode, the rewritten sentence.
4. A pattern that repeats goes in once, with two examples and a count.
5. Leave out a checklist section that found nothing. Do not praise.
