# Audio Configuration

## Quick Fix

```bash
systemctl --user restart pipewire wireplumber
```

---

## Current Setup

| Component | Details |
|-----------|---------|
| **Speakers** | Creative Pebble Pro |
| **Connection** | USB-C (power + audio via built-in DAC) |
| **Audio Stack** | PipeWire + WirePlumber |

Works out of the box with PipeWire. No special configuration needed.

---

## System Paths

| Path | Purpose |
|------|---------|
| PipeWire configs | `~/.config/pipewire/` (if customized) |
| WirePlumber configs | `~/.config/wireplumber/` (if customized) |
| System audio | `/etc/modprobe.d/audio.conf` |

**Current default sink:**
```bash
wpctl status | grep -A5 "Sinks:"
```

---

## Troubleshooting

### No Sound

1. Check speakers powered on (LED lit)
2. Check volume: `wpctl get-volume @DEFAULT_AUDIO_SINK@`
3. Check not muted: `wpctl status | grep -A5 Sinks`
4. Restart: `systemctl --user restart pipewire wireplumber`

### Wrong Output Device

```bash
# List sinks
wpctl status

# Set default (find ID from status)
wpctl set-default <sink-id>
```

### Volume Controls

```bash
# Get volume
wpctl get-volume @DEFAULT_AUDIO_SINK@

# Set volume (0.0 to 1.0)
wpctl set-volume @DEFAULT_AUDIO_SINK@ 0.5

# Mute toggle
wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
```

---

## Diagnostic Commands

```bash
# Full audio status
wpctl status

# List sinks
pactl list sinks short

# Check services
systemctl --user status pipewire wireplumber

# View logs
journalctl --user -u pipewire --since "5 min ago"
```

---

## Speaker Hardware Notes

### Creative Pebble Pro Ports (Right Speaker)

| Port | Purpose |
|------|---------|
| AUX (3.5mm) | Audio input |
| USB-C | Power (10W) + audio |
| USB-C PD (red) | Optional 30W power |

Left speaker has no ports — connects via fixed cable.

### LED Indicators

- **Blue flashing** = Bluetooth pairing mode (hold BT button to exit)
- **Purple/solid** = USB/AUX mode (correct for USB audio)

---

## Known Issues

### Arc B580 DisplayPort Audio Bug

HDMI audio via DP-to-HDMI doesn't work - xe driver bug fails to convert EDID to ELD.

**This is why we use USB speakers instead of TV audio.**

Future options if needed:
- Wait for kernel fix
- Use native HDMI (sacrifices 120Hz)
- Bluetooth speaker workaround

### Motherboard Audio Denylisted

AMD HD Audio (`7c:00.6`) is kernel-denylisted:
```
snd_hda_intel 0000:7c:00.6: Skipping the device on the denylist
```

Not an issue - USB audio works great via speaker's built-in DAC.
