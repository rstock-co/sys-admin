# Claude Code Tools Reference

Complete reference for tools available to Claude Code primitives (skills, slash commands, subagents, hooks).

**Last verified**: 2025-11-06 (Claude Code v2.0.30+)

---

## Complete Tool List

From official documentation and UI verification (screenshot: `ai_working/my_working_files/skills.png`):

| Tool Name | Description | Permission Required | Available To | Notes |
|-----------|-------------|---------------------|--------------|-------|
| **Bash** | Execute shell commands | Required | All (primitives must request/specify) | Most powerful, requires approval |
| **Glob** | Find files by pattern | None | All | Fast pattern matching |
| **Grep** | Search file contents | None | All | Full regex support |
| **Read** | Read file contents | None | All | Supports multiple formats |
| **Edit** | Make targeted edits | Required | All (primitives must request/specify) | Surgical modifications |
| **Write** | Create/overwrite files | Required | All (primitives must request/specify) | Full file creation |
| **NotebookEdit** | Modify Jupyter cells | Required | All (primitives must request/specify) | Notebook-specific editing |
| **NotebookRead** | Read Jupyter notebooks | None | All | Reads .ipynb files |
| **WebFetch** | Fetch URL content | Required | All (primitives must request/specify) | HTTP requests |
| **TodoWrite** | Manage task lists | None | All | Task tracking |
| **WebSearch** | Perform web searches | Required | All (primitives must request/specify) | Search engines |
| **BashOutput** | Read background shell output | Unknown | All | Read async bash results |
| **KillShell** | Terminate background shells | Unknown | All | Process cleanup |
| **Skill** | Invoke skills | None | All | **ORCHESTRATION**: Enables primitive composition |
| **SlashCommand** | Invoke slash commands | Required | All (primitives must request/specify) | **ORCHESTRATION**: Enables primitive composition |
| **Task** | Invoke subagents | None | All | **ORCHESTRATION**: Enables primitive composition |
| **AskUserQuestion** | Ask user questions with options | Unknown | All | Interactive prompts |

