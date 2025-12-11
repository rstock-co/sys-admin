# YUNZII AL98 Keyboard Troubleshooting

**Last Updated:** 2025-11-30
**Keyboard Model:** YUNZII AL98 QMK/VIA Wireless Mechanical Gaming Keyboard

---

## Quick Status Overview

| Issue | Status | Summary |
|-------|--------|---------|
| **Super Key Not Working** | ✅ RESOLVED | Win key was locked (Fn+Win) - factory reset fixed it |
| **VIA Web App Connection** | ✅ RESOLVED | Needed udev permissions + wired-only mode |
| **Persistent Red Light** | ✅ RESOLVED | Low battery warning - factory reset fixed it |
| **Ctrl+V Paste Conflict** | ✅ RESOLVED | Hyprland config was using CTRL_R - reverted to SUPER |
| **Bluetooth Connectivity** | ⚠️ NOT TESTED | Using 2.4GHz wireless dongle (works fine) |

## Custom Key Remaps (VIA)

| Key | Remap | Purpose |
|-----|-------|---------|
| **Caps Lock** | `MT(MOD_LALT,KC_F13)` | Tap = F13 (hyprwhspr dictation), Hold = Left Alt |

**Backup location:** `~/agents/sys-admin/keyboard/yunzii-al98-custom-layout.json`

---

## Keyboard Hardware Info

- **Model:** YUNZII AL98 QMK/VIA Wireless Mechanical Gaming Keyboard
- **Layout:** 1800 compact (98 keys)
- **Connection modes:** USB-C (wired), Bluetooth 5.0, 2.4GHz wireless (via USB dongle)
- **Current mode:** Wired (for VIA config) or 2.4GHz wireless (daily use)
- **Switches:** Factory pre-lubed Milk V2 linear
- **VIA/QMK:** Supported (requires JSON sideload)
- **USB ID:** `28e9:3174` (GDMicroelectronics YUNZII AL98)

---

## Understanding the Firmware

The YUNZII AL98 ships with **VIA firmware** (NOT Vial firmware). Critical findings:
- Keyboard uses VIA configurator tools (usevia.app)
- Does NOT have Vial magic number (`vial:f64c2b3c`) in USB serial attribute
- **No Vial firmware exists for AL98** - it's VIA-only
- Keyboard is NOT in VIA's official supported database, requires JSON sideloading
- JSON file location: `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`
- **VIA only works in wired mode** - switch mode selector to "Wired" and use USB-C cable

---

# Issue #1: Super/Win Key Not Working

**Status:** ✅ RESOLVED (2025-11-30)

## Problem

Super key (Windows key) on YUNZII AL98 keyboard not functioning in Hyprland. Cannot trigger keybinds like `Super+Return` (open terminal).

## Root Cause (INCORRECT - See Actual Solution)

~~The YUNZII AL98 has a firmware-level block on the LWin keycode.~~ **This was wrong!**

## Actual Solution

The Win key was **locked**, not broken. From the manual's ATTENTION section:

> When the Win-Key is used abnormally, please check if the Win-Key lights up in white, if so, please press the `Fn+Win` to unlock the Win-Key

**How to fix:**
1. Press **`Fn + Win`** to unlock Win key (if locked, it lights up white)
2. Ensure Windows mode is active: press **`Fn + A`** (LOG LED should flash white 3 times)
3. If still not working, do factory reset: **Long press `Fn + Spacebar`** (backlight flashes white 3 times)

### Testing Confirmed Working

After factory reset:
- `evtest` shows `KEY_LEFTMETA` when pressing Win key
- Win + Return opens Alacritty terminal
- All Hyprland keybinds functional with SUPER key

### What Was Wrong Before

Previous troubleshooting incorrectly concluded the keyboard firmware blocked the LWin keycode. The actual issue was:
- Win key was locked via `Fn+Win` (gaming mode to prevent accidental Win key presses)
- Keyboard may have been in macOS mode (`Fn+S`) where Win/Alt keys are swapped
- Factory reset cleared all settings and returned keyboard to working state

---

# Issue #2: VIA Web App Connection Failed

**Status:** ✅ RESOLVED (2025-11-30)

## Problem

Cannot connect keyboard to usevia.app. Two errors appeared:
1. **NotAllowedError: Failed to open the device**
2. **Received invalid protocol version from device**

## Root Causes

