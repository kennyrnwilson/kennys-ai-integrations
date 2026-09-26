---
name: infographic
description: Generate an expressive, readable infographic image from text or a file using the Gemini image API. Use when the user asks for an infographic or a visual summary of some content.
argument-hint: <source-file-or-text> [--style "art direction"] [--output out.png]
user-invocable: true
allowed-tools: Read, Glob, Bash
---

# Infographic Generator

Generate an infographic with the same Gemini engine as `generate-image`.
Let the subject and the user's brief determine the visual style.

## Prerequisites

`uv` on PATH and `GEMINI_API_KEY` set on a funded billing account. Same
failure modes as `generate-image`.

## Arguments

- **The source argument** — inline topic text, or a path to a markdown/text file to summarise.
  Files over 32,000 characters are truncated, and the script says so. That is a
  safety ceiling, not a target — long infographic prompts raise the chance of
  `NO_IMAGE`, so a focused summary still beats a long document here.
- `--style` — optional free-form art direction, such as `"illustrated science
  magazine, luminous depth"` or `"warm watercolour cutaway"`. Omit it to let Gemini
  choose. Existing values such as `modern`, `minimal`, `abstract`, `illustrated`
  and `tech` still work; they are suggestions, not a fixed menu.
- `--output` — defaults to `{source_stem}_infographic.png` beside the source
  file, or `infographic.png` in the working directory.
- `--aspect-ratio` — `16:9` by default. Use `4:5` or `9:16` for portrait
  infographics, `1:1` for square.

## Art direction

Give Gemini the subject, exact labels and relationships, plus any user-selected
style or reference. Leave composition, illustration, lighting and depth open
unless a particular arrangement carries meaning, such as an Euler diagram.

Do not impose a dark palette, flat boxes, thin arrows or minimal decoration by
default. Legibility does not require plainness: allow expressive imagery while
keeping labels readable and connections accurate. Respect an explicit request
for minimalism just as you would an illustrated style. Inspect the result for
missing labels and misleading connections before delivery.

## Workflow

Resolve the plugin root and private API-key environment in the same way as the
`generate-image` skill. Never print the key.

```bash
IMAGE_GEN_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
if [[ -z "$IMAGE_GEN_PLUGIN_ROOT" ]] && command -v codex >/dev/null 2>&1; then
  IMAGE_GEN_PLUGIN_ROOT="$(codex plugin list | awk \
    '$1 == "image-gen@kennys-ai-integrations" && $2 == "installed," && $3 == "enabled" {print $NF; exit}')"
fi
if [[ -z "$IMAGE_GEN_PLUGIN_ROOT" || ! -f "$IMAGE_GEN_PLUGIN_ROOT/scripts/generate_image.py" ]]; then
  echo "image-gen plugin root could not be resolved" >&2
  exit 1
fi
if [[ -f "$HOME/.zshrc.secrets" ]]; then
  source "$HOME/.zshrc.secrets"
fi
if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "GEMINI_API_KEY is missing" >&2
  exit 1
fi

uv run "$IMAGE_GEN_PLUGIN_ROOT/scripts/generate_image.py" "$SOURCE" \
  --kind infographic \
  --aspect-ratio "$ASPECT_RATIO" \
  --output "$OUTPUT_PATH"
```

Add `--style "your art direction"` only when a style has been chosen.
Report the output path and size.

## Batch Generation

There is no pacing requirement and no per-session cap — generate as many as
needed in a loop without sleeping. Any instruction mentioning 45 seconds
between images or a four-image session limit is stale guidance from the
removed browser path.

Do tell the user the count and approximate cost (~USD 0.04 each) before a large
batch.

## Error Handling

Same as `generate-image`, including its automatic retry of transient 503s. Long infographic prompts are refused more often than
short ones, so `NO_IMAGE` is more likely here — reword to be more concretely
visual rather than retrying unchanged.
