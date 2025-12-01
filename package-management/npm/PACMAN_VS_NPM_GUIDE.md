# Pacman vs NPM: When to Use Which

**Purpose:** Understand the relationship between pacman, AUR, and npm for JavaScript tooling.

---

## The Big Picture

You have **three package managers** for JavaScript tools:

1. **pacman** (Arch official repos) - System-level, pre-compiled binaries
2. **AUR** (via paru) - Community packages, often pre-compiled or built from source
3. **npm** - JavaScript-specific, installs from npm registry

They're **not mutually exclusive** - you'll use all three, but for different purposes.

---

## Quick Decision Tree

```
Do I need a JavaScript tool?
│
├─ Is it available in Arch repos (pacman -Ss)?
│  ├─ Yes → Use pacman (PREFERRED)
│  └─ No → Continue
│
├─ Is it available in AUR (paru -Ss)?
│  ├─ Yes, as *-bin package → Use AUR (NEXT BEST)
│  ├─ Yes, but builds from npm → Consider npm global instead
│  └─ No → Continue
│
└─ Install via npm globally
   ├─ CLI tool used across projects → npm install -g
   └─ One-off usage → npx (don't install)
```

---

## Your Current Setup (Examples)

### System Packages (via pacman/AUR)

| Package | Source | Why This Way | How It Works |
|---------|--------|--------------|--------------|
| `npm` | pacman | System package manager | Pre-compiled C++ binary, part of Node.js ecosystem |
| `pnpm` | pacman | Fast package manager | Rust binary, installed as Arch package |
| `bun-bin` | AUR | All-in-one runtime | Pre-compiled binary downloaded from GitHub releases |
| `spicetify-cli` | AUR | Spotify customizer | Pre-compiled Go binary, no npm involved |
| `claude-code` | AUR | Claude Code CLI | Pre-compiled binary from Anthropic releases |

**Key insight:** These are **NOT built using npm**. They're pre-compiled binaries packaged for Arch.

---

## How Pacman/AUR vs NPM Actually Works

### Method 1: Pacman (Official Repos)

**Example:** `pnpm` package

```bash
sudo pacman -S pnpm
```

**What happens:**
1. Downloads pre-compiled binary from Arch mirrors
2. Installs to `/usr/lib/node_modules/pnpm/`
3. Creates symlink: `/usr/bin/pnpm` → `/usr/lib/node_modules/pnpm/bin/pnpm.cjs`
4. Tracked by pacman: `pacman -Qo /usr/lib/node_modules/pnpm` shows ownership

**Benefits:**
- ✅ Managed by pacman (updates via `pacman -Syu`)
- ✅ System-wide installation
- ✅ No build time
- ✅ Verified by Arch maintainers
- ✅ Automatic dependency resolution

**When to use:**
- Package exists in official repos
- You want system-managed updates
- You need it for multiple users (system-wide)

---

### Method 2: AUR (Community Packages)

**Example:** `bun-bin` package

```bash
paru -S bun-bin
```

**What happens:**
1. paru downloads PKGBUILD script from AUR
2. PKGBUILD downloads pre-compiled binary from GitHub releases
3. Packages it as Arch package
4. Installs to `/usr/bin/bun`
5. Tracked by pacman: `pacman -Qm` shows it's from AUR

**Benefits:**
- ✅ Still managed by pacman (updates via `paru -Syu`)
- ✅ Pre-compiled binaries (fast install)
- ✅ System-wide installation
- ✅ Community-maintained PKGBUILD

**When to use:**
- Package not in official repos
- `-bin` variant exists (pre-compiled)
- You want system-managed updates

---

### Method 3: AUR (Built from npm)

**Example:** Hypothetical `some-tool` package

```bash
paru -S some-tool  # AUR package that builds from npm
```

**What happens (behind the scenes):**
1. PKGBUILD downloads source from npm registry
2. Runs `npm install` during build
3. Packages result as Arch package
4. Installs to system directories
5. Tracked by pacman

**Example PKGBUILD snippet:**
```bash
build() {
  cd "$srcdir/$pkgname"
  npm install --production
}

package() {
  npm install -g --prefix "$pkgdir/usr" "$srcdir/$pkgname"
}
```

**Benefits:**
- ✅ Managed by pacman
- ✅ System-wide installation
- ⚠️ Slow build (npm install during package build)

**Drawbacks:**
- ❌ Rebuilds entire package on updates
- ❌ Slower than npm global for rapid iteration
- ❌ AUR maintainer might lag behind npm releases

**When to use:**
- Package has complex system dependencies
- You prefer pacman management over npm
- You don't update it frequently

---

### Method 4: NPM Global Install

**Example:** `typescript` (hypothetical)

