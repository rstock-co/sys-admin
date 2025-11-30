# 55" TV as Computer Monitor - Required Specifications

**Use case:** Terminal work, i3 window manager, tmux (16 panes in 4×4 grid), 8+ hours daily

---

## Must-Have Specifications (Deal Breakers)

### Resolution
- **Required:** 3840×2160 (4K UHD) native
- **Why:** Anything less = pixelated text at 55"
- **Verify:** Check specs say "native 4K" not "4K upscaling"

### Chroma Subpixel Layout
- **Best:** RGB (standard LCD/LED)
- **Acceptable:** WRGB (LG OLED)
- **Avoid:** RGBW (budget panels with shared white subpixel)
- **Avoid:** Pentile (some Samsung OLED)
- **Why:** RGB gives sharpest text rendering
- **How to check:** Search "[model] subpixel layout rtings" or check rtings.com reviews

### Input Lag (in Game/PC Mode)
- **Excellent:** <15ms
- **Good:** 15-20ms
- **Avoid:** >20ms
- **Why:** Affects i3 workspace switching responsiveness
- **Where to find:** rtings.com "Input Lag" section (look for "1080p @ 60Hz" or "4K @ 60Hz" with Game Mode)

### Refresh Rate
- **Required:** 120Hz native panel
- **Avoid:** "Motion rate 240" or "effective 120Hz" (fake specs)
- **Why:** Smoother scrolling, snappier workspace transitions
- **Verify:** Specs say "native 120Hz" or "120Hz panel"

### PC/Game Mode
- **Required:** Must have "PC Mode" or "Game Mode" setting
- **Why:** Disables image processing, enables 1:1 pixel mapping, reduces input lag
- **Verify:** Check manual or reviews mention this mode

### HDMI 2.1
- **Required:** At least one HDMI 2.1 port
- **Why:** Needed for 4K @ 120Hz
- **Verify:** Specs explicitly say "HDMI 2.1" (not just "HDMI")

---

## Important Specifications (Significantly Affects Experience)

### Panel Type
- **Best for terminals:** VA panel (good contrast, no burn-in risk)
- **Good:** IPS panel (excellent viewing angles, no burn-in)
- **Avoid for 8+ hr use:** OLED (burn-in risk from static tmux status bars/borders)
- **Why:** Static terminal content causes OLED burn-in over time

### Brightness (SDR)
- **Adequate:** 300-400 nits
- **Good:** 400-600 nits
- **Excellent:** 600+ nits
- **Why:** Handles ambient light, prevents eye strain
- **Verify:** rtings.com "SDR Peak Brightness" measurement
- **Note:** OLED typically only 150-200 nits sustained (too dim for bright rooms)

### Anti-Glare Coating
- **Best:** Semi-gloss (balance of sharpness and glare control)
- **Good:** Matte (reduces reflections, slightly softer text)
- **Acceptable:** Glossy (sharper text, more reflections)
- **Where to find:** rtings.com "Reflection Handling" section

### Response Time
- **Great:** <5ms
- **Good:** 5-10ms
- **Avoid:** >10ms (causes ghosting on scrolling)
- **Where to find:** rtings.com "Response Time" section

---

## Nice-to-Have (Not Deal Breakers)

### Local Dimming (if LED/LCD, not OLED)
- **Good:** 100+ zones
- **Better:** FALD (Full Array Local Dimming)
- **Best:** Mini-LED (1000+ zones)
- **Why:** Better contrast, less backlight bleed

### VRR Support
- **Look for:** FreeSync or G-Sync Compatible
- **Why:** Smoother scrolling (minor benefit for terminals)

