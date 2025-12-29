# Claude Code - What Matters to Symbiont

Personalized changelog filtered through [context.md](context.md).

**Core Project**: Symbiont - cognitive fusion system where Claude Code IS the runtime.
**Architecture**: Mycelia (orchestrator) → SGTAs (god-tier specialists in separate terminals)
**Critical Dependencies**: Custom agents, output styles, MCP servers, hooks, background execution.
**Environment**: Arch Linux, Hyprland, Alacritty, parallel Claude Code sessions via hotkeys.

---

## Relevance Legend

| Icon | Level | Meaning |
|------|-------|---------|
| 🚀 | **Critical** | Directly affects Symbiont architecture - specialists, output styles, MCP, hooks |
| ✨ | **High** | Significant workflow enhancement - background execution, sessions, model selection |
| 🔧 | **Medium** | Quality of life - environment fixes, keyboard shortcuts, performance |

---

## Quick Reference

| Version | Date | Relevance | Why It Matters to Symbiont |
|---------|------|-----------|----------------------------|
| 2.0.74 | Dec 19 | 🔧 | Alacritty terminal setup, LSP for code navigation |
| 2.0.73 | Dec 19 | 🔧 | Kill ring paste cycling across sessions |
| 2.0.72 | Dec 18 | 🔧 | Chrome automation - potential expansion path |
| 2.0.70 | Dec 16 | ✨ | MCP wildcards for symbiont-db permissions |
| 2.0.67 | Dec 12 | ✨ | Opus 4.5 extended thinking on by default |
| 2.0.65 | Dec 11 | ✨ | Context window indicator for god-tier specialists |
| 2.0.64 | Dec 10 | ✨ | Async agents, named sessions, .claude/rules/ |
| 2.0.62 | Dec 9 | 🔧 | Symlinked skill directories fix (core/ symlinks) |
| 2.0.60 | Dec 6 | ✨ | Background agents, /mcp enable/disable toggles |
| 2.0.59 | Dec 4 | 🔧 | `--agent` flag - NOT for SGTAs (ignores CLAUDE.md), useful for quick focused helpers |
| 2.0.54 | Nov 26 | 🔧 | PermissionRequest hook modifications |
| 2.0.52 | Nov 25 | 🔧 | Linux Wayland image paste fix |
| 2.0.51 | Nov 24 | ✨ | Opus 4.5, Desktop app for session management |
| 2.0.45 | Nov 19 | ✨ | PermissionRequest hook for automation |
| 2.0.43 | Nov 18 | 🚀 | Agent permissionMode, SubagentStart hook |
| 2.0.42 | Nov 17 | ✨ | Agent resume, model selection for subagents |
| 2.0.41 | Nov 14 | 🚀 | Plugin output styles - package specialist voices |
| 2.0.37 | Nov 11 | 🔧 | Output style `keep-coding-instructions` option |
| 2.0.34 | Nov 6 | 🔧 | Rust fuzzy finder for monorepo navigation |
| 2.0.32 | Nov 4 | 🚀 | Output styles un-deprecated - voice architecture safe |
| 2.0.31 | Nov 1 | 🔧 | Tool name collision fix (subagents + MCP) |

---

## 🚀 Critical - Architecture Foundations

### 🔧 v2.0.59 - December 4

**What Changed**: `--agent` flag and agent setting for custom system prompts and tool restrictions.

**Symbiont Impact**:
After research: **`--agent` is NOT suitable for SGTAs.** Key finding: `--agent` provides full 200k context BUT ignores CLAUDE.md entirely.

**Why folder-based SGTAs are better:**
- CLAUDE.md loads automatically (persona)
- Separate output-style.md (voice)
- Symlinked core/ works (shared primitives)
- `.claude/rules/` supported (modular config)

**Where `--agent` IS useful:**
- Quick focused helpers (code-reviewer, security-auditor)
- Tool-restricted personas (read-only agents)
- Agents that don't need elaborate maintenance

**Decision**: Keep folder-based SGTAs. Use `--agent` only for simple helpers.

See: `data/claude-code/research/2.0.59/index.md` for full analysis.

---

### 🚀 v2.0.43 - November 18

