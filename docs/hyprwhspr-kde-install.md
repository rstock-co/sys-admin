# HyprWhisper Installation Guide for KDE Wayland

Voice-to-text dictation using OpenAI Whisper, running locally on CPU.

**Tested on:** Arch Linux + KDE Plasma (Wayland)

---

## What You Get

- Press a hotkey → speak → text appears at cursor
- Runs entirely offline (no cloud APIs for transcription)
- ~94% accuracy with base.en model

---

## Step 1: Install Dependencies

```bash
# Install from AUR
paru -S hyprwhspr ydotool

# Or with yay
yay -S hyprwhspr ydotool
```

This pulls in all required dependencies (pipewire, python packages, etc).

---

## Step 2: Set Up Permissions

HyprWhisper uses ydotool to simulate keyboard input, which requires uinput access.

```bash
# Load uinput module
sudo modprobe uinput

# Make it permanent across reboots
echo "uinput" | sudo tee /etc/modules-load.d/uinput.conf

# Add yourself to input group
sudo usermod -aG input $USER
```

**Important:** Log out and back in for the group change to take effect.

---

## Step 3: Enable Services

```bash
# Enable and start ydotool daemon
systemctl --user enable --now ydotool

# Enable and start hyprwhspr
systemctl --user enable --now hyprwhspr
```

Verify they're running:
```bash
systemctl --user status ydotool hyprwhspr
```

---

## Step 4: Configure HyprWhisper

Create the config directory and file:

```bash
mkdir -p ~/.config/hyprwhspr
```

Create `~/.config/hyprwhspr/config.json`:

```json
{
  "primary_shortcut": "F13",
  "recording_mode": "toggle",
  "model": "base.en",
  "threads": 4,
  "language": null,
  "paste_mode": "ctrl_shift",
  "transcription_backend": "cpu",
  "audio_feedback": true,
  "start_sound_volume": 20.0,
  "stop_sound_volume": 20.0
}
```

**Note:** `F13` is used because it's an unused key that won't conflict with anything. You'll map your preferred hotkey to F13 in the next step.

---

## Step 5: Set Up KDE Hotkey

### Option A: Map Caps Lock to F13 (Recommended)

This gives you a dedicated dictation key without losing Caps Lock functionality.

1. Install `keyd` (keyboard remapper):
   ```bash
   paru -S keyd
   sudo systemctl enable --now keyd
   ```

2. Create `/etc/keyd/default.conf`:
   ```ini
   [ids]
   *

   [main]
   capslock = overload(control, f13)
   ```

   This makes Caps Lock send F13 on tap, Ctrl on hold.

3. Reload keyd:
   ```bash
   sudo keyd reload
   ```

### Option B: Use KDE Custom Shortcut

1. Open **System Settings → Shortcuts → Custom Shortcuts**
2. Click **Edit → New → Global Shortcut → Send Keyboard Input**
3. Set trigger to your preferred key (e.g., `Super+V`)
4. Set action to send `F13`

### Option C: Change HyprWhisper's Hotkey Directly

Edit `~/.config/hyprwhspr/config.json` and change `primary_shortcut` to any key:

```json
"primary_shortcut": "ctrl+shift+d"
```

Then restart the service:
```bash
systemctl --user restart hyprwhspr
```

---

## Step 6: Download Whisper Model

The model downloads automatically on first use, but you can pre-download:

```bash
mkdir -p ~/.local/share/pywhispercpp/models
cd ~/.local/share/pywhispercpp/models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

**Available models:**

| Model | Size | Accuracy | Speed |
|-------|------|----------|-------|
| tiny.en | 75 MB | ~92% | Fastest |
| base.en | 141 MB | ~94% | Fast |
| small.en | 466 MB | ~96% | Medium |
| medium.en | 1.5 GB | ~97% | Slow |

---

## Step 7: Test It

1. Open any text field (terminal, browser, text editor)
2. Press your hotkey (Caps Lock or whatever you configured)
3. You should hear a chime (if audio_feedback is enabled)
4. Speak clearly
5. Press the hotkey again
6. Text should appear at your cursor

---

## Troubleshooting

### Nothing happens when I press the hotkey

Check if services are running:
```bash
systemctl --user status hyprwhspr ydotool
```

Check if uinput is loaded:
```bash
lsmod | grep uinput
```

Check if you're in the input group:
```bash
groups | grep input
```

### Text doesn't appear after transcription

Test ydotool manually:
```bash
echo "test" | wl-copy && sleep 0.2 && ydotool key 29:1 42:1 47:1 47:0 42:0 29:0
```

If nothing pastes, ydotool permissions are wrong. Re-check Step 2.

### Wrong microphone selected

```bash
# List audio devices
wpctl status

# Set default microphone (replace ID)
wpctl set-default <ID>
```

### View logs

```bash
journalctl --user -u hyprwhspr -f
```

---

## Quick Reference

```bash
# Restart everything
systemctl --user restart ydotool hyprwhspr

# Check status
systemctl --user status ydotool hyprwhspr

# View logs
journalctl --user -u hyprwhspr -f

# Check clipboard after transcription
wl-paste
```

---

## Upgrading Models

To use a more accurate (but slower) model:

1. Download the model:
   ```bash
   cd ~/.local/share/pywhispercpp/models
   wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
   ```

2. Update config:
   ```json
   "model": "small.en"
   ```

3. Restart:
   ```bash
   systemctl --user restart hyprwhspr
   ```
