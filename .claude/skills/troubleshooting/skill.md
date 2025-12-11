---
description: Troubleshoot system services. Use when user reports something isn't working (hyprwhspr, keyboard, audio, display).
---

# Troubleshooting Skill

You are troubleshooting a system issue. The user will tell you what's broken.

## Available Documentation

Check the `docs/` folder for service-specific troubleshooting guides:

- `docs/hyprwhspr.md` - Voice dictation (Caps Lock not working, text not appearing)
- `docs/keyboard.md` - Keyboard issues (YUNZII AL98, VIA, keymaps)
- `docs/audio.md` - Audio issues (TV speakers, PipeWire, WirePlumber)
- `docs/display.md` - Display issues (120Hz, multi-monitor, DP/HDMI)

## Workflow

1. **Identify the service** from user's description
2. **Read the relevant doc** from `docs/`
3. **Start with Quick Fix** - most docs have a "Quick Fix (Try This First)" section
4. **If quick fix fails**, follow step-by-step troubleshooting in the doc
5. **Update the doc** if you discover new issues or solutions

## Key Principle

**Try the quick fix first.** Don't run extensive diagnostics before trying a simple restart. Most issues are fixed by:

```bash
systemctl --user restart <service>
```

## If No Doc Exists

If troubleshooting a service without documentation:

1. Check service status: `systemctl --user status <service>`
2. Check logs: `journalctl --user -u <service> --since "10 min ago"`
3. Try restart: `systemctl --user restart <service>`
4. Create a new doc in `docs/<service>.md` with findings
