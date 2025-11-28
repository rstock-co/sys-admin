# YUNZII AL98 Keyboard Troubleshooting

**Date:** 2025-11-28
**Status:** In progress - Super key not working

---

## Current Issue

Super key (Windows key) on YUNZII AL98 keyboard is not functioning in Hyprland. Cannot trigger keybinds like `Super+Return` (open terminal).

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

---

## Software Installed

- **vial-appimage** (AUR) - v0.7.5
- **udev rules created:** `/etc/udev/rules.d/92-viia.rules`
- **udev rules reloaded:** `sudo udevadm control --reload-rules && sudo udevadm trigger`

---

## Next Steps

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
