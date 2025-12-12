# Keyboard Configuration (YUNZII AL98)

## Quick Fixes

**Win key not working:**
```bash
# Check if locked (lights up white)
# Press Fn + Win to toggle lock
```

**Factory reset (clears all issues):**
```
Long press Fn + Spacebar (backlight flashes white 3x)
```

---

## Current Setup

| Setting | Value |
|---------|-------|
| **Model** | YUNZII AL98 QMK/VIA |
| **Connection** | 2.4GHz wireless (daily), USB-C (for VIA) |
| **Switches** | Milk V2 linear |
| **USB ID** | `28e9:3174` |

### Custom Remaps (VIA)

| Key | Remap | Purpose |
|-----|-------|---------|
| Caps Lock | `MT(MOD_LALT,KC_F13)` | Tap=F13 (dictation), Hold=Left Alt |

**Backup:** `~/agents/sys-admin/keyboard/yunzii-al98-custom-layout.json`

---

## System Paths

| Path | Purpose |
|------|---------|
| `/etc/udev/rules.d/50-yunzii-al98.rules` | USB permissions for VIA |
| `~/.config/hypr/hyprland.conf` | Keybinds (line 244: `$mainMod = SUPER`) |
| `~/Downloads/YUNZII_AL98_QMK_V0100_20250225/*.json` | Keyboard definition for VIA |
| `~/agents/sys-admin/keyboard/yunzii-al98-custom-layout.json` | Custom keybind backup |

---

## VIA Configuration

**Only works in wired mode:**
1. Set physical switch to "Wired"
2. Unplug 2.4GHz dongle
3. Connect USB-C only

**Connect to VIA:**
1. Open https://usevia.app/ in Chrome
2. Settings → Enable "Show Design tab"
3. DESIGN tab → Load keyboard JSON
4. CONFIGURE tab → "Authorize device +"
5. Select "SmartCloud YUNZII AL98"

**Backup keybinds (IMPORTANT):**
Factory reset erases custom keybinds!
1. SAVE+LOAD tab → "Save current layout"
2. Store in `~/agents/sys-admin/keyboard/`

**Restore after reset:**
1. Connect to VIA (load definition JSON first)
2. SAVE+LOAD tab → "Load saved layout"
3. Select backup file

---

## Critical Shortcuts

| Shortcut | Action |
|----------|--------|
| `Fn + Win` | Lock/unlock Win key |
| `Fn + A` | Windows mode |
| `Fn + S` | macOS mode |
| `Fn + Spacebar` (long) | Factory reset |
| `Fn + Right Ctrl` | Battery level |
| `Fn + Backspace` | Backlight on/off |

---

## Troubleshooting

### Win Key Not Working

1. Check if locked (lights white) → `Fn + Win`
2. Ensure Windows mode → `Fn + A`
3. Factory reset → Long `Fn + Spacebar`

### VIA Won't Connect

1. Switch to wired mode
2. Unplug 2.4GHz dongle
3. Check permissions:
```bash
ls -la /dev/hidraw*  # Should be crw-rw-rw-
```
4. If wrong permissions:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### Red Breathing LED (Cloud Logo)

**Low battery warning.** Factory reset clears it.

Battery indicators:
- Red flashing = Below 10%
- Red solid = Charging
- Green (5 sec) = Fully charged

### Lighting Issues

Don't use VIA for lighting - use Fn combos:
- `Fn + \` = Change effect
- `Fn + Enter` = Change color
- `Fn + ↑/↓` = Brightness
- `Fn + →/←` = Speed

---

## Historical Reference

### Super key issue (Nov 2025)

**Problem:** Win key not working
**Root cause:** Win key was locked (`Fn + Win`)
**Solution:** Factory reset + `Fn + Win` to unlock

### VIA connection issue (Nov 2025)

**Problem:** "Failed to open device" error
**Root causes:**
- Wrong permissions on /dev/hidraw*
- Both USB-C and 2.4GHz connected simultaneously

**Solution:**
1. Wired mode only
2. udev rule for permissions:
```bash
echo 'KERNEL=="hidraw*", ATTRS{idVendor}=="28e9", ATTRS{idProduct}=="3174", MODE="0666", TAG+="uaccess"' | sudo tee /etc/udev/rules.d/50-yunzii-al98.rules
```

### Ctrl+V conflict (Nov 2025)

**Problem:** Ctrl+V triggered togglefloating
**Root cause:** Hyprland `$mainMod` was set to `CTRL_R`
**Solution:** Reverted to `$mainMod = SUPER`
