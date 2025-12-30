# Claude Code v2.0.73 - Deep Research

**Release Date:** December 19, 2025
**Tier:** ✨ Notable
**Symbiont Relevance:** 🔧 Medium
**Researched:** December 29, 2025

## Summary

Version 2.0.73 added search filtering to the plugin discovery screen, allowing users to filter by name, description, or marketplace. Also included clickable image links, alt-y kill ring (yank-pop), and custom session ID support for forking.

## What Changed

- Search filtering on plugin discovery screen (type to filter by name, description, or marketplace)
- Clickable `[Image #N]` links open attachments in default viewer
- `alt-y` yank-pop for input history cycling (Emacs-style kill ring)
- Custom session ID support with `--session-id` flag when using resume/continue/fork-session
- Performance fixes for input history navigation
- Enhanced `/theme` command
- VSCode tab icon badges for permissions/completions

## Deep Dive: Plugin Search Filtering

The plugin search feature in v2.0.73 is a quality-of-life improvement for the plugin discovery workflow. Prior to this release, users had to scroll through all available plugins in all added marketplaces. Now you can type to filter results instantly.

### How It Works

When you run `/plugin` and navigate to the **Discover** tab, you can now type a search query. The filter matches against:

1. **Plugin name** - e.g., "code-review" or "frontend"
2. **Plugin description** - e.g., "security" or "PR workflow"
3. **Marketplace source** - e.g., "anthropics" or "community"

Results update in real-time as you type, making it much faster to find relevant plugins in a growing ecosystem.

### How to Use It

```bash
# Open plugin manager
/plugin

# Navigate to Discover tab (Tab key)
# Start typing to filter - e.g., "security"
# Results filter instantly
```

## Symbiont Impact

**Relevance: 🔧 Medium**

This release doesn't touch core Symbiont dependencies (output styles, CLAUDE.md, MCP, hooks). However:

1. **Kill ring (`alt-y`)** - Useful across parallel specialist sessions. When copying/pasting between Mycelia and specialists, yank-pop lets you access earlier clipboard entries.

2. **Plugin search** - As the plugin ecosystem grows, faster discovery helps find tools that could enhance specialists. Especially relevant as output styles can now be packaged as plugins (v2.0.41).

3. **Session ID on fork** - Could be useful for specialist session management, though current hotkey approach doesn't use session forking.

**Action Items:** None required. QoL improvements only.

---

# The Complete Claude Code Plugins Guide

## What Are Claude Code Plugins?

Plugins are lightweight, shareable packages that extend Claude Code with custom functionality. They were introduced in v2.0.13 (October 2025) and are now in public beta.

A plugin can bundle any combination of:

| Component | Purpose |
|-----------|---------|
| **Slash Commands** | Custom `/commands` for frequently-used operations |
| **Agents** | Specialized AI assistants with custom expertise |
| **Skills** | Auto-invoked behaviors for specific contexts |
| **Hooks** | Event handlers that run at key workflow points |
| **MCP Servers** | Connections to external tools and data sources |

## Why Plugins Matter

Before plugins, sharing Claude Code customizations meant copying files between machines, documenting setup steps, and hoping nothing broke. Plugins solve this by:

1. **Single-command install** - One `/plugin install` gets everything working
2. **Versioning** - Plugins have versions, updates are tracked
3. **Discoverability** - Marketplaces let you browse what's available
4. **Enable/disable** - Toggle plugins on/off without uninstalling
5. **Team distribution** - Private marketplaces for organization-wide tools

## Plugin Directory Structure

Every plugin lives in its own directory:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (REQUIRED)
├── commands/                 # Slash commands (optional)
│   ├── my-command.md
│   └── another-command.md
├── agents/                   # Specialized agents (optional)
│   └── my-agent.md
├── skills/                   # Agent Skills (optional)
│   └── my-skill/
│       └── SKILL.md
├── hooks/                    # Event handlers (optional)
│   └── my-hook.md
├── .mcp.json                 # MCP server config (optional)
└── README.md                 # Documentation
```

**IMPORTANT:** Only `plugin.json` goes inside `.claude-plugin/`. All other directories (commands/, agents/, etc.) must be at the plugin root level.

## The Manifest File

Every plugin requires `.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

Claude Code uses this metadata in the plugin manager display.

## Creating Slash Commands

Commands are Markdown files in the `commands/` directory. The filename becomes the command name, prefixed with the plugin namespace.

Example: `commands/hello.md` in a plugin named `my-plugin` creates `/my-plugin:hello`

```markdown
# Hello Command

Say hello to the user with their name.

## Instructions

When this command is invoked, greet the user warmly and ask how you can help them today.
```

## Creating Agents

Agents are Markdown files in the `agents/` directory with YAML frontmatter:

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

## Creating Skills

Skills auto-invoke based on context. Each skill needs its own subdirectory with a `SKILL.md` file:

```
skills/
└── frontend-design/
    └── SKILL.md
```

Skills are automatically invoked when relevant (e.g., frontend-design activates during UI work).

