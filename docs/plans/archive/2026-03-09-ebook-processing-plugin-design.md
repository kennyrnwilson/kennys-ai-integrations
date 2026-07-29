# Ebook Processing Plugin Design

← [Back to Plans](./README.md)

Design document for migrating the ebook-processing pipeline into a Claude Code plugin within `kennys-ai-integrations`.

---

## Overview

Port the 8-stage ebook-processing pipeline from `~/code/ebook-processing` into a Claude Code plugin. The key shift: replace API-based AI summarization (OpenAI, Anthropic, Gemini Web) with **Claude-native** summarization — Claude Code itself generates summaries directly, eliminating API key management and cost complexity.

**Source repo:** `~/code/ebook-processing`
**Target repo:** `~/code/kennys-ai-integrations/plugins/ebook-processing/`

---

## Design Decisions

### What's Dropped

| Component | Reason |
|-----------|--------|
| OpenAI API summarizer | Replaced by Claude-native |
| Anthropic API summarizer | Replaced by Claude-native |
| Gemini Web summarizer | Replaced by Claude-native |
| Shortform handler (Stage 4) | Dropped entirely — service-specific, not general |
| SummarizerFactory pattern | No longer needed with single Claude-native provider |
| Python codebase | Skills are prompt-driven, no Python code |

### What's Kept

| Component | Notes |
|-----------|-------|
| Smart resume system | Each skill checks for existing outputs before processing |
| Output directory structure | 100% backward-compatible with existing `book-library/` |
| File naming conventions | Same `{book-name}_book_summary_*.md` patterns |
| Templates | Embedded directly in SKILL.md files |
| Chapter detection | Claude handles this natively from book markdown |
| Critical review structure | Same prompt, but Claude + WebSearch instead of Gemini Web |

### What's Changed

| Component | Old | New |
|-----------|-----|-----|
| Summarization | 3 API providers | Claude-native (single provider) |
| Summary filename | `_summary_{provider}_{model}.md` | `_summary_claude_{model}.md` |
| Infographics | Custom Python Playwright code | Reuse `image-gen` plugin skills |
| Critical review | Gemini Web + Google Search | Claude + WebSearch tool |
| Index generation | Anthropic API | Claude-native |
| Metadata extraction | Anthropic API | Claude-native |
| Stages 1-2 (ACSM/conversion) | Core pipeline stages | Optional utility skills |

---

## Plugin Skill Layout

8 skills total — 1 orchestrator + 7 stage skills:

| Skill | Stage | Description | Key Tools |
|-------|-------|-------------|-----------|
| `process-book` | Orchestrator | Runs all enabled stages in sequence | Bash, Read, Write, Glob |
| `convert-book` | 1-2 | Optional ACSM/DRM removal + format conversion via Calibre | Bash |
| `summarize-book` | 3 | Claude-native book summarization using embedded template | Read, Write |
| `chapter-summaries` | 5a | Extract chapters from book markdown, summarize each | Read, Write, Glob |
| `chapter-infographics` | 5b | Generate chapter infographics via `image-gen` plugin | Skill (cross-plugin) |
| `book-infographics` | 6 | Generate book-level infographics via `image-gen` plugin | Skill (cross-plugin) |
| `critical-review` | 7 | Evidence-based claim analysis using Claude + WebSearch | Read, Write, WebSearch |
| `book-index` | 8 | Generate README, action-items.md, metadata.yaml | Read, Write, Glob |

### Skill Invocation

```bash
# Full pipeline
/ebook-processing:process-book /path/to/book.epub

# Individual stages
/ebook-processing:summarize-book ~/electronic-books/designing-data-intensive-applications/
/ebook-processing:chapter-summaries ~/electronic-books/designing-data-intensive-applications/
/ebook-processing:critical-review ~/electronic-books/designing-data-intensive-applications/
/ebook-processing:book-index ~/electronic-books/designing-data-intensive-applications/
```

---

## Data Flow