**What Changed**: `permissionMode` field for custom agents. `SubagentStart` hook event. `skills` frontmatter for subagents.

**Symbiont Impact**:
Three features that directly affect the SGTA architecture:

1. **permissionMode per agent** - Specialists can declare their own permission level. health-coach might be plan-mode (cautious), business-savant might be auto-approve (trusted). No more one-size-fits-all.

2. **SubagentStart hook** - You can intercept when specialists spawn. Use cases:
   - Log to Queen's Ledger when any specialist activates
   - Prime context from PostgreSQL before specialist starts
   - Validate that specialists aren't spawning sub-subagents (violating 2-level max)

3. **skills frontmatter** - Declare which skills subagents can use. Useful for Dual Sovereignty invocations where sovereigns need specific skill access.

---

### 🚀 v2.0.41 - November 14

**What Changed**: Plugin output styles can be shared and installed.

**Symbiont Impact**:
Each specialist's voice is defined in `output-style.md`. This release means you could:
- Package specialist voices as shareable plugins
- Create a "Symbiont Voice Pack" with all specialist styles
- Use the plugin system to version and distribute voice definitions
- More easily create new specialists via the SGTA factory

Currently output styles are local files in each specialist folder. The plugin system offers distribution and versioning that manual files don't.

**Action**: Investigate packaging specialist voices (health-coach's warm/compassionate, business-savant's direct/strategic) as plugins for easier SGTA creation.

---

### 🚀 v2.0.32 - November 4

**What Changed**: Output styles un-deprecated based on community feedback.

**Symbiont Impact**:
Output styles were briefly deprecated in an earlier release. Anthropic reversed this decision. This confirms output styles are here to stay - the foundation of every specialist's personality is stable.

Your entire specialist architecture depends on `output-style.md` files. This restoration guarantees that investment is safe.

---

## ✨ High - Significant Workflow Impact

### ✨ v2.0.64 - December 10

**What Changed**: Async agent/bash execution. Named sessions. `.claude/rules/` directory. Instant auto-compacting.

**Symbiont Impact**:
Four features that enhance the specialist ecosystem:

1. **Async execution (Ctrl+B)** - Background research while you work. Mycelia could dispatch a background agent to check patterns in PostgreSQL while the main conversation continues. Critical for overnight daemon.

2. **Named sessions** - Save and resume specific conversations. Each specialist could maintain persistent context across sessions. Fork a session to experiment, resume original if it fails.

3. **`.claude/rules/`** - Modular configuration. Instead of one monolithic CLAUDE.md, split into:
   ```
   .claude/rules/
   ├── base-persona.md      # Shared across all specialists
   ├── safety-rules.md      # Universal constraints
   └── specialist-config.md # Per-specialist overrides
   ```

4. **Auto-compacting** - Instant context management. God-tier specialists that need full 200k get smarter compaction.

---

### ✨ v2.0.60 - December 6

**What Changed**: Background agent support. `/mcp enable/disable` toggles.

**Symbiont Impact**:
Foundation for v2.0.64's async capabilities. Background agents mean:
- Overnight daemon can spawn background tasks that complete while you sleep
- Mycelia can dispatch research agents without blocking the main conversation
- Multiple background tasks can run in parallel

**MCP toggles** let you disable symbiont-db temporarily for debugging without editing config files. Useful when MCP issues block specialist sessions.

---

### ✨ v2.0.70 - December 16

**What Changed**: Wildcard MCP tool permissions. Enter for prompt suggestions.

**Symbiont Impact**:
Wildcard MCP permissions directly affect symbiont-db. Instead of approving each PostgreSQL operation individually:
```
mcp:symbiont-db:*              # Allow all symbiont-db operations
mcp:symbiont-db:read*          # Allow all reads, prompt for writes
```

This dramatically reduces permission fatigue when specialists query the shared memory layer. Configure once in your permissions file, and all specialists inherit it.

---

### ✨ v2.0.42 - November 17

**What Changed**: Plan subagent. Agent resume. Model selection for subagents.

**Symbiont Impact**:
Three features for Dual Sovereignty and SGTA management:

