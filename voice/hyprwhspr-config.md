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
| Voice Modes | Clarify (Super+Alt+I), Enhance (Super+Alt+E) |

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

## Voice Processing Modes

Two AI-powered modes process your dictation through OpenRouter before submitting:

| Mode | Hotkey | Purpose |
|------|--------|---------|
| **Clarify** | `Super+Alt+I` | Removes verbal garbage (fillers, hedging, false starts) while preserving your exact meaning |
| **Enhance** | `Super+Alt+E` | Improves clarity and makes your prompt more actionable, may restructure for better communication |

**Modes are mutually exclusive.** Pressing a hotkey toggles that mode on. Pressing it again (or pressing the other mode's hotkey) toggles it off.

### How It Works

1. **Toggle a mode:** Press `Super+Alt+I` (clarify) or `Super+Alt+E` (enhance) - ascending chime plays
2. **Dictate:** Use Caps Lock as normal
3. **Processing flow:**
   - hyprwhspr transcribes and pastes your raw dictation
   - Auto-enter script detects transcription complete
   - Script grabs text from clipboard, sends to OpenRouter API
   - LLM processes the text based on active mode
   - Script clears the input field with Ctrl+U
   - Script pastes the processed text
   - Script presses Enter
4. **Toggle OFF:** Press the same hotkey again (descending chime plays)

### Clarify Mode (`Super+Alt+I`)

Removes verbal garbage while preserving your exact meaning. Use this for most dictation.

**What gets removed:**
- **Fillers:** um, uh, like, you know, basically, I mean, kind of, sort of, actually, literally
- **Hedging openers:** "yeah so", "I think maybe", "I'm not sure but", "so basically"
- **Redundant hedging:** "potentially maybe" → "maybe", "possibly perhaps" → "perhaps"
- **False starts:** "I was going to— I went to the store" → "I went to the store"
- **Repeated words:** "the the" → "the"

Also fixes punctuation.

**Example:**

| You say | Result |
|---------|--------|
| "Yeah, so I'm not sure, but I'm thinking I could maybe make a system for Claude Code that would improve my text-to-speech prompts." | "I want to make a system that can work with Claude Code to clean up my text-to-speech prompts." |

**Prompt (in `~/.local/bin/hyprwhspr-auto-enter`):**
```
Clean this dictation. Remove:
- Fillers: um, uh, like, you know, basically, I mean, kind of, sort of, actually, literally
- Hedging openers: "yeah so", "I think maybe", "I am not sure but", "so basically"
- Redundant hedging: "potentially maybe" → "maybe", "possibly perhaps" → "perhaps"
- False starts and repeated words

Fix punctuation. Preserve the core message but cut verbal fluff. Return cleaned text only.
```

**Temperature:** 0.1 (very deterministic)

### Enhance Mode (`Super+Alt+E`)

Makes your prompt clearer and more actionable. May restructure or expand vague inputs. Use this when you want the LLM to help you communicate better, not just clean up.

**What it does:**
- Makes input clearer and more actionable
- Adds helpful details/structure if input is vague
- Cleans up and clarifies if input is already specific (doesn't over-expand)
- Matches output scale to input (short note → clear paragraph, not massive document)
- Adds bullet points or sections only when they genuinely help
- Preserves your intent and voice

**Example:**

| You say | Result |
|---------|--------|
| "I want to like make something with agents" | "I want to build a system using AI agents. This could involve creating autonomous agents that can perform tasks, coordinate with each other, or integrate with existing tools and workflows." |

**Prompt (in `~/.local/bin/hyprwhspr-auto-enter`):**
```
You are a prompt improver. Take the user's input and make it clearer and more actionable. If the input is vague, add helpful details and structure. If the input is already specific, just clean it up and clarify—don't over-expand. Match the scale of your output to the input: a short note becomes a clear paragraph, not a massive document. Add bullet points or sections only when they genuinely help. Preserve the user's intent and voice. Output only the improved text, no preamble or meta-commentary.
```

**Temperature:** 0.6 (more creative)

### Components

| File | Purpose |
|------|---------|
| `~/.local/bin/hyprwhspr-mode-toggle` | Toggle script (takes "clarify" or "enhance" argument) |
| `~/.local/bin/hyprwhspr-auto-enter` | Main script (includes both mode prompts and logic) |
| `~/.config/hyprwhspr/voice_mode` | Mode file (contains "off", "clarify", or "enhance") |
| `~/.config/hyprwhspr/voice-mode.json` | Model configuration |
| `~/agents/sys-admin/.env.local` | OpenRouter API key |

### Configuration

**Model selection:** Edit `~/.config/hyprwhspr/voice-mode.json`:

```json
{
  "active_model": "google/gemini-2.0-flash-001",
  "models": {
    "free": [
      { "id": "meta-llama/llama-3.3-70b-instruct:free", "name": "Llama 3.3 70B" },
      { "id": "google/gemini-2.0-flash-exp:free", "name": "Gemini 2.0 Flash (1M ctx)" }
    ],
    "paid": [
      { "id": "google/gemini-2.0-flash-001", "name": "Gemini 2.0 Flash" }
    ]
  }
}
```

Change `active_model` to switch models. Both modes use the same model. Free models may have rate limits.

**API Key:** Stored in `~/agents/sys-admin/.env.local`:

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

### Latency

- **No mode:** ~1-3s (local Whisper transcription only)
- **Clarify mode:** ~4-6s (adds OpenRouter API call)
- **Enhance mode:** ~4-6s (adds OpenRouter API call, may be slightly longer for complex restructuring)

### Troubleshooting

**Check current mode:**
```bash
cat ~/.config/hyprwhspr/voice_mode
# Returns "off", "clarify", or "enhance"
```

**View processing logs:**
```bash
journalctl --user -u hyprwhspr-auto-enter -f
```

Look for:
- `Voice mode: clarify - waiting for paste then processing...`
- `Original: <your raw dictation>`
- `Processed (clarify): <cleaned up version>`
- `Clearing input...`

**Text duplicating (both original and processed appear):**
The Ctrl+U clear isn't working. Restart the service:
```bash
systemctl --user restart hyprwhspr-auto-enter
```

**API errors:**
Check logs for error messages. Common issues:
- Rate limiting on free models (switch to paid model)
- Invalid API key (check `~/agents/sys-admin/.env.local`)
- Network issues

**No sound on toggle:**
Sounds use `pw-play` at volume 5.0:
```bash
pw-play --volume=5.0 /usr/share/sounds/freedesktop/stereo/service-login.oga
```

### Keybind Reference

| Key | Action |
|-----|--------|
| `Super+Alt+I` | Toggle Clarify mode |
| `Super+Alt+E` | Toggle Enhance mode |
| `Caps Lock` | Start/stop dictation (unchanged) |

Keybinds are defined in `~/.config/hypr/hyprland.conf`:
```
bind = $mainMod ALT, I, exec, ~/.local/bin/hyprwhspr-mode-toggle clarify # @hotkey: Toggle Voice Clarify Mode
bind = $mainMod ALT, E, exec, ~/.local/bin/hyprwhspr-mode-toggle enhance # @hotkey: Toggle Voice Enhance Mode
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
| `~/.config/hyprwhspr/voice_mode` | Voice mode state (off/clarify/enhance) |
| `~/.config/hyprwhspr/voice-mode.json` | Voice mode model configuration |
| `~/.local/bin/hyprwhspr-auto-enter` | Auto-enter + voice mode processing script |
| `~/.local/bin/hyprwhspr-mode-toggle` | Toggle voice modes (clarify/enhance) |
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

# View auto-enter logs (includes voice mode processing)
journalctl --user -u hyprwhspr-auto-enter -f

# Check voice mode status
cat ~/.config/hyprwhspr/voice_mode

# Toggle modes manually (or use Super+Alt+I / Super+Alt+E)
~/.local/bin/hyprwhspr-mode-toggle clarify
~/.local/bin/hyprwhspr-mode-toggle enhance

# Check current voice mode model
jq '.active_model' ~/.config/hyprwhspr/voice-mode.json

# Restart auto-enter after script changes
systemctl --user restart hyprwhspr-auto-enter
```
