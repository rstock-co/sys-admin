# Audio Configuration - TCL 55" TV Default Output

**Last Updated:** 2025-11-30
**Audio Stack:** PipeWire + WirePlumber

---

## Current Setup

### Default Audio Output
**Device:** TCL 55" TV ("Beyond TV")
**Connection:** HDMI 2 from Intel Arc B580 GPU
**Technical Name:** `alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1`
**Audio Card Profile:** `output:hdmi-stereo-extra1`

---

## Audio Devices Detected

### Intel Arc B580 GPU (HDA Intel PCH) - Card 1
**PCI Address:** 0000:04:00.0
**Available HDMI Outputs:**
1. **HDMI 1** (`hdmi-output-0`) - Available
2. **HDMI 2** (`hdmi-output-1`) - ✅ **TCL 55" TV ("Beyond TV")** ← DEFAULT
3. **HDMI 3** (`hdmi-output-2`) - Samsung LS32D70xE monitor
4. **HDMI 4** (`hdmi-output-3`) - Not connected

### USB Audio Device
**Outputs:**
- S/PDIF Output
- Speakers
- Front Headphones

**Inputs:**
- Line Input
- Microphone

### AMD Radeon Audio (Ryzen 9 7950X iGPU) - Card 49
**Status:** Disabled (no displays connected)

---

## Persistent Configuration Files

### 1. Default Sink Configuration
**File:** `~/.config/pipewire/pipewire-pulse.conf.d/10-default-sink.conf`
```conf
# Set TCL 55" TV (Beyond TV) as default audio output
# This is HDMI 2 from Intel Arc B580 GPU

context.exec = [
    { path = "pactl" args = "set-default-sink alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1" }
]
```

**Purpose:** Sets TV as default audio output on PipeWire startup

### 2. Audio Card Profile Configuration
**File:** `~/.config/wireplumber/main.lua.d/50-alsa-card-profile.lua`
```lua
-- Set Intel Arc B580 audio card to use HDMI 2 profile (TCL TV)

table.insert(alsa_monitor.rules, {
  matches = {
    {
      { "device.name", "equals", "alsa_card.pci-0000_04_00.0" },
    },
  },
  apply_properties = {
    ["device.profile"] = "output:hdmi-stereo-extra1",
  },
})
```

**Purpose:** Ensures HDMI 2 profile is always active (makes TV output available)

---

## Quick Commands

### Check Current Default Output
```bash
pactl info | grep "Default Sink"
# Should show: alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1
```

### Check Current Volume
```bash
wpctl get-volume @DEFAULT_AUDIO_SINK@
```

### Set Volume
```bash
# Increase by 5%
wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+

# Decrease by 5%
wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-

# Set to specific level (e.g., 50%)
wpctl set-volume @DEFAULT_AUDIO_SINK@ 0.5
```

### Toggle Mute
```bash
wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
```

### List All Audio Devices
```bash
wpctl status
```

### List All Available Sinks
```bash
pactl list sinks short
```

### Switch to Different Output Manually
```bash
# List available outputs
pactl list sinks short

# Set default (example: USB speakers)
pactl set-default-sink alsa_output.usb-Generic_USB_Audio-00.HiFi__Speaker__sink
```

---

## Hyprland Volume Keybinds

**Configured in:** `~/.config/hypr/hyprland.conf`

```conf
# Volume controls
bind = SUPER, equal, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+
bind = SUPER, minus, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
bind = SUPER, 0, exec, wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle

# Media keys (if keyboard has them)
bindl = , XF86AudioRaiseVolume, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+
bindl = , XF86AudioLowerVolume, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
bindl = , XF86AudioMute, exec, wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
```

**Usage:**
- `Super + =` - Volume up 5%
- `Super + -` - Volume down 5%
- `Super + 0` - Toggle mute

---

## Troubleshooting

### No Sound from TV

1. **Check if TV is default:**
   ```bash
   pactl info | grep "Default Sink"
   ```
   Should show: `alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1`

2. **Check volume level:**
   ```bash
   wpctl get-volume @DEFAULT_AUDIO_SINK@
   ```
   If muted, unmute with:
   ```bash
   wpctl set-mute @DEFAULT_AUDIO_SINK@ 0
   ```

3. **Check audio card profile:**
   ```bash
   pactl list cards | grep -A 150 "alsa_card.pci-0000_04_00.0" | grep "Active Profile"
   ```
   Should show: `output:hdmi-stereo-extra1`

4. **Manually set TV as default:**
   ```bash
   pactl set-default-sink alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1
   ```

5. **Move current application to TV:**
   ```bash
   # Get application sink input ID
   pactl list sink-inputs short

   # Move it to TV (replace <ID> with actual number)
   pactl move-sink-input <ID> alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1
   ```

### Sound Going to Wrong Display

If audio is coming from a Samsung monitor instead of TV:

```bash
# Check which profile is active
pactl list cards | grep -A 150 "alsa_card.pci-0000_04_00.0" | grep "Active Profile"

# Switch to TV profile (HDMI 2)
pactl set-card-profile alsa_card.pci-0000_04_00.0 output:hdmi-stereo-extra1

# Set as default
pactl set-default-sink alsa_output.pci-0000_04_00.0.hdmi-stereo-extra1
```

### Configuration Not Persisting After Reboot

1. **Check config files exist:**
   ```bash
   ls -la ~/.config/pipewire/pipewire-pulse.conf.d/10-default-sink.conf
   ls -la ~/.config/wireplumber/main.lua.d/50-alsa-card-profile.lua
   ```

2. **Restart PipeWire and WirePlumber:**
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

3. **Check logs for errors:**
   ```bash
   journalctl --user -u pipewire -n 50
   journalctl --user -u wireplumber -n 50
   ```

---

## Technical Details

### Why HDMI 2 for DisplayPort TV?

Your TCL 55" TV is physically connected via **DisplayPort to HDMI cable** (from GPU's DP-2 port to TV's HDMI port).

The GPU's audio hardware presents this as **HDMI 2** because:
- The DisplayPort carries audio using HDMI audio protocol
- Arc B580's audio controller maps DP outputs to HDMI profiles
- The TV identifies itself as "Beyond TV" via EDID

### Audio Path
```
Application (Spotify)
    ↓
PipeWire (audio server)
    ↓
WirePlumber (session manager)
    ↓
ALSA (kernel driver)
    ↓
Intel Arc B580 GPU Audio (HDA Intel PCH)
    ↓
DisplayPort 2 (carrying HDMI audio)
    ↓
DP-to-HDMI cable
    ↓
TCL 55" TV ("Beyond TV")
```

---

## References

- PipeWire Documentation: https://docs.pipewire.org/
- WirePlumber Configuration: https://pipewire.pages.freedesktop.org/wireplumber/
- Arch Wiki: https://wiki.archlinux.org/title/PipeWire

---

**System Setup:** See `/home/neo/agents/sys-admin/SYSTEM_SETUP.md` for audio stack details