```
Input: /path/to/book.epub (or .pdf, .acsm)
                    │
                    ▼
┌─────────────────────────────────────────┐
│  convert-book (optional)                │
│  Input: .acsm / .epub / .pdf            │
│  Output: book-formats/{name}_book.*     │
│  Tools: Calibre CLI (calibredb,         │
│         ebook-convert)                  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  summarize-book                         │
│  Input: book-formats/{name}_book.md     │
│  Output: summaries/{name}_summary_      │
│          claude_{model}.md + .pdf       │
│  Tools: Claude-native + md-to-pdf       │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┼─────────┬─────────┐
        ▼         ▼         ▼         ▼
┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐
│ chapter- │ │ chapter- │ │ book-  │ │ critical-│
│ summaries│ │ infograph│ │ infogr │ │ review   │
│          │ │          │ │        │ │          │
│ chapter- │ │ chapter- │ │ *_info │ │ *_criti- │
│ summaries│ │ summaries│ │ graphic│ │ cal_     │
│ /*.md    │ │ /*_infog │ │ _*.png │ │ review.md│
│          │ │ raphic.  │ │        │ │          │
│          │ │ png      │ │        │ │          │
└────┬─────┘ └────┬─────┘ └───┬────┘ └────┬─────┘
     └─────────┬──┴───────────┴────────────┘
               ▼
┌─────────────────────────────────────────┐
│  book-index                             │
│  Output: README.md, README.pdf,         │
│          action-items.md,               │
│          metadata.yaml                  │
└─────────────────────────────────────────┘
```

---

## Output Directory Structure

Fully backward-compatible with existing `book-library/`:

```
~/electronic-books/{book-name}/
    README.md
    README.pdf
    action-items.md
    metadata.yaml
    {book-name}_book_infographic_chatgpt.png
    {book-name}_book_infographic_gemini.png
    book-formats/
        {book-name}_book.epub
        {book-name}_book.pdf
        {book-name}_book.md
        {book-name}_book.azw3
    summaries/
        {book-name}_summary_claude_{model}.md        ← NEW naming
        {book-name}_summary_claude_{model}.pdf
        {book-name}_critical_review.md
        {book-name}_critical_review.pdf
        # Legacy files (if they exist, still recognized):
        # {book-name}_book_summary_openai_*.md
        # {book-name}_book_summary_anthropic_*.md
        # {book-name}_book_summary_gemini_web.md
    chapter-summaries/
        README.md
        README.pdf
        chapter-{NN}-{slug}.md
        chapter-{NN}-{slug}.pdf
        chapter-{NN}-{slug}_infographic.png
    personal-notes/
        README.md
    slide-decks/
        README.md
```

### Summary File Naming

New summaries use: `{book-name}_summary_claude_{model-short}.md`

Where `{model-short}` is derived from the Claude model (e.g., `opus-4.6`, `sonnet-4.6`).

### Backward Compatibility with Old Provider Summaries

When checking for existing summaries (smart resume), the plugin should recognize any `*_summary_*.md` files in `summaries/` — not just Claude-named ones. This means:
- If a book already has `_summary_anthropic_sonnet-4.5.md`, the resume check sees a summary exists
- The `book-index` skill should link to whatever summary files actually exist, regardless of provider
- The `critical-review` skill should use the best available summary (any provider) as input

**Open question:** Should `summarize-book` skip if ANY provider summary exists, or should it always generate a Claude summary alongside old ones? Recommended: **always generate a Claude summary** — it's free (no API cost), and having a fresh Claude summary ensures the best input for downstream stages.

---

## Smart Resume Logic

Each skill checks for existing outputs before doing work:

| Skill | Resume Check |
|-------|-------------|
| `convert-book` | All 3 formats exist in `book-formats/` |
| `summarize-book` | `summaries/*_summary_claude_*.md` exists |
| `chapter-summaries` | `chapter-summaries/README.md` exists (whole-stage); per-chapter `chapter-{NN}-*.md` (individual) |
| `chapter-infographics` | `chapter-{NN}-*_infographic.png` exists per chapter |
| `book-infographics` | `*_infographic_chatgpt.png` and `*_infographic_gemini.png` exist |
| `critical-review` | `summaries/*_critical_review.md` exists |
| `book-index` | `README.md` exists in book root |

All skills accept a `--force` flag to bypass resume checks.

---

## Prompt Templates

Each stage skill embeds its prompt template directly in the SKILL.md file. The templates are sourced from the existing pipeline.

### Summary Template (for `summarize-book`)

Source: `~/code/ebook-processing/templates/custom_templates/detailed-book-summary-template.md`

