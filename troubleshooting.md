# Troubleshooting Guide

## Intel Arc B580 PCIe x1 Fix

### Problem
GPU stuck at PCIe x1 Gen 1.0 instead of x8 Gen 4.0, causing:
- 128× bandwidth reduction (250 MB/s vs 32 GB/s)
- Display stuck at 60Hz
- GPU initialization failures

### Diagnosis

```bash
# Check link width (should be 8, not 1)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width

# Check link speed (should be 16.0 GT/s, not 2.5 GT/s)
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed

# Check parent bridge
cat /sys/bus/pci/devices/0000:02:01.0/current_link_speed

# Full PCIe topology
lspci -tv
```

### Root Cause
Arc B580's internal PCIe switch chip (device 02:01.0) retains negotiation state. The Clear CMOS button alone is insufficient—complete power loss required.

### Fix Procedure

**Step 1: BIOS Update** (if available)
```bash
# Check current version
cat /sys/class/dmi/id/bios_version

# Target: 2A91 or newer (AGESA PI 1.2.0.3g)
# Download from: https://www.msi.com/Motherboard/MAG-X870E-TOMAHAWK-WIFI/support
```

**Step 2: Complete CMOS Reset** (CRITICAL)
1. Shut down PC completely
2. Flip PSU switch to OFF
3. Unplug power cable
4. Remove CMOS battery (CR2032)
   - MSI X870E: Battery behind chipset heatsink (may need to remove heatsink)
5. Press power button 10× (discharge capacitors)
6. **Wait 30-60 minutes** (NOT 30 seconds!)
7. Reinstall battery (+ side up)
8. Reconnect power

**Step 3: BIOS Configuration**
1. Boot, press Delete → BIOS
2. Press F7 for Advanced Mode
3. Configure:
   - Settings → Advanced → PCI Subsystem:
     - Above 4G Decoding: **Enabled**
     - Re-Size BAR Support: **Enabled**
   - Settings → Advanced → AMD CBS → NBIO → GFX Configuration:
     - PCIe Gen Switch: **Gen 4** or **Auto**
4. OC → Memory → Enable EXPO/XMP Profile 1
5. F10 to save and exit

**Step 4: Verify**
```bash
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width  # Should be 8
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed  # Should be 16.0 GT/s
```

### If Still Broken
- Try second CMOS reset with 5-minute battery removal
- Reseat GPU in PCIe slot
- Try different PCIe x16 slot (diagnostic)
- Contact Intel/ASRock for RMA

---

## TCL 55" 120Hz Not Working

### Problem
TV stuck at 60Hz despite advertising 120Hz in EDID.

### Prerequisites
**Fix PCIe x1 issue first!** 120Hz requires proper GPU bandwidth.

### Diagnosis

```bash
# Check available modes
hyprctl monitors | grep availableModes

# Check EDID
cat /sys/class/drm/card0/card0-HDMI-A-3/edid > ~/tcl-edid.bin
edid-decode ~/tcl-edid.bin | grep -i 120
```

### Fix: Kernel Parameter

Edit `/boot/loader/entries/arch.conf`:
```
options root=/dev/nvme0n1p2 rw video=HDMI-A-3:3840x2160@120
```

Reboot and verify:
```bash
hyprctl monitors | grep "3840x2160@120"
```

### Alternative Fixes
1. Try `video=HDMI-A-3:3840x2160@120e` (e = enable)
2. Check TV settings for "HDMI 2.1" or "Enhanced HDMI" mode
3. Use DisplayPort + active DP→HDMI 2.1 adapter

---

## Common Issues Quick Reference

### Boot Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| No boot device | BIOS boot order | Set NVMe as Boot Option #1 |
| Stuck at BIOS | Boot mode | Ensure UEFI (not Legacy/CSM) |
| Black screen after GRUB | GPU drivers | Boot with `nomodeset`, install `mesa` |

### Hardware Detection

| Symptom | Check | Solution |
|---------|-------|----------|
| GPU not detected | `lspci \| grep VGA` | Reseat GPU, check power cables |
| Only 32GB RAM | `free -h` | Reseat RAM in slots A2+B2 |
| WiFi disabled | `nmcli device` | `nmcli radio wifi on` |
| No audio | `pactl info` | Install `pipewire pipewire-pulse` |

