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

from generate_image import (  # noqa: E402
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


from generate_image import main  # noqa: E402


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
    source.write_text("A" * 10_000)
    captured: dict = {}
    _stub(monkeypatch, captured)

    main([str(source), "--output", str(tmp_path / "r.png")])
    assert len(captured["prompt"]) <= 3200


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
