# Learn a subject

← [Back to communicate-clearly](../SKILL.md)

How Kenny learns something with his system: route the material to the right home,
start a teaching workspace, take lessons, review them on a schedule, and promote
what lasts into permanent notes. It also tells `/teach` and the knowledge-library
teach tools what Kenny expects of them, in [For the teacher](#for-the-teacher).

The design and its reasons are in the
[Learning plan](https://github.com/kennyrnwilson/personal-portal/blob/main/docs/system-architecture/learning-plan.md).
Why the method works is the permanent note
[Learning How to Learn](https://github.com/kennyrnwilson/knowledge-library/blob/main/03-permanent-notes/productivity/knowledge-and-communication/learning-how-to-learn.md).

## The terms

- **Teaching workspace:** a folder that `/teach` keeps for one subject. It holds
  `MISSION.md`, `RESOURCES.md`, `NOTES.md`, numbered HTML lessons in `lessons/`,
  reference sheets in `reference/`, shared components in `assets/`, and learning
  records in `learning-records/`.
- **Learning record:** a short file the teacher writes when Kenny has shown he
  understands something, or a misconception was corrected. It steers what to teach
  next.
- **Teach tools:** `teach_start`, `list_lessons`, `get_lesson`, `write_teach_file`
  and `edit_teach_file` in knowledge-library-mcp. They let a claude.ai chat teach,
  with the same skill as `/teach`.

## Which kind of learning

Decide first what the learning should change. This guide covers the first kind in
full.

| Kind | The question | The end product | Where |
|---|---|---|---|
| Understand | Can I explain it without notes? | Lessons, learning records, a permanent note | A teaching workspace, by this guide |
| Change | Am I doing it? | A lever or a protocol in a guidance hub | knowledge-library's `04-guidance/`, checked by the wellbeing-app scorecards |
| Build | Can I do it well, under pressure? | A practice plan with pass-off checks | A progression note, such as the swimming progressions; logs in swim-app |

Most subjects need more than one kind. A workspace teaches the understanding; the
guidance hub and the practice plan carry the rest.

## Route the material

Route by size. Only the last two rows need a workspace.

| What it is | Where it goes |
|---|---|
| A one-off question or insight | A fleeting note, with `append_fleeting`, then `/process-inbox` |
| An article or a video | A literature note in `02-literature-notes/articles/` or `courses/` |
| A book | The book pipeline, into book-library |
| A topic worth one or two short lessons | The `explore` workspace, `05-projects/explore/teach/` |
| A topic that keeps coming back | A workspace of its own, by [Where a workspace lives](#where-a-workspace-lives) |

**Graduation rule.** A topic leaves `explore` after its third lesson. See
[Graduate a topic from explore](#graduate-a-topic-from-explore).

## Where a workspace lives

A workspace lives where its subject lives.

| Home | Path | For |
|---|---|---|
| Project | `05-projects/<project>/teach/` | A course with an end, such as `technical-writing` |
| Area | `03-permanent-notes/<area>/<topic>/teach/` | An ongoing subject, next to its permanent notes |
| Explore | `05-projects/explore/teach/` | Short lessons on whatever came up |

The teach tools accept only the project and explore homes. An area workspace works
in Claude Code only, until the tools are changed.

## Start a workspace in Claude Code

1. Open a terminal in the knowledge-library clone: `cd ~/code/knowledge-library`.
2. If the workspace folder does not exist, create it: `mkdir -p 05-projects/<project>/teach`.
3. Go to the workspace folder: `cd 05-projects/<project>/teach`.
4. Start Claude Code: `claude`.
5. Type `/teach <subject>`.
6. Answer the teacher's questions about why you want to learn it. The teacher
   writes `MISSION.md` from your answers.
7. Read the first lesson. The teacher writes it to `lessons/0001-<name>.html` and
   opens it.
8. Commit and push the workspace when you are happy with it.

`/teach` runs only when Kenny types it. An agent cannot start it by itself.

## Start a workspace in a chat

1. If the project does not exist, ask the chat to create it: "create a project
   note called <name>".
2. Ask: "teach me <subject>, in the <project> project".
3. Check that the chat called `teach_start`. Its reply names the workspace path.
4. Answer the teacher's questions about why you want to learn it.
5. Read the lesson draft the chat describes.
6. Say "save the changes". The chat reports a commit and a pending count of 0.
7. Wait about five minutes. Then open the lesson's URL, on the portal under
   `/knowledge/projects/<project>/teach/lessons/`.

## Put books in a workspace

1. List each book in `RESOURCES.md` by its portal page: `/books/<slug>/`.
2. Say which chapters to use for what, in the entry's "Use for" line.
3. Ask the teacher to teach from the chapter summaries.

In a chat, the teacher fetches a summary with `get_chapter_summary`. In Claude
Code, it reads `~/code/book-library/<slug>/chapter-summaries/`. See
[For the teacher](#for-the-teacher).

## Take a lesson

1. Open the lesson. It is written for a phone and takes about 10 minutes.
2. Read the lesson once.
3. Answer the quiz. You get one tap per question.
4. Do the Recall section without scrolling up. Type your answer in the box and
   tap **Check**: learning-app marks it against the model answer, then shows the
   model answer. Off the tailnet the box does not appear, so open the model
   answer and compare.
5. Tell the teacher what you got wrong, or what you doubt.
6. Do the "At work" box later, at a desk. It is not part of the 10 minutes.
7. Report the result of the "At work" task to the teacher in the next session.

## Who writes what

Learning is coach mode, by [`write-with-ai.md`](write-with-ai.md): Kenny writes
whatever he is meant to learn from.

| Kenny writes | The teacher writes |
|---|---|
| Quiz and recall answers, explanations, the "At work" results | Lessons, quizzes, reference sheets and assets |
| Promoted permanent notes, in coach mode | Learning records, from what Kenny showed |
| The mission's answers | `MISSION.md`, `RESOURCES.md` and `NOTES.md` |

## Review on a schedule

`/teach` keeps no schedule, so a Todoist task does it.

1. When a workspace has its first lesson, add a recurring Todoist task.
2. Name it "Review: quiz me on <project> lessons".
3. Set it to repeat every week.
4. Put it in the subject's Todoist project, or else in **Learning**.
5. When the task is due, start a session in the workspace: in Claude Code, `/teach quiz me on lessons 1 to N`; in a chat, "quiz me on <project> lessons 1 to N".
6. Answer from memory. Do not open the lessons first.
7. Ask for the feedback after the whole quiz, not after each answer.
8. Complete the Todoist task.

The teacher adds a learning record for each thing you showed or corrected.

## Promote an insight

When a learning record holds an insight you would want without the workspace,
follow "Promote a learning record" in [`keep-notes.md`](keep-notes.md). In short,
write it as a permanent note in coach mode, and link the note to its record.

## Graduate a topic from explore

Do this in Claude Code. The teach tools cannot move files.

1. When a topic in `explore` has three lessons, decide whether it has an end.
2. If it has an end, create a project: `05-projects/<topic>/README.md`.
3. If it has no end, use its area: `03-permanent-notes/<area>/<topic>/`.
4. Create the new `teach/` folder.
5. Write its `MISSION.md`, with the teacher, from the topic's lessons.
6. Move the topic's lessons and learning records into it with `git mv`.
7. Renumber them from `0001`, in their old order.
8. Copy the `assets/` they use.
9. Fix the links between the moved files.
10. Remove the moved lessons from the list in `05-projects/explore/README.md`.
11. Move the topic's review task in Todoist to the new home.

## Close the loop

Once a quarter, check whether what Kenny measures should change what he believes.

1. Open the quarterly Todoist task "Review: close the learning loop".
2. Read the Healthspan and Mind scorecards in wellbeing-app.
3. Read the practice logs, such as swim-app sessions.
4. For each lever or protocol that the results contradict, write a fleeting note.
5. For each teaching workspace, check that its mission still holds.
6. Process the fleeting notes with `/process-inbox`.
7. Complete the Todoist task.

## For the teacher

What Kenny expects of `/teach` and of a chat running the teach tools, on top of the
`teach` skill:

- Read `MISSION.md`, `NOTES.md` and the learning records before writing a lesson.
- Keep each lesson to about 10 minutes on a phone. Put desk work in an "At work" box.
- Teach from sources, never from memory. For a book in book-library, fetch its
  chapter summary and cite the portal page of that summary.
- Make every quiz answer the same number of words. Vary the position of the right
  answer.
- Write each Recall model answer as a list of key points, each one checkable, in
  the order the question asks for them. learning-app marks a typed answer against
  that list.
- Load `recall.js` after `quiz.js` in every lesson:
  `<script src="../assets/recall.js"></script>`.
- Link each lesson to its reference sheet, and the sheet back to the lesson.
- Reuse `assets/`. A new workspace may copy another workspace's `course.css`,
  `quiz.js` and `recall.js`.
- Write a learning record only for something Kenny showed, never for material that
  was only covered.
- Never write Kenny's answers, explanations or permanent notes.
- Follow the house style in lessons, as in any finished document.
- In a chat, save only when Kenny says so.
