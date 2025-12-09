---
name: email-wizard
description: Automated email management wizard. Scans inbox since last run, categorizes emails (real mail, notifications, calendar events, spam), suggests responses, creates filters, and maintains organization. Use when user asks about emails, inbox cleanup, or runs /email-wizard.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__google_workspace__search_gmail_messages, mcp__google_workspace__get_gmail_message_content, mcp__google_workspace__get_gmail_messages_content_batch, mcp__google_workspace__get_gmail_thread_content, mcp__google_workspace__send_gmail_message, mcp__google_workspace__draft_gmail_message, mcp__google_workspace__list_gmail_labels, mcp__google_workspace__manage_gmail_label, mcp__google_workspace__modify_gmail_message_labels, mcp__google_workspace__batch_modify_gmail_message_labels, mcp__google_workspace__list_gmail_filters, mcp__google_workspace__create_gmail_filter, mcp__google_workspace__delete_gmail_filter, mcp__google_workspace__get_events, mcp__google_workspace__create_event
---

# Email Wizard

Automated email management system that scans, categorizes, and organizes your inbox.

---

## ⛔ CRITICAL: CONTEXT WINDOW PROTECTION ⛔

**READ THIS FIRST. FAILURE TO COMPLY WILL BLOW UP THE 200K CONTEXT WINDOW.**

### The Problem

Fetching full email content (`format="full"`) for 100 emails returns ~100k tokens of HTML garbage. This will:
1. Fill the context window in one tool call
2. Trigger auto-compaction
3. Lose all progress and confuse the agent

### The Solution

**ALWAYS use `format="metadata"` when batch-fetching emails.**

Metadata (From, Subject, Date) is sufficient for:
- Categorizing emails (spam vs real mail)
- Identifying senders by domain
- Detecting marketing patterns

**ONLY fetch full content for INDIVIDUAL emails when:**
- User wants to read a specific email
- You need to draft a response
- You need calendar event details

### Correct Pattern

```python
# ✅ CORRECT - Metadata only for categorization
mcp__google_workspace__get_gmail_messages_content_batch(
    message_ids=[...],
    user_google_email="richard.stock@gmail.com",
    format="metadata"  # <-- ALWAYS METADATA FOR BATCH
)

# ✅ CORRECT - Full content for ONE email when needed
mcp__google_workspace__get_gmail_message_content(
    message_id="19af...",
    user_google_email="richard.stock@gmail.com"
    # Single message, full content is fine
)
```

### FORBIDDEN Pattern

```python
# ❌ FORBIDDEN - NEVER DO THIS
mcp__google_workspace__get_gmail_messages_content_batch(
    message_ids=[...100 IDs...],
    format="full"  # <-- THIS WILL DESTROY CONTEXT
)
```

### Token Budget

| Format | Per Email | 100 Emails |
|--------|-----------|------------|
| `metadata` | ~50 tokens | ~5k tokens ✅ |
| `full` | ~1000 tokens | ~100k tokens ❌ |

**Rule: NEVER exceed ~10k tokens for email content in a single wizard run.**

---

## Overview

The Email Wizard:
1. **Tracks runs** - Remembers when it last ran, only processes new emails
2. **Categorizes emails** into actionable sections
3. **Learns your preferences** via persistent data files
4. **Creates filters** to prevent future spam
5. **Maintains organization** through labels and routing

## Data Files

All persistent data stored in `data/` directory:

| File | Purpose |
|------|---------|
| `registry.json` | Last run timestamp (first key for fast access) |
| `legitimate-entities.json` | Trusted senders for "real notifications" |
| `routing-rules.json` | Label routing rules by sender |
| `exceptions.json` | Newsletters/senders to keep (not spam) |

## Default Account

**Unless specified, always use `richard.stock@gmail.com`** for all operations.

| Account | Email | Notes |
|---------|-------|-------|
| Default | richard.stock@gmail.com | Primary account |
| Secondary | rebeca.stock@gmail.com | Must explicitly request |

---

## Wizard Execution Flow

### Step 1: Check Registry

Read `data/registry.json` to get last run timestamp:

```python
# Read registry
registry = read_file("data/registry.json")
last_run = registry["last_run"]  # ISO timestamp or null
```

If `last_run` is null, this is the first run - scan last 7 days.

### Step 2: Search New Emails

Search for emails since last run:

```python
# Calculate date range
if last_run:
    query = f"in:inbox after:{last_run_date}"
else:
    query = "in:inbox newer_than:7d"

mcp__google_workspace__search_gmail_messages(
    query=query,
    user_google_email="richard.stock@gmail.com",
    page_size=100
)
```

**⛔ CRITICAL: Fetch METADATA ONLY for categorization:**

```python
# ✅ CORRECT - Metadata only (From, Subject, Date)
mcp__google_workspace__get_gmail_messages_content_batch(
    message_ids=[...],
    user_google_email="richard.stock@gmail.com",
    format="metadata"  # <-- MANDATORY: Never use "full" for batch!
)
```

