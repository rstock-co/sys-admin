# GPU Monitoring Options for Intel Arc B580

**Last Updated:** 2025-11-30

---

## TL;DR - Recommended Solution

**Install nvtop** - Best Intel Arc B580 support as of 2025:
```bash
sudo pacman -S nvtop
nvtop
```

---

## Current Monitoring Tool Status

### ❌ btop (Limited Intel Arc Support)
**Status:** Has GPU support compiled in, but **Arc B580 detection is broken**

**Your btop version:** 1.4.5 with `GPU_SUPPORT=true`

**Known Issues:**
- [Issue #1073](https://github.com/aristocratos/btop/issues/1073): Arc B580 (Battlemage) not appearing
- [Issue #938](https://github.com/aristocratos/btop/issues/938): Failed to find Intel GPU engines
- btop uses `intel_gpu_top` backend which doesn't support xe driver yet

**Verdict:** ❌ Won't work until btop/intel_gpu_top add xe driver support

---

### ❌ intel_gpu_top (No xe Driver Support)
**Status:** Does NOT support xe driver (Arc B580 uses xe, not i915)

**Package:** `intel-gpu-tools 2.2-1` (already installed)

**Error when run:**
```
No device filter specified and no discrete/integrated i915 devices found
```

**Attempting xe driver:**
```bash
intel_gpu_top -d device:driver=xe
# Error: Failed to detect engines! (No such file or directory)
```

**Known Limitations:**
- Only works with i915 driver (older Intel GPUs)
- No xe driver support as of version 2.2
- Cannot monitor VRAM usage even on supported GPUs
- Cannot monitor power consumption
- No temperature monitoring (kernel 6.12+ will add this for i915 only)

**Verdict:** ❌ Won't work with Arc B580

---

### ✅ nvtop (RECOMMENDED)
**Status:** Works with Intel Arc B580 as of version 3.2.0+

**Package:** `nvtop 3.2.0-1` (available in Arch repos)

**Features:**
- ✅ Intel Arc B580 detection (fixed in recent updates)
- ✅ GPU usage monitoring
- ✅ VRAM usage monitoring
- ✅ Process monitoring (what's using the GPU)
- ⚠️ Temperature monitoring limited (kernel limitation, coming in 6.12+)
- ⚠️ Fan speed monitoring limited (kernel limitation)

**Installation:**
```bash
sudo pacman -S nvtop
```

**Usage:**
```bash
# Run nvtop
nvtop

# Run with specific device
nvtop -d 0
```

**Confirmed Working:**
- Arch Linux user confirmed Arc B580 recognition after March 2025 nvtop update
- Uses Intel's DRM interface (works with xe driver)
- Multi-vendor support (NVIDIA, AMD, Intel all in one tool)

**Verdict:** ✅ **Best option for Arc B580 monitoring**

---

## Monitoring Comparison

| Feature | btop | intel_gpu_top | nvtop |
|---------|------|---------------|-------|
| **Arc B580 Detection** | ❌ Broken | ❌ No xe support | ✅ Works |
| **GPU Usage** | ❌ | ❌ | ✅ |
| **VRAM Usage** | ❌ | ❌ | ✅ |
| **Process Monitoring** | ❌ | ❌ | ✅ |
| **Temperature** | ❌ | ❌ | ⚠️ Limited |
| **Fan Speed** | ❌ | ❌ | ⚠️ Limited |
| **CPU/RAM Monitoring** | ✅ Best | ❌ | ❌ |
| **Multi-vendor** | ⚠️ Partial | ❌ Intel only | ✅ All |

---

## Recommended Setup

### Option 1: Run Both Tools Side-by-Side
**For comprehensive system + GPU monitoring:**

Terminal 1:
```bash
btop  # For CPU, RAM, disk, network, processes
```

Terminal 2:
```bash
nvtop  # For GPU monitoring
```

### Option 2: Use tmux/splits
**Single window with both tools:**
```bash
# Horizontal split
tmux
# Run btop in main pane
# Ctrl+B, " to split horizontally
# Run nvtop in bottom pane
```

### Option 3: Add nvtop Alias
Add to `~/zshrc/sys-admin.sh`:
```bash
alias gpu='nvtop'
```

---

## Why btop Doesn't Work (Technical Details)

### The Problem Chain:
1. **Arc B580 uses xe driver** (not i915)
2. **btop uses intel_gpu_top** as backend for Intel GPUs
3. **intel_gpu_top only supports i915 driver** (via PMU - Performance Monitoring Unit)
4. **xe driver uses different kernel interfaces**
5. **Result:** btop/intel_gpu_top can't detect xe-based GPUs

### Future Outlook:
- intel_gpu_tools may add xe support eventually
- btop would then automatically support Arc GPUs
- Monitor these GitHub issues:
  - [btop #1073](https://github.com/aristocratos/btop/issues/1073)
  - [btop #938](https://github.com/aristocratos/btop/issues/938)

---

## Kernel Limitations (All Tools)

### Temperature Monitoring
**Status:** Not available yet for Arc GPUs

**Why:** Intel's Linux driver doesn't expose thermal sensors for discrete GPUs yet

**Coming Soon:**
- Linux kernel 6.12+ adding GPU package temperature support
- Requires HWMON interface patches (in testing)
- [Phoronix: Intel GPU Temperatures](https://www.phoronix.com/news/Intel-Linux-GPU-Temperatures)

### Fan Speed Monitoring
**Status:** Not available yet

**Why:** Same driver limitation as temperature

**Workaround:** None - must wait for kernel/driver updates

---

## Alternative: Manual Monitoring Scripts

### GPU Usage via DRM
```bash
# Check GPU is active
cat /sys/class/drm/card*/device/enable
```

### VRAM Usage
```bash
# Total VRAM (bytes)
cat /sys/class/drm/card1/device/mem_info_vram_total

# Used VRAM (bytes)
cat /sys/class/drm/card1/device/mem_info_vram_used

# Calculate percentage
TOTAL=$(cat /sys/class/drm/card1/device/mem_info_vram_total)
USED=$(cat /sys/class/drm/card1/device/mem_info_vram_used)
echo "VRAM: $((USED / 1024 / 1024)) MB / $((TOTAL / 1024 / 1024)) MB ($((USED * 100 / TOTAL))%)"
```

### Simple GPU Monitor Script
Could create `/home/neo/agents/sys-admin/gpu/scripts/gpu-monitor.sh`:
```bash
#!/bin/bash
watch -n 1 'echo "=== Arc B580 VRAM Usage ===" && \
TOTAL=$(cat /sys/class/drm/card1/device/mem_info_vram_total) && \
USED=$(cat /sys/class/drm/card1/device/mem_info_vram_used) && \
echo "Total: $((TOTAL / 1024 / 1024)) MB" && \
echo "Used:  $((USED / 1024 / 1024)) MB" && \
echo "Free:  $(((TOTAL - USED) / 1024 / 1024)) MB" && \
echo "Usage: $((USED * 100 / TOTAL))%"'
```

---

## Sources & References

- [nvtop GitHub](https://github.com/Syllo/nvtop) - Multi-vendor GPU monitoring tool
- [btop Issue #1073](https://github.com/aristocratos/btop/issues/1073) - Arc B580 not appearing
- [Arch Forums: Arc B580 Monitoring](https://bbs.archlinux.org/viewtopic.php?id=304567) - User confirmed nvtop works
- [Intel Arc Linux Guide](https://www.faceofit.com/intel-arc-iris-xe-linux-driver-compatibility-guide/)
- [Phoronix: Intel GPU Temps](https://www.phoronix.com/news/Intel-Linux-GPU-Temperatures)

---

## Quick Commands Reference

```bash
# Install nvtop (RECOMMENDED)
sudo pacman -S nvtop

# Run nvtop
nvtop

# Check VRAM manually
cat /sys/class/drm/card1/device/mem_info_vram_used

# Run btop for CPU/RAM/processes
btop

# Check GPU health
gpu-check
```

---

**Bottom Line:** Install `nvtop` for GPU monitoring. Use `btop` for CPU/RAM/processes. Run them side-by-side or in tmux splits.
