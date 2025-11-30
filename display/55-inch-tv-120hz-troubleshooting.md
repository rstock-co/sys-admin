# TCL 55" QM7K 120Hz Troubleshooting Session

**Date**: 2025-11-27
**Issue**: TCL 55" TV (HDMI-A-3) not running at 120Hz on Intel Arc B580 GPU
**Status**: **CRITICAL - PCIe x1 Bottleneck Discovered** (Must Fix BIOS First)

## 🚨 CURRENT STATUS - Session 4 (Post-BIOS Update + CMOS Reset)

**BLOCKING ISSUE PERSISTS**: GPU still running at **PCIe x1 Gen 1.0** instead of **x8 Gen 4.0**

### Current State (2025-11-27 Late Evening)
- ✅ **BIOS Updated**: Version 2.A91 (September 9, 2025) - AGESA PI 1.2.0.3g
- ⚠️ **CMOS Reset**: Used Clear CMOS button (15 seconds) - **INSUFFICIENT**
  - Did NOT remove battery
  - Did NOT wait 30-60 minutes for full capacitor discharge
  - Arc B580 PCIe switch chip likely retained negotiation state
- ✅ **BIOS Reconfigured**: Above 4G Decoding, Re-Size BAR, PCIe Gen settings verified
- ✅ Kernel parameter applied: `video=HDMI-A-3:3840x2160@120`
- ❌ **PCIe Link**: STILL x1 @ 2.5 GT/s (should be x8 @ 16 GT/s)
- ❌ **Display**: Still 60Hz (4K@120Hz mode not available in driver)

### Root Cause Analysis
The GPU is stuck at **x1 PCIe 1.0** bandwidth (250 MB/s instead of 32 GB/s = **128x slower**). This catastrophic bottleneck is preventing:
1. Proper GPU initialization
2. Full EDID reading from the TV
3. Driver from exposing 4K@120Hz modes
4. Normal display functionality

### Evidence
```bash
# Current PCIe Status (BROKEN)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width   # Shows: 1 (should be 16)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed   # Shows: 2.5 GT/s (should be 16.0 GT/s)

# Available Display Modes (4K@120Hz MISSING)
hyprctl monitors | grep availableModes
# Shows: 2560x1440@120Hz ✅, 1920x1080@120Hz ✅
# Missing: 3840x2160@120Hz ❌
```

### Next Steps
**MUST TRY: Complete CMOS Reset (Extended Method)**

