# Claude Code - What Matters to AEGIS

Personalized changelog filtered through [context.md](context.md).

**Core Project**: AEGIS - work automation system where Claude Code IS the runtime for all Bullin Construction work.
**Architecture**: Single agent + parallel workers spawned in Alacritty terminals, Neon database, 30+ slash commands.
**Critical Dependencies**: Slash commands, `.claude/rules/`, hooks (worker auto-approval), `--disable-slash-commands`, session state, context loading.
**Environment**: Arch Linux, Hyprland, Alacritty, main session + 4-6 parallel workers hitting Neon.

---

## Relevance Legend

| Icon | Level | Meaning |
|------|-------|---------|
| :rocket: | **Critical** | Directly affects AEGIS operations - commands, rules, hooks, workers |
| :sparkles: | **High** | Significant workflow enhancement - sessions, context, parallelism |
| :wrench: | **Medium** | Quality of life - environment fixes, keyboard shortcuts, performance |

---

## Quick Reference

| Version | Date | Relevance | Why It Matters to AEGIS |
|---------|------|-----------|-------------------------|
| 2.1.50 | Feb 21 | :sparkles: | Opus 4.6 1M context, worktree hooks, memory leak fixes for parallel work |
| 2.1.49 | Feb 20 | :rocket: | --worktree flag for worker isolation, ConfigChange hook, background:true agents |
| 2.1.45 | Feb 17 | :sparkles: | Sonnet 4.6 - cheaper model for simple worker tasks |
| 2.1.42 | Feb 13 | :wrench: | /rename auto-generation, @-mention anchor fragments |
| 2.1.39 | Feb 11 | :wrench: | Nested session guard prevents accidental worker-in-worker |
| 2.1.33 | Feb 6 | :sparkles: | TeammateIdle/TaskCompleted hooks, memory frontmatter for agents |
| 2.1.32 | Feb 5 | :rocket: | Opus 4.6, Agent Teams, auto memory, skills from --add-dir |
| 2.1.30 | Feb 3 | :sparkles: | PDF page ranges, /debug command, 68% session resume optimization |
| 2.1.27 | Jan 30 | :sparkles: | --from-pr flag, debug logging for tool failures |
| 2.1.23 | Jan 29 | :wrench: | Terminal rendering perf, ripgrep error reporting |
| 2.1.21 | Jan 28 | :sparkles: | Session resume during tool execution, file tools preferred |
| 2.1.20 | Jan 27 | :sparkles: | --add-dir CLAUDE.md loading - layer instructions for workers |
| 2.1.19 | Jan 23 | :wrench: | Skills auto-allow without prompts, $0/$1 shorthand |
| 2.1.18 | Jan 23 | :wrench: | Enhanced /keybindings with chord sequences |
| 2.1.16 | Jan 22 | :sparkles: | Native task system - potential worker coordination enhancement |
| 2.1.14 | Jan 20 | :sparkles: | Memory leak fixes for parallel workers, context window fix (65%->98%) |
| 2.1.10 | Jan 17 | :sparkles: | Setup hook event - new lifecycle hook |
| 2.1.9 | Jan 16 | :rocket: | PreToolUse additionalContext - inject context into tool calls |
| 2.1.7 | Jan 14 | :wrench: | Customizable keybindings.json for terminal workflow |
| 2.1.6 | Jan 13 | :rocket: | Nested skill/command discovery from subdirectories |
| 2.1.3 | Jan 9 | :rocket: | Unified commands/skills model - commands ARE skills |
| 2.1.0 | Jan 9 | :sparkles: | Skill hot-reload, context:fork for research without context pollution |
| 2.0.74 | Dec 19 | :wrench: | Alacritty terminal setup, LSP for code navigation |
| 2.0.73 | Dec 19 | :wrench: | Kill ring paste cycling across sessions |
| 2.0.72 | Dec 18 | :wrench: | Chrome automation - potential expansion path |
| 2.0.70 | Dec 16 | :wrench: | MCP wildcards for permission management |
| 2.0.67 | Dec 12 | :sparkles: | Opus 4.5 extended thinking on by default |
| 2.0.65 | Dec 11 | :sparkles: | Context window indicator for long sessions |
| 2.0.64 | Dec 10 | :rocket: | Async agents, named sessions, .claude/rules/ |
| 2.0.62 | Dec 9 | :wrench: | Symlinked skill directories fix |
| 2.0.60 | Dec 6 | :sparkles: | Background agents, /mcp enable/disable toggles |
| 2.0.59 | Dec 4 | :wrench: | --agent flag - useful for worker persona definitions |
| 2.0.54 | Nov 26 | :wrench: | PermissionRequest hook modifications |
| 2.0.52 | Nov 25 | :wrench: | Linux Wayland image paste fix |
| 2.0.51 | Nov 24 | :sparkles: | Opus 4.5 - better reasoning in all AEGIS operations |
| 2.0.45 | Nov 19 | :rocket: | PermissionRequest hook for worker auto-approval |
| 2.0.43 | Nov 18 | :sparkles: | Agent permissionMode, SubagentStart hook |
| 2.0.42 | Nov 17 | :sparkles: | Agent resume, model selection for subagents |
| 2.0.41 | Nov 14 | :wrench: | Plugin output styles, SDK hook timeouts |
| 2.0.37 | Nov 11 | :wrench: | Notification hook matchers |
| 2.0.34 | Nov 6 | :wrench: | Rust fuzzy finder for file suggestions |
| 2.0.32 | Nov 4 | :wrench: | Output styles un-deprecated |
| 2.0.31 | Nov 1 | :wrench: | Tool name collision fix (subagents + MCP) |

