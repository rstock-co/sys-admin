# Claude Code Documentation

**Purpose:** Master copy of official Anthropic Claude Code documentation.

**Source:** Manually copied from https://docs.claude.ai using "Copy to markdown" button.

---

## Directory Structure

```
claude-code/
├── usage/              # How to USE Claude Code
│   ├── interactive-mode.md
│   ├── headless-mode.md
│   ├── cli-reference.md
│   └── ...
└── primitives/         # How to BUILD Claude Code primitives
    ├── skills.md
    ├── slash-commands.md
    ├── hooks-reference.md
    ├── mcp.md
    └── ...
```

---

## Usage Docs (How to USE Claude Code)

**Skill:** `claude-code-docs` (symbiont)
**Symlink:** `symbiont/.claude/skills/meta/claude-code-docs/docs/` → `usage/`

Topics covered:
- Interactive mode
- Headless mode
- Web interface
- CLI reference
- Configuration (settings, memory, model, status line, terminal)
- GitHub integration
- Common workflows
- Checkpointing
- Costs

---

## Primitives Docs (How to BUILD with Claude Code)

**Skill:** `primitive-builder` (symbiont)
**Symlink:** `symbiont/.claude/skills/meta/primitive-builder/docs/` → `primitives/`

Topics covered:
- Skills
- Slash commands
- Hooks (guide + reference)
- Sub-agents
- MCP servers
- Plugins (guide + reference + marketplace)
- Tools reference
- Selecting primitives

---

## Updating Documentation

### 1. Monitor for Changes

Use `/claude-updates` command to scan Claude Code changelog for documentation updates.

### 2. Copy from Official Docs

When updates are needed:
1. Visit https://docs.claude.ai/claude-code/[page]
2. Click "Copy to markdown" button
3. Replace file in appropriate folder (`usage/` or `primitives/`)

### 3. Track Changes

```bash
cd ~/agents/sys-admin
git add data/claude-code/
git commit -m "Update Claude Code docs: [specific pages updated]"
git push
```

Skills automatically see updates via symlinks (no action needed in symbiont).

---

## Related Commands

- `/claude-updates` - Scan for Claude Code changelog updates
- `/claude-research` - Deep dive into specific features

---

## Maintenance

**Weekly:** Run `/claude-updates` to check for doc updates
**Monthly:** Full review of documentation against official docs
**On major releases:** Expect significant doc updates

---

## Notes

- **Single source of truth** - sys-admin owns these docs
- **Symlinks** - Skills in symbiont reference these via symlinks
- **Version controlled** - All changes tracked in sys-admin repo
- **Manual process** - Anthropic's markdown export is more token-efficient than scraping
