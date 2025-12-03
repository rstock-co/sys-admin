# Hyprland Documentation Skill

Official Hyprland documentation skill for symbiont-sysadmin specialist.

## Purpose

Prevents hallucination by forcing the specialist to read official Hyprland documentation from GitHub before configuring anything.

## How It Works

The skill provides:
1. **Direct GitHub URLs** to all Hyprland wiki markdown files
2. **DeepWiki MCP integration** (recommended) for fetching docs
3. **WebFetch fallback** using raw GitHub URLs
4. **Mandatory reading rule**: Agent MUST read docs before configuring

## Structure

```
hyprland-docs/
├── SKILL.md                          # Skill definition with all GitHub URLs
└── README.md                         # This file
```

## Zero Maintenance Required

- No local documentation files to maintain
- Always up-to-date (fetches from GitHub)
- Agent reads directly from source
- No copy/paste needed

## Usage by Specialist

When symbiont-sysadmin needs Hyprland config help:

1. **Skill loads** - Agent sees all GitHub URLs organized by category
2. **Agent identifies** what needs to be configured (monitors, binds, etc.)
3. **Agent fetches** relevant markdown file using DeepWiki or WebFetch
4. **Agent reads** the COMPLETE documentation
5. **Agent applies** exact official syntax to `~/.config/hypr/hyprland.conf`
6. **Agent tests** with `hyprctl reload`

## Example Workflow

**User**: "Configure my 3 monitors in Hyprland"

**Sysadmin**:
1. Loads `hyprland-docs` skill
2. Sees: Monitors.md URL
3. Fetches: `DeepWiki("hyprwm/hyprland-wiki", "Show me Monitors.md")`
4. Reads: Complete monitor configuration documentation
5. Applies: Exact syntax for 3× 4K setup with portrait transforms
6. Tests: `hyprctl monitors`

## Documentation Coverage

All major Hyprland configuration areas:
- ✅ Monitors (multi-display, transforms, refresh rates)
- ✅ Keybindings (window/workspace management)
- ✅ Window rules (per-application behavior)
- ✅ Workspace rules (multi-monitor workspaces)
- ✅ Animations (bezier curves, performance)
- ✅ Variables (complete config reference)
- ✅ Dispatchers (available commands)
- ✅ Layouts (dwindle, master)
- ✅ Environment variables
- ✅ XWayland compatibility
- ✅ hyprctl (runtime control)
- ✅ FAQ (troubleshooting)

## Benefits

**Zero hallucination**: Official docs only, fetched on-demand
**Always current**: Reads from GitHub main branch
**No maintenance**: No local files to update
**Fast lookup**: URLs organized by category in SKILL.md
**System-aware**: Includes user's 3× 4K setup context

## DeepWiki Integration

The skill recommends using DeepWiki MCP server (already installed) because:
- Optimized for GitHub repository documentation
- Better context extraction from markdown
- Faster than WebFetch for repository docs
- Handles repo structure intelligently

Fallback to WebFetch with raw GitHub URLs if DeepWiki has issues.

---

**This skill ensures symbiont-sysadmin never guesses Hyprland configuration syntax.**
