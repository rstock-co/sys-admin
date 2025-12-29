# Async Agent Execution

**Feature introduced in:** v2.0.64 (December 10, 2025)
**Foundation laid in:** v2.0.60 (December 6, 2025)

Async execution allows you to background running subagents or bash commands within a Claude Code session, continuing work while they complete independently.

**Core value:** Interactive parallelism—continue YOUR work while Claude does something else. This is about respecting your time during active sessions, not about automation or overnight processing.

---

## How It Works

When a sub-agent or long-running bash command is executing, press **Ctrl+B** to send it to the background. The task continues running independently while you resume working with the main agent.

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE SESSION                       │
│                                                              │
│   Main Agent (foreground)                                    │
│   ├── You continue conversing here                          │
│   │                                                          │
│   Background Tasks                                           │
│   ├── [research-agent] Searching Stripe API docs...         │
│   ├── [npm install] Installing dependencies...              │
│   └── [explore-agent] Analyzing codebase structure...       │
│                                                              │
│   Background tasks send wake-up messages when done          │
└─────────────────────────────────────────────────────────────┘
```

### Key Mechanics

1. **Ctrl+B** - Sends currently running task to background
2. **Wake-up messages** - Background tasks notify main agent when complete (no polling)
3. **Managed by Claude** - Unlike separate terminal sessions, Claude coordinates these internally
4. **Unified results** - Background task output integrates into the conversation

---

## Monitoring Background Tasks

Use `/tasks` to check status of all running background processes:

```
/tasks

Active Tasks:
┌──────────────────────────────────────────────────────────┐
│ ID: task_abc123                                          │
│ Type: Agent (research)                                   │
│ Status: Running                                          │
│ Tokens: 12,450 / 200,000                                │
│ Started: 2 minutes ago                                   │
└──────────────────────────────────────────────────────────┘
```

From `/tasks` you can:
- View token usage per task
- See progress updates
- Resume or cancel tasks

---

## What to Background vs Keep Foreground

### Good for Backgrounding

| Task Type | Why |
|-----------|-----|
| Research / web searches | Independent, no user input needed |
| Large codebase analysis | Time-consuming, results needed later |
| Documentation generation | Can run while you work on code |
| Security audits | Thorough scans take time |
| Performance profiling | Analysis runs independently |
| Long builds (`npm install`, `docker build`) | Just waiting for completion |
| Parallel exploration | Multiple agents searching different areas |

### Keep in Foreground

| Task Type | Why |
|-----------|-----|
| Tasks needing immediate input | Can't provide input to background task |
| File modifications requiring review | You want to approve changes as they happen |
| Sequential dependencies | Next step depends on this result |
| Short tasks | Overhead of backgrounding not worth it |
| Critical path work | You need the result before proceeding |

---

## Practical Examples

### Example 1: Research While Coding

```
User: I need to integrate Stripe. Research their API while I set up the database models.

Claude: I'll spawn a research agent to investigate the Stripe API.
[Spawns research subagent]

User: [Presses Ctrl+B]

Claude: Research agent backgrounded. Let's work on your database models.
What schema are you thinking?

User: [Continues database discussion...]

[5 minutes later]

Claude: The research agent completed. Key findings:
- Stripe uses idempotency keys for safe retries
- Webhook signatures require STRIPE_WEBHOOK_SECRET
- Payment Intents API is recommended over Charges
[Full research integrated into conversation]
```

### Example 2: Parallel Codebase Exploration

```
User: I need to understand how auth works in this codebase, and also
find all the API endpoints.

Claude: I'll spawn two explore agents in parallel.
[Spawns auth exploration agent]
[Spawns API endpoints agent]

User: [Presses Ctrl+B on first]
User: [Presses Ctrl+B on second]

Claude: Both agents running in background. What else can I help with
while they work?

[Later, results from both integrate into conversation]
```

### Example 3: Build While Discussing

```
User: Run npm install while we discuss the architecture.

Claude: Starting npm install...
[npm install begins]

User: [Presses Ctrl+B]

Claude: npm install running in background.
Now, about the architecture—what patterns are you considering?

[Conversation continues, build completes in background]
```

---

## Critical Distinction: Async Execution vs SGTAs

This is important for Symbiont architecture:

| Aspect | Async Execution (Ctrl+B) | SGTAs (Specialists) |
|--------|--------------------------|---------------------|
| **What it is** | Background a *subagent* within one session | Separate full Claude Code sessions |
| **Context window** | Subagent gets truncated context | Full 200k each |
| **Who manages** | Claude coordinates internally | You coordinate via Hyprland hotkeys |
| **Communication** | Wake-up messages to main agent | Queens Ledger / PostgreSQL |
| **Identity** | Defined by Task tool prompt | Defined by folder's CLAUDE.md + output-style.md |
| **Persistence** | Dies when parent session ends | Independent lifecycle |
| **Spawning** | `Task` tool within session | `alacritty --working-directory` + hotkey |

### What This Means

**Your specialists (health-coach, business-savant, etc.) are NOT subagents.**

They're independent Claude Code instances spawned via:
```bash
bind = $mainMod SHIFT, 1, exec, ~/symbiont/spawn-mycelium.sh health-coach
```

Each specialist:
- Has its own terminal
- Has its own full 200k context
- Has its own CLAUDE.md defining persona
- Has its own output-style.md defining voice
- Persists independently of other sessions

**Async execution doesn't change how specialists work.** It's a feature for managing subtasks *within* a single session.

---

## Where Async IS Relevant for Symbiont

### 1. Within Mycelia (Orchestrator)

While orchestrating, Mycelia could background research:

```
User: Check the latest on sleep optimization research while we
discuss the weekly review format.

