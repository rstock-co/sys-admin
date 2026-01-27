---
name: claude-code-tracker
description: |
  Track Claude Code releases, analyze changelogs, and maintain internal documentation. Use when checking for Claude Code updates, researching new features, understanding recent changes, or when user mentions "claude updates", "what's new in claude code", or asks about Claude Code features/changes.
---

# Claude Code Tracker

**Monitor, analyze, and document Claude Code releases with comprehensive plain-language explanations.**

## When to Use This Skill

Use when:
- User asks about Claude Code updates or changes
- User wants to know "what's new" in Claude Code
- User asks about a specific Claude Code feature
- User mentions checking for updates
- Researching Claude Code capabilities
- Documenting new features for internal reference

**Trigger keywords**: claude updates, claude code changelog, what's new, new features, claude code version, release notes, claude research

## Core Resources

### Primary Data Files

| File | Purpose |
|------|---------|
| [context.md](context.md) | **READ FIRST** - Symbiont context, feature dependencies, relevance scoring |
| [tracking-resources.md](tracking-resources.md) | Gold-standard list of authoritative sources |
| [changelog.md](changelog.md) | Internal changelog with plain-language explanations |
| [relevance.md](relevance.md) | Personalized changelog filtered by context.md |
| [data/last_scan.json](data/last_scan.json) | Scan state and pending actions |

### Research Output

| Location | Purpose |
|----------|---------|
| `data/claude-code/research/` | Deep-dive research on specific releases |

### External Sources (Tier 1 - Official)

| Source | URL | Use For |
|--------|-----|---------|
| GitHub CHANGELOG | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | Official release notes |
| GitHub Releases | https://github.com/anthropics/claude-code/releases | Version tags |
| npm Versions | https://www.npmjs.com/package/@anthropic-ai/claude-code | Package versions |

### External Sources (Tier 2 - Community)

| Source | URL | Use For |
|--------|-----|---------|
| ClaudeLog | https://claudelog.com/claude-code-changelog/ | Formatted changelog |
| cchistory | https://cchistory.mariozechner.at/ | System prompt diffs |
| @ClaudeCodeLog | https://x.com/ClaudeCodeLog | Real-time updates |

## Workflows

### 1. Check for Updates

**When user asks**: "Check for Claude Code updates" / "What's new?"

1. **Read user context FIRST**:
   ```
   Read context.md
   ```
   Understand Symbiont dependencies and relevance scoring before scanning.

2. **Read last scan state**:
   ```
   Read data/last_scan.json
   ```

3. **Fetch ClaudeLog changelog**:
   ```
   WebFetch(
     url: "https://claudelog.com/claude-code-changelog/",
     prompt: "Extract all releases since {last_scan_date}. Return version, date, and changes for each."
   )
   ```

3. **Cross-reference with GitHub** (for accuracy):
   ```
   WebFetch(
     url: "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
     prompt: "Extract recent releases. Return version, date, and bullet points."
   )
   ```

4. **Classify each release** into importance tiers:
   - 🚀 Major: New models, new tools, breaking changes, new primitives
   - ✨ Notable: Workflow improvements, new options, performance gains
   - 🔧 Minor: UI polish, small fixes, keyboard shortcuts
   - 🐛 Patch: Bug fixes only, reverts, hotfixes

5. **For 🚀 Major releases - DO EXTRA RESEARCH:**
   ```
   WebSearch("Claude Code {feature} tutorial guide 2025")
   WebSearch("Claude Code {feature} site:docs.anthropic.com")
   ```
   Find blog posts, official docs, community guides. Write 3-5 paragraph entries with "How to Use It" and "Learn More" sections.

6. **For ✨ Notable releases:**
   Check official changelog for full context. Write 1-2 paragraph entries explaining workflow impact.

8. **Present findings** with impact assessment - highlight Symbiont impact based on context.md

9. **Update changelog.md:**
   - Add row to Quick Reference table (TOP of table, newest first)
   - Add detailed entry (format based on tier - see Tiered Detail Requirements)

