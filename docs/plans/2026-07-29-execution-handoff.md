# Execution Handoff — Marketplace Remediation

← [Back to Docs](../README.md)

Everything needed to pick up [the remediation plan](./2026-07-29-marketplace-remediation.md)
on another machine. Written on the MacBook Air, 2026-07-29, for continuation on
the Mac Mini.

## Status

**Nothing has been executed. No commits exist beyond this document and the plan.**

The plan was written, then revised four times as investigation invalidated its
assumptions. It is current and internally consistent: 16 tasks, 112 steps,
sequential numbering, no placeholders. The task loop has not started.

## How to resume

```bash
cd ~/code/kennys-ai-integrations
git pull
```

Then in Claude Code:

> Execute `docs/plans/2026-07-29-marketplace-remediation.md` using the
> superpowers:subagent-driven-development skill. Read
> `docs/plans/2026-07-29-execution-handoff.md` first for context and
> environment prerequisites.

**Decisions already made — do not re-litigate these:**

| Decision | Ruling |
|---|---|
| Workspace | **Work directly on `main`.** No worktree, no feature branch. Consent given explicitly. |
| `GEMINI_API_KEY` | Load via explicit source — see [API key](#the-gemini-api-key-needs-setting-by-hand) below. |
| Execution mode | Subagent-driven: fresh implementer per task, task review after each, broad review at the end. |

## Prerequisites to verify on the Mini

Run this before starting. The plan assumes each result.

```bash
for c in uv python3 calibre ebook-convert weasyprint pandoc gh jq node; do
  printf '%-16s ' "$c"; command -v $c >/dev/null 2>&1 && echo yes || echo NO
done
echo "EBOOK_LIBRARY_PATH=${EBOOK_LIBRARY_PATH:-<unset>}"
uv --version
```

Expected on the Air, and assumed by the plan:

- `uv`, `python3`, `calibre`, `ebook-convert`, `weasyprint`, `gh`, `jq`, `node` — **present**
- `pandoc` — **absent.** Tasks 14 and 15 depend on this; they replace `pandoc`
  calls with WeasyPrint. If the Mini *has* pandoc, that does not change the plan
  — the removal is still correct, because the Air does not.
- `EBOOK_LIBRARY_PATH=/Users/kenne/code/book-library`

If `calibre`/`weasyprint` are missing on the Mini, Phase 4 (Tasks 13–15) cannot
be smoke-tested there. Phases 0–3 are unaffected — do those first and report.

## The Gemini API key needs setting by hand

**This will bite otherwise.** `~/.zshrc.secrets` is excluded by name in
`mac-homedir/.gitignore` and is never synced — it must be created per machine
(see `~/README.md`, bootstrap step 2). The Mini therefore still holds the **old
free-tier key**, which returns:

```
429 RESOURCE_EXHAUSTED
limit: 0, model: gemini-2.5-flash-image
```

Gemini image generation is not merely rate-limited on the free tier — the quota
is **zero**.

On 2026-07-29 a prepaid Gemini billing account was set up (AI Studio, $10, hard
stop, auto-reload **off**) and a new key issued. Copy that key into the Mini's
`~/.zshrc.secrets`:

```bash
# ~/.zshrc.secrets  (0600, never committed)
export GEMINI_API_KEY=<the prepaid key>
```

Verify before running Phase 2:

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"a teal circle on dark navy"}]}],
       "generationConfig":{"responseModalities":["IMAGE"]}}' \
  | jq -r '.candidates[0].content.parts[]|select(.inlineData)|.inlineData.data' \
  | base64 -d > /tmp/keycheck.png && sips -g pixelWidth -g pixelHeight /tmp/keycheck.png