```bash
npm install -g typescript
```

**What happens:**
1. Downloads package from npm registry
2. Installs to `/usr/lib/node_modules/typescript/`
3. Creates symlink: `/usr/bin/tsc` → `/usr/lib/node_modules/typescript/bin/tsc`
4. **NOT tracked by pacman**: `pacman -Qo /usr/lib/node_modules/typescript` returns error

**Benefits:**
- ✅ Latest version immediately available
- ✅ Fast updates (`npm update -g typescript`)
- ✅ Direct from npm registry (no AUR middleman)
- ✅ Easy to install/uninstall (`npm uninstall -g typescript`)

**Drawbacks:**
- ❌ Not tracked by pacman
- ❌ Manual updates (not part of `pacman -Syu`)
- ❌ Requires our custom tracking system

**When to use:**
- Package not in Arch repos or AUR
- You need latest version immediately
- Frequent updates expected
- It's a pure JavaScript CLI tool (no system dependencies)

---

## Real-World Decision Examples

### Example 1: TypeScript Compiler

**Question:** Should I use pacman, AUR, or npm?

**Answer:** Check availability:
```bash
pacman -Ss typescript  # Not in official repos
paru -Ss typescript    # Check AUR
```

**If AUR has `typescript-bin`:** Use `paru -S typescript-bin` (system-managed)
**If only npm:** Use `npm install -g typescript` (latest version, fast updates)

**Recommendation:** **npm global** - TypeScript releases frequently, you want latest features.

---

### Example 2: Prettier (Code Formatter)

**Question:** Global npm install or project-local?

