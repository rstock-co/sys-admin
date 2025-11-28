# Hyprland System Setup Guide
**Last Updated:** November 28, 2025
**Purpose:** Personal reference for system configuration, packages, and decisions

---

## Core System

### Operating System
- **Arch Linux** on kernel `6.17.9-arch1-1`
- Package manager: `pacman` + `paru` (AUR helper)

### Window Manager
- **Hyprland** `0.52.1-5` - Wayland compositor
- Config: `~/.config/hypr/hyprland.conf`

---

## Display Setup

### Monitors
Triple 4K monitor configuration:
- **Left:** Samsung 32" (DP-1) - Portrait mode, 90° rotation, 3840x2160@60Hz
- **Center:** TV 55" (HDMI-A-3) - Landscape, 3840x2160@120Hz (VRR disabled), vertically centered
- **Right:** Samsung 32" (DP-2) - Portrait mode, 270° rotation, 3840x2160@60Hz

### Visual Style
- **Gaps:** Inner 5px, Outer 20px
- **Borders:** 2px, animated rotating gradient (see script below)
- **Rounding:** 10px with power 2
- **Transparency:** 0.85 opacity for VS Code, Chrome, Spotify
- **Animations:** Enabled with custom bezier curves (easeOutQuint, almostLinear, etc.)

#### Border Animation Script
Custom workaround for animated border gradients using a bash script (`~/.config/hypr/rotate-border.sh`). Hyprland doesn't natively support animated gradients, so this script continuously rotates the gradient angle every 50ms using `hyprctl`. The script runs in the background and updates the border color gradient (hot pink, purple, deep purple, royal purple, orange-red) with a rotating angle from 0-360 degrees. Auto-initialized via `exec-once` in Hyprland config on startup.

---

## Applications

### Terminal
- **Alacritty** - GPU-accelerated terminal emulator
- **Why chosen over Kitty:** Running many parallel Claude Code sessions requires minimal memory usage. Alacritty is lighter and more performant for multi-instance scenarios.
- Bound to: `Super + Return`

### Shell
- **Zsh** with **Starship** prompt
- **Modular configuration:** `~/.zshrc` sources all files from `~/zshrc/` directory
  - `core.sh` - PATH, environment variables, shell history
  - `nav.sh` - File listing and navigation aliases
  - `dotfiles.sh` - Bare git repository alias
  - `pkg.sh` - Package manager aliases (pnpm, bun, npm)
  - `agents.sh` - Agent shortcuts and PostgreSQL management
  - `hyprland.sh` - Hyprland control shortcuts
  - `internet.sh` - Chrome bookmarks/history browsing with fzf
  - `alias-management.sh` - Edit, source, and view aliases
- **eza** - Modern `ls` replacement with icons, colors, and git integration (replaces unmaintained exa)

### Browser
- **Google Chrome** (stable) - Switched from Chromium
- **Why:** Chromium (open-source) doesn't have Google API keys, can't sync bookmarks/extensions without manual API setup. Chrome has everything built-in.
- **Removed:** Chromium, all configs cleaned

### App Launcher
- **Rofi** `2.0.0-1` (rofi-wayland)
- **Why:** Most popular (15.3k GitHub stars), best for ricing, official Wayland support as of 2025
- **Alternatives considered:** Fuzzel, Tofi, Wofi, Anyrun
- Bound to: `Super + R`

#### Rofi Themes
- **Package:** `rofi-themes-collection-git` (AUR - newmanls/rofi-themes-collection)
- **Why:** Proven working with Rofi 2.0 + Hyprland (May 2025 YouTube video), simpler than adi1090x
- **Rejected:** adi1090x/rofi (outdated, built for Rofi 1.7.4, 3+ years old, compatibility issues)
- **Location:** `/usr/share/rofi/themes/`

### Code Editor
- **VS Code** (`code` package for OSS version)

