#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["google-genai>=1.33"]
# ///
"""Generate images via the Gemini image API.

Replaces the previous browser-automation approach, which captured a screenshot
of a rendered <img> element -- yielding 1024x559 crops of roughly 176 KB where
the API returns 1024x1024 native assets of roughly 830 KB, and failing about
14% of the time.

Requires GEMINI_API_KEY. Billing is prepaid with auto-reload off, so spend
cannot exceed the loaded balance.
"""

import os
import re
import sys
import time
from pathlib import Path

DEFAULT_MODEL = os.environ.get("NANOBANANA_MODEL", "gemini-2.5-flash-image")

# The pro image models return 503 "experiencing high demand" often enough that a
# single unretried call is roughly a coin flip. Without retry a 20-chapter
# infographic batch loses several chapters silently.
RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)
DEFAULT_MAX_ATTEMPTS = 4
BACKOFF_BASE_SECONDS = 2.0

# Seam for tests -- monkeypatched so the suite never actually waits.
_sleep = time.sleep


def _is_retryable(exc: BaseException) -> bool:
    """True when `exc` is a transient API failure worth retrying.

    Retries throttling and 5xx. Does NOT retry a `limit: 0` quota wall: that
    means the free tier (or an exhausted prepaid balance) allows zero requests
    for the model, so no amount of waiting will help and failing fast gives the
    user an actionable error instead of a slow one.
    """
    code = getattr(exc, "code", None)
    if not isinstance(code, int):
        match = re.search(r"\b(429|5\d\d)\b", str(exc))
        code = int(match.group(1)) if match else None

    if code not in RETRYABLE_STATUS_CODES:
        return False
    return "limit: 0" not in str(exc)

VALID_KINDS = ("image", "infographic")
VALID_STYLES = ("modern", "minimal", "abstract", "illustrated", "tech")

# Verified against the live API error message on 2026-07-29.
VALID_ASPECT_RATIOS = (
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1",
    "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
)

INFOGRAPHIC_TEMPLATE = """\
Create a single infographic image about the following.

Style: {style}, professional, clean.
Background: dark navy/blue.
Colours: bright and vibrant, chosen to read well on a dark background.
Layout: clear sections with icons, strong typographic hierarchy.
Constraint: do not depict any specific real people or public figures. Use \
abstract icons, symbols and conceptual imagery to represent all ideas and people.

Content:
{text}
"""


class ImageGenerationError(RuntimeError):
    """The model did not return an image."""


def build_prompt(text: str, *, kind: str = "image", style: str = "modern") -> str:
    """Build the model prompt.

    For kind="image" the caller's text is the prompt, passed through unchanged.
    For kind="infographic" it is wrapped in the house style.
    """
    if kind not in VALID_KINDS:
        raise ValueError(f"kind must be one of {VALID_KINDS}, got {kind!r}")
    if kind == "image":
        return text
    if style not in VALID_STYLES:
        raise ValueError(f"style must be one of {VALID_STYLES}, got {style!r}")
    return INFOGRAPHIC_TEMPLATE.format(style=style, text=text)


def _finish_reason(response) -> str | None:
    candidates = getattr(response, "candidates", None) or []
    if not candidates:
        return None
    reason = getattr(candidates[0], "finish_reason", None)
    return str(reason) if reason is not None else None