1. **Agent resume** - If a sovereign (destiny-architect or essence-guardian) needs more context during a decision, you can resume it rather than starting fresh. Preserves reasoning chain.

2. **Model selection** - Mycelia can choose Haiku for quick sovereign checks, Opus for complex reasoning. Cost optimization without sacrificing quality where it matters.

3. **Plan subagent** - Better architectural planning before implementation.

---

### ✨ v2.0.45 - November 19

**What Changed**: PermissionRequest hook. Background tasks with `&` prefix.

**Symbiont Impact**:
**PermissionRequest hook** is a key automation primitive:
- Auto-approve read operations for all specialists
- Log all permission requests to Queen's Ledger for audit
- Deny dangerous operations automatically (no specialist should `rm -rf`)
- Implement custom approval flows per specialist type

Combined with v2.0.43's `permissionMode` per agent, you have complete control over what each specialist can do.

---

### ✨ v2.0.51 - November 24

**What Changed**: Opus 4.5 released. Claude Code Desktop launched.

**Symbiont Impact**:
**Opus 4.5** improves every specialist:
- Better agentic reasoning for complex multi-step tasks
- 50% token reduction means longer conversations before compaction
- Stronger at code migration and refactoring
- Most robust against prompt injection (important for MCP-connected specialists)

**Desktop app** offers parallel session management with Git worktrees - potential alternative to your Alacritty hotkey approach. Worth evaluating whether it improves the multi-specialist workflow.

---

### ✨ v2.0.67 - December 12

**What Changed**: Prompt suggestions (Tab). Extended thinking ON by default for Opus 4.5.

**Symbiont Impact**:
**Extended thinking by default** means all Opus 4.5 specialists automatically get deeper reasoning. No configuration needed - better quality across the board.

Prompt suggestions speed up common patterns in each specialist's domain.

---

### ✨ v2.0.65 - December 11

**What Changed**: Model switching (`Alt+P`). Context window indicator in status line.

**Symbiont Impact**:
**Context window indicator** is critical for god-tier specialists. You can now SEE when a specialist is approaching the 200k limit before auto-compaction kicks in. Helps you decide when to start a new session vs continue.

**Model switching** without losing input - quickly drop to Haiku for simple tasks, back to Opus for complex reasoning.

---

## 🔧 Medium - Quality of Life

### 🔧 v2.0.74 - December 19

**What Changed**: LSP tool for code intelligence. `/terminal-setup` supports Alacritty.

**Symbiont Impact**:
**Alacritty terminal setup** - Your terminal now has official configuration support. Run `/terminal-setup` to ensure optimal rendering.

**LSP tool** improves code navigation for any specialist working on Symbiont's codebase - better go-to-definition, find-references across the monorepo.

---

### 🔧 v2.0.62 - December 9

**What Changed**: Fixed symlinked skill directories. "(Recommended)" indicator for choices.

**Symbiont Impact**:
**Symlink fix** directly affects your architecture. Each specialist symlinks to `core/` for shared primitives. This fix ensures skills in symlinked directories load correctly. Before this fix, specialists might not have had access to shared skills.

---

### 🔧 v2.0.52 - November 25

**What Changed**: Linux Wayland image paste. Bash `$!` variable support.

**Symbiont Impact**:
**Wayland image paste** - You run Hyprland on Wayland. Screenshot pasting now works correctly with wl-paste fallback. Useful for debugging visual issues in specialist sessions.

---

### 🔧 v2.0.54 - November 26

**What Changed**: Hooks can process PermissionRequest suggestions. `Ctrl+N` shortcut.

**Symbiont Impact**:
Builds on the PermissionRequest hook from v2.0.45. Hooks can now modify the permission suggestions themselves, not just approve/deny. More granular automation control.

`Ctrl+N` for new conversation speeds up specialist session management.

---

### 🔧 v2.0.72 - December 18

**What Changed**: Claude in Chrome (Beta) for browser automation.

**Symbiont Impact**:
Browser control could enable new specialist capabilities:
- business-savant could research competitors in real browser
- research-agent could navigate authenticated services
- Overnight daemon could check logged-in dashboards

Currently you use a terminal-only workflow. Chrome integration is a potential expansion path, not current architecture.

---

