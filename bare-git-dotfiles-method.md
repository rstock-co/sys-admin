# Bare Git Repository Method for Dotfiles
**For Future Agent Reference**

---

## The Problem

You want to version control your dotfiles (`.zshrc`, `.config/hypr/`, etc.) but they need to stay in their normal locations (`~/`). You can't just do `git init ~` because that would make your entire home directory a git repo (nightmare - every file would be tracked).

---

## The Solution

**Split git into two pieces:**
1. **Git's database** (`.git` folder) → Store in `~/.dotfiles/` (bare repo)
2. **Your actual files** (working tree) → Stay in `~/` where they belong

---

## Normal Git vs Bare Repo

### Normal Git Repository:
```
~/project/
├── .git/           ← Git's database
├── file1.txt       ← Your files (working tree)
└── file2.txt
```
Everything is in one place.

### Bare Repository for Dotfiles:
```
~/.dotfiles/        ← Git's database ONLY (bare = no working tree inside)
~/                  ← Your files stay here in their normal locations
├── .zshrc
├── .config/hypr/hyprland.conf
├── SYSTEM_SETUP.md
└── etc...
```
Database and files are separated.

---

## How It Works

### The Magic Alias

```bash
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
```

This alias tells git:
- **`--git-dir=$HOME/.dotfiles/`** - Git's database is stored here
- **`--work-tree=$HOME`** - The actual files live in home directory

Now when you type `dotfiles status`, git looks for tracked files in `~/` but stores all git data in `~/.dotfiles/`.

---

## Initial Setup (From Scratch)

### Step 1: Create the bare repository
```bash
git init --bare $HOME/.dotfiles
```
This creates `~/.dotfiles/` containing only git internals (no working tree).

### Step 2: Create the alias
```bash
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
```

### Step 3: Hide untracked files
```bash
dotfiles config --local status.showUntrackedFiles no
```
This is **critical**! Without this, `dotfiles status` would show every file in your home directory. With this setting, only files you explicitly add will be tracked.

### Step 4: Add the alias to your shell config
```bash
echo "alias dotfiles='/usr/bin/git --git-dir=\$HOME/.dotfiles/ --work-tree=\$HOME'" >> ~/.zshrc
```

### Step 5: Start tracking files
```bash
dotfiles add .zshrc
dotfiles add .config/hypr/hyprland.conf
dotfiles add SYSTEM_SETUP.md
dotfiles commit -m "Initial commit"
```

### Step 6: Connect to remote and push
```bash
dotfiles remote add origin <your-github-repo-url>
dotfiles branch -M main
dotfiles push -u origin main
```

---

## Daily Usage

Instead of `git`, use the `dotfiles` alias for everything:

| Normal Git Command | Bare Repo Command | What It Does |
|-------------------|-------------------|--------------|
| `git status` | `dotfiles status` | Check tracked files |
| `git add .zshrc` | `dotfiles add .zshrc` | Track a new file |
| `git commit -m "msg"` | `dotfiles commit -m "msg"` | Commit changes |
| `git push` | `dotfiles push` | Push to GitHub |
| `git pull` | `dotfiles pull` | Pull from GitHub |
| `git log` | `dotfiles log` | View history |

**Example workflow:**
```bash
# Edit your hyprland config
vim ~/.config/hypr/hyprland.conf

# Check what changed
dotfiles status
dotfiles diff

# Commit the change
dotfiles add .config/hypr/hyprland.conf
dotfiles commit -m "Update hyprland transparency settings"
dotfiles push
```

---

## Restoring on a New Machine

### Step 1: Clone the bare repository
```bash
git clone --bare <your-github-repo-url> $HOME/.dotfiles
```

### Step 2: Create the alias (temporarily)
```bash
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
```

### Step 3: Checkout the files
```bash
dotfiles checkout
```

This will place all your dotfiles in their proper locations in `~/`.

**Note:** If you get conflicts (files already exist), you can:
```bash
# Backup existing files
mkdir -p ~/.dotfiles-backup
dotfiles checkout 2>&1 | grep -E "\s+\." | awk '{print $1}' | xargs -I{} mv {} ~/.dotfiles-backup/{}

# Then checkout again
dotfiles checkout
```

