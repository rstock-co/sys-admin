# Hardware Specifications

## Primary Workstation (symbiont-tower)

### Core Components

| Component | Model | Key Specs |
|-----------|-------|-----------|
| **CPU** | AMD Ryzen 9 7950X | 16-core/32-thread, 5.7GHz boost, 80MB cache, AM5, 170W TDP |
| **GPU** | ASRock Intel Arc B580 Challenger OC | 12GB GDDR6, PCIe x8 Gen 4, 4× DP 2.1, 1× HDMI 2.1 |
| **Motherboard** | MSI MAG X870E Tomahawk WiFi | PCIe 5.0, DDR5-8400+, USB4, Wi-Fi 7, 2.5Gbps LAN, MS-7E59 |
| **RAM** | Crucial Pro 64GB DDR5-5600 | 2×32GB kit, EXPO/XMP compatible, slots A2+B2 |
| **Storage** | Samsung 990 PRO 4TB NVMe | PCIe Gen4, 7,450 MB/s read, 6,900 MB/s write |
| **Cooler** | Arctic Liquid Freezer III Pro 360 | AIO, 360mm radiator, VRM fan, 6-year warranty |
| **PSU** | Corsair RM750e | 750W, ATX 3.1, PCIe 5.1, 12V-2x6 cable |
| **Case** | NZXT H5 Flow 2024 | Mid-tower, 360mm front + 240mm top radiator support |

### Display Configuration

| Position | Model | Resolution | Refresh | Connection | Orientation |
|----------|-------|------------|---------|------------|-------------|
| Center | TCL 55" QM7K | 3840×2160 | 120Hz | HDMI 2.1 (HDMI-A-3) | Landscape |
| Left | Samsung 32" 4K | 3840×2160 | 60Hz | DisplayPort (DP-2) | Portrait |
| Right | Samsung 32" 4K | 3840×2160 | 60Hz | DisplayPort (DP-3) | Portrait |

### PCIe Topology

```
CPU Root Complex (00:01.1)
  ↓ x8 @ 16.0 GT/s Gen 4
GPU PCIe Switch Bridge 1 (01:00.0) - Intel chip on GPU
  ↓
GPU PCIe Switch Bridge 2 (02:01.0) - Intel chip on GPU
  ↓ x8 @ 16.0 GT/s Gen 4 (when working correctly)
Arc B580 GPU (03:00.0)
Arc B580 Audio (04:00.0)
```

**Note**: Arc B580 uses x8 lanes (not x16). This is by design.

### Thermal Targets

| Component | Idle | Load | Critical |
|-----------|------|------|----------|
| CPU | 35-45°C | 75-85°C | >95°C |
| GPU | 30-40°C | 65-75°C | >90°C |
| NVMe | 35-45°C | 55-65°C | >70°C |

### Power Connections

- 24-pin ATX → Motherboard (right side)
- 8-pin CPU → Motherboard (top-left)
- 8-pin PCIe → GPU
- AIO pump → CPU_FAN header
- AIO fans → SYS_FAN or PUMP_FAN header

### Hardware Verification Commands

```bash
# CPU info
lscpu | grep -E "Model name|^CPU\(s\)|Thread"

# Memory
free -h
sudo dmidecode -t memory | grep -E "Size|Speed|Manufacturer"

# GPU
lspci | grep -i vga
intel_gpu_top

# Storage
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE
sudo hdparm -Tt /dev/nvme0n1

# PCIe link status
cat /sys/bus/pci/devices/0000:03:00.0/current_link_width
cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed

# Temperatures
sensors

# All hardware summary
inxi -Fxz
```

### BIOS Information

- **Model**: MS-7E59 (MAG X870E TOMAHAWK WIFI)
- **Target BIOS**: 2A91 (AGESA PI 1.2.0.3g)
- **BIOS Key**: Delete (press repeatedly during POST)
- **Advanced Mode**: F7
- **Save & Exit**: F10
- **Load Defaults**: F5

### Critical BIOS Settings

| Setting | Location | Value |
|---------|----------|-------|
| Above 4G Decoding | Settings → Advanced → PCI Subsystem | Enabled |
| Re-Size BAR | Settings → Advanced → PCI Subsystem | Enabled |
| PCIe Gen Switch | Settings → Advanced → AMD CBS → NBIO → GFX Config | Gen 4 or Auto |
| XMP/EXPO | OC → Memory | Profile 1 (5600MHz) |
| Boot Mode | Settings → Boot | UEFI |
