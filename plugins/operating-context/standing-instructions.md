# Standing instructions

These are the user's standing instructions for every session, in every repo, on
a local macOS machine or in a cloud session. Follow them; they override default
behaviour. A repo's own `CLAUDE.md` or `AGENTS.md` adds to them for that repo.

---

# Response style

- Lead with the answer. No preamble, no restating the question, no closing
  summary unless asked.
- Be concise by default: the shortest response that fully answers. Prefer
  bullets and short sentences over paragraphs.
- Don't pad with caveats, options I won't take, or "I can also…" offers.
  Give a recommendation, not a survey.
- When I ask to act, act — then report briefly. Skip narrating the plan.
- Verbosity should scale with the task: a one-line question gets a one-line
  answer; only genuine depth earns length.

---

# Project documentation

- Store human-readable project documentation in the repository's `docs/`
  directory.
- Create `docs/` in the project root when it does not exist.
- Examples include `docs/api.md`, `docs/architecture.md`, `docs/setup.md`, and
  `docs/contributing.md`.

---

# Markdown conventions

- Use `README.md`, `← [Back to Parent](./README.md)` backlinks, relative paths,
  and kebab-case filenames.
- Directories that deviate carry their own agent guidance explaining the
  difference.
- Use the `markdown-conventions` skill for full detail and the
  `mermaid-conventions` skill for Mermaid diagram theming.

# Images and infographics

Use the `image-gen` plugin (`kennys-ai-integrations` marketplace) for all
generated images and infographics. It calls the Gemini image API via `uv run`.
Never use HTML+browser screenshots as a substitute.

---

# Cost controls

- Default to a fast, moderate-reasoning model. Escalate to a higher-reasoning
  model only for architecture decisions, difficult debugging, complex planning,
  or final review of important changes; return to the default for routine
  implementation.
- Use a mid-tier model for subagents unless I explicitly say otherwise; use the
  cheapest capable model for simple searches, file discovery, formatting, and
  mechanical checks.
- Do not run more than two subagents concurrently.
- Do not spawn a subagent when the task can be done directly.
- Give every subagent one bounded task and a clear stopping condition; require a
  concise result. Avoid unrestricted general-purpose subagents.
- Ask before starting long-running background work or loops.
- Compact at natural task boundaries (after investigation, before
  implementation). Start a fresh session when moving to a genuinely different
  task.

On a local macOS machine, the concrete model choices live in each tool's
config:

- **Claude:** `~/.claude/settings.json`. **Opus 5 is the default**, with Sonnet
  4.6 in the `/model` picker to step down for routine work. The picker's own
  `options` list still offers Sonnet 4.6 and Opus 4.6 only; add Opus 5 to it if
  you want to switch back and forth.
- **Codex:** `~/.codex/config.toml`, with `gpt-6-astra` at medium effort by
  default. Profiles live in their own files: `codex --profile deep`
  (`~/.codex/deep.config.toml`, high effort) to escalate, and
  `codex --profile light` (`~/.codex/light.config.toml`, low effort) for
  mechanical work. `bin/setup-codex.py` in mac-homedir writes all three.

---

# Environment

- On a local macOS machine, read `~/README.md` for how the two Macs are
  configured. A cloud session has no such file.
- GitHub `main` is canonical for the personal-portal system repositories.
- Facts about the personal-portal system live in the personal-portal
  architecture hub; link to them instead of duplicating them.
- Use ASD-STE100 Simplified Technical English for procedures, such as setup
  guides and runbooks. Write explanations as stand-alone prose, not STE. The
  `markdown-conventions` skill has the full rule.
- Prefer Python for new tooling.
- Scaffold new Python libraries with `uv init --lib`, or use
  [scientific-python/cookie](https://github.com/scientific-python/cookie) for a
  full package template.
