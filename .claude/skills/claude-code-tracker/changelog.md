# Claude Code Changelog

Internal changelog with plain-language explanations of Claude Code releases.

**Detailed entries are in monthly files:** `changelog/YYYY-MM.md`

**Legend:**
| Emoji | Meaning |
|-------|---------|
| 🚀 | **Major** - Game-changing features, new capabilities |
| ✨ | **Notable** - Significant improvements, workflow enhancements |
| 🔧 | **Minor** - Small enhancements, QoL improvements |
| 🐛 | **Patch** - Bug fixes only, no new features |

---

## Quick Reference (All Releases)

| Version | Date | Tier | Summary | File |
|---------|------|------|---------|------|
| 2.1.50 | Feb 21 | ✨ | Worktree hooks, claude agents CLI, Opus 4.6 1M context, memory leak fixes | [2026-02](changelog/2026-02.md) |
| 2.1.49 | Feb 20 | 🚀 | --worktree flag, ConfigChange hook, agent background:true, Ctrl+F kill | [2026-02](changelog/2026-02.md) |
| 2.1.47 | Feb 18 | 🔧 | SessionStart hook deferred, memory optimization, file mention caching | [2026-02](changelog/2026-02.md) |
| 2.1.46 | Feb 17 | 🔧 | claude.ai MCP connectors, macOS orphaned process fix | [2026-02](changelog/2026-02.md) |
| 2.1.45 | Feb 17 | ✨ | **Sonnet 4.6**, plugins from --add-dir, deferred schema loading | [2026-02](changelog/2026-02.md) |
| 2.1.42 | Feb 13 | 🔧 | Auth CLI subcommands, /rename auto-generation, @-mention anchors | [2026-02](changelog/2026-02.md) |
| 2.1.39 | Feb 11 | 🔧 | Nested session guard, agent teams model fix, MCP image crash fix | [2026-02](changelog/2026-02.md) |
| 2.1.38 | Feb 10 | 🐛 | Tab autocomplete restored, heredoc security fix, sandbox protection | [2026-02](changelog/2026-02.md) |
| 2.1.37 | Feb 9 | 🐛 | Fast mode fix after /extra-usage | [2026-02](changelog/2026-02.md) |
| 2.1.36 | Feb 7 | 🔧 | Fast mode for Opus 4.6 via /fast | [2026-02](changelog/2026-02.md) |
| 2.1.34 | Feb 6 | 🐛 | Agent teams render crash fix, sandbox bypass prevention | [2026-02](changelog/2026-02.md) |
| 2.1.33 | Feb 6 | ✨ | TeammateIdle/TaskCompleted hooks, tmux messaging, memory frontmatter | [2026-02](changelog/2026-02.md) |
| 2.1.32 | Feb 5 | 🚀 | **Opus 4.6**, Agent Teams, auto memory, summarize from here | [2026-02](changelog/2026-02.md) |
| 2.1.31 | Feb 4 | 🔧 | Session resume hint, PDF fix, plan mode crash prevention | [2026-02](changelog/2026-02.md) |
| 2.1.30 | Feb 3 | ✨ | PDF page ranges, /debug command, 68% session resume memory optimization | [2026-02](changelog/2026-02.md) |
| 2.1.29 | Jan 31 | 🐛 | Startup performance fix for sessions with saved_hook_context | [2026-01](changelog/2026-01.md) |
| 2.1.27 | Jan 30 | ✨ | --from-pr flag, debug logging for tool calls, Claude in Chrome VSCode | [2026-01](changelog/2026-01.md) |
| 2.1.25 | Jan 29 | 🐛 | Beta header validation fix for Bedrock/Vertex gateway users | [2026-01](changelog/2026-01.md) |
| 2.1.23 | Jan 29 | 🔧 | Custom spinner verbs, mTLS/proxy fixes, merged PR purple indicator | [2026-01](changelog/2026-01.md) |
| 2.1.22 | Jan 28 | 🐛 | Structured outputs fix for non-interactive mode | [2026-01](changelog/2026-01.md) |
| 2.1.21 | Jan 28 | 🔧 | Japanese IME support, VSCode Python venv activation, session resume | [2026-01](changelog/2026-01.md) |
| 2.1.20 | Jan 27 | 🚀 | PR review status, --add-dir CLAUDE.md loading, task deletion | [2026-01](changelog/2026-01.md) |
| 2.1.19 | Jan 23 | ✨ | $0/$1 argument shorthand, VSCode session forking, skills auto-allow | [2026-01](changelog/2026-01.md) |
| 2.1.18 | Jan 23 | ✨ | /keybindings command, chord sequences, per-context keybindings | [2026-01](changelog/2026-01.md) |
| 2.1.17 | Jan 22 | 🐛 | AVX instruction support crash fix | [2026-01](changelog/2026-01.md) |
| 2.1.16 | Jan 22 | 🚀 | Native task system with dependency tracking, VSCode plugin management | [2026-01](changelog/2026-01.md) |
| 2.1.15 | Jan 21 | 🔧 | npm deprecation notice, React Compiler perf, MCP stdio fix | [2026-01](changelog/2026-01.md) |
| 2.1.14 | Jan 20 | ✨ | History autocomplete, plugin pinning, context window fix (65%→98%) | [2026-01](changelog/2026-01.md) |
| 2.1.12 | Jan 17 | 🐛 | Message rendering bug fix | [2026-01](changelog/2026-01.md) |
| 2.1.11 | Jan 17 | 🔧 | MCP HTTP/SSE connection fix | [2026-01](changelog/2026-01.md) |
| 2.1.10 | Jan 17 | ✨ | New "Setup" hook event, OAuth copy shortcut | [2026-01](changelog/2026-01.md) |
| 2.1.9 | Jan 16 | 🚀 | PreToolUse additionalContext, plansDirectory, session URL attribution | [2026-01](changelog/2026-01.md) |
| 2.1.7 | Jan 14 | ✨ | Customizable keybindings.json, showTurnDuration, MCP auto mode | [2026-01](changelog/2026-01.md) |
| 2.1.6 | Jan 13 | ✨ | Nested skill discovery, /config search, /stats date filtering | [2026-01](changelog/2026-01.md) |
| 2.1.5 | Jan 12 | 🐛 | CLAUDE_CODE_TMPDIR env var | [2026-01](changelog/2026-01.md) |
| 2.1.4 | Jan 10 | 🔧 | CLAUDE_CODE_DISABLE_BACKGROUND_TASKS env var | [2026-01](changelog/2026-01.md) |
| 2.1.3 | Jan 9 | ✨ | Unified slash commands + skills model, release channel toggle | [2026-01](changelog/2026-01.md) |
| 2.1.2 | Jan 9 | 🔧 | Security fix, memory leak fix, clickable hyperlinks | [2026-01](changelog/2026-01.md) |
| 2.1.0 | Jan 9 | 🚀 | Skill hot-reload, context:fork, Vim motions, /plan command | [2026-01](changelog/2026-01.md) |
| 2.0.76 | Dec 22 | 🐛 | No prompt changes, likely infrastructure fixes | [2025-12](changelog/2025-12.md) |
| 2.0.75 | Dec 20 | 🔧 | Prompt cleanup (-183 tokens), removed redundant Task tool guidance | [2025-12](changelog/2025-12.md) |
| 2.0.74 | Dec 19 | 🚀 | LSP tool for code intelligence (go-to-def, references, hover) | [2025-12](changelog/2025-12.md) |
| 2.0.73 | Dec 19 | ✨ | Clickable images, alt-y kill ring, plugin search | [2025-12](changelog/2025-12.md) |
| 2.0.72 | Dec 18 | 🚀 | Claude in Chrome (Beta) - browser automation | [2025-12](changelog/2025-12.md) |
| 2.0.71 | Dec 16 | 🔧 | Prompt suggestion toggle, glob permission fix | [2025-12](changelog/2025-12.md) |
| 2.0.70 | Dec 16 | ✨ | Wildcard MCP permissions, Enter for suggestions | [2025-12](changelog/2025-12.md) |
| 2.0.69 | Dec 13 | 🐛 | Minor bugfixes | [2025-12](changelog/2025-12.md) |
| 2.0.68 | Dec 12 | 🔧 | CJK/IME fix, enterprise managed settings | [2025-12](changelog/2025-12.md) |
| 2.0.67 | Dec 12 | ✨ | Prompt suggestions (Tab), Opus 4.5 thinking default | [2025-12](changelog/2025-12.md) |
| 2.0.66 | Dec 11 | 🐛 | Hotfix | [2025-12](changelog/2025-12.md) |
| 2.0.65 | Dec 11 | ✨ | Model switching (alt+p), context window indicator | [2025-12](changelog/2025-12.md) |
| 2.0.64 | Dec 10 | 🚀 | Async agents/bash, .claude/rules/, /stats, named sessions | [2025-12](changelog/2025-12.md) |
| 2.0.63 | Dec 9 | 🐛 | Hotfix | [2025-12](changelog/2025-12.md) |
| 2.0.62 | Dec 9 | 🔧 | "(Recommended)" indicator, custom commit byline | [2025-12](changelog/2025-12.md) |
| 2.0.61 | Dec 7 | 🐛 | Reverted VSCode multi-terminal (caused lag) | [2025-12](changelog/2025-12.md) |
| 2.0.60 | Dec 6 | 🚀 | Background agents, /mcp enable/disable toggles | [2025-12](changelog/2025-12.md) |
| 2.0.59 | Dec 4 | 🚀 | --agent flag for custom agent personas | [2025-12](changelog/2025-12.md) |
| 2.0.58 | Dec 3 | ✨ | Pro users get Opus 4.5 access | [2025-12](changelog/2025-12.md) |
| 2.0.57 | Dec 3 | 🔧 | Feedback on plan rejection, VSCode streaming | [2025-12](changelog/2025-12.md) |
| 2.0.56 | Dec 2 | 🔧 | Progress bar toggle, VSCode secondary sidebar | [2025-12](changelog/2025-12.md) |
| 2.0.55 | Nov 27 | 🔧 | Proxy DNS fix, fuzzy matching improvements | [2025-11](changelog/2025-11.md) |
| 2.0.54 | Nov 26 | ✨ | Hooks can modify permissions, Cmd+N shortcut | [2025-11](changelog/2025-11.md) |
| 2.0.53 | Nov 25 | 🐛 | Hotfix | [2025-11](changelog/2025-11.md) |
| 2.0.52 | Nov 25 | 🔧 | Linux Wayland image paste, $! variable support | [2025-11](changelog/2025-11.md) |
| 2.0.51 | Nov 24 | 🚀 | **Opus 4.5**, Claude Code Desktop launched | [2025-11](changelog/2025-11.md) |
| 2.0.50 | Nov 21 | 🔧 | MCP nested refs fix, ultrathink display | [2025-11](changelog/2025-11.md) |
| 2.0.49 | Nov 21 | 🔧 | Readline Ctrl+Y paste, usage limit clarity | [2025-11](changelog/2025-11.md) |
| 2.0.47 | Nov 20 | 🐛 | Teleport errors, Vertex config fix | [2025-11](changelog/2025-11.md) |
| 2.0.46 | Nov 20 | 🐛 | Image media type detection fix | [2025-11](changelog/2025-11.md) |
| 2.0.45 | Nov 19 | 🚀 | Azure AI Foundry, PermissionRequest hook, `&` background | [2025-11](changelog/2025-11.md) |
| 2.0.43 | Nov 18 | ✨ | Agent permissionMode, skills frontmatter, SubagentStart hook | [2025-11](changelog/2025-11.md) |
| 2.0.42 | Nov 17 | 🚀 | Plan subagent, agent resume, model selection for subagents | [2025-11](changelog/2025-11.md) |
| 2.0.41 | Nov 14 | ✨ | Plugin output styles sharing, SDK hook timeouts | [2025-11](changelog/2025-11.md) |
| 2.0.37 | Nov 11 | 🔧 | Notification hook matchers, output style options | [2025-11](changelog/2025-11.md) |
| 2.0.36 | Nov 8 | 🐛 | Autoupdater disable fix, input loss fix | [2025-11](changelog/2025-11.md) |
| 2.0.35 | Nov 7 | 🔧 | Native Rust fuzzy finder, VSCode font settings | [2025-11](changelog/2025-11.md) |
| 2.0.34 | Nov 6 | ✨ | Native Rust fuzzy finder, VSCode permission mode | [2025-11](changelog/2025-11.md) |
| 2.0.33 | Nov 5 | 🔧 | Faster native binary launch, doctor improvements | [2025-11](changelog/2025-11.md) |
| 2.0.32 | Nov 4 | 🔧 | Output styles un-deprecated, company announcements | [2025-11](changelog/2025-11.md) |
| 2.0.31 | Nov 1 | 🔧 | Windows shift+tab, Vertex web search support | [2025-11](changelog/2025-11.md) |
