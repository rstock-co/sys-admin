# Claude Code Changelog

Internal changelog with plain-language explanations of Claude Code releases.

**Legend:**
| Emoji | Meaning |
|-------|---------|
| 🚀 | **Major** - Game-changing features, new capabilities |
| ✨ | **Notable** - Significant improvements, workflow enhancements |
| 🔧 | **Minor** - Small enhancements, QoL improvements |
| 🐛 | **Patch** - Bug fixes only, no new features |

---

## Quick Reference

| Version | Date | Tier | Summary |
|---------|------|------|---------|
| 2.1.20 | Jan 27 | 🚀 | PR review status, --add-dir CLAUDE.md loading, task deletion |
| 2.1.19 | Jan 23 | ✨ | $0/$1 argument shorthand, VSCode session forking, skills auto-allow |
| 2.1.18 | Jan 23 | ✨ | /keybindings command, chord sequences, per-context keybindings |
| 2.1.17 | Jan 22 | 🐛 | AVX instruction support crash fix |
| 2.1.16 | Jan 22 | 🚀 | Native task system with dependency tracking, VSCode plugin management |
| 2.1.15 | Jan 21 | 🔧 | npm deprecation notice, React Compiler perf, MCP stdio fix |
| 2.1.14 | Jan 20 | ✨ | History autocomplete, plugin pinning, context window fix (65%→98%) |
| 2.1.12 | Jan 17 | 🐛 | Message rendering bug fix |
| 2.1.11 | Jan 17 | 🔧 | MCP HTTP/SSE connection fix |
| 2.1.10 | Jan 17 | ✨ | New "Setup" hook event, OAuth copy shortcut |
| 2.1.9 | Jan 16 | 🚀 | PreToolUse additionalContext, plansDirectory, session URL attribution |
| 2.1.7 | Jan 14 | ✨ | Customizable keybindings.json, showTurnDuration, MCP auto mode |
| 2.1.6 | Jan 13 | ✨ | Nested skill discovery, /config search, /stats date filtering |
| 2.1.5 | Jan 12 | 🐛 | CLAUDE_CODE_TMPDIR env var |
| 2.1.4 | Jan 10 | 🔧 | CLAUDE_CODE_DISABLE_BACKGROUND_TASKS env var |
| 2.1.3 | Jan 9 | ✨ | Unified slash commands + skills model, release channel toggle |
| 2.1.2 | Jan 9 | 🔧 | Security fix, memory leak fix, clickable hyperlinks |
| 2.1.0 | Jan 9 | 🚀 | Skill hot-reload, context:fork, Vim motions, /plan command |
| 2.0.76 | Dec 22 | 🐛 | No prompt changes, likely infrastructure fixes |
| 2.0.75 | Dec 20 | 🔧 | Prompt cleanup (-183 tokens), removed redundant Task tool guidance |
| 2.0.74 | Dec 19 | 🚀 | LSP tool for code intelligence (go-to-def, references, hover) |
| 2.0.73 | Dec 19 | ✨ | Clickable images, alt-y kill ring, plugin search |
| 2.0.72 | Dec 18 | 🚀 | Claude in Chrome (Beta) - browser automation |
| 2.0.71 | Dec 16 | 🔧 | Prompt suggestion toggle, glob permission fix |
| 2.0.70 | Dec 16 | ✨ | Wildcard MCP permissions, Enter for suggestions |
| 2.0.69 | Dec 13 | 🐛 | Minor bugfixes |
| 2.0.68 | Dec 12 | 🔧 | CJK/IME fix, enterprise managed settings |
| 2.0.67 | Dec 12 | ✨ | Prompt suggestions (Tab), Opus 4.5 thinking default |
| 2.0.66 | Dec 11 | 🐛 | Hotfix |
| 2.0.65 | Dec 11 | ✨ | Model switching (alt+p), context window indicator |
| 2.0.64 | Dec 10 | 🚀 | Async agents/bash, .claude/rules/, /stats, named sessions |
| 2.0.63 | Dec 9 | 🐛 | Hotfix |
| 2.0.62 | Dec 9 | 🔧 | "(Recommended)" indicator, custom commit byline |
| 2.0.61 | Dec 7 | 🐛 | Reverted VSCode multi-terminal (caused lag) |
| 2.0.60 | Dec 6 | 🚀 | Background agents, /mcp enable/disable toggles |
| 2.0.59 | Dec 4 | 🚀 | --agent flag for custom agent personas |
| 2.0.58 | Dec 3 | ✨ | Pro users get Opus 4.5 access |
| 2.0.57 | Dec 3 | 🔧 | Feedback on plan rejection, VSCode streaming |
| 2.0.56 | Dec 2 | 🔧 | Progress bar toggle, VSCode secondary sidebar |
| 2.0.55 | Nov 27 | 🔧 | Proxy DNS fix, fuzzy matching improvements |
| 2.0.54 | Nov 26 | ✨ | Hooks can modify permissions, Cmd+N shortcut |
| 2.0.53 | Nov 25 | 🐛 | Hotfix |
| 2.0.52 | Nov 25 | 🔧 | Linux Wayland image paste, $! variable support |
| 2.0.51 | Nov 24 | 🚀 | **Opus 4.5**, Claude Code Desktop launched |
| 2.0.50 | Nov 21 | 🔧 | MCP nested refs fix, ultrathink display |
| 2.0.49 | Nov 21 | 🔧 | Readline Ctrl+Y paste, usage limit clarity |
| 2.0.47 | Nov 20 | 🐛 | Teleport errors, Vertex config fix |
| 2.0.46 | Nov 20 | 🐛 | Image media type detection fix |
| 2.0.45 | Nov 19 | 🚀 | Azure AI Foundry, PermissionRequest hook, `&` background |
| 2.0.43 | Nov 18 | ✨ | Agent permissionMode, skills frontmatter, SubagentStart hook |
| 2.0.42 | Nov 17 | 🚀 | Plan subagent, agent resume, model selection for subagents |
| 2.0.41 | Nov 14 | ✨ | Plugin output styles sharing, SDK hook timeouts |
| 2.0.37 | Nov 11 | 🔧 | Notification hook matchers, output style options |
| 2.0.36 | Nov 8 | 🐛 | Autoupdater disable fix, input loss fix |
| 2.0.35 | Nov 7 | 🔧 | Native Rust fuzzy finder, VSCode font settings |
| 2.0.34 | Nov 6 | ✨ | Native Rust fuzzy finder, VSCode permission mode |
| 2.0.33 | Nov 5 | 🔧 | Faster native binary launch, doctor improvements |
| 2.0.32 | Nov 4 | 🔧 | Output styles un-deprecated, company announcements |
| 2.0.31 | Nov 1 | 🔧 | Windows shift+tab, Vertex web search support |

