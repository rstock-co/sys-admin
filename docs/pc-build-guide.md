# Complete PC Build Guide - Coding Workstation

A workstation optimized for running multiple Claude Code agents, heavy terminal usage, and all-day coding sessions.

---

## The Build at a Glance

| Component | Model | Price (CAD) |
|-----------|-------|-------------|
| CPU | AMD Ryzen 9 7950X | $648.88 |
| Motherboard | MSI MAG X870E Tomahawk WiFi | $377.99 |
| RAM | Crucial Pro 64GB DDR5-5600 | $388.48 |
| GPU | Intel Arc B580 12GB | $355.93 |
| Storage | Samsung 990 PRO 4TB | $398.97 |
| Cooler | Arctic Liquid Freezer III 360 | $204.74 |
| PSU | Corsair RM750e 750W | $127.24 |
| Case | NZXT H5 Flow 2024 | $99.74 |
| Keyboard | YUNZII AL98 QMK/VIA | $142.79 |
| **Total** | | **$2,744.76** |

---

## CPU: AMD Ryzen 9 7950X

### Specs
- 16 cores / 32 threads
- 5.7GHz boost clock
- 80MB cache (L2+L3)
- 170W TDP
- Socket AM5

### Why This CPU?

1. **Multi-threaded beast** - Running 3-5 Claude Code agents + browsers + databases + dev servers simultaneously. More cores = more parallel workloads without slowdown.

2. **AM5 platform longevity** - AMD committed to AM5 through 2027+. Can upgrade CPU later without new motherboard.

3. **DDR5 + PCIe 5.0** - Future-proof memory and storage bandwidth.

4. **Price/performance** - The 7950X hits the sweet spot. The 7950X3D costs $200+ more for gaming cache that doesn't help coding workloads.

### Alternatives Considered

| CPU | Cores | Why Not |
|-----|-------|---------|
| Ryzen 7 7700X | 8C/16T | Half the cores, would bottleneck with many agents |
| Ryzen 9 7900X | 12C/24T | Only $100 less, worth the extra 4 cores |
| Intel i9-14900K | 24C/32T | More power hungry, Intel's hybrid architecture less predictable |

---

## Motherboard: MSI MAG X870E Tomahawk WiFi

### Specs
- Socket AM5
- DDR5-8400+ support
- PCIe 5.0 (x16 GPU + x4 NVMe)
- 4× M.2 slots
- WiFi 7 + Bluetooth 5.4
- 2.5Gb Ethernet
- USB4 ports

### Why This Board?

1. **X870E chipset** - Full PCIe 5.0 support for both GPU and storage. The cheaper B650 boards have PCIe 4.0 only.

2. **USB4** - 40Gbps ports for future devices, docks, or external storage.

3. **4× M.2 slots** - Room for multiple NVMe drives without PCIe cards.

4. **Premium VRMs** - Important for 170W CPU under sustained load. Cheaper boards throttle the 7950X.

5. **WiFi 7** - Future-proof wireless, though I use ethernet.

### Alternatives Considered

| Board | Why Not |
|-------|---------|
| ASUS ROG Crosshair X870E | $200+ more, overkill features |
| MSI MAG B650 Tomahawk | No PCIe 5.0, fewer M.2 slots |
| Gigabyte X870E Aorus | Similar price, MSI BIOS preference |

---

## RAM: Crucial Pro 64GB DDR5-5600

### Specs
- 2× 32GB sticks
- DDR5-5600 MT/s
- CL46 latency
- AMD EXPO certified
- Model: CP2K32G56C46U5

### Why This RAM?

1. **64GB capacity** - Claude Code agents are API-based (low local RAM), but browsers, databases, Docker containers, and dev servers add up. 64GB provides comfortable headroom.

2. **DDR5-5600** - Sweet spot for Ryzen 7000. Higher speeds exist but cost more with minimal real-world benefit.

3. **AMD EXPO** - One-click overclock in BIOS. Just enable EXPO Profile 1.

4. **2× 32GB** - Leaves 2 slots free for future upgrade to 128GB if needed.

5. **Crucial quality** - Micron-manufactured, reliable. Crucial RAM "just works" with AMD.

### Alternatives Considered

| RAM | Why Not |
|-----|---------|
| 32GB kit | Too tight for multi-agent + browser + DB workloads |
| DDR5-6000+ | Diminishing returns, Ryzen's sweet spot is 5600-6000 |
| G.Skill/Corsair | Similar specs, Crucial was cheaper |

