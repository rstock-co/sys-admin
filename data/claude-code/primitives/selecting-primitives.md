# Selecting the Right Claude Code Primitive(s)

**Purpose**: Match user needs to optimal primitive(s). Read AFTER clarifying user intent.

---

## Part 1: Primitive Overview

### Skills (Model-Invoked Capabilities)

**What**: Modular capabilities Claude autonomously discovers and invokes based on context. Contains SKILL.md with YAML frontmatter + optional supporting files.

**Activation**: Claude decides when to use based on `description` field matching user request.

**When to use**:
- Claude needs domain expertise automatically (PDF processing, data analysis, code review)
- Capability requires multiple files (scripts, templates, reference docs)
- Team wants standardized workflow accessible on-demand

**Characteristics**:
- Automatic discovery (no explicit invocation needed)
- Can contain subdirectories with organized documentation
- Supports `allowed-tools` to restrict tool access (security/scope control)
- Progressive disclosure (Claude loads files only when needed)

**Examples**:
- PDF processing skill with form-filling scripts
- Data analysis skill with reference docs
- Code review skill with security checklists

**Allowed Combinations**:
- Can be invoked by: Main Claude (model-decision based on context)
- Can access: Tools (via `allowed-tools` field), MCP tools
- Can invoke: Subagents (via Task tool if `allowed-tools` includes Task or inherits all)
- Can invoke: Slash commands (via SlashCommand tool if `allowed-tools` includes SlashCommand)
- Cannot invoke: Other skills programmatically (no Skill tool exists; skills are model-invoked)
- Cannot invoke: Hooks (bash-only, no invocation mechanism)

**Tool Access**: See [tools-reference.md](tools-reference.md) for complete tool list and composition capabilities.

**File**: `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/<name>/SKILL.md` (user)

---

### Slash Commands (User-Invoked Instructions)

**What**: User explicitly invokes with `/command-name`. Single Markdown file with optional YAML frontmatter.

**Activation**: User types `/command-name` (optionally with arguments).

**When to use**:
- User wants explicit control over when action runs
- Simple prompt snippet used repeatedly
- Quick template or reminder
- Need to execute bash commands before prompt (with `!` prefix)

**Characteristics**:
- Explicit invocation (user decides when)
- Supports arguments (`$ARGUMENTS`, `$1`, `$2`, etc.)
- Can execute bash commands before running (`!` prefix with `allowed-tools: Bash(...)`)
- Can trigger extended thinking (include thinking keywords)
- Supports file references (`@file.txt`)
- Can specify model, allowed-tools, argument hints

**Examples**:
- `/review` - Review code for bugs
- `/commit` - Generate commit message from git diff
- `/optimize $1` - Analyze file for performance issues

**Allowed Combinations**:
- Can be invoked by: User (explicit `/command`), Main Claude (via SlashCommand tool)
- Can access: Tools (via `allowed-tools` - inherits from conversation), bash commands (`!` prefix), file references (`@`)
- Can invoke: Subagents (via Task tool - VERIFIED in `/consolidate-docs` production example)
- Can invoke: Other slash commands (via SlashCommand tool recursively)
- Cannot invoke: Skills programmatically (no Skill tool; instructions to Claude may trigger skills indirectly)
- Cannot invoke: Hooks (bash-only, no invocation mechanism)

**Tool Access**: See [tools-reference.md](tools-reference.md) for complete tool list and composition capabilities.

**File**: `.claude/commands/<name>.md` (project) or `~/.claude/commands/<name>.md` (user)

---

### Hooks (Event-Triggered Automation)

**What**: Shell commands that execute automatically on specific events (tool use, session start, etc.). Guaranteed execution without relying on LLM memory.

**Activation**: Automatically triggered by events (PreToolUse, PostToolUse, Notification, Stop, SessionStart, etc.).

**When to use**:
- Automatic formatting after file edits (prettier, gofmt)
- Validation before operations (prevent editing sensitive files)
- Logging/auditing (track all bash commands)
- Notifications (desktop alerts when Claude needs input)
- Workflow enforcement (run tests after code changes)
- Environment setup (SessionStart: load env vars, install deps)

**Characteristics**:
- Deterministic (always runs, no LLM decision)
- Receives JSON via stdin with event context
- Returns exit codes (0=success, 2=block, other=non-blocking error)
- Can block operations (PreToolUse: deny tool, UserPromptSubmit: block prompt)
- Can modify tool inputs (PreToolUse: `updatedInput` field)
- Can add context (UserPromptSubmit, SessionStart: stdout added to context)
- 60-second timeout (configurable per command)
- Multiple hooks run in parallel

