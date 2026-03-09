# Ebook Processing Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create an ebook-processing Claude Code plugin that processes books into organized, AI-enriched library folders using Claude-native summarization.

**Architecture:** 8 skills (1 orchestrator + 7 stage skills) in a single plugin. Each skill is a SKILL.md with embedded prompt templates. No Python code — everything is prompt-driven. Skills delegate to Claude's own capabilities and existing `image-gen` plugin skills.

**Tech Stack:** Claude Code plugin system (SKILL.md files), Bash (for Calibre CLI, pandoc), WebSearch (for critical review), cross-plugin `image-gen` skills (for infographics).

**Design doc:** `docs/plans/2026-03-09-ebook-processing-plugin-design.md`

---

## Prerequisites

Before starting, ensure you're working in `/Users/kenne/code/kennys-ai-integrations/`. The design doc at `docs/plans/2026-03-09-ebook-processing-plugin-design.md` has all architectural decisions.

Reference these existing files for patterns:
- `plugins/image-gen/.claude-plugin/plugin.json` — plugin.json format
- `plugins/image-gen/skills/infographic-chatgpt/SKILL.md` — SKILL.md frontmatter format
- `plugins/notebooklm/skills/notebooklm-create/SKILL.md` — complex skill workflow format

---

### Task 1: Plugin Scaffold

**Files:**
- Create: `plugins/ebook-processing/.claude-plugin/plugin.json`
- Create: `plugins/ebook-processing/skills/` (directory)

**Step 1: Create plugin.json**

```json
{
  "name": "ebook-processing",
  "version": "1.0.0",
  "description": "Process ebooks into organized, AI-enriched library folders with summaries, chapter breakdowns, infographics, critical reviews, and index pages.",
  "author": {
    "name": "kennyrnwilson"
  },
  "repository": "https://github.com/kennyrnwilson/kennys-ai-integrations",
  "license": "MIT",
  "keywords": ["ebook", "book-processing", "summarization", "infographic", "critical-review"]
}
```

**Step 2: Create skill directories**

```bash
mkdir -p plugins/ebook-processing/skills/{process-book,convert-book,summarize-book,chapter-summaries,chapter-infographics,book-infographics,critical-review,book-index}
```

**Step 3: Commit**

```bash
git add plugins/ebook-processing/
git commit -m "feat(ebook-processing): scaffold plugin with skill directories"
```

---

### Task 2: summarize-book Skill

This is the most important skill — it replaces all 3 API-based summarizers with Claude-native generation.

**Files:**
- Create: `plugins/ebook-processing/skills/summarize-book/SKILL.md`

**Step 1: Write the SKILL.md**

The frontmatter:

```yaml
---
name: summarize-book
description: Generate a comprehensive book summary using Claude. Use when the user wants to summarize a book, create a book summary, or process a book's markdown into a structured summary.
argument-hint: <book-directory> [--force]
user-invocable: true
---
```

The body must contain:

1. **Arguments section** — `$0` is the book directory path (e.g., `~/electronic-books/designing-data-intensive-applications/`). `--force` bypasses resume check.

2. **Workflow section** with these steps:

   - **Step 1: Locate Book Content** — Use Glob to find `book-formats/*_book.md` in the book directory. Extract book name from directory name (kebab-case). If no markdown found, tell user and stop.

   - **Step 2: Resume Check** — Use Glob to check for existing `summaries/*_summary_claude_*.md`. If found and `--force` not specified, tell user summary exists and stop.

   - **Step 3: Read Book Content** — Read the book markdown file. If the file is very large, read in chunks. Note: Claude can handle large context, so read as much as possible.

   - **Step 4: Generate Summary** — Apply the embedded summary template (see below) to generate the full summary. The output must follow the template structure exactly.

   - **Step 5: Save Summary** — Determine the model short name from the current Claude model (e.g., `opus-4.6`). Create `summaries/` directory if it doesn't exist. Write to `summaries/{book-name}_summary_claude_{model-short}.md`.

   - **Step 6: Convert to PDF** — Run: `pandoc "summaries/{filename}.md" -o "summaries/{filename}.pdf" --pdf-engine=weasyprint` via Bash. If pandoc not available, try: `python3 -c "import weasyprint; weasyprint.HTML(filename='summaries/{filename}.md').write_pdf('summaries/{filename}.pdf')"`. If neither works, skip PDF and inform user.

   - **Step 7: Report** — Tell user the summary was saved, file paths, and word count.

