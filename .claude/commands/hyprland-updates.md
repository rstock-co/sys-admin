---
argument-hint: [since-version]
description: Check Hyprland releases for breaking changes and config updates needed
---

# Hyprland Updates Command

Monitors Hyprland GitHub releases and identifies breaking changes that affect your configuration.

## Usage

```bash
/hyprland-updates [since-version]
```

**First run**: Compares installed version against latest releases
**With version**: Shows changes since specified version (e.g., `v0.50.0`)

## Context

**Hyprland is in rapid development** - every release can have breaking changes. Config syntax changes, removed options, renamed variables, and plugin ABI breaks are common. This command helps you:

1. Identify breaking changes before/after updating
2. Know which config options need migration
3. Understand when plugins need rebuilding
4. Keep documentation in sync with installed version

## Workflow

### 1. Check Current State

```bash
# Get installed version
pacman -Q hyprland

# Get available version (if update pending)
pacman -Ss ^hyprland$ | grep extra

# Check for installed plugins
hyprpm list 2>/dev/null || echo "No plugins configured"
```

### 2. Fetch GitHub Releases

Use WebFetch to get release notes:

```
WebFetch(
  url: "https://github.com/hyprwm/Hyprland/releases",
  prompt: "Extract all releases from {installed_version} to latest. For each release, extract: version number, release date, BREAKING CHANGES section (critical), new features, and fixes."
)
```

For specific release details:
```
WebFetch(
  url: "https://github.com/hyprwm/Hyprland/releases/tag/v0.52.0",
  prompt: "Extract the complete release notes, focusing on breaking changes"
)
```

### 3. Identify Config Impact

**Breaking change categories:**

| Category | Impact | Action Required |
|----------|--------|-----------------|
| Config renamed | HIGH | Update hyprland.conf |
| Config removed | HIGH | Remove from config, find alternative |
| Config syntax change | HIGH | Rewrite affected lines |
| Default changed | MEDIUM | Review behavior, update if needed |
| Deprecated | LOW | Plan migration, still works for now |
| Plugin ABI break | HIGH | Rebuild all plugins (`hyprpm update -f`) |

### 4. Cross-Reference User's Config

Read and check these files:
- `~/.config/hypr/hyprland.conf` - Main config
- `~/.config/hypr/*.conf` - Any sourced configs
- `~/SYSTEM_SETUP.md` - Documented config decisions

For each breaking change, check if the user's config uses the affected option.

### 5. Present Results

## Output Format

```
🔍 Hyprland Update Check

📦 INSTALLED VERSION: v{installed}
📦 LATEST VERSION: v{latest}
📦 VERSIONS BEHIND: {count}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 BREAKING CHANGES AFFECTING YOUR CONFIG

v{version} ({date})
━━━━━━━━━━━━━━━━━━

⚠️  {old_option} → {new_option}
    Status: USED IN YOUR CONFIG (line {N})
    Action: Replace in ~/.config/hypr/hyprland.conf

    Before: {old_syntax}
    After:  {new_syntax}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 BREAKING CHANGES (NOT AFFECTING YOU)

v{version}
• {change} - You don't use this option

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔌 PLUGIN STATUS

{Plugins installed: N / No plugins installed}
{If plugins: "REBUILD REQUIRED after update: hyprpm update -f"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 NEW FEATURES (Optional)

v{version}
• {feature} - {brief description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
• Breaking changes affecting you: {N}
• Config lines to update: {M}
• Plugins to rebuild: {P}

🔧 MIGRATION COMMANDS:

# If config changes needed:
vim ~/.config/hypr/hyprland.conf
# Make the changes listed above, then:
hyprctl reload

# If plugins installed:
hyprpm update -f

# Update documentation:
# Update SYSTEM_SETUP.md if significant changes

# Proceed with system update:
sudo pacman -Syu
```

## Data Sources

### Primary: GitHub Releases
- URL: `https://github.com/hyprwm/Hyprland/releases`
- Contains: Version numbers, release notes, breaking changes
- Format: Markdown with structured sections

### Secondary: Hyprland Wiki
- URL: `https://wiki.hypr.land/`
- Contains: Current config syntax reference
- Use: Verify correct syntax after migration

### Reference: Arch Package
- Command: `pacman -Si hyprland`
- Contains: Available version, dependencies

## Common Breaking Changes Patterns

Based on Hyprland release history:

1. **Config renames**: `misc:X` → `misc:Y` (e.g., `disable_hyprland_qtutils_check` → `disable_hyprland_guiutils_check`)
2. **Option splits**: Single option split into multiple
3. **Value changes**: Boolean → enum, string format changes
4. **Section moves**: Option moved to different config section
5. **Removal**: Option removed entirely (use alternative or remove)

## Plugin Rebuild Notes

**When to rebuild plugins:**
- After ANY Hyprland version update
- Plugin ABI is NOT stable
- Use `hyprpm update -f` to force rebuild all

**Commands:**
```bash
# List installed plugins
hyprpm list

# Update/rebuild all plugins
hyprpm update -f

# If update fails, try:
hyprpm purge-cache
hyprpm update
```

## Documentation Updates

After successful update, update these files if significant:

1. **SYSTEM_SETUP.md** - If config syntax changed significantly
2. **hyprland-docs skill** - If wiki structure changed

## Tips

- **Before updating**: Run this command first to know what's coming
- **After updating**: Run again to verify all changes applied
- **Save config backup**: `cp ~/.config/hypr/hyprland.conf ~/.config/hypr/hyprland.conf.bak`
- **Test reload**: Use `hyprctl reload` before full restart to catch errors

## Related Commands

- `/troubleshoot display` - If monitors break after update
- `/pacman` - General package management

---

**Owner**: sys-admin agent
**Data Source**: GitHub Releases API (via WebFetch)
