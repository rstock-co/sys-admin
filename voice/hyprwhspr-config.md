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
| Improve Mode | Available (toggle with Super+Alt+I) |

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

## Improve Mode (AI Text Cleanup)

Improve Mode sends your dictation through an LLM (via OpenRouter) to clean up verbal garbage before submitting. This removes filler words, hedging phrases, false starts, and other speech artifacts while preserving your intended message.

### How It Works

1. **Toggle ON:** Press `Super+Alt+I` (ascending chime plays)
2. **Dictate:** Use Caps Lock as normal
3. **Processing flow:**
   - hyprwhspr transcribes and pastes your raw dictation
   - Auto-enter script detects transcription complete
   - Script grabs text from clipboard, sends to OpenRouter API
   - LLM cleans up the text (removes fillers, hedging, false starts)
   - Script clears the input field with Ctrl+U
   - Script pastes the improved text
   - Script presses Enter
4. **Toggle OFF:** Press `Super+Alt+I` again (descending chime plays)

### What Gets Cleaned Up

The LLM removes:
- **Fillers:** um, uh, like, you know, basically, I mean, kind of, sort of, actually, literally
- **Hedging openers:** "yeah so", "I think maybe", "I'm not sure but", "so basically"
- **Redundant hedging:** "potentially maybe" → "maybe", "possibly perhaps" → "perhaps"
- **False starts:** "I was going to— I went to the store" → "I went to the store"
- **Repeated words:** "the the" → "the"

It also fixes punctuation while preserving your core message.

### Example

**You say:** "Yeah, so I'm not sure, but I'm thinking I could maybe make a system for Claude Code that would improve my text-to-speech prompts."

**Result:** "I want to make a system that can work with Claude Code to clean up my text-to-speech prompts."

### Components

| File | Purpose |
|------|---------|
| `~/.local/bin/hyprwhspr-improve-toggle` | Toggle script (bound to Super+Alt+I) |
| `~/.local/bin/hyprwhspr-auto-enter` | Main script (includes improve mode logic) |
| `~/.config/hyprwhspr/improve_mode` | Flag file (contains "true" or "false") |
| `~/.config/hyprwhspr/improve-mode.json` | Model configuration |
| `~/agents/sys-admin/.env.local` | OpenRouter API key |

### Configuration

**Model selection:** Edit `~/.config/hyprwhspr/improve-mode.json`:

```json
{
  "active_model": "google/gemini-2.0-flash-001",
  "models": {
    "free": [
      { "id": "meta-llama/llama-3.3-70b-instruct:free", "name": "Llama 3.3 70B", "active": false },
      { "id": "google/gemini-2.0-flash-exp:free", "name": "Gemini 2.0 Flash (1M ctx)", "active": false }
    ],
    "paid": [
      { "id": "google/gemini-2.0-flash-001", "name": "Gemini 2.0 Flash", "active": true }
    ]
  }
}
```

Change `active_model` to switch models. Free models may have rate limits. Paid models (Gemini 2.0 Flash) are fast and cheap for short dictations.

**API Key:** Stored in `~/agents/sys-admin/.env.local`:

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

### Prompt Customization

The cleanup prompt is in `~/.local/bin/hyprwhspr-auto-enter`:

```bash
CLEANUP_PROMPT='Clean this dictation. Remove:
- Fillers: um, uh, like, you know, basically, I mean, kind of, sort of, actually, literally
- Hedging openers: "yeah so", "I think maybe", "I am not sure but", "so basically"
- Redundant hedging: "potentially maybe" → "maybe", "possibly perhaps" → "perhaps"
- False starts and repeated words

Fix punctuation. Preserve the core message but cut verbal fluff. Return cleaned text only.'
```

Edit this prompt to adjust cleanup behavior. Keep it concise - free models may struggle with long prompts.

### Latency

- **Without improve mode:** ~1-3s (local Whisper transcription only)
- **With improve mode:** ~4-6s (adds OpenRouter API call)

The API call adds ~2-3 seconds. This is acceptable for most use cases but noticeable.

### Troubleshooting Improve Mode

**Check if improve mode is on:**
```bash
cat ~/.config/hyprwhspr/improve_mode
# Returns "true" or "false"
```

**View improve mode logs:**
```bash
journalctl --user -u hyprwhspr-auto-enter -f
```

Look for:
- `Improve mode ON - waiting for paste then cleaning up...`
- `Original: <your raw dictation>`
- `Improved: <cleaned up version>`
- `Clearing input...`

**Text duplicating (both original and improved appear):**
The Ctrl+U clear isn't working. This can happen intermittently. Restart the service:
```bash
systemctl --user restart hyprwhspr-auto-enter
```

**API errors:**
Check the logs for error messages. Common issues:
- Rate limiting on free models (try a different model)
- Invalid API key (check `~/agents/sys-admin/.env.local`)
- Network issues

**No sound on toggle:**
Sounds are played via `pw-play` at volume 5.0. Check:
```bash
pw-play --volume=5.0 /usr/share/sounds/freedesktop/stereo/service-login.oga
```

### Keybind Reference

| Key | Action |
|-----|--------|
| `Super+Alt+I` | Toggle improve mode on/off |
| `Caps Lock` | Start/stop dictation (unchanged) |

The keybind is defined in `~/.config/hypr/hyprland.conf`:
```
bind = $mainMod ALT, I, exec, ~/.local/bin/hyprwhspr-improve-toggle # @hotkey: Toggle Voice Improve Mode
```

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
| `~/.config/hyprwhspr/config.json` | Main hyprwhspr configuration |
| `~/.config/hyprwhspr/improve_mode` | Improve mode flag (true/false) |
| `~/.config/hyprwhspr/improve-mode.json` | Improve mode model configuration |
| `~/.local/bin/hyprwhspr-auto-enter` | Auto-enter + improve mode script |
| `~/.local/bin/hyprwhspr-improve-toggle` | Toggle improve mode on/off |
| `~/.config/systemd/user/hyprwhspr-auto-enter.service` | Auto-enter systemd service |
| `~/agents/sys-admin/.env.local` | OpenRouter API key |
| `~/.local/share/pywhispercpp/models/` | Whisper model files |
| `~/.local/share/hyprwhspr/venv/` | Python virtual environment |
| `/etc/udev/rules.d/80-uinput.rules` | ydotool permissions |
| `/etc/modules-load.d/uinput.conf` | Load uinput module at boot |

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

# View auto-enter logs (includes improve mode)
journalctl --user -u hyprwhspr-auto-enter -f

# Check improve mode status
cat ~/.config/hyprwhspr/improve_mode

# Toggle improve mode manually (or use Super+Alt+I)
~/.local/bin/hyprwhspr-improve-toggle

# Check current improve mode model
jq '.active_model' ~/.config/hyprwhspr/improve-mode.json

# Restart auto-enter after script changes
systemctl --user restart hyprwhspr-auto-enter
```
