---
description: Troubleshoot system services. Use when user reports something isn't working (voice, keyboard, audio, display).
---

# Troubleshooting Skill

You are troubleshooting a system issue. The user will tell you what's broken.

## Subsystems

Match the user's description to a subsystem, then read its doc and run the quick fix.

| Subsystem | Aliases | Doc | Quick Fix |
|-----------|---------|-----|-----------|
| **voice** | hyprwhspr, dictation, speech-to-text, stt, caps lock | `docs/hyprwhspr.md` | `fix-voice` |
| **keyboard** | keys, keybinds, hotkeys, YUNZII, AL98, VIA | `docs/keyboard.md` | - |
| **audio** | sound, speakers, volume, pipewire, wireplumber | `docs/audio.md` | `systemctl --user restart pipewire wireplumber` |
| **display** | monitor, screen, resolution, 120hz, hdmi, displayport, tv black | `docs/display.md` | `wake-tv` (TV black) or `hyprctl reload` |

## Workflow

1. **Match subsystem** from user's description using aliases above
2. **Run quick fix first** - don't diagnose before trying the simple fix
3. **If quick fix fails**, read the doc and follow step-by-step troubleshooting
4. **Update the doc** if you discover new issues or solutions

## Key Principle

**Try the quick fix first.** Don't run extensive diagnostics before trying a simple restart. 90% of issues are fixed by the quick fix command.

## If No Subsystem Matches

If troubleshooting something not listed above:

1. Check service status: `systemctl --user status <service>`
2. Check logs: `journalctl --user -u <service> --since "10 min ago"`
3. Try restart: `systemctl --user restart <service>`
4. Create a new doc in `docs/<service>.md` with findings
5. Add the subsystem to the table above