### 🔧 v2.0.37 - November 11

**What Changed**: Notification hook matchers. `keep-coding-instructions` for output styles.

**Symbiont Impact**:
**Output style options** - `keep-coding-instructions` in frontmatter lets specialist voices preserve coding context when styles apply. Prevents health-coach from losing technical awareness when its warm/compassionate style activates.

---

### 🔧 v2.0.73 - December 19

**What Changed**: Clickable images. `Alt-Y` kill ring. Plugin search filtering.

**Symbiont Impact**:
Power user conveniences. Kill ring (`Alt-Y`) brings Emacs-style paste cycling - access earlier clipboard entries across specialist sessions.

---

### 🔧 v2.0.34 - November 6

**What Changed**: Native Rust fuzzy finder. VSCode permission mode setting.

**Symbiont Impact**:
Faster file suggestions in the Symbiont monorepo. You manage many files across `mycelium/`, `core/`, and `queens-ledger/` - better fuzzy matching helps navigation.

---

### 🔧 v2.0.31 - November 1

**What Changed**: Fixed "Tool names must be unique" error with subagents + MCP.

**Symbiont Impact**:
Bug fix that prevents tool name collisions when specialists use symbiont-db MCP alongside built-in tools. Stability improvement.

---

## Skip List (Not Relevant)

| Version | Date | Reason |
|---------|------|--------|
| v2.0.71 | Dec 16 | Prompt suggestion toggle, glob permission fix - minor |
| v2.0.68 | Dec 12 | CJK/IME fix, enterprise settings - not your use case |
| v2.0.66 | Dec 11 | Hotfix - no details |
| v2.0.63 | Dec 9 | Hotfix - no details |
| v2.0.61 | Dec 7 | VSCode multi-terminal revert - you use Alacritty |
| v2.0.58 | Dec 3 | Pro tier Opus access - you have Max |
| v2.0.57 | Dec 3 | Plan rejection feedback, VSCode streaming - minor |
| v2.0.56 | Dec 2 | Progress bar toggle, VSCode sidebar - minor |
| v2.0.55 | Nov 27 | Proxy DNS fix - corporate network issue |
| v2.0.53 | Nov 25 | Hotfix - no details |
| v2.0.50 | Nov 21 | MCP nested refs fix, ultrathink display - minor |
| v2.0.49 | Nov 21 | Ctrl+Y paste, usage limit clarity - minor |
| v2.0.47 | Nov 20 | Teleport errors, Vertex config - not your setup |
| v2.0.46 | Nov 20 | Image media type fix - minor |
| v2.0.36 | Nov 8 | Autoupdater fix, input loss fix - bug fixes only |
| v2.0.35 | Nov 7 | VSCode font settings - you use Alacritty |
| v2.0.33 | Nov 5 | Native binary launch speed - minor |
| v2.0.69 | Dec 13 | Minor bugfixes - no details |

---

## Summary: What Symbiont Needs to Watch

**CRITICAL features to leverage:**
1. ~~**Custom agents (v2.0.59)**~~ - EVALUATED: Not for SGTAs (ignores CLAUDE.md). Keep folder-based.
2. **Output styles (v2.0.41, v2.0.32)** - Package specialist voices as plugins
3. **Agent permissionMode (v2.0.43)** - Per-specialist permission levels
4. **SubagentStart hook (v2.0.43)** - Intercept specialist spawning for Queen's Ledger

**HIGH features already in use:**
- Background execution (v2.0.60, v2.0.64) - Interactive parallelism (Ctrl+B)
- MCP wildcards (v2.0.70) - symbiont-db permissions
- PermissionRequest hooks (v2.0.45) - Automation and audit
- Named sessions (v2.0.64) - Specialist persistence

**Potential architecture changes to evaluate:**
- ~~Migrate specialists to `--agent` pattern~~ - REJECTED: loses modularity
- Use `.claude/rules/` for modular configuration - PROMISING
- Package output styles as plugins vs local files
- Consider Desktop app for session management vs Alacritty hotkeys
- Headless mode for overnight daemon (not Ctrl+B async)

---

*Last updated: 2025-12-29*
*Filter criteria: [context.md](context.md)*