1. **Permissions issue**: After factory reset, hidraw devices had `crw-------` (root-only) permissions instead of `crw-rw-rw-` (world-readable)
2. **Connection mode**: VIA requires wired mode - both USB-C and 2.4GHz dongle were connected simultaneously, confusing the firmware

## Solution

### Step 1: Switch to Wired-Only Mode

1. Set keyboard's physical mode switch to **"Wired"**
2. **Unplug the 2.4GHz USB dongle** from computer
3. Keep only USB-C cable connected
4. Verify with `lsusb | grep -i yunzii` - should see only one device

### Step 2: Fix udev Permissions

Create udev rule to allow user access to keyboard's hidraw devices:

```bash
echo '# YUNZII AL98 keyboard - Allow user access for VIA configuration
KERNEL=="hidraw*", ATTRS{idVendor}=="28e9", ATTRS{idProduct}=="3174", MODE="0666", TAG+="uaccess"' | sudo tee /etc/udev/rules.d/50-yunzii-al98.rules
```

Reload udev rules:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Unplug and replug USB-C cable.

Verify permissions changed:
```bash
ls -la /dev/hidraw* | grep -E "hidraw[0-3]"
```

Should now show `crw-rw-rw-` (world-readable/writable).

### Step 3: Connect to VIA

1. Go to https://usevia.app/ in Chrome
2. Click **Settings** (gear icon) → Enable **"Show Design tab"**
3. Click **DESIGN** tab
4. Load JSON file: `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`
5. If protocol version error, click **"Use V2 definitions (deprecated)"**
6. Click **CONFIGURE** tab
7. Click **"Authorize device +"**
8. Select "SmartCloud YUNZII AL98" from Chrome popup
9. Keyboard layout should appear - ready for remapping!

---

# Issue #3: Persistent Red LED Breathing Light

**Status:** ✅ RESOLVED (2025-11-30)

## Problem

Red LED permanently on in top-left corner of keyboard (behind metal cutout of cloud). Light slowly fades in and out continuously.

## Root Cause

**Low battery warning.** From the manual (Battery Information section):

> When the battery is below 10%, the LOG LED will flash red quickly.

The breathing red light indicated the battery was below 10%. It started appearing after Bluetooth pairing attempts because wireless mode drains battery faster.

## Solution

Factory reset (`Fn + Spacebar`) cleared the issue. LED returned to multi-colored normal state.

### Battery Indicators Reference

- **Red LED flashing quickly** = Low battery (below 10%)
- **Red LED solid on** = Charging
- **Green LED solid for 5 seconds** = Fully charged

### Battery Management

Check battery level: Press `Fn + Right Ctrl` (number keys 1-0 illuminate to show percentage)

---

# Issue #4: Ctrl+V Paste Not Working

**Status:** ✅ RESOLVED (2025-11-30)

## Problem

Pressing Left Ctrl + V triggered Hyprland's `togglefloating` action instead of paste.

## Root Cause

Hyprland config was set to `$mainMod = CTRL_R` (from previous incorrect workaround for Win key issue). When the keybind `bind = $mainMod, V, togglefloating,` was evaluated, it became Ctrl + V.

## Solution

Reverted Hyprland config to use SUPER key:

File: `~/.config/hypr/hyprland.conf` line 244:
```
$mainMod = SUPER # Windows/Super key as main modifier
```

Reloaded Hyprland: `hyprctl reload`

Now:
- ✅ Ctrl + V works for paste
- ✅ Win + V triggers togglefloating
- ✅ All other keybinds work with Win key

---

# VIA Configuration Reference

## Software Status

- **vial-appimage** (AUR) - v0.7.5 - **REMOVED** (not compatible with AL98)
- **via** (AUR) - v3.0.0 - **INSTALLED** (desktop GUI configurator)
- **udev rule:** `/etc/udev/rules.d/50-yunzii-al98.rules` - **ACTIVE** (allows WebHID access)

**Reason for Vial removal:** Vial is incompatible with AL98 - keyboard has VIA firmware, not Vial firmware. No Vial firmware exists for this keyboard.

## ✅ Method: VIA Web App (usevia.app) - WORKING

**Requirements:**
- Wired mode only (USB-C cable)
- udev permissions configured
- Chrome/Chromium/Edge browser

**Initial Setup:**
1. Switch keyboard to **Wired mode** (physical switch)
2. Unplug 2.4GHz dongle
3. Connect USB-C cable only
4. Open https://usevia.app/ in Chrome
5. Click **Settings** → Enable **"Show Design tab"**
6. Click **DESIGN** tab
7. Load JSON: `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`
8. Click **CONFIGURE** tab
9. Click **"Authorize device +"**
10. Select keyboard from popup
11. Layout appears - ready for remapping