## Creating Hooks

Hooks respond to events in Claude Code's workflow:

| Hook Event | Trigger |
|------------|---------|
| `SessionStart` | When a new session begins |
| `PreToolUse` | Before a tool is executed |
| `PostToolUse` | After a tool completes |
| `PermissionRequest` | When Claude needs permission |
| `SubagentStart` | When a subagent spawns |
| `Notification` | When notifications fire |

Example hook file:

```markdown
---
event: PreToolUse
matcher:
  tool: Bash
---

Before running bash commands, verify they don't contain dangerous operations like `rm -rf /`.
```

## Installing Plugins

### From the Official Marketplace

The Anthropic marketplace is automatically available:

```bash
# Open plugin manager
/plugin

# Go to Discover tab
# Browse and install
```

### From Third-Party Marketplaces

```bash
# Add a marketplace
/plugin marketplace add user-or-org/repo-name

# Or add from Git URL
/plugin marketplace add https://github.com/user/marketplace.git

# Then browse and install from /plugin Discover tab
```

### Direct Installation

```bash
# Install specific plugin from a marketplace
/plugin install plugin-name@marketplace-name
```

### Using the Community CLI

For faster installation without adding marketplaces:

```bash
npx claude-plugins install @anthropics/claude-code-plugins/code-review
```

## Managing Plugins

```bash
# Open plugin manager
/plugin

# Tabs available:
# - Discover: browse available plugins
# - Installed: manage installed plugins
# - Marketplaces: manage marketplace sources
# - Errors: view plugin loading errors

# Enable/disable without uninstalling
/plugin enable plugin-name
/plugin disable plugin-name

# Uninstall
/plugin uninstall plugin-name

# List all marketplaces
/plugin marketplace list

# Remove a marketplace (uninstalls its plugins too)
/plugin marketplace remove marketplace-name
```

**Shortcuts:** `/plugin market` works for `/plugin marketplace`, and `rm` works for `remove`.

## Testing Plugins During Development

Use the `--plugin-dir` flag to load a plugin without installing:

```bash
claude --plugin-dir ./my-plugin
```

This loads your plugin directly from the local directory. Iterate quickly without install/uninstall cycles.

## Creating Your Own Marketplace

A marketplace is just a Git repository with `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-marketplace",
  "description": "My curated plugins",
  "plugins": [
    {
      "name": "plugin-one",
      "path": "plugins/plugin-one",
      "version": "1.0.0"
    },
    {
      "name": "plugin-two",
      "path": "plugins/plugin-two",
      "version": "2.0.0"
    }
  ]
}
```

Host on GitHub, GitLab, or any Git server. Users add it with:

```bash
/plugin marketplace add your-username/your-marketplace
```

## Official Plugins from Anthropic

Anthropic maintains 14 official plugins:

| Plugin | Purpose |
|--------|---------|
| **code-review** | 5 parallel agents for PR review with confidence scoring |
| **feature-dev** | 7-phase feature development workflow |
| **plugin-dev** | 8-phase guided plugin creation |
| **pr-review-toolkit** | 6 specialized PR review agents |
| **commit-commands** | Git workflow automation (`/commit`, `/commit-push-pr`) |
| **hookify** | Custom hook creation |
| **security-guidance** | PreToolUse hook for security monitoring |
| **frontend-design** | Auto-invoked skill for UI guidance |
| **agent-sdk-dev** | Agent SDK development toolkit |
| **learning-output-style** | Educational mode for learning |
| **explanatory-output-style** | Detailed implementation explanations |
| **ralph-wiggum** | Autonomous iteration loops |
| **claude-opus-4-5-migration** | Model migration helper |

## Community Resources

- [claude-plugins.dev](https://claude-plugins.dev/) - Community registry with CLI
- [claudecodemarketplace.com](https://claudecodemarketplace.com/) - Plugin directory
- [GitHub: awesome-claude-code-plugins](https://github.com/hekmon8/awesome-claude-code-plugins) - Curated list

## Security Considerations

1. **Review source code** before installing plugins
2. **MCP integrations** may access external systems
3. **Hooks can intercept** all tool calls
4. **Only install from trusted** marketplaces and authors
5. **Test in isolation** before using in production projects

## Plugin Auto-Updates

Marketplaces can be configured for auto-updates:

```bash
# Enable auto-update for a marketplace
/plugin marketplace auto-update marketplace-name on

# Disable
/plugin marketplace auto-update marketplace-name off
```

When enabled, Claude Code refreshes marketplaces and updates installed plugins at startup.

---

## Sources

- [Official Plugin Documentation](https://code.claude.com/docs/en/plugins)
- [Discover Plugins Guide](https://code.claude.com/docs/en/discover-plugins)
- [Anthropic Blog: Claude Code Plugins](https://claude.com/blog/claude-code-plugins)
- [GitHub: Official Plugins](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)
- [Community CLI](https://claude-plugins.dev/)
- [Plugin Structure Guide](https://claude-plugins.dev/skills/@anthropics/claude-plugins-official/plugin-structure)
