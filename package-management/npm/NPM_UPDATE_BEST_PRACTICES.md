# NPM Global Update Best Practices

**TL;DR:** `npm update -g` is **NOT recommended** for batch updates. Update packages individually instead.

---

## The Problem with `npm update -g`

Unlike `pacman -Syu` which is safe and recommended, `npm update -g` has several issues:

### 1. **Only Updates to "Wanted" Version (Not Latest)**

`npm update -g` respects semver ranges and only updates to the "wanted" version, not necessarily "latest."

**Example:**
```bash
npm outdated -g
# Package       Current  Wanted  Latest
# typescript    5.2.2    5.2.2   5.3.3
# tsx           3.12.7   3.12.7  4.0.0
```

`npm update -g` would do **nothing** here because:
- TypeScript 5.3.3 is a minor version bump (would update if you had `^5.0.0` in a package.json)
- tsx 4.0.0 is a major version bump (breaking changes, won't auto-update)

**But global packages don't have semver ranges!** They're installed at exact versions, so "wanted" = "current" = no updates.

### 2. **Silent Failures**

`npm update -g` may complete successfully but update nothing, giving you a false sense of security.

### 3. **No Breaking Change Protection**

For global CLI tools, you often DO want the latest version (including major bumps), but `npm update -g` won't give you that.

### 4. **Unclear What Changed**

Unlike `pacman -Syu` which shows exactly what's updating, `npm update -g` gives minimal feedback.

---

## Why `pacman -Syu` is Different

**pacman/paru batch updates are safe because:**
- ✅ Arch maintainers test compatibility
- ✅ System packages have defined dependencies
- ✅ Rolling release model = incremental updates
- ✅ Clear output showing what's changing
- ✅ Can rollback via pacman cache

**npm global updates are risky because:**
- ❌ No central authority testing compatibility
- ❌ Global packages may have conflicting dependencies
- ❌ Major version bumps can break workflows
- ❌ No easy rollback mechanism
- ❌ Tools may have breaking CLI changes

---

## Recommended Approach: Individual Updates

### Step 1: Check What's Outdated
```bash
npm outdated -g
```

**Output:**
```
Package           Current  Wanted  Latest  Location
typescript        5.2.2    5.2.2   5.3.3   global
tsx               3.12.7   3.12.7  4.0.0   global
npm-check-updates 16.0.0   16.0.0  16.14.0 global
```

### Step 2: Review Each Package

For each outdated package, consider:
- **Minor/patch updates** (5.2.2 → 5.3.3) - Usually safe
- **Major updates** (3.x → 4.x) - Read changelog first!

### Step 3: Update Individually

**Minor/patch updates (safe):**
```bash
npm install -g typescript@latest
npm install -g npm-check-updates@latest
```

**Major updates (read changelog first):**
```bash
# Check what's new
npm view tsx versions
npm view tsx@4.0.0

# Read changelog on GitHub/npm
# Then update if safe
npm install -g tsx@latest
```

### Step 4: Track Changes
```bash
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin
git add package-management/npm/npm-global.txt
git commit -m "Update npm globals: typescript 5.3.3, tsx 4.0.0, npm-check-updates 16.14.0"
git push
```

---

## When `npm update -g` Might Work

**Scenario:** You have packages installed with semver ranges (rare for globals)

**Example:**
```bash
# IF you installed like this (uncommon):
npm install -g typescript@^5.0.0

# THEN npm update -g would update 5.2.2 → 5.3.3
npm update -g
```

**But this is NOT standard practice for global installs.** Most people install exact versions:
```bash
npm install -g typescript  # Installs exact version, e.g., 5.2.2
```

---

## Alternative: Use `npm-check-updates` (ncu)

A better tool for batch updating:

### Install
```bash
npm install -g npm-check-updates
```

### Check Updates
```bash
ncu -g
```

**Output:**
```
typescript        5.2.2   →  5.3.3
tsx               3.12.7  →  4.0.0
npm-check-updates 16.0.0  →  16.14.0
```

### Interactive Update
```bash
ncu -g -i
```

Shows each package and asks "Update? (y/N)" - gives you control!

### Update All (Still Not Recommended)
```bash
ncu -g -u
```

This actually updates to latest, unlike `npm update -g`, but still risky for breaking changes.

---

## Real-World Scenarios

### Scenario 1: TypeScript Minor Update (5.2.2 → 5.3.3)

**Risk:** Low - TypeScript is careful with minor versions
**Action:** Update immediately
```bash
npm install -g typescript@latest
```

### Scenario 2: tsx Major Update (3.12.7 → 4.0.0)

**Risk:** Medium - Major version = breaking changes
**Action:** Read changelog first

```bash
# Check release notes
npm view tsx@4.0.0

# Visit GitHub releases
# https://github.com/privatenumber/tsx/releases

# If safe, update
npm install -g tsx@4.0.0
```

### Scenario 3: Multiple Outdated Packages

**DON'T:**
```bash
npm update -g  # Does nothing or unpredictable behavior
```

**DO:**
```bash
# Check what's outdated
npm outdated -g

# Update safe ones first (minor/patch)
npm install -g pkg1@latest pkg2@latest

# Update major versions one-by-one after checking changelogs
npm install -g pkg3@latest  # After reading v4.0.0 changelog
```

---

## Monthly Update Workflow (Recommended)

### 1st of Each Month: Global Package Review

```bash
# Step 1: Check outdated packages
npm outdated -g

# Step 2: For each package, check changelog
# - Minor/patch: Update immediately
# - Major: Read changelog, test in isolated environment first

# Step 3: Update safe packages
npm install -g typescript@latest npm-check-updates@latest

# Step 4: Update risky packages one-by-one
npm install -g tsx@latest  # After confirming v4.0.0 is safe

# Step 5: Track changes
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin
git add package-management/npm/npm-global.txt
git commit -m "Monthly npm global updates: [list changes]"
git push
```

---

## Comparison: Pacman vs NPM Updates

| Aspect | pacman -Syu | npm update -g |
|--------|-------------|---------------|
| **Safety** | High (tested by maintainers) | Low (no testing) |
| **Breaking changes** | Rare (dependencies checked) | Common (no checks) |
| **Rollback** | Easy (pacman cache) | Hard (manual reinstall) |
| **Feedback** | Clear output | Silent/minimal |
| **Recommendation** | Run regularly | DON'T use |
| **Better alternative** | N/A | Individual updates |

---

## Exceptions: When Batch Update is OK

### 1. **Fresh Install**

If you just installed all globals and want to ensure latest:
```bash
npm update -g
```

This is safe because you have no workflows depending on specific versions yet.

### 2. **Dev Environment Reset**

Starting fresh after system reinstall:
```bash
npm install -g typescript tsx npm-check-updates
npm update -g  # Ensure everything is latest
```

### 3. **CI/CD Environment**

Automated environments where you want latest versions:
```bash
npm install -g typescript
npm update -g  # Always use latest in CI
```

But even here, pinning versions is better for reproducibility.

---

## Red Flags: When NOT to Batch Update

❌ **Production tooling** - CLI tools used for work projects
❌ **Project with deadlines** - Don't risk breaking your workflow
❌ **Major version bumps available** - Always read changelogs
❌ **Unfamiliar packages** - Don't update what you don't understand
❌ **TypeScript projects in progress** - Minor TS updates can cause type errors

---

## Recommended Strategy

### Keep Globals Minimal (< 10 packages)

Easier to update individually when you have fewer packages.

### Pin Important Tools in Projects

Don't rely on global versions for critical work:
```json
// package.json
{
  "devDependencies": {
    "typescript": "5.2.2",  // Pinned for project stability
    "tsx": "3.12.7"
  }
}
```

Use globals only for convenience, not project dependencies.

### Use npx for One-offs

Don't install globally if you use it rarely:
```bash
npx create-vite my-app  # Always latest, no global install
```

### Update Individually with Intent

Each update should be a conscious decision, not a batch operation.

---

## Updated Documentation Recommendations

I should update the NPM_MANAGEMENT_GUIDE.md to reflect these best practices:

### Change This:
```bash
# Update all global packages (like pacman -Syu)
npm update -g
```

### To This:
```bash
# Check for outdated packages
npm outdated -g

# Update individually (recommended)
npm install -g typescript@latest
npm install -g tsx@latest

# Batch update (NOT RECOMMENDED - see NPM_UPDATE_BEST_PRACTICES.md)
# npm update -g
```

---

## Summary: Key Takeaways

1. **DON'T use `npm update -g` for batch updates** - It's not like `pacman -Syu`
2. **DO check `npm outdated -g` monthly** - Know what needs updating
3. **DO update individually** - `npm install -g <pkg>@latest`
4. **DO read changelogs** for major version bumps
5. **DO keep global packages minimal** - Easier to manage
6. **DO use `npm-check-updates -g -i`** for interactive updates (better than batch)

---

## Final Recommendation

**Your workflow should be:**

```bash
# Monthly check
npm outdated -g

# For each package:
# - Minor/patch updates → npm install -g <pkg>@latest
# - Major updates → Read changelog first, then update

# Track changes
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin && git add package-management/npm/npm-global.txt && git commit -m "Update npm globals: <list changes>" && git push
```

**Avoid:**
```bash
npm update -g  # DON'T - unpredictable behavior
```

Think of npm globals like AUR packages from unmaintained sources - you want to know exactly what's changing before you update.
