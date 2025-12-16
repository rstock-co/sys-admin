# NPM Global Package Tracking

**Purpose:** Track global npm packages installed outside of pacman-managed packages.

**Note:** System packages like `npm`, `pnpm`, and `node-gyp` are managed by pacman and excluded from this list.

---

## Current Status

**Global npm packages installed:** 0

The system currently has no global npm packages installed outside of pacman-managed ones. This is a clean state.

---

## Recommended Global NPM Packages

### High Priority
- [ ] `typescript` - TypeScript compiler
- [ ] `tsx` - TypeScript execute (ts-node alternative, faster)
- [ ] `prettier` - Code formatter

### Development Tools
- [ ] `eslint` - JavaScript/TypeScript linter
- [ ] `depcheck` - Check for unused dependencies
- [ ] `npm-check-updates` - Upgrade package.json dependencies

### Utilities
- [ ] `serve` - Static file server
- [ ] `http-server` - Simple HTTP server
- [ ] `concurrently` - Run multiple commands concurrently
- [ ] `nodemon` - Auto-restart Node.js on file changes

---

## Quick Commands

### Install Global Package
```bash
npm install -g <package>
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/data/packages/npm-global.txt
cd ~/agents/sys-admin && git add data/packages/npm-global.txt && git commit -m "Install npm: <package>" && git push
```

### List Global Packages
```bash
npm list -g --depth=0
```

### Check Outdated
```bash
npm outdated -g
```
