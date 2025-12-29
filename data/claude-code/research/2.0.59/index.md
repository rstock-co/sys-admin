# Claude Code v2.0.59 - Deep Research

**Release Date:** December 4, 2025
**Tier:** 🚀 Major - Custom agent personas
**Symbiont Relevance:** 🔧 Medium - Interesting but NOT a replacement for folder-based SGTAs
**Researched:** 2025-12-29

---

## Summary

v2.0.59 introduced the `--agent` CLI flag and agent setting for custom system prompts and tool restrictions. This allows defining specialized agent personas with their own toolsets, models, and permission modes. However, research reveals that `--agent` **ignores CLAUDE.md**, making it unsuitable as a replacement for folder-based SGTA architecture despite providing full 200k context.

---

## What Changed

### New Features
- **`--agent` CLI flag** - Specify an agent for the current session
- **Agent setting** - Configure default agent in settings
- **Custom system prompts** - Define agent-specific instructions
- **Tool restrictions** - Limit which tools an agent can use
- **Per-agent permission modes** - Set permissionMode per agent

---

## Deep Dive: `--agent` Flag

### How It Works

Define agent files in `.claude/agents/` (project) or `~/.claude/agents/` (user):

```markdown
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Reviews code for quality and bugs
tools: Read, Grep, Glob
model: sonnet
permissionMode: default
skills: review-skill
---

You are a senior code reviewer. Focus on:
- Logic errors and edge cases
- Performance issues
- Security vulnerabilities

Never modify files, only report findings.
```

Run with:
```bash
claude --agent code-reviewer
```

### Frontmatter Options

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase + hyphens) |
| `description` | Yes | When to use this agent |
| `tools` | No | Comma-separated tool list. Inherits ALL if omitted |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Skills to auto-load (NOT inherited from parent) |

### Agent File Locations

| Type | Location | Scope |
|------|----------|-------|
| Project agents | `.claude/agents/` | Current project only |
| User agents | `~/.claude/agents/` | All projects |

---

## Critical Finding: Context and CLAUDE.md

### The Good News

**`--agent` spawns a FULL session with full 200k context.**

It's NOT a subagent with truncated context. When you run `claude --agent health-coach`, you get the same 200k context window as a normal Claude Code session.

### The Bad News

**`--agent` IGNORES CLAUDE.md.**

The agent file's system prompt **replaces** everything. Your working directory's CLAUDE.md is not loaded.

| Method | Full Context | Loads CLAUDE.md |
|--------|--------------|-----------------|
| `claude` (normal) | ✅ 200k | ✅ Yes |
| `claude --agent X` | ✅ 200k | ❌ No |
| `claude --append-system-prompt "..."` | ✅ 200k | ✅ Yes |
| Subagent (Task tool) | ❌ Truncated | N/A |

---

## Comparison: `--agent` vs Folder-Based SGTAs

### Current Symbiont Approach (Folder-Based)

```
mycelium/health-coach/
├── CLAUDE.md          # Persona - loaded automatically
├── output-style.md    # Voice - loaded automatically
├── .claude/
│   └── rules/         # Modular rules (v2.0.64)
└── core/ → symlink    # Shared primitives across all specialists
```

Spawning:
```bash
alacritty --working-directory ~/symbiont/mycelium/health-coach -e claude
```

### `--agent` Approach

```
~/.claude/agents/
└── health-coach.md    # Everything in one file
```

Spawning:
```bash
claude --agent health-coach
```

### Feature Comparison

| Aspect | Folder-Based | `--agent` |
|--------|--------------|-----------|
| Context window | Full 200k ✅ | Full 200k ✅ |
| CLAUDE.md loading | Automatic ✅ | Ignored ❌ |
| Output style separation | Separate file ✅ | Must inline ❌ |
| `.claude/rules/` support | Yes ✅ | No (CLAUDE.md ignored) ❌ |
| Symlinked core/ | Works ✅ | N/A - single file ❌ |
| Tool restrictions | No (full toolkit) | Yes ✅ |
| Per-agent permissionMode | No | Yes ✅ |
| Per-agent model | No | Yes ✅ |
| Maintenance | Modular, easy ✅ | Monolithic ❌ |

---

## Symbiont Impact Assessment

### Why `--agent` Is NOT Right for SGTAs

The SGTA architecture relies on:

1. **Modular configuration** - CLAUDE.md, output-style.md, rules/ as separate files
2. **Symlinked core/** - Shared primitives across all specialists
3. **Easy maintenance** - Change one file, don't rewrite everything
4. **Output style separation** - Voice is distinct from instructions

`--agent` would force everything into one monolithic file per specialist. Every time you update shared behavior, you'd have to update every agent file.

### Where `--agent` DOES Make Sense

**Quick, focused personas that don't need elaborate maintenance:**

- **code-reviewer** - Read-only, focused on finding issues
- **security-auditor** - Limited tools, security prompts
- **documentation-writer** - File access only
- **research-agent** - Web search, no file modifications

**Tool restrictions:**

If you want a specialist that literally cannot write files, `--agent` with restricted `tools` is the only way. Folder-based approach gives full toolkit.

**Within Mycelia:**

Mycelia could spawn `--agent` based quick helpers for specific tasks, while SGTAs remain folder-based for full specialist sessions.

### Revised Relevance Rating

Initial assessment said "THIS IS the SGTA pattern." After research: **No, it's not.**

| Use Case | Right Approach |
|----------|----------------|
| Complex specialists with modular config | Folder-based ✅ |
| Quick focused personas | `--agent` ✅ |
| Tool-restricted helpers | `--agent` ✅ |
| Specialists sharing core/ primitives | Folder-based ✅ |
| Evolving specialists needing maintenance | Folder-based ✅ |

---

## Related Flags

### `--append-system-prompt`

Appends to the default Claude Code prompt while keeping CLAUDE.md loading:

```bash
claude --append-system-prompt "Always respond in a warm, coaching tone"
```

This could be useful for adding specialist flavor without replacing everything.

| Flag | Replaces Default | Loads CLAUDE.md |
|------|------------------|-----------------|
| `--agent` | Yes | No |
| `--system-prompt` | Yes | No |
| `--append-system-prompt` | No (appends) | Yes |

### Potential Hybrid Approach

```bash
# Folder-based for CLAUDE.md + output-style
# Plus appended tone guidance
cd ~/symbiont/mycelium/health-coach
claude --append-system-prompt "Remember: warm, compassionate, biohacker voice"
```

But this is redundant if output-style.md already handles voice.

---

## Feature Deep Dives

| Feature | File | Status |
|---------|------|--------|
| `--agent` flag | (this file) | ✅ Documented |
| Frontmatter options | agent-frontmatter.md | 📝 Pending |
| Tool restrictions | tool-restrictions.md | 📝 Pending |

---

## Action Items

1. **Keep folder-based SGTAs** - They're the right architecture
2. **Consider `--agent` for quick helpers** - Code reviewer, security auditor
3. **Test tool restrictions** - Could be useful for read-only specialists
4. **Don't migrate specialists to `--agent`** - Would lose modularity benefits

---

## Sources

### Official Documentation
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents) - Agent file format
- [CLI Reference](https://code.claude.com/docs/en/cli-reference) - Flag documentation
- [Output Styles](https://code.claude.com/docs/en/output-styles) - Style vs agent comparison

---

*Research completed: 2025-12-29*
