---
name: plugin-finder
description: |
  Find and recommend Claude Code plugins from the curated registry. Use when user asks about plugins, wants recommendations, needs to find a plugin for a specific task, or asks "what plugins exist for X". Searches by category, use case, framework, provider, or quality tier.
---

# Plugin Finder

**Find the right Claude Code plugin for any task using a curated, tagged registry.**

## When to Use This Skill

Use when:
- User asks "what plugins are there for X?"
- User wants plugin recommendations for a task
- User asks about MCP servers or integrations
- User wants to compare plugins
- User asks "how do I integrate with X?" (where X is a service like Stripe, GitHub, etc.)
- User is starting a new project and needs tooling suggestions

**Trigger keywords**: plugin, plugins, MCP, integration, find plugin, recommend plugin, what's available, marketplace

## Search Tool

**Always use `search.py` instead of reading `registry.json` directly** - this saves tokens.

```bash
# Location
/home/neo/agents/sys-admin/.claude/skills/plugin-finder/search.py

# Basic usage
python search.py --tier tier-1              # All tier-1 plugins
python search.py --category workflow        # All workflow plugins
python search.py --type mcp                 # All MCP servers
python search.py --usecase git-workflow     # Git workflow plugins
python search.py --framework laravel        # Laravel plugins
python search.py --search stripe            # Search name/description

# Combine filters
python search.py --tier tier-1 --type mcp   # Tier-1 MCP servers
python search.py --provider vendor -v       # Vendor plugins (verbose)

# Output options
python search.py --tier tier-1 -v           # Verbose (full details)
python search.py --tier tier-1 --count      # Count only
python search.py --tier tier-1 --json       # JSON output

# List available filter values
python search.py --list categories          # List all categories
python search.py --list types               # List component types
python search.py --list usecases            # List all use cases
python search.py --list tiers               # List quality tiers

# Marketplace sources
python search.py --marketplaces             # List all plugin sources
python search.py --marketplaces -v          # Verbose with URLs and stats
python search.py --marketplaces --json      # JSON output
python search.py --marketplaces -s mcp      # Search marketplaces
```

## Core Resources

| File | Purpose |
|------|---------|
| [search.py](search.py) | **CLI search tool** - Token-efficient filtering |
| [data/registry.json](data/registry.json) | **Plugin registry** - Individual plugins |
| [data/marketplaces.json](data/marketplaces.json) | **Marketplace registry** - Plugin sources |
| [data/PLUGINS.md](data/PLUGINS.md) | **Human-readable guide** - Detailed descriptions |

## Registry Schema

The registry uses a comprehensive tagging system for filtering:

### Categories
| Category | Description |
|----------|-------------|
| `development` | Languages, frameworks, code tools, LSPs |
| `infrastructure` | Deployment, cloud, databases, hosting |
| `productivity` | Project management, docs, communication |
| `design` | UI/UX, design tools, design-to-code |
| `commerce` | Payments, e-commerce |
| `security` | Auth, scanning, compliance |
| `monitoring` | Observability, errors, analytics |
| `ai-ml` | AI/ML tools, model integration |
| `workflow` | Claude Code experience, automation, time-savers |

### Component Types
| Type | Description |
|------|-------------|
| `mcp` | MCP server integration (external tools) |
| `commands` | Slash commands |
| `agents` | Subagents |
| `hooks` | Event handlers |
| `skills` | Model-invoked capabilities |
| `lsp` | Language server protocol |

### Provider Tiers
| Tier | Description |
|------|-------------|
| `anthropic` | Anthropic-maintained (highest trust) |
| `vendor` | First-party (Stripe, GitHub, etc.) |
| `community` | Third-party developers |

### Quality Tiers
| Tier | Criteria |
|------|----------|
| `tier-1` | 10k+ stars OR official vendor |
| `tier-2` | 1k-10k stars, active maintenance |
| `tier-3` | 100-1k stars, maintained |
| `tier-4` | <100 stars or new |

