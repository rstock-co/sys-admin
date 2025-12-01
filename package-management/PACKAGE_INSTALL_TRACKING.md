# Package Installation Tracking

**Purpose:** Track all package installations, removals, and configuration changes with timestamps and rationale.

---

## Active Package Changes

### Pending Installations
*(Packages identified for installation but not yet installed)*

None currently pending.

### Pending Removals
*(Packages identified for removal but not yet removed)*

None currently pending.

---

## Installation History

### 2025-11-30

#### Creative Pebble Pro Desktop Speakers
- **Type:** Hardware (USB-C powered Bluetooth speakers)
- **Status:** Purchased (Best Buy Canada, refurbished, $30 CAD)
- **Rationale:** Workaround for Intel Arc B580 xe driver DisplayPort audio bug
- **Documentation:** `SYSTEM_SETUP.md` Audio section

---

## Removal History

### 2025-11-28

#### gnome-keyring
- **Package:** `gnome-keyring`
- **Removed:** November 28, 2025
- **Rationale:** Not needed - using 1Password for password management, not using Chromium's built-in password manager
- **Cleanup:** Removed from Hyprland autostart, Chromium flags, all data directories
- **Documentation:** `SYSTEM_SETUP.md`

#### Chromium
- **Package:** `chromium`
- **Removed:** November 28, 2025
- **Replaced With:** Google Chrome (`google-chrome` from AUR)
- **Rationale:** Chromium can't sync Google account without manual API key setup, Chrome has it built-in
- **Cleanup:** Removed config dir, cache, desktop file, Hyprland window rules
- **Documentation:** `SYSTEM_SETUP.md`

#### polkit-gnome
- **Package:** `polkit-gnome`
- **Removed:** November 28, 2025
- **Rationale:** "Legacy" package, not configured in Hyprland (wasn't running), not needed
- **Documentation:** `SYSTEM_SETUP.md`

#### paru-debug
- **Package:** `paru-debug`
- **Removed:** November 28, 2025
- **Rationale:** Debug symbols for paru, only needed for development
- **Documentation:** `SYSTEM_SETUP.md`

---

## Configuration Changes

### 2025-11-30

#### Package List Format
- **Changed:** Package list generation and tracking method
- **Location:** `~/pkglist.txt` and `~/aur-pkglist.txt`
- **Method:**
  ```bash
  pacman -Qqe > ~/pkglist.txt    # Explicit packages
  pacman -Qqm > ~/aur-pkglist.txt # AUR packages
  ```
- **Tracked In:** Dotfiles repository (bare git method)
- **Rationale:** Maintain accurate system state for restoration/documentation

---

## Future Considerations

### From MODERN_PACKAGES.md Analysis

**High Priority:**
- Replace `htop` with `btop` (GPU monitoring, better for 16-core Ryzen 9)
- Add `ripgrep` (10-100x faster than grep)
- Add `fd` (5-10x faster than find)
- Add `lazygit` (TUI for git operations)
- Add `zoxide` (smarter cd command)
- Add `nvtop` (GPU monitoring for Arc B580)

**Medium Priority:**
- Add `yazi` (modern file manager, replace ranger if installed)
- Add `atuin` (enhanced shell history)
- Add `dust` (modern du replacement)
- Add `duf` (modern df replacement)
- Add `hyperfine` (benchmarking tool)

**Low Priority / Optional:**
- Consider `helix` as modern modal editor
- Consider `zellij` as modern tmux alternative
- Evaluate GPU compute packages: `intel-compute-runtime`, `level-zero-loader`

**Audio System Migration:**
- Current: PipeWire (already modern, installed)
- No changes needed

**Display System:**
- Current: Hyprland (already modern, installed)
- No changes needed

---

## Notes

- **Package lists** (`pkglist.txt`, `aur-pkglist.txt`) are regenerated after every install/removal
- **System documentation** (`SYSTEM_SETUP.md`) is updated for significant package changes
- **Dotfiles repository** tracks package lists and major config changes
- **This file** tracks chronological history with rationale for agent memory

---

## Quick Commands

### Update Package Lists
```bash
pacman -Qqe > ~/pkglist.txt && pacman -Qqm > ~/aur-pkglist.txt
dotfiles add pkglist.txt aur-pkglist.txt
dotfiles commit -m "Update package lists"
dotfiles push
```

### Check Package Installation Status
```bash
pacman -Q <package>              # Check if installed
paru -Ss <package>               # Search for package
pacman -Qi <package>             # Detailed package info
pacman -Ql <package>             # List package files
```

### Install Package Workflow
```bash
# 1. Install
sudo pacman -S <package>         # or: paru -S <aur-package>

# 2. Update package lists
pacman -Qqe > ~/pkglist.txt
pacman -Qqm > ~/aur-pkglist.txt

# 3. Track in dotfiles
dotfiles add pkglist.txt aur-pkglist.txt
dotfiles commit -m "Install <package>"
dotfiles push

# 4. Update this tracking file
# Add entry to Installation History section

# 5. Update SYSTEM_SETUP.md if significant
# Document decision and rationale
```

### Remove Package Workflow
```bash
# 1. Remove (use -Rns to remove with deps and configs)
sudo pacman -Rns <package>

# 2. Update package lists
pacman -Qqe > ~/pkglist.txt
pacman -Qqm > ~/aur-pkglist.txt

# 3. Track in dotfiles
dotfiles add pkglist.txt aur-pkglist.txt
dotfiles commit -m "Remove <package>"
dotfiles push

# 4. Update this tracking file
# Add entry to Removal History section

# 5. Update SYSTEM_SETUP.md if significant
# Document removal and rationale
```
