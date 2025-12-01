# Claude Code Documentation Context

> **Note**: This skill covers usage, configuration, and GitHub integration only. For creating primitives (hooks, skills, slash commands, etc.), see the `primitive-builder` skill.

This directory contains official Anthropic documentation for using and configuring Claude Code.

## Purpose

Authoritative documentation for Claude Code usage, configuration, and GitHub integration. Allows AI assistants to provide accurate information without web access for common queries.

## File Structure

```
docs/
├── usage/                         # How to operate Claude Code
│   ├── interactive-mode.md        # Interactive sessions
│   ├── headless-mode.md          # Headless/API usage
│   ├── web-interface.md          # Web UI features
│   ├── cli-reference.md          # CLI commands
│   ├── common-workflows.md       # Typical workflows
│   ├── checkpointing.md          # Session management
│   └── costs.md                  # Token/cost tracking
│
├── configuration/                 # How to configure Claude Code
│   ├── settings.md               # All settings
│   ├── memory.md                 # Memory system
│   ├── model.md                  # Model selection
│   ├── status-line.md            # Status line config
│   └── terminal.md               # Terminal settings
│
└── github/                        # GitHub integration with Claude Code
    └── actions.md                # GitHub Actions
```

## Coverage

**Usage**: Operating modes (interactive, headless, web), CLI commands, workflows, checkpointing, cost tracking

**Configuration**: Settings, memory system, model selection, status line, terminal

**GitHub**: Actions integration, CI/CD workflows

## Not Covered

**Primitives creation** (hooks, skills, slash commands, subagents, MCP, plugins) - Use `primitive-builder` skill instead.

## Adding Documentation

1. Navigate to page on https://docs.claude.com/
2. Click "Copy page" button → "Copy page as Markdown for LLMs"
3. Create file in appropriate subdirectory (usage/, configuration/, github/)
4. Name file descriptively (kebab-case.md)
5. Paste content

## For AI Assistants

**Progressive reading**: Load only relevant files based on query:
- Settings question? → `configuration/settings.md`
- CLI question? → `usage/cli-reference.md`
- GitHub question? → `github/actions.md`

**Do NOT preload all docs** - wastes tokens. Read only what's needed.

**Creating primitives?** → Invoke `primitive-builder` skill, not this one.

## Maintenance

Check for documentation updates periodically on Anthropic site. Local copies may become outdated.
