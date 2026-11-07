"""Tests for video_frames.py's pure helpers.

Run with:  uv run --with pytest pytest plugins/video-tutorial/scripts/test_video_frames.py -v
"""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from video_frames import (
    format_time,
    grid_shape,
    parse_frame_spec,
    parse_time,
    sheet_times,
    transcript_lines,
    video_id,
)


@pytest.mark.parametrize("url", [
    "https://www.youtube.com/watch?v=Se1j7U8EI2o",
    "https://www.youtube.com/watch?list=x&v=Se1j7U8EI2o&t=13s",
    "https://youtu.be/Se1j7U8EI2o?t=5",
    "https://www.youtube.com/shorts/Se1j7U8EI2o",
    "Se1j7U8EI2o",
])
def test_video_id_from_any_url_shape(url):
    assert video_id(url) == "Se1j7U8EI2o"


def test_video_id_rejects_a_url_without_one():
    with pytest.raises(ValueError):
        video_id("https://www.youtube.com/")


@pytest.mark.parametrize("text,seconds", [
    ("83.5", 83.5), ("1:23.5", 83.5), ("0:13", 13), ("1:01:23", 3683),
])
def test_parse_time(text, seconds):
    assert parse_time(text) == seconds


@pytest.mark.parametrize("text", ["", "a", "1::2", "1:2:3:4", "-5"])
def test_parse_time_rejects_nonsense(text):
    with pytest.raises(ValueError):
        parse_time(text)


@pytest.mark.parametrize("seconds,text", [
    (13, "0:13"), (18.5, "0:18.5"), (83.04, "1:23"), (59.96, "1:00"), (3683, "1:01:23"),
])
def test_format_time(seconds, text):
    assert format_time(seconds) == text


def test_sheet_times_steps_by_fps_and_includes_the_end():
    assert sheet_times(13, 15, 2) == [13, 13.5, 14, 14.5, 15]


def test_sheet_times_thins_a_long_range_to_the_cap():
    times = sheet_times(0, 600, 2, max_cells=64)
    assert len(times) == 64
    assert times[0] == 0 and times[-1] == 600


@pytest.mark.parametrize("start,end,fps", [(5, 5, 2), (5, 4, 2), (0, 10, 0)])
def test_sheet_times_rejects_an_empty_range(start, end, fps):
    with pytest.raises(ValueError):
        sheet_times(start, end, fps)


def test_parse_frame_spec_with_a_name():
    assert parse_frame_spec("0:18.5=flip-turn-1") == (18.5, "flip-turn-1")


def test_parse_frame_spec_names_a_bare_time_after_itself():
    assert parse_frame_spec("83.5") == (83.5, "frame-1-23-5")


def test_parse_frame_spec_rejects_a_name_that_is_not_kebab_case():
    with pytest.raises(ValueError):
        parse_frame_spec("12=../escape")


def test_transcript_lines_skip_blank_snippets():
    snippets = [SimpleNamespace(start=13.2, text="step one "), SimpleNamespace(start=14, text=" ")]
    assert transcript_lines(snippets) == ["[0:13] step one"]


@pytest.mark.parametrize("count,shape", [(1, (1, 1)), (8, (8, 1)), (9, (8, 2)), (64, (8, 8))])
def test_grid_shape(count, shape):
    assert grid_shape(count) == shape
