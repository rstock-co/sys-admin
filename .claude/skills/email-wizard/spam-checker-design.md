# Spam Checker Design Document

## Problem Statement

User has ~8,500 emails in inbox. Need to scan ALL of them for spam with:
- Minimal token usage (can't load 8,500 emails into context)
- Persistent progress (can resume if interrupted)
- High confidence that remaining emails after cleanup are legitimate

## Constraints

### MCP Tool Limits
- `search_gmail_messages`: max 100 results per query, no pagination token
- `get_gmail_messages_content_batch`: max 25 messages, ~50 tokens per email with `format="metadata"`
- No way to get just sender/subject without the batch fetch

### Token Math (Why Naive Approach Fails)
```
8,500 emails × 50 tokens/email = 425,000 tokens
Context limit = 200,000 tokens
```
**Cannot scan all emails in a single session.**

### Solution: Targeted Scans + File Accumulation

Instead of scanning every email, use Gmail's search to find spam candidates, then process in batches with immediate file persistence.

---

## Command Design

### Name: `/inbox-audit`

**Rationale:** "spam-checker" implies only spam detection. "inbox-audit" better describes the goal: audit entire inbox to ensure everything remaining is legitimate.

### Alternative Names Considered:
- `/spam-sweep` - Too narrow
- `/inbox-cleanup` - Implies automatic deletion
- `/email-audit` - Good but less specific
- `/inbox-audit` - ✅ Clear purpose, implies thoroughness

---

## Architecture

### Phase 1: Quick Win Scans (High-Confidence Spam)

Use Gmail search operators to find emails with strong spam indicators:

```python
SPAM_INDICATORS = [
    "in:inbox list:*",           # Mailing lists (has List-Unsubscribe header)
    "in:inbox unsubscribe",      # Contains "unsubscribe" in body
    "in:inbox from:noreply@",    # No-reply senders
    "in:inbox from:no-reply@",   # No-reply variant
    "in:inbox from:newsletter@", # Newsletter senders
    "in:inbox from:promo@",      # Promo senders
    "in:inbox from:marketing@",  # Marketing senders
    "in:inbox from:deals@",      # Deals senders
    "in:inbox from:offers@",     # Offers senders
    "in:inbox from:info@",       # Generic info@ (often spam)
    "in:inbox from:hello@",      # Generic hello@ (often marketing)
    "in:inbox from:support@",    # Could be spam, needs review
]
```

**Why this works:**
- Each search returns max 100 results
- Can run multiple searches efficiently
- Gmail handles the heavy lifting
- Most spam has these patterns

### Phase 2: Domain Analysis

For emails found, extract and group by domain:
1. Fetch metadata in batches of 25
2. Parse sender email to get domain
3. Group domains with counts
4. Write to file immediately (don't hold in context)

### Phase 3: Time-Based Sweep (Catch Stragglers)

For emails NOT caught by pattern searches, sweep by date range:

```python
DATE_RANGES = [
    "in:inbox after:2025/01/01 before:2025/04/01",
    "in:inbox after:2024/10/01 before:2025/01/01",
    "in:inbox after:2024/07/01 before:2024/10/01",
    "in:inbox after:2024/04/01 before:2024/07/01",
    "in:inbox after:2024/01/01 before:2024/04/01",
    # ... go back further as needed
]
```

**Token-efficient approach:**
- Process one date range at a time
- Write findings immediately
- Don't keep all results in context

---

## File Structure

### Output File: `inbox-audit-results.md`

```markdown
# Inbox Audit Results
**Generated:** 2025-12-09T18:30:00Z
**Account:** richard.stock@gmail.com

## Summary
| Metric | Count |
|--------|-------|
| Total inbox (estimated) | 8,500 |
| Spam domains identified | X |
| Emails to filter | Y |
| Already have filters | Z |

---

## High-Confidence Spam Domains

These domains have clear marketing/spam patterns. Safe to auto-filter.

| Domain | Count | Sample Sender | Sample Subject |
|--------|-------|---------------|----------------|
| @marketing.example.com | 45 | promo@marketing.example.com | "50% off today!" |
| @newsletters.foo.com | 23 | news@newsletters.foo.com | "Weekly digest" |

### Recommended Filters
```
@marketing.example.com → delete
@newsletters.foo.com → delete
```

---

## Medium-Confidence (Needs Review)

Automated senders that MIGHT be legitimate. Review before filtering.

| Sender | Domain | Count | Sample Subject | Recommendation |
|--------|--------|-------|----------------|----------------|
| noreply@bank.com | bank.com | 12 | "Statement ready" | KEEP |
| hello@startup.io | startup.io | 5 | "Check this out" | FILTER |

---

## Unique Senders Summary

All unique sender domains found, sorted by email count:

| Domain | Email Count | Has Filter? |
|--------|-------------|-------------|
| @amazon.ca | 234 | Partial |
| @gmail.com | 156 | No |
| ... | ... | ... |

---

## Audit Progress

- [x] Phase 1: Quick win scans
- [x] Phase 2: Domain analysis
- [ ] Phase 3: Time-based sweep (2024-Q4)
- [ ] Phase 3: Time-based sweep (2024-Q3)
- ...
```

### Progress File: `inbox-audit-progress.json`

```json
{
  "started": "2025-12-09T18:00:00Z",
  "last_updated": "2025-12-09T18:30:00Z",
  "status": "in_progress",
  "phase": 2,
  "account": "richard.stock@gmail.com",

  "phase1_scans": {
    "completed": ["unsubscribe", "noreply", "newsletter"],
    "pending": ["promo", "marketing"],
    "emails_found": 1250
  },

  "phase2_domains": {
    "total_unique": 145,
    "processed": 89,
    "spam_domains": 34
  },

  "phase3_sweeps": {
    "completed_ranges": ["2025-Q1"],
    "pending_ranges": ["2024-Q4", "2024-Q3", "2024-Q2", "2024-Q1"],
    "current_range": "2024-Q4"
  },

  "totals": {
    "emails_scanned": 3400,
    "spam_identified": 890,
    "filters_recommended": 45
  }
}
```

**Why JSON for progress:**
- Machine-readable for resume capability
- Agent can parse and continue from last state
- Tracks exactly what's done vs pending

---

## Execution Flow

### Agent Behavior

```
1. Load progress file (or create if first run)
2. Check current phase
3. Execute next batch of work:
   - Fetch up to 100 message IDs via search
   - Fetch metadata in batches of 25 (max 4 calls)
   - Extract sender/domain/subject
   - Classify as spam/legitimate/needs-review
   - IMMEDIATELY append to results file
   - Update progress file
4. Report progress to user
5. If more work: ask user to continue or pause
6. If done: present summary and action options
```

### Token Budget Per Iteration

```
Search (100 IDs):        ~200 tokens
Metadata (100 emails):   ~5,000 tokens (4 batches × 25 × 50)
Processing/output:       ~500 tokens
─────────────────────────────────────
Total per iteration:     ~5,700 tokens
```

**With 200k context, can do ~30 iterations before needing to compact.**

For 8,500 emails:
- 8,500 / 100 = 85 iterations needed
- Will need ~3 sessions with compaction
- Progress file enables seamless resume

---

## Spam Classification Rules

### High-Confidence Spam (Auto-filter)

```python
HIGH_CONFIDENCE_SPAM = {
    "domain_patterns": [
        r"@.*marketing\.",
        r"@.*promo\.",
        r"@.*newsletter\.",
        r"@.*deals\.",
        r"@.*offers\.",
        r"@e\.",           # e.walmart.ca, e.costco.ca etc
        r"@mail\.",        # mail.company.com often marketing
        r"@news\.",        # news.company.com often marketing
    ],
    "sender_patterns": [
        r"^noreply@",
        r"^no-reply@",
        r"^newsletter@",
        r"^promo@",
        r"^marketing@",
        r"^deals@",
        r"^offers@",
        r"^hello@",
        r"^info@",
    ],
    "subject_patterns": [
        r"unsubscribe",
        r"\d+% off",
        r"sale ends",
        r"limited time",
        r"act now",
        r"don't miss",
        r"exclusive offer",
        r"free shipping",
    ]
}
```

### Legitimate Indicators (Never filter)

```python
LEGITIMATE_INDICATORS = {
    "domains": [
        # Banking
        "@bmo.com", "@td.com", "@scotiabank.com", "@rbc.com",
        # Government
        "@canada.ca", "@cra-arc.gc.ca",
        # Known services user wants
        "@interac.ca", "@amazon.ca",  # Order confirmations only
    ],
    "sender_patterns": [
        # Personal emails (real people)
        r"^[a-z]+\.[a-z]+@",  # firstname.lastname@
        r"^[a-z]+[0-9]*@gmail\.com",  # Personal gmail
    ]
}
```

### Needs Review (Present to User)

Everything that doesn't clearly match spam or legitimate patterns.

---

## User Interaction Points

### During Scan
```
Scanning inbox... Phase 1 (Quick Wins)
├── [✓] Unsubscribe emails: 234 found
├── [✓] No-reply senders: 89 found
├── [→] Newsletter senders: scanning...
└── [ ] Promo senders: pending

Progress: 323 spam candidates, 45 unique domains
Continue scanning? [Y/n]
```

### After Scan Complete
```
## Inbox Audit Complete

Found 1,247 potential spam emails across 78 domains.

### Recommended Actions:

1. **Create filters for 45 high-confidence spam domains**
   Will auto-delete future emails from these senders.

2. **Review 23 medium-confidence domains**
   May include legitimate senders - need your input.

3. **Trash 1,102 existing spam emails**
   Moves identified spam to trash (recoverable for 30 days).

Which action? [1/2/3/all/none]
```

---

## Slash Command Definition

### File: `.claude/commands/inbox-audit.md`

```markdown
---
argument-hint: "[--resume] [--phase=1|2|3]"
description: Deep audit of inbox to identify and filter all spam
---

# Inbox Audit

Comprehensive inbox scan to identify spam and ensure all remaining emails are legitimate.

## ⛔ CRITICAL: TOKEN EFFICIENCY ⛔

This command scans thousands of emails. You MUST:
1. Use `format="metadata"` for ALL batch fetches
2. Write results to file IMMEDIATELY after each batch
3. Track progress in `inbox-audit-progress.json`
4. Never hold more than 100 emails in context at once

## Usage

/inbox-audit              # Start new audit
/inbox-audit --resume     # Continue from last progress
/inbox-audit --phase=2    # Jump to specific phase

## Execution

1. Load `data/inbox-audit-progress.json` (create if missing)
2. Execute current phase
3. Write results to `data/inbox-audit-results.md` after EACH batch
4. Update progress file after EACH batch
5. Report to user and ask to continue

## Phases

### Phase 1: Quick Win Scans
Search for emails matching spam patterns (unsubscribe, noreply, etc.)

### Phase 2: Domain Analysis
Group found emails by domain, classify spam vs legitimate

### Phase 3: Time-Based Sweep
Scan date ranges to catch emails missed by pattern matching

## Output Files

- `data/inbox-audit-results.md` - Human-readable findings
- `data/inbox-audit-progress.json` - Machine-readable progress
```

---

## SKILL.md Addition

Add this section to the existing email-wizard SKILL.md:

```markdown
---

## Inbox Audit Mode

For deep inbox cleaning, use `/inbox-audit` command.

### Key Differences from Regular Wizard

| Feature | /email-wizard | /inbox-audit |
|---------|---------------|--------------|
| Scope | Since last run | Entire inbox |
| Token usage | ~5-10k | Managed across sessions |
| Progress | Single run | Resumable via file |
| Output | In context | Written to files |

### Token Management

Inbox audit processes thousands of emails. To avoid context explosion:

1. **Batch size:** 100 emails searched, 25 fetched at a time
2. **Immediate persistence:** Write to file after each batch
3. **Progress tracking:** JSON file enables resume
4. **Session breaks:** May require multiple sessions for large inboxes

### Files Created

| File | Purpose |
|------|---------|
| `data/inbox-audit-results.md` | Findings and recommendations |
| `data/inbox-audit-progress.json` | Resume state |
```

---

## Implementation Checklist

- [ ] Create `/inbox-audit` slash command
- [ ] Add inbox audit section to SKILL.md
- [ ] Create initial `inbox-audit-progress.json` template
- [ ] Implement Phase 1 spam pattern searches
- [ ] Implement Phase 2 domain analysis
- [ ] Implement Phase 3 time-based sweep
- [ ] Add resume capability
- [ ] Add filter creation from results
- [ ] Add bulk trash capability

---

## Open Questions for User

1. **Session handling:** Should the command automatically continue until done, or pause after each phase for approval?

2. **Exceptions:** Should it load `exceptions.json` from email-wizard to skip known-good senders?

3. **Aggressiveness:** How aggressive on auto-classification?
   - Conservative: Present more for review
   - Aggressive: Auto-classify more, faster cleanup

4. **Existing filters:** Should it check existing filters to avoid duplicates?