3. **Summary Template section** — Embed the FULL detailed-book-summary-template from `~/code/ebook-processing/templates/custom_templates/detailed-book-summary-template.md`. This is 358 lines. Include the entire template verbatim in the SKILL.md under a `## Summary Template` heading, inside a fenced code block, so Claude uses it as the output format.

4. **Style Guidelines section** — Include the tone/style rules:
   - No hyperbolic language
   - Concrete, measurable actions
   - Professional, objective tone
   - Every sentence adds value

5. **Error Handling section** — Book markdown not found, directory doesn't exist, PDF conversion fails.

**Source template to embed:** Read from `/Users/kenne/code/ebook-processing/templates/custom_templates/detailed-book-summary-template.md` (already captured in the design doc).

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/summarize-book/
git commit -m "feat(ebook-processing): add summarize-book skill with full template"
```

---

### Task 3: chapter-summaries Skill

**Files:**
- Create: `plugins/ebook-processing/skills/chapter-summaries/SKILL.md`

**Step 1: Write the SKILL.md**

Frontmatter:

```yaml
---
name: chapter-summaries
description: Extract and summarize individual chapters from a book's markdown. Use when the user wants chapter-by-chapter summaries, chapter breakdowns, or detailed chapter analysis.
argument-hint: <book-directory> [--force]
user-invocable: true
---
```

Body workflow:

- **Step 1: Locate Book Content** — Glob for `book-formats/*_book.md`. Extract book name.

- **Step 2: Resume Check** — Check if `chapter-summaries/README.md` exists. If yes and not `--force`, report existing and stop.

- **Step 3: Read Book Content** — Read full book markdown.

- **Step 4: Extract Chapters** — Analyze the markdown to identify chapter boundaries. Look for patterns like `## Chapter N: Title`, `# Chapter N`, bold chapter numbers, etc. List all chapters found with their titles and approximate content ranges. Present the chapter list to the user before proceeding.

- **Step 5: Summarize Each Chapter** — For each chapter (with per-chapter resume check on `chapter-{NN}-{slug}.md`):
  1. Extract the chapter content
  2. Generate summary using the embedded chapter template
  3. Add navigation links (← Previous | Next →)
  4. Save as `chapter-summaries/chapter-{NN}-{slug}.md`
  5. Convert to PDF via pandoc
  6. Report progress: "Completed chapter {N} of {total}: {title}"

- **Step 6: Generate Chapter Index** — Create `chapter-summaries/README.md` with:
  - Book title and author
  - Table of contents linking to each chapter summary
  - Brief description of what chapter summaries contain

- **Step 7: Convert Index to PDF** — pandoc the README.md to README.pdf

- **Step 8: Report** — Total chapters summarized, any skipped (resume), file paths.

Embed the chapter summary template from `/Users/kenne/code/ebook-processing/templates/chapter_summary_template.md` (57 lines).

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/chapter-summaries/
git commit -m "feat(ebook-processing): add chapter-summaries skill with template"
```

---

### Task 4: critical-review Skill

**Files:**
- Create: `plugins/ebook-processing/skills/critical-review/SKILL.md`

**Step 1: Write the SKILL.md**

Frontmatter:

```yaml
---
name: critical-review
description: Generate an evidence-based critical review of a book's key claims using web research. Use when the user wants fact-checking, claim verification, or a critical analysis of a book.
argument-hint: <book-directory> [--force]
user-invocable: true
---
```

Body workflow:

- **Step 1: Locate Best Summary** — Search `summaries/` for the best available summary. Priority order: `*_summary_claude_*` > `*_summary_anthropic_*` > `*_summary_openai_*` > `*_summary_gemini_*`. Use Glob to find candidates. Read the best one.

- **Step 2: Resume Check** — Check if `summaries/*_critical_review.md` exists.

- **Step 3: Extract Key Claims** — Read the summary and identify 5-7 significant claims, recommendations, or action items that can be verified with evidence.

- **Step 4: Research Each Claim** — For each claim, use WebSearch to find:
  - Scientific studies or research supporting/refuting the claim
  - Expert opinions or criticisms
  - Counter-arguments or alternative perspectives
  - Any controversies

- **Step 5: Generate Critical Review** — Using the embedded review template, produce a structured document with per-claim analysis, credibility ratings, and an overall assessment.

- **Step 6: Save** — Write to `summaries/{book-name}_critical_review.md`. Convert to PDF.

- **Step 7: Report** — Number of claims analyzed, overall credibility rating, file paths.

Embed the critical review prompt template from `_build_review_prompt` in the existing pipeline (the full markdown structure with Executive Summary, Claims Analysis, Overall Assessment, Sources sections).

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/critical-review/
git commit -m "feat(ebook-processing): add critical-review skill with web research"
```

---

### Task 5: book-index Skill

**Files:**
- Create: `plugins/ebook-processing/skills/book-index/SKILL.md`

**Step 1: Write the SKILL.md**

Frontmatter:

```yaml
---
name: book-index
description: Generate a README index page, action items, and metadata for a processed book. Use when the user wants to create the book's index page, generate action items, or create metadata.yaml.
argument-hint: <book-directory> [--force]
user-invocable: true
---
```

Body workflow:

- **Step 1: Scan Book Directory** — Use Glob and LS to inventory all files: book-formats/, summaries/, chapter-summaries/, infographics, slide-decks/. Build a list of available files for template rendering.

- **Step 2: Resume Check** — Check if `README.md` exists in book root.

- **Step 3: Read Book Content** — Read the book markdown (or best summary if book is too large) for title, author extraction and content understanding.

- **Step 4: Generate action-items.md** — Extract actionable items from all available summaries. Format as a checklist with categories. Write to `action-items.md`.

- **Step 5: Generate README.md** — Using the embedded index template, generate the comprehensive README. Only include sections for files that actually exist. Use relative paths for all links. Write to `README.md`.

- **Step 6: Generate metadata.yaml** — Extract structured metadata: title, author, ISBN (if findable), publication year, categories, tags, processing date. Write to `metadata.yaml`.

- **Step 7: Create stub folders** — Create `personal-notes/README.md` and `slide-decks/README.md` if they don't exist.

- **Step 8: Convert README to PDF** — pandoc README.md to README.pdf.

- **Step 9: Add Backlinks** — For each markdown file in `summaries/`, add a backlink to the README at the top if not already present.

- **Step 10: Report** — Files created, sections included.

Embed the index page template from `/Users/kenne/code/ebook-processing/templates/index_page_prompt.md` (233 lines).

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/book-index/
git commit -m "feat(ebook-processing): add book-index skill with index template"
```

---

### Task 6: book-infographics Skill

**Files:**
- Create: `plugins/ebook-processing/skills/book-infographics/SKILL.md`

**Step 1: Write the SKILL.md**

Frontmatter:

```yaml
---
name: book-infographics
description: Generate book-level infographic images using ChatGPT and Gemini. Use when the user wants visual infographics for a book overview. Delegates to the image-gen plugin.
argument-hint: <book-directory> [--force]
user-invocable: true
---
```

Body workflow:

- **Step 1: Locate Best Summary** — Find the best summary in `summaries/` (same priority as critical-review).

- **Step 2: Resume Check** — Check for existing `*_infographic_chatgpt.png` and `*_infographic_gemini.png` in book root.

- **Step 3: Generate ChatGPT Infographic** — If not exists (or `--force`), invoke `/image-gen:infographic-chatgpt` with the summary file path and output path `{book-name}_book_infographic_chatgpt.png` in the book root directory.

- **Step 4: Generate Gemini Infographic** — If not exists (or `--force`), invoke `/image-gen:infographic-gemini` with the summary file path and output path `{book-name}_book_infographic_gemini.png`.

- **Step 5: Report** — Which infographics were generated, paths.

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/book-infographics/
git commit -m "feat(ebook-processing): add book-infographics skill delegating to image-gen"
```

---

### Task 7: chapter-infographics Skill

**Files:**
- Create: `plugins/ebook-processing/skills/chapter-infographics/SKILL.md`

**Step 1: Write the SKILL.md**

Frontmatter:

```yaml
---
name: chapter-infographics
description: Generate infographic images for each chapter summary. Use when the user wants visual infographics for individual chapters. Delegates to the image-gen plugin.
argument-hint: <book-directory> [--force]
user-invocable: true
---
```

Body workflow:

- **Step 1: Locate Chapter Summaries** — Glob for `chapter-summaries/chapter-*.md` files. If none found, tell user to run `chapter-summaries` first.

- **Step 2: For Each Chapter** — For each chapter markdown:
  1. Resume check: does `chapter-{NN}-{slug}_infographic.png` exist?
  2. If not (or `--force`), invoke `/image-gen:infographic-chatgpt` with the chapter markdown file and output to `chapter-summaries/chapter-{NN}-{slug}_infographic.png`
  3. Embed the infographic reference in the chapter markdown (add `![Chapter Infographic](chapter-{NN}-{slug}_infographic.png)` before the Connections section)
  4. Re-convert the chapter markdown to PDF (since it now includes the infographic reference)
  5. Report progress

- **Step 3: Report** — Total infographics generated, any skipped.

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/chapter-infographics/
git commit -m "feat(ebook-processing): add chapter-infographics skill"
```

---

### Task 8: convert-book Skill

**Files:**
- Create: `plugins/ebook-processing/skills/convert-book/SKILL.md`

**Step 1: Write the SKILL.md**

Frontmatter:

```yaml
---
name: convert-book
description: Convert ebook files (EPUB, PDF, ACSM) into multiple formats using Calibre. Use when the user wants to convert a book file, remove DRM, or create book-formats folder. Requires Calibre with DeDRM plugin.
argument-hint: <book-file> [--output-dir <directory>] [--force]
user-invocable: true
---
```

Body workflow:

- **Step 1: Validate Input** — Check the input file exists. Determine format (.epub, .pdf, .acsm).

- **Step 2: Determine Output Directory** — If `--output-dir` specified, use it. Otherwise, derive from book filename: kebab-case the title, create under the current working directory.

- **Step 3: Resume Check** — Check if `book-formats/` contains `*_book.epub`, `*_book.pdf`, `*_book.md`. If all exist and not `--force`, skip.

- **Step 4: Process ACSM (if applicable)** — Open with Adobe Digital Editions via: `open -a "Adobe Digital Editions" "{file}"`. Wait for the download to complete. Find the resulting epub/pdf in `~/Documents/Digital Editions/`.

- **Step 5: Add to Calibre** — Run: `calibredb add "{file}" --with-library ~/calibre-library` to add the book (DeDRM plugin removes DRM automatically).

- **Step 6: Export Formats** — Use `ebook-convert` to generate:
  - `{book-name}_book.epub` (DRM-free)
  - `{book-name}_book.pdf`
  - `{book-name}_book.md` (markdown for AI processing)
  - `{book-name}_book.azw3` (Kindle format)

- **Step 7: Organize** — Create `book-formats/` directory, move all converted files there.

- **Step 8: Report** — Files created, sizes, output directory.

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/convert-book/
git commit -m "feat(ebook-processing): add convert-book skill for Calibre conversion"
```

---

### Task 9: process-book Orchestrator Skill

**Files:**
- Create: `plugins/ebook-processing/skills/process-book/SKILL.md`

**Step 1: Write the SKILL.md**

Frontmatter:

```yaml
---
name: process-book
description: Run the full ebook processing pipeline — convert, summarize, generate chapters, infographics, critical review, and index. Use when the user wants to process a book end-to-end or run the ebook pipeline.
argument-hint: <book-file-or-directory> [--force] [--skip <stages>]
user-invocable: true
---
```

Body workflow:

- **Step 1: Determine Input Type** — If `$0` is a file (.epub/.pdf/.acsm), set mode to "full pipeline" (starts with conversion). If it's a directory, set mode to "enrichment only" (assumes book-formats/ exists).

- **Step 2: Parse Flags** — `--force` passes through to all stage skills. `--skip` is a comma-separated list of stage names to skip (e.g., `--skip infographics,critical-review`). Valid skip values: `convert`, `summarize`, `chapters`, `chapter-infographics`, `infographics`, `critical-review`, `index`.

- **Step 3: Determine Book Directory** — For files: derive book name from filename (kebab-case, remove extension), create directory. For directories: use as-is.

- **Step 4: Run Pipeline** — Execute stages in order, skipping as requested:
  1. `convert-book` (only if input is a file and not skipped)
  2. `summarize-book`
  3. `chapter-summaries`
  4. `chapter-infographics`
  5. `book-infographics`
  6. `critical-review`
  7. `book-index` (always run last)

  For each stage, invoke the corresponding skill with the book directory and `--force` flag if applicable. Report the result of each stage before moving to the next.

- **Step 5: Final Report** — Summary of all stages: which ran, which were skipped (by flag or resume), which failed. Total files generated. Book directory path.

**Important notes for the orchestrator:**
- Each stage is a separate skill invocation
- If a stage fails, log the error and continue with the next stage (don't abort the whole pipeline)
- The orchestrator does NOT embed templates — it delegates entirely to stage skills

**Step 2: Commit**

```bash
git add plugins/ebook-processing/skills/process-book/
git commit -m "feat(ebook-processing): add process-book orchestrator skill"
```

---

### Task 10: Update Repository README

**Files:**
- Modify: `README.md` (repo root)

**Step 1: Add ebook-processing to the plugins section**

Add the new plugin with its skills to the README's plugin listing, following the existing format used for image-gen and notebooklm.

Include:
- Plugin description
- List of all 8 skills with brief descriptions
- Example usage commands

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add ebook-processing plugin to README"
```

---

### Task 11: Push and Verify

**Step 1: Push all commits**

```bash
git push
```

**Step 2: Verify plugin structure**

```bash
find plugins/ebook-processing -type f | sort
```

Expected output:
```
plugins/ebook-processing/.claude-plugin/plugin.json
plugins/ebook-processing/skills/book-index/SKILL.md
plugins/ebook-processing/skills/book-infographics/SKILL.md
plugins/ebook-processing/skills/chapter-infographics/SKILL.md
plugins/ebook-processing/skills/chapter-summaries/SKILL.md
plugins/ebook-processing/skills/convert-book/SKILL.md
plugins/ebook-processing/skills/critical-review/SKILL.md
plugins/ebook-processing/skills/process-book/SKILL.md
plugins/ebook-processing/skills/summarize-book/SKILL.md
```

---

## Task Order and Dependencies

```
Task 1 (scaffold) ─── required by all others
    │
    ├── Task 2 (summarize-book) ─── core skill, no deps
    ├── Task 3 (chapter-summaries) ─── no deps
    ├── Task 4 (critical-review) ─── no deps
    ├── Task 5 (book-index) ─── no deps
    ├── Task 6 (book-infographics) ─── no deps
    ├── Task 7 (chapter-infographics) ─── no deps
    ├── Task 8 (convert-book) ─── no deps
    │
    └── Task 9 (process-book) ─── references all stage skills
            │
            Task 10 (README) ─── after all skills exist
            │
            Task 11 (push) ─── final
```

Tasks 2-8 are independent and can be parallelized. Task 9 should come after all stage skills are written. Tasks 10-11 are final.

---

## Key References

- **Design doc:** `docs/plans/2026-03-09-ebook-processing-plugin-design.md`
- **Summary template:** `/Users/kenne/code/ebook-processing/templates/custom_templates/detailed-book-summary-template.md` (358 lines — embed verbatim)
- **Chapter template:** `/Users/kenne/code/ebook-processing/templates/chapter_summary_template.md` (57 lines — embed verbatim)
- **Index template:** `/Users/kenne/code/ebook-processing/templates/index_page_prompt.md` (233 lines — embed verbatim)
- **Critical review template:** `/Users/kenne/code/ebook-processing/src/pipeline/critical_review_handler.py` lines 492-678 (embed the prompt structure)
- **Plugin pattern:** `plugins/image-gen/` (for plugin.json, SKILL.md frontmatter)
- **Complex skill example:** `plugins/notebooklm/skills/notebooklm-create/SKILL.md` (for workflow structure)