---

<!-- New releases are added below this line -->

## 🚀 v2.1.20 - January 27, 2026

### What Changed
PR review status indicator in prompt footer showing branch PR state. Support for loading `CLAUDE.md` files from directories via `--add-dir` flag. Task deletion capability via TaskUpdate tool. Arrow key history navigation in vim normal mode when cursor cannot move further. External editor shortcut (Ctrl+G) added to help menu. Session compaction fixes for resume functionality. Wide character and Unicode handling improvements. Draft prompt preservation when navigating command history. Ghost text flickering eliminated in slash commands. Dynamic task list visibility based on terminal height. Timestamped config backup rotation.

### What It Means
**PR Review Status in Footer:**
The prompt footer now shows the PR status of your current branch - whether it's under review, approved, has requested changes, etc. Provides git workflow awareness without leaving the terminal.

**--add-dir CLAUDE.md Loading:**
Load CLAUDE.md instructions from arbitrary directories, not just the working directory. **Requires environment variable:**
```bash
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```
This is opt-in for backward compatibility. Without the env var, `--add-dir` only provides file access, not instruction loading. Once enabled:
- Reference shared instructions from a central location
- Include team-wide standards from a shared folder
- Layer multiple instruction sets

**Note:** This feature is currently undocumented. See [GitHub Issue #21138](https://github.com/anthropics/claude-code/issues/21138).

**Task Deletion:**
TaskUpdate tool can now delete tasks, not just update them. Cleaner task management for long sessions.

---

## ✨ v2.1.19 - January 23, 2026

### What Changed
Environment variable `CLAUDE_CODE_ENABLE_TASKS` allows disabling the new task system temporarily. Shorthand syntax `$0`, `$1` for accessing individual arguments in custom commands. Fixed crashes on processors lacking AVX instruction support. Resolved dangling processes when terminals close unexpectedly. Fixed `/rename` and `/tag` session updates when resuming from different directories. Prompt stash functionality no longer loses pasted text. Skills without extra permissions auto-allow without approval. Changed indexed argument syntax from `$ARGUMENTS.0` to `$ARGUMENTS[0]`. SDK: Added replay of queued commands as `SDKUserMessageReplay` events. VSCode: Enabled session forking and rewind functionality for all users.

### What It Means
**$0/$1 Argument Shorthand:**
Custom skills/commands can now use `$0`, `$1`, `$2` shorthand instead of the verbose `$ARGUMENTS[0]` syntax. Cleaner skill definitions.

**VSCode Session Forking:**
Session forking and rewind (conversation state recovery) is now available to all VSCode users. Previously limited rollout.

**Skills Auto-Allow:**
Skills that don't require extra permissions now execute without prompting. Reduces friction for simple skills.

---

## ✨ v2.1.18 - January 23, 2026

### What Changed
Customizable keyboard shortcuts now available via `/keybindings` command. Configure context-specific keybindings and chord sequences for personalized workflow.

### What It Means
**Enhanced Keybindings:**
Building on v2.1.7's `keybindings.json`, this adds the `/keybindings` command for easy access and introduces chord sequences (multi-key combos like `Ctrl+K Ctrl+C`). Context-specific means different shortcuts can apply in different modes (normal, insert, command).

### How to Use It
```bash
/keybindings        # Open keybindings configuration
```

### Learn More
- [Keybindings Documentation](https://code.claude.com/docs/en/keybindings)

---

## 🐛 v2.1.17 - January 22, 2026

Fixed crashes on processors without AVX instruction support. Stability fix for older hardware.

---

## 🚀 v2.1.16 - January 22, 2026

### What Changed
New task management system with dependency tracking capabilities. VSCode: Native plugin management support added. VSCode: OAuth users can now browse and resume remote Claude sessions. Fixed out-of-memory crashes when resuming sessions with heavy subagent usage. Context warning now properly hides after running `/compact`. Session titles respect user's language setting on resume screen. IDE: Fixed race condition on Windows preventing sidebar from appearing on startup.

### What It Means
**Native Task System:**
Claude Code now has first-class task management built into the core. This is a significant evolution from the previous TodoWrite approach:

- **Dependency Tracking**: Tasks can declare `blockedBy` and `blocks` relationships
- **Status Tracking**: Tasks progress through `pending` → `in_progress` → `completed`
- **Progress Visualization**: See task status in real-time, identify available work
- **Agent Coordination**: Assign tasks to sub-agents, track completion across parallel workers

**Key Characteristics:**
- Session-scoped: Tasks exist within a session (don't persist across sessions by default)
- Integrated with sub-agents: Agents can create, claim, and complete tasks
- Replaces ad-hoc todo tracking with structured workflow

**Use Cases:**
- Complex multi-step implementations with clear dependencies
- Parallel agent work coordination
- Progress tracking for long-running tasks

**Limitations:**
- Tasks don't persist across sessions automatically
- Need "hydration pattern" (spec files) for cross-session continuity

**VSCode Plugin Management:**
Native UI for browsing, installing, and managing Claude Code plugins within VSCode.

**Remote Session Browsing:**
OAuth users can browse and resume their remote Claude.ai sessions from the CLI/VSCode.

### How to Use It
```bash
# Tasks are managed via TaskCreate, TaskUpdate, TaskGet, TaskList tools
# Claude uses these automatically for complex multi-step work
# Use /tasks to view current task state
```

### Learn More
- [Claude Code Tasks Overview](https://medium.com/@joe.njenga/claude-code-tasks-are-here-new-update-turns-claude-code-todos-to-tasks-a0be00e70847)
- [VentureBeat: Tasks Update](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)

---

## 🔧 v2.1.15 - January 21, 2026

### What Changed
Added deprecation notification for npm installations. Improved UI rendering performance with React Compiler. Fixed "Context left until auto-compact" warning persistence. Fixed MCP stdio server timeout causing UI freezes.

### What It Means
Performance and stability improvements. React Compiler adoption means faster UI rendering. MCP stdio fix prevents UI hangs when MCP servers are slow to respond.

---

## ✨ v2.1.14 - January 20, 2026

### What Changed
History-based autocomplete in bash mode with Tab completion. Search functionality for installed plugins list. Plugin pinning to specific git commit SHAs. Fixed context window blocking calculation (was ~65%, now ~98%). Memory leak fixes for parallel subagents and long-running sessions.

### What It Means
**Context Window Fix:**
A significant regression fix. The context window was only being used to ~65% capacity before blocking - now it properly uses ~98%. This means longer conversations before hitting limits.

**Memory Leak Fixes:**
Critical for long-running sessions and parallel subagents. Sessions that previously crashed or degraded over time should be stable now.

**Plugin Pinning:**
Pin plugins to specific git SHAs for reproducibility. Prevents surprise breaks when plugin authors push updates.

---

## 🐛 v2.1.12 - January 17, 2026

Fixed message rendering bug.

---

## 🔧 v2.1.11 - January 17, 2026

### What Changed
Fixed excessive MCP connection requests for HTTP/SSE transports.

### What It Means
MCP servers using HTTP/SSE (rather than stdio) no longer get spammed with reconnection attempts. Reduces network overhead and server load.

---

## ✨ v2.1.10 - January 17, 2026

### What Changed
New "Setup" hook event for repository setup operations. Keyboard shortcut 'c' to copy OAuth URL during login. Fixed crash with heredocs containing JavaScript template literals. Improved startup keystroke capture and file suggestions.

### What It Means
**Setup Hook:**
A new hook event that fires during repository setup operations. Use cases:
- Auto-configure project settings on first clone
- Install dependencies automatically
- Set up development environment

This expands the hooks system with another lifecycle event to intercept.

---

## 🚀 v2.1.9 - January 16, 2026

### What Changed
Added `auto:N` syntax for MCP tool search auto-enable threshold. Added `plansDirectory` setting for customizing plan file storage. Added external editor support (Ctrl+G) in AskUserQuestion. Session URL attribution to commits and PRs from web sessions. PreToolUse hooks can return `additionalContext`. Added `${CLAUDE_SESSION_ID}` string substitution for skills.

### What It Means
**PreToolUse additionalContext:**
This is a significant hooks enhancement. PreToolUse hooks can now inject additional context that gets included in the tool execution. Use cases:
- Inject relevant documentation before file reads
- Add context from external systems before operations
- Enrich tool calls with metadata

**MCP auto:N Threshold:**
Configure how many MCP tools must match before auto-enabling: `auto:3` means only auto-enable if 3+ tools match the pattern.

**Session ID Substitution:**
Skills can reference `${CLAUDE_SESSION_ID}` for session-aware behavior - useful for logging, coordination between skills, and persistent storage keyed by session.

**plansDirectory:**
Store plan files in a custom location instead of the default. Useful for keeping plans in version control or a shared location.

### How to Use It
```javascript
// PreToolUse hook returning additionalContext
{
  "hooks": {
    "PreToolUse": [{
      "command": "my-context-injector",
      "timeout": 5000
    }]
  }
}
// Hook script can return: { "additionalContext": "Extra info for Claude" }
```

---

## ✨ v2.1.7 - January 14, 2026

### What Changed
Customizable keyboard shortcuts via `~/.claude/keybindings.json`. `showTurnDuration` setting to hide turn duration messages. Feedback option on permission prompts. Inline agent response display in task notifications. Security fix for wildcard permission rules matching compound commands. MCP tool search auto mode enabled by default.

### What It Means
**Customizable Keybindings:**
Finally! Create `~/.claude/keybindings.json` to remap keyboard shortcuts. Useful for:
- Avoiding conflicts with terminal emulator shortcuts
- Matching your muscle memory from other tools
- Custom workflows

**MCP Auto Mode Default:**
MCP tool search now defaults to auto mode - Claude automatically finds and uses relevant MCP tools without explicit enabling. Reduces friction when working with MCP servers.

---

## ✨ v2.1.6 - January 13, 2026

### What Changed
Search functionality for `/config` command. Updates section in `/doctor` showing auto-update channel. Date range filtering in `/stats` (7/30/All time). Automatic skill discovery from nested `.claude/skills` directories. Fixed permission bypass via shell line continuation. Fixed false "File has been unexpectedly modified" errors.

### What It Means
**Nested Skill Discovery:**
Skills in subdirectories of `.claude/skills/` are now automatically discovered. Organize skills by category:
```
.claude/skills/
├── code-quality/
│   ├── lint/
│   └── review/
├── git/
│   ├── commit/
│   └── pr/
└── research/
```

**Stats Date Filtering:**
View usage stats for last 7 days, 30 days, or all time. Better cost tracking.

---

## 🐛 v2.1.5 - January 12, 2026

Added `CLAUDE_CODE_TMPDIR` environment variable to override temp directory location.

---

## 🔧 v2.1.4 - January 10, 2026

### What Changed
Added `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable. Fixed "Help improve Claude" setting fetch with OAuth retry logic.

### What It Means
Disable background tasks entirely via environment variable. Useful for debugging or resource-constrained environments.

---

## ✨ v2.1.3 - January 9, 2026

### What Changed
Merged slash commands and skills into unified model. Release channel toggle in `/config`. Detection of unreachable permission rules with warnings. Fixed plan files persisting across `/clear` commands. Fixed duplicate skill detection on filesystems with large inodes.

### What It Means
**Unified Commands + Skills:**
Slash commands and skills are now the same thing under the hood. A skill IS a slash command. This simplifies the mental model - everything is a skill, some are built-in, some are custom.

**Unreachable Permission Warnings:**
Claude Code now warns if you have permission rules that can never trigger (e.g., a deny rule after a broader allow rule). Helps debug permission configurations.

---

## 🔧 v2.1.2 - January 9, 2026

### What Changed
Source path metadata for dragged images. Clickable file path hyperlinks (OSC 8) for iTerm. Windows Package Manager (winget) installation support. Shift+Tab shortcut in plan mode. Command injection security vulnerability fix. Memory leak fix for tree-sitter parse trees.

### What It Means
Security and stability fixes. The tree-sitter memory leak fix improves performance when working with large codebases over extended sessions.

---

## 🚀 v2.1.0 - January 9, 2026

### What Changed
Automatic skill hot-reload. `context: fork` support for skill sub-agents. `language` setting for response language customization. Shift+Enter works out-of-box in iTerm2, WezTerm, Ghostty, Kitty. Extensive Vim motions support (`;`, `,`, `y`, `p`, `>>`, `<<`, `J`). `/plan` command shortcut. Wildcard pattern matching for Bash tool permissions. Unified Ctrl+B backgrounding for bash and agents.

### What It Means
**Skill Hot-Reload:**
Edit a skill file and it's immediately available - no restart required. This dramatically speeds up skill development iteration. Change your skill, test it instantly.

**context: fork for Skills:**
Skills can now spawn sub-agents in a forked context. The sub-agent gets a copy of the current conversation state but operates independently. Perfect for:
- Research that shouldn't pollute main context
- Experimental operations that might fail
- Parallel exploration paths

**Vim Motions:**
Comprehensive Vim navigation now works in the input. `;` and `,` repeat finds, `y` yanks, `p` pastes, `>>` and `<<` indent, `J` joins lines. Power users rejoice.

**Unified Ctrl+B:**
Both bash commands AND agents can be backgrounded with Ctrl+B. Consistent UX for async operations.

**/plan Command:**
Quick shortcut to enter plan mode. Equivalent to starting a message that triggers planning.

### How to Use It
```yaml
# Skill with forked context
---
name: research-topic
context: fork
---
Research this topic thoroughly without affecting main conversation.
```

---

## 🐛 v2.0.76 - December 22, 2025

### What Changed
No system prompt modifications in this release.

### What It Means
Infrastructure or CLI fixes only. No user-facing prompt changes detected. Likely bug fixes or internal improvements.

---

## 🔧 v2.0.75 - December 20, 2025

### What Changed
Prompt cleanup reducing token count by 183 tokens. Removed Task tool extra notes about absolute path usage, emoji restrictions, and colon placement before tool invocations. Removed instruction preventing colons immediately before tool calls.

### What It Means
Streamlining release. Redundant guidance in the Task tool documentation was consolidated or removed. The constraint about punctuation formatting before tool invocation syntax was eliminated. No functional changes—just cleaner prompts.

---

## 🚀 v2.0.74 - December 19, 2025

### What Changed
LSP (Language Server Protocol) tool introduced for native code intelligence. Extended `/terminal-setup` to Kitty, Alacritty, Zed, and Warp. Added `ctrl+t` syntax highlighting toggle. Fixed skill tool restrictions. Improved `/context` visualization.

### What It Means
This is a paradigm shift in how Claude navigates code. Before LSP, Claude was essentially doing "fancy grep" - text pattern matching to find definitions and references. Now Claude has access to the same code intelligence your IDE uses.

The LSP integration provides five core operations:
- **goToDefinition** - Jump directly to where a symbol is defined
- **findReferences** - Locate all usages of a function or variable across the codebase
- **documentSymbol** - View file structure and symbol hierarchy
- **hover** - Display type information and documentation
- **getDiagnostics** - Real-time error and warning detection after edits

For large codebases, this means dramatically more accurate refactoring. Claude can understand type hierarchies, inheritance chains, and symbol relationships that were previously invisible. The language server reports diagnostics after each edit, so Claude catches errors immediately rather than at build time.

There's a plugin marketplace with LSP servers for TypeScript (vtsls), Python (pyright), Rust (rust-analyzer), Go, Java, C/C++, PHP, Ruby, C#, and more.

### How to Use It
LSP is enabled automatically in v2.0.74+. Claude will use it when navigating code. For best results, ensure your project has the appropriate language server available.

### Learn More
- [Claude Code LSP Guide](https://medium.com/@joe.njenga/how-im-using-new-claude-code-lsp-to-code-fix-bugs-faster-language-server-protocol-cf744d228d02)
- [LSP Plugin Marketplace](https://github.com/Piebald-AI/claude-code-lsps)
- [Hacker News Discussion](https://news.ycombinator.com/item?id=46355165)

---

## ✨ v2.0.73 - December 19, 2025

### What Changed
Clickable `[Image #N]` links open in default viewer. Added `alt-y` kill ring history (yank-pop). Search filtering on plugin discovery. Enhanced `/theme` command. VSCode tab icon badges for permissions/completions.

### What It Means
Power user improvements. Kill ring (`alt-y`) brings Emacs-style paste cycling - access earlier clipboard entries. Clickable images make reviewing screenshots easier.

---

## 🚀 v2.0.72 - December 18, 2025

### What Changed
Launched "Claude in Chrome (Beta)" - browser control via Chrome extension. Reduced terminal flickering. QR code for mobile downloads. Loading indicator for conversation resumption. `@` file suggestions ~3x faster. Thinking toggle changed from Tab to `Alt+T`.

### What It Means
Claude Code can now control your browser directly from the terminal. This is a significant expansion of Claude's capabilities - build in terminal, test in browser, without context switching.

**What Claude can do in Chrome:**
- Navigate pages and click buttons
- Fill forms and interact with UI elements
- Read console logs and monitor network requests
- Record GIFs of browser interactions
- Access sites you're already logged into (Gmail, Notion, internal tools)

The extension uses Chrome's Native Messaging API to receive commands from Claude Code. Because it shares your browser's login state, Claude can interact with authenticated services without API configuration.

**Safety features:** Anthropic built multiple safeguards and reduced prompt injection success rates from 23.6% to 11.2%. When Claude encounters login pages or CAPTCHAs, it pauses and asks you to handle them manually.

**Note:** The thinking toggle moved from Tab to `Alt+T` to free Tab for the new prompt suggestions feature (v2.0.67).

### How to Use It
1. Install the Claude in Chrome extension
2. Run `claude --chrome` to connect
3. Claude can now control browser tabs while you work in terminal

Currently available to Max plan subscribers (beta).

### Learn More
- [Official Blog: Piloting Claude in Chrome](https://claude.com/blog/claude-for-chrome)
- [Chrome Extension Docs](https://code.claude.com/docs/en/chrome)
- [Getting Started Guide](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome)

---

## 🔧 v2.0.71 - December 16, 2025

### What Changed
`/config` toggle for prompt suggestions. Fixed permission rules rejecting bash glob patterns. Improved Bedrock environment variable handling.

### What It Means
Disable prompt suggestions if distracting. Glob pattern permissions like `Bash(ls:*)` now work correctly.

---

## ✨ v2.0.70 - December 16, 2025

### What Changed
Enter key acceptance for prompt suggestions. Wildcard MCP tool permissions. Auto-update toggle per marketplace.

### What It Means
**Wildcard MCP Permissions:**
Instead of approving each MCP tool individually, you can now use wildcards:
```
mcp:github:*           # Allow all GitHub MCP tools
mcp:filesystem:read*   # Allow all read operations
```

This dramatically reduces permission fatigue when working with MCP servers that have many tools. Configure in your permissions file or approve once with the wildcard pattern.

**Enter for Suggestions:**
Prompt suggestions can now be accepted with Enter (in addition to Tab), making the flow more natural.

---

## 🐛 v2.0.69 - December 13, 2025

Minor bugfixes only. No user-facing changes.

---

## 🔧 v2.0.68 - December 12, 2025

### What Changed
Fixed IME support for CJK languages. Corrected word navigation. Improved plan mode exit UX. Enterprise managed settings support.

### What It Means
Critical fix for Chinese/Japanese/Korean keyboard users. Enterprise orgs can now centrally manage Claude Code settings.

---

## ✨ v2.0.67 - December 12, 2025

### What Changed
Prompt suggestions introduced (Tab to accept). Thinking mode enabled by default for Opus 4.5. Enhanced `/permissions` search. MCP server loading fixes.

### What It Means
Two workflow-changing features in one release:

**Prompt Suggestions:**
As you type, Claude may suggest completions based on common patterns and your project context. Press Tab to accept, or keep typing to ignore. This speeds up:
- Common commands and file paths
- Repeated patterns from your session
- Contextual suggestions based on current task

**Opus 4.5 Extended Thinking:**
When using Opus 4.5, extended thinking is now ON by default. You'll see more thorough reasoning on complex tasks without needing to enable it manually. Use `Alt+T` to toggle if needed.

---

## 🐛 v2.0.66 - December 11, 2025

No release notes available - likely hotfix.

---

## ✨ v2.0.65 - December 11, 2025

### What Changed
Model switching while typing (`alt+p`/`option+p`). Context window status line info. Custom `@` file search commands.

### What It Means
Switch models mid-prompt without losing input. See remaining context capacity before compaction kicks in.

---

## 🚀 v2.0.64 - December 10, 2025

### What Changed
Instant auto-compacting. Asynchronous agent/bash execution. Named session support. `/stats` command. `.claude/rules/` directory support.

### What It Means
This release fundamentally changes how you interact with Claude Code by enabling true parallel workflows.

**Async Execution:**
Background agents and bash commands can now run asynchronously. When a long-running task starts, press `Ctrl+B` to send it to the background and continue working. The background task will notify the main agent when it needs attention - no polling required.

Practical use cases:
- Research while coding - Background agent researches an API while main agent prepares integration code
- Parallel reviews - Background agent reviews each PR phase, notifying only on critical issues
- Concurrent exploration - Multiple agents search different parts of the codebase simultaneously

**`.claude/rules/` Directory:**
Instead of one monolithic CLAUDE.md, you can now organize project instructions into multiple files:
```
.claude/rules/
├── coding-standards.md
├── testing-requirements.md
├── security-policies.md
└── team-conventions.md
```
Each file is loaded automatically. Great for team projects where different people own different rule sets.

**Named Sessions:**
Save and resume specific conversation states. Fork a session to experiment, then resume the original. Use `/stats` to see usage metrics.

### How to Use It
- **Background tasks:** Press `Ctrl+B` while agent/command is running
- **View tasks:** Run `/tasks` to see all background processes
- **Rules directory:** Create `.claude/rules/` and add `.md` files

### Learn More
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Memory & Rules Docs](https://code.claude.com/docs/en/memory)
- [Async Workflows Guide](https://claudefa.st/blog/guide/agents/async-workflows)

---

## 🐛 v2.0.63 - December 9, 2025

No release notes available - likely hotfix between 2.0.62 and 2.0.64.

---

## 🔧 v2.0.62 - December 9, 2025

### What Changed
"(Recommended)" indicator for multiple-choice questions. Custom commit byline settings. Fixed symlinked skill directories.

### What It Means
Claude can mark preferred options. Customize the AI commit byline (instead of default Co-Authored-By).

---

## 🐛 v2.0.61 - December 7, 2025

### What Changed
Reverted VSCode multiple terminal client support due to responsiveness issues.

### What It Means
Stability rollback. VSCode users who experienced lag should see improvement.

---

## 🚀 v2.0.60 - December 6, 2025

### What Changed
Background agent support. `--disable-slash-commands` flag. Model name in commit messages. `/mcp enable/disable` server toggles.

### What It Means
This release introduced the foundation for background execution that v2.0.64 expanded upon.

**Background Agents:**
Sub-agents can now run in the background, returning results when complete. This works with both built-in agents (plan, explore, etc.) and custom agents in `.claude/agents/`. The main agent doesn't block waiting for sub-agents to finish.

**MCP Server Toggles:**
New `/mcp enable <server>` and `/mcp disable <server>` commands let you toggle MCP servers on/off without editing config files. Useful for:
- Debugging MCP issues by disabling servers one at a time
- Temporarily disabling expensive or slow servers
- Testing configurations quickly

**Other changes:**
- `--disable-slash-commands` flag for headless/automation scenarios
- Model name now appears in commit messages for traceability

### How to Use It
```bash
/mcp disable github      # Temporarily disable GitHub MCP
/mcp enable github       # Re-enable it
/mcp                     # List all servers and their status
```

---

## 🚀 v2.0.59 - December 4, 2025

### What Changed
`--agent` CLI flag and agent setting for custom system prompts and tool restrictions.

### What It Means
This release enables custom agent personas - specialized versions of Claude with their own system prompts and restricted tool sets. Each agent operates in its own context window, preventing task pollution.

**Why This Matters:**
Instead of one Claude that does everything, you can create focused agents:
- **Code Reviewer** - Read-only access, focused on finding issues
- **Security Auditor** - Limited tools, security-focused prompts
- **Documentation Writer** - File access only, documentation expertise
- **Research Agent** - Web search and reading, no file modifications

**How Agents Work:**
Agents are defined in Markdown files with YAML frontmatter:
```markdown
---
name: code-reviewer
description: Reviews code for quality and bugs
allowed_tools: [Read, Grep, Glob]
---

You are a senior code reviewer. Focus on:
- Logic errors and edge cases
- Performance issues
- Security vulnerabilities
Never modify files, only report findings.
```

**Agent Locations:**
- Project agents: `.claude/agents/`
- Personal agents: `~/.claude/agents/`

**Automatic Delegation:**
Claude can automatically invoke custom agents for matching tasks, similar to how it invokes tools. You can also use `--append-system-prompt` to give each persona specialized expertise.

### How to Use It
```bash
claude --agent code-reviewer    # Launch with specific agent
/agents                         # List available agents in TUI
```

### Learn More
- [Custom Agents Guide](https://claudelog.com/mechanics/custom-agents/)
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Token Optimization with Personas](https://decoding.io/2025/08/solving-token-waste-with-claude-code-personas/)

---

## ✨ v2.0.58 - December 3, 2025

### What Changed
Pro users gain Opus 4.5 access. Fixed timer display. Windows managed settings location.

### What It Means
**Opus 4.5 for Pro Subscribers:**
Previously Opus 4.5 was only available via API. Now Pro plan subscribers can use it directly in Claude Code. This brings the most capable model to the consumer tier - better reasoning, 50% fewer tokens, and stronger coding performance.

Use `/model opus` to switch, or start with `claude --model opus`.

---

## 🔧 v2.0.57 - December 3, 2025

### What Changed
Feedback input when rejecting plans. VSCode streaming message support.

### What It Means
Explain why you're rejecting a plan - helps Claude understand preferences for next attempt.

---

## 🔧 v2.0.56 - December 2, 2025

### What Changed
Terminal progress bar toggle. VSCode secondary sidebar support (v1.97+).

### What It Means
Hide progress bar if distracting. Place Claude Code in VSCode's right sidebar.

---

## 🔧 v2.0.55 - November 27, 2025

### What Changed
Fixed proxy DNS forcing. Improved memory location navigation. Enhanced AskUserQuestion tool. Better fuzzy matching.

### What It Means
Corporate/proxy network users see better connectivity. Clarification dialogs are more polished.

---

## ✨ v2.0.54 - November 26, 2025

### What Changed
Hooks can process PermissionRequest suggestions. VSCode preferred location setting. `Cmd+N`/`Ctrl+N` new conversation shortcut.

### What It Means
**Hooks Can Intercept Permissions:**
Hooks gained a significant new capability - they can now intercept and process permission requests before they're shown to you. Use cases:
- Auto-approve certain operations based on patterns
- Log all permission requests for audit
- Modify or filter permissions programmatically
- Implement custom approval workflows

This is powerful for automation scenarios where you want to pre-configure which operations are allowed.

**Keyboard Shortcut:**
`Cmd+N` (Mac) or `Ctrl+N` (Linux/Windows) starts a fresh conversation instantly.

---

## 🐛 v2.0.53 - November 25, 2025

No release notes available - likely hotfix between 2.0.52 and 2.0.54.

---

## 🔧 v2.0.52 - November 25, 2025

### What Changed
Fixed duplicate messages. `/usage` progress bars. Image pasting on Linux Wayland. Bash `$!` variable support.

### What It Means
Linux Wayland users can paste images directly. `$!` (last background PID) works in bash.

---

## 🚀 v2.0.51 - November 24, 2025

### What Changed
**Opus 4.5 introduced**. Claude Code Desktop launched. Improved plan mode precision. Clarified usage limit notifications.

### What It Means
This is the most significant release of 2025 - introducing both a new frontier model and a desktop application.

**Claude Opus 4.5:**
Anthropic's newest and most capable model, released November 24, 2025. Key improvements:

*Coding Performance:*
- State-of-the-art on SWE-bench (80.9%) - the industry standard for software engineering
- Cuts token usage in half compared to previous Opus while maintaining quality
- Especially strong at code migration, refactoring, and multi-file changes

*Agentic Capabilities:*
- Excels at long-horizon, autonomous tasks requiring sustained reasoning
- One of the strongest tool-using models available - powers agents across hundreds of tools
- Self-improving: agents can refine their own capabilities, reaching peak performance in 4 iterations

*Technical Specs:*
- 200,000 token context window
- 64,000 token output limit
- March 2025 knowledge cutoff
- Pricing: $5/M input, $25/M output (much cheaper than previous Opus at $15/$75)
- Supports `effort` parameter to control reasoning depth

*Safety:*
- Most robust against prompt injection of any frontier model

**Claude Code Desktop:**
A standalone GUI application for Claude Code:
- Run multiple local and remote sessions in parallel
- Git worktree support - multiple isolated sessions in same repo
- Clean UI with option to open in VS Code or resume in CLI
- Enhanced planning with Opus 4.5 - clarifying questions upfront, user-editable plans

Available to Max, Pro, Team, and Enterprise users.

### How to Use It
```bash
/model opus              # Switch to Opus 4.5 in Claude Code
claude --model opus      # Start with Opus 4.5
```

For Desktop: Download from [claude.com/download](https://claude.com/download)

### Learn More
- [Introducing Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- [What's New in Claude 4.5](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-5)
- [Claude Code Desktop Docs](https://code.claude.com/docs/en/desktop)
- [Claude Download Page](https://claude.com/download)

---

## 🔧 v2.0.50 - November 21, 2025

### What Changed
Fixed MCP nested reference handling. Improved ultrathink display. Refined session limit warnings.

### What It Means
MCP tools with nested data structures work correctly. Extended thinking display is cleaner.

---

## 🔧 v2.0.49 - November 21, 2025

### What Changed
Added readline-style `Ctrl+Y` for pasting deleted text. Improved clarity of usage limit warning message. Fixed handling of subagent permissions.

### What It Means
Standard readline paste shortcut now works. Usage warnings are clearer.

---

## 🐛 v2.0.47 - November 20, 2025

Improved error messages for `claude --teleport`. Fixed Vertex AI config not applying from settings.json. Fixed race condition with history entry logging at exit.

---

## 🐛 v2.0.46 - November 20, 2025

Fixed image files being reported with incorrect media type when format cannot be detected from metadata.

---

## 🚀 v2.0.45 - November 19, 2025

### What Changed
Added support for Azure AI Foundry. Added `PermissionRequest` hook to automatically approve or deny tool permission requests. Send background tasks to Claude Code on the web by starting a message with `&`.

### What It Means
**Azure AI Foundry Support:**
Claude Code now supports Azure's AI platform alongside direct API, Bedrock, and Vertex. This gives enterprise Azure users native integration.

**PermissionRequest Hook:**
A powerful automation primitive - hooks can now intercept permission requests programmatically. Use cases:
- Auto-approve specific file patterns or directories
- Deny dangerous operations automatically
- Log all permission requests for audit trails
- Implement custom approval workflows

**Background Tasks with `&`:**
Start any message with `&` to send it as a background task. The web interface gains the same async capabilities as the CLI.

### How to Use It
```javascript
// PermissionRequest hook example
{
  "hooks": {
    "PermissionRequest": {
      "command": "my-approval-script",
      "timeout": 5000
    }
  }
}
```

---

## ✨ v2.0.43 - November 18, 2025

### What Changed
Added `permissionMode` field for custom agents. Added `tool_use_id` field to hook input types. Added `skills` frontmatter field to declare skills for subagents. Added the `SubagentStart` hook event.

### What It Means
Custom agents can now declare their own permission mode (plan, auto-approve, etc.) in frontmatter. The new `SubagentStart` hook lets you intercept when subagents spawn. Skills can be explicitly declared for subagents to use.

---

## 🚀 v2.0.42 - November 17, 2025

### What Changed
Introduced a new Plan subagent for plan mode. Added ability for Claude to resume subagents dynamically. Claude can now select which model subagents should use. SDK received a `--max-budget-usd` flag. Fixed terminal setup adding backslash to Shift+Enter in VS Code. Added branch/tag support for git-based plugins using fragment syntax.

### What It Means
**Plan Subagent:**
Plan mode now uses a dedicated subagent optimized for architectural planning. This improves plan quality and separates planning context from execution context.

**Subagent Resume:**
Subagents can be resumed mid-task. If a subagent needs more context or hits an issue, the parent agent can resume it with additional information rather than starting fresh.

**Model Selection for Subagents:**
Claude can choose which model each subagent uses based on task complexity. Simple tasks get Haiku for speed/cost, complex tasks get Opus for capability.

**SDK Budget Flag:**
`--max-budget-usd` limits spending in headless/automation scenarios. Essential for production deployments.

---

## ✨ v2.0.41 - November 14, 2025

### What Changed
Model parameter now available for prompt-based stop hooks. Plugin output styles can be shared and installed. SDK supports custom hook timeouts. Additional safe git commands run without approval. Fixed many bugs including slash commands loading twice, plugin hook timeouts, Bedrock duplicate Opus entries.

### What It Means
**Plugin Output Styles:**
Output styles (how Claude formats responses) can now be packaged as plugins and shared. Install community-created styles or publish your own.

**More Git Commands Auto-Approved:**
Common read-only git commands now run automatically without prompting, reducing permission fatigue during normal git workflows.

---

## 🔧 v2.0.37 - November 11, 2025

### What Changed
Corrected idleness computation for notifications. Added matcher values for Notification hook events. Added "keep-coding-instructions" option to output styles frontmatter.

### What It Means
Notification hooks can now match on specific notification types. Output styles can preserve coding instructions when switching styles.

---

## 🐛 v2.0.36 - November 8, 2025

Fixed `DISABLE_AUTOUPDATER` environment variable not working. Fixed queued messages being executed as bash commands. Prevented input loss when typing during queued message processing.

---

## 🔧 v2.0.35 - November 7, 2025

### What Changed
Improved fuzzy search results. VSCode respects `chat.fontSize` and `chat.fontFamily` settings. SDK added `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` environment variable. Migrated `ignorePatterns` to deny permissions.

### What It Means
Better file path suggestions. VSCode font customization works throughout Claude Code UI.

---

## ✨ v2.0.34 - November 6, 2025

### What Changed
VSCode Extension: New setting to configure initial permission mode. Native Rust-based fuzzy finder improves file path suggestion performance. Fixed infinite token refresh loop with OAuth MCP servers. Memory crash when reading/writing large files resolved.

### What It Means
**Native Rust Fuzzy Finder:**
File path suggestions are significantly faster thanks to a Rust-based fuzzy matching implementation. This is especially noticeable in large codebases.

**VSCode Permission Mode Setting:**
Configure whether Claude starts in plan mode, auto-approve, or default permission mode via VSCode settings.

---

## 🔧 v2.0.33 - November 5, 2025

### What Changed
Native binary installs launch quicker. `claude doctor` symlink resolution improved. Fixed `claude mcp serve` exposing tools with incompatible outputSchemas.

### What It Means
Faster startup times for native installations. MCP server tooling is more robust.

---

## 🔧 v2.0.32 - November 4, 2025

### What Changed
Output styles un-deprecated based on community feedback. Added `companyAnnouncements` setting for startup announcements. Fixed hook progress messages not updating during PostToolUse execution.

### What It Means
Output styles were briefly deprecated but restored due to community demand. Enterprise deployments can show announcements at startup.

---

## 🔧 v2.0.31 - November 1, 2025

### What Changed
Windows native installation uses "shift+tab" for mode switching. Vertex: Web Search support added for supported models. VSCode: `respectGitIgnore` configuration for `.gitignored` files. Fixed subagents and MCP servers "Tool names must be unique" error. `/compact` command failure with "prompt_too_long" resolved.

### What It Means
Windows users get consistent keyboard shortcuts. Google Vertex users can use web search through Claude. Tool name collision bugs fixed.

---

## Summary: November - December 2025

**41 releases total (v2.0.31 - v2.0.76):**
- 🚀 **8 Major**: Opus 4.5, Desktop app, LSP tool, Chrome control, background agents, custom agents, Azure AI + PermissionRequest hook, Plan subagent
- ✨ **9 Notable**: Prompt suggestions, model switching, MCP wildcards, async execution, hooks permissions, agent permissionMode, plugin output styles, Rust fuzzy finder
- 🔧 **14 Minor**: UI polish, keyboard shortcuts, platform fixes, performance improvements, prompt cleanup
- 🐛 **10 Patches**: Bug fixes, reverts, hotfixes
