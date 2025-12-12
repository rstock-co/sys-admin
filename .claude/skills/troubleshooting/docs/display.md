# Display Troubleshooting

## Quick Fix (Try This First)

```bash
hyprctl reload
```

---

## Current Setup

| Monitor | Port | Resolution | Refresh | Position | Transform |
|---------|------|------------|---------|----------|-----------|
| Samsung 32" (left) | DP-3 | 3840x2160 | 60Hz | 0x0 | Portrait (1) |
| TCL 55" TV (center) | DP-2 | 3840x2160 | 120Hz | 2160x840 | Landscape (0) |
| Samsung 32" (right) | DP-1 | 3840x2160 | 60Hz | 6000x0 | Portrait (3) |

**TV Connection**: DisplayPort-to-HDMI cable (GPU DP → TV HDMI)

This setup works because Intel Arc B580's native HDMI port had driver issues with 120Hz. Using DisplayPort output with a DP-to-HDMI cable bypasses those issues.

---

## Common Issues

### TV Not Detecting / Black Screen

```bash
# Wake TV by toggling the port
hyprctl keyword monitor DP-2,disable && sleep 3 && hyprctl keyword monitor DP-2,3840x2160@120,1080x540,1 && hyprctl reload
```

Or use the alias: `wake-tv`

### Wrong Monitor Layout / Mouse Movement

Check Hyprland config positions match physical layout:
```bash
grep "^monitor=" ~/.config/hypr/hyprland.conf
```

Expected:
- DP-3 (left) at position 0x0
- DP-2 (center) at position 2160x840
- DP-1 (right) at position 6000x0

### TV Stuck at 60Hz

Verify current refresh rate:
```bash
hyprctl monitors | grep DP-2 -A3
```

If showing 60Hz instead of 120Hz:
1. Check cable is properly seated
2. Run `hyprctl reload`
3. If still 60Hz, reboot

### Portrait Monitors Upside Down

Check transform values in config:
- Left monitor (DP-3): transform 1
- Right monitor (DP-1): transform 3

If wrong, edit `~/.config/hypr/hyprland.conf` and reload.

---

## Diagnostic Commands

```bash
# Full monitor info
hyprctl monitors

# Available modes for each display
hyprctl monitors | grep availableModes

# Check if displays are detected
ls /sys/class/drm/ | grep card

# Kernel display logs
journalctl -b 0 | grep -i drm | tail -20
```

---

## Config Location

`~/.config/hypr/hyprland.conf` - Monitor definitions around line 28-32

Example working config:
```
monitor=DP-3,3840x2160@60,0x0,1,transform,1
monitor=DP-2,3840x2160@120,2160x840,1
monitor=DP-1,3840x2160@60,6000x0,1,transform,3
```

---

## Known Issue: Arc B580 Native HDMI

The GPU's native HDMI port has driver issues with 120Hz on Linux (xe driver). **Don't use native HDMI for the TV** - always use DisplayPort with DP-to-HDMI cable.

If you accidentally connect TV to native HDMI:
1. It will work but max out at 60Hz
2. Switch to a DisplayPort output with adapter cable
3. Update hyprland.conf to use the new port name (e.g., DP-2)
