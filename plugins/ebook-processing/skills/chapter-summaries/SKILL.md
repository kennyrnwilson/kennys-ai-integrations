---
name: chapter-summaries
description: Extract and summarize individual chapters from a book's markdown. Use when the user wants chapter-by-chapter summaries, chapter breakdowns, or detailed chapter analysis.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Chapter Summaries Generator

Extract and summarize individual chapters from a book's markdown, producing a separate summary file for each chapter with key concepts, takeaways, actionable advice, and inter-chapter connections.

## Arguments

- `$0` — The book directory path (e.g., `~/electronic-books/designing-data-intensive-applications/`). Must contain a `book-formats/` subdirectory with a `*_book.md` file.
- `--force` — Bypass resume checks and regenerate all chapter summaries, even if they already exist.

If no arguments are provided, ask the user for the book directory path.

## Workflow

### Step 1: Locate Book Content

1. Use Glob to find `book-formats/*_book.md` in the provided book directory (`$0`).
2. Extract the book name from the directory name (kebab-case).
3. If no markdown file is found, tell the user: "No book markdown found in `{directory}/book-formats/`. Please run `convert-book` first." and stop.

### Step 2: Resume Check

1. Check if `chapter-summaries/README.md` exists in the book directory.
2. If it exists and `--force` was NOT specified, tell the user: "Chapter summaries already exist at `{directory}/chapter-summaries/`. Use `--force` to regenerate." and stop.
3. If `--force` was specified or no existing summaries found, continue.

### Step 3: Read Book Content

1. Read the full book markdown file.
2. If the file is very large, read in chunks to cover all content.

### Step 4: Extract Chapters

1. Analyze the markdown to identify chapter boundaries. Look for patterns like:
   - `## Chapter N: Title`
   - `# Chapter N`
   - `## Part N: Title` followed by `### Chapter N: Title`
   - Bold chapter numbers or headings
   - Any consistent chapter delimiter pattern used in the book
2. List all chapters found with their titles and approximate line ranges.
3. Present the chapter list to the user before proceeding: "Found {N} chapters. Proceeding with summaries..."

### Step 5: Summarize Each Chapter

For each chapter, in order:

1. **Per-chapter resume check**: If `chapter-summaries/chapter-{NN}-{slug}.md` already exists and `--force` was NOT specified, skip this chapter and report: "Skipping chapter {N} (already exists)."

2. **Extract content**: Extract the full text content for this chapter from the book markdown.

3. **Generate summary**: Using the Chapter Summary Template below, generate a complete summary for this chapter. Fill in every section — do not leave placeholders.

4. **Add navigation links**: At the top of the chapter summary, add:
   ```
   ← [Previous: Chapter {N-1} Title](chapter-{NN-1}-{slug}.md) | [Index](README.md) | [Next: Chapter {N+1} Title](chapter-{NN+1}-{slug}.md) →
   ```
   Omit "Previous" for the first chapter and "Next" for the last chapter.

5. **Save**: Write to `chapter-summaries/chapter-{NN}-{slug}.md` where `{NN}` is zero-padded (01, 02, etc.) and `{slug}` is the chapter title in kebab-case.

6. **Convert to PDF**: Run `pandoc "chapter-summaries/{filename}.md" -o "chapter-summaries/{filename}.pdf" --pdf-engine=weasyprint` via Bash. If pandoc is not available, skip PDF and continue.

7. **Report progress**: "Completed chapter {N} of {total}: {title}"

### Step 6: Generate Chapter Index

Create `chapter-summaries/README.md` with:

```markdown
# Chapter Summaries: [Book Title]

**By [Author Name]**

Detailed summaries for each chapter with key concepts, takeaways, and actionable advice.

---

## Table of Contents

1. [Chapter 1: {Title}](chapter-01-{slug}.md)
2. [Chapter 2: {Title}](chapter-02-{slug}.md)
...
```

Include links to both the markdown and PDF versions for each chapter.

### Step 7: Convert Index to PDF

Run `pandoc "chapter-summaries/README.md" -o "chapter-summaries/README.pdf" --pdf-engine=weasyprint` via Bash. Skip if pandoc is not available.

### Step 8: Report

Tell the user:
- Total chapters summarized
- Any chapters skipped (due to resume)
- File paths for the chapter index and individual summaries
- Whether PDF conversion succeeded

## Chapter Summary Template

Use this template as the exact output format for each chapter summary.

````markdown
# Chapter {N}: {Chapter Title}

← [Previous: {Prev Title}]({prev-file}) | [Index](README.md) | [Next: {Next Title}]({next-file}) →

---

## 📝 Summary

[2-4 paragraphs capturing the main narrative, arguments, and flow of the chapter. Focus on what the author is trying to convey and how they build their argument.]

## 🎯 Core Argument

[1-2 sentences distilling the central thesis of this chapter. What is the single most important point the author makes?]

## 🔑 Key Concepts

| Concept | Definition |
|---------|------------|
| **[Term 1]** | [Brief definition or explanation] |
| **[Term 2]** | [Brief definition or explanation] |
| **[Term 3]** | [Brief definition or explanation] |

## 💡 Key Takeaways

1. [First major insight or lesson from this chapter]
2. [Second major insight or lesson]
3. [Third major insight or lesson]
4. [Fourth major insight or lesson]
5. [Fifth major insight or lesson - if applicable]

## ✅ Actionable Advice

- [ ] [Specific, concrete action the reader can take based on this chapter]
- [ ] [Another specific action with clear implementation steps]
- [ ] [Third action item that applies the chapter's teachings]

## 💬 Notable Quotes

> "[Most impactful direct quote from the chapter that captures its essence]"

> "[Second notable quote - if there's another particularly memorable one]"

## 🔗 Connections

- **Previous Chapter:** [How this chapter builds on or relates to what came before - leave blank if N/A]
- **Next Chapter:** [What this chapter sets up for what comes next - leave blank if N/A]
- **Related Themes:** [Broader themes or ideas this chapter connects to]
````

## Tone Guidelines

- Write in a clear, direct, and objective tone
- Avoid hyperbolic or promotional language — do not use phrases like "groundbreaking exploration", "revolutionary", "game-changing", "transformative masterpiece"
- Describe the chapter's contributions accurately and let the content speak for itself
- Use precise language that conveys the author's ideas without inflating their significance

## Error Handling

- **Book markdown not found**: Tell the user to run `convert-book` first.
- **No chapters detected**: Tell the user the book markdown may not have clear chapter boundaries and suggest manual processing.
- **PDF conversion fails**: Skip PDF for that chapter, continue with remaining chapters.
- **Single chapter fails**: Log the error, skip it, continue with remaining chapters. Report skipped chapters at the end.
