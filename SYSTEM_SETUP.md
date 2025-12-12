# System Setup

Arch Linux workstation with Hyprland. Triple 4K displays. Optimized for parallel Claude Code sessions.

## Core Stack

| Layer | Choice | Config |
|-------|--------|--------|
| OS | Arch Linux | Rolling release |
| WM | Hyprland | `~/.config/hypr/hyprland.conf` |
| Shell | Zsh + Starship | Modular: `~/zshrc/*.sh` |
| Terminal | Alacritty | Low memory (many parallel sessions) |
| Browser | Google Chrome | Built-in sync (not Chromium) |
| Launcher | Rofi | `Super+R`, rofi-wayland |
| Editor | VS Code | `--disable-gpu` (Arc B580 workaround) |
| Audio | PipeWire + WirePlumber | USB speakers (DP audio broken) |
| Passwords | 1Password | No gnome-keyring |

## Key Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Terminal | Alacritty over Kitty | Lower memory for parallel Claude sessions |
| Browser | Chrome over Chromium | Google sync without API key setup |
| Node.js | Direct install over NVM | Single version, no shell overhead |
| Audio output | USB speakers | Arc B580 xe driver DP audio bug |
| TV connection | DP→HDMI cable | Arc B580 xe driver HDMI 120Hz bug |
| VS Code GPU | Disabled | Electron + Arc B580 = system lag |
| VRR | Disabled | Personal preference |

## Visual Style

- **Gaps:** Inner 5px, Outer 20px
- **Borders:** 2px animated gradient (`~/.config/hypr/rotate-border.sh`)
- **Transparency:** 0.85 for VS Code, Chrome, Spotify
- **Rounding:** 10px

## Package Managers

| Type | Tool | Use |
|------|------|-----|
| System | pacman + paru | Arch packages + AUR |
| Node.js | pnpm (primary) | Fast, disk-efficient |
| Node.js | npm (fallback) | Compatibility |
| Node.js | bun | Fast scripts |
| Python | uv | Fast pip replacement |

## Subsystem Configs

Detailed configs live in `config/` with troubleshooting guides:

| Subsystem | Config Doc | Quick Fix |
|-----------|------------|-----------|
| Voice | `config/voice/hyprwhspr.md` | `fix-voice` |
| Display | `config/display/monitors.md` | `wake-tv` / `hyprctl reload` |
| Audio | `config/audio/speakers.md` | `systemctl --user restart pipewire wireplumber` |
| Keyboard | `config/keyboard/yunzii-al98.md` | `Fn+Spacebar` (factory reset) |
| GPU | `config/gpu/arc-b580.md` | Check xe driver loaded |

**Index:** `config/INDEX.md`