### Display Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| Monitor not detected | `hyprctl monitors` | Check cables, `hyprctl reload` |
| Wrong resolution | `wlr-randr` | Edit hyprland.conf monitor line |
| Flickering | PCIe link | Fix PCIe x1 issue |
| XWayland blurry | App settings | Set `force_zero_scaling = true` |

### Performance Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| High CPU temp >90°C | `sensors` | Check AIO pump on CPU_FAN header |
| Slow storage | `hdparm -Tt` | Set I/O scheduler to `none` |
| System lag | `htop` | Check for runaway processes |

### Service Issues

```bash
# PostgreSQL
sudo systemctl status postgresql
sudo journalctl -u postgresql -n 50
# Fix: sudo -u postgres initdb -D /var/lib/postgres/data

# Docker
sudo systemctl status docker
# Fix: sudo systemctl enable --now docker

# NetworkManager
sudo systemctl status NetworkManager
nmtui  # GUI configuration
```

---

## MSI X870E BIOS Update

### Current Info
- Model: MS-7E59
- Check version: `cat /sys/class/dmi/id/bios_version`
- Support page: https://www.msi.com/Motherboard/MAG-X870E-TOMAHAWK-WIFI/support

### Method 1: M-Flash (Recommended)

1. Download BIOS to FAT32 USB (file in root directory)
2. Boot to BIOS (Delete key)
3. Navigate to M-Flash
4. Select USB → Select BIOS file
5. Confirm update (3-8 minutes)
6. System auto-reboots

### Method 2: Flash BIOS Button

1. Rename BIOS file to `MSI.ROM` exactly
2. Copy to FAT32 USB root
3. Shut down, PSU off, unplug
4. Insert USB in BIOS Flashback port (check manual)
5. Turn PSU on (don't press power button)
6. Press/hold Flash BIOS button 3-5 seconds
7. LED blinks = flashing (5-10 minutes)
8. LED stops = complete
9. Remove USB, power on

### Post-Update Checklist
- [ ] Load Optimized Defaults (F5)
- [ ] Enable XMP/EXPO
- [ ] Enable Above 4G Decoding
- [ ] Enable Re-Size BAR
- [ ] Set PCIe Gen to Auto/Gen 4
- [ ] Set boot order

---

## CMOS Reset Procedures

### Method 1: Battery Removal (Most Effective)

1. PSU off, unplug power cable
2. Locate CR2032 battery (X870E: behind chipset heatsink)
3. Remove battery
4. Press power button 10×
5. Wait 30-60 minutes
6. Reinstall battery (+ up)
7. Reconfigure BIOS

### Method 2: Clear CMOS Button (Less Effective)

1. PSU off, unplug power
2. Press/hold rear I/O Clear CMOS button 10 seconds
3. Wait 2-4 hours (for Arc B580 issues)
4. Reconnect power, boot to BIOS

### Method 3: JBAT1 Jumper

1. PSU off, unplug
2. Locate JBAT1 pins near battery
3. Short pins with screwdriver 10 seconds
4. Boot to BIOS

### What Gets Reset
- All BIOS settings to defaults
- Boot order
- XMP/EXPO memory profiles
- Fan curves
- PCIe negotiation state

---

## Diagnostic Commands Cheatsheet

```bash
# System overview
inxi -Fxz

# Hardware
lspci -v                    # All PCI devices
lsusb                       # USB devices
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE

# CPU
lscpu
sensors
cat /proc/cpuinfo | grep MHz

# Memory
free -h
sudo dmidecode -t memory

# GPU
lspci | grep -i vga
intel_gpu_top
vulkaninfo | grep deviceName

# Storage
df -h
sudo hdparm -Tt /dev/nvme0n1
sudo smartctl -a /dev/nvme0n1

# Network
ip addr
nmcli device status
ping -c 3 archlinux.org

# Display
hyprctl monitors
wlr-randr
xrandr  # XWayland only

# Services
systemctl --failed
journalctl -b 0 -p err

# Logs
journalctl -b 0 | grep -i error
dmesg | grep -i error
```
