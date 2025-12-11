# hyprwhspr Troubleshooting

## Service Not Working After Reboot

**Symptom:** Caps Lock doesn't trigger recording, services failed.

**Root cause:** `uinput` kernel module not loaded.

### Quick Fix

```bash
# Load the module
sudo modprobe uinput

# Trigger udev rules
sudo udevadm trigger /dev/uinput

# Restart services
systemctl --user restart ydotool hyprwhspr

# Verify
systemctl --user status ydotool hyprwhspr
```

### Permanent Fix

Ensure uinput loads at boot:

```bash
echo "uinput" | sudo tee /etc/modules-load.d/uinput.conf
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