---

## :rocket: Critical - Architecture Foundations

### :rocket: v2.1.49 - February 20, 2026

**What Changed**: `--worktree` flag for git worktree isolation. `ConfigChange` hook event. Agent `background: true` frontmatter. `Ctrl+F` to kill background agents.

**AEGIS Impact**:
Two features with major architectural implications for the worker system.

**`--worktree` as Worker Isolation Alternative:**
Currently AEGIS spawns workers in the same working directory with `--disable-slash-commands`. The new `--worktree` flag creates a fully isolated git worktree per session - independent file system, no edit conflicts. This could replace or augment the current worker pattern:

```bash
# Current pattern:
alacritty -e claude --disable-slash-commands --prompt "/worker T-XXX"

# Potential worktree pattern:
alacritty -e claude --worktree --disable-slash-commands --prompt "/worker T-XXX"
```

Benefits: Workers can modify files without conflicting with each other or the main session. No more race conditions on shared files. Each worker gets its own branch.

Trade-off: Worktrees add git overhead and require merging results back. For workers that primarily interact with Neon (not local files), the overhead may not be worth it. Best suited for file-heavy tasks like document generation or code modifications.

**`ConfigChange` Hook:**
Fires when configuration files change during a session. For AEGIS:
- Detect when `.claude/rules/` files are modified mid-session (people profiles updated, coaching triggers changed)
- Audit trail for configuration changes
- Could trigger rule reload or notification when rules are updated while workers are running

**Agent `background: true`:**
Agent definitions can auto-background without manual Ctrl+B. If AEGIS defines background research agents, they'd automatically spawn as background tasks.

**Action**: Evaluate `--worktree` with file-heavy worker tasks. Implement `ConfigChange` hook to monitor `.claude/rules/` modifications.

---

### :rocket: v2.1.32 - February 5, 2026

**What Changed**: Opus 4.6 model. Agent Teams (research preview). Automatic memory recording/recall. "Summarize from here." Skills from `--add-dir`.

**AEGIS Impact**:
The most significant release for AEGIS since v2.0.64. Multiple features affect core operations.

**Opus 4.6 - Better Reasoning Everywhere:**
Every AEGIS operation improves with Opus 4.6:
- **Adaptive thinking** replaces manual extended thinking toggle - Claude decides when to think deeply. Complex drafting (`/comms/draft`) gets deep reasoning automatically, simple status checks stay fast.
- **1M context window (beta)** means the main AEGIS session can hold 5x more context. Strategic context, people profiles, state, conversation history - all fit without aggressive compaction.
- **128K output** doubles the previous limit. Workers generating long documents or detailed analyses hit the ceiling less often.
- **Stronger agentic coding** means workers are more reliable at multi-step tasks - fewer failures, better planning, catches own mistakes.
- **Same pricing** ($5/$25) - no cost increase for the upgrade.

The `effort` parameter (high/medium/low) could optimize worker costs: simple file operations at `low` effort, complex drafting at `high`.

**Auto Memory:**
Claude automatically records and recalls session memories. For AEGIS:
- The main session builds knowledge about recurring patterns, people preferences, and workflow optimizations over time
- Workers benefit from shared project memory at `~/.claude/projects/{path}/memory/MEMORY.md`
- Potential interaction with `state.json` - auto memory might capture state that AEGIS already manages in Neon

**Concern**: Auto memory could save information AEGIS manages in Neon (task state, people data), creating dual sources of truth. Monitor what gets auto-saved and whether it conflicts with Neon as source of truth.

**Agent Teams:**
Research preview using tmux for multi-agent coordination. AEGIS already has its own worker pattern (Alacritty terminals + Neon task claiming). Agent Teams is an alternative approach - lighter weight (within one session) but less isolation than full terminal workers.

**Evaluation**: For research-heavy tasks that don't need Neon persistence, Agent Teams could complement AEGIS workers. For production work tasks, the Alacritty + Neon pattern is more robust. Not a replacement, potentially complementary.

**Skills from `--add-dir`:**
Combined with v2.1.20's CLAUDE.md loading, workers spawned with `--add-dir` now get both instructions AND skills from shared directories. Complete instruction layering for workers.

**Action**: Already running Opus 4.6. Monitor auto memory behavior to ensure it doesn't conflict with Neon state management. Evaluate Agent Teams for research-class tasks.

---

### :rocket: v2.1.9 - January 16, 2026

