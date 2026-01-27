# Autonomous Claude Code: Complete Implementation Guide

**Comprehensive guide to autonomous Claude Code operation, covering all features from v2.0.42 through v2.1.20.**

*Last Updated: 2026-01-27*

---

## How to Use This Guide

This guide provides **overview-level information** with links to detailed research for each feature.

**Structure:**
- Each section covers a capability with practical examples
- Version numbers indicate when features were introduced
- **→ [Deep dive](research/X-X-X.md)** links lead to detailed research files with:
  - Full technical details
  - Input/output schemas
  - Known limitations
  - Symbiont-specific use cases
  - Original sources

**For LLM readers:** When you encounter a feature that's relevant to your task, follow the deep dive link for complete implementation details.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Authentication](#authentication-max-subscription-vs-api)
4. [Known Issues](#known-issues)
5. [CLI Flags Reference](#cli-flags-reference)
6. [Instruction Loading](#instruction-loading-patterns)
7. [Hook System](#hook-system)
8. [Permission Configuration](#permission-configuration)
9. [Session Management](#session-management)
10. [Task System](#task-system)
11. [Background Agents](#background-agents)
12. [Skills with context:fork](#skills-with-contextfork)
13. [Dynamic Context Injection](#dynamic-context-injection)
14. [Complete Spawning Patterns](#complete-spawning-patterns)
15. [Cost Control](#cost-control)
16. [Feature Matrix by Version](#feature-matrix-by-version)
17. [Implementation Examples](#implementation-examples)
18. [Sources](#sources)

---

## Overview

This guide covers **autonomous Claude Code operation** - running Claude Code without human interaction for:

- Orchestrator agents spawning specialist agents
- Overnight daemon processing
- Parallel execution across multiple terminals
- CI/CD pipeline integration
- Agent-to-agent delegation with database-backed instruction handoff

**Key constraint:** Use Max subscription billing, not API billing for most use cases.

---

## Quick Start

Minimal autonomous agent spawn:

```bash
#!/bin/bash
# spawn-autonomous.sh

# 1. Force Max subscription
unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION="true"

# 2. Enable instruction loading from additional directories
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1

# 3. Launch with all necessary flags
claude \
  --add-dir ~/shared/core-instructions/ \
  --disable-slash-commands \
  --allowedTools "Read,Write,Edit,Bash,Grep,Glob" \
  --working-directory "$1" \
  -p "$2"
```

---

## Authentication: Max Subscription vs API

### The Problem

When `ANTHROPIC_API_KEY` is set, Claude Code **bypasses your subscription** and uses API billing.

### The Solution

```bash
# In every spawn script:
unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION="true"
```

### Wrapper Script (Recommended)

Create `~/.local/bin/claude_max`:

```bash
#!/bin/bash
unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION="true"
exec claude "$@"
```

**Source:** [How I Built claude_max](https://dsco2048.substack.com/p/how-i-built-claude_max-to-unlock)

---

## Known Issues

### CRITICAL: 60-Second Latency Bug (v2.1.19+)

**Status:** Open (as of 2026-01-27)

Every `claude --print` request takes 60-63 seconds on Max subscription.

**Tracking:** [#17330](https://github.com/anthropics/claude-code/issues/17330), [#18028](https://github.com/anthropics/claude-code/issues/18028), [#20527](https://github.com/anthropics/claude-code/issues/20527)

**Workarounds:**
1. Downgrade to v2.1.17 or earlier
2. Use interactive mode with SessionStart hook for instruction injection
3. Wait for fix (service-side regression)

**Recommendation:** Use **interactive mode** with hooks until fixed.

---

## CLI Flags Reference

### Essential Autonomous Flags

| Flag | Description | Since |
|------|-------------|-------|
| `-p`, `--print` | Non-interactive mode | - |
| `--allowedTools` | Auto-approve tools | - |
| `--dangerously-skip-permissions` | Skip ALL permission prompts | - |
| `--disable-slash-commands` | Prevent accidental command invocation ([deep dive](research/2-0-60.md)) | v2.0.60 |
| `--output-format` | `text`, `json`, `stream-json` | - |
| `--max-turns` | Limit agentic turns | - |

### Instruction Loading Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--add-dir` | Add directories (files + CLAUDE.md with env var) ([deep dive](research/2-1-20.md)) | v2.1.20 |
| `--system-prompt` | Replace entire system prompt | - |
| `--append-system-prompt` | Add to default prompt (keeps CLAUDE.md) | - |
| `--agent` | Use agent persona (ignores CLAUDE.md) ([deep dive](research/2-0-59.md)) | v2.0.59 |

### Session Management Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--continue`, `-c` | Continue most recent conversation | - |
| `--resume`, `-r` | Resume by ID or name ([deep dive](research/2-0-64.md)) | v2.0.64 |
| `--session-id` | Use specific UUID | - |
| `--no-session-persistence` | Don't save to disk | - |

### Initialization Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--init` | Run Setup hooks, then interactive ([deep dive](research/2-1-10.md)) | v2.1.10 |
| `--init-only` | Run Setup hooks and exit | v2.1.10 |
| `--maintenance` | Run Setup hooks with maintenance trigger | v2.1.10 |

### Cost Control (SDK)

| Flag | Description | Since |
|------|-------------|-------|
| `--max-budget-usd` | Hard spending limit ([deep dive](research/2-0-42.md)) | v2.0.28 |

---

## Instruction Loading Patterns

### Pattern 1: Folder-Based CLAUDE.md (Recommended for SGTAs)

```
mycelium/health-coach/
├── CLAUDE.md              # Persona
├── output-style.md        # Voice
├── .claude/
│   └── rules/             # Modular rules
│       ├── health-data.md # paths: **/*.health.json
│       └── core/ → symlink
```

```bash
claude --working-directory ~/symbiont/mycelium/health-coach
```

**Pros:** Modular, maintainable, supports .claude/rules/
**Cons:** Requires symlinks for shared code

### Pattern 2: --add-dir Instruction Layering (v2.1.20+)

→ [Deep dive: --add-dir CLAUDE.md loading](research/2-1-20.md)

**Requires environment variable:**
```bash
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```

```bash
claude \
  --add-dir ~/symbiont/core/ \
  --working-directory ~/symbiont/mycelium/health-coach
```

**Pros:** No symlinks, explicit layering, composable
**Cons:** Requires env var, undocumented feature

### Pattern 3: --agent Flag (v2.0.59+)

→ [Deep dive: --agent flag (ignores CLAUDE.md)](research/2-0-59.md)

```bash
claude --agent code-reviewer
```

**CRITICAL:** `--agent` IGNORES CLAUDE.md. Not suitable for SGTA architecture.

**Use for:** Tool-restricted helpers, quick focused personas, read-only reviewers

### Pattern 4: .claude/rules/ Directory (v2.0.64+)

→ [Deep dive: Async agents, named sessions, .claude/rules/](research/2-0-64.md)

```
.claude/rules/
├── code-style.md           # Always loads
├── api-patterns.md         # paths: src/api/**/*.ts
└── security.md             # paths: src/auth/**, src/payments/**
```

Path-targeted rules with YAML frontmatter:
```yaml
---
paths: src/api/**/*.ts
---
# API Development Rules
```

### Comparison

| Pattern | CLAUDE.md | .claude/rules/ | Tool Restrictions | Modularity |
|---------|-----------|----------------|-------------------|------------|
| Folder-based | Yes | Yes | No | High |
| --add-dir | Yes | Yes | No | High |
| --agent | **No** | **No** | Yes | Low |
| --append-system-prompt | Yes | Yes | No | Medium |

---

## Hook System

Hooks are the foundation of autonomous operation. They fire at lifecycle points and can inject context, control permissions, and signal completion.

### Hook Events Overview

| Event | When | Key Capability |
|-------|------|----------------|
| **Setup** | `--init`/`--maintenance` | One-time initialization |
| **SessionStart** | Every session start | Context injection |
| **SessionEnd** | Session terminates | Completion signaling |
| **Stop** | Claude finishes responding | Continue/block work |
| **PreToolUse** | Before tool execution | Context injection, allow/deny |
| **PostToolUse** | After tool execution | Context injection |
| **PermissionRequest** | Permission dialog would show | Auto-approve/deny |
| **SubagentStart** | Subagent spawns | Logging, coordination |
| **SubagentStop** | Subagent completes | Lifecycle tracking |

### Hook Configuration

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "pattern",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Setup Hook (v2.1.10+)

→ [Deep dive: Setup hook](research/2-1-10.md)

Runs with `--init`, `--init-only`, or `--maintenance`. For one-time or periodic operations.

```json
{
  "hooks": {
    "Setup": [
      {
        "matcher": "init",
        "hooks": [{ "type": "command", "command": "./scripts/init.sh" }]
      },
      {
        "matcher": "maintenance",
        "hooks": [{ "type": "command", "command": "./scripts/maintenance.sh" }]
      }
    ]
  }
}
```

**Input includes:** `trigger` field ("init" or "maintenance")
**Special:** Access to `CLAUDE_ENV_FILE` for environment persistence

### SessionStart Hook

Runs every session. stdout is added to Claude's context.

```python
#!/usr/bin/env python3
# Inject instructions from database
import json, sys, psycopg2

input_data = json.load(sys.stdin)
cwd = input_data.get("cwd")
agent_name = cwd.split("/")[-1]

conn = psycopg2.connect("postgresql://...")
cur = conn.cursor()
cur.execute("SELECT instructions FROM tasks WHERE agent=%s AND status='pending'", (agent_name,))
row = cur.fetchone()

if row:
    print(f"## Your Task\n\n{row[0]}")  # stdout → Claude's context
```

**Matchers:** `startup`, `resume`, `clear`, `compact`

### SessionEnd Hook

Runs when session terminates. Signal completion to parent agent.

```python
#!/usr/bin/env python3
import json, sys
input_data = json.load(sys.stdin)
reason = input_data.get("reason")  # exit, clear, logout, prompt_input_exit, other

# Signal completion to database
# ...
```

### Stop Hook

Runs when Claude finishes responding. Can **block** to keep agent working.

```json
{
  "decision": "block",
  "reason": "Task not complete. Please continue with step 3."
}
```

### PreToolUse Hook (v2.1.9+: additionalContext)

→ [Deep dive: PreToolUse additionalContext](research/2-1-9.md)

Runs before tool execution. Can inject context, allow/deny, modify input.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "additionalContext": "Relevant context injected before tool runs",
    "updatedInput": { "command": "modified command" }
  }
}
```

**Key feature (v2.1.9):** `additionalContext` lets you inject database knowledge before Claude acts.

### PermissionRequest Hook (v2.0.45+)

→ [Deep dive: PermissionRequest hook](research/2-0-45.md)

Runs when permission dialog would appear. Auto-approve or deny.

**Auto-approve:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": { "behavior": "allow" }
  }
}
```

**Auto-deny:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": { "behavior": "deny", "message": "Blocked", "interrupt": true }
  }
}
```

### SubagentStart/SubagentStop Hooks (v2.0.43+)

→ [Deep dive: SubagentStart hook, permissionMode](research/2-0-43.md)

Track subagent lifecycle for logging and coordination.

**Input includes:** `agent_id`, `agent_type`
**SubagentStop also includes:** `agent_transcript_path`

```bash
#!/bin/bash
# Log specialist activation to Queen's Ledger
INPUT=$(cat)
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type')
AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id')
TIMESTAMP=$(date -Iseconds)

echo "{\"event\":\"specialist_activated\",\"type\":\"$AGENT_TYPE\",\"id\":\"$AGENT_ID\",\"ts\":\"$TIMESTAMP\"}" >> ~/ledger.jsonl
```

---

## Permission Configuration

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard prompts |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny prompts (allowed tools still work) |
| `bypassPermissions` | Skip ALL checks |
| `plan` | Read-only exploration |

### Static Permission Rules

```json
{
  "permissions": {
    "allow": [
      "Read", "Glob", "Grep",
      "Bash(git *)", "Bash(npm *)"
    ],
    "deny": [
      "Bash(rm -rf *)", "Bash(sudo *)"
    ]
  }
}
```

### PermissionRequest Hook for Dynamic Control

```javascript
#!/usr/bin/env node
// Auto-approve safe operations, prompt for risky ones

const SAFE = ['get', 'list', 'read', 'search', 'find'];
const DANGEROUS = ['delete', 'remove', 'drop', 'sudo'];

const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const toolName = input.tool_name;

if (DANGEROUS.some(p => toolName.includes(p))) {
  console.log(JSON.stringify({
    hookSpecificOutput: { hookEventName: "PermissionRequest",
      decision: { behavior: "deny", message: "Dangerous operation blocked" }
    }
  }));
} else if (SAFE.some(p => toolName.includes(p))) {
  console.log(JSON.stringify({
    hookSpecificOutput: { hookEventName: "PermissionRequest",
      decision: { behavior: "allow" }
    }
  }));
}
// Otherwise: prompt user (output nothing)
```

### Full Autonomous Configuration

```json
{
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
    "defaultMode": "acceptEdits"
  },
  "hooks": {
    "PermissionRequest": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PermissionRequest\",\"decision\":{\"behavior\":\"allow\"}}}'"
      }]
    }]
  }
}
```

---

## Session Management

### Named Sessions (v2.0.64+)

→ [Deep dive: Named sessions](research/2-0-64.md)

```bash
# Name a session
/rename health-coach-main

# Resume by name
claude --resume health-coach-main
```

### Session Persistence

Sessions stored in `~/.claude/sessions.db`. Named sessions survive restarts.

### The /resume Interface

| Shortcut | Action |
|----------|--------|
| `P` | Preview conversation |
| `R` | Rename session |
| `Enter` | Resume |

---

## Task System

### Task Tools (v2.1.16+)

→ [Deep dive: Native task system with dependencies](research/2-1-16.md)

| Tool | Purpose |
|------|---------|
| **TaskCreate** | Create task with subject, description, activeForm |
| **TaskList** | View all tasks |
| **TaskGet** | Get full task details |
| **TaskUpdate** | Update status, owner, dependencies |

### Task Lifecycle

```
pending → in_progress → completed
                     ↘ deleted (v2.1.20+)
```

### Dependency Tracking

```json
TaskCreate({ "subject": "Research" })       // #1
TaskCreate({ "subject": "Plan" })           // #2
TaskCreate({ "subject": "Implement" })      // #3

TaskUpdate({ "taskId": "2", "addBlockedBy": ["1"] })
TaskUpdate({ "taskId": "3", "addBlockedBy": ["2"] })
```

Task #2 auto-unblocks when #1 completes.

### Fan-Out / Fan-In Pattern

```
#1 Analyze auth    ─┐
#2 Analyze API     ─┼──▶ #4 Synthesize (blockedBy: 1,2,3)
#3 Analyze DB      ─┘
```

### Limitations

- **Session-scoped:** Tasks don't persist across sessions
- **No cross-session sharing:** Independent sessions can't see each other's tasks
- **Storage:** `~/.claude/tasks/{sessionId}/`

### Workaround: Task Hydration Pattern

Store task specs externally, recreate via SessionStart hook:

```yaml
# task-specs/morning-briefing.yaml
tasks:
  - id: pull-sleep
    subject: Pull Oura sleep data
  - id: analyze
    subject: Analyze patterns
    blockedBy: [pull-sleep]
```

---

## Background Agents

### Async Execution (v2.0.64+)

→ [Deep dive: Async agents, background execution](research/2-0-64.md)

1. Start agent task
2. Press `Ctrl+B` while running
3. Continue other work
4. Agent notifies on completion

**tmux users:** `Ctrl+B Ctrl+B` (double press)

### Commands

| Action | Method |
|--------|--------|
| Background running task | `Ctrl+B` |
| View background tasks | `/tasks` |
| Kill background process | Press `K` |
| Disable backgrounds | `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` |

### Limitations

- Inherit parent's permissions
- Auto-deny unknown permissions
- No MCP tools
- No clarifying questions

---

## Skills with context:fork

### The Problem

Skills run inline pollute context with internal reasoning.

### The Solution (v2.1.0+)

→ [Deep dive: context:fork, agent field, skill hooks](research/2-1-0.md)

```yaml
---
name: research-topic
description: Deep research without context pollution
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly. Return a concise summary.
```

**How it works:**
1. **Fork:** Copy current conversation context
2. **Execute:** Skill runs with full session awareness
3. **Return:** Brief completion message to main context
4. **Discard:** Forked context thrown away

### Agent Types

- `Explore` - Read-only tools, codebase exploration
- `Plan` - Planning and analysis
- `general-purpose` - Full tool access
- Custom agents from `.claude/agents/`

### Skill-Scoped Hooks

```yaml
---
name: safe-deploy
context: fork
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---
```

Hooks only fire during skill's lifecycle.

---

## Dynamic Context Injection

### PreToolUse additionalContext (v2.1.9+)

→ [Deep dive: PreToolUse additionalContext](research/2-1-9.md)

Inject context from database BEFORE tool executes:

```python
#!/usr/bin/env python3
import json, sys, psycopg2

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name")
tool_input = input_data.get("tool_input", {})

if tool_name == "Read" and "health" in tool_input.get("file_path", ""):
    conn = psycopg2.connect("postgresql://...")
    cur = conn.cursor()
    cur.execute("SELECT content FROM soul_data WHERE category='health'")
    row = cur.fetchone()

    if row:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": f"HEALTH CONTEXT:\n{row[0]}"
            }
        }))
```

### Use Cases

- **Soul-aware file access:** Inject relevant soul data based on what Claude reads
- **Relationship context:** Before reading communications, inject contact info
- **Cross-agent awareness:** Inject recent ledger entries before operations
- **Pattern detection:** Inject warnings when touching sensitive areas

---

## Complete Spawning Patterns

### Pattern 1: Interactive with SessionStart Hook (Recommended)

Avoids 60-second latency bug.

```bash
#!/bin/bash
# spawn-specialist.sh

unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION=true
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1

alacritty --working-directory ~/symbiont/mycelium/$1 -e claude \
  --add-dir ~/symbiont/core/ \
  --disable-slash-commands
```

SessionStart hook injects instructions from database.

### Pattern 2: Headless Mode (Has Latency Bug)

```bash
#!/bin/bash
unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION=true
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1

claude \
  --add-dir ~/symbiont/core/ \
  --working-directory ~/symbiont/mycelium/$1 \
  --disable-slash-commands \
  --dangerously-skip-permissions \
  --output-format json \
  -p "$2" > output.json
```

### Pattern 3: Named Session Resume

```bash
#!/bin/bash
# Resume persistent specialist context

unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION=true

claude --resume health-coach-main \
  --working-directory ~/symbiont/mycelium/health-coach
```

### Pattern 4: Init Then Interactive

```bash
# First-time setup
claude --init-only --working-directory ~/symbiont/mycelium/new-specialist

# Subsequent launches
claude --working-directory ~/symbiont/mycelium/new-specialist
```

---

## Cost Control

### SDK: --max-budget-usd (v2.0.28+)

→ [Deep dive: --max-budget-usd, agent resume, model selection](research/2-0-42.md)

```typescript
const result = await query({
  prompt: "Refactor authentication module",
  options: {
    maxBudgetUsd: 5.00,
    permissionMode: "bypassPermissions"
  }
});
```

**When exceeded:** Execution stops, returns `error_max_budget_usd`.

### Model Selection for Cost Optimization

| Model | Use Case | Cost |
|-------|----------|------|
| `haiku` | Simple tasks, lookups | Low (~3x cheaper) |
| `sonnet` | Standard development | Medium |
| `opus` | Complex architecture, security | High |

**Orchestrator + Workers Pattern:**
```
Sonnet (orchestrator) → task decomposition
    ├── Haiku (worker) → subtask 1
    ├── Haiku (worker) → subtask 2
    └── Haiku (worker) → subtask 3
```
Result: 2-2.5x cost reduction.

### Budget Guidelines

| Workflow | Budget |
|----------|--------|
| Quick lookup | $0.10 - $0.50 |
| Code review | $0.50 - $2.00 |
| Refactoring | $2.00 - $5.00 |
| Complex migration | $5.00 - $20.00 |
| Full codebase audit | $20.00 - $50.00 |

---

## Feature Matrix by Version

| Version | Date | Key Features | Research |
|---------|------|--------------|----------|
| **2.1.20** | Jan 27 | --add-dir CLAUDE.md loading, task deletion | [research](research/2-1-20.md) |
| **2.1.16** | Jan 22 | Native task system with dependencies | [research](research/2-1-16.md) |
| **2.1.10** | Jan 17 | Setup hook (--init, --maintenance) | [research](research/2-1-10.md) |
| **2.1.9** | Jan 16 | PreToolUse additionalContext | [research](research/2-1-9.md) |
| **2.1.0** | Jan 7 | context:fork, agent field, skill hooks | [research](research/2-1-0.md) |
| **2.0.64** | Dec 10 | Async agents, named sessions, .claude/rules/ | [research](research/2-0-64.md) |
| **2.0.60** | Dec 6 | --disable-slash-commands, background agents | [research](research/2-0-60.md) |
| **2.0.59** | Dec 4 | --agent flag (ignores CLAUDE.md) | [research](research/2-0-59.md) |
| **2.0.45** | Nov 19 | PermissionRequest hook | [research](research/2-0-45.md) |
| **2.0.43** | Nov 18 | SubagentStart hook, permissionMode | [research](research/2-0-43.md) |
| **2.0.42** | Nov 17 | --max-budget-usd (SDK), agent resume | [research](research/2-0-42.md) |

---

## Implementation Examples

### Complete Specialist Spawning Script

```bash
#!/bin/bash
# spawn-mycelium.sh - Spawn a specialist with full autonomous capabilities

SPECIALIST="$1"
TASK="${2:-}"

# Authentication
unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION=true

# Instruction layering
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1

# Spawn in new terminal
alacritty --working-directory ~/symbiont/mycelium/$SPECIALIST -e bash -c "
  claude \
    --add-dir ~/symbiont/core/ \
    --disable-slash-commands
"
```

### SessionStart Hook: Database Instruction Injection

```python
#!/usr/bin/env python3
# ~/.claude/hooks/inject-instructions.py

import json
import sys
import psycopg2

input_data = json.load(sys.stdin)
session_id = input_data.get("session_id")
cwd = input_data.get("cwd")
agent_name = cwd.split("/")[-1]

conn = psycopg2.connect("postgresql://user:pass@host/db")
cur = conn.cursor()
cur.execute("""
    SELECT instructions, context FROM agent_tasks
    WHERE agent_name = %s AND status = 'pending'
    ORDER BY created_at DESC LIMIT 1
""", (agent_name,))
row = cur.fetchone()

if row:
    instructions, context = row
    print(f"## Your Task\n\n{instructions}")
    if context:
        print(f"\n## Context\n\n{context}")

    cur.execute("""
        UPDATE agent_tasks
        SET status = 'in_progress', session_id = %s, started_at = NOW()
        WHERE agent_name = %s AND status = 'pending'
    """, (session_id, agent_name))
    conn.commit()
else:
    print("No pending tasks. Awaiting instructions.")

conn.close()
```

### PreToolUse Hook: Context Injection

```python
#!/usr/bin/env python3
# ~/.claude/hooks/context-injector.py

import json
import sys
import psycopg2

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name")
tool_input = input_data.get("tool_input", {})

if tool_name == "Read":
    file_path = tool_input.get("file_path", "")

    # Inject health context when reading health files
    if "health" in file_path or "meals" in file_path:
        conn = psycopg2.connect("postgresql://...")
        cur = conn.cursor()
        cur.execute("SELECT content FROM soul_data WHERE category='health_context' LIMIT 1")
        row = cur.fetchone()

        if row:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": f"HEALTH CONTEXT:\n{row[0]}"
                }
            }
            print(json.dumps(output))
        conn.close()
```

### Full settings.json for Autonomous Operation

```json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Bash", "Grep", "Glob",
      "Bash(git *)", "Bash(npm *)", "Bash(pnpm *)"
    ],
    "deny": [
      "Bash(rm -rf /)", "Bash(rm -rf ~)", "Bash(sudo *)"
    ]
  },
  "hooks": {
    "Setup": [{
      "matcher": "init",
      "hooks": [{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/init.sh" }]
    }],
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/inject-instructions.py" }]
    }],
    "SessionEnd": [{
      "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/signal-completion.py" }]
    }],
    "PreToolUse": [{
      "matcher": "Read|Edit|Write",
      "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/context-injector.py" }]
    }],
    "PermissionRequest": [{
      "matcher": "*",
      "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/auto-permission.py" }]
    }],
    "SubagentStart": [{
      "hooks": [{ "type": "command", "command": "~/.claude/hooks/log-specialist.sh" }]
    }],
    "SubagentStop": [{
      "hooks": [{ "type": "command", "command": "~/.claude/hooks/log-specialist.sh" }]
    }]
  }
}
```

---

## Sources

### Official Documentation
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Settings Reference](https://code.claude.com/docs/en/settings)
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [Memory Documentation](https://code.claude.com/docs/en/memory)
- [Run Claude Code Programmatically](https://code.claude.com/docs/en/headless)

### GitHub
- [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [Issue #21138](https://github.com/anthropics/claude-code/issues/21138) - --add-dir CLAUDE.md loading (undocumented)
- [Issue #17330](https://github.com/anthropics/claude-code/issues/17330) - 60-second latency bug

### Community Resources
- [How I Built claude_max](https://dsco2048.substack.com/p/how-i-built-claude_max-to-unlock)
- [Claude Code Hooks Mastery](https://github.com/disler/claude-code-hooks-mastery)
- [ClaudeLog Changelog](https://claudelog.com/claude-code-changelog/)
- [ClaudeFast Version History](https://claudefa.st/blog/guide/changelog)
