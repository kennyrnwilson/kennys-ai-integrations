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

## Model chain

The script tries models in order until one succeeds. Configure the chain in
`~/.zshrc` (not `~/.zshrc.secrets` — these are not secrets):

```
NANOBANANA_MODEL          # first choice  (default: gemini-3-pro-image)
NANOBANANA_MODEL_FALLBACK # second choice (default: gemini-3.1-flash-image)
NANOBANANA_MODEL_FALLBACK2# third choice  (default: gemini-2.5-flash-image)
```

The order is newest first: quality falls at each step, so a fallback is a
rescue that lets a batch finish, not a cheaper preference. Pro costs roughly
USD 0.13 an image against 0.04 for 2.5 flash.

Fallback only triggers on transient exhaustion (503 after all retries). Safety
blocks and `NO_IMAGE` propagate immediately without trying the next model.
`--model` bypasses the chain entirely and uses a single model with no fallback.

## Arguments

- **The prompt argument** — inline prompt text, or a path to a text/markdown file to use as the
  prompt. Files over 32,000 characters are truncated, and the script says so.
- `--output` — output path. Defaults to `image.png` in the working directory,
  or `{source_stem}_image.png` beside a source file.
- `--aspect-ratio` — `16:9` (default), `1:1`, `9:16`, `4:3`, `3:4`, `2:3`,
  `3:2`, `4:5`, `5:4`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`.
- `--model` — use a single specific model, bypassing the fallback chain entirely.

If no arguments are given, ask the user what to generate.

## Workflow

Run the generator and report the result. That is the whole skill. Resolve the
plugin root from Claude's compatibility variable when it exists. In Codex,
resolve it from the installed marketplace entry. Source the private shell
environment before checking the API key; never print the key.

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

uv run "$IMAGE_GEN_PLUGIN_ROOT/scripts/generate_image.py" "$PROMPT_OR_FILE" \
  --aspect-ratio "$ASPECT_RATIO" \
  --output "$OUTPUT_PATH"
```

It prints `Wrote <path> (<n> bytes)` and exits `0` on success. On failure it
prints the reason to stderr and exits `1`, writing no file.

Report the output path and size.

## Cost

Each image costs roughly USD 0.04 against a prepaid balance. Billing is prepaid
with auto-reload off, so spend cannot exceed the loaded credit. When
generating many images — a per-chapter batch, say — tell the user the count
and the approximate cost before starting.

## Error Handling

The script retries transient failures itself — **503 "experiencing high demand"
and throttling are retried up to 4 times with exponential backoff** (1s, 2s,
4s) per model. If all retries are exhausted, the script automatically tries the
next model in the chain (see **Model chain** above). Do not add your own retry
loop on top; if the script reports failure, all models in the chain are spent.

These are real outcomes, not transient, and fail immediately:

- **`finish_reason=NO_IMAGE`** — the model answered in text instead of drawing.
  Re-run with a more concretely visual prompt. Do not retry unchanged.
- **`finish_reason=IMAGE_SAFETY` / `IMAGE_PROHIBITED_CONTENT`** — blocked.
  Report it plainly and stop; do not reword around a safety block.
- **`429` with `limit: 0`** — a hard quota wall, not throttling: the prepaid
  balance is exhausted, or the key is on the free tier where image generation
  has zero quota. Stop and tell the user to top up. This is deliberately *not*
  retried, since waiting cannot help.
- **Authentication errors** — `GEMINI_API_KEY` is missing or invalid.

No file is written on any failure. A missing file is the correct outcome.
