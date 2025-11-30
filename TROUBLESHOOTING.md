# System Troubleshooting Tracker

**Purpose:** Central checklist for active and resolved system issues
**Last Updated:** November 30, 2025

---

## Active Issues

### Audio
- **[BLOCKED]** No sound from TV/monitors - Intel Arc B580 GPU HDMI audio issue → `audio/tv-audio-troubleshooting.md`
  - **Status:** GPU audio codec not detecting displays (ELD invalid, monitor_present=0)
  - **Cause:** Intel Arc + DP-to-HDMI adapters don't pass audio EDID correctly
  - **Next:** Try different cable or wait for GPU driver update

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
