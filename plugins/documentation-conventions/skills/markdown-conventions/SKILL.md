---
name: markdown-conventions
description: Kenny's markdown file conventions — bidirectional parent/child links, backlink at top, relative paths, kebab-case filenames, and the Related/Tags/dates footer. Use when creating or restructuring markdown files, adding a note to the knowledge library or book library, or writing documentation in any repo. Covers both the global convention and the portal hub's Astro-driven variant.
user-invocable: true
---

# Markdown Conventions

## Which convention applies

Two forms exist. The difference is forced by Astro's content-collection slug rules
and published URLs, not by preference.

| | Global — everywhere | `personal-portal/docs/system-architecture/` |
|---|---|---|
| Index file | `README.md` | `index.md` |
| Frontmatter | none | `---`<br>`title: X`<br>`---` |
| Backlink | `← [Back to Parent](./README.md)` | `← [Back to Section](../)` |
| Footer | see below | none |

`personal-portal/docs/superpowers/` uses a third form: no frontmatter,
`← [Back to plans](./)` or `← [Back to specs](./)`, no footer.

## The Related / Tags / dates footer

**Required** in `knowledge-library` and `book-library`, where tags and backlinks
feed Zettelkasten retrieval and the Pagefind index. **Optional** in app repos and
the portal hub. Do not retrofit it onto existing files.

## Core Principles

1. **Bidirectional Links** - Child files must reference parents, and parents must link to children
2. **Consistent Structure** - Every markdown file follows a standard format
3. **Clear Navigation** - Users can easily move up and down the hierarchy
4. **Relative Paths** - All links use relative paths for portability

## File Creation Rules

### 1. Parent-Child Relationships

When creating a **child markdown file** that belongs to a parent:

**Parent File Must:**
- Contain a link to the child file in an appropriate section
- Use relative paths: `[Child Topic](./child-topic.md)`
- Organize child links in a logical structure (list, table, or sections)

**Child File Must:**
- Start with a backlink to the parent at the top (after the title)
- Use format: `← [Back to Parent](../parent.md)` or `← [Back to Parent Directory](./README.md)`
- Include the backlink before any other content

### 2. Markdown File Template

Every markdown file should follow this structure:

```markdown
# [Title]

← [Back to Parent](../parent.md)

[Brief description or introduction]

## [First Section]

[Content]

## [Second Section]

[Content]

---

**Related:**
- [Related Topic 1](./related-topic-1.md)
- [Related Topic 2](./related-topic-2.md)

**Tags:** #tag1 #tag2 #tag3

*Created: YYYY-MM-DD*
*Last Updated: YYYY-MM-DD*
```

### 3. README.md Files

Every directory should have a `README.md` that serves as the index/hub:

```markdown
# [Directory Name]

← [Back to Parent](../README.md)

[Description of this directory's purpose]

## Contents

- [Topic 1](./topic-1.md) - Brief description
- [Topic 2](./topic-2.md) - Brief description
- [Subdirectory](./subdirectory/README.md) - Brief description

---

*Last Updated: YYYY-MM-DD*
```

Repo-level conventions — the documentation locations, and the `README.md` /
`CLAUDE.md` templates — live in the portal hub's `documentation-standard.md`,
not here.

## Examples

### Example 1: Creating a Child Note

**Scenario:** Creating `wellbeing/sleep.md` under `permanent-notes/wellbeing/README.md`

**Step 1:** Update parent (`wellbeing/README.md`):
```markdown
## Topics

- [Sleep](./sleep.md) - Sleep hygiene, circadian rhythms, and rest
- [Fitness](./fitness.md) - Exercise and physical health
```

**Step 2:** Create child (`wellbeing/sleep.md`):
```markdown
# Sleep

← [Back to Wellbeing](./README.md)

Notes and insights about sleep hygiene, circadian rhythms, and rest.

## Sleep Hygiene

[Content about sleep hygiene]

## Circadian Rhythms

[Content about circadian rhythms]

---

**Related:**
- [Fitness](./fitness.md)
- [Mental Health](./mental-health.md)

**Tags:** #wellbeing #sleep #health

*Created: 2025-01-15*
*Last Updated: 2025-01-15*
```

