---
argument-hint: "<topic>"
description: Deep research on Claude Code features and best practices
---

# Claude Research Command

Comprehensive research on Claude Code features: web search, documentation analysis, usage patterns, best practices.

## Usage

```bash
/claude-research "[feature or topic]"
```

## Process

1. **Web search**: Official docs + community resources
2. **Analyze**: Anthropic docs, blog posts, changelogs, examples
3. **Identify**: Usage patterns, best practices, integrations
4. **Contextualize**: Apply to Agent Hub use cases
5. **Generate**: Structured markdown report in `~/agents/sys-admin/data/claude_updates/research/`

## Output

```
🔬 Deep Research: [Topic]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Official Documentation ({N} sources)
✓ {urls}

💬 Community Resources ({N} sources)
✓ {GitHub/forums/blogs/videos/SO}

🔍 Key Findings

Core Concept:
{2-3 sentence explanation}

Best Practices:
• {practices}

Agent Hub Integration:
• {how this applies}

Common Pitfalls:
⚠️  {what to avoid}

Migration Path:
{if applicable}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Report Saved: {path}

Next steps:
1. Review key insights
2. Update docs if needed
3. Add to primitive registry
```

## Use Cases

**Understand new features**: `/claude-updates` finds unfamiliar feature → `/claude-research "Feature Name"`
**Solve problems**: Setting up system integration → `/claude-research "MCP authentication patterns"`
**Evaluate tools**: Before installing package → `/claude-research "Linear MCP capabilities"`
**Stay current**: Monthly learning → `/claude-research "Claude Code MCP ecosystem 2025"`

## Research Scope

**Quick (default)**: 5-10 sources, 10-15 min, high-level overview
**Deep (`--deep`)**: 20+ sources, 30+ min, comprehensive analysis

## Source Types

**Official**: Anthropic docs, blog posts, changelogs, API refs
**Community**: GitHub, forums, tutorials, videos, Stack Overflow
**Local**: Existing sys-admin docs, configuration guides

## Report Structure

```markdown
# [Feature] Research Report

**Date**: YYYY-MM-DD
**Scope**: Quick|Deep

## Executive Summary
## Key Findings
## Usage Patterns
## Best Practices
## System Integration
## Common Pitfalls
## Code Examples
## Sources
## Recommendations
```

## Quality Filters

**Recency**: Prefer last 6 months
**Authority**: Official docs > community
**Relevance**: Filter tangential content
**Completeness**: Include code examples

## Related Commands

- `/claude-updates` - Discover new Claude Code features (triggers research)
- `/pacman` - System package management

---

**Owner**: sys-admin agent
**Implementation**: LLM-orchestrated (no external scripts)
