---
name: hyprland-docs
description: |
  Official Hyprland documentation from GitHub wiki for Wayland compositor configuration, monitor setup, keybindings, animations, window rules, and workspace management. ALWAYS read relevant GitHub markdown files BEFORE configuring Hyprland.
---

# Hyprland Documentation (GitHub Wiki)

**Official Hyprland wiki documentation - always read before configuring.**

## CRITICAL RULE

**YOU MUST read the complete relevant markdown file(s) from GitHub BEFORE performing any Hyprland configuration task.**

Never configure Hyprland from memory or assumptions. Always fetch and read the official docs first.

## When to Use This Skill

Use when you need to **CONFIGURE or TROUBLESHOOT** Hyprland:

- **Monitor configuration** - Multi-monitor setup, resolution, refresh rate, transforms
- **Keybindings** - Window management, workspace switching, custom binds
- **Window rules** - Application-specific behavior, floating windows, workspace assignments
- **Animations** - Bezier curves, animation configuration, performance tuning
- **Workspaces** - Multi-monitor workspace management, switching, moving windows
- **Startup** - Autostart applications, exec-once commands
- **Input** - Keyboard layouts, mouse settings, touchpad configuration
- **General settings** - Gaps, borders, colors, layouts

**Trigger keywords**: hyprland config, monitor setup, keybindings, window rules, animations, workspaces, hyprland.conf, display configuration

## GitHub Wiki Structure

**Base URL**: `https://github.com/hyprwm/hyprland-wiki/tree/main/content`

All documentation is in markdown format and organized by category.

## Documentation URLs by Category

### Configuration (Most Important)

**Configuring Hyprland (Overview)**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Configuring-Hyprland.md`
- When: Starting Hyprland config, understanding config file structure

**Monitors** ⭐ CRITICAL for your 3× 4K setup
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Monitors.md`
- When: Setting up displays, resolution, refresh rate, portrait mode (transforms)

**Variables (Complete Reference)**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Variables.md`
- When: Need complete list of all config options, default values

**Binds (Keybindings)**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Binds.md`
- When: Setting up keybindings for window/workspace management

**Window Rules**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Window-Rules.md`
- When: Per-application window behavior, floating windows, workspace assignments

**Workspace Rules**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Workspace-Rules.md`
- When: Multi-monitor workspace configuration, persistent workspaces

**Dispatchers (Commands)**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Dispatchers.md`
- When: Available commands for keybindings, what actions can be bound

**Animations**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Animations.md`
- When: Configuring animations, bezier curves, performance tuning

**Keywords (Syntax)**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Keywords.md`
- When: Understanding config file syntax, exec/exec-once, source, etc.

### Layouts

**Dwindle Layout**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Dwindle-Layout.md`
- When: Using dwindle tiling layout (default)

**Master Layout**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Master-Layout.md`
- When: Using master-stack layout (alternative)

### Advanced Configuration

**Environment Variables**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Environment-variables.md`
- When: Setting Wayland/graphics environment variables

**Advanced Config**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Advanced-config.md`
- When: Advanced features, debug options

**XWayland**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/XWayland.md`
- When: Running X11 apps on Wayland, compatibility settings

### Usage & Tools

**Using hyprctl**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Using-hyprctl.md`
- When: Runtime control, query monitors/windows, reload config, debugging

### Troubleshooting

**FAQ (Common Issues)**
- URL: `https://github.com/hyprwm/hyprland-wiki/blob/main/content/FAQ.md`
- When: Troubleshooting problems, monitors not detected, performance issues

## How to Use This Skill

### Step-by-Step Process

1. **Identify what you need to configure** (monitors, binds, window rules, etc.)

2. **Find the relevant GitHub URL above** (e.g., Monitors.md for display setup)

3. **Fetch and READ the complete markdown file** using WebFetch with raw GitHub URL:
   ```
   WebFetch(
     url: "https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/[filename].md",
     prompt: "Return the complete markdown content of this file"
   )
   ```

4. **Extract the relevant syntax/examples** from the fetched content

5. **Apply configuration** to `~/.config/hypr/hyprland.conf` using exact official syntax

