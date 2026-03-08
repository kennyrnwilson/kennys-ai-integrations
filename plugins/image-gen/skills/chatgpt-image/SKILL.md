---
name: chatgpt-image
description: Generate images using ChatGPT's web interface. Use when the user asks to create any image, picture, or visual using ChatGPT. This is the base image generation skill — pass any prompt directly to ChatGPT.
argument-hint: <prompt-text-or-file> [--output output.png]
user-invocable: true
allowed-tools: Read, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_fill_form, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_wait_for, mcp__plugin_playwright_playwright__browser_tabs
---

# ChatGPT Web Image Generator

Generate images using ChatGPT's web interface (DALL-E) via Playwright browser automation. Accepts any prompt — either as inline text or read from a file.

## Arguments

- `$0` — Either a file path (markdown or text file) OR inline text describing what to generate (e.g., `"a dancing dog in a park"`)
- `--output` — Output image path (default: `chatgpt_image.png` in current working directory, or `{source_stem}_chatgpt.png` when given a file)

If no arguments are provided, ask the user what they'd like to generate.

## First-Run Setup

On the very first use, a browser window will open and you will need to log into your OpenAI/ChatGPT account. After that first login, credentials are persisted automatically in the Playwright browser profile and subsequent runs will not require login.

## Workflow

Follow these steps exactly, in order.

### Step 1: Determine Input and Build Prompt

Examine `$0` to decide if it is a **file path** or **inline text**:

- **File path**: If `$0` looks like a file path (contains `/` or `\`, ends with a common extension like `.md`, `.txt`, `.html`, etc., or points to an existing file), treat it as a file.
- **Inline text**: Otherwise, treat `$0` as a direct text description.

**If file path:**
1. Use the `Read` tool to load the file at the path provided in `$0`.
2. If the file does not exist, tell the user and stop.
3. Truncate the content to the first 3000 characters.
4. Tell the user: "Read source file ({total_length} characters). Using first {truncated_length} characters for the ChatGPT prompt."
5. Use the file content as the prompt text.

**If inline text:**
1. Use `$0` directly as the prompt text.
2. Tell the user: "Using inline text for the ChatGPT prompt."

### Step 2: Determine Output Path

1. If `--output` was specified, use that path.
2. Otherwise:
   - **File mode**: Same directory as the source file, filename `{source_stem}_chatgpt.png`.
   - **Inline text mode**: `chatgpt_image.png` in the current working directory.
3. Tell the user the output path that will be used.

### Step 3: Navigate to ChatGPT

1. Use `browser_navigate` to go to `https://chatgpt.com/`.
2. Wait a moment for the page to load.

### Step 4: Check Login Status

1. Use `browser_snapshot` to get the accessibility tree of the page.
2. Look for a text input area (textarea, textbox, or contenteditable element) in the accessibility tree. This indicates the user is logged in and the chat interface is ready.
3. If a text input is found, proceed to Step 5.
4. If no text input is found (you see a "Log in" or "Sign up" button instead):
   - Tell the user: "Please log in to your ChatGPT account in the browser window that just opened. I'll wait for you to complete login."
   - Poll with `browser_snapshot` every 10 seconds, up to 60 seconds total (6 attempts).
   - On each poll, check if a text input area has appeared.
   - If login succeeds (text input appears), proceed to Step 5.
   - If login does not succeed after 60 seconds, tell the user: "Login timed out after 60 seconds. Please try again." and stop.

### Step 5: Enter the Prompt

1. Use `browser_snapshot` to find the chat input field. Look for an element with a role like `textbox`, `textarea`, or a contenteditable element in the accessibility tree. Note its `ref` attribute.
2. Use `browser_fill_form` with the ref of that input element to enter the prompt text.
3. Wait 1-2 seconds for the UI to update after filling the form.

### Step 6: Submit the Prompt

1. Use `browser_snapshot` to look for a "Send" or "Submit" button in the accessibility tree. Look for a button element whose accessible name contains "Send", "Submit", or similar.
2. If found, use `browser_click` with the ref of that button to submit.
3. If no send button is found, fall back to `browser_press_key` with key `Enter`.
4. Tell the user: "Prompt submitted to ChatGPT. Waiting for image generation (this may take 1-2 minutes)..."

### Step 7: Wait for Response Completion

ChatGPT shows a "Stop generating" button while it is working. Wait for it to finish:

1. Wait 10 seconds initially.
2. Use `browser_snapshot` to check if a "Stop generating" or "Stop" button is visible in the accessibility tree.
3. If found, ChatGPT is still generating — poll with `browser_snapshot` every 10 seconds until the stop button disappears (up to 3 minutes).
4. Once the stop button is gone (or was never found), proceed to Step 8.

### Step 8: Wait for Image Generation

After the text response completes, DALL-E image generation may take additional time:

1. Wait 10 seconds after the text response completes.
2. Poll with `browser_snapshot` every 10-15 seconds, for up to 5 minutes (approximately 20 attempts).
3. On each poll, look for image elements in the accessibility tree:
   - Elements with role `img` or `image`
   - Elements whose accessible name contains "Generated image" or similar
   - Look specifically in the **last** response/message area — ignore sidebar thumbnails, profile avatars, and UI icons
4. When a candidate image element is found, note its `ref` attribute and proceed to Step 9.
5. If no image appears after 20 polling attempts (approximately 5 minutes):
   - Use `browser_take_screenshot` to capture a full viewport screenshot for debugging. Save it as `{output_path_stem}_debug.png` alongside the intended output.
   - Tell the user: "No generated image found after 5 minutes. ChatGPT may have produced a text-only response. A debug screenshot has been saved. Please check the browser window and consider retrying."
   - Stop.

### Step 9: Save the Image

1. Use `browser_take_screenshot` with the `ref` of the generated image element to capture just that image. Save it to the output path determined in Step 2.
2. If the element-level screenshot fails for any reason, fall back to `browser_take_screenshot` without a ref to capture the full viewport, and save that instead. Tell the user that a viewport screenshot was captured as a fallback.

### Step 10: Clean Up

1. Use `browser_snapshot` to look for a "New chat" button or link in the accessibility tree.
2. If found, use `browser_click` with its ref to start a fresh chat session.
3. If not found, navigate to `https://chatgpt.com/` to start fresh.

### Step 11: Report to User

Tell the user:
- The image was saved successfully.
- The full output file path.
- Any relevant details (e.g., whether a fallback screenshot was used).

## Error Handling

Handle these situations gracefully:

### Login Timeout
If the user does not log in within 60 seconds during Step 4, tell them: "Login timed out after 60 seconds. Please ensure you can access chatgpt.com in your browser and try again."

### No Image Generated
If no image appears after 5 minutes of polling in Step 8, capture a debug screenshot, inform the user that ChatGPT may have produced text instead of an image, and suggest retrying with a different prompt.

### Cannot Find Chat Input
If `browser_snapshot` does not reveal a recognizable text input in Step 5, capture a snapshot for debugging, tell the user: "Could not find the chat input field. ChatGPT's UI may have changed. Please check the browser window." and stop.

### Browser Not Available
If any Playwright MCP tool call fails with a connection or browser error, tell the user: "The Playwright browser does not appear to be available. Please ensure the Playwright MCP server is configured and the browser is installed. You may need to run the browser_install tool first."