**What Changed**: PreToolUse hooks can return `additionalContext`. Added `${CLAUDE_SESSION_ID}` for skills.

**AEGIS Impact**:
This is a game-changer for worker context priming.

**PreToolUse additionalContext:**
Hooks can now INJECT context before any tool executes. For AEGIS workers, this means:

1. **Task context injection** - Before a worker reads a file, inject relevant task spec data from Neon
2. **People context** - Before drafting a communication, inject the recipient's profile and signal history
3. **Buffer awareness** - Before completing a task, inject current buffer health so the worker knows delivery timing

Example use case:
```javascript
// PreToolUse hook for workers
// Before writing a draft, inject person's communication style
if (tool === "Write" && path.includes("drafts")) {
  return { additionalContext: await getPersonProfile(recipient) }
}
```

**Session ID for Skills:**
Skills can reference `${CLAUDE_SESSION_ID}`. Each worker session gets a unique ID - use this to:
- Track which worker is active in Neon logs
- Key operations by session for debugging
- Correlate worker output with specific task claims

**Action**: Build PreToolUse hooks that inject Neon context. Could replace some of the manual @mention priming in commands.

---

### :rocket: v2.1.6 - January 13, 2026

**What Changed**: Automatic skill/command discovery from nested `.claude/skills` and `.claude/commands` directories.

**AEGIS Impact**:
AEGIS has 30+ slash commands organized across subsystems. Nested discovery means cleaner organization:

```
.claude/commands/
├── daily/
│   ├── startup/
│   ├── next/
│   ├── done/
│   └── signoff/
├── comms/
│   ├── draft/
│   ├── approve/
│   ├── log/
│   └── history/
├── buffer/
│   ├── status/
│   └── release/
├── coach/
│   ├── coach/
│   └── debrief/
└── worker/
```

All commands auto-discovered without manual registration. Better organization as AEGIS grows beyond 30 commands.

---

### :rocket: v2.1.3 - January 9, 2026

**What Changed**: Merged slash commands and skills into unified model.

**AEGIS Impact**:
This is foundational. AEGIS is built entirely on slash commands. Now every command IS a skill, and every skill IS a command. This means:

1. **Unified infrastructure** - All AEGIS commands get skill features (frontmatter, hot-reload, context forking)
2. **Consistent behavior** - No difference between built-in `/compact` and custom `/startup`
3. **Future-proof** - New skill features automatically apply to all AEGIS commands

This validates AEGIS's command-centric architecture. Building everything as commands was the right call.

---

### :rocket: v2.0.64 - December 10, 2025

**What Changed**: Async agent/bash execution. Named sessions. `.claude/rules/` directory. Instant auto-compacting.

**AEGIS Impact**:
Four features that are core to AEGIS operations:

1. **`.claude/rules/` directory** - This IS how AEGIS defines behavior. People profiles (`people/mike.md`), coaching triggers, commitment detection - all live in rules. Without this feature, AEGIS doesn't work.

2. **Named sessions** - Save and resume specific work states. The main AEGIS session can be named and resumed daily. `state.json` complements this for operational state.

3. **Async execution (Ctrl+B)** - Background research while the main session continues. Useful when a command needs to query Neon for a slow aggregation.

4. **Auto-compacting** - Long AEGIS sessions with rich context (strategic context, people profiles, state) need smart compaction to stay within limits.

---

### :rocket: v2.0.45 - November 19, 2025

**What Changed**: PermissionRequest hook. Background tasks with `&` prefix.

**AEGIS Impact**:
**PermissionRequest hook** is how workers achieve autonomy:
- Auto-approve all file operations in the AEGIS directory
- Auto-approve Bun execution for `bun app/db/exec.ts` calls
- Auto-approve git commits for audit trail
- Deny operations outside the AEGIS working directory

Without this hook, every worker would block on permission prompts, making parallel execution impossible. This is the foundation of the worker auto-approval system.

---

## :sparkles: High - Significant Workflow Impact

### :sparkles: v2.1.50 - February 21, 2026

**What Changed**: Opus 4.6 fast mode gets full 1M context window. `WorktreeCreate`/`WorktreeRemove` hook events. `claude agents` CLI command. Massive memory leak cleanup (8+ distinct leaks fixed).

**AEGIS Impact**:
**1M Context in Fast Mode:**
Opus 4.6 fast mode now has the full 1M token context window. The main AEGIS session running in fast mode (`/fast`) can hold the same massive context as normal mode. Strategic context, all people profiles, full state, and extensive conversation history - all fit without compaction pressure.

**Memory Leak Fixes - Critical for Parallel Workers:**
This release fixes leaks in: agent teams completed tasks, task state objects, LSP diagnostics, completed task output, TaskOutput retained lines, CircularBuffer, shell ChildProcess references, and file history snapshots. With 4-6 parallel workers running extended sessions, accumulated leaks degraded system performance. This release directly improves worker stability and system-wide resource usage.

**Worktree Hooks:**
If AEGIS adopts `--worktree` for workers (v2.1.49), these hooks enable:
- `WorktreeCreate` → Log worker initialization to Neon, configure worker-specific git settings
- `WorktreeRemove` → Clean up worker state, verify task artifacts were committed

