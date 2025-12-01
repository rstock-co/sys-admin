# Package Management Review

You are the sys-admin agent reviewing package installation status.

## Task

1. **Regenerate package lists from actual system state:**
   ```bash
   pacman -Qqe > ~/agents/sys-admin/package-management/pkglist.txt
   pacman -Qqm > ~/agents/sys-admin/package-management/aur-pkglist.txt
   ```
   This ensures the lists reflect what's ACTUALLY installed right now.

2. **Read package lists:**
   - `@package-management/pkglist.txt` - Official repo packages (explicit)
   - `@package-management/aur-pkglist.txt` - AUR packages

3. **Read tracking file:**
   - `@package-management/PACKAGE_INSTALL_TRACKING.md`

4. **Cross-reference and update:**
   - Compare actual installed packages against the "✅ Installed Packages" section
   - Identify packages that are installed but NOT listed in the tracking file
   - Add any missing packages to the appropriate subsection in "✅ Installed Packages"
   - Move any packages from "📋 Not Yet Installed" to "✅ Installed Packages" if they're already installed

5. **Recommend next installations:**
   - Review the "📋 Not Yet Installed" section
   - Prioritize "High Priority" items
   - Recommend 3-5 packages to install next
   - Provide installation commands (separate official repos from AUR)
   - Explain benefits for this system (Ryzen 9 7950X + Arc B580)

6. **Update tracking file:**
   - If you found installed packages missing from tracking, update the file
   - Commit changes to git with descriptive message

7. **Commit updated package lists to sys-admin repo:**
   - If package lists were regenerated and differ from what's tracked:
   ```bash
   git add package-management/pkglist.txt package-management/aur-pkglist.txt
   git commit -m "Update package lists to reflect current system state"
   git push
   ```

## Output Format

```
📦 Package Status Report

TRACKING FILE UPDATES:
- Added X packages to "Installed" section
- Moved Y packages from "Not Yet Installed"

RECOMMENDED NEXT INSTALLS:
1. package-name (category) - Why it's useful
2. package-name (category) - Why it's useful
...

INSTALL COMMANDS:
# Official repos
sudo pacman -S package1 package2
pacman -Qqe > ~/agents/sys-admin/package-management/pkglist.txt
git add package-management/pkglist.txt && git commit -m "Install packages" && git push

# AUR
paru -S aur-package1
pacman -Qqm > ~/agents/sys-admin/package-management/aur-pkglist.txt
git add package-management/aur-pkglist.txt && git commit -m "Install AUR packages" && git push
```

Be concise and actionable.
