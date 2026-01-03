# Package Categories

Explicitly installed packages grouped by purpose and criticality.

**Legend:**
- `[SYSTEM]` - Critical for boot/function, don't remove
- `[CORE]` - Important infrastructure, replaceable with care
- `[APP]` - User applications
- `[DEV]` - Development tools
- `[UTIL]` - CLI utilities and enhancements

---

## [SYSTEM] Critical System

Cannot be removed without breaking the system.

- `base` - Core Arch packages
- `base-devel` - Build essentials (gcc, make, etc.)
- `linux` - Kernel
- `linux-firmware` - Hardware firmware
- `sudo` - Privilege escalation
- `dosfstools` - FAT filesystem tools (needed for EFI)

## [SYSTEM] Hardware & Drivers

Required for hardware functionality.

- `bluez` - Bluetooth stack
- `bluez-utils` - Bluetooth CLI tools
- `ddcutil` - Monitor brightness control
- `mesa-utils` - OpenGL utilities
- `vulkan-tools` - Vulkan diagnostics
- `intel-gpu-tools` - Intel GPU tools (for Arc B580)
- `libva-utils` - Video acceleration utils
- `v4l-utils` - Video4Linux utilities
- `evtest` - Input device testing
- `ethtool` - Network driver settings
- `usbutils` - USB utilities

## [SYSTEM] Networking & Audio

Core system services.

- `networkmanager` - Network management
- `openssh` - SSH client/server
- `pipewire-alsa` - ALSA integration
- `pipewire-jack` - JACK integration
- `pipewire-pulse` - PulseAudio replacement
- `wireplumber` - PipeWire session manager
- `sound-theme-freedesktop` - System sounds

## [CORE] Desktop Environment

Hyprland and Wayland stack.

- `hyprland` - Wayland compositor
- `hyprpaper` - Wallpaper daemon
- `xdg-desktop-portal-gtk` - GTK portal
- `xdg-desktop-portal-hyprland` - Hyprland portal
- `qt5-wayland` - Qt5 Wayland support
- `qt6-wayland` - Qt6 Wayland support
- `wl-clipboard` - Wayland clipboard
- `grim` - Screenshot tool
- `slurp` - Region selection
- `rofi` - Application launcher
- `rofi-themes-collection-git` - Rofi themes
- `libnotify` - Notification library
- `ydotool` - Input automation

## [CORE] Terminal & Shell

- `alacritty` - Terminal emulator
- `zsh` - Shell
- `starship` - Shell prompt

## [APP] Applications

User-facing applications.

- `1password` - Password manager
- `code` - VS Code
- `google-chrome` - Browser
- `gimp` - Image editor
- `mpv` - Video player
- `okular` - PDF viewer
- `spotify-launcher` - Spotify
- `spicetify-cli` - Spotify customization
- `swayimg` - Image viewer
- `thunar` - File manager
- `zoom` - Video conferencing

## [APP] Voice & Input

- `hyprwhspr` - Voice dictation

## [DEV] Development Tools

- `git` - Version control
- `github-cli` - GitHub CLI
- `neovim` - Text editor
- `python` - Python runtime
- `python-pip` - Python packages
- `npm` - Node package manager
- `pnpm` - Fast npm alternative
- `bun-bin` - JavaScript runtime
- `uv` - Python package manager
- `google-cloud-cli` - GCP tools
- `vercel` - Vercel CLI
- `claude-code` - Claude Code CLI

## [DEV] Build & Debug

- `paru` - AUR helper
- `paru-debug` - Debug symbols

## [UTIL] CLI Enhancements

Modern replacements for classic tools.

- `bat` - Better cat
- `eza` - Better ls
- `fd` - Better find
- `fzf` - Fuzzy finder
- `glow` - Markdown viewer
- `jq` - JSON processor
- `less` - Pager
- `btop` - System monitor
- `nvtop` - GPU monitor
- `bluetui` - Bluetooth TUI

## [UTIL] Media & Files

- `ffmpeg` - Media processing
- `imagemagick` - Image processing
- `yt-dlp` - Video downloader
- `wget` - HTTP downloads
- `unzip` - Archive extraction

## [UTIL] Secrets & Email

- `pass` - Password store (GPG-based)
- `himalaya` - Email CLI

## [UTIL] Fonts

- `noto-fonts-emoji` - Emoji support

*Note: Nerd fonts listed separately in `fonts.txt`*

---

*Auto-generated. Regenerate with `/pacman`.*
