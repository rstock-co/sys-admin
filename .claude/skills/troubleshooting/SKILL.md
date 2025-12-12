---
description: Troubleshoot system services. Use when user reports something isn't working (voice, keyboard, audio, display, gpu).
---

# Troubleshooting Skill

You are troubleshooting a system issue. The user will tell you what's broken.

**Config docs location:** `/home/neo/agents/sys-admin/config/`

## Subsystems

Match the user's description to a subsystem, then run the quick fix.

| Subsystem | Aliases | Config Doc | Quick Fix |
|-----------|---------|------------|-----------|
| **voice** | hyprwhspr, dictation, speech-to-text, stt, caps lock | `config/voice/hyprwhspr.md` | `fix-voice` |
| **keyboard** | keys, keybinds, hotkeys, YUNZII, AL98, VIA | `config/keyboard/yunzii-al98.md` | `Fn + Spacebar` (factory reset) |
| **audio** | sound, speakers, volume, pipewire, wireplumber | `config/audio/speakers.md` | `systemctl --user restart pipewire wireplumber` |
| **display** | monitor, screen, resolution, 120hz, hdmi, displayport, tv black | `config/display/monitors.md` | `wake-tv` (TV black) or `hyprctl reload` |
| **gpu** | graphics, intel arc, b580, xe driver, vulkan, opengl | `config/gpu/arc-b580.md` | `lsmod | grep xe` (check driver loaded) |

## Workflow

1. **Run quick fix first** - don't diagnose before trying the simple fix
2. **If quick fix fails**, read the config doc for step-by-step troubleshooting
3. **Update the config doc** if you discover new issues or solutions

## Key Principle

**Try the quick fix first.** 90% of issues are fixed by the quick fix command. Don't run extensive diagnostics before trying a simple restart.

## If No Subsystem Matches

If troubleshooting something not listed above:

1. Check service status: `systemctl --user status <service>`
2. Check logs: `journalctl --user -u <service> --since "10 min ago"`
3. Try restart: `systemctl --user restart <service>`
4. Create a new config doc in `config/<subsystem>/` with findings
5. Add the subsystem to the table above and to `config/INDEX.md`
