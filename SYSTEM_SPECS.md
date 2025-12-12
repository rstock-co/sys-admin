# System Hardware

| Component | Model | Key Specs |
|-----------|-------|-----------|
| **CPU** | AMD Ryzen 9 7950X | 16-core/32-thread, 5.7GHz boost, Zen 4, AM5 |
| **GPU** | Intel Arc B580 (ASRock Challenger) | 12GB GDDR6, xe driver, DP×3 + HDMI 2.1 |
| **RAM** | Crucial Pro DDR5 | 64GB (2×32GB), 5600MHz |
| **Storage** | Samsung 990 PRO | 4TB NVMe, 7450MB/s |
| **Motherboard** | MSI MAG X870E Tomahawk | AM5, PCIe 5.0, WiFi 7, USB4 |
| **PSU** | Corsair RM750e (2025) | 750W, ATX 3.1, 12V-2×6 |
| **Cooler** | Arctic Liquid Freezer III 360 | 360mm AIO, VRM fan |
| **Case** | NZXT H5 Flow | ATX mid-tower, mesh airflow |
| **Keyboard** | YUNZII AL98 | QMK/VIA, wireless, Milk V2 switches |
| **Speakers** | Creative Pebble Pro | USB-C audio (Arc B580 DP audio workaround) |

## Displays

| Position | Model | Resolution | Refresh | Port | Orientation |
|----------|-------|------------|---------|------|-------------|
| Left | Samsung 32" | 3840×2160 | 60Hz | DP-3 | Portrait |
| Center | TCL 55" TV | 3840×2160 | 120Hz | DP-2 (via DP→HDMI) | Landscape |
| Right | Samsung 32" | 3840×2160 | 60Hz | DP-1 | Portrait |

## Known Hardware Issues

| Issue | Status | Workaround |
|-------|--------|------------|
| Arc B580 HDMI 120Hz | xe driver bug | Use DP→HDMI cable |
| Arc B580 DP audio | xe driver bug | USB speakers |
| Arc B580 PCIe reporting | Cosmetic (ignore) | Actual bandwidth is fine |
| VS Code GPU lag | Electron + Arc conflict | `--disable-gpu` flag |

**Details:** `config/gpu/arc-b580.md`
