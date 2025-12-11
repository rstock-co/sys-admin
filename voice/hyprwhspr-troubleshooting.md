# hyprwhspr Troubleshooting

## Quick Fix (Try This First)

**Symptom:** Transcription completes (Progress: 100%) but text doesn't appear, OR nothing happens when pressing Caps Lock.

**Fix:** Restart all services in order:

```bash
systemctl --user restart ydotool hyprwhspr hyprwhspr-auto-enter
```

This fixes 90% of issues after reboot or when things get stuck.

---

## Step-by-Step Troubleshooting

If the quick fix didn't work, follow these steps **in order**:

### Step 1: Check services are running

```bash
systemctl --user status ydotool hyprwhspr hyprwhspr-auto-enter
```

All three should show `active (running)`. If any failed, proceed to Step 2.

### Step 2: Check uinput module

```bash
lsmod | grep uinput
```

If no output, the module isn't loaded:

```bash
sudo modprobe uinput
sudo udevadm trigger /dev/uinput
systemctl --user restart ydotool hyprwhspr hyprwhspr-auto-enter
```

### Step 3: Check uinput permissions

```bash
ls -la /dev/uinput
```

Should show `crw-rw---- root input`. If not:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger /dev/uinput
systemctl --user restart ydotool hyprwhspr hyprwhspr-auto-enter
```

### Step 4: Test clipboard + paste manually

```bash
echo "test" | wl-copy && sleep 0.2 && ydotool key 29:1 42:1 47:1 47:0 42:0 29:0
```

If "test" appears in your focused window, the paste mechanism works. Problem is in hyprwhspr transcription.

### Step 5: Check what's on clipboard after transcription

Do a transcription, then immediately:

```bash
wl-paste
```

- If transcribed text appears → paste keystroke not reaching app
- If old/wrong text appears → transcription not reaching clipboard

---

## Specific Issues

### Caps Lock doesn't trigger recording (services failed)

**Root cause:** `uinput` kernel module not loaded.

```bash
sudo modprobe uinput
sudo udevadm trigger /dev/uinput
systemctl --user restart ydotool hyprwhspr
```

**Permanent fix** (load at boot):

```bash
echo "uinput" | sudo tee /etc/modules-load.d/uinput.conf
```

### Transcription completes but text doesn't appear

Services may be in a bad state. Restart:

```bash
systemctl --user restart hyprwhspr
```

### Permission issues (`/dev/uinput` wrong permissions)

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger /dev/uinput
```

Verify udev rule exists:

```bash
cat /etc/udev/rules.d/80-uinput.rules
# Should contain: KERNEL=="uinput", GROUP="input", MODE="0660"
```

---

## Diagnostic Commands

```bash
# Check service status
systemctl --user status hyprwhspr
systemctl --user status ydotool

# View logs
journalctl --user -u hyprwhspr -f
journalctl --user -u ydotool -f

# Check uinput permissions (should be crw-rw---- root input)
ls -la /dev/uinput

# Check if uinput module is loaded
lsmod | grep uinput

# Check group membership
groups | grep input

# Test ydotoold manually
/usr/bin/ydotoold
```

---

## Permission Issues

If `/dev/uinput` has wrong permissions (`crw-------` instead of `crw-rw----`):

```bash
# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger /dev/uinput

# Verify udev rule exists
cat /etc/udev/rules.d/80-uinput.rules
# Should contain: KERNEL=="uinput", GROUP="input", MODE="0660"
```

---

## Auto-Enter Not Working

**Symptom:** Text pastes but Enter is not pressed automatically.

### Check the service

```bash
systemctl --user status hyprwhspr-auto-enter
```

If not running:

```bash
systemctl --user restart hyprwhspr-auto-enter
```

### Check logs

```bash
journalctl --user -u hyprwhspr-auto-enter --since "5 min ago"
```

Should show "Transcription complete" and "Enter sent" after each dictation.

### Verify ydotool works

```bash
ydotool key 28:1 28:0  # Should press Enter
```

### Re-enable if disabled

```bash
systemctl --user enable --now hyprwhspr-auto-enter
```
