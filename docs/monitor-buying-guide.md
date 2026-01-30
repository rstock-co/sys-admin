# Monitor Setup for Coding: Complete Buying Guide

A 3-monitor setup optimized for terminal work, Claude Code, and long coding sessions.

---

## The Setup

```
┌──────────────┐  ┌────────────────────────────┐  ┌──────────────┐
│   Samsung    │  │                            │  │   Samsung    │
│   32" 4K     │  │      TCL 55" QM7K          │  │   32" 4K     │
│  Portrait    │  │       Landscape            │  │  Portrait    │
│   60Hz       │  │        120Hz               │  │   60Hz       │
│              │  │                            │  │              │
│  Reference   │  │      Main Workspace        │  │   Browser    │
│  Code/Docs   │  │    Claude Code / Editor    │  │   Research   │
└──────────────┘  └────────────────────────────┘  └──────────────┘
```

**Total resolution:** 10,080 × 3,840 pixels across all three displays.

---

## Center Display: TCL 55" QM7K

### Why a TV Instead of a Monitor?

1. **Size for the price** - A 55" 4K display costs $800-1200. An equivalent computer monitor (if it exists) would be $2000+.
2. **120Hz at 4K** - Most large monitors cap at 60Hz. TVs routinely support 120Hz.
3. **Text clarity** - Modern TVs with "PC Mode" disable image processing and give 1:1 pixel mapping.

### Model Details

| Spec | Value |
|------|-------|
| **Model** | TCL 55Q750G (QM7K series) |
| **Size** | 55" diagonal (1210mm × 680mm) |
| **Resolution** | 3840 × 2160 (4K UHD) |
| **Refresh Rate** | 120Hz native |
| **Panel Type** | VA with Mini-LED backlight |
| **HDR** | HDR10+, Dolby Vision |
| **Input Lag** | ~10ms in Game Mode |
| **Ports** | 4× HDMI 2.1 (all support 4K@120Hz) |
| **VRR** | Yes (AMD FreeSync Premium) |

### Why the QM7K Specifically?

1. **Mini-LED backlight** - Hundreds of dimming zones for excellent contrast without OLED burn-in risk
2. **VA panel** - Deep blacks, good for dark terminal themes, no burn-in from static UI elements
3. **True 120Hz** - Not "Motion Rate 240" marketing BS, actual 120Hz panel
4. **Low input lag** - Under 15ms in Game Mode, feels responsive for typing
5. **Full HDMI 2.1** - All 4 ports support 4K@120Hz (many TVs only have 1-2 HDMI 2.1 ports)
6. **Price** - $750.75 CAD at Costco (Black Friday 2025), regularly ~$900-1000

### Critical Settings for Coding

After connecting, configure these settings on the TV:

1. **Picture Mode** → Game or PC (lowest input lag)
2. **HDMI Mode** → Enhanced/HDMI 2.1 (required for 120Hz)
3. **Motion Smoothing** → OFF (causes input lag)
4. **Noise Reduction** → OFF
5. **Sharpness** → 0 or very low (artificial sharpening hurts text)
6. **Color Temperature** → Warm or Custom (easier on eyes)

### Alternatives Considered

| Model | Pros | Cons | Price (CAD) |
|-------|------|------|-------------|
| **TCL QM7K** (chosen) | Mini-LED, 120Hz, low lag | Generic brand | ~$900 |
| Sony X90L | Excellent processing | More expensive | ~$1300 |
| Samsung QN85B | Great brightness | Samsung tax | ~$1400 |
| LG C3 OLED | Perfect blacks | **Burn-in risk** | ~$1500 |

**Why not OLED?** For 8+ hours of terminal use with static elements (status bars, tmux borders, editor gutters), OLED burn-in is a real risk. VA/Mini-LED has zero burn-in concern.

---

## Side Displays: Samsung ViewFinity S7 32" 4K

### Model Details

| Spec | Value |
|------|-------|
| **Model** | Samsung S32D700EAU (LS32D70xE) |
| **Size** | 32" diagonal (700mm × 400mm) |
| **Resolution** | 3840 × 2160 (4K UHD) |
| **Refresh Rate** | 60Hz |
| **Panel Type** | IPS |
| **Response Time** | 5ms GTG |
| **Ports** | HDMI 2.0, DisplayPort 1.2, USB-C (65W PD) |
| **Stand** | Height/tilt/swivel/pivot adjustable |

### Why These Monitors?

1. **True 4K at 32"** - Perfect pixel density for code (137 PPI)
2. **IPS panel** - Wide viewing angles essential for portrait orientation
3. **Pivot stand included** - Rotates to portrait without buying a separate arm
4. **USB-C with 65W** - Can power a laptop while displaying
5. **Matte coating** - Reduces reflections in bright rooms

