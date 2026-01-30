# Quick Reference Card

## Hardware Summary

| Component | Spec |
|-----------|------|
| CPU | Ryzen 9 7950X (16c/32t, 5.7GHz) |
| GPU | Intel Arc B580 12GB (PCIe x8 Gen4) |
| RAM | 64GB DDR5-5600 (2×32GB) |
| Storage | Samsung 990 PRO 4TB NVMe |
| Displays | 55" 4K@120Hz + 2× 32" 4K@60Hz portrait |

## Critical BIOS Settings (MSI X870E)

| Setting | Value | Location |
|---------|-------|----------|
| Above 4G Decoding | Enabled | Settings → Advanced → PCI Subsystem |
| Re-Size BAR | Enabled | Settings → Advanced → PCI Subsystem |
| PCIe Gen Switch | Gen 4/Auto | AMD CBS → NBIO → GFX Config |
| XMP/EXPO | Profile 1 | OC → Memory |

## Common Commands

### System Info
```bash
inxi -Fxz                    # Full system summary
sensors                      # Temperatures
free -h                      # Memory usage
df -h                        # Disk usage
```

### GPU & Display
```bash
intel_gpu_top                # GPU monitor
hyprctl monitors             # Display info
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width  # PCIe width
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed  # PCIe speed
```

### Package Management
```bash
sudo pacman -Syu             # Update system
sudo pacman -S <pkg>         # Install
sudo pacman -Rs <pkg>        # Remove with deps
paru -S <pkg>                # AUR install
paru -Syu                    # Update all (including AUR)
```

### Services
```bash
systemctl status <service>
systemctl enable --now <service>
systemctl restart <service>
journalctl -u <service> -f   # Follow logs
```

### Hyprland
```bash
hyprctl reload               # Reload config
hyprctl monitors             # List monitors
hyprctl clients              # List windows
hyprctl keyword monitor ...  # Set monitor at runtime
```

## Key File Locations

| Purpose | Path |
|---------|------|
| Boot params | `/boot/loader/entries/arch.conf` |
| Hyprland config | `~/.config/hypr/hyprland.conf` |
| Waybar config | `~/.config/waybar/config` |
| Shell config | `~/.zshrc` |
| Chrome flags | `~/.config/chromium-flags.conf` |
| Electron flags | `~/.config/electron-flags.conf` |

## Troubleshooting Flowchart

### PCIe x1 Issue
```
PCIe width = 1?
  ↓ Yes
BIOS update available?
  ↓ Yes → Update BIOS
  ↓ No
CMOS Reset (battery out 30-60 min)
  ↓
Configure BIOS (Above 4G, ReBAR, Gen 4)
  ↓
Still x1? → Reseat GPU → Still x1? → RMA
```

### No 120Hz
```
PCIe fixed (width=8, speed=16 GT/s)?
  ↓ No → Fix PCIe first
  ↓ Yes
Add kernel param: video=HDMI-A-3:3840x2160@120
  ↓
Reboot → Check hyprctl monitors
  ↓
Still 60Hz? → Check TV "Enhanced HDMI" setting
```

### Service Won't Start
```
systemctl status <service>
  ↓ Failed
journalctl -u <service> -n 50
  ↓ Check error message
Common fixes:
  - PostgreSQL: initdb -D /var/lib/postgres/data
  - Docker: usermod -aG docker $USER
  - Network: nmtui
```

## Emergency Recovery

### Boot from USB
1. Create Arch USB: `dd if=archlinux.iso of=/dev/sdX bs=4M status=progress`
2. Boot from USB
3. Mount: `mount /dev/nvme0n1p2 /mnt && mount /dev/nvme0n1p1 /mnt/boot`
4. Chroot: `arch-chroot /mnt`
5. Fix issue, exit, reboot

### Reset Display Config
```bash
# From TTY (Ctrl+Alt+F2)
rm ~/.config/hypr/hyprland.conf
# Reboot - Hyprland creates default config
```

### Network Recovery
```bash
# If NetworkManager fails
sudo systemctl start NetworkManager
nmtui
# Or manual
sudo ip link set enp6s0 up
sudo dhcpcd enp6s0
```

## Performance Targets

| Metric | Expected |
|--------|----------|
| CPU idle temp | 35-45°C |
| CPU load temp | 75-85°C |
| PCIe link | x8 @ 16.0 GT/s |
| NVMe read | ~7,000 MB/s |
| RAM speed | 5600 MHz |

## Monitor Layout (Hyprland coordinates)

```
┌──────────┐ ┌──────────────────┐ ┌──────────┐
│   DP-2   │ │       DP-1       │ │   DP-3   │
│ Portrait │ │    Landscape     │ │ Portrait │
│ 2160×3840│ │   3840×2160      │ │ 2160×3840│
│  @60Hz   │ │     @120Hz       │ │   @60Hz  │
│ (0,0)    │ │   (2160,0)       │ │ (6000,0) │
└──────────┘ └──────────────────┘ └──────────┘
```

## Keyboard Shortcuts (Hyprland)

| Key | Action |
|-----|--------|
| Super + Q | Terminal |
| Super + C | Close window |
| Super + R | App launcher (wofi) |
| Super + V | Toggle floating |
| Super + 1-6 | Switch workspace |
| Super + Shift + 1-6 | Move to workspace |
| Super + Arrow | Move focus |
| Super + Mouse drag | Move/resize window |
