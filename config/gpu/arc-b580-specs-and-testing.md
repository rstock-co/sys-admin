# Intel Arc B580 GPU - Specifications and Testing Guide

**Last Updated:** 2025-11-30
**Purpose:** GPU verification, driver issue documentation, and comprehensive testing procedures

---

## GPU Specifications

### Hardware Details
- **Model:** ASRock Intel Arc B580 Challenger 12GB OC
- **Architecture:** Intel Xe2 (Battlemage)
- **VRAM:** 12GB GDDR6
- **Memory Speed:** 19 Gbps
- **Memory Bus:** 192-bit
- **Boost Clock:** 2740 MHz
- **TDP:** 190W (650W PSU recommended)
- **Max Resolution:** 7680 x 4320
- **Cooling:** Dual Fan

### Interface Specifications
- **PCIe Interface:** PCIe 4.0 x8 (should negotiate up to x16 on compatible boards)
- **Display Outputs:**
  - 3x DisplayPort 1.4a (up to 8K@60Hz or 4K@120Hz per port)
  - 1x HDMI 2.1 (up to 4K@120Hz, 8K@60Hz)

### Features
- **Video Encoding:** Intel Quick Sync Video (AV1, HEVC, H.264)
- **Ray Tracing:** Xe Super Sampling (XeSS), DirectX 12 Ultimate
- **Resizable BAR:** Supported and recommended for optimal performance
- **DisplayPort Alt Mode:** Yes
- **HDMI 2.1 Features:** Variable Refresh Rate (VRR), Auto Low Latency Mode (ALLM), eARC

---

## Known Driver Issues

### HDMI Port 120Hz Failure (RESOLVED)

**Issue Discovered:** 2025-11-27
**Resolution Date:** 2025-11-30
**Status:** ✅ **WORKAROUND IMPLEMENTED**

#### Problem Description
The GPU's native **HDMI 2.1 port** failed to properly negotiate 120Hz refresh rate at 4K resolution (3840x2160) with the TCL 55" QM7K TV, despite:
- TV correctly advertising 120Hz capability via EDID
- HDMI 2.1 certified cable being used
- Same cable working at 120Hz when connected to motherboard integrated graphics
- GPU hardware being HDMI 2.1 compliant

#### Root Cause
**Intel Arc B580 `xe` driver bug** preventing proper HDMI 2.1 mode negotiation:
- Driver failed to parse or accept 120Hz modes from TV's EDID
- Only exposed 60Hz maximum refresh rate to the system
- Lower resolutions (1920x1080@120Hz, 2560x1440@120Hz) worked correctly
- Issue specific to 4K@120Hz over native HDMI port

**Technical Details:**
- Driver possibly using HDMI 1.4 TMDS limit (340 MHz) instead of HDMI 2.1 limit (600 MHz)
- YCbCr 4:2:0 color format not being enabled (required for 4K@120Hz within bandwidth)
- Arc B580 is new hardware (released December 2024) - HDMI 2.1 driver support still maturing

#### Workaround Solution
**Switched from native HDMI port to DisplayPort output with DP-to-HDMI cable:**
- TV now connected via DisplayPort output (DP-2)
- Using DisplayPort to HDMI 2.1 cable/adapter
- **Result:** Full 3840x2160@120Hz working perfectly
- Bypasses HDMI port driver issues entirely

**Current Working Configuration:**
```bash
# TV now on DP-2 instead of HDMI-A-3
hyprctl monitors | grep "DP-2"
# Output: 3840x2160@120.00000 at 2160x840
```

#### Files Modified During Troubleshooting
1. `/boot/loader/entries/arch.conf` - Kernel parameter added (now obsolete with DP solution):
   - Previous workaround: `video=HDMI-A-3:3840x2160@120`
   - Can be removed if desired (no longer needed with DP connection)

2. `~/.config/hypr/hyprland.conf` - Monitor configuration updated:
   - Changed from `HDMI-A-3` to `DP-2` for center TV
   - Adjusted monitor positions after port change

#### Long-term Recommendations
1. **Keep using DisplayPort output** - More reliable, better driver support
2. **Monitor Intel driver updates** - Future `xe` driver releases may fix native HDMI issues
3. **Reserve HDMI port** for non-critical displays or lower refresh rates
4. **Test HDMI port periodically** after major driver updates to see if issue resolves

