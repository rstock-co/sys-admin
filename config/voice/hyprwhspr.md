# Voice Dictation (hyprwhspr)

## Quick Fix

```bash
fix-voice
```

Restarts all voice services. Fixes 90% of issues.

---

## Current Setup

| Setting | Value |
|---------|-------|
| Backend | CPU (pywhispercpp) |
| Model | base.en (141MB, English-only) |
| Hotkey | Caps Lock (sends F13 via VIA remap) |
| Paste Mode | ctrl_shift (terminal-compatible) |
| Audio Feedback | Custom chimes |
| Auto-Enter | Enabled |
| Voice Modes | Clarify (Super+Alt+C), Enhance (Super+Alt+E) |

---

## System Paths

| File | Purpose |
|------|---------|
| `~/.config/hyprwhspr/config.json` | Main config |
| `~/.config/hyprwhspr/voice_mode` | Mode state (off/clarify/enhance) |
| `~/.config/hyprwhspr/sounds/` | Custom chime sounds |
| `~/.local/bin/hyprwhspr-auto-enter` | Auto-enter + voice mode script |
| `~/.local/bin/hyprwhspr-mode-toggle` | Mode toggle script |
| `~/.local/share/pywhispercpp/models/` | Whisper models |
| `~/agents/sys-admin/.env.local` | OpenRouter API key |

---

## How to Use

1. Focus window where you want text
2. Tap **Caps Lock** (chime = recording)
3. Speak into Fifine microphone
4. Tap **Caps Lock** again (chime = transcribing)
5. Text appears and Enter is pressed automatically

**Note:** Caps Lock is remapped via VIA to send F13 on tap, Left Alt on hold.

---

## Voice Modes

| Mode | Hotkey | Purpose |
|------|--------|---------|
| **Clarify** | Super+Alt+C | Remove fillers, hedging, false starts |
| **Enhance** | Super+Alt+E | Make prompt clearer and more actionable |

Modes are mutually exclusive. Toggle on/off with same hotkey.

**Check current mode:**
```bash
cat ~/.config/hyprwhspr/voice_mode
```

**View processing logs:**
```bash
journalctl --user -u hyprwhspr-auto-enter -f
```

---

## Troubleshooting

### Quick Fix didn't work

**Step 1:** Check services
```bash
systemctl --user status ydotool hyprwhspr hyprwhspr-auto-enter
```

**Step 2:** Check uinput module
```bash
lsmod | grep uinput
# If empty:
sudo modprobe uinput
sudo udevadm trigger /dev/uinput
fix-voice
```

**Step 3:** Check uinput permissions
```bash
ls -la /dev/uinput
# Should be: crw-rw---- root input
```

**Step 4:** Test paste manually
```bash
echo "test" | wl-copy && sleep 0.2 && ydotool key 29:1 42:1 47:1 47:0 42:0 29:0
```

**Step 5:** Check clipboard after transcription
```bash
wl-paste
```

### Specific Issues

**Caps Lock doesn't trigger:** uinput module not loaded
```bash
sudo modprobe uinput
echo "uinput" | sudo tee /etc/modules-load.d/uinput.conf  # Permanent
```

**Text doesn't appear:** Services stuck
```bash
fix-voice
```

**Auto-Enter not working:**
```bash
systemctl --user restart hyprwhspr-auto-enter
```

**Wrong microphone:**
```bash
wpctl status  # Find mic ID
wpctl set-default <ID>
```

---

## Diagnostic Commands

```bash
# Service status
systemctl --user status hyprwhspr
systemctl --user status ydotool
systemctl --user status hyprwhspr-auto-enter

# Logs
journalctl --user -u hyprwhspr -f
journalctl --user -u hyprwhspr-auto-enter -f

# Permissions
ls -la /dev/uinput
lsmod | grep uinput
groups | grep input
```

---

## Model Upgrade

| Model | Size | Accuracy |
|-------|------|----------|
| tiny.en | 75 MB | ~92% |
| base.en | 141 MB | ~94% (current) |
| small.en | 466 MB | ~96% |
| medium.en | 1.5 GB | ~97% |

To change:
```bash
# Edit config
vim ~/.config/hyprwhspr/config.json
# Change "model": "small.en"

# Download model
cd ~/.local/share/pywhispercpp/models/
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin

# Restart
systemctl --user restart hyprwhspr
```

---

## Auto-Enter Configuration

Disable:
```bash
systemctl --user disable --now hyprwhspr-auto-enter
```

Re-enable:
```bash
systemctl --user enable --now hyprwhspr-auto-enter
```

Adjust timing (edit `~/.local/bin/hyprwhspr-auto-enter`):
```bash
DELAY_AFTER_PASTE=0.25  # seconds
```

---

## Voice Mode Configuration

Model selection (`~/.config/hyprwhspr/voice-mode.json`):
```json
{
  "active_model": "google/gemini-2.0-flash-001"
}
```

API key (`~/agents/sys-admin/.env.local`):
```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

---

## Audio Volume Settings

**Two different audio systems:**

| Sound | Tool | Config | Volume |
|-------|------|--------|--------|
| Caps Lock (start/stop) | hyprwhspr internal | `~/.config/hyprwhspr/config.json` | `20.0` (multiplier) |
| Clarify/Enhance toggle | `paplay` | `~/.local/bin/hyprwhspr-mode-toggle` | `65536` (100%) |

**Why paplay?** `pw-play` routes through application streams (affected by Spotify volume). `paplay` routes through system mixer (follows main speaker volume like caps lock sounds).

**paplay volume scale:**
- 65536 = 100%
- 131072 = 200%
- 32768 = 50%
