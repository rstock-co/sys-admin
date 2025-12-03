# Force Apps to Use Wayland on Hyprland

Complete guide for enabling native Wayland support in Chrome, VS Code, and other Electron-based development applications on Hyprland. Based on official documentation from Chromium, Electron, Arch Wiki, and Hyprland Wiki.

---

## Table of Contents

1. [Overview](#overview)
2. [Chrome/Chromium](#chromechromium)
3. [VS Code and Electron Apps](#vs-code-and-electron-apps)
4. [Environment Variables](#environment-variables)
5. [Screen Sharing and Portals](#screen-sharing-and-portals)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

---

## Overview

### Why Native Wayland Support Matters

Running applications in native Wayland mode (instead of XWayland compatibility layer) provides:

- **Better performance**: Direct rendering without X11 translation overhead
- **Proper HiDPI/fractional scaling**: Crisp text and UI elements
- **Improved touchpad gestures**: Native Wayland touchpad support
- **Screen sharing**: Modern PipeWire-based capture via xdg-desktop-portal
- **Security**: Wayland's security model with proper sandboxing

### The Ozone Platform

Chromium and Electron use the **Ozone** platform abstraction layer for graphics and input. Ozone allows runtime binding of different display backends (X11, Wayland) via command-line flags. Wayland support has been actively developed by Igalia in the Chromium mainline repository since 2016.

---

## Chrome/Chromium

### Current Status

- **Chrome/Chromium 140+**: Wayland support enabled by default
- **Chrome/Chromium 98+**: Use `--ozone-platform-hint=auto`
- **Chrome/Chromium 87-97**: Use `--enable-features=UseOzonePlatform --ozone-platform=wayland`

### Recommended Configuration

#### Method 1: Configuration File (Recommended)

Create or edit `~/.config/chromium-flags.conf` (or `~/.config/chrome-flags.conf` for Google Chrome):

```bash
--ozone-platform-hint=auto
```

The `auto` value automatically selects Wayland when running in a Wayland session and falls back to X11 otherwise, allowing a single configuration for both session types.

#### Method 2: Browser Flags Menu

1. Navigate to `chrome://flags`
2. Search for "Preferred Ozone platform"
3. Set to "Auto"
4. **Important**: Close and reopen the browser (don't use the relaunch button)

#### Method 3: Desktop File (Application-Specific)

Copy the desktop file to your local applications directory and modify the Exec line:

```bash
cp /usr/share/applications/chromium.desktop ~/.local/share/applications/
```

Edit `~/.local/share/applications/chromium.desktop`:

```desktop
Exec=/usr/bin/chromium --ozone-platform-hint=auto %U
```

### Additional Recommended Flags

#### For GTK4 Integration

```bash
--gtk-version=4
```

#### For Input Method Support

**Standard input methods:**
```bash
--disable-gtk-ime
```

**Fcitx5 users:**
```bash
--enable-wayland-ime --wayland-text-input-version=3
```

Note: The `text_input_v1` protocol is required for Fcitx5. Hyprland, KWin, and Weston support this protocol.

#### For Touchpad Navigation

```bash
--enable-features=TouchpadOverscrollHistoryNavigation
```

### Complete Example Configuration

`~/.config/chromium-flags.conf`:

```bash
--ozone-platform-hint=auto
--enable-features=TouchpadOverscrollHistoryNavigation
--enable-features=WaylandWindowDecorations
```

---

## VS Code and Electron Apps

### Electron Wayland Support Overview

Electron apps inherit Chromium's Ozone platform support. Native Wayland support varies by Electron version:

- **Electron 28+**: Environment variable `ELECTRON_OZONE_PLATFORM_HINT` supported
- **Electron 38+**: `--ozone-platform-hint=auto` flag no longer works, must use explicit flags
- **Electron 17+**: `--enable-features=WaylandWindowDecorations` for proper window decorations

### Global Configuration for All Electron Apps

#### Method 1: Environment Variable (Electron 28-37)

Add to your shell profile (`~/.zshrc`, `~/.bashrc`) or Hyprland config:

```bash
export ELECTRON_OZONE_PLATFORM_HINT=auto
```

**Important Notes:**
- Supported in Electron versions 28-37
- Has lower priority than command-line flags
- Planned for deprecation as `auto` behavior becomes default
- Equivalent to checking `XDG_SESSION_TYPE` environment variable

#### Method 2: Electron Flags Configuration (Arch Linux)

The Electron package on Arch Linux reads flags from configuration files:

1. Version-specific: `~/.config/electron{VERSION}-flags.conf` (e.g., `electron28-flags.conf`)
2. Fallback: `~/.config/electron-flags.conf`

**Example `~/.config/electron-flags.conf`:**

```bash
--ozone-platform-hint=auto
--enable-features=WaylandWindowDecorations
```

### VS Code Specific Configuration

VS Code cannot use application-configurable arguments because Ozone platform initialization occurs before VS Code's entry point, and the packaged install doesn't use system Electron.

#### Method 1: Desktop File Modification (Recommended)

Copy and edit the VS Code desktop file:

```bash
cp /usr/share/applications/code.desktop ~/.local/share/applications/
```

Edit `~/.local/share/applications/code.desktop`:

```desktop
Exec=/usr/bin/code --enable-features=UseOzonePlatform --ozone-platform=wayland --enable-features=WaylandWindowDecorations %F
```

For Electron 38+ (VS Code 1.94+):

```desktop
Exec=/usr/bin/code --ozone-platform=wayland --enable-features=WaylandWindowDecorations %F
```

#### Method 2: Wrapper Script

Create `~/bin/code-wayland`:

```bash
#!/bin/bash
exec /usr/bin/code --ozone-platform=wayland --enable-features=WaylandWindowDecorations "$@"
```

Make executable:

```bash
chmod +x ~/bin/code-wayland
```

#### Method 3: Shell Alias

Add to `~/.zshrc` or `~/.bashrc`:

```bash
alias code='code --ozone-platform=wayland --enable-features=WaylandWindowDecorations'
```

### Other Common Electron Apps

The same methods apply to other Electron applications:

- **Slack**: `~/.config/slack-flags.conf`
- **Discord**: `~/.config/discord-flags.conf`
- **Obsidian**: `~/.config/obsidian-flags.conf`
- **Notion**: Desktop file or wrapper script

**Generic flags for Electron apps:**

```bash
--ozone-platform=wayland
--enable-features=WaylandWindowDecorations
```

### Input Method Support (Chinese/Asian Languages)

For IME support in Electron apps, add:

```bash
--enable-wayland-ime
--wayland-text-input-version=3
```

This requires compositor support for the `text_input_v1` or `text_input_v3` Wayland protocol (Hyprland supports both).

---

## Environment Variables

### Setting Environment Variables in Hyprland

Hyprland reads environment variables from `~/.config/hypr/hyprland.conf`. Use the `env` keyword:

```bash
env = ELECTRON_OZONE_PLATFORM_HINT,auto
```

**Important for UWSM Users:**

If using UWSM (Universal Wayland Session Manager), **do not** place environment variables in `hyprland.conf`. Instead use:

- `~/.config/uwsm/env` - For theming, xcursor, Nvidia, and toolkit variables
- `~/.config/uwsm/env-hyprland` - For `HYPR*` and `AQ_*` variables

Format: `export KEY=VAL`

### Key Environment Variables for Development

**For Electron apps (v28-37):**
```bash
env = ELECTRON_OZONE_PLATFORM_HINT,auto
```

**For Qt applications:**
```bash
env = QT_QPA_PLATFORM,wayland
```

**For GTK applications:**
```bash
env = GDK_BACKEND,wayland
```

**For SDL2 applications:**
```bash
env = SDL_VIDEODRIVER,wayland
```

**For XDG Desktop Portal:**
```bash
env = XDG_CURRENT_DESKTOP,Hyprland
env = XDG_SESSION_TYPE,wayland
env = XDG_SESSION_DESKTOP,Hyprland
```

### Complete Hyprland Environment Configuration

`~/.config/hypr/hyprland.conf`:

```bash
# Wayland backend for toolkits
env = GDK_BACKEND,wayland,x11
env = QT_QPA_PLATFORM,wayland;xcb
env = SDL_VIDEODRIVER,wayland
env = CLUTTER_BACKEND,wayland

# XDG specifications
env = XDG_CURRENT_DESKTOP,Hyprland
env = XDG_SESSION_TYPE,wayland
env = XDG_SESSION_DESKTOP,Hyprland

# Electron apps (optional, v28-37 only)
env = ELECTRON_OZONE_PLATFORM_HINT,auto
```

---

## Screen Sharing and Portals

### Overview

Screen sharing on Wayland requires three components working together:

1. **xdg-desktop-portal** - Forwards requests to backend implementations
2. **Backend implementation** - Compositor-specific portal backend
3. **PipeWire** - Media streaming framework

### Required Packages

Install on Arch Linux:

```bash
sudo pacman -S xdg-desktop-portal-hyprland pipewire wireplumber
```

### How It Works

Unlike X11, Wayland applications cannot directly capture screens due to security model. Instead:

1. Application requests screen sharing via xdg-desktop-portal
2. Portal shows a dialog for user to select window/screen
3. Selected content is streamed via PipeWire
4. Application receives PipeWire stream

### Chrome/Chromium WebRTC Support

**Status:** Chrome/Chromium enable WebRTC screen capture over PipeWire by default. No additional configuration needed.

**Verification:** Test at https://mozilla.github.io/webrtc-landing/gum_test.html

### Electron WebRTC Support

**Status:** Electron enables WebRTC screen capture over PipeWire by default. The capture is based on xdg-desktop-portal.

**Supported since:** Electron 17+

### Hyprland-Specific Configuration

Hyprland wiki recommends:

```bash
# In ~/.config/hypr/hyprland.conf
exec-once = dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP
```

This ensures portal services have correct environment variables.

### Troubleshooting Screen Sharing

**Problem:** Screen sharing doesn't work

**Solutions:**

1. Verify xdg-desktop-portal-hyprland is running:
   ```bash
   systemctl --user status xdg-desktop-portal-hyprland
   ```

2. Check PipeWire is running:
   ```bash
   systemctl --user status pipewire pipewire-pulse wireplumber
   ```

3. Restart portal services:
   ```bash
   systemctl --user restart xdg-desktop-portal-hyprland xdg-desktop-portal
   ```

4. Check logs:
   ```bash
   journalctl --user -u xdg-desktop-portal-hyprland -f
   ```

---

## Verification

### Verify Chrome/Chromium is Using Wayland

1. Open Chrome/Chromium
2. Navigate to `chrome://gpu`
3. Look for "Ozone platform" - should show `wayland`
4. Check "GL_RENDERER" - should not mention XWayland

Alternative terminal check:

```bash
ps aux | grep chromium | grep wayland
```

Should see `--ozone-platform=wayland` in process arguments.

### Verify VS Code is Using Wayland

Check process arguments:

```bash
ps aux | grep code | grep wayland
```

Should see `--ozone-platform=wayland` or similar flags.

Alternative: Look for XWayland processes - if VS Code is under Wayland, it won't spawn XWayland windows.

### Verify Electron Apps are Using Wayland

Generic verification for any Electron app:

```bash
ps aux | grep <app-name> | grep wayland
```

### Check Session Type

Confirm you're running a Wayland session:

```bash
echo $XDG_SESSION_TYPE
# Should output: wayland

echo $WAYLAND_DISPLAY
# Should output: wayland-0 or wayland-1
```

### Visual Indicators

Applications running under Wayland typically exhibit:

- **Sharper rendering** - Especially noticeable on HiDPI displays
- **Smooth scrolling** - Better frame pacing
- **Proper touchpad gestures** - Three-finger swipe, pinch-to-zoom
- **Correct window decorations** - If using `WaylandWindowDecorations` feature

---

## Troubleshooting

### Issue: App Still Using XWayland

**Symptoms:**
- App appears in `xlsclients` output
- Blurry text on HiDPI displays
- Screen sharing doesn't work

**Solutions:**

1. Verify flags are being read:
   ```bash
   # For Chrome
   cat ~/.config/chromium-flags.conf

   # For Electron
   cat ~/.config/electron-flags.conf
   ```

2. Check environment variables:
   ```bash
   echo $ELECTRON_OZONE_PLATFORM_HINT
   # Should output: auto or wayland
   ```

3. Verify Electron version supports flags:
   ```bash
   # For VS Code
   code --version

   # Check if it's Electron 28+
   ```

4. Try explicit `--ozone-platform=wayland` instead of `auto`

5. Restart application completely (don't just reload window)

### Issue: Missing Window Decorations

**Symptoms:**
- No title bar
- Can't move/resize window
- Missing minimize/maximize/close buttons

**Solution:**

Add `--enable-features=WaylandWindowDecorations` flag:

```bash
--ozone-platform=wayland --enable-features=WaylandWindowDecorations
```

**Note:** Supported since Electron 17+. Particularly important for GNOME but useful on all Wayland compositors.

### Issue: Input Method (IME) Not Working

**Symptoms:**
- Can't type Chinese/Japanese/Korean characters
- IME popup doesn't appear

**Solution:**

Add IME flags:

```bash
--enable-wayland-ime --wayland-text-input-version=3
```

Verify compositor supports `text_input_v1` or `text_input_v3` protocol:

```bash
# Hyprland supports both protocols
hyprctl version
```

### Issue: Screen Sharing Not Working

**Symptoms:**
- "Share screen" button does nothing
- No screen picker dialog appears
- WebRTC test fails

**Solutions:**

1. Install required packages:
   ```bash
   sudo pacman -S xdg-desktop-portal-hyprland pipewire wireplumber
   ```

2. Restart portal services:
   ```bash
   systemctl --user restart xdg-desktop-portal-hyprland
   systemctl --user restart pipewire wireplumber
   ```

3. Check portal backend is correct:
   ```bash
   systemctl --user status xdg-desktop-portal-hyprland
   ```

4. Verify environment variables in portal service:
   ```bash
   # Should be set in ~/.config/hypr/hyprland.conf
   exec-once = dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP
   ```

### Issue: Performance Problems

**Symptoms:**
- Laggy scrolling
- High CPU usage
- Stuttering animations

**Solutions:**

1. Verify hardware acceleration is enabled:
   - Chrome: `chrome://gpu` - Check "Graphics Feature Status"
   - Should see "Hardware accelerated" for most features

2. Check compositor performance:
   ```bash
   # Monitor Hyprland performance
   hyprctl monitors
   ```

3. Disable problematic features temporarily:
   - Remove `TouchpadOverscrollHistoryNavigation` if causing issues
   - Try without `WaylandWindowDecorations` on lower-end hardware

### Issue: App Won't Start with Wayland Flags

**Symptoms:**
- App crashes immediately
- Error message about Ozone platform
- Falls back to X11

**Solutions:**

1. Check Electron version compatibility:
   - Electron 28+ required for `ELECTRON_OZONE_PLATFORM_HINT`
   - Electron 17+ required for `WaylandWindowDecorations`

2. Try different flag combinations:
   ```bash
   # Try minimal flags first
   --ozone-platform=wayland

   # Then add features incrementally
   --ozone-platform=wayland --enable-features=WaylandWindowDecorations
   ```

3. Check for conflicting flags in multiple config files

4. Verify Wayland session is running:
   ```bash
   echo $XDG_SESSION_TYPE  # Should be: wayland
   ```

---

## References

### Official Documentation

1. **Chromium Ozone Platform Documentation**
   https://chromium.googlesource.com/chromium/src/+/HEAD/docs/ozone_overview.md
   Official Chromium documentation on the Ozone platform abstraction layer and Wayland support.

2. **Chromium Configuration Documentation**
   https://chromium.googlesource.com/chromium/src/+/main/docs/configuration.md
   Official guide to Chromium features, flags, and configuration options.

3. **Electron Environment Variables**
   https://www.electronjs.org/docs/latest/api/environment-variables
   Official Electron documentation on environment variables (note: specific Wayland vars may require checking GitHub issues/PRs).

4. **Electron ELECTRON_OZONE_PLATFORM_HINT Pull Request**
   https://github.com/electron/electron/pull/39792
   Official PR adding `ELECTRON_OZONE_PLATFORM_HINT` support to Electron.

5. **Hyprland Wiki - Master Tutorial**
   https://wiki.hypr.land/Getting-Started/Master-Tutorial/#force-apps-to-use-wayland
   Official Hyprland documentation on forcing apps to use Wayland.

6. **Hyprland Wiki - Environment Variables**
   https://wiki.hypr.land/Configuring/Environment-variables/
   Official guide to setting environment variables in Hyprland configuration.

7. **Hyprland Wiki - Screen Sharing**
   https://wiki.hypr.land/Useful-Utilities/Screen-Sharing/
   Official documentation on screen sharing setup with xdg-desktop-portal.

8. **Arch Wiki - Wayland**
   https://wiki.archlinux.org/title/Wayland
   Comprehensive Arch Linux wiki page covering Wayland support, including Electron apps section.

9. **Arch Wiki - Chromium**
   https://wiki.archlinux.org/title/Chromium
   Arch-specific documentation for Chromium configuration, including Wayland support.

10. **Arch Wiki - Visual Studio Code**
    https://wiki.archlinux.org/title/Visual_Studio_Code
    Arch-specific documentation for VS Code configuration.

11. **Arch Wiki - XDG Desktop Portal**
    https://wiki.archlinux.org/title/XDG_Desktop_Portal
    Documentation on xdg-desktop-portal setup and backend configuration.

### Community Resources and Technical Details

12. **Chrome/Chromium on Wayland: The Waylandification Project**
    https://blogs.igalia.com/msisov/chrome-on-wayland-waylandification-project/
    Technical blog from Igalia (the team developing Wayland support in Chromium) on implementation details.

13. **VS Code Enable Native Wayland Support GitHub Gist**
    https://gist.github.com/qguv/e592dbeaeebc4ee7791d2ae8cfa7ef14
    Community guide for enabling Wayland in VS Code.

14. **VS Code Wayland Support Pull Request #135191**
    https://github.com/microsoft/vscode/pull/135191
    Official VS Code PR adding Electron flags for Wayland support.

15. **VS Code Issue #134612 - Add Wayland Electron Arguments**
    https://github.com/microsoft/vscode/issues/134612
    Issue discussion on Wayland support in VS Code.

16. **Electron Issue #33810 - ozone-platform-hint Flag Ignored**
    https://github.com/electron/electron/issues/33810
    Bug report and discussion on Electron Wayland flags behavior.

17. **Electron Deprecation Issue #48001 - ELECTRON_OZONE_PLATFORM_HINT**
    https://github.com/electron/electron/issues/48001
    Discussion on deprecating the environment variable as auto becomes default.

18. **Stack Overflow - Globally Set Electron Apps to Use Wayland**
    https://unix.stackexchange.com/questions/736187/how-to-globally-set-all-electron-apps-to-have-enable-features-useozoneplatform
    Community Q&A on configuring Electron apps system-wide.

19. **Stack Overflow - How to Run Electron Apps Like Slack on Wayland**
    https://stackoverflow.com/questions/63187542/how-to-run-electron-apps-like-slack-etc-for-wayland
    Practical guide for configuring various Electron applications.

20. **Chromium Debian Forum - Wayland Native Support**
    https://forums.debian.net/viewtopic.php?t=150596
    Community discussion on enabling Chromium Wayland support.

21. **Ask Ubuntu - Create .config Files for Electron Apps in Wayland**
    https://askubuntu.com/questions/1448683/how-to-properly-create-config-files-to-launch-electron-apps-in-native-wayland
    Tutorial on configuration file setup for Electron apps.

22. **Arch Forums - Code (Electron) Issue on Wayland [Solved]**
    https://bbs.archlinux.org/viewtopic.php?id=292623
    Community troubleshooting thread with working solutions.

23. **How to Enable Wayland Screen Sharing with PipeWire**
    https://www.phoronix.com/news/Wayland-Share-HowTo-Pipe-XDG
    Technical overview of Wayland screen sharing architecture.

24. **How to Enable Screen Sharing on Wayland - Jan Grulich**
    https://jgrulich.cz/2018/07/04/how-to-enable-and-use-screen-sharing-on-wayland/
    Developer blog explaining xdg-desktop-portal screen sharing setup.

### Related Specifications

25. **Wayland Protocol - Wikipedia**
    https://en.wikipedia.org/wiki/Wayland_(protocol)
    Overview of the Wayland display server protocol.

26. **Flatpak Electron Documentation**
    https://docs.flatpak.org/en/latest/electron.html
    Flatpak documentation on Electron apps (includes Wayland configuration).

---

**Document Version:** 1.0
**Last Updated:** 2025-11-26
**Hyprland Version Target:** Current (rolling)
**Chrome Version Target:** 140+
**Electron Version Target:** 28+
**VS Code Version Target:** 1.94+ (Electron 38+)