According to [Intel Community success reports](https://community.intel.com/t5/Intel-Arc-Discrete-Graphics/Intel-Arc-B580-stuck-at-PCIe-4-0-x1-instead-of-x8-on-Gigabyte/m-p/1714683), users who fixed this exact issue did:

1. ✅ BIOS update (you did this)
2. ⚠️ **Complete power loss**: PSU off + battery removed + **30-60 minute wait** (you skipped this)
3. Boot and verify

**The Clear CMOS button alone is NOT sufficient** because:
- Arc B580 has onboard Intel PCIe switch chip (device e2f0)
- Switch chip stores PCIe negotiation state
- Button shorts CMOS but capacitors retain charge
- Battery continues powering CMOS during button press
- Only complete discharge (30-60 min) clears the switch chip state

**Action Required**: Follow updated `cmos-reset-simple-guide.md` with battery removal and extended wait time.

**If extended CMOS reset still fails**:
1. Physical GPU reseat (ensure full connection in slot)
2. Try different PCIe x16 slot
3. Check for physical damage
4. Contact ASRock for RMA (defective GPU PCIe switch chip)

---

## ✅ COMPLETED/VERIFIED BIOS SETTINGS (Session 3 - 2025-11-27)

**Physical Installation**:
- ✅ GPU is in the **correct PCIe slot** (topmost x16 slot, `00:01.1`)
- ✅ GPU is fully seated (verified by user)
- ✅ Slot location confirmed via `lspci -tv` topology

**BIOS Settings Verified**:
1. ✅ **Above 4G Decoding**: Enabled (labeled "4G memory / crypto currency mining")
2. ✅ **Re-Size BAR Support**: Enabled
3. ❓ **PCI Lanes Config**: Set to "Enabled" (options: Enabled, x8+x8, x4 configs)
   - **ISSUE**: Root bridge showing x8 instead of x16 - "Enabled" might be x8+x8 mode
   - Need to find setting for full x16 mode
4. ⏳ **AMD CBS → NBIO Common Options**: Still checking for lane width/bifurcation settings

**Current PCIe Status After BIOS Changes**:
```bash
# Root bridge (00:01.1 → 01:00.0)
Link: x8 @ 16.0 GT/s Gen 4 ✅ (Gen speed correct, but width should be x16)

# PCIe switch bridge (02:01.0)
Link: x1 @ 2.5 GT/s Gen 1 ❌ BOTTLENECK HERE!

# GPU (03:00.0)
Link: x1 @ 2.5 GT/s Gen 1 ❌ (inheriting from switch bottleneck)
```

**Root Cause Identified**:
The bottleneck is at the **PCIe switch bridge** (02:01.0), not the GPU itself. The root bridge runs at x8 Gen 4, but the switch drops to x1 Gen 1. This suggests:
1. "PCI Lanes Config = Enabled" might actually be x8+x8 bifurcation mode
2. Need to find explicit "x16" or "Full" mode setting
3. Or there's a separate setting controlling the PCIe switch configuration

**Next Action**:
⚠️ **THE ISSUE IS THE GPU CARD'S OWN PCIe SWITCH, NOT THE MOTHERBOARD**

See the dedicated fix guide: **`arc-b580-pcie-fix-guide.md`**

The solution requires:
1. CMOS Reset (clears PCIe negotiation)
2. GPU Reseat (ensures proper connection)
3. BIOS PCIe settings verification

This is a **known Arc B580 issue** - multiple users fixed it with CMOS reset.

---

## Quick Reference Card (Have this open during BIOS changes)

### What's Wrong
- GPU stuck at **x1 PCIe Gen 1.0** (should be x16 Gen 4/5)
- Display stuck at **60Hz** (want 120Hz)
- PCIe is the blocker - must fix first

### BIOS Quick Nav (MSI MAG X870E)
1. Reboot, press **Delete** repeatedly
2. Press **F7** for Advanced Mode
3. Navigate: **Settings → Advanced → PCI Subsystem Settings**
   - Enable **Above 4G Decoding**
   - Enable **Re-Size BAR Support**
4. Navigate: **Settings → Advanced → AMD CBS → NBIO Common Options → GFX Configuration**
   - Set **GFX0 Gen Switch** to **Gen 5** (or Auto)
   - Ensure **Link Width** is not locked to x1
   - Disable **Bifurcation** if present
5. Press **F10** to Save & Exit

### Verification After Reboot
```bash
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width  # Must show: 16
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed  # Must show: 16.0 GT/s
hyprctl monitors | grep "3840x2160@120"  # Should appear if PCIe fixed
```

### Expected Results
- ✅ Link width: **16** (not 1)
- ✅ Link speed: **16.0 GT/s** or **32.0 GT/s** (not 2.5 GT/s)
- ✅ Display mode **3840x2160@120Hz** appears
- ✅ TV automatically switches to 120Hz (kernel parameter already set)

---

## BIOS Navigation Guide - MSI MAG X870E Tomahawk WiFi

### Purpose
Fix the PCIe x1 bottleneck by ensuring the GPU slot is configured for full x16 Gen 5.0 operation.

### How to Enter BIOS
1. **Restart the computer**
2. **Press `Delete` key repeatedly** during boot (as soon as you see the MSI logo)
3. You'll enter the BIOS/UEFI interface

### BIOS Interface Overview
The MSI X870E has two interface modes:
- **EZ Mode**: Simple, graphical dashboard (default on first boot)
- **Advanced Mode**: Full settings access (what you need)

**Switch to Advanced Mode**: Press `F7` key or click "Advanced" button in top-right

---

### CRITICAL SETTINGS TO CHECK (In Order)

#### 1. Enable Above 4G Decoding (REQUIRED)
This allows the system to allocate resources above 4GB address space for PCIe devices.

**Navigation**:
```
Advanced Mode (F7)
  → Settings (top menu)
    → Advanced
      → PCI Subsystem Settings
        → Above 4G Decoding: [Enabled]
        → Re-Size BAR Support: [Enabled]  (optional but recommended)
```

**What to set**:
- `Above 4G Decoding`: **Enabled**
- `Re-Size BAR Support`: **Enabled** (Intel Arc benefits from this)

---

#### 2. PCIe Slot Configuration (MOST CRITICAL)
This controls the link speed and width for your GPU slot.

**Navigation**:
```
Advanced Mode (F7)
  → Settings (top menu)
    → Advanced
      → AMD CBS
        → NBIO Common Options
          → GFX Configuration
            → PCIe Port Configuration
```

**Look for these settings**:

**Option A: If you see "PCIE1 Link Speed"**:
- `PCIE1 Link Speed`: Set to **Gen 5** or **Auto**
- `PCIE1 Link Width`: Set to **x16** or **Auto**

**Option B: If you see "GFX0 Configuration"** (more likely):
- `GFX0 Gen Switch`: Set to **Gen 5** or **Auto**
- `GFX0 Lane Negotiation`: Set to **Auto** (should not be locked to x1 or x4)

**Option C: Alternative location**:
```
Advanced Mode (F7)
  → Settings
    → Advanced
      → Integrated Peripherals
        → PCI Express Configuration
          → PCIe Slot 1 Configuration
            → Link Speed: Gen 5 or Auto
            → Link Width: x16 or Auto
```

---

#### 3. Disable Any PCIe Bifurcation (If Present)
Bifurcation splits the x16 slot into multiple smaller slots (like 2x8 or 4x4). You want the full x16.

**Navigation**:
```
Advanced Mode (F7)
  → Settings
    → Advanced
      → AMD CBS
        → NBIO Common Options
          → PCIe Configuration
            → PCIE1 Bifurcation: [Disabled] or [x16]
```

**What to set**:
- If you see "Bifurcation" or "Split Configuration": Set to **Disabled** or **x16**

---

#### 4. Verify Integrated Graphics Settings
Make sure iGPU isn't stealing resources from the discrete GPU.

**Navigation**:
```
Advanced Mode (F7)
  → Settings
    → Advanced
      → Integrated Graphics Configuration
        → Integrated Graphics: [Auto] or [Force] (doesn't matter much)
        → UMA Frame Buffer Size: [Auto]
        → Primary Display: [Auto] or [PEG] (PEG = PCIe Graphics)
```

**What to set**:
- `Primary Display`: **Auto** or **PEG** (PEG forces PCIe GPU as primary)

---

#### 5. Extreme Settings (Only if above doesn't work)
Some boards have hidden or poorly labeled settings.

**Check these locations if nothing above worked**:

```
Advanced Mode (F7)
  → OC (Overclocking menu)
    → Advanced CPU Configuration
      → PCIe Configuration
        → PCIe Speed: Gen 5
```

OR

```
Advanced Mode (F7)
  → Settings
    → Advanced
      → AMD Overclocking
        → PCIe Bus Configuration
          → PCIe Gen Speed: Gen 5
```

---

### Step-by-Step BIOS Fix Procedure

**Before You Start**:
- Have this guide open on your phone or another device (you won't have display once in BIOS)
- Side monitors (Samsung 32") should still work even if main TV fails

**Procedure**:

1. **Reboot and enter BIOS** (press Delete during boot)

2. **Press F7** to enter Advanced Mode

3. **Fix Above 4G Decoding first**:
   - Settings → Advanced → PCI Subsystem Settings
   - Enable "Above 4G Decoding"
   - Enable "Re-Size BAR Support"

4. **Fix PCIe Slot Configuration**:
   - Settings → Advanced → AMD CBS → NBIO Common Options → GFX Configuration
   - Find settings for "GFX0 Gen Switch" or "PCIE1 Link Speed"
   - Set to **Gen 5** (or Gen 4 if Gen 5 isn't available)
   - Ensure nothing is locked to "x1" or "x4"

5. **Check for Bifurcation**:
   - Same menu area (NBIO Common Options)
   - If you see "Bifurcation", set to **Disabled** or **x16**

6. **Set Primary Display** (optional):
   - Settings → Advanced → Integrated Graphics Configuration
   - Set "Primary Display" to **PEG** (forces PCIe GPU)

7. **Save and Exit**:
   - Press F10 (Save & Exit)
   - Confirm "Yes"
   - System will reboot

---

### After BIOS Changes - Verification Commands

Once system boots back into Linux, run these commands:

```bash
# Check PCIe link width (should show 16)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width

# Check PCIe link speed (should show 16.0 GT/s or 32.0 GT/s)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed

# Check max capabilities
cat /sys/bus/pci/devices/0000:03:00.0/max_link_width
cat /sys/bus/pci/devices/0000:03:00.0/max_link_speed

# Check if 120Hz mode is now available
hyprctl monitors | grep "3840x2160@120"
```

**Expected Results**:
```
current_link_width: 16
current_link_speed: 16.0 GT/s PCIe  (Gen 4) or 32.0 GT/s PCIe (Gen 5)
max_link_width: 16
max_link_speed: 16.0 GT/s PCIe or higher
```

**If still showing x1**:
- Double-check you saved BIOS settings (F10)
- Try physically reseating the GPU in the slot
- Check if there's a physical switch or jumper on the motherboard
- Verify GPU is in the topmost PCIe x16 slot (closest to CPU)

---

### Troubleshooting BIOS Navigation

**Can't find "AMD CBS"**:
- Try looking under "Advanced CPU Settings" or "CPU Configuration"
- Some BIOS versions label it differently

**Can't find "GFX Configuration"**:
- Try "PCI Configuration" or "PCIe Configuration"
- Look for anything mentioning "Slot 1" or "Primary PCIe"

**Settings are grayed out (can't change)**:
- Might need to disable "EZ Mode" features first
- Try setting "CPU Overclocking" to "Enabled" first (sometimes unlocks other settings)

**BIOS looks completely different**:
- Take a photo with your phone and reference it
- Look for menus with "PCI", "PCIe", "Graphics", or "Slot"
- Settings MUST exist somewhere - MSI boards always expose PCIe configuration

---

## Background (Session 1 - Original Investigation)

### The Problem

The TCL 55QM7K TV was successfully running at 120Hz 4K when connected to the **motherboard's integrated graphics** (AMD Ryzen 9 7950X), but when the same HDMI cable was plugged into the **Intel Arc B580 GPU**, it would only run at 60Hz.

**Key Evidence**:
- Same cable ✅
- Same TV ✅
- Same HDMI port on TV ✅
- Worked at 120Hz on motherboard just minutes before ❌
- Only runs at 60Hz on GPU ❌

### System Configuration

**Hardware**:
- **CPU**: AMD Ryzen 9 7950X (has integrated graphics)
- **GPU**: Intel Arc B580 12GB (ASRock Challenger OC)
- **TV**: TCL 55QM7K (HDMI 2.1 capable)
- **Connection**: HDMI 2.1 cable from GPU HDMI port to TV

**Software**:
- **OS**: Arch Linux
- **Kernel**: 6.17.9-arch1-1
- **Mesa**: 25.2.7
- **Driver**: `xe` (Intel Arc driver)
- **Compositor**: Hyprland (Wayland)

**Display Setup**:
- DP-1: Samsung 32" 4K @ 60Hz (portrait, left)
- HDMI-A-3: TCL 55" 4K @ 60Hz → **want 120Hz** (center)
- DP-2: Samsung 32" 4K @ 60Hz (portrait, right)

---

## Investigation Process

### Step 1: Check Current Display Configuration

Ran `hyprctl monitors` and confirmed:
```
Monitor HDMI-A-3 (ID 2):
	3840x2160@60.00000 at 8160x0
```

**Finding**: TV running at 60Hz, not advertising 120Hz in `availableModes` list.

### Step 2: Initial Troubleshooting Attempts

1. **Updated Hyprland config**: Changed monitor designation from `HDMI-A-5` (old port when connected to motherboard) to `HDMI-A-3` (new port on GPU)
   - File: `~/.config/hypr/hyprland.conf`
   - Line 31: `monitor=HDMI-A-3,3840x2160@120,2160x840,1,vrr,0`

2. **Reloaded Hyprland**: `hyprctl reload`

3. **Attempted to force 120Hz**: `hyprctl keyword monitor HDMI-A-3,3840x2160@120,8160x0,1`
   - Command accepted: `ok`
   - **Result**: Still showed 60Hz - kernel wasn't offering the mode

**Conclusion**: The issue wasn't Hyprland configuration. The kernel/driver wasn't detecting or offering 120Hz modes.

### Step 3: EDID Analysis (The Breakthrough)

Installed `v4l-utils` package to get `edid-decode` tool:
```bash
sudo pacman -S v4l-utils
```

Extracted and decoded the TV's EDID:
```bash
cat /sys/class/drm/card0/card0-HDMI-A-3/edid > ~/edid-custom/tcl-original.bin
edid-decode ~/edid-custom/tcl-original.bin
```

**Critical Discovery**: The TV **IS** advertising 120Hz and even 144Hz modes!

```
VIC 118:  3840x2160  120.000000 Hz  16:9    270.000 kHz   1188.000000 MHz
VTDB 1:   3840x2160  143.935698 Hz  16:9    338.249 kHz   1829.250000 MHz
VTDB 4:   3840x2160  144.000362 Hz  16:9    333.217 kHz   1306.210000 MHz
```

**Key EDID Details**:
- **HDMI 1.4 TMDS Limit**: 340 MHz
- **HDMI 2.1 TMDS Limit**: 600 MHz (from HDMI Forum VSDB)
- **YCbCr 4:2:0 Capability**: VIC 118 (120Hz) marked as requiring YCbCr 4:2:0 color format

### Step 4: Root Cause Identified

**The Problem**: The Intel Arc `xe` driver is not properly parsing or accepting the 120Hz/144Hz modes from the EDID, even though they're correctly advertised.

**Possible Driver Issues**:
1. Driver might be using old HDMI 1.4 TMDS limit (340 MHz) instead of HDMI 2.1 limit (600 MHz)
2. Driver might not be enabling YCbCr 4:2:0 output mode (required for 120Hz within bandwidth limits)
3. Driver might have bugs with HDMI 2.1 feature negotiation (Arc B580 is very new hardware, released Dec 2024)

**Why it worked on motherboard**:
- AMD integrated graphics driver handles EDID parsing and HDMI 2.1 differently
- Different driver = different EDID interpretation = different available modes

---

## Solution Implemented

### Approach: Force 120Hz Mode via Kernel Parameter

Since the EDID is correct but the driver isn't offering the mode, we bypassed driver detection by telling the kernel to force the mode at boot.

**Edit Made**:
- File: `/boot/loader/entries/arch.conf`
- Line 4 changed from:
  ```
  options	root=/dev/nvme0n1p2 rw
  ```
  To:
  ```
  options	root=/dev/nvme0n1p2 rw video=HDMI-A-3:3840x2160@120
  ```

**What This Does**:
- The `video=` kernel parameter forces the kernel DRM subsystem to set HDMI-A-3 to 3840x2160@120Hz regardless of what modes the driver thinks are available
- This bypasses the driver's mode filtering and EDID parsing

**Safety**:
- Parameter is port-specific (`HDMI-A-3` only)
- DP-1 and DP-2 (Samsung monitors) are unaffected
- If TV fails, the two side monitors will still work
- Reversible: Boot with motherboard HDMI, edit file, remove parameter, reboot

---

## Verification Steps (After Reboot)

### 1. Check if 120Hz is Active

```bash
hyprctl monitors | grep -A 5 "HDMI-A-3"
```

**Expected output**:
```
Monitor HDMI-A-3 (ID 2):
	3840x2160@120.00000 at 2160x840
```

Look for `@120.00000` instead of `@60.00000`.

### 2. Verify in availableModes

```bash
hyprctl monitors | grep -A 50 "HDMI-A-3" | grep availableModes
```

Check if 120Hz appears in the list now.

### 3. Visual Confirmation

- Check if there's any flickering or instability
- Test with fast-moving content (scroll code rapidly, move windows)
- 120Hz should feel noticeably smoother than 60Hz

### 4. Check Logs for Issues

```bash
journalctl -b 0 | grep -i "hdmi\|drm.*mode\|3840x2160"
```

Look for any errors or warnings about the forced mode.

---

## If It Doesn't Work

### Scenario 1: TV Shows Nothing (Black Screen)

**Recovery**:
1. Samsung monitors (DP-1, DP-2) should still work
2. Use side monitors to access the system
3. Edit `/boot/loader/entries/arch.conf` and remove `video=HDMI-A-3:3840x2160@120`
4. Reboot

**Alternative Recovery** (if all displays fail):
1. Plug monitor into **motherboard HDMI port**
2. System boots normally on integrated graphics
3. Edit `/boot/loader/entries/arch.conf` and remove the parameter
4. Reboot, plug back into GPU

### Scenario 2: TV Works But Still Shows 60Hz

**Possible Issues**:
- Driver might be overriding the kernel parameter
- TV might be falling back to 60Hz due to signal issues
- YCbCr 4:2:0 mode might not be enabled

**Next Steps to Try**:
1. Check TV settings for "HDMI 2.1" or "Enhanced HDMI" mode
2. Try adding more specific kernel parameters:
   ```
   video=HDMI-A-3:3840x2160@120e
   ```
   (The `e` means "enable")

3. Try forcing YCbCr color format:
   ```
   video=HDMI-A-3:3840x2160@120 drm.force_ycbcr420=HDMI-A-3
   ```

### Scenario 3: Display Works But Flickers/Unstable

**Possible Issues**:
- Bandwidth limitations
- Cable not certified for HDMI 2.1 (though user confirmed it worked on motherboard)
- Driver instability with forced mode

**Next Steps**:
1. Try dropping to 100Hz: `video=HDMI-A-3:3840x2160@100`
2. Update kernel/mesa to latest versions
3. Check Arc driver bug reports and kernel changelogs

---

## Alternative Solutions (If Kernel Parameter Doesn't Work)

### Option 1: Custom EDID Override

If the kernel parameter doesn't work, we can create a modified EDID that forces the driver to accept 120Hz:

1. Extract current EDID (already done): `~/edid-custom/tcl-original.bin`
2. Modify EDID to prioritize 120Hz mode (requires EDID editing tools)
3. Save to `/lib/firmware/edid/tcl-120hz.bin`
4. Add kernel parameter: `drm.edid_firmware=HDMI-A-3:edid/tcl-120hz.bin`
5. Reboot

**Pros**: More comprehensive, tells driver exactly what to do
**Cons**: More complex, requires EDID editing knowledge

### Option 2: Wait for Driver Updates

The Arc B580 is brand new (Dec 2024), and the `xe` driver is still maturing. HDMI 2.1 support bugs are expected.

**Monitor**:
- Arch Linux kernel updates
- Mesa driver updates
- Intel xe driver patches

Check changelogs for HDMI 2.1, Arc B580, or high refresh rate fixes.

### Option 3: DisplayPort + Active Adapter

If all else fails:
- Use one of the GPU's DisplayPort 1.4a outputs
- Get a **DisplayPort to HDMI 2.1 active adapter** (~$50-100)
- DisplayPort 1.4a can easily handle 4K@120Hz
- Adapter handles conversion to HDMI 2.1 for TV

**Pros**: Guaranteed to work, bypasses driver HDMI issues
**Cons**: Extra cost, extra cable/adapter to manage

---

## Technical Details for Reference

### Display Identifiers
- **Kernel/DRM**: `HDMI-A-3`
- **Hyprland**: `HDMI-A-3`
- **Physical port**: GPU HDMI output (only one on Arc B580)

### EDID Information
- **Manufacturer**: Technical Concepts Ltd (TCL)
- **Model**: Beyond TV
- **EDID Size**: 512 bytes (4 blocks)
- **HDMI Version**: 2.1 capable (600 MHz TMDS rate)

### Supported Modes (per EDID)
- 3840x2160 @ 24/25/30/50/60Hz (standard)
- 3840x2160 @ 120Hz (VIC 118, requires YCbCr 4:2:0)
- 3840x2160 @ 143.9Hz (VTDB custom timing)
- 3840x2160 @ 144Hz (VTDB detailed timing)

### Bandwidth Requirements
- **4K @ 60Hz RGB 8-bit**: ~12.54 Gbps
- **4K @ 120Hz RGB 8-bit**: ~25.08 Gbps (exceeds HDMI 2.0)
- **4K @ 120Hz YCbCr 4:2:0**: ~12.54 Gbps (fits within HDMI 2.0)
- **4K @ 120Hz with HDMI 2.1 DSC**: Variable (compression)

### Why YCbCr 4:2:0 is Used
- Chroma subsampling reduces bandwidth by ~50%
- Imperceptible quality loss for video content
- Allows 120Hz within HDMI bandwidth limits
- Standard technique for high refresh 4K displays

---

## Files Modified

1. `/home/neo/.config/hypr/hyprland.conf`
   - Line 31: Changed `HDMI-A-5` → `HDMI-A-3`

2. `/boot/loader/entries/arch.conf`
   - Line 4: Added `video=HDMI-A-3:3840x2160@120` parameter

## Files Created

1. `~/edid-custom/tcl-original.bin` - Extracted EDID from TV
2. `~/edid-custom/edid-decode/` - Attempted tool build (not needed)

---

## Next Session Checklist (Post-BIOS Fix)

### Priority 1: Fix PCIe x1 Bottleneck (BLOCKING)
- [ ] Enter BIOS (Delete key during boot)
- [ ] Enable Above 4G Decoding
- [ ] Enable Re-Size BAR Support
- [ ] Set PCIe Slot 1 to Gen 5 (or Gen 4)
- [ ] Ensure Link Width is x16 (not x1)
- [ ] Disable PCIe Bifurcation if present
- [ ] Save BIOS settings (F10)

### Priority 2: Verify PCIe Fix After Reboot
- [ ] Check link width: `cat /sys/bus/pci/devices/0000:03:00.0/current_link_width` (must show 16)
- [ ] Check link speed: `cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed` (must show 16.0 GT/s or higher)
- [ ] Verify GPU is using full bandwidth (not 2.5 GT/s)

### Priority 3: Verify 120Hz Working
- [ ] Check if 3840x2160@120Hz appears in available modes
- [ ] Verify TV running at 120Hz: `hyprctl monitors | grep "3840x2160@120"`
- [ ] Check for visual artifacts or flickering
- [ ] Test performance/smoothness with real usage
- [ ] Check kernel logs for any warnings: `journalctl -b 0 | grep -i drm`

### Priority 4: If Still Not Working
- [ ] Try kernel parameter variations (see "Scenario 2" section)
- [ ] Consider custom EDID override (see "Option 1" section)
- [ ] Check for BIOS updates from MSI
- [ ] Consider DisplayPort to HDMI 2.1 adapter (see "Option 3" section)

### Success Criteria
✅ PCIe link at x16 @ 16 GT/s (or 32 GT/s for Gen 5)
✅ Display mode 3840x2160@120Hz appears in availableModes
✅ Monitor actively running at 120Hz without artifacts
✅ Smooth scrolling and window movement (visually noticeable improvement)

---

## Key Learnings

### Session 1 (Original Investigation)
1. **EDID is not the problem** - The TV correctly advertises 120Hz modes
2. **Driver parsing is the issue** - Arc `xe` driver not accepting advertised modes
3. **Port naming changes** - HDMI-A-5 (motherboard) became HDMI-A-3 (GPU)
4. **YCbCr 4:2:0 is normal** - Standard method for high refresh 4K displays
5. **Kernel parameters can bypass driver limits** - Force modes the hardware supports
6. **New hardware = driver bugs** - Arc B580 is very new, expect HDMI 2.1 issues

### Session 2 (PCIe Bottleneck Discovery)
7. **PCIe x1 bottleneck is catastrophic** - GPU at x1 Gen 1.0 = 128x slower bandwidth (250 MB/s vs 32 GB/s)
8. **PCIe issues prevent proper GPU initialization** - Can't read EDID, can't expose modes, can't function normally
9. **BIOS settings don't always stick** - Changed "Gen Switch" to Gen 5 but didn't take effect
10. **Above 4G Decoding is critical** - Often required for proper PCIe resource allocation
11. **Multiple BIOS settings control PCIe** - Need to check Gen Switch, Link Width, Bifurcation, and Above 4G
12. **Driver won't expose 4K@120Hz without proper PCIe** - Even with kernel parameter, modes won't appear if PCIe is broken
13. **Lower resolution 120Hz works** - 1920x1080@120Hz and 2560x1440@120Hz available, proving TV and driver support 120Hz
14. **Fix PCIe first, then 120Hz** - Can't troubleshoot display modes until GPU has proper bandwidth

---

## References

- Hyprland monitors config: https://wiki.hyprland.org/Configuring/Monitors/
- Kernel video= parameter: https://www.kernel.org/doc/html/latest/fb/modedb.html
- EDID specification: https://en.wikipedia.org/wiki/Extended_Display_Identification_Data
- Intel Arc B580 specs: Released December 2024, HDMI 2.1 support
- TCL 55QM7K specs: QD-Mini LED, HDMI 2.1, 120Hz native support
