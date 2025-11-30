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

**Confirmed: Intel xe kernel driver bug, not cable issue**
- UGREEN cable is high-quality and works correctly (passes video EDID)
- Research confirms: xe driver fails to convert DisplayPort EDID→ELD for audio codec
- Known Linux kernel bug affecting Arc B580 + DisplayPort outputs
- Native HDMI works because GPU firmware handles EDID→ELD directly
- DisplayPort requires kernel driver conversion, which xe driver doesn't implement properly

**Research Sources:**
- [Arch Linux: xe driver audio regression kernel 6.17.8](https://bbs.archlinux.org/viewtopic.php?pid=2273908)
- [Unix StackExchange: EDID-to-ELD conversion failure](https://unix.stackexchange.com/questions/391326/how-to-force-hdmi-audio-intel-card-to-be-enabled-despite-receiving-broken-edid)
- [Intel Community: Arc B580 audio failures](https://community.intel.com/t5/Intel-ARC-Graphics/New-B580-graphics-card-and-now-no-audio-through-DP-or-HDMI/td-p/1680276)

**Implemented Solution:**
1. ✅ **JBL Flip 6 Bluetooth speaker** - Paired successfully, audio working (minor glitching) - TEMPORARY WORKAROUND
2. **PipeWire config tuning** - Created `~/.config/pipewire/pipewire.conf.d/99-bluetooth.conf` with increased buffer size (quantum 2048) to reduce Bluetooth glitches
3. ✅ **Creative Pebble Pro USB speakers** - Ordered Nov 30, 2025 from Best Buy Canada (refurbished, $30 CAD) - PERMANENT SOLUTION

**Creative Pebble Pro Specs:**
- Model: 51MF1710AA001
- Power: 10W RMS (20W peak), upgradeable to 30W RMS with USB-PD brick
- Connectivity: USB-C powered, Bluetooth 5.3, 3.5mm AUX input
- Features: Re-engineered 2.25" drivers, 3.5x better bass than V3, RGB lighting, BassFlex technology
- Condition: Refurbished - Like New
- Price: $30 CAD (50% off $60 new price)
- Source: Best Buy Canada Black Friday 2025

**Alternative Solutions (not pursued):**
- **USB DAC** ($30-50) - 3.5mm output to TV AUX, zero latency, no glitching - NOT VIABLE (TCL QM7 3.5mm jack is output-only)
- **Revert to native HDMI** - Trade 120Hz for working audio - Rejected, keeping 120Hz
- **Wait for kernel update** - xe driver DP audio may be fixed in future kernel releases - Too uncertain

**Tested and rejected:**
- ✗ Bluetooth to TV - TV only supports remote/accessories, not audio input
- ✗ Different DP-to-HDMI cable - Not a cable issue, confirmed kernel driver bug
- ✗ Firmware update - Already on latest (20251111-1), issue is in kernel driver code
