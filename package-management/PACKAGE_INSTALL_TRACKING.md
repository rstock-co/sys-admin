# Package Installation Tracking

**Purpose:** Checklist-style tracker for modern package installations from MODERN_PACKAGES.md analysis.

---

## ✅ Installed Packages

### Shell & CLI Tools
- [x] `bat` - Modern cat with syntax highlighting
- [x] `eza` - Modern ls replacement with icons
- [x] `fzf` - Fuzzy finder
- [x] `jq` - JSON processor
- [x] `starship` - Modern shell prompt
- [x] `zsh` - Modern shell
- [x] `glow` - Markdown renderer for terminal

### Development Tools
- [x] `uv` - Fast Python package installer
- [x] `rust` - Rust toolchain
- [x] `clang` - Modern compiler
- [x] `git` - Version control
- [x] `github-cli` - GitHub CLI (`gh`)
- [x] `docker` - Container platform
- [x] `pnpm` - Fast Node.js package manager
- [x] `nodejs` - Node.js runtime
- [x] `npm` - Node package manager
- [x] `neovim` - Terminal editor
- [x] `openssh` - SSH client/server

### System Tools
- [x] `alacritty` - GPU-accelerated terminal
- [x] `reflector` - Arch mirror management
- [x] `paru-bin` - Modern AUR helper
- [x] `zram-generator` - Memory compression
- [x] `unzip` - Archive extraction

### Audio & Video
- [x] `pipewire` - Modern audio server
- [x] `pipewire-alsa` - ALSA compatibility
- [x] `pipewire-pulse` - PulseAudio replacement
- [x] `pipewire-jack` - JACK compatibility
- [x] `wireplumber` - PipeWire session manager
- [x] `v4l-utils` - Video4Linux utilities
- [x] `ffmpeg` - Video/audio processing

### Window Manager & Desktop
- [x] `hyprland` - Wayland compositor
- [x] `rofi` - App launcher (Wayland version)
- [x] `sddm` - Display manager

### Fonts
- [x] `ttf-jetbrains-mono-nerd` - JetBrains Mono Nerd Font
- [x] `ttf-hack-nerd` - Hack Nerd Font
- [x] `noto-fonts-emoji` - Emoji support
- [x] 67 other Nerd Fonts packages

### Screenshot Tools
- [x] `grim` - Screenshot tool for Wayland
- [x] `slurp` - Area selection for screenshots
- [x] `wl-clipboard` - Wayland clipboard utilities

### Utilities
- [x] `via` (AUR) - QMK/VIA keyboard configurator

---

## 📋 Not Yet Installed

### System Monitoring (High Priority)
- [ ] `btop` - Modern resource monitor with GPU support (replaces htop)
- [ ] `nvtop` - GPU monitoring for Arc B580
- [ ] `bottom` - Alternative resource monitor
- [ ] `procs` - Modern ps replacement

### Shell & CLI Tools (High Priority)
- [ ] `ripgrep` - Fast grep replacement (10-100x faster)
- [ ] `fd` - Fast find replacement (5-10x faster)
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

### GPU & Performance
- [ ] `intel-gpu-tools` - Intel GPU debugging tools
- [ ] `vulkan-tools` - Vulkan utilities (vulkaninfo)
- [ ] `intel-compute-runtime` - OpenCL/Level Zero for Intel GPU
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
- [x] `paru-debug` - Debug symbols, not needed

### Candidates for Removal
- [ ] `htop` - Will replace with `btop` once installed
- [ ] Check: `iwd`, `wireless_tools`, `wpa_supplicant` - May be redundant (NetworkManager handles this)
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
pacman -Qqe > ~/pkglist.txt
dotfiles add pkglist.txt && dotfiles commit -m "Install <package>" && dotfiles push
```

### Install from AUR
```bash
paru -S <package>
pacman -Qqm > ~/aur-pkglist.txt
dotfiles add aur-pkglist.txt && dotfiles commit -m "Install <package>" && dotfiles push
```

### Batch Install (Official Repos)
```bash
sudo pacman -S package1 package2 package3
pacman -Qqe > ~/pkglist.txt
dotfiles add pkglist.txt && dotfiles commit -m "Install multiple packages" && dotfiles push
```

### Batch Install (AUR)
```bash
paru -S package1 package2 package3
pacman -Qqm > ~/aur-pkglist.txt
dotfiles add aur-pkglist.txt && dotfiles commit -m "Install AUR packages" && dotfiles push
```

### Remove Package
```bash
sudo pacman -Rns <package>
pacman -Qqe > ~/pkglist.txt && pacman -Qqm > ~/aur-pkglist.txt
dotfiles add pkglist.txt aur-pkglist.txt && dotfiles commit -m "Remove <package>" && dotfiles push
```

---

## Notes

- **Check boxes:** Update manually as packages are installed
- **Priority:** Focus on "High Priority" items first
- **Testing:** Test each package before marking as installed
- **Documentation:** Update `SYSTEM_SETUP.md` for significant changes
- **Package lists:** Auto-regenerated after every install/remove
