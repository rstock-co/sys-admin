# Package Installation Tracking

**Purpose:** Checklist-style tracker for modern package installations from MODERN_PACKAGES.md analysis.

---

## ✅ Installed Packages

### Shell & CLI Tools
- [x] `eza` - Modern ls replacement with icons
- [x] `fzf` - Fuzzy finder
- [x] `jq` - JSON processor
- [x] `starship` - Modern shell prompt
- [x] `zsh` - Modern shell
- [x] `glow` - Markdown renderer for terminal
- [x] `ripgrep` - Fast grep replacement (rg command)
- [x] `bat` - Modern cat with syntax highlighting
- [x] `fd` - Fast find replacement

### Development Tools
- [x] `uv` - Fast Python package installer
- [x] `rust` - Rust toolchain
- [x] `git` - Version control
- [x] `github-cli` - GitHub CLI (`gh`)
- [x] `pnpm` - Fast Node.js package manager
- [x] `bun-bin` (AUR) - All-in-one JavaScript runtime (10-100x faster)
- [x] `npm` - Node package manager
- [x] `neovim` - Terminal editor
- [x] `openssh` - SSH client/server
- [x] `python` - Python 3.13.7
- [x] `python-pip` - Python package installer
- [x] `python-sounddevice` (AUR) - Python bindings for PortAudio
- [x] `claude-code` (AUR) - Claude Code CLI agent
- [x] `vercel` (AUR) - Vercel CLI for deployments
- [x] `google-cloud-cli` (AUR) - Google Cloud SDK CLI tools

### System Tools
- [x] `alacritty` - GPU-accelerated terminal
- [x] `paru` (AUR) - Modern AUR helper
- [x] `unzip` - Archive extraction
- [x] `btop` - Modern resource monitor with GPU support
- [x] `nvtop` - GPU monitoring for Arc B580
- [x] `less` - Terminal pager
- [x] `dosfstools` - FAT filesystem utilities
- [x] `sudo` - Privilege escalation
- [x] `base` - Arch Linux base meta package
- [x] `base-devel` - Development meta package (make, gcc, etc.)
- [x] `wget` - File download utility
- [x] `usbutils` - USB device utilities
- [x] `pass` - Unix password manager (GPG-based)
- [x] `thunar` - GTK file manager

### Audio & Video
- [x] `pipewire-alsa` - ALSA compatibility (pulls pipewire)
- [x] `pipewire-pulse` - PulseAudio replacement
- [x] `pipewire-jack` - JACK compatibility
- [x] `wireplumber` - PipeWire session manager
- [x] `sound-theme-freedesktop` - System sound theme
- [x] `v4l-utils` - Video4Linux utilities
- [x] `ffmpeg` - Video/audio processing
- [x] `yt-dlp` - Video/audio downloader (YouTube, Vimeo, etc.)
- [x] `mpv` - Video player

### Window Manager & Desktop
- [x] `hyprland` - Wayland compositor
- [x] `hyprwhspr` (AUR) - Whisper voice input for Hyprland
- [x] `rofi` - App launcher (Wayland version)
- [x] `rofi-themes-collection-git` (AUR) - Rofi theme collection
- [x] `qt5-wayland` - Qt5 Wayland platform plugin
- [x] `qt6-wayland` - Qt6 Wayland platform plugin
- [x] `xdg-desktop-portal-hyprland` - Hyprland-specific portal
- [x] `xdg-desktop-portal-gtk` - GTK portal for file dialogs
- [x] `ydotool` - Generic dotool-like tool for Wayland
- [x] `libnotify` - Notification library

### Fonts
- [x] `ttf-jetbrains-mono-nerd` - JetBrains Mono Nerd Font
- [x] `ttf-hack-nerd` - Hack Nerd Font
- [x] 65 other Nerd Fonts packages (otf-* and ttf-*-nerd)

### Screenshot Tools
- [x] `grim` - Screenshot tool for Wayland
- [x] `slurp` - Area selection for screenshots
- [x] `wl-clipboard` - Wayland clipboard utilities

### Utilities
- [x] `evtest` - Input device event testing tool
- [x] `swayimg` - Image viewer for Wayland

### Network & Connectivity
- [x] `networkmanager` - Network connection manager
- [x] `ethtool` - Ethernet device configuration
- [x] `himalaya` - CLI email client

### Bluetooth
- [x] `bluez` - Bluetooth protocol stack
- [x] `bluez-utils` - Bluetooth utilities
- [x] `bluetui` - TUI for Bluetooth management

### Applications
- [x] `code` - VS Code (OSS version)
- [x] `google-chrome` (AUR) - Google Chrome browser
- [x] `spotify-launcher` - Spotify client
- [x] `spicetify-cli` (AUR) - Spotify customization
- [x] `zoom` (AUR) - Video conferencing
- [x] `1password` (AUR) - Password manager

### Linux Kernel & Firmware
- [x] `linux` - Linux kernel (6.17.9-arch1-1)
- [x] `linux-firmware` - Hardware firmware files

---

## 📋 Not Yet Installed

### System Monitoring (High Priority)
- [ ] `bottom` - Alternative resource monitor
- [ ] `procs` - Modern ps replacement

### Shell & CLI Tools (High Priority)
- [ ] `zoxide` - Smart cd command with learning
- [ ] `atuin` - Enhanced shell history with sync
- [ ] `dust` - Modern du replacement
- [ ] `duf` - Modern df replacement

