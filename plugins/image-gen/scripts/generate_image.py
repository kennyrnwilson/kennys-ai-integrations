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
from pathlib import Path

DEFAULT_MODEL = os.environ.get("NANOBANANA_MODEL", "gemini-2.5-flash-image")

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
) -> Path:
    """Generate one image and write it to `output`.

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

        client = genai.Client()

    model = model or DEFAULT_MODEL

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
        ),
    )

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