```

Expected: **1024×1024**. A `429` means the old key is still in place.

### Loading the key inside tooling

`zsh -lc` is a *non-interactive* login shell: it reads `.zprofile` but **not**
`.zshrc`, so it never sources `.zshrc.secrets` and silently inherits a stale
value. Use the explicit form in any script or smoke test:

```bash
export GEMINI_API_KEY="$(zsh -c 'source ~/.zshrc.secrets 2>/dev/null; printf "%s" "$GEMINI_API_KEY"')"
```

Interactive terminals are fine — they read `.zshrc` and get the right key.

## Machine-specific: Task 1 differs on the Mini

Task 1 deletes `./~` (a 131 MB stray Chrome profile) and `.playwright-mcp/`.
**Those are untracked artefacts that exist only on the MacBook Air.** They were
created by a tilde-in-argv bug in `plugins/image-gen/.mcp.json`, which passed
`--user-data-dir "~/Library/..."` — a path `execve` takes literally.

On the Mini, expect:

```bash
ls -d './~' .playwright-mcp 2>/dev/null || echo "not present — nothing to delete"
```

If absent, Task 1's deletion steps are no-ops. **Report that rather than
skipping the task** — the `.gitignore` guard rules and the two `.mcp.json`
removals are still required, and they are the parts that get committed.

The Air's copy must still be deleted there. It is untracked, so it will not
arrive via git.

## Why the plan says what it says

The plan was rewritten repeatedly as investigation contradicted it. The
reasoning is recorded so it is not re-derived or accidentally reversed.

### Image generation is Gemini API only

Every alternative was tested, not assumed:

| Route | Evidence | Outcome |
|---|---|---|
| OpenAI image models | Organization Verification requires government photo ID + live selfie, covering `gpt-image-2`, `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini` | **Refused by the repo owner. Permanently out of scope — do not propose it again.** |
| `dall-e-3` | API returns *"The model 'dall-e-3' does not exist"* | Retired by OpenAI |
| Gemini free tier | `429`, `limit: 0` | Zero quota, not a small one |
| Gemini prepaid | Live call → HTTP 200, **1024×1024, 850 KB PNG** | **Adopted** |
| Browser automation | 1024×**559** crops, ~176 KB median; 98 failure artefacts vs 581 successes in `book-library` (~14%) | Removed |

The browser path was not a naive choice — it was a correct reading of the
owner's cost constraints before prepaid Gemini billing existed. It is being
replaced because that constraint was lifted, not because it was wrong.

### No browser automation anywhere

By the end of the plan, `grep -rn 'mcp__\|playwright\|browser_' plugins/` must
return nothing. No MCP servers, no external plugin dependencies, no browser
profiles to keep logged in.

One deliberate exception: `download-acsm` drives Adobe Digital Editions via
`open -a`. That is a desktop app with a human in the loop, not browser
automation, and Adobe DRM redemption has no API to migrate to. It stays off the
default pipeline.

### Three plugins are retired, two replaced by better third-party work

- **`mermaid-diagrams`** → absorbed into the new `documentation-conventions`.
  Its original instruction to *always* hardcode a dark theme is a defect:
  GitHub, Obsidian and VS Code follow the reader's theme, so baked-in
  `fill:#1a3a5c` is unreadable in light mode. Theming becomes opt-in.
- **`notebooklm`** → [`notebooklm-py`](https://github.com/teng-lin/notebooklm-py)
  (MIT, ~18k stars, active). Calls NotebookLM's internal `batchexecute` RPC
  instead of scraping the DOM, and ships its own Claude Code skill. Google has
  no *consumer* NotebookLM API; the official one is enterprise-only via Google
  Cloud.
- **`dev-conventions`** → `uv init --lib` plus
  [`scientific-python/cookie`](https://github.com/scientific-python/cookie).
  `python-project-setup` carried eight defects against current tooling: `pip`
  with no lockfile, `./venv` instead of `.venv`, the deprecated `"python"`
  debugger type, the long-removed `python.pythonPath` setting, dev deps in
  `optional-dependencies` rather than PEP 735 `dependency-groups`, and no
  `py.typed`, `.python-version`, pre-commit or CI.

**Final roster: `image-gen`, `ebook-processing`, `documentation-conventions`.**

### Bugs found by inspection, encoded as tasks

Each was verified against the real `book-library` repo, not inferred:

- **`summarize-book`'s resume check never fires.** It globs
  `*_summary_claude_*`; the library holds **50** `anthropic`-tokened summaries
  and **1** `claude`. For 49 of 50 books it misses and regenerates a summary
  that already exists — a full book of context burned each time. (Task 15)
- **`metadata.yaml` omits `source_folder`**, which `book-library-mcp` keys off.
  Books written by the current `book-index` are unreachable through search.
  (Task 15)
- **`chapter-infographics` was structurally impossible.** One image per chapter,
  against the old browser rules of 45s apart and 4 per session. A 20-chapter
  book could not complete. Nobody noticed because the plugin was never enabled.
  (Task 14)
- **`CATALOG.md` is stale** — last touched a month before the repo's last
  commit, because no skill knew the sync rule existed. (Task 15)

## Outstanding / known risks

1. **Cross-plugin path traversal is unverified.** Task 14 calls
   `${CLAUDE_PLUGIN_ROOT}/../image-gen/scripts/generate_image.py` from
   `ebook-processing`. Both ship from this marketplace so they should install as
   siblings, but this was never confirmed against a real installation. If it
   fails at runtime, that is the reason.
2. **Three of five plugins are enabled locally, none of the retired ones.**
   `~/.claude/settings.json` enables `image-gen` and `dev-conventions`. After
   Tasks 10–12 the owner must enable `documentation-conventions` and remove
   `dev-conventions` and `notebooklm`. Reported by Tasks 10 and 11.
3. **The global `~/.claude/CLAUDE.md` will have a dangling reference.**
   Lines 18–19 name `markdown-conventions` and `python-project-setup`; the first
   moves plugin, the second is deleted. Task 11 Step 6 reports the replacement
   text rather than editing a file outside the repo.
4. **Every image now costs ~$0.04** against a $10 prepaid balance with
   auto-reload off. A 20-chapter book is roughly $0.80. Spend cannot exceed the
   balance; exhaustion surfaces as `429`.

## Cleanup deferred to the owner

`book-library` holds 34 `*.debug.png` and 64 `*.error.png` — residue from the
retired browser path.

```bash
cd ~/code/book-library
find . \( -name '*.debug.png' -o -name '*.error.png' \) -not -path './.git/*' | wc -l   # 98
```

Deleting them is a separate commit in a separate repo and is deliberately **not**
part of this plan — that repo commits large binaries on purpose and warns
against history-rewriting operations.

---

*Last Updated: 2026-07-29*
