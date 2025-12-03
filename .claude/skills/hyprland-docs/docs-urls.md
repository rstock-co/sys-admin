# Hyprland Documentation Source URLs

Quick reference for copying official docs into skill files.

## Configuring/

| File | Source URL |
|------|------------|
| `hyprland-conf.md` | https://wiki.hyprland.org/Configuring/Configuring-Hyprland/ |
| `monitors.md` | https://wiki.hyprland.org/Configuring/Monitors/ |
| `variables.md` | https://wiki.hyprland.org/Configuring/Variables/ |
| `keywords.md` | https://wiki.hyprland.org/Configuring/Keywords/ |
| `binds.md` | https://wiki.hyprland.org/Configuring/Binds/ |
| `window-rules.md` | https://wiki.hyprland.org/Configuring/Window-Rules/ |
| `workspace-rules.md` | https://wiki.hyprland.org/Configuring/Workspace-Rules/ |
| `dispatchers.md` | https://wiki.hyprland.org/Configuring/Dispatchers/ |
| `animations.md` | https://wiki.hyprland.org/Configuring/Animations/ |
| `decorations.md` | https://wiki.hyprland.org/Configuring/Variables/#decoration (section) |
| `colors.md` | https://wiki.hyprland.org/Configuring/Variables/#general (colors section) |
| `input.md` | https://wiki.hyprland.org/Configuring/Variables/#input |
| `gestures.md` | https://wiki.hyprland.org/Configuring/Variables/#gestures |
| `dwindle-layout.md` | https://wiki.hyprland.org/Configuring/Dwindle-Layout/ |
| `master-layout.md` | https://wiki.hyprland.org/Configuring/Master-Layout/ |
| `environment-variables.md` | https://wiki.hyprland.org/Configuring/Environment-variables/ |
| `advanced-config.md` | https://wiki.hyprland.org/Configuring/Advanced-config/ |
| `xwayland.md` | https://wiki.hyprland.org/Configuring/XWayland/ |

## Usage/

| File | Source URL |
|------|------------|
| `hyprctl.md` | https://wiki.hyprland.org/Configuring/Using-hyprctl/ |
| `startup.md` | https://wiki.hyprland.org/Configuring/Keywords/ (exec, exec-once section) |
| `workspaces.md` | https://wiki.hyprland.org/Configuring/Workspace-Rules/ |

## Troubleshooting/

| File | Source URL |
|------|------------|
| `common-issues.md` | https://wiki.hyprland.org/FAQ/ |
| `monitors.md` | https://wiki.hyprland.org/FAQ/ (monitor section) + https://wiki.hyprland.org/Configuring/Monitors/ (troubleshooting notes) |
| `performance.md` | https://wiki.hyprland.org/Configuring/Performance/ (if exists) or compile from Variables page |

## Priority Order for Copying

1. ✅ **monitors.md** - CRITICAL for your 3× 4K setup
2. ✅ **hyprland-conf.md** - Main config reference
3. ✅ **binds.md** - Keybindings
4. ✅ **window-rules.md** - Window management
5. ✅ **workspace-rules.md** - Workspace config
6. ✅ **hyprctl.md** - Debugging and runtime control
7. ✅ **dispatchers.md** - Available commands
8. ✅ **variables.md** - Complete variable reference
9. ✅ **animations.md** - Animation config
10. ✅ **input.md** - Keyboard/mouse settings

## How to Copy

1. Visit URL in browser
2. View page source or use browser's "Copy as Markdown" extension
3. Or manually copy the markdown content from GitHub: https://github.com/hyprwm/hyprland-wiki
4. Paste into corresponding file in `docs/`
5. Keep formatting intact

## Alternative: Clone Wiki Repo

```bash
cd /tmp
git clone https://github.com/hyprwm/hyprland-wiki.git
cd hyprland-wiki/pages/Configuring
# Copy files directly to skill docs/
```

## Notes

- Some files (decorations.md, colors.md, input.md) may need content extracted from Variables.md sections
- startup.md content is in Keywords.md under exec/exec-once
- common-issues.md and monitors.md troubleshooting sections come from FAQ.md
- Keep all official examples and syntax intact
