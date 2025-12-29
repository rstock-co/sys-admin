# LSP in Claude Code Terminal - Deep Dive

**Focus:** Using LSP capabilities in the terminal-based Claude Code (not IDE extensions)

## Quick Answer

**Yes, LSP works in terminal Claude Code.** The LSP tool is part of Claude Code's core capabilities, not an IDE-specific feature. When you run `claude` in Alacritty, you get the same LSP access as VSCode users.

## How Claude Uses LSP Behind the Scenes

When you ask Claude about code navigation, it can now invoke LSP tools:

```
You: "Find all places where UserSession is used"

Claude's internal process:
1. Identifies symbol: UserSession
2. Invokes: findReferences(symbol="UserSession")
3. Language server returns: [
     src/auth/session.py:23,
     src/api/middleware.py:45,
     src/api/middleware.py:89,
     tests/test_auth.py:12,
     ...
   ]
4. Claude reads relevant context from each location
5. Presents organized summary to you
```

You don't need to explicitly ask Claude to "use LSP" - it's automatic when the tools are available.

## Setup for Terminal Users

### Step 1: Verify Claude Code Version
```bash
claude --version
# Must be 2.0.74 or higher
```

### Step 2: Add the LSP Marketplace
```bash
claude
# Inside Claude Code:
/plugin marketplace add Piebald-AI/claude-code-lsps
```

### Step 3: Install Language Plugins
```
/plugins
# Navigate to "Discover" tab
# Find your language (e.g., "Python LSP", "TypeScript LSP")
# Press 'i' to install
```

### Step 4: Install Language Server Binaries

Your system needs the actual language servers:

**Arch Linux examples:**
```bash
# Rust
rustup component add rust-analyzer

# Python
sudo pacman -S pyright
# or: pip install pyright

# TypeScript
npm install -g @vtsls/language-server

# Go
go install golang.org/x/tools/gopls@latest

# C/C++
sudo pacman -S clang  # clangd included
```

### Step 5: Restart Claude Code
```bash
# Exit and relaunch
exit
claude
```

## What You'll Notice

### Before LSP (grep-based navigation)
- Claude searches with text patterns
- Multiple potential matches to sift through
- No type information
- Comments/strings can be false positives

### After LSP (semantic navigation)
- Single authoritative answer
- Full type signatures
- Documentation inline
- Errors detected immediately after edits

## Terminal-Specific Considerations

### Alacritty/Kitty/Warp
All supported via `/terminal-setup` in 2.0.74. Run it to optimize rendering.

### Multiple Sessions (Symbiont Pattern)
Each terminal session loads LSP plugins independently. If you spawn specialists via hotkeys, each gets LSP access if plugins are installed globally (`~/.claude/plugins/`).

### Resource Usage
Language servers run as background processes. With multiple Claude Code sessions + multiple LSP servers, monitor memory:
```bash
ps aux | grep -E "(claude|rust-analyzer|pyright|gopls)"
```

## Current State (December 2025)

From community testing:

| Status | Note |
|--------|------|
| ✅ Works | TypeScript, Rust, Go, Python (pyright) |
| ⚠️ Partial | C/C++ (diagnostics incomplete) |
| ❌ Not yet | Zig, some niche languages |
| 🔄 Improving | Rename/refactor operations |

**Key limitation:** Claude sometimes provides imprecise line:column coordinates, causing LSP queries to fail. The cclsp MCP server addresses this with intelligent position fallbacks.

## Alternative: cclsp MCP Server

For more robust LSP in terminal:

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "cclsp": {
      "command": "npx",
      "args": ["cclsp"]
    }
  }
}
```

Benefits over built-in:
- Handles LLM position errors gracefully
- Full rename/refactor support
- Better diagnostics integration
- Interactive setup wizard

## Practical Terminal Workflow

```
# Start Claude in your project
cd ~/symbiont/core
claude

# Claude now has LSP access to the codebase
# Ask naturally - LSP is used automatically:

You: "What's the signature of the fire_pulse function?"
Claude: [uses hover on fire_pulse]
"fire_pulse(event_type: PulseType, intensity: float = 1.0) -> AsyncResult[bool]"

You: "Find everywhere we call this"
Claude: [uses findReferences]
"Found 12 references across 5 files..."

You: "Any type errors in this file?"
Claude: [uses getDiagnostics]
"Line 47: Expected 'str', got 'int' for parameter 'source'"
```

## Summary

LSP in terminal Claude Code:
- **Works** - Same capability as IDE users
- **Automatic** - Claude uses it without explicit requests
- **Requires setup** - Install plugins + language server binaries
- **Still maturing** - Some rough edges, improving quickly
