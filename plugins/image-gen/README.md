# image-gen

← [Back to Marketplace](../../README.md)

Generate images and infographics through the Gemini image API.

## Skills

| Skill | Purpose |
|---|---|
| `generate-image` | Any image, from inline text or a source file |
| `infographic` | Dark-themed infographic from text or a file |

## Requirements

`uv` on PATH, and `GEMINI_API_KEY` set on a billing account with credit.
Dependencies resolve automatically via PEP 723 inline metadata — no install
step.

Optional: `NANOBANANA_MODEL` overrides the model (default
`gemini-2.5-flash-image`).

Billing is prepaid with auto-reload off, so spend cannot exceed the loaded
balance. When credit runs out, calls return `429 RESOURCE_EXHAUSTED` and no
image is produced.

## Why Gemini only

**OpenAI** image models require Organization Verification — government photo
ID plus a live selfie — covering the whole GPT Image family. Declined.
`dall-e-3` has been retired, so there is no unverified alternative.

## Why the API, not the browser

This plugin previously drove the Gemini and ChatGPT web interfaces with
Playwright. That approach captured a screenshot of a rendered `<img>` element
rather than downloading the asset:

| | Browser capture | API |
|---|---|---|
| Typical output | 1024×559 crop, ~176 KB | 1024×1024 native, ~830 KB |
| Failure rate | ~14% | Structured `finishReason` |
| Pacing | 45s apart, 4 per session | None |
| Terms of service | Outside both providers' terms | Supported |

The failure residue is still visible in the sibling `book-library` repo: 34
`*.debug.png` and 64 `*.error.png` files committed alongside 581 successes.

The browser implementation, including its `stealth.js` anti-detection script,
remains in git history if it is ever needed again.