### Use Case Tags
```
code-review, git-workflow, testing, debugging, documentation,
database, api-integration, deployment, ci-cd, code-generation,
refactoring, search, payments, auth, notifications, calendar,
email, chat, file-management, browser-automation, design-to-code,
commit-automation, pr-workflow, session-management, output-formatting,
permission-handling, hook-automation, prompt-enhancement, context-management,
dev-environment, repetitive-tasks, code-intelligence, type-checking,
security-scanning
```

## Workflows

### 1. Find Plugins by Task

**When user asks**: "What plugins help with X?" / "I need a plugin for Y"

```bash
python search.py --usecase <use-case> -v
# or search by keyword
python search.py --search <keyword> -v
```

Present top matches with install command: `/plugin install {name}@claude-plugins-official`

### 2. Find Plugins by Category

**When user asks**: "Show me all workflow plugins" / "What productivity tools exist?"

```bash
python search.py --category workflow
python search.py --category productivity -v
```

### 3. Find Plugins for a Framework

**When user asks**: "What plugins work with Laravel?" / "React plugins?"

```bash
python search.py --framework laravel -v
python search.py --framework react -v
```

### 4. Compare Plugins

**When user asks**: "Should I use X or Y?" / "Compare these plugins"

```bash
python search.py --search plugin1 --json
python search.py --search plugin2 --json
```

Compare on stars, provider tier, component types, use cases.

### 5. Find Time-Saving / QoL Plugins

**When user asks**: "What plugins save time?" / "QoL plugins?"

```bash
python search.py --category workflow -v
python search.py --usecase commit-automation -v
```

### 6. Find by Quality/Trust

```bash
python search.py --tier tier-1           # Highest quality
python search.py --provider anthropic    # Anthropic-maintained
python search.py --provider vendor       # First-party vendors
```

## Response Format

When recommending plugins, use this format:

```markdown
## Recommended: {Plugin Name}

**Category:** {category} | **Provider:** {provider} | **Quality:** {qualityTier}

{Description}

**Why this fits:** {1-2 sentences on why this matches their need}

**Install:**
```
/plugin install {name}@claude-plugins-official
```

**Token cost:** {Low/Medium/High} - {explanation if MCP with many tools}
```

## Token Cost Guidance

Warn users about MCP token overhead:

| Tools | Estimated Overhead | Warning Level |
|-------|-------------------|---------------|
| 1-5 | ~100-500 tokens | Low - no warning needed |
| 5-15 | ~500-2,000 tokens | Medium - mention it |
| 15-30 | ~2,000-5,000 tokens | High - warn user |
| 30+ | ~5,000+ tokens | Very High - explicit warning |

**Known high-token MCP servers:**
- GitHub (~40 tools) - ~4,000-6,000 tokens
- Stripe (~20 tools) - ~2,000-4,000 tokens
- Context7 (2 tools) - ~200-400 tokens (lightweight)

## Updating the Registry

When new plugins are discovered or stats change:

1. **Edit `data/registry.json`** with new plugin data
2. **Update `data/PLUGINS.md`** with descriptions
3. **Update `lastUpdated` field** in registry.json
4. **Fetch fresh GitHub stats** for external plugins

## External Plugin Discovery

To find new plugins beyond the official marketplace:

1. **Search GitHub**:
   ```
   WebSearch("claude code plugin github 2025")
   WebSearch("claude-plugins marketplace github")
   ```

2. **Check awesome lists**:
   - https://github.com/ccplugins/awesome-claude-code-plugins
   - https://github.com/hekmon8/awesome-claude-code-plugins

3. **Verify quality before adding**:
   - Check stars and maintenance
   - Review code for security
   - Test functionality
   - Only add tier-2 or better

---

**Remember**: Always recommend tier-1 and vendor plugins first. Community plugins should come with appropriate caveats about trust and maintenance.