---

### :sparkles: v2.1.45 - February 17, 2026

**What Changed**: Claude Sonnet 4.6 model. Plugins from `--add-dir` directories. Deferred schema loading for faster startup.

**AEGIS Impact**:
**Sonnet 4.6 for Cost-Optimized Workers:**
Sonnet 4.6 approaches Opus quality at 1/5 the cost ($3/$15 vs $5/$25). For AEGIS worker optimization:
- Simple workers (file operations, status updates, data entry) could run on Sonnet 4.6
- Complex workers (drafting in Richard's voice, strategic analysis, coaching) stay on Opus 4.6
- Model selection per worker type: `claude --model sonnet --disable-slash-commands --prompt "/worker T-XXX"`

With 4-6 parallel workers, using Sonnet 4.6 for straightforward tasks significantly reduces overall cost while maintaining quality where it matters.

**Deferred Schema Loading:**
Faster session startup. Workers spawn and start executing faster - less idle time between task assignment and first tool call.

---

### :sparkles: v2.1.33 - February 6, 2026

**What Changed**: `TeammateIdle` and `TaskCompleted` hook events. Tmux messaging for agent teammates. Memory frontmatter for agents. `Task(agent_type)` restrictions.

**AEGIS Impact**:
**TeammateIdle and TaskCompleted Hooks:**
These hooks fire during agent coordination. While AEGIS uses its own worker pattern (not Agent Teams), these hooks have potential:
- `TaskCompleted` could be adapted to fire when an AEGIS worker finishes its task - trigger downstream workflows like notification via ntfy or auto-assign the next task
- `TeammateIdle` - if AEGIS experiments with Agent Teams for research tasks, this hook enables automatic task assignment when a teammate finishes

**Memory Frontmatter for Agents:**
Agent definitions can declare a `memory` field. AEGIS worker agents could specify what persistent memory to load at startup - project conventions, common patterns, frequently needed context - reducing the priming overhead in each worker's initial context.

**Tmux Messaging:**
Foundation for inter-agent communication. If AEGIS evaluates Agent Teams as a complement to the Alacritty worker pattern, tmux messaging enables coordination between team members. Not immediately useful for the current architecture but worth watching.

---

### :sparkles: v2.1.30 - February 3, 2026

**What Changed**: PDF page ranges via `pages` parameter. `/debug` command. 68% session resume memory optimization. Task tool metrics.

**AEGIS Impact**:
**PDF Page Ranges:**
AEGIS processes Bullin Construction documents - contracts, specs, reports. Page-range reading means:
- Extract specific sections from long contracts without loading the entire document
- Reference specific pages in task specs
- Reduce context usage by only loading relevant pages

```
Read("contract.pdf", pages: "12-15")  # Just the scope section
```

**/debug Command:**
Session-level troubleshooting for when AEGIS operations behave unexpectedly. Diagnose:
- MCP server issues affecting Neon connectivity
- Hook configuration problems blocking worker auto-approval
- Plugin or skill loading failures

**68% Session Resume Optimization:**
Resuming the main AEGIS session (or recovering from a crash) uses 68% less memory. The main session often has extensive conversation history from a full day of operations - this makes resume significantly faster and more reliable.

**Task Tool Metrics:**
Track token count and duration per task. Useful for understanding worker cost - which task types consume the most tokens? Which commands are most expensive? Data for optimizing the worker cost model.

---

### :sparkles: v2.1.27 - January 30, 2026

**What Changed**: `--from-pr` flag, debug logging for tool failures/denials.

**AEGIS Impact**:
**Debug Logging for Tool Failures:**
When a worker's operation fails unexpectedly (Neon query fails, file not found, permission denied), tool failures now appear in debug logs. Critical for diagnosing issues in parallel worker execution where failures can be hard to trace.

**PR-Linked Sessions:**
Not directly relevant to AEGIS daily operations, but useful for development work ON AEGIS itself.

---

### :sparkles: v2.1.21 - January 28, 2026

**What Changed**: Session resume during interrupted tool execution. File tools preferred over bash.

**AEGIS Impact**:
**Session Resume Improvements:**
If the main AEGIS session is interrupted during a Neon query or file operation (network hiccup, terminal crash), resuming now works properly. Critical for maintaining `state.json` consistency - an interrupted `/done` command could leave state inconsistent.

**File Tools Preference:**
Claude prefers native tools (Read, Write, Edit) over bash equivalents. Workers won't use `cat` when `Read` is more appropriate - cleaner operations and better permission tracking.

---

### :sparkles: v2.1.20 - January 27, 2026

**What Changed**: `--add-dir` for loading CLAUDE.md from arbitrary directories. Requires `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`.

**AEGIS Impact**:
Potential enhancement for worker spawning. Currently workers use `--disable-slash-commands` in the AEGIS working directory. With `--add-dir`, workers could:

1. Load shared instructions from a central location
2. Layer worker-specific context on top of base AEGIS instructions
3. Share command definitions across multiple AEGIS instances

```bash
# Potential enhanced worker spawn:
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
claude --add-dir ~/agents/aegis/shared/ --disable-slash-commands --prompt "/worker T-XXX"
```

**Note**: Feature requires env var and is currently undocumented.

---

### :sparkles: v2.1.16 - January 22, 2026

**What Changed**: Native task system with dependency tracking.

**AEGIS Impact**:
AEGIS already has its own task system in Neon (tasks table, atomic claiming, dependency tracking). The native Claude Code task system is session-scoped and doesn't persist to database.

**Where it could help:**
- Within a single worker session, break complex tasks into subtasks with dependencies
- Track multi-step deliverables within a session
- Visualize progress on long-running worker operations

**Limitation:** Tasks don't persist across sessions, so this complements but doesn't replace the Neon task system. AEGIS workers need cross-session persistence that only Neon provides.

---

### :sparkles: v2.1.14 - January 20, 2026

**What Changed**: Memory leak fixes for parallel subagents. Context window fix (65% -> 98%).

**AEGIS Impact**:
**Memory Leak Fixes:**
Critical for parallel workers. Memory leaks in long-running sessions degraded performance over time. With 4-6 workers running simultaneously, accumulated leaks could slow the entire system.

**Context Window Fix:**
The context window was only 65% utilized before blocking. Now 98%. For AEGIS:
- Before: ~130k usable context
- After: ~196k usable context

Workers handling complex tasks (long documents, rich context from Neon) benefit significantly from the extra 50% usable context.

---

### :sparkles: v2.1.10 - January 17, 2026

**What Changed**: New "Setup" hook event.

**AEGIS Impact**:
A lifecycle hook that fires during repository/project setup. For AEGIS:

1. **Worker initialization** - Setup hook could auto-configure worker environment on first spawn
2. **Database connection validation** - Verify Neon connectivity before operations begin
3. **State validation** - Check `state.json` consistency at startup

This complements the existing `/startup` command with a hook-based initialization that runs before any user interaction.

---

### :sparkles: v2.1.0 - January 9, 2026

**What Changed**: Skill hot-reload. `context: fork` for skills. Vim motions. Unified Ctrl+B.

**AEGIS Impact**:
**Skill Hot-Reload:**
Edit an AEGIS command, it's immediately available. No restart needed. Critical for iterating on the 30+ commands during development. Change `/comms/draft`, test it instantly.

**context: fork:**
Skills can spawn sub-agents in a forked context. For AEGIS:
- Research commands can fork context to explore deeply without filling up the main session
- `/coach/debrief` could fork to analyze patterns without polluting the main conversation
- Experimental drafts can be generated in a fork and discarded if bad

**Unified Ctrl+B:**
Both bash commands and agents can be backgrounded. Useful when a Neon query takes time - background it and continue working.

---

### :sparkles: v2.0.67 - December 12, 2025

**What Changed**: Prompt suggestions (Tab). Extended thinking ON by default for Opus 4.5.

**AEGIS Impact**:
**Extended thinking by default** means all AEGIS operations automatically get deeper reasoning. Complex tasks like `/comms/draft` (which needs to match Richard's voice, consider relationship context, and respect buffer timing) benefit from more thorough reasoning without manual configuration.

---

### :sparkles: v2.0.65 - December 11, 2025

**What Changed**: Model switching (Alt+P). Context window indicator in status line.

**AEGIS Impact**:
**Context window indicator** - Critical for long AEGIS sessions. When the main session approaches the 200k limit after loading strategic context, people profiles, and state, you can SEE when compaction will kick in. Helps decide when to start a fresh session vs continue.

**Model switching** - Drop to Haiku for simple status checks, back to Opus for complex drafting. Cost optimization across AEGIS operations.

---

### :sparkles: v2.0.60 - December 6, 2025

**What Changed**: Background agent support. `/mcp enable/disable` toggles.

**AEGIS Impact**:
Background agents mean AEGIS could dispatch research tasks without blocking:
- Background agent queries Neon for trend analysis while main session continues
- Multiple background tasks run in parallel for throughput
- Potential complement to the worker spawning pattern (lighter-weight than full terminal workers)

**MCP toggles** let you disable MCP servers temporarily for debugging without editing config files.

---

### :sparkles: v2.0.51 - November 24, 2025

**What Changed**: Opus 4.5 released. Claude Code Desktop launched.

**AEGIS Impact**:
**Opus 4.5** improves every AEGIS operation:
- Better reasoning for complex drafting (`/comms/draft` in Richard's voice)
- 50% token reduction means longer sessions before compaction
- Stronger agentic capabilities for workers executing multi-step tasks
- Most robust against prompt injection (important when processing external email content)

**Desktop app** - AEGIS uses CLI + Alacritty terminals. Desktop app isn't part of the architecture but could be evaluated for session management.

---

### :sparkles: v2.0.43 - November 18, 2025

**What Changed**: `permissionMode` for agents. `SubagentStart` hook. `skills` frontmatter.

**AEGIS Impact**:
**permissionMode per agent:**
Workers could declare their own permission level in their spawn configuration. Production workers might be auto-approve (trusted), while experimental workers could be plan-mode (cautious).

**SubagentStart hook:**
Intercept when workers spawn. Use cases:
- Log worker activation to Neon for audit trail
- Validate task assignment before worker starts
- Inject initial context from Neon before execution begins

---

### :sparkles: v2.0.42 - November 17, 2025

**What Changed**: Plan subagent. Agent resume. Model selection for subagents.

**AEGIS Impact**:
**Model selection for subagents** - Workers could use Haiku for simple file operations, Opus for complex drafting. Cost optimization across 4-6 parallel workers.

**Agent resume** - If a worker needs more context mid-task, resume it with additional information rather than restarting. Preserves work already done.

---

## :wrench: Medium - Quality of Life

### :wrench: v2.1.47 - February 18, 2026

**What Changed**: SessionStart hook deferred (~500ms faster startup). Memory optimization for long sessions. File mention pre-warming and caching.

**AEGIS Impact**:
**Faster Startup:** Worker sessions start ~500ms faster due to deferred SessionStart hook execution. With 4-6 workers spawning, this adds up to 2-3 seconds saved across all workers.

**Memory Optimization:** Long-running AEGIS sessions (main session can run all day) benefit from more aggressive buffer release and agent cleanup. Prevents gradual degradation over hours of continuous operation.

---

### :wrench: v2.1.42 - February 13, 2026

**What Changed**: `/rename` auto-generation. @-mention anchor fragments. Auth CLI subcommands.

**AEGIS Impact**:
**@-Mention Anchor Fragments:** Reference specific sections of files with `@README.md#installation`. For AEGIS context loading, this enables more precise priming:
- `@STRATEGIC_CONTEXT.md#current-priorities` - Load just the priorities section
- `@people/mike.md#communication-style` - Load just Mike's communication preferences
- Reduces context token usage by loading exactly what a command needs

---

### :wrench: v2.1.39 - February 11, 2026

**What Changed**: Guard against nested Claude Code sessions. Agent Teams model fix. MCP image crash fix.

**AEGIS Impact**:
**Nested Session Guard:** Prevents accidentally launching Claude Code inside a worker session. If a worker's task content includes a shell command that would spawn another Claude session, this guard catches it. Prevents runaway recursive worker spawning - a critical safety feature for autonomous worker execution.

---

### :wrench: v2.1.36 - February 7, 2026

**What Changed**: Fast mode (`/fast`) for Opus 4.6.

**AEGIS Impact**:
Same Opus 4.6 model with faster output. The main AEGIS session can toggle fast mode for quick operations (`/status`, `/next`) then switch back to normal for complex work (`/comms/draft`). Workers doing straightforward tasks could default to fast mode for better throughput.

---

### :wrench: v2.1.23 - January 29, 2026

**What Changed**: Custom spinner verbs, mTLS/proxy fixes, ripgrep error reporting, terminal rendering optimization.

**AEGIS Impact**:
**Terminal rendering performance** - With 4-6 worker terminals open simultaneously, rendering optimizations keep everything responsive.

**Ripgrep error reporting** - Search timeouts no longer silently return empty results. When a worker searches the codebase and hits a timeout, it reports an error instead of appearing to find nothing.

---

### :wrench: v2.1.19 - January 23, 2026

**What Changed**: $0/$1 argument shorthand. VSCode session forking. Skills auto-allow.

**AEGIS Impact**:
**Skills Auto-Allow:** Commands that don't require extra permissions execute without prompting. Reduces friction in the daily loop - `/status` and `/next` just run.

**Argument Shorthand:** Cleaner command definitions using `$0`, `$1` instead of verbose `$ARGUMENTS[0]`.

---

### :wrench: v2.1.18 - January 23, 2026

**What Changed**: `/keybindings` command. Chord sequences. Per-context keybindings.

**AEGIS Impact**:
**Chord sequences** (multi-key combos like `Ctrl+K Ctrl+C`) provide more binding options without conflicts with Hyprland/Alacritty keybindings. Useful when running multiple AEGIS terminals.

---

### :wrench: v2.1.7 - January 14, 2026

**What Changed**: Customizable keybindings.json. `showTurnDuration`. MCP auto mode.

**AEGIS Impact**:
Custom keybindings let you avoid conflicts between Claude Code shortcuts and Hyprland/Alacritty bindings across all AEGIS terminals. The keybindings file is user-level (`~/.claude/`), so all workers inherit the same configuration.

---

### :wrench: v2.0.74 - December 19, 2025

**What Changed**: LSP tool. `/terminal-setup` supports Alacritty.

**AEGIS Impact**:
**Alacritty terminal setup** - Official configuration support for the terminal AEGIS runs in. Run `/terminal-setup` for optimal rendering.

**LSP tool** - Better code navigation when working on AEGIS's TypeScript operations (Drizzle schema, Bun executor).

---

### :wrench: v2.0.72 - December 18, 2025

**What Changed**: Claude in Chrome (Beta).

**AEGIS Impact**:
Browser control could enable new AEGIS capabilities:
- Auto-check Bullin web dashboards
- Research competitors in authenticated browser sessions
- Navigate internal tools for data extraction

Currently AEGIS is CLI-only. Chrome integration is a potential expansion path for web-based work tasks.

---

### :wrench: v2.0.62 - December 9, 2025

**What Changed**: Fixed symlinked skill directories. "(Recommended)" indicator.

**AEGIS Impact**:
If AEGIS uses symlinks for shared command directories, this fix ensures they load correctly.

---

### :wrench: v2.0.59 - December 4, 2025

**What Changed**: `--agent` flag for custom agent personas.

**AEGIS Impact**:
The `--agent` flag provides custom system prompts and tool restrictions. For AEGIS:
- Workers could use `--agent worker` for a focused worker persona
- Read-only review agents could inspect deliverables
- **Limitation**: `--agent` ignores CLAUDE.md, so workers using it wouldn't get AEGIS rules

**Decision**: AEGIS workers use `--disable-slash-commands` + working directory CLAUDE.md instead of `--agent`. The rules system is too critical to lose.

---

### :wrench: v2.0.70 - December 16, 2025

**What Changed**: Wildcard MCP permissions.

**AEGIS Impact**:
If AEGIS adds MCP servers (e.g., a Neon MCP server), wildcard permissions reduce friction:
```
mcp:neon:*              # Allow all Neon operations
mcp:neon:read*          # Allow reads, prompt for writes
```

Currently AEGIS accesses Neon via `bun app/db/exec.ts`, not MCP. But if migrated to MCP, wildcards would be essential.

---

### :wrench: v2.0.54 - November 26, 2025

**What Changed**: Hooks can process PermissionRequest suggestions. `Ctrl+N` shortcut.

**AEGIS Impact**:
Builds on the PermissionRequest hook. Hooks can now modify permission suggestions themselves, not just approve/deny. More granular control over worker auto-approval.

`Ctrl+N` for new conversation speeds up session management.

---

### :wrench: v2.0.52 - November 25, 2025

**What Changed**: Linux Wayland image paste. Bash `$!` variable.

**AEGIS Impact**:
Wayland image paste works correctly in Hyprland. Useful for pasting screenshots of Bullin documents into AEGIS sessions.

---

### :wrench: v2.0.41 - November 14, 2025

**What Changed**: Plugin output styles. SDK hook timeouts.

**AEGIS Impact**:
**SDK hook timeouts** - If AEGIS hooks (worker auto-approval) have a custom timeout configured, this ensures they don't hang indefinitely.

---

### :wrench: v2.0.37 - November 11, 2025

**What Changed**: Notification hook matchers.

**AEGIS Impact**:
Notification hooks can match on specific notification types. Could be used for ntfy integration - route urgent AEGIS alerts based on notification content.

---

### :wrench: v2.0.73 - December 19, 2025

**What Changed**: Clickable images. `Alt-Y` kill ring.

**AEGIS Impact**:
Kill ring (`Alt-Y`) - Access earlier clipboard entries when working across multiple AEGIS terminals. Useful for copying between sessions.

---

### :wrench: v2.0.34 - November 6, 2025

**What Changed**: Native Rust fuzzy finder.

**AEGIS Impact**:
Faster file suggestions in the AEGIS codebase. 30+ commands, multiple diagram directories, architecture docs - better fuzzy matching helps navigation.

---

### :wrench: v2.0.32 - November 4, 2025

**What Changed**: Output styles un-deprecated.

**AEGIS Impact**:
Output styles confirmed as stable feature. If AEGIS adds custom output formatting for different command types (coaching voice vs professional voice), this is supported.

---

### :wrench: v2.0.31 - November 1, 2025

**What Changed**: Tool name collision fix with subagents + MCP.

**AEGIS Impact**:
Stability fix preventing tool name collisions when workers use MCP alongside built-in tools.

---

## Skip List (Not Relevant)

| Version | Date | Reason |
|---------|------|--------|
| v2.1.46 | Feb 17 | claude.ai MCP connectors, macOS orphaned process fix - not my platform |
| v2.1.38 | Feb 10 | Tab autocomplete, heredoc security, sandbox fixes - bug fixes only |
| v2.1.37 | Feb 9 | Fast mode fix after /extra-usage - bug fix only |
| v2.1.34 | Feb 6 | Agent teams render crash, sandbox bypass - bug fixes only |
| v2.1.31 | Feb 4 | Session resume hint, PDF fix, plan mode crash - minor QoL |
| v2.1.25 | Jan 29 | Beta header validation - Bedrock/Vertex only |
| v2.1.22 | Jan 28 | Structured outputs in -p mode - not using non-interactive |
| v2.1.17 | Jan 22 | AVX crash fix - hardware-specific |
| v2.1.15 | Jan 21 | npm deprecation, React perf - infrastructure |
| v2.1.12 | Jan 17 | Message rendering bug - minor |
| v2.1.11 | Jan 17 | MCP HTTP/SSE fix - not using HTTP transport |
| v2.1.5 | Jan 12 | TMPDIR env var - minor |
| v2.1.4 | Jan 10 | Background tasks env var - minor |
| v2.1.2 | Jan 9 | Security fix, iTerm hyperlinks, winget - not my platforms |
| v2.0.76 | Dec 22 | No prompt changes - infrastructure |
| v2.0.75 | Dec 20 | Prompt token cleanup - internal |
| v2.0.71 | Dec 16 | Prompt suggestion toggle, glob permission fix - minor |
| v2.0.68 | Dec 12 | CJK/IME fix, enterprise settings - not my use case |
| v2.0.66 | Dec 11 | Hotfix - no details |
| v2.0.63 | Dec 9 | Hotfix - no details |
| v2.0.61 | Dec 7 | VSCode multi-terminal revert - I use Alacritty |
| v2.0.58 | Dec 3 | Pro tier Opus access - I have Max |
| v2.0.57 | Dec 3 | Plan rejection feedback, VSCode streaming - minor |
| v2.0.56 | Dec 2 | Progress bar toggle, VSCode sidebar - minor |
| v2.0.55 | Nov 27 | Proxy DNS fix - corporate network issue |
| v2.0.53 | Nov 25 | Hotfix - no details |
| v2.0.50 | Nov 21 | MCP nested refs fix - minor |
| v2.0.49 | Nov 21 | Ctrl+Y paste, usage limit clarity - minor |
| v2.0.47 | Nov 20 | Teleport errors, Vertex config - not my setup |
| v2.0.46 | Nov 20 | Image media type fix - minor |
| v2.0.36 | Nov 8 | Autoupdater fix - bug fix only |
| v2.0.35 | Nov 7 | VSCode font settings - I use Alacritty |
| v2.0.33 | Nov 5 | Native binary launch speed - minor |
| v2.0.69 | Dec 13 | Minor bugfixes - no details |

---

## Summary: What AEGIS Needs to Watch

**CRITICAL features in use:**
1. **`.claude/rules/`** (v2.0.64) - FOUNDATION: All behavior rules, people profiles, coaching triggers
2. **PermissionRequest hook** (v2.0.45) - FOUNDATION: Worker auto-approval system
3. **Unified commands/skills** (v2.1.3) - All 30+ commands are skills
4. **Nested command discovery** (v2.1.6) - Organized command structure
5. **PreToolUse additionalContext** (v2.1.9) - Context injection before tool calls
6. **ConfigChange hook** (v2.1.49) - Monitor `.claude/rules/` modifications in real-time
7. **Opus 4.6 adaptive thinking** (v2.1.32) - Automatic reasoning depth across all operations

**HIGH features enhancing workflow:**
- Skill hot-reload (v2.1.0) - Instant command iteration
- Context:fork (v2.1.0) - Research without context pollution
- Context window 98% (v2.1.14) - Full window for rich context sessions
- Memory leak fixes (v2.1.14, v2.1.50) - Stable parallel workers
- Session resume (v2.1.21) - Recover interrupted operations
- 68% resume optimization (v2.1.30) - Faster session recovery
- Extended thinking default (v2.0.67) → Adaptive thinking (v2.1.32)
- Named sessions (v2.0.64) - Persistent work state
- Background agents (v2.0.60) - Async operations
- 1M context window (v2.1.32, v2.1.50) - Massive context for rich AEGIS sessions
- Sonnet 4.6 (v2.1.45) - Cost-optimized model for simple worker tasks
- PDF page ranges (v2.1.30) - Targeted document extraction

**Architecture decisions:**
- Workers use `--disable-slash-commands` + working directory (NOT `--agent`)
- Rules system (`.claude/rules/`) is the behavior layer (not CLAUDE.md only)
- Neon database is source of truth (not Claude Code's task system or auto memory)
- Hooks enable worker autonomy (PermissionRequest auto-approval)
- Commands ARE skills (unified model since v2.1.3)
- Opus 4.6 for complex work, Sonnet 4.6 potential for simple workers

**Potential enhancements to evaluate:**
- `--worktree` for file-heavy worker isolation (v2.1.49) - alternative to shared directory workers
- PreToolUse hooks for Neon context injection (v2.1.9)
- `--add-dir` for worker instruction layering (v2.1.20)
- Setup hook for worker initialization (v2.1.10)
- ConfigChange hook for rules monitoring (v2.1.49)
- Agent Teams for research-class tasks (v2.1.32) - complement to Alacritty workers
- Auto memory impact on Neon state management (v2.1.32)
- Native task system within worker sessions (v2.1.16)
- TeammateIdle/TaskCompleted hooks for coordination (v2.1.33)
- Worker memory frontmatter for context priming (v2.1.33)
- Chrome automation for web-based work tasks (v2.0.72)
- context:fork for research commands (v2.1.0)
- Fast mode for throughput-oriented workers (v2.1.36)
- @-mention anchors for precise context loading (v2.1.42)

---

*Last updated: 2026-02-21 (February releases completed)*
*Filter criteria: [context.md](context.md)*
