"""Tests for generate_image.py.

Run with:  uv run --with pytest --with google-genai pytest plugins/image-gen/scripts/test_generate_image.py -v

(google-genai must be installed alongside pytest: generate() imports
google.genai.types even when a FakeClient is injected, and the tests
construct/inspect real google.genai.types objects.)
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from generate_image import (
    MAX_SOURCE_CHARS,
    VALID_ASPECT_RATIOS,
    ImageGenerationError,
    build_prompt,
    generate,
)

PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"fake image data"


class FakePart:
    def __init__(self, data: bytes | None):
        self.inline_data = type("Blob", (), {"data": data})() if data else None


class FakeResponse:
    def __init__(self, parts=None, finish_reason=None):
        self.parts = parts or []
        candidate = type("Candidate", (), {"finish_reason": finish_reason})()
        self.candidates = [candidate]


class FakeModels:
    def __init__(self, response):
        self._response = response
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return self._response


class FakeClient:
    def __init__(self, response):
        self.models = FakeModels(response)


def test_build_prompt_passes_plain_text_through_for_images():
    assert build_prompt("a dancing dog in a park", kind="image") == "a dancing dog in a park"


def test_build_prompt_adds_infographic_styling():
    result = build_prompt("benefits of remote work", kind="infographic", style="minimal")
    assert "benefits of remote work" in result
    assert "infographic" in result.lower()
    assert "minimal" in result
    assert "dark navy" in result.lower()


def test_build_prompt_forbids_depicting_real_people_in_infographics():
    result = build_prompt("history of aviation", kind="infographic")
    assert "real people" in result.lower() or "public figures" in result.lower()


def test_build_prompt_rejects_an_unknown_kind():
    with pytest.raises(ValueError, match="kind"):
        build_prompt("x", kind="nonsense")


def test_build_prompt_rejects_an_unknown_style():
    with pytest.raises(ValueError, match="style"):
        build_prompt("x", kind="infographic", style="neon-brutalist")


def test_generate_writes_the_returned_bytes(tmp_path: Path):
    client = FakeClient(FakeResponse(parts=[FakePart(PNG_BYTES)]))
    out = tmp_path / "result.png"

    assert generate("a prompt", out, client=client) == out
    assert out.read_bytes() == PNG_BYTES


def test_generate_passes_model_and_aspect_ratio(tmp_path: Path):
    client = FakeClient(FakeResponse(parts=[FakePart(PNG_BYTES)]))
    generate("p", tmp_path / "o.png", aspect_ratio="9:16",
             model="gemini-2.5-flash-image", client=client)

    call = client.models.calls[0]
    assert call["model"] == "gemini-2.5-flash-image"
    assert call["config"].image_config.aspect_ratio == "9:16"


def test_generate_rejects_an_invalid_aspect_ratio(tmp_path: Path):
    client = FakeClient(FakeResponse(parts=[FakePart(PNG_BYTES)]))
    with pytest.raises(ValueError, match="aspect_ratio"):
        generate("p", tmp_path / "o.png", aspect_ratio="99:1", client=client)


def test_every_documented_aspect_ratio_is_accepted(tmp_path: Path):
    for ratio in VALID_ASPECT_RATIOS:
        client = FakeClient(FakeResponse(parts=[FakePart(PNG_BYTES)]))
        generate("p", tmp_path / f"{ratio.replace(':', '-')}.png",
                 aspect_ratio=ratio, client=client)


def test_generate_raises_when_the_model_answered_in_text(tmp_path: Path):
    client = FakeClient(FakeResponse(parts=[FakePart(None)], finish_reason="NO_IMAGE"))
    with pytest.raises(ImageGenerationError, match="NO_IMAGE"):
        generate("p", tmp_path / "o.png", client=client)


def test_generate_raises_on_a_safety_block(tmp_path: Path):
    client = FakeClient(FakeResponse(parts=[], finish_reason="IMAGE_SAFETY"))
    with pytest.raises(ImageGenerationError, match="IMAGE_SAFETY"):
        generate("p", tmp_path / "o.png", client=client)


def test_generate_writes_no_file_when_it_fails(tmp_path: Path):
    client = FakeClient(FakeResponse(parts=[], finish_reason="NO_IMAGE"))
    out = tmp_path / "should-not-exist.png"
    with pytest.raises(ImageGenerationError):
        generate("p", out, client=client)
    assert not out.exists()


def test_generate_creates_missing_parent_directories(tmp_path: Path):
    client = FakeClient(FakeResponse(parts=[FakePart(PNG_BYTES)]))
    out = tmp_path / "nested" / "deeper" / "result.png"
    generate("p", out, client=client)
    assert out.exists()


def test_generate_requires_gemini_api_key_when_no_client_is_injected(tmp_path, monkeypatch):
    # google-genai also reads GOOGLE_API_KEY and prefers it when both are
    # set, so without GEMINI_API_KEY this must fail fast and by name --
    # never fall through to a network call using some other ambient key.
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    out = tmp_path / "should-not-exist.png"
    with pytest.raises(ImageGenerationError, match="GEMINI_API_KEY"):
        generate("p", out)
    assert not out.exists()


from generate_image import main


def _stub(monkeypatch, captured: dict):
    def fake_generate(prompt, output, **kwargs):
        captured["prompt"] = prompt
        captured["output"] = output
        captured.update(kwargs)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(PNG_BYTES)
        return output

    monkeypatch.setattr("generate_image.generate", fake_generate)


def test_cli_reads_a_prompt_from_a_file(tmp_path: Path, monkeypatch):
    source = tmp_path / "notes.md"
    source.write_text("# Remote work\n\nSome content about remote work.")
    out = tmp_path / "result.png"
    captured: dict = {}
    _stub(monkeypatch, captured)

    assert main([str(source), "--output", str(out)]) == 0
    assert out.exists()
    assert "Remote work" in captured["prompt"]


def test_cli_treats_a_non_path_argument_as_inline_text(tmp_path: Path, monkeypatch):
    captured: dict = {}
    _stub(monkeypatch, captured)

    assert main(["a dancing dog in a park", "--output", str(tmp_path / "r.png")]) == 0
    assert captured["prompt"] == "a dancing dog in a park"


def test_cli_applies_infographic_styling_when_requested(tmp_path: Path, monkeypatch):
    captured: dict = {}
    _stub(monkeypatch, captured)

    main(["remote work", "--kind", "infographic", "--style", "tech",
          "--output", str(tmp_path / "r.png")])
    assert "infographic" in captured["prompt"].lower()
    assert "tech" in captured["prompt"]


def test_cli_forwards_the_aspect_ratio(tmp_path: Path, monkeypatch):
    captured: dict = {}
    _stub(monkeypatch, captured)

    main(["x", "--aspect-ratio", "1:1", "--output", str(tmp_path / "r.png")])
    assert captured["aspect_ratio"] == "1:1"


def test_cli_truncates_very_long_source_files(tmp_path: Path, monkeypatch):
    source = tmp_path / "big.md"
    source.write_text("A" * (MAX_SOURCE_CHARS * 2))
    captured: dict = {}
    _stub(monkeypatch, captured)

    main([str(source), "--output", str(tmp_path / "r.png")])
    assert len(captured["prompt"]) == MAX_SOURCE_CHARS


def test_cli_does_not_truncate_a_source_within_the_limit(tmp_path: Path, monkeypatch):
    # A full README-sized document must survive intact. The old 3000-char cap,
    # inherited from the retired browser path, silently cut documents mid-sentence.
    body = "B" * (MAX_SOURCE_CHARS - 1)
    source = tmp_path / "readme.md"
    source.write_text(body)
    captured: dict = {}
    _stub(monkeypatch, captured)

    main([str(source), "--output", str(tmp_path / "r.png")])
    assert captured["prompt"] == body


def test_cli_defaults_output_beside_a_source_file(tmp_path: Path, monkeypatch):
    source = tmp_path / "notes.md"
    source.write_text("content")
    captured: dict = {}
    _stub(monkeypatch, captured)

    main([str(source), "--kind", "infographic"])
    assert captured["output"] == tmp_path / "notes_infographic.png"


def test_cli_returns_nonzero_and_reports_when_generation_fails(
    tmp_path: Path, monkeypatch, capsys
):
    def fake_generate(prompt, output, **kwargs):
        raise ImageGenerationError("finish_reason=NO_IMAGE")

    monkeypatch.setattr("generate_image.generate", fake_generate)

    assert main(["x", "--output", str(tmp_path / "o.png")]) == 1
    assert "NO_IMAGE" in capsys.readouterr().err


# --- Retry on transient API failures -----------------------------------------
#
# gemini-3-pro-image returns 503 "experiencing high demand" often enough that a
# single unretried call is roughly a coin flip. Without retry, a 20-chapter
# infographic batch loses several chapters silently.

from generate_image import (
    DEFAULT_MAX_ATTEMPTS,
    RETRYABLE_STATUS_CODES,
    _is_retryable,
)


class FakeAPIError(Exception):
    """Stands in for google.genai.errors.APIError, which carries a .code."""

    def __init__(self, code: int, message: str = ""):
        super().__init__(f"{code} {message}")
        self.code = code


class FlakyModels:
    """Raises the queued exceptions in order, then returns the response."""

    def __init__(self, response, failures):
        self._response = response
        self._failures = list(failures)
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self._failures:
            raise self._failures.pop(0)
        return self._response


class FlakyClient:
    def __init__(self, response, failures):
        self.models = FlakyModels(response, failures)


@pytest.fixture
def no_sleep(monkeypatch):
    """Record backoff delays instead of actually waiting."""
    delays = []
    monkeypatch.setattr("generate_image._sleep", delays.append)
    return delays


def test_503_is_retryable():
    assert _is_retryable(FakeAPIError(503, "UNAVAILABLE high demand")) is True


def test_throttling_429_is_retryable():
    assert _is_retryable(FakeAPIError(429, "RESOURCE_EXHAUSTED retry in 33s")) is True


def test_quota_wall_429_is_not_retryable():
    # "limit: 0" is a hard wall (free tier / exhausted balance), not throttling.
    # Retrying cannot succeed, so it must fail fast.
    exc = FakeAPIError(429, "RESOURCE_EXHAUSTED ... limit: 0, model: gemini-3-pro-image")
    assert _is_retryable(exc) is False


def test_client_errors_are_not_retryable():
    assert _is_retryable(FakeAPIError(400, "INVALID_ARGUMENT")) is False
    assert _is_retryable(FakeAPIError(403, "PERMISSION_DENIED")) is False


def test_retryable_codes_cover_the_transient_5xx_range():
    for code in (500, 502, 503, 504):
        assert code in RETRYABLE_STATUS_CODES


def test_status_code_is_read_from_the_message_when_there_is_no_code_attribute():
    assert _is_retryable(RuntimeError("ServerError: 503 UNAVAILABLE")) is True
    assert _is_retryable(RuntimeError("ClientError: 400 INVALID_ARGUMENT")) is False


def test_generate_retries_a_503_then_succeeds(tmp_path: Path, no_sleep):
    client = FlakyClient(
        FakeResponse(parts=[FakePart(PNG_BYTES)]), [FakeAPIError(503, "UNAVAILABLE")]
    )
    out = tmp_path / "r.png"

    assert generate("p", out, client=client) == out
    assert out.read_bytes() == PNG_BYTES
    assert len(client.models.calls) == 2
    assert len(no_sleep) == 1


def test_generate_backs_off_exponentially(tmp_path: Path, no_sleep):
    client = FlakyClient(
        FakeResponse(parts=[FakePart(PNG_BYTES)]),
        [FakeAPIError(503), FakeAPIError(503), FakeAPIError(503)],
    )
    generate("p", tmp_path / "r.png", client=client)
    assert no_sleep == sorted(no_sleep), "delays must be non-decreasing"
    assert no_sleep[-1] > no_sleep[0], "backoff must actually grow"


def test_generate_gives_up_after_max_attempts(tmp_path: Path, no_sleep):
    client = FlakyClient(FakeResponse(), [FakeAPIError(503)] * 10)
    out = tmp_path / "r.png"

    with pytest.raises(ImageGenerationError, match="503"):
        generate("p", out, client=client)

    assert len(client.models.calls) == DEFAULT_MAX_ATTEMPTS
    assert not out.exists(), "no file may be written on failure"


def test_generate_does_not_retry_a_non_retryable_error(tmp_path: Path, no_sleep):
    client = FlakyClient(FakeResponse(), [FakeAPIError(400, "INVALID_ARGUMENT")] * 5)

    with pytest.raises(Exception, match="400"):
        generate("p", tmp_path / "r.png", client=client)

    assert len(client.models.calls) == 1, "must fail on the first attempt"
    assert no_sleep == []


def test_generate_does_not_retry_a_quota_wall(tmp_path: Path, no_sleep):
    client = FlakyClient(FakeResponse(), [FakeAPIError(429, "limit: 0, model: x")] * 5)

    with pytest.raises(Exception, match="429"):
        generate("p", tmp_path / "r.png", client=client)

    assert len(client.models.calls) == 1
    assert no_sleep == []


def test_max_attempts_is_configurable(tmp_path: Path, no_sleep):
    client = FlakyClient(FakeResponse(), [FakeAPIError(503)] * 10)

    with pytest.raises(ImageGenerationError):
        generate("p", tmp_path / "r.png", client=client, max_attempts=2)

    assert len(client.models.calls) == 2


def test_no_image_is_still_not_retried(tmp_path: Path, no_sleep):
    # A text answer is a real outcome, not a transient failure.
    client = FlakyClient(FakeResponse(parts=[], finish_reason="NO_IMAGE"), [])

    with pytest.raises(ImageGenerationError, match="NO_IMAGE"):
        generate("p", tmp_path / "r.png", client=client)

    assert len(client.models.calls) == 1
    assert no_sleep == []


# --- Long prompts are not paths ----------------------------------------------
#
# Path.is_file() raises OSError(errno 63, "File name too long") rather than
# returning False when a path component exceeds the filesystem limit (255 bytes
# on macOS/APFS). A detailed image prompt easily exceeds that, so the naive
# is_file() probe crashed on exactly the prompts users are most likely to write.

from generate_image import _default_output, _read_source

LONG_PROMPT = (
    "A dramatic Scottish Highlands landscape at golden hour: a still loch "
    "reflecting steep heather-covered mountains, with a weathered stone castle "
    "on a rocky promontory at the water's edge. Low mist drifting across the "
    "glen, moody overcast sky breaking into warm light. Photorealistic, wide "
    "cinematic composition."
)


def test_long_prompt_is_treated_as_inline_text_not_a_path():
    assert len(LONG_PROMPT) > 255, "fixture must exceed the filesystem name limit"
    assert _read_source(LONG_PROMPT) == LONG_PROMPT


def test_long_prompt_does_not_break_default_output_naming(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert _default_output(LONG_PROMPT, "image") == tmp_path / "image.png"


def test_a_real_file_is_still_read(tmp_path: Path):
    f = tmp_path / "prompt.txt"
    f.write_text("contents from the file")
    assert _read_source(str(f)) == "contents from the file"


def test_short_non_path_text_is_still_inline(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert _read_source("a dancing dog") == "a dancing dog"
    assert _default_output("a dancing dog", "infographic") == tmp_path / "infographic.png"
