# Modern Arch Linux Tech Stack Recommendations

**Generated from analysis-engine subagent**
**Date**: 2025-11-25
**Target**: Ryzen 9 7950X + Arc B580 development machine

## Packages to REPLACE (Upgrade to Modern Alternatives)

### Shell & CLI Tools
- **OLD**: `htop`
- **NEW**: `btop`
- **REASON**: Modern C++ rewrite with GPU monitoring, network stats, better UI, themes. Perfect for monitoring your 16-core Ryzen 9.

- **OLD**: `grep`
- **NEW**: `ripgrep` (rg)
- **REASON**: 10-100x faster than grep, respects .gitignore by default, colored output. Essential for large codebases.

- **OLD**: `find`
- **NEW**: `fd`
- **REASON**: 5-10x faster than find, simpler syntax, colored output, respects .gitignore.

- **OLD**: `ranger`
- **NEW**: `yazi`
- **REASON**: Modern file manager written in Rust, async operations, image previews with sixel/kitty, much faster on large directories.

- **OLD**: `tmux`
- **NEW**: `zellij`
- **REASON**: Modern Rust alternative with better defaults, floating panes, session resurrection, better plugin system. (Keep tmux if heavily invested in config)

### Audio System
- **OLD**: `pulseaudio` + `pulseaudio-alsa` + `pulseaudio-bluetooth`
- **NEW**: `pipewire` + `pipewire-alsa` + `pipewire-pulse` + `pipewire-jack` + `wireplumber`
- **REASON**: Modern audio server with lower latency, better Bluetooth support, professional audio capabilities (Jack replacement). Standard on 2025 systems.

### Display & Session
- **OLD**: `xorg-server` + `xorg-xinit` + `lightdm` + `lightdm-gtk-greeter`
- **NEW**: `hyprland` + `wayland` + `sddm`
- **REASON**: Wayland compositor with GPU acceleration on Arc B580, modern protocols, better multi-monitor, smoother animations. Or keep Xorg with `ly` (minimal TUI display manager) if staying on X11.

### Text Editor
- **OLD**: `nano` + `vim`
- **NEW**: `helix`
- **REASON**: Modern modal editor with LSP built-in, multiple cursors, tree-sitter syntax, better defaults than Vim. Faster iteration than Neovim setup.

### System Monitoring
- **OLD**: None present
- **NEW**: `nvtop`
- **REASON**: GPU monitoring for Intel Arc B580 - essential for GPU-accelerated workloads. Supports Intel in recent versions.

## Packages to ADD (Missing Modern Tools)

### Development Tools
- **PACKAGE**: `lazygit`
- **REASON**: TUI for git with intuitive interface, faster than CLI for complex operations. Written in Go, very fast.

- **PACKAGE**: `lazydocker`
- **REASON**: TUI for Docker management. Monitor containers, logs, stats in real-time. Essential if using Docker regularly.

- **PACKAGE**: `tokei`
- **REASON**: Fast code statistics tool - counts lines of code across projects. Written in Rust, useful for project analysis.

- **PACKAGE**: `hyperfine`
- **REASON**: Modern benchmarking tool for comparing command performance. Warm-up runs, statistical analysis.

- **PACKAGE**: `dust`
- **REASON**: Modern `du` replacement with better visualization of disk usage. Instant insights into space consumption.

- **PACKAGE**: `duf`
- **REASON**: Modern `df` replacement with better output formatting and colors. Clearer disk space overview.

- **PACKAGE**: `procs`
- **REASON**: Modern `ps` replacement with colored output, tree view, better filtering. Complements btop.

- **PACKAGE**: `bottom` (btm)
- **REASON**: Alternative to btop - customizable, cross-platform, resource monitoring with graphs.

### Shell Enhancement
- **PACKAGE**: `zoxide`
- **REASON**: Smarter cd command that learns your most-used directories. Jump anywhere with `z <partial-name>`.

