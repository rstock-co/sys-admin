# `.claude/rules/` Directory

**Feature introduced in:** v2.0.64 (December 10, 2025)

The rules directory provides a modular alternative to monolithic CLAUDE.md files. Instead of one massive instruction file, you organize project-specific rules into focused markdown files.

---

## How It Works

All `.md` files in `.claude/rules/` are automatically loaded as project memory with the **same priority** as `.claude/CLAUDE.md`. They're treated as high-priority instructions in Claude's context window.

```
.claude/rules/
├── api-guidelines.md      # Loaded automatically
├── testing.md             # Loaded automatically
├── security.md            # Loaded automatically
└── frontend/
    └── react.md           # Loaded automatically (nested works)
```

No configuration needed. Drop a markdown file in, it's active.

---

## Path-Scoped Rules

Rules can target specific files using YAML frontmatter:

```yaml
---
paths: src/api/**/*.ts
---
# API Development Rules

All API endpoints must:
- Return consistent error formats
- Include rate limiting headers
- Log request/response timing
```

This rule **only activates** when Claude is working with files matching `src/api/**/*.ts`. Otherwise it's not in context at all.

### Glob Pattern Examples

| Pattern | Matches |
|---------|---------|
| `src/**/*.ts` | All TypeScript files under src/ |
| `*.md` | Markdown files in root only |
| `tests/**` | Everything under tests/ |
| `src/api/**/*.ts` | TypeScript files under src/api/ |

---

## Why It's Better Than Monolithic CLAUDE.md

| Problem with Monolithic | How Rules Directory Solves It |
|-------------------------|-------------------------------|
| **Context bloat** - Every instruction loaded every time | Path-scoped rules only load when relevant |
| **Hard to maintain** - One huge file becomes unwieldy | One concern per file, easy to find and edit |
| **No separation of concerns** - API rules mixed with testing mixed with security | Natural organization by domain |
| **Difficult to share** - Can't easily reuse rules across projects | Symlink individual rule files |
| **All-or-nothing** - Can't disable one section | Delete/rename one file to disable |

---

## Best Practices

1. **One concern per file** - Keep rules focused
2. **Descriptive names** - `api-validation.md` beats `rules1.md`
3. **Leverage path targeting** - Scope when rules load to reduce noise
4. **Version control** - Rules are code, track changes
5. **Use symlinks** - Share common rules across projects

---

## Priority Hierarchy

| Source | Priority | Best For |
|--------|----------|----------|
| `CLAUDE.md` (project root) | High | Universal operational workflows |
| `.claude/rules/*.md` | High (same level) | Domain-specific instructions |
| Skills | Medium | Cross-project capabilities |

Both CLAUDE.md and rules/ are high priority—they're peers, not hierarchical.

---

## Symbiont Application

### Current Pattern
```
mycelium/health-coach/
├── CLAUDE.md          # Everything in one file
└── output-style.md
```

### Modular Pattern
```
mycelium/health-coach/
├── .claude/
│   └── rules/
│       ├── persona.md              # Core identity
│       ├── safety-constraints.md   # What it can't do
│       ├── biohacking-expertise.md # Domain knowledge
│       └── output-voice.md         # Symlinked from core/
├── CLAUDE.md                       # Just operational workflow
└── output-style.md
```

### Benefits for SGTA Pattern

1. **Symlink shared rules** - `safety-constraints.md` could be identical across all specialists, symlinked from `core/rules/`

2. **Path-scoped specialist behavior** - If health-coach works with different types of data:
   ```yaml
   ---
   paths: data/bloodwork/**
   ---
   # Bloodwork Analysis Rules
   Always flag values outside reference ranges...
   ```

3. **Easier SGTA factory** - When creating new specialists, copy the rules you need rather than editing a monolith

4. **Cleaner CLAUDE.md** - Keep CLAUDE.md for operational workflow only, move persona/constraints to rules

---

## Migration Strategy

Start small:

1. Pick one specialist (e.g., `health-coach`)
2. Extract one concern from its CLAUDE.md into `.claude/rules/safety-constraints.md`
3. Test that the behavior is identical
4. If it works, gradually modularize the rest

Don't migrate everything at once. The monolithic CLAUDE.md still works fine—this is an option, not a requirement.

---

## Example: Health Coach Rules Structure

```
mycelium/health-coach/.claude/rules/
├── persona.md
│   # Health Coach Persona
│   You are a warm, compassionate biohacking coach...
│
├── safety-constraints.md
│   # Safety Constraints
│   - Never provide medical diagnoses
│   - Always recommend consulting healthcare providers for...
│   - Flag concerning symptoms immediately
│
├── biohacking-expertise.md
│   # Domain Knowledge
│   Areas of expertise:
│   - Sleep optimization (Huberman protocols)
│   - Circadian rhythm management
│   - Supplement stacks...
│
└── bloodwork-analysis.md
    ---
    paths: data/bloodwork/**
    ---
    # Bloodwork Analysis Rules
    When analyzing bloodwork:
    - Compare against optimal ranges, not just reference ranges
    - Flag trends across multiple tests...
```

---

*Last updated: 2025-12-29*
