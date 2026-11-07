---
name: video-tutorial
description: Turn a YouTube video into an illustrated markdown tutorial — summarise it into steps and illustrate each step with the best frame from the video, optionally edited with image-gen. Use when the user gives a YouTube link and asks for a tutorial, a how-to, a step-by-step summary, or a summary "with images" or "with frames".
argument-hint: <youtube-url> [output-dir]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Video Tutorial

Turn a YouTube video into a markdown tutorial whose images are real frames from
the video. Tools do the mechanical work; you choose the steps and the frames by
reading the transcript and looking at contact sheets.

## Choose a route

The same work can run in two places. Use the first one that is available.

1. **MCP tools.** The `youtube` MCP server, usually through the personal MCP
   portal, has `get_contact_sheet` and `get_frames`. Its tool names carry a
   prefix that depends on the client, such as `youtube_get_frames`. This route
   needs no local install and works in cloud sessions and chat. Use it when
   both tools are available.
2. **Local script.** `scripts/video_frames.py`, on a Mac with `uv` and
   `ffmpeg`. Use it when the MCP tools are missing, when they report `blocked`,
   or for a video longer than one hour, which the MCP server refuses.

Say which route you used in the report.

## Inputs

- **URL** — any YouTube URL shape, or the bare video ID. If none is given, ask.
- **Output** — default `docs/<kebab-title>.md` in the current repo, with images
  in `docs/images/`. Create `docs/` if missing, and add the page to
  `docs/README.md` per the `markdown-conventions` skill.
- **A summary the user pasted** — treat it as a draft. Check every timestamp in
  it against the transcript; pasted summaries often have wrong or placeholder
  times and links. Say which ones you corrected.

## Workflow

The steps are the same on both routes. Only the commands differ; each step
gives the MCP tool first and the local command second.

1. **Fetch the transcript.**
   - MCP: `get_video_metadata`, then `get_transcript` with `timestamps=true`.
     Read further pages with `offset=next_offset` until it is null.
   - Local: `uv run "$VF" fetch "$URL" --dir "$WORK"`. This writes
     `video.mp4`, `meta.json` and `transcript.txt` (`[m:ss] text` lines).

   If there is no transcript, say so and work from contact sheets alone.
2. **Find the steps.** From the transcript, decide the tutorial's steps and the
   time range in which each one is spoken. Speech usually leads the matching
   picture by a few seconds, so the range runs from when a step is introduced
   to when the next one starts.
3. **Look before choosing.** Make a contact sheet for each range, or one sheet
   that covers all of them. Each cell is labelled with its time. Use 4 frames
   a second on a short range for fast movement. A sheet holds at most 64
   frames.
   - MCP: `get_contact_sheet` with `url_or_id`, `start`, `end` and `fps`. The
     sheet comes back inline. The first frame call for a video downloads it,
     which takes a few seconds; later calls reuse it.
   - Local: `uv run "$VF" sheet "$WORK" --start 0:13 --end 0:45 [--fps 4]`,
     then Read the sheet image.
4. **Choose one frame per step.** Prefer the frame that *shows* the step:
   - the body position the step describes, at its clearest
   - on-screen captions or step titles, when the video has them — they confirm
     the match
   - little motion blur, splash or occlusion
   - over the first frame where the step is mentioned
5. **Extract.** Name frames in kebab-case after the tutorial and step, such as
   `flip-turn-2-knee-tuck.jpg`.
   - MCP: `get_frames` with `url_or_id` and `times`, up to 12 a call. For each
     frame it returns a preview, a file name `frame-<32 hex>.jpg` and a signed
     download link. With a shell, save each one at once, because links expire
     after one hour:
     `curl -fsS -o docs/images/<slug>-<n>-<step>.jpg '<link>'`.
     Without a shell, keep the links and the frame names for the report.
   - Local: `uv run "$VF" frames "$WORK" --frame 0:18.5=<slug>-1-<step> ...
     --out-dir docs/images`.

   Look at the frames together to check them before writing.
6. **Write the page** (structure below). Without a shell, give the page text
   in the reply and tell the user to save the images from the links within the
   hour.
7. **Report** the route, the page path, the images, any timestamps you
   corrected, and any step whose frame is weak (and why), so the user can ask
   for an edit.

### Local route setup

`uv` and `ffmpeg` on PATH. If `ffmpeg` is missing, run `brew install ffmpeg`.
Resolve the script:

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
caption", "add an arrow showing the rotation" — edit a copy and keep the
original. Say what to keep as well as what to change. Each edit costs roughly
USD 0.13; say the count and cost before a batch.

- MCP: `image-gen`'s `edit_image`, with `source` set to the frame's file name
  (`frame-<32 hex>.jpg`) from `get_frames`. It returns a signed link to the
  edited image; save it beside the original, for example as
  `docs/images/<frame>-annotated.png`. Frames are kept for 7 days on the
  server; after that, call `get_frames` again for a new name.
- Local: the `image-gen` plugin's script, with the saved frame as the source.
  It needs `GEMINI_API_KEY`:

  ```bash
  uv run "$IMAGE_GEN_PLUGIN_ROOT/scripts/generate_image.py" \
    "<the change>" \
    --edit docs/images/<frame>.jpg --output docs/images/<frame>-annotated.png
  ```

  `--edit` keeps the source's shape unless `--aspect-ratio` is given.

Point the page at the edit. Generated edits can change details of the scene:
check that the result still shows what the step describes before using it.

## Errors

- **`blocked`** (MCP) or **`Sign in to confirm you're not a bot`** (local) —
  YouTube refused the download from that machine's IP. Try the other route.
  Do not add cookies without asking.
- **`video_unavailable`** — private, removed or region-locked.
- **`invalid_request`** (MCP) — a time past the end of the video, more than 12
  frames in one call, or a video longer than one hour. Use the local route for
  long videos.
- **`no frame at m:ss`** (local) — the time is past the end of the video.
- **No transcript** — normal for some videos; choose steps from contact sheets
  and the video's own captions.
