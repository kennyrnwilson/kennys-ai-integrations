---
name: infographic
description: Generate a professional dark-themed infographic image from text or a file using the Gemini image API. Use when the user asks for an infographic or a visual summary of some content.
argument-hint: <source-file-or-text> [--style modern|minimal|abstract|illustrated|tech] [--output out.png]
user-invocable: true
allowed-tools: Read, Glob, Bash
---

# Infographic Generator

Generate a dark-themed infographic. Same engine as `generate-image`, with the
house infographic styling applied to the prompt.

## Prerequisites

`uv` on PATH and `GEMINI_API_KEY` set on a funded billing account. Same
failure modes as `generate-image`.

## Arguments

- `$0` — inline topic text, or a path to a markdown/text file to summarise.
  Files over 32,000 characters are truncated, and the script says so. That is a
  safety ceiling, not a target — long infographic prompts raise the chance of
  `NO_IMAGE`, so a focused summary still beats a long document here.
- `--style` — `modern` (default), `minimal`, `abstract`, `illustrated`, `tech`.
- `--output` — defaults to `{source_stem}_infographic.png` beside the source
  file, or `infographic.png` in the working directory.
- `--aspect-ratio` — `16:9` by default. Use `4:5` or `9:16` for portrait
  infographics, `1:1` for square.

## Applied Styling

The script wraps the content with: dark navy background, vibrant colours
chosen for dark backgrounds, clear sections with icons, strong typographic
hierarchy, and a constraint against depicting real people or public figures.

## Workflow

```bash
uv run "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" "$SOURCE" \
  --kind infographic \
  --style "$STYLE" \
  --aspect-ratio "$ASPECT_RATIO" \
  --output "$OUTPUT_PATH"
```

Report the output path and size.

## Batch Generation

There is no pacing requirement and no per-session cap — generate as many as
needed in a loop without sleeping. Any instruction mentioning 45 seconds
between images or a four-image session limit is stale guidance from the
removed browser path.

Do tell the user the count and approximate cost (~$0.04 each) before a large
batch.

## Error Handling

Same as `generate-image`, including its automatic retry of transient 503s. Long infographic prompts are refused more often than
short ones, so `NO_IMAGE` is more likely here — reword to be more concretely
visual rather than retrying unchanged.
