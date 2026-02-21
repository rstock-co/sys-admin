# Claude Code Tracker Context

**Why Claude Code updates matter to me, and how to evaluate relevance.**

Read this FIRST before scanning updates or answering questions about releases.

---

## What I'm Building: AEGIS

AEGIS is a work automation system that fully automates my job at Bullin Construction. Claude Code IS the runtime - not a coding assistant, but the execution engine for all work: research, analysis, drafting, communications, deliveries.

### Core Philosophy

AEGIS does the job. I collect the paycheck and supervise. The system handles all Bullin work so I can focus on building my own ventures.

### The Four-Layer Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     1. BRAIN - Claude Code                   │
│                                                              │
│   - Runs on my machine (subscription, not API-billed)        │
│   - Executes 30+ slash commands                              │
│   - Generates communications in my voice                     │
│   - Spawns parallel worker agents in Alacritty terminals     │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  2. STATE     │  │ 3. ORCHESTR  │  │ 4. INTERFACE │
    │  Neon DB      │  │  n8n (VPS)   │  │  CLI + Cmds  │
    │              │  │              │  │              │
    │  20+ tables  │  │  Email IMAP  │  │  /startup    │
    │  Drizzle ORM │  │  SMS relay   │  │  /next       │
    │  56 ops      │  │  Scheduled   │  │  /done       │
    └──────────────┘  └──────────────┘  └──────────────┘
```

### Why This Matters for Updates

AEGIS depends on Claude Code primitives at every layer:
1. **Slash commands** are the entire user interface (30+ commands)
2. **Rules** (`.claude/rules/`) define behavior, people profiles, coaching triggers
3. **Hooks** enable autonomous workers (permission auto-approval)
4. **Terminal spawning** powers parallel workers in Alacritty
5. **Session state** persists via `state.json` across sessions
6. **Context loading** (@mentions, fragments) primes each command
7. **Git integration** creates audit trail commits per command

When Claude Code changes how commands work, how rules load, how hooks fire, or how sessions persist - it directly affects every AEGIS operation.

---

## The Worker System

### How Workers Are Spawned

```bash
# From /worker command - spawns isolated worker in new terminal
alacritty --working-directory /home/neo/agents/aegis \
  -e claude --disable-slash-commands --prompt "/worker T-XXX"
