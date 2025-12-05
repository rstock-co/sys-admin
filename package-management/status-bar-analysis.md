## 🔍 Hyprland Status Bar Comparison (December 2025)

### Summary Table

| Bar | GitHub Stars | AUR Votes | Config Language | Last Release | Best For |
|-----|-------------|-----------|-----------------|--------------|----------|
| [**Eww**](https://github.com/elkowar/eww) | **10.6k** ⭐ | 38 | Yuck (Lisp-like) + SCSS | Active (2025) | Ultimate customization, works on X11 too |
| [**Waybar**](https://github.com/Alexays/Waybar) | **~10k** ⭐ | Official repo | JSON/YAML + CSS | 0.14.0 | Stability, easy setup, massive theme ecosystem |
| [**AGS/Astal**](https://github.com/Aylur/ags) | **2.8k** ⭐ | 16 | TypeScript/JavaScript | v3.1.0 (Nov 2025) | Programmers, full widget framework |
| [**HyprPanel**](https://github.com/Jas-SinghFSU/HyprPanel) | **2.1k** ⭐ | 12 | TypeScript (built on AGS) | Active | Hyprland-specific, batteries included |
| [**Ironbar**](https://github.com/JakeStanger/ironbar) | **789** ⭐ | - | TOML/YAML/JSON + CSS | Alpha | Rust enthusiasts, GTK4 |

---

### Detailed Analysis

#### 🥇 **Eww** - Most Stars, Maximum Flexibility
- **Stars:** 10.6k (highest)
- **Language:** Rust + GTK
- **Config:** Yuck (Lisp-like DSL) + SCSS
- **Pros:**
  - WM-independent (works on Hyprland, Sway, i3, bspwm, etc.)
  - Ultimate widget flexibility - build anything
  - Active development (Feb 2025 commits)
  - Largest community due to cross-WM support
- **Cons:**
  - Steeper learning curve (Lisp syntax)
  - Relies on external scripts for data
  - More setup required for Wayland

#### 🥈 **Waybar** - Most Popular for Hyprland/Sway
- **Stars:** ~10k
- **Package:** `extra/waybar` (official Arch repo - not even AUR!)
- **Config:** JSON + CSS
- **Pros:**
  - **Official repo** = most stable, best tested
  - Easiest setup - works out of the box
  - Huge theme ecosystem (waybar-themes on GitHub)
  - Native Hyprland support
  - Most documentation and tutorials
- **Cons:**
  - Less flexible than Eww/AGS for complex widgets
  - JSON config can get verbose

#### 🥉 **AGS (Aylur's GTK Shell)** - Developer's Choice
- **Stars:** 2.8k (growing fast)
- **Latest:** v3.1.0 (Nov 27, 2025) - actively maintained
- **Config:** TypeScript/JavaScript + JSX
- **Pros:**
  - Full programming language = unlimited flexibility
  - Built-in modules for Network, Bluetooth, Audio, etc.
  - Modern React-like development experience
  - Powers HyprPanel
- **Cons:**
  - Requires JS/TS knowledge
  - More complex initial setup

#### **HyprPanel** - Hyprland-Native, Batteries Included
- **Stars:** 2.1k
- **Built on:** AGS/Astal
- **Pros:**
  - **Hyprland-specific** features and integration
  - Pre-built with sensible defaults
  - Context menus for Volume, Network, Bluetooth
  - GUI customization options
- **Cons:**
  - Hyprland-only (not portable)
  - Dependent on AGS ecosystem

---

### 📊 My Recommendation

**For your use case** (ricing, extensibility, feature-rich, well-supported):

| Priority | Recommendation |
|----------|----------------|
| **Easiest Start** | **Waybar** - Official repo, instant gratification, massive theme library |
| **Maximum Ricing** | **Eww** - Highest stars, ultimate widget freedom, Lisp is learnable |
| **If You Code** | **AGS** - TypeScript = familiar, modern framework, very powerful |
| **Hyprland-Only** | **HyprPanel** - Pre-built AGS config, Hyprland-native features |

### My Take

**Waybar** is the safest choice - it's in the official Arch repo (not even AUR), has the most themes ready to go, and "just works" with Hyprland. You can achieve 90% of what you'd want without touching code.

**Eww** has the most stars because it works everywhere, but the Lisp-like config has a learning curve.

**AGS/HyprPanel** is the future - TypeScript-based, modern architecture, but smaller community for now.

---

### Quick Install Commands

```bash
# Waybar (recommended - official repo)
sudo pacman -S waybar

# Eww (most stars)
paru -S eww

# AGS (programmer's choice)
paru -S aylurs-gtk-shell

# HyprPanel (Hyprland-specific, built on AGS)
paru -S ags-hyprpanel-git
```

Which direction are you leaning?

---

**Sources:**
- [Waybar GitHub](https://github.com/Alexays/Waybar)
- [Eww GitHub](https://github.com/elkowar/eww)
- [AGS GitHub](https://github.com/Aylur/ags)
- [HyprPanel GitHub](https://github.com/Jas-SinghFSU/HyprPanel)
- [Ironbar GitHub](https://github.com/JakeStanger/ironbar)
- [Hyprland Wiki - Status Bars](https://wiki.hypr.land/Useful-Utilities/Status-Bars/)
- [awesome-hyprland](https://github.com/hyprland-community/awesome-hyprland)
