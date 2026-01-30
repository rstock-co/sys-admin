# Hyprland Configuration Guide

## Installation

```bash
# Core Hyprland components
sudo pacman -S \
  hyprland \
  waybar \
  wofi \
  wl-clipboard \
  xdg-desktop-portal-hyprland \
  xdg-desktop-portal-gtk \
  polkit-gnome \
  qt5-wayland \
  qt6-wayland \
  mako \
  swaylock \
  swaybg \
  grim \
  slurp
```

## Monitor Configuration

### 3-Monitor Setup (Portrait-Landscape-Portrait)

```conf
# ~/.config/hypr/hyprland.conf

# Center: TCL 55" @ 120Hz (main workspace)
monitor=DP-1,3840x2160@120,2160x0,1

# Left: Samsung 32" portrait @ 60Hz
monitor=DP-2,3840x2160@60,0x0,1,transform,1

# Right: Samsung 32" portrait @ 60Hz
monitor=DP-3,3840x2160@60,6000x0,1,transform,1

# Workspace assignments
workspace=1,monitor:DP-1,default:true
workspace=2,monitor:DP-1
workspace=3,monitor:DP-2,default:true
workspace=4,monitor:DP-2
workspace=5,monitor:DP-3,default:true
workspace=6,monitor:DP-3
```

**Transform values**: `0`=normal, `1`=90° CW, `2`=180°, `3`=90° CCW

### Monitor Commands

```bash
# List all monitors
hyprctl monitors

# Check available modes
hyprctl monitors | grep availableModes

# Force monitor refresh
hyprctl reload

# Set monitor at runtime
hyprctl keyword monitor HDMI-A-3,3840x2160@120,2160x0,1
```

## Environment Variables

```conf
# ~/.config/hypr/hyprland.conf

# Wayland support
env = GDK_BACKEND,wayland,x11
env = QT_QPA_PLATFORM,wayland;xcb
env = SDL_VIDEODRIVER,wayland
env = CLUTTER_BACKEND,wayland
env = XDG_CURRENT_DESKTOP,Hyprland
env = XDG_SESSION_TYPE,wayland
env = XDG_SESSION_DESKTOP,Hyprland
env = ELECTRON_OZONE_PLATFORM_HINT,auto

# Intel Arc GPU
env = LIBVA_DRIVER_NAME,iHD
```

## Autostart

```conf
exec-once = waybar
exec-once = mako
exec-once = /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1
exec-once = dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP
```

## Default Keybindings

```conf
$mainMod = SUPER

# Applications
bind = $mainMod, Q, exec, alacritty
bind = $mainMod, C, killactive,
bind = $mainMod, M, exit,
bind = $mainMod, E, exec, thunar
bind = $mainMod, V, togglefloating,
bind = $mainMod, R, exec, wofi --show drun
bind = $mainMod, P, pseudo,
bind = $mainMod, J, togglesplit,

# Focus
bind = $mainMod, left, movefocus, l
bind = $mainMod, right, movefocus, r
bind = $mainMod, up, movefocus, u
bind = $mainMod, down, movefocus, d

# Workspaces
bind = $mainMod, 1, workspace, 1
bind = $mainMod, 2, workspace, 2
bind = $mainMod, 3, workspace, 3
bind = $mainMod, 4, workspace, 4
bind = $mainMod, 5, workspace, 5
bind = $mainMod, 6, workspace, 6

# Move to workspace
bind = $mainMod SHIFT, 1, movetoworkspace, 1
bind = $mainMod SHIFT, 2, movetoworkspace, 2
bind = $mainMod SHIFT, 3, movetoworkspace, 3
bind = $mainMod SHIFT, 4, movetoworkspace, 4
bind = $mainMod SHIFT, 5, movetoworkspace, 5
bind = $mainMod SHIFT, 6, movetoworkspace, 6

# Mouse bindings
bindm = $mainMod, mouse:272, movewindow
bindm = $mainMod, mouse:273, resizewindow
```

## Native Wayland for Apps

### Chrome/Chromium

Create `~/.config/chromium-flags.conf`:
```
--ozone-platform-hint=auto
--enable-features=TouchpadOverscrollHistoryNavigation
--enable-features=WaylandWindowDecorations
```

### Electron Apps (VS Code, Discord, etc.)

Create `~/.config/electron-flags.conf`:
```
--ozone-platform=wayland
--enable-features=WaylandWindowDecorations
```

### VS Code Desktop Entry

```bash
mkdir -p ~/.local/share/applications
cp /usr/share/applications/code.desktop ~/.local/share/applications/
sed -i 's|^Exec=/usr/bin/code|Exec=/usr/bin/code --ozone-platform=wayland --enable-features=WaylandWindowDecorations|g' ~/.local/share/applications/code.desktop
```

### Verify Wayland Usage

```bash
# Native Wayland apps won't appear here
xlsclients

# Check if Chrome is using Wayland
ps aux | grep chromium | grep wayland
```

## Status Bar Options

| Bar | Stars | Language | Best For |
|-----|-------|----------|----------|
| **Waybar** | 9.9k | JSON+CSS | Beginners, stability |
| **AGS** | 2.8k | TypeScript | Advanced ricing |
| **Eww** | 11.5k | Lisp | WM-independent, hybrid |

### Waybar Quick Setup

```bash
mkdir -p ~/.config/waybar

# Config: ~/.config/waybar/config
{
    "layer": "top",
    "position": "top",
    "height": 30,
    "modules-left": ["hyprland/workspaces", "hyprland/window"],
    "modules-right": ["cpu", "memory", "network", "pulseaudio", "clock"],
    "clock": { "format": "{:%Y-%m-%d %H:%M}" },
    "cpu": { "format": "CPU: {usage}%" },
    "memory": { "format": "RAM: {}%" }
}
```

## Decorations & Animations

```conf
general {
    gaps_in = 5
    gaps_out = 10
    border_size = 2
    col.active_border = rgba(33ccffee) rgba(00ff99ee) 45deg
    col.inactive_border = rgba(595959aa)
    layout = dwindle
}

decoration {
    rounding = 10
    blur {
        enabled = true
        size = 3
        passes = 1
    }
    drop_shadow = yes
    shadow_range = 4
}

animations {
    enabled = yes
    bezier = myBezier, 0.05, 0.9, 0.1, 1.05
    animation = windows, 1, 7, myBezier
    animation = windowsOut, 1, 7, default, popin 80%
    animation = fade, 1, 7, default
    animation = workspaces, 1, 6, default
}
```

## Troubleshooting

### Monitor Not Detected

```bash
# Check connected displays
hyprctl monitors

# Check DRM devices
ls /sys/class/drm/

# Force detection
hyprctl reload
```

### Wrong Resolution

```bash
# List available modes
wlr-randr

# Set specific mode
hyprctl keyword monitor DP-1,3840x2160@60,0x0,1
```

### XWayland Apps Blurry

```conf
# In hyprland.conf
xwayland {
    force_zero_scaling = true
}

# Set GDK scale
env = GDK_SCALE,2
```

## Ricing Resources

- **Top Rice Repos**: end-4/dots-hyprland (10.5k⭐), prasanthrangan/hyprdots (8.6k⭐)
- **Wallpapers**: JaKooLit/Wallpaper-Bank, dharmx/walls
- **Color Schemes**: Catppuccin, Tokyonight, Everforest, Nord, Gruvbox
- **r/unixporn**: Search "Hyprland" sorted by Top
