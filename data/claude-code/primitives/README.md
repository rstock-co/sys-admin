# Claude Code Primitives

> **Last sync check:** 2025-10-30 | **Update:** Deprecated features removed

This directory contains documentation for all Claude Code extensibility primitives provided by Anthropic.

## What are Claude Code Primitives?

Claude Code primitives are the core extensibility mechanisms built into Claude Code by Anthropic. These primitives allow developers to customize, extend, and automate Claude Code's behavior without modifying its core functionality.

## Available Primitives

### 1. **Hooks** (`CLAUDE_CODE_HOOKS.md`, `CLAUDE_CODE_HOOKS_REFERENCE.md`)
Event-driven automation that executes shell commands at specific points in Claude Code's lifecycle.

**Hook Events:**
- PreToolUse - Runs before tool calls (can block them)
- PostToolUse - Runs after tool calls complete
- UserPromptSubmit - Runs when user submits a prompt
- Notification - Runs when Claude Code sends notifications
- Stop - Runs when Claude Code finishes responding
- SubagentStop - Runs when subagent tasks complete
- PreCompact - Runs before compaction operations
- SessionStart - Runs when sessions begin or resume
- SessionEnd - Runs when sessions end

**Use Cases:**
- Automatic code formatting
- Logging and compliance tracking
- Custom notifications
- File protection
- Automated feedback

### 2. **Slash Commands** (`CLAUDE_CODE_SLASH_COMMANDS.md`)
User-invoked commands prefixed with `/` that trigger specific actions or workflows.

**Types:**
- Built-in commands (system-provided)
- Custom commands (project or personal)

**Features:**
- Namespacing support
- Arguments passing
- Bash command execution

**Use Cases:**
- Workflow automation
- Code generation templates
- Project-specific utilities
- Testing and deployment shortcuts

### 3. **Skills** (`CLAUDE_CODE_SKILLS.md`)
Model-invoked capabilities that extend Claude's autonomous decision-making.

**Characteristics:**
- Filesystem-based (`.claude/skills/`)
- Automatic discovery and loading
- Progressive loading (metadata → instructions → resources)
- Personal or project-based

**Structure:**
- `SKILL.md` with YAML frontmatter
- Name and description fields
- Step-by-step guidance
- Optional resources/utilities

**Use Cases:**
- Domain expertise packaging
- Organizational knowledge sharing
- Frequent capability reuse
- Context-specific guidance

### 4. **Subagents** (`CLAUDE_CODE_SUBAGENTS.md`)
Specialized agents for complex, multi-step tasks that require deep analysis.

**Features:**
- Automatic delegation
- Explicit invocation
- Chaining capabilities
- Isolated context

**Use Cases:**
- Complex code analysis
- Multi-step refactoring
- Specialized domain work
- Research and synthesis

### 5. **MCP Servers** (`CLAUDE_CODE_MCP_SERVERS.md`)
Model Context Protocol integrations for connecting to external tools and services.

**Types:**
- HTTP servers
- SSE servers
- stdio servers

**Features:**
- Remote and local tool access
- Automatic startup
- Configuration management

**Use Cases:**
- External API integration
- Custom tool development
- Service connectivity
- Data source access

### 6. **Plugins** (`CLAUDE_CODE_PLUGINS.md`)
Packaged extensions that bundle multiple primitives together.

**Components:**
- Commands
- Agents
- Skills
- Hooks
- MCP Servers

**Features:**
- Marketplace distribution
- Version management
- Dependency handling

**Use Cases:**
- Complete feature packages
- Team-wide standardization
- Third-party extensions
- Reusable toolsets

### 7. **Status Line Configuration** (`CLAUDE_CODE_STATUS_LINE_CONFIGURATION.md`)
Custom display at the bottom of Claude Code interface showing contextual information.

**Features:**
- Updates every 300ms
- JSON input with session context
- ANSI color support
- Shell script execution

**Use Cases:**
- Current model display
- Working directory info
- Git branch information
- Cost tracking
- Custom context display


## Choosing the Right Primitive

**Use Hooks when:**
- You need deterministic, automatic behavior
- Actions must always execute at specific points
- You're implementing formatting, logging, or validation

**Use Slash Commands when:**
- Users need explicit control over invocation
- You're creating workflows or templates
- Actions are too specific for autonomous use

**Use Skills when:**
- Claude should decide when to use the capability
- The functionality is frequently needed
- You want autonomous, context-aware behavior

**Use Subagents when:**
- Tasks require deep, specialized analysis
- Multi-step complex reasoning is needed
- You want isolated context for specific work

**Use MCP Servers when:**
- Integrating with external systems
- Building custom tools
- Connecting to APIs or databases

**Use Plugins when:**
- Bundling multiple primitives together
- Distributing complete feature sets
- Standardizing across teams

**Use Status Line when:**
- Displaying persistent contextual information
- Monitoring session state
- Showing dynamic environment data

## File Naming Convention

All files follow the pattern:
- `CLAUDE_CODE_<PRIMITIVE_NAME>.md`

This matches the URL structure from docs.anthropic.com:
- URL: `https://docs.claude.com/en/docs/claude-code/hooks`
- File: `CLAUDE_CODE_HOOKS.md`

## For AI Assistants

When helping users with Claude Code extensibility:

1. **Understand the use case** - Different primitives serve different purposes
2. **Recommend the simplest solution** - Don't over-engineer with complex primitives
3. **Consider combinations** - Many solutions use multiple primitives together
4. **Security first** - Hooks run with full credentials, emphasize security review

## Related Documentation

- Main SDK documentation: `../sdk/`
- General Claude Code docs: `../`
- Project instructions: `../../../CLAUDE.md`

## Maintenance

These files are copied from official Anthropic documentation. Check for updates periodically as Claude Code evolves.
