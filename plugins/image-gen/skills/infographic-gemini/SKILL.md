---
name: infographic-gemini
description: Generate professional dark-themed infographic images using Google Gemini. Use when the user asks to create an infographic or visual summary from text or a file. Adds professional styling on top of the base gemini-image skill.
argument-hint: <source-file-or-text> [--output output.png] [--style modern|minimal|abstract|illustrated|tech]
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_fill_form, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_wait_for, mcp__plugin_playwright_playwright__browser_tabs
---

# Gemini Professional Infographic Generator

Generate professional dark-themed infographic images using Google Gemini. This skill wraps the base `gemini-image` skill, adding styling and layout instructions to produce polished infographics.

## Arguments

- `$0` — Either a file path (markdown or text file) OR inline text describing the infographic topic (e.g., `"benefits of remote work"`)
- `--output` — Output image path (default: `{source_stem}_infographic_gemini.png` for files, or `infographic_gemini.png` for inline text)
- `--style` — Visual style: `modern` (default), `minimal`, `abstract`, `illustrated`, `tech`

If no arguments are provided, ask the user what they'd like to create an infographic about.

## Workflow

### Step 1: Determine Input

Examine `$0` to decide if it is a **file path** or **inline text**:

- **File path**: If `$0` looks like a file path (contains `/` or `\`, ends with a common extension like `.md`, `.txt`, `.html`, etc., or points to an existing file), treat it as a file.
- **Inline text**: Otherwise, treat `$0` as a direct text description.

**If file path:**
1. Use the `Read` tool to load the file at the path provided in `$0`.
2. If the file does not exist, tell the user and stop.
3. Truncate the content to the first 3000 characters.
4. Tell the user: "Read source file ({total_length} characters). Using first {truncated_length} characters."

**If inline text:**
1. Use `$0` directly as the content.

### Step 2: Determine Output Path

1. If `--output` was specified, use that path.
2. Otherwise:
   - **File mode**: Same directory as the source file, filename `{source_stem}_infographic_gemini.png`.
   - **Inline text mode**: `infographic_gemini.png` in the current working directory.

### Step 3: Construct the Styled Prompt

Determine the style from `--style` (default to `modern` if not specified).

**IMPORTANT — Prompt wording**: Gemini frequently responds with a text description of what an infographic *would* look like instead of generating an actual image. The prompt must lead with an explicit image generation instruction and end with a reminder. Do not omit these — they are the difference between getting an image and getting text.

**For file-based input**, construct this prompt:

```
Generate an image. Create a single infographic image summarizing this text.

IMPORTANT: I need you to GENERATE AN ACTUAL IMAGE, not describe one in text.

Style: {style}, professional, dark navy/blue background with bright vibrant colors
Layout: Clear sections with icons and visual elements
Important: Do not depict any specific real people or public figures. Use abstract icons, symbols, and conceptual imagery.

Text to summarize:
{text_content}

Remember: Generate the image directly, do not write text describing what an infographic would look like.
```

**For inline text input**, construct this prompt:

```
Generate an image. Create a single infographic image about: {description}

IMPORTANT: I need you to GENERATE AN ACTUAL IMAGE, not describe one in text.

Style: {style}, professional, dark navy/blue background with bright vibrant colors
Layout: Clear sections with icons and visual elements
Important: Do not depict any specific real people or public figures. Use abstract icons, symbols, and conceptual imagery.

Remember: Generate the image directly, do not write text describing what an infographic would look like.
```

### Step 4: Generate the Image

**IMPORTANT**: Follow all rate limit avoidance rules from the `gemini-image` skill — wait 3-5 seconds after navigation, 2-3 seconds after filling the prompt, 25 seconds before first poll, and 45 seconds between batch generations.

Now follow the `gemini-image` skill workflow **starting from Step 3** (Navigate to Gemini), using:
- The styled prompt constructed in Step 3 above as the prompt text (do NOT wrap it again — it already includes the explicit image generation instructions)
- The output path determined in Step 2 above

This means: navigate to Gemini, check login, enter the styled prompt, submit, wait for image generation (including the retry logic in Step 7a if Gemini returns text), save, clean up, and report — exactly as described in the `gemini-image` skill Steps 3-10.
