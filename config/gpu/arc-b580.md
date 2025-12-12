# GPU Configuration (Intel Arc B580)

## Quick Fix

**GPU not detected / driver issues:**
```bash
# Check driver loaded
lsmod | grep xe

# Restart display manager (last resort)
sudo systemctl restart sddm
```

**Display issues:** See `config/display/monitors.md`

---

## Current Setup

| Setting | Value |
|---------|-------|
| **Model** | ASRock Intel Arc B580 Challenger 12GB OC |
| **Driver** | xe (Intel Xe2/Battlemage) |
| **VRAM** | 12GB GDDR6 @ 19 Gbps |
| **PCIe** | 4.0 x8 @ 16.0 GT/s (via motherboard) |
| **Displays** | 3x DP 1.4a + 1x HDMI 2.1 |

**Current display connections:**
- DP-1: Samsung 32" right (portrait)
- DP-2: TCL 55" TV center (120Hz)
- DP-3: Samsung 32" left (portrait)
- HDMI: Unused (driver issues with 120Hz)

---

## System Paths

| Path | Purpose |
|------|---------|
| `/sys/bus/pci/devices/0000:03:00.0/` | GPU sysfs |
| `/sys/class/drm/card0/` | DRM device |
| `~/.config/hypr/hyprland.conf` | Display config |

---

## Known Driver Issues

### HDMI 2.1 @ 120Hz Broken

**Status:** Workaround in place (use DisplayPort)

The native HDMI port won't negotiate 4K@120Hz. xe driver bug - doesn't parse HDMI 2.1 EDID modes correctly.

**Workaround:** Use DisplayPort with DP-to-HDMI cable. Works perfectly at 120Hz.

### DisplayPort Audio Broken

**Status:** Workaround in place (use USB speakers)

HDMI audio via DP-to-HDMI doesn't work. xe driver doesn't convert DisplayPort EDID to ELD for audio codec.

**Workaround:** Use USB speakers (Creative Pebble Pro).

### PCIe x1 Reporting Bug

**Status:** Cosmetic - ignore

GPU reports x1 @ 2.5 GT/s but actually runs at x8 @ 16.0 GT/s through motherboard.

```bash
# Shows wrong value (x1) - IGNORE
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width

# Check via lspci for real value
lspci -vvv -s 03:00.0 | grep -i "lnksta\|width"
```

---

## Diagnostic Commands

```bash
# Driver loaded
lsmod | grep xe

# GPU info
glxinfo | grep "OpenGL renderer"

# VRAM
glxinfo | grep "Video memory"

# Vulkan
vulkaninfo --summary

# Monitor GPU usage
nvtop  # btop doesn't support xe driver

# PCIe link (ignore - reports wrong)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed

# Display status
hyprctl monitors
```

---

## Health Check

```bash
gpu-check  # Alias for health check script
# Or: /home/neo/agents/sys-admin/scripts/gpu-health-check.sh
```

---

## BIOS Settings (MSI MAG X870E)

Required for proper GPU operation:

```
Settings → Advanced → PCI Subsystem Settings
  → Above 4G Decoding: Enabled
  → Re-Size BAR Support: Enabled

Settings → Advanced → AMD CBS → NBIO Common Options → GFX Configuration
  → GFX0 Gen Switch: Gen 5 or Auto
  → Bifurcation: Disabled
```

---

## Historical Reference

### HDMI 120Hz investigation (Nov 2025)

**Tried:**
- EDID decode - 120Hz advertised correctly
- Kernel parameter `video=HDMI-A-3:3840x2160@120`
- Force mode via hyprctl
- Different HDMI cables

**Root cause:** xe driver HDMI 2.1 parsing bug

**Solution:** DP-to-HDMI cable bypasses driver issues

### PCIe x1 bottleneck investigation (Nov 2025)

**Tried:**
- BIOS update to 2.A91
- Above 4G Decoding, Re-Size BAR
- CMOS reset (button + extended)
- GPU reseat

**Finding:** GPU has onboard PCIe switch (Intel e2f0) that reports wrong link width. Actual bandwidth is fine - motherboard shows x8 @ 16.0 GT/s.

### DP audio failure (Nov 2025)

**Tried:**
- WirePlumber config for HDMI output
- Different DP-to-HDMI cables
- EDID audio block verification

**Root cause:** xe driver doesn't populate audio ELD from DisplayPort EDID

**Solution:** USB speakers (Creative Pebble Pro)

---

## Monitoring Tools

- `nvtop` - GPU usage (btop doesn't support xe)
- `intel_gpu_top` - Limited Arc support
- `glxinfo` - OpenGL/VRAM info
- `vulkaninfo` - Vulkan capabilities

---

## Reference Docs

Detailed specs and test results: `arc-b580-specs-and-testing.md` (same folder)
