---
name: generate-image
description: Generate an image from a text prompt or a source file using the Gemini image API. Use when the user asks to create any image, picture, or visual. Returns a native-resolution PNG.
argument-hint: <prompt-text-or-file> [--aspect-ratio 16:9] [--output out.png]
user-invocable: true
allowed-tools: Read, Glob, Bash
---

# Image Generator

Generate images through the Gemini image API. A direct API call — no browser,
no login, no rate-limit pacing.

## Prerequisites

- `uv` on PATH (dependencies resolve automatically on first run).
- `GEMINI_API_KEY` set, on a billing account with credit.

If the key is unset, say so and stop. If a call fails with
`429 RESOURCE_EXHAUSTED`, the prepaid balance is exhausted — tell the user to
top up in AI Studio. Do not attempt any browser-based workaround; none exists
in this plugin any more.

## Arguments

- `$0` — inline prompt text, or a path to a text/markdown file to use as the
  prompt. Files over 32,000 characters are truncated, and the script says so.
- `--output` — output path. Defaults to `image.png` in the working directory,
  or `{source_stem}_image.png` beside a source file.
- `--aspect-ratio` — `16:9` (default), `1:1`, `9:16`, `4:3`, `3:4`, `2:3`,
  `3:2`, `4:5`, `5:4`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`.
- `--model` — override `NANOBANANA_MODEL` (default `gemini-2.5-flash-image`).

If no arguments are given, ask the user what to generate.

## Workflow

Run the generator and report the result. That is the whole skill.

```bash
uv run "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" "$PROMPT_OR_FILE" \
  --aspect-ratio "$ASPECT_RATIO" \
  --output "$OUTPUT_PATH"
```

It prints `Wrote <path> (<n> bytes)` and exits `0` on success. On failure it
prints the reason to stderr and exits `1`, writing no file.

Report the output path and size.

## Cost

Each image costs roughly $0.04 against a prepaid balance. Billing is prepaid
with auto-reload off, so spend cannot exceed the loaded credit. When
generating many images — a per-chapter batch, say — tell the user the count
and the approximate cost before starting.

## Error Handling

- **`finish_reason=NO_IMAGE`** — the model answered in text instead of drawing.
  Re-run with a more concretely visual prompt. Do not retry unchanged.
- **`finish_reason=IMAGE_SAFETY` / `IMAGE_PROHIBITED_CONTENT`** — blocked.
  Report it plainly and stop; do not reword around a safety block.
- **`429 RESOURCE_EXHAUSTED`** — prepaid balance exhausted. Stop and tell the
  user to top up.
- **Authentication errors** — `GEMINI_API_KEY` is missing or invalid.

No file is written on any failure. A missing file is the correct outcome.
