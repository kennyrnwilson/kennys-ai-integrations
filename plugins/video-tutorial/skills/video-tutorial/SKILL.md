---
name: video-tutorial
description: Turn a YouTube video into an illustrated markdown tutorial — summarise it into steps and illustrate each step with the best frame from the video, optionally edited with image-gen. Use when the user gives a YouTube link and asks for a tutorial, a how-to, a step-by-step summary, or a summary "with images" or "with frames".
argument-hint: <youtube-url> [output-dir]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Video Tutorial

Turn a YouTube video into a markdown tutorial whose images are real frames from
the video. The script does the mechanical work; you choose the steps and the
frames by reading the transcript and looking at contact sheets.

## Prerequisites

- `uv` and `ffmpeg` on PATH. If `ffmpeg` is missing, run `brew install ffmpeg`.
- For edited images only: the `image-gen` plugin and `GEMINI_API_KEY`.

## Inputs

- **URL** — any YouTube URL shape, or the bare video ID. If none is given, ask.
- **Output** — default `docs/<kebab-title>.md` in the current repo, with images
  in `docs/images/`. Create `docs/` if missing, and add the page to
  `docs/README.md` per the `markdown-conventions` skill.
- **A summary the user pasted** — treat it as a draft. Check every timestamp in
  it against the transcript; pasted summaries often have wrong or placeholder
  times and links. Say which ones you corrected.

## Resolve the script

```bash
VT_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
if [[ -z "$VT_ROOT" ]] && command -v codex >/dev/null 2>&1; then
  VT_ROOT="$(codex plugin list | awk \
    '$1 == "video-tutorial@kennys-ai-integrations" && $2 == "installed," && $3 == "enabled" {print $NF; exit}')"
fi
VF="$VT_ROOT/scripts/video_frames.py"
[[ -f "$VF" ]] || { echo "video-tutorial plugin root could not be resolved" >&2; exit 1; }
```

Use a work directory in the session scratchpad (or `$TMPDIR`), one per video:
`WORK=<scratchpad>/video-<id>`. It caches the download.

## Workflow

1. **Fetch.** `uv run "$VF" fetch "$URL" --dir "$WORK"`. This writes
   `video.mp4`, `meta.json` and `transcript.txt` (`[m:ss] text` lines). Read
   the transcript and metadata. If there is no transcript, say so and work from
   contact sheets alone.
2. **Find the steps.** From the transcript, decide the tutorial's steps and the
   time range in which each one is spoken. Speech usually leads the matching
   picture by a few seconds, so the range runs from when a step is introduced
   to when the next one starts.
3. **Look before choosing.** For each range (or one sheet covering all of
   them), run `uv run "$VF" sheet "$WORK" --start 0:13 --end 0:45` and Read the
   sheet image. Each cell is labelled with its time. Use `--fps 4` on a short
   range for fast movement. A sheet holds at most 64 frames.
4. **Choose one frame per step.** Prefer the frame that *shows* the step:
   - the body position the step describes, at its clearest
   - on-screen captions or step titles, when the video has them — they confirm
     the match
   - little motion blur, splash or occlusion
   - over the first frame where the step is mentioned
5. **Extract.** `uv run "$VF" frames "$WORK" --frame 0:18.5=<slug>-1-<step> ...
   --out-dir docs/images`. Name frames in kebab-case after the tutorial and
   step. Read the extracted frames together to check them before writing.
6. **Write the page** (structure below).
7. **Report** the page path, the images, any timestamps you corrected, and any
   step whose frame is weak (and why), so the user can ask for an edit.

## Page structure

```markdown
# <Tutorial title>

← [Back to Parent](./README.md)

Source: [<video title>](<url>) (<duration>), <channel>.

## 1. <Step name>

**Timestamp:** [m:ss](<url>&t=<seconds>s) (frame at m:ss)

![<what the frame shows, for alt text>](./images/<file>.jpg)

<What to do, in one or two sentences, in the imperative.>

- **Look for:** <the visual cue in the frame, and why it matters, from the video>
```

The timestamp link points to where the step starts in the video; "frame at"
gives the time of the picture. Write in the house style
(`communicate-clearly`). Keep claims to what the video says.

## Editing frames

When the user asks to change an image — "circle the knees", "remove the
caption", "add an arrow showing the rotation" — use `image-gen`'s
`generate-image` skill with the frame as the source:

```bash
uv run "$IMAGE_GEN_PLUGIN_ROOT/scripts/generate_image.py" \
  "<the change; say what to keep as well as what to change>" \
  --edit docs/images/<frame>.jpg --output docs/images/<frame>-annotated.png
```

`--edit` keeps the source's shape unless `--aspect-ratio` is given. Keep the
original frame and write the edit beside it, then point the page at the edit.
Each edit costs roughly USD 0.13; say the count and cost before a batch.
Generated edits can change details of the scene: check the result still shows
what the step describes before using it.

## Errors

- **`Sign in to confirm you're not a bot`** from `fetch` — YouTube blocked the
  download from this IP. Report it; do not add cookies without asking.
- **`no frame at m:ss`** — the time is past the end of the video.
- **No transcript** — normal for some videos; choose steps from contact sheets
  and the video's own captions.
