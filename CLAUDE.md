# kennys-ai-integrations — Agent Guide

Working notes for editing THIS repo.

## Purpose
A Claude Code plugin marketplace: three plugins, published via
`.claude-plugin/marketplace.json` and consumed by adding this repo as a
marketplace source.

## Where things live
- `plugins/<name>/` — one directory per plugin; each needs
  `.claude-plugin/plugin.json` and `skills/<skill>/SKILL.md`
- `tools/` — the marketplace validator (Python, uv-managed, has tests)
- `.github/workflows/validate.yml` — CI: validator tests, ruff, structural check
- `docs/plans/` — implementation plans; `docs/plans/archive/` holds superseded
  design documents

## Commands
- Validate: `cd tools && uv run validate-marketplace ..`
- Test: `cd tools && uv run --extra dev pytest -v`
- Lint: `cd tools && uv run --extra dev ruff check .`

Run the validator before every commit. CI runs the same three commands.

## Conventions
- **Never put a tilde in a process argument.** `.mcp.json` args go to `execve`;
  `~` is not expanded and creates a literal `~` directory. The validator
  rejects this — a 131 MB Chrome profile once landed in the repo root this way.
- **`name` must match the directory** in both `plugin.json` and `SKILL.md`
  frontmatter. Validator-enforced.
- **Bump the plugin version on every skill change.** Skipping this has already
  forced a "bump to refresh cache" commit.
- **Every plugin directory must appear in `marketplace.json` and vice versa.**
  Validator-enforced.
- **Prefer a script to prose.** If a workflow is deterministic, write it in
  bash or Python under the plugin's `scripts/` and have the skill call it.
  Skills should carry decisions and sequence, not step-by-step instructions for
  running a CLI.
- British spelling in prose; US spelling in code identifiers.
- **No browser automation.** Every plugin uses an API or a local CLI. If a task seems to need Playwright, it is the wrong task — check whether a maintained library already solves it.

## External dependencies
**None.** No plugin here requires an MCP server or another plugin. The
validator's `validate_tool_dependencies` rule should report zero warnings — if
it ever reports one, a skill has picked up a dependency on an externally
installed plugin and that must be deliberate and documented, not accidental.

## Gotchas
- `ebook-processing` writes into `/Users/kenne/code/book-library`, which has its
  own `CLAUDE.md` and conventions (`source_folder` in `metadata.yaml`,
  `CATALOG.md` sync). Read that repo's guide before changing output shape.
- `pandoc` is not installed on this machine; WeasyPrint is. Do not add pandoc
  calls.
- `image-gen` v2 is API-based. Any instruction mentioning 45-second pacing or a
  four-image session cap is stale browser-path guidance.