**Examples**:
- PostToolUse on Edit/Write → run linter
- PreToolUse on Bash → validate command patterns
- Notification → send desktop notification
- SessionStart → load project context, set env vars

**Tool Access**: See [tools-reference.md](tools-reference.md) for hook limitations and indirect tool access patterns.

**File**: Python/shell script in `.claude/hooks/`, registered in `.claude/settings.json`

---

### Subagents (Specialized Task Contexts)

**What**: Specialized AI personalities with custom system prompts, separate context windows, and specific tool access. Delegated by main Claude or invoked explicitly.

**Activation**: Claude delegates automatically based on task match, or user explicitly invokes ("Use the X subagent...").

**When to use**:
- Complex multi-step task requiring specialized expertise
- Need separate context to avoid polluting main conversation
- Different tool access levels (e.g., read-only analyst vs. code-writer)
- Task-specific instructions too detailed for main prompt

**Characteristics**:
- Isolated context window (preserves main conversation)
- Custom system prompt (tailored instructions)
- Configurable tool access (inherit all, explicit allow-list, or disallow-list)
- Model selection (specify model alias or inherit from main)
- Reusable across projects (user-level) or shared with team (project-level)

**Examples**:
- `code-reviewer` - Reviews code without making changes (Read, Grep, Glob only)
- `debugger` - Investigates errors with full tool access
- `data-scientist` - SQL queries and analysis (Bash, Read, Write only)

**Allowed Combinations**:
- Can be invoked by: Main Claude (task delegation), User (explicit request)
- Can access: Tools (configurable via `tools` field), MCP tools
- Can invoke: Other subagents (via Task tool if `tools` field includes Task or is omitted - default inherits all)
- Can invoke: Slash commands (via SlashCommand tool if inherited or specified)
- Cannot invoke: Skills programmatically (no Skill tool exists; skills are model-invoked)
- Cannot invoke: Hooks (bash-only, no invocation mechanism)

**Tool Access**: See [tools-reference.md](tools-reference.md) for complete tool list and composition capabilities.

**File**: `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (user)

---

### MCP Servers (External Service Integration)

**What**: Model Context Protocol servers that expose external tools, resources, and prompts to Claude. Connect to databases, APIs, issue trackers, monitoring tools, etc.

**Activation**: Claude uses MCP tools automatically, user references MCP resources with `@`, or user invokes MCP prompts via `/mcp__server__prompt`.

**When to use**:
- Need access to external service (GitHub, Jira, Sentry, databases)
- Integrating with existing APIs/tools
- Real-time data from external systems
- Team needs standardized external integrations

**Characteristics**:
- Three transport types: HTTP (remote servers), SSE (deprecated), stdio (local processes)
- Tools appear as `mcp__server__tool` (callable by Claude)
- Resources appear in `@` mentions (protocol://resource/path)
- Prompts appear as `/mcp__server__prompt` slash commands
- OAuth support for authentication
- Scopes: local (user-only, project-specific), project (shared via .mcp.json), user (cross-project)

**Examples**:
- GitHub MCP → Create PRs, review issues
- Sentry MCP → Query errors, debug production
- PostgreSQL MCP → Query databases directly
- Figma MCP → Fetch designs for implementation

**Configuration**: `claude mcp add --transport <http|sse|stdio> <name> <url|command>`

---

## Part 2: Selection Guidance

### Decision Tree

Start here when choosing primitive(s):

```
1. Does this need to connect to EXTERNAL service/API?
   YES → MCP Server
   NO → Continue to 2

2. Should this run AUTOMATICALLY on specific events?
   YES → Hook
   NO → Continue to 3

3. Does user want EXPLICIT CONTROL over when it runs?
   YES → Slash Command
   NO → Continue to 4

4. Is this COMPLEX MULTI-STEP task needing specialized context?
   YES → Subagent
   NO → Continue to 5

5. Does Claude need this capability ON-DEMAND based on context?
   YES → Skill
   NO → Reconsider requirements (may need multiple primitives)
