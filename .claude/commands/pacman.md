# Package Management Review

You are the sys-admin agent reviewing package installation status.

## Task

1. **Regenerate package lists from actual system state:**
   ```bash
   pacman -Qqe > ~/pkglist.txt
   pacman -Qqm > ~/aur-pkglist.txt
   ```
   This ensures the lists reflect what's ACTUALLY installed right now.

2. **Read package lists:**
   - `~/pkglist.txt` - Official repo packages (explicit)
   - `~/aur-pkglist.txt` - AUR packages

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

7. **Commit updated package lists to dotfiles:**
   - If package lists were regenerated and differ from what's tracked:
   ```bash
   dotfiles add pkglist.txt aur-pkglist.txt
   dotfiles commit -m "Update package lists to reflect current system state"
   dotfiles push
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
pacman -Qqe > ~/pkglist.txt
dotfiles add pkglist.txt && dotfiles commit -m "Install packages" && dotfiles push

# AUR
paru -S aur-package1
pacman -Qqm > ~/aur-pkglist.txt
dotfiles add aur-pkglist.txt && dotfiles commit -m "Install AUR packages" && dotfiles push
```

Be concise and actionable.
