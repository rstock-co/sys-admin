---
argument-hint: "[email-address] [--spam-only]"
description: Run the Email Wizard to scan, categorize, and organize inbox emails
---

# Email Wizard

Automated email management - scans inbox, categorizes emails, suggests responses, filters spam.

---

## ⛔ CRITICAL: CONTEXT WINDOW PROTECTION ⛔

**STOP. READ THIS BEFORE EXECUTING ANYTHING.**

**NEVER use `format="full"` when batch-fetching emails.** This will return ~100k tokens of HTML garbage and destroy the context window.

**ALWAYS use `format="metadata"`** - From/Subject/Date headers are sufficient for categorization.

```python
# ✅ CORRECT
get_gmail_messages_content_batch(..., format="metadata")

# ❌ FORBIDDEN - WILL BLOW UP CONTEXT
get_gmail_messages_content_batch(..., format="full")
```

**Only fetch full content for individual emails when user wants to read or respond.**

---

## Usage

```bash
/email-wizard                              # Scan richard.stock@gmail.com (default)
/email-wizard rebeca.stock@gmail.com       # Scan specific account
/email-wizard --spam-only                  # Only run spam detection
```

**Email account:** $ARGUMENTS (default: richard.stock@gmail.com)

---

## Instructions

**FIRST:** Load the email-wizard skill for full documentation and data files.

### Step 1: Parse Arguments

- If `$ARGUMENTS` contains an email address, use it
- If `$ARGUMENTS` contains `--spam-only`, only run spam section
- Default: `richard.stock@gmail.com`, full wizard

### Step 2: Load Data Files

Read the wizard's persistent data from `.claude/skills/email-wizard/data/`:

```
registry.json         - Last run timestamp
legitimate-entities.json - Trusted senders
routing-rules.json    - Label routing rules
exceptions.json       - Newsletters to keep
```

### Step 3: Calculate Date Range

From `registry.json`:
- If `last_run` exists: search emails after that date
- If null (first run): search `newer_than:7d`

### Step 4: Search Inbox

```python
mcp__google_workspace__search_gmail_messages(
    query="in:inbox after:YYYY/MM/DD",  # or newer_than:7d
    user_google_email="<email>",
    page_size=100
)
```

**⛔ Then fetch METADATA ONLY (never full content for batch!):**

```python
# ✅ CORRECT - Metadata only
mcp__google_workspace__get_gmail_messages_content_batch(
    message_ids=[...],
    user_google_email="<email>",
    format="metadata"  # <-- MANDATORY
)
```

### Step 5: Categorize & Present

For each email, categorize into sections and present to user:

---

## Output Sections

### 1. Real Mail from Humans/Organizations

Emails requiring personal response. For each:
- Show sender, subject, preview
- Provide suggested response draft
- Offer to create draft reply

### 2. Real Notifications

Legitimate automated notifications from trusted entities.
- Cross-reference with `legitimate-entities.json`
- Show in table format
- Ask if any new senders should be added to trusted list

### 3. Calendar Events & Reminders

Emails containing events/meetings.
- Parse date, time, location
- Offer to add to Google Calendar
- Ask which calendar to use

### 4. Routing & Labeling

Emails that should be auto-organized.
- Check against `routing-rules.json`
- Suggest new labels for unrouted senders
- Offer to create labels and filters

### 5. Spam for Filtering/Deletion

Unwanted marketing/promotional emails.
- Check against `exceptions.json` (exclude kept newsletters)
- Group by domain
- Show display name vs actual sender (catch spoofing)
- For each spam domain:
  1. Create Gmail filter (auto-trash future emails)
  2. Trash existing emails from that sender
- Ask user to confirm before each action
- Offer to add any to exceptions list

---

## Step 6: Update Registry

After processing, update `data/registry.json`:

```json
{
  "last_run": "2025-12-09T10:30:00Z",
  "runs": [
    {"date": "2025-12-09T10:30:00Z", "emails_processed": 45, "spam_filtered": 12}
  ]
}
```

---

## Final Summary

Report back:
- Emails scanned since last run
- Breakdown by category
- Filters created
- Emails trashed
- Labels applied
- Data files updated

---

## Important Notes

### ⛔ Context Window Protection (CRITICAL)

- **NEVER use `format="full"` for batch email fetching**
- **ALWAYS use `format="metadata"` for categorization**
- Full HTML content = ~1000 tokens per email = context explosion
- Metadata = ~50 tokens per email = safe for 100+ emails
- Only fetch full content for INDIVIDUAL emails when user needs to read/respond

### Spam Detection

- **Check ACTUAL From address** - Spammers use fake display names
- **Filter by domain** - `@domain.com` catches all from that sender
- **Filters only affect future emails** - Must trash existing separately
- **Subdomains are different** - `@mail.example.com` ≠ `@example.com`

### Tool Selection

- **Use MCP for**: Search, read, filters, calendar, labels
- **Use Himalaya for**: Fast bulk move/delete (different message IDs!)

### Data Persistence

All wizard memory is stored in JSON files under `data/`:
- Update these files as user makes decisions
- Files persist between sessions
- First key in registry.json is always most recent run
