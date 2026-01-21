# System Configuration Index

Central registry of all system subsystems. Each subsystem has one source of truth in `config/`.

---

## Subsystems

| Subsystem | Status | Config Doc | System Paths | Quick Fix |
|-----------|--------|------------|--------------|-----------|
| **voice** | Working | [voice/hyprwhspr.md](voice/hyprwhspr.md) | `~/.config/hyprwhspr/config.json` | `fix-voice` |
| **display** | Working | [display/monitors.md](display/monitors.md) | `~/.config/hypr/hyprland.conf` | `wake-tv` or `hyprctl reload` |
| **audio** | Working | [audio/speakers.md](audio/speakers.md) | PipeWire (no config needed) | `systemctl --user restart pipewire wireplumber` |
| **keyboard** | Working | [keyboard/yunzii-al98.md](keyboard/yunzii-al98.md) | `~/.config/hypr/hyprland.conf`, VIA app | - |
| **gpu** | Working (workarounds) | [gpu/arc-b580.md](gpu/arc-b580.md) | xe driver, BIOS settings | See doc (driver issues) |
| **recording** | Working | [recording/screen-recording.md](recording/screen-recording.md) | `~/.config/swayimg/config` | `rec-tv`, `frames` |

---

## How to Use This Index

1. **Find a subsystem** - Look up by name or browse the table
2. **Read the config doc** - Single source of truth for that subsystem
3. **Quick fix first** - If something's broken, try the quick fix command
4. **Check system paths** - Actual config file locations on the system

---

## Adding New Subsystems

1. Create `config/<subsystem-name>/<name>.md`
2. Add entry to this index table
3. Include: current setup, common issues, diagnostic commands, historical reference
4. Update troubleshooting skill aliases if needed

---

## Known Issues

| Issue | Since | Status | Workaround |
|-------|-------|--------|------------|
| **paru broken** | 2025-12-16 | Waiting for upstream fix | Use `sudo pacman -Syu` directly. The `alpm` Rust crate needs update for new libalpm API. |

---

## Related Files

- **CLAUDE.md** - Agent instructions (references this index)
- **SYSTEM_SETUP.md** - High-level system decisions and package choices
- **SYSTEM_SPECS.md** - Hardware specifications
- **.claude/skills/troubleshooting/** - Troubleshooting skill (references config docs)
