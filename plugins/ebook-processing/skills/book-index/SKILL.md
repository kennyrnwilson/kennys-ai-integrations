---
name: book-index
description: Generate a README index page, action items, and metadata for a processed book. Use when the user wants to create the book's index page, generate action items, or create metadata.yaml.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Book Index Generator

Generate a comprehensive README index page, action items checklist, and metadata file for a processed book directory. Scans for all available materials and creates a central hub linking to every resource.

## Arguments

- `$0` — The book directory path or book name. Can be:
  - A full/relative path (e.g., `/Users/kenne/code/book-library/designing-data-intensive-applications/`)
  - A bare book name (e.g., `designing-data-intensive-applications`) — resolved against `$EBOOK_LIBRARY_PATH`
- `--force` — Bypass resume check and regenerate all index files even if they already exist.

If no arguments are provided, ask the user for the book directory path.

## Path Resolution

Resolve `$0` to a book directory path:
1. If `$0` is an absolute path or starts with `~`, `./`, or `../` — use it directly
2. If `$0` is a bare name (no path separators): check the `EBOOK_LIBRARY_PATH` environment variable (via Bash: `echo $EBOOK_LIBRARY_PATH`). If set, resolve to `$EBOOK_LIBRARY_PATH/{name}/`. If not set, resolve to `./{name}/`

## Workflow

### Step 1: Scan Book Directory

1. Use Glob and LS (via Bash `ls`) to inventory all files and subdirectories:
   - `book-formats/` — converted book files (epub, pdf, md, azw3)
   - `summaries/` — summary files and critical review
   - `chapter-summaries/` — individual chapter summary files
   - `*_infographic_*.png` — infographic images at the book root
   - `slide-decks/` — presentation files
   - `personal-notes/` — user's personal notes
2. Build a complete list of available files for template rendering.

### Step 2: Resume Check

1. Check if `README.md` exists in the book root directory.
2. If it exists and `--force` was NOT specified, tell the user: "An index page already exists at `{directory}/README.md`. Use `--force` to regenerate." and stop.

### Step 3: Read Book Content

1. Read the book markdown (from `book-formats/*_book.md`) or the best available summary (from `summaries/`) for title, author extraction and content understanding.
2. Use the same summary priority as critical-review: `*_summary_anthropic_*` (dominant, 50 files) > `*_summary_claude_*` (legacy, one file) > `*_summary_openai_*` > `*_summary_gemini_*` / `*_summary_gemini_web_*`.

### Step 4: Generate action-items.md

1. Read all available summaries in `summaries/`.
2. Extract actionable items from the summaries — look for sections titled "Actionable Advice", "Key Interventions", "Quick Wins", "Action Items", etc.
3. Organize into categories (e.g., "Quick Wins", "Core Practices", "Advanced Applications").
4. Format as a markdown checklist with checkboxes (`- [ ]`).
5. Write to `action-items.md` in the book root.

### Step 5: Generate README.md

Using the Index Page Template below, generate the comprehensive README. Follow these rules:
- **Only include sections for files that actually exist** — do not create sections for missing materials
- **Use relative paths** for all links
- **Extract book title and author** from the book content or summary
- **Write a brief 2-3 sentence summary** of what the book is about
- **Identify 3 core themes** from the book content

Write to `README.md` in the book root.

### Step 6: Generate metadata.yaml

Extract structured metadata and write to `metadata.yaml` in the book root,
following the library's real schema (verified against
`designing-data-intensive-applications/metadata.yaml` and
`atomic-habits/metadata.yaml` in `book-library`):

```yaml
title: Designing Data-Intensive Applications
author: Martin Kleppmann
categories:
- technology
- databases
- distributed-systems
source_folder: designing-data-intensive-applications
formats:
  epub: book-formats/designing-data-intensive-applications_book.epub
  pdf: book-formats/designing-data-intensive-applications_book.pdf
  md: book-formats/designing-data-intensive-applications_book.md
summaries:
  anthropic: summaries/designing-data-intensive-applications_book_summary_anthropic_opus-4.5.md
  openai: summaries/designing-data-intensive-applications_book_summary_openai_gpt-5.2.md
  critical_review: summaries/designing-data-intensive-applications_critical_review.md
infographics:
  gemini: designing-data-intensive-applications_book_infographic_gemini.png
tags:
- scalability
- replication
- partitioning
embedding_status: pending
```

**Field rules**

- `source_folder` is **required** and must exactly equal the book's directory
  name in kebab-case. The `book-library` MCP server keys off it; a mismatch
  makes the book unreachable through search.
- `formats`, `summaries` and `infographics` are maps of short key → repo-relative
  path. Only include keys whose file actually exists — do not emit a key with a
  path to a file you did not find.
- `summaries` keys are provider tokens: `anthropic`, `openai`, `gemini`,
  `gemini_web`, `critical_review`.
- `categories` is broad subject areas; `tags` is specific concepts. Both are
  kebab-case lists. Aim for 3–6 categories and 8–12 tags.
- `embedding_status: pending` on every newly created file — a separate pipeline
  in `book-library` consumes and updates it. Never set it to anything else here.

### Step 7: Create Stub Folders

1. If `personal-notes/` doesn't exist, create it with a `README.md`:
   ```markdown
   # Personal Notes

   Add your personal notes, highlights, and reflections about this book here.
   ```

2. If `slide-decks/` doesn't exist, create it with a `README.md`:
   ```markdown
   # Slide Decks

   A collection of presentations and slide decks related to this book.
   Add your downloaded slides here.
   ```

### Step 8: Convert README to PDF

Run `pandoc "README.md" -o "README.pdf" --pdf-engine=weasyprint` via Bash in the book directory. Skip if pandoc is not available.

