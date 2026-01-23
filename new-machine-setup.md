# New Machine Setup

Fresh Arch Linux install → fully replicated environment.

---

## Overview

1. Boot Arch ISO
2. Connect to internet
3. Install Claude Code in live session
4. Paste API key, launch Claude
5. **Claude takes over** — partitions, formats, mounts drive
6. pacstrap base system + kernel + microcode + networking
7. Generate fstab
8. Chroot: timezone, locale, hostname, NetworkManager
9. Create user with sudo
10. Install systemd-boot + boot entries
11. Reboot *(you type your password at login)*
12. Install git + base-devel + github-cli + paru + claude-code on real system
13. `gh auth login` *(you punch a code into your phone)*
14. Generate SSH key, add to GitHub
15. Clone sys-admin repo (Claude has full context now)
16. Clone dotfiles + checkout
17. Install all packages from both lists
18. Switch shell to zsh, source config
19. Sign into apps (1Password, Chrome, Spotify)

**You do 5 things with your hands:** boot USB, connect internet, paste API key, type login password after reboot, punch GitHub device code into phone. Claude does the rest.

---

## Part 0: Live ISO — Get Claude Running

Boot the [Arch ISO](https://archlinux.org/download/) (USB stick via Ventoy or `dd`).

### Connect to internet

```bash
# Wired: should just work (dhcpcd runs in ISO)
# WiFi:
iwctl station wlan0 connect "SSID"
```

Verify: `ping archlinux.org`

### Install Claude Code

```bash
pacman -Sy nodejs npm
npm i -g @anthropic-ai/claude-code
```

### Launch Claude

```bash
export ANTHROPIC_API_KEY=sk-ant-...
claude
```

---

**>>> Claude takes over from here ↓**

---

## Part 1: Arch Install (Claude executes)

### Partition the drive

```bash
fdisk /dev/nvme0n1
```

Create two partitions (GPT):

| # | Type | Size | Purpose |
|---|------|------|---------|
| 1 | EFI System | 1G | Boot |
| 2 | Linux filesystem | Rest | Root |

### Format

```bash
mkfs.fat -F32 /dev/nvme0n1p1
mkfs.ext4 /dev/nvme0n1p2
```

### Mount

```bash
mount /dev/nvme0n1p2 /mnt
mount --mkdir /dev/nvme0n1p1 /mnt/boot
```

### Install base system

```bash
pacstrap -K /mnt base linux linux-firmware amd-ucode networkmanager sudo vim
```

Note: use `intel-ucode` instead of `amd-ucode` for Intel CPUs.

### Generate fstab

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

### Chroot and configure

```bash
arch-chroot /mnt
```

```bash
ln -sf /usr/share/zoneinfo/America/Vancouver /etc/localtime
hwclock --systohc

# Locale
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Hostname
echo "archbox" > /etc/hostname

# Enable networking
systemctl enable NetworkManager
```

### Create user

```bash
useradd -m -G wheel -s /bin/bash neo
passwd neo
EDITOR=vim visudo  # Uncomment %wheel ALL=(ALL:ALL) ALL
```

### Install systemd-boot

```bash
bootctl install
```

Create `/boot/loader/loader.conf`:
```
default arch.conf
timeout 3
console-mode max
editor no
```

Create `/boot/loader/entries/arch.conf`:
```
title   Arch Linux
linux   /vmlinuz-linux
initrd  /amd-ucode.img
initrd  /initramfs-linux.img
options root=/dev/nvme0n1p2 rw
```

### Reboot

```bash
exit
umount -R /mnt
reboot
```

Remove USB. Log in as `neo`.

---

## Part 2: Environment Setup (Claude executes)

### Install toolchain + Claude Code on real system

```bash
sudo pacman -S git base-devel github-cli nodejs npm
npm i -g @anthropic-ai/claude-code
```

### Install paru

```bash
git clone https://aur.archlinux.org/paru.git /tmp/paru
cd /tmp/paru && makepkg -si
cd ~
```

### Authenticate GitHub (user punches code into phone)

```bash
gh auth login
```

### SSH key

```bash
ssh-keygen -t ed25519 -C "your-email"
gh ssh-key add ~/.ssh/id_ed25519.pub --title "archbox"
```

### Clone sys-admin repo (Claude gets full context)

```bash
mkdir -p ~/agents/admin
git clone git@github.com:rstock-co/sys-admin.git ~/agents/admin/system
```

### Clone and checkout dotfiles

```bash
git clone --bare git@github.com:rstock-co/dotfiles.git $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dotfiles checkout
dotfiles config --local status.showUntrackedFiles no
```

If checkout conflicts with existing files:
```bash
mkdir -p ~/.dotfiles-backup
dotfiles checkout 2>&1 | grep -E "\s+\." | awk '{print $1}' | xargs -I{} mv {} ~/.dotfiles-backup/{}
dotfiles checkout
```

### Install all packages

```bash
sudo pacman -S --needed - < ~/agents/admin/system/data/packages/pkglist.txt
paru -S --needed - < ~/agents/admin/system/data/packages/aur-pkglist.txt
```

### Switch shell to zsh

```bash
chsh -s /usr/bin/zsh
source ~/.zshrc
```

---

## What's NOT covered (manual per-machine)

- **1Password:** Sign in via app
- **Chrome:** Sign into Google account for sync
- **Spotify + Spicetify:** Sign in, apply theme
- **Monitor layout:** May need adjusting in `hyprland.conf` if different hardware
- **GPU-specific workarounds:** Current config assumes Arc B580 (xe driver quirks)