### Example 2: Multi-Level Navigation

**Scenario:** Creating `permanent-notes/professional/technical-skills/python.md`

**File Structure:**
```
permanent-notes/
├── README.md
└── professional/
    ├── README.md
    └── technical-skills/
        ├── README.md
        └── python.md
```

**`python.md` content:**
```markdown
# Python Programming

← [Back to Technical Skills](./README.md) | [Professional](../README.md) | [Permanent Notes](../../README.md)

Notes and insights about Python programming.

## Fundamentals

[Content]

## Advanced Topics

[Content]

---

**Related:**
- [JavaScript](./javascript.md)
- [Software Architecture](../software-architecture.md)

**Tags:** #professional #technical-skills #python #programming

*Created: 2025-01-15*
*Last Updated: 2025-01-15*
```

## Link Formats

### Relative Path Examples

```markdown
# Same directory
[File](./file.md)

# Parent directory
[Parent](../README.md)

# Sibling directory
[Sibling](../sibling-dir/file.md)

# Grandparent directory
[Grandparent](../../README.md)

# Child directory
[Child](./child-dir/README.md)
```

### Navigation Breadcrumbs

For deeply nested files, provide a breadcrumb trail:

```markdown
← [Back to Immediate Parent](./README.md) | [Section](../README.md) | [Root](../../README.md)
```

## Checklist for Creating New Markdown Files

Before completing a markdown file creation task, verify:

- [ ] **Backlink added** - Child file has `← [Back to Parent](...)` link at the top
- [ ] **Parent updated** - Parent file contains link to the new child
- [ ] **Title present** - File starts with `# Title`
- [ ] **Description added** - Brief description after the backlink
- [ ] **Sections organized** - Content is in logical sections with `##` headings
- [ ] **Footer present where required** - Related links, Tags, and Created/Last
      Updated dates, per "The Related / Tags / dates footer" above: required in
      `knowledge-library` and `book-library`, optional elsewhere, never retrofitted
- [ ] **Relative paths used** - All links use `./` or `../` notation
- [ ] **Links tested** - All internal links point to valid files

## Special Cases

### Cross-Referencing Between Branches

When linking between different sections (e.g., Professional → Wellbeing):

```markdown
**Related Topics:**
- [Sleep Quality](../../wellbeing/sleep.md) - Impact of sleep on productivity
- [Time Management](../../productivity/time-management.md)
```

### Index Files

For directories with many files, create an organized index:

```markdown
# Topic Index

← [Back to Parent](../README.md)

## A-C
- [Alpha](./alpha.md)
- [Beta](./beta.md)

## D-F
- [Delta](./delta.md)

## By Category

### Fundamentals
- [Basics](./basics.md)
- [Introduction](./introduction.md)

### Advanced
- [Expert Topics](./expert.md)
```

## Automation Helpers

When Claude Code creates markdown files, it should:

1. **Always ask for confirmation** before creating parent-child relationships
2. **Update both parent and child** in the same operation
3. **Use consistent naming** - kebab-case for files (e.g., `my-topic.md`)
4. **Verify paths** - Check that parent directories exist
5. **Create README.md first** - When creating new directories, start with README

## Anti-Patterns to Avoid

❌ **Don't:**
- Create orphan files (no parent link)
- Use absolute paths (breaks portability)
- Forget to update parent when adding child
- Use spaces in filenames (use hyphens instead)
- Create circular references
- Skip backlinks "because it's obvious"

✅ **Do:**
- Always create bidirectional links
- Use relative paths consistently
- Update parent immediately when adding child
- Use kebab-case for filenames
- Maintain clear hierarchy
- Include backlinks even for "obvious" relationships

---

**Version:** 1.0
**Last Updated:** 2025-01-15
