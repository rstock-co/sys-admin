---
argument-hint: [--fresh] [--phase=1|2|3]
description: Deep audit of inbox to identify and filter all spam
---

# Inbox Audit

Comprehensive inbox scan to identify spam and ensure all remaining emails are legitimate.

---

## ⛔ CRITICAL: TOKEN EFFICIENCY ⛔

This command scans thousands of emails. You MUST:

1. **Use `format="metadata"` for ALL batch fetches** - NEVER use "full"
2. **Write results to file IMMEDIATELY after each batch** - Don't hold in context
3. **Track progress in `inbox-audit-progress.json`** - Enables resume
4. **Never hold more than 100 emails in context at once**
5. **Pause after each phase for user approval**

**Token budget per iteration: ~5,700 tokens (100 emails)**

---

## Usage

```bash
/inbox-audit              # Auto-resumes if incomplete, starts fresh if done
/inbox-audit --fresh      # Force start over (resets progress files)
/inbox-audit --phase=2    # Jump to specific phase
```

**Email account:** richard.stock@gmail.com (default)

---

## Before Starting

Load the email-wizard skill and read these data files:

```
.claude/skills/email-wizard/data/
├── inbox-audit-progress.json   # Resume state
├── inbox-audit-results.md      # Accumulated findings
├── exceptions.json             # Senders to SKIP (user wants to keep)
└── legitimate-entities.json    # Trusted senders
```

---

## Execution Flow

### Step 1: Check Progress File

Read `data/inbox-audit-progress.json`:

- If exists and `status != "completed"`: Resume from last state
- If missing or completed: Start fresh audit

### Step 2: Execute Current Phase

Run ONE phase at a time, then STOP and ask user to continue.

### Step 3: Write Results Immediately

After EACH batch of emails:
1. Append findings to `data/inbox-audit-results.md`
2. Update `data/inbox-audit-progress.json`

### Step 4: Report and Wait

Show progress summary, then ask:
```
Continue to next phase? [Y/n]
```

---

## Phase 1: Quick Win Scans

Search for emails matching spam patterns.

**Searches to run (one at a time):**

```python
SPAM_SEARCHES = [
    "in:inbox list:*",              # Has List-Unsubscribe header
    "in:inbox unsubscribe",         # Contains "unsubscribe" in body
    "in:inbox from:noreply@",       # No-reply senders
    "in:inbox from:no-reply@",      # No-reply variant
    "in:inbox from:newsletter@",    # Newsletter senders
    "in:inbox from:promo@",         # Promo senders
    "in:inbox from:marketing@",     # Marketing senders
    "in:inbox from:deals@",         # Deals senders
    "in:inbox from:offers@",        # Offers senders
    "in:inbox from:info@",          # Generic info@ (often spam)
    "in:inbox from:hello@",         # Generic hello@ (often marketing)
]
```

**For each search:**
1. Get up to 100 message IDs
2. Fetch metadata in batches of 25 (format="metadata")
3. Extract sender domain and subject
4. Check against exceptions.json - SKIP if listed
5. Append to results file immediately
6. Update progress file

**Output to results file:**
```markdown
## Phase 1: Quick Win Scans

### Search: "unsubscribe"
Found 87 emails

| Domain | Count | Sample Subject |
|--------|-------|----------------|
| @marketing.walmart.ca | 12 | "Weekly deals..." |
| @e.costco.ca | 8 | "New arrivals..." |
```

---

## Phase 2: Domain Analysis

Group all Phase 1 findings by domain and classify.

**Classification (CONSERVATIVE mode):**

| Category | Criteria | Action |
|----------|----------|--------|
| High-confidence spam | Subdomain patterns: `@e.`, `@mail.`, `@marketing.`, `@news.`, `@promo.` | Present for confirmation |
| Medium-confidence | Generic senders: `noreply@`, `info@`, `hello@` | Present for review |
| Needs review | Everything else | Present for decision |

**IMPORTANT:** Do NOT auto-classify. Present ALL findings for user review.