**Why metadata is sufficient:**
- From header → Identify sender domain for spam detection
- Subject → Categorize email type
- Date → Sort chronologically

**Only fetch full content when user requests to read/respond to a specific email.**

### Step 3: Categorize Emails

Process each email and assign to one of these categories:

---

## Output Categories

### 1. Real Mail from Humans/Organizations

**Criteria:** Personal emails requiring a response
- Direct emails from individuals (not automated)
- Business correspondence
- Support tickets/inquiries
- Invitations requiring RSVP

**Output format:**
```markdown
## Real Mail Requiring Response

### From: John Smith <john@company.com>
**Subject:** Project Proposal Follow-up
**Received:** Dec 8, 2025 3:45 PM
**Preview:** Hi Richard, I wanted to follow up on our discussion about...

**Suggested Response:**
> Hi John,
>
> Thank you for following up. [Acknowledge their point]. [Your response].
>
> Best regards,
> Richard
```

**Actions:** Offer to draft replies

---

### 2. Real Notifications

**Criteria:** Legitimate automated notifications from trusted entities
- Order confirmations, shipping updates
- Banking alerts, security notifications
- Service status updates
- Account activity alerts

**Source:** Check against `data/legitimate-entities.json`

**Output format:**
```markdown
## Real Notifications

| From | Subject | Summary |
|------|---------|---------|
| Amazon | Your order has shipped | Package arriving Dec 10 |
| TD Bank | Account alert | Login from new device |
| Dragonfly | Deploy successful | Production deploy completed |
```

**Actions:**
- Ask if any should be added to legitimate-entities.json
- Suggest routing labels

---

### 3. Calendar Events & Reminders

**Criteria:** Emails containing events/meetings
- Webinar invitations
- Conference confirmations
- Meeting reminders
- Event RSVPs

**Detection patterns:**
- Date/time mentions in future
- "Join meeting" / "RSVP" / "Add to calendar" links
- iCal attachments

**Output format:**
```markdown
## Calendar Events

### Webinar: AI in Production
**When:** Thursday, Dec 12, 2025 at 3:00 PM EST
**Duration:** 1 hour
**From:** TechConf <events@techconf.com>

Add to calendar? [Yes/No] Which calendar? [Primary/Work/...]
```

**Actions:**
- Offer to create calendar events via MCP
- Parse event details automatically

---

### 4. Routing & Labeling

**Criteria:** Emails that should be auto-organized
- Recurring senders that belong in specific folders
- Categories of emails (receipts, newsletters, alerts)

**Source:** Check against `data/routing-rules.json`

**Output format:**
```markdown
## Suggested Routing

### New Senders (not yet routed)
| Sender | Domain | Suggested Label |
|--------|--------|-----------------|
| GitHub | @github.com | Development/GitHub |
| Stripe | @stripe.com | Finance/Payments |

### Apply routing? [Yes/No/Customize]
```

**Actions:**
- Create labels if they don't exist
- Apply labels to messages
- Update routing-rules.json
- Create filters for future emails

---

### 5. Spam for Filtering/Deletion

**Criteria:** Unwanted emails
- Marketing/promotional emails
- Newsletters you didn't subscribe to
- Phishing attempts
- Political spam

**Exclusions:** Check `data/exceptions.json` for newsletters to keep

**Output format:**
```markdown
## Spam Detected

| Sender | Domain | Count | Display Name |
|--------|--------|-------|--------------|
| @finopulses.com | finopulses.com | 3 | "Lendify Loans" |
| @marketing.linkedin.com | linkedin.com | 5 | "LinkedIn" |
| @news.retailer.com | retailer.com | 2 | "Daily Deals" |

**Note:** The following are in your exceptions list (kept):
- newsletter@techweekly.com (Tech Weekly)

### Actions:
1. [Filter & Delete All] - Create filters and trash existing
2. [Review Each] - Go through one by one
3. [Keep Some] - Select which to add to exceptions
```

**Actions:**
- Create Gmail filters for domains (auto-trash future emails)
- Batch trash existing emails
- Update exceptions.json for keepers

---

## Spam Detection Logic

### Spam Indicators

**High confidence spam:**
- Sender domain doesn't match display name
- Unsubscribe links in every email
- Marketing/promotional language patterns
- Sender in common spam domains list

**Check the ACTUAL From address:**
```
Display: "Lendify Financial"
Actual: noreply@finopulses.com  <-- This is what matters
```

### Creating Filters

Always filter by DOMAIN (not specific address):

```python
# Create filter
mcp__google_workspace__create_gmail_filter(
    user_google_email="richard.stock@gmail.com",
    from_address="@spam-domain.com",  # Domain filter
    delete=True
)

# Search and trash existing
results = mcp__google_workspace__search_gmail_messages(
    query="from:@spam-domain.com in:inbox",
    user_google_email="richard.stock@gmail.com",
    page_size=100
)

# Batch trash
mcp__google_workspace__batch_modify_gmail_message_labels(
    message_ids=[...],
    add_label_ids=["TRASH"],
    remove_label_ids=["INBOX"],
    user_google_email="richard.stock@gmail.com"
)
```

