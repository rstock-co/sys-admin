# GPU Documentation and Testing

**GPU:** Intel Arc B580 12GB (ASRock Challenger OC)

---

## Directory Structure

```
gpu/
├── README.md                           # This file
├── MONITORING.md                       # GPU monitoring tools guide
├── arc-b580-specs-and-testing.md      # Complete GPU documentation and testing guide
└── scripts/
    └── gpu-health-check.sh             # Quick GPU health check script
```

---

## Quick Reference

### Run GPU Health Check

**Using alias (preferred):**
```bash
gpu-check
```

**Direct path:**
```bash
/home/neo/agents/sys-admin/gpu/scripts/gpu-health-check.sh
```

**Note:** The `gpu-check` alias is defined in `~/zshrc/sys-admin.sh`

### Key Documentation
- **GPU monitoring guide:** `MONITORING.md`
- **Full specs and testing:** `arc-b580-specs-and-testing.md`
- **Display troubleshooting:** `/home/neo/agents/sys-admin/display/55-inch-tv-120hz-troubleshooting.md`

### GPU Monitoring
**btop doesn't work with Arc B580** (no xe driver support). Install nvtop instead:
```bash
sudo pacman -S nvtop
nvtop
```
See `MONITORING.md` for full details.

---

## Current Status Summary

✅ **Working Perfectly:**
- PCIe 4.0 x8 @ 16.0 GT/s (verified via motherboard root port)
- 12GB VRAM fully accessible
- xe driver loaded and functional
- Mesa 25.2.7 with OpenGL 4.6 support
- Triple 4K displays (2x 60Hz + 1x 120Hz)
- Center TV at 4K@120Hz via DisplayPort

⚠️ **Known Issues:**
- PCIe reporting bug: GPU reports x1 @ 2.5 GT/s (FALSE - ignore this)
- HDMI port 120Hz bug: Use DisplayPort instead for high refresh rates

---

## Testing Tools Installed

All standard monitoring tools are installed:
- `glxinfo` (mesa-utils) - OpenGL info, VRAM detection
- `vulkaninfo` (vulkan-tools) - Vulkan capabilities
- `intel_gpu_top` (intel-gpu-tools) - GPU usage monitoring (limited Arc support)

---

Last Updated: 2025-11-30
