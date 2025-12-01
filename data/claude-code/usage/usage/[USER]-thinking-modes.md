# Thinking Modes in Claude Code
**[USER-CREATED DOCUMENTATION]**
*This document supplements official Claude Code documentation with community-discovered features.*

---

## Overview

Claude Code supports **thinking modes** that trigger extended reasoning by allocating specific token budgets for deep analysis before responding. These are triggered by magic keywords in your prompts.

**Source:** [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) (official)

---

## The Four Thinking Modes

| Keyword | Token Budget | Best For |
|---------|--------------|----------|
| `think` | 4,000 tokens | Routine debugging, basic refactoring, straightforward problems |
| `think hard` | ~7,000 tokens (estimated) | Moderate complexity, architectural considerations |
| `think harder` | ~10,000 tokens (estimated) | Complex problem-solving, multi-step reasoning |
| `ultrathink` | 31,999 tokens (max) | Deep architectural analysis, unfamiliar codebases, optimization |

**Official documentation states:** *"These specific phrases are mapped directly to increasing levels of thinking budget in the system: 'think' < 'think hard' < 'think harder' < 'ultrathink.'"*

---

## How to Use

Simply include the keyword **anywhere in your prompt**:

```bash
# Basic thinking
Analyze this API design think

# Maximum thinking
Research the best approach for migrating this legacy system ultrathink

# Planning complex features
Plan the implementation strategy for distributed caching ultrathink
```

The keyword triggers preprocessing in Claude Code's terminal interface that allocates the corresponding thinking budget.

---

## How It Works

1. **Preprocessing:** Claude Code detects the keyword before sending the prompt to the model
2. **Budget allocation:** Sets the extended thinking token limit based on the keyword
3. **Deep reasoning:** Claude uses the allocated tokens to internally reason through alternatives, evaluate trade-offs, and iterate on solutions
4. **Response:** After thinking phase completes, Claude responds with the refined solution

**Key insight:** The thinking happens *before* Claude starts writing the response you see. Higher budgets allow more thorough internal deliberation.

---

## When to Use Each Mode

### `think` (4,000 tokens)
- Understanding unfamiliar code patterns
- Debugging straightforward errors
- Basic architectural decisions
- Default mode for most complex tasks

**Example:**
```bash
Explain how this authentication middleware works think
```

### `think hard` (7,000 tokens)
- Moderate refactoring decisions
- Performance optimization opportunities
- Cross-module dependencies analysis

**Example:**
```bash
How should we restructure this module to reduce coupling? think hard
```

### `think harder` (10,000 tokens)
- Complex architectural planning
- Multi-step migration strategies
- System-wide optimization approaches

**Example:**
```bash
Design a strategy to migrate from REST to GraphQL think harder
```

### `ultrathink` (31,999 tokens - MAX)
- Unfamiliar/undocumented codebases requiring deep exploration
- Critical architectural decisions with major trade-offs
- Performance bottleneck investigation across entire system
- Planning large-scale refactors or migrations

**Example:**
```bash
Analyze this legacy codebase and recommend a complete modernization plan ultrathink
```

---

## Important Limitations

### ⚠️ Claude Code Terminal Only

**Thinking modes ONLY work in Claude Code's CLI/terminal interface.**

They do **NOT** work in:
- Claude web chat (claude.ai)
- Claude API
- Mobile apps

**Why?** Claude Code has a preprocessing layer that intercepts these keywords. The web interface and API don't have this preprocessing, so "ultrathink" is treated as ordinary text.

### ⚠️ Token Consumption

Higher thinking budgets consume more tokens from your usage limits:
- **Cost:** Extended thinking counts against your Claude Code subscription usage
- **Reserve for complexity:** Don't use `ultrathink` for trivial tasks
- **Balance quality vs. cost:** Start with `think`, escalate to `ultrathink` only when needed

---

## Best Practices

### ✅ DO Use Thinking Modes When:
- Working with unfamiliar codebases
- Making architectural decisions with long-term impact
- Debugging complex, multi-layered issues
- Planning large features or refactors
- Optimizing performance-critical code

### ❌ DON'T Use Ultrathink For:
- Simple syntax questions
- Routine file edits
- Basic debugging (typos, simple logic errors)
- Tasks with obvious solutions

### 💡 Pro Tips

**1. Combine with Plan Mode**
```bash
Create a plan for implementing user authentication ultrathink
```
Maximizes planning intelligence while maintaining execution efficiency.

**2. Use for "Explore" Phase**
```bash
Explore this codebase and identify the data flow ultrathink
```
Thorough initial understanding reduces iterations later.

**3. Escalate Progressively**
Start with `think`, only move to `ultrathink` if the initial response lacks depth.

**4. Be Specific**
```bash
# Vague (wastes tokens)
Help me with this code ultrathink

# Specific (focused thinking)
Identify performance bottlenecks in the database query layer and propose optimization strategies ultrathink
```

---

## Verification

**Official confirmation:** The [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) documentation explicitly states thinking modes are mapped to increasing budgets, recommending use of "think" for complex planning.

**Community validation:**
- [ClaudeLog FAQ: What is UltraThink?](https://claudelog.com/faqs/what-is-ultrathink/)
- [Vibe Sparking: Claude Code Thinking Modes Guide](https://www.vibesparking.com/en/blog/ai/claude-code/2025-07-28-claude-code-thinking-modes-guide/)

---

## Changelog Updates

**v2.0.50 (Nov 21, 2025):** "Improved ultrathink text display" - Enhanced UI rendering of thinking output

---

## Related Documentation

- [Official: Interactive Mode](./interactive-mode.md) - Core Claude Code usage
- [Official: Common Workflows](./common-workflows.md) - Explore, plan, code, commit
- [Official: Costs](./costs.md) - Understanding token usage

---

**Last Updated:** November 30, 2025
**Maintained By:** User (sys-admin agent)
**Status:** Community-validated, officially referenced feature