Key sections in the template:
- 1-Page Executive Summary (Core Thesis, Key Themes, Top Takeaways)
- Ultra-Compact Summary (3-sentence + 1-paragraph)
- 10 Key Actionable Interventions
- Extended Overview (~2 pages)
- Chapter-by-Chapter Breakdown (Summary, Core Argument, Key Concepts table, Takeaways, Quotes, Actionable Advice, Why This Matters)
- Practical Implementation Guide (Quick Wins, Core Practices, Advanced Applications, Common Pitfalls)
- Key Frameworks & Mental Models (5-7 frameworks with Purpose, Components, Application, Example)
- Critical Reflection (Strengths, Limitations, Counterarguments, Complementary Reading)
- Next Steps & Application (Week, Month, Quarter timelines)

Style guidelines embedded:
- No hyperbolic language ("groundbreaking", "revolutionary", etc.)
- Concrete, measurable actionable items
- Balance theory and practice
- Consider multiple perspectives

### Chapter Summary Template (for `chapter-summaries`)

Source: `~/code/ebook-processing/templates/chapter_summary_template.md`

Sections per chapter:
- Summary (2-4 paragraphs)
- Core Argument (1-2 sentences)
- Key Concepts (table: Concept | Definition)
- Key Takeaways (5 items)
- Actionable Advice (3 checkbox items)
- Notable Quotes (1-2 blockquotes)
- Connections (Previous Chapter, Next Chapter, Related Themes)

### Index Page Template (for `book-index`)

Source: `~/code/ebook-processing/templates/index_page_prompt.md`

Sections:
1. Header (title, author, 2-3 sentence summary)
2. 3 Core Themes
3. Visual Overview (infographic images)
4. Top 5 Actionable Interventions
5. Full Book Formats (links to epub/pdf/md)
6. Summaries (grouped by provider)
7. Critical Review
8. Chapter Summaries (link to index + preview)
9. Slide Decks
10. Footer (date, pipeline credit)

### Critical Review Template (for `critical-review`)

Source: `~/code/ebook-processing/src/pipeline/critical_review_handler.py` (`_build_review_prompt`)

Structure:
- Executive Summary (Overview, Quick Assessment Table with star ratings, Key Takeaways)
- Key Claims Analysis (5-7 claims, each with: The Claim quote, Supporting Evidence with primary research + expert support, Criticisms & Counter-Arguments, Credibility Assessment table, Verdict with color-coded rating)
- Overall Assessment (Strengths, Weaknesses, Who Should Read This Book?)
- Sources & References (Academic, Expert Commentary, Additional Reading)
- Methodology Note

The critical review skill uses **WebSearch** to verify claims against current research, replacing the Gemini Web + Google Search approach.

---

## Cross-Plugin Dependencies

### image-gen Plugin

The `chapter-infographics` and `book-infographics` skills delegate to the `image-gen` plugin:

```bash
# Book-level infographics
/image-gen:infographic-chatgpt  # for ChatGPT infographic
/image-gen:infographic-gemini   # for Gemini infographic

# Chapter-level infographics (same skills, per chapter)
/image-gen:infographic-chatgpt  # for each chapter
```

These skills require Chrome running with remote debugging on port 9222.

---

## Plugin Structure

```
plugins/ebook-processing/
├── plugin.json
├── .mcp.json                    # If any MCP servers needed
└── skills/
    ├── process-book/
    │   └── SKILL.md             # Orchestrator
    ├── convert-book/
    │   └── SKILL.md             # Calibre conversion
    ├── summarize-book/
    │   └── SKILL.md             # Claude-native summary (embeds full template)
    ├── chapter-summaries/
    │   └── SKILL.md             # Chapter extraction + summaries (embeds template)
    ├── chapter-infographics/
    │   └── SKILL.md             # Delegates to image-gen plugin
    ├── book-infographics/
    │   └── SKILL.md             # Delegates to image-gen plugin
    ├── critical-review/
    │   └── SKILL.md             # Claude + WebSearch (embeds review template)
    └── book-index/
        └── SKILL.md             # README, action-items, metadata (embeds template)
```

### plugin.json

```json
{
  "name": "ebook-processing",
  "description": "Process ebooks into organized, AI-enriched library folders with summaries, chapter breakdowns, infographics, critical reviews, and index pages.",
  "version": "1.0.0"
}
```