```

**What happens**:
1. New Alacritty terminal opens at AEGIS working directory
2. `--disable-slash-commands` prevents task content from triggering commands
3. `--prompt "/worker T-XXX"` immediately starts the worker on a task
4. Worker claims task atomically from Neon (prevents race conditions)
5. Worker executes independently with hook-based auto-approval
6. 4-6 workers run in parallel for throughput

### Three-Phase Worker Lifecycle

1. **Phase 1 (Automated Setup):** Claim task from Neon, validate inputs, discover context
2. **Phase 2 (Collaborative Work):** Richard + worker iterate on deliverable
3. **Phase 3 (Automated Cleanup):** Validate completion, capture artifacts, commit, cleanup

### Why Worker Architecture Matters for Updates

When Claude Code changes:
- **`--disable-slash-commands`** → Affects worker isolation
- **`--prompt` flag behavior** → Affects worker startup
- **Hook execution** → Affects auto-approval in workers
- **Terminal spawning** → Affects parallel execution
- **Session management** → Affects worker persistence

---

## The Dual Timeline (Buffer System)

AEGIS maintains two parallel timelines:
- **REALITY** - When work is actually completed (fast, Claude-assisted)
- **THEATER** - When the outside world sees it delivered (paced, professional)

The gap between them is the **buffer** (target: 5+ days). This is how automation stays sustainable and never reveals superhuman speed.

Buffer health drives all decisions:
- **Healthy (5+):** Flexibility available
- **Yellow (3-5):** Commit cautiously
- **Red (1-2):** Full Bullin focus
- **Critical (<1):** Release immediately

---

## The Command System

### Daily Loop

```bash
/startup          # Morning briefing, buffer status, today's plan
/next             # Get next prioritized task
/done             # Complete task, commit, update state
/signoff          # End of day summary, handoff notes
```

### Communication Commands

```bash
/comms/draft      # Draft response in Richard's voice
/comms/approve    # Approve for scheduled delivery
/comms/log        # Log external communications
/comms/history    # View communication history with person
```

### All Commands Depend On

- **Slash command loading** from `.claude/commands/`
- **YAML frontmatter** parsing (description, metadata)
- **@mention context** loading (`@STRATEGIC_CONTEXT.md`, `@state.json`, `@people/*.md`)
- **Bun execution** via `bun app/db/exec.ts domain:verb --params`
- **Rules** from `.claude/rules/` shaping behavior

---

## The Rules System

```
.claude/rules/
├── aegis.md                 # Core AEGIS behavior rules
├── coaching-triggers.md     # When/how to coach Richard
├── commitment-detection.md  # Detect commitments in communications
├── context-loading.md       # How to load context efficiently
└── people/
    ├── mike.md              # Mike's profile, expectations, signals
    ├── lee.md               # Lee's profile
    └── bj.md                # BJ's profile
```

**When Claude Code changes rules loading** (`.claude/rules/` behavior, file discovery, priority), it affects every AEGIS operation because rules shape priority weights, drafting behavior, coaching content, and people interactions.

---

## Data Layer: Neon Database

All state lives in Neon (serverless Postgres), accessed via Drizzle ORM:

| Area | Tables | Purpose |
|------|--------|---------|
| Tasks | `tasks`, `task_artifacts` | Work orders with specs, artifacts |
| Comms | `inbox`, `outbox`, `drafts` | All communications |
| People | `people`, `expectations` | Profiles, signal tracking |
| Buffer | `buffer_items`, `deliveries` | Staged work, delivery timing |
| State | `daily_snapshots`, `journal` | Daily state, reflection |

**56 TypeScript operations** via `bun app/db/exec.ts domain:verb`:
```bash
bun app/db/exec.ts tasks:next          # Get next prioritized task
bun app/db/exec.ts comms:draft --to mike --subject "Update"
bun app/db/exec.ts buffer:status       # Buffer health check
```

---

## External Integrations

| System | Role | Connection |
|--------|------|------------|
| n8n (VPS) | Email IMAP fetch, SMS relay, scheduled sends | Webhooks to Neon |
| SMS Gateway | Android SMS inbound | Webhook → n8n → Neon |
| KDE Connect | SMS outbound | `kdeconnect-cli --send-sms` |
| ntfy | Push notifications for urgent items | Self-hosted Docker |
| IMAP/SMTP | Email ingest and delivery | Via n8n hourly |

---

## Feature Dependency Summary

### CRITICAL - Architecture Depends On These

| Claude Code Feature | AEGIS Dependency |
|---------------------|------------------|
| **Slash commands** | Entire UI - 30+ commands define all workflows |
| **`.claude/rules/`** | Behavior rules, people profiles, coaching triggers |
| **Hooks** | Worker auto-approval, autonomous execution |
| **`--disable-slash-commands`** | Worker isolation (prevents task content triggering commands) |
| **`--prompt` flag** | Worker immediate execution on spawn |
| **Session state** | `state.json` persistence across sessions |
| **Context loading (@mentions)** | Strategic context, people profiles, state priming |
| **Git integration** | Audit trail commits per command |

### HIGH - Significant Workflow Impact

| Claude Code Feature | AEGIS Dependency |
|---------------------|------------------|
| **Terminal spawning** | Parallel workers in Alacritty (4-6 concurrent) |
| **Context window / compacting** | Long sessions with rich context need full window |
| **Model selection** | Haiku for quick tasks, Opus for complex reasoning |
| **Background execution** | Potential for async worker coordination |
| **Task system** | Could enhance worker task tracking |
| **YAML frontmatter** | Command metadata parsing |

### MEDIUM - Quality of Life

| Claude Code Feature | Relevance |
|---------------------|-----------|
| **Terminal rendering** | Multiple parallel sessions in Alacritty |
| **Keyboard shortcuts** | Heavy terminal user |
| **File suggestions / @mentions** | Context priming speed |
| **PDF reading** | Document ingestion pipeline |
| **Session resume** | Recover interrupted work sessions |

### LOW - Note But Don't Prioritize

| Claude Code Feature | Why Low |
|---------------------|---------|
| **Windows/macOS fixes** | I use Arch Linux |
| **iTerm/Terminal.app** | I use Alacritty |
| **Bedrock/Vertex** | I use subscription billing |
| **VSCode extension** | CLI-first workflow |
| **Agent teams** | AEGIS uses worker spawning, not agent teams |

---

## My Environment

| Component | Choice |
|-----------|--------|
| OS | Arch Linux (rolling release) |
| Display | Wayland (Hyprland compositor) |
| Terminal | Alacritty |
| Shell | Zsh |
| GPU | Intel Arc B580 (xe driver) |
| Database | Neon (serverless Postgres) |
| ORM | Drizzle (TypeScript) |
| Runtime | Bun |
| Orchestration | n8n (self-hosted VPS) |

**Key pattern**: I run a main AEGIS session + 4-6 parallel worker sessions in separate Alacritty terminals, all hitting the same Neon database.

---

## How to Evaluate a Release

### Questions to Ask

1. **Does it touch slash commands?**
   → Affects the entire AEGIS command interface

2. **Does it touch `.claude/rules/` loading or behavior?**
   → Affects behavior rules, people profiles, coaching triggers

3. **Does it touch hooks?**
   → Affects worker auto-approval and autonomous execution

4. **Does it touch `--disable-slash-commands` or `--prompt`?**
   → Affects worker spawning and isolation

5. **Does it touch session state or resume?**
   → Affects `state.json` persistence and session recovery

6. **Does it touch context loading (@mentions, fragments)?**
   → Affects how commands prime with strategic context

7. **Does it touch terminal/parallel execution?**
   → Affects worker throughput

8. **Does it touch context window/compacting?**
   → Affects long AEGIS sessions with rich context

9. **Is it Linux/Wayland/Alacritty specific?**
   → Directly affects my environment

10. **Does it touch git integration?**
    → Affects audit trail commits

### Relevance Scoring

**CRITICAL**:
- Slash commands, rules, hooks, worker flags, session state, context loading
- Deep research immediately
- Document specific AEGIS impact

**HIGH**:
- Terminal spawning, context window, model selection, background execution, task system
- Note practical impact
- Consider testing

**MEDIUM**:
- Linux/Wayland/Alacritty fixes, keyboard shortcuts, terminal rendering, PDF reading
- Brief note

**LOW**:
- Windows/macOS, enterprise features, VSCode, Bedrock/Vertex
- Skip in relevance.md (keep in changelog.md)

---

## Example Relevance Analysis

### Good Analysis (Shows AEGIS Reasoning)

```markdown
## v2.X.XX - CRITICAL

**What Changed**: Skills from --add-dir directories now load properly

**AEGIS Impact**:
This affects the worker spawning pattern. Workers currently use
`--disable-slash-commands` to prevent task content from triggering
commands. If `--add-dir` skills loading changes, it could affect
how workers discover and execute shared commands.

Currently AEGIS loads all commands from `.claude/commands/` in the
working directory. With `--add-dir`, we could potentially share
command definitions across multiple AEGIS instances or load
additional context from separate directories.

**Action**: Test --add-dir with worker spawning to see if it affects
command isolation.
```

### Bad Analysis (Too Generic)

```markdown
## v2.X.XX - HIGH

**What Changed**: Skills from --add-dir directories now load properly

**Why Relevant**: I use slash commands.
```

The first analysis shows reasoning about HOW the change affects AEGIS's worker architecture. The second just states a fact.

---

## When to Create Deep Research

Create a file in `data/claude-code/research/` when:

1. **Change to commands/rules/hooks** that could affect AEGIS operations
   - New command loading behavior → could break daily loop
   - New hook event → could enhance worker automation
   - Rules loading change → could affect people profiles

2. **Major model release** (Opus 4.6, Sonnet 4.6)
   - Affects reasoning quality in worker execution

3. **Breaking change** to something AEGIS depends on
   - `--disable-slash-commands` behavior change
   - `--prompt` flag change
   - Session state handling change

4. **New primitive I could use for workers**
   - New parallelism features → could improve worker throughput
   - New context injection → could improve worker priming
   - New hook events → could improve worker lifecycle

5. **I explicitly ask** for deep research on a version

---

*Last updated: 2026-02-21*
