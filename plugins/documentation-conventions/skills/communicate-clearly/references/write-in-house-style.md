# Write in house style

← [Back to communicate-clearly](../SKILL.md)

The house style in full: each rule, why it exists, and a bad and a good example.
`SKILL.md` carries the short form. Apply every rule to every finished document.

## 1. UK spelling

**Rule.** Use UK spelling in prose: "organise", "colour", "behaviour". Code
identifiers, commands and quoted product names keep their own spelling.

**Why.** One spelling throughout keeps search and reading consistent; mixing the two
looks careless and splits search results.

- Bad: "Organize the notes by color."
- Good: "Organise the notes by colour."
- Good: "Set `backgroundColor` in the theme." (an identifier keeps its spelling)

## 2. Plain English

**Rule.** Use the common word. Replace a long or Latinate word when a short one says
the same thing.

**Why.** The reader spends attention decoding vocabulary that adds nothing. An AI
reader copies the register it reads, so inflated prose spreads.

- Bad: "Utilise the script to initiate the synchronisation process."
- Good: "Run the script to start the sync."

## 3. Lead with the point

**Rule.** The first sentence of a page, section or paragraph says what it is for or
what it concludes. Background follows.

**Why.** Readers skim. A reader who stops after one sentence should still leave with
the main point, and an AI deciding whether a section is relevant reads its opening
first.

- Bad: "Over the past few months several approaches to backups were tried, each
  with drawbacks, and after some discussion it was decided that…"
- Good: "Backups run nightly to the NAS. Two earlier approaches failed, for these
  reasons: …"

## 4. Name the actor and the action

**Rule.** Make the thing that acts the subject, and the action the verb. Avoid
nominalisations, where an action is turned into a noun ("performance of a test").

**Why.** A sentence with a real subject and verb says who does what. Passive
sentences and nominalisations hide the actor, which is often the one fact the reader
needs.

- Bad: "Deployment of the site is performed after the completion of the build."
- Good: "The runner deploys the site after the build finishes."

## 5. One thing, one name

**Rule.** Pick one name for each thing and use it in the prose, the tables, the
headings and the figures. Do not switch to a synonym for variety.

**Why.** A reader assumes a new name means a new thing. "The database", "the account
store" and a drawing of a disk read as three objects when there is one.

- Bad: "Cloudflare Tunnel reaches the ingress VM. The Linux guest then passes the
  request to nginx."
- Good: "Cloudflare Tunnel reaches the ingress VM. The ingress VM then passes the
  request to nginx."

## 6. Earn every claim

**Rule.** State a fact before any sentence relies on it. Mark a judgement, an
uncertainty, or something you did not check, as such.

**Why.** A sentence the reader cannot check from what they have been shown is worse
than no sentence. Kenny uses his notes to learn; an unearned premise teaches him
something false or leaves him stuck.

- Bad: "A breach at the least important site is a breach of her email." (nothing
  said she reused the password)
- Good: "If she reused that password for her email, a breach at the least important
  site is a breach of her email."
- Good: "Codex probably caches the token per machine; this was not checked."

## 7. Say it plainly

**Rule.** Write captions, headings, figure labels and summaries as plain statements.
Read each one as if seeing it cold, without the text around it.

**Why.** A compressed, aphoristic line reads as a riddle. The reader has to
reconstruct the meaning the writer skipped.

- Bad caption: "One read is every account, not one."
- Good caption: "Read the password file once and you have every user's password."

## 8. Simplify the explanation, never the facts

**Rule.** Make the explanation simpler, never the facts. Numbers, commands, paths,
versions and code stay exact.

**Why.** A rounded number or a paraphrased command looks right and fails when used.
The reader cannot tell which details were simplified.

- Bad: "Run the build with npm."
- Good: "Run `npm run build`."
- Bad: "The test allows about 25 words."
- Good: "The test fails on a sentence of more than 25 words."
