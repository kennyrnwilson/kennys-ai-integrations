---
name: summarize-book
description: Generate a comprehensive book summary using Claude. Use when the user wants to summarize a book, create a book summary, or process a book's markdown into a structured summary.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Book Summarizer

Generate a comprehensive, structured book summary using Claude's native capabilities. Reads the book's markdown and produces a detailed summary following a rich template with executive summary, chapter breakdowns, frameworks, critical reflection, and action items.

## Arguments

- `$0` — The book directory path (e.g., `~/electronic-books/designing-data-intensive-applications/`). Must contain a `book-formats/` subdirectory with a `*_book.md` file.
- `--force` — Bypass resume check and regenerate the summary even if one already exists.

If no arguments are provided, ask the user for the book directory path.

## Workflow

### Step 1: Locate Book Content

1. Use Glob to find `book-formats/*_book.md` in the provided book directory (`$0`).
2. Extract the book name from the directory name (kebab-case, e.g., `designing-data-intensive-applications`).
3. If no markdown file is found, tell the user: "No book markdown found in `{directory}/book-formats/`. Please run `convert-book` first to generate the markdown." and stop.

### Step 2: Resume Check

1. Use Glob to check for existing files matching `summaries/*_summary_claude_*.md` in the book directory.
2. If a matching file is found and `--force` was NOT specified, tell the user: "A Claude summary already exists at `{path}`. Use `--force` to regenerate." and stop.
3. If `--force` was specified or no existing summary found, continue.

### Step 3: Read Book Content

1. Read the book markdown file found in Step 1.
2. If the file is very large, read in chunks to fit context. Claude can handle large context, so read as much as possible.
3. Note the total character/word count for the final report.

### Step 4: Generate Summary

Apply the Summary Template below to generate the full summary. Follow the template structure exactly — fill in every section with content derived from the book. Do not skip sections or leave placeholders.

Important style rules:
- No hyperbolic language (avoid "groundbreaking", "revolutionary", "game-changing", "transformative masterpiece")
- Concrete, measurable actions in all actionable sections
- Professional, objective tone throughout
- Every sentence must add value — no filler

### Step 5: Save Summary

1. Determine the model short name from the current Claude model. Use `opus-4.6` for Claude Opus 4.6, `sonnet-4.6` for Sonnet 4.6, etc.
2. Create the `summaries/` directory in the book directory if it doesn't exist.
3. Write the generated summary to: `summaries/{book-name}_summary_claude_{model-short}.md`

### Step 6: Convert to PDF

1. Run via Bash: `pandoc "summaries/{filename}.md" -o "summaries/{filename}.pdf" --pdf-engine=weasyprint`
2. If pandoc is not available, try: `python3 -c "import weasyprint; weasyprint.HTML(filename='summaries/{filename}.md').write_pdf('summaries/{filename}.pdf')"`
3. If neither works, skip PDF conversion and inform the user: "PDF conversion skipped — install pandoc or weasyprint for PDF output."

### Step 7: Report

Tell the user:
- Summary saved successfully
- File paths (markdown and PDF if generated)
- Approximate word count of the summary
- Model used for generation

## Summary Template

Use this template as the exact output format. Fill in every section with content from the book.

````markdown
# Summary of [BOOK TITLE]

**Original book by [AUTHOR NAME]**

---

*[Write a 2-3 paragraph introduction that briefly introduces the book's main focus, what problem it solves, and who it's for. Use engaging language that captures the essence of the book.]*

---

## 🎯 1-Page Executive Summary

**Purpose:** A complete standalone summary that can be read in 5 minutes

#### 🎯 Core Thesis
- [Write 2-4 sentences articulating the book's central argument. What is the author fundamentally claiming? What problem does it solve? Who is it for? Be specific and comprehensive enough that someone could understand the book's purpose from this paragraph alone.]

#### 🔑 Key Themes (3 main ideas)
- **[Theme 1 Title]**: [2-3 sentences explaining this theme. What is it? Why does it matter? How does it relate to the core thesis?]
- **[Theme 2 Title]**: [2-3 sentences explaining this theme. What is it? Why does it matter? How does it relate to the core thesis?]
- **[Theme 3 Title]**: [2-3 sentences explaining this theme. What is it? Why does it matter? How does it relate to the core thesis?]

#### ✅ Top Takeaways (5 items)
- **[Takeaway 1]**: [1-2 sentences providing specific, actionable insight or principle]
- **[Takeaway 2]**: [1-2 sentences providing specific, actionable insight or principle]
- **[Takeaway 3]**: [1-2 sentences providing specific, actionable insight or principle]
- **[Takeaway 4]**: [1-2 sentences providing specific, actionable insight or principle]
- **[Takeaway 5]**: [1-2 sentences providing specific, actionable insight or principle]

