# Package Management Review

You are the sys-admin agent reviewing package installation status.

## Task

1. **Regenerate package lists from actual system state:**
   ```bash
   pacman -Qqe > ~/agents/sys-admin/data/packages/pkglist.txt
   pacman -Qqm > ~/agents/sys-admin/data/packages/aur-pkglist.txt
   ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/data/packages/npm-global.txt
   ```
   This ensures the lists reflect what's ACTUALLY installed right now.

   **How npm detection works:** Lists packages in `/usr/lib/node_modules/` that are NOT owned by any pacman package. System packages (npm, pnpm, node-gyp, etc.) are owned by pacman and automatically excluded.

2. **Read package lists:**
   - `@data/packages/pkglist.txt` - Official repo packages (explicit)
   - `@data/packages/aur-pkglist.txt` - AUR packages
   - `@data/packages/npm-global.txt` - Global npm packages

3. **Read tracking files:**
   - `@data/packages/PACKAGE_INSTALL_TRACKING.md`
   - `@data/packages/NPM_INSTALL_TRACKING.md`

4. **Cross-reference and update (System Packages):**
   - Compare actual installed packages against the "✅ Installed Packages" section
   - Identify packages that are installed but NOT listed in the tracking file
   - Add any missing packages to the appropriate subsection in "✅ Installed Packages"
   - Move any packages from "📋 Not Yet Installed" to "✅ Installed Packages" if they're already installed

5. **Cross-reference and update (NPM Packages):**
   - Compare `npm-global.txt` against `NPM_INSTALL_TRACKING.md`
   - Identify npm packages that are installed but NOT tracked
   - Check if any tracked packages are no longer installed
   - Note: Empty file or "# No global npm packages installed yet" means zero globals (clean state)

6. **Recommend next installations:**
   - Review both "📋 Not Yet Installed" sections (system + npm)
   - Prioritize "High Priority" items
   - Recommend 3-5 system packages AND 2-3 npm packages to install next
   - Provide installation commands (separate official repos, AUR, and npm)
   - Explain benefits for this system (Ryzen 9 7950X + Arc B580)

7. **Update tracking files:**
   - If you found installed packages missing from tracking, update the files
   - Commit changes to git with descriptive message

8. **Commit updated package lists to sys-admin repo:**
   - If package lists were regenerated and differ from what's tracked:
   ```bash
   cd ~/agents/sys-admin
   git add data/packages/pkglist.txt data/packages/aur-pkglist.txt data/packages/npm-global.txt
   git commit -m "Update package lists to reflect current system state"
   git push
   ```

## Output Format

```
📦 Package Status Report

SYSTEM PACKAGE UPDATES:
- Added X packages to "Installed" section
- Moved Y packages from "Not Yet Installed"

NPM PACKAGE STATUS:
- Global packages installed: N
- Tracked in NPM_INSTALL_TRACKING.md: M
- Discrepancies: [list any]

RECOMMENDED NEXT INSTALLS:

System Packages:
1. package-name (category) - Why it's useful
2. package-name (category) - Why it's useful
...

NPM Packages:
1. package-name - Why it's useful
2. package-name - Why it's useful

INSTALL COMMANDS:

# System - Official repos
sudo pacman -S package1 package2
pacman -Qqe > ~/agents/sys-admin/data/packages/pkglist.txt
cd ~/agents/sys-admin && git add data/packages/pkglist.txt && git commit -m "Install packages" && git push

# System - AUR
paru -S aur-package1
pacman -Qqm > ~/agents/sys-admin/data/packages/aur-pkglist.txt
cd ~/agents/sys-admin && git add data/packages/aur-pkglist.txt && git commit -m "Install AUR packages" && git push

# NPM - Global
npm install -g package1 package2
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/data/packages/npm-global.txt
cd ~/agents/sys-admin && git add data/packages/npm-global.txt && git commit -m "Install npm: package1, package2" && git push
```

Be concise and actionable.
