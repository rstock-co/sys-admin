# YUNZII AL98 Keyboard Troubleshooting

**Date:** 2025-11-28
**Status:** RESOLVED - Super key firmware bug bypassed via Caps Lock remapping

---

## Original Issue

Super key (Windows key) on YUNZII AL98 keyboard is not functioning in Hyprland. Cannot trigger keybinds like `Super+Return` (open terminal).

## Resolution

**Root cause:** YUNZII AL98 firmware blocks the LWin/Super keycode at the firmware level. Any physical key mapped to LWin gets blocked - not just the physical Windows key, but ANY key assigned to send LWin.

**Solution:**
1. Remapped Caps Lock → Right Ctrl in VIA (usevia.app)
2. Changed Hyprland mod key from `SUPER` to `CTRL_R` in `~/.config/hypr/hyprland.conf`
3. Now Caps Lock functions as the Super/Mod key for all Hyprland keybinds

**Working:** All Hyprland keybinds now work with Caps Lock as modifier (e.g., Caps Lock + Return opens terminal)

---

## What Works

- ✅ Keyboard detected by system: `lsusb` shows `ID 28e9:3174 GDMicroelectronics YUNZII AL98`
- ✅ Regular typing works (all letter/number keys functional)
- ✅ Keyboard is connected via USB-C (wired mode)
- ✅ Vial detects keyboard: Shows "smartCloud YUNZII AL98" at top
- ✅ JSON file sideloaded: `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`

---

## What Doesn't Work

