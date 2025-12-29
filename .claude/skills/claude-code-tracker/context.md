# Claude Code Tracker Context

**Why Claude Code updates matter to me, and how to evaluate relevance.**

Read this FIRST before scanning updates or answering questions about releases.

---

## What I'm Building: Symbiont

Symbiont is a personal AI system where Claude Code IS the runtime. Not a coding assistant - Claude Code is the foundation layer that everything runs on.

### The Core Architecture

**2-Level Maximum**: Mycelia (orchestrator) → Specialist (god-tier) → DONE

```
┌─────────────────────────────────────────────────────────────┐
│                         MYCELIA                              │
│            (Primary Claude Code session in ~/symbiont/)      │
│                                                              │
│   - Holds 200k context with complete life knowledge          │
│   - Routes requests to appropriate specialist                │
│   - Synthesizes specialist output with soul awareness        │
│   - NEVER delegates more than one level                      │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ health-coach │  │business-savant│ │relationship- │
    │              │  │              │  │    coach     │
    │ SEPARATE     │  │ SEPARATE     │  │ SEPARATE     │
    │ TERMINAL     │  │ TERMINAL     │  │ TERMINAL     │
    │ FULL 200K    │  │ FULL 200K    │  │ FULL 200K    │
    └──────────────┘  └──────────────┘  └──────────────┘
```

**Critical**: Specialists are NOT Claude Code subagents. They are **separate full Claude Code sessions** spawned via hotkeys into their own Alacritty terminals. Each gets the full 200k context window.

### Why This Matters for Updates