10. **Update relevance.md:**
    - Filter releases through context.md criteria (Symbiont impact)
    - Only include RELEVANT and PARTIALLY RELEVANT releases
    - Annotate WHY each release matters to user's specific setup
    - Format: version, date, relevance level, personalized explanation

11. **Save scan state** to data/last_scan.json

### 2. Research Specific Feature

**When user asks**: "How does X work?" / "Tell me about feature Y"

1. **Check internal docs first**:
   - Read `data/claude-code/` for existing documentation
   - Check changelog.md for recent context

2. **Search official sources**:
   ```
   WebSearch("Claude Code {feature} site:docs.anthropic.com OR site:github.com/anthropics")
   ```

3. **Check community resources**:
   ```
   WebSearch("Claude Code {feature} tutorial guide 2025")
   ```

4. **Synthesize findings** into actionable guidance

5. **Update changelog.md** if this reveals new understanding

### 3. Analyze System Prompt Changes

**When user asks**: "What changed in the system prompt?" / "Why is Claude behaving differently?"

1. **Fetch cchistory diff**:
   ```
   WebFetch(
     url: "https://cchistory.mariozechner.at/",
     prompt: "Extract the diff between the two most recent Claude Code versions"
   )
   ```

2. **Explain changes** in plain language

3. **Document implications** for our workflows

### 4. Deep Research a Specific Release

**When user asks**: "Research 2.0.54 in depth" / "Tell me more about version X" / "Deep dive on release Y"

**CRITICAL: Always read existing documentation first, then research externally.**

1. **Read context.md** to understand Symbiont dependencies

2. **Read changelog.md entry** for the specified version
   - This is your baseline - understand what we already know
   - Note any gaps or questions

3. **Read existing research** if it exists:
   ```
   Read data/claude-code/research/{version}.md
   ```
   If file exists, you may be updating it. If not, you're creating it.

4. **Research external sources** using tracking-resources.md:
   ```
   WebFetch("https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
            "Find version {X} entry with full details")

   WebSearch("Claude Code {version} {key feature} tutorial guide 2025")
   WebSearch("Claude Code {key feature} site:docs.anthropic.com")
   WebSearch("Claude Code {version} announcement blog")
   ```

5. **Search for community content**:
   ```
   WebSearch("Claude Code {feature} reddit OR hackernews OR twitter 2025")
   WebFetch("https://claudelog.com/claude-code-changelog/", "Find {version} details")
   ```

6. **Write research file** to `data/claude-code/research/`

   **Filename format**: `{version}.md` (e.g., `2-0-54.md`)

   **File structure**:
   ```markdown
   # Claude Code v{version} - Deep Research

   **Release Date:** {date}
   **Tier:** {emoji} {tier}
   **Researched:** {today's date}

   ## Summary
   {2-3 sentence overview}

   ## What Changed
   {Bullet list of all changes from official changelog}

   ## Deep Dive: {Main Feature}
   {3-5 paragraphs explaining the main feature in depth}

   ### How It Works
   {Technical explanation}

   ### How to Use It
   {Practical examples, commands, config snippets}

   ## Relevance to My Setup
   {Based on context.md - Symbiont impact and why this matters}

   ## Sources
   - [Official Changelog](url)
   - [Blog Post](url) (if found)
   - [Documentation](url) (if found)
   - [Community Discussion](url) (if found)
   ```

7. **Update last_scan.json** to note research was completed for this version

### 5. Answer Questions About a Version

**When user asks**: "What's in 2.0.54?" / "Does version X have feature Y?"

**CRITICAL: Check local docs before answering.**

1. **Read changelog.md** - check if we have an entry
2. **Read research file** if it exists: `data/claude-code/research/{version}.md`
3. **Read relevance.md** - check personalized notes
4. **Only then** answer the question, citing what we know
5. **If insufficient info**, offer to do deep research

## CRITICAL: Complete Coverage Rule

**Every single release MUST be documented in changelog.md.** No exceptions.