- ❌ Super key not sending keypress
- ❌ Vial GUI keys not clickable (can't select/remap keys in GUI)
- ❌ Hyprland keybinds with Super modifier don't trigger
- ❌ **Vial desktop app error:** "unsupported protocol version, please download latest Vial from..."

---

## Software Installed

- **vial-appimage** (AUR) - v0.7.5 - **REMOVED** (not compatible with AL98)
- **udev rules:** All Vial-related udev rules **REMOVED**
  - Removed `/etc/udev/rules.d/92-viia.rules`
  - Removed `/etc/udev/rules.d/59-vial.rules`
  - udev reloaded after cleanup
- **Vial config cleaned:**
  - Removed `~/.config/Vial` (if existed)
  - Removed `~/.local/share/Vial` (if existed)

**Reason for removal:** Vial is incompatible with AL98 - keyboard has VIA firmware, not Vial firmware. No Vial firmware exists for this keyboard.

---

## Keyboard Configuration - Tested Methods

### Understanding the Firmware
The YUNZII AL98 ships with **VIA firmware** (NOT Vial firmware). Critical findings:
- Keyboard uses VIA configurator tools
- Does NOT have Vial magic number (`vial:f64c2b3c`) in USB serial attribute
- Confirmed via `HID_UNIQ=` being empty when checking `/sys/class/hidraw/*/device/uevent`
- **No Vial firmware exists for AL98** - it's VIA-only
- Keyboard is NOT in VIA's official supported database, requires JSON sideloading
- JSON file location: `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`

---

### ❌ Method 1: Vial Desktop App - FAILED
**Tested:** Vial desktop app v0.7.5 (vial-appimage from AUR)

**Initial error:** "On linux you need to set up a custom udev rule for keyboards to be detected. Follow the instructions linked here: https://get.vial.today/manual/linux-udev.html"

**udev rules attempted:**
1. Created `/etc/udev/rules.d/59-vial.rules` with official Vial rule:
   ```
   KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{serial}=="*vial:f64c2b3c*", MODE="0660", GROUP="users", TAG+="uaccess", TAG+="udev-acl"
   ```
2. Reloaded udev rules and replugged keyboard
3. **Still failed** - keyboard not detected

**Root cause:** The udev rule looks for `vial:f64c2b3c` magic number in the keyboard's USB serial attribute (`ATTRS{serial}`). The AL98 does NOT have this magic number because it ships with VIA firmware, not Vial firmware. Confirmed by checking `HID_UNIQ=` (empty) in sysfs.

**Additional issues:**
- Protocol version error when attempting to sideload VIA JSON file
- Desktop app v0.7.5 doesn't support VIA keyboards properly
- "Sideload VIA JSON" feature exists in desktop app but fails due to protocol mismatch

**Why it failed:** Keyboard has VIA firmware (not Vial), lacks Vial magic number, and no Vial firmware exists for AL98.

---

### ❌ Method 2: VIA Web App (usevia.app) - Initial Attempt FAILED
**Tested:** https://usevia.app/ in Google Chrome

**Steps attempted (incorrect order):**
1. Opened usevia.app in Chrome
2. Clicked "Authorize device +" button FIRST (wrong - need to load JSON first!)
3. Chrome popup appeared showing "SmartCloud YUNZII AL98"
4. Selected keyboard and clicked "Connect"
5. Popup closed but nothing happened - remained on "Authorize device +" screen

**Why it failed:** Tried to authorize device BEFORE loading the JSON definition file. usevia.app expects keyboards to be in VIA's official supported database (https://caniusevia.com/docs/supported_keyboards). The AL98 is NOT listed, so VIA doesn't know what to do with it until you load the JSON file first.

**Note:** Keyboard shows up as 4 separate HID devices (hidraw1-4) with vendor ID `28e9:3174`, all with world-readable permissions (`rw-rw-rw-`), so permissions are NOT the issue.

---

### ✅ Method 2 (Corrected): VIA Web App (usevia.app) - CONFIRMED WORKING
**Use:** https://usevia.app/ in Google Chrome/Chromium/Edge

**Correct steps (load JSON FIRST, then authorize):**
1. Open https://usevia.app/ in Chrome
2. Click **Settings** button (gear icon, top right)
3. Enable **"Show Design tab"**
4. Click the **DESIGN** tab (now visible at top)
5. Click **"Load"** button or drag-and-drop JSON file
6. Select JSON file: `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`
7. If protocol version error appears, click **"Use V2 definitions (deprecated)"** and try loading again
8. Once JSON loaded successfully, click **CONFIGURE** tab
9. Keyboard layout appears automatically (may not need explicit "Authorize device +" - already connected)
10. **Test:** Press Super/Win key on physical keyboard - should see corresponding key light up on screen (labeled "LWin")
11. Keyboard is now connected and ready for remapping!

**Confirmed working:** Super key shows as "LWin" on the visual layout and lights up when pressed in Key Tester tab.

**However:** Super key not sending actual events to the system. Confirmed via `evtest` - pressing Super key produces NO output, even though keyboard supports `KEY_LEFTMETA` (event code 125).

**Attempted fix in VIA:**
1. Clicked LWin key on visual layout
2. Reassigned it to LGUI/Win key from BASIC tab
3. Change appeared to save in VIA interface
4. After replug, still no events in Key Tester or evtest
5. **Changes not persisting to keyboard firmware**

**Root issue:** VIA web app cannot save changes to keyboard firmware, or keyboard has a firmware lock/bug preventing Super key from functioning.

**Why this works (partially):** Loading the JSON definition in the DESIGN tab tells VIA what the keyboard layout is BEFORE trying to connect. This is the official YUNZII-recommended method. However, saving key remappings back to the keyboard is failing.

---

### ❌ Method 3: Vial Web App (vial.rocks) - FAILED
**Tested:** https://vial.rocks/ in Google Chrome

**Steps attempted:**
1. Opened https://vial.rocks/ in Chrome
2. Clicked **"Start Vial"** button
3. Chrome popup appeared - selected **"SmartCloud YUNZII AL98"**
4. Clicked **"Connect"**
5. Got error: "No devices connected. Connect a Vial-compatible device and press 'Refresh' or select File → Download VIA definitions..."
6. Checked **File** menu - NO "Download VIA definitions" option exists!
7. Only options available: "Load saved layout" and "Save current layout"

**Why it failed:** The vial.rocks **web version does not have the "Sideload VIA JSON" feature** - that feature only exists in the desktop app. The web version is designed for keyboards that already have Vial firmware. Since the AL98 has VIA firmware (not Vial), and there's no way to load VIA definitions in the web version, this method cannot work.

**Key finding:** "Download VIA definitions" / "Sideload VIA JSON" is **desktop-only**, not available in web version.

---

### Key Findings Summary

**Firmware type:** VIA (not Vial)
- Keyboard ships with VIA firmware from factory (confirmed via missing Vial magic number)
- Does NOT require flashing new firmware
- **No Vial firmware exists** for YUNZII AL98
- Cannot use Vial tools - VIA-only keyboard

**WebHID permissions:** Working correctly
- Chrome successfully connects via WebHID
- All 4 keyboard HID devices (hidraw1-4) with correct permissions (`rw-rw-rw-`)
- Not a Linux permissions issue

**udev rules:** Not the issue
- Created correct Vial udev rule in `/etc/udev/rules.d/59-vial.rules`
- Rule looks for Vial magic number that doesn't exist on this keyboard
- udev rules irrelevant since keyboard has VIA firmware, not Vial

**Critical mistake in initial approach:**
- Tried to authorize device BEFORE loading JSON definition
- Must load JSON in DESIGN tab FIRST, then authorize device

**Working method:** VIA Web App (usevia.app) with JSON sideloaded
- Enable Design tab in Settings
- Load JSON definition FIRST
- Then authorize device in Configure tab
- Official YUNZII-recommended approach

---

### Sources
- [VIA JSON Loading - CannonKeys](https://docs.cannonkeys.com/via-json-loading/)
- [VIA Usage Guide - Keebio](https://docs.keeb.io/via)
- [How to Use VIA - Keychron](https://www.keychron.com/blogs/archived/how-to-use-via-to-program-your-keyboard)
- [How to Use VIA - Epomaker](https://epomaker.com/blogs/guides/how-to-use-via-for-beginners)
- [Vial Linux udev Rules](https://get.vial.today/manual/linux-udev.html)
- [QMK with VIA/Vial - tinkerBOY](https://www.tinkerboy.xyz/qmk-firmware-remapping-and-configuring-your-keyboard-with-via-or-vial/)
- [VIA stuck on authorize - GitHub #221](https://github.com/the-via/releases/issues/221)
- [Authorize button does nothing - GitHub #81](https://github.com/the-via/app/issues/81)
- [VIA Definitions Discussion - GitHub #203](https://github.com/vial-kb/vial-gui/discussions/203)
- [YUNZII Software Page](https://www.yunzii.com/pages/software)
- [YUNZII Manual Pages](https://www.yunzii.com/pages/manuals)

---

## Final Solution Summary

### The Firmware Bug
The YUNZII AL98 has a firmware-level block on the **LWin keycode** itself. This is not just the physical Windows key being broken - the firmware prevents ANY key from sending the LWin/Super/GUI keycode. When tested:
- Mapping physical LWin key → LWin = blocked (no events)
- Mapping physical LWin key → C = works (sends KEY_C)
- Mapping Caps Lock → LWin = blocked (no events)
- Mapping Caps Lock → RCtrl = works (sends KEY_RIGHTCTRL)

This appears to be an intentional "gaming mode" feature (prevents accidental Windows key presses during games) that cannot be disabled.

### The Workaround
Since the keyboard firmware blocks LWin but allows other modifiers:
1. **In VIA (usevia.app):** Map Caps Lock → Right Ctrl
2. **In Hyprland config:** Change `$mainMod = SUPER` → `$mainMod = CTRL_R`
3. **Result:** Caps Lock now functions as the mod key for all Hyprland keybinds

### Configuration Files Modified
- **VIA:** Caps Lock remapped to RCtrl (saved in keyboard firmware)
- **Hyprland:** `~/.config/hypr/hyprland.conf` line 244:
  ```
  $mainMod = CTRL_R # Sets Right Ctrl (remapped from Caps Lock on YUNZII AL98) as main modifier
  ```

### Testing Confirmed Working
- `evtest` shows `KEY_RIGHTCTRL` when pressing Caps Lock
- Caps Lock + Return opens Alacritty terminal
- All Hyprland keybinds functional with Caps Lock as modifier

---

## Next Steps (Archived - Issue Resolved)

### 1. Fix Vial Permissions (REQUIRED)

Keys in Vial GUI are not clickable due to permissions. Need to add user to input group:

```bash
sudo usermod -a -G input $USER
```

**Then log out and log back in:**
- Press `Super+M` to exit Hyprland (if Super works from another keyboard)
- Or use Ctrl+Alt+F2 to switch to TTY, login, then `reboot`
- Or just reboot: `reboot` from terminal

After relogin, launch Vial and keys should be clickable.

---

### 2. Remap/Check Super Key in Vial

Once Vial keys are clickable:

1. Launch `Vial`
2. Click the **Win/Super key** (bottom left, next to Ctrl)
3. Check if it shows `KC_LGUI` (correct) or something else
4. If wrong, remap it to `KC_LGUI`
5. Save changes to keyboard

---

### 3. Test Super Key

After remapping in Vial:
- Test in terminal: Run `xev | grep -i super` and press Super key
- Test Hyprland keybind: `Super+Return` should open Alacritty
- Test other keybinds: `Super+B` (Chrome), `Super+R` (Rofi)

---

## Keyboard Hardware Info

- **Model:** YUNZII AL98 QMK/VIA Wireless Mechanical Gaming Keyboard
- **Layout:** 1800 compact (98 keys)
- **Connection modes:** USB-C (wired), Bluetooth 5.0, 2.4GHz wireless
- **Current mode:** Wired (USB-C)
- **Switches:** Factory pre-lubed Milk V2 linear
- **VIA/QMK:** Supported (JSON file loaded)

---

## Files/Paths

- **JSON file:** `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/YUNZII_AL98_QMK_V0100_20250225.json`
- **Vial command:** `Vial`
- **udev rules:** `/etc/udev/rules.d/92-viia.rules`

---

## Resources

- Vial website: https://get.vial.today/
- YUNZII software page: https://www.yunzii.com/pages/software
- YUNZII manuals: https://www.yunzii.com/pages/manuals