**Answer:** **Project-local** (don't install globally at all!)

```bash
# In project directory
pnpm add -D prettier
```

**Why?**
- Different projects may need different Prettier versions
- Config files are project-specific
- Keeps global environment clean

**Rule:** Formatters, linters, build tools → Always project-local

---

### Example 3: http-server (Simple File Server)

**Question:** npm global or npx?

**Answer:** **Use npx** (no install needed)

```bash
# One-off usage
npx http-server ./build

# NOT: npm install -g http-server
```

**Why?**
- Used occasionally, not daily
- npx downloads and runs temporarily
- Zero trace after execution

---

### Example 4: pnpm (Package Manager)

**Question:** npm global or pacman?

**Answer:** **pacman** (already installed this way!)

```bash
# Already installed via:
sudo pacman -S pnpm
```

**Why?**
- Available in official repos
- System-managed updates (`pacman -Syu`)
- Used system-wide across all projects
- Pre-compiled binary (fast)

---

### Example 5: create-react-app (Project Scaffolder)

**Question:** npm global or npx?

**Answer:** **npx** (don't install globally)

```bash
# ❌ Don't do this:
npm install -g create-react-app
create-react-app my-app
npm uninstall -g create-react-app

# ✅ Do this:
npx create-react-app my-app
```

**Why?**
- Used once per project
- Always want latest version
- No need to clutter global environment

---

## The "npm Under the Hood" Myth

**Important clarification:** Most AUR packages do **NOT** use npm under the hood.

### How AUR `-bin` Packages Work

Taking `bun-bin` as example:

```bash
# PKGBUILD simplified
pkgname=bun-bin
source=("https://github.com/oven-sh/bun/releases/download/bun-v${pkgver}/bun-linux-x64.zip")

package() {
  install -Dm755 bun-linux-x64/bun "$pkgdir/usr/bin/bun"
}
```

**Steps:**
1. Downloads pre-compiled binary from GitHub
2. Extracts it
3. Places in `/usr/bin/`
4. pacman tracks it as installed

**No npm involved!** The binary is built by the upstream project (Bun team), not via npm.

---

### When AUR Actually Uses npm

Some AUR packages DO use npm during build:

**Example PKGBUILD pattern:**
```bash
pkgname=some-npm-tool
makedepends=('npm')

build() {
  npm install --production
}

package() {
  npm install -g --prefix "$pkgdir/usr" .
}
```

**This happens when:**
- No pre-compiled binary available
- Package is distributed via npm registry
- AUR maintainer wraps it for Arch

**Your choice:**
- Use AUR package → Slower builds, pacman-managed
- Use `npm install -g` → Faster, but manual tracking

---

## When to Use Each Method

### Use Pacman (Official Repos)

- Package exists in repos (`pacman -Ss <name>`)
- You want system-managed updates
- Tool is foundational (npm, node, git, etc.)

**Examples:** `npm`, `pnpm`, `nodejs`, `python-pip`

---

### Use AUR (-bin packages)

- Not in official repos
- `-bin` variant available (pre-compiled)
- You want pacman management
- Tool doesn't update super frequently

**Examples:** `bun-bin`, `claude-code`, `google-chrome`

---

### Use AUR (Built from npm)

- Rare - usually better to use npm global
- Only if package has complex system dependencies
- You strongly prefer pacman management

**When to avoid:** Tool updates frequently (you'll rebuild entire package each time)

---

### Use npm Global Install

- Pure JavaScript CLI tool
- Not in repos/AUR, or AUR version is outdated
- Frequent updates expected
- Used across multiple projects

**Examples:** `tsx`, `npm-check-updates`, `typescript` (if not in AUR)

**Track with:** Our custom tracking system (`npm-global.txt`)

---

### Use npx (No Install)

- One-off commands
- Project scaffolders (`create-*`)
- Tools you use rarely
- Always want latest version

**Examples:** `create-vite`, `create-next-app`, `degit`

---

### Use Project-local (package.json)

- Development dependencies
- Build tools, formatters, linters
- Libraries used in code
- Anything project-specific

**Examples:** `prettier`, `eslint`, `webpack`, `react`

**Install with:** `pnpm add <package>` (not npm global!)

---

## Your Current Strategy (Recommended)

Based on your setup:

| Category | Method | Why |
|----------|--------|-----|
| **System tools** (npm, pnpm, node) | pacman | System-managed, foundational |
| **Binaries** (bun, claude-code) | AUR `-bin` | Pre-compiled, pacman-managed |
| **CLI tools** (future: tsx, typescript) | npm global | Fast updates, JavaScript-specific |
| **Project deps** (react, express) | pnpm (project-local) | Per-project versions |
| **One-offs** (create-*, scaffolders) | npx | Zero install, always latest |

---

## Common Misconceptions

### ❌ "I should install everything via pacman/AUR"

**Reality:** npm global is fine for pure JavaScript tools. Don't force everything through AUR.

### ❌ "npm global pollutes my system"

**Reality:** Our tracking system keeps it tidy. npm globals are isolated in `/usr/lib/node_modules/`.

### ❌ "AUR packages use npm to install"

**Reality:** Most `-bin` packages download pre-compiled binaries. npm is NOT involved.

### ❌ "I need npm global for project dependencies"

**Reality:** Use `pnpm add` in project directory. Never install project deps globally.

---

## Practical Workflow

### Installing a New JavaScript Tool

**Step 1:** Check official repos
```bash
pacman -Ss <tool-name>
```
If found → `sudo pacman -S <tool-name>`

**Step 2:** Check AUR
```bash
paru -Ss <tool-name>
```
If found as `-bin` → `paru -S <tool-name>-bin`

**Step 3:** Check if it's a one-off
If it's a scaffolder or rarely-used → Use `npx <tool-name>`

**Step 4:** Check if it's project-specific
If it's a dev dependency → `pnpm add -D <tool-name>` in project

**Step 5:** Install via npm global
```bash
npm install -g <tool-name>
ls -1 /usr/lib/node_modules/ | while read pkg; do pacman -Qo "/usr/lib/node_modules/$pkg" >/dev/null 2>&1 || echo "$pkg"; done > ~/agents/sys-admin/package-management/npm/npm-global.txt
cd ~/agents/sys-admin && git add package-management/npm/npm-global.txt && git commit -m "Install npm: <tool-name>" && git push
```

---

## Summary Table

| Source | Tracking | Updates | Speed | Use Case |
|--------|----------|---------|-------|----------|
| **pacman** | Automatic | `pacman -Syu` | Fast | System tools (npm, pnpm, node) |
| **AUR -bin** | Automatic | `paru -Syu` | Fast | Pre-compiled tools (bun, chrome) |
| **AUR (npm)** | Automatic | `paru -Syu` | Slow | Complex builds (rare) |
| **npm global** | Manual (our system) | `npm update -g` | Fast | Pure JS CLIs (tsx, typescript) |
| **npx** | None (temporary) | Always latest | Instant | One-offs (create-*, scaffolders) |
| **pnpm (project)** | package.json | `pnpm update` | Fast | Project dependencies (95% of packages) |

---

## Key Takeaways

1. **Prefer pacman/AUR** when available (system-managed updates)
2. **Use npm global** for pure JavaScript CLIs not in repos
3. **Use npx** for one-off commands (no install needed)
4. **Use project-local** for 95% of packages (never global)
5. **Track npm globals** with our custom system (no hardcoded filters!)

---

## Still Unsure?

Ask yourself:

- **Is it in pacman/AUR?** → Use that (system-managed)
- **Is it a CLI I use often?** → npm global
- **Is it a one-time command?** → npx
- **Is it project-specific?** → pnpm add (project-local)

When in doubt, start with npx. If you use it 5+ times, then consider npm global.
