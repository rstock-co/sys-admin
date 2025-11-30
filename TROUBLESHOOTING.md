# System Troubleshooting Tracker

**Purpose:** Central checklist for active and resolved system issues
**Last Updated:** November 30, 2025

---

## Active Issues

### Audio
- **[RESOLVED - Workaround]** No sound from TV/monitors - Intel Arc xe driver DP audio bug → `audio/tv-audio-troubleshooting.md`
  - **Root Cause:** Confirmed Linux kernel xe driver bug - fails to convert DP EDID→ELD for audio codec
  - **Research:** Known issue with Arc B580 + DisplayPort, native HDMI works (GPU firmware handles conversion)
  - **Solution:** JBL Flip 6 Bluetooth speaker paired, PipeWire config tuned (minor glitching remains)
  - **Future:** Wait for kernel xe driver update or use USB DAC for zero-latency audio

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
