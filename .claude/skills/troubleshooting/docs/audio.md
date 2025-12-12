# Audio Troubleshooting

## Quick Fix (Try This First)

```bash
systemctl --user restart pipewire wireplumber
```

---

## Current Setup

| Component | Details |
|-----------|---------|
| **Speakers** | Creative Pebble Pro (USB-C powered) |
| **Connection** | USB-C to motherboard |
| **Audio Stack** | PipeWire + WirePlumber |

The Creative Pebble Pro speakers connect via USB-C and work out of the box with PipeWire. No special configuration needed.

---

## Common Issues

### No Sound

1. Check speakers are powered on (LED should be lit)
2. Check volume: `wpctl get-volume @DEFAULT_AUDIO_SINK@`
3. Check not muted: `wpctl status | grep -A5 Sinks`
4. Restart audio: `systemctl --user restart pipewire wireplumber`

### Wrong Output Device

```bash
# List sinks
wpctl status

# Set default (find ID from status output)
wpctl set-default <sink-id>
```

### Volume Controls

```bash
# Get current volume
wpctl get-volume @DEFAULT_AUDIO_SINK@

# Set volume (0.0 to 1.0)
wpctl set-volume @DEFAULT_AUDIO_SINK@ 0.5

# Mute/unmute
wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
```

---

## Diagnostic Commands

```bash
# Full audio status
wpctl status

# List all sinks with details
pactl list sinks short

# Check PipeWire is running
systemctl --user status pipewire wireplumber

# View audio logs
journalctl --user -u pipewire --since "5 min ago"
```

---

## Known Issue: Intel Arc B580 + DisplayPort Audio

HDMI audio via DisplayPort-to-HDMI does NOT work with Intel Arc B580 due to xe driver bug. The kernel driver fails to convert DisplayPort EDID to ELD for the audio codec.

**This is why we use USB speakers instead of TV audio.**

If you need TV audio in the future, options:
- Wait for kernel fix (xe driver)
- Use native HDMI port (sacrifices 120Hz)
- Use Bluetooth speaker as workaround
