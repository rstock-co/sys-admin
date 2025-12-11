# Input Navigation

Shortcuts for navigating text in the Claude Code input field.

---

## Readline Shortcuts (Default)

### Cursor Movement
| Keys | Action |
|------|--------|
| `Ctrl+A` | Jump to start of line |
| `Ctrl+E` | Jump to end of line |
| `Ctrl+←` or `Alt+B` | Jump back one word |
| `Ctrl+→` or `Alt+F` | Jump forward one word |

### Deletion
| Keys | Action |
|------|--------|
| `Ctrl+U` | Delete from cursor to start of line |
| `Ctrl+K` | Delete from cursor to end of line |
| `Ctrl+W` | Delete word before cursor |
| `Alt+D` | Delete word after cursor |

### Other
| Keys | Action |
|------|--------|
| `Ctrl+L` | Clear screen |
| `Ctrl+C` | Cancel current input |
| `Escape` ×2 | Clear entire input field |

---

## Vim Mode

Enable Vim keybindings for full modal navigation:

```bash
claude config set --global preferredVimMode enabled
```

### Mode Switching
| Keys | Action |
|------|--------|
| `Escape` | Enter normal mode |
| `i` | Insert before cursor |
| `a` | Insert after cursor |
| `I` | Insert at start of line |
| `A` | Insert at end of line |
| `o` | New line below |
| `O` | New line above |

### Navigation (Normal Mode)
| Keys | Action |
|------|--------|
| `h/j/k/l` | Left/down/up/right |
| `w` | Jump forward one word |
| `b` | Jump back one word |
| `e` | Jump to end of word |
| `0` | Jump to start of line |
| `$` | Jump to end of line |
| `gg` | Jump to top |
| `G` | Jump to bottom |

### Editing (Normal Mode)
| Keys | Action |
|------|--------|
| `x` | Delete character |
| `dw` | Delete word |
| `dd` | Delete line |
| `d$` or `D` | Delete to end of line |
| `d0` | Delete to start of line |
| `cw` | Change word (delete + insert) |
| `cc` | Change line |
| `u` | Undo |
| `Ctrl+R` | Redo |

### Disable Vim Mode

```bash
claude config set --global preferredVimMode disabled
```
