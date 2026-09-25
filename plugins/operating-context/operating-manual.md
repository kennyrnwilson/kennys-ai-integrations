# Operating manual

The public index to how I run my life and projects — structure and pointers only.
The depth lives in a private hub this points into.

## What this is

An AI-first personal system that turns knowledge into action across eight repos,
with GitHub `main` as the single source of truth: knowledge-base articles, book
libraries, database-backed apps, the portal, and the two that configure the
machines and the agents themselves.

Claude Code and OpenAI Codex reach the system in three ways:

1. **The repos, directly.** On a Mac or in a cloud session, an agent clones and
   reads or writes them.
2. **Four MCP servers on the always-on Mac Mini,** stdio child processes
   registered for both makers against the same commands. Two front a git
   repository of markdown — the notes and the books — and two front an app
   database. Starting or driving a session on the Mini from a phone gets the
   same four.
3. **Two of those servers again, as HTTP daemons in a Linux VM on the Mini,**
   behind Cloudflare Access and a tunnel that dials out. This route needs no
   Mac, so a browser session reaches the notes and the books from anywhere.

The through-line is two operating systems — Longevity OS and Mind OS — carrying
book action items -> ranked guidance -> live scorecards -> daily protocols across
those repos. Full architecture is in the personal-portal hub, under
`docs/system-architecture`: https://github.com/kennyrnwilson/personal-portal —
start at `pictorial-guide.md` for the shape, `index.md` for the specification.

## The repos

- [knowledge-library](https://github.com/kennyrnwilson/knowledge-library) — the
  note and life-management system, **inspired by** Zettelkasten and blended with
  PARA and my own methods, not an implementation of either. Holds the guidance
  goals (maximise-healthspan, master-your-mind, sharpen-focus, lead-people).
- [book-library](https://github.com/kennyrnwilson/book-library) — a folder per book,
  with notes and action items.
- [wellbeing-app](https://github.com/kennyrnwilson/wellbeing-app) — Apple Health data;
  longevity and mind scorecards.
- [swim-app](https://github.com/kennyrnwilson/swim-app) — swim sessions and drills.
- [finances](https://github.com/kennyrnwilson/finances) — self-hosted Actual Budget.
  No MCP server: it is the one part no agent can see.
- [personal-portal](https://github.com/kennyrnwilson/personal-portal) — the Astro
  build, the nginx router, and the system docs (the hub).
- [mac-homedir](https://github.com/kennyrnwilson/mac-homedir) — how a Mac becomes a
  participating node of this system.
- [kennys-ai-integrations](https://github.com/kennyrnwilson/kennys-ai-integrations) —
  the plugin marketplace, including the hook that loads this page into a session.

## The host

The always-on Mac Mini serves the site, runs the MCP servers, hosts the ingress
VM, and bridges mobile. GitHub `main` is canonical; every machine fast-forwards
from it automatically.

## Conventions

- Link, don't duplicate — system-wide facts live in the hub; repos point at it.
- Documentation lives in each repo's `docs/`; markdown per the
  documentation-conventions skill.
- One `AGENTS.md` per repo, read by both makers, with `CLAUDE.md` a pointer to it.
- Writing: ASD-STE100 Simplified Technical English for procedures; explanations
  are stand-alone prose (the markdown-conventions skill has the rule).
  Python-first for new tooling.

## A note on access

Most of these repos are private; the links resolve only for my own authenticated
sessions. This page is the public top sheet — secrets, private paths, and machine
endpoints are deliberately not here.
