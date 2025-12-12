# Display Configuration

## Quick Fix

**TV black after power on:**
```bash
wake-tv
```

**General display issues:**
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

---

## System Paths

| File | Purpose |
|------|---------|
| `~/.config/hypr/hyprland.conf` | Monitor definitions (lines 28-32) |
| `/sys/class/drm/` | Kernel display devices |

**Working config:**
```
monitor=DP-3,3840x2160@60,0x0,1,transform,1
monitor=DP-2,3840x2160@120,2160x840,1
monitor=DP-1,3840x2160@60,6000x0,1,transform,3
```

---

## Troubleshooting

### TV Not Detecting / Black Screen

```bash
wake-tv
```

Or manually:
```bash
hyprctl keyword monitor DP-2,disable && sleep 3 && hyprctl keyword monitor DP-2,3840x2160@120,1080x540,1 && hyprctl reload
```

### Wrong Monitor Layout / Mouse Movement

Check positions match physical layout:
```bash
grep "^monitor=" ~/.config/hypr/hyprland.conf
```

Expected:
- DP-3 (left) at 0x0
- DP-2 (center) at 2160x840
- DP-1 (right) at 6000x0

### TV Stuck at 60Hz

```bash
hyprctl monitors | grep DP-2 -A3
```

If 60Hz:
1. Check cable seated
2. `hyprctl reload`
3. Reboot if still 60Hz

### Portrait Monitors Upside Down

Check transforms:
- Left (DP-3): transform 1
- Right (DP-1): transform 3

---

## Diagnostic Commands

```bash
# Full monitor info
hyprctl monitors

# Available modes
hyprctl monitors | grep availableModes

# Detected displays
ls /sys/class/drm/ | grep card

# Kernel logs
journalctl -b 0 | grep -i drm | tail -20
```

---

## Known Issue: Arc B580 Native HDMI

Intel xe driver has HDMI 2.1 bugs - native HDMI maxes at 60Hz.

**Solution:** Use DisplayPort with DP-to-HDMI cable.

If TV connected to native HDMI:
1. Works but stuck at 60Hz
2. Switch to DP output with adapter
3. Update hyprland.conf port name

---

## Historical Reference

### Native HDMI 60Hz issue (Nov 2025)

**Tried:**
- EDID decode - 120Hz advertised (VIC 118)
- Kernel parameter `video=HDMI-A-3:3840x2160@120`
- Force mode via hyprctl

**Root cause:** xe driver not parsing HDMI 2.1 modes

**Solution:** DP-to-HDMI cable

### PCIe x1 bottleneck (Nov 2025)

**Tried:**
- BIOS update 2.A91
- Above 4G Decoding, Re-Size BAR
- CMOS reset

**Diagnosis:**
```bash
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width   # Should be 16
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed   # Should be 16.0 GT/s
```

**Note:** Unrelated to display - DP-to-HDMI worked regardless

### BIOS reference (MSI MAG X870E)

```
Settings → Advanced → PCI Subsystem Settings
  → Above 4G Decoding: Enabled
  → Re-Size BAR Support: Enabled

Settings → Advanced → AMD CBS → NBIO Common Options → GFX Configuration
  → GFX0 Gen Switch: Gen 5 or Auto
  → Bifurcation: Disabled
```

### EDID extraction

```bash
sudo pacman -S v4l-utils
cat /sys/class/drm/card0/card0-DP-2/edid > ~/edid-custom/tcl.bin
edid-decode ~/edid-custom/tcl.bin
```

### Kernel parameter forcing

Edit `/boot/loader/entries/arch.conf`:
```
options root=/dev/nvme0n1p2 rw video=DP-2:3840x2160@120
```

### Recovery (all displays fail)

1. Plug monitor into motherboard HDMI
2. Boot on integrated graphics
3. Fix config files
4. Reconnect to GPU
