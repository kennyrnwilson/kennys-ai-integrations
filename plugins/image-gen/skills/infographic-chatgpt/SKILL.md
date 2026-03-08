---
name: infographic-chatgpt
description: Generate professional dark-themed infographic images using ChatGPT. Use when the user asks to create an infographic or visual summary from text or a file using ChatGPT. Adds professional styling on top of the base chatgpt-image skill.
argument-hint: <source-file-or-text> [--output output.png] [--style modern|minimal|abstract|illustrated|tech]
user-invocable: true
allowed-tools: Read, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_fill_form, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_wait_for, mcp__plugin_playwright_playwright__browser_tabs
---

# ChatGPT Professional Infographic Generator

Generate professional dark-themed infographic images using ChatGPT (DALL-E). This skill wraps the base `chatgpt-image` skill, adding styling and layout instructions to produce polished infographics.

## Arguments

- `$0` — Either a file path (markdown or text file) OR inline text describing the infographic topic (e.g., `"benefits of remote work"`)
- `--output` — Output image path (default: `{source_stem}_infographic_chatgpt.png` for files, or `infographic_chatgpt.png` for inline text)
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
   - **File mode**: Same directory as the source file, filename `{source_stem}_infographic_chatgpt.png`.
   - **Inline text mode**: `infographic_chatgpt.png` in the current working directory.

### Step 3: Construct the Styled Prompt

Determine the style from `--style` (default to `modern` if not specified).

**For file-based input**, construct this prompt:

```
Create an infographic image that summarizes this text.

Style: {style}, professional, and clean design
Background: Dark navy/blue background
Colors: Bright, vibrant colors that work well on dark backgrounds
Layout: Clear sections with icons and visual elements
Important: Do not depict any specific real people or public figures. Use abstract icons, symbols, and conceptual imagery to represent all ideas and people.

Text to summarize:
{text_content}

Make it visually engaging with icons, clear typography, and a good information hierarchy.
```

**For inline text input**, construct this prompt:

```
Create an infographic image about: {description}

Style: {style}, professional, and clean design
Background: Dark navy/blue background
Colors: Bright, vibrant colors that work well on dark backgrounds
Layout: Clear sections with icons and visual elements
Important: Do not depict any specific real people or public figures. Use abstract icons, symbols, and conceptual imagery to represent all ideas and people.

Make it visually engaging with icons, clear typography, and a good information hierarchy.
```

### Step 4: Generate the Image

Now follow the `chatgpt-image` skill workflow **starting from Step 3** (Navigate to ChatGPT), using:
- The styled prompt constructed in Step 3 above as the prompt text
- The output path determined in Step 2 above

This means: navigate to ChatGPT, check login, enter the styled prompt, submit, wait for response completion, wait for image generation, save, clean up, and report — exactly as described in the `chatgpt-image` skill Steps 3-11.