---

## Skill Details

### process-book (Orchestrator)

**Arguments:** `$0` = path to book file (epub/pdf/acsm) or existing book directory
**Flags:** `--force` (regenerate everything), `--skip <stages>` (comma-separated list of stages to skip)

Workflow:
1. Determine book name from filename (kebab-case)
2. Determine/create book directory under output base
3. Run stages in order, respecting `--skip` and resume logic:
   - `convert-book` (if input is a file, not a directory)
   - `summarize-book`
   - `chapter-summaries`
   - `chapter-infographics`
   - `book-infographics`
   - `critical-review`
   - `book-index`
4. Report results

### summarize-book

**Arguments:** `$0` = book directory path
**Input:** `book-formats/{book-name}_book.md`
**Output:** `summaries/{book-name}_summary_claude_{model}.md` + `.pdf`

Workflow:
1. Read book markdown from `book-formats/`
2. Check for existing Claude summary (resume)
3. Apply the detailed summary template (embedded in SKILL.md)
4. Generate summary using Claude's own capabilities
5. Save as markdown
6. Convert to PDF (using a markdown-to-pdf approach — WeasyPrint via Bash, or the `document-skills:pdf` skill)

### chapter-summaries

**Arguments:** `$0` = book directory path
**Input:** `book-formats/{book-name}_book.md`
**Output:** `chapter-summaries/README.md`, `chapter-{NN}-{slug}.md`, `.pdf` for each

Workflow:
1. Read book markdown
2. Extract chapter boundaries (Claude analyzes the markdown structure)
3. For each chapter (with resume check per chapter):
   - Generate summary using the chapter template
   - Add navigation links (prev/next chapter)
   - Save as markdown
   - Convert to PDF
4. Generate chapter index (README.md) with links to all chapters

### critical-review

**Arguments:** `$0` = book directory path
**Input:** Best available summary from `summaries/` (priority: Claude > Anthropic > OpenAI > Gemini)
**Output:** `summaries/{book-name}_critical_review.md` + `.pdf`

Workflow:
1. Find best available summary
2. Extract 5-7 key claims
3. Use WebSearch to verify each claim against current research
4. Generate structured critical review using the embedded template
5. Save as markdown and PDF

### book-index

**Arguments:** `$0` = book directory path
**Input:** All files in the book directory
**Output:** `README.md`, `README.pdf`, `action-items.md`, `metadata.yaml`, `personal-notes/README.md`, `slide-decks/README.md`

Workflow:
1. Scan book directory for all existing files
2. Read book content and summaries
3. Generate action-items.md (extracted from summaries)
4. Generate README.md using index template (links to all existing files)
5. Generate metadata.yaml (title, author, ISBN, categories, tags)
6. Create personal-notes/ and slide-decks/ stub folders
7. Convert README to PDF
8. Add backlinks to all summary markdown files

---

## Implementation Notes

### MD-to-PDF Conversion

The existing pipeline uses WeasyPrint. Options for the plugin:
1. **WeasyPrint via Bash** — `python -c "import weasyprint; ..."` or a small script
2. **document-skills:pdf skill** — if the skill supports markdown-to-PDF
3. **Calibre's ebook-convert** — `ebook-convert input.md output.pdf`
4. **pandoc** — `pandoc input.md -o output.pdf`

Recommendation: Use **pandoc** if available (most common), fall back to WeasyPrint.

### Book Name Derivation

The book name (kebab-case) is derived from the directory name:
- Input: `~/electronic-books/designing-data-intensive-applications/`
- Book name: `designing-data-intensive-applications`

### Output Base Directory

The default output base is `~/electronic-books/`. This should be documented in the skill but not hardcoded — the user passes the book directory path directly.

---

## Testing Plan

1. **Summarize an existing book** — pick a book that already has `book-formats/*.md`, run `summarize-book`
2. **Chapter summaries** — run on a book with clear chapter headings
3. **Critical review** — verify WebSearch integration finds relevant research
4. **Book index** — run on a fully processed book, verify all links work
5. **Full pipeline** — run `process-book` on a new epub end-to-end

---

*Created: 2026-03-09*
*Last Updated: 2026-03-09*
