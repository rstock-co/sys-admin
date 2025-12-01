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
ls /usr/lib/node_modules/ | grep -v npm | grep -v node-gyp | grep -v nopt | grep -v semver | grep -v pnpm > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin && git add package-management/npm/npm-global.txt && git commit -m "Install npm: <package>" && git push
```

### Uninstall Global + Track
```bash
npm uninstall -g <package>
ls /usr/lib/node_modules/ | grep -v npm | grep -v node-gyp | grep -v nopt | grep -v semver | grep -v pnpm > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin && git add package-management/npm/npm-global.txt && git commit -m "Remove npm: <package>" && git push
```

### List All Global Packages
```bash
ls /usr/lib/node_modules/
```

### Check If Package Is Global
```bash
npm list -g <package> 2>&1 | grep -v error || echo "Not installed globally"
```

---

## Notes

- **pnpm** is installed via AUR (system package), not npm global
- **npm** itself is installed via pacman (Arch repos)
- Using `ls /usr/lib/node_modules/` instead of `npm list -g` due to npm config quirks
- Filter out npm's own dependencies: npm, node-gyp, nopt, semver, pnpm
