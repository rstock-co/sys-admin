---
name: arch-install-helper
description: Interactive guide for Arch Linux installation on new Ryzen 9 7950X + Arc B580 build
trigger: When user mentions "new PC", "arch install", "boot USB", or references installation guide
---

# Arch Linux Installation Helper

## Purpose

Guide user through complete Arch Linux installation on their new build:
- **CPU**: AMD Ryzen 9 7950X (16-core)
- **GPU**: Intel Arc B580 12GB
- **RAM**: 64GB DDR5-5600
- **Storage**: Samsung 990 PRO 4TB NVMe
- **Motherboard**: MSI MAG X870E Tomahawk WiFi

## Installation Phases

### Phase 1: Bootable USB Creation (Current System)

**Prerequisites**:
- USB drive (8GB+)
- Current Arch system

**Steps**:
1. Read `@docs/new-computer-setup/arch-linux-bootable-usb-guide.md`
2. Download latest Arch ISO
3. Create bootable USB with `dd`
4. Verify USB boot capability

**Output**: Bootable USB ready for new PC

### Phase 2: BIOS/UEFI Configuration (New PC)

**Steps**:
1. Boot new PC, enter BIOS (usually Del or F2)
2. Enable UEFI mode
3. Disable Secure Boot (for easier installation)
4. Set boot priority: USB first
5. Enable XMP/EXPO for RAM (DDR5-5600)
6. Save and reboot from USB

**Output**: System boots Arch Linux live environment

### Phase 3: Installation (From USB)

**Guide user through**:
1. Read `@docs/new-computer-setup/NEW_BUILD_INSTALLATION_GUIDE.md`
2. Partition disk (GPT + UEFI):
   - 512MB EFI partition
   - Rest for root (btrfs recommended)
3. Format partitions
4. Mount filesystems
5. Install base system: `pacstrap /mnt base linux linux-firmware`
6. Generate fstab: `genfstab -U /mnt >> /mnt/etc/fstab`
7. Chroot: `arch-chroot /mnt`
8. Configure system:
   - Set timezone
   - Set locale
   - Set hostname
   - Create user
   - Install bootloader (systemd-boot or GRUB)
9. Install essential packages:
   - `pacman -S base-devel git sudo networkmanager`
10. Enable NetworkManager: `systemctl enable NetworkManager`
11. Set root password
12. Exit chroot and reboot

**Output**: Bootable Arch Linux system

### Phase 4: Post-Installation Setup (New System)

**After first boot**:

1. **Network**:
   ```bash
   nmtui  # Connect to network
   ```

2. **Create user** (if not done during install):
   ```bash
   useradd -m -G wheel -s /bin/bash neo
   passwd neo
   visudo  # Uncomment %wheel ALL=(ALL:ALL) ALL
   ```

3. **Install packages**:
   ```bash
   # Clone dotfiles and scripts
   git clone <dotfiles-repo> ~/dotfiles

   # Run package installation
   cd ~/agents/scripts
   ./install-arch-packages.sh --all
   ```

4. **Install dotfiles**:
   ```bash
   cd ~/dotfiles
   ./install.sh
   ```

5. **GPU drivers** (Intel Arc B580):
   ```bash
   sudo pacman -S mesa lib32-mesa vulkan-intel intel-compute-runtime intel-gpu-tools
   ```

6. **Set default shell**:
   ```bash
   chsh -s $(which zsh)
   ```

7. **Enable services**:
   ```bash
   sudo systemctl enable --now postgresql docker
   ```

**Output**: Fully configured system with dotfiles

### Phase 5: Symbiont Setup

**Final steps**:

1. **Clone symbiont repo**:
   ```bash
   cd ~/agents
   git clone <symbiont-repo> symbiont
   ```

2. **Install Claude Code**:
   ```bash
   # Follow official installation
   ```

3. **Verify specialists**:
   ```bash
   ls -la ~/agents/symbiont/specialists/
   ```

4. **Test spawn**:
   ```bash
   ~/agents/scripts/mycelia-spawn-specialist.sh symbiont-sysadmin "Verify new system setup"
   ```

**Output**: Symbiont operational on new hardware

## Commands Available

- `~/agents/scripts/install-arch-packages.sh` - Package installation
- `~/dotfiles/install.sh` - Dotfiles setup
- `~/agents/scripts/mycelia-spawn-specialist.sh` - Spawn specialists

## Documentation References

Always reference these docs:
- `@docs/new-computer-setup/arch-linux-bootable-usb-guide.md` - USB creation
- `@docs/new-computer-setup/NEW_BUILD_INSTALLATION_GUIDE.md` - Full install guide
- `@docs/new-computer-setup/modern-tech-stack-recommendations.md` - Package recommendations
- `@docs/core/vision/symbiont-hardware.md` - Hardware specifications
- `~/dotfiles/README.md` - Dotfiles usage

## Interactive Mode

When user asks for installation help:

1. **Determine current phase** (ask where they are)
2. **Provide step-by-step guidance** for current phase only
3. **Verify completion** before moving to next phase
4. **Troubleshoot issues** as they arise
5. **Document any deviations** from standard install

## Safety Checks

Before destructive operations:
- ✅ Confirm correct disk (`lsblk`)
- ✅ Verify backup of current system (if applicable)
- ✅ Double-check partition table before format
- ✅ Test bootloader config before reboot

## Common Issues

### USB won't boot
- Verify UEFI vs BIOS mode
- Check Secure Boot disabled
- Try different USB port
- Recreate USB with `dd` using `bs=4M`

### No network after install
- Install NetworkManager during install
- Enable: `systemctl enable --now NetworkManager`
- Use `nmtui` for connection

### Intel Arc GPU not detected
- Install mesa + vulkan-intel + intel-compute-runtime
- Check: `intel_gpu_top` (from intel-gpu-tools)
- Verify: `lspci | grep VGA`

### Ryzen performance
- Enable XMP/EXPO in BIOS for RAM
- Install `linux-zen` kernel for better desktop performance
- Monitor: `btop` or `sensors`

## Output Format

Provide guidance in this format:

```markdown
## Phase X: [Name]

**Current Status**: [Where user is]

**Next Steps**:
1. [Step with command]
2. [Step with expected output]
3. [Verification command]

**Expected Outcome**: [What success looks like]

**Troubleshooting**: [If something goes wrong]
```

## When to Use This Skill

- User mentions new PC build
- User asks about installation
- User needs boot USB created
- User encounters installation issues
- User wants post-install setup guidance