- **PACKAGE**: `atuin`
- **REASON**: Magical shell history with SQLite backend, sync across machines, fuzzy search. Replaces Ctrl+R.

- **PACKAGE**: `mcfly`
- **REASON**: Alternative to atuin - uses neural network to prioritize history results by context.

### File Operations
- **PACKAGE**: `rsync`
- **REASON**: Essential for file sync/backup. Should be on every dev machine.

- **PACKAGE**: `rclone`
- **REASON**: Rsync for cloud storage - supports 40+ backends. Sync to S3, Drive, Dropbox, etc.

- **PACKAGE**: `restic`
- **REASON**: Modern backup solution with encryption, deduplication, cloud backends.

### JSON/Data Tools
- **PACKAGE**: `jless`
- **REASON**: JSON viewer with collapsible sections, better than `jq` for exploration.

- **PACKAGE**: `yq`
- **REASON**: jq for YAML/XML/TOML. Essential for modern config file manipulation.

- **PACKAGE**: `glow`
- **REASON**: Render markdown in terminal with styling. Perfect for README previews.

### Network Tools
- **PACKAGE**: `bandwhich`
- **REASON**: Network bandwidth monitor showing which processes use bandwidth. Essential for diagnosing network issues.

- **PACKAGE**: `dog`
- **REASON**: Modern DNS client, better output than `dig`, colored, supports DoH/DoT.

- **PACKAGE**: `httpie`
- **REASON**: Modern curl alternative with better syntax, JSON support, sessions.

- **PACKAGE**: `mtr`
- **REASON**: Combined traceroute and ping - continuous network path analysis.

### System Tools
- **PACKAGE**: `lshw`
- **REASON**: Detailed hardware information. Essential for new system documentation.

- **PACKAGE**: `hwinfo`
- **REASON**: Comprehensive hardware detection. Useful for Arc B580 info.

- **PACKAGE**: `neofetch` or `fastfetch`
- **REASON**: System information display. Fastfetch is faster, written in C.

- **PACKAGE**: `systemctl-tui`
- **REASON**: TUI for systemd service management. Easier than memorizing systemctl commands.

### GPU & Performance
- **PACKAGE**: `intel-gpu-tools`
- **REASON**: Intel GPU debugging and monitoring tools. Essential for Arc B580 development.

- **PACKAGE**: `vulkan-tools`
- **REASON**: Vulkan utilities including `vulkaninfo`. Test Arc B580 Vulkan support.

- **PACKAGE**: `intel-compute-runtime` + `level-zero-loader`
- **REASON**: OpenCL and Level Zero for Intel GPU compute. Essential for GPU-accelerated Python workloads.

- **PACKAGE**: `ocl-icd` + `opencl-headers`
- **REASON**: OpenCL ICD loader for GPU compute frameworks.

### Database Tools
- **PACKAGE**: `pgcli`
- **REASON**: Modern PostgreSQL CLI with autocomplete, syntax highlighting. Better than psql.

- **PACKAGE**: `usql`
- **REASON**: Universal SQL client supporting 20+ databases. One tool for all databases.

### Container/Virtualization
- **PACKAGE**: `podman`
- **REASON**: Daemonless container engine, rootless by default. Modern Docker alternative.

- **PACKAGE**: `distrobox`
- **REASON**: Run any Linux distribution inside your terminal. Perfect for testing/isolation.

### Build Tools
- **PACKAGE**: `mold`
- **REASON**: Modern linker 10-20x faster than GNU ld. Essential for large C++ projects.

- **PACKAGE**: `sccache` or `ccache`
- **REASON**: Compiler cache for Rust/C++. Massive speedup on rebuilds with 16-core CPU.

- **PACKAGE**: `just`
- **REASON**: Modern command runner, better than Make for task automation.

### Python Development
- **PACKAGE**: `ruff`
- **REASON**: Extremely fast Python linter/formatter (10-100x faster than pylint). Written in Rust.