### Development Tools (High Priority)
- [ ] `lazygit` - TUI for git operations
- [ ] `lazydocker` - TUI for Docker management
- [ ] `tokei` - Fast code statistics
- [ ] `hyperfine` - Command benchmarking tool

### File Management
- [ ] `yazi` - Modern file manager (Rust, async)
- [ ] `rsync` - File sync/backup
- [ ] `rclone` - Cloud storage sync
- [ ] `restic` - Modern backup with encryption

### JSON/Data Tools
- [ ] `jless` - JSON viewer with collapsible sections
- [ ] `yq` - jq for YAML/XML/TOML

### Network Tools
- [ ] `bandwhich` - Network bandwidth monitor by process
- [ ] `dog` - Modern DNS client (better than dig)
- [ ] `httpie` - Modern curl alternative
- [ ] `mtr` - Combined traceroute and ping

### System Information
- [ ] `lshw` - Detailed hardware info
- [ ] `hwinfo` - Comprehensive hardware detection
- [ ] `fastfetch` - Fast system info display

### GPU & Performance (High Priority)
- [x] `intel-gpu-tools` - Intel GPU debugging tools
- [x] `vulkan-tools` - Vulkan utilities (vulkaninfo)
- [x] `libva-utils` - VA-API utilities for hardware acceleration
- [x] `mesa-utils` - Mesa utilities (glxinfo, glxgears)
- [x] `glmark2` - OpenGL benchmark
- [ ] `intel-compute-runtime` - OpenCL/Level Zero for Intel GPU compute
- [ ] `level-zero-loader` - Level Zero API loader
- [ ] `ocl-icd` - OpenCL ICD loader
- [ ] `opencl-headers` - OpenCL headers

### Database Tools
- [ ] `pgcli` - Modern PostgreSQL CLI
- [ ] `usql` - Universal SQL client (20+ databases)

### Container/Virtualization
- [ ] `podman` - Daemonless container engine
- [ ] `distrobox` - Run any Linux distro in terminal

### Build Tools
- [ ] `mold` - Fast linker (10-20x faster than GNU ld)
- [ ] `sccache` - Compiler cache for Rust
- [ ] `ccache` - Compiler cache for C/C++
- [ ] `just` - Modern command runner

### Python Development
- [ ] `ruff` - Fast Python linter/formatter
- [ ] `ipython` - Enhanced Python REPL
- [ ] `python-poetry` - Python dependency management

### Archive Tools
- [ ] `ouch` - Unified archive interface
- [ ] `p7zip` - 7zip compression

### Text Editors (Optional)
- [ ] `helix` - Modern modal editor with LSP built-in

### Terminal Multiplexer (Optional)
- [ ] `zellij` - Modern tmux alternative

### Screenshot Tools
- [ ] `flameshot` - Screenshot tool with annotation (alternative to grim/slurp)

### System Management
- [ ] `systemctl-tui` - TUI for systemd management

---

## 🗑️ Packages to Consider Removing

### Already Removed (2025-11-28)
- [x] `gnome-keyring` - Replaced by 1Password
- [x] `chromium` - Replaced by Google Chrome
- [x] `polkit-gnome` - Legacy package, not needed

### Still Installed (Consider Removing)
- [ ] `paru-debug` - Debug symbols (158MB), not needed for normal use

### Candidates for Removal
- [ ] `htop` - btop is now installed, can remove htop
- [ ] Check: `iwd`, `wireless_tools`, `wpa_supplicant` - May be redundant (NetworkManager handles this)
- [ ] `via` - VIA keyboard configurator (if no longer using YUNZII AL98 customization)
- [ ] Verify: Old X11 tools if fully migrated to Wayland

---

## Quick Commands

### Check if Package Installed
```bash
pacman -Q <package>
```

### Install from Official Repos
```bash
sudo pacman -S <package>
pacman -Qqe > ~/agents/sys-admin/package-management/pkglist.txt
git add package-management/pkglist.txt && git commit -m "Install <package>" && git push
```

### Install from AUR
```bash
paru -S <package>
pacman -Qqm > ~/agents/sys-admin/package-management/aur-pkglist.txt
git add package-management/aur-pkglist.txt && git commit -m "Install <package>" && git push
```

### Batch Install (Official Repos)
```bash
sudo pacman -S package1 package2 package3
pacman -Qqe > ~/agents/sys-admin/package-management/pkglist.txt
git add package-management/pkglist.txt && git commit -m "Install multiple packages" && git push
```

### Batch Install (AUR)
```bash
paru -S package1 package2 package3
pacman -Qqm > ~/agents/sys-admin/package-management/aur-pkglist.txt
git add package-management/aur-pkglist.txt && git commit -m "Install AUR packages" && git push
```

### Remove Package
```bash
sudo pacman -Rns <package>
pacman -Qqe > ~/agents/sys-admin/package-management/pkglist.txt
pacman -Qqm > ~/agents/sys-admin/package-management/aur-pkglist.txt
git add package-management/pkglist.txt package-management/aur-pkglist.txt && git commit -m "Remove <package>" && git push
```

---

## Notes

- **Check boxes:** Update manually as packages are installed
- **Priority:** Focus on "High Priority" items first
- **Testing:** Test each package before marking as installed
- **Documentation:** Update `SYSTEM_SETUP.md` for significant changes
- **Package lists:** Auto-regenerated after every install/remove