### Step 9: Add Backlinks

For each markdown file in `summaries/`, check if a backlink to the README exists at the top. If not, prepend:
```markdown
← [Back to Index](../README.md)

```

### Step 10: Report

Tell the user:
- Files created (README.md, action-items.md, metadata.yaml, stub folders)
- Sections included in the README (based on what materials exist)
- File paths

### Step 11: Update the library catalogue

`book-library/CLAUDE.md` requires `CATALOG.md` to stay in sync when a book is
added. There is no generation script in that repo — it is maintained by hand.

1. Check whether the book already appears:

```bash
grep -n "{slug}" "$EBOOK_LIBRARY_PATH/CATALOG.md" || echo "not in catalogue"
```

2. If absent, add a row matching the surrounding format exactly. Read the
   neighbouring rows first — do not guess the column layout.

3. Tell the user that `catalog.html` and `CATALOG.pdf` are generated separately
   and may also need regenerating. Do not attempt to regenerate them; no script
   exists for this and hand-editing the PDF is not sensible.

## Index Page Template

Use this template as the output format for README.md. Only include sections for materials that actually exist.

````markdown
# [Book Title]

## By [Author Name]

[2-3 sentence engaging summary of the book]

---

## 🎯 3 Core Themes

1. **[Theme Title 1]**
   [1-2 sentences explaining the theme and its significance to the book]

2. **[Theme Title 2]**
   [1-2 sentences explaining the theme and its significance to the book]

3. **[Theme Title 3]**
   [1-2 sentences explaining the theme and its significance to the book]

---

## 📊 Visual Overview

[Only include if infographic files exist at the book root]

### ChatGPT Visualization
![Book Overview - ChatGPT]({book-name}_book_infographic_chatgpt.png)

### Gemini Visualization
![Book Overview - Gemini]({book-name}_book_infographic_gemini.png)

---

## 🎯 Top 5 Actionable Interventions

1. **[Intervention Title 1]**
   [2-3 sentences explaining the specific action to take and why it's important]

2. **[Intervention Title 2]**
   [2-3 sentences explaining the specific action to take and why it's important]

3. **[Intervention Title 3]**
   [2-3 sentences explaining the specific action to take and why it's important]

4. **[Intervention Title 4]**
   [2-3 sentences explaining the specific action to take and why it's important]

5. **[Intervention Title 5]**
   [2-3 sentences explaining the specific action to take and why it's important]

📋 [View Complete Action Items Checklist](action-items.md)

---

## 📚 Full Book

[Only include if book-formats/ exists]

- 📗 [Read as EPUB](book-formats/{book-name}_book.epub)
- 📕 [View PDF](book-formats/{book-name}_book.pdf)
- 📝 [Browse Markdown](book-formats/{book-name}_book.md)

---

## 📝 Summaries

[Only include providers whose files actually exist]

### Anthropic Summary
- [Markdown Version](summaries/{book-name}_book_summary_anthropic_{model}.md)
- [PDF Version](summaries/{book-name}_book_summary_anthropic_{model}.pdf)

### Claude Summary (legacy naming)
- [Markdown Version](summaries/{book-name}_book_summary_claude_{model}.md)
- [PDF Version](summaries/{book-name}_book_summary_claude_{model}.pdf)

### OpenAI Summary
- [Markdown Version](summaries/{book-name}_book_summary_openai_{model}.md)
- [PDF Version](summaries/{book-name}_book_summary_openai_{model}.pdf)

### Gemini Web Summary
- [Markdown Version](summaries/{book-name}_book_summary_gemini_web.md)
- [PDF Version](summaries/{book-name}_book_summary_gemini_web.pdf)

### Shortform Summary
- [Markdown Version](summaries/{book-name}_book_summary_shortform.md)
- [PDF Version](summaries/{book-name}_book_summary_shortform.pdf)

---

## 🔬 Critical Review

[Only include if critical review file exists]

An evidence-based analysis of key claims and recommendations from the book.

- [Markdown Version](summaries/{book-name}_critical_review.md)
- [PDF Version](summaries/{book-name}_critical_review.pdf)

---

## 📖 Chapter Summaries

[Only include if chapter-summaries/ exists]

Detailed summaries for each chapter with key concepts, takeaways, and actionable advice.

📚 [View All Chapter Summaries](chapter-summaries/README.md) | [PDF Version](chapter-summaries/README.pdf)

**Preview:**
- [Chapter 1: {Title}](chapter-summaries/chapter-01-{slug}.md)
- [Chapter 2: {Title}](chapter-summaries/chapter-02-{slug}.md)
- [Chapter 3: {Title}](chapter-summaries/chapter-03-{slug}.md)

---

## 🎬 Slide Decks

A collection of presentations and slide decks related to this book. Add your downloaded slides here.

_No slide decks added yet — download presentations and add them to the `slide-decks/` folder._

📁 [Browse Slide Decks](slide-decks/README.md)

---

*Generated on [Date] with the [ebook-processing plugin](https://github.com/kennyrnwilson/kennys-ai-integrations)*
````

## Formatting Guidelines

- Use proper markdown formatting throughout
- Use emojis sparingly but effectively for visual appeal
- Ensure all links use relative paths
- Keep the summary concise but informative
- Use horizontal rules (`---`) to separate major sections
- Prefer clean, professional styling over excessive decoration
- Avoid hyperbolic or promotional language

## Error Handling

- **No book content or summary found**: Tell the user to run `summarize-book` or `convert-book` first.
- **Directory doesn't exist**: Tell the user the path is invalid.
- **PDF conversion fails**: Skip PDF, inform user, continue.
- **Some materials missing**: Generate the README with only the sections that have corresponding files. Note which sections were omitted.
