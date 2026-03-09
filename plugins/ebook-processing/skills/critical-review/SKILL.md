---
name: critical-review
description: Generate an evidence-based critical review of a book's key claims using web research. Use when the user wants fact-checking, claim verification, or a critical analysis of a book.
argument-hint: <book-directory> [--force]
user-invocable: true
---

# Critical Review Generator

Generate an evidence-based critical review of a book by extracting key claims from its summary and researching each claim using web search. Produces a structured document with per-claim analysis, credibility ratings, and an overall assessment.

## Arguments

- `$0` — The book directory path (e.g., `~/electronic-books/designing-data-intensive-applications/`). Must contain a `summaries/` subdirectory with at least one summary file.
- `--force` — Bypass resume check and regenerate the critical review even if one already exists.

If no arguments are provided, ask the user for the book directory path.

## Workflow

### Step 1: Locate Best Summary

1. Use Glob to search `summaries/` in the book directory for available summary files.
2. Select the best summary using this priority order:
   - `*_summary_claude_*` (Claude-generated, highest quality)
   - `*_summary_anthropic_*` (Anthropic API)
   - `*_summary_openai_*` (OpenAI API)
   - `*_summary_gemini_*` (Gemini)
   - Any other `*_summary_*` file
3. If no summary is found, tell the user: "No summary found in `{directory}/summaries/`. Please run `summarize-book` first." and stop.
4. Read the selected summary file.

### Step 2: Resume Check

1. Use Glob to check for existing `summaries/*_critical_review.md` in the book directory.
2. If found and `--force` was NOT specified, tell the user: "A critical review already exists at `{path}`. Use `--force` to regenerate." and stop.

### Step 3: Extract Key Claims

1. Read the summary and identify 5-7 significant claims, recommendations, or action items that can be verified with evidence.
2. Focus on claims that are:
   - Specific enough to research (not vague platitudes)
   - Consequential (if wrong, it matters)
   - Testable (can find supporting or refuting evidence)
3. Present the claims to the user before proceeding: "Identified {N} key claims to research. Proceeding with analysis..."

### Step 4: Research Each Claim

For each claim, use WebSearch to find:
- Scientific studies or research supporting or refuting the claim
- Expert opinions or criticisms
- Counter-arguments or alternative perspectives
- Any controversies surrounding the topic

Conduct 2-3 web searches per claim to get a balanced perspective. Look for peer-reviewed sources, expert commentary, and reputable publications.

### Step 5: Generate Critical Review

Using the Critical Review Template below, produce a structured document with:
- Executive summary with quick assessment table
- Per-claim analysis with supporting evidence, criticisms, and credibility ratings
- Overall assessment of strengths and weaknesses
- Sources and references

### Step 6: Save

1. Extract the book name from the directory (kebab-case).
2. Write to `summaries/{book-name}_critical_review.md`.
3. Convert to PDF: `pandoc "summaries/{filename}.md" -o "summaries/{filename}.pdf" --pdf-engine=weasyprint` via Bash. Skip if pandoc is not available.

### Step 7: Report

Tell the user:
- Number of claims analyzed
- Overall credibility assessment
- File paths (markdown and PDF)
- Any claims that were particularly well-supported or concerning

## Critical Review Template

Use this template as the exact output format.

````markdown
# 📚 Critical Review: [Book Title]

> *An evidence-based analysis of key claims and recommendations*

---

## 📋 Executive Summary

### Overview
[2-3 paragraphs about the book's overall credibility and main findings from the research]

### Quick Assessment Table

| Aspect | Rating | Notes |
|--------|--------|-------|
| Scientific Accuracy | ⭐⭐⭐⭐☆ | [Note] |
| Practical Applicability | ⭐⭐⭐⭐⭐ | [Note] |
| Balanced Perspective | ⭐⭐⭐☆☆ | [Note] |
| Overall Credibility | ⭐⭐⭐⭐☆ | [Note] |

### Key Takeaways
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

---

## 🔬 Key Claims Analysis

### Claim 1: [Descriptive Title]

#### 📌 The Claim
> "[Quote or paraphrase the specific claim from the book]"

#### ✅ Supporting Evidence

##### Primary Research
- **[Study Name]** ([Year]): [Key finding]
- **[Study Name]** ([Year]): [Key finding]

##### Expert Support
- [Expert opinions supporting this claim]

#### ⚠️ Criticisms & Counter-Arguments

##### Scientific Concerns
- [Concern 1]
- [Concern 2]

##### Alternative Perspectives
- [Alternative view]

#### 📊 Credibility Assessment

| Factor | Assessment | Details |
|--------|------------|---------|
| Research Support | Strong/Moderate/Weak | [Explanation] |
| Expert Consensus | High/Mixed/Low | [Explanation] |
| Potential Bias | Low/Medium/High | [Explanation] |

#### 🎯 Verdict: [🟢 High / 🟡 Medium / 🔴 Low] Credibility
[1-2 sentence explanation]

---

[Repeat the above structure for each claim]

---

## 📊 Overall Assessment

### ✅ Strengths

#### Scientific Foundation
- [Strength related to science]

#### Practical Value
- [Strength related to applicability]

#### Unique Contributions
- [What makes this book valuable]

### ⚠️ Weaknesses

#### Limitations
- [Weakness 1]

#### Potential Concerns
- [Weakness 2]

#### Accessibility Issues
- [Weakness 3]

### 🎯 Who Should Read This Book?

#### Ideal Readers
> [Description of who would benefit most]

#### Caveats
- [Important caveat 1]
- [Important caveat 2]

---

## 📖 Sources & References

### Academic Sources
1. **[Author]** - *[Title]* ([Year]) - [Relevance]
2. **[Author]** - *[Title]* ([Year]) - [Relevance]

### Expert Commentary
- [Source 1]
- [Source 2]

### Additional Reading
- [Recommended resource]

---

## 📝 Methodology Note

*This critical review was generated using AI with web search capabilities. Claims were verified against peer-reviewed research where available. Always consult qualified professionals for health, medical, or financial decisions.*

---
````

## Style Guidelines

- Maintain objectivity — present evidence fairly, not just confirming or refuting
- Use star ratings (⭐) consistently for assessments
- Cite specific studies, papers, and experts by name when found
- Use the credibility traffic light system: 🟢 High, 🟡 Medium, 🔴 Low
- Avoid hyperbolic language in assessments

## Error Handling

- **No summary found**: Tell the user to run `summarize-book` first.
- **WebSearch unavailable**: Inform the user that web research could not be performed and generate a review based solely on internal analysis of the summary content.
- **Few claims found**: If fewer than 5 verifiable claims can be extracted, proceed with whatever is available and note the limitation.
- **PDF conversion fails**: Skip PDF, inform user, continue.