- If a version exists, it gets an entry
- If sources don't have notes for a version, mark it as `🐛 Patch` with note: "No release notes available - likely hotfix"
- Never skip versions, even if they seem minor
- Maintain chronological order (newest first)

## CRITICAL: Quick Reference Table Maintenance

The changelog.md has a **Quick Reference** table at the top. This MUST be updated for every new release.

**When adding a new release:**
1. Add a row to the Quick Reference table (at the TOP, newest first)
2. Add the detailed entry below the table

**Table format:**
```markdown
| Version | Date | Tier | Summary |
|---------|------|------|---------|
| 2.0.XX | Mon DD | 🚀 | Brief one-line summary of key change |
```

**Keep summaries short** - max ~60 characters. The detailed entry has the full explanation.

## Importance Tiers (Emoji System)

Use these emoji prefixes in changelog headers to indicate importance at a glance:

| Emoji | Level | Criteria | Examples |
|-------|-------|----------|----------|
| 🚀 | **Major** | Game-changing features, new capabilities, breaking changes | New model (Opus 4.5), LSP tool, browser control, new primitives |
| ✨ | **Notable** | Significant improvements, new options, workflow enhancements | Background agents, `.claude/rules/`, prompt suggestions, MCP wildcards |
| 🔧 | **Minor** | Small enhancements, QoL improvements, non-critical fixes | UI tweaks, keyboard shortcuts, display improvements |
| 🐛 | **Patch** | Bug fixes only, reverts, hotfixes, no new features | "Minor bugfixes", stability fixes, reverts |

### Classification Guidelines

**🚀 Major** - Ask: "Does this fundamentally change what Claude Code can do?"
- New tools or primitives
- New model availability
- Breaking changes requiring user action
- Major new integrations (browser, desktop app)

**✨ Notable** - Ask: "Does this meaningfully improve daily workflows?"
- New configuration options
- Performance improvements users will notice
- New keyboard shortcuts or commands
- Enhanced existing features

**🔧 Minor** - Ask: "Is this nice-to-have but not essential?"
- Visual/UI improvements
- Platform-specific fixes
- Small convenience features
- Documentation in the app

**🐛 Patch** - Ask: "Is this purely fixing something broken?"
- Bug fixes with no new features
- Reverts of previous changes
- Hotfixes
- Stability improvements

## Tiered Detail Requirements

**The amount of research and detail scales with importance tier.**

### 🚀 Major Releases - DEEP RESEARCH REQUIRED

For major releases, you MUST:
1. **Research extensively** - Use WebSearch to find blog posts, announcements, tutorials
2. **Check official docs** - Look for new documentation pages on docs.anthropic.com
3. **Find practical examples** - How are people using this feature?
4. **Document thoroughly** - 3-5 paragraphs minimum

**Major release format:**
```markdown
## 🚀 v{version} - {date}

### What Changed
{2-3 sentences: Technical summary with specifics}

### What It Means
{2-3 paragraphs: Deep explanation of the feature, why it matters, how it works}

### How to Use It
{Practical examples, commands, configuration snippets}

### Learn More
- [Link to docs or blog post]
- [Link to tutorial or guide]

---
```

### ✨ Notable Releases - MODERATE RESEARCH

For notable releases:
1. **Check official changelog** for full context
2. **Understand the workflow impact**
3. **Provide 1-2 paragraphs** of explanation

**Notable release format:**
```markdown
## ✨ v{version} - {date}

### What Changed
{1-2 sentences: Technical summary}

### What It Means
{1-2 paragraphs: Explanation of practical impact and how to use it}

---
```

### 🔧 Minor Releases - BASIC DOCUMENTATION

For minor releases:
1. **Document what changed**
2. **Brief explanation** of impact
3. **2-4 sentences total**

**Minor release format:**
```markdown
## 🔧 v{version} - {date}

### What Changed
{1 sentence: What changed}

### What It Means
{1-2 sentences: Brief impact}

---
```

### 🐛 Patch Releases - MINIMAL