**Source**: [Official tools documentation](https://code.claude.com/docs/en/settings#tools-available-to-claude)

---

## Tool Categories

### File Operations
Read, search, and modify files:
- **Read** - Read file contents (any format)
- **Write** - Create/overwrite files
- **Edit** - Targeted edits to existing files
- **Glob** - Find files by pattern
- **Grep** - Search file contents (regex)
- **NotebookRead** - Read Jupyter notebooks
- **NotebookEdit** - Modify Jupyter cells

### Execution
Run commands and manage processes:
- **Bash** - Execute shell commands
- **BashOutput** - Read background shell output
- **KillShell** - Terminate background shells

### Orchestration (CRITICAL FOR COMPOSITION)
Invoke other primitives:
- **Task** - Invoke subagents
- **Skill** - Invoke skills (model-invoked primitives)
- **SlashCommand** - Invoke slash commands

**Composition Implications**: Primitives with access to Task, Skill, or SlashCommand tools can orchestrate other primitives, enabling powerful multi-layer workflows.

### External
Interact with web and external services:
- **WebFetch** - Fetch URL content
- **WebSearch** - Perform web searches
- **MCP Tools** - Tools from configured MCP servers (dynamic list)

### User Interaction
Communicate with user:
- **AskUserQuestion** - Ask questions with options
- **TodoWrite** - Manage task lists

---

## Tool Inheritance for Primitives

Each primitive type controls tool access differently:

### Skills
**Configuration**: `allowed-tools` field in YAML frontmatter (skills.md L122)

**Behavior**:
- If `allowed-tools` omitted: Claude asks for permission (standard model behavior)
- If `allowed-tools` specified: Only listed tools allowed
- Can include: Any tool from complete list above
- **Including orchestration tools**: Task, Skill, SlashCommand

**Example**:
```yaml
---
name: orchestrator-skill
description: Coordinates multiple specialists
allowed-tools: Read, Grep, Task, Skill
---
```

**Composition**: Skill with `allowed-tools: Task` can invoke subagents. Skill with `allowed-tools: SlashCommand` can invoke slash commands.

**Reference**: See [skills.md](skills.md) for details.

---

### Slash Commands
**Configuration**: `allowed-tools` field in YAML frontmatter (slash-commands.md L178)

**Behavior**:
- Inherits tools from conversation context by default
- If `allowed-tools` specified: Restricts to listed tools
- Can include: Any tool from complete list above
- **Including orchestration tools**: Task, SlashCommand (recursive invocation), Skill

**Example**:
```yaml
---
description: Consolidate documentation
allowed-tools: Task, Read, Grep
---
```

**Composition**: Slash command that inherits Task tool can invoke subagents (VERIFIED in production: `/consolidate-docs` uses Task tool successfully).

**Reference**: See [slash-commands.md](slash-commands.md) for details.

---

### Subagents
**Configuration**: `tools` or `disallowedTools` field in YAML frontmatter (sub-agents.md L152, L178)

**Behavior** (sub-agents.md L178):
- **If `tools` omitted**: **Inherits ALL tools from main thread** (including Task, SlashCommand, Skill)
- **If `tools` specified**: Only listed tools allowed (explicit allow-list)
- **If `disallowedTools` specified**: Inherits all tools EXCEPT listed (deny-list)

**Example (inherit all)**:
```yaml
---
name: orchestrator-agent
description: Coordinates multiple specialists
# tools field omitted → inherits ALL tools, including Task
---
```

**Example (explicit allow-list)**:
```yaml
---
name: read-only-analyst
description: Analyzes code without modifications
tools: Read, Grep, Glob, Bash
---
```

**Example (deny-list)**:
```yaml
---
name: safe-reviewer
description: Reviews code without making changes
disallowedTools: Edit, Write, NotebookEdit
---
```

**Composition**:
- Subagent with no `tools` field → inherits Task, Skill, SlashCommand → can orchestrate other primitives
- Subagent with `tools: Task` → can invoke other subagents (recursive delegation)
- Enables orchestrator pattern (one subagent coordinates multiple specialists)

**Reference**: See [sub-agents.md](sub-agents.md) for details.

---

### Hooks
**Configuration**: None (bash execution only)

**Behavior** (hooks-reference.md L48):
- Hooks execute bash commands directly
- No direct tool access
- Can call CLI tools via bash (indirect)
- Can output instructions for Claude to use tools

**Example**:
```python
# Hook outputs suggestion, Claude decides
print("Suggest using Read tool to check file before edit")
```

**Limitation**: Hooks cannot directly invoke tools, skills, commands, or subagents. They can only suggest actions via stdout.

**Reference**: See [hooks-reference.md](hooks-reference.md) for details.

---

## Permission Requirements

From official documentation:

### No Permission Required (Auto-approved)
- Glob
- Grep
- NotebookRead
- Read
- Task
- TodoWrite
- Skill (likely, verification needed)

### Permission Required (User approval)
- Bash
- Edit
- NotebookEdit
- SlashCommand
- WebFetch
- WebSearch
- Write

### Unknown/Conditional
- AskUserQuestion
- BashOutput
- KillShell

**Note**: Permission requirements apply to main Claude. Primitives using `allowed-tools` can pre-authorize tools.

---

## Orchestration Tools: Composition Implications

**CRITICAL INSIGHT**: Tools `Task`, `Skill`, and `SlashCommand` enable primitives to invoke other primitives.

### Composition Patterns Enabled

**1. Slash Command → Subagent** (VERIFIED in production)
```markdown
# /consolidate-docs.md
---
allowed-tools: Task
---
Use Task tool to invoke zen-docs-manager subagent...
```
**Status**: ✅ PRODUCTION VERIFIED

---

**2. Skill → Subagent**
```yaml
# skills/code-analyzer/SKILL.md
---
allowed-tools: Read, Grep, Task
---
For security analysis, invoke security-auditor via Task tool...
```
**Status**: ✅ SUPPORTED (not yet production tested)

---

**3. Subagent → Subagent (Orchestrator Pattern)**
```yaml
# agents/system-architect.md
---
# tools: omitted → inherits ALL including Task
---
Invoke backend-specialist, frontend-specialist, devops-specialist via Task tool...
```
**Status**: ✅ SUPPORTED (tool inheritance confirmed in docs)

---

**4. Slash Command → Slash Command (Recursive)**
```markdown
# /advanced-workflow.md
---
# inherits SlashCommand tool from conversation
---
First run /analyze, then /optimize, finally /deploy...
```
**Status**: ✅ SUPPORTED (SlashCommand tool available)

---

### Orchestration Anti-Patterns

**Skills cannot invoke other skills programmatically**:
- No `Skill` tool exists for invoking specific skills
- Skills are model-invoked (Claude decides based on context)
- Workaround: Skill can output suggestions that trigger Claude's skill selection

**Hooks cannot invoke primitives directly**:
- Hooks are bash-only
- Can output suggestions that Claude reads
- Cannot programmatically invoke skills/commands/subagents

---

## MCP Tools Integration

**Subagents** (sub-agents.md L184):
- When `tools` field omitted: Inherits ALL MCP tools from main thread
- When `tools` specified: Must explicitly list MCP tools (format: `mcp__server__tool`)

**Skills** (skills.md L122):
- Can access MCP tools if listed in `allowed-tools`
- Format: `mcp__server__tool` (double underscores)

**Slash Commands**:
- Inherit MCP tools from conversation context
- Can restrict via `allowed-tools`

**Example**:
```yaml
---
name: github-manager
allowed-tools: Read, mcp__github__create_pr, mcp__github__list_issues
---
```

---

## Tool Selection Guidelines

### When to Grant Tool Access

**Read-only operations**:
- Read, Grep, Glob, NotebookRead
- Safe for analysis/review subagents

**Modification operations**:
- Edit, Write, NotebookEdit
- Grant only to trusted/specialized primitives

**Execution**:
- Bash (most powerful, highest risk)
- Grant only when necessary

**Orchestration**:
- Task, Skill, SlashCommand
- Grant when primitive needs to coordinate other primitives

### Restrictive vs Permissive

**Restrictive** (explicit allow-list):
```yaml
tools: Read, Grep, Glob
```
Use when: Primitive has narrow, well-defined purpose

**Permissive** (inherit all):
```yaml
# tools: omitted
```
Use when: Primitive needs flexibility, is trusted

**Deny-list** (inherit all except):
```yaml
disallowedTools: Edit, Write, Bash
```
Use when: Primitive needs most tools but must avoid specific risky ones

---

## References

**Official Documentation**:
- [Tools available to Claude](https://code.claude.com/docs/en/settings#tools-available-to-claude)
- [Skills documentation](https://code.claude.com/docs/en/skills)
- [Slash commands documentation](https://code.claude.com/docs/en/slash-commands)
- [Subagents documentation](https://code.claude.com/docs/en/sub-agents)
- [Hooks documentation](https://code.claude.com/docs/en/hooks-guide)

**Screenshot Verification**:
- `ai_working/my_working_files/skills.png` (shows Skill and SlashCommand tools in UI)

**Production Examples**:
- `/consolidate-docs` slash command successfully uses Task tool to invoke zen-docs-manager subagent

**Related Documentation**:
- [selecting-primitives.md](selecting-primitives.md) - How to choose primitives
- [re-audit-report.md](re-audit-report.md) - Primitive composition audit findings

---

## Quick Reference: Common Tool Combinations

| Use Case | Recommended Tools | Rationale |
|----------|-------------------|-----------|
| Read-only analysis | Read, Grep, Glob | Safe, non-destructive |
| Code modification | Read, Edit, Grep, Glob | Surgical changes |
| Full file creation | Read, Write, Grep, Glob | Complete control |
| Build/test automation | Bash, Read | Execution + verification |
| External data fetch | WebFetch, Read, Write | Fetch + process |
| Multi-agent coordination | Task, Read, Grep | Delegate + gather context |
| Workflow orchestration | Task, SlashCommand, Skill, Read | Full composition capability |
| Safe code review | Read, Grep, Glob (no Edit/Write) | Prevent accidental changes |

---

**Last Updated**: 2025-11-06
**Claude Code Version**: v2.0.30+
**Verified By**: Screenshot verification + production testing + official docs
