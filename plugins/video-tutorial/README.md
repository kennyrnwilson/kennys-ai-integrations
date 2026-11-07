# video-tutorial

← [Back to Marketplace](../../README.md)

Turn a YouTube video into an illustrated markdown tutorial. The skill reads the
transcript, picks the steps, looks at contact sheets of the video and chooses
the frame that best shows each step. The `image-gen` plugin's `--edit` option
can then annotate or change a frame. Works in Claude Code and Codex.

## Skills

| Skill | Purpose |
|---|---|
| `video-tutorial` | YouTube URL to a markdown tutorial illustrated with frames |

## Script

`scripts/video_frames.py`, run with `uv run`:

| Command | Does |
|---|---|
| `fetch URL --dir DIR` | Downloads the video (720p at most), `meta.json` and a timestamped `transcript.txt` |
| `sheet DIR --start --end [--fps]` | A contact sheet: up to 64 frames in a grid, each labelled with its time |
| `frames DIR --frame TIME=NAME ...` | Full-resolution frames at chosen times |

## Requirements

`uv` and `ffmpeg` on PATH. Python dependencies (`yt-dlp`,
`youtube-transcript-api`, `pillow`) resolve automatically via PEP 723 inline
metadata.

Tests: `uv run --with pytest pytest plugins/video-tutorial/scripts/test_video_frames.py -v`
