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

---

## Historical Troubleshooting Reference

### Issue: Native HDMI stuck at 60Hz (Nov 2025)

**What we tried:**
- Decoded TV EDID - confirmed 120Hz advertised correctly (VIC 118)
- Kernel parameter `video=HDMI-A-3:3840x2160@120` - didn't work
- Updated Hyprland config port from HDMI-A-5 to HDMI-A-3
- Force mode via `hyprctl keyword monitor` - still 60Hz

**Root cause:** Intel xe driver not parsing HDMI 2.1 modes correctly

**Solution:** Switched to DisplayPort-to-HDMI cable (bypasses driver HDMI issues)

### Issue: PCIe x1 bottleneck (Nov 2025)

**What we tried:**
- BIOS update to 2.A91 (AGESA PI 1.2.0.3g)
- Enabled Above 4G Decoding and Re-Size BAR
- CMOS reset via button (15 sec) - insufficient
- Checked PCIe link: `cat /sys/bus/pci/devices/0000:03:00.0/current_link_width`

**Diagnosis commands:**
```bash
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width   # Should be 16
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed   # Should be 16.0 GT/s
```

**Note:** PCIe issue was separate from display issue - DP-to-HDMI worked regardless

### Issue: Monitor layout wrong after port change (Nov 2025)

**What we tried:**
- Wallpaper upside down on portrait monitors
- Mouse movement going to wrong monitor

**Solution:** Updated hyprland.conf positions and transforms:
- DP-3 (physical left) → position 0x0, transform 1
- DP-2 (physical center) → position 2160x840
- DP-1 (physical right) → position 6000x0, transform 3

### BIOS settings reference (MSI MAG X870E)

If PCIe issues return:
```
Settings → Advanced → PCI Subsystem Settings
  → Above 4G Decoding: Enabled
  → Re-Size BAR Support: Enabled

Settings → Advanced → AMD CBS → NBIO Common Options → GFX Configuration
  → GFX0 Gen Switch: Gen 5 or Auto
  → Bifurcation: Disabled
```

### EDID extraction (if needed again)

```bash
sudo pacman -S v4l-utils
cat /sys/class/drm/card0/card0-DP-2/edid > ~/edid-custom/tcl.bin
edid-decode ~/edid-custom/tcl.bin
```

### Kernel parameter forcing (if needed again)

Edit `/boot/loader/entries/arch.conf`:
```
options root=/dev/nvme0n1p2 rw video=DP-2:3840x2160@120
```

### Recovery if all displays fail

1. Plug monitor into motherboard HDMI port
2. Boot on integrated graphics
3. Fix config files
4. Reconnect to GPU
