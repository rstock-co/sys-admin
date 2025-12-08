# Creative Pebble Pro Speaker Setup

**Date:** December 8, 2025
**Status:** [RESOLVED] Working via USB audio

## Hardware

- **Speakers:** Creative Pebble Pro
- **Connection:** USB-C only (provides both power AND audio via built-in DAC)

## Speaker Ports (Right Speaker)

| Port | Purpose |
|------|---------|
| AUX (3.5mm) | Audio input from PC |
| USB-C | Power input (10W) |
| USB-C PD (red circle) | Optional 30W power with USB-PD brick |

Left speaker has no ports — connects to right speaker via fixed cable.

## Problem Found

Motherboard audio chip (AMD Family 17h/19h HD Audio at `7c:00.6`) was on kernel denylist:

```
snd_hda_intel 0000:7c:00.6: Skipping the device on the denylist
```

Only GPU HDMI audio and USB audio were available — no analog 3.5mm output.

## Fix Applied

```bash
# Created modprobe config to enable all HDA devices
echo 'options snd_hda_intel enable=1,1,1' | sudo tee /etc/modprobe.d/audio.conf

# Rebuilt initramfs
sudo mkinitcpio -P

# Reboot required
sudo reboot
```

## Working Configuration

**Sink ID:** 87 (Creative Pebble Pro Analog Stereo)

```bash
# Set as default
wpctl set-default 87

# Adjust volume
wpctl set-volume 87 0.7
```

## Notes

- **USB-C provides both power and audio** - no 3.5mm jack needed
- Motherboard audio (ALC4082 at `7c:00.6`) is kernel-denylisted and cannot be enabled without kernel recompilation
- USB audio uses the speaker's built-in DAC which works great
- Speaker has Bluetooth 5.3 but USB is preferred (lower latency, no compression)
- **Blue flashing light** = Bluetooth pairing mode (hold BT button to exit)
- **Purple/solid light** = USB/AUX mode (correct for USB audio)