Mycelia: [Spawns research agent, user backgrounds it]
Let's discuss the review format. Currently I'm thinking...

[Research completes, Mycelia integrates findings]
```

### 2. Within Any Specialist

A specialist could background a long-running analysis:

```
[In health-coach session]

User: Analyze my last 6 months of bloodwork for trends while
we discuss today's protocol.

Health-coach: [Spawns analysis agent, user backgrounds it]
For today's protocol, let's focus on...

[Analysis completes with trend insights]
```

### 3. Overnight Daemon (Clarification)

**Ctrl+B async is NOT directly relevant for overnight daemon.** Here's why:

Ctrl+B is an **interactive** feature—you press it to continue working while something runs. If you're sleeping, you're not pressing anything.

#### What Overnight Daemon Would Actually Use

**Option A: Single headless session, sequential tasks**
```bash
# Cron at 2am
claude --headless -p "Run overnight tasks:
1. Pattern detection - write to PostgreSQL
2. Generate morning briefing - write to PostgreSQL
3. Opportunity scan - write to PostgreSQL"
```
Simple. Tasks run in order. You're asleep anyway—who cares if it takes 20 min or 2 hours?

**Option B: Multiple separate headless instances**
```bash
# Cron at 2am - parallel via separate processes
claude --headless -p "Pattern detection..." &
claude --headless -p "Morning briefing..." &
claude --headless -p "Opportunity scan..." &
wait
```
Parallelism via separate processes. No Ctrl+B needed.

**Option C: Claude-initiated background (different from Ctrl+B)**
```bash
claude --headless -p "Run these tasks in parallel, write results to PostgreSQL..."
```
Claude *itself* might use `run_in_background: true` internally via the Task tool. This is Claude deciding to parallelize, not you pressing Ctrl+B.

#### When Parallelism Matters Overnight

| Reason | Validity |
|--------|----------|
| Time constraint (finish before 6am) | ✅ Valid if tasks are slow |
| Failure isolation (one fails, others continue) | ✅ Valid |
| You're sleeping anyway | ❌ Sequential is fine |
| Token efficiency | 🤔 Debatable |

**Bottom line:** Overnight daemon benefits from **headless mode**, not specifically from Ctrl+B async. The parallelism decision is about time constraints and failure isolation, not interactive workflow.

---

## Technical Details

### Wake-up Messages

Background tasks don't require polling. When a background agent or bash command completes, it sends a wake-up message to the main agent. This notification appears in your session:

```
[Background task completed: research-agent]
Results available. Would you like me to summarize?
```

### Token Accounting

Background tasks consume tokens from your session's allocation:
- Each background agent has its own token counter
- Use `/tasks` to monitor per-task usage
- Heavy backgrounding can accelerate context limits

### Unified TaskOutputTool

v2.0.64 unified the previously separate `AgentOutputTool` and `BashOutputTool` into a single `TaskOutputTool`. This means consistent handling whether you're getting output from a background agent or a background bash command.

---

## Limitations

1. **No input to background tasks** - Once backgrounded, you can't provide additional input to that task
2. **Subagent context is truncated** - Background agents don't get full 200k, they get summarized context
3. **Session-scoped** - Background tasks die when the parent session ends
4. **No cross-session coordination** - Background agents in one session can't communicate with other sessions (use PostgreSQL/Queens Ledger for that)

---

## Comparison: Backgrounding Options

| Method | Use Case | Context | Coordination |
|--------|----------|---------|--------------|
| **Ctrl+B async** | Subtasks within a session | Truncated | Claude internal |
| **Separate terminals** | Independent specialists | Full 200k each | Queens Ledger / PostgreSQL |
| **`&` bash suffix** | Shell commands only | N/A | None |
| **Headless mode** | Automation / daemon | Full | External orchestration |

---

## Relevance Summary

| Symbiont Component | Async Relevance | Notes |
|--------------------|-----------------|-------|
| **Specialist identity/spawning** | ❌ Not relevant | Specialists are full sessions, not subagents |
| **Work within Mycelia** | ✅ Useful | Background research while orchestrating |
| **Work within specialists** | ✅ Useful | Background analysis while conversing |
| **Overnight daemon** | ❌ Not Ctrl+B | Use headless mode + separate instances instead |
| **Dual Sovereignty** | 🤔 Maybe | Could background sovereign consultations, but they're quick |

### The Core Value of Ctrl+B Async

**Interactive parallelism**: Continue YOUR work while Claude does something else.

This is valuable when you're actively working and don't want to wait. It's not about automation or overnight processing—it's about respecting your time during interactive sessions.

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| **Ctrl+B** | Background currently running task |
| `/tasks` | List all background tasks with status |
| `/tasks cancel <id>` | Cancel a background task |

---

*Last updated: 2025-12-29*