**Output:**
```markdown
## Phase 2: Domain Analysis

### High-Confidence Spam Patterns
| Domain | Count | Pattern Match |
|--------|-------|---------------|
| @e.walmart.ca | 45 | Subdomain: @e. |
| @marketing.bestbuy.ca | 23 | Subdomain: @marketing. |

### Medium-Confidence (Needs Review)
| Domain | Count | Sample Subject | Your Decision |
|--------|-------|----------------|---------------|
| @noreply.github.com | 12 | "Security alert" | KEEP / FILTER |
| @hello.notion.com | 5 | "Tips for..." | KEEP / FILTER |

### Uncategorized (Needs Review)
| Domain | Count | Sample Subject | Your Decision |
|--------|-------|----------------|---------------|
| @randomdomain.com | 3 | "Check this out" | KEEP / FILTER |
```

---

## Phase 3: Time-Based Sweep

Scan date ranges to catch emails missed by pattern matching.

**Date ranges (most recent first):**
```python
DATE_RANGES = [
    "in:inbox after:2025/01/01",
    "in:inbox after:2024/07/01 before:2025/01/01",
    "in:inbox after:2024/01/01 before:2024/07/01",
    "in:inbox after:2023/07/01 before:2024/01/01",
    "in:inbox after:2023/01/01 before:2023/07/01",
    # Continue back as needed
]
```

**For each range:**
1. Search and fetch metadata
2. Extract domains NOT already in results
3. Present new domains for classification
4. Update progress

---

## File Formats

### inbox-audit-progress.json

```json
{
  "started": "2025-12-09T18:00:00Z",
  "last_updated": "2025-12-09T18:30:00Z",
  "status": "in_progress",
  "current_phase": 1,
  "account": "richard.stock@gmail.com",

  "phase1": {
    "searches_completed": ["unsubscribe", "noreply"],
    "searches_pending": ["newsletter", "promo"],
    "emails_found": 234
  },

  "phase2": {
    "domains_processed": 45,
    "spam_domains": 23,
    "keep_domains": 12,
    "pending_review": 10
  },

  "phase3": {
    "ranges_completed": ["2025-Q1"],
    "ranges_pending": ["2024-H2", "2024-H1"],
    "new_domains_found": 5
  },

  "totals": {
    "unique_domains": 156,
    "spam_identified": 89,
    "to_keep": 67
  }
}
```

### inbox-audit-results.md

```markdown
# Inbox Audit Results
**Generated:** 2025-12-09
**Account:** richard.stock@gmail.com

## Summary
| Metric | Count |
|--------|-------|
| Total domains found | X |
| Spam domains | Y |
| Domains to keep | Z |

---

## Phase 1 Results
[Accumulated findings from each search]

---

## Phase 2 Analysis
[Domain groupings and classifications]

---

## Phase 3 Sweep
[Additional domains found]

---

## User Decisions
[Record of KEEP/FILTER decisions]

---

## Recommended Actions
1. Create filters for X domains
2. Trash Y existing emails
3. Add Z to exceptions list
```

---

## User Interaction

### After Each Phase
```
## Phase 1 Complete

Scanned 11 spam patterns.
Found 456 potential spam emails across 78 domains.

Progress saved to inbox-audit-progress.json
Results appended to inbox-audit-results.md

Continue to Phase 2 (Domain Analysis)? [Y/n]
```

### After All Phases
```
## Audit Complete

### Summary
- Domains identified: 156
- Recommended for filtering: 89
- Recommended to keep: 67

### Next Steps
1. Review results in inbox-audit-results.md
2. Mark domains as KEEP or FILTER
3. Run /email-wizard to create filters

Ready to review domains? [Y/n]
```

---

## Important Notes

### Exceptions Handling
- **ALWAYS** check `data/exceptions.json` before flagging as spam
- If sender is in exceptions → Skip entirely, don't include in results
- User explicitly chose to keep these

### Conservative Mode
- **DO NOT auto-filter anything**
- Present ALL findings for user review
- User makes final decision on every domain
- Only create filters after explicit approval

### Resume Capability
- Progress is saved after every batch
- If interrupted, `/inbox-audit --resume` continues from last point
- Never lose progress, never repeat work

### Token Discipline
- Maximum 100 emails searched per query
- Maximum 25 emails fetched per batch (4 batches max)
- Write to file immediately, don't accumulate in context
- ~5,700 tokens per iteration budget

---

## Quick Reference

| Phase | Purpose | Output |
|-------|---------|--------|
| 1 | Find spam candidates via patterns | List of domains by search type |
| 2 | Analyze and group domains | Categorized domain list for review |
| 3 | Sweep by date to catch stragglers | Additional uncategorized domains |

**Goal:** After audit, user is confident ALL remaining inbox emails are legitimate.