---

## 📊 Ultra-Compact Summary

**Three-Sentence Snapshot:**
1.  [First sentence: What is the book and what's its main argument?]
2.  [Second sentence: What's the key framework, structure, or approach the book uses?]
3.  [Third sentence: What's the outcome or key benefit for the reader?]

**One-Paragraph Overview:**
- [Write a comprehensive 4-6 sentence paragraph that someone could read to understand the book's essence. Include: the target audience, the core problem addressed, the main solution/framework offered, the author's unique perspective, and the book's key value proposition.]

---

## ✅ Key Actionable Interventions (10 items)

1.  **[Intervention 1 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
2.  **[Intervention 2 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
3.  **[Intervention 3 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
4.  **[Intervention 4 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
5.  **[Intervention 5 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
6.  **[Intervention 6 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
7.  **[Intervention 7 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
8.  **[Intervention 8 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
9.  **[Intervention 9 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]
10. **[Intervention 10 Title]**: [2-3 sentences describing a specific, practical action readers can take. Be concrete and specific.]

---

## 📌 Extended Overview (Approx. 2 pages)

#### The Core Argument
[Write 2-3 paragraphs explaining the book's central argument in detail. What is the fundamental claim? What assumptions does it rest on? What's the logical structure of the argument? Be thorough and analytical.]

#### Main Supporting Themes
[Break down the book's structure into 3-5 major supporting themes or sections. For each theme, write 2-3 paragraphs explaining:
- What it covers
- How it supports the core argument
- Key concepts or frameworks introduced
- How it connects to other themes]

1.  **[Major Theme 1 Title]**: [Description as outlined above]
2.  **[Major Theme 2 Title]**: [Description as outlined above]
3.  **[Major Theme 3 Title]**: [Description as outlined above]

#### Intended Audience & Applications
[Write 2-3 paragraphs covering:
- Who is the primary audience?
- What secondary audiences might benefit?
- In what contexts/situations is this book most applicable?
- What prerequisite knowledge is helpful?
- What specific use cases does it address?]

#### The Author's Unique Perspective
[Write 1-2 paragraphs explaining:
- What makes the author qualified to write this book?
- What unique angle or perspective do they bring?
- How does this book fill a gap in existing literature?
- What distinguishes it from similar books?]

---

## 📖 Detailed Chapter-by-Chapter Breakdown

**[Part/Section Title if applicable]**

### Chapter [#]: [Chapter Title]

#### 📝 Chapter Summary
[Write 1-2 substantial paragraphs (6-10 sentences total) that thoroughly summarize this chapter. Include:
- The main argument or thesis of this chapter
- How the author builds the case (structure and logic)
- Key evidence, examples, or data presented
- How it advances the book's overall narrative]

#### 🎯 Core Argument
[1-2 sentences stating the fundamental claim this chapter makes. What is the author trying to convince you of?]

#### 📚 Key Concepts & Definitions
- **[Term/Concept 1]**: [Definition and significance - 1-2 sentences]
- **[Term/Concept 2]**: [Definition and significance - 1-2 sentences]
- **[Term/Concept 3]**: [Definition and significance - 1-2 sentences]
[Include all new vocabulary, frameworks, or mental models introduced in this chapter]

#### 🔑 Key Takeaways
1. [Important insight #1 - 1-2 sentences with specific detail]
2. [Important insight #2 - 1-2 sentences with specific detail]
3. [Important insight #3 - 1-2 sentences with specific detail]
4. [Important insight #4 - 1-2 sentences with specific detail]
5. [Important insight #5 - 1-2 sentences with specific detail]
[Aim for 4-6 takeaways per chapter]


#### 💬 Memorable Quotes
> "[Direct quote from the chapter that captures a key insight]"
> "[Another significant quote worth remembering]"
[Include 1-3 particularly impactful or memorable quotes]

#### ✅ Actionable Advice
1. **[Action 1]**: [2-3 sentences describing a specific, practical action with clear implementation steps]
2. **[Action 2]**: [2-3 sentences describing a specific, practical action with clear implementation steps]
3. **[Action 3]**: [2-3 sentences describing a specific, practical action with clear implementation steps]
[Focus on concrete, implementable recommendations]

#### 🤔 Why This Matters
[1-2 sentences explaining the practical significance of this chapter. How does this knowledge change how the reader should think or act? What problems does it solve?]


---

[Repeat the above structure for each chapter in the book.]

---

## 🎯 Practical Implementation Guide

#### Quick Wins (Start Here)
1.  **[Quick Win 1]**: [2-3 sentences describing an easy, immediate action that takes minimal time but delivers quick value]
2.  **[Quick Win 2]**: [2-3 sentences describing an easy, immediate action that takes minimal time but delivers quick value]
3.  **[Quick Win 3]**: [2-3 sentences describing an easy, immediate action that takes minimal time but delivers quick value]
4.  **[Quick Win 4]**: [2-3 sentences describing an easy, immediate action that takes minimal time but delivers quick value]
5.  **[Quick Win 5]**: [2-3 sentences describing an easy, immediate action that takes minimal time but delivers quick value]

#### Core Practices (Build These Habits)
1.  **[Core Practice 1]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]
2.  **[Core Practice 2]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]
3.  **[Core Practice 3]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]
4.  **[Core Practice 4]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]
5.  **[Core Practice 5]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]
6.  **[Core Practice 6]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]
7.  **[Core Practice 7]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]
8.  **[Core Practice 8]**: [2-3 sentences describing a fundamental habit or practice to build over weeks/months]

#### Advanced Applications (Level Up)
1.  **[Advanced Application 1]**: [2-3 sentences describing a sophisticated, high-impact application requiring significant investment]
2.  **[Advanced Application 2]**: [2-3 sentences describing a sophisticated, high-impact application requiring significant investment]
3.  **[Advanced Application 3]**: [2-3 sentences describing a sophisticated, high-impact application requiring significant investment]
4.  **[Advanced Application 4]**: [2-3 sentences describing a sophisticated, high-impact application requiring significant investment]
5.  **[Advanced Application 5]**: [2-3 sentences describing a sophisticated, high-impact application requiring significant investment]

#### Common Pitfalls to Avoid
-   **[Pitfall 1]**: [1-2 sentences describing a common mistake or trap]
-   **[Pitfall 2]**: [1-2 sentences describing a common mistake or trap]
-   **[Pitfall 3]**: [1-2 sentences describing a common mistake or trap]
-   **[Pitfall 4]**: [1-2 sentences describing a common mistake or trap]
-   **[Pitfall 5]**: [1-2 sentences describing a common mistake or trap]
-   **[Pitfall 6]**: [1-2 sentences describing a common mistake or trap]
-   **[Pitfall 7]**: [1-2 sentences describing a common mistake or trap]
-   **[Pitfall 8]**: [1-2 sentences describing a common mistake or trap]

---

## 📚 Key Frameworks & Mental Models

* **[Framework 1 Name]**
    * **Purpose**: [1 sentence describing what problem this framework solves or what it helps you understand]
    * **Components**: [2-4 sentences breaking down the key elements or parts of this framework]
    * **Application**: [1-2 sentences describing how to use this framework in practice]
    * **Example**: [1-2 sentences providing a concrete example of the framework in action]

* **[Framework 2 Name]**
    * **Purpose**: [1 sentence describing what problem this framework solves or what it helps you understand]
    * **Components**: [2-4 sentences breaking down the key elements or parts of this framework]
    * **Application**: [1-2 sentences describing how to use this framework in practice]
    * **Example**: [1-2 sentences providing a concrete example of the framework in action]

* **[Framework 3 Name]**
    * **Purpose**: [1 sentence describing what problem this framework solves or what it helps you understand]
    * **Components**: [2-4 sentences breaking down the key elements or parts of this framework]
    * **Application**: [1-2 sentences describing how to use this framework in practice]
    * **Example**: [1-2 sentences providing a concrete example of the framework in action]

[Continue with additional frameworks as needed - aim for 5-7 key frameworks]

---

## 💭 Critical Reflection

**Strengths:**
-   **[Strength 1]**: [1-2 sentences explaining what the book does exceptionally well]
-   **[Strength 2]**: [1-2 sentences explaining what the book does exceptionally well]
-   **[Strength 3]**: [1-2 sentences explaining what the book does exceptionally well]
-   **[Strength 4]**: [1-2 sentences explaining what the book does exceptionally well]
-   **[Strength 5]**: [1-2 sentences explaining what the book does exceptionally well]

**Limitations:**
-   **[Limitation 1]**: [1-2 sentences explaining where the book falls short or what it doesn't cover]
-   **[Limitation 2]**: [1-2 sentences explaining where the book falls short or what it doesn't cover]
-   **[Limitation 3]**: [1-2 sentences explaining where the book falls short or what it doesn't cover]
-   **[Limitation 4]**: [1-2 sentences explaining where the book falls short or what it doesn't cover]
-   **[Limitation 5]**: [1-2 sentences explaining where the book falls short or what it doesn't cover]

**Counterarguments & Critiques:**

* **[Main Argument 1 from the book]**
    * **Author's Position**: [1-2 sentences stating what the author argues]
    * **Supporting Evidence**: [1-2 sentences describing how the author supports this claim]
    * **Potential Counterarguments**:
        * [Counterargument A]: [1-2 sentences presenting an alternative view]
        * [Counterargument B]: [1-2 sentences presenting an alternative view]
        * [Counterargument C]: [1-2 sentences presenting an alternative view]
    * **Devil's Advocate**: "[1-2 sentences presenting a provocative challenge to this argument]"
    * **Context Matters**: [1-2 sentences discussing when the argument holds vs. when it might not]

* **[Main Argument 2 from the book]**
    * **Author's Position**: [1-2 sentences stating what the author argues]
    * **Supporting Evidence**: [1-2 sentences describing how the author supports this claim]
    * **Potential Counterarguments**:
        * [Counterargument A]: [1-2 sentences presenting an alternative view]
        * [Counterargument B]: [1-2 sentences presenting an alternative view]
        * [Counterargument C]: [1-2 sentences presenting an alternative view]
    * **Devil's Advocate**: "[1-2 sentences presenting a provocative challenge to this argument]"
    * **Context Matters**: [1-2 sentences discussing when the argument holds vs. when it might not]

**Common Critiques of This Type of Book:**
-   [Critique 1]: [1-2 sentences describing a common criticism of books in this genre/category]
-   [Critique 2]: [1-2 sentences describing a common criticism of books in this genre/category]
-   [Critique 3]: [1-2 sentences describing a common criticism of books in this genre/category]
-   [Critique 4]: [1-2 sentences describing a common criticism of books in this genre/category]

**Questions to Consider:**
-   [Thought-provoking question 1 that challenges or extends the book's ideas]
-   [Thought-provoking question 2 that challenges or extends the book's ideas]
-   [Thought-provoking question 3 that challenges or extends the book's ideas]
-   [Thought-provoking question 4 that challenges or extends the book's ideas]

**Complementary & Contrasting Reading:**
-   **Complementary**:
    * [Book Title] by [Author] ([Brief description of how it complements])
    * [Book Title] by [Author] ([Brief description of how it complements])
    * [Book Title] by [Author] ([Brief description of how it complements])
    * [Book Title] by [Author] ([Brief description of how it complements])
-   **Contrasting**:
    * [Book Title/Topic] ([Brief description of contrasting perspective])
    * [Book Title/Topic] ([Brief description of contrasting perspective])
    * [Book Title/Topic] ([Brief description of contrasting perspective])
-   **Prerequisites**: [What knowledge or experience would be helpful before reading this book]
-   **Follow-up**: [What books or topics should the reader explore next to deepen their understanding]

---

## 🔄 Next Steps & Application

**Immediate Actions (This Week):**
1.  **[Action 1]**: [2-3 sentences describing a specific action to take this week, with clear success criteria]
2.  **[Action 2]**: [2-3 sentences describing a specific action to take this week, with clear success criteria]
3.  **[Action 3]**: [2-3 sentences describing a specific action to take this week, with clear success criteria]

**Short-Term Goals (This Month):**
-   **[Goal 1]**: [2-3 sentences describing what to accomplish this month. Include: Success criteria]
-   **[Goal 2]**: [2-3 sentences describing what to accomplish this month. Include: Success criteria]
-   **[Goal 3]**: [2-3 sentences describing what to accomplish this month. Include: Success criteria]

**Long-Term Integration (This Quarter/Year):**
-   **[Goal 1]**: [2-3 sentences describing a longer-term application or integration. Include: Success criteria]
-   **[Goal 2]**: [2-3 sentences describing a longer-term application or integration. Include: Success criteria]
-   **[Goal 3]**: [2-3 sentences describing a longer-term application or integration. Include: Success criteria]

**Resources Needed:**
-   **[Resource Category 1]**: [1-2 sentences describing what resources (time, tools, support, etc.) are needed]
-   **[Resource Category 2]**: [1-2 sentences describing what resources (time, tools, support, etc.) are needed]
-   **[Resource Category 3]**: [1-2 sentences describing what resources (time, tools, support, etc.) are needed]
-   **[Resource Category 4]**: [1-2 sentences describing what resources (time, tools, support, etc.) are needed]
````

## Style Guidelines

- **No hyperbolic language** — avoid "groundbreaking", "revolutionary", "game-changing", "transformative masterpiece". Describe the book's contributions accurately and let the content speak for itself.
- **Concrete, measurable actions** — every actionable item should be specific enough that a reader knows exactly what to do.
- **Professional, objective tone** — maintain analytical distance while being engaging.
- **Every sentence adds value** — no filler, no padding, no restatement of obvious points.
- **Use emojis consistently** as shown in the template for visual navigation.

## Error Handling

- **Book markdown not found**: Tell the user to run `convert-book` first.
- **Directory doesn't exist**: Tell the user the directory path is invalid.
- **PDF conversion fails**: Skip PDF, inform user, continue. The markdown summary is the primary output.
- **Book too large to read at once**: Read in chunks, process the full content across multiple reads.