- **PACKAGE**: `ipython`
- **REASON**: Enhanced Python REPL with autocomplete, syntax highlighting.

- **PACKAGE**: `python-poetry`
- **REASON**: Modern Python dependency management. Alternative to pip-tools, works well with uv.

### Node.js Tools
- **PACKAGE**: Keep `pnpm` - it's already modern
- **REASON**: Fast, disk-efficient package manager. Better than npm/yarn.

### Screenshot/Screen Recording
- **OLD**: `shutter`
- **NEW**: `flameshot`
- **REASON**: Modern screenshot tool with annotation, better Wayland support if migrating.

- **PACKAGE**: `wl-clipboard` (if moving to Wayland)
- **REASON**: Wayland clipboard utilities, replaces `xclip`.

### Archive Tools
- **PACKAGE**: `ouch`
- **REASON**: Unified interface for all archive formats. No more remembering tar flags.

- **PACKAGE**: `7zip`
- **REASON**: Better compression than gzip/zip, widely compatible.

## Packages to KEEP (Already Modern)

### Shell & CLI
- `bat` - Modern cat with syntax highlighting (keep)
- `eza` - Modern ls replacement (keep)
- `fzf` - Fuzzy finder, essential tool (keep)
- `jq` - JSON processor, industry standard (keep)
- `starship` - Modern prompt, excellent choice (keep)
- `zsh` + `oh-my-zsh-git` - Modern shell setup (keep)
- `direnv` - Environment management, essential (keep)
- `tmux` - If keeping, still excellent (but consider zellij)

### Development
- `uv` - Cutting-edge Python package installer (keep)
- `rust` - Modern systems language toolchain (keep)
- `clang` - Modern compiler (keep)
- `git` + `github-cli` - Version control essentials (keep)
- `docker` - Container platform (keep, but add podman)
- `pnpm` - Modern Node.js package manager (keep)
- `nodejs` + `npm` - Keep for compatibility
- `nvm` - Node version manager (keep)

### System
- `reflector` - Arch mirror management (keep)
- `paru-bin` - Modern AUR helper (keep)
- `zram-generator` - Memory compression, good for performance (keep)

### Terminal
- `alacritty` - GPU-accelerated terminal, excellent (keep)

### Fonts
- `ttf-jetbrains-mono-nerd` - Modern monospace font (keep)
- `ttf-hack-nerd` - Good monospace alternative (keep)
- `noto-fonts-emoji` - Emoji support (keep)

### Tools
- `ffmpeg` - Video/audio processing standard (keep)
- `unzip` - Archive tool (keep, supplement with ouch)

## Packages to REMOVE (Potentially Outdated/Unused)

### Uncertain Usage
- `openai-codex` - Verify if still used
- `opencode-bin` - Verify if still used
- `gemini-cli` - Verify if still used
- `iwd` + `wireless_tools` + `wpa_supplicant` - May be redundant (NetworkManager handles this)

### X11-specific (If migrating to Wayland)
- `i3-wm` + `i3blocks` + `i3status` + `i3lock` - Replace with Hyprland
- `arandr` - X11 display config tool
- `xorg-xwayland` - Keep only if running X11 apps on Wayland
- `xclip` - Replace with `wl-clipboard` on Wayland

### Audio (Replace with PipeWire)
- `pulseaudio` + `pulseaudio-alsa` + `pulseaudio-bluetooth`
- `pamixer` - Works with PipeWire, but verify
- `alsa-oss` - Likely unnecessary with modern audio stack

## Final Installation Commands

### 1. Remove Old Packages (Staged Replacement)

```bash
# Audio replacement (requires careful migration)
# First install PipeWire, THEN remove PulseAudio
sudo pacman -S pipewire pipewire-alsa pipewire-pulse pipewire-jack wireplumber
systemctl --user enable --now pipewire pipewire-pulse wireplumber
# After verifying audio works:
sudo pacman -Rns pulseaudio pulseaudio-alsa pulseaudio-bluetooth pamixer

# Optional: Remove if migrating to Wayland
# sudo pacman -Rns i3-wm i3blocks i3status i3lock arandr dmenu xclip

# Optional: Remove htop if replacing with btop
# sudo pacman -Rns htop

# Optional: Remove if using helix instead
# sudo pacman -Rns nano vim
```

