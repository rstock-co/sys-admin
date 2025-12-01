---
argument-hint: [since-date]
description: Scan Claude Code changelog and identify documentation updates needed
---

# Claude Updates Command

Monitors Claude Code changelog and maps updates to affected documentation files.

## Usage

```bash
/claude-updates [since-date]
```

**First run**: Scans last 30 days
**Subsequent runs**: Shows new + pending items, resume where you left off

## Workflow

1. **Load last scan**: Read `~/agents/sys-admin/data/claude_updates/last_scan.json` for pending actions
2. **Fetch changelog**: Use WebFetch on https://claudelog.com/claude-code-changelog/
3. **Filter relevance**: Keywords (Claude Code, MCP, Task, agent, skill, subagent, hook, primitive, SDK)
4. **Map affected files**: Identify which docs need updates (BREAKING/GUIDANCE/INFORMATIONAL)
5. **Present results**: Show formatted report with file paths and reasons
6. **Interactive implementation**: Q&A-driven updates with progress tracking
7. **Save state**: Update last_scan.json (resumable)

### Two-Stage Filtering

**Stage 1 - Keywords**: Quick scan for relevant terms
**Stage 2 - LLM Assessment**: Impact level (HIGH/MEDIUM/LOW), beta status, relevance to Agent Hub

### File Discovery

Use Glob to find Claude Code documentation files:
- `data/claude-code/usage/**/*.md` - How to USE Claude Code docs
- `data/claude-code/primitives/**/*.md` - How to BUILD Claude Code docs
- `.claude/skills/**/*.md` - Skill definitions
- `.claude/commands/**/*.md` - Command definitions

### Output Format

```
🔍 Scanning Claude Code Changelog...

Last scan: {days_ago} days ago
Scanning: {since_date} to {today}

📢 Found {total} Features ({relevant} relevant, {irrelevant} filtered)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 RELEVANT UPDATES

1. {title} {[BETA]}
   Released: {date}
   Impact: {HIGH|MEDIUM|LOW}

   Changes:
   • {bullet points}

   📄 Files Affected:

   🔴 BREAKING:
   ✏️  {file_path}
       Reason: {specific section/requirement}

   📝 GUIDANCE:
   ✏️  {file_path}
       Reason: {what to document}

   📚 Anthropic Docs:
   • {url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
✅ {total} scanned
📝 {relevant} relevant ({high_impact} HIGH)
✏️  {affected_files} files need updates
{🔴 Breaking changes}{⚠️  BETA features}

Next Steps:
1. Visit https://docs.claude.ai/claude-code/[page]
2. Click "Copy to markdown" button
3. Update affected files in ~/agents/sys-admin/data/claude-code/
4. Commit changes to sys-admin repo
5. Use /claude-research for complex features

✓ Last scan updated

Would you like to implement these now? [Y/n/Later]
```

### Interactive Implementation

If user selects **Y**:

**Priority order**: Breaking → High → Medium → Low → Beta

**For each item**:
1. Explain context
2. Read affected files
3. Ask approach (review/update/skip)
4. Show proposed changes
5. Apply after approval
6. Mark complete in last_scan.json

**Progress tracking**: Save after each item, allow pause/resume

## Impact Levels

**HIGH**: SDK versions, Task tool changes, breaking MCP changes
**MEDIUM**: New MCP servers, primitives, performance improvements
**LOW**: Context window, UI/UX, unrelated bug fixes

## Beta Features

Flagged with ⚠️, clearly labeled in docs, tracked for stabilization.

## Data Persistence

**last_scan.json**:
```json
{
  "last_scan": "ISO timestamp",
  "scan_range": {"from": "date", "to": "date"},
  "summary": {"total": N, "relevant": M, "breaking": X, "beta": Y},
  "relevant_entries": [
    {
      "version": "v2.0.X",
      "title": "...",
      "impact_level": "HIGH",
      "affected_files": ["..."],
      "action_taken": false,
      "beta": false
    }
  ],
  "irrelevant_entries": [...],
  "pending_actions": {
    "breaking_changes": [...],
    "high_impact": [...]
  }
}
```

**Purpose**: Deduplication, action tracking, trend analysis, resumability

## When to Run

**Weekly check**: `/claude-updates` (recommended)
**Specific range**: `/claude-updates 2025-10-01`
**Monthly routine**: Part of sys-admin maintenance cycle

## Data Source

**ClaudeLog**: https://claudelog.com/claude-code-changelog/
- Third-party (Wilfred Kasekende, r/ClaudeAI moderator)
- Referenced in official docs
- Comprehensive version history

Features cross-referenced with official docs during file mapping.

## Related Commands

- `/claude-research "<feature>"` - Deep dive into specific Claude Code feature
- `/pacman` - Check system package updates (similar workflow)
- `/troubleshoot` - System troubleshooting

---

**Owner**: sys-admin agent
**Implementation**: LLM-orchestrated (no external scripts)
