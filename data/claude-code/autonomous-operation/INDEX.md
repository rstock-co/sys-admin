# Autonomous Claude Code Operation

**Documentation for spawning and orchestrating autonomous Claude Code instances.**

---

## Quick Start

**Read this first:** [guide.md](guide.md)

The guide covers everything needed to spawn Claude Code instances programmatically from an orchestrating agent, with instruction handoff via hooks, using Max subscription billing.

---

## Documentation Structure

```
autonomous-operation/
├── INDEX.md          # You are here - start point for LLMs
├── guide.md          # MAIN GUIDE - read this first
└── research/         # Deep-dive reports on specific versions
    ├── 2-1-20.md     # --add-dir CLAUDE.md loading
    ├── 2-1-16.md     # Native task system
    ├── 2-1-10.md     # Setup hook event
    ├── 2-1-9.md      # PreToolUse additionalContext
    ├── 2-1-0.md      # context:fork for skills
    ├── 2-0-64.md     # Async agents, named sessions
    ├── 2-0-60.md     # --disable-slash-commands
    ├── 2-0-59.md     # --agent flag
    ├── 2-0-45.md     # PermissionRequest hook
    ├── 2-0-43.md     # SubagentStart hook, permissionMode
    └── 2-0-42.md     # --max-budget-usd (SDK)
```

---

## What You'll Learn

### From the Guide

| Section | What It Covers |
|---------|----------------|
| Authentication | How to use Max subscription instead of API billing |
| Known Issues | Critical 60-second latency bug in headless mode |
| CLI Flags | All flags for autonomous operation |
| Hook Events | SessionStart, Setup, Stop, SessionEnd, PreToolUse, PermissionRequest |
| Spawning Patterns | Three approaches with full code examples |
| Database Handoff | PostgreSQL schema and code for instruction injection |
| Completion Signaling | How child agents report back to parent |
| Permissions | Configuration for fully autonomous operation |

### From Research Reports

Each research report provides deep analysis of a specific Claude Code version's features relevant to autonomous operation. Read these after the guide for implementation details.

| Report | Key Feature | When to Read |
|--------|-------------|--------------|
| [2-1-20](research/2-1-20.md) | `--add-dir` CLAUDE.md loading | Layering instructions from multiple directories |
| [2-1-16](research/2-1-16.md) | Native task system | Agent coordination with dependency tracking |
| [2-1-10](research/2-1-10.md) | Setup hook | One-time initialization at spawn |
| [2-1-9](research/2-1-9.md) | PreToolUse additionalContext | Injecting context before tool calls |
| [2-1-0](research/2-1-0.md) | context:fork | Forked context for skill sub-agents |
| [2-0-64](research/2-0-64.md) | Async agents | Background execution, named sessions |
| [2-0-60](research/2-0-60.md) | `--disable-slash-commands` | Clean headless mode |
| [2-0-59](research/2-0-59.md) | `--agent` flag | Custom agent personas |
| [2-0-45](research/2-0-45.md) | PermissionRequest hook | Auto-approve without prompts |
| [2-0-43](research/2-0-43.md) | SubagentStart hook | Intercept agent spawning |
| [2-0-42](research/2-0-42.md) | `--max-budget-usd` | Budget limits for SDK |

---

## Key Concepts

### The Core Pattern

1. **Parent agent** (e.g., Mycelia) creates a task in PostgreSQL
2. **Parent spawns child** via Bash tool running `alacritty -e claude`
3. **Child's SessionStart hook** fetches instructions from database
4. **Child executes autonomously** with pre-configured permissions
5. **Child's SessionEnd hook** signals completion via PostgreSQL NOTIFY
6. **Parent receives notification** and continues workflow

### Critical Environment Variables

```bash
# Force Max subscription (not API billing)
unset ANTHROPIC_API_KEY
export CLAUDE_USE_SUBSCRIPTION="true"

# Enable CLAUDE.md loading from --add-dir directories
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```

### Known Limitation

**60-second latency bug** affects `-p` (headless) mode with Max subscription as of v2.1.19+. Workaround: use interactive mode with SessionStart hook for instruction injection instead of `-p` flag.

---

## Reading Order for LLMs

1. **Required:** Read [guide.md](guide.md) completely
2. **As needed:** Read specific research reports based on implementation needs
3. **Reference:** Return to guide sections as needed during implementation

---

*Last updated: 2026-01-27*
