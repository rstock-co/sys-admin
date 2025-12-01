# NPM Global Package Tracking

**Purpose:** Document all globally-installed npm packages and their use cases.

**Philosophy:** Keep global installs minimal. Prefer `npx` for one-offs, `package.json` for projects.

---

## ✅ Installed Global Packages

### CLI Tools
- [ ] `typescript` - TypeScript compiler (tsc)
- [ ] `tsx` - TypeScript executor (fast alternative to ts-node)
- [ ] `npm-check-updates` - Update package.json dependencies

### Development Utilities
- [ ] `nodemon` - Auto-restart on file changes
- [ ] `http-server` - Simple static file server
- [ ] `serve` - Static file serving

### Build Tools
- [ ] None (prefer project-local installs)

### Other
- [ ] None yet

---

## 📋 Candidates for Global Install

### High Priority
- [ ] `tsx` - Fast TypeScript executor without compilation
  - **Why:** Run .ts files directly, faster than ts-node
  - **Install:** `npm install -g tsx`
- [ ] `typescript` - TypeScript compiler
  - **Why:** Global tsc for quick type checking
  - **Install:** `npm install -g typescript`

### Medium Priority
- [ ] `npm-check-updates` - Update package.json to latest versions
  - **Why:** Useful across all projects
  - **Install:** `npm install -g npm-check-updates`
- [ ] `serve` - Simple static file server
  - **Why:** Quick preview of built frontends
  - **Install:** `npm install -g serve`

### Low Priority
- [ ] `nodemon` - Auto-restart on file changes
  - **Why:** Can use project-local or `npx nodemon`
  - **Install:** `npm install -g nodemon`

---

## 🗑️ Removed Packages

*None yet - starting fresh!*

---

## 📝 Installation Log

### 2025-11-30
- **System initialized** - No global npm packages installed
- **Strategy:** Keep globals minimal, use npx/pnpm for everything else

---

## Quick Commands

### Install Global + Track
```bash
npm install -g <package>
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin && git add package-management/npm/npm-global.txt && git commit -m "Install npm: <package>" && git push
```

### Uninstall Global + Track
```bash
npm uninstall -g <package>
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin && git add package-management/npm/npm-global.txt && git commit -m "Remove npm: <package>" && git push
```

### List All Global Packages (User-installed Only)
```bash
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done
```

### Check If Package Is Global
```bash
ls /usr/lib/node_modules/ | grep -w <package>
```

---

## Notes

- **pnpm** is installed via AUR (system package), not npm global
- **npm** itself is installed via pacman (Arch repos)
- **Scalable detection:** Uses `pacman -Qo` to automatically filter out system packages
- System packages (npm, pnpm, node-gyp, etc.) are owned by pacman and excluded automatically
- Only user-installed npm global packages appear in tracking list