### Portrait Orientation for Code

At 32" 4K in portrait:
- **Width:** 2160 pixels (plenty for 120-150 character lines)
- **Height:** 3840 pixels (100+ lines of code visible)
- **Perfect for:** Reference code, documentation, logs, terminal output

### Price

- **Regular price:** ~$450-550 CAD each
- **Black Friday 2025 price:** $292.74 each ($585.48 for pair) from Best Buy

Watch for Black Friday deals - these monitors drop nearly 50%.

---

## Complete Shopping List

### Actual Purchase (Black Friday 2025)

| Item | Model | Retailer | Price | GST | Total |
|------|-------|----------|-------|-----|-------|
| Center TV | TCL QM7K 55" | Costco | $750.75 | $37.54 | $788.29 |
| Side Monitors (×2) | Samsung 32" 4K White | Best Buy | $585.48 | $29.28 | $614.76 |
| **Displays Total** | | | **$1,336.23** | | **$1,403.05** |

That's **$293/monitor** and **$751 for the TV** - exceptional value for 3× 4K displays.

### Accessories

| Item | Model | Price + GST |
|------|-------|-------------|
| Monitor Mounts (×2) | HUANUO Single Mount, White | $102.88 |
| DP→HDMI 2.1 Cable | UGREEN 6ft braided | $25.50 |
| DisplayPort 1.4 (×2) | IVANKY 6ft + 10ft | $35.68 |
| **Accessories Total** | | **$164.06** |

### Grand Total: ~$1,567 CAD (displays + accessories)

### Where to Buy (Canada)

- **TCL QM7K**: Best Buy, Costco, Amazon.ca
- **Samsung S32D700**: Memory Express, Canada Computers, Amazon.ca

---

## Connection Requirements

### GPU Requirements

Your GPU needs:
- 3× display outputs (DP or HDMI)
- HDMI 2.1 for TV at 120Hz (or use DP→HDMI 2.1 adapter)
- Enough bandwidth for 3× 4K displays

**Recommended GPUs:**
- Intel Arc A770/B580 (3× DP 2.1 + HDMI 2.1)
- NVIDIA RTX 4060+ (3× DP 1.4a + HDMI 2.1)
- AMD RX 7600+ (3× DP 2.1 + HDMI 2.1)

### Cables Needed

| Connection | Cable | Notes |
|------------|-------|-------|
| TV | HDMI 2.1 Ultra High Speed | Must be certified for 4K@120Hz |
| Left Monitor | DisplayPort 1.4 | Standard DP cable works |
| Right Monitor | DisplayPort 1.4 | Standard DP cable works |

**Important:** For 4K@120Hz, you MUST use a certified HDMI 2.1 cable. Older HDMI cables max out at 4K@60Hz.

---

## Linux/Hyprland Configuration

### Monitor Layout

```conf
# ~/.config/hypr/hyprland.conf

# Center: TCL 55" @ 120Hz (main workspace)
monitor=DP-2,3840x2160@120,2160x0,1

# Left: Samsung 32" portrait @ 60Hz
monitor=DP-3,3840x2160@60,0x0,1,transform,1

# Right: Samsung 32" portrait @ 60Hz
monitor=DP-1,3840x2160@60,6000x0,1,transform,3
```

**Note:** `transform,1` = 90° clockwise (left monitor), `transform,3` = 90° counter-clockwise (right monitor).

### Workspace Assignment

```conf
# Main workspaces on TV
workspace=1,monitor:DP-2,default:true
workspace=2,monitor:DP-2

# Reference on left portrait
workspace=3,monitor:DP-3,default:true

# Browser on right portrait
workspace=4,monitor:DP-1,default:true
```

---

## Ergonomics

### Viewing Distance

| Display | Recommended Distance |
|---------|---------------------|
| 55" TV | 3-4 feet (90-120cm) |
| 32" Monitors | 2-3 feet (60-90cm) |

### Desk Requirements

- **Depth:** Minimum 30" (75cm), ideally 36"+ (90cm+) for comfortable TV viewing distance
- **Width:** 6+ feet (180cm+) to accommodate the full setup

### Mounting Options

- **TV:** Wall mount or deep desk with stock stand
- **Monitors:** Stock stands work (they pivot to portrait), or use monitor arms for cleaner look

---

## Summary

This setup gives you:

- **12.4 million pixels** of screen real estate
- **Zero burn-in risk** (VA + IPS panels)
- **120Hz center display** for smooth scrolling
- **Portrait side panels** optimized for code
- **~$1,400 CAD** for 3× 4K displays (Black Friday pricing)
- **~$1,567 CAD** including mounts and cables

It's the best balance of size, quality, and value for serious coding work.