#### Reference Documentation
Full troubleshooting history: `/home/neo/agents/sys-admin/display/55-inch-tv-120hz-troubleshooting.md`

---

## Known Intel Arc PCIe Reporting Bug on Linux

### ⚠️ CRITICAL: False PCIe x1 Reporting Issue

**Intel has officially confirmed** that Linux tools like `lspci` and sysfs (`/sys/class/pci/...`) **incorrectly report** Intel Arc GPUs as running at **PCIe Gen 1.0 x1**, when they are actually running at full speed (Gen 4.0 x8 or x16).

**This is a reporting bug only - it does NOT affect actual performance.**

#### Official Intel Statement
From [Intel Support Article 000094587](https://www.intel.com/content/www/us/en/support/articles/000094587/graphics.html):

> "Tools like lspci on Linux don't report actual PCIe configuration information about generation and lanes for Intel Arc graphics cards. They show Gen1 and x1 lanes instead of the expected product information (such as Gen4 and x16 lanes). **This does not affect the PCIe port speed or the card's operation/performance.** There is no PCIe standard-compliant way of resolving this at the moment."

#### Performance Confirmation
Users have verified actual PCIe bandwidth through testing:
- **OpenCL memory tests show 17-18 GB/s** over PCIe (confirms Gen 4.0 x16)
- **Real-world performance matches expectations** for PCIe 4.0 x8/x16
- **Occurs across multiple kernel versions** (6.2+, 6.8+, 6.17+) and drivers (i915, xe)

#### What This Means
If you see:
```bash
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width  # Shows: 1
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed  # Shows: 2.5 GT/s
```

**This is normal for Intel Arc on Linux.** Your GPU is likely running at full speed despite the false reporting.

#### How to Verify Actual Performance
Instead of relying on sysfs reporting, verify with:
1. **Bandwidth tests** (Test 6 below) - Should show 15+ GB/s
2. **Benchmark performance** (Test 5 below) - Compare against known results
3. **Real-world usage** - 4K@120Hz works, smooth performance indicates proper PCIe speed

#### When to Actually Worry
Only investigate PCIe issues if you experience:
- ❌ Severe performance degradation (far below expected)
- ❌ Display modes not available (4K@120Hz missing when it should work)
- ❌ Crashes or instability under load
- ❌ VRAM not fully accessible

If performance is good and displays work correctly, **ignore the x1 reporting** - it's a known cosmetic bug.

#### References
- [Intel: Why Is My System Reporting PCIe Gen 1x1](https://www.intel.com/content/www/us/en/support/articles/000094587/graphics.html)
- [Intel Community: Arc B580 PCIe x1 Discussion](https://community.intel.com/t5/Intel-Arc-Discrete-Graphics/Intel-Arc-B580-stuck-at-PCIe-4-0-x1-instead-of-x8-on-Gigabyte/m-p/1714683)
- [Intel Community: Arc A770 False Reporting](https://community.intel.com/t5/Graphics/Intel-ARC-A770-on-Ubuntu-22-04-LTS-showing-up-as-PCIe-Gen1-x1/td-p/1451016)

---

## GPU Testing Procedures

### Prerequisites
```bash
# Install required tools
sudo pacman -S pciutils mesa-utils vulkan-tools

# Verify GPU is detected
lspci | grep VGA
# Expected: Intel Arc B580 at 0000:03:00.0
```

---

### Test 1: PCIe Interface Verification

**Purpose:** Verify actual PCIe performance (not relying on sysfs reporting due to Intel Arc bug)

**⚠️ NOTE:** Due to the Intel Arc reporting bug documented above, `current_link_width` and `current_link_speed` will show incorrect values (x1 @ 2.5 GT/s). This is normal and does not indicate a problem.

#### Check Reported PCIe Configuration (Informational Only)
```bash
# These will show INCORRECT values on Intel Arc (known bug)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width  # Will show: 1 (FALSE)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed  # Will show: 2.5 GT/s (FALSE)

# Check maximum capabilities (also may show incorrect values)
cat /sys/bus/pci/devices/0000:03:00.0/max_link_width
cat /sys/bus/pci/devices/0000:03:00.0/max_link_speed
```

**Expected (Incorrect) Output on Intel Arc:**
```
current_link_width: 1        ← FALSE (reporting bug)
current_link_speed: 2.5 GT/s ← FALSE (reporting bug)
max_link_width: 8 or 16      ← May be correct
max_link_speed: 16.0 GT/s    ← May be correct
```

#### ✅ CORRECT METHOD: Check Motherboard Root Port
```bash
# Check what the MOTHERBOARD sees (this is accurate!)
cat /sys/bus/pci/devices/0000:00:01.1/current_link_width
cat /sys/bus/pci/devices/0000:00:01.1/current_link_speed

# Expected (CORRECT) output:
# 8 or 16
# 16.0 GT/s PCIe

# This bypasses Intel Arc's reporting bug by checking the AMD root complex
```

#### Alternative: Check with lspci (also shows incorrect values)
```bash
# This may also show incorrect values on Intel Arc
sudo lspci -vvv -s 03:00.0 | grep -E "LnkCap|LnkSta"

# May show (incorrectly):
# LnkSta: Speed 2.5GT/s, Width x1
```

#### ✅ PASS Criteria (Actual Performance-Based)
Since sysfs reporting is unreliable on Intel Arc, determine if PCIe is working by:

1. **Display functionality:**
   - ✅ All monitors detected and working
   - ✅ 4K@120Hz available and working on TV
   - ✅ No display artifacts or instability

2. **GPU detected and functional:**
   - ✅ `xe` driver loaded
   - ✅ VRAM accessible (12GB)
   - ✅ Vulkan/OpenGL working

3. **Performance tests pass** (see Test 5 and Test 6 below):
   - ✅ Benchmark scores reasonable
   - ✅ PCIe bandwidth test shows 15+ GB/s

#### ❌ FAIL Indicators (Actual Problems)
Only worry if you experience:
- ❌ Severe performance issues (far below expected)
- ❌ 4K@120Hz modes not available
- ❌ Frequent crashes or hangs
- ❌ VRAM not fully accessible
- ❌ Bandwidth tests show <5 GB/s (indicates real bottleneck)

#### Troubleshooting (Only If Experiencing Actual Performance Problems)

**⚠️ IMPORTANT:** Due to the Intel Arc reporting bug, seeing "x1 @ 2.5 GT/s" is NORMAL and does NOT require troubleshooting unless you have actual performance issues.

**Only proceed with troubleshooting if you experience:**
- Severe performance degradation
- Missing display modes (4K@120Hz not available)
- Frequent crashes or instability
- Bandwidth tests showing <5 GB/s

**If you have actual problems:**

1. **Check BIOS settings:**
   - Above 4G Decoding: Enabled
   - Re-Size BAR Support: Enabled
   - PCIe Slot Configuration: Gen 4 or Auto
   - PCIe Bifurcation: Disabled

2. **Perform complete CMOS reset:**
   - Power off system
   - Flip PSU switch to off
   - Remove motherboard CMOS battery
   - Wait 30-60 minutes (critical for Arc B580 PCIe switch chip to reset)
   - Reinstall battery, power on
   - Reconfigure BIOS

3. **Physical inspection:**
   - Reseat GPU in PCIe slot
   - Ensure GPU is in primary x16 slot (closest to CPU)
   - Check for bent pins or physical damage
   - Verify all power connectors fully seated

---

### Test 2: VRAM Verification

**Purpose:** Confirm full 12GB VRAM is available and functional

#### Check VRAM Amount
```bash
# Using intel_gpu_top (install intel-gpu-tools if missing)
sudo pacman -S intel-gpu-tools
intel_gpu_top -l
# Look for "local memory" or "vram" in output

# Alternative: Check via DRM
cat /sys/class/drm/card*/device/mem_info_vram_total 2>/dev/null

# Using glxinfo (from mesa-utils)
glxinfo | grep -i "video memory"
```

#### Using vulkaninfo
```bash
vulkaninfo | grep -A 5 "memoryHeaps"

# Expected output should show:
# memoryHeaps[0]:
#     size   = 12884901888 (12.00 GiB)  <- GPU VRAM
#     budget = ...
#     usage  = ...
```

#### ✅ PASS Criteria
- Total VRAM: **12 GB** (12884901888 bytes or similar)
- Memory type: GDDR6
- Full capacity available (not reduced)

#### ❌ FAIL Indicators
- VRAM showing less than 12 GB
- System unable to detect VRAM
- Memory errors in dmesg

---

### Test 3: Driver and Mesa Verification

**Purpose:** Ensure correct drivers are loaded and functioning

#### Check Active Driver
```bash
# Verify xe driver is loaded (not i915)
lsmod | grep xe

# Check driver version and info
modinfo xe | grep -E "version|description"

# Verify Mesa version
glxinfo | grep "OpenGL version"
```

#### Check DRM Device
```bash
# List DRM devices
ls -la /dev/dri/

# Should show:
# card0 or card1 -> Intel Arc GPU
# renderD128 or similar -> Render node
```

#### Verify Vulkan Support
```bash
# List Vulkan devices
vulkaninfo --summary | grep -E "deviceName|driverName|driverInfo"

# Expected:
# deviceName     = Intel Arc B580
# driverName     = Intel open-source Mesa driver
# driverInfo     = Mesa X.X.X
```

#### ✅ PASS Criteria
- `xe` driver loaded (for Arc Alchemist/Battlemage)
- Mesa version 24.0+ (Arc support started ~23.3)
- Vulkan 1.3+ support
- OpenGL 4.6 support

---

### Test 4: Display Output Testing

**Purpose:** Verify all display outputs function at expected resolutions and refresh rates

#### Current Display Configuration
```bash
# List all connected displays
hyprctl monitors

# Check available modes per display
hyprctl monitors | grep -E "Monitor|3840x2160|availableModes"
```

#### Test Each Output Port
```bash
# DP-1: Right Samsung 32" (Portrait)
# Expected: 3840x2160@60Hz, transform 3

# DP-2: Center TCL 55" TV (Landscape)
# Expected: 3840x2160@120Hz, transform 0

# DP-3: Left Samsung 32" (Portrait)
# Expected: 3840x2160@60Hz, transform 1
```

#### Verify High Refresh Rate
```bash
# Verify 120Hz is active on center monitor
hyprctl monitors | grep "DP-2" -A 3

# Should show: 3840x2160@120.00000
```

#### ✅ PASS Criteria
- All three monitors detected
- Center TV running at **120Hz**
- Side monitors running at **60Hz**
- No flickering or artifacts
- Smooth mouse movement across displays

---

### Test 5: Rendering Performance Test

**Purpose:** Verify GPU can render and compute at expected performance

#### Basic OpenGL Test
```bash
# Install glmark2 if not present
sudo pacman -S glmark2

# Run benchmark (Wayland version)
glmark2-wayland --fullscreen

# Expected score: 2000+ (depends on settings)
# Should complete without crashes or artifacts
```

#### Vulkan Compute Test
```bash
# Install vkmark if available
paru -S vkmark  # AUR package

# Run Vulkan benchmark
vkmark

# Should complete without errors
```

#### Video Decode Test
```bash
# Install vainfo
sudo pacman -S libva-utils

# Check video acceleration capabilities
vainfo

# Expected:
# VAProfileH264Main, VAProfileHEVC, VAProfileAV1
# Multiple entrypoints (VLD, EncSlice, etc.)
```

#### ✅ PASS Criteria
- Benchmarks complete without crashes
- Video decode acceleration working (AV1, HEVC, H.264)
- Frame rates stable during testing
- No thermal throttling (check temps)

---

### Test 6: Memory Bandwidth Test

**Purpose:** Verify VRAM and system memory bandwidth

#### Using intel_gpu_top
```bash
# Monitor GPU while running stress test
sudo intel_gpu_top

# Look for:
# - GPU usage % (should reach near 100% under load)
# - VRAM usage climbing during memory-intensive tasks
# - No "throttling" indicators
```

#### Stress Test with glmark2
```bash
# Run extended test with high texture usage
glmark2-wayland --benchmark=texture --duration=60

# Monitor VRAM usage during test
watch -n 1 "cat /sys/class/drm/card*/device/mem_info_vram_used"
```

#### ✅ PASS Criteria
- VRAM bandwidth matches expected ~456 GB/s (12GB @ 19 Gbps)
- No memory errors in `dmesg`
- Full VRAM capacity utilized when needed

---

### Test 7: Thermal and Power Testing

**Purpose:** Ensure cooling and power delivery are adequate

#### Monitor GPU Temperature
```bash
# Install sensors package if missing
sudo pacman -S lm_sensors

# Detect sensors
sudo sensors-detect

# Monitor temps in real-time
watch -n 1 sensors

# Look for GPU temp (likely under "xe" or similar)
```

#### Stress Test Thermal Performance
```bash
# Run glmark2 for extended period
glmark2-wayland --fullscreen --duration=300  # 5 minutes

# Monitor temperatures throughout
# Should stabilize under 85°C (typical max safe temp)
```

#### Power Consumption Check
```bash
# Using intel_gpu_top
sudo intel_gpu_top

# Look for power consumption (watts)
# Should show ~190W under full load
```

#### ✅ PASS Criteria
- Idle temp: **30-50°C**
- Load temp: **65-85°C** (under sustained load)
- No thermal throttling
- Power draw appropriate for workload
- Fans spinning and audible under load

---

## Comprehensive Test Script

### Quick Health Check
Located at `/home/neo/agents/sys-admin/gpu/scripts/gpu-health-check.sh`:
```bash
#!/bin/bash

echo "=== Intel Arc B580 Health Check ==="
echo ""

echo "1. PCIe Interface:"
echo "   Width: $(cat /sys/bus/pci/devices/0000:03:00.0/current_link_width)"
echo "   Speed: $(cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed)"
echo ""

echo "2. Driver Status:"
lsmod | grep -q xe && echo "   ✅ xe driver loaded" || echo "   ❌ xe driver NOT loaded"
echo ""

echo "3. Display Outputs:"
hyprctl monitors | grep -E "Monitor.*DP-" | awk '{print "   "$1" "$2" "$3}'
echo ""

echo "4. VRAM (from Vulkan):"
vulkaninfo 2>/dev/null | grep -A 1 "memoryHeaps\[0\]" | grep size | awk '{print "   "$3" "$4" "$5}'
echo ""

echo "5. Mesa Version:"
glxinfo 2>/dev/null | grep "OpenGL version" | awk '{print "   "$0}'
echo ""

echo "6. Current Refresh Rates:"
hyprctl monitors | grep -E "3840x2160@" | awk '{print "   "$1}'
echo ""

echo "=== Test Complete ==="
```

Run anytime:
```bash
# Using alias (preferred)
gpu-check

# Or direct path
/home/neo/agents/sys-admin/gpu/scripts/gpu-health-check.sh
```

**Note:** The `gpu-check` alias is defined in `~/zshrc/sys-admin.sh` and will be available in new shell sessions.

---

## Troubleshooting Quick Reference

### Issue: GPU not detected
```bash
# Check if GPU appears in PCI bus
lspci | grep VGA

# Check kernel logs for errors
dmesg | grep -i "xe\|gpu\|pci"

# Verify GPU is seated properly (physical check required)
```

### Issue: PCIe running at x1 or slow speed
1. Enter BIOS and verify:
   - Above 4G Decoding: Enabled
   - Re-Size BAR: Enabled
   - PCIe Gen: Auto or Gen 4
2. Perform complete CMOS reset (30-60 min power loss)
3. Reseat GPU physically

### Issue: Display not working
1. Check cable connections
2. Try different display output (DP vs HDMI)
3. Verify display detected: `hyprctl monitors`
4. Check kernel logs: `journalctl -b 0 | grep drm`

### Issue: Poor performance
1. Verify PCIe running at full speed (Test 1)
2. Check thermal throttling (Test 7)
3. Update Mesa: `sudo pacman -Syu`
4. Verify Re-Size BAR enabled in BIOS

### Issue: Crashes or artifacts
1. Check temperatures (overheating?)
2. Test VRAM for errors
3. Update drivers: `sudo pacman -Syu`
4. Check power supply adequate (650W recommended)

---

## Success Criteria Summary

✅ **GPU is fully functional when ALL of these are true:**

1. **PCIe:** x8 or x16 @ 16.0 GT/s (Gen 4.0)
2. **VRAM:** Full 12 GB detected and available
3. **Driver:** xe module loaded, Mesa 24.0+
4. **Displays:** All outputs working at expected resolutions/refresh rates
5. **Performance:** Benchmarks complete without errors, reasonable scores
6. **Thermal:** Temps under 85°C under load, no throttling
7. **Stability:** No crashes, artifacts, or errors during stress testing

If any test fails, refer to troubleshooting sections and cross-reference with display troubleshooting documentation.

---

## References

- Intel Arc B580 Specs: https://www.intel.com/arc
- PCIe Troubleshooting: `/home/neo/agents/sys-admin/display/55-inch-tv-120hz-troubleshooting.md`
- Mesa Arc Support: https://docs.mesa3d.org/drivers/intel.html
- Arch Wiki Intel Graphics: https://wiki.archlinux.org/title/Intel_graphics