6. **Test the configuration**:
   ```bash
   hyprctl reload  # Reload config without restart
   # OR
   # Restart Hyprland (Super+M to exit, log back in)
   ```

7. **Verify results**:
   ```bash
   hyprctl monitors      # Check monitor config
   hyprctl clients       # Check window rules
   hyprctl workspaces    # Check workspace setup
   ```

## Using WebFetch to Read Documentation

**Use WebFetch with raw GitHub URLs to fetch official documentation.**

### Why WebFetch Works Well

- ✅ No MCP server installation required
- ✅ Direct access to raw markdown files
- ✅ Always fetches latest from main branch
- ✅ Simple and reliable

### How to Use WebFetch

For each documentation file, convert the GitHub URL to raw format:

**GitHub URL format**:
```
https://github.com/hyprwm/hyprland-wiki/blob/main/content/Configuring/Monitors.md
```

**Raw URL format** (use this with WebFetch):
```
https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Monitors.md
```

**WebFetch pattern**:
```
WebFetch(
  url: "https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/[FILE].md",
  prompt: "Return the complete markdown content"
)
```

### Raw URLs by Category

All URLs follow the pattern:
`https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/[category]/[filename].md`

**Examples**:
- Monitors: `.../content/Configuring/Monitors.md`
- Binds: `.../content/Configuring/Binds.md`
- Window Rules: `.../content/Configuring/Window-Rules.md`
- FAQ: `.../content/FAQ.md`

## System Context

User's setup:
- **3× 4K monitors**: TCL 55" center@120Hz + 2× Samsung 32" portrait@60Hz
- **GPU**: Intel Arc B580 (DisplayPort 2.1)
- **Use case**: Development workstation (Alacritty, tmux, VS Code, browser)
- **Layout**: Center landscape + 2× portrait sides

## Priority Configuration Areas

For this system, focus on:

1. **Monitors.md** - 3-monitor 4K setup with portrait transforms
2. **Workspace-Rules.md** - Per-monitor workspace assignments
3. **Binds.md** - Keybindings for 6 workspaces (2 per monitor)
4. **Window-Rules.md** - Application-specific behavior (VS Code, Alacritty, browser)
5. **Variables.md** - General settings (gaps, borders, colors)

## Example Workflow

**Task**: Configure 3× 4K monitors with portrait side displays

1. **Read docs**:
   ```
   WebFetch(
     url: "https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Monitors.md",
     prompt: "Return the complete markdown content"
   )
   ```

2. **Extract syntax**:
   ```conf
   monitor=DP-1,3840x2160@120,2160x0,1
   monitor=DP-2,3840x2160@60,0x0,1,transform,1
   monitor=DP-3,3840x2160@60,6000x0,1,transform,1
   ```

3. **Apply to config**:
   ```bash
   Edit ~/.config/hypr/hyprland.conf
   ```

4. **Test**:
   ```bash
   hyprctl reload
   hyprctl monitors  # Verify
   ```

## Important Reminders

- ⚠️ **ALWAYS read the GitHub docs before configuring** - never configure from memory
- ⚠️ **Use exact official syntax** - Hyprland config is sensitive to format
- ⚠️ **Test with `hyprctl reload`** before full restart
- ⚠️ **Use `hyprctl monitors`** to verify detected displays
- ⚠️ **Transform values**: 0=normal, 1=90°, 2=180°, 3=270°
- ⚠️ **Read COMPLETE files** - don't just search for snippets, get full context

## Quick Reference: Raw URLs for Common Files

**Configuration**:
- Monitors: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Monitors.md`
- Binds: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Binds.md`
- Window Rules: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Window-Rules.md`
- Workspace Rules: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Workspace-Rules.md`
- Variables: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Variables.md`
- Animations: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Animations.md`

**Usage**:
- hyprctl: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Using-hyprctl.md`

**Troubleshooting**:
- FAQ: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/FAQ.md`

---

**Remember: ALWAYS read the official documentation from GitHub BEFORE configuring Hyprland. Use WebFetch to access the raw markdown files. Zero hallucination, zero guessing.**