### 2. Install Modern CLI Tools (pacman)

```bash
sudo pacman -S \
  btop \
  ripgrep \
  fd \
  zoxide \
  dust \
  duf \
  procs \
  bottom \
  rsync \
  rclone \
  restic \
  dog \
  httpie \
  mtr \
  lshw \
  hwinfo \
  fastfetch \
  vulkan-tools \
  intel-gpu-tools \
  intel-compute-runtime \
  level-zero-loader \
  ocl-icd \
  opencl-headers \
  pgcli \
  podman \
  distrobox \
  mold \
  ccache \
  ruff \
  ipython \
  flameshot \
  p7zip \
  helix
```

### 3. Install Modern Tools (AUR via paru)

```bash
paru -S \
  yazi-git \
  lazygit \
  lazydocker \
  tokei \
  hyperfine \
  atuin \
  jless \
  yq \
  glow \
  bandwhich \
  nvtop \
  systemctl-tui \
  usql \
  sccache \
  just \
  ouch
```

### 4. Optional: Wayland Migration

```bash
# If migrating from i3/X11 to Wayland
paru -S hyprland sddm wl-clipboard waybar rofi-wayland swaylock
sudo systemctl enable sddm
```

### 5. Configure New Tools

```bash
# Initialize zoxide
echo 'eval "$(zoxide init zsh)"' >> ~/.zshrc

# Initialize atuin
echo 'eval "$(atuin init zsh)"' >> ~/.zshrc

# Configure starship (already have it)
# Consider adding direnv hook if not present
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# Set mold as default linker
export RUSTFLAGS="-C link-arg=-fuse-ld=mold"

# Configure ccache for C++ builds
export PATH="/usr/lib/ccache/bin:$PATH"

# GPU compute verification
clinfo  # Check OpenCL devices
vulkaninfo  # Check Vulkan support for Arc B580
```

### 6. Verify GPU Support

```bash
# Check Arc B580 detection
lspci | grep -i vga
lshw -C display

# Monitor GPU
nvtop  # Should detect Intel Arc B580
btop   # Should show GPU stats

# Test GPU compute
clinfo  # List OpenCL platforms/devices
```

### 7. System Optimization for 16-Core CPU

```bash
# Configure ccache for parallel builds
ccache --max-size=10G
ccache --set-config=max_files=0

# Rust parallel compilation (in ~/.cargo/config.toml)
mkdir -p ~/.cargo
cat >> ~/.cargo/config.toml << 'EOF'
[build]
jobs = 16

[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
EOF

# Python uv parallel installs (already optimal by default)
```

## Summary of Key Upgrades

**Performance Winners**:
- `htop` → `btop` (GPU monitoring, better for 16-core)
- `grep` → `ripgrep` (10-100x faster)
- `find` → `fd` (5-10x faster)
- `pulseaudio` → `pipewire` (lower latency, better features)
- GNU `ld` → `mold` (10-20x faster linking)

**Modern Replacements**:
- `ranger` → `yazi` (async, faster, better previews)
- `nano`/`vim` → `helix` (modern modal editor, LSP built-in)
- `tmux` → `zellij` (optional, better defaults)

**Essential Additions**:
- `lazygit` + `lazydocker` (TUI productivity)
- `zoxide` + `atuin` (shell navigation/history)
- `nvtop` + `intel-gpu-tools` (Arc B580 monitoring)
- `intel-compute-runtime` (GPU compute for Python/AI workloads)
- `ruff` (10-100x faster Python linting)

**Total Package Count**: ~170 packages (current) → ~200 packages (optimized stack)
