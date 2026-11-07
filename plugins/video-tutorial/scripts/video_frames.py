#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["yt-dlp>=2025.1", "youtube-transcript-api>=1.2", "pillow>=11"]
# ///
"""Fetch a YouTube video and pull frames from it for an illustrated tutorial.

Three subcommands, run in this order:

    fetch URL --dir DIR        download the video (720p at most), metadata and a
                               timestamped transcript into DIR
    sheet DIR --start --end    a contact sheet: a grid of frames, each labelled
                               with its time, to look at before choosing frames
    frames DIR --frame T=NAME  full-resolution frames at chosen times

Needs `ffmpeg` on PATH. The work directory is a cache: `fetch` skips the
download when DIR already holds the video.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VIDEO_NAME = "video.mp4"
META_NAME = "meta.json"
TRANSCRIPT_NAME = "transcript.txt"
MAX_SHEET_CELLS = 64
CELL_WIDTH = 320

_ID_PATTERN = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})")


# --- pure helpers (tested) --------------------------------------------------


def video_id(url_or_id: str) -> str:
    """The 11-character video ID from a YouTube URL, or the ID itself."""
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    match = _ID_PATTERN.search(url_or_id)
    if not match:
        raise ValueError(f"no YouTube video ID in {url_or_id!r}")
    return match.group(1)


def parse_time(text: str) -> float:
    """Seconds from '83.5', '1:23.5' or '1:01:23'."""
    parts = text.strip().split(":")
    if not 1 <= len(parts) <= 3 or any(p == "" for p in parts):
        raise ValueError(f"not a time: {text!r}")
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + float(part)
    if seconds < 0:
        raise ValueError(f"not a time: {text!r}")
    return seconds


def format_time(seconds: float) -> str:
    """'m:ss' or 'm:ss.s' when the time is not a whole second; 'h:mm:ss' past an hour."""
    whole = int(seconds)
    tenths = round((seconds - whole) * 10)
    if tenths == 10:
        whole, tenths = whole + 1, 0
    hours, rest = divmod(whole, 3600)
    minutes, secs = divmod(rest, 60)
    text = f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"
    return f"{text}.{tenths}" if tenths else text


def sheet_times(start: float, end: float, fps: float, max_cells: int = MAX_SHEET_CELLS) -> list[float]:
    """Evenly spaced times from start up to end, thinned to at most max_cells."""
    if end <= start:
        raise ValueError("end must be after start")
    if fps <= 0:
        raise ValueError("fps must be positive")
    step = 1 / fps
    count = int((end - start) / step + 1e-9) + 1
    if count > max_cells:
        step = (end - start) / (max_cells - 1)
        count = max_cells
    return [round(start + i * step, 2) for i in range(count)]


def parse_frame_spec(spec: str) -> tuple[float, str]:
    """'18.5=flip-turn-1' -> (18.5, 'flip-turn-1'); a bare time names itself."""
    time_text, _, name = spec.partition("=")
    seconds = parse_time(time_text)
    name = name.strip() or "frame-" + re.sub(r"[:.]", "-", format_time(seconds))
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise ValueError(f"frame name must be kebab-case: {name!r}")
    return seconds, name


def transcript_lines(snippets) -> list[str]:
    """'[m:ss] text' lines from objects with .start and .text."""
    return [f"[{format_time(int(s.start))}] {s.text.strip()}" for s in snippets if s.text.strip()]


def grid_shape(count: int) -> tuple[int, int]:
    """(columns, rows) for a near-square-by-width grid of 16:9 cells."""
    cols = min(8, max(1, count))
    rows = -(-count // cols)
    return cols, rows


# --- side effects ------------------------------------------------------------


def _need_ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        sys.exit("ffmpeg is not on PATH. Install it with: brew install ffmpeg")
    return path


def _grab(ffmpeg: str, video: Path, seconds: float, out: Path, width: int | None = None) -> None:
    command = [ffmpeg, "-loglevel", "error", "-y", "-ss", f"{seconds}", "-i", str(video),
               "-frames:v", "1", "-q:v", "3"]
    if width:
        command += ["-vf", f"scale={width}:-2"]
    subprocess.run(command + [str(out)], check=True)
    if not out.exists():
        raise RuntimeError(f"no frame at {format_time(seconds)}; is it past the end of the video?")


def _load(work: Path) -> tuple[Path, dict]:
    video = work / VIDEO_NAME
    if not video.exists():
        sys.exit(f"{video} is missing. Run: fetch URL --dir {work}")
    meta = json.loads((work / META_NAME).read_text()) if (work / META_NAME).exists() else {}
    return video, meta


def cmd_fetch(args) -> int:
    from yt_dlp import YoutubeDL

    vid = video_id(args.url)
    work: Path = args.dir
    work.mkdir(parents=True, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={vid}"

    options = {
        "format": "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/b[height<=720]/b",
        "merge_output_format": "mp4",
        "outtmpl": str(work / "video.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=not (work / VIDEO_NAME).exists())
    meta = {
        "id": vid,
        "url": url,
        "title": info.get("title"),
        "channel": info.get("channel") or info.get("uploader"),
        "duration": info.get("duration"),
        "width": info.get("width"),
        "height": info.get("height"),
    }
    (work / META_NAME).write_text(json.dumps(meta, indent=2) + "\n")

    transcript_note = ""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        fetched = YouTubeTranscriptApi().fetch(vid, languages=[args.language, "en"])
        (work / TRANSCRIPT_NAME).write_text("\n".join(transcript_lines(fetched)) + "\n")
        transcript_note = f"transcript: {work / TRANSCRIPT_NAME}"
    except Exception as exc:  # noqa: BLE001 - no transcript is a normal outcome
        transcript_note = f"transcript: none ({type(exc).__name__})"

    print(f"{meta['title']} ({format_time(meta['duration'] or 0)})")
    print(f"video: {work / VIDEO_NAME}")
    print(transcript_note)
    return 0


def cmd_sheet(args) -> int:
    from PIL import Image, ImageDraw, ImageFont

    ffmpeg = _need_ffmpeg()
    video, meta = _load(args.dir)
    end = args.end if args.end is not None else float(meta.get("duration") or 0)
    times = sheet_times(args.start, end, args.fps)

    with tempfile.TemporaryDirectory() as tmp:
        cells = []
        for i, t in enumerate(times):
            out = Path(tmp) / f"{i:03d}.jpg"
            try:
                _grab(ffmpeg, video, t, out, width=CELL_WIDTH)
            except RuntimeError:
                break
            cells.append((t, Image.open(out).convert("RGB")))
        if not cells:
            sys.exit("no frames in that range")

        cell_w, cell_h = cells[0][1].size
        cols, rows = grid_shape(len(cells))
        sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "black")
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.load_default(size=22)
        for i, (t, image) in enumerate(cells):
            x, y = (i % cols) * cell_w, (i // cols) * cell_h
            sheet.paste(image, (x, y))
            label = format_time(t)
            box = draw.textbbox((x + 6, y + 4), label, font=font)
            draw.rectangle((box[0] - 4, box[1] - 2, box[2] + 4, box[3] + 2), fill="black")
            draw.text((x + 6, y + 4), label, fill="yellow", font=font)

    out = args.out or args.dir / f"sheet-{format_time(args.start)}-{format_time(end)}.jpg".replace(":", "_")
    sheet.save(out, quality=85)
    print(f"Wrote {out} ({len(cells)} frames, {format_time(cells[0][0])}-{format_time(cells[-1][0])})")
    return 0


def cmd_frames(args) -> int:
    ffmpeg = _need_ffmpeg()
    video, _ = _load(args.dir)
    specs = [parse_frame_spec(s) for s in args.frame]
    out_dir: Path = args.out_dir or args.dir
    out_dir.mkdir(parents=True, exist_ok=True)
    for seconds, name in specs:
        out = out_dir / f"{name}.jpg"
        _grab(ffmpeg, video, seconds, out, width=args.width)
        print(f"Wrote {out} ({format_time(seconds)})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="download video, metadata and transcript")
    fetch.add_argument("url")
    fetch.add_argument("--dir", type=Path, required=True)
    fetch.add_argument("--language", default="en")
    fetch.set_defaults(run=cmd_fetch)

    sheet = sub.add_parser("sheet", help="contact sheet of labelled frames")
    sheet.add_argument("dir", type=Path)
    sheet.add_argument("--start", type=parse_time, default=0.0)
    sheet.add_argument("--end", type=parse_time, default=None, help="defaults to the end of the video")
    sheet.add_argument("--fps", type=float, default=2.0, help=f"thinned to {MAX_SHEET_CELLS} frames at most")
    sheet.add_argument("--out", type=Path, default=None)
    sheet.set_defaults(run=cmd_sheet)

    frames = sub.add_parser("frames", help="full-resolution frames at chosen times")
    frames.add_argument("dir", type=Path)
    frames.add_argument("--frame", action="append", required=True, metavar="TIME[=NAME]")
    frames.add_argument("--out-dir", type=Path, default=None)
    frames.add_argument("--width", type=int, default=None, help="scale to this width; default keeps the source size")
    frames.set_defaults(run=cmd_frames)

    args = parser.parse_args(argv)
    try:
        return args.run(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