def generate(
    prompt: str,
    output: Path,
    *,
    aspect_ratio: str = "16:9",
    model: str | None = None,
    client=None,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
) -> Path:
    """Generate one image and write it to `output`.

    Transient API failures (503, throttling) are retried with exponential
    backoff up to `max_attempts`. A `limit: 0` quota wall, a safety block and a
    text-instead-of-image answer are all real outcomes, not transient, and fail
    immediately.

    Writes nothing on failure -- a missing file is a correct failure, whereas
    the browser path's habit of saving whatever was on screen silently
    corrupted the library with screenshots of prose.
    """
    from google.genai import types

    if aspect_ratio not in VALID_ASPECT_RATIOS:
        raise ValueError(
            f"aspect_ratio must be one of {VALID_ASPECT_RATIOS}, got {aspect_ratio!r}"
        )

    if client is None:
        from google import genai

        # google-genai also reads GOOGLE_API_KEY and prefers it over
        # GEMINI_API_KEY when both are set. This script's contract (see the
        # module docstring) is GEMINI_API_KEY, so the key is bound explicitly
        # here rather than left to genai.Client()'s own env lookup -- do not
        # "simplify" this back to a bare genai.Client() call.
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ImageGenerationError(
                "GEMINI_API_KEY is not set. Note that the google-genai SDK "
                "also reads GOOGLE_API_KEY and prefers it when both are set, "
                "so this script binds GEMINI_API_KEY explicitly to avoid "
                "silently picking up a different key."
            )
        client = genai.Client(api_key=api_key)

    model = model or DEFAULT_MODEL

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
    )

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model=model, contents=prompt, config=config
            )
            break
        # Broad by design: the SDK raises several unrelated exception types for
        # transient conditions. Anything _is_retryable() does not recognise is
        # re-raised untouched on the line below.
        except Exception as exc:
            if not _is_retryable(exc):
                raise
            if attempt == max_attempts:
                raise ImageGenerationError(
                    f"{model} still failing after {max_attempts} attempts: {exc}"
                ) from exc
            delay = BACKOFF_BASE_SECONDS ** (attempt - 1)
            print(
                f"Transient API error on attempt {attempt}/{max_attempts} "
                f"({exc}); retrying in {delay:.0f}s...",
                file=sys.stderr,
            )
            _sleep(delay)

    for part in getattr(response, "parts", None) or []:
        blob = getattr(part, "inline_data", None)
        data = getattr(blob, "data", None) if blob else None
        if data:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
            return output

    reason = _finish_reason(response) or "no image part in response"
    raise ImageGenerationError(
        f"Gemini returned no image (finish_reason={reason}). "
        f"NO_IMAGE means the model answered in text -- reword the prompt to be "
        f"more concretely visual. IMAGE_SAFETY and IMAGE_PROHIBITED_CONTENT "
        f"mean the request was blocked; do not attempt to reword around a "
        f"safety block."
    )


# Guard against accidentally passing a whole book as a prompt; it is not an API
# limit. The previous value of 3000 was inherited from the retired browser path,
# where the prompt was typed into a web chat textarea and long input was slow and
# unreliable. The API has no such constraint, so the cap is now generous enough
# to pass a full README or chapter through intact.
#
# Note this is a *safety* ceiling, not a target: very long infographic prompts
# raise the chance of finish_reason=NO_IMAGE (the model replying in text instead
# of drawing). For infographics, a focused summary still beats a long document.
MAX_SOURCE_CHARS = 32_000


def _looks_like_a_file(argument: str) -> Path | None:
    """Return the path if `argument` names an existing file, else None.

    Path.is_file() raises OSError(ENAMETOOLONG) rather than returning False when
    a path component exceeds the filesystem limit (255 bytes on macOS). A
    detailed image prompt easily exceeds that, so the probe must not assume the
    argument is path-shaped.
    """
    try:
        candidate = Path(argument).expanduser()
        return candidate if candidate.is_file() else None
    except (OSError, ValueError):
        return None


def _read_source(argument: str) -> str:
    """Return prompt text from `argument`, reading it as a file when it is one."""
    candidate = _looks_like_a_file(argument)
    if candidate is not None:
        text = candidate.read_text(encoding="utf-8", errors="replace")
        if len(text) > MAX_SOURCE_CHARS:
            print(f"Source is {len(text)} chars; using the first {MAX_SOURCE_CHARS}.")
            text = text[:MAX_SOURCE_CHARS]
        return text
    return argument


def _default_output(argument: str, kind: str) -> Path:
    candidate = _looks_like_a_file(argument)
    if candidate is not None:
        return candidate.parent / f"{candidate.stem}_{kind}.png"
    return Path.cwd() / f"{kind}.png"


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Generate an image with the Gemini API from inline text or a file."
    )
    parser.add_argument("source", help="Inline prompt text, or a path to a text/markdown file")
    parser.add_argument("--kind", choices=VALID_KINDS, default="image")
    parser.add_argument("--style", choices=VALID_STYLES, default="modern")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--aspect-ratio", default="16:9", choices=VALID_ASPECT_RATIOS)
    parser.add_argument("--model", default=None, help="Override NANOBANANA_MODEL")
    args = parser.parse_args(argv)

    prompt = build_prompt(_read_source(args.source), kind=args.kind, style=args.style)
    output = args.output or _default_output(args.source, args.kind)

    try:
        written = generate(
            prompt, output, aspect_ratio=args.aspect_ratio, model=args.model
        )
    except ImageGenerationError as exc:
        print(f"Image generation failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - surface auth/quota errors verbatim
        print(f"Image generation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {written} ({written.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