**Patch format:**
```markdown
## 🐛 v{version} - {date}

{One line: "Minor bugfixes" or "Hotfix" or brief description}

---
```

## Impact Assessment Criteria (Detailed)

### 🚀 Major Impact
- New models (Opus, Sonnet versions)
- SDK breaking changes
- New tools (LSP, browser control)
- New primitives (skills, hooks, plugins system)
- Desktop/mobile app launches
- Breaking MCP changes

### ✨ Notable Impact
- Background/async execution
- New configuration directories (`.claude/rules/`)
- MCP improvements (wildcards, toggles)
- New slash commands
- Performance improvements (3x faster, etc.)
- New keyboard shortcuts for core features

### 🔧 Minor Impact
- UI/UX polish
- Theme changes
- Platform-specific improvements
- Display tweaks
- Non-essential keyboard shortcuts

### 🐛 Patch Impact
- "Minor bugfixes"
- Reverts
- Hotfixes
- No release notes available

## Data Persistence

### last_scan.json Structure

```json
{
  "last_scan": "2025-12-29T10:00:00Z",
  "last_version": "2.0.76",
  "scan_range": {"from": "2025-12-01", "to": "2025-12-29"},
  "pending_actions": [
    {
      "version": "2.0.75",
      "title": "Plugin system released",
      "impact": "HIGH",
      "documented": false
    }
  ]
}
```

## Local Documentation Map

Your Claude Code docs live in `data/claude-code/`. When a release mentions certain topics, these are the files that need updating:

### Keyword → File Mapping

| If release mentions... | Update this file |
|------------------------|------------------|
| CLI, flags, commands | `usage/usage/cli-reference.md` |
| settings, config | `usage/configuration/settings.md` |
| model, opus, sonnet, haiku | `usage/configuration/model.md` |
| terminal, shell | `usage/configuration/terminal.md` |
| memory, CLAUDE.md | `usage/configuration/memory.md` |
| thinking, extended thinking | `usage/usage/[USER]-thinking-modes.md` |
| headless, automation, SDK | `usage/usage/headless-mode.md` |
| checkpoints, restore | `usage/usage/checkpointing.md` |
| GitHub Actions, CI/CD | `usage/github/actions.md` |
| costs, pricing, tokens | `usage/usage/costs.md` |
| hooks | `primitives/hooks-guide.md`, `primitives/hooks-reference.md` |
| skills | `primitives/skills.md` |
| plugins | `primitives/plugins-guide.md`, `primitives/plugins-reference.md` |
| MCP, servers | `primitives/mcp.md` |
| sub-agents, Task tool | `primitives/sub-agents.md` |
| tools, Read, Write, Bash | `primitives/tools-reference.md` |
| slash commands | `primitives/slash-commands.md` |

### Workflow Step: Identify Affected Docs

After fetching updates, for EACH change:

1. **Scan the release notes** for keywords from the table above
2. **List affected files** with the specific reason
3. **Present to user**:
   ```
   📄 Files needing updates:

   primitives/hooks-reference.md
     → Release added new hook event type "onSessionEnd"

   usage/configuration/settings.md
     → New config option "autoBackground" for long commands
   ```
4. **Ask**: "Want me to update these now, or just note them for later?"

### Changelog Entry Format (with Docs)

For releases that affect local documentation:

```markdown
## 🚀 v{version} - {date}

### What Changed
{Technical summary}

### What It Means
{Plain-language explanation}

### Docs to Update
- `primitives/tools-reference.md` - Add LSP tool documentation
- `usage/configuration/settings.md` - Document new autoBackground option

---
```

## Monitoring Schedule

| Frequency | Action |
|-----------|--------|
| Daily | Check @ClaudeCodeLog on X for prompt changes |
| Weekly | Full changelog scan via this skill |
| Per-release | Update changelog.md with plain-language summary |
| Monthly | Deep research on new primitives |

---

**Remember**: My training data has a cutoff. ALWAYS fetch external sources for current Claude Code information. Never rely on memory for recent features.
