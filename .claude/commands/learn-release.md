---
description: Learn about a Claude Code release from compiled research
argument-hint: [version] [optional: specific question]
---

# Learn: Claude Code v$ARGUMENTS

Load all compiled knowledge about this version and be ready to discuss.

**User Question:** If a specific question was provided after the version number, focus your synthesis and response on answering that question directly using the compiled research.

---

## Step 1: Parse Arguments

The `$ARGUMENTS` may contain:
- Just a version number: `2.0.74`
- Version + question: `2.0.74 How do I enable LSP for Python?`

Extract the version number (first token) and any follow-up question.

---

## Step 2: Load All Context

Read these files to gather everything we know about this version:

1. **Research files** (if exist) - Deep dive analysis
   ```
   ~/agents/sys-admin/data/claude-code/research/{version}/
   ```
   Read `index.md` and any topic-specific files in this directory.

2. **Changelog entry** - Search for the version in:
   ```
   .claude/skills/claude-code-tracker/changelog.md
   ```

3. **Relevance entry** - Search for the version in:
   ```
   .claude/skills/claude-code-tracker/relevance.md
   ```

4. **Symbiont context** - Understand why features matter:
   ```
   .claude/skills/claude-code-tracker/context.md
   ```

---

## Step 3: Synthesize Knowledge

After reading, mentally organize:

- **What changed** in this version (features, fixes, improvements)
- **Tier classification** (🚀 Major | ✨ Notable | 🔧 Minor | 🐛 Patch)
- **Symbiont relevance** (🚀 Critical | ✨ High | 🔧 Medium | Skip)
- **Key Symbiont impacts** (which specialists/primitives affected)
- **Action items** (things to test or implement)

---

## Step 4: Respond Based on Input

### If user provided a specific question:

Answer the question directly using the compiled research. Structure your response as:

1. **Direct answer** to the question
2. **Supporting details** from the research files
3. **Practical guidance** (commands, config, examples)
4. **Gaps** - If the research doesn't fully cover the question, note what's missing

### If just a version number (no question):

Acknowledge you've loaded the context and invite questions:

> Loaded v{version} context. This was a [tier] release with [relevance] Symbiont relevance.
>
> Key features: [list main features]
>
> What would you like to explore?

---

## Dialogue Guidelines

When answering questions:

- **Connect to Symbiont** - Relate features back to specialists, MCP, hooks, etc.
- **Be practical** - Suggest how to test or use features
- **Reference sources** - If we have deep research, cite specific sections
- **Identify gaps** - If we don't have info, suggest running `/research-release {version} {question}`

Common questions to be ready for:
- "How does [feature] work?"
- "How would I use this in Symbiont?"
- "What's the practical benefit?"
- "Should I update my workflow for this?"
- "What should I test first?"
