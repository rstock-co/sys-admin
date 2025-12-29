---
description: Deep research a specific Claude Code release version
argument-hint: [version] [optional: focus area or question]
---

# Deep Research: Claude Code v$ARGUMENTS

Execute this workflow step-by-step to research and document Claude Code version **$ARGUMENTS**.

**User Focus:** If a focus area or question was provided after the version number, prioritize researching that aspect in depth. Tailor the deep dive sections and Symbiont analysis to address the user's specific interest.

---

## Step 1: Load Context

Read these files to understand Symbiont dependencies and what we already know:

1. **Read context.md** - Symbiont architecture, feature dependencies, relevance scoring criteria
   ```
   .claude/skills/claude-code-tracker/context.md
   ```

2. **Read changelog.md** - Check if we have an existing entry for this version
   ```
   .claude/skills/claude-code-tracker/changelog.md
   ```

3. **Read relevance.md** - Check if we have personalized notes for this version
   ```
   .claude/skills/claude-code-tracker/relevance.md
   ```

4. **Check for existing research** - See if we've already researched this version
   ```
   ~/agents/sys-admin/data/claude-code/research/
   ```

---

## Step 2: Research External Sources

Fetch information from official and community sources:

1. **GitHub CHANGELOG** - Get the official release notes
   ```
   WebFetch("https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
            "Find version $ARGUMENTS entry with full details")
   ```

2. **ClaudeLog** - Get formatted changelog entry
   ```
   WebFetch("https://claudelog.com/claude-code-changelog/",
            "Find version $ARGUMENTS details")
   ```

3. **Search for tutorials/guides** on the key features in this release
   ```
   WebSearch("Claude Code $ARGUMENTS [key feature] tutorial guide 2025")
   WebSearch("Claude Code [key feature] site:docs.anthropic.com")
   ```

4. **Search for announcements**
   ```
   WebSearch("Claude Code $ARGUMENTS announcement blog")
   ```

5. **Search community discussions**
   ```
   WebSearch("Claude Code [feature] reddit OR hackernews 2025")
   ```

6. **If user provided a focus area**, do targeted research:
   - Search for that specific topic in official docs
   - Find tutorials/guides specific to that feature
   - Look for edge cases, limitations, and best practices
   - Search for how it interacts with other features

---

## Step 3: Analyze Symbiont Relevance

Using context.md criteria, evaluate this release:

1. Does it touch **output styles**? → Affects specialist voices
2. Does it touch **CLAUDE.md loading**? → Affects specialist personas
3. Does it touch **MCP**? → Affects symbiont-db
4. Does it touch **hooks**? → Affects pulse system
5. Does it touch **background execution**? → Affects overnight daemon
6. Does it touch **sessions**? → Affects specialist persistence
7. Does it touch **subagents**? → Affects Dual Sovereignty
8. Is it **Linux/Wayland/Alacritty** specific? → Direct environment impact

Assign relevance: 🚀 Critical | ✨ High | 🔧 Medium

---

## Step 4: Create Research File

Write a comprehensive research file to:
```
~/agents/sys-admin/data/claude-code/research/$ARGUMENTS/index.md
```

If the user provided a focus area, create an additional deep-dive file:
```
~/agents/sys-admin/data/claude-code/research/$ARGUMENTS/[focus-topic].md
```

Use this structure for index.md:

```markdown
# Claude Code v$ARGUMENTS - Deep Research

**Release Date:** {date from changelog}
**Tier:** {🚀|✨|🔧|🐛} {Major|Notable|Minor|Patch}
**Symbiont Relevance:** {🚀|✨|🔧} {Critical|High|Medium}
**Researched:** {today's date}

## Summary

{2-3 sentence overview of what this release contains}

## What Changed

{Bullet list of all changes from official changelog}

## Deep Dive: {Main Feature}

{3-5 paragraphs explaining the main feature in depth}

### How It Works

{Technical explanation of the feature}

### How to Use It

{Practical examples, commands, configuration snippets}

## Symbiont Impact

{Based on context.md - explain specifically how this affects:}
- Which specialists are affected?
- Which primitives (hooks, MCP, skills) are affected?
- What architectural changes might this enable?
- Any action items or potential migrations?

## Sources

- [Official Changelog](url)
- [Blog Post](url) - if found
- [Documentation](url) - if found
- [Community Discussion](url) - if found
```

---

## Step 5: Update Tracking Files

1. **Update changelog.md** if the entry is missing or incomplete:
   - Add row to Quick Reference table (newest first)
   - Add detailed entry with appropriate tier emoji

2. **Update relevance.md** if this release is relevant to Symbiont:
   - Add row to Quick Reference table with relevance icon
   - Add detailed entry explaining Symbiont impact

---

## Step 6: Report Findings

Summarize for the user:
- What tier is this release? (Major/Notable/Minor/Patch)
- How relevant is it to Symbiont? (Critical/High/Medium/Skip)
- What are the key takeaways?
- Any action items or things to test?