```

---

### Comparison Table

| Primitive         | Activation                     | User Control             | Best For                                                      | Avoid When                                     |
| ----------------- | ------------------------------ | ------------------------ | ------------------------------------------------------------- | ---------------------------------------------- |
| **Skill**         | Model decides                  | No (automatic)           | Domain expertise, multi-file capabilities, team workflows     | User needs explicit control, simple one-liners |
| **Slash Command** | User types `/cmd`              | Yes (explicit)           | Repeated prompts, templates, user-controlled workflows        | Need automatic execution, complex multi-step   |
| **Hook**          | Event triggers                 | No (automatic)           | Automation, validation, logging, guaranteed execution         | Task requires intelligence/LLM reasoning       |
| **Subagent**      | Task delegation                | Partial (Claude or user) | Complex specialized tasks, isolated context, restricted tools | Simple single-step operations                  |
| **MCP**           | Tool calls, resources, prompts | Mixed (depends on usage) | External service integration, real-time data                  | Internal-only capabilities                     |

---

### Key Decision Factors

**User Control vs Autonomous Behavior**:
- Explicit user control → Slash Command
- Automatic based on context → Skill
- Automatic on events → Hook
- Delegated by Claude or user → Subagent

**Execution Frequency**:
- Every time event occurs → Hook
- On-demand when needed → Skill
- Repeatedly invoked → Slash Command
- Complex task once → Subagent

**Complexity Level**:
- Simple prompt snippet → Slash Command
- Multi-file capability → Skill
- Deterministic automation → Hook
- Complex reasoning task → Subagent

**Context Management**:
- Add to main context → Skill or Slash Command
- Separate context → Subagent
- No context impact → Hook (side effects only)

**External Dependencies**:
- External service required → MCP Server
- Internal Claude Code only → Other primitives

---

## Part 3: Powerful Primitive Combinations

Synergistic patterns that solve complex scenarios:

---

### 1. Skill + Slash Command (Dual Activation)

**Problem Solved**: Capability needs both automatic discovery AND explicit user control.

**Primitives Used**: Skill + Slash Command (same functionality, different triggers)

**How They Work Together**:
- Skill provides automatic invocation when Claude detects need
- Slash command provides explicit control when user wants to force execution
- Both reference same underlying scripts/logic (DRY)

**Example**:
```
Skill: code-review (Claude invokes after detecting code changes)
Command: /review (user explicitly requests review anytime)
Both use: .claude/skills/code-review/scripts/review.sh
```

**Why This Works**: Flexibility—automatic when convenient, manual when needed. No duplication of logic.

---

### 2. Hook + Skill (Automated Triggering)

**Problem Solved**: Skill needs guaranteed execution without relying on LLM to remember.

**Primitives Used**: Hook triggers event → Skill provides capability

**How They Work Together**:
- Hook detects event (PostToolUse: Edit/Write)
- Hook output instructs Claude to invoke specific Skill
- Skill executes with full context and capabilities

**Example**:
```
Hook: PostToolUse on Edit → outputs "Run the test-runner skill"
Skill: test-runner → runs tests, analyzes failures, fixes them
```

**Why This Works**: Hook ensures action always happens, Skill provides intelligence.

---

### 3. Slash Command + Hook (User-Initiated Workflow Automation)

**Problem Solved**: User starts workflow, subsequent steps run automatically.

**Primitives Used**: Slash Command initiates → Hooks automate follow-up

**How They Work Together**:
- User invokes slash command to start workflow
- Command performs initial action
- Hooks automatically handle subsequent steps (formatting, validation, notifications)

**Example**:
```
Command: /commit → generates commit message
Hook: PostToolUse on Bash(git commit) → runs tests, pushes if pass
Hook: Notification → sends desktop alert when complete
```

**Why This Works**: User initiates intentionally, automation handles tedious follow-up.

---

**Why This Works**: Subagent provides isolation and focus, Skills provide specialized capabilities.

---

### 5. Hook + MCP (Event-Driven External Integration)

**Problem Solved**: External service needs automatic updates based on Claude Code events.

**Primitives Used**: Hook detects event → Calls MCP tool for external action

**How They Work Together**:
- Hook triggers on event (PostToolUse: file save, Stop: task complete)
- Hook invokes MCP tool programmatically or outputs instruction
- External service receives update automatically

**Example**:
```
Hook: PostToolUse on Write → triggers GitHub MCP to update PR
Hook: Stop → triggers Jira MCP to update issue status
Hook: SubagentStop → triggers Slack MCP to send completion notification
```

**Why This Works**: Guaranteed external sync without relying on LLM memory.

---

### 6. Multiple Hooks (Multi-Stage Workflow)

**Problem Solved**: Complex workflow requires multiple deterministic steps in sequence.

**Primitives Used**: Chain of hooks at different events

**How They Work Together**:
- Hook 1: PreToolUse → validates operation can proceed
- Hook 2: PostToolUse → formats output
- Hook 3: PostToolUse → runs tests
- Hook 4: Notification → alerts user of results

**Example**:
```
PreToolUse on Edit → validates file not protected
PostToolUse on Edit → runs prettier formatter
PostToolUse on Edit → runs linter, blocks if errors (exit code 2)
Notification → desktop alert "File edited and validated"
```

**Why This Works**: Each hook guarantees its step executes, no LLM decision failures.

---

### 7. Skill + MCP (Enhanced Capability with External Data)

**Problem Solved**: Capability requires both LLM intelligence AND real-time external data.

**Primitives Used**: Skill orchestrates logic → MCP provides data

**How They Work Together**:
- Skill contains instructions for analysis/workflow
- Skill uses MCP tools to fetch real-time data
- Skill applies intelligence to external data
- Results presented with full context

**Example**:
```
Skill: incident-responder
- Fetches errors from Sentry MCP
- Analyzes stack traces and logs
- Queries database via PostgreSQL MCP
- Cross-references with GitHub MCP issues
- Generates comprehensive incident report
```

**Why This Works**: Skill provides intelligence, MCP provides real-time data. Best of both worlds.

---

### 8. Hook + Slash Command + Subagent (Complete Automation System)

**Problem Solved**: System needs manual triggers, automatic enforcement, and specialized execution.

**Primitives Used**: All three working together

**How They Work Together**:
- Slash command: User initiates complex workflow
- Hook (PreToolUse): Validates operation can proceed
- Hook (PostToolUse): Enforces standards automatically
- Subagent: Handles complex sub-task in isolated context
- Hook (SubagentStop): Confirms subagent completion
- Hook (Notification): Alerts user when complete

**Example**:
```
/deploy-feature → User initiates deployment
PreToolUse hook → Validates all tests pass
Subagent: deployment-coordinator → Handles multi-step deployment
PostToolUse hooks → Update external systems (Jira, Slack, monitoring)
Notification hook → Desktop alert "Deployment complete"
```

**Why This Works**: Combines control, automation, and specialized execution for robust workflows.

---

## Selection Anti-Patterns

**DON'T**:
- ❌ Use Skill for simple prompt snippets → Use Slash Command
- ❌ Use Slash Command when automatic execution needed → Use Hook or Skill
- ❌ Use Hook for operations requiring LLM intelligence → Use Skill or Subagent
- ❌ Use Subagent for simple single-step operations → Use Skill
- ❌ Duplicate logic across primitives → Use combinations that reference shared scripts

**DO**:
- ✅ Clarify user intent FIRST before selecting primitive(s)
- ✅ Consider combinations for complex workflows
- ✅ Use hooks for guaranteed execution (don't rely on LLM memory)
- ✅ Keep primitives focused (single responsibility)
- ✅ Leverage existing primitives before creating new ones

---

## Quick Reference: Common Scenarios

| User Need                                       | Recommended Primitive(s)                         |
| ----------------------------------------------- | ------------------------------------------------ |
| "Run linter after every file edit"              | Hook (PostToolUse on Edit/Write)                 |
| "Command to generate boilerplate code"          | Slash Command                                    |
| "Claude should review code automatically"       | Skill (code-review)                              |
| "Specialized code analyzer for security"        | Subagent (security-auditor)                      |
| "Connect to GitHub for PR management"           | MCP Server (GitHub)                              |
| "Format files AND run tests automatically"      | Multiple Hooks (PostToolUse chain)               |
| "User starts workflow, automation handles rest" | Slash Command + Hooks                            |
| "Complex task needing external data"            | Subagent + MCP or Skill + MCP                    |
| "Enforce code standards without LLM decision"   | Hook (PreToolUse: validate, PostToolUse: format) |
| "Team-wide capability with documentation"       | Skill (multi-file structure)                     |

---

## Tool Access Reference

All primitives can access tools, but with different inheritance models:

**Skills**:
- Specified via `allowed-tools` field
- If omitted: Claude asks for permission (standard model)
- Can include orchestration tools (Task, SlashCommand) for composition

**Slash Commands**:
- Inherit tools from conversation context
- Can specify `allowed-tools` to restrict
- Can include orchestration tools (Task, SlashCommand) for composition

**Subagents**:
- If `tools` field omitted: **Inherits ALL tools** (including Task, Skill, SlashCommand)
- If `tools` field specified: Only listed tools
- Use `disallowedTools` to inherit all EXCEPT specific tools

**Hooks**:
- Bash execution only (no direct tool access)
- Can call CLI tools via bash
- Can output instructions for Claude to use tools

**Complete tool list**: See [tools-reference.md](tools-reference.md) for all available tools, composition patterns, and permission requirements.

**Orchestration tools** (Task, Skill, SlashCommand) enable primitive composition - primitives can invoke other primitives when these tools are available.

---

**Next Steps After Selection**:

1. Confirm selection with user ("Based on your needs, I recommend X primitive(s) because...")
2. Load appropriate template(s) from `templates/`
3. Reference detailed docs if needed (`docs/<primitive>.md`)
4. Build implementation
5. Validate against requirements
6. Test before presenting

**Remember**: Selection happens AFTER clarifying user intent. Never assume.