---

## GPU: Intel Arc B580 12GB

### Specs
- 12GB GDDR6
- Battlemage architecture (BMG-G21)
- PCIe 4.0 x8
- 3× DisplayPort 2.1 + 1× HDMI 2.1
- 190W TDP

### Why This GPU?

1. **Three 4K displays** - Need a GPU that can drive 3× 4K monitors. The B580 has 4 display outputs, all capable of 4K.

2. **HDMI 2.1** - Required for 4K@120Hz to the TV.

3. **12GB VRAM** - Enough for potential local LLM experimentation (though not primary use case).

4. **Price** - $340 CAD is exceptional for this capability. Comparable NVIDIA cards cost $500+.

5. **Linux support** - Intel's open-source `xe` driver is in the kernel. No proprietary driver hassle like NVIDIA.

### Why Not NVIDIA?

| Concern | Details |
|---------|---------|
| Price | RTX 4060 costs $150+ more for similar display capability |
| Linux drivers | Proprietary drivers, kernel module signing issues, Wayland complications |
| Power | RTX cards draw more power for coding workloads where GPU is mostly idle |

### Known Issues (Arc B580 on Linux)

1. **HDMI 2.1 bugs** - Native HDMI port may not negotiate 120Hz properly. Workaround: Use DisplayPort with DP→HDMI 2.1 adapter cable.

2. **PCIe negotiation** - GPU's internal PCIe switch can get stuck at x1. Requires CMOS reset to fix (see troubleshooting.md).

3. **No DP audio** - DisplayPort audio doesn't work with xe driver. Use USB speakers or HDMI audio.

These issues are annoying but solvable. The price and open-source drivers make it worthwhile.

---

## Storage: Samsung 990 PRO 4TB

### Specs
- 4TB capacity
- PCIe Gen4 NVMe
- 7,450 MB/s read
- 6,900 MB/s write
- With heatsink

### Why This Drive?

1. **4TB capacity** - Projects, Docker images, databases, models, and general accumulation. 2TB fills up fast.

2. **Speed** - Gen4 NVMe is plenty fast. Gen5 drives exist but run hotter and cost more.

3. **Samsung reliability** - 990 PRO is proven. Some cheaper drives have reliability issues.

4. **Heatsink included** - Maintains performance under sustained load, matches motherboard aesthetic.

### Alternatives Considered

| Drive | Why Not |
|-------|---------|
| 2TB drives | Would fill up within a year |
| WD Black SN850X | Similar performance, Samsung preference |
| Gen5 drives | Run hot, expensive, overkill for coding |

---

## Cooler: Arctic Liquid Freezer III Pro 360

### Specs
- 360mm AIO liquid cooler
- 38mm thick radiator
- 3× 120mm P-fans
- VRM cooling fan
- PWM pump
- 6-year warranty

### Why This Cooler?

1. **7950X runs hot** - 170W TDP needs serious cooling. Air coolers struggle under sustained load.

2. **Arctic quality** - Consistently top-rated AIO. Outperforms coolers costing twice as much.

3. **VRM fan** - Unique feature that cools motherboard VRMs. Important for high-power CPU.

4. **6-year warranty** - Confidence in longevity. AIOs have pump failure risk; long warranty matters.

5. **Price** - $195 CAD for a top-tier 360mm AIO is excellent value.

### Alternatives Considered

| Cooler | Why Not |
|--------|---------|
| Noctua NH-D15 | Great air cooler but marginal for 7950X under sustained load |
| NZXT Kraken | More expensive, worse performance |
| Corsair H150i | Similar price, Arctic performs better |

---

## PSU: Corsair RM750e 750W

### Specs
- 750W continuous
- 80+ Gold efficiency
- ATX 3.1 standard
- 12V-2×6 connector (native)
- Fully modular
- 7-year warranty

### Why This PSU?

1. **750W is enough** - 7950X (170W) + B580 (190W) + system = ~450W typical, ~550W peak. 750W provides headroom.

2. **ATX 3.1 / 12V-2×6** - Modern standard with native GPU power connector. No adapters needed.

3. **Corsair RM quality** - Reliable, quiet, proven platform.

4. **Fully modular** - Only connect cables you need. Cleaner build.

