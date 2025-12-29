---
description: Learn about a Claude Code release from compiled research
argument-hint: [version]
---

# Learn: Claude Code v$ARGUMENTS

Load all compiled knowledge about version **$ARGUMENTS** and be ready to discuss.

---

## Step 1: Load All Context

Read these files to gather everything we know about this version:

1. **Research file** (if exists) - Deep dive analysis
   ```
   ~/agents/sys-admin/data/claude-code/research/$ARGUMENTS.md
   ```

2. **Changelog entry** - Search for v$ARGUMENTS in:
   ```
   .claude/skills/claude-code-tracker/changelog.md
   ```

3. **Relevance entry** - Search for v$ARGUMENTS in:
   ```
   .claude/skills/claude-code-tracker/relevance.md
   ```

4. **Symbiont context** - Understand why features matter:
   ```
   .claude/skills/claude-code-tracker/context.md
   ```

---

## Step 2: Synthesize Knowledge

After reading, mentally organize:

- **What changed** in this version (features, fixes, improvements)
- **Tier classification** (🚀 Major | ✨ Notable | 🔧 Minor | 🐛 Patch)
- **Symbiont relevance** (🚀 Critical | ✨ High | 🔧 Medium | Skip)
- **Key Symbiont impacts** (which specialists/primitives affected)
- **Action items** (things to test or implement)

---

## Step 3: Ready for Dialogue

Acknowledge you've loaded the context and invite questions. Example:

> Loaded v$ARGUMENTS context. This was a [tier] release with [relevance] Symbiont relevance.
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
- **Identify gaps** - If we don't have info, suggest running `/research-release $ARGUMENTS`

Common questions to be ready for:
- "How does [feature] work?"
- "How would I use this in Symbiont?"
- "What's the practical benefit?"
- "Should I update my workflow for this?"
- "What should I test first?"