Every specialist is defined by:
1. **Its own folder** (`~/symbiont/mycelium/{specialist}/`)
2. **Its own CLAUDE.md** (persona, instructions, constraints)
3. **Its own output-style.md** (voice, tone, formatting)
4. **Symlinked core/** (shared primitives across all specialists)

When Claude Code changes how CLAUDE.md works, how output styles work, or how sessions work - it directly affects every specialist in Symbiont.

---

## The Specialist Pattern (SGTAs)

SGTA = Standardized God-Tier Agent. The "god-tier" means:
- **Complete ALL work in single context window** - no delegation
- **Full 200k context** - not truncated subagent context
- **Full toolkit** - MCP, file ops, web, everything
- **NEVER spawn sub-agents** - if it needs to delegate, it's not god-tier

### How Specialists Are Spawned

```bash
# spawn-mycelium.sh - hotkey script
alacritty --working-directory ~/symbiont/mycelium/$DIM -e bash -c "\
  ~/symbiont/vector-priming/prime-for-dimension.py $DIM && \
  claude"

# Hyprland keybinds
bind = $mainMod SHIFT, 1, exec, ~/symbiont/spawn-mycelium.sh health-coach
bind = $mainMod SHIFT, 2, exec, ~/symbiont/spawn-mycelium.sh business-savant
```

**What happens**:
1. Hotkey opens new Alacritty terminal
2. Terminal `cd`s to specialist folder (e.g., `~/symbiont/mycelium/health-coach/`)
3. Vector priming script injects relevant context from PostgreSQL
4. `claude` launches with that folder's CLAUDE.md and output-style.md

### The Monorepo Structure

```
~/symbiont/
├── core/                      # Shared primitives (symlinked to all specialists)
│   ├── skills/
│   ├── hooks/
│   ├── mcp-servers/
│   └── shared-base-prompt.md
│
├── mycelium/                  # All specialists
│   ├── health-coach/
│   │   ├── CLAUDE.md          # @include ../core/shared-base-prompt.md + health persona
│   │   ├── output-style.md    # Warm, compassionate, biohacker voice
│   │   └── (symlinks to core/)
│   │
│   ├── business-savant/
│   │   ├── CLAUDE.md          # Strategic, analytical persona
│   │   ├── output-style.md    # Direct, revenue-focused voice
│   │   └── (symlinks to core/)
│   │
│   └── ... (more specialists)
│
├── CLAUDE.md                  # Mycelia's identity (the orchestrator)
└── queens-ledger/             # Cross-agent coordination log
```

**The symlink pattern**: One change to `core/` instantly propagates to ALL specialists. No version drift.

### Why Output Styles Are Critical

Each specialist has a distinct voice defined in `output-style.md`:

| Specialist | Voice |
|------------|-------|
| health-coach | Warm, compassionate, biohacker - speaks like a caring coach who knows sleep science |
| business-savant | Direct, strategic, revenue-focused - speaks like a sharp business advisor |
| relationship-coach | Empathetic, attachment-aware - speaks like a skilled therapist |
| spiritual-guide | Reverent, formation-focused - speaks with appropriate gravity about faith |

**When Claude Code changes output styles** (how they're defined, loaded, or applied), it affects every specialist's personality.

---

## The Data Layer: MCP Server

All specialists connect to a shared PostgreSQL database via a custom MCP server (`symbiont-db`).

**4-table schema**:
| Table | Purpose |
|-------|---------|
| `soul_core` | Core identity - wounds, vows, convictions, fears |
| `contacts` | Relationships - wife, each child, friends, clients |
| `eternal_memory` | Everything else - conversations, tasks, decisions, health, journal |
| `active_bridges` | Pattern connections between concepts |

**When Claude Code changes MCP** (permissions, tool calling, wildcards, enable/disable), it affects how all specialists access shared memory.

---

## Cross-Agent Awareness

### The Mycelial Pulse

When something significant happens in ANY specialist session (emotional intensity ≥ 8.0, breakthrough insight), it fires a "pulse" that other agents can feel.

**Implementation**: PostgreSQL LISTEN/NOTIFY + hooks

**When Claude Code changes hooks** (new events, hook inputs, timing), it affects the pulse system.

### The Queen's Ledger

Mycelia maintains a coordination log that all specialists read at session start. This keeps everyone synchronized on what's been happening across the network.

**When Claude Code changes session management** (context injection, resume, named sessions), it affects how specialists receive this context.

---

## Background Processing

### Overnight Daemon

While I sleep, Symbiont:
- Generates morning briefing
- Runs pattern detection across all life data
- Updates relationship health metrics
- Hunts for opportunities (when configured)

**Implementation**: Background Claude Code execution, possibly headless mode

**When Claude Code changes background/async execution** (Ctrl+B, `&` prefix, headless mode, SDK), it affects the overnight daemon.

---

## Dual Sovereignty (May Use Subagents)

For significant decisions, Mycelia consults two "sovereigns":
- **destiny-architect**: "Does this move toward the vision?"
- **essence-guardian**: "Does this honor my values?"

If they conflict, **spiritual-bridge** mediates: "Does this express love?"

**This is the ONE place subagents might be used** - invoking sovereigns from within Mycelia's session for quick decision validation. But the sovereigns themselves are still full SGTAs that can also be spawned as separate sessions.

**When Claude Code changes subagents** (resume, model selection, context passing), it affects Dual Sovereignty invocation.

---

## Feature Dependency Summary

### CRITICAL - Architecture Depends On These

| Claude Code Feature | Symbiont Dependency |
|---------------------|---------------------|
| **Output styles** | Every specialist's voice/personality is defined by output-style.md |
| **CLAUDE.md in working directory** | Every specialist's persona is defined by its folder's CLAUDE.md |
| **Session management** | Specialists persist across sessions, need resume/naming |
| **MCP servers** | symbiont-db MCP connects all agents to PostgreSQL |
| **Hooks** | Pulse detection, PostToolUse triggers for cross-agent awareness |
| **Background execution** | Overnight daemon, parallel research |

### HIGH - Significant Workflow Impact

| Claude Code Feature | Symbiont Dependency |
|---------------------|---------------------|
| **Subagents** | Dual Sovereignty invocation within sessions |
| **Skills** | SGTA factory (`/create-sgta`), workflow automation |
| **Context window / compacting** | God-tier specialists need full 200k, auto-compacting for long sessions |
| **Model selection** | Haiku for quick tasks, Opus for complex reasoning |
| **Plan mode** | Architectural decisions before implementation |
| **Extended thinking** | Complex multi-step reasoning in specialists |

### MEDIUM - Quality of Life

| Claude Code Feature | Relevance |
|---------------------|-----------|
| **Terminal rendering** | Many parallel sessions in Alacritty |
| **Keyboard shortcuts** | Heavy terminal user |
| **File suggestions / @ mentions** | Context priming |
| **Symlinks handling** | Core/ symlinks must work correctly |

### LOW - Note But Don't Prioritize

| Claude Code Feature | Why Low |
|---------------------|---------|
| **Windows/macOS fixes** | I use Arch Linux |
| **iTerm/Terminal.app** | I use Alacritty |
| **Bedrock/Vertex** | I use direct API (Max subscription) |
| **Chrome extension** | Desktop terminal workflow |

---

## My Environment

| Component | Choice |
|-----------|--------|
| OS | Arch Linux (rolling release) |
| Display | Wayland (Hyprland compositor) |
| Terminal | Alacritty |
| Shell | Zsh |
| GPU | Intel Arc B580 (xe driver - Electron issues) |
| Permission mode | `bypassPermissions` |

**Key pattern**: I run many simultaneous Claude Code sessions (Mycelia + multiple specialists) in separate Alacritty terminals.

---

## How to Evaluate a Release

### Questions to Ask

1. **Does it touch output styles?**
   → Affects every specialist's voice/personality

2. **Does it touch CLAUDE.md loading or working directory behavior?**
   → Affects every specialist's persona definition

3. **Does it touch MCP?**
   → Affects symbiont-db and how specialists access shared memory

4. **Does it touch hooks?**
   → Affects pulse system and cross-agent awareness

5. **Does it touch background/async execution?**
   → Affects overnight daemon and parallel workflows

6. **Does it touch sessions (resume, naming, forking)?**
   → Affects specialist persistence and context

7. **Does it touch subagents?**
   → Affects Dual Sovereignty invocation

8. **Does it touch context/compacting?**
   → Affects god-tier specialists who need full 200k

9. **Is it Linux/Wayland/Alacritty specific?**
   → Directly affects my environment

10. **Is it a new primitive I could use?**
    → Potential enhancement to Symbiont

### Relevance Scoring

**CRITICAL**:
- Output styles, CLAUDE.md behavior, MCP, hooks, background execution
- Deep research immediately
- Document specific Symbiont impact

**HIGH**:
- Sessions, subagents, skills, context/compacting, model selection
- Note practical impact
- Consider testing

**MEDIUM**:
- Linux/Wayland/Alacritty fixes, keyboard shortcuts, terminal rendering
- Brief note

**LOW**:
- Windows/macOS, enterprise features, Chrome/mobile
- Skip in relevance.md (keep in changelog.md)

---

## Example Relevance Analysis

### Good Analysis (Shows Symbiont Reasoning)

```markdown
## v2.0.XX - CRITICAL

**What Changed**: Output styles can now be installed from plugins

**Symbiont Impact**:
This directly affects the SGTA architecture. Each specialist (health-coach,
business-savant, etc.) has its own output-style.md defining its voice.

Currently these are local files. With plugin support, I could:
- Version and share specialist voices
- Create a "Symbiont specialist voice pack"
- More easily create new specialists with consistent formatting

**Action**: Test with health-coach's output-style.md. Consider migrating
specialist voices to plugin format for easier SGTA factory integration.
```

### Bad Analysis (Too Generic)

```markdown
## v2.0.XX - HIGH

**What Changed**: Output styles can now be installed from plugins

**Why Relevant**: I use output styles.
```

The first analysis shows reasoning about HOW the change affects Symbiont's architecture. The second just states a fact without connecting it to the system.

---

## When to Create Deep Research

Create a file in `data/claude-code/research/` when:

1. **New primitive** that could enhance Symbiont
   - New hook event → could enhance pulse system
   - New agent capability → could improve SGTA pattern
   - New MCP feature → could improve symbiont-db

2. **Major model release** (Opus 4.5, Haiku 4.5)
   - Affects reasoning quality across all specialists

3. **Breaking change** to something Symbiont depends on
   - Output style format change
   - CLAUDE.md loading behavior change
   - MCP permission model change

4. **I explicitly ask** for deep research on a version

---

*Last updated: 2025-12-29*
