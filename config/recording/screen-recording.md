# Screen Recording & Frame Viewing

Tools for recording the TV monitor and viewing extracted frames.

---

## Monitor Layout

| Monitor | Resolution | Position | Description |
|---------|-----------|----------|-------------|
| DP-1 | 3840x2160 | 5136,0 | Samsung (right) |
| DP-2 | 3840x2160 | 1296,612 | Beyond TV (center) |
| DP-3 | 3840x2160 | 0,0 | Samsung (left) |

---

## Recording with wf-recorder

### Aliases

| Alias | Description |
|-------|-------------|
| `rec-tv` | Record left half of TV (1920x2160) |
| `rec-tv filename.mp4` | Record to specific file |
| `rec-stop` | Stop recording (sends SIGINT) |

### Usage

```bash
# Start recording (auto-timestamped filename)
rec-tv

# Start recording to specific file
rec-tv ~/Videos/my-recording.mp4

# Stop recording
rec-stop
# or press Ctrl+C in the recording terminal
```

### Raw Command

```bash
wf-recorder -g "1296,612 1920x2160" -f ~/Videos/output.mp4
```

**Geometry breakdown:**
- `1296,612` = TV position (x,y)
- `1920x2160` = Left half width x full height

### Recording Other Regions

| Region | Geometry |
|--------|----------|
| TV full | `"1296,612 3840x2160"` |
| TV left half | `"1296,612 1920x2160"` |
| TV right half | `"3216,612 1920x2160"` |

---

## Extracting Frames with ffmpeg

```bash
# Extract all frames (1 per frame)
ffmpeg -i video.mp4 -vsync vfr frame_%04d.png

# Extract at 1fps
ffmpeg -i video.mp4 -vf fps=1 frame_%04d.png

# Extract at specific interval (every 2 seconds)
ffmpeg -i video.mp4 -vf fps=0.5 frame_%04d.png
```

---

## Viewing Frames with swayimg

### Aliases

| Alias | Description |
|-------|-------------|
| `frames` | View frames in current directory |
| `frames /path/to/dir` | View frames in specified directory |

### Keybindings

| Key | Action |
|-----|--------|
| `Page Down` / `Space` | Next image |
| `Page Up` | Previous image |
| `Home` | First image |
| `End` | Last image |
| `i` | Toggle info overlay (filename, index) |
| `+` / `-` | Zoom in/out |
| `0` | Reset zoom |
| `s` | Start/stop slideshow |
| `q` | Quit |

### Config

Info overlay enabled by default in `~/.config/swayimg/config`:

```ini
[info]
show = yes
info_timeout = 0

[info.viewer]
top_left = +name,+index
```

---

## Complete Workflow Example

```bash
# 1. Record the left half of TV
rec-tv ~/Videos/facilpay-scroll.mp4

# 2. Stop recording when done
rec-stop

# 3. Extract frames
mkdir /tmp/frames
ffmpeg -i ~/Videos/facilpay-scroll.mp4 -vsync vfr /tmp/frames/frame_%04d.png

# 4. View frames
frames /tmp/frames
```

---

## Dependencies

- `wf-recorder` - Wayland screen recorder
- `swayimg` - Wayland image viewer
- `ffmpeg` - Frame extraction

Install:
```bash
sudo pacman -S wf-recorder swayimg ffmpeg
```