### Step 4: Hide untracked files
```bash
dotfiles config --local status.showUntrackedFiles no
```

### Step 5: Make alias permanent
The alias is now in your `.zshrc` (which was just checked out), so reload it:
```bash
source ~/.zshrc
```

---

## Best Practices

### 1. **What to Track**
✅ **DO track:**
- Shell configs: `.zshrc`, `.bashrc`
- App configs: `.config/hypr/`, `.config/alacritty/`, etc.
- Documentation: `SYSTEM_SETUP.md`
- Scripts: Custom scripts in `~/scripts/` or `~/.local/bin/`

❌ **DON'T track:**
- Secrets: `.ssh/`, `.gnupg/`, API keys
- Cache: `.cache/`
- Generated files: `.zsh_history`
- Large binaries

### 2. **Use .gitignore**
Create `~/.gitignore_global`:
```gitignore
.ssh/
.gnupg/
*.log
.DS_Store
```

Then:
```bash
dotfiles config --local core.excludesfile ~/.gitignore_global
```

### 3. **Branch Strategy**
Use branches for different machines:
```bash
# On work laptop
dotfiles checkout -b work-laptop

# On home desktop
dotfiles checkout -b home-desktop
```

Merge common changes to `main`, keep machine-specific stuff in branches.

---

## Why This Method is Best for Agents

1. **No extra tools** - Only git (universally available)
2. **Simple commands** - Just git with an alias
3. **Transparent** - Agent sees exactly what's happening (no magic)
4. **Standard git workflow** - Agent can use existing git knowledge
5. **Easy debugging** - If something breaks, it's just git
6. **Zero abstraction** - No layers between agent and version control

---

## Troubleshooting

### "I see all my home directory files in status"
```bash
dotfiles config --local status.showUntrackedFiles no
```

### "Checkout fails with conflicts"
Back up conflicting files first:
```bash
mkdir -p ~/.dotfiles-backup
# Move conflicting files to backup, then checkout again
```

### "I forgot the alias"
```bash
/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME status
```
Or add it back to your shell config.

### "I accidentally tracked too many files"
```bash
dotfiles rm --cached <file>  # Untrack but keep file
dotfiles commit -m "Untrack file"
```

---

## Quick Reference

### Setup Commands
```bash
# Initialize
git init --bare $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no

# Track files
dotfiles add <file>
dotfiles commit -m "message"
dotfiles push
```

### Clone to New Machine
```bash
git clone --bare <repo-url> $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dotfiles checkout
dotfiles config --local status.showUntrackedFiles no
```

---

## Sources & Further Reading

- [Atlassian Official Tutorial](https://www.atlassian.com/git/tutorials/dotfiles)
- [Ackama Detailed Explanation](https://www.ackama.com/what-we-think/the-best-way-to-store-your-dotfiles-a-bare-git-repository-explained/)
- [Arch Wiki - Dotfiles](https://wiki.archlinux.org/title/Dotfiles)
- [Stegosaurus Dormant Guide](https://stegosaurusdormant.com/bare-git-repo/)

---

## Agent Implementation Notes

When building an autonomous agent for dotfile management:

1. **Always use the `dotfiles` alias** - Never use bare `git` commands for dotfile operations
2. **Check alias exists** - Verify `dotfiles` command works before operations
3. **Confirm status.showUntrackedFiles is false** - Prevents noise in status output
4. **Track changes automatically** - After modifying configs, add/commit/push
5. **Pull before modifications** - Ensure latest configs before making changes
6. **Use descriptive commit messages** - Include what changed and why
7. **Handle conflicts gracefully** - On checkout failures, backup and retry

### Example Agent Workflow:
```bash
# Before making changes
dotfiles pull

# Make modifications to config
# ... agent edits ~/.config/hypr/hyprland.conf ...

# Track and commit
dotfiles add .config/hypr/hyprland.conf
dotfiles commit -m "Agent: Updated hyprland transparency to 0.85"
dotfiles push

# Verify
dotfiles status
```