**⚠️ Important: Backup Custom Keybinds**

VIA saves keybinds to the keyboard's EEPROM (firmware storage), but **factory reset (`Fn + Spacebar`) will erase all custom keybinds**. Always backup after customizing:

**To Backup:**
1. After configuring keybinds, go to **SAVE+LOAD** tab in usevia.app
2. Click **"Save current layout"** - downloads JSON with your custom mappings
3. Save to: `/home/neo/agents/sys-admin/keyboard/yunzii-al98-custom-layout.json`
4. Commit to sys-admin repo: `git add keyboard/ && git commit -m "Backup YUNZII AL98 custom keybinds" && git push`

**To Restore After Factory Reset:**
1. Connect to VIA (load keyboard definition JSON first)
2. Go to **SAVE+LOAD** tab
3. Click **"Load saved layout"**
4. Select your backup: `~/agents/sys-admin/keyboard/yunzii-al98-custom-layout.json`
5. Custom keybinds restored to keyboard firmware

**Lighting Control Note:**

Don't use VIA for lighting changes - it triggers error state (red breathing cloud LED). Use Fn key combinations instead:
- `Fn + Backspace` - Backlight ON/OFF
- `Fn + \` - Change effect
- `Fn + Enter` - Change color
- `Fn + ↑/↓` - Brightness
- `Fn + →/←` - Speed

If cloud LED turns red and breathing, factory reset keyboard: `Fn + Spacebar` (then restore keybinds from backup).

## ❌ Method: Vial Desktop/Web - NOT COMPATIBLE

- Vial desktop app: Requires Vial firmware (AL98 has VIA firmware)
- Vial web app: No "Sideload VIA JSON" feature
- **Do not use Vial tools** - AL98 is VIA-only

---

# Files & Paths

- **Keyboard definition JSON:** `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`
- **Custom keybinds backup:** `~/agents/sys-admin/keyboard/yunzii-al98-custom-layout.json` (save after customizing)
- **VIA web app:** https://usevia.app/
- **Hyprland config:** `~/.config/hypr/hyprland.conf` (line 244: `$mainMod = SUPER`)
- **udev rule:** `/etc/udev/rules.d/50-yunzii-al98.rules`

---

# Keyboard Manual Reference

See `keyboard-manual.md` in this directory for complete manual.

## Critical Keyboard Shortcuts

- **Factory Reset:** Long press `Fn + Spacebar` (backlight flashes white 3 times)
- **Lock/Unlock Win Key:** `Fn + Win` (key lights up white when locked)
- **Windows Mode:** `Fn + A` (LOG LED flashes white 3 times)
- **macOS Mode:** `Fn + S` (LOG LED flashes white 3 times)
- **Battery Check:** `Fn + Right Ctrl` (number keys show percentage)

## Connection Mode Switch

Physical switch on keyboard (back/side):
- **Wired** - USB-C cable (required for VIA configuration)
- **2.4G** - Wireless dongle (daily use)
- **BT** - Bluetooth (not tested)

---

# Resources

## VIA Documentation
- [VIA JSON Loading - CannonKeys](https://docs.cannonkeys.com/via-json-loading/)
- [VIA Usage Guide - Keebio](https://docs.keeb.io/via)
- [How to Use VIA - Keychron](https://www.keychron.com/blogs/archived/how-to-use-via-to-program-your-keyboard)
- [How to Use VIA - Epomaker](https://epomaker.com/blogs/guides/how-to-use-via-for-beginners)

## YUNZII Resources
- [YUNZII Software Page](https://www.yunzii.com/pages/software)
- [YUNZII Manual Pages](https://www.yunzii.com/pages/manuals)

---

# Lessons Learned

1. **Always check the manual first** - Win key lock feature and factory reset instructions were documented
2. **Factory reset is powerful** - Clears firmware state issues, locked keys, and strange behavior
3. **VIA requires specific setup** - Wired mode only, proper permissions, JSON sideload for unsupported keyboards
4. **Don't jump to firmware conclusions** - "Firmware blocks LWin" was incorrect; key was just locked
5. **LED indicators have meaning** - Red breathing = low battery, not a bug
6. **One connection at a time** - Having both USB-C and 2.4GHz dongle confused the keyboard
