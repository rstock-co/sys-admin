# Claude Code Tracking Resources

Gold-standard compilation of authoritative sources for tracking Claude Code developments.

**Purpose**: External sources to monitor Claude Code changes beyond training data cutoff.

**Used by**: `/claude-updates` and `/claude-research` commands.

---

## Tier 1: Official Sources

Primary authoritative sources from Anthropic.

| Resource | URL | Update Frequency |
|----------|-----|------------------|
| GitHub CHANGELOG.md | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | Every release |
| GitHub Releases | https://github.com/anthropics/claude-code/releases | Every release |
| npm Package Versions | https://www.npmjs.com/package/@anthropic-ai/claude-code | Every release |
| Claude Docs Release Notes | https://docs.claude.com/en/release-notes/overview | Major releases |
| Claude Help Center | https://support.claude.com/en/articles/12138966-release-notes | Major releases |
| Claude Status | https://status.claude.com | Real-time |

---

## Tier 2: Community Changelog Aggregators

Curated changelogs with better formatting and context.

| Resource | URL | Notes |
|----------|-----|-------|
| ClaudeLog | https://claudelog.com/claude-code-changelog/ | Best formatted changelog, version history, revert guides |
| Releasebot | https://releasebot.io/updates/anthropic/claude-code | Automated release tracking |
| Developer Toolkit | https://developertoolkit.ai/en/claude-code/version-management/changelog/ | Community-maintained |

---

## Tier 3: System Prompt & Tool Tracking

Deep technical analysis of internal changes.

| Resource | URL | Notes |
|----------|-----|-------|
| cchistory (Mario Zechner) | https://cchistory.mariozechner.at/ | System prompt diffs between versions, updates every 30 min |
| cchistory GitHub | https://github.com/badlogic/cchistory | Extract and compare prompts/tools |
| System Prompts Archive | https://github.com/Piebald-AI/claude-code-system-prompts | All system prompts, tool descriptions, sub-agent prompts |

---

## Tier 4: Social Media & Real-Time Updates

Breaking news and community discussion.

| Resource | URL | Notes |
|----------|-----|-------|
| @ClaudeCodeLog (X/Twitter) | https://x.com/ClaudeCodeLog | Unofficial bot, ~10K followers, posts prompt/CLI changes |
| @claudeai (X/Twitter) | https://x.com/claudeai | Official Anthropic account |
| r/ClaudeAI (Reddit) | https://reddit.com/r/ClaudeAI | 386K members, high activity |
| r/ClaudeCode (Reddit) | https://reddit.com/r/ClaudeCode | Dedicated Claude Code subreddit |
| Claude Developers Discord | https://discord.com/invite/6PPFFzqPDZ | Official, ~50K members |

---

## Tier 5: Content Creators & Educators

In-depth tutorials and feature breakdowns.

| Creator | Platform | Focus |
|---------|----------|-------|
| IndyDevDan | [YouTube](https://youtube.com/@indydevdan) / [Blog](https://indydevdan.com/) | Agentic coding, parallelization, hooks, SDK |
| WorldofAI | YouTube | Feature update breakdowns |
| Geeky Gadgets | https://www.geeky-gadgets.com/?s=claude+code | Detailed feature coverage |
| Sankalp (bearblog) | https://sankalp.bearblog.dev/ | Practical usage guides |

---

## Tier 6: Curated Lists & Aggregators

Meta-resources collecting Claude ecosystem tools.

| Resource | URL | Notes |
|----------|-----|-------|
| awesome-claude | https://github.com/alvinunreal/awesome-claude | Comprehensive Claude ecosystem list |
| ClaudeLog News | https://claudelog.com/claude-news/ | Aggregated Claude news |
| SwipeInsight Claude Topics | https://web.swipeinsight.app/topics/claude | Monthly update aggregation |

---

## Recommended Monitoring Strategy

### Daily
- Check `@ClaudeCodeLog` on X for prompt/CLI changes

### Weekly
- Run `/claude-updates` to scan ClaudeLog changelog
- Browse r/ClaudeAI for community discoveries

### Per Release
- Read GitHub CHANGELOG.md for official notes
- Check cchistory for system prompt diffs
- Watch IndyDevDan if major feature

### Monthly
- Deep dive with `/claude-research` on new primitives
- Update `claude_code_changelog.md` with plain-language summaries

---

## How to Use These Resources

The `/claude-updates` command should:
1. Fetch from ClaudeLog (Tier 2) for formatted changelog
2. Cross-reference with GitHub CHANGELOG (Tier 1) for accuracy
3. Check cchistory (Tier 3) for prompt/tool changes
4. Search X/Reddit (Tier 4) for community context

The `/claude-research` command should:
1. Start with official docs (Tier 1)
2. Search creator content (Tier 5) for tutorials
3. Check awesome-claude (Tier 6) for related tools
4. Browse community discussions (Tier 4) for gotchas

---

**Last Updated**: 2025-12-29