5. **7-year warranty** - PSU failures can kill components. Long warranty = confidence.

### Alternatives Considered

| PSU | Why Not |
|-----|---------|
| 650W | Too close to peak draw, no upgrade headroom |
| 850W+ | Unnecessary for this build |
| Cheaper brands | PSU is not where to save money |

---

## Case: NZXT H5 Flow 2024

### Specs
- ATX Mid-Tower
- Tempered glass side panel
- High airflow mesh front
- 360mm front radiator support
- 280mm top radiator support
- Excellent cable management

### Why This Case?

1. **360mm radiator support** - Fits the Arctic Liquid Freezer III in front.

2. **Airflow focused** - Mesh front panel for unrestricted airflow. Not a glass oven.

3. **Compact** - Smaller than full towers but fits everything.

4. **Cable management** - Generous space behind motherboard tray.

5. **Clean aesthetic** - Minimal, professional look. Not "gamer" RGB chaos.

### Alternatives Considered

| Case | Why Not |
|------|---------|
| Fractal Meshify 2 | Larger, similar features |
| Lian Li Lancool III | Bigger than needed |
| NZXT H7 | Larger, more expensive |

---

## Keyboard: YUNZII AL98 QMK/VIA

### Specs
- Full aluminum construction
- QMK/VIA programmable
- Wireless (Bluetooth + 2.4GHz + USB-C)
- Hot-swappable switches
- Gasket mount
- 1800 layout (96%)
- Milk V2 switches (pre-lubed linear)

### Why This Keyboard?

1. **QMK/VIA support** - Fully programmable. Remap any key, create layers, macros.

2. **Caps Lock → F13** - Remapped via VIA to trigger voice dictation on tap, Left Alt on hold.

3. **Wireless options** - Bluetooth for clean desk, 2.4GHz for lower latency, USB-C for charging.

4. **Hot-swap** - Can change switches without soldering.

5. **Build quality** - Full aluminum, gasket mount, premium feel.

6. **1800 layout** - Has numpad but more compact than full-size.

---

## Thermal Performance

| Component | Idle | Load | Max Safe |
|-----------|------|------|----------|
| CPU | 35-45°C | 75-85°C | 95°C |
| GPU | 30-40°C | 65-75°C | 90°C |
| NVMe | 35-45°C | 55-65°C | 70°C |

Monitor with: `sensors` command

---

## Power Consumption

| State | Wattage |
|-------|---------|
| Idle (displays on) | ~120W |
| Coding (light load) | ~180W |
| Compiling / Heavy | ~350W |
| Maximum draw | ~550W |

The 750W PSU has plenty of headroom.

---

## Build Tips

### RAM Installation
- Use slots **A2 + B2** (2nd and 4th from CPU)
- This is required for dual-channel on MSI boards

### Cooler Orientation
- Mount radiator in **front** (intake)
- Tubes at **bottom** for pump longevity
- VRM fan points toward motherboard VRMs

### Cable Management
- Route 24-pin and CPU 8-pin behind motherboard
- Use case's built-in cable channels
- Only connect modular cables you need

### BIOS Settings
After first boot, configure:
1. Enable **XMP/EXPO Profile 1** (RAM speed)
2. Enable **Above 4G Decoding** (GPU)
3. Enable **Re-Size BAR** (GPU performance)
4. Set boot order (NVMe first)

---

## Linux Compatibility

Everything works on Arch Linux / Hyprland:

| Component | Driver | Status |
|-----------|--------|--------|
| CPU | In-kernel | Perfect |
| GPU | xe (in-kernel) | Works (minor HDMI bugs) |
| WiFi | iwlwifi | Perfect |
| Bluetooth | btusb | Perfect |
| NVMe | nvme | Perfect |
| Audio | PipeWire | Perfect |

No proprietary drivers needed. Everything is open-source and in the kernel.

---

## Summary

This build prioritizes:

1. **Multi-threaded performance** - 16 cores for parallel workloads
2. **Memory headroom** - 64GB for browsers, DBs, containers
3. **Display flexibility** - GPU with 4 outputs for multi-monitor
4. **Linux compatibility** - All open-source drivers
5. **Reliability** - Quality components with long warranties
6. **Value** - High performance without overspending

Total cost: **$2,744.76 CAD** for a workstation that handles anything you throw at it.

Add the display setup (~$1,400) and you have a complete coding environment for ~$4,200 CAD.