### Filter vs Delete Workflow

1. **Create filter FIRST** (catches future emails)
2. **Then trash existing emails** (cleans current inbox)
3. **Update exceptions.json** if user wants to keep any

---

## Step 4: Update Registry

After processing, update registry with current timestamp:

```python
# Update registry.json
{
  "last_run": "2025-12-09T10:30:00Z",
  "runs": [
    {"date": "2025-12-09T10:30:00Z", "emails_processed": 45, "spam_filtered": 12},
    // ... previous runs (append to front for fast access)
  ]
}
```

---

## Tool Reference

### Google Workspace MCP (Primary)

Best for: Searching, reading content, filters, sending

See [docs/google-workspace-mcp/gmail.md](docs/google-workspace-mcp/gmail.md)

### Himalaya CLI (Bulk Operations)

Best for: Fast batch move/delete operations

See [docs/himalaya/commands.md](docs/himalaya/commands.md)

**CRITICAL:** Gmail API (MCP) and Himalaya use DIFFERENT message IDs - NOT interchangeable!

| Tool | ID Format | Example |
|------|-----------|---------|
| Gmail API (MCP) | Hex string | `19a82aa55f2a5f17` |
| Himalaya (IMAP) | Integer | `163926` |

**Rule:** Search and act with the SAME tool. Don't mix IDs.

### Gmail Folder Names

| Purpose | Name |
|---------|------|
| All emails | `[Gmail]/All Mail` |
| Trash | `[Gmail]/Trash` |
| Sent | `[Gmail]/Sent Mail` |
| Spam | `[Gmail]/Spam` |
| Inbox | `INBOX` |

---

## Quick Commands

### Run Full Wizard
```
/email-wizard
```

### Run for Specific Account
```
/email-wizard rebeca.stock@gmail.com
```

### Just Spam Cleanup
```
/email-wizard --spam-only
```

---

## Data File Management

### Adding Legitimate Entity

Edit `data/legitimate-entities.json`:

```json
{
  "entities": {
    "Amazon": {
      "keep": ["auto-confirm@amazon.ca", "shipment-tracking@amazon.ca"],
      "block": ["store-news@amazon.ca"]
    },
    "Your Bank": {
      "keep": ["@alerts.yourbank.com"],
      "block": ["@marketing.yourbank.com"]
    }
  }
}
```

### Adding Routing Rule

Edit `data/routing-rules.json`:

```json
{
  "rules": {
    "Finance/Banking": ["@td.com", "@scotiabank.com"],
    "Shopping/Orders": ["auto-confirm@amazon.ca"],
    "Development/GitHub": ["@github.com"]
  }
}
```

### Adding Exception (Keep Newsletter)

Edit `data/exceptions.json`:

```json
{
  "keep": [
    {"address": "newsletter@techweekly.com", "name": "Tech Weekly", "reason": "Good industry news"},
    {"address": "@substack.com", "name": "Substack", "reason": "Selected subscriptions"}
  ]
}
```

---

## Inbox Audit Mode

For deep inbox cleaning (thousands of emails), use `/inbox-audit` command.

### Key Differences from Regular Wizard

| Feature | /email-wizard | /inbox-audit |
|---------|---------------|--------------|
| Scope | Since last run | Entire inbox |
| Token usage | ~5-10k | Managed across sessions |
| Progress | Single run | Resumable via file |
| Output | In context | Written to files |
| User control | Automated categories | Manual approval per domain |

### Three-Phase Approach

1. **Phase 1: Quick Win Scans** - Search spam patterns (unsubscribe, noreply, etc.)
2. **Phase 2: Domain Analysis** - Group and categorize domains for review
3. **Phase 3: Time-Based Sweep** - Date range scans to catch stragglers

### Token Management

Inbox audit processes thousands of emails. To avoid context explosion:

1. **Batch size:** 100 emails searched, 25 fetched at a time
2. **Immediate persistence:** Write to file after each batch
3. **Progress tracking:** JSON file enables resume
4. **Session breaks:** Pauses after each phase for user approval

### Files Created

| File | Purpose |
|------|---------|
| `data/inbox-audit-results.md` | Findings and recommendations |
| `data/inbox-audit-progress.json` | Resume state |

### Conservative Mode (Default)

The audit runs in **conservative mode**:
- NO auto-filtering - all domains presented for review
- User makes final decision on every domain
- Only creates filters after explicit approval
- Checks `exceptions.json` to skip known-good senders

---

## Tips

1. **First run takes longer** - No history, scans 7 days
2. **Run regularly** - Daily or every few days for best results
3. **Review spam carefully** - Some legitimate senders use bad patterns
4. **Domain filters are broad** - `@domain.com` catches all subdomains
5. **Exceptions persist** - Once added, newsletters won't be flagged again
