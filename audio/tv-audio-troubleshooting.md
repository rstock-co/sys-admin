# TV Audio Troubleshooting & Configuration

**Last Updated:** November 30, 2025

---

## Issue: No Sound from TV Speakers

### Problem Summary
Audio was not playing through TCL 55" TV (Beyond TV) internal speakers despite correct PipeWire/WirePlumber configuration showing audio was being sent to the TV.

### Root Cause
WirePlumber configuration file was set to wrong HDMI output profile:
- Config was set to: `output:hdmi-stereo-extra2` (HDMI 3)
- TV is actually on: `output:hdmi-stereo-extra1` (HDMI 2)

This happened because the TV was moved from one DisplayPort connection to another, changing its HDMI output mapping.

---

## Audio Configuration

### Physical Setup
- **TV:** TCL 55" (Beyond TV)
- **Connection:** DisplayPort-to-HDMI cable
- **GPU Port:** DP-2
- **System Device:** `alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1`
- **Audio Hardware:** Intel Arc B580 GPU HDMI audio (HDA Intel PCH)

### HDMI Output Mapping
- **hdmi-output-0** (HDMI 1): Samsung monitor on DP-1
- **hdmi-output-1** (HDMI 2): Beyond TV on DP-2 ← **DEFAULT AUDIO**
- **hdmi-output-2** (HDMI 3): Samsung monitor on DP-3

---

## The Fix

### WirePlumber Config File
**File:** `~/.config/wireplumber/wireplumber.conf.d/51-tv-audio.conf`

**Changed from:**
```conf
device.profile = "output:hdmi-stereo-extra2"
```

**Changed to:**
```conf
device.profile = "output:hdmi-stereo-extra1"
```

**Full corrected config:**
```conf
monitor.alsa.rules = [
  {
    matches = [
      {
        # Match the Intel HDA card (Arc GPU audio)
        device.name = "alsa_card.pci-0000_04_00.0"
      }
    ]
    actions = {
      update-props = {
        # Set HDMI 2 profile (Beyond TV on DP-2)
        api.alsa.use-acp = true
        device.profile = "output:hdmi-stereo-extra1"
      }
    }
  }
]
```

### Cleanup Actions
Moved old deprecated WirePlumber Lua configs:
```bash
mv ~/.config/wireplumber/main.lua.d ~/.config/wireplumber/main.lua.d.backup
```

These files were generating warnings because WirePlumber 0.5 doesn't support `.lua` configs anymore:
- `51-default-sink-tv.lua`
- `51-default-audio.lua`

---

## Verification Commands

### Check Active Profile
```bash
pactl list cards | grep "Active Profile"
```
Should show: `Active Profile: output:hdmi-stereo-extra1`

### Check Default Sink
```bash
wpctl status | grep -A 5 "Sinks:"
```
Should show `*` next to `HDA Intel PCH Digital Stereo (HDMI 2)`

### Check What's Playing Where
```bash
pactl list sink-inputs
```
Shows which applications are sending audio and to which sink.

---

## Restart Audio Services

After config changes:
```bash
systemctl --user restart wireplumber.service pipewire-pulse.service
```

If audio still not working, **reboot** to fully reinitialize HDMI audio drivers.

---

## TV Settings Checklist

**VERIFIED (Nov 30, 2025):**
1. ✅ **Audio Output:** Internal Speaker
2. ✅ **Digital Audio Out:** PCM
3. ✅ **Volume:** Turned up (confirmed)
4. ✅ **Mute:** Off (confirmed)

---

## DisplayPort-to-HDMI Cable Notes

The TV uses a DP-to-HDMI cable instead of native HDMI because the Intel Arc B580's native HDMI port had 120Hz issues.

**Audio considerations:**
- DP-to-HDMI cables must support audio passthrough
- Cheap cables sometimes don't pass audio correctly
- Audio flows: Linux → PipeWire → GPU DP audio → Cable → HDMI → TV
- Some TVs need audio input setting adjusted for DP-converted signals

---

## Next Steps After Reboot

1. **Test audio immediately** - Play Spotify or YouTube
2. **If still no sound:**
   - Check TV remote/settings for audio output
   - Try different DP-to-HDMI cable
   - Test with JBL PartyBox to verify Linux audio works
   - Check kernel logs: `sudo dmesg | grep -i "hdmi\|audio"`
3. **If working:**
   - Commit the config change to dotfiles repo
   - Update SYSTEM_SETUP.md with audio section

---

## Status

**Current State:** HDMI audio not working - Intel Arc xe driver + DP-to-HDMI incompatibility.

**Root Cause (Nov 30, 2025 - Deep Investigation):**
Intel Arc B580 xe driver not populating audio ELD when using DisplayPort outputs:
```bash
cat /proc/asound/card1/eld#* shows:
monitor_present 0  (GPU doesn't detect monitor)
eld_valid 0        (No valid EDID audio data)
```

**Timeline:**
- ✅ Audio worked with native HDMI-to-HDMI cable (Nov 29)
- ❌ Audio broke when switched to DisplayPort-to-HDMI cable (for 120Hz fix)

**Technical Analysis:**
- **Cable:** UGREEN 8K@60Hz Active DP1.4 to HDMI2.1, supports Dolby 7.1 (high quality)
- **Video EDID:** Working correctly (GPU sees display, video works fine)
- **Audio EDID:** GPU receives it (`/sys/class/drm/card0-DP-2/edid` shows CEA-861 audio blocks)
- **Problem:** xe driver not passing audio EDID to HDA codec to populate ELD
- **GPU Layout:** Graphics at `0000:03:00.0`, Audio at `0000:04:00.0` (separate devices)
- **Codec State:** All audio pins disabled (`Pin-ctls: 0x00`, `Devices: 0`, `Connection: 0`)

**Not the cable's fault** - Cable passes video EDID fine, supports audio. Issue is xe driver not bridging graphics→audio subsystems for DisplayPort outputs.

**Solutions:**
1. **Bluetooth speaker workaround** - User's chosen solution (bypasses GPU audio)
2. **Revert to native HDMI** - Trade 120Hz for working audio
3. **Wait for kernel xe driver update** - DisplayPort audio support may be incomplete in current xe driver
4. **Try linux-firmware-git** - Unlikely to help, but bleeding-edge firmware worth trying

**Tested and rejected:**
- ✗ Bluetooth to TV - TV only supports remote/accessories, not audio input
- ✗ Different DP-to-HDMI cable - Not a cable quality issue, driver issue
- ✗ Firmware update - Already on latest (20251111-1), issue is in kernel driver