### Multiple HDMI 2.1 Ports
- **Nice:** 2+ HDMI 2.1 ports
- **Why:** Convenience (not critical, you need 1 for TV + GPU has other outputs for 27" monitors)

---

## Red Flags (Avoid These Models)

❌ **"4K upscaling"** instead of native 4K
❌ **RGBW subpixel layout** (terrible text rendering)
❌ **>25ms input lag** (feels sluggish)
❌ **60Hz only** (not smooth enough)
❌ **No PC/Game Mode** (will have processing lag)
❌ **Edge-lit LED backlight** (uneven brightness, backlight bleed)
❌ **OLED for 8+ hour terminal use** (burn-in risk too high)

---

## Recommended Models (as of 2024)

### Top Pick: Sony X90L 55" (~$1100-1300 CAD)
- ✅ Native 4K, VA panel, RGB subpixel
- ✅ 120Hz native, ~9ms input lag
- ✅ 600+ nits brightness
- ✅ Full array local dimming (96 zones)
- ✅ Excellent anti-glare coating
- ✅ HDMI 2.1
- ✅ Safe for long-term terminal use (no burn-in)

### Budget Alternative: TCL 6-Series R655 55" (~$800-1000 CAD)
- ✅ Mini-LED VA panel
- ✅ 120Hz, <15ms input lag
- ✅ 1000+ nits brightness
- ⚠️ Less refined processing (but you disable in PC mode anyway)

### Premium (If You Must): Samsung QN90D 55" (~$1400-1600 CAD)
- ✅ Mini-LED, excellent brightness (1500+ nits)
- ✅ 120Hz, <10ms input lag
- ⚠️ More expensive, diminishing returns

---

## How to Research a Model

1. **Find model on rtings.com** (best TV review site)
2. **Check these sections:**
   - "Input Lag" (look for <15ms in Game Mode)
   - "Response Time" (look for <10ms)
   - "SDR Peak Brightness" (look for 400+ nits)
   - "Reflection Handling" (check anti-glare quality)
   - "Subpixel Layout" (RGB is best)
3. **Verify specs:**
   - Native 4K (3840×2160)
   - Native 120Hz panel
   - HDMI 2.1
   - PC/Game Mode available
4. **Search Reddit:** "[model name] as monitor" or "[model name] text rendering"

---

## Setup Requirements

### Desk/Mounting
- **Desk depth needed:** 36-48" minimum for 55" TV
- **VESA mount recommended:** TV stands are huge, use desk mount arm or wall mount
- **Viewing distance:** 3-4 feet optimal

### Connection
- **Cable:** HDMI 2.1 or DisplayPort 1.4 (your GPU supports both)
- **Setup:** Enable "PC Mode" or "Game Mode" in TV settings immediately

### Configuration
1. Connect TV to GPU
2. Boot into i3
3. Use `xrandr` to set resolution: `xrandr --output HDMI-1 --mode 3840x2160 --rate 120`
4. Enable PC/Game Mode in TV settings menu
5. Disable all motion smoothing, noise reduction, etc.
6. Set picture mode to "PC" or "Game"

---

## 4×4 Grid Layout

**55" TV (3840×2160) split into 4×4 grid:**
- Each pane: 11.56" wide × 6.94" tall
- Each pane: 960×540 pixels
- Matches your current 4×27" setup almost exactly

**tmux configuration for 4×4:**
```bash
# Split into 4×4 grid
tmux split-window -h
tmux split-window -h
tmux split-window -h
tmux select-pane -t 0
tmux split-window -v
tmux split-window -v
tmux split-window -v
# Repeat for remaining columns...
```

---

## Budget Summary

| Option | Price (CAD) | Quality | Risk |
|--------|-------------|---------|------|
| **Sony X90L 55"** | $1100-1300 | Excellent | Low |
| **TCL R655 55"** | $800-1000 | Good | Medium |
| **Samsung QN90D** | $1400-1600 | Premium | Low |
| **LG C3 OLED** | $1200-1500 | Best image | **High burn-in risk** |
| **Odyssey Ark** | $2599 | Gaming-focused | Low |

**Recommended:** Sony X90L 55" at ~$1200 CAD (best balance of price, performance, safety for terminal use)

---

**Last updated:** 2024-11-18
