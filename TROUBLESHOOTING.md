# System Troubleshooting Tracker

**Purpose:** Central checklist for active and resolved system issues
**Last Updated:** November 30, 2025

---

## Active Issues

### Audio
- **[WORKAROUND]** No sound from TV/monitors - Intel Arc xe driver DP audio bug → `audio/tv-audio-troubleshooting.md`
  - **Status:** xe driver doesn't populate audio ELD for DisplayPort outputs (works on native HDMI)
  - **Cause:** Driver issue - graphics and audio subsystems not communicating for DP
  - **Workaround:** Using Bluetooth speaker for audio (bypasses GPU audio entirely)

---

## Resolved Issues

### Display
- **[RESOLVED - Nov 28, 2025]** 55-inch TV 120Hz not working → `display/55-inch-tv-120hz-troubleshooting.md`
  - **Solution:** Switched from native HDMI to DisplayPort-to-HDMI cable

### Keyboard
- **[RESOLVED - Nov 28, 2025]** YUNZII AL98 lighting resets on reboot → `keyboard/yunzii-al98-troubleshooting.md`
  - **Solution:** Disabled VIA lighting controls, use hardware Fn keys only

---

## Backlog / TODO

*(No pending issues)*

---

## Usage Notes

**For the agent:**
- Read this file first when using `/troubleshoot <folder>` command
- Check status of issue before diving into folder details
- Update this file when issue status changes (in progress → resolved, or new issues added)

**Status definitions:**
- `[IN PROGRESS]` - Actively troubleshooting
- `[RESOLVED]` - Fixed and working
- `[TODO]` - Known issue, not yet started
- `[BLOCKED]` - Waiting on external factor (hardware, updates, etc.)