### File Manager
- **Dolphin** - NOT currently installed (keybind `Super + E` configured but won't work until installed)

### Music
- **Spotify** via `spotify-launcher` and `spicetify-cli` (AUR) for customization

---

## System Monitors & Management

### Resource Monitoring
- **btop** - Resource monitor

### Bluetooth
- **bluez** `5.85-1` - Bluetooth protocol stack
- **bluez-utils** `5.85-1` - Bluetooth utilities
- **bluetui** - TUI for managing Bluetooth connections

---

## Audio & Video

### Audio Stack
- **PipeWire** `1.4.9-1` - Modern audio/video server
- **WirePlumber** `0.5.12-1` - Session manager for PipeWire
- **pipewire-pulse** - PulseAudio replacement
- **pipewire-alsa** - ALSA compatibility
- **pipewire-jack** - JACK compatibility
- **Why:** Modern replacement for PulseAudio, better performance, lower latency, handles both audio and video

### Video/Camera
- **v4l-utils** `1.32.0-1` - Video4Linux utilities
- **Why:** Standard Linux webcam/camera support, required for Chrome video calls/screen sharing, works with PipeWire
- **Note:** V4L2 is the kernel API, PipeWire sits on top for multi-app support and security

### Volume Controls
- **Tool:** `wpctl` (WirePlumber control)
- **Keybinds:**
  - `Super + =` - Volume up 5%
  - `Super + -` - Volume down 5%
  - `Super + 0` - Mute toggle
  - Media keys (XF86Audio*) - Configured for keyboards with dedicated media keys

---

## Desktop Integration

### Portals
- **xdg-desktop-portal-hyprland** - Hyprland-specific portal
- **xdg-desktop-portal-gtk** - GTK portal for Chrome file dialogs
- **Why GTK portal:** Chrome depends on GTK3, needs it for file picker dialogs

---

## Fonts

### Nerd Fonts Collection
Installed 67 Nerd Font packages (otf-* and ttf-*) for terminal icons and glyphs.
- Kept all fonts (decided against cleanup for maximum compatibility)
- Common ones: JetBrains Mono, FiraCode, Meslo, Hack, Iosevka

---

## Removed Packages & Why

### gnome-keyring
- **Removed:** November 28, 2025
- **Why:** Not needed - using 1Password for password management, not using Chromium's built-in password manager
- **Cleaned:** Hyprland autostart, Chromium flags, all data directories

### Chromium
- **Removed:** November 28, 2025
- **Replaced with:** Google Chrome
- **Why:** Can't sync Google account without manual API key setup, Chrome has it built-in
- **Cleaned:** Config dir, cache, desktop file, Hyprland window rules

### polkit-gnome
- **Removed:** November 28, 2025
- **Why:** "Legacy" package, not configured in Hyprland (wasn't running), not needed

### paru-debug
- **Removed:** November 28, 2025
- **Why:** Debug symbols for paru, only needed for development

---

## Development Tools

### Languages & Package Managers

#### Node.js & JavaScript Runtime
- **Node.js:** `v25.2.1` with **npm** `11.6.4` - Direct install via Arch repos (not using NVM)
- **pnpm** `10.23.0-1` - Primary package manager (3x faster than npm, massive disk savings via hard links)
- **bun-bin** `1.3.3-1` (AUR) - All-in-one JavaScript runtime (10-100x faster, includes bundler, test runner, package manager)

**Why not NVM?**
NVM (Node Version Manager) is useful for managing multiple Node.js versions but adds shell initialization overhead (several milliseconds delay). Since only one Node.js version is needed for this system, direct install from Arch repos is simpler and has zero performance overhead. If multiple versions were needed, FNM (Fast Node Manager, Rust-based) would be preferred over NVM for better performance.

**Package Manager Strategy:**
Use pnpm for all projects (proven, stable, massive performance gains). Keep npm as fallback. Use bun for fast script execution and experimentation. All three coexist without conflict.

#### Python
- **Python** `3.13.7-1` with **pip** and **uv** (fast Python package manager)

#### Git
- **Git** `2.52.0-2` with **GitHub CLI** (`gh`)

### Utilities
- **eza** - Modern `ls` replacement with icons, colors, and git integration. Active fork of unmaintained exa. Used for terminal file listing in modular zsh config.
- **fzf** - Fuzzy finder for command-line. Used in zsh modules for alias searching (va), Chrome bookmarks/history browsing (ib/ih), and interactive selection workflows.
- **jq** `1.8.1-1` - Command-line JSON processor. The de facto standard for parsing, filtering, and transforming JSON data in shell scripts and pipelines. Powerful query language for extracting specific fields, reshaping data, and formatting output. Industry-standard tool used in DevOps, API testing, and data processing workflows.
- **glow** - Markdown renderer for terminal
- **neovim** - Terminal editor
- **openssh** - SSH client/server
- **unzip** - Archive extraction

---

## Networking

### Network Manager
- **NetworkManager** `1.54.2-1`
- Handles WiFi, Ethernet, VPN connections

---

## Key Decisions Summary

| Decision | Choice | Reason |
|----------|--------|--------|
| Browser | Chrome over Chromium | Built-in Google sync, no manual API setup |
| Launcher | Rofi over Fuzzel/Tofi | Most popular, best theme ecosystem |
| Rofi Themes | newmanls over adi1090x | Modern, Rofi 2.0 compatible, actively maintained |
| Audio | PipeWire over PulseAudio | Modern standard, better performance |
| Keyring | None (removed gnome-keyring) | Using 1Password instead |
| Fonts | Keep all 67 Nerd Fonts | Maximum compatibility |
| Terminal | Alacritty over Kitty | Lower memory usage for parallel Claude Code sessions |
| Node.js | Direct install over NVM | Single version needed, no shell overhead |
| VRR | Disabled on center monitor | Personal preference |

---

## Quick Reference

### Reload Hyprland Config
```bash
hyprctl reload
```

### Launch Rofi Theme Selector
```bash
rofi-theme-selector
```

### Check Audio Devices
```bash
wpctl status
```

### Monitor Layout
```
[Portrait Left] [Landscape Center TV] [Portrait Right]
    DP-1           HDMI-A-3              DP-2
   3840x2160       3840x2160           3840x2160
     @60Hz          @120Hz               @60Hz
```

---

## Notes

- All transparency set to 0.85 opacity for VS Code, Chrome, Spotify
- Border gradient animated via script: hot pink → purple → deep purple → royal purple → orange-red
- Using dwindle layout with `Super + J` to toggle split orientation
- Scratchpad workspace bound to `Super + S`
- Dolphin file manager configured but not installed (install with: `sudo pacman -S dolphin`)
