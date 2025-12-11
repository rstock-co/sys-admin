# hyprwhspr Configuration

**Installed:** December 11, 2025
**Purpose:** Voice dictation for Claude Code and any focused application

---

## Current Configuration

| Setting | Value |
|---------|-------|
| Backend | CPU (pywhispercpp) |
| Model | base.en (141MB, English-only) |
| Hotkey | Caps Lock (sends F13 via VIA remap) |
| Paste Mode | ctrl_shift (terminal-compatible) |
| Audio Feedback | Enabled (custom chimes in ~/.config/hyprwhspr/sounds/) |
| Waybar Integration | Disabled |
| Auto-Enter | Enabled (custom wrapper service) |

**Config file:** `~/.config/hyprwhspr/config.json`
**Model location:** `~/.local/share/pywhispercpp/models/ggml-base.en.bin`
**Service:** `systemctl --user status hyprwhspr`
**Custom sounds:** `~/.config/hyprwhspr/sounds/hyprwhspr-1.mp3` (start), `hyprwhspr-2.mp3` (stop)

---

## How to Use

1. Focus the window where you want text to appear (e.g., Claude Code input)
2. Tap **Caps Lock** (sound = recording started)
3. Speak clearly into your Fifine microphone
4. Tap **Caps Lock** again (sound = transcribing)
5. Text appears at cursor position and **Enter is pressed automatically**

**Note:** Caps Lock is remapped via VIA to send F13 on tap, Left Alt on hold. You retain Alt functionality by holding the key.

---

## Auto-Enter Feature

Automatically presses Enter after transcription completes, so dictated text is submitted immediately (useful for Claude Code input).

### How It Works

1. A wrapper service (`hyprwhspr-auto-enter`) monitors the hyprwhspr journal
2. When it sees `Progress: 100%` (transcription complete), it waits 0.25s for the paste to finish
3. Then sends Enter via `ydotool key 28:1 28:0`

### Components

| File | Purpose |
|------|---------|
| `~/.local/bin/hyprwhspr-auto-enter` | Wrapper script |
| `~/.config/systemd/user/hyprwhspr-auto-enter.service` | Systemd user service |

### Disable Auto-Enter

If you don't want Enter pressed automatically:

```bash
systemctl --user disable --now hyprwhspr-auto-enter
```

### Re-enable Auto-Enter

```bash
systemctl --user enable --now hyprwhspr-auto-enter
```

### Adjust Timing

Edit the delay in `~/.local/bin/hyprwhspr-auto-enter`:

```bash
DELAY_AFTER_PASTE=0.25  # seconds to wait after transcription before Enter
```

Then restart: `systemctl --user restart hyprwhspr-auto-enter`

---

## Upgrading Models for Better Accuracy

If `base.en` accuracy isn't sufficient, upgrade to a larger model:

### Available English Models

| Model | Size | Accuracy | Speed |
|-------|------|----------|-------|
| tiny.en | 75 MB | ~92% | Fastest |
| base.en | 141 MB | ~94% | Fast (current) |
| small.en | 466 MB | ~96% | Medium |
| medium.en | 1.5 GB | ~97% | Slower |

### How to Change Model

1. Edit config:
   ```bash
   vim ~/.config/hyprwhspr/config.json
   ```

2. Change the `model` value:
   ```json
   "model": "small.en"
   ```

3. Download the new model:
   ```bash
   hyprwhspr setup
   # Select option to download model when prompted
   ```

   Or manually:
   ```bash
   cd ~/.local/share/pywhispercpp/models/
   wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
   ```

4. Restart the service:
   ```bash
   systemctl --user restart hyprwhspr
   ```

---

## Troubleshooting

### Service not running
```bash
systemctl --user status hyprwhspr
systemctl --user restart hyprwhspr
```

### Check logs
```bash
journalctl --user -u hyprwhspr -f
```

### Hotkey not working
Ensure service is running and you've logged out/in after setup.

### Text not appearing
- Check that `ydotool` service is running:
  ```bash
  systemctl --user status ydotool
  ```
- Verify `/dev/uinput` permissions:
  ```bash
  ls -la /dev/uinput
  # Should be: crw-rw---- root input
  ```

### Wrong microphone
Set default source in PipeWire:
```bash
wpctl status  # Find your mic's ID
wpctl set-default <ID>
```

---

## Key Files

| Path | Purpose |
|------|---------|
| `~/.config/hyprwhspr/config.json` | Main configuration |
| `~/.local/share/pywhispercpp/models/` | Whisper model files |
| `~/.local/share/hyprwhspr/venv/` | Python virtual environment |
| `/etc/udev/rules.d/80-uinput.rules` | ydotool permissions |
| `/etc/modules-load.d/uinput.conf` | Load uinput module at boot |
| `~/.local/bin/hyprwhspr-auto-enter` | Auto-Enter wrapper script |
| `~/.config/systemd/user/hyprwhspr-auto-enter.service` | Auto-Enter systemd service |

---

## Useful Commands

```bash
# Check service status
systemctl --user status hyprwhspr

# Restart after config changes
systemctl --user restart hyprwhspr

# View real-time logs
journalctl --user -u hyprwhspr -f

# Re-run setup wizard
hyprwhspr setup

# Check current default microphone
wpctl status | grep -A5 "Sources:"

# Check auto-enter service
systemctl --user status hyprwhspr-auto-enter

# View auto-enter logs
journalctl --user -u hyprwhspr-auto-enter -f
```
